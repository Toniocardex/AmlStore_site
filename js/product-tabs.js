(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var page = document.querySelector('.product-page');
        if (!page) return;
        var header = page.querySelector('.tabs-header');
        if (!header) return;
        var tabs = header.querySelectorAll('.tab-btn');
        var panels = page.querySelectorAll('.tab-panel');
        if (!tabs.length || !panels.length) return;

        function go(index) {
            var i = Math.max(0, Math.min(tabs.length - 1, index));
            tabs.forEach(function (t, j) {
                var on = j === i;
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
