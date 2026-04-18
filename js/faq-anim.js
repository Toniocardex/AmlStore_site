/**
 * faq-anim.js — Animazione height smooth su <details> con classe body specificata.
 *
 * Uso: initFaqAnim('.my-faq-body')
 * Funziona su qualsiasi <details> che contenga un div con quella classe.
 * Rispetta prefers-reduced-motion: se attivo, salta l'animazione.
 * Compatibile con home.js (usa selettori diversi, non interferisce).
 */
(function () {
    'use strict';

    function initFaqAnim(bodySelector) {
        if (!bodySelector) return;
        var reducedMotion =
            typeof window.matchMedia === 'function' &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        var bodies = document.querySelectorAll(bodySelector);
        bodies.forEach(function (body) {
            var details = body.closest('details');
            if (!details) return;
            var summary = details.querySelector('summary');
            if (!summary) return;

            summary.addEventListener('click', function (e) {
                e.preventDefault();

                if (reducedMotion) {
                    details.toggleAttribute('open');
                    return;
                }

                if (details.open) {
                    /* Chiusura: height → 0 */
                    body.style.height = body.scrollHeight + 'px';
                    body.style.overflow = 'hidden';
                    requestAnimationFrame(function () {
                        body.style.transition = 'height 0.25s cubic-bezier(0.4, 0, 0.2, 1)';
                        body.style.height = '0px';
                        body.addEventListener('transitionend', function onEnd() {
                            body.removeEventListener('transitionend', onEnd);
                            details.removeAttribute('open');
                            body.style.cssText = '';
                        }, { once: true });
                    });
                } else {
                    /* Apertura: height 0 → scrollHeight */
                    details.setAttribute('open', '');
                    var targetH = body.scrollHeight;
                    body.style.height = '0px';
                    body.style.overflow = 'hidden';
                    requestAnimationFrame(function () {
                        body.style.transition = 'height 0.25s cubic-bezier(0.4, 0, 0.2, 1)';
                        body.style.height = targetH + 'px';
                        body.addEventListener('transitionend', function onEnd() {
                            body.removeEventListener('transitionend', onEnd);
                            body.style.cssText = '';
                        }, { once: true });
                    });
                }
            });
        });
    }

    /* Espone la funzione per uso da altri script */
    window.AmlFaqAnim = { init: initFaqAnim };

    /* Auto-init per la pagina prodotto */
    function autoInit() {
        initFaqAnim('.product-faq-body');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', autoInit);
    } else {
        autoInit();
    }
})();
