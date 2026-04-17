/**
 * checkout.js — logica pagina checkout Aml Store.
 * IIFE, 'use strict', ES6 vanilla, nessun framework.
 */
(function (global) {
    'use strict';

    /* ─── Costanti ─────────────────────────────────────────────────────────── */

    /** Endpoint Cloudflare Worker Stripe (non ancora implementato). */
    const STRIPE_WORKER_URL = '/api/create-checkout-session';

    /** Endpoint Cloudflare Worker PayPal (non ancora implementato). */
    const PAYPAL_WORKER_CREATE  = '/api/paypal-create-order';
    const PAYPAL_WORKER_CAPTURE = '/api/paypal-capture-order';

    /** PayPal Client ID — sandbox. Sostituire con ID live prima del deploy. */
    const PAYPAL_CLIENT_ID = 'AaY8zQfK-vpfHUqIc9TKbVppU7-UbPkBGPy0Pop5xXr3tQXrfDCZiT9_39YhqgPzPGq2gOPcEC1-ZOHa';

    /** Mappa lingua → locale PayPal SDK */
    const PAYPAL_LOCALE_MAP = {
        it: 'it_IT',
        en: 'en_US',
        fr: 'fr_FR',
        de: 'de_DE',
        es: 'es_ES',
    };

    /** Lingue supportate → path carrello fallback */
    const CART_PATHS = {
        it: '/it/cart.html',
        en: '/en/cart.html',
        fr: '/fr/cart.html',
        de: '/de/cart.html',
        es: '/es/cart.html',
    };

    /* ─── Stato PayPal SDK ─────────────────────────────────────────────────── */

    var _ppSdkLoaded   = false;
    var _ppSdkLoading  = false;
    var _ppSdkQueue    = []; // { resolve, reject }[]

    /* ─── Utility ──────────────────────────────────────────────────────────── */

    function getLang() {
        const htmlLang = document.documentElement.lang || '';
        const match = htmlLang.match(/^[a-z]{2}/i);
        if (match) return match[0].toLowerCase();
        const pathMatch = global.location.pathname.match(/^\/([a-z]{2})\//);
        return pathMatch ? pathMatch[1].toLowerCase() : 'it';
    }

    function formatMoney(minor, currency) {
        const cur = String(currency || 'eur').toUpperCase();
        try {
            return new Intl.NumberFormat(getLang(), { style: 'currency', currency: cur }).format(minor / 100);
        } catch (_) {
            return '€ ' + (minor / 100).toFixed(2);
        }
    }

    function generateOrderId() {
        const rand = Math.random().toString(36).slice(2, 6).toUpperCase();
        return 'AML-' + Date.now() + '-' + rand;
    }

    /* ─── Validazione ──────────────────────────────────────────────────────── */

    function validatePIVA(v) {
        if (!/^\d{11}$/.test(v)) return false;
        var s = 0;
        for (var i = 0; i <= 9; i += 2) { s += parseInt(v[i], 10); }
        for (var i = 1; i <= 9; i += 2) {
            var d = parseInt(v[i], 10) * 2;
            s += d > 9 ? d - 9 : d;
        }
        return (10 - (s % 10)) % 10 === parseInt(v[10], 10);
    }

    function validateSDI(v) {
        return /^[A-Z0-9]{7}$/i.test(v);
    }

    function validateEmail(v) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
    }

    /* ─── Gestione errori inline ───────────────────────────────────────────── */

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

    function clearFieldError(field) {
        field.classList.remove('is-invalid');
        var err = field.querySelector('.field-error');
        if (err) err.remove();
    }

    function clearErrors() {
        document.querySelectorAll('.form-field.is-invalid').forEach(function (f) { clearFieldError(f); });
    }

    function showGlobalError(msg) {
        var el = document.getElementById('checkout-error-msg');
        if (!el) return;
        el.textContent = msg;
        el.hidden = false;
    }

    function hideGlobalError() {
        var el = document.getElementById('checkout-error-msg');
        if (el) el.hidden = true;
    }

    /* ─── Tabs tipo cliente ────────────────────────────────────────────────── */

    function initCustomerTabs() {
        var tablist = document.querySelector('[role="tablist"].customer-tabs');
        if (!tablist) return;

        var tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));
        var panels = tabs.map(function (tab) {
            return document.getElementById(tab.getAttribute('aria-controls'));
        });

        var businessRequiredIds = ['field-ragione-sociale', 'field-piva'];

        function setBusinessRequired(isCompany) {
            businessRequiredIds.forEach(function (id) {
                var input = document.getElementById(id);
                if (input) {
                    if (isCompany) input.setAttribute('required', '');
                    else input.removeAttribute('required');
                }
            });
        }

        function activateTab(index) {
            tabs.forEach(function (tab, i) {
                tab.setAttribute('aria-selected', String(i === index));
                tab.setAttribute('tabindex', i === index ? '0' : '-1');
            });
            panels.forEach(function (panel, i) {
                if (panel) panel.hidden = i !== index;
            });
            var isCompany = tabs[index] && tabs[index].dataset.customerType === 'business';
            setBusinessRequired(isCompany);
        }

        tabs.forEach(function (tab, i) {
            tab.addEventListener('click', function () { activateTab(i); clearErrors(); });
            tab.addEventListener('keydown', function (e) {
                var idx = i;
                if (e.key === 'ArrowRight' || e.key === 'ArrowDown')       idx = (i + 1) % tabs.length;
                else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp')     idx = (i - 1 + tabs.length) % tabs.length;
                else if (e.key === 'Home')  idx = 0;
                else if (e.key === 'End')   idx = tabs.length - 1;
                else return;
                e.preventDefault();
                activateTab(idx);
                tabs[idx].focus();
            });
        });

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

    /* ─── Raccolta dati form ───────────────────────────────────────────────── */

    function collectFormData() {
        var activeTab = document.querySelector('[role="tab"][aria-selected="true"]');
        var isCompany = activeTab && activeTab.dataset.customerType === 'business';
        var sfx = isCompany ? '-b' : '';

        var data = {
            type: isCompany ? 'business' : 'private',
            firstName: (document.getElementById('field-first-name' + sfx) || {}).value || '',
            lastName:  (document.getElementById('field-last-name' + sfx)  || {}).value || '',
            email:     (document.getElementById('field-email' + sfx)       || {}).value || '',
            phone:     (document.getElementById('field-phone' + sfx)       || {}).value || '',
        };

        if (isCompany) {
            data.ragioneSociale = (document.getElementById('field-ragione-sociale') || {}).value || '';
            data.piva = (document.getElementById('field-piva') || {}).value || '';
            data.sdi  = (document.getElementById('field-sdi')  || {}).value || '';
            data.pec  = (document.getElementById('field-pec')  || {}).value || '';
        }

        return data;
    }

    /* ─── Validazione form ─────────────────────────────────────────────────── */

    function getErrorMessages() {
        var form = document.getElementById('checkout-form');
        if (!form) return {};
        try {
            return JSON.parse(form.getAttribute('data-errors') || '{}');
        } catch (_) { return {}; }
    }

    function validateForm() {
        clearErrors();
        var msgs = getErrorMessages();
        var valid = true;
        var firstInvalid = null;

        function fail(fieldEl, msg) {
            var wrapper = fieldEl.closest('.form-field');
            if (wrapper) showFieldError(wrapper, msg);
            if (!firstInvalid) firstInvalid = fieldEl;
            valid = false;
        }

        var activeTab = document.querySelector('[role="tab"][aria-selected="true"]');
        var isCompany = activeTab && activeTab.dataset.customerType === 'business';
        var sfx = isCompany ? '-b' : '';

        var firstName = document.getElementById('field-first-name' + sfx);
        var lastName  = document.getElementById('field-last-name' + sfx);
        var email     = document.getElementById('field-email' + sfx);
        var phone     = document.getElementById('field-phone' + sfx);

        if (firstName && !firstName.value.trim()) fail(firstName, msgs.required || 'Campo obbligatorio');
        if (lastName  && !lastName.value.trim())  fail(lastName,  msgs.required || 'Campo obbligatorio');
        if (email) {
            if (!email.value.trim())                     fail(email, msgs.required   || 'Campo obbligatorio');
            else if (!validateEmail(email.value.trim())) fail(email, msgs.emailInvalid || 'Indirizzo email non valido');
        }
        if (phone && phone.value.trim() && phone.value.trim().length < 7) {
            fail(phone, msgs.phoneInvalid || 'Numero di telefono non valido');
        }

        if (isCompany) {
            var ragioneSociale = document.getElementById('field-ragione-sociale');
            var piva = document.getElementById('field-piva');
            var sdi  = document.getElementById('field-sdi');
            var pec  = document.getElementById('field-pec');

            if (ragioneSociale && !ragioneSociale.value.trim()) fail(ragioneSociale, msgs.required || 'Campo obbligatorio');
            if (piva) {
                if (!piva.value.trim())               fail(piva, msgs.required   || 'Campo obbligatorio');
                else if (!validatePIVA(piva.value.trim())) fail(piva, msgs.pivaInvalid || 'Partita IVA non valida');
            }

            var sdiVal = sdi ? sdi.value.trim() : '';
            var pecVal = pec ? pec.value.trim() : '';
            if (!sdiVal && !pecVal) {
                if (sdi) {
                    var sdiWrapper = sdi.closest('.form-field');
                    if (sdiWrapper) showFieldError(sdiWrapper, msgs.sdiOrPecRequired || 'Inserire Codice SDI o PEC');
                }
                valid = false;
            } else {
                if (sdiVal && !validateSDI(sdiVal)) fail(sdi, msgs.sdiInvalid || 'Codice SDI non valido (7 caratteri alfanumerici)');
                if (pecVal && !validateEmail(pecVal)) fail(pec, msgs.emailInvalid || 'Indirizzo PEC non valido');
            }
        }

        if (firstInvalid) setTimeout(function () { firstInvalid.focus(); }, 0);
        return valid;
    }

    /* ─── Metodi di pagamento — visibilità ────────────────────────────────── */

    function initPaymentMethod() {
        var radios          = document.querySelectorAll('input[name="payment-method"]');
        var stripeSection   = document.getElementById('stripe-section');
        var transferSection = document.getElementById('transfer-section');
        var paypalSection   = document.getElementById('paypal-section');
        var btnStripe       = document.getElementById('btn-stripe-submit');
        var btnTransfer     = document.getElementById('btn-transfer-submit');

        function updateVisibility() {
            var selected = document.querySelector('input[name="payment-method"]:checked');
            if (!selected) return;
            var method = selected.value;

            // Sezioni contestuali
            if (stripeSection)   stripeSection.hidden   = method !== 'stripe';
            if (transferSection) transferSection.hidden  = method !== 'transfer';
            if (paypalSection)   paypalSection.hidden    = method !== 'paypal';

            // Bottoni custom (Stripe e Bonifico)
            // PayPal usa i bottoni del SDK — i bottoni custom vengono nascosti
            if (btnStripe)   btnStripe.style.display   = method === 'stripe'   ? '' : 'none';
            if (btnTransfer) btnTransfer.style.display  = method === 'transfer' ? '' : 'none';

            // Carica il SDK PayPal in lazy quando l'utente seleziona PayPal
            if (method === 'paypal') initPaypalButtons();
        }

        radios.forEach(function (r) { r.addEventListener('change', updateVisibility); });
        updateVisibility();
    }

    /* ─── Riepilogo carrello ───────────────────────────────────────────────── */

    function renderCartSummary() {
        var cart = global.AmlCart;
        if (!cart) return;

        var lines    = cart.getItems  ? cart.getItems()  : [];
        var totalQty = cart.totalQty  ? cart.totalQty()  : 0;

        if (!lines.length || totalQty === 0) {
            var lang = getLang();
            global.location.href = CART_PATHS[lang] || CART_PATHS['it'];
            return;
        }

        var container = document.getElementById('checkout-items');
        if (!container) return;
        container.textContent = '';

        var currency = (lines[0] && lines[0].currency) || 'eur';

        lines.forEach(function (line) {
            var qty       = Number(line.quantity) || 0;
            var lineMinor = Math.round(Number(line.unitAmount) || 0) * qty;

            var item  = document.createElement('div');  item.className  = 'checkout-item';
            var info  = document.createElement('div');  info.className  = 'checkout-item-info';
            var name  = document.createElement('div');  name.className  = 'checkout-item-name';
            var qtyEl = document.createElement('div');  qtyEl.className = 'checkout-item-qty';
            var price = document.createElement('div');  price.className = 'checkout-item-price';

            name.textContent  = line.name || line.sku;
            qtyEl.textContent = (container.getAttribute('data-qty-label') || 'Qtà') + ': ' + qty;
            price.textContent = formatMoney(lineMinor, currency);

            info.appendChild(name);
            info.appendChild(qtyEl);
            item.appendChild(info);
            item.appendChild(price);
            container.appendChild(item);
        });

        var minor    = cart.totalMinor ? cart.totalMinor() : 0;
        var totalEl  = document.getElementById('checkout-grand-total');
        var subEl    = document.getElementById('checkout-subtotal');
        var tAmount  = document.getElementById('transfer-amount');

        if (totalEl) totalEl.textContent = formatMoney(minor, currency);
        if (subEl)   subEl.textContent   = formatMoney(minor, currency);
        if (tAmount) tAmount.textContent = formatMoney(minor, currency);

        var emptySection    = document.getElementById('checkout-empty-section');
        var checkoutContent = document.getElementById('checkout-content');
        if (emptySection)    emptySection.hidden    = true;
        if (checkoutContent) checkoutContent.hidden = false;
    }

    /* ─── Toggle riepilogo mobile ──────────────────────────────────────────── */

    function initSummaryToggle() {
        var btn  = document.getElementById('summary-toggle-btn');
        var body = document.getElementById('checkout-summary-body');
        if (!btn || !body) return;
        btn.addEventListener('click', function () {
            var expanded = btn.getAttribute('aria-expanded') === 'true';
            btn.setAttribute('aria-expanded', String(!expanded));
            body.hidden = expanded;
        });
    }

    /* ─── Flusso Stripe ────────────────────────────────────────────────────── */

    function handleStripeSubmit(e) {
        e.preventDefault();
        if (!validateForm()) return;

        var btn     = document.getElementById('btn-stripe-submit');
        var customer = collectFormData();
        var cart    = global.AmlCart;
        var items   = cart && cart.getItems ? cart.getItems() : [];
        var lang    = getLang();

        var payload = {
            customer: customer,
            items: items,
            lang: lang,
            metadata: { skus: items.map(function (i) { return i.sku; }).join(','), lang: lang },
        };

        // [DEV] mostra payload — rimuovere quando il Worker è attivo
        console.log('[DEV] Checkout payload Stripe:', payload);
        alert('[DEV] Dati → Worker Stripe:\n' + JSON.stringify(payload, null, 2));

        /* --- Produzione (decommentare con Worker attivo) ---
        if (btn) { btn.setAttribute('aria-busy', 'true'); btn.disabled = true; }
        hideGlobalError();

        fetch(STRIPE_WORKER_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        })
        .then(function (res) { if (!res.ok) throw new Error('HTTP ' + res.status); return res.json(); })
        .then(function (data) {
            if (data && data.url) global.location.href = data.url;
            else throw new Error('Risposta Worker non valida');
        })
        .catch(function (err) {
            console.error('[Checkout] Stripe error:', err);
            var errorEl = document.getElementById('checkout-error-msg');
            showGlobalError(errorEl && errorEl.getAttribute('data-network-error') || 'Errore di connessione. Riprova.');
        })
        .finally(function () {
            if (btn) { btn.removeAttribute('aria-busy'); btn.disabled = false; }
        });
        --- */
    }

    /* ─── Flusso Bonifico ──────────────────────────────────────────────────── */

    function handleTransferSubmit(e) {
        e.preventDefault();
        if (!validateForm()) return;

        var orderId  = generateOrderId();
        var cart     = global.AmlCart;
        var items    = cart && cart.getItems  ? cart.getItems()  : [];
        var minor    = cart && cart.totalMinor ? cart.totalMinor() : 0;
        var currency = (items[0] && items[0].currency) || 'eur';
        var productNames = items.map(function (i) { return i.name || i.sku; }).join(', ');
        var causale  = orderId + ' ' + productNames;

        var confirmSection  = document.getElementById('transfer-confirm-section');
        var orderIdEl       = document.getElementById('confirm-order-id');
        var causaleEl       = document.getElementById('confirm-causale');
        var confirmAmountEl = document.getElementById('confirm-amount');
        var causaleDisplay  = document.getElementById('transfer-causale');

        if (orderIdEl)       orderIdEl.textContent       = orderId;
        if (causaleEl)       causaleEl.textContent        = causale;
        if (confirmAmountEl) confirmAmountEl.textContent  = formatMoney(minor, currency);
        if (causaleDisplay)  causaleDisplay.textContent   = causale;

        if (confirmSection) {
            confirmSection.hidden = false;
            confirmSection.setAttribute('tabindex', '-1');
            confirmSection.focus({ preventScroll: false });
            confirmSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    /* ─── PayPal SDK loader ────────────────────────────────────────────────── */

    /**
     * Carica il PayPal JS SDK in lazy (una sola volta per sessione).
     * Gestisce chiamate concorrenti accodandole.
     * @returns {Promise<void>}
     */
    function loadPaypalSDK() {
        return new Promise(function (resolve, reject) {
            if (_ppSdkLoaded && global.paypal) { resolve(); return; }
            if (_ppSdkLoading) { _ppSdkQueue.push({ resolve: resolve, reject: reject }); return; }

            _ppSdkLoading = true;
            var lang   = getLang();
            var locale = PAYPAL_LOCALE_MAP[lang] || 'it_IT';
            var src    = 'https://www.paypal.com/sdk/js'
                       + '?client-id='  + encodeURIComponent(PAYPAL_CLIENT_ID)
                       + '&currency=EUR&intent=capture'
                       + '&locale='     + locale
                       + '&components=buttons';

            var script = document.createElement('script');
            script.src = src;
            script.setAttribute('data-sdk-integration-source', 'amlstore');

            script.onload = function () {
                _ppSdkLoaded  = true;
                _ppSdkLoading = false;
                _ppSdkQueue.forEach(function (cb) { cb.resolve(); });
                _ppSdkQueue = [];
                resolve();
            };

            script.onerror = function () {
                _ppSdkLoading = false;
                var err = new Error('PayPal SDK load failed');
                _ppSdkQueue.forEach(function (cb) { cb.reject(err); });
                _ppSdkQueue = [];
                reject(err);
            };

            document.head.appendChild(script);
        });
    }

    /* ─── PayPal Buttons ───────────────────────────────────────────────────── */

    function initPaypalButtons() {
        var container  = document.getElementById('paypal-buttons-container');
        var loadingEl  = document.getElementById('paypal-loading');
        var errorEl    = document.getElementById('checkout-error-msg');

        if (!container) return;
        // Evita doppio render (es. utente seleziona PayPal due volte)
        if (container.dataset.ppRendered) return;

        if (loadingEl) loadingEl.hidden = false;
        hideGlobalError();

        loadPaypalSDK()
            .then(function () {
                if (loadingEl) loadingEl.hidden = true;

                container.dataset.ppRendered = '1';

                global.paypal.Buttons({
                    style: {
                        layout: 'vertical',
                        color:  'gold',
                        shape:  'pill',
                        label:  'paypal',
                        height: 48,
                    },

                    /**
                     * Crea l'ordine PayPal.
                     * Valida il form prima di procedere: se invalido lancia un errore
                     * che cancella il flusso PayPal senza mostrare UI di errore PayPal.
                     */
                    createOrder: function () {
                        if (!validateForm()) {
                            // Errore intenzionale — onError lo ignora
                            throw new Error('aml-validation');
                        }

                        var cart  = global.AmlCart;
                        var items = cart && cart.getItems  ? cart.getItems()  : [];
                        var minor = cart && cart.totalMinor ? cart.totalMinor() : 0;
                        var lang  = getLang();

                        var payload = {
                            customer: collectFormData(),
                            items:    items,
                            lang:     lang,
                            amount: {
                                value:         (minor / 100).toFixed(2),
                                currency_code: 'EUR',
                            },
                        };

                        // [DEV] mock — decommentare il fetch per produzione
                        console.log('[DEV] PayPal createOrder payload:', payload);
                        return Promise.resolve('MOCK-PP-' + Date.now());

                        /* --- Produzione ---
                        return fetch(PAYPAL_WORKER_CREATE, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload),
                        })
                        .then(function (res) {
                            if (!res.ok) throw new Error('HTTP ' + res.status);
                            return res.json();
                        })
                        .then(function (data) { return data.orderID; });
                        --- */
                    },

                    /**
                     * Utente ha approvato il pagamento su PayPal.
                     * In produzione: chiama il Worker di capture e reindirizza alla conferma.
                     */
                    onApprove: function (data) {
                        // [DEV]
                        console.log('[DEV] PayPal onApprove:', data);
                        alert('[DEV] Pagamento PayPal approvato!\nOrder ID: ' + data.orderID);

                        /* --- Produzione ---
                        return fetch(PAYPAL_WORKER_CAPTURE, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ orderID: data.orderID, customer: collectFormData() }),
                        })
                        .then(function (res) {
                            if (!res.ok) throw new Error('HTTP ' + res.status);
                            return res.json();
                        })
                        .then(function () {
                            var lang = getLang();
                            global.location.href = '/' + lang + '/checkout-success.html?order=' + data.orderID;
                        })
                        .catch(function (err) {
                            console.error('[PayPal] Capture error:', err);
                            showGlobalError('Errore nella conferma del pagamento PayPal. Contatta il supporto.');
                        });
                        --- */
                    },

                    /** Errori PayPal SDK — ignora errori di validazione lanciati da createOrder. */
                    onError: function (err) {
                        if (err && err.message === 'aml-validation') return;
                        console.error('[PayPal] SDK error:', err);
                        var netErr = errorEl && errorEl.getAttribute('data-network-error');
                        showGlobalError(netErr || 'Errore PayPal. Riprova o scegli un altro metodo di pagamento.');
                    },

                    onCancel: function () {
                        console.log('[PayPal] Pagamento annullato dall\'utente.');
                    },

                }).render('#paypal-buttons-container');
            })
            .catch(function (err) {
                console.error('[PayPal] Impossibile caricare SDK:', err);
                if (loadingEl) loadingEl.hidden = true;
                showGlobalError('Impossibile caricare PayPal. Controlla la connessione o scegli un altro metodo.');
            });
    }

    /* ─── Bind submit buttons ──────────────────────────────────────────────── */

    function initSubmitButtons() {
        var btnStripe   = document.getElementById('btn-stripe-submit');
        var btnTransfer = document.getElementById('btn-transfer-submit');
        var form        = document.getElementById('checkout-form');

        if (btnStripe)   btnStripe.addEventListener('click', handleStripeSubmit);
        if (btnTransfer) btnTransfer.addEventListener('click', handleTransferSubmit);
        if (form) form.addEventListener('submit', function (e) { e.preventDefault(); });
    }

    /* ─── Init principale ──────────────────────────────────────────────────── */

    function init() {
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
        initPaymentMethod();  // gestisce visibilità sezioni + bottoni + lazy PayPal
        initSummaryToggle();
        initSubmitButtons();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})(typeof window !== 'undefined' ? window : globalThis);
