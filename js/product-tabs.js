(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        const page = document.querySelector('.product-page');
        if (!page) return;
        const header = page.querySelector('.tabs-header');
        if (!header) return;
        const tabs = header.querySelectorAll('.tab-btn');
        const panels = page.querySelectorAll('.tab-panel');
        if (!tabs.length || !panels.length) return;

        function go(index) {
            const i = Math.max(0, Math.min(tabs.length - 1, index));
            tabs.forEach(function (t, j) {
                const on = j === i;
                t.classList.toggle('active', on);
                t.setAttribute('aria-selected', on ? 'true' : 'false');
            });
            panels.forEach(function (p, j) {
                if (j === i) p.removeAttribute('hidden');
                else p.setAttribute('hidden', '');
            });
        }

        tabs.forEach(function (tab, i) {
            tab.addEventListener('click', function () {
                go(i);
            });
        });
    });
})();
