/**
 * Trustpilot TrustBox — load only after marketing consent (ad_storage),
 * and only when the widget is near the viewport.
 * Shared by home + product pages.
 */
(function () {
    'use strict';

    var CONSENT_KEY = 'aml-consent-v2';
    var TRUSTPILOT_SCRIPT_ID = 'trustpilot-widget-script';
    var TRUSTPILOT_SCRIPT_SRC = 'https://widget.trustpilot.com/bootstrap/v5/tp.widget.bootstrap.min.js';
    var LOAD_ROOT_MARGIN = '200px 0px';

    var _nearViewportObserver = null;
    var _loadStarted = false;

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

    function setTrustpilotFallbackVisible(visible) {
        document.querySelectorAll('.trustpilot-fallback, .home-social-proof__fallback').forEach(function (el) {
            el.hidden = !visible;
        });
    }

    function getLoadTarget(widget) {
        return (
            widget.closest('.home-social-proof, .product-trustpilot') ||
            widget.parentElement ||
            widget
        );
    }

    function disconnectNearViewportObserver() {
        if (_nearViewportObserver) {
            _nearViewportObserver.disconnect();
            _nearViewportObserver = null;
        }
    }

    function renderTrustpilotWidget(widget) {
        if (!window.Trustpilot || typeof window.Trustpilot.loadFromElement !== 'function') return false;

        try {
            setWidgetActive(true);
            window.Trustpilot.loadFromElement(widget, true);
            setTrustpilotFallbackVisible(false);
            return true;
        } catch (_) {
            setWidgetActive(false);
            setTrustpilotFallbackVisible(true);
            return false;
        }
    }

    function loadTrustpilotWidget() {
        var widget = getTrustpilotWidget();
        if (!widget) return;

        var businessUnitId = (widget.getAttribute('data-businessunit-id') || '').trim();
        if (!businessUnitId) return;

        if (_loadStarted && document.getElementById(TRUSTPILOT_SCRIPT_ID)) {
            renderTrustpilotWidget(widget);
            return;
        }
        _loadStarted = true;
        disconnectNearViewportObserver();

        function bootstrapWidget() {
            renderTrustpilotWidget(widget);
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
        script.onerror = function () {
            _loadStarted = false;
            setWidgetActive(false);
            setTrustpilotFallbackVisible(true);
            script.remove();
        };
        document.head.appendChild(script);
    }

    /** Consent granted → load when widget is near viewport (or immediately if no IO). */
    function scheduleTrustpilotLoad() {
        var widget = getTrustpilotWidget();
        if (!widget) return;

        if (_loadStarted) {
            loadTrustpilotWidget();
            return;
        }

        if (!('IntersectionObserver' in window)) {
            loadTrustpilotWidget();
            return;
        }

        disconnectNearViewportObserver();
        _nearViewportObserver = new IntersectionObserver(
            function (entries) {
                var e = entries[0];
                if (!e || !e.isIntersecting) return;
                loadTrustpilotWidget();
            },
            { root: null, rootMargin: LOAD_ROOT_MARGIN, threshold: 0 }
        );
        _nearViewportObserver.observe(getLoadTarget(widget));
    }

    function initTrustpilot() {
        if (!readMarketingConsent()) {
            setWidgetActive(false);
            setTrustpilotFallbackVisible(true);
            disconnectNearViewportObserver();
            return;
        }
        scheduleTrustpilotLoad();
    }

    function onConsentUpdated(event) {
        var consent = event && event.detail;
        if (consent && consent.ad_storage === 'granted') {
            scheduleTrustpilotLoad();
        } else if (consent) {
            setWidgetActive(false);
            setTrustpilotFallbackVisible(true);
            disconnectNearViewportObserver();
        }
    }

    function init() {
        if (!getTrustpilotWidget()) return;
        initTrustpilot();
        window.addEventListener('aml-consent-updated', onConsentUpdated);
        window.addEventListener('storage', function (e) {
            if (e.key !== CONSENT_KEY) return;
            if (readMarketingConsent()) {
                scheduleTrustpilotLoad();
            } else {
                setWidgetActive(false);
                setTrustpilotFallbackVisible(true);
                disconnectNearViewportObserver();
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
