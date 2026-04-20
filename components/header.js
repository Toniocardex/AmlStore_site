(function () {
    'use strict';

    const HEADER_I18N = {
        it: {
            logoAlt: 'Aml Store',
            navHome: 'Home',
            navOs: 'Sistemi Operativi',
            navM365: 'Microsoft 365',
            navM365OpenSubmenu: 'Apri sottomenu Microsoft 365',
            navM365Overview: 'Panoramica suite',
            navM365Personal: 'Microsoft 365 Personal',
            navM365Family: 'Microsoft 365 Family',
            navM365Business: 'Microsoft 365 Business Standard',
            navAntivirus: 'Antivirus',
            assistanceSmall: 'Assistenza',
            openNavMenu: 'Apri menu di navigazione',
            closeNavMenu: 'Chiudi menu',
            selectLanguage: 'Seleziona lingua',
            cartAriaEmpty: 'Carrello, nessun articolo',
            cartAriaOne: 'Carrello, 1 articolo',
            cartAriaMany: 'Carrello, {{n}} articoli',
            signIn: 'Accedi',
            drawerAssist: 'Assistenza: +39 392 558 0413',
        },
        en: {
            logoAlt: 'Aml Store',
            navHome: 'Home',
            navOs: 'Operating systems',
            navM365: 'Microsoft 365',
            navM365OpenSubmenu: 'Open Microsoft 365 submenu',
            navM365Overview: 'Suite overview',
            navM365Personal: 'Microsoft 365 Personal',
            navM365Family: 'Microsoft 365 Family',
            navM365Business: 'Microsoft 365 Business Standard',
            navAntivirus: 'Antivirus',
            assistanceSmall: 'Support',
            openNavMenu: 'Open navigation menu',
            closeNavMenu: 'Close menu',
            selectLanguage: 'Select language',
            cartAriaEmpty: 'Shopping cart, empty',
            cartAriaOne: 'Shopping cart, 1 item',
            cartAriaMany: 'Shopping cart, {{n}} items',
            signIn: 'Sign in',
            drawerAssist: 'Support: +39 392 558 0413',
        },
        fr: {
            logoAlt: 'Aml Store',
            navHome: 'Home',
            navOs: "Systèmes d'exploitation",
            navM365: 'Microsoft 365',
            navM365OpenSubmenu: 'Ouvrir le sous-menu Microsoft 365',
            navM365Overview: 'Vue d’ensemble de la suite',
            navM365Personal: 'Microsoft 365 Personnel',
            navM365Family: 'Microsoft 365 Famille',
            navM365Business: 'Microsoft 365 Business Standard',
            navAntivirus: 'Antivirus',
            assistanceSmall: 'Assistance',
            openNavMenu: 'Ouvrir le menu de navigation',
            closeNavMenu: 'Fermer le menu',
            selectLanguage: 'Choisir la langue',
            cartAriaEmpty: 'Panier vide',
            cartAriaOne: 'Panier, 1 article',
            cartAriaMany: 'Panier, {{n}} articles',
            signIn: 'Se connecter',
            drawerAssist: 'Assistance : +39 392 558 0413',
        },
        de: {
            logoAlt: 'Aml Store',
            navHome: 'Home',
            navOs: 'Betriebssysteme',
            navM365: 'Microsoft 365',
            navM365OpenSubmenu: 'Microsoft-365-Untermenü öffnen',
            navM365Overview: 'Suite-Überblick',
            navM365Personal: 'Microsoft 365 Personal',
            navM365Family: 'Microsoft 365 Family',
            navM365Business: 'Microsoft 365 Business Standard',
            navAntivirus: 'Antivirus',
            assistanceSmall: 'Support',
            openNavMenu: 'Navigationsmenü öffnen',
            closeNavMenu: 'Menü schließen',
            selectLanguage: 'Sprache wählen',
            cartAriaEmpty: 'Warenkorb leer',
            cartAriaOne: 'Warenkorb, 1 Artikel',
            cartAriaMany: 'Warenkorb, {{n}} Artikel',
            signIn: 'Anmelden',
            drawerAssist: 'Support: +39 392 558 0413',
        },
        es: {
            logoAlt: 'Aml Store',
            navHome: 'Home',
            navOs: 'Sistemas operativos',
            navM365: 'Microsoft 365',
            navM365OpenSubmenu: 'Abrir submenú Microsoft 365',
            navM365Overview: 'Panorama de la suite',
            navM365Personal: 'Microsoft 365 Personal',
            navM365Family: 'Microsoft 365 Familia',
            navM365Business: 'Microsoft 365 Business Standard',
            navAntivirus: 'Antivirus',
            assistanceSmall: 'Asistencia',
            openNavMenu: 'Abrir menú de navegación',
            closeNavMenu: 'Cerrar menú',
            selectLanguage: 'Seleccionar idioma',
            cartAriaEmpty: 'Carrito vacío',
            cartAriaOne: 'Carrito, 1 artículo',
            cartAriaMany: 'Carrito, {{n}} artículos',
            signIn: 'Iniciar sesión',
            drawerAssist: 'Asistencia: +39 392 558 0413',
        },
    };

    class EcommerceHeader extends HTMLElement {
        constructor() {
            super();
            this.attachShadow({ mode: 'open' });
        }

        connectedCallback() {
            if (this.__headerUiInit) return;
            this.__headerUiInit = true;

            this.setAttribute('translate', 'no');
            this.classList.add('notranslate');

            const S = window.AmlSite;
            if (!S) {
                console.error('ecommerce-header: includere ../js/locale-path.js prima di questo script.');
                return;
            }
            const parsed = S.parseLocalePath(window.location.pathname);
            const LANGS = S.LANGS;
            const activeLang = parsed.activeLang;
            const otherLangs = LANGS.filter((l) => l.code !== activeLang.code);
            const hrefForLang = (code) =>
                S.hrefSwitchLocale(
                    parsed.pathPrefix,
                    code,
                    parsed.pathAfterLang,
                    window.location.search,
                    window.location.hash
                );
            const homeHref = S.homeHref(parsed.pathPrefix, activeLang.code);
            const cartHref = S.localePageUrl(parsed.pathPrefix, activeLang.code, 'cart.html');
            const t = HEADER_I18N[activeLang.code] || HEADER_I18N.it;

            /* Rileva se siamo sulla home page della lingua attiva */
            const afterLang = (parsed.pathAfterLang || '').replace(/^\//, '');
            const isHome = afterLang === '' || afterLang === 'index.html';
            const hrefM365Solutions = S.localePageUrl(parsed.pathPrefix, activeLang.code, 'microsoft-365-solutions.html');
            const hrefM365Personal = S.localePageUrl(parsed.pathPrefix, activeLang.code, 'microsoft-365-personal.html');
            const hrefM365Family = S.localePageUrl(parsed.pathPrefix, activeLang.code, 'microsoft-365-family.html');
            const afterLangLower = String(parsed.pathAfterLang || '').toLowerCase();
            const isM365Solutions = afterLangLower.includes('microsoft-365-solutions');
            const isM365Personal = afterLangLower.includes('microsoft-365-personal');
            const isM365Family = afterLangLower.includes('microsoft-365-family');
            const isM365NavActive = isM365Solutions || isM365Personal || isM365Family;
            const mailM365Business = 'mailto:Info@amlstore.it?subject=' + encodeURIComponent('Microsoft 365 Business Standard');
            const esc = S.escapeHtmlAttr;

            const cartAriaForCount = (n) => {
                const c = Number(n) || 0;
                if (c <= 0) return t.cartAriaEmpty;
                if (c === 1) return t.cartAriaOne;
                return String(t.cartAriaMany).replace('{{n}}', String(c));
            };

            const staticRoot = S.staticRootFromScriptPath('/components/header.js');
            const logoSrc = `${staticRoot}/logo/logo-header-400.webp`;
            const flagSrc = (flag) => `${staticRoot}/images/flags/${flag}.svg`;

            this.shadowRoot.innerHTML = `

                <style>
                    :host {
                        display: block;
                        position: sticky;
                        top: 0;
                        z-index: 1000;
                        font-family: 'Montserrat', sans-serif;
                        /* Stessa tonalità del footer (#050505 / #111111) con trasparenza glass */
                        --bg-base: rgba(5, 5, 5, 0.75);
                        --bg-surface: rgba(17, 17, 17, 0.85);
                        --border-color: rgba(255, 255, 255, 0.08);
                        --text-primary: #ffffff;
                        --text-secondary: #a1a1aa;
                        --text-muted: #71717a;
                        --accent: #3b82f6;
                        --accent-hover: #60a5fa;

                        background-color: var(--bg-base);
                        backdrop-filter: blur(20px);
                        -webkit-backdrop-filter: blur(20px);
                        border-bottom: 1px solid var(--border-color);
                    }

                    * { box-sizing: border-box; margin: 0; padding: 0; }

                    .header-container {
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        gap: 2rem;
                        height: 88px;
                        
                        /* FIX: Allineamento e Padding condiviso con il Footer */
                        max-width: 1280px;
                        margin: 0 auto;
                        padding: 0 clamp(2rem, 5vw, 4rem);
                    }

                    .left-section {
                        display: flex;
                        align-items: center;
                        gap: clamp(1.5rem, 3vw, 3rem); /* Spazio Fluido tra logo e nav */
                    }

                    .logo {
                        display: flex;
                        align-items: center;
                        text-decoration: none;
                        transition: opacity 0.2s ease, transform 0.2s ease;
                        border-radius: 6px;
                        flex-shrink: 0;
                    }
                    .logo:hover { opacity: 0.9; transform: scale(1.02); }
                    .logo:focus-visible { outline: 2px solid var(--accent); outline-offset: 4px; }
                    .logo img {
                        height: 56px;
                        width: auto;
                        max-height: 100%;
                        display: block;
                        filter: brightness(0) invert(1);
                    }

                    .nav-links {
                        display: flex;
                        align-items: center;
                        gap: clamp(1rem, 2vw, 2rem); /* Spazio fluido tra i link */
                    }

                    .nav-links a {
                        color: var(--text-secondary);
                        text-decoration: none;
                        font-size: 0.9rem;
                        font-weight: 500;
                        transition: color 0.3s ease, text-shadow 0.3s ease;
                        position: relative;
                        padding-bottom: 4px; /* Spazio per l'animazione della linea */
                        white-space: nowrap; /* Impedisce che i link si spezzino su due righe */
                    }
                    
                    /* Linea animata dal centro sui link */
                    .nav-links a::after {
                        content: '';
                        position: absolute;
                        bottom: -2px;
                        left: 50%;
                        width: 0;
                        height: 2px;
                        background-color: var(--text-primary);
                        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                        border-radius: 2px;
                    }

                    .nav-links a:hover {
                        color: var(--text-primary);
                        text-shadow: 0 0 12px rgba(255, 255, 255, 0.2);
                    }
                    
                    .nav-links a:hover::after, .nav-links a.active::after {
                        width: 100%;
                        left: 0;
                    }

                    .nav-links a.active {
                        color: var(--text-primary);
                        font-weight: 600;
                    }

                    /* Microsoft 365 — voce principale (link overview) + sottomenù */
                    .nav-m365-wrap {
                        position: relative;
                        display: flex;
                        align-items: center;
                    }
                    .nav-m365-inner {
                        display: inline-flex;
                        align-items: center;
                        gap: 0.15rem;
                    }
                    .nav-m365-root {
                        color: var(--text-secondary);
                        text-decoration: none;
                        font-size: 0.9rem;
                        font-weight: 500;
                        transition: color 0.3s ease, text-shadow 0.3s ease;
                        position: relative;
                        padding-bottom: 4px;
                        white-space: nowrap;
                    }
                    .nav-m365-root::after {
                        content: '';
                        position: absolute;
                        bottom: -2px;
                        left: 50%;
                        width: 0;
                        height: 2px;
                        background-color: var(--text-primary);
                        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                        border-radius: 2px;
                    }
                    .nav-m365-root:hover {
                        color: var(--text-primary);
                        text-shadow: 0 0 12px rgba(255, 255, 255, 0.2);
                    }
                    .nav-m365-root:hover::after,
                    .nav-m365-root.active::after {
                        width: 100%;
                        left: 0;
                    }
                    .nav-m365-root.active {
                        color: var(--text-primary);
                        font-weight: 600;
                    }
                    .nav-m365-caret {
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        width: 1.5rem;
                        height: 1.5rem;
                        padding: 0;
                        margin: 0 0 2px 0;
                        border: none;
                        border-radius: 6px;
                        background: transparent;
                        color: var(--text-secondary);
                        cursor: pointer;
                        transition: color 0.2s ease, background 0.2s ease;
                    }
                    .nav-m365-caret:hover,
                    .nav-m365-wrap.open .nav-m365-caret {
                        color: var(--text-primary);
                        background: rgba(255, 255, 255, 0.06);
                    }
                    .nav-m365-caret:focus-visible {
                        outline: 2px solid var(--accent);
                        outline-offset: 2px;
                    }
                    .nav-m365-caret svg {
                        width: 12px;
                        height: 12px;
                        fill: currentColor;
                        transition: transform 0.25s ease;
                    }
                    .nav-m365-wrap.open .nav-m365-caret svg {
                        transform: rotate(180deg);
                    }
                    /* Ponte invisibile sopra il pannello: senza, il mouse attraversa il gap
                       tra trigger e dropdown e :hover sul wrap cade → il menu si chiude. */
                    .nav-m365-dropdown::before {
                        content: '';
                        position: absolute;
                        bottom: 100%;
                        left: 0;
                        right: 0;
                        height: calc(0.5rem + 12px);
                    }
                    .nav-m365-dropdown {
                        position: absolute;
                        top: calc(100% + 0.5rem);
                        left: 0;
                        min-width: 16.5rem;
                        background: var(--bg-surface);
                        backdrop-filter: blur(16px);
                        -webkit-backdrop-filter: blur(16px);
                        border: 1px solid var(--border-color);
                        border-radius: 12px;
                        padding: 0.4rem;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.05);
                        opacity: 0;
                        visibility: hidden;
                        pointer-events: none;
                        transform: translateY(-6px) scale(0.98);
                        transition: opacity 0.18s ease, transform 0.18s ease, visibility 0.18s;
                        z-index: 50;
                    }
                    .nav-m365-wrap:hover .nav-m365-dropdown,
                    .nav-m365-wrap:focus-within .nav-m365-dropdown,
                    .nav-m365-wrap.open .nav-m365-dropdown {
                        opacity: 1;
                        visibility: visible;
                        pointer-events: auto;
                        transform: translateY(0) scale(1);
                        transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1),
                                    transform 0.25s cubic-bezier(0.16, 1, 0.3, 1),
                                    visibility 0.25s;
                    }
                    .nav-m365-dropdown a {
                        display: block;
                        padding: 0.55rem 0.75rem;
                        border-radius: 8px;
                        color: var(--text-secondary);
                        text-decoration: none;
                        font-size: 0.85rem;
                        font-weight: 500;
                        white-space: nowrap;
                        transition: background 0.2s ease, color 0.2s ease;
                    }
                    .nav-m365-dropdown a:hover {
                        background: rgba(255, 255, 255, 0.08);
                        color: var(--text-primary);
                    }
                    .nav-m365-dropdown a.nav-m365-dropdown__overview {
                        font-weight: 700;
                        color: var(--text-primary);
                        border-bottom: 1px solid var(--border-color);
                        border-radius: 8px 8px 0 0;
                        margin-bottom: 0.15rem;
                        padding-bottom: 0.65rem;
                    }
                    .nav-m365-dropdown a.nav-m365-dropdown__overview:hover {
                        background: rgba(59, 130, 246, 0.12);
                    }

                    .right-section {
                        display: flex;
                        align-items: center;
                        gap: clamp(0.75rem, 1.5vw, 1.5rem); /* Spazio fluido tra gli elementi di destra */
                    }

                    .support-info {
                        display: flex;
                        align-items: center;
                        gap: 0.75rem;
                        text-decoration: none;
                        border-radius: 8px;
                    }
                    .support-info:focus-visible {
                        outline: 2px solid var(--accent);
                        outline-offset: 3px;
                    }
                    .support-icon {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        width: 36px;
                        height: 36px;
                        border-radius: 50%;
                        background: rgba(255, 255, 255, 0.05);
                        color: var(--text-secondary);
                        transition: background 0.3s ease, color 0.3s ease;
                        flex-shrink: 0;
                    }
                    .support-info:hover .support-icon {
                        background: rgba(255, 255, 255, 0.1);
                        color: var(--text-primary);
                    }
                    .support-text {
                        display: flex;
                        flex-direction: column;
                        white-space: nowrap; /* Impedisce al testo di andare a capo */
                    }
                    .support-text small {
                        font-size: 0.7rem;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                        color: var(--text-muted);
                        font-weight: 600;
                    }
                    .support-text span {
                        font-size: 0.9rem;
                        color: var(--text-primary);
                        font-weight: 600;
                    }

                    .divider {
                        width: 1px;
                        height: 24px;
                        background: linear-gradient(to bottom, transparent, rgba(255, 255, 255, 0.15), transparent);
                    }

                    .lang-wrapper { position: relative; }
                    .lang-selector {
                        display: flex;
                        align-items: center;
                        gap: 0.5rem;
                        background: transparent;
                        border: 1px solid transparent;
                        color: var(--text-secondary);
                        font-size: 0.9rem;
                        font-weight: 500;
                        cursor: pointer;
                        font-family: inherit;
                        padding: 0.5rem;
                        border-radius: 8px;
                        transition: color 0.3s ease, background 0.3s ease, border 0.3s ease;
                    }
                    .lang-selector:hover, .lang-wrapper.open .lang-selector {
                        color: var(--text-primary);
                        background: rgba(255, 255, 255, 0.05);
                        border-color: rgba(255, 255, 255, 0.1);
                    }
                    .lang-selector:focus-visible {
                        outline: 2px solid var(--accent);
                        outline-offset: 3px;
                    }
                    /* Sostituto visivo per l'anteprima se non c'è l'immagine della flag */
                    .lang-selector img {
                        width: 20px;
                        height: 20px;
                        border-radius: 50%;
                        object-fit: cover;
                        background: rgba(255, 255, 255, 0.1);
                        color: transparent;
                        border: 1px solid rgba(255,255,255,0.2);
                    }
                    .chevron-down {
                        width: 14px;
                        height: 14px;
                        fill: currentColor;
                        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    }
                    .lang-wrapper.open .chevron-down {
                        transform: rotate(180deg);
                    }

                    .lang-dropdown {
                        position: absolute;
                        top: calc(100% + 0.75rem);
                        right: 0;
                        background: var(--bg-surface);
                        backdrop-filter: blur(16px);
                        -webkit-backdrop-filter: blur(16px);
                        border: 1px solid var(--border-color);
                        border-radius: 12px;
                        padding: 0.5rem;
                        min-width: 140px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.05);
                        /* Stato chiuso: invisibile ma nel flusso — permette transizione in uscita */
                        opacity: 0;
                        visibility: hidden;
                        pointer-events: none;
                        transform: translateY(-6px) scale(0.98);
                        transition: opacity 0.18s ease, transform 0.18s ease, visibility 0.18s;
                    }
                    .lang-wrapper.open .lang-dropdown {
                        opacity: 1;
                        visibility: visible;
                        pointer-events: auto;
                        transform: translateY(0) scale(1);
                        transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1),
                                    transform 0.25s cubic-bezier(0.16, 1, 0.3, 1),
                                    visibility 0.25s;
                    }

                    .lang-option {
                        display: flex;
                        align-items: center;
                        gap: 0.75rem;
                        padding: 0.6rem 0.75rem;
                        color: var(--text-secondary);
                        text-decoration: none;
                        font-size: 0.85rem;
                        font-weight: 500;
                        border-radius: 8px;
                        transition: background 0.2s ease, color 0.2s ease, transform 0.2s ease;
                    }
                    .lang-option:hover {
                        background: rgba(255, 255, 255, 0.08);
                        color: var(--text-primary);
                        transform: translateX(2px);
                    }
                    .lang-option img {
                        width: 18px;
                        height: 18px;
                        border-radius: 50%;
                        object-fit: cover;
                        background: rgba(255, 255, 255, 0.1);
                        color: transparent;
                    }

                    .cart-wrapper {
                        position: relative;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        width: 42px;
                        height: 42px;
                        border-radius: 50%;
                        color: var(--text-secondary);
                        cursor: pointer;
                        transition: color 0.3s ease, background 0.3s ease;
                        flex-shrink: 0;
                        text-decoration: none;
                    }
                    .cart-wrapper:hover {
                        color: var(--text-primary);
                        background: rgba(255, 255, 255, 0.08);
                    }
                    .cart-wrapper:focus-visible {
                        outline: 2px solid var(--accent);
                        outline-offset: 3px;
                    }
                    .cart-wrapper svg {
                        width: 22px;
                        height: 22px;
                        fill: currentColor;
                        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                    }
                    /* Rimbalzo giocoso ma elegante al passaggio del mouse sul carrello */
                    .cart-wrapper:hover svg {
                        transform: scale(1.1) rotate(-8deg);
                    }
                    
                    .cart-badge {
                        position: absolute;
                        top: 0;
                        right: -2px;
                        background: linear-gradient(135deg, #ef4444, #dc2626);
                        color: white;
                        font-size: 0.65rem;
                        font-weight: 800;
                        min-width: 18px;
                        height: 18px;
                        padding: 0 4px;
                        display: none;
                        align-items: center;
                        justify-content: center;
                        border-radius: 50%;
                        border: 2px solid #050505; /* Bordo che "buca" l'icona sottostante */
                        box-shadow: 0 2px 4px rgba(0,0,0,0.5);
                    }
                    .cart-badge.is-visible {
                        display: flex;
                    }

                    .cart-badge.is-visible.cart-badge-pop {
                        animation: aml-cart-badge-pop 0.55s cubic-bezier(0.34, 1.56, 0.64, 1);
                    }

                    @keyframes aml-cart-badge-pop {
                        0%,
                        100% {
                            transform: scale(1);
                        }
                        45% {
                            transform: scale(1.14);
                        }
                    }

                    .cart-wrapper.cart-nudge {
                        color: var(--text-primary);
                        background: rgba(255, 255, 255, 0.1);
                    }

                    .cart-wrapper.cart-nudge svg {
                        animation: aml-cart-icon-nudge 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
                    }

                    @keyframes aml-cart-icon-nudge {
                        0%,
                        100% {
                            transform: scale(1) rotate(0deg);
                        }
                        35% {
                            transform: scale(1.12) rotate(-10deg);
                        }
                        70% {
                            transform: scale(1.05) rotate(4deg);
                        }
                    }

                    @media (prefers-reduced-motion: reduce) {
                        /* Carrello */
                        .cart-badge.is-visible.cart-badge-pop { animation: none; }
                        .cart-wrapper.cart-nudge svg { animation: none; }
                        /* Logo */
                        .logo { transition: none; }
                        /* Nav desktop */
                        .nav-links a,
                        .nav-links a::after { transition: none; }
                        /* Supporto */
                        .support-icon { transition: none; }
                        /* Selettore lingua */
                        .lang-selector { transition: none; }
                        .chevron-down { transition: none; }
                        .lang-dropdown,
                        .lang-wrapper.open .lang-dropdown { transition: none; }
                        .nav-m365-dropdown,
                        .nav-m365-wrap:hover .nav-m365-dropdown,
                        .nav-m365-wrap:focus-within .nav-m365-dropdown,
                        .nav-m365-wrap.open .nav-m365-dropdown { transition: none; }
                        .nav-m365-caret svg { transition: none; }
                        /* Pulsante Accedi */
                        .btn-signin { transition: none; }
                        /* Overlay e Drawer mobile */
                        .overlay { transition: none; }
                        .mobile-drawer { transition: none; }
                        .close-drawer { transition: none; }
                        .drawer-nav a { transition: none; }
                        .drawer-lang-link { transition: none; }
                        .drawer-btn-signin { transition: none; }
                    }

                    .btn-signin {
                        background: linear-gradient(135deg, #ffffff 0%, #e4e4e7 100%);
                        color: #000000; /* Testo in alto contrasto */
                        border: none;
                        padding: 0.6rem 1.4rem;
                        border-radius: 10px;
                        font-family: inherit;
                        font-size: 0.9rem;
                        font-weight: 700;
                        cursor: pointer;
                        box-shadow: 0 4px 14px rgba(255, 255, 255, 0.15);
                        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease;
                        white-space: nowrap;
                    }
                    .btn-signin:hover {
                        transform: translateY(-2px) scale(1.02);
                        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.25);
                    }
                    .btn-signin:active {
                        transform: translateY(0) scale(0.98);
                    }
                    .btn-signin:focus-visible {
                        outline: 2px solid var(--accent);
                        outline-offset: 3px;
                    }

                    .mobile-toggle {
                        display: none;
                        background: none;
                        border: none;
                        color: var(--text-primary);
                        cursor: pointer;
                        padding: 0.5rem;
                        margin-left: -0.5rem; /* Compensa il padding per l'allineamento */
                        border-radius: 6px;
                        transition: opacity 0.2s;
                        touch-action: manipulation; /* Ottimizzazione touch */
                    }
                    .mobile-toggle:hover {
                        opacity: 0.7;
                    }
                    .mobile-toggle:focus-visible {
                        outline: 2px solid var(--accent);
                        outline-offset: 3px;
                    }
                    .mobile-toggle svg {
                        width: 28px;
                        height: 28px;
                        fill: none;
                        stroke: currentColor;
                        stroke-width: 2;
                        stroke-linecap: round;
                    }

                    /* --- RESPONSIVE DESIGN HEADER --- */

                    /* GRACEFUL DEGRADATION 1: Tolgo la parola ASSISTENZA per far spazio */
                    @media (max-width: 1280px) {
                        .support-text small { display: none; }
                        .support-info { gap: 0.5rem; }
                    }

                    /* GRACEFUL DEGRADATION 2: Nascondo anche il numero, lascio solo l'icona cuffia con Tooltip */
                    @media (max-width: 1180px) {
                        .support-text { display: none; }
                    }

                    /* Breakpoint 1: Tablet o schermi piccoli - Nasconde nav links e attiva menu mobile */
                    @media (max-width: 1100px) {
                        .nav-links { display: none; }
                        .mobile-toggle { display: block; }
                        .left-section { gap: 1rem; }
                    }

                    /* Breakpoint 2: Tablet verticali - Nasconde assistenza del tutto per pulizia */
                    @media (max-width: 900px) {
                        .support-info { display: none; }
                        .divider:first-of-type { display: none; }
                    }

                    /* Breakpoint 3: Smartphone - Ottimizzazione estrema spazi */
                    @media (max-width: 640px) {
                        .header-container { 
                            padding: 0 clamp(1.25rem, 5vw, 2rem); 
                            height: 72px; /* Barra mobile: spazio per marchio più leggibile */
                            gap: 1rem;
                        }
                        .btn-signin { display: none; } /* Lo user troverà il login nel drawer */
                        .divider { display: none; }
                        .lang-selector span { display: none; } /* Solo icona lingua */
                        .lang-selector { padding: 0.4rem; }
                        .right-section { gap: 0.5rem; }
                        .header-container .left-section .logo img { height: 44px; }
                        .cart-wrapper { 
                            width: 36px; 
                            height: 36px; 
                        }
                    }

                    /* DRAWER MOBILE */
                    .overlay {
                        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                        background: rgba(0,0,0,0.6);
                        backdrop-filter: blur(6px);
                        z-index: 1999;
                        opacity: 0; pointer-events: none;
                        /* Chiusura: ease-in (veloce all'uscita) */
                        transition: opacity 0.25s cubic-bezier(0.4, 0, 1, 1);
                    }
                    .overlay.open {
                        opacity: 1; pointer-events: auto;
                        /* Apertura: ease-out (parte veloce, rallenta) */
                        transition: opacity 0.4s cubic-bezier(0, 0, 0.2, 1);
                    }

                    .mobile-drawer {
                        position: fixed; top: 0; left: -100%;
                        width: 100%; max-width: 320px;
                        height: 100vh;
                        background: var(--bg-surface);
                        backdrop-filter: blur(20px);
                        -webkit-backdrop-filter: blur(20px);
                        border-right: 1px solid var(--border-color);
                        z-index: 2000;
                        /* Chiusura: ease-in più rapida */
                        transition: left 0.3s cubic-bezier(0.4, 0, 1, 1);
                        padding: 1.5rem 1.25rem;
                        display: flex; flex-direction: column;
                        overflow-y: auto;
                        box-shadow: 10px 0 30px rgba(0,0,0,0.5);
                    }
                    .mobile-drawer.open {
                        left: 0;
                        /* Apertura: ease-out con overshoot leggero */
                        transition: left 0.4s cubic-bezier(0.16, 1, 0.3, 1);
                    }

                    .drawer-header {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 2rem;
                    }
                    .mobile-drawer .drawer-header .logo img {
                        height: 52px;
                        width: auto;
                    }
                    .close-drawer {
                        background: rgba(255, 255, 255, 0.05);
                        border: 1px solid var(--border-color);
                        color: var(--text-primary);
                        width: 36px; height: 36px;
                        border-radius: 50%;
                        display: flex; align-items: center; justify-content: center;
                        cursor: pointer;
                        transition: background 0.3s ease, transform 0.3s ease;
                    }
                    .close-drawer:hover {
                        background: rgba(255, 255, 255, 0.15);
                        transform: rotate(90deg);
                    }
                    .close-drawer:focus-visible {
                        outline: 2px solid var(--accent);
                        outline-offset: 3px;
                    }
                    .close-drawer svg { width: 20px; height: 20px; fill: currentColor; }

                    .drawer-nav {
                        display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 2.5rem;
                    }
                    .drawer-m365-block { margin-bottom: 0.25rem; }
                    .drawer-m365-heading {
                        font-size: 0.72rem;
                        font-weight: 700;
                        text-transform: uppercase;
                        letter-spacing: 0.08em;
                        color: var(--text-muted);
                        padding: 0.5rem 1rem 0.35rem;
                    }
                    .drawer-m365-block a { font-size: 1rem; font-weight: 600; }
                    .drawer-nav a {
                        color: var(--text-primary);
                        text-decoration: none;
                        font-size: 1.2rem;
                        font-weight: 600;
                        padding: 1rem; /* Area touch massimizzata */
                        border-radius: 10px;
                        transition: background 0.3s ease, padding-left 0.3s ease;
                    }
                    .drawer-nav a:hover, .drawer-nav a.active {
                        background: rgba(255, 255, 255, 0.08);
                        padding-left: 1.5rem; /* Effetto indentazione al passaggio del mouse */
                    }

                    .drawer-section-title {
                        font-size: 0.75rem;
                        color: var(--text-muted);
                        text-transform: uppercase;
                        letter-spacing: 0.1em;
                        font-weight: 600;
                        margin-bottom: 1rem;
                        padding-left: 0.5rem;
                    }

                    .drawer-langs {
                        display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;
                        margin-bottom: auto;
                    }
                    .drawer-lang-link {
                        display: flex; align-items: center; gap: 0.75rem;
                        padding: 0.75rem 1rem;
                        border-radius: 10px;
                        font-size: 0.9rem; font-weight: 500;
                        color: var(--text-secondary);
                        text-decoration: none;
                        border: 1px solid transparent;
                        transition: background 0.3s ease, border-color 0.3s ease, color 0.3s ease;
                    }
                    .drawer-lang-link.active {
                        background: rgba(255, 255, 255, 0.1);
                        border-color: rgba(255, 255, 255, 0.2);
                        color: var(--text-primary);
                    }
                    .drawer-lang-link:hover:not(.active) {
                        background: rgba(255, 255, 255, 0.05);
                        color: var(--text-primary);
                    }
                    .drawer-lang-link img {
                        width: 20px; height: 20px; border-radius: 50%; object-fit: cover;
                        background: rgba(255, 255, 255, 0.1); color: transparent;
                    }

                    .drawer-footer {
                        margin-top: 2.5rem;
                        padding-top: 1.5rem;
                        border-top: 1px solid var(--border-color);
                    }
                    .drawer-btn-signin {
                        width: 100%;
                        background: linear-gradient(135deg, #ffffff 0%, #e4e4e7 100%);
                        color: #000;
                        border: none;
                        padding: 1rem;
                        border-radius: 10px;
                        font-weight: 700;
                        font-size: 1rem;
                        cursor: pointer;
                        margin-bottom: 1.5rem;
                        transition: opacity 0.2s ease, transform 0.2s ease;
                    }
                    .drawer-btn-signin:hover {
                        opacity: 0.9;
                        transform: scale(1.01);
                    }
                    .drawer-btn-signin:focus-visible {
                        outline: 2px solid var(--accent);
                        outline-offset: 3px;
                    }
                    .drawer-assist {
                        display: flex;
                        align-items: center;
                        gap: 0.75rem;
                        text-decoration: none;
                        padding: 0.875rem 1rem;
                        border-radius: 10px;
                        background: rgba(255, 255, 255, 0.03);
                        border: 1px solid rgba(255, 255, 255, 0.07);
                        transition: background 0.2s ease, border-color 0.2s ease;
                    }
                    .drawer-assist:hover {
                        background: rgba(255, 255, 255, 0.06);
                        border-color: rgba(255, 255, 255, 0.12);
                    }
                    .drawer-assist:focus-visible {
                        outline: 2px solid var(--accent);
                        outline-offset: 3px;
                    }
                    .drawer-assist-icon {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        width: 36px;
                        height: 36px;
                        border-radius: 10px;
                        background: rgba(255, 255, 255, 0.05);
                        color: var(--text-secondary);
                        flex-shrink: 0;
                    }
                    .drawer-assist-icon svg { width: 18px; height: 18px; fill: currentColor; }
                    .drawer-assist-text {
                        display: flex;
                        flex-direction: column;
                        gap: 0.1rem;
                        overflow: hidden;
                    }
                    .drawer-assist-label {
                        font-size: 0.7rem;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 0.06em;
                        color: var(--text-muted);
                    }
                    .drawer-assist-number {
                        font-size: 0.9rem;
                        font-weight: 600;
                        color: var(--text-primary);
                        white-space: nowrap;
                        text-overflow: ellipsis;
                        overflow: hidden;
                    }
                </style>

                <div class="header-container">
                    <div class="left-section">
                        <button type="button" class="mobile-toggle" aria-label="${esc(t.openNavMenu)}">
                            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"></path></svg>
                        </button>
                        <a href="${esc(homeHref)}" class="logo">
                            <img src="${esc(logoSrc)}" width="280" height="56" alt="${esc(t.logoAlt)}">
                        </a>
                        <nav class="nav-links">
                            <a href="${esc(homeHref)}"${isHome ? ' class="active"' : ''}>${esc(t.navHome)}</a>
                            <a href="#">${esc(t.navOs)}</a>
                            <div class="nav-m365-wrap">
                                <div class="nav-m365-inner">
                                    <a href="${esc(hrefM365Solutions)}" class="nav-m365-root${isM365NavActive ? ' active' : ''}">${esc(t.navM365)}</a>
                                    <button type="button" class="nav-m365-caret" aria-expanded="false" aria-haspopup="true" aria-label="${esc(t.navM365OpenSubmenu)}">
                                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>
                                    </button>
                                </div>
                                <div class="nav-m365-dropdown" role="menu">
                                    <a href="${esc(hrefM365Solutions)}" class="nav-m365-dropdown__overview" role="menuitem">${esc(t.navM365Overview)}</a>
                                    <a href="${esc(hrefM365Personal)}" role="menuitem">${esc(t.navM365Personal)}</a>
                                    <a href="${esc(hrefM365Family)}" role="menuitem">${esc(t.navM365Family)}</a>
                                    <a href="${esc(mailM365Business)}" role="menuitem">${esc(t.navM365Business)}</a>
                                </div>
                            </div>
                            <a href="#">${esc(t.navAntivirus)}</a>
                        </nav>
                    </div>
                    
                    <div class="right-section">
                        <a href="tel:+393925580413" class="support-info" title="${esc(t.assistanceSmall)}: +39 392 558 0413">
                            <div class="support-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 1a9 9 0 0 0-9 9v7c0 1.66 1.34 3 3 3h3v-8H5v-2c0-3.87 3.13-7 7-7s7 3.13 7 7v2h-4v8h3c1.66 0 3-1.34 3-3v-7a9 9 0 0 0-9-9z"/></svg>
                            </div>
                            <div class="support-text">
                                <small>${esc(t.assistanceSmall)}</small>
                                <span>+39 392 558 0413</span>
                            </div>
                        </a>

                        <div class="divider"></div>

                        <div class="lang-wrapper">
                            <button type="button" class="lang-selector" aria-haspopup="true" aria-expanded="false" aria-label="${esc(t.selectLanguage)}">
                                <img class="flag-icon" src="${esc(flagSrc(activeLang.flag))}" alt="" decoding="async">
                                <span>${activeLang.label}</span>
                                <svg class="chevron-down" viewBox="0 0 24 24"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>
                            </button>
                            <div class="lang-dropdown" role="menu">
                                ${otherLangs.map(l => `
                                <a href="${esc(hrefForLang(l.code))}" class="lang-option" role="menuitem" hreflang="${l.code}">
                                    <img class="flag-icon" src="${esc(flagSrc(l.flag))}" alt="" decoding="async">
                                    ${l.label}
                                </a>`).join('')}
                            </div>
                        </div>

                        <div class="divider"></div>

                        <a href="${esc(cartHref)}" class="cart-wrapper" aria-label="${esc(cartAriaForCount(0))}">
                            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z"/></svg>
                            <span class="cart-badge" aria-hidden="true">0</span>
                        </a>

                        <button type="button" class="btn-signin">${esc(t.signIn)}</button>
                    </div>
                </div>

                <div class="overlay"></div>
                <div class="mobile-drawer">
                    <div class="drawer-header">
                        <a href="${esc(homeHref)}" class="logo">
                            <img src="${esc(logoSrc)}" width="260" height="52" alt="${esc(t.logoAlt)}">
                        </a>
                        <button type="button" class="close-drawer" aria-label="${esc(t.closeNavMenu)}">
                            <svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
                        </button>
                    </div>
                    
                    <nav class="drawer-nav">
                        <a href="${esc(homeHref)}"${isHome ? ' class="active"' : ''}>${esc(t.navHome)}</a>
                        <a href="#">${esc(t.navOs)}</a>
                        <div class="drawer-m365-block">
                            <div class="drawer-m365-heading">${esc(t.navM365)}</div>
                            <a href="${esc(hrefM365Solutions)}"${isM365Solutions ? ' class="active"' : ''}>${esc(t.navM365Overview)}</a>
                            <a href="${esc(hrefM365Personal)}"${isM365Personal ? ' class="active"' : ''}>${esc(t.navM365Personal)}</a>
                            <a href="${esc(hrefM365Family)}"${isM365Family ? ' class="active"' : ''}>${esc(t.navM365Family)}</a>
                            <a href="${esc(mailM365Business)}">${esc(t.navM365Business)}</a>
                        </div>
                        <a href="#">${esc(t.navAntivirus)}</a>
                    </nav>
                    
                    <div class="drawer-section-title">${esc(t.selectLanguage)}</div>
                    <div class="drawer-langs">
                        ${LANGS.map(l => `
                        <a href="${esc(hrefForLang(l.code))}" class="drawer-lang-link${l.code === activeLang.code ? ' active' : ''}" hreflang="${l.code}">
                            <img class="flag-icon" src="${esc(flagSrc(l.flag))}" alt="" decoding="async">
                            ${l.label}
                        </a>`).join('')}
                    </div>
                    
                    <div class="drawer-footer">
                        <button type="button" class="drawer-btn-signin">${esc(t.signIn)}</button>
                        <a href="tel:+393925580413" class="drawer-assist">
                            <div class="drawer-assist-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24"><path d="M12 1a9 9 0 0 0-9 9v7c0 1.66 1.34 3 3 3h3v-8H5v-2c0-3.87 3.13-7 7-7s7 3.13 7 7v2h-4v8h3c1.66 0 3-1.34 3-3v-7a9 9 0 0 0-9-9z"/></svg>
                            </div>
                            <div class="drawer-assist-text">
                                <span class="drawer-assist-label">${esc(t.assistanceSmall)}</span>
                                <span class="drawer-assist-number">+39 392 558 0413</span>
                            </div>
                        </a>
                    </div>
                </div>
            `;

            const toggle = this.shadowRoot.querySelector('.mobile-toggle');
            const close = this.shadowRoot.querySelector('.close-drawer');
            const overlay = this.shadowRoot.querySelector('.overlay');
            const drawer = this.shadowRoot.querySelector('.mobile-drawer');
            const langWrapper = this.shadowRoot.querySelector('.lang-wrapper');
            const langSelector = this.shadowRoot.querySelector('.lang-selector');

            const openMenu = () => {
                if (drawer) drawer.classList.add('open');
                if (overlay) overlay.classList.add('open');
            };
            const closeMenu = () => {
                if (drawer) drawer.classList.remove('open');
                if (overlay) overlay.classList.remove('open');
            };

            if (toggle) toggle.addEventListener('click', openMenu);
            if (close) close.addEventListener('click', closeMenu);
            if (overlay) overlay.addEventListener('click', closeMenu);

            const toggleLangMenu = (e) => {
                if (e) e.stopPropagation();
                const m365WClose = this.shadowRoot.querySelector('.nav-m365-wrap');
                const m365CClose = this.shadowRoot.querySelector('.nav-m365-caret');
                if (m365WClose) m365WClose.classList.remove('open');
                if (m365CClose) m365CClose.setAttribute('aria-expanded', 'false');
                if (!langWrapper || !langSelector) return;
                const isOpen = langWrapper.classList.toggle('open');
                langSelector.setAttribute('aria-expanded', isOpen);
            };

            if (langSelector && langWrapper) {
                langSelector.addEventListener('click', (e) => {
                    e.stopPropagation();
                    toggleLangMenu(e);
                });
                langSelector.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        e.stopPropagation();
                        toggleLangMenu(e);
                    }
                });
            }

            const m365Wrap = this.shadowRoot.querySelector('.nav-m365-wrap');
            const m365Caret = this.shadowRoot.querySelector('.nav-m365-caret');
            const closeM365Menu = () => {
                if (!m365Wrap || !m365Caret) return;
                m365Wrap.classList.remove('open');
                m365Caret.setAttribute('aria-expanded', 'false');
            };
            if (m365Caret && m365Wrap) {
                m365Caret.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    if (langWrapper) {
                        langWrapper.classList.remove('open');
                        if (langSelector) langSelector.setAttribute('aria-expanded', 'false');
                    }
                    const isOpen = m365Wrap.classList.toggle('open');
                    m365Caret.setAttribute('aria-expanded', isOpen);
                });
                this.shadowRoot.querySelectorAll('.nav-m365-dropdown a').forEach((a) => {
                    a.addEventListener('click', closeM365Menu);
                });
            }

            this.__docClickHandler = (e) => {
                const path = typeof e.composedPath === 'function' ? e.composedPath() : [];
                if (langWrapper && langSelector && !path.includes(langWrapper)) {
                    langWrapper.classList.remove('open');
                    langSelector.setAttribute('aria-expanded', 'false');
                }
                const m365W = this.shadowRoot.querySelector('.nav-m365-wrap');
                const m365C = this.shadowRoot.querySelector('.nav-m365-caret');
                if (m365W && !path.includes(m365W)) {
                    m365W.classList.remove('open');
                    if (m365C) m365C.setAttribute('aria-expanded', 'false');
                }
            };
            this.__docKeydownHandler = (e) => {
                if (e.key !== 'Escape') return;
                if (langWrapper?.classList.contains('open')) {
                    langWrapper.classList.remove('open');
                    if (langSelector) {
                        langSelector.setAttribute('aria-expanded', 'false');
                        langSelector.focus();
                    }
                    return;
                }
                const m365W = this.shadowRoot.querySelector('.nav-m365-wrap');
                const m365C = this.shadowRoot.querySelector('.nav-m365-caret');
                if (m365W?.classList.contains('open')) {
                    m365W.classList.remove('open');
                    if (m365C) {
                        m365C.setAttribute('aria-expanded', 'false');
                        m365C.focus();
                    }
                }
            };
            document.addEventListener('click', this.__docClickHandler);
            document.addEventListener('keydown', this.__docKeydownHandler);

            // TODO: collegare btn-signin e drawer-btn-signin al sistema di autenticazione
            //       (es. Stripe Identity, custom auth) — al momento visivi/placeholder.
            const cartLink = this.shadowRoot.querySelector('a.cart-wrapper');
            const cartBadge = this.shadowRoot.querySelector('.cart-badge');
            let prevCartQty = null;
            let cartBadgePopTimer = null;
            let cartIconNudgeTimer = null;
            const syncCartChrome = () => {
                const count =
                    window.AmlCart && typeof window.AmlCart.totalQty === 'function' ? window.AmlCart.totalQty() : 0;
                const increased = prevCartQty !== null && count > prevCartQty;

                if (cartBadge) {
                    cartBadge.textContent = count > 99 ? '99+' : String(count);
                    cartBadge.classList.toggle('is-visible', count > 0);
                    if (increased && count > 0) {
                        cartBadge.classList.remove('cart-badge-pop');
                        void cartBadge.offsetWidth;
                        cartBadge.classList.add('cart-badge-pop');
                        clearTimeout(cartBadgePopTimer);
                        cartBadgePopTimer = setTimeout(function () {
                            cartBadge.classList.remove('cart-badge-pop');
                        }, 600);
                    }
                }
                if (cartLink) {
                    cartLink.setAttribute('aria-label', cartAriaForCount(count));
                    if (increased) {
                        cartLink.classList.remove('cart-nudge');
                        void cartLink.offsetWidth;
                        cartLink.classList.add('cart-nudge');
                        clearTimeout(cartIconNudgeTimer);
                        cartIconNudgeTimer = setTimeout(function () {
                            cartLink.classList.remove('cart-nudge');
                        }, 650);
                    }
                }
                prevCartQty = count;
            };
            syncCartChrome();
            this.__syncCartChrome = syncCartChrome;
            document.addEventListener('aml-cart-changed', syncCartChrome);
        }

        disconnectedCallback() {
            if (typeof this.__docClickHandler === 'function') {
                document.removeEventListener('click', this.__docClickHandler);
                this.__docClickHandler = null;
            }
            if (typeof this.__docKeydownHandler === 'function') {
                document.removeEventListener('keydown', this.__docKeydownHandler);
                this.__docKeydownHandler = null;
            }
            if (typeof this.__syncCartChrome === 'function') {
                document.removeEventListener('aml-cart-changed', this.__syncCartChrome);
                this.__syncCartChrome = null;
            }
        }
    }

    if (!customElements.get('ecommerce-header')) {
        customElements.define('ecommerce-header', EcommerceHeader);
    }
})();