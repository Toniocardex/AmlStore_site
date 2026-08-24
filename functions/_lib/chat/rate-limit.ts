import { ChatProtocolError } from '../../../support/shared/errors';
import { encodeBase64Url } from './base64url';
import { emitMetric } from '../../../workers/support-realtime/src/observability';

export interface RateLimitEnv {
    DB: D1Database;
    CHAT_GUEST_SESSION_SECRET?: string;
}

async function bucketKey(secret: string, scope: string, value: string): Promise<string> {
    const key = await crypto.subtle.importKey(
        'raw',
        new TextEncoder().encode(secret),
        { name: 'HMAC', hash: 'SHA-256' },
        false,
        ['sign'],
    );
    const signature = await crypto.subtle.sign(
        'HMAC',
        key,
        new TextEncoder().encode(`${scope}\n${value}`),
    );
    return encodeBase64Url(new Uint8Array(signature));
}

export async function consumeGlobalRateLimit(
    env: RateLimitEnv,
    scope: string,
    value: string,
    limit: number,
    windowMs: number,
    now = Date.now(),
): Promise<void> {
    const secret = env.CHAT_GUEST_SESSION_SECRET || '';
    if (secret.length < 32) {
        throw new ChatProtocolError('TEMPORARILY_UNAVAILABLE', 'Chat is unavailable', 503);
    }
    const key = await bucketKey(secret, scope, value);
    const windowStart = Math.floor(now / windowMs) * windowMs;
    const result = await env.DB.prepare(`
        INSERT INTO chat_rate_buckets (bucket_key, window_start, request_count, expires_at)
        VALUES (?, ?, 1, ?)
        ON CONFLICT(bucket_key, window_start) DO UPDATE SET
            request_count = request_count + 1
        RETURNING request_count
    `).bind(key, windowStart, windowStart + windowMs * 2).first<{ request_count: number }>();
    if (!result || result.request_count > limit) {
        emitMetric('chat_rate_limited_total', 1, { scope });
        throw new ChatProtocolError('RATE_LIMITED', 'Too many requests; retry later', 429);
    }
}

export function requestIp(request: Request): string {
    return request.headers.get('CF-Connecting-IP') || 'unknown';
}
