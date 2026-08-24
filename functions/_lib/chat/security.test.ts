import { env } from 'cloudflare:test';
import { beforeEach, describe, expect, it } from 'vitest';
import { createId } from '../../../support/shared/ids';
import { encodeBase64Url, encodeUtf8Base64Url } from './base64url';
import {
    handleCreateConversation,
    handleGuestConversationDetail,
    handleGuestSession,
    handleGuestWebSocket,
    handleSendGuestMessage,
    type ChatPagesEnv,
} from './gateway';
import { createGuestSession, encodeGuestSession } from './guest-session';
import { consumeGlobalRateLimit } from './rate-limit';
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

    it('rifiuta un JWT Cloudflare Access scaduto prima di verificarne la firma', async () => {
        // L'header/payload di un JWT sono base64url-JSON leggibili senza
        // verificarne la firma: la scadenza va controllata PRIMA di
        // raggiungere il JWKS remoto, altrimenti un token scaduto ma ancora
        // strutturalmente valido continuerebbe a fare rete inutilmente (e in
        // un mondo con un bug nel controllo dell'ordine, rischierebbe di
        // essere accettato se la verifica della firma fosse permissiva).
        const expiredPayload = {
            email: 'ops@amlstore.it',
            aud: 'test-aud',
            exp: Math.floor(Date.now() / 1000) - 3600,
        };
        const header = encodeUtf8Base64Url(JSON.stringify({ alg: 'RS256', kid: 'test-kid' }));
        const payload = encodeUtf8Base64Url(JSON.stringify(expiredPayload));
        const bogusSignature = encodeBase64Url(new Uint8Array([1, 2, 3, 4]));
        const expiredJwt = `${header}.${payload}.${bogusSignature}`;

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
        const request = new Request(`${SITE_ORIGIN}/admin/api/support/conversations`, {
            headers: { 'Cf-Access-Jwt-Assertion': expiredJwt },
        });
        const context = { request, env: adminEnv, params: { path: ['conversations'] } };
        // @ts-expect-error -- contesto minimale: la function legge solo request/env/params.path
        const response = await adminOnRequest(context);
        expect(response.status).toBe(401);
    });
});

describe('sicurezza — WebSocket cross-origin', () => {
    it('rifiuta un upgrade WebSocket da un Origin non in whitelist, prima di leggere la sessione', async () => {
        const conversationId = createId('conversation');
        const wsRequest = new Request(
            `${SITE_ORIGIN}/api/chat/conversations/${conversationId}/ws`,
            { headers: { Origin: 'https://attacker-site.example', Upgrade: 'websocket' } },
        );
        await expect(handleGuestWebSocket(wsRequest, gatewayEnv, conversationId)).rejects.toMatchObject({
            code: 'FORBIDDEN',
            status: 403,
        });
    });

    it('rifiuta un upgrade WebSocket senza header Origin', async () => {
        const conversationId = createId('conversation');
        const wsRequest = new Request(
            `${SITE_ORIGIN}/api/chat/conversations/${conversationId}/ws`,
            { headers: { Upgrade: 'websocket' } },
        );
        await expect(handleGuestWebSocket(wsRequest, gatewayEnv, conversationId)).rejects.toMatchObject({
            code: 'FORBIDDEN',
            status: 403,
        });
    });
});

describe('sicurezza — spam burst su volumi realistici', () => {
    it('il rate limiter globale rifiuta esattamente dalla richiesta successiva al limite configurato', async () => {
        // Stesso primitivo (consumeGlobalRateLimit) usato da tutti gli
        // endpoint pubblici della chat: un burst di 121 richieste nella
        // stessa finestra simula un singolo visitor malevolo che martella
        // message-send su piu' conversazioni per aggirare il cap per-DO
        // (20/min per conversazione, non globale per visitor).
        const scope = 'message-send:visitor';
        const value = createId('visitor');
        const limit = 120;
        const now = Date.now();
        const outcomes: Array<'ok' | 'limited'> = [];
        for (let i = 0; i < limit + 5; i += 1) {
            try {
                await consumeGlobalRateLimit(gatewayEnv, scope, value, limit, 10 * 60_000, now);
                outcomes.push('ok');
            } catch (error) {
                outcomes.push('limited');
            }
        }
        expect(outcomes.filter((o) => o === 'ok')).toHaveLength(limit);
        expect(outcomes.slice(limit).every((o) => o === 'limited')).toBe(true);
    });
});

describe('sicurezza — replay idempotente su larga scala', () => {
    it('50 invii concorrenti dello stesso clientMessageId producono un solo messaggio', async () => {
        // handleSendGuestMessage (limite 120/10min) invece di
        // handleCreateConversation (limite 8/10min): con la creazione, 50
        // richieste concorrenti sulla STESSA sessione farebbero scattare il
        // rate limiter ben prima di poter osservare l'idempotenza — non e'
        // quello che si vuole isolare qui.
        const session = createGuestSession(gatewayEnv);
        const cookie = await encodeGuestSession(session, gatewayEnv);
        const created = await handleCreateConversation(
            new Request(`${SITE_ORIGIN}/api/chat/conversations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Origin: SITE_ORIGIN,
                    Cookie: `__Host-aml_chat_guest=${cookie}`,
                },
                body: JSON.stringify({ clientMessageId: createId('message'), body: 'primo messaggio' }),
            }),
            gatewayEnv,
        );
        const { conversationId } = await created.json<{ conversationId: string }>();

        const clientMessageId = createId('message');
        const sendOnce = () => handleSendGuestMessage(
            new Request(`${SITE_ORIGIN}/api/chat/conversations/${conversationId}/messages`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Origin: SITE_ORIGIN,
                    Cookie: `__Host-aml_chat_guest=${cookie}`,
                },
                body: JSON.stringify({ clientMessageId, body: 'replay burst' }),
            }),
            gatewayEnv,
            conversationId,
        );

        const responses = await Promise.all(Array.from({ length: 50 }, sendOnce));
        expect(responses.every((r) => r.status === 201)).toBe(true);
        const bodies = await Promise.all(responses.map((r) => r.json<{ eventId: string; seq: number }>()));
        expect(new Set(bodies.map((b) => b.eventId)).size).toBe(1);
        expect(new Set(bodies.map((b) => b.seq)).size).toBe(1);

        await expect.poll(async () => env.CHAT_DB.prepare(
            'SELECT last_seq FROM chat_conversations WHERE id = ?',
        ).bind(conversationId).first<{ last_seq: number }>()).toMatchObject({ last_seq: 2 });
    });
});
