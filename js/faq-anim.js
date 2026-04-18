/**
 * faq-anim.js — FAQ smooth via grid-template-rows (no layout reflow).
 *
 * L'apertura è gestita interamente da CSS (details[open] → grid-template-rows: 1fr).
 * Il JS intercetta solo la chiusura per prevenire che il browser rimuova [open]
 * prima che la transizione CSS finisca.
 * Rispetta prefers-reduced-motion.
 */
(function () {
    'use strict';

    var reducedMotion =
        typeof window.matchMedia === 'function' &&
        window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function init() {
        document.querySelectorAll('.product-faq details').forEach(function (details) {
            var summary = details.querySelector('summary');
            if (!summary) return;

            summary.addEventListener('click', function (e) {
                if (!details.open) return; // apertura: lascia fare al browser, CSS anima

                e.preventDefault();

                if (reducedMotion) {
                    details.removeAttribute('open');
                    return;
                }

                var body = details.querySelector('.product-faq-body');
                if (!body) { details.removeAttribute('open'); return; }

                body.style.gridTemplateRows = '0fr';
                body.addEventListener('transitionend', function onEnd() {
                    body.removeEventListener('transitionend', onEnd);
                    details.removeAttribute('open');
                    body.style.gridTemplateRows = '';
                }, { once: true });
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
