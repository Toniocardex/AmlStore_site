import { ChatProtocolError } from '../../../support/shared/errors';
import { decodeBase64Url } from './base64url';
import { normalizeEmail } from './contact';

export interface OrderTokenInput {
    oid?: unknown;
    exp?: unknown;
    t?: unknown;
}

export interface OrderContextEnv {
    DB: D1Database;
    TOKEN_SECRET?: string;
}

export interface VerifiedOrderContext {
    orderId: string;
    customerEmail: string | null;
}

function uuid(value: unknown): value is string {
    return typeof value === 'string'
        && /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value);
}

function base64UrlBytes(value: string): Uint8Array<ArrayBuffer> {
    try { return decodeBase64Url(value); } catch { return new Uint8Array(new ArrayBuffer(0)); }
}

export async function verifyOrderContext(
    input: OrderTokenInput | null | undefined,
    env: OrderContextEnv,
): Promise<VerifiedOrderContext | null> {
    if (!input) return null;
    if (!uuid(input.oid) || typeof input.t !== 'string') {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid order token');
    }
    const exp = Number(input.exp);
    if (!Number.isInteger(exp) || exp < Math.floor(Date.now() / 1_000)) {
        throw new ChatProtocolError('FORBIDDEN', 'Order token expired', 403);
    }
    const secret = String(env.TOKEN_SECRET || '');
    if (secret.length < 32) throw new Error('TOKEN_SECRET must be at least 32 characters');
    const key = await crypto.subtle.importKey(
        'raw',
        new TextEncoder().encode(secret),
        { name: 'HMAC', hash: 'SHA-256' },
        false,
        ['verify'],
    );
    const valid = await crypto.subtle.verify(
        'HMAC',
        key,
        base64UrlBytes(input.t),
        new TextEncoder().encode(`${input.oid}|${exp}`),
    );
    if (!valid) throw new ChatProtocolError('FORBIDDEN', 'Invalid order token', 403);

    const order = await env.DB.prepare(
        'SELECT id, customer_email FROM orders WHERE id = ?',
    ).bind(input.oid).first<{ id: string; customer_email: string | null }>();
    if (!order) throw new ChatProtocolError('NOT_FOUND', 'Order not found', 404);
    return {
        orderId: order.id,
        customerEmail: order.customer_email ? normalizeEmail(order.customer_email) : null,
    };
}
