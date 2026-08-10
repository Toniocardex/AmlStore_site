/**
 * analytics.js — pageview tracking server-side (analytics interna).
 *
 * Esporta:
 *   shouldTrackPageView(request, response)     — filtro: solo pagine HTML reali
 *   recordPageView(context, response)          — scrive una riga in page_views
 *   getAnalyticsSummary(db, opts)              — aggregati per la vista admin
 *   runAnalyticsRetention(db, env)             — cancella righe oltre il termine
 *   maybeRunAnalyticsRetention(context, opts)  — la lancia al più una volta all'ora
 *
 * Nessun cookie, nessun ID persistente: `visitor_hash` è un HMAC(ip+ua) con un
 * salt che include il giorno (kind = "pv-<day>"), quindi ruota ogni 24h e non è
 * riconducibile tra un giorno e l'altro. Riusa FRAUD_HASH_SECRET — nessun nuovo
 * secret da configurare. Fail-open ovunque: un errore qui non deve mai riflettersi
 * sulla risposta servita all'utente (il chiamante gira dentro waitUntil).
 */

import { now }                                       from './utils.js';
import { hmacIdentifier, bumpBucket, windowSlot }    from './rate-limit.js';

const ALLOWED_LOCALES = new Set(['it', 'en', 'fr', 'de', 'es']);

const STATIC_EXT_RE = /\.(css|js|mjs|json|png|jpe?g|webp|avif|gif|svg|ico|woff2?|ttf|eot|mp4|webm|pdf|xml|txt|map)$/i;

const BOT_UA_RE = new RegExp([
    'bot', 'crawl', 'spider', 'slurp', 'facebookexternalhit', 'whatsapp',
    'telegrambot', 'discordbot', 'semrush', 'ahrefs', 'mj12bot', 'petalbot',
    'bytespider', 'googlebot', 'bingbot', 'yandex', 'duckduckbot', 'applebot',
    'headlesschrome', 'pingdom', 'uptimerobot', 'lighthouse',
].join('|'), 'i');

/* ─── Filtro pageview ─────────────────────────────────────────────────────────── */

/**
 * Vero solo per navigazioni reali verso una pagina HTML servita con successo.
 * Esclude API, admin, asset statici e i bot più comuni.
 */
export function shouldTrackPageView(request, response) {
    if (request.method !== 'GET')   return false;
    if (response.status !== 200)    return false;

    const url = new URL(request.url);
    const path = url.pathname;
    if (path.startsWith('/api/'))   return false;
    if (path.startsWith('/admin'))  return false;
    if (STATIC_EXT_RE.test(path))   return false;

    const contentType = response.headers.get('content-type') || '';
    if (!contentType.includes('text/html')) return false;

    const ua = request.headers.get('User-Agent') || '';
    if (BOT_UA_RE.test(ua)) return false;

    return true;
}

/* ─── Scrittura pageview ──────────────────────────────────────────────────────── */

function localeFromPath(path) {
    const seg = path.split('/').filter(Boolean)[0] || '';
    return ALLOWED_LOCALES.has(seg) ? seg : null;
}

function referrerHostFrom(request, siteUrl) {
    const raw = request.headers.get('Referer');
    if (!raw) return null;
    try {
        const host = new URL(raw).hostname;
        return host === siteUrl.hostname ? null : host;
    } catch (_) {
        return null;
    }
}

function deviceFromUA(ua) {
    if (/mobile/i.test(ua))                          return 'mobile';
    if (/tablet|ipad/i.test(ua))                      return 'tablet';
    return 'desktop';
}

/**
 * Registra una pageview. Va chiamata dopo next(), dentro context.waitUntil.
 * @param {object} context   contesto Pages Functions (request, env)
 */
export async function recordPageView(context) {
    const { request, env } = context;
    const secret = env.FRAUD_HASH_SECRET;
    if (!secret || !env.DB) return;

    try {
        const url  = new URL(request.url);
        const ua   = request.headers.get('User-Agent') || '';
        const ip   = request.headers.get('CF-Connecting-IP') || '';
        const ts   = now();
        const day  = ts.slice(0, 10);

        const visitorHash = ip
            ? await hmacIdentifier(secret, `pv-${day}`, `${ip}|${ua}`)
            : await hmacIdentifier(secret, `pv-${day}`, `anon|${ua}`);

        await env.DB.prepare(`
            INSERT INTO page_views (
                day, ts, path, locale, referrer_host, utm_source,
                country, device, visitor_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        `).bind(
            day, ts, url.pathname, localeFromPath(url.pathname),
            referrerHostFrom(request, url), url.searchParams.get('utm_source') || null,
            request.cf?.country || null, deviceFromUA(ua), visitorHash
        ).run();
    } catch (e) {
        console.warn('[analytics] recordPageView fallita:', e?.message || e);
    }
}

