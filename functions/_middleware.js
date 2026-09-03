/**
 * functions/_middleware.js — Pages Function globale, gira su ogni richiesta
 * (asset statici inclusi) prima che venga servita.
 *
 * Cablaggio: il tracking vive in api/_lib/analytics.js, l'allineamento della
 * disponibilita' per i crawler in api/_lib/seo-availability.js. Qui viene anche
 * applicato l'header Content-Security-Policy (vedi CSP piu' sotto): sta in
 * codice e non in _headers perche' Cloudflare Pages scarta silenziosamente le
 * righe di _headers oltre ~2000 caratteri e la nostra CSP e' piu' lunga.
 */

import { shouldTrackPageView, recordPageView, maybeRunAnalyticsRetention } from './api/_lib/analytics.js';
import {
    physicalSkuForPath,
    isShoppingFeedPath,
    rewriteProductAvailability,
    rewriteFeedAvailability,
} from './api/_lib/seo-availability.js';

// CSP forbids wildcards on the TLD side (https://www.google.*), quindi i domini
// Google di mercato vanno elencati uno per uno.
const GOOGLE_MARKET_HOSTS = [
    'com', 'it', 'de', 'fr', 'es', 'ie', 'co.uk', 'nl', 'be', 'at', 'ch', 'pt', 'pl',
]
    .flatMap((tld) => [`https://www.google.${tld}`, `https://google.${tld}`])
    .join(' ');

// Sorgente unica della Content-Security-Policy servita sulle pagine HTML.
// Aggiornare qui quando si aggiunge un fornitore terzo (tag, pixel, iframe).
const CSP = [
    "default-src 'self'",
    "base-uri 'self'",
    "object-src 'none'",
    "frame-ancestors 'none'",
    "form-action 'self'",
    "script-src 'self' 'unsafe-inline' https://js.stripe.com https://widget.trustpilot.com " +
        'https://*.paypal.com https://*.paypalobjects.com https://www.googletagmanager.com ' +
        'https://www.google-analytics.com https://www.googleadservices.com https://www.google.com ' +
        'https://google.com https://pagead2.googlesyndication.com https://googleads.g.doubleclick.net ' +
        'https://www.clarity.ms https://*.clarity.ms',
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "img-src 'self' data: https://*.clarity.ms https://c.bing.com https://*.stripe.com " +
        'https://*.trustpilot.com https://*.paypalobjects.com https://*.google-analytics.com ' +
        'https://www.googletagmanager.com https://*.g.doubleclick.net https://googleads.g.doubleclick.net ' +
        'https://pagead2.googlesyndication.com https://www.googleadservices.com https://www.gstatic.com ' +
        `https://ssl.gstatic.com ${GOOGLE_MARKET_HOSTS}`,
    "font-src 'self' data: https://fonts.gstatic.com",
    "connect-src 'self' https://api.stripe.com https://js.stripe.com https://*.trustpilot.com " +
        'https://*.paypal.com https://*.paypalobjects.com https://*.google-analytics.com ' +
        'https://*.analytics.google.com https://www.googletagmanager.com https://*.g.doubleclick.net ' +
        'https://googleads.g.doubleclick.net https://ad.doubleclick.net https://pagead2.googlesyndication.com ' +
        'https://www.googleadservices.com https://*.merchant-center-analytics.goog ' +
        `https://*.clarity.ms https://c.bing.com ${GOOGLE_MARKET_HOSTS}`,
    'frame-src https://js.stripe.com https://hooks.stripe.com https://widget.trustpilot.com ' +
        'https://*.paypal.com https://www.googletagmanager.com https://*.doubleclick.net ' +
        'https://www.googleadservices.com',
    "worker-src 'self' blob:",
    "manifest-src 'self'",
    "media-src 'self'",
    'upgrade-insecure-requests',
].join('; ');

export async function onRequest(context) {
    const response = await context.next();

    if (shouldTrackPageView(context.request, response)) {
        context.waitUntil(recordPageView(context));
        // Agganciata alla pageview, non a ogni richiesta: una pagina carica
        // decine di asset (css/js/immagini/font), che passano comunque da qui
        // ma non devono ciascuno tentare il lock di retention.
        maybeRunAnalyticsRetention(context, { cheapGate: true });
    }

    return withContentSecurityPolicy(await applyAvailability(context, response));
}

/**
 * Applica la CSP alle sole risposte HTML (le pagine). Asset statici, JSON delle
 * API e redirect non ne hanno bisogno e resterebbero appesantiti inutilmente.
 * La risposta viene ricreata perche' gli header di quella servita da
 * context.next() sono immutabili.
 */
function withContentSecurityPolicy(response) {
    const contentType = response.headers.get('content-type') || '';
    if (!contentType.includes('text/html')) return response;

    const withCsp = new Response(response.body, response);
    withCsp.headers.set('Content-Security-Policy', CSP);
    return withCsp;
}

/**
 * Riscrive la disponibilita' dichiarata (JSON-LD delle pagine fisiche, g:availability
 * del feed Merchant) sul magazzino reale. Su qualunque errore restituisce la
 * risposta statica intatta: meglio il valore di fallback della pagina che una
 * 500 su un URL indicizzato.
 */
async function applyAvailability(context, response) {
    const db = context.env && context.env.DB;
    if (!db || context.request.method !== 'GET') return response;

    try {
        const { pathname } = new URL(context.request.url);

        const sku = physicalSkuForPath(pathname);
        if (sku) return await rewriteProductAvailability(db, sku, response);

        if (isShoppingFeedPath(pathname)) return await rewriteFeedAvailability(db, response);
    } catch (e) {
        console.warn('[seo-availability] rewrite fallito:', e?.message || e);
    }

    return response;
}
