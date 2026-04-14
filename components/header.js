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

/** Prefisso path statici (es. /repo) da components/header.js — compatibile con defer e base path Pages. */
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
                    font-family: 'Montserrat', sans-serif;
                    /* Allineato al footer — Premium Dark */
                    --bg-base: #050505;
                    --bg-surface: #111111;
                    --border-color: rgba(255, 255, 255, 0.08);
                    --text-primary: #ffffff;
                    --text-secondary: #a1a1aa;
                    --text-muted: #71717a;
                    --accent: #3b82f6;
                    --accent-hover: #60a5fa;
                    --glow-color: rgba(59, 130, 246, 0.15);

                    --h-height: 84px;
                    --tap-min: 44px;
                    /* Pannello chiaro (sinistra) / blu (destra) — separati dal clip-path */
                    --color-gradient-start: #003182;
                    --color-gradient-end: #1a5fd1;
                    --text-dark: #1a1a1a;
                    --text-light: #ffffff;
                    --text-grey: #5c5c5c;
                    --nav-active: #003182;
                    --neon-line: rgba(180, 220, 255, 0.95);
                    --neon-glow: rgba(26, 95, 209, 0.85);
                    --neon-glow-soft: rgba(100, 170, 255, 0.45);

                    position: relative;
                    z-index: 1000;
                    border-bottom: 1px solid rgba(0, 49, 130, 0.08);
                    background: transparent;
                    color: var(--text-dark);
                    overflow: hidden;
                }

                * { box-sizing: border-box; margin: 0; padding: 0; }

                .header-bg-glow {
                    position: absolute;
                    top: 0;
                    left: 42%;
                    right: 0;
                    transform: none;
                    width: auto;
                    height: 260px;
                    background: radial-gradient(ellipse 90% 100% at 50% 0%, var(--glow-color) 0%, transparent 72%);
                    pointer-events: none;
                    z-index: 0;
                }

                .header-container {
                    position: relative;
                    height: var(--h-height);
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    box-shadow: none;
                    overflow: hidden;
                }

                .bg-colored {
                    position: absolute;
                    top: 0; left: 0; right: 0; bottom: 0;
                    background: linear-gradient(118deg, var(--color-gradient-start) 0%, #0d4bb8 45%, var(--color-gradient-end) 100%);
                    z-index: 1;
                }

                .bg-white {
                    position: absolute;
                    top: 0; left: 0; bottom: 0;
                    width: 56%;
                    max-width: 720px;
                    background: linear-gradient(180deg, #ffffff 0%, #fafbfc 100%);
                    clip-path: polygon(0 0, calc(100% - 88px) 0, 100% 100%, 0 100%);
                    box-shadow: inset -1px 0 0 rgba(0, 49, 130, 0.06);
                    z-index: 2;
                }

                .content-wrapper {
                    position: relative;
                    z-index: 3;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    padding: 0 clamp(1.5rem, 5vw, 4rem);
                }

                .left-section {
                    display: flex;
                    align-items: center;
                    gap: clamp(1.25rem, 3vw, 2.75rem);
                    flex: 1;
                    min-width: 0;
                    color: var(--text-dark);
                }

                .logo {
                    display: flex;
                    align-items: center;
                    text-decoration: none;
                    border-radius: 12px;
                    outline-offset: 4px;
                }
                .logo:focus-visible {
                    outline: 2px solid var(--nav-active);
                }
                .logo img {
                    height: 56px;
                    width: auto;
                    display: block;
                    object-fit: contain;
                }

                .nav-links {
                    display: flex;
                    align-items: center;
                    gap: 0.35rem;
                }
                .nav-links a {
                    text-decoration: none;
                    color: var(--text-grey);
                    font-weight: 600;
                    font-size: 14px;
                    letter-spacing: 0.01em;
                    padding: 0.5rem 1.1rem;
                    border-radius: 999px;
                    background: linear-gradient(180deg, #ffffff 0%, #eef0f4 100%);
                    border: 1px solid rgba(0, 49, 130, 0.08);
                    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.07), inset 0 1px 0 rgba(255, 255, 255, 0.92);
                    transition: color 0.2s ease, background 0.2s ease, box-shadow 0.2s ease, transform 0.15s ease, border-color 0.2s ease;
                }
                .nav-links a:hover {
                    color: var(--text-dark);
                    background: linear-gradient(180deg, #ffffff 0%, #e4e7ed 100%);
                    border-color: rgba(0, 49, 130, 0.12);
                    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.95);
                    transform: translateY(-1px);
                }
                .nav-links a:active:not(.active) {
                    transform: translateY(0);
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.85);
                }
                .nav-links a.active {
                    color: rgba(255, 255, 255, 0.98);
                    font-weight: 700;
                    background: linear-gradient(118deg, var(--color-gradient-start) 0%, #0d4bb8 50%, var(--color-gradient-end) 100%);
                    border-color: rgba(255, 255, 255, 0.18);
                    box-shadow: 0 4px 16px rgba(0, 35, 90, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.2);
                    transform: none;
                }
                .nav-links a.active:hover {
                    color: #fff;
                    background: linear-gradient(118deg, #004099 0%, #1a5fd1 55%, #2b6fe0 100%);
                    box-shadow: 0 6px 20px rgba(0, 35, 90, 0.42), inset 0 1px 0 rgba(255, 255, 255, 0.22);
                    transform: translateY(-1px);
                }
                .nav-links a.active:active {
                    transform: translateY(0);
                    box-shadow: 0 3px 12px rgba(0, 35, 90, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.18);
                }

                .right-section {
                    display: flex;
                    align-items: center;
                    gap: 0;
                    color: var(--text-light);
                    flex-shrink: 0;
                }

                .rail-divider {
                    align-self: center;
                    width: 2px;
                    height: 30px;
                    flex-shrink: 0;
                    margin: 0 clamp(0.75rem, 1.8vw, 1.35rem);
                    border-radius: 99px;
                    background: linear-gradient(180deg,
                        rgba(255, 255, 255, 0.12) 0%,
                        var(--neon-line) 50%,
                        rgba(255, 255, 255, 0.12) 100%);
                    box-shadow:
                        0 0 8px rgba(200, 230, 255, 0.75),
                        0 0 16px var(--neon-glow),
                        0 0 26px rgba(0, 49, 130, 0.45);
                }

                .phone-number {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    font-size: 12px;
                    font-weight: 700;
                    letter-spacing: 0.04em;
                    color: rgba(255, 255, 255, 0.95);
                    white-space: nowrap;
                }
                .phone-number .phone-icon-wrap {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 34px;
                    height: 34px;
                    border-radius: 10px;
                    background: rgba(255, 255, 255, 0.14);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    transition: background 0.2s ease, border-color 0.2s ease;
                }
                .phone-number:hover .phone-icon-wrap {
                    background: rgba(255, 255, 255, 0.22);
                    border-color: rgba(255, 255, 255, 0.3);
                }
                .phone-number svg {
                    width: 16px;
                    height: 16px;
                    fill: currentColor;
                }
                .phone-number .phone-label {
                    display: flex;
                    flex-direction: column;
                    gap: 2px;
                    line-height: 1.2;
                }
                .phone-number .phone-label small {
                    font-size: 10px;
                    font-weight: 700;
                    letter-spacing: 0.12em;
                    opacity: 0.75;
                }

                /* ── Language selector ── */
                .lang-wrapper {
                    position: relative;
                }

                .lang-selector {
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                    min-height: var(--tap-min);
                    padding: 0 14px 0 12px;
                    font-size: 14px;
                    font-weight: 700;
                    letter-spacing: 0.02em;
                    cursor: pointer;
                    user-select: none;
                    color: rgba(255, 255, 255, 0.98);
                    background: rgba(255, 255, 255, 0.12);
                    border: 1px solid rgba(255, 255, 255, 0.28);
                    border-radius: 999px;
                    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
                    transition: background 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease, transform 0.15s ease;
                }
                .lang-selector:hover {
                    background: rgba(255, 255, 255, 0.2);
                    border-color: rgba(255, 255, 255, 0.45);
                    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
                }
                .lang-selector:focus {
                    outline: none;
                }
                .lang-selector:focus-visible {
                    outline: 2px solid #fff;
                    outline-offset: 3px;
                }
                .lang-wrapper.open .lang-selector {
                    background: rgba(255, 255, 255, 0.22);
                    border-color: rgba(255, 255, 255, 0.5);
                }
                .flag-icon {
                    width: 22px;
                    height: 22px;
                    border-radius: 50%;
                    border: 2px solid rgba(255, 255, 255, 0.35);
                    object-fit: cover;
                    object-position: center;
                    flex-shrink: 0;
                    box-shadow: 0 1px 4px rgba(0,0,0,0.15);
                    box-sizing: border-box;
                    display: block;
                }
                .chevron-down {
                    width: 12px;
                    height: 12px;
                    fill: currentColor;
                    opacity: 0.9;
                    transition: transform 0.2s ease;
                }
                .lang-wrapper.open .chevron-down {
                    transform: rotate(180deg);
                }

                .lang-dropdown {
                    display: none;
                    position: absolute;
                    top: calc(100% + 10px);
                    right: 0;
                    background: #fff;
                    border-radius: 14px;
                    box-shadow: 0 12px 40px rgba(0, 20, 60, 0.18);
                    border: 1px solid rgba(0, 49, 130, 0.08);
                    overflow: hidden;
                    min-width: 156px;
                    padding: 6px 0;
                    z-index: 100;
                }
                .lang-wrapper.open .lang-dropdown {
                    display: block;
                    animation: langDrop 0.18s ease-out;
                }
                @keyframes langDrop {
                    from { opacity: 0; transform: translateY(-6px); }
                    to { opacity: 1; transform: translateY(0); }
                }

                .lang-option {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    padding: 12px 16px;
                    font-size: 14px;
                    font-weight: 600;
                    color: #1a1a1a;
                    text-decoration: none;
                    transition: background 0.15s ease, color 0.15s ease;
                }
                .lang-option:hover,
                .lang-option:focus-visible {
                    background: #f0f4ff;
                    color: var(--color-gradient-start);
                }
                .lang-option .flag-icon {
                    border-color: rgba(0, 0, 0, 0.08);
                    box-shadow: none;
                }

                /* ── Cart ── */
                .cart-wrapper {
                    position: relative;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: var(--tap-min);
                    height: var(--tap-min);
                    border-radius: 14px;
                    color: var(--text-light);
                    transition: background 0.2s ease, transform 0.15s ease, color 0.2s ease;
                }
                .cart-wrapper:hover {
                    background: rgba(255, 255, 255, 0.12);
                    transform: translateY(-1px);
                }
                .cart-wrapper:focus-visible {
                    outline: 2px solid #fff;
                    outline-offset: 2px;
                }
                .cart-wrapper svg {
                    width: 24px;
                    height: 24px;
                    fill: currentColor;
                }
                .cart-badge {
                    position: absolute;
                    top: 6px;
                    right: 6px;
                    background: linear-gradient(135deg, #ff5e62, #e0243a);
                    color: white;
                    font-size: 10px;
                    font-weight: 800;
                    height: 18px;
                    min-width: 18px;
                    border-radius: 9px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 0 5px;
                    box-shadow: 0 2px 8px rgba(224,36,58,0.45);
                    border: 2px solid rgba(0, 49, 130, 0.35);
                }

                .btn-signin {
                    margin-left: clamp(0.35rem, 1vw, 0.75rem);
                    background: var(--text-light);
                    color: var(--color-gradient-start);
                    border: none;
                    padding: 0 22px;
                    min-height: var(--tap-min);
                    border-radius: 999px;
                    font-weight: 700;
                    font-size: 14px;
                    letter-spacing: 0.02em;
                    cursor: pointer;
                    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
                    transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease, color 0.2s ease;
                }
                .btn-signin:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.14);
                }
                .btn-signin:focus-visible {
                    outline: 2px solid #fff;
                    outline-offset: 3px;
                }
                .btn-signin:active {
                    transform: translateY(0);
                }

                .mobile-toggle {
                    display: none;
                    width: var(--tap-min);
                    height: var(--tap-min);
                    background: rgba(0, 49, 130, 0.06);
                    border: none;
                    border-radius: 12px;
                    cursor: pointer;
                    color: var(--text-dark);
                    flex-shrink: 0;
                    transition: background 0.2s ease, color 0.2s ease;
                }
                .mobile-toggle:hover {
                    background: rgba(0, 49, 130, 0.1);
                }
                .mobile-toggle:focus-visible {
                    outline: 2px solid var(--nav-active);
                    outline-offset: 2px;
                }
                .mobile-toggle svg {
                    width: 24px;
                    height: 24px;
                    stroke: currentColor;
                    stroke-width: 2;
                    stroke-linecap: round;
                }

                @media (max-width: 1100px) {
                    .bg-white { width: 52%; }
                    .nav-links { display: none; }
                    .mobile-toggle { display: flex; align-items: center; justify-content: center; }
                }

                @media (max-width: 768px) {
                    :host { --h-height: 72px; }
                    .bg-colored { display: none; }
                    .bg-white {
                        width: 100%;
                        max-width: none;
                        clip-path: none;
                        box-shadow: none;
                        background: linear-gradient(180deg, #ffffff 0%, #fafbfc 100%);
                    }
                    .content-wrapper { padding: 0 0.75rem 0 0.5rem; }

                    .logo img { height: 44px; }

                    .left-section { gap: 0.65rem; }
                    .right-section { color: var(--color-gradient-start); }

                    .rail-divider { display: none; }

                    .phone-number { display: none; }

                    .lang-selector {
                        color: var(--color-gradient-start);
                        background: rgba(0, 49, 130, 0.06);
                        border: 1px solid rgba(0, 49, 130, 0.12);
                        box-shadow: none;
                        padding: 0 12px 0 10px;
                        min-height: 42px;
                    }
                    .lang-selector:hover {
                        background: rgba(0, 49, 130, 0.1);
                        border-color: rgba(0, 49, 130, 0.2);
                    }
                    .lang-wrapper.open .lang-selector {
                        background: rgba(0, 49, 130, 0.12);
                    }
                    .lang-selector:focus-visible {
                        outline-color: var(--color-gradient-start);
                    }
                    .lang-selector .flag-icon {
                        border-color: rgba(0, 49, 130, 0.15);
                        box-shadow: none;
                    }

                    .cart-wrapper {
                        color: var(--color-gradient-start);
                    }
                    .cart-wrapper:hover {
                        background: rgba(0, 49, 130, 0.06);
                    }
                    .cart-wrapper:focus-visible {
                        outline-color: var(--color-gradient-start);
                    }
                    .cart-badge {
                        border-color: #fff;
                    }

                    .btn-signin {
                        margin-left: 0.35rem;
                        background: var(--color-gradient-start);
                        color: #fff;
                        padding: 0 16px;
                        min-height: 42px;
                        font-size: 13px;
                        box-shadow: 0 4px 12px rgba(0, 49, 130, 0.25);
                    }
                    .btn-signin:focus-visible {
                        outline-color: var(--color-gradient-start);
                    }
                }

                .mobile-drawer {
                    position: fixed;
                    top: 0; left: -100%;
                    width: 80%; max-width: 320px; height: 100vh;
                    background: var(--bg-surface);
                    z-index: 2000;
                    box-shadow: 5px 0 24px rgba(0, 0, 0, 0.5);
                    border-right: 1px solid var(--border-color);
                    transition: left 0.3s ease;
                    padding: 2rem;
                    display: flex; flex-direction: column; gap: 2rem;
                    color: var(--text-primary);
                }
                .mobile-drawer.open { left: 0; }
                .overlay {
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(0, 0, 0, 0.6); z-index: 1999;
                    opacity: 0; pointer-events: none; transition: opacity 0.3s;
                }
                .overlay.open { opacity: 1; pointer-events: auto; }
                .close-drawer {
                    align-self: flex-end;
                    background: rgba(255, 255, 255, 0.04);
                    border: 1px solid var(--border-color);
                    border-radius: 10px;
                    cursor: pointer;
                    color: var(--text-primary);
                    padding: 0.35rem;
                }
                .close-drawer svg {
                    width: 24px;
                    height: 24px;
                    display: block;
                    fill: currentColor;
                }

                .drawer-nav {
                    display: flex;
                    flex-direction: column;
                    gap: 0;
                    font-weight: 700;
                }
                .drawer-nav a {
                    color: var(--text-secondary);
                    text-decoration: none;
                    padding: 0.85rem 0;
                    border-bottom: 1px solid var(--border-color);
                    transition: color 0.2s ease;
                }
                .drawer-nav a:hover,
                .drawer-nav a:focus-visible {
                    color: var(--accent-hover);
                }
                .drawer-nav a:last-child {
                    border-bottom: none;
                }

                .drawer-langs {
                    display: flex;
                    gap: 8px;
                    flex-wrap: wrap;
                    padding-top: 0.5rem;
                    border-top: 1px solid var(--border-color);
                }
                .drawer-lang-link {
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    padding: 6px 10px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: 700;
                    color: var(--text-secondary);
                    text-decoration: none;
                    background: rgba(255, 255, 255, 0.04);
                    border: 1px solid var(--border-color);
                    transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
                }
                .drawer-lang-link.active {
                    background: rgba(59, 130, 246, 0.25);
                    color: var(--text-primary);
                    border-color: rgba(59, 130, 246, 0.45);
                }
                .drawer-lang-link:hover:not(.active) {
                    background: rgba(255, 255, 255, 0.08);
                    color: var(--accent-hover);
                    border-color: rgba(255, 255, 255, 0.12);
                }
                .drawer-lang-link .flag-icon {
                    width: 16px; height: 16px;
                    border: none;
                }

                .drawer-assist {
                    margin-top: auto;
                    font-size: 14px;
                    font-weight: 500;
                    color: var(--text-muted);
                    line-height: 1.5;
                }
            </style>

            <div class="header-container">
                <div class="header-bg-glow" aria-hidden="true"></div>
                <div class="bg-colored"></div>
                <div class="bg-white"></div>
                <div class="content-wrapper">
                    <div class="left-section">
                        <button type="button" class="mobile-toggle" aria-label="${esc(t.openNavMenu)}">
                            <svg viewBox="0 0 24 24"><path d="M3 12h18M3 6h18M3 18h18"></path></svg>
                        </button>
                        <a href="${esc(homeHref)}" class="logo">
                            <img src="${esc(logoSrc)}" width="200" height="56" alt="${esc(t.logoAlt)}">
                        </a>
                        <nav class="nav-links">
                            <a href="${esc(homeHref)}" class="active">${esc(t.navHome)}</a>
                            <a href="#">${esc(t.navOs)}</a>
                            <a href="#">${esc(t.navOffice)}</a>
                            <a href="#">${esc(t.navAntivirus)}</a>
                        </nav>
                    </div>
                    <div class="right-section">
                        <div class="phone-number">
                            <span class="phone-icon-wrap" aria-hidden="true">
                                <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                            </span>
                            <span class="phone-label">
                                <small>${esc(t.assistanceSmall)}</small>
                                <span>+39 02 1234 5678</span>
                            </span>
                        </div>

                        <span class="rail-divider" aria-hidden="true"></span>

                        <div class="lang-wrapper">
                            <div class="lang-selector" role="button" tabindex="0" aria-haspopup="true" aria-expanded="false" aria-label="${esc(t.selectLanguage)}">
                                <img class="flag-icon" src="${esc(flagSrc(activeLang.flag))}" alt="" width="22" height="22" decoding="async">
                                <span>${activeLang.label}</span>
                                <svg class="chevron-down" viewBox="0 0 24 24" aria-hidden="true"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>
                            </div>
                            <div class="lang-dropdown" role="menu">
                                ${otherLangs.map(l => `
                                <a href="${esc(hrefForLang(l.code))}" class="lang-option" role="menuitem" hreflang="${l.code}">
                                    <img class="flag-icon" src="${esc(flagSrc(l.flag))}" alt="" width="22" height="22" decoding="async">
                                    ${l.label}
                                </a>`).join('')}
                            </div>
                        </div>

                        <span class="rail-divider" aria-hidden="true"></span>

                        <div class="cart-wrapper" role="button" tabindex="0" aria-label="${esc(t.cartAria)}">
                            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z"/></svg>
                            <div class="cart-badge">2</div>
                        </div>
                        <button type="button" class="btn-signin">${esc(t.signIn)}</button>
                    </div>
                </div>
            </div>

            <div class="overlay"></div>
            <div class="mobile-drawer">
                <button type="button" class="close-drawer" aria-label="${esc(t.closeNavMenu)}"><svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg></button>
                <nav class="drawer-nav">
                    <a href="${esc(homeHref)}">${esc(t.navHome)}</a>
                    <a href="#">${esc(t.navOs)}</a>
                    <a href="#">${esc(t.navOffice)}</a>
                    <a href="#">${esc(t.navAntivirus)}</a>
                </nav>
                <div class="drawer-langs">
                    ${LANGS.map(l => `
                    <a href="${esc(hrefForLang(l.code))}" class="drawer-lang-link${l.code === activeLang.code ? ' active' : ''}" hreflang="${l.code}">
                        <img class="flag-icon" src="${esc(flagSrc(l.flag))}" alt="" width="22" height="22" decoding="async">
                        ${l.label}
                    </a>`).join('')}
                </div>
                <div class="drawer-assist">
                    ${esc(t.drawerAssist)}
                </div>
            </div>
        `;

        // ── Event listeners ──
        const toggle = this.shadowRoot.querySelector('.mobile-toggle');
        const close = this.shadowRoot.querySelector('.close-drawer');
        const overlay = this.shadowRoot.querySelector('.overlay');
        const drawer = this.shadowRoot.querySelector('.mobile-drawer');
        const langWrapper = this.shadowRoot.querySelector('.lang-wrapper');
        const langSelector = this.shadowRoot.querySelector('.lang-selector');

        const openMenu = () => { drawer.classList.add('open'); overlay.classList.add('open'); };
        const closeMenu = () => { drawer.classList.remove('open'); overlay.classList.remove('open'); };

        if (toggle) toggle.addEventListener('click', openMenu);
        if (close) close.addEventListener('click', closeMenu);
        if (overlay) overlay.addEventListener('click', closeMenu);

        const toggleLangMenu = (e) => {
            if (e) e.stopPropagation();
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
