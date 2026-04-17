(function () {
    'use strict';

const FOOTER_I18N = {
    it: {
        logoAlt: 'Aml Store',
        brandDesc:
            "Il tuo partner affidabile per l'acquisto di licenze software originali. Sistemi Operativi, Office e Antivirus al miglior prezzo garantito.",
        headingProducts: 'Prodotti',
        headingSupport: 'Supporto',
        headingContact: 'Contattaci',
        prodOs: 'Sistemi Operativi',
        prodOffice: 'Office',
        prodAntivirus: 'Antivirus',
        prodBusiness: 'Software Aziendali',
        prodDeals: 'Offerte Speciali',
        supportMyAccount: 'Il mio account',
        supportInstallGuide: "Guida all'installazione",
        supportReturns: 'Resi e Rimborsi',
        supportTerms: 'Termini e Condizioni',
        supportPrivacy: 'Privacy Policy',
        supportCookies: 'Cookie policy',
        cookieManage: 'Gestisci preferenze cookie',
        assistanceLabel: 'Assistenza',
        emailSub: 'Rispondiamo h24',
        copyright: 'Aml Store. Tutti i diritti riservati. P.IVA 11461870963.',
        themeLabel: 'Aspetto',
        themeAria: 'Tema della pagina: chiaro o scuro (barra in alto e piè di pagina invariati)',
        paymentLogosAria:
            'Metodi di pagamento disponibili al checkout (carta, PayPal, Apple Pay, Google Pay), elaborati tramite Stripe',
    },
    en: {
        logoAlt: 'Aml Store',
        brandDesc:
            'Your trusted partner for genuine software licenses. Operating systems, Office and antivirus at the best guaranteed price.',
        headingProducts: 'Products',
        headingSupport: 'Support',
        headingContact: 'Contact us',
        prodOs: 'Operating systems',
        prodOffice: 'Office',
        prodAntivirus: 'Antivirus',
        prodBusiness: 'Business software',
        prodDeals: 'Special offers',
        supportMyAccount: 'My account',
        supportInstallGuide: 'Installation guide',
        supportReturns: 'Returns & refunds',
        supportTerms: 'Terms & conditions',
        supportPrivacy: 'Privacy policy',
        supportCookies: 'Cookie policy',
        cookieManage: 'Manage cookie preferences',
        assistanceLabel: 'Support',
        emailSub: 'We respond 24/7',
        copyright: 'Aml Store. All rights reserved. VAT 11461870963.',
        themeLabel: 'Appearance',
        themeAria: 'Page theme: light or dark (header and footer unchanged)',
        paymentLogosAria:
            'Payment methods available at checkout (card, PayPal, Apple Pay, Google Pay), processed with Stripe',
    },
    fr: {
        logoAlt: 'Aml Store',
        brandDesc:
            "Votre partenaire de confiance pour des licences logicielles d'origine. Systèmes d'exploitation, Office et antivirus au meilleur prix garanti.",
        headingProducts: 'Produits',
        headingSupport: 'Assistance',
        headingContact: 'Contact',
        prodOs: "Systèmes d'exploitation",
        prodOffice: 'Office',
        prodAntivirus: 'Antivirus',
        prodBusiness: 'Logiciels professionnels',
        prodDeals: 'Offres spéciales',
        supportMyAccount: 'Mon compte',
        supportInstallGuide: "Guide d'installation",
        supportReturns: 'Retours et remboursements',
        supportTerms: 'Conditions générales',
        supportPrivacy: 'Politique de confidentialité',
        supportCookies: 'Politique cookies',
        cookieManage: 'Gérer les préférences cookies',
        assistanceLabel: 'Assistance',
        emailSub: 'Réponse 24h/24',
        copyright: 'Aml Store. Tous droits réservés. TVA 11461870963.',
        themeLabel: 'Apparence',
        themeAria: "Thème de la page : clair ou sombre (en-tête et pied de page inchangés)",
        paymentLogosAria:
            'Moyens de paiement au checkout (carte, PayPal, Apple Pay, Google Pay), traités via Stripe',
    },
    de: {
        logoAlt: 'Aml Store',
        brandDesc:
            'Ihr zuverlässiger Partner für originale Softwarelizenzen. Betriebssysteme, Office und Antivirus zum besten garantierten Preis.',
        headingProducts: 'Produkte',
        headingSupport: 'Support',
        headingContact: 'Kontakt',
        prodOs: 'Betriebssysteme',
        prodOffice: 'Office',
        prodAntivirus: 'Antivirus',
        prodBusiness: 'Business-Software',
        prodDeals: 'Sonderangebote',
        supportMyAccount: 'Mein Konto',
        supportInstallGuide: 'Installationsanleitung',
        supportReturns: 'Rückgabe & Erstattung',
        supportTerms: 'Allgemeine Geschäftsbedingungen',
        supportPrivacy: 'Datenschutz',
        supportCookies: 'Cookie-Richtlinie',
        cookieManage: 'Cookie-Einstellungen',
        assistanceLabel: 'Support',
        emailSub: 'Wir antworten rund um die Uhr',
        copyright: 'Aml Store. Alle Rechte vorbehalten. USt-IdNr. 11461870963.',
        themeLabel: 'Erscheinungsbild',
        themeAria: 'Seitenthema: hell oder dunkel (Kopf- und Fußzeile unverändert)',
        paymentLogosAria:
            'Zahlungsarten im Checkout (Karte, PayPal, Apple Pay, Google Pay), Abwicklung über Stripe',
    },
    es: {
        logoAlt: 'Aml Store',
        brandDesc:
            'Tu socio de confianza para licencias de software originales. Sistemas operativos, Office y antivirus al mejor precio garantizado.',
        headingProducts: 'Productos',
        headingSupport: 'Soporte',
        headingContact: 'Contacto',
        prodOs: 'Sistemas operativos',
        prodOffice: 'Office',
        prodAntivirus: 'Antivirus',
        prodBusiness: 'Software empresarial',
        prodDeals: 'Ofertas especiales',
        supportMyAccount: 'Mi cuenta',
        supportInstallGuide: 'Guía de instalación',
        supportReturns: 'Devoluciones y reembolsos',
        supportTerms: 'Términos y condiciones',
        supportPrivacy: 'Política de privacidad',
        supportCookies: 'Política de cookies',
        cookieManage: 'Gestionar cookies',
        assistanceLabel: 'Asistencia',
        emailSub: 'Respondemos 24/7',
        copyright: 'Aml Store. Todos los derechos reservados. NIF 11461870963.',
        themeLabel: 'Apariencia',
        themeAria: 'Tema de la página: claro u oscuro (cabecera y pie sin cambios)',
        paymentLogosAria:
            'Métodos de pago en el checkout (tarjeta, PayPal, Apple Pay, Google Pay), procesados con Stripe',
    },
};

class EcommerceFooter extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        if (this.__footerUiInit) return;

        this.setAttribute('translate', 'no');
        this.classList.add('notranslate');

        const S = window.AmlSite;
        if (!S) {
            console.error('ecommerce-footer: includere ../js/locale-path.js prima di questo script.');
            return;
        }
        const parsed = S.parseLocalePath(window.location.pathname);
        const activeLang = parsed.activeLang;
        const t = FOOTER_I18N[activeLang.code] || FOOTER_I18N.it;
        const homeHref = S.homeHref(parsed.pathPrefix, activeLang.code);
        const esc = S.escapeHtmlAttr;
        const staticRoot = S.staticRootFromScriptPath('/components/footer.js');
        const logoSrc = `${staticRoot}/logo/logo-header-400.webp`;
        const pageTheme =
            document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';

        try {
            this.shadowRoot.innerHTML = `

            <style>
                :host {
                    display: block;
                    font-family: 'Montserrat', sans-serif;
                    /* Colori base "Premium Dark" */
                    --bg-base: #050505;
                    --bg-surface: #111111;
                    --border-color: rgba(255, 255, 255, 0.08);
                    --text-primary: #ffffff;
                    --text-secondary: #a1a1aa; /* Zinco 400 */
                    --text-muted: #71717a; /* Zinco 500 */
                    --accent: #3b82f6;
                    --accent-hover: #ffffff;
                    --glow-color: rgba(59, 130, 246, 0.10);
                    
                    position: relative;
                    z-index: 10;
                    background-color: var(--bg-base);
                    color: var(--text-primary);
                    overflow: hidden;
                    /* Sottile linea di separazione sfumata in alto */
                    box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.05);
                }

                * { box-sizing: border-box; margin: 0; padding: 0; }

                /* Effetto Glow di sfondo */
                .footer-bg-glow {
                    position: absolute;
                    top: 0; left: 50%; transform: translateX(-50%);
                    width: 100%; height: 400px;
                    background: radial-gradient(ellipse at top, var(--glow-color) 0%, transparent 60%);
                    pointer-events: none; z-index: 0;
                }

                .container {
                    position: relative;
                    z-index: 1;
                    max-width: 1280px; /* Allineato perfettamente all'Header */
                    margin: 0 auto;
                    padding: 0 clamp(2rem, 5vw, 4rem); /* Safety padding su tutti i dispositivi */
                }

                /* --- ARCHITETTURA FLEX FLUIDA --- */
                .footer-main {
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: space-between;
                    /* FIX: Usiamo padding-top e padding-bottom separati, in modo 
                       da non sovrascrivere o uccidere il padding orizzontale di .container! */
                    padding-top: clamp(4rem, 6vw, 6rem);
                    padding-bottom: clamp(3rem, 5vw, 4rem);
                    gap: 4rem 2rem;
                }

                /* BRAND COL (A Sinistra) */
                .brand-col {
                    flex: 1 1 320px; /* Cresce e si restringe, base 320px */
                    max-width: 420px;
                }

                .footer-logo {
                    display: inline-block;
                    margin-bottom: 1.5rem;
                    border-radius: 6px;
                    transition: opacity 0.3s ease, transform 0.3s ease;
                }
                .footer-logo:hover { opacity: 0.9; transform: scale(1.02); }
                .footer-logo:focus-visible { outline: 2px solid var(--accent); outline-offset: 4px; }
                .footer-logo img {
                    height: 44px; width: auto; display: block;
                    filter: brightness(0) invert(1); 
                }

                .brand-desc {
                    color: var(--text-secondary);
                    font-size: 0.95rem;
                    line-height: 1.8;
                    font-weight: 500;
                }

                /* GRUPPO NAVIGAZIONE (A Destra) */
                .nav-group {
                    flex: 2 1 600px; /* Prende più spazio del brand */
                    display: flex;
                    flex-wrap: wrap;
                    gap: 3rem 2rem;
                }

                .nav-col {
                    flex: 1 1 140px; /* Colonne link base 140px */
                    display: flex;
                    flex-direction: column;
                }

                /* CARD CONTATTI (Glassmorfica) */
                .contact-card {
                    flex: 1 1 280px; /* Colonna contatti un po' più larga */
                    background: linear-gradient(145deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
                    border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 16px;
                    padding: 1.75rem;
                    box-shadow: 0 4px 24px -1px rgba(0,0,0,0.1);
                    display: flex;
                    flex-direction: column;
                    gap: 1.5rem;
                    backdrop-filter: blur(10px);
                    -webkit-backdrop-filter: blur(10px);
                }

                /* TITOLI COLONNE */
                h3.col-title {
                    font-size: 0.8rem;
                    font-weight: 700;
                    color: var(--text-primary);
                    text-transform: uppercase;
                    letter-spacing: 0.12em;
                    margin-bottom: 1.5rem;
                }

                .contact-card h3.col-title {
                    margin-bottom: 0; /* Gestone margini interna alla card */
                }

                /* LINK LISTE */
                .link-list {
                    list-style: none;
                    display: flex;
                    flex-direction: column;
                    gap: 0.5rem;
                }

                .link-list a {
                    color: var(--text-secondary);
                    text-decoration: none;
                    font-size: 0.95rem;
                    font-weight: 500;
                    display: inline-flex;
                    align-items: center;
                    padding: 0.35rem 0;
                    width: max-content;
                    position: relative;
                    transition: color 0.3s ease, transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                }

                /* Effetto Hover: Il testo diventa bianco e appare una freccina */
                .link-list a::before {
                    content: '→';
                    position: absolute;
                    left: -1.2rem;
                    opacity: 0;
                    color: var(--accent-hover);
                    transform: translateX(-5px);
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                }

                .link-list a:hover, .link-list a:focus-visible {
                    color: var(--text-primary);
                    transform: translateX(1.2rem);
                }
                
                .link-list a:hover::before, .link-list a:focus-visible::before {
                    opacity: 1;
                    transform: translateX(0);
                }

                .link-list button.link-as-a {
                    appearance: none;
                    background: none;
                    border: none;
                    margin: 0;
                    font: inherit;
                    color: var(--text-secondary);
                    font-size: 0.95rem;
                    font-weight: 500;
                    display: inline-flex;
                    align-items: center;
                    padding: 0.35rem 0;
                    width: max-content;
                    position: relative;
                    cursor: pointer;
                    text-align: left;
                    transition: color 0.3s ease, transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                }
                .link-list button.link-as-a::before {
                    content: '→';
                    position: absolute;
                    left: -1.2rem;
                    opacity: 0;
                    color: var(--accent-hover);
                    transform: translateX(-5px);
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                }
                .link-list button.link-as-a:hover,
                .link-list button.link-as-a:focus-visible {
                    color: var(--text-primary);
                    transform: translateX(1.2rem);
                }
                .link-list button.link-as-a:hover::before,
                .link-list button.link-as-a:focus-visible::before {
                    opacity: 1;
                    transform: translateX(0);
                }
                .link-list button.link-as-a:focus-visible {
                    outline: 2px solid var(--accent);
                    outline-offset: 2px;
                }

                /* ITEMS CONTATTO */
                .contact-items-wrapper {
                    display: flex;
                    flex-direction: column;
                    gap: 1.25rem;
                }

                .contact-item {
                    display: flex; align-items: center; gap: 1rem;
                    text-decoration: none; /* In caso l'intero item diventi cliccabile */
                }
                
                .contact-icon {
                    display: flex; align-items: center; justify-content: center;
                    width: 42px; height: 42px; border-radius: 12px;
                    background: rgba(255, 255, 255, 0.05);
                    color: var(--text-primary);
                    flex-shrink: 0;
                    transition: background 0.3s ease, transform 0.3s ease;
                }
                .contact-item:hover .contact-icon {
                    background: rgba(255, 255, 255, 0.1);
                    transform: scale(1.05);
                }
                .contact-icon svg { width: 20px; height: 20px; fill: currentColor; }

                .contact-text {
                    display: flex; flex-direction: column; gap: 0.1rem;
                    overflow: hidden;
                }
                .contact-label {
                    font-size: 0.75rem; font-weight: 600; color: var(--text-muted);
                    text-transform: uppercase; letter-spacing: 0.05em;
                }
                .contact-value {
                    font-size: 0.95rem;
                    font-weight: 600; color: var(--text-primary);
                    white-space: nowrap; text-overflow: ellipsis; overflow: hidden;
                    transition: color 0.3s ease;
                }
                .contact-item:hover .contact-value { color: var(--accent-hover); }

                /* --- BARRA INFERIORE --- */
                .footer-bottom {
                    /* Linea sfumata super premium al posto del border solido */
                    position: relative;
                    background-color: transparent;
                }
                .footer-bottom::before {
                    content: ''; position: absolute; top: 0; left: 10%; width: 80%; height: 1px;
                    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
                }

                .bottom-content {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 2rem clamp(2rem, 5vw, 4rem);
                    flex-wrap: wrap;
                    gap: clamp(1rem, 2.5vw, 1.75rem);
                }
                .copyright {
                    color: var(--text-muted);
                    font-size: 0.85rem;
                    font-weight: 500;
                    flex: 1 1 14rem;
                    min-width: min(100%, 12rem);
                    max-width: 100%;
                    line-height: 1.45;
                }

                /* Toggle sempre a sinistra dei loghi pagamento, con respiro costante */
                .bottom-right-cluster {
                    display: flex;
                    align-items: center;
                    justify-content: flex-end;
                    flex-wrap: wrap;
                    gap: clamp(1rem, 2.5vw, 2rem);
                    column-gap: clamp(1.25rem, 3vw, 2.25rem);
                    row-gap: 1rem;
                    flex: 0 1 auto;
                    min-width: 0;
                }

                .theme-toggle {
                    display: inline-flex;
                    align-items: center;
                    gap: 0.55rem;
                    flex-wrap: nowrap;
                    flex-shrink: 0;
                    margin-inline-end: auto;
                }
                .theme-toggle-label {
                    font-size: 0.75rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.08em;
                    color: var(--text-muted);
                    white-space: nowrap;
                }

                /* Pill + thumb: inset simmetrico, corsa = larghezza − thumb − 2 inset */
                .theme-glass-switch {
                    --theme-track-w: 52px;
                    --theme-track-h: 30px;
                    --theme-thumb: 24px;
                    --theme-inset: 3px;
                    --theme-travel: calc(var(--theme-track-w) - var(--theme-thumb) - 2 * var(--theme-inset));
                    --theme-ease: cubic-bezier(0.175, 0.885, 0.32, 1.275);
                    margin: 0;
                    padding: 0.5rem 0.55rem;
                    border: none;
                    background: transparent;
                    cursor: pointer;
                    font-family: inherit;
                    line-height: 0;
                    border-radius: 999px;
                    -webkit-tap-highlight-color: transparent;
                    flex-shrink: 0;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    min-width: 2.75rem;
                    min-height: 2.75rem;
                }
                .theme-glass-switch:focus-visible {
                    outline: 2px solid var(--accent);
                    outline-offset: 3px;
                    border-radius: 999px;
                }
                .theme-glass-track {
                    position: relative;
                    display: block;
                    width: var(--theme-track-w);
                    height: var(--theme-track-h);
                    box-sizing: border-box;
                    border-radius: calc(var(--theme-track-h) / 2);
                    background: rgba(0, 0, 0, 0.5);
                    backdrop-filter: blur(12px);
                    -webkit-backdrop-filter: blur(12px);
                    border: 1px solid rgba(255, 255, 255, 0.12);
                    box-shadow:
                        inset 0 1px 0 rgba(255, 255, 255, 0.07),
                        inset 0 -1px 0 rgba(0, 0, 0, 0.35),
                        inset 0 2px 6px rgba(0, 0, 0, 0.4);
                    overflow: hidden;
                }
                .theme-glass-thumb {
                    position: absolute;
                    left: var(--theme-inset);
                    top: 50%;
                    width: var(--theme-thumb);
                    height: var(--theme-thumb);
                    border-radius: 50%;
                    box-sizing: border-box;
                    background: linear-gradient(160deg, rgba(255, 255, 255, 0.38) 0%, rgba(255, 255, 255, 0.1) 48%, rgba(255, 255, 255, 0.06) 100%);
                    backdrop-filter: blur(10px);
                    -webkit-backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.48);
                    box-shadow:
                        0 2px 8px rgba(0, 0, 0, 0.45),
                        0 1px 0 rgba(255, 255, 255, 0.55) inset;
                    display: grid;
                    place-items: center;
                    transform: translateY(-50%) translateX(0);
                    transition:
                        transform 0.45s var(--theme-ease),
                        box-shadow 0.35s ease,
                        border-color 0.35s ease;
                    z-index: 1;
                }
                .theme-glass-switch.theme-is-dark .theme-glass-thumb {
                    transform: translateY(-50%) translateX(var(--theme-travel));
                }
                .theme-glass-ico {
                    position: absolute;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #fff;
                    transition:
                        opacity 0.38s var(--theme-ease),
                        transform 0.38s var(--theme-ease);
                }
                .theme-glass-ico svg {
                    width: 14px;
                    height: 14px;
                    display: block;
                }
                .theme-glass-switch.theme-is-dark .ico-moon {
                    opacity: 1;
                    transform: scale(1) rotate(0deg);
                }
                .theme-glass-switch.theme-is-dark .ico-sun {
                    opacity: 0;
                    transform: scale(0.5) rotate(45deg);
                }
                .theme-glass-switch.theme-is-light .ico-moon {
                    opacity: 0;
                    transform: scale(0.5) rotate(-40deg);
                }
                .theme-glass-switch.theme-is-light .ico-sun {
                    opacity: 1;
                    transform: scale(1) rotate(0deg);
                }
                @media (prefers-reduced-motion: reduce) {
                    .theme-glass-thumb {
                        transition-duration: 0.12s;
                    }
                    .theme-glass-ico {
                        transition-duration: 0.12s;
                    }
                }

                /* PAGAMENTI (sempre dopo il toggle, senza restringersi a zero) */
                .payments {
                    display: flex;
                    align-items: center;
                    gap: 1.25rem;
                    flex-wrap: wrap;
                    flex-shrink: 0;
                }
                .payment-logo {
                    display: block;
                    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                    filter: grayscale(100%) opacity(0.4);
                    cursor: default;
                }
                .payment-logo:hover {
                    filter: grayscale(0%) opacity(1);
                    transform: translateY(-3px) scale(1.05);
                }
                .payment-logo img {
                    height: 22px;
                    width: auto;
                    max-width: 72px;
                    object-fit: contain;
                    display: block;
                    border-radius: 4px;
                }

                /* --- STRATEGIA RESPONSIVE --- */
                
                /* BREAKPOINT 1 (Laptop/Tablet Landscape < 1024px) */
                @media (max-width: 1024px) {
                    .brand-col {
                        flex: 1 1 100%;
                        max-width: 100%;
                        margin-bottom: 1rem;
                    }
                    .brand-desc { max-width: 600px; }
                    .footer-main { padding-top: 4rem; }
                }

                /* BREAKPOINT 2 (Tablet Portrait < 768px) */
                @media (max-width: 768px) {
                    .nav-group { flex-direction: column; gap: 2.5rem; }
                    .contact-card {
                        border-radius: 12px;
                        padding: 1.5rem;
                    }
                }

                /* BREAKPOINT 3 (Smartphone < 640px) */
                @media (max-width: 640px) {
                    .container { padding: 0 clamp(1.25rem, 5vw, 2rem); }
                    .footer-main { gap: 2.5rem; padding-top: 3rem; padding-bottom: 2rem; }
                    
                    .link-list a {
                        padding: 0.75rem 0; /* Padding Touch Enorme */
                        width: 100%;
                        font-size: 1rem;
                        border-bottom: 1px solid rgba(255,255,255,0.05);
                    }
                    .link-list a:last-child { border-bottom: none; }
                    .link-list a::before { display: none; }
                    .link-list a:hover, .link-list a:focus-visible { transform: none; color: var(--text-primary); }
                    .link-list button.link-as-a {
                        width: 100%;
                        padding: 0.75rem 0;
                        font-size: 1rem;
                        border-bottom: 1px solid rgba(255,255,255,0.05);
                    }
                    .link-list button.link-as-a::before { display: none; }
                    .link-list button.link-as-a:hover,
                    .link-list button.link-as-a:focus-visible { transform: none; }
                    
                    .bottom-content {
                        flex-direction: column-reverse;
                        justify-content: center;
                        text-align: center;
                        padding: 2.5rem clamp(1.25rem, 5vw, 2rem);
                    }
                    .payments { justify-content: center; }
                    .bottom-right-cluster {
                        justify-content: center;
                        width: 100%;
                        margin-inline-end: 0;
                    }
                    .theme-toggle {
                        margin-inline-end: 0;
                        flex-wrap: wrap;
                        justify-content: center;
                    }
                }
            </style>

            <div class="footer-bg-glow"></div>
            
            <div class="container footer-main">
                <!-- Brand (Colonna 1) -->
                <div class="brand-col">
                    <a href="${esc(homeHref)}" class="footer-logo">
                        <img src="${esc(logoSrc)}" width="200" height="48" alt="${esc(t.logoAlt)}">
                    </a>
                    <p class="brand-desc">
                        ${esc(t.brandDesc)}
                    </p>
                </div>

                <!-- Gruppo Navigazione (Destra) -->
                <div class="nav-group">
                    <!-- Prodotti -->
                    <div class="nav-col">
                        <h3 class="col-title">${esc(t.headingProducts)}</h3>
                        <ul class="link-list">
                            <li><a href="#">${esc(t.prodOs)}</a></li>
                            <li><a href="#">${esc(t.prodOffice)}</a></li>
                            <li><a href="#">${esc(t.prodAntivirus)}</a></li>
                            <li><a href="#">${esc(t.prodBusiness)}</a></li>
                            <li><a href="#">${esc(t.prodDeals)}</a></li>
                        </ul>
                    </div>

                    <!-- Supporto -->
                    <div class="nav-col">
                        <h3 class="col-title">${esc(t.headingSupport)}</h3>
                        <ul class="link-list">
                            <li><a href="#">${esc(t.supportMyAccount)}</a></li>
                            <li><a href="#">${esc(t.supportInstallGuide)}</a></li>
                            <li><a href="#">${esc(t.supportReturns)}</a></li>
                            <li><a href="#">${esc(t.supportTerms)}</a></li>
                            <li><a href="#">${esc(t.supportPrivacy)}</a></li>
                            <li><a href="cookie-policy.html">${esc(t.supportCookies)}</a></li>
                            <li><button type="button" class="link-as-a" data-aml-cookie-settings>${esc(t.cookieManage)}</button></li>
                        </ul>
                    </div>

                    <!-- Contatti (Card Design) -->
                    <div class="contact-card">
                        <h3 class="col-title">${esc(t.headingContact)}</h3>
                        <div class="contact-items-wrapper">
                            <a href="tel:+390212345678" class="contact-item">
                                <div class="contact-icon" aria-hidden="true">
                                    <svg viewBox="0 0 24 24"><path d="M12 1a9 9 0 0 0-9 9v7c0 1.66 1.34 3 3 3h3v-8H5v-2c0-3.87 3.13-7 7-7s7 3.13 7 7v2h-4v8h3c1.66 0 3-1.34 3-3v-7a9 9 0 0 0-9-9z"/></svg>
                                </div>
                                <div class="contact-text">
                                    <span class="contact-label">${esc(t.assistanceLabel)}</span>
                                    <span class="contact-value">+39 392 558 0413</span>
                                </div>
                            </a>
                            <a href="mailto:Info@amlstore.it" class="contact-item">
                                <div class="contact-icon" aria-hidden="true">
                                    <svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
                                </div>
                                <div class="contact-text">
                                    <span class="contact-label">${esc(t.emailSub)}</span>
                                    <span class="contact-value">Info@amlstore.it</span>
                                </div>
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Footer Bottom -->
            <div class="footer-bottom">
                <div class="bottom-content">
                    <p class="copyright">
                        &copy; ${new Date().getFullYear()} ${esc(t.copyright)}
                    </p>
                    <div class="bottom-right-cluster">
                        <div class="theme-toggle">
                            <span class="theme-toggle-label">${esc(t.themeLabel)}</span>
                            <button type="button" class="theme-glass-switch${pageTheme === 'dark' ? ' theme-is-dark' : ' theme-is-light'}" role="switch" aria-checked="${pageTheme === 'dark' ? 'true' : 'false'}" aria-label="${esc(t.themeAria)}">
                                <span class="theme-glass-track">
                                    <span class="theme-glass-thumb">
                                        <span class="theme-glass-ico ico-moon" aria-hidden="true">
                                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M21 12.79A9 9 0 1 1 11.21 3a7 7 0 0 0 9.79 9.79z"/></svg>
                                        </span>
                                        <span class="theme-glass-ico ico-sun" aria-hidden="true">
                                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>
                                        </span>
                                    </span>
                                </span>
                            </button>
                        </div>
                        <div class="payments" role="group" aria-label="${esc(t.paymentLogosAria)}">
                            <span class="payment-logo" title="Visa"><img src="${esc(staticRoot)}/asset/payments_logo/img-aml-store_Visa_logo.svg" width="56" height="22" alt="" loading="lazy" decoding="async"></span>
                            <span class="payment-logo" title="Mastercard"><img src="${esc(staticRoot)}/asset/payments_logo/img-aml-store_Mastercard_logo.svg" width="40" height="22" alt="" loading="lazy" decoding="async"></span>
                            <span class="payment-logo" title="PayPal"><img src="${esc(staticRoot)}/asset/payments_logo/img-aml-store_PayPal-logo.svg" width="72" height="22" alt="" loading="lazy" decoding="async"></span>
                            <span class="payment-logo" title="Apple Pay"><img src="${esc(staticRoot)}/asset/payments_logo/img-aml-store_Apple_Pay_logo.svg" width="48" height="22" alt="" loading="lazy" decoding="async"></span>
                            <span class="payment-logo" title="Google Pay"><img src="${esc(staticRoot)}/asset/payments_logo/img-aml-store_Google_Pay_Logo.svg" width="52" height="22" alt="" loading="lazy" decoding="async"></span>
                            <span class="payment-logo" title="Stripe"><img src="${esc(staticRoot)}/asset/payments_logo/img-aml-store_Stripe_Logo.svg" width="56" height="22" alt="" loading="lazy" decoding="async"></span>
                        </div>
                    </div>
                </div>
            </div>
        `;
            const THEME_KEY = 'aml-theme';
            const docEl = document.documentElement;
            const storedThemeValue = () => {
                try {
                    return localStorage.getItem(THEME_KEY);
                } catch (_) {
                    return null;
                }
            };
            const hasUserThemeOverride = () => {
                const v = storedThemeValue();
                return v === 'light' || v === 'dark';
            };
            const syncGlassToggle = () => {
                const isDark = docEl.getAttribute('data-theme') !== 'light';
                const glassBtn = this.shadowRoot.querySelector('.theme-glass-switch');
                if (!glassBtn) return;
                glassBtn.classList.toggle('theme-is-dark', isDark);
                glassBtn.classList.toggle('theme-is-light', !isDark);
                glassBtn.setAttribute('aria-checked', isDark ? 'true' : 'false');
            };
            const applySystemThemeFromOs = () => {
                if (hasUserThemeOverride()) return;
                const dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
                docEl.setAttribute('data-theme', dark ? 'dark' : 'light');
                syncGlassToggle();
            };
            const glassBtn = this.shadowRoot.querySelector('.theme-glass-switch');
            if (glassBtn) {
                glassBtn.addEventListener('click', () => {
                    const next = docEl.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
                    docEl.setAttribute('data-theme', next);
                    try {
                        localStorage.setItem(THEME_KEY, next);
                    } catch (_) {}
                    syncGlassToggle();
                });
            }
            const onStorage = (e) => {
                if (e.key !== THEME_KEY || !e.newValue) return;
                if (e.newValue !== 'light' && e.newValue !== 'dark') return;
                docEl.setAttribute('data-theme', e.newValue);
                syncGlassToggle();
            };
            const mq =
                typeof window.matchMedia === 'function'
                    ? window.matchMedia('(prefers-color-scheme: dark)')
                    : null;
            const onOsTheme = () => applySystemThemeFromOs();
            window.addEventListener('storage', onStorage);
            if (mq && typeof mq.addEventListener === 'function') {
                mq.addEventListener('change', onOsTheme);
            } else if (mq && typeof mq.addListener === 'function') {
                mq.addListener(onOsTheme);
            }
            this.__footerThemeCleanup = () => {
                window.removeEventListener('storage', onStorage);
                if (mq && typeof mq.removeEventListener === 'function') {
                    mq.removeEventListener('change', onOsTheme);
                } else if (mq && typeof mq.removeListener === 'function') {
                    mq.removeListener(onOsTheme);
                }
            };
            syncGlassToggle();

            this.shadowRoot.querySelector('[data-aml-cookie-settings]')?.addEventListener('click', (e) => {
                e.preventDefault();
                window.dispatchEvent(new CustomEvent('aml-open-cookie-settings'));
            });

            this.__footerUiInit = true;
        } catch (err) {
            console.error('ecommerce-footer: render failed', err);
        }
    }

    disconnectedCallback() {
        if (typeof this.__footerThemeCleanup === 'function') {
            this.__footerThemeCleanup();
            this.__footerThemeCleanup = null;
        }
    }
}

if (!customElements.get('ecommerce-footer')) {
    customElements.define('ecommerce-footer', EcommerceFooter);
}
})();