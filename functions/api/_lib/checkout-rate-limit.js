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

/** Finestra e soglia per l'IP sull'express-create: nessuna email disponibile
 *  a questo punto del flusso (PayPal la fornisce solo alla cattura), quindi
 *  l'unico freno possibile prima di chiamare l'API PayPal è per IP. */
const EXPRESS_IP_WINDOW_MS = 10 * 60 * 1000;
const EXPRESS_IP_MAX_ATTEMPTS = 10;

/**
 * Rate limit per IP sulla creazione di un ordine PayPal Express (nuovo
 * checkout, non riuso di idempotency_key). Fail-open: un errore qui non deve
 * mai impedire un acquisto legittimo.
 *
 * @param {object} env
 * @param {Request} request
 * @returns {Promise<null | { limited: true, retryAfter: number, message: string, code: string, status: number }>}
 */
export async function checkExpressCheckoutIpRateLimit(env, request) {
    const secret = env.FRAUD_HASH_SECRET;
    if (!secret || !env.DB) return null;

    const ip = request.headers.get('CF-Connecting-IP') || '';
    if (!ip) return null;

    try {
        const ipHash = await hmacIdentifier(secret, 'pp-express-ip', ip);
        const bucketKey = `pp-express:${ipHash}`;
        const windowId = `10m:${windowSlot(EXPRESS_IP_WINDOW_MS)}`;
        const count = await bumpBucket(env.DB, bucketKey, windowId);
        if (count > EXPRESS_IP_MAX_ATTEMPTS) {
            return {
                limited: true,
                retryAfter: retryAfterForWindow(EXPRESS_IP_WINDOW_MS),
                message: 'Too many checkout attempts. Please try again later.',
                code: 'CHECKOUT_RATE_LIMITED',
                status: 429,
            };
        }
    } catch (e) {
        console.warn('[rate-limit] express IP check failed (fail-open):', e?.message || e);
    }
    return null;
}

/** Finestra e soglia per l'IP sullo Stripe Express (wallet 1-click).
 *  Soglia piu' bassa del gemello PayPal e bucket separato: qui l'endpoint
 *  restituisce un clientSecret, cioe' una credenziale di pagamento confermabile
 *  dal browser con la sola publishable key. Il gemello PayPal restituisce invece
 *  un order id che si puo' pagare solo passando dall'interfaccia PayPal, quindi
 *  non regge lo stesso modello di minaccia (vedi ADR-001 §3.2 T7). */
const STRIPE_EXPRESS_IP_WINDOW_MS = 10 * 60 * 1000;
const STRIPE_EXPRESS_IP_MAX_ATTEMPTS = 5;

/**
 * Rate limit per IP sulla creazione di un PaymentIntent Stripe Express.
 *
 * Fail-CLOSED sugli errori D1, al contrario del gemello PayPal: su questo path
 * il controllo per email (`checkCheckoutEmailRateLimit`, gia' fail-closed) e'
 * comunque primario, quindi un D1 non raggiungibile blocca il checkout in ogni
 * caso — restare fail-open qui darebbe solo l'illusione di un secondo livello.
 *
 * Un header CF-Connecting-IP assente NON blocca: in produzione Cloudflare lo
 * imposta sempre, in `wrangler pages dev` non esiste, e il freno per email
 * resta attivo in entrambi i casi.
 *
 * @param {object} env
 * @param {Request} request
 * @returns {Promise<null | { limited: true, retryAfter: number, message: string, code: string, status: number }>}
 */
export async function checkStripeExpressIpRateLimit(env, request) {
    const secret = env.FRAUD_HASH_SECRET;
    if (!secret || !env.DB) return null;

    const ip = request.headers.get('CF-Connecting-IP') || '';
    if (!ip) return null;

    try {
        const ipHash = await hmacIdentifier(secret, 'st-express-ip', ip);
        const bucketKey = `st-express:${ipHash}`;
        const windowId = `10m:${windowSlot(STRIPE_EXPRESS_IP_WINDOW_MS)}`;
        const count = await bumpBucket(env.DB, bucketKey, windowId);
        if (count > STRIPE_EXPRESS_IP_MAX_ATTEMPTS) {
            console.warn('[rate-limit] stripe express IP blocked', {
                count,
                max: STRIPE_EXPRESS_IP_MAX_ATTEMPTS,
            });
            return {
                limited: true,
                retryAfter: retryAfterForWindow(STRIPE_EXPRESS_IP_WINDOW_MS),
                message: 'Too many checkout attempts. Please try again later.',
                code: 'CHECKOUT_RATE_LIMITED',
                status: 429,
            };
        }
    } catch (e) {
        console.error('[rate-limit] stripe express IP check failed (fail closed):', e?.message || e);
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
