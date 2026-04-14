(function () {
    'use strict';
    var KEY = 'aml-theme';
    function systemTheme() {
        try {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                return 'dark';
            }
        } catch (_) {}
        return 'light';
    }
    try {
        var v = localStorage.getItem(KEY);
        if (v === 'light' || v === 'dark') {
            document.documentElement.setAttribute('data-theme', v);
            return;
        }
    } catch (_) {}
    document.documentElement.setAttribute('data-theme', systemTheme());
})();
