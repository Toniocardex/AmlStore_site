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
 * I bot riconosciuti (BOT_UA_RE) non vengono più scartati: sono registrati
 * con is_bot = 1 e restano fuori dagli aggregati di default, ma
 * getAnalyticsSummary può includerli su richiesta (opts.includeBots) così il
 * pannello admin li mostra come categoria a sé invece di farli sparire.
 *
 * Nessun cookie, nessun ID persistente: `visitor_hash` è un HMAC(ip+ua) con un
 * salt che include il giorno (kind = "pv-<day>"), quindi ruota ogni 24h e non è
 * riconducibile tra un giorno e l'altro. Riusa FRAUD_HASH_SECRET — nessun nuovo
 * secret da configurare. Fail-open ovunque: un errore qui non deve mai riflettersi
 * sulla risposta servita all'utente (il chiamante gira dentro waitUntil).
 */

import { now }                                       from './utils.js';
import { hmacIdentifier, bumpBucket, windowSlot }    from './rate-limit.js';

const ALLOWED_LOCALES = new Set(['it', 'en', 'fr', 'de', 'es', 'pt', 'nl']);

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
 * Esclude API, admin e asset statici. I bot noti (BOT_UA_RE) non sono
 * esclusi qui: passano il filtro e vengono registrati da recordPageView con
 * is_bot = 1, cosi' restano visibili come categoria a se' invece di sparire.
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

    return true;
}

/** Vero se lo User-Agent corrisponde a un bot/crawler noto (vedi BOT_UA_RE). */
export function isBotUA(ua) {
    return BOT_UA_RE.test(ua || '');
}

/* ─── Scrittura pageview ──────────────────────────────────────────────────────── */

function localeFromPath(path) {
    const seg = path.split('/').filter(Boolean)[0] || '';
    return ALLOWED_LOCALES.has(seg) ? seg : null;
}

/**
 * Ordina le lingue di un header Accept-Language per preferenza (q-value
 * decrescente, a parità di q mantiene l'ordine del header) e ne estrae i
 * primary subtag ('it-IT' -> 'it').
 */
function parseAcceptLanguage(header) {
    if (!header) return [];
    return header.split(',')
        .map((part, idx) => {
            const bits = part.trim().split(';q=');
            const tag = (bits[0] || '').trim();
            const q = bits[1] !== undefined ? parseFloat(bits[1]) : 1;
            return { tag, q: Number.isFinite(q) ? q : 1, idx };
        })
        .filter((e) => e.tag)
        .sort((a, b) => b.q - a.q || a.idx - b.idx)
        .map((e) => e.tag.split('-')[0].toLowerCase());
}

/**
 * Lingua che <aml-lang-suggest> (components/lang-suggest.js) suggerirebbe per
 * questa richiesta: stesso identico algoritmo del componente client
 * (topSupportedBrowserLang), solo che qui legge Accept-Language invece di
 * navigator.languages. Ferma la scansione alla prima lingua supportata
 * dell'header, anche se coincide con la pagina — non continua a cercarne
 * una diversa più in basso (altrimenti un browser bilingue it/en su una
 * pagina già in italiano risulterebbe "suggerirebbe inglese", falso: la sua
 * preferenza principale è già soddisfatta).
 */
function suggestedLangFromRequest(request, pageLocale) {
    const prefs = parseAcceptLanguage(request.headers.get('Accept-Language') || '');
    const top = prefs.find((code) => ALLOWED_LOCALES.has(code)) || null;
    return (top && top !== pageLocale) ? top : null;
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

/* Reload, tasto "indietro" o un bot che ribatte la stessa pagina in rapida
   successione non sono nuove visite: se lo stesso visitor_hash ha già una riga
   sullo stesso path entro questa finestra, la pageview non viene ri-contata. */
const PAGEVIEW_DEDUP_WINDOW_MS = 30 * 60 * 1000;

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

        const dedupSince = new Date(Date.parse(ts) - PAGEVIEW_DEDUP_WINDOW_MS).toISOString();
        const recent = await env.DB.prepare(`
            SELECT 1 FROM page_views
            WHERE day = ? AND path = ? AND visitor_hash = ? AND ts >= ?
            LIMIT 1
        `).bind(day, url.pathname, visitorHash, dedupSince).first();
        if (recent) return;

        const locale = localeFromPath(url.pathname);

        await env.DB.prepare(`
            INSERT INTO page_views (
                day, ts, path, locale, referrer_host, utm_source,
                country, device, visitor_hash, suggested_lang, is_bot
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `).bind(
            day, ts, url.pathname, locale,
            referrerHostFrom(request, url), url.searchParams.get('utm_source') || null,
            request.cf?.country || null, deviceFromUA(ua), visitorHash,
            suggestedLangFromRequest(request, locale), isBotUA(ua) ? 1 : 0
        ).run();
    } catch (e) {
        console.warn('[analytics] recordPageView fallita:', e?.message || e);
    }
}

