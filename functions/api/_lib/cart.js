/**
 * cart.js — helper D1 per il tracking carrelli (analytics fase 1).
 *
 * Esporta:
 *   upsertCartSession(db, params)          — upsert snapshot carrello (anche vuoto)
 *   markCartCheckoutStarted(db, id, orderId) — collega un cartId a un ordine creato
 *   checkCartSyncRateLimit(env, request)   — rate limit per IP su /api/cart/sync
 *   listCarts(db, opts)                    — lista admin paginata e filtrabile
 *   getCartStats(db, opts)                 — KPI aggregati per la vista admin
 *
 * Nota sugli stati: nessuna colonna di stato salvata. "Abbandonato" = nessun
 * checkout avviato, carrello non vuoto, inattivo da più di `hoursIdle` ore.
 * "Pagato" si legge sempre da orders.status (join), mai duplicato qui.
 */

import { now, safeParseJSON }          from './utils.js';
import { hmacIdentifier, bumpBucket, windowSlot, retryAfterForWindow } from './rate-limit.js';

/* ─── Upsert snapshot carrello ───────────────────────────────────────────────── */

/**
 * Crea o aggiorna la riga cart_sessions per un cartId.
 * `email` viene scritta solo se il chiamante la passa con un valore
 * (COALESCE preserva l'email già agganciata sui sync anonimi successivi).
 */
export async function upsertCartSession(db, {
    id,
    email,
    locale,
    country,
    lineItems,
    totalMinor,
    currency,
}) {
    const ts = now();
    const itemCount = Array.isArray(lineItems) ? lineItems.length : 0;

    await db.prepare(`
        INSERT INTO cart_sessions (
            id, email, locale, country, line_items, item_count,
            total_minor, currency, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            email       = COALESCE(excluded.email, cart_sessions.email),
            locale      = excluded.locale,
            country     = excluded.country,
            line_items  = excluded.line_items,
            item_count  = excluded.item_count,
            total_minor = excluded.total_minor,
            currency    = excluded.currency,
            updated_at  = excluded.updated_at
    `).bind(
        id, email || null, locale || 'it', country || null,
        JSON.stringify(lineItems || []), itemCount,
        totalMinor || 0, currency || 'EUR', ts, ts
    ).run();
}

/** Collega un cartId a un ordine appena creato (checkout avviato, non necessariamente pagato). */
export async function markCartCheckoutStarted(db, cartId, orderId) {
    await db.prepare(`
        UPDATE cart_sessions
        SET checkout_started_at = ?, checkout_order_id = ?
        WHERE id = ? AND checkout_order_id IS NULL
    `).bind(now(), orderId, cartId).run();
}

/* ─── Rate limit /api/cart/sync (per IP) ─────────────────────────────────────── */

const CART_SYNC_WINDOW_MS = 60 * 1000;
const CART_SYNC_MAX_PER_MINUTE = 20;

/**
 * Rate limit per IP (mai salvato in chiaro — solo HMAC) sull'endpoint pubblico
 * /api/cart/sync. A differenza del gate anti-frode del checkout, qui si fallisce
 * "aperto" quando manca l'IP o si verifica un errore imprevisto: è un endpoint
 * di analytics best-effort, non un controllo antifrode — il costo di un sync
 * perso è nullo, il costo di bloccare il tracking per un blip infrastrutturale
 * non lo è.
 */
export async function checkCartSyncRateLimit(env, request) {
    const secret = env.FRAUD_HASH_SECRET;
    if (!secret || !env.DB) return null;

    const ip = request.headers.get('CF-Connecting-IP') || '';
    if (!ip) return null;

    try {
        const ipHash = await hmacIdentifier(secret, 'cartsync-ip', ip);
        const bucketKey = `cartsync:${ipHash}`;
        const windowId = `1m:${windowSlot(CART_SYNC_WINDOW_MS)}`;
        const count = await bumpBucket(env.DB, bucketKey, windowId);
        if (count > CART_SYNC_MAX_PER_MINUTE) {
            return { limited: true, status: 429, retryAfter: retryAfterForWindow(CART_SYNC_WINDOW_MS) };
        }
    } catch (e) {
        console.warn('[cart] rate limit check failed (fail-open):', e?.message || e);
    }
    return null;
}

