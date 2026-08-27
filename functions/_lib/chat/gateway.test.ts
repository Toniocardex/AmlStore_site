import { env } from 'cloudflare:test';
import { beforeEach, describe, expect, it } from 'vitest';
import { createId } from '../../../support/shared/ids';
import { handleCreateConversation, type ChatPagesEnv } from './gateway';
import {
    createGuestSession,
    deriveConversationId,
    encodeGuestSession,
} from './guest-session';

const SITE_ORIGIN = 'https://eurolicenze.com';

const gatewayEnv = {
    DB: env.CHAT_DB,
    CHAT_CONVERSATIONS: env.CHAT_CONVERSATIONS,
    SUPPORT_HUB: env.SUPPORT_HUB,
    CHAT_ENABLED: '1',
    CHAT_GUEST_SESSION_SECRET: 'test-only-guest-session-secret-at-least-32-chars',
    CHAT_CONTACT_LOOKUP_SECRET: 'test-only-contact-lookup-secret-at-least-32-chars',
    CHAT_GUEST_COOKIE_NAME: '__Host-aml_chat_guest',
    SITE_ORIGIN,
} as unknown as ChatPagesEnv;

beforeEach(async () => {
    const queries = JSON.parse(env.CHAT_CORE_MIGRATION_QUERIES) as string[];
    await env.CHAT_DB.batch(queries.map((query) => env.CHAT_DB.prepare(query)));
});

async function createRequest(cookie: string, clientMessageId: string): Promise<Request> {
    return new Request(`${SITE_ORIGIN}/api/chat/conversations`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Origin: SITE_ORIGIN,
            Cookie: `__Host-aml_chat_guest=${cookie}`,
        },
        body: JSON.stringify({
            clientMessageId,
            body: 'Buongiorno, avrei bisogno di informazioni.',
            pagePath: '/it/office-2024-home-business',
            locale: 'it',
        }),
    });
}

describe('guest conversation creation', () => {
    it('creates the conversation and its D1 projection from the first message', async () => {
        const session = createGuestSession(gatewayEnv);
        const cookie = await encodeGuestSession(session, gatewayEnv);
        const clientMessageId = createId('message');

        const response = await handleCreateConversation(
            await createRequest(cookie, clientMessageId),
            gatewayEnv,
        );
        expect(response.status).toBe(201);

        const conversationId = await deriveConversationId(
            session.visitorId, clientMessageId, gatewayEnv,
        );
        await expect.poll(async () => env.CHAT_DB.prepare(`
            SELECT visitor_id, status, last_seq FROM chat_conversations WHERE id = ?
        `).bind(conversationId).first<Record<string, unknown>>()).toMatchObject({
            visitor_id: session.visitorId,
            status: 'OPEN',
            last_seq: 1,
        });
    });

    it('never resurrects a purged conversation and lets a new contact open a new one', async () => {
        const session = createGuestSession(gatewayEnv);
        const cookie = await encodeGuestSession(session, gatewayEnv);
        const clientMessageId = createId('message');
        const conversationId = await deriveConversationId(
            session.visitorId, clientMessageId, gatewayEnv,
        );
        await env.CHAT_DB.prepare(`
            INSERT INTO chat_conversation_tombstones (conversation_id, purged_at, deletion_reason)
            VALUES (?, ?, 'retention')
        `).bind(conversationId, Date.now()).run();

        // Il route handler mappa l'errore in 410 tramite chatError().
        await expect(handleCreateConversation(
            await createRequest(cookie, clientMessageId),
            gatewayEnv,
        )).rejects.toMatchObject({ code: 'CONVERSATION_PURGED', status: 410 });

        // Lo storage del Durable Object non deve essere stato reinizializzato.
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        const detail = await stub.fetch('https://internal/internal/conversations/detail', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ conversationId, visitorId: session.visitorId }),
        });
        expect(detail.status).toBe(404);
        expect(await env.CHAT_DB.prepare('SELECT id FROM chat_conversations WHERE id = ?')
            .bind(conversationId).first()).toBeNull();

        const fresh = await handleCreateConversation(
            await createRequest(cookie, createId('message')),
            gatewayEnv,
        );
        expect(fresh.status).toBe(201);
    });
});