/* ─── Aggregati (vista admin) ─────────────────────────────────────────────────── */

const EPOCH_ISO = '1970-01-01';

function dayCutoff(days) {
    if (!(days > 0)) return EPOCH_ISO;
    return new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);
}

/**
 * Aggregati per la vista admin "Analytics", finestra di `days` giorni.
 * @param {D1Database} db
 * @param {object} opts
 * @param {number} [opts.days=30]
 */
export async function getAnalyticsSummary(db, { days = 30 } = {}) {
    const cutoff = dayCutoff(days);

    const [totals, daily, topPages, topReferrers, topCountries, devices] = await Promise.all([
        db.prepare(`
            SELECT COUNT(*) as views, COUNT(DISTINCT visitor_hash) as visitors
            FROM page_views WHERE day >= ?
        `).bind(cutoff).first(),

        db.prepare(`
            SELECT day, COUNT(*) as views, COUNT(DISTINCT visitor_hash) as visitors
            FROM page_views WHERE day >= ?
            GROUP BY day ORDER BY day ASC
        `).bind(cutoff).all(),

        db.prepare(`
            SELECT path, COUNT(*) as views
            FROM page_views WHERE day >= ?
            GROUP BY path ORDER BY views DESC LIMIT 10
        `).bind(cutoff).all(),

        db.prepare(`
            SELECT referrer_host, COUNT(*) as views
            FROM page_views WHERE day >= ? AND referrer_host IS NOT NULL
            GROUP BY referrer_host ORDER BY views DESC LIMIT 10
        `).bind(cutoff).all(),

        db.prepare(`
            SELECT country, COUNT(*) as views
            FROM page_views WHERE day >= ? AND country IS NOT NULL
            GROUP BY country ORDER BY views DESC LIMIT 10
        `).bind(cutoff).all(),

        db.prepare(`
            SELECT device, COUNT(*) as views
            FROM page_views WHERE day >= ?
            GROUP BY device ORDER BY views DESC
        `).bind(cutoff).all(),
    ]);

    return {
        days,
        views:    totals?.views    || 0,
        visitors: totals?.visitors || 0,
        daily:        (daily.results        || []).map(r => ({ day: r.day, views: r.views, visitors: r.visitors })),
        topPages:     (topPages.results     || []).map(r => ({ path: r.path, views: r.views })),
        topReferrers: (topReferrers.results || []).map(r => ({ host: r.referrer_host, views: r.views })),
        topCountries: (topCountries.results || []).map(r => ({ country: r.country, views: r.views })),
        devices:      (devices.results      || []).map(r => ({ device: r.device, views: r.views })),
    };
}

/* ─── Conservazione limitata ──────────────────────────────────────────────────── */

const RETENTION_DELETE_DAYS_DEFAULT = 400;
const RETENTION_LOCK_WINDOW_MS      = 60 * 60 * 1000;

function retentionDeleteDays(env) {
    const n = Number(env?.ANALYTICS_DELETE_AFTER_DAYS);
    return Number.isFinite(n) && n > 0 ? Math.floor(n) : RETENTION_DELETE_DAYS_DEFAULT;
}

/** Cancella le pageview oltre il termine di conservazione. Nessun dato personale da anonimizzare a monte. */
export async function runAnalyticsRetention(db, env) {
    const deleteAfterDays = retentionDeleteDays(env);
    const cutoff = dayCutoff(deleteAfterDays);
    const deleted = await db.prepare('DELETE FROM page_views WHERE day < ?').bind(cutoff).run();
    return { deleteAfterDays, deleted: deleted?.meta?.changes ?? 0 };
}

/**
 * Lancia la pulizia al più una volta all'ora, in coda alla risposta.
 * Stesso schema di maybeRunCartRetention in cart.js: lock via bumpBucket
 * (INSERT..ON CONFLICT atomico), waitUntil per non pagare la latenza.
 */
export function maybeRunAnalyticsRetention(context, { cheapGate = false } = {}) {
    const { env } = context;
    if (!env?.DB) return;
    if (cheapGate && new Date().getUTCMinutes() >= 2) return;

    const work = (async () => {
        try {
            const windowId = `1h:${windowSlot(RETENTION_LOCK_WINDOW_MS)}`;
            const count = await bumpBucket(env.DB, 'analytics-retention', windowId);
            if (count !== 1) return;
            const res = await runAnalyticsRetention(env.DB, env);
            if (res.deleted) {
                console.log(`[analytics] retention: ${res.deleted} righe cancellate (>${res.deleteAfterDays}gg)`);
            }
        } catch (e) {
            console.warn('[analytics] retention fallita:', e?.message || e);
        }
    })();

    if (typeof context.waitUntil === 'function') context.waitUntil(work);
}
