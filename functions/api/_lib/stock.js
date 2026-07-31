/**
 * stock.js — inventario D1 per SKU fisici (DVD/COA).
 * Fonte qty: Admin. Riga assente = 0.
 */

import { CATALOG, getCatalogEntry } from './catalog.js';
import { now } from './utils.js';

const LOW_STOCK_MAX = 10;

/** @returns {Array<{ sku: string, name: string }>} */
export function listPhysicalSkus() {
    return Object.entries(CATALOG)
        .filter(([, e]) => Boolean(e.physical))
        .map(([sku, e]) => ({ sku, name: e.name }));
}

export function isPhysicalSku(sku) {
    const entry = getCatalogEntry(sku);
    return Boolean(entry && entry.physical);
}

/**
 * @param {D1Database} db
 * @param {string} sku
 * @returns {Promise<number>}
 */
export async function getStockQty(db, sku) {
    const key = String(sku || '').trim();
    if (!key || !isPhysicalSku(key)) return 0;
    const row = await db.prepare('SELECT qty FROM product_stock WHERE sku = ?').bind(key).first();
    if (!row) return 0;
    const q = Number(row.qty);
    return Number.isFinite(q) && q > 0 ? Math.floor(q) : 0;
}

/**
 * @param {D1Database} db
 * @returns {Promise<Array<{ sku: string, name: string, qty: number, updatedAt: string|null, updatedBy: string|null }>>}
 */
export async function listAdminStock(db) {
    const physical = listPhysicalSkus();
    const rows = await db.prepare('SELECT sku, qty, updated_at, updated_by FROM product_stock').all();
    const bySku = new Map();
    for (const r of rows.results || []) {
        bySku.set(String(r.sku), r);
    }
    return physical.map(({ sku, name }) => {
        const r = bySku.get(sku);
        const qty = r ? Math.max(0, Math.floor(Number(r.qty) || 0)) : 0;
        return {
            sku,
            name,
            qty,
            updatedAt: r ? (r.updated_at || null) : null,
            updatedBy: r ? (r.updated_by || null) : null,
        };
    });
}

/**
 * @param {D1Database} db
 * @param {string} sku
 * @param {number} qty
 * @param {string} actorEmail
 */
export async function setStockQty(db, sku, qty, actorEmail) {
    const key = String(sku || '').trim();
    if (!isPhysicalSku(key)) {
        const err = new Error('SKU non fisico o non in catalogo');
        err.reason = 'not_physical';
        throw err;
    }
    const q = Math.round(Number(qty));
    if (!Number.isFinite(q) || q < 0 || q > 999999) {
        const err = new Error('Quantità non valida');
        err.reason = 'invalid_qty';
        throw err;
    }
    const ts = now();
    const actor = String(actorEmail || '').trim() || null;
    await db.prepare(`
        INSERT INTO product_stock (sku, qty, updated_at, updated_by)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(sku) DO UPDATE SET
            qty = excluded.qty,
            updated_at = excluded.updated_at,
            updated_by = excluded.updated_by
    `).bind(key, q, ts, actor).run();
    return { sku: key, qty: q, updatedAt: ts, updatedBy: actor };
}

/**
 * Aggrega qty carrello per SKU fisico e confronta con magazzino.
 * @param {D1Database} db
 * @param {Array<{ sku: string, qty?: number, physical?: boolean }>} items
 */
export async function assertCartStock(db, items) {
    const needed = new Map();
    for (const item of items || []) {
        if (!item.physical && !isPhysicalSku(item.sku)) continue;
        if (!isPhysicalSku(item.sku)) continue;
        const q = Math.max(1, Math.min(99, Number(item.qty) || 1));
        needed.set(item.sku, (needed.get(item.sku) || 0) + q);
    }
    if (needed.size === 0) return;

    for (const [sku, want] of needed) {
        const have = await getStockQty(db, sku);
        if (want > have) {
            const err = new Error(
                have <= 0
                    ? `Prodotto esaurito: ${sku}`
                    : `Stock insufficiente per ${sku} (richiesti ${want}, disponibili ${have})`
            );
            err.reason = 'insufficient_stock';
            err.sku = sku;
            err.requested = want;
            err.available = have;
            err.status = 409;
            throw err;
        }
    }
}

/**
 * Scala stock a pagamento confermato. Idempotente per order_id.
 * @returns {Promise<{ ok: boolean, skipped?: boolean, warnings?: string[] }>}
 */
export async function deductStockForPaidOrder(db, orderId, lineItems) {
    const oid = String(orderId || '').trim();
    if (!oid) return { ok: false, skipped: true };

    const already = await db.prepare(
        'SELECT order_id FROM stock_deductions WHERE order_id = ?'
    ).bind(oid).first();
    if (already) return { ok: true, skipped: true };

    const needed = new Map();
    for (const item of lineItems || []) {
        const sku = String(item.sku || '').trim();
        if (!sku || !isPhysicalSku(sku)) continue;
        const q = Math.max(1, Math.min(99, Number(item.qty || item.quantity) || 1));
        needed.set(sku, (needed.get(sku) || 0) + q);
    }

    if (needed.size === 0) {
        await db.prepare(
            'INSERT INTO stock_deductions (order_id, deducted_at) VALUES (?, ?)'
        ).bind(oid, now()).run();
        return { ok: true, skipped: true };
    }

    const warnings = [];
    const ts = now();

    try {
        const stmts = [];
        for (const [sku, want] of needed) {
            const actor = `order:${oid}`;
            stmts.push(
                db.prepare(`
                    UPDATE product_stock
                    SET qty = qty - ?, updated_at = ?, updated_by = ?
                    WHERE sku = ? AND qty >= ?
                `).bind(want, ts, actor, sku, want)
            );
        }
        stmts.push(
            db.prepare(
                'INSERT INTO stock_deductions (order_id, deducted_at) VALUES (?, ?)'
            ).bind(oid, ts)
        );

        const results = await db.batch(stmts);
        // Ultimo statement = insert deduction; precedenti = update per SKU
        for (let i = 0; i < results.length - 1; i++) {
            const meta = results[i]?.meta || results[i];
            const changes = meta?.changes ?? meta?.rows_written ?? 0;
            if (!changes) {
                const sku = [...needed.keys()][i];
                warnings.push(`stock_deduct_failed:${sku}`);
                console.warn('[stock] Deduct failed or insufficient for', sku, 'order', oid);
            }
        }
    } catch (e) {
        // Race su stock_deductions UNIQUE → già scalato
        if (String(e?.message || '').includes('UNIQUE')) {
            return { ok: true, skipped: true };
        }
        console.error('[stock] deductStockForPaidOrder error:', e?.message || e);
        return { ok: false, warnings: [String(e?.message || e)] };
    }

    return { ok: true, warnings: warnings.length ? warnings : undefined };
}

export function stockStatusFromQty(qty) {
    const q = Math.max(0, Math.floor(Number(qty) || 0));
    if (q <= 0) return 'out';
    if (q <= LOW_STOCK_MAX) return 'low';
    return 'ok';
}

export { LOW_STOCK_MAX };
