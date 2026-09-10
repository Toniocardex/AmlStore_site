/**
 * licenses.js — pool D1 di chiavi digitali e evasione automatica (ADR-004).
 *
 * All-or-nothing sulle righe non fisiche: se manca anche una chiave non si
 * assegna nulla e non si manda la mail di consegna. Il pagamento non dipende
 * da questo modulo (fail-soft se lo schema non c'e').
 */

import { CATALOG, getCatalogEntry } from './catalog.js';
import { now, safeParseJSON } from './utils.js';
import { sendLicenseDeliveryOnce } from './email.js';

const MAX_IMPORT = 500;
const MAX_KEY_LEN = 256;
const MIN_KEY_LEN = 6;
const IMPORT_BATCH = 40;
const PENDING_FULFILL_LIMIT = 15;
/** Allineato a resolveAndValidateItems: una riga carrello non supera 99. */
const MAX_QTY_PER_LINE = 99;
const ASSIGN_STALE_MS = 120_000;
const EMAIL_CLAIM_STALE_MS = 120_000;

export function normalizeLicenseKey(raw) {
    return String(raw || '').trim();
}

export function licenseKeyNorm(raw) {
    return normalizeLicenseKey(raw).toLowerCase();
}

export function parseLicenseKeys(raw) {
    const text = String(raw || '');
    const seen = new Set();
    const keys = [];
    const skipped = { empty: 0, duplicate: 0, invalid: 0, overflow: 0 };

    for (const line of text.split(/\r?\n/)) {
        const material = normalizeLicenseKey(line);
        if (!material) { skipped.empty += 1; continue; }
        if (material.startsWith('#')) { skipped.empty += 1; continue; }
        if (material.length < MIN_KEY_LEN || material.length > MAX_KEY_LEN) {
            skipped.invalid += 1;
            continue;
        }
        if (keys.length >= MAX_IMPORT) {
            skipped.overflow += 1;
            continue;
        }
        const norm = licenseKeyNorm(material);
        if (seen.has(norm)) { skipped.duplicate += 1; continue; }
        seen.add(norm);
        keys.push({ material, norm });
    }

    return { keys, skipped };
}

export function maskLicenseKey(key) {
    const s = String(key || '');
    if (s.length <= 8) return '••••';
    return `${s.slice(0, 4)}…${s.slice(-4)}`;
}

/** Stessa euristica del generatore admin (email-license-generator.html). */
export function activationFromProductName(productName) {
    const n = String(productName || '').toLowerCase();
    if (/mcafee/.test(n)) return 'mcafee';
    if (/kaspersky/.test(n)) return 'kaspersky';
    if (/norton/.test(n)) return 'norton';
    if (/\beset\b/.test(n)) return 'eset';
    if (/adobe|photoshop|acrobat|illustrator/.test(n)) return 'adobe';
    if (/acronis/.test(n)) return 'acronis';
    if (/corel|coreldraw|paintshop/.test(n)) return 'corel';
    if (/windows\s*server/.test(n)) return 'windows_server';
    if (/windows/.test(n)) return 'windows';
    if (/office|microsoft\s*365|project|visio/.test(n)) return 'office';
    return '';
}

export function isDigitalSku(sku) {
    const entry = getCatalogEntry(sku);
    return Boolean(entry && !entry.physical);
}

export function listDigitalSkus() {
    return Object.entries(CATALOG)
        .filter(([, e]) => !e.physical)
        .map(([sku, e]) => ({ sku, name: e.name }));
}

/**
 * Qty digitali per SKU. Righe fisiche (flag o catalogo) escluse.
 * @param {Array<{ sku?: string, qty?: number, quantity?: number, physical?: boolean }>} items
 * @returns {Map<string, number>}
 */
export function digitalNeedFromItems(items) {
    const needed = new Map();
    for (const item of items || []) {
        const sku = String(item?.sku || '').trim();
        if (!sku) continue;
        const physical = item.physical === true || Boolean(getCatalogEntry(sku)?.physical);
        if (physical) continue;
        const qty = Math.max(0, Math.min(
            MAX_QTY_PER_LINE,
            Math.floor(Number(item.qty || item.quantity || 1) || 0)
        ));
        if (!qty) continue;
        needed.set(sku, (needed.get(sku) || 0) + qty);
    }
    return needed;
}

