/**
 * restock.js — richieste "Avvisami quando torna disponibile" sugli SKU fisici.
 *
 * Serve a due cose insieme, e la seconda e' quella che conta di piu' per il
 * negozio: avvisare chi ha lasciato l'indirizzo, e misurare quanta domanda
 * resta scoperta mentre un articolo e' esaurito (vedi la colonna "In attesa"
 * nella tab Magazzino dell'Admin).
 *
 * Il dato personale ha vita breve: l'email viene azzerata subito dopo l'invio,
 * la riga sopravvive come conteggio anonimo. Vedi schema-restock-migration.sql.
 */

import { isPhysicalSku } from './stock.js';
import { now } from './utils.js';
import { windowSlot, retryAfterForWindow, hmacIdentifier, bumpBucket } from './rate-limit.js';

/** Lingue con una PDP pubblicata: fuori da questo insieme non si iscrive. */
export const RESTOCK_LOCALES = new Set(['it', 'en', 'de', 'fr', 'es', 'nl', 'pt']);

/** Resend accetta al massimo 100 messaggi per chiamata batch. */
const NOTIFY_CHUNK = 100;

export function normalizeRestockEmail(email) {
    return String(email || '').trim().toLowerCase().slice(0, 254);
}

export function isValidRestockEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(email || ''));
}

/**
 * Path della PDP di provenienza, usato per il link nell'email di ritorno
 * disponibilita'. Si accetta solo un path interno della lingua dichiarata:
 * finisce dentro un'email, quindi non deve poter diventare un rimando altrove.
 *
 * @returns {string} path normalizzato, o '/<lang>/' se non utilizzabile
 */
