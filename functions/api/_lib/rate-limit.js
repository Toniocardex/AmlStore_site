/**
 * rate-limit.js — primitive generiche di rate limiting su D1 (tabella
 * checkout_rate_buckets), condivise da checkout-rate-limit.js (email) e
 * cart.js (IP su /api/cart/sync).
 */

import { now } from './utils.js';

export function windowSlot(windowMs, t = Date.now()) {
    return Math.floor(t / windowMs);
}

export function retryAfterForWindow(windowMs, t = Date.now()) {
    const slot = windowSlot(windowMs, t);
    const end = (slot + 1) * windowMs;
    return Math.max(1, Math.ceil((end - t) / 1000));
}

/**
 * HMAC-SHA256 esadecimale di `kind:value`, versionato per poter ruotare
 * lo schema in futuro senza ambiguità tra bucket vecchi e nuovi.
 */
export async function hmacIdentifier(secret, kind, value, version = 1) {
    const key = await crypto.subtle.importKey(
        'raw',
        new TextEncoder().encode(secret),
        { name: 'HMAC', hash: 'SHA-256' },
        false,
        ['sign']
    );
    const payload = `${version}:${kind}:${value}`;
    const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(payload));
    return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

/**
 * Incrementa atomicamente il bucket (bucket_key, window_id) e restituisce il nuovo count.
 * @param {D1Database} db
 * @param {string} bucketKey
 * @param {string} windowId
 * @returns {Promise<number>}
 */
export async function bumpBucket(db, bucketKey, windowId) {
    const ts = now();
    const row = await db
        .prepare(
            `INSERT INTO checkout_rate_buckets (bucket_key, window_id, count, updated_at)
             VALUES (?, ?, 1, ?)
             ON CONFLICT(bucket_key, window_id) DO UPDATE SET
               count = count + 1,
               updated_at = excluded.updated_at
             RETURNING count`
        )
        .bind(bucketKey, windowId, ts)
        .first();
    return Number(row?.count || 0);
}
