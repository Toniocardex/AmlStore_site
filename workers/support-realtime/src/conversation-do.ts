import { CONVERSATION_SCHEMA } from './local-schema';
import type { SupportRealtimeEnv } from './env';
import { createId, isPrefixedId } from '../../../support/shared/ids';
import { ChatProtocolError } from '../../../support/shared/errors';
import { CHAT_PROTOCOL_VERSION } from '../../../support/shared/protocol';
import { normalizePlainText, parseMessageSendCommand } from '../../../support/shared/schemas';
import { assertTransition, isConversationStatus, type ConversationStatus } from '../../../support/shared/lifecycle';
import { drainOutbox, scheduleOutbox } from './outbox';
import { emitMetric } from './observability';

interface CreateConversationInput {
    conversationId: string;
    visitorId: string;
    clientMessageId: string;
    body: string;
    contactName: string | null;
    contactEmail: string | null;
    contactEmailLookupHash: string | null;
    contactVerifiedAt: number | null;
    pagePath: string | null;
    productId: string | null;
    orderId: string | null;
    locale: string | null;
    countryCode: string | null;
    createdAt: number;
}

interface SendMessageInput {
    conversationId: string;
    visitorId: string;
    clientMessageId: string;
    body: string;
    createdAt: number;
}

interface MessageRow {
    [key: string]: SqlStorageValue;
    seq: number;
    id: string;
    client_message_id: string;
    sender_type: string;
    sender_id: string;
    body_text: string;
    created_at: number;
}

interface SocketAttachment {
    role: 'visitor';
    visitorId: string;
    participantKey: string;
    lastTypingAt: number;
}

function json(data: unknown, status = 200): Response {
    return Response.json(data, { status, headers: { 'Cache-Control': 'no-store' } });
}

export class ConversationDurableObject {
    readonly ctx: DurableObjectState;
    readonly env: SupportRealtimeEnv;
    private purged = false;

    constructor(ctx: DurableObjectState, env: SupportRealtimeEnv) {
        this.ctx = ctx;
        this.env = env;
        this.ctx.blockConcurrencyWhile(async () => {
            this.ctx.storage.sql.exec(CONVERSATION_SCHEMA);
        });
    }

