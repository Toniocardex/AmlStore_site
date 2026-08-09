/**
 * not-found.js — collega il bottone "cerca" della 404 alla ricerca dell'header.
 *
 * La ricerca vera vive gia' nell'header (components/header.js, indice in
 * asset/search-index/{lang}.json): qui non se ne duplica una seconda, si apre
 * quella. Se per qualsiasi motivo l'header non fosse disponibile, il bottone
 * viene nascosto e restano gli altri percorsi della pagina (categorie,
 * prodotti, home), invece di lasciare un comando che non fa nulla.
 */
(function () {
    'use strict';

    var HEADER_SEARCH_TOGGLE = '.search-toggle';

    function findHeaderSearchToggle() {
        return document.querySelector(HEADER_SEARCH_TOGGLE);
    }

    function init() {
        var button = document.querySelector('[data-nf-search]');
        if (!button) return;

        var toggle = findHeaderSearchToggle();
        if (!toggle) {
            button.hidden = true;
            return;
        }

        button.addEventListener('click', function () {
            // Ricontrollato al click: l'header aggancia il comportamento con
            // `defer`, quindi puo' essere pronto dopo questo script.
            var current = findHeaderSearchToggle();
            if (current) current.click();
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
