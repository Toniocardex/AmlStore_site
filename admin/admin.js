/**
 * admin.js — Eurolicenze Admin Panel (vanilla JS, no dipendenze)
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
        capabilities:    { deleteOrders: false },
        view:            'orders',
        stockLoading:    false,
        selected:        new Set(),
        cart: {
            page:      1,
            status:    'abandoned',
            days:      '30',
            hoursIdle: '2',
            hasEmail:  '',
            country:   '',
            total:     0,
            pageSize:  50,
            loading:   false,
            // Soglia effettivamente applicata, come la rimanda l'API: le etichette
            // di stato devono usare quella, non una copia locale.
            effectiveHoursIdle: 2,
            capabilities: { deleteCarts: false },
            selected:     new Set(),
            // cartId con checkout_order_id valorizzato nell'ultima riga renderizzata:
            // eliminarli fa sparire dati storici da "Checkout avviati"/"Pagati" in
            // getCartStats (JOIN su checkout_order_id), quindi il dialog li segnala.
            linkedIds:    new Set(),
        },
    };

    /* ─── Utility DOM ──────────────────────────────────────────────────────── */

    function $  (id) { return document.getElementById(id); }
    function esc(s)  { return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

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

    function authHeaders(extra) {
        return Object.assign({}, extra || {});
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
        clearSelection();

        show('adm-loading');
        hide('adm-error');
        hide('adm-empty');
        hide('adm-table-wrap');

        var url = '/api/admin/orders' + buildQueryString();

        apiGet(url).then(function (data) {
            state.total    = data.total   || 0;
            state.pageSize = data.pageSize || 50;
            state.capabilities = data.capabilities || { deleteOrders: false };
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

    /* Etichetta di ripiego per un valore non mappato: leggibile a video, ma
       riconoscibile come dato grezzo. */
    function rawLabel(value) {
        return String(value || '—').replace(/_/g, ' ');
    }

    function statusBadge(status) {
        var map = {
            pending_payment: ['pending', 'In attesa'],
            paid:            ['paid',    'Pagato'],
            cancelled:       ['cancelled','Annullato'],
            refunded:        ['refunded', 'Rimborsato'],
        };
        /* Un valore fuori mappa e' un dato inatteso, non un ordine in attesa:
           badge neutro, cosi' si vede che e' sconosciuto invece di leggersi
           come uno stato che non e'. */
        var m = map[status] || ['unknown', rawLabel(status)];
        return '<span class="adm-badge adm-badge--' + m[0] + '">' + esc(m[1]) + '</span>';
    }

    function methodBadge(method) {
        var map = {
            stripe:        ['stripe',   'Carta'],
            paypal:        ['paypal',   'PayPal'],
            bank_transfer: ['transfer', 'Bonifico'],
        };
        /* Il backend scrive solo stripe | paypal | bank_transfer (vedi
           functions/api/[[catchall]].js). Qualsiasi altro valore prendeva lo
           stile del bonifico: un metodo diverso col colore di un altro. */
        var m = map[method] || ['unknown', rawLabel(method)];
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
            updateBulkBar();
            return;
        }

        text('adm-count', state.total + ' ordini totali');
        show('adm-table-wrap');

        var rows = orders.map(function (o) {
            var items = (o.lineItems || []).map(function (i) {
                return '<span>' + esc((i.qty || 1) + '× ' + (i.name || i.sku || '?')) + '</span>';
            }).join('');

            var archived = o.archivedAt ? ' adm-row--archived' : '';
            var checked  = state.selected.has(o.orderId) ? ' checked' : '';

            var cust = o.customer || {};
            return '<tr class="adm-order-row' + archived + '" data-id="' + esc(o.orderId) + '">'
                + '<td class="adm-td--check" data-label="Seleziona">'
                    + '<input type="checkbox" class="adm-checkbox adm-row-check" data-id="'
                    + esc(o.orderId) + '"' + checked
                    + ' aria-label="Seleziona ordine ' + esc(o.orderId) + '">'
                + '</td>'
                + '<td class="adm-td--nowrap" data-label="Ordine"><span class="adm-order-id">' + esc(o.orderId) + '</span>' + (o.requiresShipping ? ' <span title="Contiene articoli fisici da spedire">📦</span>' : '') + '</td>'
                + '<td data-label="Cliente">'
                    + '<div class="adm-customer-name">' + esc((cust.firstName || '') + ' ' + (cust.lastName || '')) + '</div>'
                    + '<div class="adm-customer-email">' + esc(cust.email || '') + '</div>'
                    + (cust.company ? '<div class="adm-customer-company">' + esc(cust.company) + '</div>' : '')
                + '</td>'
                + '<td data-label="Articoli"><div class="adm-items-list">' + (items || '<span class="adm-td--muted">—</span>') + '</div></td>'
                + '<td data-label="Metodo">' + methodBadge(o.paymentMethod) + '</td>'
                + '<td data-label="Stato">' + statusBadge(o.status) + (o.archivedAt ? ' <span class="adm-badge adm-badge--archived">Archiviato</span>' : '') + '</td>'
                + '<td class="adm-td--center adm-td--nowrap" data-label="Totale"><strong>' + esc(fmtMoney(o.totalMinor, o.currency)) + '</strong></td>'
                + '<td class="adm-td--nowrap adm-td--muted" data-label="Data">' + esc(fmtDate(o.createdAt)) + '</td>'
                + '<td class="adm-td--center adm-td--actions">'
                    + '<button class="adm-btn adm-btn--ghost adm-btn--sm btn-detail" data-id="' + esc(o.orderId) + '" title="Dettagli">Dettagli</button>'
                + '</td>'
            + '</tr>';
        }).join('');

        $('adm-tbody').innerHTML = rows;

        // Click su riga o pulsante dettaglio
        $('adm-tbody').querySelectorAll('.adm-order-row').forEach(function (row) {
            row.addEventListener('click', function (e) {
                if (e.target.closest('.adm-td--actions')) return;
                if (e.target.closest('.adm-td--check')) return;
                openDetail(row.dataset.id);
            });
        });
        $('adm-tbody').querySelectorAll('.btn-detail').forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.stopPropagation();
                openDetail(btn.dataset.id);
            });
        });
        $('adm-tbody').querySelectorAll('.adm-row-check').forEach(function (cb) {
            cb.addEventListener('click', function (e) { e.stopPropagation(); });
            cb.addEventListener('change', function () {
                var id = cb.dataset.id;
                if (cb.checked) state.selected.add(id);
                else state.selected.delete(id);
                syncSelectAll();
                updateBulkBar();
            });
        });

        syncSelectAll();
        updateBulkBar();
    }

    /* ─── Selezione multipla ───────────────────────────────────────────────── */

    function clearSelection() {
        state.selected.clear();
        var selectAll = $('orders-select-all');
        if (selectAll) {
            selectAll.checked = false;
            selectAll.indeterminate = false;
        }
        updateBulkBar();
    }

    function syncSelectAll() {
        var selectAll = $('orders-select-all');
        if (!selectAll) return;
        var boxes = $('adm-tbody')
            ? Array.prototype.slice.call($('adm-tbody').querySelectorAll('.adm-row-check'))
            : [];
        if (!boxes.length) {
            selectAll.checked = false;
            selectAll.indeterminate = false;
            return;
        }
        var nChecked = boxes.filter(function (b) { return b.checked; }).length;
        selectAll.checked = nChecked === boxes.length;
        selectAll.indeterminate = nChecked > 0 && nChecked < boxes.length;
    }

    function updateBulkBar() {
        var bar = $('adm-bulk-bar');
        if (!bar) return;
        var n = state.selected.size;
        if (n === 0) {
            bar.hidden = true;
            return;
        }
        bar.hidden = false;
        var countEl = $('adm-bulk-count');
        if (countEl) countEl.textContent = n + (n === 1 ? ' selezionato' : ' selezionati');
        var btnDel = $('btn-bulk-delete');
        if (btnDel) btnDel.hidden = !state.capabilities.deleteOrders;
    }

    function selectedIds() {
        var out = [];
        state.selected.forEach(function (id) { out.push(id); });
        return out;
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
            + field('N° Ordine',  '<span style="font-family:monospace;color:var(--adm-accent-ink)">' + esc(o.orderId) + '</span>')
            + field('Stato',      statusBadge(o.status))
            + field('Metodo',     methodBadge(o.paymentMethod))
            + field('Totale',     '<strong>' + esc(fmtMoney(o.totalMinor, o.currency)) + '</strong>')
            + field('Creato',     esc(fmtDate(o.createdAt)))
            + field('Pagato il',  o.paidAt ? esc(fmtDate(o.paidAt)) : dash())
            + field('Locale',     esc(o.locale || '—'))
            + field('Email conf.', o.confirmationEmailSentAt ? esc(fmtDate(o.confirmationEmailSentAt)) : dash())
        + '</div></div>';

        html += '<div class="adm-detail-section">'
            + '<p class="adm-detail-section__title">Notifiche</p>'
            + '<div class="adm-detail-grid">'
            + field('Email cliente', o.confirmationEmailSentAt ? esc(fmtDate(o.confirmationEmailSentAt)) : dash())
            + field('Email interna', o.internalNotificationSentAt ? esc(fmtDate(o.internalNotificationSentAt)) : dash())
            + (o.internalNotificationEventSrc ? field('Evento interno', esc(o.internalNotificationEventSrc)) : '')
            + (isBT ? field('Email pagato', o.paidNotificationSentAt ? esc(fmtDate(o.paidNotificationSentAt)) : dash()) : '')
        + '</div></div>';

        // Cliente
        var c = o.customer || {};
        html += '<div class="adm-detail-section">'
            + '<p class="adm-detail-section__title">Cliente</p>'
            + '<div class="adm-detail-grid">'
            + field('Nome',      esc((c.firstName || '') + ' ' + (c.lastName || '')))
            + field('Email',     '<a href="mailto:' + esc(c.email || '') + '">' + esc(c.email || '—') + '</a>')
            + field('Tipo',      esc(c.type === 'business' ? 'Azienda' : 'Privato'))
            + (c.company ? field('Ragione Soc.', esc(c.company)) : '')
            + (c.phone   ? field('Telefono',     esc(c.phone))   : '')
            + (c.piva    ? field('P.IVA',        esc(c.piva))    : '')
            + (c.pec     ? field('PEC',          esc(c.pec))     : '')
            + (c.sdi     ? field('SDI',          esc(c.sdi))     : '')
        + '</div></div>';

        // Spedizione (solo ordini con articoli fisici: DVD/COA)
        if (o.requiresShipping && o.shipping) {
            var s = o.shipping;
            html += '<div class="adm-detail-section">'
                + '<p class="adm-detail-section__title">📦 Spedizione</p>'
                + '<div class="adm-detail-grid">'
                + field('Indirizzo', esc(s.addressLine1 || '—'))
                + field('Città',     esc(s.city || '—') + ' ' + esc(s.postalCode || ''))
                + (s.province ? field('Provincia', esc(s.province)) : '')
                + field('Paese',     esc(s.country || '—'))
            + '</div></div>';
        }

        // Articoli
        var itemRows = (o.lineItems || []).map(function (i) {
            var qty  = i.qty || i.quantity || 1;
            var unit = i.unit_amount_minor || i.unitAmount || 0;
            return '<tr>'
                + '<td>' + esc(i.name || i.sku || '?') + (i.physical ? ' 📦' : '') + (i.sku ? '<br><small style="color:var(--adm-muted)">' + esc(i.sku) + '</small>' : '') + '</td>'
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
                + field('Eliminazione', state.capabilities.deleteOrders ? 'Disponibile' : 'Disattivata da configurazione')
            + '</div></div>';
        }

        $('modal-body').innerHTML = html;

        // ── Footer con azioni ─────────────────────────────────────────────────
        var footerHtml = '';
        var canDelete = state.capabilities.deleteOrders
            && (isPending || o.status === 'cancelled' || isArchived);

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

        if (canDelete) {
            footerHtml += '<button class="adm-btn adm-btn--danger adm-btn--sm" id="btn-delete"'
                + ' title="Elimina definitivamente dal database">Elimina</button>';
        }
        // Generatore email licenza: si apre in una nuova scheda, cosi' il riepilogo
        // qui accanto resta visibile e si copia/incolla direttamente nel tool.
        footerHtml += '<a class="adm-btn adm-btn--ghost" href="/admin/email-license-generator.html"'
            + ' target="_blank" rel="noopener"'
            + ' title="Apre il generatore in una nuova scheda: copia qui il riepilogo e incollalo la">Email licenza ↗</a>';

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

    function doBulkArchive(ids) {
        closeConfirm();
        var ok = 0;
        var fail = 0;
        var i = 0;

        function next() {
            if (i >= ids.length) {
                toast(
                    'Archiviati ' + ok + '/' + ids.length
                        + (fail ? ', errori ' + fail : ''),
                    fail ? 'error' : 'info'
                );
                loadOrders();
                return;
            }
            var id = ids[i++];
            apiPost('/api/admin/orders/' + encodeURIComponent(id) + '/archive')
                .then(function () { ok++; next(); })
                .catch(function () { fail++; next(); });
        }
        next();
    }

    /* ─── Dialog eliminazione definitiva ──────────────────────────────────── */

    var _deleteOrderId = null;
    var _deleteMode    = 'single'; // 'single' | 'bulk'
    var _deleteIds     = [];
    var _deleteEntity  = 'order'; // 'order' | 'cart' — quale API/reload usare alla conferma
    var BULK_DELETE_TOKEN = 'ELIMINA';

    function deleteConfirmExpected() {
        // I cartId sono UUID opachi: farli ridigitare per intero sarebbe solo
        // attrito, quindi anche l'eliminazione singola di un carrello usa il
        // token fisso come il bulk.
        if (_deleteMode === 'bulk' || _deleteEntity === 'cart') return BULK_DELETE_TOKEN;
        return _deleteOrderId;
    }

    function syncDeleteOkEnabled() {
        var deleteInput = $('delete-confirm-input');
        var deleteOk    = $('delete-ok');
        if (!deleteInput || !deleteOk) return;
        deleteOk.disabled = (deleteInput.value.trim() !== deleteConfirmExpected());
    }

    function openDeleteConfirm(orderId) {
        _deleteMode    = 'single';
        _deleteEntity  = 'order';
        _deleteOrderId = orderId;
        _deleteIds     = [];
        $('delete-msg').innerHTML =
            'Stai per <strong>eliminare definitivamente</strong> l\'ordine ' +
            '<code style="color:#ef4444">' + esc(orderId) + '</code>.<br><br>' +
            'Consentito su ordini <strong>in attesa</strong> / <strong>annullati</strong> ' +
            '(es. spam) oppure su ordini già <strong>archiviati</strong>. ' +
            'Questa operazione è <strong>irreversibile</strong>: tutti i dati ' +
            '(cliente, articoli, riferimenti PSP) saranno cancellati dal database.';
        var label = $('delete-confirm-label');
        if (label) label.textContent = 'Digita l\'ID ordine per confermare:';
        var input = $('delete-confirm-input');
        if (input) {
            input.value = '';
            input.placeholder = 'EL-XXXXXXXX';
        }
        $('delete-ok').disabled = true;
        $('delete-ok').textContent = 'Elimina definitivamente';
        show('adm-delete-backdrop');
        $('adm-delete-backdrop').removeAttribute('aria-hidden');
        setTimeout(function () { $('delete-confirm-input').focus(); }, 50);
    }

    function openBulkDeleteConfirm(ids) {
        _deleteMode    = 'bulk';
        _deleteEntity  = 'order';
        _deleteOrderId = null;
        _deleteIds     = ids.slice();
        $('delete-msg').innerHTML =
            'Stai per <strong>eliminare definitivamente</strong> ' +
            '<strong style="color:#ef4444">' + ids.length + ' ordini</strong> selezionati.<br><br>' +
            'Consentito su ordini <strong>in attesa</strong> / <strong>annullati</strong> ' +
            '(es. spam) oppure già <strong>archiviati</strong>. ' +
            'Gli ordini non eliminabili verranno saltati. ' +
            'Operazione <strong>irreversibile</strong>.';
        var label = $('delete-confirm-label');
        if (label) label.textContent = 'Digita ELIMINA per confermare:';
        var input = $('delete-confirm-input');
        if (input) {
            input.value = '';
            input.placeholder = 'ELIMINA';
        }
        $('delete-ok').disabled = true;
        $('delete-ok').textContent = 'Elimina definitivamente';
        show('adm-delete-backdrop');
        $('adm-delete-backdrop').removeAttribute('aria-hidden');
        setTimeout(function () { $('delete-confirm-input').focus(); }, 50);
    }

    function openCartDeleteConfirm(cartId) {
        _deleteMode    = 'single';
        _deleteEntity  = 'cart';
        _deleteOrderId = cartId;
        _deleteIds     = [];
        $('delete-msg').innerHTML =
            'Stai per <strong>eliminare definitivamente</strong> questo carrello.<br><br>' +
            'Verranno cancellati lo snapshot e l\'email eventualmente associata. ' +
            'L\'ordine collegato (se il checkout è stato completato) non viene toccato: ' +
            'vive in una tabella separata. Operazione <strong>irreversibile</strong>.' +
            (state.cart.linkedIds.has(cartId)
                ? '<br><br>⚠️ <strong>Questo carrello ha un checkout collegato</strong>: eliminandolo, il conteggio storico ' +
                  '"Checkout avviati"/"Pagati" nelle statistiche di questo periodo diminuirà di conseguenza.'
                : '');
        var label = $('delete-confirm-label');
        if (label) label.textContent = 'Digita ELIMINA per confermare:';
        var input = $('delete-confirm-input');
        if (input) {
            input.value = '';
            input.placeholder = 'ELIMINA';
        }
        $('delete-ok').disabled = true;
        $('delete-ok').textContent = 'Elimina definitivamente';
        show('adm-delete-backdrop');
        $('adm-delete-backdrop').removeAttribute('aria-hidden');
        setTimeout(function () { $('delete-confirm-input').focus(); }, 50);
    }

    function openCartBulkDeleteConfirm(ids) {
        _deleteMode    = 'bulk';
        _deleteEntity  = 'cart';
        _deleteOrderId = null;
        _deleteIds     = ids.slice();
        var linkedCount = ids.filter(function (id) { return state.cart.linkedIds.has(id); }).length;
        $('delete-msg').innerHTML =
            'Stai per <strong>eliminare definitivamente</strong> ' +
            '<strong style="color:#ef4444">' + ids.length + ' carrelli</strong> selezionati.<br><br>' +
            'Gli ordini collegati (se presenti) non vengono toccati. ' +
            'Operazione <strong>irreversibile</strong>.' +
            (linkedCount
                ? '<br><br>⚠️ <strong>' + linkedCount + ' di questi hanno un checkout collegato</strong>: eliminandoli, il conteggio storico ' +
                  '"Checkout avviati"/"Pagati" nelle statistiche di questo periodo diminuirà di conseguenza.'
                : '');
        var label = $('delete-confirm-label');
        if (label) label.textContent = 'Digita ELIMINA per confermare:';
        var input = $('delete-confirm-input');
        if (input) {
            input.value = '';
            input.placeholder = 'ELIMINA';
        }
        $('delete-ok').disabled = true;
        $('delete-ok').textContent = 'Elimina definitivamente';
        show('adm-delete-backdrop');
        $('adm-delete-backdrop').removeAttribute('aria-hidden');
        setTimeout(function () { $('delete-confirm-input').focus(); }, 50);
    }

    function closeDeleteConfirm() {
        hide('adm-delete-backdrop');
        $('adm-delete-backdrop').setAttribute('aria-hidden', 'true');
        _deleteOrderId = null;
        _deleteMode    = 'single';
        _deleteEntity  = 'order';
        _deleteIds     = [];
    }

    function deleteReasonMessage(reason, fallback) {
        return {
            delete_disabled: 'Eliminazione disattivata da configurazione (ADMIN_ALLOW_DELETE_ORDERS).',
            not_deletable:   'Eliminabile solo se in attesa/annullato, oppure dopo archivio.',
            order_not_found: 'Ordine non trovato.',
        }[reason] || fallback;
    }

    function apiDeleteOrder(orderId) {
        return fetch('/api/admin/orders/' + encodeURIComponent(orderId), {
            method:      'DELETE',
            credentials: 'same-origin',
            headers:     authHeaders(),
        }).then(function (res) {
            return res.json().then(function (data) {
                if (!res.ok) throw Object.assign(new Error(data.error || 'HTTP ' + res.status), {
                    data: data,
                    status: res.status,
                });
                return data;
            });
        });
    }

    function doDelete(orderId) {
        var btn = $('delete-ok');
        if (btn) { btn.disabled = true; btn.textContent = 'Eliminazione…'; }

        apiDeleteOrder(orderId).then(function () {
            closeDeleteConfirm();
            closeDetail();
            toast('Ordine ' + orderId + ' eliminato definitivamente', 'error');
            loadOrders();
        }).catch(function (e) {
            if (btn) { btn.disabled = false; btn.textContent = 'Elimina definitivamente'; }
            var reason = e.data && e.data.reason;
            toast('Errore eliminazione: ' + deleteReasonMessage(reason, e.message), 'error');
        });
    }

    function doBulkDelete(ids) {
        var btn = $('delete-ok');
        if (btn) { btn.disabled = true; btn.textContent = 'Eliminazione…'; }

        var ok = 0;
        var skip = 0;
        var i = 0;

        function next() {
            if (i >= ids.length) {
                closeDeleteConfirm();
                toast(
                    'Eliminati ' + ok + '/' + ids.length
                        + (skip ? ', saltati ' + skip : ''),
                    ok ? 'error' : 'info'
                );
                loadOrders();
                return;
            }
            var id = ids[i++];
            apiDeleteOrder(id)
                .then(function () { ok++; next(); })
                .catch(function () { skip++; next(); });
        }
        next();
    }

    function cartDeleteReasonMessage(reason, fallback) {
        return {
            delete_disabled: 'Eliminazione disattivata da configurazione (ADMIN_ALLOW_DELETE_CARTS).',
            cart_not_found:  'Carrello non trovato (forse già rimosso dalla conservazione automatica).',
        }[reason] || fallback;
    }

    function apiDeleteCart(cartId) {
        return fetch('/api/admin/carts/' + encodeURIComponent(cartId), {
            method:      'DELETE',
            credentials: 'same-origin',
            headers:     authHeaders(),
        }).then(function (res) {
            return res.json().then(function (data) {
                if (!res.ok) throw Object.assign(new Error(data.error || 'HTTP ' + res.status), {
                    data: data,
                    status: res.status,
                });
                return data;
            });
        });
    }

    function doCartDelete(cartId) {
        var btn = $('delete-ok');
        if (btn) { btn.disabled = true; btn.textContent = 'Eliminazione…'; }

        apiDeleteCart(cartId).then(function () {
            closeDeleteConfirm();
            state.cart.selected.delete(cartId);
            toast('Carrello eliminato definitivamente', 'error');
            loadCarts();
        }).catch(function (e) {
            if (btn) { btn.disabled = false; btn.textContent = 'Elimina definitivamente'; }
            var reason = e.data && e.data.reason;
            toast('Errore eliminazione: ' + cartDeleteReasonMessage(reason, e.message), 'error');
        });
    }

    function doCartBulkDelete(ids) {
        var btn = $('delete-ok');
        if (btn) { btn.disabled = true; btn.textContent = 'Eliminazione…'; }

        var ok = 0;
        var skip = 0;
        var i = 0;

        function next() {
            if (i >= ids.length) {
                closeDeleteConfirm();
                clearCartSelection();
                toast(
                    'Eliminati ' + ok + '/' + ids.length
                        + (skip ? ', saltati ' + skip : ''),
                    ok ? 'error' : 'info'
                );
                loadCarts();
                return;
            }
            var id = ids[i++];
            apiDeleteCart(id)
                .then(function () { ok++; next(); })
                .catch(function () { skip++; next(); });
        }
        next();
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

        function confirmDelete() {
            if (_deleteEntity === 'cart') {
                if (_deleteMode === 'bulk') doCartBulkDelete(_deleteIds.slice());
                else if (_deleteOrderId) doCartDelete(_deleteOrderId);
            } else {
                if (_deleteMode === 'bulk') doBulkDelete(_deleteIds.slice());
                else if (_deleteOrderId) doDelete(_deleteOrderId);
            }
        }

        if (deleteInput) {
            deleteInput.addEventListener('input', syncDeleteOkEnabled);
            deleteInput.addEventListener('keydown', function (e) {
                if (e.key !== 'Enter' || deleteOk.disabled) return;
                confirmDelete();
            });
        }
        if (deleteOk) deleteOk.addEventListener('click', confirmDelete);
        if (deleteCancel) deleteCancel.addEventListener('click', closeDeleteConfirm);
        if (deleteBack)   deleteBack.addEventListener('click', function (e) {
            if (e.target === deleteBack) closeDeleteConfirm();
        });

        // Selezione multipla
        var selectAll = $('orders-select-all');
        if (selectAll) {
            selectAll.addEventListener('change', function () {
                var boxes = $('adm-tbody')
                    ? Array.prototype.slice.call($('adm-tbody').querySelectorAll('.adm-row-check'))
                    : [];
                boxes.forEach(function (cb) {
                    cb.checked = selectAll.checked;
                    if (selectAll.checked) state.selected.add(cb.dataset.id);
                    else state.selected.delete(cb.dataset.id);
                });
                selectAll.indeterminate = false;
                updateBulkBar();
            });
        }

        var btnBulkArchive = $('btn-bulk-archive');
        if (btnBulkArchive) {
            btnBulkArchive.addEventListener('click', function () {
                var ids = selectedIds();
                if (!ids.length) return;
                openConfirm(
                    'Archivia ' + ids.length + ' ordini?',
                    'Gli ordini selezionati saranno nascosti dalla lista principale ma non eliminati.',
                    false,
                    function () { doBulkArchive(ids); }
                );
            });
        }

        var btnBulkDelete = $('btn-bulk-delete');
        if (btnBulkDelete) {
            btnBulkDelete.addEventListener('click', function () {
                var ids = selectedIds();
                if (!ids.length) return;
                if (!state.capabilities.deleteOrders) {
                    toast('Eliminazione disattivata da configurazione.', 'error');
                    return;
                }
                openBulkDeleteConfirm(ids);
            });
        }

        var btnBulkClear = $('btn-bulk-clear');
        if (btnBulkClear) {
            btnBulkClear.addEventListener('click', function () {
                clearSelection();
                var boxes = $('adm-tbody')
                    ? Array.prototype.slice.call($('adm-tbody').querySelectorAll('.adm-row-check'))
                    : [];
                boxes.forEach(function (cb) { cb.checked = false; });
            });
        }

        // ESC per chiudere modal
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                if (!$('adm-delete-backdrop').hidden)  { closeDeleteConfirm(); return; }
                if (!$('adm-confirm-backdrop').hidden) { closeConfirm();       return; }
                if (!$('adm-modal-backdrop').hidden)   { closeDetail();        return; }
            }
        });
    }

    /* ─── Magazzino ────────────────────────────────────────────────────────── */

    function setView(view) {
        state.view = (view === 'stock' || view === 'carts' || view === 'analytics') ? view : 'orders';
        var ordersEl    = $('adm-view-orders');
        var stockEl     = $('adm-view-stock');
        var cartsEl     = $('adm-view-carts');
        var analyticsEl = $('adm-view-analytics');
        var navOrders    = $('nav-orders');
        var navStock     = $('nav-stock');
        var navCarts     = $('nav-carts');
        var navAnalytics = $('nav-analytics');
        if (ordersEl)    ordersEl.hidden    = state.view !== 'orders';
        if (stockEl)     stockEl.hidden     = state.view !== 'stock';
        if (cartsEl)     cartsEl.hidden     = state.view !== 'carts';
        if (analyticsEl) analyticsEl.hidden = state.view !== 'analytics';
        if (navOrders)    navOrders.classList.toggle('is-active', state.view === 'orders');
        if (navStock)     navStock.classList.toggle('is-active', state.view === 'stock');
        if (navCarts)     navCarts.classList.toggle('is-active', state.view === 'carts');
        if (navAnalytics) navAnalytics.classList.toggle('is-active', state.view === 'analytics');
        if (state.view === 'stock')          loadStock();
        else if (state.view === 'carts')     loadCarts();
        else if (state.view === 'analytics') loadAnalytics();
        else                                   loadOrders();

        // Persiste la scheda attiva nell'URL: un refresh o un link diretto
        // deve riaprire la stessa vista, non ripartire sempre da Ordini.
        var hash = '#' + state.view;
        if (window.location.hash !== hash) history.replaceState(null, '', hash);
    }

    /**
     * La vista Analytics vive in admin-analytics.js, uno script separato.
     * Entrambi i file sono `defer`, quindi quando init() gira (readyState è già
     * 'interactive') quel modulo può non essersi ancora registrato: chiamarlo
     * solo se presente lasciava lo spinner acceso per sempre. Qui il
     * caricamento parte comunque, appena il modulo si annuncia.
     */
    function loadAnalytics() {
        if (window.adminAnalytics) { window.adminAnalytics.load(); return; }
        window.addEventListener('aml-analytics-ready', function () {
            window.adminAnalytics.load();
        }, { once: true });
    }

    function loadStock() {
        if (state.stockLoading) return;
        state.stockLoading = true;
        show('adm-stock-loading');
        hide('adm-stock-error');
        hide('adm-stock-table-wrap');

        apiGet('/api/admin/stock').then(function (data) {
            state.stockLoading = false;
            hide('adm-stock-loading');
            renderStockTable(data.items || []);
        }).catch(function (e) {
            state.stockLoading = false;
            hide('adm-stock-loading');
            if (e.message !== '401') {
                show('adm-stock-error');
                text('adm-stock-error-msg', 'Errore caricamento magazzino: ' + e.message);
            }
        });
    }

    function renderStockTable(items) {
        text('adm-stock-count', items.length + ' SKU fisici');
        if (!items.length) {
            show('adm-stock-error');
            text('adm-stock-error-msg', 'Nessun SKU fisico in catalogo.');
            return;
        }
        show('adm-stock-table-wrap');
        var tbody = $('adm-stock-tbody');
        if (!tbody) return;
        tbody.innerHTML = items.map(function (it) {
            var qty = Number(it.qty) || 0;
            var updated = it.updatedAt
                ? fmtDate(it.updatedAt) + (it.updatedBy ? ' · ' + esc(it.updatedBy) : '')
                : '—';
            return '<tr data-sku="' + esc(it.sku) + '">'
                + '<td class="adm-td--nowrap" data-label="SKU"><code class="adm-sku">' + esc(it.sku) + '</code></td>'
                + '<td data-label="Prodotto">' + esc(it.name) + '</td>'
                + '<td class="adm-th--center" data-label="Qty">'
                + '<input type="number" class="adm-input adm-input--qty" min="0" max="999999" step="1" '
                + 'value="' + qty + '" data-stock-qty="' + esc(it.sku) + '" aria-label="Quantità ' + esc(it.sku) + '">'
                + '</td>'
                + '<td class="adm-muted" data-label="Aggiornato">' + updated + '</td>'
                + '<td class="adm-th--center adm-td--actions">'
                + '<button type="button" class="adm-btn adm-btn--primary adm-btn--sm" data-stock-save="' + esc(it.sku) + '">Salva</button>'
                + '</td>'
                + '</tr>';
        }).join('');
    }

    function saveStock(sku) {
        var input = document.querySelector('[data-stock-qty="' + CSS.escape(sku) + '"]');
        if (!input) {
            var row = document.querySelector('tr[data-sku="' + CSS.escape(sku) + '"]');
            input = row ? row.querySelector('[data-stock-qty]') : null;
        }
        if (!input) return;
        var qty = Math.round(Number(input.value));
        if (!Number.isFinite(qty) || qty < 0) {
            toast('Quantità non valida', 'error');
            return;
        }
        apiPost('/api/admin/stock', { sku: sku, qty: qty }).then(function () {
            toast('Stock aggiornato: ' + sku + ' → ' + qty, 'success');
            loadStock();
        }).catch(function (e) {
            toast((e.data && e.data.error) || e.message || 'Errore salvataggio', 'error');
        });
    }

    /* ─── Carrelli (analytics carrelli abbandonati) ───────────────────────────── */

    function buildCartQueryString() {
        var params = new URLSearchParams();
        if (state.cart.page > 1)                                     params.set('page', state.cart.page);
        if (state.cart.status)                                       params.set('status', state.cart.status);
        if (state.cart.days !== '' && state.cart.days != null)       params.set('days', state.cart.days);
        if (state.cart.hoursIdle)                                    params.set('hoursIdle', state.cart.hoursIdle);
        if (state.cart.hasEmail === '1' || state.cart.hasEmail === '0') params.set('hasEmail', state.cart.hasEmail);
        if (state.cart.country)                                      params.set('country', state.cart.country);
        return params.toString() ? '?' + params.toString() : '';
    }

    function loadCarts() {
        if (state.cart.loading) return;
        state.cart.loading = true;
        clearCartSelection();

        show('adm-cart-loading');
        hide('adm-cart-error');
        hide('adm-cart-empty');
        hide('adm-cart-table-wrap');

        apiGet('/api/admin/carts' + buildCartQueryString()).then(function (data) {
            state.cart.total    = data.total    || 0;
            state.cart.pageSize = data.pageSize || 50;
            state.cart.loading  = false;
            state.cart.effectiveHoursIdle = Number(data.hoursIdle) || state.cart.effectiveHoursIdle;
            state.cart.capabilities = data.capabilities || { deleteCarts: false };

            renderCartStats(data.stats || {});
            renderCartsTable(data.carts || []);
            renderCartPagination();
        }).catch(function (e) {
            state.cart.loading = false;
            hide('adm-cart-loading');
            if (e.message !== '401') {
                show('adm-cart-error');
                text('adm-cart-error-msg', 'Errore caricamento carrelli: ' + e.message);
            }
        });
    }

    /**
     * Stato visivo di una riga. Due fonti di verità restano fuori da qui:
     * il pagato viene da orders.status (join lato server) e la soglia di
     * inattività è quella che l'API dichiara di aver applicato — riscriverla
     * qui significherebbe mostrare "Attivo" con criteri diversi da quelli con
     * cui la riga è stata selezionata.
     */
    function cartStatusInfo(c) {
        if (c.checkoutOrderId) {
            return c.orderStatus === 'paid' ? ['paid', 'Pagato'] : ['checkout', 'Checkout avviato'];
        }
        if (!c.itemCount) return ['empty', 'Vuoto'];
        var idleMs = Date.now() - new Date(c.updatedAt).getTime();
        return idleMs < state.cart.effectiveHoursIdle * 60 * 60 * 1000
            ? ['active', 'Attivo']
            : ['abandoned', 'Abbandonato'];
    }

    /* Etichette brevi: la colonna sta accanto a Stato e non deve allargare la
       tabella. Le stesse posizioni, per esteso, sono nel funnel della tab
       Analytics; l'ordine canonico vive in CHECKOUT_FUNNEL_STEPS lato server. */
    var CART_STEP_LABELS = {
        checkout_view:              ['Checkout',       'empty'],
        checkout_contact_started:   ['Dati avviati',   'unknown'],
        checkout_contact_completed: ['Dati ok',        'active'],
        checkout_payment_started:   ['Pagamento',      'checkout'],
        checkout_pay_clicked:       ['Ha premuto paga', 'pending'],
    };

    /**
     * Punto piu' avanzato toccato nel checkout.
     *
     * Il trattino non vuol dire "non e' mai arrivato al checkout": i carrelli
     * precedenti alla migrazione che ha aggiunto cart_id non hanno eventi
     * agganciabili. Il title lo dice, per non far leggere come dato un buco.
     */
    function furthestStepCell(c) {
        var step = c.furthestStep;
        if (!step) {
            return '<span class="adm-td--muted" title="Nessun evento di checkout '
                 + 'collegato: il cliente non ha raggiunto il checkout, oppure il '
                 + 'carrello precede il tracciamento del funnel.">—</span>';
        }
        var info = CART_STEP_LABELS[step] || [step, 'neutral'];
        return '<span class="adm-badge adm-badge--' + info[1] + '">' + esc(info[0]) + '</span>';
    }

    function renderCartsTable(carts) {
        hide('adm-cart-loading');

        if (!carts.length) {
            show('adm-cart-empty');
            text('adm-cart-count', '0 carrelli');
            updateCartBulkBar();
            return;
        }

        text('adm-cart-count', state.cart.total + ' carrelli totali');
        show('adm-cart-table-wrap');

        state.cart.linkedIds.clear();

        $('adm-cart-tbody').innerHTML = carts.map(function (c) {
            var items = (c.lineItems || []).map(function (i) {
                return '<span>' + esc((i.qty || 1) + '× ' + (i.name || i.sku || '?')) + '</span>';
            }).join('');
            var emailCell = c.email
                ? '<a href="mailto:' + esc(c.email) + '">' + esc(c.email) + '</a>'
                : '<span class="adm-td--muted">Anonimo</span>';
            var st = cartStatusInfo(c);
            var checked = state.cart.selected.has(c.cartId) ? ' checked' : '';
            if (c.checkoutOrderId) state.cart.linkedIds.add(c.cartId);

            return '<tr data-id="' + esc(c.cartId) + '">'
                + '<td class="adm-td--check" data-label="Seleziona">'
                    + '<input type="checkbox" class="adm-checkbox adm-cart-row-check" data-id="'
                    + esc(c.cartId) + '"' + checked
                    + ' aria-label="Seleziona carrello">'
                + '</td>'
                + '<td class="adm-td--nowrap adm-td--muted" data-label="Aggiornato">' + esc(fmtDate(c.updatedAt)) + '</td>'
                + '<td data-label="Email">' + emailCell + '</td>'
                + '<td data-label="Paese">' + esc(c.country || '—') + '</td>'
                + '<td data-label="Articoli"><div class="adm-items-list">' + (items || '<span class="adm-td--muted">—</span>') + '</div></td>'
                + '<td class="adm-td--center adm-td--nowrap" data-label="Totale"><strong>' + esc(fmtMoney(c.totalMinor, c.currency)) + '</strong></td>'
                + '<td data-label="Lingua">' + esc((c.locale || '').toUpperCase()) + '</td>'
                + '<td class="adm-td--center adm-td--nowrap" data-label="Arrivato a">' + furthestStepCell(c) + '</td>'
                + '<td class="adm-td--center" data-label="Stato"><span class="adm-badge adm-badge--' + st[0] + '">' + esc(st[1]) + '</span></td>'
                + '<td class="adm-td--center adm-td--actions">'
                    + (state.cart.capabilities.deleteCarts
                        ? '<button class="adm-btn adm-btn--ghost adm-btn--sm btn-cart-delete" data-id="' + esc(c.cartId) + '" title="Elimina definitivamente">Elimina</button>'
                        : '')
                + '</td>'
            + '</tr>';
        }).join('');

        $('adm-cart-tbody').querySelectorAll('.adm-cart-row-check').forEach(function (cb) {
            cb.addEventListener('change', function () {
                var id = cb.dataset.id;
                if (cb.checked) state.cart.selected.add(id);
                else state.cart.selected.delete(id);
                syncCartSelectAll();
                updateCartBulkBar();
            });
        });
        $('adm-cart-tbody').querySelectorAll('.btn-cart-delete').forEach(function (btn) {
            btn.addEventListener('click', function () {
                openCartDeleteConfirm(btn.dataset.id);
            });
        });

        syncCartSelectAll();
        updateCartBulkBar();
    }

    /* ─── Selezione multipla carrelli ──────────────────────────────────────── */

    function clearCartSelection() {
        state.cart.selected.clear();
        var selectAll = $('carts-select-all');
        if (selectAll) {
            selectAll.checked = false;
            selectAll.indeterminate = false;
        }
        updateCartBulkBar();
    }

    function syncCartSelectAll() {
        var selectAll = $('carts-select-all');
        if (!selectAll) return;
        var boxes = $('adm-cart-tbody')
            ? Array.prototype.slice.call($('adm-cart-tbody').querySelectorAll('.adm-cart-row-check'))
            : [];
        if (!boxes.length) {
            selectAll.checked = false;
            selectAll.indeterminate = false;
            return;
        }
        var nChecked = boxes.filter(function (b) { return b.checked; }).length;
        selectAll.checked = nChecked === boxes.length;
        selectAll.indeterminate = nChecked > 0 && nChecked < boxes.length;
    }

    function updateCartBulkBar() {
        var bar = $('adm-cart-bulk-bar');
        if (!bar) return;
        var n = state.cart.selected.size;
        if (n === 0) {
            bar.hidden = true;
            return;
        }
        bar.hidden = false;
        var countEl = $('adm-cart-bulk-count');
        if (countEl) countEl.textContent = n + (n === 1 ? ' selezionato' : ' selezionati');
        var btnDel = $('btn-cart-bulk-delete');
        if (btnDel) btnDel.hidden = !state.cart.capabilities.deleteCarts;
    }

    function selectedCartIds() {
        var out = [];
        state.cart.selected.forEach(function (id) { out.push(id); });
        return out;
    }

    function statRow(label, value) {
        // esc() tratta 0 come falsy (0 || '' → ''): i numeri vanno convertiti a parte,
        // altrimenti i contatori a zero (es. "Abbandonati: 0") sparirebbero dalla vista.
        var v = (typeof value === 'number') ? String(value) : esc(value);
        return '<div class="adm-stat-row"><span>' + esc(label) + '</span><strong>' + v + '</strong></div>';
    }

    function pct(n) { return (Math.round((n || 0) * 1000) / 10) + '%'; }

    function renderCartStats(stats) {
        var el = $('adm-cart-stats');
        if (!el) return;

        var days  = stats.days || 30;
        var hours = Number(stats.hoursIdle) || state.cart.effectiveHoursIdle;
        var periodo = days > 0 ? 'creati negli ultimi ' + days + ' gg' : 'tutti i carrelli';

        // I tassi hanno per denominatore "Con contenuto": dirlo evita che vengano
        // letti sul totale delle righe, svuotati compresi.
        var html = '<p class="adm-filter-section__title">Statistiche</p>'
            + '<p class="adm-stat-note">Coorte: ' + esc(periodo) + '.<br>'
            + 'Abbandonato = fermo da oltre ' + hours + (hours === 1 ? ' ora' : ' ore') + '.</p>'
            + statRow('Con contenuto',             stats.created || 0)
            + statRow('Svuotati',                  stats.emptied || 0)
            + statRow('Attivi',                    stats.active || 0)
            + statRow('Abbandonati',               stats.abandoned || 0)
            + statRow('Tasso abbandono',           pct(stats.abandonmentRate))
            + statRow('Checkout avviati',          stats.checkoutStarted || 0)
            + statRow('Tasso carrello → checkout', pct(stats.cartToCheckoutRate))
            + statRow('Ordini pagati',             stats.paid || 0)
            + statRow('Tasso carrello → pagato',   pct(stats.cartToPaidRate))
            + statRow('Valore abbandonato',        fmtMoney(stats.abandonedValueMinor, 'EUR'))
            + statRow('Valore medio',              fmtMoney(stats.abandonedAvgValueMinor, 'EUR'));

        if ((stats.topProducts || []).length) {
            html += '<p class="adm-filter-section__title" style="margin-top:1rem">Top prodotti abbandonati</p>'
                + stats.topProducts.map(function (p) { return statRow(p.name || p.sku, p.carts); }).join('');
        }
        if ((stats.topCountries || []).length) {
            html += '<p class="adm-filter-section__title" style="margin-top:1rem">Top paesi</p>'
                + stats.topCountries.map(function (c) { return statRow(c.country, c.carts); }).join('');
        }

        el.innerHTML = html;
    }

    function renderCartPagination() {
        var totalPages = Math.ceil(state.cart.total / state.cart.pageSize) || 1;
        var el = $('adm-cart-pagination');
        if (!el) return;

        if (totalPages <= 1) { el.innerHTML = ''; return; }

        var html = '<button class="adm-page-btn" id="cart-pg-prev" '
            + (state.cart.page <= 1 ? 'disabled' : '') + '>‹</button>';

        var start = Math.max(1, state.cart.page - 2);
        var end   = Math.min(totalPages, start + 4);
        start     = Math.max(1, end - 4);

        for (var p = start; p <= end; p++) {
            html += '<button class="adm-page-btn' + (p === state.cart.page ? ' adm-page-btn--active' : '')
                + '" data-cart-page="' + p + '">' + p + '</button>';
        }

        html += '<button class="adm-page-btn" id="cart-pg-next" '
            + (state.cart.page >= totalPages ? 'disabled' : '') + '>›</button>';

        el.innerHTML = html;

        el.querySelector('#cart-pg-prev').addEventListener('click', function () {
            if (state.cart.page > 1) { state.cart.page--; loadCarts(); }
        });
        el.querySelector('#cart-pg-next').addEventListener('click', function () {
            if (state.cart.page < totalPages) { state.cart.page++; loadCarts(); }
        });
        el.querySelectorAll('[data-cart-page]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                state.cart.page = Number(btn.dataset.cartPage);
                loadCarts();
            });
        });
    }

    function applyCartFilters() {
        var statusSel  = $('cart-filter-status');
        var daysSel    = $('cart-filter-days');
        var emailSel   = $('cart-filter-email');
        var countryInp = $('cart-filter-country');

        var hoursSel = $('cart-filter-hours');

        state.cart.status    = statusSel  ? statusSel.value  : 'abandoned';
        state.cart.days      = daysSel    ? daysSel.value    : '30';
        state.cart.hoursIdle = hoursSel   ? hoursSel.value   : '2';
        state.cart.hasEmail  = emailSel   ? emailSel.value   : '';
        state.cart.country   = countryInp ? countryInp.value.trim().toUpperCase() : '';
        state.cart.page      = 1;
        loadCarts();
    }

    function initCartEvents() {
        var btnSearch = $('btn-cart-search');
        if (btnSearch) btnSearch.addEventListener('click', applyCartFilters);

        var countryInput = $('cart-filter-country');
        if (countryInput) {
            countryInput.addEventListener('input', function () {
                countryInput.value = countryInput.value.toUpperCase();
            });
            countryInput.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') applyCartFilters();
            });
        }

        var selectAll = $('carts-select-all');
        if (selectAll) {
            selectAll.addEventListener('change', function () {
                var boxes = $('adm-cart-tbody')
                    ? Array.prototype.slice.call($('adm-cart-tbody').querySelectorAll('.adm-cart-row-check'))
                    : [];
                boxes.forEach(function (cb) {
                    cb.checked = selectAll.checked;
                    if (selectAll.checked) state.cart.selected.add(cb.dataset.id);
                    else state.cart.selected.delete(cb.dataset.id);
                });
                selectAll.indeterminate = false;
                updateCartBulkBar();
            });
        }

        var btnCartBulkDelete = $('btn-cart-bulk-delete');
        if (btnCartBulkDelete) {
            btnCartBulkDelete.addEventListener('click', function () {
                var ids = selectedCartIds();
                if (!ids.length) return;
                if (!state.cart.capabilities.deleteCarts) {
                    toast('Eliminazione disattivata da configurazione.', 'error');
                    return;
                }
                openCartBulkDeleteConfirm(ids);
            });
        }

        var btnCartBulkClear = $('btn-cart-bulk-clear');
        if (btnCartBulkClear) {
            btnCartBulkClear.addEventListener('click', function () {
                clearCartSelection();
                var boxes = $('adm-cart-tbody')
                    ? Array.prototype.slice.call($('adm-cart-tbody').querySelectorAll('.adm-cart-row-check'))
                    : [];
                boxes.forEach(function (cb) { cb.checked = false; });
            });
        }
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

        document.querySelectorAll('[data-adm-view]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                setView(btn.getAttribute('data-adm-view'));
            });
        });
        var stockReload = $('btn-stock-reload');
        if (stockReload) stockReload.addEventListener('click', loadStock);
        var stockTbody = $('adm-stock-tbody');
        if (stockTbody) {
            stockTbody.addEventListener('click', function (e) {
                var btn = e.target && e.target.closest ? e.target.closest('[data-stock-save]') : null;
                if (btn) saveStock(btn.getAttribute('data-stock-save'));
            });
            stockTbody.addEventListener('keydown', function (e) {
                if (e.key !== 'Enter') return;
                var inp = e.target;
                if (!inp || !inp.getAttribute || !inp.getAttribute('data-stock-qty')) return;
                e.preventDefault();
                saveStock(inp.getAttribute('data-stock-qty'));
            });
        }
        initCartEvents();

        setView((window.location.hash || '').slice(1));
    }

    // Espone reload per il pulsante "Riprova"
    window.adminApp = {
        reload: function () {
            if (state.view === 'stock')          loadStock();
            else if (state.view === 'carts')     loadCarts();
            else if (state.view === 'analytics') loadAnalytics();
            else                                   loadOrders();
        },
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
