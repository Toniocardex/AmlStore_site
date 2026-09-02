/**
 * PILOTA McAfee — micro-interazioni della sola scheda pilota.
 * Attivo solo su body.pdp-hero--banner. Nessuna dipendenza.
 *  1. reveal-on-scroll delle sezioni corpo + fascia di chiusura;
 *  2. count-up del prezzo quando la buy card entra in viewport.
 * Tutto degrada a "gia' visibile / valore finale" senza JS o con
 * prefers-reduced-motion.
 */
(function () {
    'use strict';
    if (!document.body || !document.body.classList.contains('pdp-hero--banner')) return;

    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* 1. Reveal-on-scroll -------------------------------------------------- */
    var targets = document.querySelectorAll('.pdp-sec, .pdp-mc-close');
    if (targets.length && 'IntersectionObserver' in window && !reduce) {
        targets.forEach(function (el) { el.classList.add('mc-reveal'); });
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (e.isIntersecting) {
                    e.target.classList.add('mc-in');
                    io.unobserve(e.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
        targets.forEach(function (el) { io.observe(el); });
    }

    /* 2. Count-up del prezzo ------------------------------------------------ */
    var priceEl = document.querySelector('#product-pricing .pdp-price-sale');
    var buy = document.getElementById('product-pricing');
    if (priceEl && buy && !reduce && 'IntersectionObserver' in window) {
        var raw = priceEl.textContent;                       // es. "€ 7,95"
        var m = raw.match(/([\d.]+),(\d{2})/);
        if (m) {
            var target = parseFloat(m[1].replace(/\./g, '') + '.' + m[2]);
            var prefix = raw.slice(0, raw.indexOf(m[0]));    // "€ "
            var fmt = function (v) {
                return prefix + v.toLocaleString('it-IT', {
                    minimumFractionDigits: 2, maximumFractionDigits: 2
                });
            };
            var run = function () {
                var start = null, dur = 460, from = 0;
                var step = function (ts) {
                    start = start || ts;
                    var p = Math.min(1, (ts - start) / dur);
                    var eased = 1 - Math.pow(1 - p, 3);
                    priceEl.textContent = fmt(from + (target - from) * eased);
                    if (p < 1) requestAnimationFrame(step);
                    else priceEl.textContent = fmt(target);
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
