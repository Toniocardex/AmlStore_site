/**
 * Microsoft Clarity — sempre attivo, cookie solo col consenso analytics.
 *
 * Variante "cookieless prima del consenso": Clarity si carica a ogni visita e
 * raccoglie heatmap/registrazioni in modalita' cookieless; passa al tracciamento
 * con cookie (_clck/_clsk, stitching tra sessioni) solo quando l'utente concede
 * la categoria "Misurazione e statistiche" dal cookie banner.
 *
 * REQUISITO LATO CLARITY: nel dashboard del progetto, Settings -> Setup ->
 * "Cookie" deve restare ATTIVATO (default). E' il permesso a usare i cookie
 * quando il consenso lo consente; la modalita' senza cookie prima del consenso
 * la impone questo loader chiamando clarity('consent', false). Con "Cookie"
 * disattivato Clarity sarebbe sempre cookieless e clarity('consent', true) non
 * riabiliterebbe i cookie dopo il consenso.
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

    // Segnaliamo SEMPRE lo stato a Clarity, gia' al primo load:
    //   granted            -> clarity('consent', true)  -> cookie (_clck/_clsk, stitching)
    //   assente o negato    -> clarity('consent', false) -> modalita' senza cookie
    // La chiamata immediata (prima ancora che il tag sia scaricato) finisce in
    // coda e viene processata da clarity.js all'avvio, cosi' i cookie non
    // vengono mai impostati senza consenso.
    function syncConsent(consent) {
        try {
            w.clarity('consent', analyticsGranted(consent));
        } catch (_) {
            /* la coda assorbe la chiamata finche' il tag non e' pronto */
        }
    }

    syncConsent(readStoredConsent());

    w.addEventListener('aml-consent-updated', function (ev) {
        syncConsent(ev && ev.detail ? ev.detail : readStoredConsent());
    });
})(window, document);
