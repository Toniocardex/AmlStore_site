/**
 * Trustpilot TrustBox — carica sempre (non e' un tracker: mostra solo il
 * voto pubblico, nessun cookie/consenso di marketing coinvolto), solo
 * quando il widget e' vicino al viewport. Condiviso da home + carrello.
 */
(function () {
    'use strict';

    var TRUSTPILOT_SCRIPT_ID = 'trustpilot-widget-script';
    var TRUSTPILOT_SCRIPT_SRC = 'https://widget.trustpilot.com/bootstrap/v5/tp.widget.bootstrap.min.js';
    var LOAD_ROOT_MARGIN = '200px 0px';

    var _nearViewportObserver = null;
    var _loadStarted = false;

    function getTrustpilotWidget() {
        return document.getElementById('trustpilot-widget') || document.querySelector('.trustpilot-widget');
    }

    function setWidgetActive(active) {
        var widget = getTrustpilotWidget();
        if (widget) widget.classList.toggle('trustpilot-widget--active', active);
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
            return true;
        } catch (_) {
            setWidgetActive(false);
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
            script.remove();
        };
        document.head.appendChild(script);
    }

    /** Carica quando il widget e' vicino al viewport (o subito se non c'e' IO). */
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

    function init() {
        if (!getTrustpilotWidget()) return;
        scheduleTrustpilotLoad();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
