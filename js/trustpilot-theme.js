/**
 * TrustBox (carrello + schede prodotto): iframe cross-origin.
 * Sincronizza data-token + data-theme con html[data-theme] e ricarica al cambio tema.
 */
(function () {
    'use strict';

    var HTML_THEME = 'data-theme';
    /** Token embed “Micro Review Count” tema chiaro (senza data-theme sul div). */
    var TP_LIGHT_TOKEN = 'c92325c4-322c-4b67-b5ff-129c9cf65c90';
    /** Token embed tema scuro (data-theme="dark"). */
    var TP_DARK_TOKEN = '18617ae8-b57b-4ae2-91e2-f1fa72dd73cf';

    function isSiteDark() {
        return document.documentElement.getAttribute(HTML_THEME) === 'dark';
    }

    function trustpilotNodes() {
        return document.querySelectorAll('.trustpilot-widget');
    }

    /** @returns {boolean} true se c’è almeno un widget da gestire */
    function applyWidgetTrustboxAttrs() {
        var nodes = trustpilotNodes();
        var n = nodes.length;
        var dark = isSiteDark();
        for (var i = 0; i < n; i++) {
            var el = nodes[i];
            el.setAttribute('data-token', dark ? TP_DARK_TOKEN : TP_LIGHT_TOKEN);
            if (dark) {
                el.setAttribute('data-theme', 'dark');
            } else {
                el.removeAttribute('data-theme');
            }
        }
        return n > 0;
    }

    function reloadTrustpilotWidgets() {
        if (!window.Trustpilot || typeof window.Trustpilot.loadFromElement !== 'function') {
            return;
        }
        trustpilotNodes().forEach(function (el) {
            try {
                window.Trustpilot.loadFromElement(el);
            } catch (_) {}
        });
    }

    function boot() {
        if (!applyWidgetTrustboxAttrs()) {
            return;
        }
        try {
            var obs = new MutationObserver(function () {
                applyWidgetTrustboxAttrs();
                reloadTrustpilotWidgets();
            });
            obs.observe(document.documentElement, { attributes: true, attributeFilter: [HTML_THEME] });
        } catch (_) {}
    }

    boot();
})();
