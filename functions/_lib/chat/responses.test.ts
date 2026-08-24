import { describe, expect, it } from 'vitest';
import { chatJson } from './responses';

describe('chatJson', () => {
    it('preserves Headers instances passed by the guest-session gateway', () => {
        const extra = new Headers({ 'Set-Cookie': 'guest=signed; Path=/; HttpOnly' });
        const response = chatJson({ ok: true }, 201, extra);

        expect(response.status).toBe(201);
        expect(response.headers.get('set-cookie')).toBe('guest=signed; Path=/; HttpOnly');
        expect(response.headers.get('cache-control')).toBe('no-store');
    });
});
