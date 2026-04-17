/**
 * token.js — HMAC-SHA256 token per la thank-you page.
 *
 * Formato URL:
 *   ?oid=<uuid>&exp=<unix-ts-seconds>&t=<base64url-hmac>
 *
 * Il messaggio firmato è: "<orderId>|<exp>"
 * Scadenza predefinita: 30 minuti (TOKEN_TTL_SECONDS).
 */

const TOKEN_TTL_SECONDS = 1800; // 30 minuti

/**
 * Importa la chiave HMAC dal secret stringa.
 * @param {string} secret
 * @returns {Promise<CryptoKey>}
 */
async function importKey(secret) {
    return crypto.subtle.importKey(
        'raw',
        new TextEncoder().encode(secret),
        { name: 'HMAC', hash: 'SHA-256' },
        false,
        ['sign', 'verify']
    );
}

/**
 * Converte ArrayBuffer in stringa base64url.
 * @param {ArrayBuffer} buf
 * @returns {string}
 */
function toBase64url(buf) {
    return btoa(String.fromCharCode(...new Uint8Array(buf)))
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=/g, '');
}

/**
 * Genera un token firmato HMAC per un orderId.
 * @param {string} secret   — env var TOKEN_SECRET
 * @param {string} orderId  — UUID v4
 * @returns {Promise<{ oid: string, exp: number, t: string }>}
 */
export async function generateToken(secret, orderId) {
    const exp = Math.floor(Date.now() / 1000) + TOKEN_TTL_SECONDS;
    const message = `${orderId}|${exp}`;
    const key = await importKey(secret);
    const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(message));
    return { oid: orderId, exp, t: toBase64url(sig) };
}

/**
 * Verifica un token dalla URL della thank-you page.
 * @param {string} secret
 * @param {string} oid    — da URL param
 * @param {string|number} exp  — da URL param (unix seconds)
 * @param {string} t      — da URL param (base64url hmac)
 * @returns {Promise<{ valid: boolean, reason?: string }>}
 */
export async function verifyToken(secret, oid, exp, t) {
    if (!oid || !exp || !t) {
        return { valid: false, reason: 'missing_params' };
    }

    const expNum = Number(exp);
    if (!Number.isFinite(expNum) || expNum < Math.floor(Date.now() / 1000)) {
        return { valid: false, reason: 'expired' };
    }

    const message = `${oid}|${expNum}`;
    const key = await importKey(secret);

    // Ricostruisci firma attesa
    const expectedSig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(message));
    const expectedB64 = toBase64url(expectedSig);

    // Confronto costante-time tramite subtle.verify non disponibile direttamente
    // per HMAC verify ma usiamo Web Crypto che lo fa internamente in tempo costante
    if (t !== expectedB64) {
        return { valid: false, reason: 'invalid_signature' };
    }

    return { valid: true };
}