/* ─── Eventi CRO (click PayPal Express, buy-now, purchase, ecc.) ──────────────── */
// Stessa impostazione privacy delle pageview: nessun cookie, visitor_hash HMAC
// che ruota ogni giorno, fail-open (mai nel path critico di un acquisto).
// 'purchase' è scritto solo server-side dagli handler di capture/webhook, mai
// dal client via /api/track, per restare un dato attendibile e non spoofabile.

export const TRACKABLE_EVENTS = new Set([
    'add_to_cart',
    'buy_now_click',
    'paypal_express_click',
    'paypal_opened',
    'paypal_approved',
    'paypal_captured',
    'paypal_cancelled',
    'paypal_failed',
]);

/**
 * Registra un evento CRO. Va chiamata con `await` (nessun waitUntil qui: gli
 * handler ordini/tracking non hanno un `context`, solo request/env) ma è
 * fail-open al suo interno — un suo errore non deve mai bloccare la risposta.
 * @param {object} env
 * @param {Request} request
 * @param {{eventName: string, orderId?: string, sku?: string}} params
 */
export async function recordEvent(env, request, { eventName, orderId, sku }) {
    const secret = env.FRAUD_HASH_SECRET;
    if (!secret || !env.DB) return;
    if (!TRACKABLE_EVENTS.has(eventName) && eventName !== 'purchase') return;

    try {
        const ua  = request.headers.get('User-Agent') || '';
        const ip  = request.headers.get('CF-Connecting-IP') || '';
        const ts  = now();
        const day = ts.slice(0, 10);

        const visitorHash = ip
            ? await hmacIdentifier(secret, `ev-${day}`, `${ip}|${ua}`)
            : await hmacIdentifier(secret, `ev-${day}`, `anon|${ua}`);

        await env.DB.prepare(`
            INSERT INTO analytics_events (id, event_name, order_id, sku, visitor_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        `).bind(crypto.randomUUID(), eventName, orderId || null, sku || null, visitorHash, ts).run();
    } catch (e) {
        console.warn('[analytics] recordEvent fallita:', e?.message || e);
    }
}

/* ─── Aggregati (vista admin) ─────────────────────────────────────────────────── */

const EPOCH_ISO = '1970-01-01';

function dayCutoff(days) {
    if (!(days > 0)) return EPOCH_ISO;
    return new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);
}

/**
 * Completa la serie giornaliera con i giorni a zero.
 *
 * `GROUP BY day` restituisce solo i giorni che hanno almeno una riga: passata
 * cosi' com'e' a un grafico, una settimana senza traffico sparisce e le barre
 * si stringono, facendo sembrare continuo un andamento che non lo e'. Qui la
 * serie viene riempita fino a oggi, cosi' un giorno vuoto resta visibile come
 * tale.
 */
function fillDailyGaps(rows, days) {
    if (!(days > 0)) return rows;

    const byDay = new Map(rows.map(r => [r.day, r]));
    const out = [];
    const cursor = new Date(`${dayCutoff(days)}T00:00:00Z`);
    const today = new Date(`${new Date().toISOString().slice(0, 10)}T00:00:00Z`);

    while (cursor <= today) {
        const day = cursor.toISOString().slice(0, 10);
        const row = byDay.get(day);
        out.push({ day, views: row?.views || 0, visitors: row?.visitors || 0 });
        cursor.setUTCDate(cursor.getUTCDate() + 1);
    }
    return out;
}

const DEFAULT_DAYS = 30;
const MAX_DAYS     = 365;

/**
 * Finestra in giorni proveniente dalla query string. Oltre a scartare i valori
 * non numerici, il tetto evita che un `?days=99999` faccia costruire a
 * fillDailyGaps una serie di decine di migliaia di punti.
 */
export function normalizeDays(value) {
    const n = Number(value);
    if (!Number.isFinite(n) || n <= 0) return DEFAULT_DAYS;
    return Math.min(Math.round(n), MAX_DAYS);
}

