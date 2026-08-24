import type { SupportRealtimeEnv } from './env';
import { ChatProtocolError } from '../../../support/shared/errors';
import { isPrefixedId } from '../../../support/shared/ids';
import { dispatchVisitorPush } from './push';
import { emitMetric } from './observability';

interface OperatorAttachment {
    role: 'operator';
    operatorId: string;
    visibility: 'visible' | 'hidden';
    operatorState: 'ONLINE' | 'BUSY' | 'OFFLINE';
}

export class SupportHubDurableObject {
    protected readonly ctx: DurableObjectState;
    protected readonly env: SupportRealtimeEnv;

    constructor(ctx: DurableObjectState, env: SupportRealtimeEnv) {
        this.ctx = ctx;
        this.env = env;
    }

    async fetch(request: Request): Promise<Response> {
        const url = new URL(request.url);
        if (request.method === 'GET' && url.pathname === '/internal/health') {
            return Response.json({ ok: true, component: 'support-hub' });
        }
        if (request.method === 'GET' && url.pathname === '/internal/availability') {
            const settings = await this.env.CHAT_DB.prepare(`
                SELECT public_availability_override FROM chat_support_settings WHERE settings_key = 'default'
            `).first<{ public_availability_override: 'AUTO' | 'ONLINE' | 'OFFLINE' }>();
            const override = settings?.public_availability_override || 'AUTO';
            const operatorOnline = this.ctx.getWebSockets('operator').some((socket) => {
                const attachment = socket.deserializeAttachment() as OperatorAttachment | null;
                return attachment?.operatorState === 'ONLINE';
            });
            const availability = override === 'AUTO' ? (operatorOnline ? 'ONLINE' : 'OFFLINE') : override;
            return Response.json({ availability, override, operatorConnected: this.ctx.getWebSockets('operator').length > 0 });
        }
        if (request.method === 'POST' && url.pathname === '/internal/events') {
            const event = await request.json<Record<string, unknown>>();
            const serialized = JSON.stringify(event);
            for (const socket of this.ctx.getWebSockets('operator')) {
                try { socket.send(serialized); } catch { /* runtime removes stale sockets */ }
            }
            const payload = event.payload as Record<string, unknown> | undefined;
            const conversationId = typeof payload?.conversationId === 'string'
                ? payload.conversationId
                : null;
            const sequence = Number(event.seq || 0);
            const kind = event.type === 'conversation.created'
                ? 'new_conversation'
                : event.type === 'message.created' && payload?.senderType === 'visitor' && sequence > 1
                    ? 'visitor_message'
                    : event.type === 'operator.assignment' && typeof payload?.assignedOperatorId === 'string'
                        ? 'assigned_conversation'
                        : null;
            if (conversationId && kind) {
                const visibleOperators = new Set<string>();
                for (const socket of this.ctx.getWebSockets('operator')) {
                    const attachment = socket.deserializeAttachment() as OperatorAttachment | null;
                    if (attachment?.visibility === 'visible') visibleOperators.add(attachment.operatorId);
                }
                this.ctx.waitUntil(dispatchVisitorPush(this.env, {
                    conversationId,
                    body: typeof payload?.body === 'string' ? payload.body : undefined,
                    kind,
                }, visibleOperators,
                kind === 'assigned_conversation' ? String(payload?.assignedOperatorId) : undefined));
            }
            return new Response(null, { status: 204 });
        }
        if (request.method === 'POST' && url.pathname === '/internal/push/test') {
            const input = await request.json<Record<string, unknown>>();
            if (!isPrefixedId(input.operatorId, 'operator')
                || !isPrefixedId(input.conversationId, 'conversation')) {
                throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid push test payload');
            }
            const result = await dispatchVisitorPush(this.env, {
                conversationId: input.conversationId,
                body: 'Notifica di prova Aml Store Support',
                kind: 'test',
            }, new Set(), input.operatorId);
            return Response.json(result);
        }
        if (request.method === 'GET' && url.pathname === '/internal/operators/ws') {
            const operatorId = url.searchParams.get('operatorId');
            if (!isPrefixedId(operatorId, 'operator')) {
                throw new ChatProtocolError('UNAUTHORIZED', 'Invalid operator', 401);
            }
            if (request.headers.get('Upgrade')?.toLowerCase() !== 'websocket') {
                throw new ChatProtocolError('INVALID_PAYLOAD', 'WebSocket upgrade required', 426);
            }
            const pair = new WebSocketPair();
            const [client, server] = Object.values(pair) as [WebSocket, WebSocket];
            const preferences = await this.env.CHAT_DB.prepare(`
                SELECT availability_state FROM chat_operator_preferences WHERE operator_id = ?
            `).bind(operatorId).first<{ availability_state: 'ONLINE' | 'BUSY' | 'OFFLINE' }>();
            server.serializeAttachment({
                role: 'operator',
                operatorId,
                visibility: 'visible',
                operatorState: preferences?.availability_state || 'OFFLINE',
            } satisfies OperatorAttachment);
            this.ctx.acceptWebSocket(server, ['operator', `operator:${operatorId}`]);
            emitMetric('chat_ws_connected', 1, { role: 'operator' });
            const presence = JSON.stringify({
                v: 1,
                type: 'operator.presence',
                eventId: `evt_${crypto.randomUUID()}`,
                serverTs: Date.now(),
                payload: { operatorId, state: 'connected' },
            });
            for (const socket of this.ctx.getWebSockets('operator')) {
                try { socket.send(presence); } catch { /* runtime removes stale sockets */ }
            }
            return new Response(null, { status: 101, webSocket: client });
        }
        return Response.json({ error: 'Not found' }, { status: 404 });
    }

