/**
 * admin-analytics.js — vista "Analytics" del pannello admin (vanilla JS).
 *
 * Modulo indipendente da admin.js: nessun import del suo stato interno, solo
 * un piccolo set di helper propri. admin.js lo richiama via
 * window.adminAnalytics.load() quando l'utente apre il tab, e resta in ascolto
 * dell'evento `aml-analytics-ready` per il caso in cui apra la vista prima che
 * questo file sia stato eseguito (entrambi gli script sono `defer`).
 */

(function () {
    'use strict';

    var state = {
        days:    '30',
        loading: false,
    };

    /* ─── Utility DOM (copia minima, stesso stile di admin.js) ───────────────── */

    function $  (id) { return document.getElementById(id); }

    /* Attenzione a `s || ''`: con un valore 0 restituirebbe stringa vuota, e i
       numeri a zero sparirebbero dalla pagina invece di essere mostrati. */
    function esc(s) {
        return (s === null || s === undefined ? '' : String(s))
            .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    }

    function show(id) { var el = $(id); if (el) el.hidden = false; }
    function hide(id) { var el = $(id); if (el) el.hidden = true; }
    function text(id, val) { var el = $(id); if (el) el.textContent = val; }

    function apiGet(path) {
        return fetch(path, { credentials: 'same-origin' }).then(function (res) {
            if (res.status === 401) throw new Error('401');
            if (!res.ok) throw new Error('HTTP ' + res.status);
            return res.json();
        });
    }

    /* ─── Formattazione ────────────────────────────────────────────────────── */

    function fmtNum(n) {
        try { return new Intl.NumberFormat('it-IT').format(Number(n) || 0); }
        catch (_) { return String(Number(n) || 0); }
    }

    /** Percentuale sul totale, senza decimali inutili sotto l'1%. */
    function fmtPct(part, total) {
        if (!total) return '—';
        var p = (Number(part) || 0) / total * 100;
        return (p < 1 && p > 0 ? p.toFixed(1) : Math.round(p)) + '%';
    }

    /** '2026-08-10' → '10 ago' */
    var MONTHS = ['gen','feb','mar','apr','mag','giu','lug','ago','set','ott','nov','dic'];
    function fmtDay(iso) {
        var p = String(iso || '').split('-');
        if (p.length !== 3) return iso;
        return Number(p[2]) + ' ' + (MONTHS[Number(p[1]) - 1] || '');
    }

    function statRow(label, value) {
        return '<div class="adm-stat-row"><span>' + esc(label) + '</span>'
             + '<strong>' + esc(value) + '</strong></div>';
    }

    /**
     * Tetto "tondo" per la scala del grafico (10, 25, 50, 100, 250…): un asse
     * che finisce sul valore grezzo del picco produce etichette come 137,
     * illeggibili a colpo d'occhio.
     */
    function niceCeil(max) {
        if (max <= 5) return 5;
        var mag  = Math.pow(10, Math.floor(Math.log10(max)));
        var step = [1, 2, 2.5, 5, 10].find(function (s) { return max <= s * mag; }) || 10;
        return Math.ceil(max / (step * mag / 10)) * (step * mag / 10);
    }

    /* ─── Caricamento ──────────────────────────────────────────────────────── */

    function load() {
        if (state.loading) return;
        state.loading = true;

        show('adm-analytics-loading');
        hide('adm-analytics-error');
        hide('adm-analytics-content');

        apiGet('/api/admin/analytics?days=' + encodeURIComponent(state.days)).then(function (data) {
            state.loading = false;
            hide('adm-analytics-loading');
            show('adm-analytics-content');
            render(data);
        }).catch(function (e) {
            state.loading = false;
            hide('adm-analytics-loading');
            if (e.message !== '401') {
                show('adm-analytics-error');
                text('adm-analytics-error-msg', 'Errore caricamento analytics: ' + e.message);
            }
        });
    }

    /* ─── Render ───────────────────────────────────────────────────────────── */

    function render(data) {
        var daily = data.daily || [];
        renderStats(data, daily);
        renderChart(daily);

        var views = data.views || 0;
        renderTopList('adm-analytics-pages-tbody',     data.topPages     || [], 'path',    views, 'Pagina');
        renderTopList('adm-analytics-countries-tbody', data.topCountries || [], 'country', views, 'Paese');
        renderTopList('adm-analytics-lang-suggest-tbody', data.topSuggestedLangs || [], 'suggested_lang', views, 'Lingua');
        renderTopList('adm-analytics-devices-tbody',   data.devices      || [], 'device',  views, 'Tipo');
        renderReferrers(data, views);
    }

    function renderStats(data, daily) {
        var el = $('adm-analytics-stats');
        if (!el) return;

        var views    = data.views || 0;
        var visitors = data.visitors || 0;
        var nDays    = daily.length || Number(data.days) || 1;

        var peak = daily.reduce(function (best, d) {
            return (!best || d.views > best.views) ? d : best;
        }, null);

        var html = '<p class="adm-filter-section__title">Statistiche</p>'
            + statRow('Visite totali',      fmtNum(views))
            + statRow('Visitatori unici',   fmtNum(visitors))
            + statRow('Media giornaliera',  fmtNum(Math.round(views / nDays)))
            + statRow('Pagine per visita',  visitors ? (views / visitors).toFixed(1) : '—')
            + (peak && peak.views
                ? statRow('Giorno di picco', fmtDay(peak.day) + ' · ' + fmtNum(peak.views))
                : '')
            + '<p class="adm-stat-note">Visitatore unico = combinazione anonima di '
            + 'IP e browser, rinnovata ogni giorno: chi torna in giorni diversi '
            + 'viene contato una volta per giorno.</p>';

        el.innerHTML = html;
    }

    /**
     * Grafico a barre delle visite giornaliere.
     *
     * Ogni barra porta due valori: le visite (barra intera) e i visitatori
     * unici (porzione piena in basso), così si legge subito quanta parte del
     * traffico sono persone diverse invece che pagine in più della stessa
     * sessione. La scala è esplicita a sinistra: senza, una barra alta non
     * dice nulla finché non ci passi sopra col mouse.
     */
    function renderChart(daily) {
        var el = $('adm-analytics-chart');
        if (!el) return;

        if (!daily.length) {
            el.innerHTML = '<p class="adm-muted">Nessun dato nel periodo.</p>';
            return;
        }

        var maxViews = daily.reduce(function (m, d) { return Math.max(m, d.views); }, 0);
        var scale    = niceCeil(maxViews || 1);

        // Con 30+ barre le date si sovrappongono: se ne etichetta una ogni N,
        // tenendo sempre la prima e l'ultima.
        var every = Math.max(1, Math.ceil(daily.length / 8));

        var grid = [1, 0.5, 0].map(function (f) {
            return '<div class="adm-chart__gridline" style="bottom:' + (f * 100) + '%">'
                 + '<span>' + fmtNum(Math.round(scale * f)) + '</span></div>';
        }).join('');

        var bars = daily.map(function (d, i) {
            var vh = scale ? (d.views / scale) * 100 : 0;
            var uh = d.views ? (d.visitors / d.views) * 100 : 0;
            var labelled = (i % every === 0) || (i === daily.length - 1);
            var title = fmtDay(d.day) + ': ' + fmtNum(d.views) + ' visite, '
                      + fmtNum(d.visitors) + ' visitatori';

            return '<div class="adm-chart__col" title="' + esc(title) + '">'
                 + '<div class="adm-chart__bar' + (d.views ? '' : ' is-empty') + '" '
                 +      'style="height:' + vh.toFixed(2) + '%">'
                 +   '<span class="adm-chart__bar-visitors" style="height:' + uh.toFixed(2) + '%"></span>'
                 + '</div>'
                 + (labelled
                     ? '<span class="adm-chart__label">' + esc(fmtDay(d.day)) + '</span>'
                     : '')
                 + '</div>';
        }).join('');

        /* Oltre ~45 giorni la spaziatura fissa fra le barre si mangia lo spazio
           delle barre stesse: su schermi stretti la finestra a 90 giorni le
           riduceva a meno di un pixel. */
        var colsClass = 'adm-chart__cols' + (daily.length > 45 ? ' is-dense' : '');

        el.innerHTML =
              '<div class="adm-chart">'
            +   '<div class="adm-chart__plot">' + grid + '<div class="' + colsClass + '">' + bars + '</div></div>'
            + '</div>'
            + '<div class="adm-chart__legend">'
            +   '<span><i class="adm-chart__key"></i>Visite</span>'
            +   '<span><i class="adm-chart__key adm-chart__key--visitors"></i>Visitatori unici</span>'
            + '</div>';
    }

    /**
     * Riga di classifica con barra proporzionale di sfondo: il confronto fra le
     * voci si legge dalla lunghezza, senza dover rapportare i numeri a mente.
     */
    function listRow(label, views, total, max, colLabel) {
        var width = max ? (views / max) * 100 : 0;
        return '<tr>'
             + '<td data-label="' + esc(colLabel) + '">'
             +   '<span class="adm-rank"><span class="adm-rank__fill" style="width:' + width.toFixed(1) + '%"></span>'
             +   '<span class="adm-rank__text">' + esc(label) + '</span></span>'
             + '</td>'
             + '<td class="adm-th--center adm-td--nowrap" data-label="Visite">'
             +   '<span class="adm-rank__value">' + esc(fmtNum(views)) + '</span>'
             +   '<span class="adm-rank__pct">' + esc(fmtPct(views, total)) + '</span>'
             + '</td>'
             + '</tr>';
    }

    function emptyRow() {
        return '<tr><td class="adm-muted" colspan="2">Nessun dato nel periodo.</td></tr>';
    }

    function renderTopList(tbodyId, rows, key, total, colLabel) {
        var tbody = $(tbodyId);
        if (!tbody) return;
        if (!rows.length) { tbody.innerHTML = emptyRow(); return; }

        var max = rows.reduce(function (m, r) { return Math.max(m, r.views); }, 0);
        tbody.innerHTML = rows.map(function (r) {
            return listRow(r[key] || '—', r.views, total, max, colLabel);
        }).join('');
    }

    /**
     * I referrer hanno una riga in più: il traffico diretto (o interno al sito),
     * che l'API tiene fuori dalla classifica ma che va mostrato, altrimenti le
     * percentuali non tornano e un sito con poche fonti esterne sembra senza dati.
     */
    function renderReferrers(data, total) {
        var tbody = $('adm-analytics-referrers-tbody');
        if (!tbody) return;

        var rows   = (data.topReferrers || []).slice();
        var direct = data.directViews || 0;
        if (!rows.length && !direct) { tbody.innerHTML = emptyRow(); return; }

        var max = Math.max(direct, rows.reduce(function (m, r) { return Math.max(m, r.views); }, 0));
        var html = rows.map(function (r) {
            return listRow(r.host || '—', r.views, total, max, 'Origine');
        }).join('');

        if (direct) html += listRow('Diretto / interno', direct, total, max, 'Origine');
        tbody.innerHTML = html;
    }

    /* ─── Eventi ───────────────────────────────────────────────────────────── */

    function initEvents() {
        var daysSelect = $('analytics-filter-days');
        if (daysSelect) {
            daysSelect.addEventListener('change', function () {
                state.days = daysSelect.value;
                load();
            });
        }
        var reloadBtn = $('btn-analytics-reload');
        if (reloadBtn) reloadBtn.addEventListener('click', load);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initEvents);
    } else {
        initEvents();
    }

    window.adminAnalytics = { load: load };

    // admin.js può aver aperto questa vista prima che il file fosse eseguito.
    window.dispatchEvent(new CustomEvent('aml-analytics-ready'));
})();
