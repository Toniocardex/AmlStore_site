/**
 * functions/_middleware.js — Pages Function globale, gira su ogni richiesta
 * (asset statici inclusi) prima che venga servita.
 *
 * Solo cablaggio: la logica di tracking vive in api/_lib/analytics.js.
 */

import { shouldTrackPageView, recordPageView, maybeRunAnalyticsRetention } from './api/_lib/analytics.js';

export async function onRequest(context) {
    const response = await context.next();

    if (shouldTrackPageView(context.request, response)) {
        context.waitUntil(recordPageView(context));
        // Agganciata alla pageview, non a ogni richiesta: una pagina carica
        // decine di asset (css/js/immagini/font), che passano comunque da qui
        // ma non devono ciascuno tentare il lock di retention.
        maybeRunAnalyticsRetention(context, { cheapGate: true });
    }

    return response;
}
