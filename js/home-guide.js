/**
 * home-guide.js — "Guida all'acquisto" della home: tre opzioni, un consiglio.
 *
 * File esterno e non inline per coerenza col resto del sito (vedi
 * pdp-activation-modal.js): la copia dello script sta in un posto solo invece
 * che dentro cinque index.html.
 *
 * Il contenuto delle raccomandazioni non e' nel JS ma negli attributi data-
 * dei bottoni, cosi' resta tradotto insieme al markup e non serve un
 * dizionario per lingua qui dentro. Senza JS restano visibili la domanda e il
 * consiglio di partenza, che e' gia' un link valido a una scheda prodotto.
 */
(function () {
    'use strict';

    function init() {
        var root = document.querySelector('[data-home-guide]');
        if (!root) return;

        var options = root.querySelectorAll('[data-guide-option]');
        var title = root.querySelector('[data-guide-title]');
        var body = root.querySelector('[data-guide-body]');
        var link = root.querySelector('[data-guide-link]');
        if (!options.length || !title || !body || !link) return;

        function select(btn) {
            options.forEach(function (b) {
                var on = b === btn;
                b.classList.toggle('is-selected', on);
                b.setAttribute('aria-pressed', on ? 'true' : 'false');
            });
            title.textContent = btn.getAttribute('data-guide-title-value') || title.textContent;
            body.textContent = btn.getAttribute('data-guide-body-value') || body.textContent;
            var href = btn.getAttribute('data-guide-href');
            if (href) link.setAttribute('href', href);
        }

        options.forEach(function (btn) {
            btn.addEventListener('click', function () {
                select(btn);
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