/* ─── Query D1 lista admin ───────────────────────────────────────────────────── */

const PAGE_SIZE = 50;
const DEFAULT_HOURS_IDLE = 2;

function isoHoursAgo(hours) {
    return new Date(Date.now() - hours * 60 * 60 * 1000).toISOString();
}

const EPOCH_ISO = '1970-01-01T00:00:00.000Z';

/** `days <= 0` significa "nessun limite temporale" (finestra "Tutto" in admin). */
function cutoffDaysAgo(days) {
    return days > 0 ? new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString() : EPOCH_ISO;
}

/**
 * Lista carrelli con filtri opzionali e paginazione, per la vista admin.
 * @param {D1Database} db
 * @param {object} opts
 * @param {number}  [opts.page=1]
 * @param {'active'|'abandoned'|'checkout'|'paid'|'all'} [opts.status='abandoned']
 * @param {number}  [opts.hoursIdle=2]  soglia di inattività per "abbandonato"
 * @param {boolean} [opts.hasEmail]     filtra per presenza/assenza email
 * @param {string}  [opts.country]      filtro paese esatto (ISO-2)
 * @param {number}  [opts.days=30]      finestra temporale su updated_at (0/undefined = nessun limite)
 */
export async function listCarts(db, {
    page      = 1,
    status    = 'abandoned',
    hoursIdle = DEFAULT_HOURS_IDLE,
    hasEmail,
    country   = '',
    days      = 30,
} = {}) {
    const offset     = (Math.max(1, page) - 1) * PAGE_SIZE;
    const conditions = [];
    const bindings   = [];
    const cutoffIdle = isoHoursAgo(hoursIdle);

    if (days > 0) {
        conditions.push('cart_sessions.updated_at >= ?');
        bindings.push(cutoffDaysAgo(days));
    }

    if (status === 'active') {
        conditions.push('cart_sessions.checkout_order_id IS NULL', 'cart_sessions.item_count > 0', 'cart_sessions.updated_at >= ?');
        bindings.push(cutoffIdle);
    } else if (status === 'abandoned') {
        conditions.push('cart_sessions.checkout_order_id IS NULL', 'cart_sessions.item_count > 0', 'cart_sessions.updated_at < ?');
        bindings.push(cutoffIdle);
    } else if (status === 'checkout') {
        conditions.push('cart_sessions.checkout_order_id IS NOT NULL');
    } else if (status === 'paid') {
        conditions.push('cart_sessions.checkout_order_id IS NOT NULL', "orders.status = 'paid'");
    }
    // status === 'all' → nessun filtro aggiuntivo

    if (hasEmail === true)  conditions.push('cart_sessions.email IS NOT NULL');
    if (hasEmail === false) conditions.push('cart_sessions.email IS NULL');
    if (country) { conditions.push('cart_sessions.country = ?'); bindings.push(country); }

    const where = conditions.length ? 'WHERE ' + conditions.join(' AND ') : '';
    const join  = 'LEFT JOIN orders ON orders.id = cart_sessions.checkout_order_id';

    const [countRow, rows] = await Promise.all([
        db.prepare(`SELECT COUNT(*) as n FROM cart_sessions ${join} ${where}`)
          .bind(...bindings).first(),
        db.prepare(`
            SELECT cart_sessions.*, orders.status as order_status, orders.paid_at as order_paid_at
            FROM cart_sessions ${join} ${where}
            ORDER BY cart_sessions.updated_at DESC
            LIMIT ? OFFSET ?
        `).bind(...bindings, PAGE_SIZE, offset).all(),
    ]);

    return {
        carts:    (rows.results || []).map(formatCartRow),
        total:    countRow?.n ?? 0,
        page:     Math.max(1, page),
        pageSize: PAGE_SIZE,
    };
}