/**
 * Aggregati per la vista admin "Analytics", finestra di `days` giorni.
 *
 * Di default i bot (is_bot = 1, vedi recordPageView) restano fuori da tutti
 * gli aggregati: gonfierebbero pagine e conteggi con traffico che non è
 * pubblico reale. `botViews`/`botVisitors` sono comunque sempre calcolati sul
 * periodo, cosi' il pannello puo' mostrarne l'esistenza anche a bot esclusi.
 * Con `includeBots: true` il filtro cade e gli aggregati coprono tutto il
 * traffico, bot compresi.
 *
 * @param {D1Database} db
 * @param {object} opts
 * @param {number} [opts.days=30]
 * @param {boolean} [opts.includeBots=false]
 */
export async function getAnalyticsSummary(db, { days = DEFAULT_DAYS, includeBots = false } = {}) {
    days = normalizeDays(days);
    const cutoff = dayCutoff(days);
    const botClause = includeBots ? '' : 'AND is_bot = 0';

    const [totals, daily, topPages, topReferrers, topCountries, topSuggestedLangs, devices, direct, bots] = await Promise.all([
        db.prepare(`
            SELECT COUNT(*) as views, COUNT(DISTINCT visitor_hash) as visitors
            FROM page_views WHERE day >= ? ${botClause}
        `).bind(cutoff).first(),

        db.prepare(`
            SELECT day, COUNT(*) as views, COUNT(DISTINCT visitor_hash) as visitors
            FROM page_views WHERE day >= ? ${botClause}
            GROUP BY day ORDER BY day ASC
        `).bind(cutoff).all(),

        db.prepare(`
            SELECT path, COUNT(*) as views
            FROM page_views WHERE day >= ? ${botClause}
            GROUP BY path ORDER BY views DESC LIMIT 10
        `).bind(cutoff).all(),

        db.prepare(`
            SELECT referrer_host, COUNT(*) as views
            FROM page_views WHERE day >= ? AND referrer_host IS NOT NULL ${botClause}
            GROUP BY referrer_host ORDER BY views DESC LIMIT 10
        `).bind(cutoff).all(),

        db.prepare(`
            SELECT country, COUNT(*) as views
            FROM page_views WHERE day >= ? AND country IS NOT NULL ${botClause}
            GROUP BY country ORDER BY views DESC LIMIT 10
        `).bind(cutoff).all(),

        /* Lingua che <aml-lang-suggest> avrebbe suggerito (da Accept-Language,
           vedi suggestedLangFromRequest): quante pageview arrivano da un
           visitatore la cui lingua preferita differisce da quella della
           pagina, e verso quale lingua. NULL = nessun suggerimento (lingua
           già corretta, o nessuna delle 5 supportate in Accept-Language). */
        db.prepare(`
            SELECT suggested_lang, COUNT(*) as views
            FROM page_views WHERE day >= ? AND suggested_lang IS NOT NULL ${botClause}
            GROUP BY suggested_lang ORDER BY views DESC LIMIT 10
        `).bind(cutoff).all(),

        db.prepare(`
            SELECT device, COUNT(*) as views
            FROM page_views WHERE day >= ? ${botClause}
            GROUP BY device ORDER BY views DESC
        `).bind(cutoff).all(),

        /* Contato a parte e non per differenza dalla classifica: quella è
           limitata ai primi 10, quindi sottrarla dal totale farebbe passare per
           "diretto" anche il traffico delle sorgenti dall'undicesima in giù. */
        db.prepare(`
            SELECT COUNT(*) as views
            FROM page_views WHERE day >= ? AND referrer_host IS NULL ${botClause}
        `).bind(cutoff).first(),

        db.prepare(`
            SELECT COUNT(*) as views, COUNT(DISTINCT visitor_hash) as visitors
            FROM page_views WHERE day >= ? AND is_bot = 1
        `).bind(cutoff).first(),
    ]);

    /* `directViews` sta fuori dalla classifica: "nessun referrer" non e' una
       sorgente fra le altre, ma e' il dato che dice quanta parte del traffico
       non arriva da un link esterno. */
    return {
        days,
        includeBots,
        views:    totals?.views    || 0,
        visitors: totals?.visitors || 0,
        botViews:    bots?.views    || 0,
        botVisitors: bots?.visitors || 0,
        daily: fillDailyGaps(
            (daily.results || []).map(r => ({ day: r.day, views: r.views, visitors: r.visitors })),
            days
        ),
        topPages:     (topPages.results     || []).map(r => ({ path: r.path, views: r.views })),
        topReferrers: (topReferrers.results || []).map(r => ({ host: r.referrer_host, views: r.views })),
        directViews:  direct?.views || 0,
        topCountries: (topCountries.results || []).map(r => ({ country: r.country, views: r.views })),
        topSuggestedLangs: (topSuggestedLangs.results || []).map(r => ({ suggested_lang: r.suggested_lang, views: r.views })),
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
