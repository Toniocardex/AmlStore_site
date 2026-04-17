(function () {
    'use strict';

    function initTabs() {
        var page = document.querySelector('.product-page');
        if (!page) return;
        var header = page.querySelector('.tabs-header');
        if (!header) return;
        var tabs = Array.from(header.querySelectorAll('.tab-btn'));
        var panels = Array.from(page.querySelectorAll('.tab-panel'));
        if (!tabs.length || !panels.length) return;

        /* Attiva il tab all'indice i, aggiorna ARIA e roving tabindex */
        function go(i) {
            i = Math.max(0, Math.min(tabs.length - 1, i));
            tabs.forEach(function (t, j) {
                var on = j === i;
                t.classList.toggle('active', on);
                t.setAttribute('aria-selected', on ? 'true' : 'false');
                /* Roving tabindex: solo il tab attivo è raggiungibile con Tab */
                t.setAttribute('tabindex', on ? '0' : '-1');
            });
            panels.forEach(function (p, j) {
                if (j === i) p.removeAttribute('hidden');
                else p.setAttribute('hidden', '');
            });
        }

        /* Stato iniziale: roving tabindex sul primo tab */
        tabs.forEach(function (t, i) {
            t.setAttribute('tabindex', i === 0 ? '0' : '-1');
        });

        tabs.forEach(function (tab, i) {
            /* Click: attiva e mantieni focus sul tab cliccato */
            tab.addEventListener('click', function () {
                go(i);
            });

            /* Tastiera: frecce ← →, Home, End (pattern ARIA tablist) */
            tab.addEventListener('keydown', function (e) {
                var key = e.key;
                var current = tabs.indexOf(document.activeElement);
                if (current < 0) current = i;

                if (key === 'ArrowRight') {
                    e.preventDefault();
                    var next = (current + 1) % tabs.length;
                    go(next);
                    tabs[next].focus();
                } else if (key === 'ArrowLeft') {
                    e.preventDefault();
                    var prev = (current - 1 + tabs.length) % tabs.length;
                    go(prev);
                    tabs[prev].focus();
                } else if (key === 'Home') {
                    e.preventDefault();
                    go(0);
                    tabs[0].focus();
                } else if (key === 'End') {
                    e.preventDefault();
                    go(tabs.length - 1);
                    tabs[tabs.length - 1].focus();
                }
            });
        });
    }

    /* Guard: funziona sia con defer (DOM già pronto) sia senza */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTabs);
    } else {
        initTabs();
    }
})();
