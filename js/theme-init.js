(function () {
  'use strict';
  try {
    var t = localStorage.getItem('aml-theme');
    if (t === 'light' || t === 'dark') {
      document.documentElement.setAttribute('data-theme', t);
    }
  } catch (e) {}
})();
