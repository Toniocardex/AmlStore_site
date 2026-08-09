/**
 * cart.js — helper D1 per il tracking carrelli (analytics fase 1).
 *
 * Esporta:
 *   upsertCartSession(db, params)          — upsert snapshot carrello (anche vuoto)
 *   markCartCheckoutStarted(db, id, orderId) — collega un cartId a un ordine creato
 *   checkCartSyncRateLimit(env, request)   — rate limit per IP su /api/cart/sync
 *   listCarts(db, opts)                    — lista admin paginata e filtrabile
 *   getCartStats(db, opts)                 — KPI aggregati per la vista admin
 *   normalizeHoursIdle(value)              — valida la soglia "inattivo da N ore"
 *   runCartRetention(db, env)              — applica i termini di conservazione
 *   maybeRunCartRetention(context)         — la lancia al piu' una volta all'ora
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

/* ─── Conservazione limitata ─────────────────────────────────────────────────── */

/*
 * I carrelli sono dati personali raccolti col consenso alla misurazione: senza
 * un termine tecnico che li faccia scadere resterebbero in D1 per sempre, email
 * comprese. Due stadi, contati dall'ultima attivita' (`updated_at`):
 *
 *   1. dopo ANONYMIZE giorni  -> `email` azzerata; la riga resta e continua a
 *      contribuire alle statistiche aggregate, che non usano l'email;
 *   2. dopo DELETE giorni     -> la riga sparisce.
 *
 * Le finestre della vista admin arrivano a 90 giorni, quindi il default di 180
 * per la cancellazione non toglie nulla di operativo. Entrambi i termini sono
 * sovrascrivibili da variabile d'ambiente.
 */
const RETENTION_ANONYMIZE_DAYS_DEFAULT = 30;
const RETENTION_DELETE_DAYS_DEFAULT    = 180;
const RETENTION_LOCK_WINDOW_MS         = 60 * 60 * 1000;

function retentionDays(env) {
    const read = (key, fallback) => {
        const n = Number(env?.[key]);
        return Number.isFinite(n) && n > 0 ? Math.floor(n) : fallback;
    };
    const anonymize = read('CART_ANONYMIZE_AFTER_DAYS', RETENTION_ANONYMIZE_DAYS_DEFAULT);
    const remove    = read('CART_DELETE_AFTER_DAYS', RETENTION_DELETE_DAYS_DEFAULT);
    // Cancellare prima di anonimizzare renderebbe il primo stadio inutile.
    return { anonymize, remove: Math.max(anonymize, remove) };
}

/** Applica i due stadi. Restituisce quante righe ha toccato. */
export async function runCartRetention(db, env) {
    const { anonymize, remove } = retentionDays(env);

    const anonymized = await db.prepare(`
        UPDATE cart_sessions
        SET email = NULL
        WHERE email IS NOT NULL AND updated_at < ?
    `).bind(cutoffDaysAgo(anonymize)).run();

    const deleted = await db.prepare(`
        DELETE FROM cart_sessions WHERE updated_at < ?
    `).bind(cutoffDaysAgo(remove)).run();

    return {
        anonymizedAfterDays: anonymize,
        deletedAfterDays:    remove,
        anonymized:          anonymized?.meta?.changes ?? 0,
        deleted:             deleted?.meta?.changes ?? 0,
    };
}

/**
 * Lancia la pulizia al massimo una volta all'ora, in coda alla risposta.
 *
 * Pages Functions non ha cron trigger, quindi il giro parte dal traffico. Il
 * "chi lo fa" si decide con lo stesso bucket usato dal rate limit: l'INSERT..
 * ON CONFLICT e' atomico e restituisce il contatore, quindi solo la prima
 * richiesta della finestra oraria vede 1 e procede. `waitUntil` la sposta dopo
 * la risposta: l'utente non paga la latenza.
 *
 * `cheapGate` serve a non pagare quella scrittura su ogni sync: /api/cart/sync
 * fa gia' un bumpBucket per il rate limit, e tentare sempre anche il lock ne
 * raddoppierebbe le scritture su D1 per non fare nulla nel 99,99% dei casi. Sul
 * percorso pubblico si prova quindi solo a inizio ora; la vista admin, che e'
 * rara, tenta sempre, cosi' la pulizia ha comunque un innesco certo.
 *
 * @param {object} context             contesto Pages Functions (env, waitUntil)
 * @param {boolean} [opts.cheapGate]   true sui percorsi ad alto traffico
 */
export function maybeRunCartRetention(context, { cheapGate = false } = {}) {
    const { env } = context;
    if (!env?.DB) return;
    if (cheapGate && new Date().getUTCMinutes() >= 2) return;

    const work = (async () => {
        try {
            const windowId = `1h:${windowSlot(RETENTION_LOCK_WINDOW_MS)}`;
            const count = await bumpBucket(env.DB, 'cart-retention', windowId);
            if (count !== 1) return;
            const res = await runCartRetention(env.DB, env);
            if (res.anonymized || res.deleted) {
                console.log(
                    `[cart] retention: ${res.anonymized} email azzerate (>${res.anonymizedAfterDays}gg), ` +
                    `${res.deleted} righe cancellate (>${res.deletedAfterDays}gg)`
                );
            }
        } catch (e) {
            // Non deve mai disturbare la richiesta in corso.
            console.warn('[cart] retention fallita:', e?.message || e);
        }
    })();

    if (typeof context.waitUntil === 'function') context.waitUntil(work);
}

