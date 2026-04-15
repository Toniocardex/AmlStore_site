(function () {
    'use strict';

    var STORAGE_KEY = 'aml-consent-v2';

    var CONSENT_REJECT = {
        ad_storage: 'denied',
        ad_user_data: 'denied',
        ad_personalization: 'denied',
        analytics_storage: 'denied',
        functionality_storage: 'denied',
        personalization_storage: 'denied',
    };

    var CONSENT_ACCEPT = {
        ad_storage: 'granted',
        ad_user_data: 'granted',
        ad_personalization: 'granted',
        analytics_storage: 'granted',
        functionality_storage: 'granted',
        personalization_storage: 'granted',
    };

    var BANNER_I18N = {
        it: {
            title: 'Cookie e preferenze sulla privacy',
            body:
                'Usiamo cookie e tecnologie simili per funzioni essenziali del sito, misurare le visite e, solo con il tuo consenso, marketing e personalizzazione. Puoi modificare le scelte in ogni momento.',
            policyLink: 'Cookie policy',
            reject: 'Rifiuta non essenziali',
            customize: 'Personalizza',
            accept: 'Accetta tutto',
            save: 'Salva preferenze',
            catAnalytics: 'Misurazione e statistiche (analytics_storage)',
            catAds: 'Marketing e pubblicità (ad_storage, ad_user_data, ad_personalization)',
            catFunc: 'Funzionalità e personalizzazione locale (functionality_storage, personalization_storage)',
            policyHref: 'cookie-policy.html',
        },
        en: {
            title: 'Cookies and privacy preferences',
            body:
                'We use cookies and similar technologies for essential site features, audience measurement, and—with your consent—marketing and personalization. You can change your choices at any time.',
            policyLink: 'Cookie policy',
            reject: 'Reject non-essential',
            customize: 'Customize',
            accept: 'Accept all',
            save: 'Save preferences',
            catAnalytics: 'Measurement and statistics (analytics_storage)',
            catAds: 'Marketing and advertising (ad_storage, ad_user_data, ad_personalization)',
            catFunc: 'Functionality and personalization (functionality_storage, personalization_storage)',
            policyHref: 'cookie-policy.html',
        },
        fr: {
            title: 'Cookies et préférences de confidentialité',
            body:
                "Nous utilisons des cookies et technologies similaires pour le fonctionnement du site, la mesure d'audience et, avec votre consentement, le marketing et la personnalisation. Vous pouvez modifier vos choix à tout moment.",
            policyLink: 'Politique cookies',
            reject: 'Refuser le non essentiel',
            customize: 'Personnaliser',
            accept: 'Tout accepter',
            save: 'Enregistrer les préférences',
            catAnalytics: 'Mesure et statistiques (analytics_storage)',
            catAds: 'Marketing et publicité (ad_storage, ad_user_data, ad_personalization)',
            catFunc: 'Fonctionnalités et personnalisation (functionality_storage, personalization_storage)',
            policyHref: 'cookie-policy.html',
        },
        de: {
            title: 'Cookies und Datenschutzeinstellungen',
            body:
                'Wir verwenden Cookies und ähnliche Technologien für notwendige Funktionen, Reichweitenmessung und—mit Ihrer Einwilligung—Marketing und Personalisierung. Sie können Ihre Auswahl jederzeit ändern.',
            policyLink: 'Cookie-Richtlinie',
            reject: 'Nicht notwendige ablehnen',
            customize: 'Anpassen',
            accept: 'Alle akzeptieren',
            save: 'Einstellungen speichern',
            catAnalytics: 'Messung und Statistik (analytics_storage)',
            catAds: 'Marketing und Werbung (ad_storage, ad_user_data, ad_personalization)',
            catFunc: 'Funktionalität und Personalisierung (functionality_storage, personalization_storage)',
            policyHref: 'cookie-policy.html',
        },
        es: {
            title: 'Cookies y preferencias de privacidad',
            body:
                'Usamos cookies y tecnologías similares para funciones esenciales, medición de audiencia y, con su consentimiento, marketing y personalización. Puede cambiar sus decisiones en cualquier momento.',
            policyLink: 'Política de cookies',
            reject: 'Rechazar lo no esencial',
            customize: 'Personalizar',
            accept: 'Aceptar todo',
            save: 'Guardar preferencias',
            catAnalytics: 'Medición y estadísticas (analytics_storage)',
            catAds: 'Marketing y publicidad (ad_storage, ad_user_data, ad_personalization)',
            catFunc: 'Funcionalidad y personalización (functionality_storage, personalization_storage)',
            policyHref: 'cookie-policy.html',
        },
    };

    function langCode() {
        var S = window.AmlSite;
        if (S && typeof S.parseLocalePath === 'function') {
            try {
                return S.parseLocalePath(window.location.pathname).langCode || 'it';
            } catch (_) {
                /* fall through */
            }
        }
        var lang = (document.documentElement.getAttribute('lang') || 'it').slice(0, 2).toLowerCase();
        return BANNER_I18N[lang] ? lang : 'it';
    }

    function esc(text) {
        var S = window.AmlSite;
        if (S && typeof S.escapeHtmlAttr === 'function') return S.escapeHtmlAttr(text);
        return String(text)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function persist(consent) {
        var payload = { version: 2, consent: consent, savedAt: new Date().toISOString() };
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
        } catch (_) {
            /* private mode etc. */
        }
        if (typeof window.gtag === 'function') {
            window.gtag('consent', 'update', consent);
        }
    }

    function readStored() {
        try {
            var raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) return null;
            var parsed = JSON.parse(raw);
            if (!parsed || !parsed.consent) return null;
            return parsed.consent;
        } catch (_) {
            return null;
        }
    }

    function togglesFromConsent(c) {
        if (!c) return { analytics: false, ads: false, func: false };
        return {
            analytics: c.analytics_storage === 'granted',
            ads: c.ad_storage === 'granted',
            func: c.functionality_storage === 'granted',
        };
    }

    function consentFromToggles(analytics, ads, func) {
        return {
            ad_storage: ads ? 'granted' : 'denied',
            ad_user_data: ads ? 'granted' : 'denied',
            ad_personalization: ads ? 'granted' : 'denied',
            analytics_storage: analytics ? 'granted' : 'denied',
            functionality_storage: func ? 'granted' : 'denied',
            personalization_storage: func ? 'granted' : 'denied',
        };
    }

    class AmlCookieBanner extends HTMLElement {
        constructor() {
            super();
            this.attachShadow({ mode: 'open' });
            this.__openCustomize = false;
            this.__forceVisible = false;
        }

        connectedCallback() {
            if (this.__init) return;
            this.__init = true;
            this.render();
            window.addEventListener('aml-open-cookie-settings', this.__onOpenSettings);
        }

        disconnectedCallback() {
            window.removeEventListener('aml-open-cookie-settings', this.__onOpenSettings);
        }

        __onOpenSettings = () => {
            this.__forceVisible = true;
            this.__openCustomize = true;
            this.render();
            this.__focusFirst();
        };

        openSettings() {
            this.__onOpenSettings();
        }

        __focusFirst() {
            var root = this.shadowRoot;
            if (!root) return;
            requestAnimationFrame(function () {
                var btn = root.querySelector('.btn-primary, .btn-ghost');
                if (btn) btn.focus();
            });
        }

        render() {
            var code = langCode();
            var t = BANNER_I18N[code] || BANNER_I18N.it;
            var stored = readStored();
            var hasChoice = !!stored && !this.__forceVisible;
            var toggles = togglesFromConsent(stored);

            if (hasChoice) {
                this.setAttribute('hidden', '');
            } else {
                this.removeAttribute('hidden');
            }

            this.shadowRoot.innerHTML =
                '\n            <style>\n                :host {\n                    --cb-bg: rgba(10, 10, 10, 0.92);\n                    --cb-border: rgba(255, 255, 255, 0.12);\n                    --cb-text: #fafafa;\n                    --cb-muted: #a1a1aa;\n                    --cb-accent: #3b82f6;\n                    --cb-accent-hover: #60a5fa;\n                    font-family: "Montserrat", system-ui, sans-serif;\n                    position: fixed;\n                    left: 0;\n                    right: 0;\n                    bottom: 0;\n                    z-index: 10050;\n                    display: block;\n                    pointer-events: none;\n                }\n                :host([hidden]) { display: none !important; }\n                .panel {\n                    pointer-events: auto;\n                    margin: 0 auto max(0.75rem, env(safe-area-inset-bottom));\n                    max-width: min(960px, calc(100vw - 1.5rem));\n                    background: var(--cb-bg);\n                    color: var(--cb-text);\n                    border: 1px solid var(--cb-border);\n                    border-radius: 14px;\n                    box-shadow: 0 -8px 40px rgba(0, 0, 0, 0.45);\n                    backdrop-filter: blur(14px);\n                    -webkit-backdrop-filter: blur(14px);\n                    padding: 1.25rem clamp(1rem, 3vw, 1.5rem);\n                }\n                .head {\n                    display: flex;\n                    flex-wrap: wrap;\n                    align-items: flex-start;\n                    justify-content: space-between;\n                    gap: 0.75rem 1rem;\n                    margin-bottom: 0.75rem;\n                }\n                h2 {\n                    margin: 0;\n                    font-size: 1.05rem;\n                    font-weight: 800;\n                    letter-spacing: -0.02em;\n                    line-height: 1.3;\n                    max-width: 42ch;\n                }\n                p {\n                    margin: 0 0 1rem;\n                    font-size: 0.875rem;\n                    line-height: 1.55;\n                    color: var(--cb-muted);\n                    max-width: 72ch;\n                }\n                .policy {\n                    font-size: 0.85rem;\n                    margin-bottom: 1rem;\n                }\n                .policy a {\n                    color: var(--cb-accent);\n                    font-weight: 600;\n                    text-decoration: underline;\n                    text-underline-offset: 2px;\n                }\n                .policy a:hover { color: var(--cb-accent-hover); }\n                .actions {\n                    display: flex;\n                    flex-wrap: wrap;\n                    gap: 0.5rem;\n                    align-items: center;\n                }\n                button {\n                    font-family: inherit;\n                    font-size: 0.85rem;\n                    font-weight: 700;\n                    border-radius: 999px;\n                    padding: 0.65rem 1.1rem;\n                    cursor: pointer;\n                    border: 1px solid transparent;\n                    min-height: 44px;\n                    transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;\n                }\n                .btn-primary {\n                    background: linear-gradient(135deg, #fff 0%, #e4e4e7 100%);\n                    color: #0a0a0a;\n                }\n                .btn-primary:hover { filter: brightness(1.05); }\n                .btn-secondary {\n                    background: rgba(255, 255, 255, 0.08);\n                    color: var(--cb-text);\n                    border-color: var(--cb-border);\n                }\n                .btn-secondary:hover { background: rgba(255, 255, 255, 0.12); }\n                .btn-ghost {\n                    background: transparent;\n                    color: var(--cb-muted);\n                    border-color: transparent;\n                    text-decoration: underline;\n                    text-underline-offset: 3px;\n                }\n                .btn-ghost:hover { color: var(--cb-text); }\n                .custom {\n                    margin-top: 1rem;\n                    padding-top: 1rem;\n                    border-top: 1px solid var(--cb-border);\n                    display: none;\n                }\n                .custom.open { display: block; }\n                .row {\n                    display: flex;\n                    align-items: flex-start;\n                    gap: 0.75rem;\n                    margin-bottom: 0.85rem;\n                }\n                .row label {\n                    font-size: 0.8rem;\n                    line-height: 1.45;\n                    color: var(--cb-muted);\n                    cursor: pointer;\n                }\n                input[type="checkbox"] {\n                    width: 1.15rem;\n                    height: 1.15rem;\n                    margin-top: 0.15rem;\n                    accent-color: var(--cb-accent);\n                    flex-shrink: 0;\n                }\n                .save-row { margin-top: 0.75rem; }\n                button:focus-visible {\n                    outline: 2px solid var(--cb-accent);\n                    outline-offset: 2px;\n                }\n                @media (prefers-reduced-motion: reduce) {\n                    button { transition: none; }\n                }\n            </style>\n            <div class="panel" role="dialog" aria-modal="true" aria-labelledby="aml-cb-title">\n                <div class="head">\n                    <h2 id="aml-cb-title">' +
                esc(t.title) +
                '</h2>\n                </div>\n                <p>' +
                esc(t.body) +
                '</p>\n                <div class="policy"><a href="' +
                esc(t.policyHref) +
                '">' +
                esc(t.policyLink) +
                '</a></div>\n                <div class="actions">\n                    <button type="button" class="btn-secondary" data-act="reject">' +
                esc(t.reject) +
                '</button>\n                    <button type="button" class="btn-secondary" data-act="custom">' +
                esc(t.customize) +
                '</button>\n                    <button type="button" class="btn-primary" data-act="accept">' +
                esc(t.accept) +
                '</button>\n                </div>\n                <div class="custom' +
                (this.__openCustomize ? ' open' : '') +
                '" id="aml-cb-custom">\n                    <div class="row">\n                        <input type="checkbox" id="aml-cb-an" data-toggle="analytics"' +
                (toggles.analytics ? ' checked' : '') +
                '>\n                        <label for="aml-cb-an">' +
                esc(t.catAnalytics) +
                '</label>\n                    </div>\n                    <div class="row">\n                        <input type="checkbox" id="aml-cb-ad" data-toggle="ads"' +
                (toggles.ads ? ' checked' : '') +
                '>\n                        <label for="aml-cb-ad">' +
                esc(t.catAds) +
                '</label>\n                    </div>\n                    <div class="row">\n                        <input type="checkbox" id="aml-cb-fn" data-toggle="func"' +
                (toggles.func ? ' checked' : '') +
                '>\n                        <label for="aml-cb-fn">' +
                esc(t.catFunc) +
                '</label>\n                    </div>\n                    <div class="save-row">\n                        <button type="button" class="btn-primary" data-act="save">' +
                esc(t.save) +
                '</button>\n                    </div>\n                </div>\n            </div>\n        ';

            var host = this;
            var root = this.shadowRoot;

            function closeBanner() {
                host.__forceVisible = false;
                host.__openCustomize = false;
                host.setAttribute('hidden', '');
            }

            function openCustomize() {
                host.__openCustomize = true;
                var box = root.querySelector('#aml-cb-custom');
                if (box) box.classList.add('open');
            }

            root.querySelector('[data-act="reject"]')?.addEventListener('click', function () {
                persist(CONSENT_REJECT);
                closeBanner();
            });

            root.querySelector('[data-act="accept"]')?.addEventListener('click', function () {
                persist(CONSENT_ACCEPT);
                closeBanner();
            });

            root.querySelector('[data-act="custom"]')?.addEventListener('click', function () {
                openCustomize();
            });

            root.querySelector('[data-act="save"]')?.addEventListener('click', function () {
                var an = !!root.querySelector('#aml-cb-an')?.checked;
                var ad = !!root.querySelector('#aml-cb-ad')?.checked;
                var fn = !!root.querySelector('#aml-cb-fn')?.checked;
                persist(consentFromToggles(an, ad, fn));
                closeBanner();
            });
        }
    }

    if (!customElements.get('aml-cookie-banner')) {
        customElements.define('aml-cookie-banner', AmlCookieBanner);
    }

    window.AmlCookieConsent = {
        open: function () {
            var el = document.querySelector('aml-cookie-banner');
            if (el && typeof el.openSettings === 'function') el.openSettings();
            else window.dispatchEvent(new CustomEvent('aml-open-cookie-settings'));
        },
    };
})();
