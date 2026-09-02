/**
 * checkout.js — logica pagina checkout Eurolicenze.
 * IIFE, 'use strict', ES6 vanilla, nessun framework.
 */
(function (global) {
    'use strict';

    /* ─── Costanti ─────────────────────────────────────────────────────────── */

    const STRIPE_WORKER_URL      = '/api/stripe-create-session';
    const PAYPAL_WORKER_CREATE   = '/api/paypal-create-order';
    const PAYPAL_WORKER_CAPTURE  = '/api/paypal-capture-order';
    const TRANSFER_WORKER_URL    = '/api/bank-transfer-order';
    const PAYPAL_CONFIG_URL      = '/api/paypal-config';

    // Pilota IT: solo /it/checkout ha il markup on-page (#payment-element).
    // Le altre lingue restano sul flusso Stripe Checkout ospitato (redirect)
    // finché non vengono migrate. Un solo checkout.js serve entrambi.
    function isOnPageStripe() {
        return !!document.getElementById('payment-element');
    }

    const PAYPAL_LOCALE_MAP = {
        it: 'it_IT', en: 'en_US', fr: 'fr_FR', de: 'de_DE', es: 'es_ES', pt: 'pt_PT', nl: 'nl_NL',
    };

    const CART_PATHS = {
        it: '/it/cart', en: '/en/cart', fr: '/fr/cart',
        de: '/de/cart', es: '/es/cart', pt: '/pt/cart', nl: '/nl/cart',
    };

    /* Copertina di ripiego per le miniature del riepilogo: percorso assoluto
       perche' il checkout vive sotto /<lang>/ in tutte e sette le lingue. */
    const FALLBACK_THUMB = '/asset/media/product-cover-fallback.webp';

    /** Fa cadere una miniatura sulla copertina di ripiego se la sua non carica. */
    function bindThumbFallback(img) {
        img.addEventListener('error', function () {
            if (img.getAttribute('src') !== FALLBACK_THUMB) img.src = FALLBACK_THUMB;
        });
    }

    /* ─── Stato PayPal SDK ─────────────────────────────────────────────────── */

    var _ppSdkLoaded  = false;
    var _ppSdkLoading = false;
    var _ppSdkQueue   = [];

    /* ─── Stato Sottomissione ──────────────────────────────────────────────── */
    var _isSubmitting = false;

    /* ─── Stato Stripe Elements (flusso on-page) ───────────────────────────── */
    var STRIPE_CONFIG_URL          = '/api/stripe-config';
    var STRIPE_PI_URL              = '/api/create-payment-intent';
    var STRIPE_INTENT_RETURN_URL   = '/api/stripe-intent-return';

    var _stripe            = null;   // istanza Stripe(pk)
    var _stripeEnabled     = false;  // publishable key presente
    var _elementsManual    = null;   // elements() per il Payment Element (carta)
    var _paymentElement    = null;
    var _paymentElMounting = false;
    var _elementsExpress   = null;   // elements() per l'Express Checkout Element
    var _lastPiCustomerKey = '';     // per rimontare il PE se cambiano i dati cliente

    /* ─── Idempotency key ──────────────────────────────────────────────────── */
    // Chiave stabile per (sessione, metodo, carrello, email): un retry dello stesso
    // ordine riusa la stessa chiave (niente doppioni in D1), mentre un carrello o
    // una email diversi producono una chiave nuova. Il sale di sessione viene
    // ruotato a ordine completato (qui e in checkout-success.js).
    var SALT_STORAGE_KEY = 'aml-ikey-salt';

    function getSessionSalt() {
        var s = null;
        try { s = sessionStorage.getItem(SALT_STORAGE_KEY); } catch (_) {}
        if (!s) {
            var arr = new Uint32Array(2);
            crypto.getRandomValues(arr);
            s = arr[0].toString(36) + arr[1].toString(36);
            try { sessionStorage.setItem(SALT_STORAGE_KEY, s); } catch (_) {}
        }
        return s;
    }

    function rotateSessionSalt() {
        try {
            sessionStorage.removeItem(SALT_STORAGE_KEY);
            sessionStorage.removeItem('aml-transfer-ikey'); // legacy
        } catch (_) {}
    }

    function randomIdempotencyKey(prefix) {
        var arr = new Uint32Array(2);
        crypto.getRandomValues(arr);
        return prefix + '-' + Date.now() + '-' + arr[0].toString(36) + arr[1].toString(36);
    }

    /** @returns {Promise<string>} chiave deterministica; fallback random se manca crypto.subtle */
    function buildIdempotencyKey(prefix, items, email) {
        var basis;
        try {
            basis = JSON.stringify([getSessionSalt(), prefix, String(email || '').toLowerCase()]
                .concat(items.map(function (i) { return [i.sku, Number(i.quantity) || 1]; })));
        } catch (_) {
            return Promise.resolve(randomIdempotencyKey(prefix));
        }
        if (!(global.crypto && crypto.subtle && global.TextEncoder)) {
            return Promise.resolve(randomIdempotencyKey(prefix));
        }
        return crypto.subtle.digest('SHA-256', new TextEncoder().encode(basis))
            .then(function (buf) {
                var hex = Array.prototype.map.call(new Uint8Array(buf), function (b) {
                    return ('0' + b.toString(16)).slice(-2);
                }).join('');
                return prefix + '-' + hex.slice(0, 40);
            })
            .catch(function () { return randomIdempotencyKey(prefix); });
    }

    /* ─── Utility ──────────────────────────────────────────────────────────── */

    /** Righe carrello con nomi leggibili (stesso formato di cart.js). */
    function checkoutCartLines(cart) {
        if (!cart) return [];
        if (typeof cart.getItemsForCheckout === 'function') return cart.getItemsForCheckout();
        return cart.getItems ? cart.getItems() : [];
    }

    function getLang() {
        var htmlLang = document.documentElement.lang || '';
        var match    = htmlLang.match(/^[a-z]{2}/i);
        if (match) return match[0].toLowerCase();
        var pathMatch = global.location.pathname.match(/^\/([a-z]{2})\//);
        return pathMatch ? pathMatch[1].toLowerCase() : 'it';
    }

    function formatMoney(minor, currency) {
        var cur = String(currency || 'eur').toUpperCase();
        try {
            return new Intl.NumberFormat(getLang(), {
                style: 'currency', currency: cur,
                minimumFractionDigits: 2, maximumFractionDigits: 2
            }).format(minor / 100);
        } catch (_) {
            return '€ ' + (minor / 100).toFixed(2);
        }
    }

    /* ─── Validazione ──────────────────────────────────────────────────────── */

    function validatePIVA(v) {
        if (!/^\d{11}$/.test(v)) return false;
        var s = 0;
        for (var i = 0; i <= 9; i += 2) { s += parseInt(v[i], 10); }
        for (var j = 1; j <= 9; j += 2) {
            var d = parseInt(v[j], 10) * 2;
            s += d > 9 ? d - 9 : d;
        }
        return (10 - (s % 10)) % 10 === parseInt(v[10], 10);
    }

    function validateSDI(v) { return /^[A-Z0-9]{7}$/i.test(v); }

    function validateEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v); }

    /* ─── Gestione errori inline ───────────────────────────────────────────── */

    function checkoutApiErrorMessage(res, body, fallback) {
        if (res && (res.status === 429 || res.status === 503)) {
            if (body && body.error) return body.error;
            var el = document.getElementById('checkout-error-msg');
            return (el && el.getAttribute('data-rate-limit-error'))
                || 'Troppi tentativi di checkout. Riprova tra qualche minuto.';
        }
        if (body && body.error) return body.error;
        return fallback || ('HTTP ' + (res && res.status));
    }

    function readCheckoutApi(res) {
        return res.json().catch(function () { return {}; }).then(function (body) {
            if (!res.ok) {
                var err = new Error(checkoutApiErrorMessage(res, body, 'HTTP ' + res.status));
                err.status = res.status;
                err.code = body && body.code;
                throw err;
            }
            return body;
        });
    }

    function showFieldError(field, msg) {
        field.classList.add('is-invalid');
        var existing = field.querySelector('.field-error');
        if (existing) {
            existing.textContent = msg;
        } else {
            var errEl = document.createElement('p');
            errEl.className = 'field-error';
            errEl.setAttribute('role', 'alert');
            errEl.setAttribute('aria-live', 'polite');
            errEl.textContent = msg;
            field.appendChild(errEl);
        }
    }

    function clearFieldError(field) {
        field.classList.remove('is-invalid');
        var e = field.querySelector('.field-error');
        if (e) e.remove();
    }

    function clearErrors() {
        document.querySelectorAll('.form-field.is-invalid').forEach(function (f) { clearFieldError(f); });
    }

    /**
     * Porta l'elemento in vista solo se non lo e' gia'.
     *
     * Un messaggio d'errore smascherato fuori schermo e' indistinguibile da un
     * click che non ha fatto nulla: e' li' che l'utente abbandona o ritenta.
     */
    function scrollIntoViewIfNeeded(el) {
        if (!el) return;

        function attempt() {
            try {
                var rect = el.getBoundingClientRect();
                var vh   = global.innerHeight || document.documentElement.clientHeight;
                // Margine per la barra CTA fissa su mobile.
                if (rect.top >= 0 && rect.bottom <= vh - 80) return true;
                el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } catch (_) {
                try { el.scrollIntoView(); } catch (__) {}
            }
            return false;
        }

        if (attempt()) return;

        // Riepilogo carrello e campi carta montano dopo il primo scroll e
        // spingono il messaggio piu' in basso: senza i tentativi successivi
        // finirebbe di nuovo fuori schermo.
        //
        // Le retry vanno pero' annullate appena l'utente scrolla da solo: il
        // solo controllo "e' in vista" non distingue "il layout non si e'
        // ancora assestato" da "l'utente e' andato via di proposito", e
        // riporterebbe indietro chi e' risalito a correggere un campo.
        var cancelled = false;
        function onUserScroll() { cancelled = true; cleanup(); }
        function cleanup() {
            global.removeEventListener('wheel', onUserScroll);
            global.removeEventListener('touchmove', onUserScroll);
            global.removeEventListener('keydown', onUserScroll);
        }
        global.addEventListener('wheel', onUserScroll, { passive: true, once: true });
        global.addEventListener('touchmove', onUserScroll, { passive: true, once: true });
        global.addEventListener('keydown', onUserScroll, { once: true });

        function retry() { if (!cancelled) attempt(); }
        setTimeout(retry, 700);
        setTimeout(function () { retry(); cleanup(); }, 1600);
    }

    function showGlobalError(msg) {
        var el = document.getElementById('checkout-error-msg');
        if (!el) return;
        el.textContent = msg;
        el.hidden = false;
        scrollIntoViewIfNeeded(el);
    }

    function hideGlobalError() {
        var el = document.getElementById('checkout-error-msg');
        if (el) el.hidden = true;
    }

    /* ─── Tabs tipo cliente ────────────────────────────────────────────────── */

    function initCustomerTabs() {
        var tablist = document.querySelector('[role="tablist"].customer-tabs');
        if (!tablist) return;

        var tabs   = Array.from(tablist.querySelectorAll('[role="tab"]'));
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
                if      (e.key === 'ArrowRight' || e.key === 'ArrowDown') idx = (i + 1) % tabs.length;
                else if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   idx = (i - 1 + tabs.length) % tabs.length;
                else if (e.key === 'Home') idx = 0;
                else if (e.key === 'End')  idx = tabs.length - 1;
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

    /* ─── Tracking carrello: aggancia l'email digitata al cartId ─────────────── */
    // Statistica carrelli abbandonati (fase 1): nessun campo nuovo, si riusa
    // l'email già presente nel form. Solo se sintatticamente valida, altrimenti
    // un'email incompleta a metà digitazione finirebbe salvata come "abbandono".

    function initCartEmailSync() {
        var cart = global.AmlCart;
        if (!cart || !cart.notifyEmail) return;
        ['field-email', 'field-email-b'].forEach(function (id) {
            var input = document.getElementById(id);
            if (!input) return;
            input.addEventListener('blur', function () {
                var value = input.value.trim();
                if (value && validateEmail(value)) cart.notifyEmail(value);
            });
        });
    }

    /* ─── Raccolta dati form ───────────────────────────────────────────────── */

    function collectFormData() {
        var activeTab  = document.querySelector('[role="tab"][aria-selected="true"]');
        var isCompany  = activeTab && activeTab.dataset.customerType === 'business';
        var sfx        = isCompany ? '-b' : '';

        var data = {
            type:      isCompany ? 'business' : 'private',
            firstName: (document.getElementById('field-first-name' + sfx) || {}).value || '',
            lastName:  (document.getElementById('field-last-name'  + sfx) || {}).value || '',
            email:     (document.getElementById('field-email'       + sfx) || {}).value || '',
            phone:     (document.getElementById('field-phone'       + sfx) || {}).value || '',
        };

        if (isCompany) {
            data.ragioneSociale = (document.getElementById('field-ragione-sociale') || {}).value || '';
            data.piva           = (document.getElementById('field-piva')            || {}).value || '';
            data.sdi            = (document.getElementById('field-sdi')             || {}).value || '';
            data.pec            = (document.getElementById('field-pec')             || {}).value || '';
        }

        return data;
    }

    /* ─── Validazione form ─────────────────────────────────────────────────── */

    function getErrorMessages() {
        var form = document.getElementById('checkout-form');
        if (!form) return {};
        try { return JSON.parse(form.getAttribute('data-errors') || '{}'); } catch (_) { return {}; }
    }

    function validateForm() {
        clearErrors();
        var msgs   = getErrorMessages();
        var valid  = true;
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
        var lastName  = document.getElementById('field-last-name'  + sfx);
        var email     = document.getElementById('field-email'       + sfx);
        var phone     = document.getElementById('field-phone'       + sfx);

        if (firstName && !firstName.value.trim()) fail(firstName, msgs.required    || 'Campo obbligatorio');
        if (lastName  && !lastName.value.trim())  fail(lastName,  msgs.required    || 'Campo obbligatorio');
        if (email) {
            if (!email.value.trim())                      fail(email, msgs.required    || 'Campo obbligatorio');
            else if (!validateEmail(email.value.trim()))  fail(email, msgs.emailInvalid || 'Indirizzo email non valido');
        }
        if (phone && phone.value.trim() && phone.value.trim().length < 7) {
            fail(phone, msgs.phoneInvalid || 'Numero di telefono non valido');
        }

        if (isCompany) {
            var ragioneSociale = document.getElementById('field-ragione-sociale');
            var piva           = document.getElementById('field-piva');
            var sdi            = document.getElementById('field-sdi');
            var pec            = document.getElementById('field-pec');

            if (ragioneSociale && !ragioneSociale.value.trim()) fail(ragioneSociale, msgs.required || 'Campo obbligatorio');
            if (piva) {
                if (!piva.value.trim())                   fail(piva, msgs.required    || 'Campo obbligatorio');
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
                if (sdiVal && !validateSDI(sdiVal)) fail(sdi, msgs.sdiInvalid    || 'Codice SDI non valido (7 caratteri alfanumerici)');
                if (pecVal && !validateEmail(pecVal)) fail(pec, msgs.emailInvalid || 'Indirizzo PEC non valido');
            }
        }

        var shippingValid = validateShippingForm();

        if (firstInvalid) setTimeout(function () { firstInvalid.focus(); }, 0);
        return valid && shippingValid;
    }

    /* --- Funnel: dove si ferma il cliente ---------------------------------- */

    /**
     * Registra la posizione raggiunta nel checkout.
     *
     * Ogni evento parte UNA SOLA VOLTA per caricamento pagina: sono posizioni nel
     * funnel, non contatori di interazione, e senza il dedup un utente che
     * corregge l'email gonfierebbe checkout_contact_started falsando il tasso di
     * abbandono fra uno step e l'altro.
     *
     * cartId aggancia l'evento alla riga di cart_sessions, cosi' un carrello
     * abbandonato si legge fin dove era arrivato invece che solo in aggregato.
     * Vedi schema-analytics-checkout-funnel-migration.sql.
     */
    var _funnelSent = {};

    function trackFunnel(step) {
        if (_funnelSent[step]) return;
        _funnelSent[step] = true;
        try {
            var cart = global.AmlCart;
            var payload = { event: step };
            if (cart && cart.getCartId) {
                var cid = cart.getCartId();
                if (cid) payload.cartId = cid;
            }
            fetch('/api/track', {
                method:    'POST',
                headers:   { 'Content-Type': 'application/json' },
                keepalive: true,
                body:      JSON.stringify(payload),
            }).catch(function () {});
        } catch (_) { /* il tracking non deve mai rompere il checkout */ }
    }

    /* --- Sezioni progressive ----------------------------------------------- */

    /**
     * Tiene bloccata la sezione pagamento finche' l'anagrafica non e' completa.
     *
     * Il testo del blocco viene clonato da #payment-element-gate invece di essere
     * scritto qui: quella stringa esiste gia' tradotta in tutte e 7 le lingue e
     * dice esattamente la stessa cosa. Nessuna traduzione nuova da mantenere.
     */
    function initProgressiveSections() {
        var paymentTitle = document.getElementById('section-title-payment');
        if (!paymentTitle) return;
        var section = paymentTitle.closest('.form-section');
        if (!section) return;

        var lock = document.createElement('p');
        lock.className = 'checkout-step-lock';
        lock.id = 'checkout-step-lock';
        var gate = document.getElementById('payment-element-gate');
        lock.textContent = (gate && gate.textContent.trim()) || '';
        lock.insertAdjacentHTML('afterbegin',
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
            + '<rect x="3" y="11" width="18" height="11" rx="2"></rect>'
            + '<path stroke-linecap="round" d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>');
        paymentTitle.insertAdjacentElement('afterend', lock);

        var wasReady = null;
        function sync() {
            var ready = customerDataReady();
            if (ready === wasReady) return;
            wasReady = ready;

            section.classList.toggle('form-section--locked', !ready);
            lock.hidden = ready;
            // inert toglie interazione e voce nell'albero di accessibilita': la
            // sola opacita' lascerebbe i radio raggiungibili col tab.
            if (ready) section.removeAttribute('inert');
            else section.setAttribute('inert', '');

            if (ready) trackFunnel('checkout_contact_completed');
        }

        var CONTACT_IDS = [
            'field-first-name', 'field-last-name', 'field-email', 'field-phone',
            'field-first-name-b', 'field-last-name-b', 'field-email-b', 'field-phone-b',
            'field-ragione-sociale', 'field-piva', 'field-sdi', 'field-pec',
        ];
        CONTACT_IDS.forEach(function (id) {
            var el = document.getElementById(id);
            if (!el) return;
            // Il telefono e' opzionale: da solo non significa "ha iniziato
            // l'anagrafica", segnerebbe come avviati anche gli abbandoni immediati.
            var countsAsStart = id.indexOf('field-phone') !== 0;
            el.addEventListener('input', function () {
                if (countsAsStart && el.value.trim()) trackFunnel('checkout_contact_started');
                sync();
            });
            el.addEventListener('blur', sync);
        });

        var tablist = document.querySelector('[role="tablist"].customer-tabs');
        if (tablist) tablist.addEventListener('click', function () { setTimeout(sync, 0); });

        // Il ripristino dei campi del browser (torna indietro, bfcache, gestore
        // password) non emette 'input': senza questi due sync la sezione
        // resterebbe bloccata con l'anagrafica gia' piena, cioe' un vicolo cieco.
        global.addEventListener('pageshow', sync);
        setTimeout(sync, 400);

        // Scelta metodo o campi carta = il cliente e' entrato nel passo pagamento.
        //
        // isTrusted scarta i change sintetici: showStripeUnavailable() seleziona
        // il bonifico via dispatchEvent, e senza questo filtro ogni pagina con
        // Stripe non disponibile registrerebbe un checkout_payment_started prima
        // ancora che il cliente tocchi il form, falsando tutto il funnel.
        document.querySelectorAll('input[name="payment-method"]').forEach(function (r) {
            r.addEventListener('change', function (ev) {
                if (ev && ev.isTrusted === false) return;
                trackFunnel('checkout_payment_started');
            });
        });
        // Niente listener DOM su #payment-element: il Payment Element e' un iframe
        // cross-origin, i click al suo interno non arrivano mai al parent. Il
        // segnale vero e' l'evento 'focus' di Stripe Elements, agganciato al
        // momento del mount in maybeMountPaymentElement().

        sync();
    }

    /* ─── Metodi di pagamento — visibilità ────────────────────────────────── */

    /**
     * Nasconde la barra azioni quando nessuno dei due bottoni di submit e'
     * visibile.
     *
     * Serve con PayPal selezionato: li' la CTA sono i bottoni dell'SDK e
     * entrambi i submit sono spenti. Su mobile la barra e' una superficie fissa
     * con bordo e sfondo, quindi senza questo resterebbe in fondo allo schermo
     * come una striscia vuota. Legge lo stato dal DOM invece di riceverlo come
     * argomento, cosi' vale anche per showStripeUnavailable(), che spegne il
     * bottone carta da un altro punto del flusso.
     */
    function syncActionsBar() {
        var bar = document.querySelector('.checkout-actions');
        if (!bar) return;
        var anyVisible = ['btn-stripe-submit', 'btn-transfer-submit'].some(function (id) {
            var el = document.getElementById(id);
            return el && !el.hidden && el.style.display !== 'none';
        });
        bar.hidden = !anyVisible;
    }

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

            if (stripeSection)   stripeSection.hidden   = method !== 'stripe';
            if (transferSection) transferSection.hidden  = method !== 'transfer';
            if (paypalSection)   paypalSection.hidden    = method !== 'paypal';

            var stripeBtnOk = method === 'stripe' && (!isOnPageStripe() || _stripeEnabled);
            if (btnStripe)   btnStripe.style.display   = stripeBtnOk ? '' : 'none';
            // La nota "consegna in 2-15 min" vale per il pagamento con carta:
            // col bonifico la licenza parte quando l'incasso e' visibile, e
            // lasciarla li' sarebbe una promessa che non manteniamo.
            var ctaNote = document.getElementById('checkout-cta-note');
            if (ctaNote) ctaNote.hidden = !stripeBtnOk;
            if (btnTransfer) btnTransfer.style.display  = method === 'transfer' ? '' : 'none';
            syncActionsBar();

            if (method === 'paypal') initPaypalButtons();
            if (method === 'stripe' && isOnPageStripe()) maybeMountPaymentElement();
        }

        radios.forEach(function (r) { r.addEventListener('change', updateVisibility); });
        updateVisibility();
    }

    /* ─── Spedizione ───────────────────────────────────────────────────────── */
    // Mostra/richiede l'indirizzo solo se il carrello contiene un articolo fisico
    // (DVD/COA — flag impostato in cart.js da data-physical sulla pagina prodotto).
    // Il server rivalida comunque in modo indipendente via catalog.js.

    var SHIPPING_FIELD_IDS = ['field-address', 'field-city', 'field-postal-code', 'field-country'];

    function cartHasPhysical(items) {
        return (items || []).some(function (l) { return Boolean(l.physical); });
    }

    function updateShippingVisibility(items) {
        var section = document.getElementById('shipping-section');
        var note    = document.getElementById('checkout-shipping-note');
        var needsShipping = cartHasPhysical(items);

        if (section) {
            section.hidden = !needsShipping;
            SHIPPING_FIELD_IDS.forEach(function (id) {
                var input = document.getElementById(id);
                if (!input) return;
                if (needsShipping) input.setAttribute('required', '');
                else input.removeAttribute('required');
            });
        }
        if (note) {
            note.textContent = needsShipping
                ? (note.getAttribute('data-label-physical') || note.textContent)
                : (note.getAttribute('data-label-digital')  || note.textContent);
        }
        return needsShipping;
    }

    function collectShippingData() {
        return {
            addressLine1: (document.getElementById('field-address')      || {}).value || '',
            city:         (document.getElementById('field-city')         || {}).value || '',
            postalCode:   (document.getElementById('field-postal-code')  || {}).value || '',
            province:     (document.getElementById('field-province')     || {}).value || '',
            country:      (document.getElementById('field-country')      || {}).value || '',
        };
    }

    function validateShippingForm() {
        var section = document.getElementById('shipping-section');
        if (!section || section.hidden) return true;

        var msgs  = getErrorMessages();
        var valid = true;
        var firstInvalid = null;

        function fail(fieldEl) {
            var wrapper = fieldEl.closest('.form-field');
            if (wrapper) showFieldError(wrapper, msgs.required || 'Campo obbligatorio');
            if (!firstInvalid) firstInvalid = fieldEl;
            valid = false;
        }

        SHIPPING_FIELD_IDS.forEach(function (id) {
            var input = document.getElementById(id);
            if (input && !input.value.trim()) fail(input);
        });

        if (firstInvalid) setTimeout(function () { firstInvalid.focus(); }, 0);
        return valid;
    }

    function shippingPayloadIfNeeded() {
        var section = document.getElementById('shipping-section');
        if (!section || section.hidden) return undefined;
        return collectShippingData();
    }

    /* ─── Riepilogo carrello ───────────────────────────────────────────────── */

    function renderCartSummary() {
        var cart = global.AmlCart;
        if (!cart) return;

        var lines    = checkoutCartLines(cart);
        var totalQty = cart.totalQty  ? cart.totalQty()  : 0;

        if (!lines.length || totalQty === 0) {
            global.location.href = CART_PATHS[getLang()] || CART_PATHS['it'];
            return;
        }

        var container = document.getElementById('checkout-items');
        if (!container) return;
        container.textContent = '';

        var currency = (lines[0] && lines[0].currency) || 'eur';

        updateShippingVisibility(lines);

        lines.forEach(function (line) {
            var qty       = Number(line.quantity) || 0;
            var lineMinor = Math.round(Number(line.unitAmount) || 0) * qty;

            var item  = document.createElement('div'); item.className  = 'checkout-item';
            var thumb = document.createElement('img'); thumb.className = 'checkout-item-thumb';
            var info  = document.createElement('div'); info.className  = 'checkout-item-info';
            var name  = document.createElement('div'); name.className  = 'checkout-item-name';
            var qtyEl = document.createElement('div'); qtyEl.className = 'checkout-item-qty';
            var price = document.createElement('div'); price.className = 'checkout-item-price';

            name.textContent  = (cart.lineDisplayName && cart.lineDisplayName(line)) || line.name || line.sku;
            qtyEl.textContent = (container.getAttribute('data-qty-label') || 'Qtà') + ': ' + qty;
            price.textContent = formatMoney(lineMinor, currency);

            // Stessa copertina e stesso fallback del carrello: le righe salvate
            // prima di questa versione non hanno `image`, e senza fallback
            // resterebbe un'icona di immagine rotta dentro il riepilogo.
            thumb.src = line.image || FALLBACK_THUMB;
            thumb.alt = '';
            thumb.width = 44;
            thumb.height = 44;
            thumb.loading = 'lazy';
            thumb.decoding = 'async';
            bindThumbFallback(thumb);

            info.appendChild(name);
            info.appendChild(qtyEl);
            item.appendChild(thumb);
            item.appendChild(info);
            item.appendChild(price);
            container.appendChild(item);
        });

        // Nessuna riga IVA: le vendite sono in regime forfettario, quindi l'IVA
        // non e' applicata e il prezzo esposto e' gia' quello finale. Mostrarne
        // una quota sarebbe una dichiarazione fiscale falsa — e un cliente con
        // P.IVA potrebbe tentare di detrarre un'imposta mai addebitata.
        var minor   = cart.totalMinor ? cart.totalMinor() : 0;

        var totalEl = document.getElementById('checkout-grand-total');
        var subEl   = document.getElementById('checkout-subtotal');
        var tAmount = document.getElementById('transfer-amount');
        var payAmt  = document.getElementById('btn-pay-amount');

        if (totalEl) totalEl.textContent = formatMoney(minor, currency);
        if (subEl)   subEl.textContent   = formatMoney(minor, currency);
        if (tAmount) tAmount.textContent = formatMoney(minor, currency);
        if (payAmt)  payAmt.textContent  = formatMoney(minor, currency);

        // Mirror sul riepilogo comprimibile mobile (<details> nativo, zero JS)
        var mItems = document.getElementById('mcheckout-items');
        if (mItems) {
            mItems.innerHTML = container.innerHTML;
            // innerHTML serializza il markup ma non porta con se' i listener:
            // le copie vanno riagganciate o qui il ripiego non scatterebbe.
            mItems.querySelectorAll('.checkout-item-thumb').forEach(bindThumbFallback);
        }
        [
            ['mcheckout-grand-total',   formatMoney(minor, currency)],
            ['mcheckout-grand-total-2', formatMoney(minor, currency)],
            ['mcheckout-subtotal',      formatMoney(minor, currency)],
        ].forEach(function (pair) {
            var el = document.getElementById(pair[0]);
            if (el) el.textContent = pair[1];
        });

        var emptySection    = document.getElementById('checkout-empty-section');
        var checkoutContent = document.getElementById('checkout-content');
        if (emptySection)    emptySection.hidden    = true;
        if (checkoutContent) checkoutContent.hidden = false;

        /* Riepilogo mobile aperto di default, ma solo per carrelli corti.
           Chiuso mostra il totale senza dire per cosa, e verificarlo costa un
           tocco proprio nel punto in cui si esita. Sopra le 3 voci resta chiuso:
           aperto spingerebbe il form fuori schermo, che e' peggio del problema
           che risolve. Se l'utente lo ha gia' aperto o chiuso a mano non si
           tocca piu' nulla: e' una scelta sua. */
        var msummary = document.getElementById('checkout-msummary');
        if (msummary && !msummary.dataset.amlAutoOpened) {
            msummary.dataset.amlAutoOpened = '1';
            if (lines.length > 0 && lines.length <= 3) msummary.open = true;
        }

        // Prima posizione del funnel. Va qui e non in init(): e' l'unico punto in
        // cui sappiamo che il carrello non e' vuoto e il form e' davvero a schermo,
        // altrimenti conteremmo come "arrivati al checkout" anche i carrelli vuoti.
        trackFunnel('checkout_view');
    }

    /* ─── Flusso Stripe legacy (Checkout ospitato, redirect) — lingue non IT ─── */

    function handleStripeSubmit(e) {
        e.preventDefault();
        if (_isSubmitting) return;
        if (!validateForm()) return;
        // Dopo la validazione: un click su form invalido registrerebbe
        // pay_clicked senza contact_completed, cioe' uno stadio tardivo con piu'
        // eventi di uno precedente. Chi si blocca qui risulta gia' fermo allo
        // step contatti, che e' dove si e' fermato davvero.
        trackFunnel('checkout_pay_clicked');

        var btn      = document.getElementById('btn-stripe-submit');
        var cart     = global.AmlCart;
        var items    = checkoutCartLines(cart);
        var lang     = getLang();
        var customer = collectFormData();

        _isSubmitting = true;
        if (btn) { btn.setAttribute('aria-busy', 'true'); btn.disabled = true; }
        hideGlobalError();

        buildIdempotencyKey('sk', items, customer.email)
        .then(function (idempotencyKey) {
            return fetch(STRIPE_WORKER_URL, {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify({
                    idempotencyKey: idempotencyKey,
                    customer:       customer,
                    items:          items,
                    lang:           lang,
                    shipping:       shippingPayloadIfNeeded(),
                    cartId:         global.AmlCart && global.AmlCart.getCartId ? global.AmlCart.getCartId() : undefined,
                }),
            });
        })
        .then(function (res) { return readCheckoutApi(res); })
        .then(function (data) {
            if (data && data.url) {
                global.location.href = data.url;
            } else {
                throw new Error('Risposta Worker non valida');
            }
        })
        .catch(function (err) {
            console.error('[Checkout] Stripe error:', err);
            var errorEl = document.getElementById('checkout-error-msg');
            var fallback = errorEl && errorEl.getAttribute('data-network-error') || 'Errore di connessione. Riprova.';
            showGlobalError(err && err.message && err.status ? err.message : fallback);
            if (btn) { btn.removeAttribute('aria-busy'); btn.disabled = false; }
            _isSubmitting = false;
        });
    }

    /* ─── Flusso Stripe on-page (Express Checkout Element + Payment Element) ─── */

    // Stati PaymentIntent in cui il denaro e' impegnato e il cliente ha finito.
    // Deve restare allineata a SETTLED_PI_STATUSES in functions/api/[[catchall]].js:
    // se il client redirige per uno stato che il server non accetta, chi ha appena
    // pagato si ritrova sul form con un errore.
    var SETTLED_PI_STATUSES = ['succeeded', 'processing', 'requires_capture'];

    function getReturnUrl() {
        return global.location.origin + STRIPE_INTENT_RETURN_URL + '?lang=' + getLang();
    }

    /** true se l'anagrafica minima per creare il PaymentIntent manuale è valida. */
    function customerDataReady() {
        var activeTab = document.querySelector('[role="tab"][aria-selected="true"]');
        var isCompany = activeTab && activeTab.dataset.customerType === 'business';
        var sfx       = isCompany ? '-b' : '';
        var val = function (id) {
            var el = document.getElementById(id);
            return el ? el.value.trim() : '';
        };
        if (!val('field-first-name' + sfx) || !val('field-last-name' + sfx)) return false;
        if (!validateEmail(val('field-email' + sfx))) return false;
        if (isCompany) {
            if (!val('field-ragione-sociale') || !validatePIVA(val('field-piva'))) return false;
            if (!val('field-sdi') && !val('field-pec')) return false;
        }
        return true;
    }

    /** Chiave per capire se i dati cliente sono cambiati e va rimontato il PE. */
    function customerKey() {
        var c = collectFormData();
        return [c.type, c.email, c.firstName, c.lastName, c.piva, c.sdi, c.pec].join('|').toLowerCase();
    }

    function showStripeUnavailable() {
        var ids = ['express-checkout', 'btn-stripe-submit', 'payment-element-gate', 'payment-element'];
        ids.forEach(function (id) { var el = document.getElementById(id); if (el) el.hidden = true; });
        var btn = document.getElementById('btn-stripe-submit');
        if (btn) btn.style.display = 'none';
        syncActionsBar();
        var un = document.getElementById('stripe-unavailable');
        if (un) un.hidden = false;

        // Senza questo ripiego la pagina resta senza CTA: la carta e' nascosta ma
        // il bonifico non e' selezionato, quindi nessun bottone di submit e'
        // visibile e l'utente arriva in fondo al form senza nulla da premere.
        var stripeRadio = document.getElementById('pay-stripe');
        if (stripeRadio) {
            stripeRadio.disabled = true;
            var opt = stripeRadio.closest('.payment-option');
            if (opt) opt.classList.add('payment-option--disabled');
        }
        var transferRadio = document.getElementById('pay-transfer');
        if (transferRadio && !transferRadio.checked) {
            transferRadio.checked = true;
            // initPaymentMethod e' gia' inizializzato: l'evento fa comparire la
            // sezione bonifico e il relativo bottone "Conferma ordine".
            transferRadio.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }

    function postPaymentIntent(payload) {
        return fetch(STRIPE_PI_URL, {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(payload),
        }).then(readCheckoutApi);
    }

    function initStripeCheckout() {
        if (!global.Stripe) { showStripeUnavailable(); return; }
        fetch(STRIPE_CONFIG_URL)
            .then(function (res) { return res.ok ? res.json() : {}; })
            .then(function (cfg) {
                if (!cfg || !cfg.publishableKey) { showStripeUnavailable(); return; }
                _stripe        = global.Stripe(cfg.publishableKey);
                _stripeEnabled = true;
                var selected = document.querySelector('input[name="payment-method"]:checked');
                if (selected && selected.value === 'stripe') {
                    var btn = document.getElementById('btn-stripe-submit');
                    if (btn) btn.style.display = '';
                    syncActionsBar();
                    maybeMountPaymentElement();
                }
                mountExpressCheckout();
            })
            .catch(function () { showStripeUnavailable(); });
    }

    /**
     * Express Checkout Element: wallet 1-click.
     *
     * Deferred mode (`mode:'payment'` + amount, senza clientSecret): l'Element si
     * monta con il solo importo e il PaymentIntent nasce nell'handler `confirm`,
     * cioe' solo quando qualcuno preme davvero il bottone del wallet. Montarlo
     * con un clientSecret significherebbe creare un ordine e una credenziale di
     * pagamento a ogni caricamento di pagina, anche sui browser senza wallet.
     *
     * `emailRequired` non e' cosmetico: senza, i wallet non restituiscono l'email
     * ne' a noi ne' a Stripe, e la licenza (emessa a mano dopo i controlli
     * antifrode) resterebbe senza destinatario.
     */
    function mountExpressCheckout() {
        var section = document.getElementById('express-checkout');
        var mount   = document.getElementById('express-checkout-element');
        if (!section || !mount || !_stripe) return;

        var cart  = global.AmlCart;
        var items = checkoutCartLines(cart);
        if (!items.length || cartHasPhysical(items)) return; // no wallet per articoli fisici

        var totalMinor = cart && cart.totalMinor ? cart.totalMinor() : 0;
        if (!totalMinor) return;

        _elementsExpress = _stripe.elements({
            mode:     'payment',
            amount:   totalMinor,
            currency: String((items[0] && items[0].currency) || 'eur').toLowerCase(),
        });

        var ece = _elementsExpress.create('expressCheckout', {
            buttonHeight: 48,
            emailRequired: true,
            // `paymentMethodOrder` ordina soltanto, non filtra: senza
            // `paymentMethods` l'Element propone tutti i wallet attivi in
            // dashboard. Qui l'elenco e' esplicito.
            //
            // amazonPay era 'never' finche' eurolicenze.com non era fra i domini
            // registrati in Stripe (il bottone si disegnava e poi falliva in CORS
            // con merchantId=undefined). Dominio registrato il 2026-08-29
            // (pmd_1U9mwOKD4bVig4Jg74x1VXgD), quindi riattivato.
            //
            // paypal e' passato a Stripe: la nostra integrazione SDK stava sotto
            // il form e in createOrder chiamava validateForm(), quindi il bottone
            // non partiva finche' il cliente non aveva compilato l'anagrafica —
            // l'opposto di un 1-click. Qui in cima non vede nemmeno il form.
            // L'opzione PayPal e il contenitore dei bottoni SDK sono stati tolti
            // dai sette checkout: restava un doppione che creava l'ordine per
            // un'altra strada.
            paymentMethods: {
                applePay:  'auto',
                googlePay: 'auto',
                link:      'auto',
                amazonPay: 'auto',
                paypal:    'auto',
            },
            paymentMethodOrder: ['applePay', 'googlePay', 'paypal', 'link', 'amazonPay'],
        });

        ece.on('ready', function (e) {
            var methods = e && e.availablePaymentMethods;
            section.hidden = !methods; // nessun wallet disponibile → resta nascosto
        });

        ece.on('confirm', function (event) {
            if (_isSubmitting) {
                if (event && event.paymentFailed) event.paymentFailed({ reason: 'fail' });
                return;
            }
            _isSubmitting = true;
            hideGlobalError();
            confirmExpressPayment(event);
        });

        ece.mount(mount);
    }

    /** Conferma il wallet: submit → PaymentIntent server-side → confirmPayment. */
    function confirmExpressPayment(event) {
        var cart    = global.AmlCart;
        var items   = checkoutCartLines(cart);
        var details = (event && event.billingDetails) || {};
        var email   = String(details.email || '').trim();

        function abort(msg) {
            _isSubmitting = false;
            if (event && event.paymentFailed) event.paymentFailed({ reason: 'fail' });
            if (msg) showGlobalError(msg);
        }

        if (!validateEmail(email)) {
            abort('Non abbiamo ricevuto un indirizzo email dal wallet. Completa l’ordine con il modulo qui sotto.');
            return;
        }

        // Deferred mode: submit() prima di creare il PaymentIntent (richiesto da Stripe).
        _elementsExpress.submit()
        .then(function (res) {
            if (res && res.error) throw res.error;
            return buildIdempotencyKey('pex', items, email);
        })
        .then(function (idempotencyKey) {
            return postPaymentIntent({
                mode:           'express',
                idempotencyKey: idempotencyKey,
                walletEmail:    email,
                walletName:     String(details.name || '').trim() || undefined,
                items:          items,
                lang:           getLang(),
                cartId:         cart && cart.getCartId ? cart.getCartId() : undefined,
            });
        })
        .then(function (data) {
            if (!data || !data.clientSecret) throw new Error('clientSecret mancante');
            confirmStripePayment(_elementsExpress, data.clientSecret);
        })
        .catch(function (err) {
            console.error('[Checkout] Express Checkout error:', err);
            abort(err && err.status && err.message ? err.message
                : 'Pagamento rapido non riuscito. Riprova o completa l’ordine con il modulo qui sotto.');
        });
    }

    /** (Ri)monta il Payment Element quando l'anagrafica è pronta e Stripe è il metodo scelto. */
    function maybeMountPaymentElement() {
        if (!_stripeEnabled || !_stripe) return;
        var selected = document.querySelector('input[name="payment-method"]:checked');
        if (!selected || selected.value !== 'stripe') return;

        var gate    = document.getElementById('payment-element-gate');
        var loading = document.getElementById('payment-element-loading');

        if (!customerDataReady()) {
            if (gate) gate.hidden = false;
            return;
        }
        var key = customerKey();
        if (_paymentElement && key === _lastPiCustomerKey) { if (gate) gate.hidden = true; return; }
        if (_paymentElMounting) return;

        _paymentElMounting = true;
        if (gate) gate.hidden = true;
        if (loading) loading.hidden = false;

        var cart     = global.AmlCart;
        var items    = checkoutCartLines(cart);
        var customer = collectFormData();

        buildIdempotencyKey('pi', items, customer.email)
        .then(function (idempotencyKey) {
            return postPaymentIntent({
                mode:           'manual',
                idempotencyKey: idempotencyKey,
                customer:       customer,
                items:          items,
                lang:           getLang(),
                shipping:       shippingPayloadIfNeeded(),
                cartId:         cart && cart.getCartId ? cart.getCartId() : undefined,
            });
        })
        .then(function (data) {
            if (!data || !data.clientSecret) throw new Error('clientSecret mancante');
            if (_paymentElement) { try { _paymentElement.unmount(); } catch (_) {} _paymentElement = null; }
            _elementsManual = _stripe.elements({ clientSecret: data.clientSecret });
            _paymentElement = _elementsManual.create('payment', { layout: 'tabs' });
            // Il default e' gia' "carta": chi non cambia metodo non emette mai un
            // change sui radio, quindi senza questo il passo pagamento risulterebbe
            // saltato proprio per il percorso piu' comune.
            _paymentElement.on('focus', function () { trackFunnel('checkout_payment_started'); });
            _paymentElement.mount('#payment-element');
            _lastPiCustomerKey = customerKey();
        })
        .catch(function (err) {
            console.error('[Checkout] Payment Element error:', err);
            showGlobalError(err && err.status && err.message ? err.message
                : 'Impossibile preparare il pagamento con carta. Riprova o usa PayPal.');
        })
        .then(function () {
            _paymentElMounting = false;
            if (loading) loading.hidden = true;
        });
    }

    /**
     * Conferma un pagamento con l'istanza elements passata.
     * `clientSecret` va passato solo dal flusso express (deferred mode); nel
     * flusso manuale e' gia' legato all'istanza `elements`.
     */
    function confirmStripePayment(elements, clientSecret) {
        var btn = document.getElementById('btn-stripe-submit');
        if (btn) { btn.setAttribute('aria-busy', 'true'); btn.disabled = true; }

        var opts = {
            elements: elements,
            confirmParams: { return_url: getReturnUrl() },
            redirect: 'if_required',
        };
        if (clientSecret) opts.clientSecret = clientSecret;

        _stripe.confirmPayment(opts)
        .then(function (result) {
            if (result.error) {
                showGlobalError(result.error.message || 'Pagamento non riuscito. Riprova.');
                if (btn) { btn.removeAttribute('aria-busy'); btn.disabled = false; }
                _isSubmitting = false;
                return;
            }
            var pi = result.paymentIntent;
            if (pi && SETTLED_PI_STATUSES.indexOf(pi.status) !== -1) {
                // Niente rotateSessionSalt() qui: il sale va ruotato solo a ordine
                // davvero concluso, e ci pensa checkout-success.js quando l'ordine
                // viene trovato. Ruotarlo prima significherebbe che un ritorno in
                // errore fa ripartire il cliente con una idempotency key nuova,
                // cioe' con un secondo ordine e un secondo addebito.
                global.location.href = getReturnUrl() + '&payment_intent=' + encodeURIComponent(pi.id);
            } else {
                showGlobalError('Pagamento in sospeso. Se hai completato l’operazione riceverai la conferma via email.');
                if (btn) { btn.removeAttribute('aria-busy'); btn.disabled = false; }
                _isSubmitting = false;
            }
        })
        .catch(function (err) {
            console.error('[Checkout] confirmPayment error:', err);
            showGlobalError('Errore di connessione durante il pagamento. Riprova.');
            if (btn) { btn.removeAttribute('aria-busy'); btn.disabled = false; }
            _isSubmitting = false;
        });
    }

    /** Click sul bottone "Paga" del percorso carta manuale. */
    function handleStripePayClick(e) {
        e.preventDefault();
        if (_isSubmitting) return;
        if (!_stripeEnabled) return;
        if (!validateForm()) return;
        trackFunnel('checkout_pay_clicked');

        hideGlobalError();

        if (!_paymentElement) {
            // Anagrafica ok ma campi carta non ancora montati: montali e porta
            // l'utente sopra di essi. Senza lo scroll il click sembra a vuoto,
            // perche' i campi da compilare stanno fuori schermo.
            // Porta subito in vista l'area pagamento: maybeMountPaymentElement
            // scopre gia' #payment-element-loading, quindi l'utente vede
            // "Caricamento campi carta..." invece di un click a vuoto.
            scrollIntoViewIfNeeded(document.getElementById('stripe-section')
                || document.getElementById('payment-element'));
            // Il mount richiede una chiamata di rete per creare il PaymentIntent:
            // con un ritardo fisso il focus cadrebbe su un div ancora vuoto ogni
            // volta che la rete e' piu' lenta della stima. Qui si aspetta il
            // mount vero, con un tetto per non restare appesi se fallisce.
            maybeMountPaymentElement();
            var waited = 0;
            var poll = setInterval(function () {
                waited += 150;
                if (_paymentElement) {
                    clearInterval(poll);
                    if (_paymentElement.focus) {
                        try { _paymentElement.focus(); } catch (_) {}
                    }
                } else if (waited >= 6000) {
                    clearInterval(poll);
                }
            }, 150);
            return;
        }
        _isSubmitting = true;
        confirmStripePayment(_elementsManual);
    }

    /* ─── Flusso Bonifico ──────────────────────────────────────────────────── */

    function handleTransferSubmit(e) {
        e.preventDefault();
        if (_isSubmitting) return;
        if (!validateForm()) return;
        trackFunnel('checkout_pay_clicked');

        var btn      = document.getElementById('btn-transfer-submit');
        var cart     = global.AmlCart;
        var items    = checkoutCartLines(cart);
        var lang     = getLang();
        var customer = collectFormData();

        _isSubmitting = true;
        if (btn) { btn.setAttribute('aria-busy', 'true'); btn.disabled = true; }
        hideGlobalError();

        buildIdempotencyKey('bt', items, customer.email)
        .then(function (idempotencyKey) {
            return fetch(TRANSFER_WORKER_URL, {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify({
                    idempotencyKey: idempotencyKey,
                    customer:       customer,
                    items:          items,
                    lang:           lang,
                    shipping:       shippingPayloadIfNeeded(),
                    cartId:         global.AmlCart && global.AmlCart.getCartId ? global.AmlCart.getCartId() : undefined,
                }),
            });
        })
        .then(function (res) {
            return readCheckoutApi(res);
        })
        .then(function (data) {
            if (data && data.oid) {
                // Ordine creato → ruota il sale: il prossimo checkout è un nuovo ordine
                rotateSessionSalt();
                // Redirect alla thank-you page con token
                global.location.href = '/' + lang + '/checkout-success'
                    + '?oid=' + encodeURIComponent(data.oid)
                    + '&exp=' + encodeURIComponent(data.exp)
                    + '&t='   + encodeURIComponent(data.t);
            } else {
                throw new Error('Risposta Worker non valida');
            }
        })
        .catch(function (fetchErr) {
            console.error('[Checkout] Transfer error:', fetchErr);
            var errorEl = document.getElementById('checkout-error-msg');
            var fallback = errorEl && errorEl.getAttribute('data-network-error') || 'Errore di connessione. Riprova.';
            showGlobalError(fetchErr && fetchErr.message && fetchErr.status ? fetchErr.message : fallback);
            if (btn) { btn.removeAttribute('aria-busy'); btn.disabled = false; }
            _isSubmitting = false;
        });
    }

    /* ─── PayPal SDK loader ────────────────────────────────────────────────── */

    var _ppClientIdPromise = null;

    /** Client ID PayPal dal backend (sandbox o live a seconda dell'ambiente). */
    function fetchPaypalClientId() {
        if (_ppClientIdPromise) return _ppClientIdPromise;
        _ppClientIdPromise = fetch(PAYPAL_CONFIG_URL)
            .then(function (res) {
                if (!res.ok) throw new Error('HTTP ' + res.status);
                return res.json();
            })
            .then(function (data) {
                if (!data || !data.clientId) throw new Error('PayPal non configurato');
                return data.clientId;
            })
            .catch(function (cfgErr) {
                _ppClientIdPromise = null; // consente un retry al prossimo tentativo
                throw cfgErr;
            });
        return _ppClientIdPromise;
    }

    function loadPaypalSDK() {
        return fetchPaypalClientId().then(function (clientId) {
            return loadPaypalSDKWithClientId(clientId);
        });
    }

    function loadPaypalSDKWithClientId(clientId) {
        return new Promise(function (resolve, reject) {
            if (_ppSdkLoaded && global.paypal) { resolve(); return; }
            if (_ppSdkLoading) { _ppSdkQueue.push({ resolve: resolve, reject: reject }); return; }

            _ppSdkLoading = true;
            var lang   = getLang();
            var locale = PAYPAL_LOCALE_MAP[lang] || 'it_IT';
            var src    = 'https://www.paypal.com/sdk/js'
                       + '?client-id='  + encodeURIComponent(clientId)
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
                var loadErr = new Error('PayPal SDK load failed');
                _ppSdkQueue.forEach(function (cb) { cb.reject(loadErr); });
                _ppSdkQueue = [];
                reject(loadErr);
            };

            document.head.appendChild(script);
        });
    }

    /* ─── PayPal Buttons ───────────────────────────────────────────────────── */

    function setPaypalLoadingVisible(loadingEl, visible) {
        if (!loadingEl) return;
        loadingEl.hidden = !visible;
    }

    function initPaypalButtons() {
        var container = document.getElementById('paypal-buttons-container');
        var loadingEl = document.getElementById('paypal-loading');
        var errorEl   = document.getElementById('checkout-error-msg');

        if (!container) return;
        if (container.dataset.ppRendered) {
            setPaypalLoadingVisible(loadingEl, false);
            return;
        }

        setPaypalLoadingVisible(loadingEl, true);
        hideGlobalError();

        loadPaypalSDK()
            .then(function () {
                container.dataset.ppRendered = '1';

                return global.paypal.Buttons({
                    style: {
                        layout: 'vertical',
                        color:  'gold',
                        shape:  'rect',
                        label:  'paypal',
                        height: 48,
                    },

                    createOrder: function () {
                        if (_isSubmitting) {
                            // Doppio click — onError lo ignora (stesso marker della validazione)
                            throw new Error('aml-validation');
                        }
                        if (!validateForm()) {
                            // Errore intenzionale — onError lo ignora
                            throw new Error('aml-validation');
                        }

                        var cart     = global.AmlCart;
                        var items    = checkoutCartLines(cart);
                        var lang     = getLang();
                        var customer = collectFormData();

                        _isSubmitting = true;
                        return buildIdempotencyKey('pp', items, customer.email)
                        .then(function (idempotencyKey) {
                            return fetch(PAYPAL_WORKER_CREATE, {
                                method:  'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body:    JSON.stringify({
                                    idempotencyKey: idempotencyKey,
                                    customer:       customer,
                                    items:          items,
                                    lang:           lang,
                                    shipping:       shippingPayloadIfNeeded(),
                                    cartId:         global.AmlCart && global.AmlCart.getCartId ? global.AmlCart.getCartId() : undefined,
                                }),
                            });
                        })
                        .then(function (res) {
                            return readCheckoutApi(res);
                        })
                        .then(function (data) {
                            if (!data.orderID) throw new Error('orderID mancante dalla risposta Worker');
                            return data.orderID;
                        });
                    },

                    onApprove: function (data) {
                        return fetch(PAYPAL_WORKER_CAPTURE, {
                            method:  'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body:    JSON.stringify({ orderID: data.orderID }),
                        })
                        .then(function (res) {
                            if (!res.ok) throw new Error('HTTP ' + res.status);
                            return res.json();
                        })
                        .then(function (result) {
                            rotateSessionSalt();
                            var lang = getLang();
                            global.location.href = '/' + lang + '/checkout-success'
                                + '?oid=' + encodeURIComponent(result.oid)
                                + '&exp=' + encodeURIComponent(result.exp)
                                + '&t='   + encodeURIComponent(result.t);
                        })
                        .catch(function (captureErr) {
                            _isSubmitting = false;
                            console.error('[PayPal] Capture error:', captureErr);
                            showGlobalError('Errore nella conferma del pagamento PayPal. Contatta il supporto.');
                        });
                    },

                    onError: function (ppErr) {
                        _isSubmitting = false;
                        if (ppErr && ppErr.message === 'aml-validation') return;
                        console.error('[PayPal] SDK error:', ppErr);
                        if (ppErr && ppErr.status && ppErr.message) {
                            showGlobalError(ppErr.message);
                            return;
                        }
                        var netErr = errorEl && errorEl.getAttribute('data-network-error');
                        showGlobalError(netErr || 'Errore PayPal. Riprova o scegli un altro metodo.');
                    },

                    onCancel: function () {
                        _isSubmitting = false;
                        console.log('[PayPal] Pagamento annullato.');
                    },

                }).render('#paypal-buttons-container');
            })
            .then(function () {
                setPaypalLoadingVisible(loadingEl, false);
            })
            .catch(function (sdkErr) {
                console.error('[PayPal] Impossibile caricare SDK:', sdkErr);
                setPaypalLoadingVisible(loadingEl, false);
                showGlobalError('Impossibile caricare PayPal. Controlla la connessione o scegli un altro metodo.');
            });
    }

    /* ─── Bind submit buttons ──────────────────────────────────────────────── */

    function initSubmitButtons() {
        var btnStripe   = document.getElementById('btn-stripe-submit');
        var btnTransfer = document.getElementById('btn-transfer-submit');
        var form        = document.getElementById('checkout-form');

        if (btnStripe)   btnStripe.addEventListener('click', isOnPageStripe() ? handleStripePayClick : handleStripeSubmit);
        if (btnTransfer) btnTransfer.addEventListener('click', handleTransferSubmit);
        if (form) form.addEventListener('submit', function (ev) { ev.preventDefault(); });
    }

    /**
     * Mostra il motivo per cui il PSP ci ha rimandato indietro.
     *
     * /api/stripe-intent-return e il cancel_url del Checkout ospitato rimandano
     * su /{lang}/checkout?error=... (o ?cancelled=1). Senza questo, chi torna
     * indietro trova il form intatto e nessuna spiegazione: il riflesso naturale
     * e' ritentare, ed e' cosi' che nasce un secondo addebito.
     *
     * I testi vivono come data-attribute su #checkout-error-msg (stesso schema di
     * data-network-error). Se mancano — le lingue non ancora allineate — non si
     * mostra nulla, invece di scrivere in italiano su una pagina tedesca.
     */
    function initReturnNotice() {
        var el = document.getElementById('checkout-error-msg');
        if (!el || !global.URLSearchParams) return;

        var qs = new URLSearchParams(global.location.search);
        var reason = qs.get('error');
        var attr;

        if (qs.get('cancelled')) {
            attr = 'data-cancelled-notice';
        } else if (!reason) {
            return;
        } else if (reason.indexOf('payment_') === 0) {
            // Pagamento rifiutato/annullato dal PSP: ritentare ha senso.
            attr = 'data-payment-failed-notice';
        } else {
            // missing_pi / pi_lookup / order_not_found: non sappiamo se l'addebito
            // sia andato a buon fine, quindi va scoraggiato un secondo tentativo.
            attr = 'data-payment-unconfirmed-notice';
        }

        var msg = el.getAttribute(attr);
        if (msg) showGlobalError(msg);

        // Ripulisce la query: un refresh non deve rimostrare l'avviso.
        try {
            qs.delete('error');
            qs.delete('cancelled');
            var q = qs.toString();
            global.history.replaceState({}, '', global.location.pathname + (q ? '?' + q : ''));
        } catch (_) {}
    }

    /** Al variare dei dati cliente, (ri)monta il Payment Element se serve. */
    function initStripeRemountTriggers() {
        var ids = [
            'field-first-name', 'field-last-name', 'field-email',
            'field-first-name-b', 'field-last-name-b', 'field-email-b',
            'field-ragione-sociale', 'field-piva', 'field-sdi', 'field-pec',
        ];
        var debounce;
        ids.forEach(function (id) {
            var el = document.getElementById(id);
            if (!el) return;
            el.addEventListener('blur', function () {
                clearTimeout(debounce);
                debounce = setTimeout(maybeMountPaymentElement, 150);
            });
            // Il solo blur non basta: chi compila e tocca direttamente l'area
            // pagamento trova il testo del gate al posto dei campi carta.
            // Solo il PRIMO mount, pero': rimontare mentre si digita creerebbe
            // un PaymentIntent per ogni variazione dei dati cliente.
            el.addEventListener('input', function () {
                if (_paymentElement || _paymentElMounting) return;
                clearTimeout(debounce);
                debounce = setTimeout(function () {
                    if (_paymentElement || _paymentElMounting) return;
                    maybeMountPaymentElement();
                }, 800);
            });
        });
        var tablist = document.querySelector('[role="tablist"].customer-tabs');
        if (tablist) tablist.addEventListener('click', function () {
            setTimeout(maybeMountPaymentElement, 0);
        });
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
        initPaymentMethod();
        initProgressiveSections();
        initSubmitButtons();
        initCartEmailSync();
        initReturnNotice();

        if (isOnPageStripe()) {
            initStripeRemountTriggers();
            initStripeCheckout();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})(typeof window !== 'undefined' ? window : globalThis);
