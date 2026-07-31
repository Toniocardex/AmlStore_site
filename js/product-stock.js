/**
 * Badge magazzino su schede fisiche (data-physical="true").
 * Fetch GET /api/stock?sku= — non tocca LCP; defer only.
 */
(function () {
    'use strict';

    var LOW_MAX = 10;

    function pricingRoot() {
        return document.querySelector('[data-physical="true"][data-stripe-product-sku], #product-pricing[data-physical="true"]');
    }

    function stockEl(root) {
        return root ? root.querySelector('.v2-stock') : document.querySelector('.v2-stock');
    }

    function tpl(el, key, n) {
        var raw = el.getAttribute('data-stock-' + key) || '';
        return raw.replace(/\{n\}/g, String(n));
    }

    function setStatus(el, status, text) {
        el.setAttribute('data-stock-status', status);
        var t = el.querySelector('.v2-stock__text');
        if (t) t.textContent = text || '';
    }

    function setCtasDisabled(disabled) {
        var buttons = document.querySelectorAll('[data-cart-add]');
        for (var i = 0; i < buttons.length; i++) {
            var btn = buttons[i];
            if (disabled) {
                btn.setAttribute('disabled', '');
                btn.setAttribute('aria-disabled', 'true');
                btn.setAttribute('tabindex', '-1');
                btn.classList.add('is-stock-out');
            } else {
                btn.removeAttribute('disabled');
                btn.removeAttribute('aria-disabled');
                btn.removeAttribute('tabindex');
                btn.classList.remove('is-stock-out');
            }
        }
    }

    function updateJsonLd(inStock) {
        var scripts = document.querySelectorAll('script[type="application/ld+json"]');
        var avail = inStock
            ? 'https://schema.org/InStock'
            : 'https://schema.org/OutOfStock';
        for (var i = 0; i < scripts.length; i++) {
            var node = scripts[i];
            var raw = node.textContent;
            if (!raw || raw.indexOf('"Offer"') === -1 && raw.indexOf('Offer') === -1) continue;
            try {
                var data = JSON.parse(raw);
                var changed = false;
                function walk(obj) {
                    if (!obj || typeof obj !== 'object') return;
                    if (Array.isArray(obj)) {
                        obj.forEach(walk);
                        return;
                    }
                    var type = obj['@type'];
                    var isOffer = type === 'Offer' || (Array.isArray(type) && type.indexOf('Offer') !== -1);
                    if (isOffer && Object.prototype.hasOwnProperty.call(obj, 'availability')) {
                        obj.availability = avail;
                        changed = true;
                    }
                    if (obj.offers) walk(obj.offers);
                    if (obj['@graph']) walk(obj['@graph']);
                }
                walk(data);
                if (changed) node.textContent = JSON.stringify(data);
            } catch (_) { /* ignore malformed */ }
        }
    }

    function applyQty(el, qty) {
        var q = Math.max(0, Math.floor(Number(qty) || 0));
        if (q <= 0) {
            setStatus(el, 'out', tpl(el, 'out', 0));
            setCtasDisabled(true);
            updateJsonLd(false);
            return;
        }
        setCtasDisabled(false);
        updateJsonLd(true);
        if (q <= LOW_MAX) {
            setStatus(el, 'low', tpl(el, 'low', q));
        } else {
            setStatus(el, 'ok', tpl(el, 'available', q));
        }
    }

    function run() {
        var root = pricingRoot();
        if (!root) return;
        var el = stockEl(root);
        if (!el) return;
        var sku = String(
            root.getAttribute('data-stripe-product-sku') ||
            (root.dataset && root.dataset.stripeProductSku) ||
            ''
        ).trim();
        if (!sku) {
            setStatus(el, 'error', tpl(el, 'error', 0));
            return;
        }

        fetch('/api/stock?sku=' + encodeURIComponent(sku), {
            credentials: 'same-origin',
            headers: { Accept: 'application/json' },
        })
            .then(function (res) {
                if (!res.ok) throw new Error('stock ' + res.status);
                return res.json();
            })
            .then(function (data) {
                applyQty(el, data && data.qty);
            })
            .catch(function () {
                setStatus(el, 'error', tpl(el, 'error', 0));
                /* CTA resta attiva: non bloccare vendita su fallimento rete */
            });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', run);
    } else {
        run();
    }
})();
