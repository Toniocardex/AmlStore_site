/**
 * Barra di avanzamento scroll in cima (stessa logica di home.js, markup: .scroll-progress).
 */
(function () {
    'use strict';

    function initScrollProgress() {
        var bar = document.querySelector('.scroll-progress');
        if (!bar) return;

        var pending = false;
        function update() {
            var scrolled = window.scrollY;
            var total = document.documentElement.scrollHeight - window.innerHeight;
            bar.style.transform = 'scaleX(' + (total > 0 ? scrolled / total : 0) + ')';
            pending = false;
        }

        window.addEventListener('scroll', function () {
            if (!pending) {
                pending = true;
                requestAnimationFrame(update);
            }
        }, { passive: true });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initScrollProgress);
    } else {
        initScrollProgress();
    }
}());
