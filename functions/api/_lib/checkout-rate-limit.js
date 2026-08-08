/**
 * checkout-rate-limit.js — ponte antispam pre-createOrder (ADR-001).
 *
 * Limite per email normalizzata (HMAC): max 3 tentativi per finestra.
 * Fail-closed se manca FRAUD_HASH_SECRET o D1 non disponibile.
 */

import { windowSlot, retryAfterForWindow, hmacIdentifier, bumpBucket } from './rate-limit.js';

/** Massimo tentativi ammessi per email in ciascuna finestra corta. */
export const CHECKOUT_EMAIL_MAX_ATTEMPTS = 3;

const WINDOWS = [
    { name: '10m', ms: 10 * 60 * 1000, max: CHECKOUT_EMAIL_MAX_ATTEMPTS },
    { name: '30m', ms: 30 * 60 * 1000, max: CHECKOUT_EMAIL_MAX_ATTEMPTS },
    { name: '24h', ms: 24 * 60 * 60 * 1000, max: 8 },
];

function normalizeEmail(email) {
    return String(email || '').trim().toLowerCase();
}

/**
 * Applica rate limit per email. Da chiamare solo per nuovi checkout
 * (non per riuso della stessa idempotency_key).
 *
 * @param {object} env
 * @param {string} customerEmail
 * @returns {Promise<null | { limited: true, retryAfter: number, message: string, code: string }>}
 */
export async function checkCheckoutEmailRateLimit(env, customerEmail) {
    const secret = env.FRAUD_HASH_SECRET;
    if (!secret || String(secret).length < 16) {
        console.error('[rate-limit] FRAUD_HASH_SECRET mancante o troppo corto');
        return {
            limited: true,
            retryAfter: 60,
            message: 'Checkout temporarily unavailable. Please try again later.',
            code: 'PROTECTION_UNAVAILABLE',
            status: 503,
        };
    }
    if (!env.DB) {
        console.error('[rate-limit] DB binding mancante');
        return {
            limited: true,
            retryAfter: 60,
            message: 'Checkout temporarily unavailable. Please try again later.',
            code: 'PROTECTION_UNAVAILABLE',
            status: 503,
        };
    }

    const email = normalizeEmail(customerEmail);
    if (!email) {
        return {
            limited: true,
            retryAfter: 60,
            message: 'Invalid email',
            code: 'CHECKOUT_RATE_LIMITED',
            status: 400,
        };
    }

    const t = Date.now();
    let emailHash;
    try {
        emailHash = await hmacIdentifier(secret, 'email', email);
    } catch (e) {
        console.error('[rate-limit] HMAC failed:', e?.message || e);
        return {
            limited: true,
            retryAfter: 60,
            message: 'Checkout temporarily unavailable. Please try again later.',
            code: 'PROTECTION_UNAVAILABLE',
            status: 503,
        };
    }

    const bucketKey = `email:${emailHash}`;

    try {
        for (const w of WINDOWS) {
            const windowId = `${w.name}:${windowSlot(w.ms, t)}`;
            const count = await bumpBucket(env.DB, bucketKey, windowId);
            if (count > w.max) {
                const retryAfter = retryAfterForWindow(w.ms, t);
                console.warn('[rate-limit] blocked', {
                    window: w.name,
                    count,
                    max: w.max,
                    retryAfter,
                });
                return {
                    limited: true,
                    retryAfter,
                    message: 'Too many checkout attempts. Please try again later.',
                    code: 'CHECKOUT_RATE_LIMITED',
                    status: 429,
                };
            }
        }
    } catch (e) {
        console.error('[rate-limit] D1 error (fail closed):', e?.message || e);
        return {
            limited: true,
            retryAfter: 60,
            message: 'Checkout temporarily unavailable. Please try again later.',
            code: 'PROTECTION_UNAVAILABLE',
            status: 503,
        };
    }

    return null;
}
