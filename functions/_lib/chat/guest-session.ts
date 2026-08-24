import { ChatProtocolError } from '../../../support/shared/errors';
import { createId, isPrefixedId } from '../../../support/shared/ids';
import { decodeBase64Url, decodeUtf8Base64Url, encodeBase64Url, encodeUtf8Base64Url } from './base64url';

export interface GuestSessionEnv {
    CHAT_GUEST_SESSION_SECRET?: string;
    CHAT_GUEST_SESSION_DAYS?: string;
    CHAT_GUEST_COOKIE_NAME?: string;
}

export interface GuestSession {
    version: 1;
    visitorId: string;
    issuedAt: number;
    expiresAt: number;
}

interface SignedGuestPayload {
    v: 1;
    vid: string;
    iat: number;
    exp: number;
}

const DEFAULT_COOKIE = '__Host-aml_chat_guest';
const DEFAULT_DAYS = 180;
const MIN_SECRET_LENGTH = 32;

function cookieName(env: GuestSessionEnv): string {
    const value = String(env.CHAT_GUEST_COOKIE_NAME || DEFAULT_COOKIE);
    if (!/^(?:__Host-)?[A-Za-z0-9_-]{1,64}$/.test(value)) {
        throw new Error('Invalid CHAT_GUEST_COOKIE_NAME');
    }
    return value;
}

function sessionDays(env: GuestSessionEnv): number {
    const value = Number(env.CHAT_GUEST_SESSION_DAYS || DEFAULT_DAYS);
    if (!Number.isInteger(value) || value <= 0 || value > 365) {
        throw new Error('CHAT_GUEST_SESSION_DAYS must be an integer between 1 and 365');
    }
    return value;
}

function secretValue(env: GuestSessionEnv): string {
    const secret = String(env.CHAT_GUEST_SESSION_SECRET || '');
    if (secret.length < MIN_SECRET_LENGTH) {
        throw new Error('CHAT_GUEST_SESSION_SECRET must be at least 32 characters');
    }
    return secret;
}

async function hmacKey(secret: string): Promise<CryptoKey> {
    return crypto.subtle.importKey(
        'raw',
        new TextEncoder().encode(secret),
        { name: 'HMAC', hash: 'SHA-256' },
        false,
        ['sign', 'verify'],
    );
}

async function sign(value: string, secret: string): Promise<string> {
    const signature = await crypto.subtle.sign(
        'HMAC',
        await hmacKey(secret),
        new TextEncoder().encode(value),
    );
    return encodeBase64Url(new Uint8Array(signature));
}

async function verifySignature(value: string, signature: string, secret: string): Promise<boolean> {
    try {
        return await crypto.subtle.verify(
            'HMAC',
            await hmacKey(secret),
            decodeBase64Url(signature),
            new TextEncoder().encode(value),
        );
    } catch {
        return false;
    }
}

function parseCookies(request: Request): Map<string, string> {
    const cookies = new Map<string, string>();
    for (const part of (request.headers.get('Cookie') || '').split(';')) {
        const separator = part.indexOf('=');
        if (separator <= 0) continue;
        cookies.set(part.slice(0, separator).trim(), part.slice(separator + 1).trim());
    }
    return cookies;
}

export async function encodeGuestSession(session: GuestSession, env: GuestSessionEnv): Promise<string> {
    const payload: SignedGuestPayload = {
        v: 1,
        vid: session.visitorId,
        iat: session.issuedAt,
        exp: session.expiresAt,
    };
    const encoded = encodeUtf8Base64Url(JSON.stringify(payload));
    return `v1.${encoded}.${await sign(`v1.${encoded}`, secretValue(env))}`;
}

export async function decodeGuestSession(
    value: string,
    env: GuestSessionEnv,
    now = Date.now(),
): Promise<GuestSession | null> {
    const parts = value.split('.');
    if (parts.length !== 3 || parts[0] !== 'v1') return null;
    if (!await verifySignature(`${parts[0]}.${parts[1]}`, parts[2], secretValue(env))) return null;
    try {
        const payload = JSON.parse(decodeUtf8Base64Url(parts[1])) as Partial<SignedGuestPayload>;
        if (payload.v !== 1 || !isPrefixedId(payload.vid, 'visitor')) return null;
        const issuedAt = payload.iat;
        const expiresAt = payload.exp;
        if (typeof issuedAt !== 'number' || !Number.isInteger(issuedAt)) return null;
        if (typeof expiresAt !== 'number' || !Number.isInteger(expiresAt)) return null;
        if (issuedAt > now + 60_000 || expiresAt <= now) return null;
        if (expiresAt <= issuedAt) return null;
        return {
            version: 1,
            visitorId: payload.vid,
            issuedAt,
            expiresAt,
        };
    } catch {
        return null;
    }
}

export async function readGuestSession(
    request: Request,
    env: GuestSessionEnv,
    now = Date.now(),
): Promise<GuestSession | null> {
    const raw = parseCookies(request).get(cookieName(env));
    return raw ? decodeGuestSession(raw, env, now) : null;
}

export function createGuestSession(env: GuestSessionEnv, now = Date.now()): GuestSession {
    return {
        version: 1,
        visitorId: createId('visitor'),
        issuedAt: now,
        expiresAt: now + sessionDays(env) * 86_400_000,
    };
}

export function shouldRenewGuestSession(session: GuestSession, now = Date.now()): boolean {
    const lifetime = session.expiresAt - session.issuedAt;
    return session.expiresAt - now <= lifetime * 0.2;
}

export function renewGuestSession(session: GuestSession, env: GuestSessionEnv, now = Date.now()): GuestSession {
    return {
        ...session,
        issuedAt: now,
        expiresAt: now + sessionDays(env) * 86_400_000,
    };
}

export async function serializeGuestCookie(
    session: GuestSession,
    env: GuestSessionEnv,
    request: Request,
): Promise<string> {
    const isHttps = new URL(request.url).protocol === 'https:';
    const maxAge = Math.max(0, Math.floor((session.expiresAt - Date.now()) / 1_000));
    const parts = [
        `${cookieName(env)}=${await encodeGuestSession(session, env)}`,
        'Path=/',
        `Max-Age=${maxAge}`,
        'HttpOnly',
        'SameSite=Lax',
    ];
    if (isHttps) parts.push('Secure');
    return parts.join('; ');
}

export async function requireGuestSession(request: Request, env: GuestSessionEnv): Promise<GuestSession> {
    const session = await readGuestSession(request, env);
    if (!session) {
        throw new ChatProtocolError('UNAUTHORIZED', 'Valid guest session required', 401);
    }
    return session;
}

export async function deriveConversationId(
    visitorId: string,
    clientMessageId: string,
    env: GuestSessionEnv,
): Promise<string> {
    const input = `conversation:v1:${visitorId}:${clientMessageId}`;
    const digest = await crypto.subtle.sign(
        'HMAC',
        await hmacKey(secretValue(env)),
        new TextEncoder().encode(input),
    );
    return `conv_${encodeBase64Url(new Uint8Array(digest).slice(0, 24))}`;
}
