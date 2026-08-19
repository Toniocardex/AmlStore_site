/**
 * home-guide.js — "Guida all'acquisto" della home: due domande a cascata.
 *
 * Step 1 sceglie la categoria (Office, Windows, Antivirus, Business), step 2
 * mostra solo le opzioni di quella categoria e produce il consiglio finale.
 *
 * File esterno e non inline per coerenza col resto del sito (vedi
 * pdp-activation-modal.js): la copia dello script sta in un posto solo invece
 * che dentro cinque index.html.
 *
 * Il contenuto delle raccomandazioni non e' nel JS ma negli attributi data-
 * dei bottoni, cosi' resta tradotto insieme al markup e non serve un
 * dizionario per lingua qui dentro. Senza JS resta visibile il primo gruppo
 * di step 2 con il consiglio di partenza, che e' gia' un link valido a una
 * scheda prodotto.
 */
(function () {
    'use strict';

    function init() {
        var root = document.querySelector('[data-home-guide]');
        if (!root) return;

        var categories = root.querySelectorAll('[data-guide-category]');
        var groups = root.querySelectorAll('[data-guide-group]');
        var title = root.querySelector('[data-guide-title]');
        var body = root.querySelector('[data-guide-body]');
        var link = root.querySelector('[data-guide-link]');
        var image = root.querySelector('[data-guide-image]');
        if (!categories.length || !groups.length || !title || !body || !link) return;

        function showResult(btn) {
            var group = btn.closest('[data-guide-group]');
            if (group) {
                group.querySelectorAll('[data-guide-option]').forEach(function (b) {
                    var on = b === btn;
                    b.classList.toggle('is-selected', on);
                    b.setAttribute('aria-pressed', on ? 'true' : 'false');
                });
            }
            title.textContent = btn.getAttribute('data-guide-title-value') || title.textContent;
            body.textContent = btn.getAttribute('data-guide-body-value') || body.textContent;
            var href = btn.getAttribute('data-guide-href');
            if (href) {
                link.setAttribute('href', href);
                /* Il nome file immagine coincide sempre con lo slug prodotto
                   (data-guide-href), come per le card di tutto il sito: non
                   serve un attributo dati separato solo per l'immagine. */
                if (image) image.src = '../asset/media/products/' + href + '.webp';
            }
        }

        function selectCategory(btn) {
            var key = btn.getAttribute('data-guide-category');

            categories.forEach(function (b) {
                var on = b === btn;
                b.classList.toggle('is-selected', on);
                b.setAttribute('aria-pressed', on ? 'true' : 'false');
            });

            groups.forEach(function (group) {
                var on = group.getAttribute('data-guide-group') === key;
                group.hidden = !on;
                /* Cambiando categoria il consiglio mostrato apparterrebbe ancora
                   a quella precedente: si riparte dalla prima opzione del nuovo
                   gruppo, cosi' il pannello resta coerente con la scelta. */
                if (on) {
                    var first = group.querySelector('[data-guide-option]');
                    if (first) showResult(first);
                }
            });
        }

        categories.forEach(function (btn) {
            btn.addEventListener('click', function () {
                selectCategory(btn);
            });
        });

        root.querySelectorAll('[data-guide-option]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                showResult(btn);
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
