/**
 * admin-analytics.js — vista "Analytics" del pannello admin (vanilla JS).
 *
 * Modulo indipendente da admin.js: nessun import del suo stato interno, solo
 * un piccolo set di helper propri. admin.js lo richiama via
 * window.adminAnalytics.load() quando l'utente apre il tab.
 */

(function () {
    'use strict';

    var state = {
        days:    '30',
        loading: false,
    };

    /* ─── Utility DOM (copia minima, stesso stile di admin.js) ───────────────── */

    function $  (id) { return document.getElementById(id); }
    function esc(s)  { return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
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

    function statRow(label, value) {
        return '<div class="adm-stat-row"><span>' + esc(label) + '</span><strong>' + esc(value) + '</strong></div>';
    }

    /* ─── Caricamento ──────────────────────────────────────────────────────── */

    function buildQueryString() {
        var params = new URLSearchParams();
        params.set('days', state.days);
        return '?' + params.toString();
    }

    function load() {
        if (state.loading) return;
        state.loading = true;

        show('adm-analytics-loading');
        hide('adm-analytics-error');
        hide('adm-analytics-content');

        apiGet('/api/admin/analytics' + buildQueryString()).then(function (data) {
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
        renderStats(data);
        renderChart(data.daily || []);
        renderTopList('adm-analytics-pages-tbody', data.topPages || [], function (r) { return r.path; }, function (r) { return r.views; }, null, 'Pagina');
        renderTopList('adm-analytics-referrers-tbody', data.topReferrers || [], function (r) { return r.host; }, function (r) { return r.views; }, 'Diretto / interno', 'Origine');
        renderTopList('adm-analytics-countries-tbody', data.topCountries || [], function (r) { return r.country; }, function (r) { return r.views; }, null, 'Paese');
        renderTopList('adm-analytics-devices-tbody', data.devices || [], function (r) { return r.device; }, function (r) { return r.views; }, null, 'Tipo');
    }

    function renderStats(data) {
        var el = $('adm-analytics-stats');
        if (!el) return;
        var avgPerDay = data.days ? Math.round((data.views || 0) / data.days) : 0;
        el.innerHTML = '<p class="adm-filter-section__title">Statistiche</p>'
            + statRow('Visite totali', data.views || 0)
            + statRow('Visitatori unici (stima)', data.visitors || 0)
            + statRow('Media giornaliera', avgPerDay);
    }

    function renderChart(daily) {
        var el = $('adm-analytics-chart');
        if (!el) return;
        if (!daily.length) { el.innerHTML = '<p class="adm-muted">Nessun dato nel periodo.</p>'; return; }

        var max = daily.reduce(function (m, d) { return Math.max(m, d.views); }, 1);
        el.innerHTML = daily.map(function (d) {
            var pct = Math.max(2, Math.round((d.views / max) * 100));
            var label = d.day.slice(5); // MM-DD
            return '<div class="adm-analytics-bar" title="' + esc(d.day) + ': ' + esc(d.views) + ' visite">'
                + '<div class="adm-analytics-bar__fill" style="height:' + pct + '%"></div>'
                + '<span class="adm-analytics-bar__label">' + esc(label) + '</span>'
                + '</div>';
        }).join('');
    }

    function renderTopList(tbodyId, rows, getKey, getValue, emptyKeyLabel, keyColLabel) {
        var tbody = $(tbodyId);
        if (!tbody) return;
        if (!rows.length) {
            tbody.innerHTML = '<tr><td class="adm-muted" colspan="2">Nessun dato.</td></tr>';
            return;
        }
        tbody.innerHTML = rows.map(function (r) {
            var key = getKey(r);
            return '<tr><td data-label="' + esc(keyColLabel || '') + '">' + esc(key || emptyKeyLabel || '—') + '</td>'
                + '<td class="adm-th--center" data-label="Visite">' + esc(getValue(r)) + '</td></tr>';
        }).join('');
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
})();
