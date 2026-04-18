/**
 * utils.js — utility condivise tra i moduli _lib del Worker.
 *
 * Tenere questo file leggero e senza dipendenze circolari.
 */

/** Timestamp ISO corrente. */
export function now() {
    return new Date().toISOString();
}

/**
 * JSON.parse sicuro con fallback.
 * @template T
 * @param {string|null|undefined} raw
 * @param {T} fallback
 * @returns {T}
 */
export function safeParseJSON(raw, fallback) {
    try { return JSON.parse(raw ?? 'null') ?? fallback; } catch (_) { return fallback; }
}