export function safeRestockPath(raw, lang) {
    const locale = RESTOCK_LOCALES.has(lang) ? lang : 'it';
    const fallback = `/${locale}/`;
    const path = String(raw || '').trim().slice(0, 240);
    if (!path.startsWith(`/${locale}/`)) return fallback;
    if (path.includes('//') || path.includes('..') || /[\s<>"'\\]/.test(path)) return fallback;
    return path;
}

function randomToken() {
    const bytes = new Uint8Array(16);
    crypto.getRandomValues(bytes);
    return [...bytes].map((b) => b.toString(16).padStart(2, '0')).join('');
}

/**
 * Registra un'iscrizione. Idempotente per (sku, email): una seconda richiesta
 * dallo stesso indirizzo non crea una riga nuova e non e' un errore per chi
 * scrive — dal punto di vista del cliente l'esito e' identico.
 *
 * @param {D1Database} db
 * @returns {Promise<{ ok: boolean, duplicate?: boolean, reason?: string }>}
 */
export async function createRestockRequest(db, { sku, email, lang, pagePath, ipHash }) {
    const key = String(sku || '').trim();
    if (!isPhysicalSku(key)) return { ok: false, reason: 'not_physical' };

    const locale = RESTOCK_LOCALES.has(lang) ? lang : 'it';
    const addr = normalizeRestockEmail(email);
    if (!isValidRestockEmail(addr)) return { ok: false, reason: 'invalid_email' };

    try {
        const res = await db.prepare(`
            INSERT INTO restock_requests
                (id, sku, email, lang, page_path, token, created_at, notified_at, ip_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?)
            ON CONFLICT(sku, email) DO NOTHING
        `).bind(
            crypto.randomUUID(), key, addr, locale,
            safeRestockPath(pagePath, locale), randomToken(), now(), ipHash || null
        ).run();

        const changes = res?.meta?.changes ?? 0;
        return { ok: true, duplicate: changes === 0 };
    } catch (e) {
        console.error('[restock] insert fallito:', e?.message || e);
        return { ok: false, reason: 'db_error' };
    }
}

/**
 * Conteggio delle iscrizioni in attesa per ogni SKU fisico.
 * @param {D1Database} db
 * @returns {Promise<Map<string, { pending: number, lastAt: string|null }>>}
 */
export async function pendingCountsBySku(db) {
    const map = new Map();
    try {
        const rows = await db.prepare(`
            SELECT sku, COUNT(*) AS pending, MAX(created_at) AS last_at
            FROM restock_requests
            WHERE notified_at IS NULL AND email IS NOT NULL
            GROUP BY sku
        `).all();
        for (const r of rows.results || []) {
            map.set(String(r.sku), {
                pending: Number(r.pending) || 0,
                lastAt: r.last_at || null,
            });
        }
    } catch (e) {
        // La tab Magazzino deve restare utilizzabile anche prima della
        // migrazione: senza tabella si mostra zero, non un errore.
        console.warn('[restock] conteggi non disponibili:', e?.message || e);
    }
    return map;
}

/**
 * Iscrizioni in attesa per un singolo SKU, dalla piu' vecchia.
 * @param {D1Database} db
 */
export async function listPendingForSku(db, sku) {
    const key = String(sku || '').trim();
    if (!key) return [];
    const rows = await db.prepare(`
        SELECT id, email, lang, page_path, created_at
        FROM restock_requests
        WHERE sku = ? AND notified_at IS NULL AND email IS NOT NULL
        ORDER BY created_at ASC
        LIMIT 500
    `).bind(key).all();
    return (rows.results || []).map((r) => ({
        id: r.id,
        email: r.email,
        lang: r.lang,
        pagePath: r.page_path,
        createdAt: r.created_at,
    }));
}

/**
 * Chiude le iscrizioni appena notificate: timestamp di invio e cancellazione
 * dell'indirizzo, in un colpo solo. Il token resta perche' e' la chiave del
 * link di annullamento gia' partito nell'email.
 *
 * @param {D1Database} db
 * @param {string[]} ids
 */
export async function markRestockNotified(db, ids) {
    const list = (ids || []).filter(Boolean);
    if (!list.length) return;
    const ts = now();
    const placeholders = list.map(() => '?').join(',');
    await db.prepare(`
        UPDATE restock_requests
        SET notified_at = ?, email = NULL
        WHERE id IN (${placeholders})
    `).bind(ts, ...list).run();
}

/**
 * Iscrizione ancora annullabile a partire dal token del link email.
 * @param {D1Database} db
 */
export async function findRestockByToken(db, token) {
    const t = String(token || '').trim();
    if (!/^[0-9a-f]{32}$/.test(t)) return null;
    const row = await db.prepare(`
        SELECT id, sku, email, lang, notified_at
        FROM restock_requests
        WHERE token = ?
    `).bind(t).first();
    return row || null;
}

/**
 * Cancella l'iscrizione legata al token. Idempotente: un secondo clic sullo
 * stesso link non e' un errore.
 *
 * @param {D1Database} db
 * @returns {Promise<boolean>} true se la riga esisteva
 */
export async function cancelRestockByToken(db, token) {
    const t = String(token || '').trim();
    if (!/^[0-9a-f]{32}$/.test(t)) return false;
    const res = await db.prepare('DELETE FROM restock_requests WHERE token = ?').bind(t).run();
    return (res?.meta?.changes ?? 0) > 0;
}

/**
 * Destinatari da avvisare per uno SKU tornato disponibile, gia' divisi in
 * blocchi della dimensione accettata da Resend.
 *
 * @param {D1Database} db
 * @returns {Promise<Array<Array<{ id: string, email: string, lang: string, pagePath: string|null, token: string }>>>}
 */
export async function pendingBatchesForSku(db, sku) {
    const key = String(sku || '').trim();
    if (!key) return [];
    const rows = await db.prepare(`
        SELECT id, email, lang, page_path, token
        FROM restock_requests
        WHERE sku = ? AND notified_at IS NULL AND email IS NOT NULL
        ORDER BY created_at ASC
    `).bind(key).all();

    const all = (rows.results || []).map((r) => ({
        id: r.id,
        email: r.email,
        lang: r.lang,
        pagePath: r.page_path,
        token: r.token,
    }));

    const batches = [];
    for (let i = 0; i < all.length; i += NOTIFY_CHUNK) {
        batches.push(all.slice(i, i + NOTIFY_CHUNK));
    }
    return batches;
}

/* ─── Freno per IP ───────────────────────────────────────────────────────────── */

const IP_WINDOW_MS = 10 * 60 * 1000;
const IP_MAX_REQUESTS = 5;

/**
 * Rate limit per IP sull'iscrizione. Fail-OPEN: qui non si muove denaro e non
 * parte nessuna email immediata, quindi un problema su D1 non deve impedire a
 * un cliente vero di lasciare l'indirizzo — e se D1 e' davvero rotto la INSERT
 * fallisce comunque subito dopo.
 *
 * @param {object} env
 * @param {Request} request
 * @returns {Promise<null | { limited: true, retryAfter: number }>}
 */
export async function checkRestockIpRateLimit(env, request) {
    const secret = env.FRAUD_HASH_SECRET;
    if (!secret || !env.DB) return null;

    const ip = request.headers.get('CF-Connecting-IP') || '';
    if (!ip) return null;

    try {
        const ipHash = await hmacIdentifier(secret, 'restock-ip', ip);
        const windowId = `10m:${windowSlot(IP_WINDOW_MS)}`;
        const count = await bumpBucket(env.DB, `restock:${ipHash}`, windowId);
        if (count > IP_MAX_REQUESTS) {
            return { limited: true, retryAfter: retryAfterForWindow(IP_WINDOW_MS) };
        }
    } catch (e) {
        console.warn('[restock] rate limit non applicato (fail-open):', e?.message || e);
    }
    return null;
}

/**
 * Hash dell'IP da salvare sulla riga: serve solo a riconoscere a posteriori un
 * eventuale abuso, non a risalire alla persona.
 */
export async function restockIpHash(env, request) {
    const secret = env.FRAUD_HASH_SECRET;
    const ip = request.headers.get('CF-Connecting-IP') || '';
    if (!secret || !ip) return null;
    try {
        return await hmacIdentifier(secret, 'restock-row-ip', ip);
    } catch (_) {
        return null;
    }
}

export { NOTIFY_CHUNK };
