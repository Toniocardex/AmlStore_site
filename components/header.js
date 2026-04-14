(function () {
    'use strict';

    const LANGS = [
        { code: 'it', label: 'IT', flag: 'it' },
        { code: 'en', label: 'EN', flag: 'gb' },
        { code: 'fr', label: 'FR', flag: 'fr' },
        { code: 'de', label: 'DE', flag: 'de' },
        { code: 'es', label: 'ES', flag: 'es' },
    ];

    const HEADER_I18N = {
        it: {
            logoAlt: 'Aml Store',
            navHome: 'Home',
            navOs: 'Sistemi Operativi',
            navOffice: 'Office',
            navAntivirus: 'Antivirus',
            assistanceSmall: 'Assistenza',
            openNavMenu: 'Apri menu di navigazione',
            closeNavMenu: 'Chiudi menu',
            selectLanguage: 'Seleziona lingua',
            cartAria: 'Carrello, 2 articoli',
            signIn: 'Accedi',
            drawerAssist: 'Assistenza: +39 02 1234 5678',
        },
        en: {
            logoAlt: 'Aml Store',
            navHome: 'Home',
            navOs: 'Operating systems',
            navOffice: 'Office',
            navAntivirus: 'Antivirus',
            assistanceSmall: 'Support',
            openNavMenu: 'Open navigation menu',
            closeNavMenu: 'Close menu',
            selectLanguage: 'Select language',
            cartAria: 'Shopping cart, 2 items',
            signIn: 'Sign in',
            drawerAssist: 'Support: +39 02 1234 5678',
        },
        fr: {
            logoAlt: 'Aml Store',
            navHome: 'Home',
            navOs: "Systèmes d'exploitation",
            navOffice: 'Office',
            navAntivirus: 'Antivirus',
            assistanceSmall: 'Assistance',
            openNavMenu: 'Ouvrir le menu de navigation',
            closeNavMenu: 'Fermer le menu',
            selectLanguage: 'Choisir la langue',
            cartAria: 'Panier, 2 articles',
            signIn: 'Se connecter',
            drawerAssist: 'Assistance : +39 02 1234 5678',
        },
        de: {
            logoAlt: 'Aml Store',
            navHome: 'Home',
            navOs: 'Betriebssysteme',
            navOffice: 'Office',
            navAntivirus: 'Antivirus',
            assistanceSmall: 'Support',
            openNavMenu: 'Navigationsmenü öffnen',
            closeNavMenu: 'Menü schließen',
            selectLanguage: 'Sprache wählen',
            cartAria: 'Warenkorb, 2 Artikel',
            signIn: 'Anmelden',
            drawerAssist: 'Support: +39 02 1234 5678',
        },
        es: {
            logoAlt: 'Aml Store',
            navHome: 'Home',
            navOs: 'Sistemas operativos',
            navOffice: 'Office',
            navAntivirus: 'Antivirus',
            assistanceSmall: 'Asistencia',
            openNavMenu: 'Abrir menú de navegación',
            closeNavMenu: 'Cerrar menú',
            selectLanguage: 'Seleccionar idioma',
            cartAria: 'Carrito, 2 artículos',
            signIn: 'Iniciar sesión',
            drawerAssist: 'Asistencia: +39 02 1234 5678',
        },
    };

    function amlStaticRootFromHeaderScript() {
        const needle = '/components/header.js';
        const scripts = document.scripts;
        for (let i = 0; i < scripts.length; i++) {
            const raw = scripts[i].getAttribute('src');
            if (!raw) continue;
            let pathname;
            try {
                pathname = new URL(raw, window.location.href).pathname;
            } catch (_) {
                continue;
            }
            if (!pathname.endsWith(needle)) continue;
            return pathname.slice(0, -needle.length);
        }
        return '';
    }

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

            const segments = window.location.pathname.split('/').filter(Boolean);
            const langCode = segments.find((seg) => LANGS.some((l) => l.code === seg)) || 'it';
            const activeLang = LANGS.find((l) => l.code === langCode) || LANGS[0];
            const otherLangs = LANGS.filter((l) => l.code !== activeLang.code);
            const langSegIdx = segments.indexOf(activeLang.code);
            const pathPrefix = langSegIdx > 0 ? '/' + segments.slice(0, langSegIdx).join('/') : '';
            const hrefForLang = (code) => `${pathPrefix}/${code}/`;
            const homeHref = hrefForLang(activeLang.code);
            const t = HEADER_I18N[activeLang.code] || HEADER_I18N.it;
            const esc = (s) =>
                String(s)
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;');

            const staticRoot = amlStaticRootFromHeaderScript();
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
                        /* Condivisione tavolozza colori col Footer */
                        --bg-base: rgba(5, 5, 5, 0.75);
                        --bg-surface: rgba(17, 17, 17, 0.85);
                        --border-color: rgba(255, 255, 255, 0.08);
                        --text-primary: #ffffff;
                        --text-secondary: #a1a1aa;
                        --text-muted: #71717a;
                        --accent: #ffffff; 
                        
                        /* FIX: Spostiamo lo sfondo e il blur sul componente radice 
                           così prende il 100% della larghezza e l'header-container può
                           avere la max-width per allinearsi al footer */
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
                        height: 80px;
                        
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
                    .logo:focus-visible { outline: 2px solid var(--text-primary); outline-offset: 4px; }
                    .logo img {
                        height: 40px;
                        width: auto;
                        display: block;
                        filter: brightness(0) invert(1);
                        color: white;
                        font-weight: 800;
                        font-size: 1.2rem;
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

                    .right-section {
                        display: flex;
                        align-items: center;
                        gap: clamp(0.75rem, 1.5vw, 1.5rem); /* Spazio fluido tra gli elementi di destra */
                    }

                    .support-info {
                        display: flex;
                        align-items: center;
                        gap: 0.75rem;
                        cursor: default;
                        text-decoration: none; /* In caso lo si trasformi in link in futuro */
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
                        display: none;
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
                    }
                    .lang-wrapper.open .lang-dropdown { display: block; animation: dropIn 0.25s cubic-bezier(0.16, 1, 0.3, 1); }

                    @keyframes dropIn {
                        from { opacity: 0; transform: translateY(-8px) scale(0.98); }
                        to { opacity: 1; transform: translateY(0) scale(1); }
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
                    }
                    .cart-wrapper:hover {
                        color: var(--text-primary);
                        background: rgba(255, 255, 255, 0.08);
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
                        width: 18px;
                        height: 18px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border-radius: 50%;
                        border: 2px solid #050505; /* Bordo che "buca" l'icona sottostante */
                        box-shadow: 0 2px 4px rgba(0,0,0,0.5);
                    }

                    .btn-signin {
                        background: linear-gradient(135deg, #ffffff 0%, #e4e4e7 100%);
                        color: #000000; /* Testo in alto contrasto */
                        border: none;
                        padding: 0.6rem 1.4rem;
                        border-radius: 999px;
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

                    .mobile-toggle {
                        display: none;
                        background: none;
                        border: none;
                        color: var(--text-primary);
                        cursor: pointer;
                        padding: 0.5rem;
                        margin-left: -0.5rem; /* Compensa il padding per l'allineamento */
                        transition: opacity 0.2s;
                        touch-action: manipulation; /* Ottimizzazione touch */
                    }
                    .mobile-toggle:hover {
                        opacity: 0.7;
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
                            height: 64px; /* Header più sottile su mobile */
                            gap: 1rem;
                        }
                        .btn-signin { display: none; } /* Lo user troverà il login nel drawer */
                        .divider { display: none; }
                        .lang-selector span { display: none; } /* Solo icona lingua */
                        .lang-selector { padding: 0.4rem; }
                        .right-section { gap: 0.5rem; }
                        .logo img { height: 32px; } /* Logo rimpicciolito */
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
                        opacity: 0; pointer-events: none; transition: opacity 0.4s ease;
                    }
                    .overlay.open { opacity: 1; pointer-events: auto; }

                    .mobile-drawer {
                        position: fixed; top: 0; left: -100%;
                        width: 100%; max-width: 320px; /* Meglio 320px per mobile */
                        height: 100vh;
                        background: var(--bg-surface);
                        backdrop-filter: blur(20px);
                        -webkit-backdrop-filter: blur(20px);
                        border-right: 1px solid var(--border-color);
                        z-index: 2000;
                        transition: left 0.4s cubic-bezier(0.16, 1, 0.3, 1);
                        padding: 1.5rem 1.25rem;
                        display: flex; flex-direction: column;
                        overflow-y: auto;
                        box-shadow: 10px 0 30px rgba(0,0,0,0.5);
                    }
                    .mobile-drawer.open { left: 0; }

                    .drawer-header {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 2rem;
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
                    .close-drawer svg { width: 20px; height: 20px; fill: currentColor; }

                    .drawer-nav {
                        display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 2.5rem;
                    }
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
                    .drawer-assist {
                        text-align: center;
                        font-size: 0.85rem;
                        color: var(--text-muted);
                    }
                </style>

                <div class="header-container">
                    <div class="left-section">
                        <button type="button" class="mobile-toggle" aria-label="${esc(t.openNavMenu)}">
                            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"></path></svg>
                        </button>
                        <a href="${esc(homeHref)}" class="logo">
                            <img src="${esc(logoSrc)}" width="200" height="40" alt="${esc(t.logoAlt)}">
                        </a>
                        <nav class="nav-links">
                            <a href="${esc(homeHref)}" class="active">${esc(t.navHome)}</a>
                            <a href="#">${esc(t.navOs)}</a>
                            <a href="#">${esc(t.navOffice)}</a>
                            <a href="#">${esc(t.navAntivirus)}</a>
                        </nav>
                    </div>
                    
                    <div class="right-section">
                        <div class="support-info" title="${esc(t.assistanceSmall)}: +39 02 1234 5678">
                            <div class="support-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 1a9 9 0 0 0-9 9v7c0 1.66 1.34 3 3 3h3v-8H5v-2c0-3.87 3.13-7 7-7s7 3.13 7 7v2h-4v8h3c1.66 0 3-1.34 3-3v-7a9 9 0 0 0-9-9z"/></svg>
                            </div>
                            <div class="support-text">
                                <small>${esc(t.assistanceSmall)}</small>
                                <span>+39 02 1234 5678</span>
                            </div>
                        </div>

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

                        <div class="cart-wrapper" role="button" tabindex="0" aria-label="${esc(t.cartAria)}">
                            <svg viewBox="0 0 24 24"><path d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z"/></svg>
                            <div class="cart-badge">2</div>
                        </div>

                        <button type="button" class="btn-signin">${esc(t.signIn)}</button>
                    </div>
                </div>

                <div class="overlay"></div>
                <div class="mobile-drawer">
                    <div class="drawer-header">
                        <a href="${esc(homeHref)}" class="logo">
                            <img src="${esc(logoSrc)}" width="160" height="32" alt="${esc(t.logoAlt)}">
                        </a>
                        <button type="button" class="close-drawer" aria-label="${esc(t.closeNavMenu)}">
                            <svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
                        </button>
                    </div>
                    
                    <nav class="drawer-nav">
                        <a href="${esc(homeHref)}" class="active">${esc(t.navHome)}</a>
                        <a href="#">${esc(t.navOs)}</a>
                        <a href="#">${esc(t.navOffice)}</a>
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
                        <div class="drawer-assist">${esc(t.drawerAssist)}</div>
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

            document.addEventListener('click', () => {
                if (!langWrapper || !langSelector) return;
                langWrapper.classList.remove('open');
                langSelector.setAttribute('aria-expanded', 'false');
            });

            document.addEventListener('keydown', (e) => {
                if (e.key !== 'Escape' || !langWrapper?.classList.contains('open')) return;
                langWrapper.classList.remove('open');
                if (langSelector) {
                    langSelector.setAttribute('aria-expanded', 'false');
                    langSelector.focus();
                }
            });
        }
    }

    if (!customElements.get('ecommerce-header')) {
        customElements.define('ecommerce-header', EcommerceHeader);
    }
})();