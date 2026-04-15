/**
 * Google Consent Mode v2 — default e ripristino da preferenze salvate.
 * Caricare come primo script in <head>, prima di Google Tag Manager / gtag.js.
 * Dopo questo file è sicuro inserire GTM (snippet consigliato da Google).
 */
(function (w) {
    'use strict';

    var STORAGE_KEY = 'aml-consent-v2';

    w.dataLayer = w.dataLayer || [];
    if (typeof w.gtag !== 'function') {
        w.gtag = function gtag() {
            w.dataLayer.push(arguments);
        };
    }

    w.gtag('consent', 'default', {
        ad_storage: 'denied',
        ad_user_data: 'denied',
        ad_personalization: 'denied',
        analytics_storage: 'denied',
        functionality_storage: 'denied',
        personalization_storage: 'denied',
        security_storage: 'granted',
        wait_for_update: 500,
    });

    try {
        var raw = w.localStorage.getItem(STORAGE_KEY);
        if (!raw) return;
        var parsed = JSON.parse(raw);
        if (!parsed || !parsed.consent || typeof parsed.consent !== 'object') return;
        w.gtag('consent', 'update', parsed.consent);
    } catch (_) {
        /* ignore */
    }
})(typeof window !== 'undefined' ? window : globalThis);
