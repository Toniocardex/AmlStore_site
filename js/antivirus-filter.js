/**
 * Filtri catalogo antivirus: brand (Kaspersky/Norton/ESET/McAfee/Bitdefender)
 * e dispositivi (1/3/5/10), combinati in AND. Legge ?brand=&devices= o
 * #devices-N e i chip data-av-brand/data-av-filter.
 */
(function () {
    'use strict';

    function init() {
        var devRoot = document.querySelector('[data-av-filters]');
        var brandRoot = document.querySelector('[data-av-brand-filters]');
        var cards = document.querySelectorAll('.product-grid .product-card[data-devices]');
        if ((!devRoot && !brandRoot) || !cards.length) return;

        var devChips = devRoot ? devRoot.querySelectorAll('[data-av-filter]') : [];
        var brandChips = brandRoot ? brandRoot.querySelectorAll('[data-av-brand]') : [];

        function currentDeviceFromUrl() {
            var params = new URLSearchParams(window.location.search);
            var q = params.get('devices');
            if (q && /^(1|3|5|10)$/.test(q)) return q;
            var hash = (window.location.hash || '').replace(/^#devices-?/, '');
            if (hash && /^(1|3|5|10)$/.test(hash)) return hash;
            return 'all';
        }

        function currentBrandFromUrl() {
            var params = new URLSearchParams(window.location.search);
            var b = params.get('brand');
            if (b && /^[a-z]+$/.test(b)) return b;
            return 'all';
        }

        function apply(deviceValue, brandValue) {
            devChips.forEach(function (chip) {
                var on = chip.getAttribute('data-av-filter') === deviceValue;
                chip.classList.toggle('is-selected', on);
                chip.setAttribute('aria-pressed', on ? 'true' : 'false');
            });
            brandChips.forEach(function (chip) {
                var on = chip.getAttribute('data-av-brand') === brandValue;
                chip.classList.toggle('is-selected', on);
                chip.setAttribute('aria-pressed', on ? 'true' : 'false');
            });
            cards.forEach(function (card) {
                var devices = card.getAttribute('data-devices') || '';
                var brand = card.getAttribute('data-brand') || '';
                var deviceOk = deviceValue === 'all' || devices.split(/\s+/).indexOf(deviceValue) !== -1;
                var brandOk = brandValue === 'all' || brand === brandValue;
                card.hidden = !(deviceOk && brandOk);
            });
        }

        function syncUrl(deviceValue, brandValue) {
            var url = new URL(window.location.href);
            if (deviceValue === 'all') url.searchParams.delete('devices');
            else url.searchParams.set('devices', deviceValue);
            if (brandValue === 'all') url.searchParams.delete('brand');
            else url.searchParams.set('brand', brandValue);
            url.hash = '';
            history.replaceState(null, '', url.pathname + url.search);
        }

        var state = { device: currentDeviceFromUrl(), brand: currentBrandFromUrl() };

        devChips.forEach(function (chip) {
            chip.addEventListener('click', function () {
                state.device = chip.getAttribute('data-av-filter') || 'all';
                apply(state.device, state.brand);
                syncUrl(state.device, state.brand);
            });
        });

        brandChips.forEach(function (chip) {
            chip.addEventListener('click', function () {
                state.brand = chip.getAttribute('data-av-brand') || 'all';
                apply(state.device, state.brand);
                syncUrl(state.device, state.brand);
            });
        });

        apply(state.device, state.brand);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
