/**
 * checkout.js — logica pagina checkout Aml Store.
 * IIFE, 'use strict', ES6 vanilla, nessun framework.
 */
(function (global) {
    'use strict';

    /* ─── Costanti ─────────────────────────────────────────────────────────── */

    /** Endpoint Cloudflare Worker (non ancora implementato). */
    const WORKER_URL = '/api/create-checkout-session';

    /** Lingue supportate → path carrello fallback */
    const CART_PATHS = {
        it: '/it/cart.html',
        en: '/en/cart.html',
        fr: '/fr/cart.html',
        de: '/de/cart.html',
        es: '/es/cart.html',
    };

    /* ─── Utility ──────────────────────────────────────────────────────────── */

    /**
     * Ottiene la lingua corrente dalla pagina o dal pathname.
     * @returns {string}
     */
    function getLang() {
        const htmlLang = document.documentElement.lang || '';
        const match = htmlLang.match(/^[a-z]{2}/i);
        if (match) return match[0].toLowerCase();
        const pathMatch = global.location.pathname.match(/^\/([a-z]{2})\//);
        return pathMatch ? pathMatch[1].toLowerCase() : 'it';
    }

    /**
     * Formatta centesimi come valuta.
     * @param {number} minor - importo in centesimi
     * @param {string} [currency='eur']
     * @returns {string}
     */
    function formatMoney(minor, currency) {
        const cur = String(currency || 'eur').toUpperCase();
        try {
            return new Intl.NumberFormat(getLang(), { style: 'currency', currency: cur }).format(minor / 100);
        } catch (_) {
            return '€ ' + (minor / 100).toFixed(2);
        }
    }

    /**
     * Genera un ID ordine univoco.
     * @returns {string}
     */
    function generateOrderId() {
        const rand = Math.random().toString(36).slice(2, 6).toUpperCase();
        return 'AML-' + Date.now() + '-' + rand;
    }

    /* ─── Validazione ──────────────────────────────────────────────────────── */

    /**
     * Valida Partita IVA italiana (11 cifre + checksum).
     * @param {string} v
     * @returns {boolean}
     */
    function validatePIVA(v) {
        if (!/^\d{11}$/.test(v)) return false;
        var s = 0;
        for (var i = 0; i <= 9; i += 2) {
            s += parseInt(v[i], 10);
        }
        for (var i = 1; i <= 9; i += 2) {
            var d = parseInt(v[i], 10) * 2;
            s += d > 9 ? d - 9 : d;
        }
        return (10 - (s % 10)) % 10 === parseInt(v[10], 10);
    }

    /**
     * Valida Codice SDI (7 caratteri alfanumerici).
     * @param {string} v
     * @returns {boolean}
     */
    function validateSDI(v) {
        return /^[A-Z0-9]{7}$/i.test(v);
    }

    /**
     * Validazione base dell'email (HTML5 pattern + struttura).
     * @param {string} v
     * @returns {boolean}
     */
    function validateEmail(v) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
    }

    /* ─── Gestione errori inline ───────────────────────────────────────────── */

    /**
     * Mostra errore inline su un campo.
     * @param {HTMLElement} field - elemento .form-field
     * @param {string} msg - messaggio di errore
     */
    function showFieldError(field, msg) {
        field.classList.add('is-invalid');
        var existing = field.querySelector('.field-error');
        if (existing) {
            existing.textContent = msg;
        } else {
            var err = document.createElement('p');
            err.className = 'field-error';
            err.setAttribute('role', 'alert');
            err.setAttribute('aria-live', 'polite');
            err.textContent = msg;
            field.appendChild(err);
        }
    }

    /**
     * Rimuove l'errore inline da un campo.
     * @param {HTMLElement} field
     */
    function clearFieldError(field) {
        field.classList.remove('is-invalid');
        var err = field.querySelector('.field-error');
        if (err) err.remove();
    }

    /**
     * Rimuove tutti gli errori dal form.
     */
    function clearErrors() {
        var fields = document.querySelectorAll('.form-field.is-invalid');
        fields.forEach(function (f) { clearFieldError(f); });
    }

    /* ─── Tabs tipo cliente ────────────────────────────────────────────────── */

    /**
     * Inizializza i tab privato/azienda con gestione ARIA e required dinamici.
     */
    function initCustomerTabs() {
        var tablist = document.querySelector('[role="tablist"].customer-tabs');
        if (!tablist) return;

        var tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));
        var panels = tabs.map(function (tab) {
            return document.getElementById(tab.getAttribute('aria-controls'));
        });

        /** Campi obbligatori solo per azienda */
        var businessRequiredIds = ['field-ragione-sociale', 'field-piva'];

        function setBusinessRequired(isCompany) {
            businessRequiredIds.forEach(function (id) {
                var input = document.getElementById(id);
                if (input) {
                    if (isCompany) {
                        input.setAttribute('required', '');
                    } else {
                        input.removeAttribute('required');
                    }
                }
            });
        }

        function activateTab(index) {
            tabs.forEach(function (tab, i) {
                var isSelected = i === index;
                tab.setAttribute('aria-selected', String(isSelected));
                tab.setAttribute('tabindex', isSelected ? '0' : '-1');
            });
            panels.forEach(function (panel, i) {
                if (!panel) return;
                panel.hidden = i !== index;
            });
            // Aggiorna required in base al tab attivo
            var isCompany = tabs[index] && tabs[index].dataset.customerType === 'business';
            setBusinessRequired(isCompany);
        }

        tabs.forEach(function (tab, i) {
            tab.addEventListener('click', function () {
                activateTab(i);
                clearErrors();
            });

            // Navigazione tastiera tablist
            tab.addEventListener('keydown', function (e) {
                var idx = i;
                if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
                    idx = (i + 1) % tabs.length;
                } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
                    idx = (i - 1 + tabs.length) % tabs.length;
                } else if (e.key === 'Home') {
                    idx = 0;
                } else if (e.key === 'End') {
                    idx = tabs.length - 1;
                } else {
                    return;
                }
                e.preventDefault();
                activateTab(idx);
                tabs[idx].focus();
            });
        });

        // Stato iniziale
        activateTab(0);
    }

    /* ─── Auto-uppercase SDI ───────────────────────────────────────────────── */

    function initSDIUppercase() {
        var sdiInput = document.getElementById('field-sdi');
        if (!sdiInput) return;
        sdiInput.addEventListener('input', function () {
            var pos = this.selectionStart;
            this.value = this.value.toUpperCase();
            try { this.setSelectionRange(pos, pos); } catch (_) {}
        });
    }

    /* ─── Metodi di pagamento ──────────────────────────────────────────────── */

    /**
     * Inizializza la selezione metodo pagamento e la visibilità delle sezioni.
     */
    function initPaymentMethod() {
        var radios = document.querySelectorAll('input[name="payment-method"]');
        var stripeSection = document.getElementById('stripe-section');
        var transferSection = document.getElementById('transfer-section');

        function updateVisibility() {
            var selected = document.querySelector('input[name="payment-method"]:checked');
            if (!selected) return;
            var method = selected.value;
            if (stripeSection) stripeSection.hidden = method !== 'stripe';
            if (transferSection) transferSection.hidden = method !== 'transfer';
        }

        radios.forEach(function (radio) {
            radio.addEventListener('change', updateVisibility);
        });

        updateVisibility();
    }

    /* ─── Riepilogo carrello ───────────────────────────────────────────────── */

    /**
     * Popola il riepilogo ordine leggendo AmlCart.
     * Se il carrello è vuoto, reindirizza alla pagina carrello.
     */
    function renderCartSummary() {
        var cart = global.AmlCart;
        if (!cart) return;

        var lines = cart.getItems ? cart.getItems() : [];
        var totalQty = cart.totalQty ? cart.totalQty() : 0;

        // Carrello vuoto → redirect
        if (!lines.length || totalQty === 0) {
            var lang = getLang();
            var cartPath = CART_PATHS[lang] || CART_PATHS['it'];
            global.location.href = cartPath;
            return;
        }

        var container = document.getElementById('checkout-items');
        if (!container) return;

        // Svuota con textContent (sicuro vs innerHTML)
        container.textContent = '';

        var currency = (lines[0] && lines[0].currency) || 'eur';

        lines.forEach(function (line) {
            var qty = Number(line.quantity) || 0;
            var lineMinor = Math.round(Number(line.unitAmount) || 0) * qty;

            var item = document.createElement('div');
            item.className = 'checkout-item';

            var info = document.createElement('div');
            info.className = 'checkout-item-info';

            var name = document.createElement('div');
            name.className = 'checkout-item-name';
            name.textContent = line.name || line.sku;

            var qtyEl = document.createElement('div');
            qtyEl.className = 'checkout-item-qty';
            // Il testo "Qtà:" è già nell'HTML come data-attr sull'item container
            var qtyLabel = container.getAttribute('data-qty-label') || 'Qtà';
            qtyEl.textContent = qtyLabel + ': ' + qty;

            info.appendChild(name);
            info.appendChild(qtyEl);

            var price = document.createElement('div');
            price.className = 'checkout-item-price';
            price.textContent = formatMoney(lineMinor, currency);

            item.appendChild(info);
            item.appendChild(price);
            container.appendChild(item);
        });

        // Totale
        var minor = cart.totalMinor ? cart.totalMinor() : 0;
        var totalEl = document.getElementById('checkout-grand-total');
        if (totalEl) totalEl.textContent = formatMoney(minor, currency);

        // Aggiorna importo nelle istruzioni bonifico (se visibile)
        var transferAmount = document.getElementById('transfer-amount');
        if (transferAmount) transferAmount.textContent = formatMoney(minor, currency);

        // Nascondi la sezione "carrello vuoto" e mostra il checkout
        var emptySection = document.getElementById('checkout-empty-section');
        var checkoutContent = document.getElementById('checkout-content');
        if (emptySection) emptySection.hidden = true;
        if (checkoutContent) checkoutContent.hidden = false;
    }

    /* ─── Toggle riepilogo mobile ──────────────────────────────────────────── */

    function initSummaryToggle() {
        var btn = document.getElementById('summary-toggle-btn');
        var body = document.getElementById('checkout-summary-body');
        if (!btn || !body) return;

        btn.addEventListener('click', function () {
            var expanded = btn.getAttribute('aria-expanded') === 'true';
            btn.setAttribute('aria-expanded', String(!expanded));
            body.hidden = expanded;
        });
    }

    /* ─── Validazione form ─────────────────────────────────────────────────── */

    /**
     * Legge i messaggi di errore localizzati dall'attributo data-errors del form.
     * @returns {Object}
     */
    function getErrorMessages() {
        var form = document.getElementById('checkout-form');
        if (!form) return {};
        try {
            var raw = form.getAttribute('data-errors') || '{}';
            return JSON.parse(raw);
        } catch (_) {
            return {};
        }
    }

    /**
     * Valida tutti i campi del form.
     * Applica .is-invalid e messaggi di errore inline.
     * @returns {boolean} true se il form è valido
     */
    function validateForm() {
        clearErrors();
        var msgs = getErrorMessages();
        var valid = true;

        function fail(fieldEl, msg) {
            var wrapper = fieldEl.closest('.form-field');
            if (wrapper) showFieldError(wrapper, msg);
            if (valid) {
                // Focus sul primo campo invalido
                setTimeout(function () { fieldEl.focus(); }, 0);
            }
            valid = false;
        }

        // Determina tipo cliente prima di accedere ai campi
        var activeTab = document.querySelector('[role="tab"][aria-selected="true"]');
        var isCompany = activeTab && activeTab.dataset.customerType === 'business';

        // ── Campi comuni (lettura dal panel attivo) ──
        var sfx = isCompany ? '-b' : '';
        var firstName = document.getElementById('field-first-name' + sfx);
        var lastName = document.getElementById('field-last-name' + sfx);
        var email = document.getElementById('field-email' + sfx);
        var phone = document.getElementById('field-phone' + sfx);

        if (firstName && !firstName.value.trim()) {
            fail(firstName, msgs.required || 'Campo obbligatorio');
        }
        if (lastName && !lastName.value.trim()) {
            fail(lastName, msgs.required || 'Campo obbligatorio');
        }
        if (email) {
            if (!email.value.trim()) {
                fail(email, msgs.required || 'Campo obbligatorio');
            } else if (!validateEmail(email.value.trim())) {
                fail(email, msgs.emailInvalid || 'Indirizzo email non valido');
            }
        }
        // Telefono: facoltativo, ma se compilato deve avere almeno 7 char
        if (phone && phone.value.trim() && phone.value.trim().length < 7) {
            fail(phone, msgs.phoneInvalid || 'Numero di telefono non valido');
        }

        // ── Campi aziendali (solo se tab azienda attivo) ──
        if (isCompany) {
            var ragioneSociale = document.getElementById('field-ragione-sociale');
            var piva = document.getElementById('field-piva');
            var sdi = document.getElementById('field-sdi');
            var pec = document.getElementById('field-pec');

            if (ragioneSociale && !ragioneSociale.value.trim()) {
                fail(ragioneSociale, msgs.required || 'Campo obbligatorio');
            }

            if (piva) {
                if (!piva.value.trim()) {
                    fail(piva, msgs.required || 'Campo obbligatorio');
                } else if (!validatePIVA(piva.value.trim())) {
                    fail(piva, msgs.pivaInvalid || 'Partita IVA non valida (11 cifre + checksum)');
                }
            }

            // Almeno uno tra SDI e PEC richiesto
            var sdiVal = sdi ? sdi.value.trim() : '';
            var pecVal = pec ? pec.value.trim() : '';

            if (!sdiVal && !pecVal) {
                if (sdi) {
                    var sdiWrapper = sdi.closest('.form-field');
                    if (sdiWrapper) showFieldError(sdiWrapper, msgs.sdiOrPecRequired || 'Inserire Codice SDI o PEC');
                }
                valid = false;
            } else {
                if (sdiVal && !validateSDI(sdiVal)) {
                    fail(sdi, msgs.sdiInvalid || 'Codice SDI non valido (7 caratteri alfanumerici)');
                }
                if (pecVal && !validateEmail(pecVal)) {
                    fail(pec, msgs.emailInvalid || 'Indirizzo PEC non valido');
                }
            }
        }

        return valid;
    }

    /* ─── Raccolta dati form ───────────────────────────────────────────────── */

    /**
     * Raccoglie i dati del form in un oggetto.
     * Legge dagli input del panel attivo.
     * @returns {Object}
     */
    function collectFormData() {
        var activeTab = document.querySelector('[role="tab"][aria-selected="true"]');
        var isCompany = activeTab && activeTab.dataset.customerType === 'business';

        // Suffisso per i campi del panel azienda
        var sfx = isCompany ? '-b' : '';

        var data = {
            type: isCompany ? 'business' : 'private',
            firstName: (document.getElementById('field-first-name' + sfx) || {}).value || '',
            lastName: (document.getElementById('field-last-name' + sfx) || {}).value || '',
            email: (document.getElementById('field-email' + sfx) || {}).value || '',
            phone: (document.getElementById('field-phone' + sfx) || {}).value || '',
        };

        if (isCompany) {
            data.ragioneSociale = (document.getElementById('field-ragione-sociale') || {}).value || '';
            data.piva = (document.getElementById('field-piva') || {}).value || '';
            data.sdi = (document.getElementById('field-sdi') || {}).value || '';
            data.pec = (document.getElementById('field-pec') || {}).value || '';
        }

        return data;
    }

    /* ─── Flusso Stripe ────────────────────────────────────────────────────── */

    /**
     * Gestisce il submit per il pagamento Stripe.
     * Chiama POST /api/create-checkout-session (Cloudflare Worker placeholder).
     * In DEV mostra alert con il payload.
     * @param {Event} e
     */
    function handleStripeSubmit(e) {
        e.preventDefault();
        if (!validateForm()) return;

        var btn = document.getElementById('btn-stripe-submit');
        var errorEl = document.getElementById('checkout-error-msg');

        var customer = collectFormData();
        var cart = global.AmlCart;
        var items = cart && cart.getItems ? cart.getItems() : [];
        var lang = getLang();

        var payload = {
            customer: customer,
            items: items,
            lang: lang,
            metadata: {
                skus: items.map(function (i) { return i.sku; }).join(','),
                lang: lang,
            },
        };

        // [DEV] Mostra il payload in console e alert (rimuovere quando il Worker è attivo)
        console.log('[DEV] Checkout payload Stripe:', payload);
        alert('[DEV] Dati che verrebbero inviati al Worker Stripe:\n' + JSON.stringify(payload, null, 2));

        /* --- Codice produzione (decommentare quando il Worker è pronto) ---
        if (btn) {
            btn.setAttribute('aria-busy', 'true');
            btn.disabled = true;
        }
        if (errorEl) errorEl.hidden = true;

        fetch(WORKER_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        })
        .then(function (res) {
            if (!res.ok) throw new Error('HTTP ' + res.status);
            return res.json();
        })
        .then(function (data) {
            if (data && data.url) {
                global.location.href = data.url;
            } else {
                throw new Error('Risposta Worker non valida');
            }
        })
        .catch(function (err) {
            console.error('[Checkout] Errore Stripe:', err);
            if (errorEl) {
                errorEl.textContent = errorEl.getAttribute('data-network-error') ||
                    'Errore di connessione. Riprova tra qualche istante.';
                errorEl.hidden = false;
            }
        })
        .finally(function () {
            if (btn) {
                btn.removeAttribute('aria-busy');
                btn.disabled = false;
            }
        });
        --- Fine codice produzione --- */
    }

    /* ─── Flusso Bonifico ──────────────────────────────────────────────────── */

    /**
     * Gestisce il submit per il bonifico bancario.
     * Genera orderId, popola la sezione istruzioni, la mostra con aria-live.
     * NON chiama API.
     * @param {Event} e
     */
    function handleTransferSubmit(e) {
        e.preventDefault();
        if (!validateForm()) return;

        var orderId = generateOrderId();
        var cart = global.AmlCart;
        var items = cart && cart.getItems ? cart.getItems() : [];
        var minor = cart && cart.totalMinor ? cart.totalMinor() : 0;
        var currency = (items[0] && items[0].currency) || 'eur';

        var productNames = items.map(function (i) { return i.name || i.sku; }).join(', ');
        var causale = orderId + ' ' + productNames;

        // Popola la sezione conferma
        var confirmSection = document.getElementById('transfer-confirm-section');
        var orderIdEl = document.getElementById('confirm-order-id');
        var causaleEl = document.getElementById('confirm-causale');
        var confirmAmountEl = document.getElementById('confirm-amount');

        if (orderIdEl) orderIdEl.textContent = orderId;
        if (causaleEl) causaleEl.textContent = causale;
        if (confirmAmountEl) confirmAmountEl.textContent = formatMoney(minor, currency);

        // Aggiorna causale nelle istruzioni bonifico già visibili
        var causaleDisplay = document.getElementById('transfer-causale');
        if (causaleDisplay) causaleDisplay.textContent = causale;

        // Mostra la sezione conferma
        if (confirmSection) {
            confirmSection.hidden = false;
            // Scroll verso la conferma con focus accessibile
            confirmSection.setAttribute('tabindex', '-1');
            confirmSection.focus({ preventScroll: false });
            confirmSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    /* ─── Bind submit buttons ──────────────────────────────────────────────── */

    function initSubmitButtons() {
        var btnStripe = document.getElementById('btn-stripe-submit');
        if (btnStripe) {
            btnStripe.addEventListener('click', handleStripeSubmit);
        }

        var btnTransfer = document.getElementById('btn-transfer-submit');
        if (btnTransfer) {
            btnTransfer.addEventListener('click', handleTransferSubmit);
        }

        // Previeni submit HTML5 nativo
        var form = document.getElementById('checkout-form');
        if (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
            });
        }
    }

    /* ─── Init principale ──────────────────────────────────────────────────── */

    function init() {
        // Il carrello potrebbe non essere ancora disponibile → aspettiamo l'evento
        if (global.AmlCart) {
            renderCartSummary();
        } else {
            document.addEventListener('aml-cart-changed', function onFirstCart() {
                document.removeEventListener('aml-cart-changed', onFirstCart);
                renderCartSummary();
            });
        }

        initCustomerTabs();
        initSDIUppercase();
        initPaymentMethod();
        initSummaryToggle();
        initSubmitButtons();
    }

    /* ─── Bootstrap ────────────────────────────────────────────────────────── */

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})(typeof window !== 'undefined' ? window : globalThis);
