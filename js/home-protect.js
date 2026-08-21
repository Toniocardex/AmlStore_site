/**
 * Protection Selector multi-brand: solo tab brand (Kaspersky/Norton/ESET/
 * McAfee/Bitdefender) fuori dalle card. Il numero di dispositivi si sceglie
 * SOLO dentro ogni card: pill fissa per i piani a dispositivi fissi, oppure
 * il <select> del piano Kaspersky Premium (unico piano che varia SKU/prezzo
 * al cambio dispositivi). Nessun selettore dispositivi esterno.
 */
(function () {
    'use strict';

    function fmtEur(minor) {
        var n = Number(minor) / 100;
        return n.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }

    function init() {
        var root = document.querySelector('[data-home-protect]');
        if (!root) return;

        var brandTabs = root.querySelectorAll('[data-protect-brand]');
        var panels = root.querySelectorAll('[data-protect-brand-panel]');
        if (!brandTabs.length || !panels.length) return;

        function panelFor(brand) {
            for (var i = 0; i < panels.length; i++) {
                if (panels[i].getAttribute('data-protect-brand-panel') === brand) return panels[i];
            }
            return null;
        }

        function applyOffer(card, offer) {
            card.setAttribute('data-stripe-product-sku', offer.sku);
            card.setAttribute('data-stripe-unit-amount', String(offer.amount));
            card.setAttribute('data-stripe-compare-at-amount', String(offer.compare));
            card.setAttribute('data-discount-percent', String(offer.disc || 0));
            // Stessa convenzione slug -> products/<slug>.webp usata alla generazione
            // della pagina (vedi stripe_attrs in apply-security-first-phase2.py).
            if (offer.slug) card.setAttribute('data-cart-image', '../asset/media/products/' + offer.slug + '.webp');
            var price = card.querySelector('[data-plan-price]');
            if (price) price.textContent = fmtEur(offer.amount);
            var msrp = card.querySelector('[data-plan-msrp]');
            if (msrp) msrp.textContent = '\u20AC ' + fmtEur(offer.compare);
            var more = card.querySelector('[data-plan-more]');
            if (more && offer.slug) more.setAttribute('href', offer.slug);
        }

        function wireDevicesSelect(panel) {
            var select = panel.querySelector('[data-plan-devices-select]');
            if (!select) return;
            var source = panel.querySelector('[data-protect-matrix]');
            if (!source) return;
            var matrix;
            try {
                matrix = JSON.parse(source.textContent);
            } catch (err) {
                return;
            }
            if (!matrix || !matrix.devices) return;

            var premiumCard = select.closest('.plan-card') || panel.querySelector('[data-plan="premium"]');
            var plusCard = panel.querySelector('[data-plan="plus"]');
            if (!premiumCard) return;

            select.addEventListener('change', function () {
                var row = matrix.devices[select.value];
                if (!row) return;
                applyOffer(premiumCard, row.premium);
                if (plusCard) plusCard.classList.toggle('is-featured', row.featured === 'plus');
                premiumCard.classList.toggle('is-featured', row.featured === 'premium');
                var idealEl = premiumCard.querySelector('[data-plan-ideal-value]');
                if (idealEl && row.premium.ideal) idealEl.textContent = row.premium.ideal;
            });
        }

        panels.forEach(wireDevicesSelect);

        function showBrand(brand) {
            var target = panelFor(brand);
            if (!target) return;
            panels.forEach(function (panel) {
                panel.hidden = panel !== target;
            });
            brandTabs.forEach(function (tab) {
                var on = tab.getAttribute('data-protect-brand') === brand;
                tab.classList.toggle('is-selected', on);
                tab.setAttribute('aria-pressed', on ? 'true' : 'false');
            });
        }

        function syncUrl(brand) {
            var url = new URL(window.location.href);
            if (brand === 'kaspersky') url.searchParams.delete('brand');
            else url.searchParams.set('brand', brand);
            history.replaceState(null, '', url.pathname + url.search + url.hash);
        }

        brandTabs.forEach(function (tab) {
            tab.addEventListener('click', function () {
                var brand = tab.getAttribute('data-protect-brand');
                showBrand(brand);
                syncUrl(brand);
            });
        });

        var params = new URLSearchParams(window.location.search);
        var initialBrand = params.get('brand');
        showBrand(initialBrand && panelFor(initialBrand) ? initialBrand : 'kaspersky');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
