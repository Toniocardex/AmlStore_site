/**
 * Trustpilot TrustBox — load only after marketing consent (ad_storage).
 * Shared by home + product pages.
 */
(function () {
    'use strict';

    var CONSENT_KEY = 'aml-consent-v2';
    var TRUSTPILOT_SCRIPT_ID = 'trustpilot-widget-script';
    var TRUSTPILOT_SCRIPT_SRC = 'https://widget.trustpilot.com/bootstrap/v5/tp.widget.bootstrap.min.js';

    function readMarketingConsent() {
        try {
            var raw = localStorage.getItem(CONSENT_KEY);
            if (!raw) return false;
            var parsed = JSON.parse(raw);
            var consent = parsed && parsed.consent;
            return Boolean(consent && consent.ad_storage === 'granted');
        } catch (_) {
            return false;
        }
    }

    function getTrustpilotWidget() {
        return document.getElementById('trustpilot-widget') || document.querySelector('.trustpilot-widget');
    }

    function setWidgetActive(active) {
        var widget = getTrustpilotWidget();
        if (widget) widget.classList.toggle('trustpilot-widget--active', active);
    }

    function hideTrustpilotFallback() {
        document.querySelectorAll('.trustpilot-fallback, .home-social-proof__fallback').forEach(function (el) {
            el.hidden = true;
        });
    }

    function loadTrustpilotWidget() {
        var widget = getTrustpilotWidget();
        if (!widget) return;

        var businessUnitId = (widget.getAttribute('data-businessunit-id') || '').trim();
        if (!businessUnitId) return;

        setWidgetActive(true);

        function bootstrapWidget() {
            if (window.Trustpilot && typeof window.Trustpilot.loadFromElement === 'function') {
                window.Trustpilot.loadFromElement(widget, true);
                hideTrustpilotFallback();
            }
        }

        if (document.getElementById(TRUSTPILOT_SCRIPT_ID)) {
            bootstrapWidget();
            return;
        }

        var script = document.createElement('script');
        script.id = TRUSTPILOT_SCRIPT_ID;
        script.src = TRUSTPILOT_SCRIPT_SRC;
        script.async = true;
        script.onload = bootstrapWidget;
        document.head.appendChild(script);
    }

    function initTrustpilot() {
        if (!readMarketingConsent()) {
            setWidgetActive(false);
            return;
        }
        loadTrustpilotWidget();
    }

    function onConsentUpdated(event) {
        var consent = event && event.detail;
        if (consent && consent.ad_storage === 'granted') {
            loadTrustpilotWidget();
        } else if (consent) {
            setWidgetActive(false);
        }
    }

    function init() {
        if (!getTrustpilotWidget()) return;
        initTrustpilot();
        window.addEventListener('aml-consent-updated', onConsentUpdated);
        window.addEventListener('storage', function (e) {
            if (e.key === CONSENT_KEY && readMarketingConsent()) {
                loadTrustpilotWidget();
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
