(function () {
    'use strict';
    var KEY = 'aml-theme';
    try {
        var v = localStorage.getItem(KEY);
        if (v === 'light' || v === 'dark') {
            document.documentElement.setAttribute('data-theme', v);
            return;
        }
    } catch (_) {}
    document.documentElement.setAttribute('data-theme', 'light');
})();
