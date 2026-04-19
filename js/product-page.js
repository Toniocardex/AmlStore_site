/**
 * Scheda prodotto: barra CTA sticky solo quando la CTA principale (#product-primary-cta)
 * non è più visibile nell’area utile sotto l’header (altezza misurata, non fissa).
 */
(function () {
    'use strict';

    var HEADER_MIN = 56;
    var HEADER_MAX = 120;
    var RESIZE_DEBOUNCE_MS = 100;
    var obs = null;
    var resizeTimer = null;
    var lastInset = -1;

    function readSafeAreaTop() {
        try {
            var probe = document.createElement('div');
            probe.style.cssText =
                'position:fixed;top:0;left:0;padding-top:env(safe-area-inset-top,0px);visibility:hidden;pointer-events:none';
            document.documentElement.appendChild(probe);
            var pt = parseFloat(getComputedStyle(probe).paddingTop) || 0;
            document.documentElement.removeChild(probe);
            return pt;
        } catch (_) {
            return 0;
        }
    }

    function headerElement() {
        return document.querySelector('ecommerce-header');
    }

    function headerInsetPx() {
        var el = headerElement();
        var h = 88;
        if (el) {
            var rect = el.getBoundingClientRect();
            h = Math.round(rect.height || el.offsetHeight || 88);
        }
        h = Math.min(HEADER_MAX, Math.max(HEADER_MIN, h));
        return Math.round(h + readSafeAreaTop());
    }

    function syncHeaderCssVar() {
        var px = headerInsetPx();
        document.documentElement.style.setProperty('--aml-header-offset', px + 'px');
    }

    function applySticky(sticky, on) {
        sticky.classList.toggle('product-sticky-cta--visible', on);
        sticky.setAttribute('aria-hidden', on ? 'false' : 'true');
        sticky.inert = !on;
    }

    /** Doppio rAF: layout stabile (fonte/header) prima del primo IntersectionObserver. */
    function afterLayoutStable(fn) {
        requestAnimationFrame(function () {
            requestAnimationFrame(fn);
        });
    }

    function connectObserver(sticky, primaryCta) {
        if (!('IntersectionObserver' in window)) return;

        syncHeaderCssVar();
        var inset = headerInsetPx();

        // Skip rebuild if header height hasn't changed — avoids unnecessary disconnect/reconnect
        if (obs && inset === lastInset) return;
        lastInset = inset;

        if (obs) { obs.disconnect(); obs = null; }

        var topMargin = '-' + inset + 'px';

        obs = new IntersectionObserver(
            function (entries) {
                var e = entries[0];
                if (!e) return;
                var primaryVisible = e.isIntersecting === true;
                applySticky(sticky, !primaryVisible);
            },
            {
                root: null,
                rootMargin: topMargin + ' 0px 0px 0px',
                threshold: 0,
            }
        );
        obs.observe(primaryCta);
    }

    document.addEventListener('DOMContentLoaded', function () {
        var sticky = document.getElementById('product-sticky-cta');
        var primaryCta = document.getElementById('product-primary-cta');
        if (!sticky || !primaryCta) return;

        applySticky(sticky, false);
        syncHeaderCssVar();
        afterLayoutStable(function () {
            connectObserver(sticky, primaryCta);
        });

        function scheduleRebuild() {
            if (resizeTimer) clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function () {
                resizeTimer = null;
                connectObserver(sticky, primaryCta);
            }, RESIZE_DEBOUNCE_MS);
        }

        window.addEventListener('resize', scheduleRebuild, { passive: true });
        window.addEventListener('orientationchange', scheduleRebuild, { passive: true });

        var headerEl = headerElement();
        if (headerEl && 'ResizeObserver' in window) {
            new ResizeObserver(scheduleRebuild).observe(headerEl);
        }
    });
})();