export function isLicensesSchemaMissing(err) {
    const m = String(err?.message || err || '');
    return /no such table: license_keys/i.test(m)
        || /no such column: license_/i.test(m);
}

/**
 * Tiene al massimo `needed` chiavi per SKU (ordine di arrivo).
 * Usato per non spedire/tenere chiavi in eccesso se due worker assegnano insieme.
 */
export function capKeysToNeed(keys, needed) {
    const used = new Map();
    const kept = [];
    const extras = [];
    for (const key of keys || []) {
        const sku = String(key.sku || '');
        const cap = Number(needed.get(sku) || 0);
        const have = used.get(sku) || 0;
        if (have < cap) {
            kept.push(key);
            used.set(sku, have + 1);
        } else {
            extras.push(key);
        }
    }
    return { kept, extras };
}

export function coversDigitalNeed(keys, needed) {
    const have = new Map();
    for (const key of keys || []) {
        const sku = String(key.sku || '');
        have.set(sku, (have.get(sku) || 0) + 1);
    }
    for (const [sku, qty] of needed) {
        if ((have.get(sku) || 0) < qty) return false;
    }
    return true;
}

function newLicenseId() {
    const bytes = new Uint8Array(16);
    crypto.getRandomValues(bytes);
    return 'lk_' + [...bytes].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export async function setLicenseStatus(db, orderId, status) {
    const ts = now();
    await db.prepare(
        'UPDATE orders SET license_status = ?, updated_at = ? WHERE id = ?'
    ).bind(status, ts, orderId).run();
}

export async function markLicenseKeysEmailed(db, keyIds) {
    if (!keyIds?.length) return;
    const ts = now();
    const stmts = keyIds.map((id) => db.prepare(
        'UPDATE license_keys SET emailed_at = ? WHERE id = ? AND emailed_at IS NULL'
    ).bind(ts, id));
    await db.batch(stmts);
}

export async function listAssignedKeysForOrder(db, orderId) {
    const rows = await db.prepare(`
        SELECT id, sku, key_material, assigned_at, emailed_at
        FROM license_keys
        WHERE order_id = ? AND status = 'assigned'
        ORDER BY assigned_at, id
    `).bind(orderId).all();
    return rows.results || [];
}

async function countAssignedBySku(db, orderId) {
    const rows = await db.prepare(`
        SELECT sku, COUNT(*) AS n
        FROM license_keys
        WHERE order_id = ? AND status = 'assigned'
        GROUP BY sku
    `).bind(orderId).all();
    const map = new Map();
    for (const r of rows.results || []) map.set(String(r.sku), Number(r.n) || 0);
    return map;
}

async function countAvailableBySku(db, skus) {
    const map = new Map();
    if (!skus.length) return map;
    const placeholders = skus.map(() => '?').join(',');
    const rows = await db.prepare(`
        SELECT sku, COUNT(*) AS n
        FROM license_keys
        WHERE status = 'available' AND sku IN (${placeholders})
        GROUP BY sku
    `).bind(...skus).all();
    for (const r of rows.results || []) map.set(String(r.sku), Number(r.n) || 0);
    return map;
}

async function assignOneKey(db, orderId, sku, ts, maxQty) {
    const cap = Math.max(0, Math.floor(Number(maxQty) || 0));
    // SELECT annidato: SQLite rifiuta UPDATE sulla stessa tabella del subquery.
    const result = await db.prepare(`
        UPDATE license_keys
        SET status = 'assigned', order_id = ?, assigned_at = ?
        WHERE id = (
            SELECT id FROM (
                SELECT id FROM license_keys
                WHERE sku = ? AND status = 'available'
                  AND (
                    SELECT COUNT(*) FROM license_keys AS already
                    WHERE already.order_id = ? AND already.sku = ? AND already.status = 'assigned'
                  ) < ?
                ORDER BY imported_at ASC, id ASC
                LIMIT 1
            )
        )
        AND status = 'available'
    `).bind(orderId, ts, sku, orderId, sku, cap).run();
    return (result.meta?.changes ?? 0) > 0;
}

async function tryBeginAssignment(db, orderId) {
    const ts = now();
    const stale = new Date(Date.now() - ASSIGN_STALE_MS).toISOString();
    const result = await db.prepare(`
        UPDATE orders
        SET license_status = 'assigning', updated_at = ?
        WHERE id = ?
          AND status = 'paid'
          AND (
            license_status IS NULL
            OR license_status = 'pending'
            OR (license_status = 'assigning' AND updated_at < ?)
          )
    `).bind(ts, orderId, stale).run();
    return (result.meta?.changes ?? 0) > 0;
}

async function claimLicenseEmailSend(db, orderId, eventSrc) {
    const ts = now();
    const stale = new Date(Date.now() - EMAIL_CLAIM_STALE_MS).toISOString();
    const token = 'sending:' + String(eventSrc || 'unknown').slice(0, 40);
    const result = await db.prepare(`
        UPDATE orders
        SET license_email_event_src = ?, updated_at = ?
        WHERE id = ?
          AND license_email_sent_at IS NULL
          AND (
            license_email_event_src IS NULL
            OR (license_email_event_src LIKE 'sending:%' AND updated_at < ?)
          )
    `).bind(token, ts, orderId, stale).run();
    return (result.meta?.changes ?? 0) > 0;
}

async function releaseLicenseEmailClaim(db, orderId) {
    await db.prepare(`
        UPDATE orders
        SET license_email_event_src = NULL, updated_at = ?
        WHERE id = ?
          AND license_email_sent_at IS NULL
          AND license_email_event_src LIKE 'sending:%'
    `).bind(now(), orderId).run();
}

async function trimUnemailedExtras(db, orderId, extras) {
    const ids = (extras || []).filter((k) => k.id && !k.emailed_at).map((k) => k.id);
    if (!ids.length) return;
    const placeholders = ids.map(() => '?').join(',');
    await db.prepare(`
        UPDATE license_keys
        SET status = 'available', order_id = NULL, assigned_at = NULL
        WHERE order_id = ?
          AND status = 'assigned'
          AND emailed_at IS NULL
          AND id IN (${placeholders})
    `).bind(orderId, ...ids).run();
}

async function releaseUnemailedAssignments(db, orderId, skuList) {
    if (!skuList.length) return;
    const placeholders = skuList.map(() => '?').join(',');
    await db.prepare(`
        UPDATE license_keys
        SET status = 'available', order_id = NULL, assigned_at = NULL
        WHERE order_id = ?
          AND status = 'assigned'
          AND emailed_at IS NULL
          AND sku IN (${placeholders})
    `).bind(orderId, ...skuList).run();
}

async function remainingNeed(db, order, needed) {
    const assigned = await countAssignedBySku(db, order.id);
    const remaining = new Map();
    for (const [sku, qty] of needed) {
        const have = assigned.get(sku) || 0;
        const left = qty - have;
        if (left > 0) remaining.set(sku, left);
    }
    return { assigned, remaining };
}

/**
 * Tenta l'assegnazione all-or-nothing. Non invia email.
 * Lease `assigning` + cap SQL sul COUNT per ordine/SKU: due worker non
 * possono assegnare piu' chiavi di quelle acquistate (webhook Stripe doppi).
 * @returns {Promise<{ status: string, needed: number, assigned: number, remaining: Map<string, number>, reason?: string }>}
 */
export async function assignKeysForOrder(db, order) {
    const live = await db.prepare(
        'SELECT id, status, line_items, license_status FROM orders WHERE id = ?'
    ).bind(order.id).first();
    if (!live || live.status !== 'paid') {
        return { status: 'skipped', needed: 0, assigned: 0, remaining: new Map(), reason: 'not_paid' };
    }

    const items = safeParseJSON(live.line_items, []);
    const needed = digitalNeedFromItems(items);
    const neededTotal = [...needed.values()].reduce((a, b) => a + b, 0);

    if (neededTotal === 0) {
        await setLicenseStatus(db, order.id, 'not_applicable');
        return { status: 'not_applicable', needed: 0, assigned: 0, remaining: new Map() };
    }

    if (live.license_status === 'fulfilled') {
        const assigned = await countAssignedBySku(db, order.id);
        const assignedTotal = [...needed.keys()].reduce((a, sku) => a + (assigned.get(sku) || 0), 0);
        return { status: 'fulfilled', needed: neededTotal, assigned: assignedTotal, remaining: new Map() };
    }

    const claimed = await tryBeginAssignment(db, order.id);
    if (!claimed) {
        const again = await db.prepare('SELECT license_status FROM orders WHERE id = ?').bind(order.id).first();
        if (again?.license_status === 'fulfilled') {
            const assigned = await countAssignedBySku(db, order.id);
            const assignedTotal = [...needed.keys()].reduce((a, sku) => a + (assigned.get(sku) || 0), 0);
            return { status: 'fulfilled', needed: neededTotal, assigned: assignedTotal, remaining: new Map() };
        }
        return { status: 'pending', needed: neededTotal, assigned: 0, remaining: needed, reason: 'in_progress' };
    }

    const { assigned, remaining } = await remainingNeed(db, order, needed);
    const assignedTotal = [...needed.keys()].reduce((a, sku) => a + (assigned.get(sku) || 0), 0);

    if (remaining.size === 0) {
        const rows = await listAssignedKeysForOrder(db, order.id);
        const { extras } = capKeysToNeed(rows, needed);
        await trimUnemailedExtras(db, order.id, extras);
        await setLicenseStatus(db, order.id, 'fulfilled');
        return { status: 'fulfilled', needed: neededTotal, assigned: neededTotal, remaining };
    }

    const available = await countAvailableBySku(db, [...remaining.keys()]);
    for (const [sku, want] of remaining) {
        if ((available.get(sku) || 0) < want) {
            await setLicenseStatus(db, order.id, 'pending');
            return { status: 'pending', needed: neededTotal, assigned: assignedTotal, remaining };
        }
    }

    const ts = now();
    const attemptedSkus = [...remaining.keys()];
    for (const [sku, want] of remaining) {
        const cap = needed.get(sku) || want;
        for (let i = 0; i < want; i++) {
            const ok = await assignOneKey(db, order.id, sku, ts, cap);
            if (!ok) {
                await releaseUnemailedAssignments(db, order.id, attemptedSkus);
                await setLicenseStatus(db, order.id, 'pending');
                return { status: 'pending', needed: neededTotal, assigned: assignedTotal, remaining, reason: 'race' };
            }
        }
    }

    const after = await listAssignedKeysForOrder(db, order.id);
    const { extras } = capKeysToNeed(after, needed);
    await trimUnemailedExtras(db, order.id, extras);
    const finalCounts = await countAssignedBySku(db, order.id);
    for (const [sku, qty] of needed) {
        if ((finalCounts.get(sku) || 0) < qty) {
            await releaseUnemailedAssignments(db, order.id, [...needed.keys()]);
            await setLicenseStatus(db, order.id, 'pending');
            return { status: 'pending', needed: neededTotal, assigned: assignedTotal, remaining, reason: 'short' };
        }
    }

    await setLicenseStatus(db, order.id, 'fulfilled');
    return {
        status: 'fulfilled',
        needed: neededTotal,
        assigned: neededTotal,
        remaining: new Map(),
    };
}

function deliveryItemsForOrder(order, keys) {
    const items = safeParseJSON(order.line_items, []);
    const nameBySku = new Map();
    for (const item of items) {
        const sku = String(item.sku || '').trim();
        if (sku && !nameBySku.has(sku)) nameBySku.set(sku, item.name || sku);
    }
    return keys.map((row) => {
        const productName = nameBySku.get(row.sku) || getCatalogEntry(row.sku)?.name || row.sku;
        return {
            productName,
            sku: row.sku,
            key: row.key_material,
            activation: activationFromProductName(productName),
        };
    });
}

/**
 * Orchestratore post-pagamento (ADR-004 §6). Idempotente.
 * @param {{ DB: D1Database, RESEND_API_KEY?: string }} env
 */
export async function fulfillLicensesForPaidOrder(env, order, eventSrc) {
    const db = env.DB;
    if (!order?.id) {
        return { status: 'skipped', reason: 'not_paid' };
    }

    const live = await db.prepare('SELECT * FROM orders WHERE id = ?').bind(order.id).first();
    if (!live || live.status !== 'paid') {
        return { status: 'skipped', reason: 'not_paid' };
    }

    const assign = await assignKeysForOrder(db, live);
    if (assign.status !== 'fulfilled') {
        return assign;
    }

    const keys = await listAssignedKeysForOrder(db, live.id);
    const needed = digitalNeedFromItems(safeParseJSON(live.line_items, []));
    const { kept, extras } = capKeysToNeed(keys, needed);
    await trimUnemailedExtras(db, live.id, extras);

    if (!coversDigitalNeed(kept, needed)) {
        return { status: 'pending', needed: assign.needed, assigned: kept.length, reason: 'short' };
    }

    const unemailed = kept.filter((k) => !k.emailed_at);
    if (!unemailed.length) {
        return { status: 'fulfilled', needed: assign.needed, assigned: assign.assigned, emailed: 0, skipped: 'already_emailed' };
    }

    const liveEmail = await db.prepare(
        'SELECT license_email_sent_at FROM orders WHERE id = ?'
    ).bind(live.id).first();
    if (liveEmail?.license_email_sent_at) {
        await markLicenseKeysEmailed(db, unemailed.map((k) => k.id));
        return {
            status: 'fulfilled',
            needed: assign.needed,
            assigned: assign.assigned,
            emailed: unemailed.length,
            skipped: 'already_emailed',
        };
    }

    const claimed = await claimLicenseEmailSend(db, live.id, eventSrc);
    if (!claimed) {
        return { status: 'fulfilled', needed: assign.needed, assigned: assign.assigned, emailed: 0, skipped: 'send_in_progress' };
    }

    const deliveryItems = deliveryItemsForOrder(live, unemailed);
    const sent = await sendLicenseDeliveryOnce(db, live, deliveryItems, env.RESEND_API_KEY || '', eventSrc);
    if (sent.sent || sent.already) {
        await markLicenseKeysEmailed(db, unemailed.map((k) => k.id));
        return {
            status: 'fulfilled',
            needed: assign.needed,
            assigned: assign.assigned,
            emailed: unemailed.length,
            skipped: sent.already ? 'already_emailed' : undefined,
        };
    }

    await releaseLicenseEmailClaim(db, live.id);
    return {
        status: 'fulfilled',
        needed: assign.needed,
        assigned: assign.assigned,
        emailed: 0,
        emailError: sent.error || 'send_failed',
    };
}

export async function importLicenseKeys(db, sku, rawKeys, actorEmail) {
    const key = String(sku || '').trim();
    if (!key || !getCatalogEntry(key)) {
        const err = new Error('SKU non in catalogo');
        err.reason = 'unknown_sku';
        throw err;
    }
    if (!isDigitalSku(key)) {
        const err = new Error('SKU fisico: usare Magazzino, non il pool licenze');
        err.reason = 'physical_sku';
        throw err;
    }

    const source = Array.isArray(rawKeys) ? rawKeys.join('\n') : String(rawKeys || '');
    const { keys, skipped } = parseLicenseKeys(source);
    if (!keys.length) {
        return { imported: 0, duplicates: skipped.duplicate, skipped };
    }

    const ts = now();
    const actor = actorEmail || null;
    let imported = 0;
    let duplicates = skipped.duplicate;

    for (let i = 0; i < keys.length; i += IMPORT_BATCH) {
        const chunk = keys.slice(i, i + IMPORT_BATCH);
        const stmts = chunk.map((k) => db.prepare(`
            INSERT OR IGNORE INTO license_keys (
                id, sku, key_norm, key_material, status, imported_at, imported_by
            ) VALUES (?, ?, ?, ?, 'available', ?, ?)
        `).bind(newLicenseId(), key, k.norm, k.material, ts, actor));
        const results = await db.batch(stmts);
        for (const r of results) {
            const changes = r?.meta?.changes ?? 0;
            if (changes > 0) imported += 1;
            else duplicates += 1;
        }
    }

    return { imported, duplicates, skipped };
}

export async function revokeAvailableKey(db, keyId) {
    const id = String(keyId || '').trim();
    if (!id) {
        const err = new Error('id mancante');
        err.reason = 'invalid_id';
        throw err;
    }
    const result = await db.prepare(`
        DELETE FROM license_keys WHERE id = ? AND status = 'available'
    `).bind(id).run();
    if ((result.meta?.changes ?? 0) === 0) {
        const err = new Error('Chiave non trovata o gia assegnata');
        err.reason = 'not_available';
        throw err;
    }
    return { ok: true };
}

export async function summarizeLicensePool(db) {
    const rows = await db.prepare(`
        SELECT sku, status, COUNT(*) AS n
        FROM license_keys
        GROUP BY sku, status
    `).all();
    const bySku = new Map();
    for (const r of rows.results || []) {
        const sku = String(r.sku);
        const cur = bySku.get(sku) || { sku, name: getCatalogEntry(sku)?.name || sku, available: 0, assigned: 0 };
        if (r.status === 'available') cur.available = Number(r.n) || 0;
        if (r.status === 'assigned') cur.assigned = Number(r.n) || 0;
        bySku.set(sku, cur);
    }
    return [...bySku.values()].sort((a, b) => a.sku.localeCompare(b.sku));
}

export async function listAvailableKeysForSku(db, sku, limit = 100) {
    const key = String(sku || '').trim();
    const cap = Math.min(200, Math.max(1, Number(limit) || 100));
    const rows = await db.prepare(`
        SELECT id, sku, key_material, imported_at, imported_by
        FROM license_keys
        WHERE sku = ? AND status = 'available'
        ORDER BY imported_at ASC
        LIMIT ?
    `).bind(key, cap).all();
    return (rows.results || []).map((r) => ({
        id: r.id,
        sku: r.sku,
        masked: maskLicenseKey(r.key_material),
        importedAt: r.imported_at,
        importedBy: r.imported_by || null,
    }));
}

function likeSkuPattern(sku) {
    return `%"sku":"${String(sku).replace(/[%_]/g, '\\$&')}"%`;
}

export async function listPendingLicenseOrders(db, { sku = '', limit = 30 } = {}) {
    const cap = Math.min(50, Math.max(1, Number(limit) || 30));
    let sql = `
        SELECT id, status, paid_at, created_at, customer_email,
               customer_first_name, customer_last_name, locale,
               line_items, license_status, license_email_sent_at
        FROM orders
        WHERE status = 'paid'
          AND (license_status IS NULL OR license_status = 'pending')
    `;
    const binds = [];
    if (sku) {
        sql += ' AND line_items LIKE ?';
        binds.push(likeSkuPattern(sku));
    }
    sql += ' ORDER BY COALESCE(paid_at, created_at) ASC LIMIT ?';
    binds.push(cap);
    const rows = await db.prepare(sql).bind(...binds).all();
    return (rows.results || []).map((row) => {
        const items = safeParseJSON(row.line_items, []);
        const needed = digitalNeedFromItems(items);
        return {
            orderId: row.id,
            paidAt: row.paid_at,
            createdAt: row.created_at,
            email: row.customer_email,
            name: `${row.customer_first_name || ''} ${row.customer_last_name || ''}`.trim(),
            licenseStatus: row.license_status || null,
            needed: Object.fromEntries(needed),
        };
    });
}

export async function fulfillPendingOrdersForSku(env, sku, eventSrc) {
    const orders = await listPendingLicenseOrders(env.DB, { sku, limit: PENDING_FULFILL_LIMIT });
    const results = [];
    for (const summary of orders) {
        const row = await env.DB.prepare('SELECT * FROM orders WHERE id = ?').bind(summary.orderId).first();
        if (!row || row.status !== 'paid') continue;
        const result = await fulfillLicensesForPaidOrder(env, row, eventSrc);
        results.push({ orderId: summary.orderId, status: result.status, emailed: result.emailed || 0 });
    }
    return results;
}
