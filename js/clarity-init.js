/**
 * Microsoft Clarity — sempre attivo, cookie solo col consenso analytics.
 *
 * Variante "cookieless prima del consenso": Clarity si carica a ogni visita e
 * raccoglie heatmap/registrazioni in modalita' cookieless; passa al tracciamento
 * con cookie (_clck/_clsk, stitching tra sessioni) solo quando l'utente concede
 * la categoria "Misurazione e statistiche" dal cookie banner.
 *
 * REQUISITO LATO CLARITY: nel dashboard del progetto, Settings -> Setup ->
 * "Cookie consent" deve essere ON, altrimenti Clarity parte gia' con i cookie
 * ignorando lo stato gestito qui sotto.
 *
 * Il consenso e' persistito in localStorage 'aml-consent-v2' e gli aggiornamenti
 * arrivano via evento 'aml-consent-updated' (vedi components/cookie-banner.js).
 * Speculare a consent-init.js, che fa lo stesso per Google Consent Mode.
 */
(function (w, d) {
    'use strict';

    var STORAGE_KEY = 'aml-consent-v2';
    var CLARITY_PROJECT_ID = 'yarcggnbi3';

    function analyticsGranted(consent) {
        return !!consent && consent.analytics_storage === 'granted';
    }

    function readStoredConsent() {
        try {
            var raw = w.localStorage.getItem(STORAGE_KEY);
            if (!raw) return null;
            var parsed = JSON.parse(raw);
            return parsed && parsed.consent && typeof parsed.consent === 'object'
                ? parsed.consent
                : null;
        } catch (_) {
            return null;
        }
    }

    // Snippet ufficiale Clarity: carica il tag e crea la coda w.clarity(...).
    (function (c, l, a, r, i, t, y) {
        c[a] = c[a] || function () {
            (c[a].q = c[a].q || []).push(arguments);
        };
        t = l.createElement(r);
        t.async = 1;
        t.src = 'https://www.clarity.ms/tag/' + i;
        y = l.getElementsByTagName(r)[0];
        y.parentNode.insertBefore(t, y);
    })(w, d, 'clarity', 'script', CLARITY_PROJECT_ID);

    // true  -> tracciamento con cookie (stitching tra sessioni)
    // false -> revoca esplicita, Clarity torna/resta in cookieless
    // Senza scelta salvata non chiamiamo nulla: con "Cookie consent" ON Clarity
    // e' gia' in cookieless di default e una chiamata sarebbe rumore.
    function syncConsent(consent, force) {
        if (!consent && !force) return;
        try {
            w.clarity('consent', analyticsGranted(consent));
        } catch (_) {
            /* la coda assorbe la chiamata finche' il tag non e' pronto */
        }
    }

    syncConsent(readStoredConsent(), false);

    w.addEventListener('aml-consent-updated', function (ev) {
        syncConsent(ev && ev.detail ? ev.detail : readStoredConsent(), true);
    });
})(window, document);