function formatCartRow(row) {
    return {
        cartId:            row.id,
        email:             row.email || null,
        locale:            row.locale,
        country:           row.country || null,
        lineItems:         safeParseJSON(row.line_items, []),
        itemCount:         row.item_count,
        totalMinor:        row.total_minor,
        currency:          row.currency,
        createdAt:         row.created_at,
        updatedAt:         row.updated_at,
        checkoutStartedAt: row.checkout_started_at || null,
        checkoutOrderId:   row.checkout_order_id   || null,
        orderStatus:       row.order_status        || null,
        orderPaidAt:       row.order_paid_at        || null,
    };
}

/* ─── Statistiche aggregate (vista admin "Carrelli") ─────────────────────────── */

/**
 * KPI aggregati sugli ultimi `days` giorni (default 30) per non mescolare
 * carrelli vecchissimi con la situazione commerciale corrente.
 */
export async function getCartStats(db, { days = 30, hoursIdle = DEFAULT_HOURS_IDLE } = {}) {
    const cutoffDays = cutoffDaysAgo(days);
    const cutoffIdle = isoHoursAgo(hoursIdle);

    const [counts, paidRow, topProducts, topCountries] = await Promise.all([
        db.prepare(`
            SELECT
                COUNT(*) as created,
                SUM(CASE WHEN checkout_order_id IS NULL AND item_count > 0 AND updated_at >= ? THEN 1 ELSE 0 END) as active,
                SUM(CASE WHEN checkout_order_id IS NULL AND item_count > 0 AND updated_at <  ? THEN 1 ELSE 0 END) as abandoned,
                SUM(CASE WHEN checkout_order_id IS NULL AND item_count > 0 AND updated_at <  ? THEN total_minor ELSE 0 END) as abandoned_value_minor,
                SUM(CASE WHEN checkout_order_id IS NOT NULL THEN 1 ELSE 0 END) as checkout_started
            FROM cart_sessions
            WHERE updated_at >= ?
        `).bind(cutoffIdle, cutoffIdle, cutoffIdle, cutoffDays).first(),

        db.prepare(`
            SELECT COUNT(*) as paid
            FROM cart_sessions
            JOIN orders ON orders.id = cart_sessions.checkout_order_id
            WHERE orders.status = 'paid' AND cart_sessions.updated_at >= ?
        `).bind(cutoffDays).first(),

        db.prepare(`
            SELECT je.value ->> 'sku' as sku, je.value ->> 'name' as name,
                   COUNT(DISTINCT cart_sessions.id) as carts
            FROM cart_sessions, json_each(cart_sessions.line_items) as je
            WHERE checkout_order_id IS NULL AND item_count > 0
              AND updated_at < ? AND updated_at >= ?
            GROUP BY sku
            ORDER BY carts DESC
            LIMIT 5
        `).bind(cutoffIdle, cutoffDays).all(),

        db.prepare(`
            SELECT country, COUNT(*) as carts
            FROM cart_sessions
            WHERE checkout_order_id IS NULL AND item_count > 0
              AND updated_at < ? AND updated_at >= ? AND country IS NOT NULL
            GROUP BY country
            ORDER BY carts DESC
            LIMIT 5
        `).bind(cutoffIdle, cutoffDays).all(),
    ]);

    const created         = counts?.created || 0;
    const active          = counts?.active || 0;
    const abandoned       = counts?.abandoned || 0;
    const checkoutStarted = counts?.checkout_started || 0;
    const paid            = paidRow?.paid || 0;
    const abandonedValueMinor = counts?.abandoned_value_minor || 0;

    return {
        days,
        created,
        active,
        abandoned,
        abandonmentRate:    created ? abandoned / created : 0,
        checkoutStarted,
        cartToCheckoutRate: created ? checkoutStarted / created : 0,
        paid,
        cartToPaidRate:     created ? paid / created : 0,
        abandonedValueMinor,
        abandonedAvgValueMinor: abandoned ? Math.round(abandonedValueMinor / abandoned) : 0,
        topProducts:  (topProducts.results  || []).map(r => ({ sku: r.sku, name: r.name, carts: r.carts })),
        topCountries: (topCountries.results || []).map(r => ({ country: r.country, carts: r.carts })),
    };
}
