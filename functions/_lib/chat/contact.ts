import { ChatProtocolError } from '../../../support/shared/errors';
import { encodeBase64Url } from './base64url';

export interface ContactInput {
    name?: unknown;
    email?: unknown;
}

export interface NormalizedContact {
    name: string | null;
    email: string | null;
    emailLookupHash: string | null;
}

export interface ContactEnv {
    CHAT_CONTACT_LOOKUP_SECRET?: string;
}

export function normalizeEmail(value: string): string {
    return value.trim().normalize('NFKC').toLowerCase();
}

function normalizeName(value: unknown): string | null {
    if (value == null || value === '') return null;
    if (typeof value !== 'string') throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid contact name');
    const name = value.trim().replace(/\s+/g, ' ');
    if (name.length > 100) throw new ChatProtocolError('INVALID_PAYLOAD', 'Contact name is too long');
    return name || null;
}

async function lookupHash(email: string, env: ContactEnv): Promise<string> {
    const secret = String(env.CHAT_CONTACT_LOOKUP_SECRET || '');
    if (secret.length < 32) throw new Error('CHAT_CONTACT_LOOKUP_SECRET must be at least 32 characters');
    const key = await crypto.subtle.importKey(
        'raw',
        new TextEncoder().encode(secret),
        { name: 'HMAC', hash: 'SHA-256' },
        false,
        ['sign'],
    );
    const digest = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(email));
    return encodeBase64Url(new Uint8Array(digest));
}

export async function normalizeContact(
    input: ContactInput | null | undefined,
    env: ContactEnv,
): Promise<NormalizedContact> {
    const name = normalizeName(input?.name);
    if (input?.email == null || input.email === '') {
        return { name, email: null, emailLookupHash: null };
    }
    if (typeof input.email !== 'string') {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid contact email');
    }
    const email = normalizeEmail(input.email);
    if (email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid contact email');
    }
    return { name, email, emailLookupHash: await lookupHash(email, env) };
}
