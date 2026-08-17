/**
 * pdp-activation-modal.js — modale "come si attiva" della scheda prodotto.
 *
 * File esterno e non inline: la CSP in _headers oggi ammette 'unsafe-inline'
 * su script-src, ma tenerlo fuori dall'HTML e' comunque preferibile — si
 * scrive una volta sola invece che in ogni pagina generata, ed e' l'unico
 * modo perche' resti valido se un domani quella direttiva viene stretta.
 *
 * Usa <dialog> nativo con showModal(): focus trap, chiusura con Esc, inerzia
 * del resto della pagina e ::backdrop li mette il browser, senza doverli
 * reimplementare. Se il tag non e' supportato il bottone resta un link alla
 * sezione "come funziona" gia' presente in pagina, quindi il contenuto e'
 * comunque raggiungibile.
 */
(function () {
    'use strict';

    function init() {
        var dialog = document.getElementById('pdp-activation');
        var trigger = document.querySelector('[data-pdp-guide]');
        if (!dialog || !trigger) return;

        // Senza <dialog> il bottone non viene attivato: resta l'href di fallback.
        if (typeof dialog.showModal !== 'function') return;

        trigger.addEventListener('click', function (e) {
            e.preventDefault();
            dialog.showModal();
        });

        dialog.querySelectorAll('[data-pdp-guide-close]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                dialog.close();
            });
        });

        // Click sul backdrop: l'evento arriva al dialog stesso, non ai figli,
        // quindi il target coincide col dialog solo se si e' cliccato fuori.
        dialog.addEventListener('click', function (e) {
            if (e.target === dialog) dialog.close();
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
