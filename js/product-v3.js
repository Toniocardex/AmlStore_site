/**
 * PRODUCT PAGE v3 — comportamenti della scheda prodotto
 * Quando la barra prodotto sticky è visibile (desktop/tablet) l'header principale si
 * ritira: header + barra + contenuto occupavano insieme ~150px di altezza utile.
 * La barra torna sotto l'header appena la CTA principale rientra in viewport.
 *
 * Su mobile (<=768px) la barra è ancorata in basso e l'header non viene toccato.
 */
(function () {
    'use strict';

    var DESKTOP_MEDIA_QUERY = '(min-width: 769px)';
    var HIDDEN_CLASS = 'pdp-nav-hidden';

    function isDesktop() {
        return window.matchMedia
            ? window.matchMedia(DESKTOP_MEDIA_QUERY).matches
            : window.innerWidth >= 769;
    }

    document.addEventListener('DOMContentLoaded', function () {
        var sticky = document.getElementById('product-sticky-cta');
        if (!sticky || !('MutationObserver' in window)) return;

        var root = document.documentElement;

        function sync() {
            var stickyVisible = sticky.classList.contains('product-sticky-cta--visible');
            root.classList.toggle(HIDDEN_CLASS, stickyVisible && isDesktop());
        }

        new MutationObserver(sync).observe(sticky, {
            attributes: true,
            attributeFilter: ['class'],
        });

        window.addEventListener('resize', sync, { passive: true });
        sync();
    });

    /**
     * Ponte verso il checkout dopo l'aggiunta al carrello.
     * Senza "Acquista ora" il percorso standard non ha piu' un invito
     * persistente a proseguire: resta solo il toast di cart.js, che sparisce
     * dopo 4 secondi e compare in fondo allo schermo mentre l'utente sta
     * guardando un bottone a meta' pagina. Il link nasce hidden nella buy
     * card e resta scoperto per tutta la sessione di lettura.
     * No-op sulle pagine che .pdp-added non ce l'hanno.
     */
    document.addEventListener('click', function (event) {
        if (!event.target || !event.target.closest) return;
        if (!event.target.closest('[data-cart-add]')) return;
        var bridge = document.querySelector('.pdp-added');
        if (bridge) bridge.hidden = false;
    });

    /**
     * Frecce di scroll della barra tab app: su desktop non c'e' lo swipe del
     * touch e la scrollbar resta nascosta (vedi product-pdp.css), quindi senza
     * questo non c'e' alcun indizio che Outlook/OneDrive/Copilot esistono
     * oltre il bordo. Le frecce restano invisibili finche' non c'e' davvero
     * altro da scorrere, e si disabilitano da sole a inizio/fine corsa.
     */
    document.addEventListener('DOMContentLoaded', function () {
        var wraps = document.querySelectorAll('.pdp-apptabs__wrap');
        if (!wraps.length) return;

        wraps.forEach(function (wrap) {
            var row = wrap.querySelector('.pdp-apptabs__row');
            var prev = wrap.querySelector('[data-apptabs-nav="-1"]');
            var next = wrap.querySelector('[data-apptabs-nav="1"]');
            if (!row || !prev || !next) return;

            function sync() {
                var max = row.scrollWidth - row.clientWidth;
                wrap.classList.toggle('pdp-apptabs__wrap--scrollable', max > 2);
                prev.disabled = row.scrollLeft <= 1;
                next.disabled = row.scrollLeft >= max - 1;
            }

            prev.addEventListener('click', function () {
                row.scrollBy({ left: -160, behavior: 'smooth' });
            });
            next.addEventListener('click', function () {
                row.scrollBy({ left: 160, behavior: 'smooth' });
            });
            row.addEventListener('scroll', sync, { passive: true });
            window.addEventListener('resize', sync, { passive: true });
            sync();
        });
    });
})();

