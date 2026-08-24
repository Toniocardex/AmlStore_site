import { describe, expect, it } from 'vitest';
import { createId } from '../../../support/shared/ids';
import {
    createGuestSession,
    decodeGuestSession,
    deriveConversationId,
    encodeGuestSession,
    readGuestSession,
    serializeGuestCookie,
} from './guest-session';

const env = {
    CHAT_GUEST_SESSION_SECRET: 'test-only-guest-session-secret-at-least-32-chars',
    CHAT_GUEST_SESSION_DAYS: '180',
    CHAT_GUEST_COOKIE_NAME: '__Host-aml_chat_guest',
};

describe('signed guest session', () => {
    it('round-trips a signed HttpOnly session', async () => {
        const now = 1_800_000_000_000;
        const session = createGuestSession(env, now);
        const encoded = await encodeGuestSession(session, env);
        await expect(decodeGuestSession(encoded, env, now + 1_000)).resolves.toEqual(session);

        const cookie = await serializeGuestCookie(
            session,
            env,
            new Request('https://aml-store.com/api/chat/session'),
        );
        expect(cookie).toContain('HttpOnly');
        expect(cookie).toContain('Secure');
        expect(cookie).toContain('SameSite=Lax');
    });

    it('rejects a tampered cookie', async () => {
        const session = createGuestSession(env);
        const encoded = await encodeGuestSession(session, env);
        const parts = encoded.split('.');
        const middle = Math.floor(parts[1].length / 2);
        parts[1] = `${parts[1].slice(0, middle)}${parts[1][middle] === 'A' ? 'B' : 'A'}${parts[1].slice(middle + 1)}`;
        const tampered = parts.join('.');
        await expect(decodeGuestSession(tampered, env)).resolves.toBeNull();
    });

    it('does not trust a raw visitor cookie', async () => {
        const request = new Request('https://aml-store.com/api/chat/conversations', {
            headers: { Cookie: `__Host-aml_chat_guest=${createId('visitor')}` },
        });
        await expect(readGuestSession(request, env)).resolves.toBeNull();
    });

    it('derives a stable opaque conversation id for first-message retries', async () => {
        const visitorId = createId('visitor');
        const clientMessageId = createId('message');
        const first = await deriveConversationId(visitorId, clientMessageId, env);
        const retry = await deriveConversationId(visitorId, clientMessageId, env);
        const other = await deriveConversationId(visitorId, createId('message'), env);
        expect(retry).toBe(first);
        expect(other).not.toBe(first);
        expect(first).toMatch(/^conv_[A-Za-z0-9_-]+$/);
        expect(first).not.toContain(visitorId);
    });
});
