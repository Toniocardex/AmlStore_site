import { readChatConfig } from '../../../support/shared/config';
import { ChatProtocolError } from '../../../support/shared/errors';
import { isPrefixedId } from '../../../support/shared/ids';
import { normalizePlainText } from '../../../support/shared/schemas';
import { normalizeContact, normalizeEmail, type ContactInput } from './contact';
import {
    createGuestSession,
    deriveConversationId,
    readGuestSession,
    renewGuestSession,
    requireGuestSession,
    serializeGuestCookie,
    shouldRenewGuestSession,
    type GuestSessionEnv,
} from './guest-session';
import { assertAllowedOrigin } from './origin';
import { verifyOrderContext, type OrderTokenInput } from './order-context';
import { consumeGlobalRateLimit, requestIp } from './rate-limit';
import { chatJson, readJsonBody } from './responses';

export interface ChatPagesEnv extends GuestSessionEnv {
    DB: D1Database;
    CHAT_CONVERSATIONS: DurableObjectNamespace;
    SUPPORT_HUB: DurableObjectNamespace;
    CHAT_CONTACT_LOOKUP_SECRET?: string;
    CHAT_ENABLED?: string;
    CHAT_MAX_MESSAGE_LENGTH?: string;
    CHAT_ARCHIVE_AFTER_DAYS?: string;
    CHAT_RETENTION_DAYS?: string;
    CHAT_SPAM_RETENTION_DAYS?: string;
    CHAT_DELETE_GRACE_DAYS?: string;
    CHAT_TOMBSTONE_RETENTION_DAYS?: string;
    CHAT_RETENTION_BATCH_SIZE?: string;
    TOKEN_SECRET?: string;
    SITE_ORIGIN?: string;
}

interface CreateConversationBody {
    clientMessageId?: unknown;
    body?: unknown;
    pagePath?: unknown;
    productId?: unknown;
    locale?: unknown;
    contact?: ContactInput;
    orderToken?: OrderTokenInput;
    visitorId?: unknown;
}

interface SendMessageBody {
    clientMessageId?: unknown;
    body?: unknown;
    visitorId?: unknown;
}

function config(env: ChatPagesEnv) {
    return readChatConfig(env as unknown as Record<string, string | undefined>);
}

function requireEnabled(env: ChatPagesEnv): void {
    if (!config(env).enabled) {
        throw new ChatProtocolError('TEMPORARILY_UNAVAILABLE', 'Chat is disabled', 503);
    }
}

function optionalString(value: unknown, max: number): string | null {
    if (value == null || value === '') return null;
    if (typeof value !== 'string') throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid string field');
    const normalized = value.trim();
    if (normalized.length > max) throw new ChatProtocolError('INVALID_PAYLOAD', 'String field is too long');
    return normalized || null;
}

function locale(value: unknown): string | null {
    const normalized = optionalString(value, 5);
    if (normalized == null) return null;
    if (!['it', 'en', 'fr', 'de', 'es'].includes(normalized)) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Unsupported locale');
    }
    return normalized;
}

export async function handleGuestSession(request: Request, env: ChatPagesEnv): Promise<Response> {
    assertAllowedOrigin(request, env);
    requireEnabled(env);
    const existing = await readGuestSession(request, env);
    const session = existing || createGuestSession(env);
    const headers = new Headers();
    if (!existing) headers.set('Set-Cookie', await serializeGuestCookie(session, env, request));
    return chatJson({ ok: true, expiresAt: session.expiresAt }, 200, headers);
}

export async function handleAvailability(env: ChatPagesEnv): Promise<Response> {
    const chatConfig = config(env);
    if (!chatConfig.enabled) return chatJson({ enabled: false, availability: 'OFFLINE' });
    try {
        const hub = env.SUPPORT_HUB.get(env.SUPPORT_HUB.idFromName('support-hub:default'));
        const response = await hub.fetch('https://internal/internal/availability');
        if (response.ok) {
            const state = await response.json<Record<string, unknown>>();
            return chatJson({ enabled: true, availability: state.availability || 'OFFLINE' });
        }
    } catch { /* public availability fails closed */ }
    return chatJson({ enabled: true, availability: 'OFFLINE' });
}

