/**
 * functions/_middleware.js — Pages Function globale, gira su ogni richiesta
 * (asset statici inclusi) prima che venga servita.
 *
 * Solo cablaggio: il tracking vive in api/_lib/analytics.js, l'allineamento
 * della disponibilita' per i crawler in api/_lib/seo-availability.js.
 */

import { shouldTrackPageView, recordPageView, maybeRunAnalyticsRetention } from './api/_lib/analytics.js';
import {
    physicalSkuForPath,
    isShoppingFeedPath,
    rewriteProductAvailability,
    rewriteFeedAvailability,
} from './api/_lib/seo-availability.js';

export async function onRequest(context) {
    const response = await context.next();

    if (shouldTrackPageView(context.request, response)) {
        context.waitUntil(recordPageView(context));
        // Agganciata alla pageview, non a ogni richiesta: una pagina carica
        // decine di asset (css/js/immagini/font), che passano comunque da qui
        // ma non devono ciascuno tentare il lock di retention.
        maybeRunAnalyticsRetention(context, { cheapGate: true });
    }

    return await applyAvailability(context, response);
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