    webSocketMessage(socket: WebSocket, message: string | ArrayBuffer): void {
        const attachment = socket.deserializeAttachment() as OperatorAttachment | null;
        if (!attachment || attachment.role !== 'operator') {
            socket.close(1008, 'Invalid identity');
            return;
        }
        if (typeof message !== 'string') return;
        let event: Record<string, unknown>;
        try { event = JSON.parse(message) as Record<string, unknown>; } catch { return; }
        const payload = event.payload as Record<string, unknown> | undefined;
        if (event.v === 1 && event.type === 'operator.visibility'
            && (payload?.visibility === 'visible' || payload?.visibility === 'hidden')) {
            socket.serializeAttachment({ ...attachment, visibility: payload.visibility } satisfies OperatorAttachment);
        }
        if (event.v === 1 && event.type === 'operator.presence'
            && ['ONLINE', 'BUSY', 'OFFLINE'].includes(String(payload?.state))) {
            const operatorState = payload?.state as OperatorAttachment['operatorState'];
            socket.serializeAttachment({ ...attachment, operatorState } satisfies OperatorAttachment);
            const presence = JSON.stringify({
                v: 1,
                type: 'operator.presence',
                eventId: `evt_${crypto.randomUUID()}`,
                serverTs: Date.now(),
                payload: { operatorId: attachment.operatorId, state: operatorState },
            });
            for (const peer of this.ctx.getWebSockets('operator')) {
                try { peer.send(presence); } catch { /* stale socket */ }
            }
        }
        if (event.v === 1 && event.type === 'operator.reconnect') {
            emitMetric('chat_ws_reconnect_total', 1, { role: 'operator' });
        }
    }

    webSocketClose(socket: WebSocket, _code: number, _reason: string): void {
        const attachment = socket.deserializeAttachment() as OperatorAttachment | null;
        if (!attachment) return;
        const presence = JSON.stringify({
            v: 1,
            type: 'operator.presence',
            eventId: `evt_${crypto.randomUUID()}`,
            serverTs: Date.now(),
            payload: { operatorId: attachment.operatorId, state: 'disconnected' },
        });
        for (const peer of this.ctx.getWebSockets('operator')) {
            try { peer.send(presence); } catch { /* runtime removes stale sockets */ }
        }
    }
}
