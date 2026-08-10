/**
 * Banner "questa pagina esiste anche in <tua lingua>", non un redirect.
 * Confronta la lingua del browser con quella della pagina corrente e, se
 * differiscono, propone il link alla pagina equivalente (via AmlSite.hrefSwitchLocale).
 * Mostrato al massimo una volta a sessione; il rifiuto esplicito è permanente
 * per quella lingua (localStorage, nessun cookie HTTP).
 */
(function () {
    'use strict';

    var DISMISSED_KEY = 'aml-lang-suggest-dismissed';
    var SESSION_SEEN_KEY = 'aml-lang-suggest-seen';

    var ENDONYMS = { it: 'Italiano', en: 'English', fr: 'Français', de: 'Deutsch', es: 'Español' };
    var FLAG_CODES = { it: 'it', en: 'gb', fr: 'fr', de: 'de', es: 'es' };

    var BAR_I18N = {
        it: {
            message: 'Questa pagina è disponibile anche nella tua lingua.',
            switchCta: '{{lang}}',
            dismissAria: 'Chiudi suggerimento lingua',
        },
        en: {
            message: 'This page is also available in your language.',
            switchCta: '{{lang}}',
            dismissAria: 'Dismiss language suggestion',
        },
        fr: {
            message: 'Cette page est aussi disponible dans votre langue.',
            switchCta: '{{lang}}',
            dismissAria: 'Fermer la suggestion de langue',
        },
        de: {
            message: 'Diese Seite ist auch in Ihrer Sprache verfügbar.',
            switchCta: '{{lang}}',
            dismissAria: 'Sprachvorschlag schließen',
        },
        es: {
            message: 'Esta página también está disponible en tu idioma.',
            switchCta: '{{lang}}',
            dismissAria: 'Cerrar sugerencia de idioma',
        },
    };

    function esc(text) {
        var S = window.AmlSite;
        if (S && typeof S.escapeHtmlAttr === 'function') return S.escapeHtmlAttr(text);
        return String(text)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function readDismissed() {
        try {
            var raw = localStorage.getItem(DISMISSED_KEY);
            var parsed = raw ? JSON.parse(raw) : [];
            return Array.isArray(parsed) ? parsed : [];
        } catch (_) {
            return [];
        }
    }

    function persistDismissed(langCode) {
        try {
            var list = readDismissed();
            if (list.indexOf(langCode) === -1) list.push(langCode);
            localStorage.setItem(DISMISSED_KEY, JSON.stringify(list));
        } catch (_) {
            /* private mode etc. */
        }
    }

    function alreadySeenThisSession() {
        try {
            return sessionStorage.getItem(SESSION_SEEN_KEY) === '1';
        } catch (_) {
            return false;
        }
    }

    function markSeenThisSession() {
        try {
            sessionStorage.setItem(SESSION_SEEN_KEY, '1');
        } catch (_) {
            /* ignore */
        }
    }

    /** Prima lingua tra quelle preferite dal browser che il sito supporta. */
    function topSupportedBrowserLang(supportedCodes) {
        var prefs = (navigator.languages && navigator.languages.length)
            ? navigator.languages
            : [navigator.language || ''];
        for (var i = 0; i < prefs.length; i++) {
            var primary = String(prefs[i] || '').split('-')[0].toLowerCase();
            if (supportedCodes.indexOf(primary) !== -1) return primary;
        }
        return null;
    }

    class AmlLangSuggest extends HTMLElement {
        constructor() {
            super();
            this.attachShadow({ mode: 'open' });
        }

        connectedCallback() {
            if (this.__init) return;
            this.__init = true;
            this.__compute();
        }

        __compute() {
            var S = window.AmlSite;
            if (!S || typeof S.parseLocalePath !== 'function') return;
            if (alreadySeenThisSession()) return;

            var parsed = S.parseLocalePath(window.location.pathname);
            var currentLang = parsed.langCode;
            var supportedCodes = S.LANGS.map(function (l) { return l.code; });

            var suggested = topSupportedBrowserLang(supportedCodes);
            if (!suggested || suggested === currentLang) return;
            if (readDismissed().indexOf(suggested) !== -1) return;

            var href = S.hrefSwitchLocale(
                parsed.pathPrefix, suggested, parsed.pathAfterLang,
                window.location.search, window.location.hash
            );

            this.__render(suggested, href);
            markSeenThisSession();
        }

        __render(suggested, href) {
            // Il testo va nella lingua SUGGERITA, non in quella della pagina corrente:
            // chi legge questo banner è, per definizione, un visitatore la cui lingua
            // preferita non è quella in cui la pagina è già scritta.
            var t = BAR_I18N[suggested] || BAR_I18N.it;
            var endonym = ENDONYMS[suggested] || suggested.toUpperCase();
            var flagCode = FLAG_CODES[suggested] || suggested;
            var ctaLabel = t.switchCta.replace('{{lang}}', endonym);

            var host = this;
            var root = this.shadowRoot;

            root.innerHTML =
                '<style>' +
                ':host{--ls-bg:#101827;--ls-bg-2:#0a101d;--ls-border:rgba(255,255,255,.1);--ls-text:#f4f6fb;' +
                '--ls-muted:#aab2c5;--ls-accent:#3b82f6;--ls-accent-hover:#5b9bf7;' +
                'font-family:"Montserrat",system-ui,sans-serif;display:block;' +
                'animation:ls-in .3s ease-out;}' +
                '@keyframes ls-in{from{opacity:0;transform:translateY(-100%);}to{opacity:1;transform:translateY(0);}}' +
                '.bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:.6rem 1rem;' +
                'padding:.65rem 2.75rem .65rem 1rem;' +
                'background:linear-gradient(135deg,var(--ls-bg) 0%,var(--ls-bg-2) 100%);' +
                'color:var(--ls-text);border-bottom:1px solid var(--ls-border);' +
                'box-shadow:0 4px 16px rgba(0,0,0,.25);position:relative;font-size:.85rem;line-height:1.4;' +
                'text-align:center;}' +
                '.msg{display:flex;align-items:center;gap:.55rem;color:var(--ls-muted);}' +
                '.flag{width:20px;height:20px;border-radius:50%;object-fit:cover;flex-shrink:0;' +
                'box-shadow:0 0 0 1px rgba(255,255,255,.25);}' +
                'a.switch{display:inline-flex;align-items:center;gap:.4rem;color:#fff;font-weight:700;' +
                'text-decoration:none;white-space:nowrap;background:var(--ls-accent);' +
                'padding:.4rem .85rem;border-radius:6px;transition:background .15s ease,transform .15s ease;}' +
                'a.switch:hover{background:var(--ls-accent-hover);transform:translateY(-1px);}' +
                'a.switch .arrow{transition:transform .15s ease;}' +
                'a.switch:hover .arrow{transform:translateX(2px);}' +
                '.dismiss{position:absolute;right:.5rem;top:50%;transform:translateY(-50%);' +
                'background:transparent;border:none;color:var(--ls-text);opacity:.55;cursor:pointer;' +
                'width:30px;height:30px;font-size:1.15rem;line-height:1;border-radius:50%;' +
                'transition:opacity .15s ease,background .15s ease;}' +
                '.dismiss:hover{opacity:1;background:rgba(255,255,255,.1);}' +
                '.dismiss:focus-visible,a.switch:focus-visible{outline:2px solid var(--ls-accent-hover);outline-offset:2px;}' +
                '@media (prefers-reduced-motion: reduce){:host{animation:none;}}' +
                '</style>' +
                '<div class="bar" role="status">' +
                '<span class="msg">' +
                '<img class="flag" src="/images/flags/' + esc(flagCode) + '.svg" alt="" decoding="async">' +
                esc(t.message) +
                '</span>' +
                '<a class="switch" href="' + esc(href) + '">' + esc(ctaLabel) + '<span class="arrow">→</span></a>' +
                '<button type="button" class="dismiss" aria-label="' + esc(t.dismissAria) + '">×</button>' +
                '</div>';

            root.querySelector('.dismiss').addEventListener('click', function () {
                persistDismissed(suggested);
                host.remove();
            });
        }
    }

    if (!customElements.get('aml-lang-suggest')) {
        customElements.define('aml-lang-suggest', AmlLangSuggest);
    }
})();
