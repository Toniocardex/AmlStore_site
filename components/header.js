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
                        --bg-base: rgba(5, 5, 5, 0.85);
                        --bg-surface: #111111;
                        --border-color: rgba(255, 255, 255, 0.08);
                        --text-primary: #ffffff;
                        --text-secondary: #a1a1aa;
                        --text-muted: #71717a;
                        --accent: #3b82f6;
                        --accent-hover: #60a5fa;
                    }

                    * { box-sizing: border-box; margin: 0; padding: 0; }

                    .header-container {
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        height: 80px;
                        padding: 0 clamp(1.5rem, 5vw, 4rem);
                        background-color: var(--bg-base);
                        backdrop-filter: blur(16px);
                        -webkit-backdrop-filter: blur(16px);
                        border-bottom: 1px solid var(--border-color);
                    }

                    .left-section {
                        display: flex;
                        align-items: center;
                        gap: 3rem;
                    }

                    .logo {
                        display: flex;
                        align-items: center;
                        text-decoration: none;
                        transition: opacity 0.2s ease;
                        border-radius: 6px;
                    }
                    .logo:hover { opacity: 0.9; }
                    .logo:focus-visible { outline: 2px solid var(--accent); outline-offset: 4px; }
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
                        gap: 2rem;
                    }

                    .nav-links a {
                        color: var(--text-secondary);
                        text-decoration: none;
                        font-size: 0.9rem;
                        font-weight: 500;
                        transition: color 0.2s ease;
                        position: relative;
                    }
                    .nav-links a:hover {
                        color: var(--text-primary);
                    }
                    .nav-links a.active {
                        color: var(--text-primary);
                        font-weight: 600;
                    }
                    .nav-links a.active::after {
                        content: '';
                        position: absolute;
                        bottom: -6px;
                        left: 0;
                        width: 100%;
                        height: 2px;
                        background-color: var(--text-primary);
                        border-radius: 2px;
                    }

                    .right-section {
                        display: flex;
                        align-items: center;
                        gap: 1.5rem;
                    }

                    .support-info {
                        display: flex;
                        align-items: center;
                        gap: 0.75rem;
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
                    }
                    .support-text {
                        display: flex;
                        flex-direction: column;
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
                        background-color: var(--border-color);
                    }

                    .lang-wrapper { position: relative; }
                    .lang-selector {
                        display: flex;
                        align-items: center;
                        gap: 0.5rem;
                        background: none;
                        border: none;
                        color: var(--text-secondary);
                        font-size: 0.9rem;
                        font-weight: 500;
                        cursor: pointer;
                        font-family: inherit;
                        padding: 0.5rem;
                        border-radius: 6px;
                        transition: color 0.2s, background 0.2s;
                    }
                    .lang-selector:hover,
                    .lang-wrapper.open .lang-selector {
                        color: var(--text-primary);
                        background: rgba(255, 255, 255, 0.05);
                    }
                    /* Sostituto visivo se manca l'immagine della bandiera */
                    .lang-selector img {
                        width: 20px;
                        height: 20px;
                        border-radius: 50%;
                        object-fit: cover;
                        background: rgba(255, 255, 255, 0.1);
                        color: transparent;
                    }
                    .chevron-down {
                        width: 14px;
                        height: 14px;
                        fill: currentColor;
                        transition: transform 0.2s ease;
                    }
                    .lang-wrapper.open .chevron-down {
                        transform: rotate(180deg);
                    }

                    .lang-dropdown {
                        display: none;
                        position: absolute;
                        top: calc(100% + 0.5rem);
                        right: 0;
                        background: var(--bg-surface);
                        border: 1px solid var(--border-color);
                        border-radius: 12px;
                        padding: 0.5rem;
                        min-width: 140px;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                    }
                    .lang-wrapper.open .lang-dropdown { display: block; animation: fadeIn 0.2s ease; }

                    @keyframes fadeIn {
                        from { opacity: 0; transform: translateY(-5px); }
                        to { opacity: 1; transform: translateY(0); }
                    }

                    .lang-option {
                        display: flex;
                        align-items: center;
                        gap: 0.75rem;
                        padding: 0.5rem 0.75rem;
                        color: var(--text-secondary);
                        text-decoration: none;
                        font-size: 0.85rem;
                        font-weight: 500;
                        border-radius: 6px;
                        transition: background 0.2s, color 0.2s;
                    }
                    .lang-option:hover {
                        background: rgba(255, 255, 255, 0.08);
                        color: var(--text-primary);
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
                        width: 40px;
                        height: 40px;
                        border-radius: 50%;
                        color: var(--text-secondary);
                        cursor: pointer;
                        transition: color 0.2s, background 0.2s;
                    }
                    .cart-wrapper:hover {
                        color: var(--text-primary);
                        background: rgba(255, 255, 255, 0.05);
                    }
                    .cart-wrapper svg {
                        width: 20px;
                        height: 20px;
                        fill: currentColor;
                    }
                    .cart-badge {
                        position: absolute;
                        top: 2px;
                        right: 2px;
                        background: #ef4444;
                        color: white;
                        font-size: 0.65rem;
                        font-weight: 700;
                        width: 16px;
                        height: 16px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border-radius: 50%;
                        border: 2px solid var(--bg-base);
                    }

                    .btn-signin {
                        background: var(--text-primary);
                        color: var(--bg-surface);
                        border: none;
                        padding: 0.6rem 1.25rem;
                        border-radius: 999px;
                        font-family: inherit;
                        font-size: 0.9rem;
                        font-weight: 600;
                        cursor: pointer;
                        transition: transform 0.2s, opacity 0.2s;
                    }
                    .btn-signin:hover {
                        transform: translateY(-1px);
                        opacity: 0.9;
                    }

                    .mobile-toggle {
                        display: none;
                        background: none;
                        border: none;
                        color: var(--text-primary);
                        cursor: pointer;
                        padding: 0.5rem;
                    }
                    .mobile-toggle svg {
                        width: 24px;
                        height: 24px;
                        fill: none;
                        stroke: currentColor;
                        stroke-width: 2;
                        stroke-linecap: round;
                    }

                    @media (max-width: 1100px) {
                        .nav-links, .support-info, .divider:first-of-type { display: none; }
                        .mobile-toggle { display: block; }
                        .left-section { gap: 1rem; }
                    }

                    @media (max-width: 640px) {
                        .header-container { padding: 0 1rem; height: 70px; }
                        .btn-signin { display: none; }
                        .divider { display: none; }
                        .lang-selector span { display: none; }
                        .right-section { gap: 0.5rem; }
                        .logo img { height: 32px; }
                    }

                    /* DRAWER MOBILE */
                    .overlay {
                        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                        background: rgba(0,0,0,0.6);
                        backdrop-filter: blur(4px);
                        z-index: 1999;
                        opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
                    }
                    .overlay.open { opacity: 1; pointer-events: auto; }

                    .mobile-drawer {
                        position: fixed; top: 0; left: -100%;
                        width: 85%; max-width: 360px; height: 100vh;
                        background: var(--bg-surface);
                        border-right: 1px solid var(--border-color);
                        z-index: 2000;
                        transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                        padding: 1.5rem;
                        display: flex; flex-direction: column;
                        overflow-y: auto;
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
                        transition: background 0.2s;
                    }
                    .close-drawer:hover { background: rgba(255, 255, 255, 0.1); }
                    .close-drawer svg { width: 20px; height: 20px; fill: currentColor; }

                    .drawer-nav {
                        display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 2rem;
                    }
                    .drawer-nav a {
                        color: var(--text-primary);
                        text-decoration: none;
                        font-size: 1.1rem;
                        font-weight: 600;
                        padding: 0.75rem 1rem;
                        border-radius: 8px;
                        transition: background 0.2s;
                    }
                    .drawer-nav a:hover, .drawer-nav a.active {
                        background: rgba(255, 255, 255, 0.05);
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
                        border-radius: 8px;
                        font-size: 0.9rem; font-weight: 500;
                        color: var(--text-secondary);
                        text-decoration: none;
                        border: 1px solid transparent;
                        transition: background 0.2s, border-color 0.2s, color 0.2s;
                    }
                    .drawer-lang-link.active {
                        background: rgba(255, 255, 255, 0.05);
                        border-color: var(--border-color);
                        color: var(--text-primary);
                    }
                    .drawer-lang-link:hover:not(.active) {
                        background: rgba(255, 255, 255, 0.02);
                        color: var(--text-primary);
                    }
                    .drawer-lang-link img {
                        width: 20px; height: 20px; border-radius: 50%; object-fit: cover;
                        background: rgba(255, 255, 255, 0.1); color: transparent;
                    }

                    .drawer-footer {
                        margin-top: 2rem;
                        padding-top: 1.5rem;
                        border-top: 1px solid var(--border-color);
                    }
                    .drawer-btn-signin {
                        width: 100%;
                        background: var(--text-primary);
                        color: var(--bg-surface);
                        border: none;
                        padding: 0.85rem;
                        border-radius: 8px;
                        font-weight: 600;
                        font-size: 1rem;
                        cursor: pointer;
                        margin-bottom: 1rem;
                        transition: opacity 0.2s;
                    }
                    .drawer-btn-signin:hover { opacity: 0.9; }
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
                        <div class="support-info">
                            <div class="support-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
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

            // --- Event Listeners ---
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