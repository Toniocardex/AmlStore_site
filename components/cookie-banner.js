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
            title: 'Preferenze sui cookie e privacy',
            body: 'Utilizziamo cookie e tecnologie simili per garantire le funzionalità essenziali del sito, misurare il traffico e, con il tuo consenso, personalizzare contenuti e offerte commerciali.',
            policyLink: 'Informativa sui cookie',
            reject: 'Rifiuta non essenziali',
            customize: 'Personalizza',
            accept: 'Accetta tutti',
            save: 'Salva preferenze',
            back: 'Indietro',
            customTitle: 'Personalizza le tue preferenze',
            customDesc: 'Scegli quali categorie di cookie desideri autorizzare. Puoi modificare queste impostazioni in qualsiasi momento.',
            alwaysActive: 'Sempre attivi',
            catEssentialTitle: 'Cookie tecnici ed essenziali',
            catEssentialDesc: 'Indispensabili per il funzionamento del sito, del carrello e della sicurezza.',
            catAnalyticsTitle: 'Misurazione e statistiche',
            catAnalyticsDesc: 'Ci permettono di analizzare in forma aggregata l\'uso del sito per migliorarne prestazioni e usabilità.',
            catAdsTitle: 'Marketing e profilazione',
            catAdsDesc: 'Utilizzati per mostrare annunci pertinenti alle tue preferenze e valutare l\'efficacia delle campagne.',
            catFuncTitle: 'Funzionalità e preferenze',
            catFuncDesc: 'Memorizzano impostazioni come lingua, valuta e preferenze di navigazione.',
            policyHref: 'cookie-policy',
        },
        en: {
            title: 'Cookie and privacy preferences',
            body: 'We use cookies and similar technologies to ensure essential site features, analyze traffic, and—with your consent—tailor content and advertising to your interests.',
            policyLink: 'Cookie policy',
            reject: 'Reject non-essential',
            customize: 'Customize',
            accept: 'Accept all',
            save: 'Save preferences',
            back: 'Back',
            customTitle: 'Customize your preferences',
            customDesc: 'Choose which cookie categories you want to allow. You can update these settings at any time.',
            alwaysActive: 'Always active',
            catEssentialTitle: 'Essential technical cookies',
            catEssentialDesc: 'Required for basic site operation, shopping cart, and platform security.',
            catAnalyticsTitle: 'Analytics and performance',
            catAnalyticsDesc: 'Help us understand how visitors interact with the store to improve user experience.',
            catAdsTitle: 'Marketing and advertising',
            catAdsDesc: 'Used to deliver relevant offers and measure the performance of advertising campaigns.',
            catFuncTitle: 'Functionality and preferences',
            catFuncDesc: 'Remember user selections such as language, region, and layout settings.',
            policyHref: 'cookie-policy',
        },
        fr: {
            title: 'Préférences de cookies et confidentialité',
            body: 'Nous utilisons des cookies pour assurer le bon fonctionnement du site, mesurer l\'audience et, avec votre accord, vous proposer des contenus et offres personnalisés.',
            policyLink: 'Politique de cookies',
            reject: 'Refuser les non-essentiels',
            customize: 'Personnaliser',
            accept: 'Tout accepter',
            save: 'Enregistrer mes choix',
            back: 'Retour',
            customTitle: 'Personnalisez vos préférences',
            customDesc: 'Sélectionnez les catégories de cookies que vous autorisez. Vous pouvez modifier votre choix à tout moment.',
            alwaysActive: 'Toujours actifs',
            catEssentialTitle: 'Cookies techniques indispensables',
            catEssentialDesc: 'Nécessaires au fonctionnement du panier, à la sécurité et à la navigation.',
            catAnalyticsTitle: 'Mesure d\'audience et statistiques',
            catAnalyticsDesc: 'Nous aident à évaluer l\'utilisation du site pour optimiser les fonctionnalités.',
            catAdsTitle: 'Marketing et publicité ciblée',
            catAdsDesc: 'Permettent de vous proposer des offres adaptées à vos centres d\'intérêt.',
            catFuncTitle: 'Fonctionnalités et personnalisation',
            catFuncDesc: 'Mémorisent vos préférences telles que la langue et la devise.',
            policyHref: 'cookie-policy',
        },
        de: {
            title: 'Cookie- und Datenschutzeinstellungen',
            body: 'Wir verwenden Cookies und ähnliche Technologien für den reibungslosen Betrieb der Website, Reichweitenmessung und—mit Ihrer Einwilligung—personalisierte Angebote.',
            policyLink: 'Cookie-Richtlinie',
            reject: 'Nicht essenzielle ablehnen',
            customize: 'Anpassen',
            accept: 'Alle akzeptieren',
            save: 'Einstellungen speichern',
            back: 'Zurück',
            customTitle: 'Präferenzen anpassen',
            customDesc: 'Wählen Sie aus, welche Cookie-Kategorien Sie aktivieren möchten. Sie können die Auswahl jederzeit ändern.',
            alwaysActive: 'Immer aktiv',
            catEssentialTitle: 'Technisch notwendige Cookies',
            catEssentialDesc: 'Unerlässlich für Warenkorbfunktionen, Nutzersitzungen und Sicherheit.',
            catAnalyticsTitle: 'Statistik und Reichweitenmessung',
            catAnalyticsDesc: 'Helfen uns zu verstehen, wie Besucher die Website nutzen, um sie stetig zu verbessern.',
            catAdsTitle: 'Marketing und Personalisierung',
            catAdsDesc: 'Ermöglichen relevante Angebote und unterstützen die Auswertung von Werbekampagnen.',
            catFuncTitle: 'Funktionalität und Komfort',
            catFuncDesc: 'Speichern ausgewählte Einstellungen wie Sprache und Anzeigepräferenzen.',
            policyHref: 'cookie-policy',
        },
        es: {
            title: 'Preferencias de cookies y privacidad',
            body: 'Utilizamos cookies y tecnologías similares para garantizar funciones esenciales, medir el rendimiento y, con su consentimiento, personalizar contenidos y publicidad.',
            policyLink: 'Política de cookies',
            reject: 'Rechazar no esenciales',
            customize: 'Personalizar',
            accept: 'Aceptar todo',
            save: 'Guardar preferencias',
            back: 'Volver',
            customTitle: 'Personalizar preferencias',
            customDesc: 'Seleccione qué categorías de cookies desea autorizar. Puede modificar su decisión en cualquier momento.',
            alwaysActive: 'Siempre activas',
            catEssentialTitle: 'Cookies técnicas y esenciales',
            catEssentialDesc: 'Imprescindibles para el carrito de compras, la seguridad y la navegación.',
            catAnalyticsTitle: 'Medición y estadísticas',
            catAnalyticsDesc: 'Nos permiten analizar de forma agregada el uso de la tienda para optimizarla.',
            catAdsTitle: 'Marketing y publicidad',
            catAdsDesc: 'Utilizadas para mostrar promociones relevantes y medir el impacto de campañas.',
            catFuncTitle: 'Funcionalidad y preferencias',
            catFuncDesc: 'Recuerdan ajustes locales como el idioma o la región seleccionada.',
            policyHref: 'cookie-policy',
        },
        pt: {
            title: 'Preferências de cookies e privacidade',
            body: 'Utilizamos cookies e tecnologias semelhantes para garantir o funcionamento essencial do site, medir o tráfego e, com o seu consentimento, personalizar anúncios e conteúdos.',
            policyLink: 'Política de cookies',
            reject: 'Rejeitar não essenciais',
            customize: 'Personalizar',
            accept: 'Aceitar tudo',
            save: 'Guardar preferências',
            back: 'Voltar',
            customTitle: 'Personalizar preferências',
            customDesc: 'Escolha quais categorias de cookies pretende autorizar. Pode alterar as suas preferências quando quiser.',
            alwaysActive: 'Sempre ativos',
            catEssentialTitle: 'Cookies técnicos e essenciais',
            catEssentialDesc: 'Indispensáveis para o funcionamento do carrinho, segurança e navegação.',
            catAnalyticsTitle: 'Estatísticas e medição',
            catAnalyticsDesc: 'Ajudam a compreender o comportamento de navegação para melhorar o serviço.',
            catAdsTitle: 'Marketing e publicidade',
            catAdsDesc: 'Utilizados para apresentar ofertas relevantes e avaliar campanhas.',
            catFuncTitle: 'Funcionalidade e preferências',
            catFuncDesc: 'Guardam definições como idioma, moeda e preferências do utilizador.',
            policyHref: 'cookie-policy',
        },
        nl: {
            title: 'Cookie- en privacyvoorkeuren',
            body: 'Wij gebruiken cookies en vergelijkbare technologieën voor essentiële sitefuncties, publieksmeting en—met uw toestemming—gepersonaliseerde inhoud en advertenties.',
            policyLink: 'Cookiebeleid',
            reject: 'Niet-essentiële weigeren',
            customize: 'Aanpassen',
            accept: 'Alles accepteren',
            save: 'Voorkeuren opslaan',
            back: 'Terug',
            customTitle: 'Voorkeuren aanpassen',
            customDesc: 'Kies welke categorieën cookies u wilt toestaan. U kunt uw instellingen op elk gewenst moment wijzigen.',
            alwaysActive: 'Altijd actief',
            catEssentialTitle: 'Essentiële technische cookies',
            catEssentialDesc: 'Noodzakelijk voor de winkelwagen, gebruikerssessie en beveiliging.',
            catAnalyticsTitle: 'Statistieken en analyse',
            catAnalyticsDesc: 'Helpen ons het gebruik van de site te analyseren om de ervaring te optimaliseren.',
            catAdsTitle: 'Marketing en advertenties',
            catAdsDesc: 'Gebruikt om relevante aanbiedingen te tonen en campagneresultaten te meten.',
            catFuncTitle: 'Functionaliteit en voorkeuren',
            catFuncDesc: 'Onthouden uw gekozen instellingen zoals taal en regio.',
            policyHref: 'cookie-policy',
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

    function getPolicyUrl(code) {
        var S = window.AmlSite;
        if (S && typeof S.staticRootFromScriptPath === 'function') {
            try {
                var root = S.staticRootFromScriptPath('/components/cookie-banner.js');
                return (root ? root : '') + '/' + code + '/cookie-policy';
            } catch (_) {}
        }
        return '/' + code + '/cookie-policy';
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
        try {
            window.dispatchEvent(new CustomEvent('aml-consent-updated', { detail: consent }));
        } catch (_) {
            /* ignore */
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
                var btn = root.querySelector('.btn-primary, .btn-secondary, .btn-outline, .btn-ghost');
                if (btn) btn.focus();
            });
        }

        render() {
            var code = langCode();
            var t = BANNER_I18N[code] || BANNER_I18N.it;
            var stored = readStored();
            var hasChoice = !!stored && !this.__forceVisible;
            var toggles = togglesFromConsent(stored);
            var policyUrl = getPolicyUrl(code);

            if (hasChoice) {
                this.setAttribute('hidden', '');
            } else {
                this.removeAttribute('hidden');
            }

            var shieldCookieSvg = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="M9 12l2 2 4-4"></path></svg>';
            var lockSvg = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>';
            var arrowRightSvg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"></path><path d="M12 5l7 7-7 7"></path></svg>';
            var arrowLeftSvg = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5"></path><path d="M12 19l-7-7 7-7"></path></svg>';

            this.shadowRoot.innerHTML =
                '\n            <style>\n                :host {\n                    --aml-cb-bg: #ffffff;\n                    --aml-cb-border: #e2e8f0;\n                    --aml-cb-title: #0f172a;\n                    --aml-cb-text: #475569;\n                    --aml-cb-text-muted: #64748b;\n                    --aml-cb-primary-grad: linear-gradient(135deg, #f05a10 0%, #ff7024 100%);\n                    --aml-cb-primary-hover: linear-gradient(135deg, #ff7024 0%, #ff8442 100%);\n                    --aml-cb-primary-shadow: 0 4px 14px rgba(240, 90, 16, 0.28);\n                    --aml-cb-accent: #f05a10;\n                    --aml-cb-card-bg: #f8fafc;\n                    --aml-cb-card-border: #e2e8f0;\n                    font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;\n                    position: fixed;\n                    left: 0;\n                    right: 0;\n                    bottom: 0;\n                    z-index: 10050;\n                    display: block;\n                    pointer-events: none;\n                    padding: 0 1rem clamp(0.75rem, 2vw, 1.25rem);\n                }\n                :host([hidden]) { display: none !important; }\n                \n                .panel {\n                    pointer-events: auto;\n                    margin: 0 auto max(0.5rem, env(safe-area-inset-bottom));\n                    max-width: 820px;\n                    background: var(--aml-cb-bg);\n                    color: var(--aml-cb-text);\n                    border: 1px solid var(--aml-cb-border);\n                    border-radius: 16px;\n                    box-shadow: 0 20px 45px -10px rgba(15, 23, 42, 0.18), 0 0 0 1px rgba(0, 0, 0, 0.04);\n                    padding: 1.35rem clamp(1.1rem, 2.8vw, 1.65rem);\n                    animation: amlCbSlideIn 0.32s cubic-bezier(0.16, 1, 0.3, 1) forwards;\n                    backdrop-filter: blur(12px);\n                    -webkit-backdrop-filter: blur(12px);\n                    transition: opacity 0.2s ease, transform 0.2s ease;\n                }\n                .panel.is-closing {\n                    opacity: 0;\n                    transform: translateY(12px);\n                }\n\n                @keyframes amlCbSlideIn {\n                    from {\n                        opacity: 0;\n                        transform: translateY(16px);\n                    }\n                    to {\n                        opacity: 1;\n                        transform: translateY(0);\n                    }\n                }\n\n                .view-main,\n                .view-custom {\n                    display: block;\n                }\n                .view-main.is-hidden,\n                .view-custom.is-hidden {\n                    display: none;\n                }\n\n                .head {\n                    display: flex;\n                    align-items: center;\n                    gap: 0.75rem;\n                    margin-bottom: 0.65rem;\n                }\n                .icon-badge {\n                    width: 36px;\n                    height: 36px;\n                    border-radius: 10px;\n                    background: #fff7ed;\n                    color: #f05a10;\n                    border: 1px solid #ffd1b3;\n                    display: flex;\n                    align-items: center;\n                    justify-content: center;\n                    flex-shrink: 0;\n                }\n                h2 {\n                    margin: 0;\n                    font-size: 1.05rem;\n                    font-weight: 700;\n                    letter-spacing: -0.015em;\n                    line-height: 1.3;\n                    color: var(--aml-cb-title);\n                }\n                .desc {\n                    margin: 0 0 0.85rem;\n                    font-size: 0.865rem;\n                    line-height: 1.55;\n                    color: var(--aml-cb-text);\n                }\n                .policy-wrap {\n                    display: inline-flex;\n                    align-items: center;\n                    margin-bottom: 1.15rem;\n                }\n                .policy-link {\n                    display: inline-flex;\n                    align-items: center;\n                    gap: 0.3rem;\n                    color: #f05a10;\n                    font-size: 0.84rem;\n                    font-weight: 600;\n                    text-decoration: none;\n                    transition: color 0.15s ease, transform 0.15s ease;\n                }\n                .policy-link:hover {\n                    color: #c74104;\n                    text-decoration: underline;\n                    text-underline-offset: 3px;\n                }\n                .policy-link svg {\n                    transition: transform 0.15s ease;\n                }\n                .policy-link:hover svg {\n                    transform: translateX(2px);\n                }\n\n                .actions {\n                    display: flex;\n                    flex-wrap: wrap;\n                    gap: 0.6rem;\n                    align-items: center;\n                    justify-content: flex-end;\n                }\n                .actions-left {\n                    display: flex;\n                    flex-wrap: wrap;\n                    gap: 0.6rem;\n                    margin-right: auto;\n                }\n                .actions-right {\n                    display: flex;\n                    flex-wrap: wrap;\n                    gap: 0.6rem;\n                }\n\n                button {\n                    font-family: inherit;\n                    font-size: 0.84rem;\n                    font-weight: 600;\n                    border-radius: 8px;\n                    padding: 0.6rem 1.15rem;\n                    cursor: pointer;\n                    border: 1px solid transparent;\n                    min-height: 42px;\n                    display: inline-flex;\n                    align-items: center;\n                    justify-content: center;\n                    gap: 0.4rem;\n                    transition: all 0.2s ease;\n                    user-select: none;\n                }\n                button:focus-visible {\n                    outline: 2px solid #f05a10;\n                    outline-offset: 2px;\n                }\n\n                .btn-primary {\n                    background: var(--aml-cb-primary-grad);\n                    color: #ffffff;\n                    font-weight: 700;\n                    box-shadow: var(--aml-cb-primary-shadow);\n                }\n                .btn-primary:hover {\n                    background: var(--aml-cb-primary-hover);\n                    box-shadow: 0 6px 18px rgba(240, 90, 16, 0.36);\n                    transform: translateY(-1px);\n                }\n                .btn-primary:active {\n                    transform: translateY(0);\n                }\n\n                .btn-secondary {\n                    background: #f1f5f9;\n                    color: #475569;\n                    border-color: #e2e8f0;\n                }\n                .btn-secondary:hover {\n                    background: #e2e8f0;\n                    color: #1e293b;\n                }\n\n                .btn-outline {\n                    background: #ffffff;\n                    color: #334155;\n                    border-color: #cbd5e1;\n                }\n                .btn-outline:hover {\n                    background: #f8fafc;\n                    border-color: #94a3b8;\n                    color: #0f172a;\n                }\n\n                .btn-ghost {\n                    background: transparent;\n                    color: #64748b;\n                    border-color: transparent;\n                    padding: 0.45rem 0.65rem;\n                    min-height: 36px;\n                    font-size: 0.82rem;\n                }\n                .btn-ghost:hover {\n                    color: #0f172a;\n                    background: #f1f5f9;\n                }\n\n                /* Customize View styling */\n                .custom-head {\n                    display: flex;\n                    align-items: center;\n                    justify-content: space-between;\n                    margin-bottom: 0.85rem;\n                    padding-bottom: 0.75rem;\n                    border-bottom: 1px solid var(--aml-cb-border);\n                    gap: 0.75rem;\n                }\n                .custom-head-title {\n                    display: flex;\n                    align-items: center;\n                    gap: 0.6rem;\n                }\n                .custom-categories {\n                    display: grid;\n                    grid-template-columns: 1fr;\n                    gap: 0.65rem;\n                    margin-bottom: 1.25rem;\n                    max-height: min(48vh, 360px);\n                    overflow-y: auto;\n                    padding-right: 0.25rem;\n                }\n                .cat-card {\n                    background: var(--aml-cb-card-bg);\n                    border: 1px solid var(--aml-cb-card-border);\n                    border-radius: 10px;\n                    padding: 0.85rem 1rem;\n                    display: flex;\n                    align-items: center;\n                    justify-content: space-between;\n                    gap: 1rem;\n                    transition: border-color 0.15s ease, background 0.15s ease;\n                    user-select: none;\n                }\n                .cat-card--toggle {\n                    cursor: pointer;\n                }\n                .cat-card:hover {\n                    border-color: #cbd5e1;\n                    background: #ffffff;\n                }\n                .cat-info {\n                    flex: 1;\n                }\n                .cat-title-row {\n                    display: flex;\n                    align-items: center;\n                    gap: 0.5rem;\n                    margin-bottom: 0.2rem;\n                }\n                .cat-title {\n                    font-size: 0.875rem;\n                    font-weight: 700;\n                    color: var(--aml-cb-title);\n                    margin: 0;\n                }\n                .cat-desc {\n                    font-size: 0.79rem;\n                    line-height: 1.45;\n                    color: var(--aml-cb-text-muted);\n                    margin: 0;\n                }\n                .badge-essential {\n                    display: inline-flex;\n                    align-items: center;\n                    gap: 0.25rem;\n                    font-size: 0.72rem;\n                    font-weight: 700;\n                    color: #166534;\n                    background: #dcfce7;\n                    border: 1px solid #bbf7d0;\n                    padding: 0.15rem 0.5rem;\n                    border-radius: 6px;\n                    letter-spacing: 0.02em;\n                }\n\n                /* iOS-style toggle switch */\n                .toggle-wrap {\n                    position: relative;\n                    display: inline-block;\n                    width: 44px;\n                    height: 24px;\n                    flex-shrink: 0;\n                }\n                .toggle-wrap input {\n                    opacity: 0;\n                    width: 0;\n                    height: 0;\n                    position: absolute;\n                }\n                .toggle-slider {\n                    position: absolute;\n                    cursor: pointer;\n                    top: 0;\n                    left: 0;\n                    right: 0;\n                    bottom: 0;\n                    background-color: #cbd5e1;\n                    transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);\n                    border-radius: 24px;\n                }\n                .toggle-slider:before {\n                    position: absolute;\n                    content: "";\n                    height: 18px;\n                    width: 18px;\n                    left: 3px;\n                    bottom: 3px;\n                    background-color: white;\n                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);\n                    transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);\n                    border-radius: 50%;\n                }\n                .toggle-wrap input:checked + .toggle-slider {\n                    background-color: #f05a10;\n                }\n                .toggle-wrap input:focus-visible + .toggle-slider {\n                    box-shadow: 0 0 0 2px #ffffff, 0 0 0 4px #f05a10;\n                }\n                .toggle-wrap input:checked + .toggle-slider:before {\n                    transform: translateX(20px);\n                }\n\n                @media (max-width: 680px) {\n                    :host {\n                        padding: 0 0.5rem 0.5rem;\n                    }\n                    .panel {\n                        padding: 1.15rem 1rem;\n                        border-radius: 14px;\n                    }\n                    h2 {\n                        font-size: 0.96rem;\n                    }\n                    .desc {\n                        font-size: 0.82rem;\n                        margin-bottom: 0.75rem;\n                    }\n                    .actions {\n                        flex-direction: column-reverse;\n                        align-items: stretch;\n                        gap: 0.5rem;\n                    }\n                    .actions-left,\n                    .actions-right {\n                        width: 100%;\n                        flex-direction: column-reverse;\n                        margin-right: 0;\n                    }\n                    button {\n                        width: 100%;\n                    }\n                    .custom-categories {\n                        max-height: 48vh;\n                    }\n                }\n\n                @media (prefers-reduced-motion: reduce) {\n                    .panel { animation: none; transition: none; }\n                    button, .policy-link, .toggle-slider, .toggle-slider:before { transition: none; }\n                }\n            </style>\n            <div class="panel" role="dialog" aria-modal="false" aria-labelledby="aml-cb-title">\n                <!-- Main View -->\n                <div class="view-main' +
                (this.__openCustomize ? ' is-hidden' : '') +
                '" id="aml-cb-view-main">\n                    <div class="head">\n                        <div class="icon-badge">' +
                shieldCookieSvg +
                '</div>\n                        <h2 id="aml-cb-title">' +
                esc(t.title) +
                '</h2>\n                    </div>\n                    <p class="desc" id="aml-cb-desc">' +
                esc(t.body) +
                '</p>\n                    <div class="policy-wrap">\n                        <a href="' +
                esc(policyUrl) +
                '" class="policy-link">\n                            <span>' +
                esc(t.policyLink) +
                '</span>\n                            ' +
                arrowRightSvg +
                '\n                        </a>\n                    </div>\n                    <div class="actions">\n                        <div class="actions-left">\n                            <button type="button" class="btn-secondary" data-act="reject">' +
                esc(t.reject) +
                '</button>\n                            <button type="button" class="btn-outline" data-act="custom">' +
                esc(t.customize) +
                '</button>\n                        </div>\n                        <div class="actions-right">\n                            <button type="button" class="btn-primary" data-act="accept">' +
                esc(t.accept) +
                '</button>\n                        </div>\n                    </div>\n                </div>\n\n                <!-- Customize Preferences View -->\n                <div class="view-custom' +
                (this.__openCustomize ? '' : ' is-hidden') +
                '" id="aml-cb-view-custom">\n                    <div class="custom-head">\n                        <div class="custom-head-title">\n                            <div class="icon-badge">' +
                shieldCookieSvg +
                '</div>\n                            <h2 id="aml-cb-custom-title">' +
                esc(t.customTitle) +
                '</h2>\n                        </div>\n                        <button type="button" class="btn-ghost" data-act="back" aria-label="' +
                esc(t.back) +
                '">\n                            ' +
                arrowLeftSvg +
                ' <span>' +
                esc(t.back) +
                '</span>\n                        </button>\n                    </div>\n                    <p class="desc">' +
                esc(t.customDesc) +
                '</p>\n                    \n                    <div class="custom-categories">\n                        <!-- Essential (Always on) -->\n                        <div class="cat-card">\n                            <div class="cat-info">\n                                <div class="cat-title-row">\n                                    <span class="cat-title">' +
                esc(t.catEssentialTitle) +
                '</span>\n                                    <span class="badge-essential">' +
                lockSvg +
                ' ' +
                esc(t.alwaysActive) +
                '</span>\n                                </div>\n                                <p class="cat-desc">' +
                esc(t.catEssentialDesc) +
                '</p>\n                            </div>\n                        </div>\n\n                        <!-- Analytics -->\n                        <label class="cat-card cat-card--toggle" for="aml-cb-an">\n                            <div class="cat-info">\n                                <div class="cat-title-row">\n                                    <span class="cat-title">' +
                esc(t.catAnalyticsTitle) +
                '</span>\n                                </div>\n                                <p class="cat-desc">' +
                esc(t.catAnalyticsDesc) +
                '</p>\n                            </div>\n                            <div class="toggle-wrap">\n                                <input type="checkbox" id="aml-cb-an" role="switch" aria-checked="' +
                (toggles.analytics ? 'true' : 'false') +
                '" data-toggle="analytics"' +
                (toggles.analytics ? ' checked' : '') +
                '>\n                                <span class="toggle-slider"></span>\n                            </div>\n                        </label>\n\n                        <!-- Marketing / Ads -->\n                        <label class="cat-card cat-card--toggle" for="aml-cb-ad">\n                            <div class="cat-info">\n                                <div class="cat-title-row">\n                                    <span class="cat-title">' +
                esc(t.catAdsTitle) +
                '</span>\n                                </div>\n                                <p class="cat-desc">' +
                esc(t.catAdsDesc) +
                '</p>\n                            </div>\n                            <div class="toggle-wrap">\n                                <input type="checkbox" id="aml-cb-ad" role="switch" aria-checked="' +
                (toggles.ads ? 'true' : 'false') +
                '" data-toggle="ads"' +
                (toggles.ads ? ' checked' : '') +
                '>\n                                <span class="toggle-slider"></span>\n                            </div>\n                        </label>\n\n                        <!-- Functionality -->\n                        <label class="cat-card cat-card--toggle" for="aml-cb-fn">\n                            <div class="cat-info">\n                                <div class="cat-title-row">\n                                    <span class="cat-title">' +
                esc(t.catFuncTitle) +
                '</span>\n                                </div>\n                                <p class="cat-desc">' +
                esc(t.catFuncDesc) +
                '</p>\n                            </div>\n                            <div class="toggle-wrap">\n                                <input type="checkbox" id="aml-cb-fn" role="switch" aria-checked="' +
                (toggles.func ? 'true' : 'false') +
                '" data-toggle="func"' +
                (toggles.func ? ' checked' : '') +
                '>\n                                <span class="toggle-slider"></span>\n                            </div>\n                        </label>\n                    </div>\n\n                    <div class="actions">\n                        <div class="actions-left">\n                            <button type="button" class="btn-secondary" data-act="reject">' +
                esc(t.reject) +
                '</button>\n                            <button type="button" class="btn-outline" data-act="save">' +
                esc(t.save) +
                '</button>\n                        </div>\n                        <div class="actions-right">\n                            <button type="button" class="btn-primary" data-act="accept">' +
                esc(t.accept) +
                '</button>\n                        </div>\n                    </div>\n                </div>\n            </div>\n        ';

            var host = this;
            var root = this.shadowRoot;

            function closeBanner() {
                var panel = root.querySelector('.panel');
                if (panel) {
                    panel.classList.add('is-closing');
                    setTimeout(function () {
                        host.__forceVisible = false;
                        host.__openCustomize = false;
                        host.setAttribute('hidden', '');
                        panel.classList.remove('is-closing');
                    }, 200);
                } else {
                    host.__forceVisible = false;
                    host.__openCustomize = false;
                    host.setAttribute('hidden', '');
                }
            }

            function showCustomize(open) {
                host.__openCustomize = open;
                var viewMain = root.querySelector('#aml-cb-view-main');
                var viewCustom = root.querySelector('#aml-cb-view-custom');
                if (viewMain && viewCustom) {
                    if (open) {
                        viewMain.classList.add('is-hidden');
                        viewCustom.classList.remove('is-hidden');
                    } else {
                        viewMain.classList.remove('is-hidden');
                        viewCustom.classList.add('is-hidden');
                    }
                }
            }

            root.querySelectorAll('[data-act="reject"]').forEach(function (btn) {
                btn.addEventListener('click', function () {
                    persist(CONSENT_REJECT);
                    closeBanner();
                });
            });

            root.querySelectorAll('[data-act="accept"]').forEach(function (btn) {
                btn.addEventListener('click', function () {
                    persist(CONSENT_ACCEPT);
                    closeBanner();
                });
            });

            root.querySelector('[data-act="custom"]')?.addEventListener('click', function () {
                showCustomize(true);
                host.__focusFirst();
            });

            root.querySelector('[data-act="back"]')?.addEventListener('click', function () {
                showCustomize(false);
                host.__focusFirst();
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
