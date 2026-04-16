/**
 * Due TrustBox nel markup (snippet light + dark); la visibilità è gestita in CSS (.trustpilot-host).
 * Dopo il bootstrap Trustpilot e al cambio tema ricarica i widget così anche quello prima nascosto viene renderizzato.
 */
(function () {
    'use strict';

    var HTML_THEME = 'data-theme';

    function widgets() {
        return document.querySelectorAll('.trustpilot-host .trustpilot-widget');
    }

    function reloadAll() {
        if (!window.Trustpilot || typeof window.Trustpilot.loadFromElement !== 'function') {
            return;
        }
        widgets().forEach(function (el) {
            try {
                window.Trustpilot.loadFromElement(el, true);
            } catch (_) {
                try {
                    window.Trustpilot.loadFromElement(el);
                } catch (_2) {}
            }
        });
    }

    function boot() {
        if (!widgets().length) {
            return;
        }
        function onWindowLoad() {
            reloadAll();
        }
        if (document.readyState === 'complete') {
            onWindowLoad();
        } else {
            window.addEventListener('load', onWindowLoad, { once: true });
        }
        try {
            new MutationObserver(reloadAll).observe(document.documentElement, {
                attributes: true,
                attributeFilter: [HTML_THEME],
            });
        } catch (_) {}
    }

    boot();
})();
