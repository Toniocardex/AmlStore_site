/**
 * PILOTA McAfee 1 dispositivo — micro-interazioni.
 * Attivo solo su body.pdp-hero--banner. Nessuna dipendenza.
 *  1. reveal-on-scroll di .mc-sec e .mc-close;
 *  2. count-up del prezzo (.pdp-price-sale) quando la buy card entra in view.
 * Degrada a "gia' visibile / valore finale" senza JS o con reduced-motion.
 */
(function () {
    'use strict';
    if (!document.body || !document.body.classList.contains('pdp-hero--banner')) return;

    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var hasIO = 'IntersectionObserver' in window;

    /* 1. reveal ---------------------------------------------------------- */
    var secs = document.querySelectorAll('.mc-sec, .mc-close');
    if (secs.length && hasIO && !reduce) {
        secs.forEach(function (el) { el.classList.add('mc-reveal'); });
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (e.isIntersecting) { e.target.classList.add('mc-in'); io.unobserve(e.target); }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
        secs.forEach(function (el) { io.observe(el); });
    }

    /* 2. count-up prezzo ---------------------------------------------------- */
    var buy = document.getElementById('product-pricing');
    var priceEl = buy && buy.querySelector('.pdp-price-sale');
    if (priceEl && hasIO && !reduce) {
        var raw = priceEl.textContent;                       // "€ 7,95"
        var mm = raw.match(/([\d.]+),(\d{2})/);
        if (mm) {
            var target = parseFloat(mm[1].replace(/\./g, '') + '.' + mm[2]);
            var prefix = raw.slice(0, raw.indexOf(mm[0]));
            var fmt = function (v) {
                return prefix + v.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            };
            var run = function () {
                var t0 = null, dur = 460;
                var step = function (ts) {
                    t0 = t0 || ts;
                    var p = Math.min(1, (ts - t0) / dur);
                    priceEl.textContent = fmt(target * (1 - Math.pow(1 - p, 3)));
                    if (p < 1) requestAnimationFrame(step); else priceEl.textContent = fmt(target);
                };
                requestAnimationFrame(step);
            };
            var pio = new IntersectionObserver(function (entries) {
                if (entries[0].isIntersecting) { run(); pio.disconnect(); }
            }, { threshold: 0.6 });
            pio.observe(buy);
        }
    }
})();
