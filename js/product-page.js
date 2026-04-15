/**
 * Scheda prodotto: barra CTA sticky (IntersectionObserver), nessun dato inventato.
 */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        const sticky = document.getElementById('product-sticky-cta');
        const sentinel = document.getElementById('product-sticky-sentinel');
        if (!sticky || !sentinel) return;

        function applySticky(on) {
            sticky.toggleAttribute('hidden', !on);
            sticky.classList.toggle('product-sticky-cta--visible', on);
        }

        if (!('IntersectionObserver' in window)) return;

        var obs = new IntersectionObserver(
            function (entries) {
                var e = entries[0];
                applySticky(!e.isIntersecting);
            },
            { root: null, rootMargin: '-88px 0px 0px 0px', threshold: 0 }
        );
        obs.observe(sentinel);
    });
})();
