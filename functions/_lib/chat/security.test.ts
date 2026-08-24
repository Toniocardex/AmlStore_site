import { env } from 'cloudflare:test';
import { beforeEach, describe, expect, it } from 'vitest';
import { createId } from '../../../support/shared/ids';
import {
    handleCreateConversation,
    handleGuestConversationDetail,
    handleGuestSession,
    handleGuestWebSocket,
    type ChatPagesEnv,
} from './gateway';
import { createGuestSession, encodeGuestSession } from './guest-session';
import { onRequest as adminOnRequest } from '../../admin/api/support/[[path]]';

const SITE_ORIGIN = 'https://aml-store.com';

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

/**
 * Test di sicurezza di base (ADR-CHAT-001 §93): questi sono i controlli
 * server-side esercitabili senza un browser reale. La difesa contro lo
 * stored XSS del corpo messaggio e' invece interamente client-side (vedi
 * components/support-chat.js e admin/support/support.js: solo
 * `.textContent`, mai `.innerHTML`, su testo proveniente dal guest) e va
 * verificata con un browser vero, non qui.
 */
describe('sicurezza — validazione Origin', () => {
    it('rifiuta una richiesta senza header Origin', async () => {
        const request = new Request(`${SITE_ORIGIN}/api/chat/session`, { method: 'POST', body: '{}' });
        await expect(handleGuestSession(request, gatewayEnv)).rejects.toMatchObject({
            code: 'FORBIDDEN',
            status: 403,
        });
    });

    it('rifiuta un Origin non in whitelist', async () => {
        const request = new Request(`${SITE_ORIGIN}/api/chat/session`, {
            method: 'POST',
            body: '{}',
            headers: { Origin: 'https://evil-phishing-clone.example' },
        });
        await expect(handleGuestSession(request, gatewayEnv)).rejects.toMatchObject({
            code: 'FORBIDDEN',
            status: 403,
        });
    });
});

describe('sicurezza — sessione guest e WebSocket', () => {
    it('rifiuta la creazione di una conversazione senza cookie di sessione', async () => {
        const request = new Request(`${SITE_ORIGIN}/api/chat/conversations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Origin: SITE_ORIGIN },
            body: JSON.stringify({ clientMessageId: createId('message'), body: 'ciao' }),
        });
        await expect(handleCreateConversation(request, gatewayEnv)).rejects.toMatchObject({
            code: 'UNAUTHORIZED',
            status: 401,
        });
    });

    it('rifiuta un upgrade WebSocket senza sessione valida, anche con un conversationId reale', async () => {
        const session = createGuestSession(gatewayEnv);
        const cookie = await encodeGuestSession(session, gatewayEnv);
        const create = await handleCreateConversation(
            new Request(`${SITE_ORIGIN}/api/chat/conversations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Origin: SITE_ORIGIN,
                    Cookie: `__Host-aml_chat_guest=${cookie}`,
                },
                body: JSON.stringify({ clientMessageId: createId('message'), body: 'ciao' }),
            }),
            gatewayEnv,
        );
        expect(create.status).toBe(201);
        const { conversationId } = await create.json<{ conversationId: string }>();

        // Nessun cookie: un aggressore che scoprisse un conversationId reale
        // (es. da un log) non deve poter aprire il canale realtime.
        const wsRequest = new Request(
            `${SITE_ORIGIN}/api/chat/conversations/${conversationId}/ws`,
            { headers: { Origin: SITE_ORIGIN, Upgrade: 'websocket' } },
        );
        await expect(handleGuestWebSocket(wsRequest, gatewayEnv, conversationId)).rejects.toMatchObject({
            code: 'UNAUTHORIZED',
            status: 401,
        });
    });

    it('rifiuta visitorId iniettato nel payload invece di derivarlo dal cookie', async () => {
        const session = createGuestSession(gatewayEnv);
        const cookie = await encodeGuestSession(session, gatewayEnv);
        const request = new Request(`${SITE_ORIGIN}/api/chat/conversations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Origin: SITE_ORIGIN,
                Cookie: `__Host-aml_chat_guest=${cookie}`,
            },
            // Un client malevolo tenta di impersonare un altro visitorId.
            body: JSON.stringify({
                clientMessageId: createId('message'),
                body: 'ciao',
                visitorId: createId('visitor'),
            }),
        });
        await expect(handleCreateConversation(request, gatewayEnv)).rejects.toMatchObject({
            code: 'INVALID_PAYLOAD',
        });
    });
});

describe('sicurezza — enumerazione conversationId e accesso cross-visitor', () => {
    it('un conversationId inesistente e uno di un altro visitor restituiscono lo stesso 404 generico', async () => {
        const sessionA = createGuestSession(gatewayEnv);
        const cookieA = await encodeGuestSession(sessionA, gatewayEnv);
        const create = await handleCreateConversation(
            new Request(`${SITE_ORIGIN}/api/chat/conversations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Origin: SITE_ORIGIN,
                    Cookie: `__Host-aml_chat_guest=${cookieA}`,
                },
                body: JSON.stringify({ clientMessageId: createId('message'), body: 'ciao' }),
            }),
            gatewayEnv,
        );
        const { conversationId: realId } = await create.json<{ conversationId: string }>();
        const fakeId = createId('conversation');

        const sessionB = createGuestSession(gatewayEnv);
        const cookieB = await encodeGuestSession(sessionB, gatewayEnv);
        const asVisitorB = (id: string) => handleGuestConversationDetail(
            new Request(`${SITE_ORIGIN}/api/chat/conversations/${id}`, {
                headers: { Cookie: `__Host-aml_chat_guest=${cookieB}` },
            }),
            gatewayEnv,
            id,
        );

        const [realFromB, fakeFromB] = await Promise.all([asVisitorB(realId), asVisitorB(fakeId)]);
        expect(realFromB.status).toBe(404);
        expect(fakeFromB.status).toBe(404);
        const [bodyReal, bodyFake] = await Promise.all([realFromB.json(), fakeFromB.json()]);
        // La risposta non deve rivelare se il conversationId esiste davvero:
        // stesso codice, stesso messaggio, indipendentemente dalla causa.
        expect(bodyReal).toEqual(bodyFake);
    });
});

