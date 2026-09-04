/**
 * Badge magazzino su schede fisiche (data-physical="true").
 * Fetch GET /api/stock?sku= — non tocca LCP; defer only.
 *
 * Quando la quantita' e' zero costruisce anche il form "Avvisami quando torna
 * disponibile". Il markup e le stringhe stanno qui e non nelle 49 PDP fisiche:
 * il blocco esiste solo nello stato esaurito, quindi baked nelle pagine
 * sarebbe HTML morto nel 99% delle visite, e ogni ritocco alla copia
 * costringerebbe a ripassare su sette lingue di file statici.
 */
(function () {
    'use strict';

    var LOW_MAX = 3;

    function pricingRoot() {
        return document.querySelector('[data-physical="true"][data-stripe-product-sku], #product-pricing[data-physical="true"]');
    }

    function stockEl(root) {
        return root ? root.querySelector('.v2-stock') : document.querySelector('.v2-stock');
    }

    function tpl(el, key, n) {
        var raw = el.getAttribute('data-stock-' + key) || '';
        return raw.replace(/\{n\}/g, String(n));
    }

    function setStatus(el, status, text) {
        el.setAttribute('data-stock-status', status);
        var t = el.querySelector('.v2-stock__text');
        if (t) t.textContent = text || '';
    }

    function setCtasDisabled(disabled) {
        var buttons = document.querySelectorAll('[data-cart-add]');
        for (var i = 0; i < buttons.length; i++) {
            var btn = buttons[i];
            if (disabled) {
                btn.setAttribute('disabled', '');
                btn.setAttribute('aria-disabled', 'true');
                btn.setAttribute('tabindex', '-1');
                btn.classList.add('is-stock-out');
            } else {
                btn.removeAttribute('disabled');
                btn.removeAttribute('aria-disabled');
                btn.removeAttribute('tabindex');
                btn.classList.remove('is-stock-out');
            }
        }
    }

    function updateJsonLd(inStock) {
        var scripts = document.querySelectorAll('script[type="application/ld+json"]');
        var avail = inStock
            ? 'https://schema.org/InStock'
            : 'https://schema.org/OutOfStock';
        for (var i = 0; i < scripts.length; i++) {
            var node = scripts[i];
            var raw = node.textContent;
            if (!raw || raw.indexOf('"Offer"') === -1 && raw.indexOf('Offer') === -1) continue;
            try {
                var data = JSON.parse(raw);
                var changed = false;
                function walk(obj) {
                    if (!obj || typeof obj !== 'object') return;
                    if (Array.isArray(obj)) {
                        obj.forEach(walk);
                        return;
                    }
                    var type = obj['@type'];
                    var isOffer = type === 'Offer' || (Array.isArray(type) && type.indexOf('Offer') !== -1);
                    if (isOffer && Object.prototype.hasOwnProperty.call(obj, 'availability')) {
                        obj.availability = avail;
                        changed = true;
                    }
                    if (obj.offers) walk(obj.offers);
                    if (obj['@graph']) walk(obj['@graph']);
                }
                walk(data);
                if (changed) node.textContent = JSON.stringify(data);
            } catch (_) { /* ignore malformed */ }
        }
    }

    /* ── Avvisami quando torna disponibile ─────────────────────────────────── */

    var COPY = {
        it: {
            title: 'Avvisami quando torna disponibile',
            desc: 'Ti scriviamo una sola volta, appena rientra in magazzino.',
            placeholder: 'La tua email',
            submit: 'Avvisami',
            sending: 'Invio…',
            privacy: 'Il tuo indirizzo viene usato solo per questo avviso e cancellato dopo l’invio. Nessuna newsletter.',
            privacyLink: 'Privacy policy',
            ok: 'Fatto. Ti avvisiamo appena torna disponibile.',
            errEmail: 'Controlla l’indirizzo email.',
            errRate: 'Troppe richieste. Riprova fra qualche minuto.',
            errGeneric: 'Non è stato possibile registrare la richiesta. Riprova più tardi.',
            inStock: 'Buona notizia: è di nuovo disponibile. Ricarica la pagina.'
        },
        en: {
            title: 'Notify me when it is back in stock',
            desc: 'We write once, as soon as it is back in the warehouse.',
            placeholder: 'Your email',
            submit: 'Notify me',
            sending: 'Sending…',
            privacy: 'Your address is used only for this alert and deleted after sending. No newsletter.',
            privacyLink: 'Privacy policy',
            ok: 'Done. We will let you know as soon as it is back.',
            errEmail: 'Please check the email address.',
            errRate: 'Too many requests. Try again in a few minutes.',
            errGeneric: 'We could not register your request. Please try again later.',
            inStock: 'Good news: it is available again. Please reload the page.'
        },
        de: {
            title: 'Benachrichtigen, wenn wieder verfügbar',
            desc: 'Wir schreiben Ihnen einmal, sobald der Artikel wieder auf Lager ist.',
            placeholder: 'Ihre E-Mail',
            submit: 'Benachrichtigen',
            sending: 'Wird gesendet…',
            privacy: 'Ihre Adresse wird nur für diese Benachrichtigung verwendet und danach gelöscht. Kein Newsletter.',
            privacyLink: 'Datenschutz',
            ok: 'Erledigt. Wir melden uns, sobald der Artikel wieder da ist.',
            errEmail: 'Bitte prüfen Sie die E-Mail-Adresse.',
            errRate: 'Zu viele Anfragen. Bitte in einigen Minuten erneut versuchen.',
            errGeneric: 'Die Anfrage konnte nicht gespeichert werden. Bitte später erneut versuchen.',
            inStock: 'Gute Nachricht: wieder verfügbar. Bitte laden Sie die Seite neu.'
        },
        fr: {
            title: 'Prévenez-moi du retour en stock',
            desc: 'Nous vous écrivons une seule fois, dès le retour en stock.',
            placeholder: 'Votre e-mail',
            submit: 'Prévenez-moi',
            sending: 'Envoi…',
            privacy: 'Votre adresse sert uniquement à cette alerte et est supprimée après l’envoi. Pas de newsletter.',
            privacyLink: 'Politique de confidentialité',
            ok: 'C’est fait. Nous vous préviendrons dès son retour.',
            errEmail: 'Vérifiez l’adresse e-mail.',
            errRate: 'Trop de demandes. Réessayez dans quelques minutes.',
            errGeneric: 'Impossible d’enregistrer la demande. Réessayez plus tard.',
            inStock: 'Bonne nouvelle : de nouveau disponible. Rechargez la page.'
        },
        es: {
            title: 'Avísame cuando vuelva a estar disponible',
            desc: 'Te escribimos una sola vez, en cuanto vuelva al almacén.',
            placeholder: 'Tu correo electrónico',
            submit: 'Avísame',
            sending: 'Enviando…',
            privacy: 'Tu dirección se usa solo para este aviso y se elimina tras el envío. Sin newsletter.',
            privacyLink: 'Política de privacidad',
            ok: 'Listo. Te avisamos en cuanto vuelva a estar disponible.',
            errEmail: 'Revisa la dirección de correo.',
            errRate: 'Demasiadas solicitudes. Inténtalo en unos minutos.',
            errGeneric: 'No se ha podido registrar la solicitud. Inténtalo más tarde.',
            inStock: 'Buenas noticias: vuelve a estar disponible. Recarga la página.'
        },
        nl: {
            title: 'Waarschuw mij bij nieuwe voorraad',
            desc: 'We schrijven je één keer, zodra het artikel weer op voorraad is.',
            placeholder: 'Je e-mailadres',
            submit: 'Waarschuw mij',
            sending: 'Versturen…',
            privacy: 'Je adres wordt alleen voor deze melding gebruikt en daarna verwijderd. Geen nieuwsbrief.',
            privacyLink: 'Privacybeleid',
            ok: 'Klaar. We laten het weten zodra het er weer is.',
            errEmail: 'Controleer het e-mailadres.',
            errRate: 'Te veel verzoeken. Probeer het over een paar minuten opnieuw.',
            errGeneric: 'We konden je verzoek niet registreren. Probeer het later opnieuw.',
            inStock: 'Goed nieuws: weer op voorraad. Laad de pagina opnieuw.'
        },
        pt: {
            title: 'Avisar quando estiver disponível',
            desc: 'Escrevemos uma só vez, assim que voltar ao armazém.',
            placeholder: 'O seu e-mail',
            submit: 'Avisar-me',
            sending: 'A enviar…',
            privacy: 'O seu endereço é usado apenas para este aviso e eliminado após o envio. Sem newsletter.',
            privacyLink: 'Política de privacidade',
            ok: 'Feito. Avisamos assim que estiver disponível.',
            errEmail: 'Verifique o endereço de e-mail.',
            errRate: 'Demasiados pedidos. Tente novamente dentro de alguns minutos.',
            errGeneric: 'Não foi possível registar o pedido. Tente mais tarde.',
            inStock: 'Boa notícia: está novamente disponível. Recarregue a página.'
        }
    };

    function pageLang() {
        var lang = String(document.documentElement.lang || 'it').toLowerCase().slice(0, 2);
        return COPY[lang] ? lang : 'it';
    }

    function track(eventName, sku) {
        try {
            fetch('/api/track', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ event: eventName, sku: sku }),
                keepalive: true,
            }).catch(function () { /* la telemetria non disturba la pagina */ });
        } catch (_) { /* noop */ }
    }

    function buildRestockForm(sku) {
        if (document.querySelector('.v2-restock')) return;

        var anchor = document.getElementById('product-primary-cta')
            || document.querySelector('[data-cart-add]');
        if (!anchor || !anchor.parentNode) return;

        var lang = pageLang();
        var t = COPY[lang];

        var box = document.createElement('div');
        box.className = 'v2-restock';
        box.innerHTML =
            '<p class="v2-restock__title">' + t.title + '</p>' +
            '<p class="v2-restock__desc">' + t.desc + '</p>' +
            '<form class="v2-restock__form" novalidate>' +
                '<label class="visually-hidden" for="restock-email">' + t.placeholder + '</label>' +
                '<input class="v2-restock__input" id="restock-email" type="email" name="email" ' +
                    'autocomplete="email" required placeholder="' + t.placeholder + '">' +
                '<input class="v2-restock__hp" type="text" name="website" tabindex="-1" ' +
                    'autocomplete="off" aria-hidden="true">' +
                '<button class="v2-restock__btn" type="submit">' + t.submit + '</button>' +
            '</form>' +
            '<p class="v2-restock__privacy">' + t.privacy +
                ' <a href="/' + lang + '/privacy-policy">' + t.privacyLink + '</a></p>' +
            '<p class="v2-restock__msg" role="status" aria-live="polite"></p>';

        anchor.parentNode.insertBefore(box, anchor.nextSibling);

        var form = box.querySelector('form');
        var input = box.querySelector('.v2-restock__input');
        var btn = box.querySelector('.v2-restock__btn');
        var msg = box.querySelector('.v2-restock__msg');
        var hp = box.querySelector('.v2-restock__hp');

        function say(text, state) {
            msg.textContent = text;
            msg.setAttribute('data-state', state);
        }

        form.addEventListener('submit', function (ev) {
            ev.preventDefault();
            var email = String(input.value || '').trim();
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
                say(t.errEmail, 'error');
                input.focus();
                return;
            }

            btn.disabled = true;
            btn.textContent = t.sending;
            say('', 'idle');

            fetch('/api/restock-request', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({
                    sku: sku,
                    email: email,
                    lang: lang,
                    privacy: true,
                    sourcePath: location.pathname,
                    website: hp ? hp.value : '',
                }),
            })
                .then(function (res) {
                    return res.json().catch(function () { return {}; })
                        .then(function (data) { return { status: res.status, data: data }; });
                })
                .then(function (r) {
                    if (r.status === 200 && r.data && r.data.ok) {
                        form.hidden = true;
                        say(t.ok, 'ok');
                        track('restock_request', sku);
                        return;
                    }
                    if (r.status === 409) {
                        say(t.inStock, 'error');
                    } else if (r.status === 429) {
                        say(t.errRate, 'error');
                    } else if (r.status === 400) {
                        say(t.errEmail, 'error');
                    } else {
                        say(t.errGeneric, 'error');
                    }
                    btn.disabled = false;
                    btn.textContent = t.submit;
                })
                .catch(function () {
                    say(t.errGeneric, 'error');
                    btn.disabled = false;
                    btn.textContent = t.submit;
                });
        });

        track('restock_view', sku);
    }

    function applyQty(el, qty, sku) {
        var q = Math.max(0, Math.floor(Number(qty) || 0));
        if (q <= 0) {
            setStatus(el, 'out', tpl(el, 'out', 0));
            setCtasDisabled(true);
            updateJsonLd(false);
            buildRestockForm(sku);
            return;
        }
        setCtasDisabled(false);
        updateJsonLd(true);
        if (q <= LOW_MAX) {
            setStatus(el, 'low', tpl(el, 'low', q));
        } else {
            setStatus(el, 'ok', tpl(el, 'available', q));
        }
    }

    function run() {
        var root = pricingRoot();
        if (!root) return;
        var el = stockEl(root);
        if (!el) return;
        var sku = String(
            root.getAttribute('data-stripe-product-sku') ||
            (root.dataset && root.dataset.stripeProductSku) ||
            ''
        ).trim();
        if (!sku) {
            setStatus(el, 'error', tpl(el, 'error', 0));
            return;
        }

        fetch('/api/stock?sku=' + encodeURIComponent(sku), {
            credentials: 'same-origin',
            headers: { Accept: 'application/json' },
        })
            .then(function (res) {
                if (!res.ok) throw new Error('stock ' + res.status);
                return res.json();
            })
            .then(function (data) {
                applyQty(el, data && data.qty, sku);
            })
            .catch(function () {
                setStatus(el, 'error', tpl(el, 'error', 0));
                /* CTA resta attiva: non bloccare vendita su fallimento rete */
            });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', run);
    } else {
        run();
    }
})();