/* ─── Query D1 lista admin ───────────────────────────────────────────────────── */

const PAGE_SIZE = 50;
const DEFAULT_HOURS_IDLE = 2;
const MAX_HOURS_IDLE = 24 * 30;

/**
 * Soglia "inattivo da N ore" proveniente dalla query string: un valore non
 * numerico diventerebbe NaN e farebbe esplodere `toISOString()`.
 */
export function normalizeHoursIdle(value) {
    const n = Number(value);
    if (!Number.isFinite(n) || n <= 0) return DEFAULT_HOURS_IDLE;
    return Math.min(Math.round(n), MAX_HOURS_IDLE);
}

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
 * @param {number}  [opts.days=30]      finestra temporale su created_at (0 = nessun limite)
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

    // Il periodo e' una coorte: "carrelli nati in questi giorni", non "toccati".
    // Filtrare su updated_at faceva rientrare nel periodo carrelli molto piu'
    // vecchi solo perche' ripresi di recente, e faceva divergere i numeri della
    // sidebar da quelli della tabella.
    if (days > 0) {
        conditions.push('cart_sessions.created_at >= ?');
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
 * KPI aggregati sulla coorte dei carrelli **nati** negli ultimi `days` giorni.
 *
 * Due scelte che cambiano i numeri rispetto alla prima versione:
 *
 *  - la finestra e' su `created_at`, non su `updated_at`: "di quelli iniziati
 *    nel periodo, com'e' finita". Prima un carrello di due mesi fa ripreso ieri
 *    entrava fra i "creati negli ultimi 30 giorni";
 *  - il denominatore conta solo i carrelli che hanno avuto contenuto. Prima era
 *    `COUNT(*)`, quindi comprendeva anche quelli svuotati dall'utente, che pero'
 *    sono esclusi dai numeratori (`item_count > 0`): il tasso di abbandono
 *    risultava sistematicamente piu' basso del reale. I carrelli svuotati sono
 *    ora esposti a parte come `emptied`, invece di sparire dentro il totale.
 */
export async function getCartStats(db, { days = 30, hoursIdle = DEFAULT_HOURS_IDLE } = {}) {
    const cutoffDays = cutoffDaysAgo(days);
    const cutoffIdle = isoHoursAgo(hoursIdle);

    /* Un carrello "ha avuto contenuto" se ne ha ancora, o se e' arrivato al
       checkout (dopo il quale lo snapshot puo' essere vuoto). */
    const HAD_CONTENT = '(item_count > 0 OR checkout_order_id IS NOT NULL)';

    const [counts, paidRow, topProducts, topCountries] = await Promise.all([
        db.prepare(`
            SELECT
                SUM(CASE WHEN ${HAD_CONTENT} THEN 1 ELSE 0 END) as created,
                SUM(CASE WHEN NOT ${HAD_CONTENT} THEN 1 ELSE 0 END) as emptied,
                SUM(CASE WHEN checkout_order_id IS NULL AND item_count > 0 AND updated_at >= ? THEN 1 ELSE 0 END) as active,
                SUM(CASE WHEN checkout_order_id IS NULL AND item_count > 0 AND updated_at <  ? THEN 1 ELSE 0 END) as abandoned,
                SUM(CASE WHEN checkout_order_id IS NULL AND item_count > 0 AND updated_at <  ? THEN total_minor ELSE 0 END) as abandoned_value_minor,
                SUM(CASE WHEN checkout_order_id IS NOT NULL THEN 1 ELSE 0 END) as checkout_started
            FROM cart_sessions
            WHERE created_at >= ?
        `).bind(cutoffIdle, cutoffIdle, cutoffIdle, cutoffDays).first(),

        db.prepare(`
            SELECT COUNT(*) as paid
            FROM cart_sessions
            JOIN orders ON orders.id = cart_sessions.checkout_order_id
            WHERE orders.status = 'paid' AND cart_sessions.created_at >= ?
        `).bind(cutoffDays).first(),

        db.prepare(`
            SELECT je.value ->> 'sku' as sku, je.value ->> 'name' as name,
                   COUNT(DISTINCT cart_sessions.id) as carts
            FROM cart_sessions, json_each(cart_sessions.line_items) as je
            WHERE checkout_order_id IS NULL AND item_count > 0
              AND updated_at < ? AND created_at >= ?
            GROUP BY sku
            ORDER BY carts DESC
            LIMIT 5
        `).bind(cutoffIdle, cutoffDays).all(),

        db.prepare(`
            SELECT country, COUNT(*) as carts
            FROM cart_sessions
            WHERE checkout_order_id IS NULL AND item_count > 0
              AND updated_at < ? AND created_at >= ? AND country IS NOT NULL
            GROUP BY country
            ORDER BY carts DESC
            LIMIT 5
        `).bind(cutoffIdle, cutoffDays).all(),
    ]);

    const created         = counts?.created || 0;
    const emptied         = counts?.emptied || 0;
    const active          = counts?.active || 0;
    const abandoned       = counts?.abandoned || 0;
    const checkoutStarted = counts?.checkout_started || 0;
    const paid            = paidRow?.paid || 0;
    const abandonedValueMinor = counts?.abandoned_value_minor || 0;

    return {
        days,
        hoursIdle,
        created,
        emptied,
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