describe('sicurezza — endpoint admin senza autenticazione', () => {
    it('rifiuta con 401 qualsiasi richiesta priva di JWT Cloudflare Access', async () => {
        const adminEnv = {
            DB: env.CHAT_DB,
            CHAT_CONVERSATIONS: env.CHAT_CONVERSATIONS,
            SUPPORT_HUB: env.SUPPORT_HUB,
            CHAT_ENABLED: '1',
            CF_ACCESS_AUD: 'test-aud',
            CF_ACCESS_TEAM_DOMAIN: 'test-team.cloudflareaccess.com',
            ADMIN_ALLOWED_EMAILS: 'ops@amlstore.it',
            ADMIN_DEV_BYPASS: '0',
            SITE_ORIGIN,
        };
        const request = new Request(`${SITE_ORIGIN}/admin/api/support/conversations`);
        const context = { request, env: adminEnv, params: { path: ['conversations'] } };
        // @ts-expect-error -- contesto minimale: la function legge solo request/env/params.path
        const response = await adminOnRequest(context);
        expect(response.status).toBe(401);
        const body = await response.json<{ error: { code: string } }>();
        expect(body.error.code).toBe('UNAUTHORIZED');
    });

    it('non concede accesso spacciandosi per un dominio diverso da aml-store.com', async () => {
        // Il bypass locale e' scoped a localhost/127.0.0.1: un host di
        // produzione non deve poterlo attivare nemmeno con ADMIN_DEV_BYPASS=1
        // impostato per errore.
        const adminEnv = {
            DB: env.CHAT_DB,
            CHAT_CONVERSATIONS: env.CHAT_CONVERSATIONS,
            SUPPORT_HUB: env.SUPPORT_HUB,
            CHAT_ENABLED: '1',
            CF_ACCESS_AUD: 'test-aud',
            CF_ACCESS_TEAM_DOMAIN: 'test-team.cloudflareaccess.com',
            ADMIN_ALLOWED_EMAILS: 'ops@amlstore.it',
            ADMIN_DEV_BYPASS: '1',
            SITE_ORIGIN,
        };
        const request = new Request(`${SITE_ORIGIN}/admin/api/support/conversations`);
        const context = { request, env: adminEnv, params: { path: ['conversations'] } };
        // @ts-expect-error -- contesto minimale: la function legge solo request/env/params.path
        const response = await adminOnRequest(context);
        expect(response.status).toBe(401);
    });
});
