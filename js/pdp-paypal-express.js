/**
 * pdp-paypal-express.js — bottone PayPal ufficiale sulla pagina prodotto.
 * Terzo percorso di conversione sotto "Acquista ora" / "Aggiungi al carrello":
 * niente form cliente prima di PayPal, l'identità del cliente arriva dal
 * payer PayPal alla cattura (vedi /api/paypal-express-create-order e il
 * backfill in /api/paypal-capture-order).
 *
 * Duplica volutamente una piccola parte di checkout.js (loader SDK, chiave di
 * idempotenza) invece di condividerla: sono due flussi diversi (qui niente
 * form/cliente) e toccare checkout.js per questo avrebbe allargato il rischio
 * sul checkout tradizionale già in produzione.
 */
(function (global) {
    'use strict';

    var CONTAINER = document.getElementById('pdp-paypal-express');
    if (!CONTAINER) return; // SKU fisico o pagina senza buy-box: niente da fare

    var EXPRESS_CREATE_URL = '/api/paypal-express-create-order';
    var CAPTURE_URL        = '/api/paypal-capture-order';
    var PAYPAL_CONFIG_URL  = '/api/paypal-config';
    var TRACK_URL          = '/api/track';

    var PAYPAL_LOCALE_MAP = {
        it: 'it_IT', en: 'en_US', fr: 'fr_FR', de: 'de_DE', es: 'es_ES', pt: 'pt_PT', nl: 'nl_NL',
    };

    function getLang() {
        var htmlLang = document.documentElement.lang || '';
        var match    = htmlLang.match(/^[a-z]{2}/i);
        if (match) return match[0].toLowerCase();
        var pathMatch = global.location.pathname.match(/^\/([a-z]{2})\//);
        return pathMatch ? pathMatch[1].toLowerCase() : 'it';
    }

    /* ─── Tracking fire-and-forget ─────────────────────────────────────────── */

    function track(eventName, extra) {
        try {
            var payload = Object.assign({ event: eventName }, extra || {});
            fetch(TRACK_URL, {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                keepalive: true,
                body: JSON.stringify(payload),
            }).catch(function () {});
        } catch (_) { /* fetch non disponibile */ }
    }

    /* ─── Chiave di idempotenza ────────────────────────────────────────────── */
    // Stesso principio di checkout.js (sale di sessione ruotato a ordine
    // completato) ma senza email: la base è sale + sku, così un doppio click
    // sullo stesso prodotto non crea due ordini, un prodotto diverso sì.

    var SALT_KEY = 'aml-ikey-salt';

    function getSessionSalt() {
        var s = null;
        try { s = sessionStorage.getItem(SALT_KEY); } catch (_) {}
        if (!s) {
            var arr = new Uint32Array(2);
            crypto.getRandomValues(arr);
            s = arr[0].toString(36) + arr[1].toString(36);
            try { sessionStorage.setItem(SALT_KEY, s); } catch (_) {}
        }
        return s;
    }

    function rotateSessionSalt() {
        try { sessionStorage.removeItem(SALT_KEY); } catch (_) {}
    }

    function randomIdempotencyKey() {
        var arr = new Uint32Array(2);
        crypto.getRandomValues(arr);
        return 'ppx-' + Date.now() + '-' + arr[0].toString(36) + arr[1].toString(36);
    }

    function buildIdempotencyKey(sku) {
        try {
            var basis = JSON.stringify([getSessionSalt(), 'ppx', sku]);
            if (!(global.crypto && crypto.subtle && global.TextEncoder)) {
                return Promise.resolve(randomIdempotencyKey());
            }
            return crypto.subtle.digest('SHA-256', new TextEncoder().encode(basis))
                .then(function (buf) {
                    var hex = Array.prototype.map.call(new Uint8Array(buf), function (b) {
                        return ('0' + b.toString(16)).slice(-2);
                    }).join('');
                    return 'ppx-' + hex.slice(0, 40);
                })
                .catch(function () { return randomIdempotencyKey(); });
        } catch (_) {
            return Promise.resolve(randomIdempotencyKey());
        }
    }

    /* ─── Selezione corrente sulla PDP ─────────────────────────────────────── */
    // Stessa fonte di dati di [data-cart-add] (js/cart.js): letta al click, non
    // in fase di init, così una variante/piano scelto dopo il caricamento della
    // pagina (plan switcher) è sempre quello effettivamente inviato.

    function currentSelection() {
        var root = document.getElementById('product-pricing');
        if (!root) return null;
        var sku = String(root.dataset.stripeProductSku || '').trim();
        if (!sku) return null;
        var physical = (root.dataset.physical || '') === 'true';
        return { sku: sku, physical: physical };
    }

    /* ─── Messaggi inline ───────────────────────────────────────────────────── */

    var errorEl   = document.getElementById('pdp-paypal-express-error');
    var loadingEl = document.getElementById('pdp-paypal-express-loading');
    var ERROR_AUTOHIDE_MS = 6000;
    var _errorTimer = null;

    /** Messaggio temporaneo: sparisce da solo, non deve restare li' per sempre
     *  a bloccare la vista una volta che l'utente ha gia' letto "annullato". */
    function showError(msg) {
        if (!errorEl) return;
        if (_errorTimer) { clearTimeout(_errorTimer); _errorTimer = null; }
        errorEl.textContent = msg;
        errorEl.hidden = false;
        _errorTimer = setTimeout(hideError, ERROR_AUTOHIDE_MS);
    }

    function hideError() {
        if (_errorTimer) { clearTimeout(_errorTimer); _errorTimer = null; }
        if (errorEl) errorEl.hidden = true;
    }

    function setLoading(visible) {
        if (loadingEl) loadingEl.hidden = !visible;
    }

    /* ─── PayPal SDK loader ─────────────────────────────────────────────────── */

    var _ppSdkLoaded  = false;
    var _ppSdkLoading = false;
    var _ppSdkQueue   = [];
    var _ppClientIdPromise = null;

    function fetchPaypalClientId() {
        if (_ppClientIdPromise) return _ppClientIdPromise;
        // window.__amlPaypalConfig: fetch partita da un <script> inline in <head>
        // (vedi _paypal_express_preload in product_page_lib.py), prima ancora che
        // questo file (defer) venga eseguito — risparmia un intero round-trip in
        // sequenza sul percorso critico del bottone.
        var prefetched = global.__amlPaypalConfig;
        _ppClientIdPromise = (prefetched ? prefetched : fetch(PAYPAL_CONFIG_URL).then(function (res) {
                if (!res.ok) throw new Error('HTTP ' + res.status);
                return res.json();
            }))
            .then(function (data) {
                if (!data || !data.clientId) throw new Error('PayPal non configurato');
                return data.clientId;
            })
            .catch(function (cfgErr) {
                _ppClientIdPromise = null;
                throw cfgErr;
            });
        return _ppClientIdPromise;
    }

    function loadPaypalSDK() {
        return fetchPaypalClientId().then(function (clientId) {
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
                script.setAttribute('data-sdk-integration-source', 'amlstore-pdp');

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
        });
    }

    /* ─── Bottone PayPal ────────────────────────────────────────────────────── */

    var _isSubmitting = false;

    function readApiResponse(res) {
        return res.json().catch(function () { return {}; }).then(function (body) {
            if (!res.ok) {
                var e = new Error((body && body.error) || ('HTTP ' + res.status));
                throw e;
            }
            return body;
        });
    }

    /**
     * Monta (o rimonta) i bottoni nel contenitore. Serve anche dopo un
     * annullamento: l'SDK PayPal a volte non ridisegna da solo il componente
     * dopo la chiusura del popup, lasciando il contenitore vuoto finche' non
     * lo si richiama esplicitamente — qui si pulisce e si rimonta, cosi'
     * l'utente puo' riprovare subito senza dover ricaricare la pagina.
     */
    function mountButtons(buttonsEl) {
        buttonsEl.innerHTML = '';

        return global.paypal.Buttons({
                    style: { layout: 'horizontal', color: 'gold', shape: 'rect', label: 'paypal', tagline: false, height: 38 },

                    createOrder: function () {
                        if (_isSubmitting) throw new Error('aml-busy');
                        var selection = currentSelection();
                        if (!selection || !selection.sku || selection.physical) {
                            throw new Error('aml-invalid-selection');
                        }

                        _isSubmitting = true;
                        hideError();

                        return buildIdempotencyKey(selection.sku).then(function (idempotencyKey) {
                            return fetch(EXPRESS_CREATE_URL, {
                                method:  'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body:    JSON.stringify({
                                    idempotencyKey: idempotencyKey,
                                    items:          [{ sku: selection.sku, quantity: 1 }],
                                    lang:           getLang(),
                                    cartId:         global.AmlCart && global.AmlCart.getCartId ? global.AmlCart.getCartId() : undefined,
                                }),
                            });
                        })
                        .then(readApiResponse)
                        .then(function (data) {
                            if (!data.orderID) throw new Error('orderID mancante dalla risposta');
                            return data.orderID;
                        });
                    },

                    onApprove: function (data) {
                        track('paypal_approved');
                        return fetch(CAPTURE_URL, {
                            method:  'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body:    JSON.stringify({ orderID: data.orderID }),
                        })
                        .then(readApiResponse)
                        .then(function (result) {
                            track('paypal_captured');
                            rotateSessionSalt();
                            if (global.AmlCart && global.AmlCart.resetCartSession) global.AmlCart.resetCartSession();
                            var lang = getLang();
                            global.location.href = '/' + lang + '/checkout-success'
                                + '?oid=' + encodeURIComponent(result.oid)
                                + '&exp=' + encodeURIComponent(result.exp)
                                + '&t='   + encodeURIComponent(result.t);
                        })
                        .catch(function (captureErr) {
                            _isSubmitting = false;
                            console.error('[PayPal Express] Capture error:', captureErr);
                            track('paypal_failed');
                            showError((errorEl && errorEl.getAttribute('data-msg-capture-error')) || 'Errore PayPal.');
                        });
                    },

                    onError: function (ppErr) {
                        _isSubmitting = false;
                        if (ppErr && /aml-busy/.test(ppErr.message)) return;
                        if (ppErr && /aml-invalid-selection/.test(ppErr.message)) {
                            showError((errorEl && errorEl.getAttribute('data-msg-error')) || 'PayPal non disponibile.');
                            return;
                        }
                        console.error('[PayPal Express] SDK error:', ppErr);
                        track('paypal_failed');
                        showError((errorEl && errorEl.getAttribute('data-msg-error')) || 'Errore PayPal.');
                    },

                    onCancel: function () {
                        _isSubmitting = false;
                        track('paypal_cancelled');
                        showError((errorEl && errorEl.getAttribute('data-msg-cancelled')) || 'Pagamento annullato.');
                        // L'SDK a volte non ridisegna da solo il bottone dopo la chiusura
                        // del popup: piccolo ritardo per lasciare che l'animazione di
                        // chiusura finisca, poi si rimonta cosi' resta cliccabile.
                        setTimeout(function () {
                            mountButtons(buttonsEl).catch(function (remountErr) {
                                console.error('[PayPal Express] Rimonta dopo annullamento fallita:', remountErr);
                            });
                        }, 400);
                    },

                }).render(buttonsEl);
    }

    function init() {
        var buttonsEl = document.getElementById('pdp-paypal-express-buttons');
        if (!buttonsEl) return;

        setLoading(true);
        hideError();

        loadPaypalSDK()
            .then(function () {
                return mountButtons(buttonsEl);
            })
            .then(function () {
                setLoading(false);
            })
            .catch(function (sdkErr) {
                console.warn('[PayPal Express] SDK non caricato, componente nascosto:', sdkErr);
                setLoading(false);
                if (CONTAINER) {
                    CONTAINER.hidden = true;
                    var sep = CONTAINER.previousElementSibling;
                    if (sep && sep.classList && (sep.classList.contains('pdp-paypal-sep')
                        || sep.classList.contains('pdp-cta-sep'))) {
                        sep.hidden = true;
                    }
                }
            });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})(typeof window !== 'undefined' ? window : globalThis);