export async function handleCreateConversation(request: Request, env: ChatPagesEnv): Promise<Response> {
    assertAllowedOrigin(request, env);
    requireEnabled(env);
    const session = await requireGuestSession(request, env);
    const body = await readJsonBody(request) as CreateConversationBody;
    if (Object.prototype.hasOwnProperty.call(body, 'visitorId')) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'visitorId must not be supplied');
    }
    if (!isPrefixedId(body.clientMessageId, 'message')) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid clientMessageId');
    }

    await Promise.all([
        consumeGlobalRateLimit(env, 'conversation-create:visitor', session.visitorId, 8, 10 * 60_000),
        consumeGlobalRateLimit(env, 'conversation-create:ip', requestIp(request), 30, 10 * 60_000),
    ]);

    const chatConfig = config(env);
    const messageBody = normalizePlainText(body.body, chatConfig.maxMessageLength);
    const contact = await normalizeContact(body.contact, env);
    const order = await verifyOrderContext(body.orderToken, env);
    const contactVerifiedAt = order?.customerEmail && contact.email
        && order.customerEmail === normalizeEmail(contact.email)
        ? Date.now()
        : null;
    const conversationId = await deriveConversationId(session.visitorId, body.clientMessageId, env);
    // ADR §69.8/§69.9: il conversationId è deterministico, quindi un create tardivo con
    // lo stesso clientMessageId ricadrebbe sul Durable Object già svuotato e ne
    // reinizializzerebbe lo storage, mentre la projection resterebbe scartata dal
    // tombstone. Il gateway consulta il tombstone prima di toccare il DO: un nuovo
    // contatto del guest deve generare una conversazione nuova.
    const tombstone = await env.DB.prepare(
        'SELECT conversation_id FROM chat_conversation_tombstones WHERE conversation_id = ?',
    ).bind(conversationId).first<{ conversation_id: string }>();
    if (tombstone) {
        throw new ChatProtocolError('CONVERSATION_PURGED', 'Conversation no longer exists', 410);
    }
    const stub = env.CHAT_CONVERSATIONS.get(env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`));
    const internalRequest = new Request('https://internal/internal/conversations/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            conversationId,
            visitorId: session.visitorId,
            clientMessageId: body.clientMessageId,
            body: messageBody,
            contactName: contact.name,
            contactEmail: contact.email,
            contactEmailLookupHash: contact.emailLookupHash,
            contactVerifiedAt,
            pagePath: optionalString(body.pagePath, 500),
            productId: optionalString(body.productId, 100),
            orderId: order?.orderId || null,
            locale: locale(body.locale),
            countryCode: request.cf?.country || null,
            createdAt: Date.now(),
        }),
    });
    const response = await stub.fetch(internalRequest);
    const headers = new Headers(response.headers);
    headers.set('Cache-Control', 'no-store');
    if (shouldRenewGuestSession(session)) {
        headers.append('Set-Cookie', await serializeGuestCookie(renewGuestSession(session, env), env, request));
    }
    return new Response(response.body, { status: response.status, headers });
}

export async function handleListGuestConversations(request: Request, env: ChatPagesEnv): Promise<Response> {
    requireEnabled(env);
    const session = await requireGuestSession(request, env);
    const rows = await env.DB.prepare(`
        SELECT id, status, locale, product_id, order_id, page_path,
               last_seq, projection_version, last_message_at,
               last_message_sender, last_message_preview,
               visitor_unread_count, operator_unread_count,
               created_at, updated_at
        FROM chat_conversations
        WHERE visitor_id = ? AND status != 'PURGE_PENDING'
        ORDER BY COALESCE(last_message_at, created_at) DESC, id DESC
        LIMIT 50
    `).bind(session.visitorId).all();
    return chatJson({
        conversations: (rows.results || []).map((row) => ({
            id: row.id,
            status: row.status,
            locale: row.locale,
            productId: row.product_id,
            orderId: row.order_id,
            pagePath: row.page_path,
            lastSeq: row.last_seq,
            projectionVersion: row.projection_version,
            lastMessageAt: row.last_message_at,
            lastMessageSender: row.last_message_sender,
            lastMessagePreview: row.last_message_preview,
            visitorUnreadCount: row.visitor_unread_count,
            operatorUnreadCount: row.operator_unread_count,
            createdAt: row.created_at,
            updatedAt: row.updated_at,
        })),
    });
}

export async function handleSendGuestMessage(
    request: Request,
    env: ChatPagesEnv,
    conversationId: string,
): Promise<Response> {
    assertAllowedOrigin(request, env);
    requireEnabled(env);
    if (!isPrefixedId(conversationId, 'conversation')) {
        throw new ChatProtocolError('NOT_FOUND', 'Conversation not found', 404);
    }
    const session = await requireGuestSession(request, env);
    const body = await readJsonBody(request) as SendMessageBody;
    if (Object.prototype.hasOwnProperty.call(body, 'visitorId')) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'visitorId must not be supplied');
    }
    if (!isPrefixedId(body.clientMessageId, 'message')) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid clientMessageId');
    }
    await Promise.all([
        consumeGlobalRateLimit(env, 'message-send:visitor', session.visitorId, 120, 10 * 60_000),
        consumeGlobalRateLimit(env, 'message-send:ip', requestIp(request), 300, 10 * 60_000),
    ]);
    const messageBody = normalizePlainText(body.body, config(env).maxMessageLength);
    const stub = env.CHAT_CONVERSATIONS.get(
        env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
    );
    const response = await stub.fetch(new Request(
        'https://internal/internal/conversations/messages/send',
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                conversationId,
                visitorId: session.visitorId,
                clientMessageId: body.clientMessageId,
                body: messageBody,
                createdAt: Date.now(),
            }),
        },
    ));
    const headers = new Headers(response.headers);
    headers.set('Cache-Control', 'no-store');
    if (shouldRenewGuestSession(session)) {
        headers.append('Set-Cookie', await serializeGuestCookie(renewGuestSession(session, env), env, request));
    }
    return new Response(response.body, { status: response.status, headers });
}

export async function handleGuestRead(
    request: Request,
    env: ChatPagesEnv,
    conversationId: string,
): Promise<Response> {
    assertAllowedOrigin(request, env);
    requireEnabled(env);
    if (!isPrefixedId(conversationId, 'conversation')) {
        throw new ChatProtocolError('NOT_FOUND', 'Conversation not found', 404);
    }
    const session = await requireGuestSession(request, env);
    const body = await readJsonBody(request) as { lastReadSeq?: unknown; visitorId?: unknown };
    if (Object.prototype.hasOwnProperty.call(body, 'visitorId')) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'visitorId must not be supplied');
    }
    const lastReadSeq = Number(body.lastReadSeq);
    if (!Number.isInteger(lastReadSeq) || lastReadSeq < 0) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid lastReadSeq');
    }
    const stub = env.CHAT_CONVERSATIONS.get(
        env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
    );
    const response = await stub.fetch(new Request('https://internal/internal/conversations/read', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            conversationId,
            visitorId: session.visitorId,
            lastReadSeq,
            updatedAt: Date.now(),
        }),
    }));
    return new Response(response.body, {
        status: response.status,
        headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
    });
}

export async function handleGuestWebSocket(
    request: Request,
    env: ChatPagesEnv,
    conversationId: string,
): Promise<Response> {
    assertAllowedOrigin(request, env);
    requireEnabled(env);
    if (!isPrefixedId(conversationId, 'conversation')) {
        throw new ChatProtocolError('NOT_FOUND', 'Conversation not found', 404);
    }
    const url = new URL(request.url);
    if (url.searchParams.has('visitorId')) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'visitorId must not be supplied');
    }
    const lastKnownSeq = Number(url.searchParams.get('lastKnownSeq') || 0);
    if (!Number.isInteger(lastKnownSeq) || lastKnownSeq < 0) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid lastKnownSeq');
    }
    const session = await requireGuestSession(request, env);
    const stub = env.CHAT_CONVERSATIONS.get(
        env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
    );
    return stub.fetch(new Request(
        `https://internal/internal/conversations/ws?conversationId=${encodeURIComponent(conversationId)}`
            + `&visitorId=${encodeURIComponent(session.visitorId)}&lastKnownSeq=${lastKnownSeq}`,
        { headers: { Upgrade: 'websocket' } },
    ));
}

export async function handleGuestConversationDetail(
    request: Request,
    env: ChatPagesEnv,
    conversationId: string,
    messagesOnly = false,
): Promise<Response> {
    requireEnabled(env);
    if (!isPrefixedId(conversationId, 'conversation')) {
        throw new ChatProtocolError('NOT_FOUND', 'Conversation not found', 404);
    }
    const session = await requireGuestSession(request, env);
    const stub = env.CHAT_CONVERSATIONS.get(env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`));
    const url = new URL(request.url);
    const internal = new Request(`https://internal/internal/conversations/${messagesOnly ? 'messages' : 'detail'}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            conversationId,
            visitorId: session.visitorId,
            beforeSeq: url.searchParams.get('beforeSeq'),
            limit: url.searchParams.get('limit'),
        }),
    });
    const response = await stub.fetch(internal);
    return new Response(response.body, {
        status: response.status,
        headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
    });
}