    async fetch(request: Request): Promise<Response> {
        const url = new URL(request.url);
        if (request.method === 'GET' && url.pathname === '/internal/health') {
            return Response.json({ ok: true, component: 'conversation' });
        }
        try {
            if (request.method === 'GET' && url.pathname === '/internal/conversations/ws') {
                return this.acceptGuestSocket(request);
            }
            if (request.method === 'POST' && url.pathname === '/internal/conversations/create') {
                return await this.createConversation(await request.json());
            }
            if (request.method === 'POST' && url.pathname === '/internal/conversations/detail') {
                return this.getDetail(await request.json());
            }
            if (request.method === 'POST' && url.pathname === '/internal/conversations/messages') {
                return this.getMessages(await request.json());
            }
            if (request.method === 'POST' && url.pathname === '/internal/conversations/messages/send') {
                return await this.sendMessage(await request.json());
            }
            if (request.method === 'POST' && url.pathname === '/internal/conversations/read') {
                return await this.markRead(await request.json());
            }
            if (request.method === 'POST' && url.pathname === '/internal/admin/conversations/detail') {
                return this.getAdminDetail(await request.json());
            }
            if (request.method === 'POST' && url.pathname === '/internal/admin/conversations/messages') {
                return this.getAdminMessages(await request.json());
            }
            if (request.method === 'POST' && url.pathname === '/internal/admin/conversations/messages/send') {
                return await this.sendOperatorMessage(await request.json());
            }
            if (request.method === 'POST' && url.pathname === '/internal/admin/conversations/state') {
                return await this.updateConversationState(await request.json());
            }
            if (request.method === 'POST' && url.pathname === '/internal/admin/conversations/assignment') {
                return await this.updateAssignment(await request.json());
            }
            if (request.method === 'POST' && url.pathname === '/internal/admin/conversations/read') {
                return await this.markOperatorRead(await request.json());
            }
            if (request.method === 'POST' && url.pathname === '/internal/admin/conversations/export') {
                return this.getAdminExport(await request.json());
            }
            if (request.method === 'POST' && url.pathname === '/internal/system/conversations/state') {
                const input = await request.json<Record<string, unknown>>();
                return await this.updateConversationState({ ...input, operatorId: 'op_system' });
            }
            if (request.method === 'POST' && url.pathname === '/internal/system/conversations/purge/request') {
                return await this.requestPurge(await request.json());
            }
            if (request.method === 'POST' && url.pathname === '/internal/system/conversations/purge/finalize') {
                return await this.finalizePurge(await request.json());
            }
            if (request.method === 'POST' && url.pathname === '/internal/system/conversations/purge/cancel') {
                return await this.cancelPurge(await request.json());
            }
        } catch (error) {
            if (error instanceof ChatProtocolError) {
                return json({
                    v: CHAT_PROTOCOL_VERSION,
                    type: 'error',
                    error: { code: error.code, message: error.message },
                }, error.status);
            }
            console.error('[conversation-do] request failed', {
                error: error instanceof Error ? error.message : String(error),
            });
            emitMetric('chat_error_total', 1, { component: 'conversation-do' });
            return json({ error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } }, 500);
        }
        return Response.json({ error: 'Not found' }, { status: 404 });
    }

    async alarm(): Promise<void> {
        await drainOutbox(this);
    }

    async webSocketMessage(socket: WebSocket, message: string | ArrayBuffer): Promise<void> {
        let requestId: string | undefined;
        try {
            if (typeof message !== 'string') {
                throw new ChatProtocolError('INVALID_PAYLOAD', 'Binary messages are not supported');
            }
            const raw = JSON.parse(message) as Record<string, unknown>;
            requestId = typeof raw.requestId === 'string' ? raw.requestId : undefined;
            const attachment = socket.deserializeAttachment() as SocketAttachment | null;
            if (!attachment || attachment.role !== 'visitor') {
                throw new ChatProtocolError('UNAUTHORIZED', 'Invalid socket identity', 401);
            }

            if (raw.type === 'message.send') {
                const command = parseMessageSendCommand(raw, Number(this.env.CHAT_MAX_MESSAGE_LENGTH || 4_000));
                if (command.conversationId !== this.stateValue('conversation_id')) {
                    throw new ChatProtocolError('NOT_FOUND', 'Conversation not found', 404);
                }
                const response = await this.sendMessage({
                    conversationId: command.conversationId,
                    visitorId: attachment.visitorId,
                    clientMessageId: command.payload.clientMessageId,
                    body: command.payload.body,
                    createdAt: Date.now(),
                });
                const event = await response.json<Record<string, unknown>>();
                if (!response.ok) {
                    socket.send(JSON.stringify({ ...event, requestId }));
                    return;
                }
                return;
            }

            if (raw.v === CHAT_PROTOCOL_VERSION && raw.type === 'message.read') {
                if (!isPrefixedId(raw.requestId, 'request')
                    || !isPrefixedId(raw.conversationId, 'conversation')) {
                    throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid message.read envelope');
                }
                const payload = raw.payload as Record<string, unknown> | null;
                const response = await this.markRead({
                    conversationId: raw.conversationId,
                    visitorId: attachment.visitorId,
                    lastReadSeq: payload?.lastReadSeq,
                    updatedAt: Date.now(),
                });
                const event = await response.json<Record<string, unknown>>();
                if (!response.ok) {
                    socket.send(JSON.stringify({ ...event, requestId }));
                    return;
                }
                return;
            }

            if (raw.v === CHAT_PROTOCOL_VERSION
                && (raw.type === 'typing.started' || raw.type === 'typing.stopped')) {
                if (!isPrefixedId(raw.requestId, 'request')
                    || !isPrefixedId(raw.conversationId, 'conversation')) {
                    throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid typing envelope');
                }
                if (raw.conversationId !== this.stateValue('conversation_id')) {
                    throw new ChatProtocolError('NOT_FOUND', 'Conversation not found', 404);
                }
                const now = Date.now();
                if (raw.type === 'typing.started' && now - attachment.lastTypingAt < 1_000) return;
                attachment.lastTypingAt = now;
                socket.serializeAttachment(attachment);
                this.broadcast({
                    v: CHAT_PROTOCOL_VERSION,
                    type: raw.type,
                    eventId: createId('event'),
                    conversationId: raw.conversationId,
                    serverTs: now,
                    payload: { participantType: 'visitor' },
                });
                return;
            }
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Unsupported command');
        } catch (error) {
            const known = error instanceof ChatProtocolError
                ? error
                : new ChatProtocolError('INVALID_PAYLOAD', 'Invalid realtime command');
            socket.send(JSON.stringify({
                v: CHAT_PROTOCOL_VERSION,
                type: 'error',
                ...(requestId ? { requestId } : {}),
                error: { code: known.code, message: known.message },
            }));
        }
    }

    webSocketClose(_socket: WebSocket, _code: number, _reason: string): void {
        // The runtime has already closed the hibernating socket.
    }

    private broadcast(event: unknown): void {
        const serialized = JSON.stringify(event);
        for (const socket of this.ctx.getWebSockets()) {
            try { socket.send(serialized); } catch { /* stale sockets are discarded by the runtime */ }
        }
    }

    private acceptGuestSocket(request: Request): Response {
        if (request.headers.get('Upgrade')?.toLowerCase() !== 'websocket') {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'WebSocket upgrade required', 426);
        }
        const url = new URL(request.url);
        const conversationId = url.searchParams.get('conversationId');
        const visitorId = url.searchParams.get('visitorId');
        if (!isPrefixedId(conversationId, 'conversation') || !isPrefixedId(visitorId, 'visitor')) {
            throw new ChatProtocolError('NOT_FOUND', 'Conversation not found', 404);
        }
        this.assertOwner({ conversationId, visitorId });
        const requestedSeq = Number(url.searchParams.get('lastKnownSeq') || 0);
        if (!Number.isInteger(requestedSeq) || requestedSeq < 0) {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid lastKnownSeq');
        }

        const pair = new WebSocketPair();
        const [client, server] = Object.values(pair) as [WebSocket, WebSocket];
        server.serializeAttachment({
            role: 'visitor',
            visitorId,
            participantKey: `visitor:${visitorId}`,
            lastTypingAt: 0,
        } satisfies SocketAttachment);
        this.ctx.acceptWebSocket(server, [`visitor:${visitorId}`]);
        emitMetric('chat_ws_connected', 1, { role: 'visitor' });
        if (requestedSeq > 0) emitMetric('chat_ws_reconnect_total', 1, { role: 'visitor' });

        const rows = this.ctx.storage.sql.exec<MessageRow & {
            event_id: string | null;
            projection_version: number | null;
        }>(`
            SELECT m.seq, m.id, m.client_message_id, m.sender_type, m.sender_id,
                   m.body_text, m.created_at, o.event_id, o.projection_version
            FROM messages m
            LEFT JOIN outbox o ON o.seq = m.seq AND o.event_type = 'message.created'
            WHERE m.seq > ?
            ORDER BY m.seq ASC
            LIMIT 101
        `, requestedSeq).toArray();
        for (const row of rows.slice(0, 100)) {
            server.send(JSON.stringify(this.messageEnvelope(
                row,
                row.projection_version || Number(this.stateValue('projection_version') || 0),
                row.event_id || createId('event'),
            )));
        }
        server.send(JSON.stringify({
            v: CHAT_PROTOCOL_VERSION,
            type: 'conversation.updated',
            eventId: createId('event'),
            conversationId,
            projectionVersion: Number(this.stateValue('projection_version') || 0),
            serverTs: Date.now(),
            payload: {
                status: this.stateValue('status'),
                lastSeq: rows.at(-1)?.seq || requestedSeq,
                catchUpTruncated: rows.length > 100,
            },
        }));
        return new Response(null, { status: 101, webSocket: client });
    }

    private stateValue(key: string): string | null {
        if (this.purged) return null;
        const row = this.ctx.storage.sql.exec<{ value: string }>(
            'SELECT value FROM conversation_local_state WHERE key = ?', key,
        ).toArray()[0];
        return row?.value ?? null;
    }

    private setLocalState(key: string, value: string): void {
        this.ctx.storage.sql.exec(
            'INSERT INTO conversation_local_state (key, value) VALUES (?, ?) '
                + 'ON CONFLICT(key) DO UPDATE SET value = excluded.value',
            key, value,
        );
    }

    private clearLocalState(key: string): void {
        this.ctx.storage.sql.exec('DELETE FROM conversation_local_state WHERE key = ?', key);
    }

    private assertOwner(input: Record<string, unknown>): void {
        const conversationId = this.stateValue('conversation_id');
        const visitorId = this.stateValue('visitor_id');
        if (!conversationId || input.conversationId !== conversationId) {
            throw new ChatProtocolError('NOT_FOUND', 'Conversation not found', 404);
        }
        if (!visitorId || input.visitorId !== visitorId) {
            // Do not reveal that the conversation exists.
            throw new ChatProtocolError('NOT_FOUND', 'Conversation not found', 404);
        }
    }

    private messageEnvelope(row: MessageRow, projectionVersion: number, eventId: string) {
        return {
            v: CHAT_PROTOCOL_VERSION,
            type: 'message.created',
            eventId,
            conversationId: this.stateValue('conversation_id'),
            seq: row.seq,
            projectionVersion,
            serverTs: row.created_at,
            payload: {
                messageId: row.id,
                clientMessageId: row.client_message_id,
                senderType: row.sender_type,
                body: row.body_text,
            },
        };
    }

    private consumeMessageRateLimit(participantKey: string, now: number): void {
        const windowStart = Math.floor(now / 60_000) * 60_000;
        const row = this.ctx.storage.sql.exec<{ window_start: number; message_count: number }>(`
            SELECT window_start, message_count
            FROM message_rate_limits WHERE participant_key = ?
        `, participantKey).toArray()[0];
        if (!row || row.window_start !== windowStart) {
            this.ctx.storage.sql.exec(`
                INSERT INTO message_rate_limits (participant_key, window_start, message_count)
                VALUES (?, ?, 1)
                ON CONFLICT(participant_key) DO UPDATE SET
                    window_start = excluded.window_start,
                    message_count = 1
            `, participantKey, windowStart);
            return;
        }
        if (row.message_count >= 20) {
            throw new ChatProtocolError('RATE_LIMITED', 'Too many messages; retry shortly', 429);
        }
        this.ctx.storage.sql.exec(`
            UPDATE message_rate_limits SET message_count = message_count + 1
            WHERE participant_key = ?
        `, participantKey);
    }

    private async createConversation(raw: unknown): Promise<Response> {
        const startedAt = Date.now();
        let created = false;
        if (!raw || typeof raw !== 'object') {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid create payload');
        }
        const input = raw as CreateConversationInput;
        if (!isPrefixedId(input.conversationId, 'conversation')
            || !isPrefixedId(input.visitorId, 'visitor')
            || !isPrefixedId(input.clientMessageId, 'message')) {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid conversation identity');
        }
        const body = normalizePlainText(input.body);
        if (!Number.isInteger(input.createdAt) || input.createdAt <= 0) {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid createdAt');
        }

        const result = this.ctx.storage.transactionSync(() => {
            const existingConversationId = this.stateValue('conversation_id');
            if (existingConversationId) {
                if (existingConversationId !== input.conversationId
                    || this.stateValue('visitor_id') !== input.visitorId) {
                    throw new ChatProtocolError('FORBIDDEN', 'Conversation identity mismatch', 403);
                }
                const existing = this.ctx.storage.sql.exec<MessageRow>(`
                    SELECT seq, id, client_message_id, sender_type, sender_id, body_text, created_at
                    FROM messages WHERE sender_id = ? AND client_message_id = ?
                `, input.visitorId, input.clientMessageId).toArray()[0];
                if (!existing) {
                    throw new ChatProtocolError('INVALID_PAYLOAD', 'Conversation is already initialized', 409);
                }
                const event = this.ctx.storage.sql.exec<{ event_id: string; projection_version: number }>(`
                    SELECT event_id, projection_version FROM outbox
                    WHERE event_type = 'message.created' AND seq = ? LIMIT 1
                `, existing.seq).toArray()[0];
                return this.messageEnvelope(existing, event?.projection_version || 1, event?.event_id || '');
            }

            const messageId = createId('message');
            created = true;
            const conversationEventId = createId('event');
            const messageEventId = createId('event');
            const projectionVersion = 1;
            const message = this.ctx.storage.sql.exec<MessageRow>(`
                INSERT INTO messages (
                    id, client_message_id, sender_type, sender_id,
                    message_type, body_text, created_at
                ) VALUES (?, ?, 'visitor', ?, 'text', ?, ?)
                RETURNING seq, id, client_message_id, sender_type, sender_id, body_text, created_at
            `, messageId, input.clientMessageId, input.visitorId, body, input.createdAt).one();

            const stateEntries: Array<[string, string]> = [
                ['conversation_id', input.conversationId],
                ['visitor_id', input.visitorId],
                ['status', 'OPEN'],
                ['projection_version', String(projectionVersion)],
                ['write_gate', 'OPEN'],
                ['metadata_json', JSON.stringify({
                    contactName: input.contactName,
                    contactEmail: input.contactEmail,
                    contactEmailLookupHash: input.contactEmailLookupHash,
                    contactVerifiedAt: input.contactVerifiedAt,
                    pagePath: input.pagePath,
                    productId: input.productId,
                    orderId: input.orderId,
                    locale: input.locale,
                    countryCode: input.countryCode,
                    createdAt: input.createdAt,
                })],
            ];
            for (const [key, value] of stateEntries) {
                this.ctx.storage.sql.exec(
                    'INSERT INTO conversation_local_state (key, value) VALUES (?, ?)', key, value,
                );
            }
            this.ctx.storage.sql.exec(`
                INSERT INTO participant_state (participant_key, last_read_seq, updated_at)
                VALUES (?, ?, ?)
            `, `visitor:${input.visitorId}`, message.seq, input.createdAt);
            this.ctx.storage.sql.exec(`
                INSERT INTO message_rate_limits (participant_key, window_start, message_count)
                VALUES (?, ?, 1)
            `, `visitor:${input.visitorId}`, Math.floor(input.createdAt / 60_000) * 60_000);

            const projectionPayload = JSON.stringify({
                conversationId: input.conversationId,
                visitorId: input.visitorId,
                contactName: input.contactName,
                contactEmail: input.contactEmail,
                contactEmailLookupHash: input.contactEmailLookupHash,
                contactVerifiedAt: input.contactVerifiedAt,
                locale: input.locale,
                countryCode: input.countryCode,
                productId: input.productId,
                orderId: input.orderId,
                pagePath: input.pagePath,
                messageId,
                body,
                createdAt: input.createdAt,
            });
            this.ctx.storage.sql.exec(`
                INSERT INTO outbox (
                    event_id, event_type, seq, projection_version,
                    payload_json, attempts, created_at
                ) VALUES (?, 'conversation.created', ?, ?, ?, 0, ?)
            `, conversationEventId, message.seq, projectionVersion, projectionPayload, input.createdAt);
            this.ctx.storage.sql.exec(`
                INSERT INTO outbox (
                    event_id, event_type, seq, projection_version,
                    payload_json, attempts, created_at
                ) VALUES (?, 'message.created', ?, ?, ?, 0, ?)
            `, messageEventId, message.seq, projectionVersion, JSON.stringify({
                conversationId: input.conversationId,
                senderType: 'visitor',
                body,
                createdAt: input.createdAt,
            }), input.createdAt);
            return this.messageEnvelope(message, projectionVersion, messageEventId);
        });

        await scheduleOutbox(this);
        this.ctx.waitUntil(drainOutbox(this));
        this.broadcast(result);
        if (created) {
            emitMetric('chat_conversation_created_total');
            emitMetric('chat_message_created_total', 1, { senderType: 'visitor' });
            emitMetric('chat_message_persistence_latency_ms', Date.now() - startedAt, { operation: 'create' });
        }
        return json(result, 201);
    }

    private async markRead(raw: unknown): Promise<Response> {
        if (!raw || typeof raw !== 'object') {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid read payload');
        }
        const input = raw as Record<string, unknown>;
        this.assertOwner(input);
        const requestedSeq = Number(input.lastReadSeq);
        const updatedAt = Number(input.updatedAt);
        if (!Number.isInteger(requestedSeq) || requestedSeq < 0
            || !Number.isInteger(updatedAt) || updatedAt <= 0) {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid read cursor');
        }
        const maxSeq = this.ctx.storage.sql.exec<{ max_seq: number }>(
            'SELECT COALESCE(MAX(seq), 0) AS max_seq FROM messages',
        ).one().max_seq;
        const lastReadSeq = Math.min(requestedSeq, maxSeq);
        const participantKey = `visitor:${String(input.visitorId)}`;
        const current = this.ctx.storage.sql.exec<{ last_read_seq: number }>(`
            SELECT last_read_seq FROM participant_state WHERE participant_key = ?
        `, participantKey).toArray()[0]?.last_read_seq || 0;
        if (lastReadSeq <= current) {
            return json({ ok: true, conversationId: input.conversationId, lastReadSeq: current });
        }
        const projectionVersion = Number(this.stateValue('projection_version') || 0) + 1;
        const eventId = createId('event');
        this.ctx.storage.transactionSync(() => {
            this.ctx.storage.sql.exec(`
                INSERT INTO participant_state (participant_key, last_read_seq, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(participant_key) DO UPDATE SET
                    last_read_seq = MAX(last_read_seq, excluded.last_read_seq),
                    updated_at = excluded.updated_at
            `, participantKey, lastReadSeq, updatedAt);
            this.ctx.storage.sql.exec(
                "UPDATE conversation_local_state SET value = ? WHERE key = 'projection_version'",
                String(projectionVersion),
            );
            this.ctx.storage.sql.exec(`
                INSERT INTO outbox (
                    event_id, event_type, seq, projection_version,
                    payload_json, attempts, created_at
                ) VALUES (?, 'message.read', ?, ?, ?, 0, ?)
            `, eventId, lastReadSeq, projectionVersion, JSON.stringify({
                conversationId: input.conversationId,
                participantType: 'visitor',
                lastReadSeq,
                updatedAt,
            }), updatedAt);
        });
        await scheduleOutbox(this);
        this.ctx.waitUntil(drainOutbox(this));
        const event = {
            v: CHAT_PROTOCOL_VERSION,
            type: 'message.read',
            eventId,
            conversationId: input.conversationId,
            seq: lastReadSeq,
            projectionVersion,
            serverTs: updatedAt,
            payload: { participantType: 'visitor', lastReadSeq },
        };
        this.broadcast(event);
        return json(event);
    }

    private async sendMessage(raw: unknown): Promise<Response> {
        const startedAt = Date.now();
        let created = false;
        if (!raw || typeof raw !== 'object') {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid message payload');
        }
        const input = raw as SendMessageInput;
        if (!isPrefixedId(input.conversationId, 'conversation')
            || !isPrefixedId(input.visitorId, 'visitor')
            || !isPrefixedId(input.clientMessageId, 'message')) {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid message identity');
        }
        if (!Number.isInteger(input.createdAt) || input.createdAt <= 0) {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid createdAt');
        }
        const body = normalizePlainText(input.body);

        const result = this.ctx.storage.transactionSync(() => {
            this.assertOwner(input as unknown as Record<string, unknown>);
            const existing = this.ctx.storage.sql.exec<MessageRow>(`
                SELECT seq, id, client_message_id, sender_type, sender_id, body_text, created_at
                FROM messages WHERE sender_id = ? AND client_message_id = ?
            `, input.visitorId, input.clientMessageId).toArray()[0];
            if (existing) {
                const event = this.ctx.storage.sql.exec<{ event_id: string; projection_version: number }>(`
                    SELECT event_id, projection_version FROM outbox
                    WHERE event_type = 'message.created' AND seq = ? LIMIT 1
                `, existing.seq).toArray()[0];
                return this.messageEnvelope(
                    existing,
                    event?.projection_version || Number(this.stateValue('projection_version') || 1),
                    event?.event_id || '',
                );
            }

            const status = this.stateValue('status');
            if (status === 'PURGE_PENDING') {
                throw new ChatProtocolError(
                    'CONVERSATION_PURGE_PENDING',
                    'Conversation is pending deletion',
                    409,
                );
            }
            if (status === 'SPAM') {
                throw new ChatProtocolError('FORBIDDEN', 'Conversation is not writable', 403);
            }

            this.consumeMessageRateLimit(`visitor:${input.visitorId}`, input.createdAt);
            const projectionVersion = Number(this.stateValue('projection_version') || 0) + 1;
            created = true;
            const messageId = createId('message');
            const messageEventId = createId('event');
            const message = this.ctx.storage.sql.exec<MessageRow>(`
                INSERT INTO messages (
                    id, client_message_id, sender_type, sender_id,
                    message_type, body_text, created_at
                ) VALUES (?, ?, 'visitor', ?, 'text', ?, ?)
                RETURNING seq, id, client_message_id, sender_type, sender_id, body_text, created_at
            `, messageId, input.clientMessageId, input.visitorId, body, input.createdAt).one();

            // ADR §29: un messaggio del visitatore riporta a OPEN sia una conversazione
            // riaperta (CLOSED/ARCHIVED) sia una in attesa di risposta (PENDING).
            // L'evento di stato usa una projection_version successiva a quella del
            // messaggio: le due update D1 restano applicabili in qualsiasi ordine.
            const reopened = status === 'CLOSED' || status === 'ARCHIVED';
            const resumed = status === 'PENDING';
            const stateVersion = reopened || resumed ? projectionVersion + 1 : projectionVersion;
            if (reopened || resumed) {
                this.ctx.storage.sql.exec(
                    "UPDATE conversation_local_state SET value = 'OPEN' WHERE key = 'status'",
                );
                this.clearLocalState('closed_at');
                this.ctx.storage.sql.exec(`
                    INSERT INTO outbox (
                        event_id, event_type, seq, projection_version,
                        payload_json, attempts, created_at
                    ) VALUES (?, ?, ?, ?, ?, 0, ?)
                `, createId('event'), reopened ? 'conversation.reopened' : 'conversation.updated',
                message.seq, stateVersion, JSON.stringify({
                    conversationId: input.conversationId,
                    status: 'OPEN',
                    updatedAt: input.createdAt,
                }), input.createdAt);
            }
            this.ctx.storage.sql.exec(
                "UPDATE conversation_local_state SET value = ? WHERE key = 'projection_version'",
                String(stateVersion),
            );
            this.ctx.storage.sql.exec(`
                INSERT INTO outbox (
                    event_id, event_type, seq, projection_version,
                    payload_json, attempts, created_at
                ) VALUES (?, 'message.created', ?, ?, ?, 0, ?)
            `, messageEventId, message.seq, projectionVersion, JSON.stringify({
                conversationId: input.conversationId,
                senderType: 'visitor',
                body,
                createdAt: input.createdAt,
            }), input.createdAt);
            return this.messageEnvelope(message, projectionVersion, messageEventId);
        });

        await scheduleOutbox(this);
        this.ctx.waitUntil(drainOutbox(this));
        this.broadcast(result);
        if (created) {
            emitMetric('chat_message_created_total', 1, { senderType: 'visitor' });
            emitMetric('chat_message_persistence_latency_ms', Date.now() - startedAt, { operation: 'send' });
        }
        return json(result, 201);
    }

    private assertOperatorInput(input: Record<string, unknown>): void {
        if (input.conversationId !== this.stateValue('conversation_id')) {
            throw new ChatProtocolError('NOT_FOUND', 'Conversation not found', 404);
        }
        if (!isPrefixedId(input.operatorId, 'operator')) {
            throw new ChatProtocolError('UNAUTHORIZED', 'Invalid operator', 401);
        }
    }

    private async sendOperatorMessage(raw: unknown): Promise<Response> {
        if (!raw || typeof raw !== 'object') {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid message payload');
        }
        const input = raw as Record<string, unknown>;
        this.assertOperatorInput(input);
        if (!isPrefixedId(input.clientMessageId, 'message')) {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid clientMessageId');
        }
        const body = normalizePlainText(input.body);
        const createdAt = Number(input.createdAt);
        if (!Number.isInteger(createdAt) || createdAt <= 0) {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid createdAt');
        }
        const operatorId = String(input.operatorId);
        const result = this.ctx.storage.transactionSync(() => {
            const existing = this.ctx.storage.sql.exec<MessageRow>(`
                SELECT seq, id, client_message_id, sender_type, sender_id, body_text, created_at
                FROM messages WHERE sender_id = ? AND client_message_id = ?
            `, operatorId, input.clientMessageId as string).toArray()[0];
            if (existing) {
                const outbox = this.ctx.storage.sql.exec<{ event_id: string; projection_version: number }>(`
                    SELECT event_id, projection_version FROM outbox
                    WHERE event_type = 'message.created' AND seq = ? LIMIT 1
                `, existing.seq).toArray()[0];
                return this.messageEnvelope(existing, outbox?.projection_version || 1, outbox?.event_id || '');
            }
            const status = this.stateValue('status');
            if (status === 'PURGE_PENDING') {
                throw new ChatProtocolError('CONVERSATION_PURGE_PENDING', 'Conversation is pending deletion', 409);
            }
            if (status === 'SPAM') {
                throw new ChatProtocolError('FORBIDDEN', 'Conversation is marked as spam', 403);
            }
            if (status === 'CLOSED') {
                throw new ChatProtocolError('CONVERSATION_CLOSED', 'Conversation is closed', 409);
            }
            if (status === 'ARCHIVED') {
                throw new ChatProtocolError('CONVERSATION_ARCHIVED', 'Conversation is archived', 409);
            }
            const projectionVersion = Number(this.stateValue('projection_version') || 0) + 1;
            const messageEventId = createId('event');
            const message = this.ctx.storage.sql.exec<MessageRow>(`
                INSERT INTO messages (
                    id, client_message_id, sender_type, sender_id,
                    message_type, body_text, created_at
                ) VALUES (?, ?, 'operator', ?, 'text', ?, ?)
                RETURNING seq, id, client_message_id, sender_type, sender_id, body_text, created_at
            `, createId('message'), input.clientMessageId as string, operatorId, body, createdAt).one();
            // ADR §29: la risposta dell'operatore mette la conversazione in attesa del visitatore.
            const stateVersion = status === 'OPEN' ? projectionVersion + 1 : projectionVersion;
            if (status === 'OPEN') {
                this.ctx.storage.sql.exec(
                    "UPDATE conversation_local_state SET value = 'PENDING' WHERE key = 'status'",
                );
                this.ctx.storage.sql.exec(`
                    INSERT INTO outbox (
                        event_id, event_type, seq, projection_version,
                        payload_json, attempts, created_at
                    ) VALUES (?, 'conversation.updated', ?, ?, ?, 0, ?)
                `, createId('event'), message.seq, stateVersion, JSON.stringify({
                    conversationId: input.conversationId,
                    status: 'PENDING',
                    updatedAt: createdAt,
                }), createdAt);
            }
            this.ctx.storage.sql.exec(
                "UPDATE conversation_local_state SET value = ? WHERE key = 'projection_version'",
                String(stateVersion),
            );
            this.ctx.storage.sql.exec(`
                INSERT INTO outbox (
                    event_id, event_type, seq, projection_version,
                    payload_json, attempts, created_at
                ) VALUES (?, 'message.created', ?, ?, ?, 0, ?)
            `, messageEventId, message.seq, projectionVersion, JSON.stringify({
                conversationId: input.conversationId,
                senderType: 'operator',
                body,
                createdAt,
            }), createdAt);
            return this.messageEnvelope(message, projectionVersion, messageEventId);
        });
        await scheduleOutbox(this);
        this.ctx.waitUntil(drainOutbox(this));
        this.broadcast(result);
        return json(result, 201);
    }

    private getAdminDetail(raw: unknown): Response {
        if (!raw || typeof raw !== 'object') throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid request');
        const input = raw as Record<string, unknown>;
        this.assertOperatorInput(input);
        return this.getDetail({
            conversationId: input.conversationId,
            visitorId: this.stateValue('visitor_id'),
        });
    }

    private getAdminMessages(raw: unknown): Response {
        if (!raw || typeof raw !== 'object') throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid request');
        const input = raw as Record<string, unknown>;
        this.assertOperatorInput(input);
        return this.getMessages({
            conversationId: input.conversationId,
            visitorId: this.stateValue('visitor_id'),
            beforeSeq: input.beforeSeq,
            limit: input.limit,
        });
    }

    private getAdminExport(raw: unknown): Response {
        if (!raw || typeof raw !== 'object') throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid request');
        const input = raw as Record<string, unknown>;
        this.assertOperatorInput(input);
        const metadata = JSON.parse(this.stateValue('metadata_json') || '{}') as Record<string, unknown>;
        const rows = this.ctx.storage.sql.exec<MessageRow>(`
            SELECT seq, id, client_message_id, sender_type, sender_id, body_text, created_at
            FROM messages ORDER BY seq ASC
        `).toArray();
        return json({
            exportedAt: Date.now(),
            conversation: {
                conversationId: this.stateValue('conversation_id'),
                status: this.stateValue('status'),
                assignedOperatorId: this.stateValue('assigned_operator_id') || null,
                projectionVersion: Number(this.stateValue('projection_version') || 0),
                ...metadata,
            },
            messages: rows.map((row) => ({
                seq: row.seq,
                messageId: row.id,
                clientMessageId: row.client_message_id,
                senderType: row.sender_type,
                senderId: row.sender_id,
                body: row.body_text,
                createdAt: row.created_at,
            })),
        });
    }

    private async updateConversationState(raw: unknown): Promise<Response> {
        if (!raw || typeof raw !== 'object') throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid request');
        const input = raw as Record<string, unknown>;
        this.assertOperatorInput(input);
        if (!isConversationStatus(input.status) || input.status === 'PURGE_PENDING') {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid target status');
        }
        const current = this.stateValue('status');
        if (!isConversationStatus(current)) throw new ChatProtocolError('INTERNAL_ERROR', 'Invalid state', 500);
        assertTransition(current, input.status);
        const updatedAt = Number(input.updatedAt);
        if (!Number.isInteger(updatedAt) || updatedAt <= 0) {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid updatedAt');
        }
        const projectionVersion = Number(this.stateValue('projection_version') || 0) + 1;
        const lastSeq = this.ctx.storage.sql.exec<{ max_seq: number }>(
            'SELECT COALESCE(MAX(seq), 0) AS max_seq FROM messages',
        ).one().max_seq;
        const eventType: Record<Exclude<ConversationStatus, 'PURGE_PENDING'>, string> = {
            OPEN: current === 'CLOSED' || current === 'ARCHIVED' ? 'conversation.reopened' : 'conversation.updated',
            PENDING: 'conversation.updated',
            CLOSED: 'conversation.closed',
            ARCHIVED: 'conversation.archived',
            SPAM: 'conversation.spam_marked',
        };
        const day = 86_400_000;
        // ADR §69.2: `closed_at` è l'origine di entrambe le scadenze. Viene persistito
        // alla chiusura così che l'archiviazione non faccia ripartire la retention.
        const closedAt = input.status === 'CLOSED'
            ? updatedAt
            : Number(this.stateValue('closed_at') || 0) || null;
        const archiveAt = input.status === 'CLOSED'
            ? updatedAt + Number(this.env.CHAT_ARCHIVE_AFTER_DAYS || 30) * day
            : null;
        const purgeAt = input.status === 'SPAM'
            ? updatedAt + Number(this.env.CHAT_SPAM_RETENTION_DAYS || 14) * day
            : input.status === 'CLOSED' || input.status === 'ARCHIVED'
                ? (closedAt ?? updatedAt) + Number(this.env.CHAT_RETENTION_DAYS || 180) * day
                : null;
        const eventId = createId('event');
        this.ctx.storage.transactionSync(() => {
            this.ctx.storage.sql.exec(
                "UPDATE conversation_local_state SET value = ? WHERE key = 'status'",
                input.status as string,
            );
            if (input.status === 'CLOSED') this.setLocalState('closed_at', String(updatedAt));
            if (input.status === 'OPEN') this.clearLocalState('closed_at');
            this.ctx.storage.sql.exec(
                "UPDATE conversation_local_state SET value = ? WHERE key = 'projection_version'",
                String(projectionVersion),
            );
            this.ctx.storage.sql.exec(`
                INSERT INTO outbox (
                    event_id, event_type, seq, projection_version,
                    payload_json, attempts, created_at
                ) VALUES (?, ?, ?, ?, ?, 0, ?)
            `, eventId, eventType[input.status as Exclude<ConversationStatus, 'PURGE_PENDING'>],
            lastSeq, projectionVersion, JSON.stringify({
                conversationId: input.conversationId,
                status: input.status,
                closedAt: input.status === 'OPEN' ? null : closedAt,
                archivedAt: input.status === 'ARCHIVED' ? updatedAt : null,
                archiveAt,
                purgeAt,
                updatedAt,
            }), updatedAt);
        });
        await scheduleOutbox(this);
        this.ctx.waitUntil(drainOutbox(this));
        const event = {
            v: CHAT_PROTOCOL_VERSION,
            type: eventType[input.status as Exclude<ConversationStatus, 'PURGE_PENDING'>],
            eventId,
            conversationId: input.conversationId,
            seq: lastSeq,
            projectionVersion,
            serverTs: updatedAt,
            payload: { status: input.status },
        };
        this.broadcast(event);
        return json(event);
    }

    private async updateAssignment(raw: unknown): Promise<Response> {
        if (!raw || typeof raw !== 'object') throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid request');
        const input = raw as Record<string, unknown>;
        this.assertOperatorInput(input);
        const assignedOperatorId = input.assignedOperatorId == null ? null : input.assignedOperatorId;
        if (assignedOperatorId !== null && !isPrefixedId(assignedOperatorId, 'operator')) {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid assignedOperatorId');
        }
        const updatedAt = Number(input.updatedAt);
        if (!Number.isInteger(updatedAt) || updatedAt <= 0) {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid updatedAt');
        }
        const projectionVersion = Number(this.stateValue('projection_version') || 0) + 1;
        const eventId = createId('event');
        this.ctx.storage.transactionSync(() => {
            this.ctx.storage.sql.exec(
                "INSERT INTO conversation_local_state (key, value) VALUES ('assigned_operator_id', ?) "
                    + 'ON CONFLICT(key) DO UPDATE SET value = excluded.value',
                assignedOperatorId || '',
            );
            this.ctx.storage.sql.exec(
                "UPDATE conversation_local_state SET value = ? WHERE key = 'projection_version'",
                String(projectionVersion),
            );
            this.ctx.storage.sql.exec(`
                INSERT INTO outbox (
                    event_id, event_type, seq, projection_version,
                    payload_json, attempts, created_at
                ) VALUES (?, 'operator.assignment', NULL, ?, ?, 0, ?)
            `, eventId, projectionVersion, JSON.stringify({
                conversationId: input.conversationId,
                assignedOperatorId,
                updatedAt,
            }), updatedAt);
        });
        await scheduleOutbox(this);
        this.ctx.waitUntil(drainOutbox(this));
        const event = {
            v: CHAT_PROTOCOL_VERSION,
            type: 'operator.assignment',
            eventId,
            conversationId: input.conversationId,
            projectionVersion,
            serverTs: updatedAt,
            payload: { assignedOperatorId },
        };
        this.broadcast(event);
        return json(event);
    }

    private async markOperatorRead(raw: unknown): Promise<Response> {
        if (!raw || typeof raw !== 'object') throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid request');
        const input = raw as Record<string, unknown>;
        this.assertOperatorInput(input);
        const maxSeq = this.ctx.storage.sql.exec<{ max_seq: number }>(
            'SELECT COALESCE(MAX(seq), 0) AS max_seq FROM messages',
        ).one().max_seq;
        const requested = Number(input.lastReadSeq);
        const updatedAt = Number(input.updatedAt);
        if (!Number.isInteger(requested) || requested < 0 || !Number.isInteger(updatedAt) || updatedAt <= 0) {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid read cursor');
        }
        const lastReadSeq = Math.min(requested, maxSeq);
        const participantKey = `operator:${String(input.operatorId)}`;
        const current = this.ctx.storage.sql.exec<{ last_read_seq: number }>(
            'SELECT last_read_seq FROM participant_state WHERE participant_key = ?', participantKey,
        ).toArray()[0]?.last_read_seq || 0;
        if (lastReadSeq <= current) return json({ ok: true, lastReadSeq: current });
        const projectionVersion = Number(this.stateValue('projection_version') || 0) + 1;
        const eventId = createId('event');
        this.ctx.storage.transactionSync(() => {
            this.ctx.storage.sql.exec(`
                INSERT INTO participant_state (participant_key, last_read_seq, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(participant_key) DO UPDATE SET
                    last_read_seq = MAX(last_read_seq, excluded.last_read_seq),
                    updated_at = excluded.updated_at
            `, participantKey, lastReadSeq, updatedAt);
            this.ctx.storage.sql.exec(
                "UPDATE conversation_local_state SET value = ? WHERE key = 'projection_version'",
                String(projectionVersion),
            );
            this.ctx.storage.sql.exec(`
                INSERT INTO outbox (
                    event_id, event_type, seq, projection_version,
                    payload_json, attempts, created_at
                ) VALUES (?, 'message.read', ?, ?, ?, 0, ?)
            `, eventId, lastReadSeq, projectionVersion, JSON.stringify({
                conversationId: input.conversationId,
                participantType: 'operator',
                lastReadSeq,
                updatedAt,
            }), updatedAt);
        });
        await scheduleOutbox(this);
        this.ctx.waitUntil(drainOutbox(this));
        return json({ ok: true, eventId, lastReadSeq, projectionVersion });
    }

    private async requestPurge(raw: unknown): Promise<Response> {
        if (!raw || typeof raw !== 'object') throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid purge request');
        const input = raw as Record<string, unknown>;
        if (input.conversationId !== this.stateValue('conversation_id')) {
            // An already deleted DO is an idempotent success.
            if (!this.stateValue('conversation_id')) return json({ ok: true, alreadyDeleted: true });
            throw new ChatProtocolError('NOT_FOUND', 'Conversation not found', 404);
        }
        const now = Number(input.requestedAt);
        if (!Number.isInteger(now) || now <= 0) throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid requestedAt');
        const purgeAt = Number(input.purgeAt || now);
        if (!Number.isInteger(purgeAt) || purgeAt < now) {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid purgeAt');
        }
        if (this.stateValue('status') === 'PURGE_PENDING') {
            // A retry must also flush a previously persisted purge event before D1 is deleted.
            await scheduleOutbox(this);
            await drainOutbox(this);
            return json({ ok: true, alreadyPending: true });
        }
        const projectionVersion = Number(this.stateValue('projection_version') || 0) + 1;
        const eventId = createId('event');
        const lastSeq = this.ctx.storage.sql.exec<{ max_seq: number }>(
            'SELECT COALESCE(MAX(seq), 0) AS max_seq FROM messages',
        ).one().max_seq;
        this.ctx.storage.transactionSync(() => {
            this.ctx.storage.sql.exec("UPDATE conversation_local_state SET value = 'PURGE_PENDING' WHERE key = 'status'");
            this.ctx.storage.sql.exec("UPDATE conversation_local_state SET value = 'CLOSED' WHERE key = 'write_gate'");
            this.ctx.storage.sql.exec(
                "UPDATE conversation_local_state SET value = ? WHERE key = 'projection_version'",
                String(projectionVersion),
            );
            this.ctx.storage.sql.exec(`
                INSERT INTO outbox (event_id,event_type,seq,projection_version,payload_json,attempts,created_at)
                VALUES (?, 'conversation.purge_requested', ?, ?, ?, 0, ?)
            `, eventId, lastSeq, projectionVersion, JSON.stringify({
                conversationId: input.conversationId,
                status: 'PURGE_PENDING',
                purgeRequestedAt: now,
                purgeAt,
                deletionReason: String(input.reason || 'retention'),
                updatedAt: now,
            }), now);
        });
        await scheduleOutbox(this);
        await drainOutbox(this);
        const event = { v: 1, type: 'conversation.purge_requested', eventId,
            conversationId: input.conversationId, projectionVersion, serverTs: now,
            payload: { status: 'PURGE_PENDING' } };
        this.broadcast(event);
        for (const socket of this.ctx.getWebSockets()) socket.close(1000, 'Conversation deleted');
        return json(event);
    }

    private async finalizePurge(raw: unknown): Promise<Response> {
        if (!raw || typeof raw !== 'object') throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid purge finalization');
        const input = raw as Record<string, unknown>;
        const currentId = this.stateValue('conversation_id');
        if (!currentId) return json({ ok: true, alreadyDeleted: true });
        if (input.conversationId !== currentId || this.stateValue('status') !== 'PURGE_PENDING') {
            throw new ChatProtocolError('CONVERSATION_PURGE_PENDING', 'Purge gate is not active', 409);
        }
        await this.ctx.storage.deleteAll();
        this.purged = true;
        return json({ ok: true });
    }

    private async cancelPurge(raw: unknown): Promise<Response> {
        if (!raw || typeof raw !== 'object') throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid purge cancellation');
        const input = raw as Record<string, unknown>;
        const currentId = this.stateValue('conversation_id');
        if (!currentId || input.conversationId !== currentId) {
            throw new ChatProtocolError('NOT_FOUND', 'Conversation not found', 404);
        }
        if (this.stateValue('status') !== 'PURGE_PENDING') {
            return json({ ok: true, alreadyCancelled: true });
        }
        if (!isConversationStatus(input.previousStatus) || input.previousStatus === 'PURGE_PENDING') {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid previous status');
        }
        const updatedAt = Number(input.updatedAt);
        if (!Number.isInteger(updatedAt) || updatedAt <= 0) {
            throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid updatedAt');
        }
        const projectionVersion = Number(this.stateValue('projection_version') || 0) + 1;
        const eventId = createId('event');
        const lastSeq = this.ctx.storage.sql.exec<{ max_seq: number }>(
            'SELECT COALESCE(MAX(seq), 0) AS max_seq FROM messages',
        ).one().max_seq;
        const payload = {
            conversationId: currentId,
            status: input.previousStatus,
            closedAt: input.previousClosedAt ?? null,
            archivedAt: input.previousArchivedAt ?? null,
            archiveAt: input.previousArchiveAt ?? null,
            purgeAt: input.previousPurgeAt ?? null,
            purgeRequestedAt: null,
            deletionReason: null,
            updatedAt,
        };
        this.ctx.storage.transactionSync(() => {
            this.ctx.storage.sql.exec(
                'UPDATE conversation_local_state SET value = ? WHERE key = \'status\'',
                input.previousStatus as string,
            );
            this.ctx.storage.sql.exec("UPDATE conversation_local_state SET value = 'OPEN' WHERE key = 'write_gate'");
            this.ctx.storage.sql.exec(
                "UPDATE conversation_local_state SET value = ? WHERE key = 'projection_version'",
                String(projectionVersion),
            );
            this.ctx.storage.sql.exec(`
                INSERT INTO outbox (event_id,event_type,seq,projection_version,payload_json,attempts,created_at)
                VALUES (?, 'conversation.updated', ?, ?, ?, 0, ?)
            `, eventId, lastSeq, projectionVersion, JSON.stringify(payload), updatedAt);
        });
        await scheduleOutbox(this);
        await drainOutbox(this);
        const event = { v: 1, type: 'conversation.updated', eventId,
            conversationId: currentId, projectionVersion, serverTs: updatedAt,
            payload: { status: input.previousStatus } };
        this.broadcast(event);
        return json(event);
    }

    private getDetail(raw: unknown): Response {
        if (!raw || typeof raw !== 'object') throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid request');
        const input = raw as Record<string, unknown>;
        this.assertOwner(input);
        const metadata = JSON.parse(this.stateValue('metadata_json') || '{}') as Record<string, unknown>;
        const last = this.ctx.storage.sql.exec<{ last_seq: number }>(
            'SELECT COALESCE(MAX(seq), 0) AS last_seq FROM messages',
        ).one();
        return json({
            conversationId: this.stateValue('conversation_id'),
            status: this.stateValue('status'),
            lastSeq: last.last_seq,
            projectionVersion: Number(this.stateValue('projection_version') || 0),
            ...metadata,
        });
    }

    private getMessages(raw: unknown): Response {
        if (!raw || typeof raw !== 'object') throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid request');
        const input = raw as Record<string, unknown>;
        this.assertOwner(input);
        const requestedLimit = Number(input.limit || 50);
        const limit = Number.isInteger(requestedLimit) ? Math.max(1, Math.min(100, requestedLimit)) : 50;
        const requestedBefore = Number(input.beforeSeq);
        const beforeSeq = Number.isInteger(requestedBefore) && requestedBefore > 0
            ? requestedBefore
            : Number.MAX_SAFE_INTEGER;
        const rows = this.ctx.storage.sql.exec<MessageRow>(`
            SELECT seq, id, client_message_id, sender_type, sender_id, body_text, created_at
            FROM messages
            WHERE seq < ?
            ORDER BY seq DESC
            LIMIT ?
        `, beforeSeq, limit).toArray().reverse();
        return json({
            conversationId: this.stateValue('conversation_id'),
            messages: rows.map((row) => ({
                seq: row.seq,
                messageId: row.id,
                clientMessageId: row.client_message_id,
                senderType: row.sender_type,
                body: row.body_text,
                createdAt: row.created_at,
            })),
            nextBeforeSeq: rows.length === limit ? rows[0]?.seq ?? null : null,
        });
    }
}
