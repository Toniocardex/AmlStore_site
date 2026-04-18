/**
 * admin.js — Aml Store Admin Panel (vanilla JS, no dipendenze)
 *
 * Chiama le API /api/admin/* same-origin (protette da Cloudflare Access + JWT).
 * Il JWT viene inviato automaticamente dal browser come cookie CF_Authorization
 * impostato da Cloudflare Access — non è necessario gestirlo manualmente.
 */

(function () {
    'use strict';

    /* ─── Stato globale ────────────────────────────────────────────────────── */

    var state = {
        page:            1,
        status:          '',
        paymentMethod:   '',
        search:          '',
        includeArchived: false,
        total:           0,
        pageSize:        50,
        loading:         false,
        openOrderId:     null,
    };

    /* ─── Utility DOM ──────────────────────────────────────────────────────── */

    function $  (id) { return document.getElementById(id); }
    function esc(s)  { return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

    function show(id) { var el = $(id); if (el) el.hidden = false; }
    function hide(id) { var el = $(id); if (el) el.hidden = true; }
    function text(id, val) { var el = $(id); if (el) el.textContent = val; }

    function fmtDate(iso) {
        if (!iso) return '—';
        try {
            return new Date(iso).toLocaleString('it-IT', {
                day:'2-digit', month:'2-digit', year:'2-digit',
                hour:'2-digit', minute:'2-digit',
            });
        } catch (_) { return iso; }
    }

    function fmtMoney(minor, currency) {
        try {
            return new Intl.NumberFormat('it-IT', {
                style: 'currency', currency: currency || 'EUR',
            }).format((minor || 0) / 100);
        } catch (_) { return '€ ' + ((minor || 0) / 100).toFixed(2); }
    }

    function nullOrDash(val) {
        return (val === null || val === undefined || val === '') ? null : val;
    }

    /* ─── Toast ────────────────────────────────────────────────────────────── */

    function toast(msg, type) {
        var c   = $('adm-toast-container');
        var el  = document.createElement('div');
        el.className = 'adm-toast adm-toast--' + (type || 'info');
        el.textContent = msg;
        c.appendChild(el);
        setTimeout(function () { el.remove(); }, 4000);
    }

    /* ─── API calls ────────────────────────────────────────────────────────── */

    function getCFToken() {
        var match = document.cookie.match(/(?:^|;\s*)CF_Authorization=([^;]+)/);
        return match ? match[1] : null;
    }

    function authHeaders(extra) {
        var h = Object.assign({}, extra || {});
        var token = getCFToken();
        if (token) h['Cf-Access-Jwt-Assertion'] = token;
        return h;
    }

    function apiGet(path) {
        return fetch(path, {
            credentials: 'same-origin',
            headers: authHeaders(),
        }).then(function (res) {
            if (res.status === 401) { toast('Sessione scaduta — ricarica la pagina', 'error'); throw new Error('401'); }
            if (!res.ok) throw new Error('HTTP ' + res.status);
            return res.json();
        });
    }

    function apiPost(path, body) {
        return fetch(path, {
            method:      'POST',
            credentials: 'same-origin',
            headers:     authHeaders({ 'Content-Type': 'application/json' }),
            body:        JSON.stringify(body || {}),
        }).then(function (res) {
            if (res.status === 401) { toast('Sessione scaduta — ricarica la pagina', 'error'); throw new Error('401'); }
            return res.json().then(function (data) {
                if (!res.ok) throw Object.assign(new Error(data.error || 'Error'), { data: data, status: res.status });
                return data;
            });
        });
    }

    /* ─── Carica lista ordini ──────────────────────────────────────────────── */

    function buildQueryString() {
        var params = new URLSearchParams();
        if (state.page > 1)         params.set('page',          state.page);
        if (state.status)           params.set('status',         state.status);
        if (state.paymentMethod)    params.set('paymentMethod',  state.paymentMethod);
        if (state.search)           params.set('search',         state.search);
        if (state.includeArchived)  params.set('archived',       '1');
        return params.toString() ? '?' + params.toString() : '';
    }

    function loadOrders() {
        if (state.loading) return;
        state.loading = true;

        show('adm-loading');
        hide('adm-error');
        hide('adm-empty');
        hide('adm-table-wrap');

        var url = '/api/admin/orders' + buildQueryString();

        apiGet(url).then(function (data) {
            state.total    = data.total   || 0;
            state.pageSize = data.pageSize || 50;
            state.loading  = false;

            renderStats(data);
            renderTable(data.orders || []);
            renderPagination();

        }).catch(function (e) {
            state.loading = false;
            hide('adm-loading');
            if (e.message !== '401') {
                show('adm-error');
                text('adm-error-msg', 'Errore caricamento ordini: ' + e.message);
            }
        });
    }

    /* ─── Rendering tabella ────────────────────────────────────────────────── */

    function statusBadge(status) {
        var map = {
            pending_payment: ['pending', 'In attesa'],
            paid:            ['paid',    'Pagato'],
            cancelled:       ['cancelled','Annullato'],
            refunded:        ['refunded', 'Rimborsato'],
        };
        var m = map[status] || ['pending', status];
        return '<span class="adm-badge adm-badge--' + m[0] + '">' + esc(m[1]) + '</span>';
    }

    function methodBadge(method) {
        var map = {
            stripe:        ['stripe',   'Carta'],
            paypal:        ['paypal',   'PayPal'],
            bank_transfer: ['transfer', 'Bonifico'],
        };
        var m = map[method] || ['transfer', method];
        return '<span class="adm-badge adm-badge--' + m[0] + '">' + esc(m[1]) + '</span>';
    }

    function renderStats(data) {
        var statEl = $('adm-stats');
        if (!statEl) return;
        var total = data.total || 0;
        var shown = (data.orders || []).length;
        statEl.innerHTML =
            '<p class="adm-filter-section__title">Risultati</p>' +
            '<div class="adm-stat-row"><span>Trovati</span><strong>' + total + '</strong></div>' +
            '<div class="adm-stat-row"><span>Mostrati</span><strong>' + shown + '</strong></div>';
    }

    function renderTable(orders) {
        hide('adm-loading');

        if (!orders.length) {
            show('adm-empty');
            text('adm-count', '0 ordini');
            return;
        }

        text('adm-count', state.total + ' ordini totali');
        show('adm-table-wrap');

        var rows = orders.map(function (o) {
            var items = (o.lineItems || []).map(function (i) {
                return '<span>' + esc((i.qty || 1) + '× ' + (i.name || i.sku || '?')) + '</span>';
            }).join('');

            var archived = o.archivedAt ? ' adm-row--archived' : '';

            return '<tr class="adm-order-row' + archived + '" data-id="' + esc(o.orderId) + '">'
                + '<td class="adm-td--nowrap"><span class="adm-order-id">' + esc(o.orderId) + '</span></td>'
                + '<td>'
                    + '<div class="adm-customer-name">' + esc((o.customer.firstName || '') + ' ' + (o.customer.lastName || '')) + '</div>'
                    + '<div class="adm-customer-email">' + esc(o.customer.email || '') + '</div>'
                    + (o.customer.company ? '<div class="adm-customer-company">' + esc(o.customer.company) + '</div>' : '')
                + '</td>'
                + '<td><div class="adm-items-list">' + (items || '<span class="adm-td--muted">—</span>') + '</div></td>'
                + '<td>' + methodBadge(o.paymentMethod) + '</td>'
                + '<td>' + statusBadge(o.status) + (o.archivedAt ? ' <span class="adm-badge adm-badge--archived">Archiviato</span>' : '') + '</td>'
                + '<td class="adm-td--center adm-td--nowrap"><strong>' + esc(fmtMoney(o.totalMinor, o.currency)) + '</strong></td>'
                + '<td class="adm-td--nowrap adm-td--muted">' + esc(fmtDate(o.createdAt)) + '</td>'
                + '<td class="adm-td--center adm-td--actions">'
                    + '<button class="adm-btn adm-btn--ghost adm-btn--sm btn-detail" data-id="' + esc(o.orderId) + '" title="Dettaglio">Dettaglio</button>'
                + '</td>'
            + '</tr>';
        }).join('');

        $('adm-tbody').innerHTML = rows;

        // Click su riga o pulsante dettaglio
        $('adm-tbody').querySelectorAll('.adm-order-row').forEach(function (row) {
            row.addEventListener('click', function (e) {
                if (e.target.closest('.adm-td--actions')) return; // gestito da btn-detail
                openDetail(row.dataset.id);
            });
        });
        $('adm-tbody').querySelectorAll('.btn-detail').forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.stopPropagation();
                openDetail(btn.dataset.id);
            });
        });
    }

    /* ─── Paginazione ──────────────────────────────────────────────────────── */

    function renderPagination() {
        var totalPages = Math.ceil(state.total / state.pageSize) || 1;
        var el = $('adm-pagination');
        if (!el) return;

        if (totalPages <= 1) { el.innerHTML = ''; return; }

        var html = '<button class="adm-page-btn" id="pg-prev" '
            + (state.page <= 1 ? 'disabled' : '') + '>‹</button>';

        // Mostra max 5 pagine intorno alla corrente
        var start = Math.max(1, state.page - 2);
        var end   = Math.min(totalPages, start + 4);
        start     = Math.max(1, end - 4);

        for (var p = start; p <= end; p++) {
            html += '<button class="adm-page-btn' + (p === state.page ? ' adm-page-btn--active' : '')
                + '" data-page="' + p + '">' + p + '</button>';
        }

        html += '<button class="adm-page-btn" id="pg-next" '
            + (state.page >= totalPages ? 'disabled' : '') + '>›</button>';

        el.innerHTML = html;

        el.querySelector('#pg-prev').addEventListener('click', function () {
            if (state.page > 1) { state.page--; loadOrders(); }
        });
        el.querySelector('#pg-next').addEventListener('click', function () {
            if (state.page < totalPages) { state.page++; loadOrders(); }
        });
        el.querySelectorAll('[data-page]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                state.page = Number(btn.dataset.page);
                loadOrders();
            });
        });
    }

    /* ─── Modal dettaglio ──────────────────────────────────────────────────── */

    function openDetail(orderId) {
        state.openOrderId = orderId;
        show('adm-modal-backdrop');
        $('adm-modal-backdrop').removeAttribute('aria-hidden');
        $('modal-body').innerHTML = '<div class="adm-loading adm-loading--inline"><div class="adm-spinner"></div><span>Caricamento…</span></div>';
        $('modal-footer').innerHTML = '';
        $('modal-title').textContent = 'Ordine ' + orderId;
        document.body.style.overflow = 'hidden';

        apiGet('/api/admin/orders/' + encodeURIComponent(orderId)).then(function (order) {
            renderDetail(order);
        }).catch(function (e) {
            $('modal-body').innerHTML = '<div class="adm-empty"><p>Errore caricamento: ' + esc(e.message) + '</p></div>';
        });
    }

    function closeDetail() {
        hide('adm-modal-backdrop');
        $('adm-modal-backdrop').setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
        state.openOrderId = null;
    }

    function renderDetail(o) {
        var isPaid     = o.status === 'paid';
        var isBT       = o.paymentMethod === 'bank_transfer';
        var isPending  = o.status === 'pending_payment';
        var isArchived = !!o.archivedAt;

        // ── Body ─────────────────────────────────────────────────────────────
        var html = '';

        // Intestazione ordine
        html += '<div class="adm-detail-section">'
            + '<p class="adm-detail-section__title">Riepilogo</p>'
            + '<div class="adm-detail-grid">'
            + field('N° Ordine',  '<span style="font-family:monospace;color:var(--adm-accent)">' + esc(o.orderId) + '</span>')
            + field('Stato',      statusBadge(o.status))
            + field('Metodo',     methodBadge(o.paymentMethod))
            + field('Totale',     '<strong>' + esc(fmtMoney(o.totalMinor, o.currency)) + '</strong>')
            + field('Creato',     esc(fmtDate(o.createdAt)))
            + field('Pagato il',  o.paidAt ? esc(fmtDate(o.paidAt)) : dash())
            + field('Locale',     esc(o.locale || '—'))
            + field('Email conf.', o.confirmationEmailSentAt ? esc(fmtDate(o.confirmationEmailSentAt)) : dash())
        + '</div></div>';

        // Cliente
        html += '<div class="adm-detail-section">'
            + '<p class="adm-detail-section__title">Cliente</p>'
            + '<div class="adm-detail-grid">'
            + field('Nome',      esc((o.customer.firstName || '') + ' ' + (o.customer.lastName || '')))
            + field('Email',     '<a href="mailto:' + esc(o.customer.email) + '">' + esc(o.customer.email) + '</a>')
            + field('Tipo',      esc(o.customer.type === 'business' ? 'Azienda' : 'Privato'))
            + (o.customer.company ? field('Ragione Soc.', esc(o.customer.company)) : '')
            + (o.customer.phone   ? field('Telefono',     esc(o.customer.phone))   : '')
            + (o.customer.piva    ? field('P.IVA',        esc(o.customer.piva))    : '')
            + (o.customer.pec     ? field('PEC',          esc(o.customer.pec))     : '')
            + (o.customer.sdi     ? field('SDI',          esc(o.customer.sdi))     : '')
        + '</div></div>';

        // Articoli
        var itemRows = (o.lineItems || []).map(function (i) {
            var qty  = i.qty || i.quantity || 1;
            var unit = i.unit_amount_minor || i.unitAmount || 0;
            return '<tr>'
                + '<td>' + esc(i.name || i.sku || '?') + (i.sku ? '<br><small style="color:var(--adm-muted)">' + esc(i.sku) + '</small>' : '') + '</td>'
                + '<td class="adm-td--right">' + qty + '</td>'
                + '<td class="adm-td--right">' + esc(fmtMoney(unit * qty, o.currency)) + '</td>'
            + '</tr>';
        }).join('');

        html += '<div class="adm-detail-section">'
            + '<p class="adm-detail-section__title">Articoli</p>'
            + '<table class="adm-detail-table"><thead><tr>'
            + '<th>Prodotto</th><th style="text-align:right">Qtà</th><th style="text-align:right">Subtotale</th>'
            + '</tr></thead><tbody>' + (itemRows || '<tr><td colspan="3" style="color:var(--adm-muted)">—</td></tr>') + '</tbody></table>'
            + '<p class="adm-detail-total">' + esc(fmtMoney(o.totalMinor, o.currency)) + '</p>'
        + '</div>';

        // Riferimenti PSP
        if (o.stripeSessionId || o.stripePaymentIntent || o.paypalOrderId || o.paypalCaptureId) {
            html += '<div class="adm-detail-section">'
                + '<p class="adm-detail-section__title">Riferimenti PSP</p>'
                + '<div class="adm-detail-grid">'
                + (o.stripeSessionId     ? fieldMono('Stripe Session',  o.stripeSessionId)     : '')
                + (o.stripePaymentIntent ? fieldMono('Payment Intent',  o.stripePaymentIntent) : '')
                + (o.paypalOrderId       ? fieldMono('PayPal Order ID', o.paypalOrderId)       : '')
                + (o.paypalCaptureId     ? fieldMono('PayPal Capture',  o.paypalCaptureId)     : '')
            + '</div></div>';
        }

        // Bonifico: causale
        if (isBT) {
            html += '<div class="adm-detail-section">'
                + '<p class="adm-detail-section__title">Bonifico</p>'
                + '<div class="adm-detail-grid">'
                + fieldMono('Causale (= ID ordine)', o.orderId)
                + field('Email IBAN inviata', o.confirmationEmailSentAt ? esc(fmtDate(o.confirmationEmailSentAt)) : dash())
                + field('Email pagato inviata', o.paidNotificationSentAt ? esc(fmtDate(o.paidNotificationSentAt)) : dash())
                + (o.markedPaidAt ? field('Marcato pagato il', esc(fmtDate(o.markedPaidAt))) : '')
                + (o.markedPaidBy ? field('Da',                esc(o.markedPaidBy)) : '')
                + (o.adminNotes   ? field('Note admin',        esc(o.adminNotes))   : '')
            + '</div></div>';
        }

        // Archivio
        if (isArchived) {
            html += '<div class="adm-detail-section">'
                + '<p class="adm-detail-section__title">Archivio</p>'
                + '<div class="adm-detail-grid">'
                + field('Archiviato il', esc(fmtDate(o.archivedAt)))
            + '</div></div>';
        }

        $('modal-body').innerHTML = html;

        // ── Footer con azioni ─────────────────────────────────────────────────
        var footerHtml = '';

        // "Segna come pagato": solo per bonifico pending e non archiviato
        if (isBT && isPending && !isArchived) {
            footerHtml += '<button class="adm-btn adm-btn--primary" id="btn-mark-paid">✓ Segna come pagato</button>';
        }

        // Archive / Unarchive
        if (!isArchived) {
            footerHtml += '<button class="adm-btn adm-btn--ghost" id="btn-archive">Archivia</button>';
        } else {
            footerHtml += '<button class="adm-btn adm-btn--ghost" id="btn-unarchive">Ripristina</button>';
        }

        footerHtml += '<button class="adm-btn adm-btn--danger adm-btn--sm" id="btn-delete" title="Eliminazione definitiva — irreversibile">🗑 Elimina</button>';
        footerHtml += '<button class="adm-btn adm-btn--ghost" id="btn-close-detail">Chiudi</button>';
        $('modal-footer').innerHTML = footerHtml;

        // Listeners footer
        var btnClose = document.getElementById('btn-close-detail');
        if (btnClose) btnClose.addEventListener('click', closeDetail);

        var btnMarkPaid = document.getElementById('btn-mark-paid');
        if (btnMarkPaid) {
            btnMarkPaid.addEventListener('click', function () {
                openConfirm(
                    'Segna ordine ' + o.orderId + ' come pagato?',
                    'Questa azione aggiornerà lo stato a <strong>Pagato</strong> e invierà la email di conferma al cliente con BCC Trustpilot.',
                    true,
                    function (notes) { doMarkPaid(o.orderId, notes); }
                );
            });
        }

        var btnArchive = document.getElementById('btn-archive');
        if (btnArchive) {
            btnArchive.addEventListener('click', function () {
                openConfirm(
                    'Archivia ordine ' + o.orderId + '?',
                    'L\'ordine sarà nascosto dalla lista principale ma non eliminato.',
                    false,
                    function () { doArchive(o.orderId); }
                );
            });
        }

        var btnUnarchive = document.getElementById('btn-unarchive');
        if (btnUnarchive) {
            btnUnarchive.addEventListener('click', function () { doUnarchive(o.orderId); });
        }

        var btnDelete = document.getElementById('btn-delete');
        if (btnDelete) {
            btnDelete.addEventListener('click', function () { openDeleteConfirm(o.orderId); });
        }
    }

    /* ─── Helper rendering campi detail ───────────────────────────────────── */

    function field(label, valueHtml) {
        return '<div class="adm-detail-field">'
            + '<div class="adm-detail-field__label">' + label + '</div>'
            + '<div class="adm-detail-field__value">' + valueHtml + '</div>'
            + '</div>';
    }

    function fieldMono(label, value) {
        return field(label,
            '<span class="adm-detail-field__value--mono">' + esc(value || '—') + '</span>'
        );
    }

    function dash() {
        return '<span class="adm-detail-field__value--null">—</span>';
    }

    /* ─── Dialog conferma ──────────────────────────────────────────────────── */

    var _confirmCallback = null;

    function openConfirm(title, msg, showNotes, callback) {
        _confirmCallback = callback;
        text('confirm-title', title);
        $('confirm-msg').innerHTML = msg;
        $('confirm-notes').value = '';
        $('confirm-notes-label').hidden = !showNotes;
        $('confirm-notes').hidden = !showNotes;
        show('adm-confirm-backdrop');
        $('adm-confirm-backdrop').removeAttribute('aria-hidden');
    }

    function closeConfirm() {
        hide('adm-confirm-backdrop');
        $('adm-confirm-backdrop').setAttribute('aria-hidden', 'true');
        _confirmCallback = null;
    }

    /* ─── Azioni admin ─────────────────────────────────────────────────────── */

    function doMarkPaid(orderId, notes) {
        var btn = $('confirm-ok');
        if (btn) { btn.disabled = true; btn.textContent = 'Elaborazione…'; }

        apiPost('/api/admin/orders/' + encodeURIComponent(orderId) + '/mark-paid', { notes: notes || null })
            .then(function (res) {
                closeConfirm();
                if (res.ok) {
                    toast('Ordine ' + orderId + ' segnato come pagato ✓', 'success');
                    closeDetail();
                    loadOrders();
                } else {
                    var msg = {
                        already_paid:    'Ordine già pagato.',
                        not_bank_transfer: 'Non è un ordine con bonifico.',
                        order_not_found: 'Ordine non trovato.',
                    }[res.reason] || 'Errore: ' + (res.reason || 'sconosciuto');
                    toast(msg, 'error');
                }
            })
            .catch(function (e) {
                closeConfirm();
                toast('Errore: ' + (e.message || 'sconosciuto'), 'error');
            });
    }

    function doArchive(orderId) {
        closeConfirm();
        apiPost('/api/admin/orders/' + encodeURIComponent(orderId) + '/archive')
            .then(function () {
                toast('Ordine archiviato', 'info');
                closeDetail();
                loadOrders();
            })
            .catch(function (e) { toast('Errore archivio: ' + e.message, 'error'); });
    }

    function doUnarchive(orderId) {
        apiPost('/api/admin/orders/' + encodeURIComponent(orderId) + '/unarchive')
            .then(function () {
                toast('Ordine ripristinato', 'info');
                closeDetail();
                loadOrders();
            })
            .catch(function (e) { toast('Errore ripristino: ' + e.message, 'error'); });
    }

    /* ─── Dialog eliminazione definitiva ──────────────────────────────────── */

    var _deleteOrderId = null;

    function openDeleteConfirm(orderId) {
        _deleteOrderId = orderId;
        $('delete-msg').innerHTML =
            'Stai per <strong>eliminare definitivamente</strong> l\'ordine ' +
            '<code style="color:#ef4444">' + esc(orderId) + '</code>.<br><br>' +
            'Questa operazione è <strong>irreversibile</strong>: tutti i dati ' +
            '(cliente, articoli, riferimenti PSP) saranno cancellati dal database.';
        $('delete-confirm-input').value = '';
        $('delete-ok').disabled = true;
        show('adm-delete-backdrop');
        $('adm-delete-backdrop').removeAttribute('aria-hidden');
        setTimeout(function () { $('delete-confirm-input').focus(); }, 50);
    }

    function closeDeleteConfirm() {
        hide('adm-delete-backdrop');
        $('adm-delete-backdrop').setAttribute('aria-hidden', 'true');
        _deleteOrderId = null;
    }

    function doDelete(orderId) {
        var btn = $('delete-ok');
        if (btn) { btn.disabled = true; btn.textContent = 'Eliminazione…'; }

        fetch('/api/admin/orders/' + encodeURIComponent(orderId), {
            method:      'DELETE',
            credentials: 'same-origin',
            headers:     authHeaders(),
        }).then(function (res) {
            return res.json().then(function (data) {
                if (!res.ok) throw new Error(data.error || 'HTTP ' + res.status);
                return data;
            });
        }).then(function () {
            closeDeleteConfirm();
            closeDetail();
            toast('Ordine ' + orderId + ' eliminato definitivamente', 'error');
            loadOrders();
        }).catch(function (e) {
            if (btn) { btn.disabled = false; btn.textContent = 'Elimina definitivamente'; }
            toast('Errore eliminazione: ' + e.message, 'error');
        });
    }

    /* ─── Event listeners globali ──────────────────────────────────────────── */

    function initEvents() {
        // Ricerca con debounce
        var searchTimer;
        var searchInput = $('filter-search');
        if (searchInput) {
            searchInput.addEventListener('input', function () {
                clearTimeout(searchTimer);
                searchTimer = setTimeout(function () {
                    state.search = searchInput.value.trim();
                    state.page   = 1;
                    loadOrders();
                }, 400);
            });
            searchInput.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') {
                    clearTimeout(searchTimer);
                    state.search = searchInput.value.trim();
                    state.page   = 1;
                    loadOrders();
                }
            });
        }

        var statusSel = $('filter-status');
        if (statusSel) statusSel.addEventListener('change', function () {
            state.status = statusSel.value;
            state.page   = 1;
        });

        var methodSel = $('filter-method');
        if (methodSel) methodSel.addEventListener('change', function () {
            state.paymentMethod = methodSel.value;
            state.page          = 1;
        });

        var archivedCb = $('filter-archived');
        if (archivedCb) archivedCb.addEventListener('change', function () {
            state.includeArchived = archivedCb.checked;
            state.page            = 1;
        });

        var btnSearch = $('btn-search');
        if (btnSearch) btnSearch.addEventListener('click', function () {
            state.search        = (searchInput ? searchInput.value.trim() : '');
            state.status        = (statusSel  ? statusSel.value  : '');
            state.paymentMethod = (methodSel  ? methodSel.value  : '');
            state.includeArchived = (archivedCb ? archivedCb.checked : false);
            state.page          = 1;
            loadOrders();
        });

        // Chiudi modal
        var modalClose = $('modal-close');
        if (modalClose) modalClose.addEventListener('click', closeDetail);

        var backdrop = $('adm-modal-backdrop');
        if (backdrop) backdrop.addEventListener('click', function (e) {
            if (e.target === backdrop) closeDetail();
        });

        // Conferma dialog
        var confirmOk     = $('confirm-ok');
        var confirmCancel = $('confirm-cancel');
        if (confirmOk) confirmOk.addEventListener('click', function () {
            if (_confirmCallback) {
                var notes = ($('confirm-notes').hidden ? null : $('confirm-notes').value.trim()) || null;
                _confirmCallback(notes);
            }
        });
        if (confirmCancel) confirmCancel.addEventListener('click', closeConfirm);

        var confirmBack = $('adm-confirm-backdrop');
        if (confirmBack) confirmBack.addEventListener('click', function (e) {
            if (e.target === confirmBack) closeConfirm();
        });

        // Dialog eliminazione
        var deleteInput  = $('delete-confirm-input');
        var deleteOk     = $('delete-ok');
        var deleteCancel = $('delete-cancel');
        var deleteBack   = $('adm-delete-backdrop');

        if (deleteInput) {
            deleteInput.addEventListener('input', function () {
                deleteOk.disabled = (deleteInput.value.trim() !== _deleteOrderId);
            });
            deleteInput.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' && !deleteOk.disabled) doDelete(_deleteOrderId);
            });
        }
        if (deleteOk)     deleteOk.addEventListener('click', function () {
            if (_deleteOrderId) doDelete(_deleteOrderId);
        });
        if (deleteCancel) deleteCancel.addEventListener('click', closeDeleteConfirm);
        if (deleteBack)   deleteBack.addEventListener('click', function (e) {
            if (e.target === deleteBack) closeDeleteConfirm();
        });

        // ESC per chiudere modal
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                if (!$('adm-delete-backdrop').hidden)  { closeDeleteConfirm(); return; }
                if (!$('adm-confirm-backdrop').hidden) { closeConfirm();       return; }
                if (!$('adm-modal-backdrop').hidden)   { closeDetail();        return; }
            }
        });
    }

    /* ─── Init ─────────────────────────────────────────────────────────────── */

    function init() {
        // Mostra email utente dall'header CF-Access
        // L'email è disponibile nell'header Cf-Access-Authenticated-User-Email
        // ma non accessibile dal browser JS direttamente; usiamo un fetch a
        // /cdn-cgi/access/get-identity per recuperare le info utente
        fetch('/cdn-cgi/access/get-identity', { credentials: 'same-origin' })
            .then(function (r) { return r.ok ? r.json() : null; })
            .then(function (d) {
                if (d && d.email) {
                    var el = $('adm-user-email');
                    if (el) el.textContent = d.email;
                }
            })
            .catch(function () {});

        initEvents();
        loadOrders();
    }

    // Espone reload per il pulsante "Riprova"
    window.adminApp = { reload: loadOrders };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
