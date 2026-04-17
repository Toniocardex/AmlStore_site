/**
 * checkout-success.js — logica thank-you page Aml Store.
 *
 * Flusso:
 *   1. Legge ?oid, ?exp, ?t dall'URL.
 *   2. Controlla scadenza token lato client (exp).
 *   3. Chiama GET /api/order-status per verifica server-side.
 *   4. Se status = pending_payment + metodo != bank_transfer → polling (Stripe race).
 *   5. Renderizza dettagli ordine oppure messaggio di errore/scadenza.
 *   6. Pulisce il carrello localStorage.
 */
(function (global) {
    'use strict';

    var ORDER_STATUS_URL  = '/api/order-status';
    var POLL_ATTEMPTS     = 4;
    var POLL_DELAY_MS     = 3000;

    /* ─── Stringhe UI per locale ───────────────────────────────────────────── */

    var UI = {
        it: {
            loading:        'Caricamento ordine…',
            order_id:       'N° ordine',
            date:           'Data',
            payment:        'Pagamento',
            product:        'Prodotto',
            qty:            'Qtà',
            subtotal:       'Subtotale',
            total:          'Totale',
            method_stripe:  'Carta di credito',
            method_paypal:  'PayPal',
            method_transfer:'Bonifico bancario',
            transfer_wait:  'In attesa di pagamento',
            paid:           'Pagato',
            causale_label:  'Causale da usare per il bonifico',
            expired_title:  'Link scaduto',
            expired_msg:    'Questo link di conferma è scaduto (30 minuti). Controlla la tua email per i dettagli dell\'ordine.',
            error_title:    'Ordine non trovato',
            error_msg:      'Non è stato possibile recuperare i dati dell\'ordine. Contatta il supporto: Info@amlstore.it',
            shop_btn:       'Torna al negozio',
        },
        en: {
            loading:        'Loading order…',
            order_id:       'Order no.',
            date:           'Date',
            payment:        'Payment',
            product:        'Product',
            qty:            'Qty',
            subtotal:       'Subtotal',
            total:          'Total',
            method_stripe:  'Credit card',
            method_paypal:  'PayPal',
            method_transfer:'Bank transfer',
            transfer_wait:  'Awaiting payment',
            paid:           'Paid',
            causale_label:  'Bank transfer reference',
            expired_title:  'Link expired',
            expired_msg:    'This confirmation link has expired (30 minutes). Check your email for order details.',
            error_title:    'Order not found',
            error_msg:      'We could not retrieve your order. Please contact support: Info@amlstore.it',
            shop_btn:       'Back to store',
        },
        fr: {
            loading:        'Chargement de la commande…',
            order_id:       'N° commande',
            date:           'Date',
            payment:        'Paiement',
            product:        'Produit',
            qty:            'Qté',
            subtotal:       'Sous-total',
            total:          'Total',
            method_stripe:  'Carte bancaire',
            method_paypal:  'PayPal',
            method_transfer:'Virement bancaire',
            transfer_wait:  'En attente de paiement',
            paid:           'Payé',
            causale_label:  'Référence pour le virement',
            expired_title:  'Lien expiré',
            expired_msg:    'Ce lien de confirmation a expiré (30 minutes). Consultez votre email pour les détails.',
            error_title:    'Commande introuvable',
            error_msg:      'Impossible de récupérer votre commande. Contactez le support : Info@amlstore.it',
            shop_btn:       'Retour à la boutique',
        },
        de: {
            loading:        'Bestellung wird geladen…',
            order_id:       'Bestellnr.',
            date:           'Datum',
            payment:        'Zahlung',
            product:        'Produkt',
            qty:            'Menge',
            subtotal:       'Zwischensumme',
            total:          'Gesamt',
            method_stripe:  'Kreditkarte',
            method_paypal:  'PayPal',
            method_transfer:'Banküberweisung',
            transfer_wait:  'Zahlung ausstehend',
            paid:           'Bezahlt',
            causale_label:  'Verwendungszweck für die Überweisung',
            expired_title:  'Link abgelaufen',
            expired_msg:    'Dieser Bestätigungslink ist abgelaufen (30 Minuten). Prüfen Sie Ihre E-Mail.',
            error_title:    'Bestellung nicht gefunden',
            error_msg:      'Ihre Bestellung konnte nicht abgerufen werden. Kontaktieren Sie uns: Info@amlstore.it',
            shop_btn:       'Zum Shop',
        },
        es: {
            loading:        'Cargando pedido…',
            order_id:       'N.° de pedido',
            date:           'Fecha',
            payment:        'Pago',
            product:        'Producto',
            qty:            'Cant.',
            subtotal:       'Subtotal',
            total:          'Total',
            method_stripe:  'Tarjeta de crédito',
            method_paypal:  'PayPal',
            method_transfer:'Transferencia bancaria',
            transfer_wait:  'Pago pendiente',
            paid:           'Pagado',
            causale_label:  'Concepto para la transferencia',
            expired_title:  'Enlace caducado',
            expired_msg:    'Este enlace de confirmación ha caducado (30 minutos). Consulte su correo para los detalles.',
            error_title:    'Pedido no encontrado',
            error_msg:      'No se pudo recuperar su pedido. Contacte el soporte: Info@amlstore.it',
            shop_btn:       'Volver a la tienda',
        },
    };

    /* ─── Utility ──────────────────────────────────────────────────────────── */

    function getLang() {
        var htmlLang  = document.documentElement.lang || '';
        var match     = htmlLang.match(/^[a-z]{2}/i);
        if (match) return match[0].toLowerCase();
        var pathMatch = global.location.pathname.match(/^\/([a-z]{2})\//);
        return pathMatch ? pathMatch[1].toLowerCase() : 'it';
    }

    function t(key) {
        var lang = getLang();
        var dict = UI[lang] || UI.it;
        return dict[key] || key;
    }

    function formatMoney(minor, currency) {
        var cur = String(currency || 'EUR').toUpperCase();
        try {
            return new Intl.NumberFormat(getLang(), { style: 'currency', currency: cur }).format(minor / 100);
        } catch (_) {
            return '€ ' + (minor / 100).toFixed(2);
        }
    }

    function fmtDate(iso) {
        try {
            return new Date(iso).toLocaleString(getLang(), {
                day: '2-digit', month: 'long', year: 'numeric',
                hour: '2-digit', minute: '2-digit',
            });
        } catch (_) { return iso || ''; }
    }

    function esc(str) {
        return String(str || '')
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    /* ─── DOM helpers ──────────────────────────────────────────────────────── */

    var $ = function (id) { return document.getElementById(id); };

    function showEl(id) { var el = $(id); if (el) el.hidden = false; }
    function hideEl(id) { var el = $(id); if (el) el.hidden = true;  }
    function setText(id, val) { var el = $(id); if (el) el.textContent = val; }
    function setHtml(id, val) { var el = $(id); if (el) el.innerHTML  = val; }

    /* ─── Rendering ordine ─────────────────────────────────────────────────── */

    function renderOrder(order) {
        var isPaid  = order.status === 'paid';
        var isBT    = order.paymentMethod === 'bank_transfer';

        var methodLabel = {
            stripe:        t('method_stripe'),
            paypal:        t('method_paypal'),
            bank_transfer: t('method_transfer'),
        }[order.paymentMethod] || order.paymentMethod;

        // Titolo e sottotitolo dinamici
        setText('success-order-id', order.orderId);
        setText('success-date',     fmtDate(order.createdAt));
        setText('success-method',   methodLabel);
        setText('success-status-badge', isPaid ? t('paid') : t('transfer_wait'));

        // Classe badge
        var badge = $('success-status-badge');
        if (badge) {
            badge.className = 'success-badge ' + (isPaid ? 'success-badge--paid' : 'success-badge--pending');
        }

        // Righe prodotto
        var rows = (order.lineItems || []).map(function (item) {
            var qty      = item.qty || item.quantity || 1;
            var unit     = item.unit_amount_minor || item.unitAmount || 0;
            var subMinor = Math.round(unit) * qty;
            return '<tr>'
                + '<td class="success-td">' + esc(item.name || item.sku || '') + '</td>'
                + '<td class="success-td success-td--center">' + qty + '</td>'
                + '<td class="success-td success-td--right">' + formatMoney(subMinor, order.currency) + '</td>'
                + '</tr>';
        }).join('');

        setHtml('success-items-body', rows);
        setText('success-total', formatMoney(order.totalMinor, order.currency));

        // Causale bonifico
        if (isBT && order.causale) {
            setText('success-causale', order.causale);
            showEl('success-transfer-box');
        } else {
            hideEl('success-transfer-box');
        }

        hideEl('success-loading');
        hideEl('success-error');
        showEl('success-details');
    }

    /* ─── Errore / scadenza ────────────────────────────────────────────────── */

    function showError(reason) {
        var isExpired = reason === 'expired' || reason === 'missing_params';
        setText('success-error-title', t(isExpired ? 'expired_title' : 'error_title'));
        setText('success-error-msg',   t(isExpired ? 'expired_msg'   : 'error_msg'));
        hideEl('success-loading');
        hideEl('success-details');
        showEl('success-error');
    }

    /* ─── Polling per race condition Stripe ────────────────────────────────── */

    function pollStatus(oid, exp, token, attempt) {
        if (attempt >= POLL_ATTEMPTS) {
            // Timeout polling: mostra comunque i dati (potrebbe essere pending_payment bonifico)
            return fetchStatus(oid, exp, token).then(renderOrder).catch(function () {
                showError('error');
            });
        }

        setTimeout(function () {
            fetchStatus(oid, exp, token).then(function (order) {
                if (order.status === 'pending_payment' && order.paymentMethod !== 'bank_transfer') {
                    pollStatus(oid, exp, token, attempt + 1);
                } else {
                    renderOrder(order);
                }
            }).catch(function () {
                showError('error');
            });
        }, POLL_DELAY_MS);
    }

    /* ─── Fetch order status ───────────────────────────────────────────────── */

    function fetchStatus(oid, exp, token) {
        var url = ORDER_STATUS_URL
            + '?oid=' + encodeURIComponent(oid)
            + '&exp=' + encodeURIComponent(exp)
            + '&t='   + encodeURIComponent(token);

        return fetch(url).then(function (res) {
            if (res.status === 410) throw { reason: 'expired' };
            if (res.status === 401) throw { reason: 'invalid_token' };
            if (!res.ok)            throw { reason: 'error' };
            return res.json();
        });
    }

    /* ─── Init ─────────────────────────────────────────────────────────────── */

    function init() {
        var params = new URLSearchParams(global.location.search);
        var oid    = params.get('oid');
        var exp    = params.get('exp');
        var token  = params.get('t');

        // Loading state iniziale
        setText('success-loading-msg', t('loading'));
        showEl('success-loading');
        hideEl('success-details');
        hideEl('success-error');

        // Controllo scadenza lato client (fast path — evita round-trip)
        if (!oid || !exp || !token) {
            showError('missing_params');
            return;
        }
        if (Number(exp) < Math.floor(Date.now() / 1000)) {
            showError('expired');
            return;
        }

        // Fetch server-side
        fetchStatus(oid, exp, token).then(function (order) {
            // Se Stripe e non ancora paid → polling breve (race condition webhook)
            if (order.status === 'pending_payment' && order.paymentMethod === 'stripe') {
                pollStatus(oid, exp, token, 0);
            } else {
                renderOrder(order);
            }

            // Pulisce il carrello solo se ordine trovato (qualunque status)
            if (global.AmlCart && global.AmlCart.clear) {
                global.AmlCart.clear();
            }

        }).catch(function (errObj) {
            showError(errObj && errObj.reason ? errObj.reason : 'error');
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})(typeof window !== 'undefined' ? window : globalThis);
