(function () {
    'use strict';

const FOOTER_I18N = {
    it: {
        logoAlt: 'Aml Store',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italia',
        supportHours: 'Lun–Ven · 09:00–19:00',
        supportLanguage: 'Assistenza in italiano',
        headingProducts: 'Prodotti',
        headingSupport: 'Supporto',
        headingLegal: 'Informazioni legali',
        headingContact: 'Contattaci',
        prodOs: 'Sistemi Operativi',
        prodOffice: 'Office',
        prodAntivirus: 'Antivirus',
        prodBusiness: 'Software Aziendali',
        prodDeals: 'Offerte Speciali',
        supportMyAccount: 'Il mio account',
        supportConsultation: 'Consulenza software',
        consultationSlug: 'consulenza',
        supportContacts: 'Contatti',
        supportReturns: 'Resi e Rimborsi',
        supportTerms: 'Termini e Condizioni',
        supportPrivacy: 'Privacy Policy',
        supportCookies: 'Cookie policy',
        cookieManage: 'Gestisci preferenze cookie',
        assistanceLabel: 'Telefono',
        whatsappLabel: 'WhatsApp',
        emailSub: 'Email',
        copyright: 'Aml Store. Tutti i diritti riservati.',
        vatLabel: 'P.IVA 11461870963',
        paymentSecure: 'Pagamenti sicuri',
        themeLabel: 'Aspetto',
        themeAria: 'Tema della pagina: chiaro o scuro (barra in alto e piè di pagina invariati)',
        paymentLogosAria:
            'Metodi di pagamento disponibili al checkout (carta, PayPal, Apple Pay, Google Pay), elaborati tramite Stripe',
    },
    en: {
        logoAlt: 'Aml Store',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italia',
        supportHours: 'Mon–Fri · 09:00–19:00 (Italy time)',
        supportLanguage: 'Support in English',
        headingProducts: 'Products',
        headingSupport: 'Support',
        headingLegal: 'Legal information',
        headingContact: 'Contact us',
        prodOs: 'Operating systems',
        prodOffice: 'Office',
        prodAntivirus: 'Antivirus',
        prodBusiness: 'Business software',
        prodDeals: 'Special offers',
        supportMyAccount: 'My account',
        supportConsultation: 'Software consultation',
        consultationSlug: 'consultation',
        supportContacts: 'Contact',
        supportReturns: 'Returns & refunds',
        supportTerms: 'Terms & conditions',
        supportPrivacy: 'Privacy policy',
        supportCookies: 'Cookie policy',
        cookieManage: 'Manage cookie preferences',
        assistanceLabel: 'Phone',
        whatsappLabel: 'WhatsApp',
        emailSub: 'Email',
        copyright: 'Aml Store. All rights reserved.',
        vatLabel: 'VAT 11461870963',
        paymentSecure: 'Secure payments',
        themeLabel: 'Appearance',
        themeAria: 'Page theme: light or dark (header and footer unchanged)',
        paymentLogosAria:
            'Payment methods available at checkout (card, PayPal, Apple Pay, Google Pay), processed with Stripe',
    },
    fr: {
        logoAlt: 'Aml Store',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italia',
        supportHours: 'Lun–Ven · 09:00–19:00 (heure italienne)',
        supportLanguage: 'Assistance en anglais',
        headingProducts: 'Produits',
        headingSupport: 'Assistance',
        headingLegal: 'Informations légales',
        headingContact: 'Contact',
        prodOs: "Systèmes d'exploitation",
        prodOffice: 'Office',
        prodAntivirus: 'Antivirus',
        prodBusiness: 'Logiciels professionnels',
        prodDeals: 'Offres spéciales',
        supportMyAccount: 'Mon compte',
        supportConsultation: 'Conseil logiciel',
        consultationSlug: 'consultation',
        supportContacts: 'Contact',
        supportReturns: 'Retours et remboursements',
        supportTerms: 'Conditions générales',
        supportPrivacy: 'Politique de confidentialité',
        supportCookies: 'Politique cookies',
        cookieManage: 'Gérer les préférences cookies',
        assistanceLabel: 'Téléphone',
        whatsappLabel: 'WhatsApp',
        emailSub: 'E-mail',
        copyright: 'Aml Store. Tous droits réservés.',
        vatLabel: 'TVA 11461870963',
        paymentSecure: 'Paiements sécurisés',
        themeLabel: 'Apparence',
        themeAria: "Thème de la page : clair ou sombre (en-tête et pied de page inchangés)",
        paymentLogosAria:
            'Moyens de paiement au checkout (carte, PayPal, Apple Pay, Google Pay), traités via Stripe',
    },
    de: {
        logoAlt: 'Aml Store',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italia',
        supportHours: 'Mo–Fr · 09:00–19:00 Uhr (italienische Zeit)',
        supportLanguage: 'Support auf Englisch',
        headingProducts: 'Produkte',
        headingSupport: 'Support',
        headingLegal: 'Rechtliche Informationen',
        headingContact: 'Kontakt',
        prodOs: 'Betriebssysteme',
        prodOffice: 'Office',
        prodAntivirus: 'Antivirus',
        prodBusiness: 'Business-Software',
        prodDeals: 'Sonderangebote',
        supportMyAccount: 'Mein Konto',
        supportConsultation: 'Softwareberatung',
        consultationSlug: 'beratung',
        supportContacts: 'Kontakt',
        supportReturns: 'Rückgabe & Erstattung',
        supportTerms: 'Allgemeine Geschäftsbedingungen',
        supportPrivacy: 'Datenschutz',
        supportCookies: 'Cookie-Richtlinie',
        cookieManage: 'Cookie-Einstellungen',
        assistanceLabel: 'Telefon',
        whatsappLabel: 'WhatsApp',
        emailSub: 'E-Mail',
        copyright: 'Aml Store. Alle Rechte vorbehalten.',
        vatLabel: 'USt-IdNr. 11461870963',
        paymentSecure: 'Sichere Zahlungen',
        themeLabel: 'Erscheinungsbild',
        themeAria: 'Seitenthema: hell oder dunkel (Kopf- und Fußzeile unverändert)',
        paymentLogosAria:
            'Zahlungsarten im Checkout (Karte, PayPal, Apple Pay, Google Pay), Abwicklung über Stripe',
    },
    es: {
        logoAlt: 'Aml Store',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italia',
        supportHours: 'Lun–Vie · 09:00–19:00 (hora de Italia)',
        supportLanguage: 'Asistencia en inglés',
        headingProducts: 'Productos',
        headingSupport: 'Soporte',
        headingLegal: 'Información legal',
        headingContact: 'Contacto',
        prodOs: 'Sistemas operativos',
        prodOffice: 'Office',
        prodAntivirus: 'Antivirus',
        prodBusiness: 'Software empresarial',
        prodDeals: 'Ofertas especiales',
        supportMyAccount: 'Mi cuenta',
        supportConsultation: 'Asesoramiento de software',
        consultationSlug: 'consultoria',
        supportContacts: 'Contacto',
        supportReturns: 'Devoluciones y reembolsos',
        supportTerms: 'Términos y condiciones',
        supportPrivacy: 'Política de privacidad',
        supportCookies: 'Política de cookies',
        cookieManage: 'Gestionar cookies',
        assistanceLabel: 'Teléfono',
        whatsappLabel: 'WhatsApp',
        emailSub: 'Email',
        copyright: 'Aml Store. Todos los derechos reservados.',
        vatLabel: 'NIF 11461870963',
        paymentSecure: 'Pagos seguros',
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
        const consultationHref = S.localePageUrl(parsed.pathPrefix, activeLang.code, t.consultationSlug);
        const esc = S.escapeHtmlAttr;
        const staticRoot = S.staticRootFromScriptPath('/components/footer.js');
        const logoSrc = `${staticRoot}/logo/logo-header-400.webp`;
        // Accento derivato dal blu del logo AML Store (design system istituzionale,
        // css/page.css --aml-brand), non più il blu SaaS generico di un tempo.
        const accentColor = 'var(--aml-brand, #3267AC)';

        try {
            this.shadowRoot.innerHTML = `

            <style>
                :host {
                    display: block;
                    font-family: 'Montserrat', sans-serif;
                    /* Alias verso i token globali del design system (css/page.css). */
                    --bg-base: var(--aml-paper, #F4F6F8);
                    --bg-surface: var(--aml-surface, #FFFFFF);
                    --border-color: var(--aml-line, #DCE3EA);
                    --text-primary: var(--aml-ink, #152033);
                    --text-secondary: var(--aml-ink-2, #5F6B7A);
                    --text-muted: var(--aml-ink-2, #5F6B7A);
                    --accent: ${accentColor};
                    --accent-hover: #26507f;
                    --glow-color: color-mix(in srgb, ${accentColor} 10%, transparent);

                    position: relative;
                    z-index: 10;
                    background-color: var(--bg-base);
                    color: var(--text-primary);
                    overflow: hidden;
                    /* Sottile linea di separazione in alto */
                    box-shadow: inset 0 1px 0 0 rgba(16, 24, 40, 0.06);
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
                    flex: 0 1 140px;
                    max-width: 160px;
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

                /* GRUPPO NAVIGAZIONE (A Destra) */
                .nav-group {
                    flex: 1 1 900px;
                    display: flex;
                    flex-wrap: nowrap;
                    align-items: flex-start;
                    gap: 3rem clamp(1rem, 2vw, 2rem);
                }

                .nav-col {
                    flex: 1 1 145px;
                    min-width: 0;
                    display: flex;
                    flex-direction: column;
                }
                .nav-col:nth-child(3) { flex-grow: 1.4; flex-basis: 210px; }

                /* CARD CONTATTI */
                .contact-card {
                    flex: 0 0 280px;
                    background: var(--bg-surface);
                    border: 1px solid var(--border-color);
                    border-radius: 8px;
                    padding: 1.75rem;
                    box-shadow: var(--aml-shadow-sm, 0 1px 2px rgba(16, 24, 40, 0.04));
                    display: flex;
                    flex-direction: column;
                    gap: 1.5rem;
                    backdrop-filter: none;
                    -webkit-backdrop-filter: none;
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

                /* Stili condivisi <a> e <button> */
                .link-list a,
                .link-list button.link-as-a {
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

                /* Effetto hover: freccina animata */
                .link-list a::before,
                .link-list button.link-as-a::before {
                    content: '→';
                    position: absolute;
                    left: -1.2rem;
                    opacity: 0;
                    color: var(--accent-hover);
                    transform: translateX(-5px);
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                }

                .link-list a:hover,
                .link-list a:focus-visible,
                .link-list button.link-as-a:hover,
                .link-list button.link-as-a:focus-visible {
                    color: var(--text-primary);
                    transform: translateX(1.2rem);
                }

                .link-list a:hover::before,
                .link-list a:focus-visible::before,
                .link-list button.link-as-a:hover::before,
                .link-list button.link-as-a:focus-visible::before {
                    opacity: 1;
                    transform: translateX(0);
                }

                /* Reset specifico <button> */
                .link-list button.link-as-a {
                    appearance: none;
                    background: none;
                    border: none;
                    margin: 0;
                    font: inherit;
                    cursor: pointer;
                    text-align: left;
                }

                .link-list button.link-as-a:focus-visible {
                    outline: 2px solid var(--accent);
                    outline-offset: 2px;
                }

                @media (prefers-reduced-motion: reduce) {
                    .link-list a,
                    .link-list button.link-as-a,
                    .link-list a::before,
                    .link-list button.link-as-a::before {
                        transition: none;
                    }
                }

                /* ITEMS CONTATTO */
                .contact-items-wrapper {
                    display: flex;
                    flex-direction: column;
                    gap: 1.25rem;
                }

                .support-availability {
                    padding-top: 1rem;
                    border-top: 1px solid var(--border-color);
                    color: var(--text-secondary);
                    font-size: 0.8rem;
                    line-height: 1.6;
                }
                .support-availability strong {
                    display: block;
                    color: var(--text-primary);
                    font-weight: 700;
                }

                .contact-item {
                    display: flex; align-items: center; gap: 1rem;
                    text-decoration: none; /* In caso l'intero item diventi cliccabile */
                }
                
                .contact-icon {
                    display: flex; align-items: center; justify-content: center;
                    width: 42px; height: 42px; border-radius: 8px;
                    background: color-mix(in srgb, var(--accent) 8%, transparent);
                    color: var(--accent);
                    flex-shrink: 0;
                    transition: background 0.3s ease, transform 0.3s ease;
                }
                .contact-item:hover .contact-icon {
                    background: color-mix(in srgb, var(--accent) 14%, transparent);
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
                    background: linear-gradient(90deg, transparent, rgba(16, 24, 40, 0.12), transparent);
                }

                .bottom-content {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 2rem 0;
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

                /* PAGAMENTI — pill glassmorphism */
                .payments {
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                    flex-wrap: wrap;
                    /* Deve poter rimpicciolirsi: con flex-shrink:0 la pill restava alla
                       sua larghezza max-content (~610px) e usciva dal container sugli
                       schermi stretti invece di mandare i loghi a capo. */
                    flex-shrink: 1;
                    min-width: 0;
                    max-width: 100%;
                    background: var(--bg-surface);
                    border: 1px solid var(--border-color);
                    border-radius: 6px;
                    padding: 0.45rem 0.875rem;
                }

                /* Etichetta sicurezza: lock + testo */
                .payment-secure {
                    display: flex;
                    align-items: center;
                    gap: 0.3rem;
                    color: var(--text-muted);
                    font-size: 0.68rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.09em;
                    white-space: nowrap;
                    padding-inline-end: 0.75rem;
                    border-inline-end: 1px solid var(--border-color);
                    flex-shrink: 0;
                }
                .payment-secure svg {
                    width: 11px;
                    height: 11px;
                    flex-shrink: 0;
                    opacity: 0.7;
                }

                /* Divisore verticale tra toggle e payments */
                .bottom-divider {
                    width: 1px;
                    height: 1.25rem;
                    background: rgba(255, 255, 255, 0.1);
                    flex-shrink: 0;
                    align-self: center;
                }

                .copyright-legal {
                    display: block;
                    margin-top: 0.35rem;
                    color: var(--text-muted);
                    font-size: 0.78rem;
                    line-height: 1.55;
                }
                .payment-logo {
                    display: block;
                    transition: filter 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275),
                                transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                    filter: grayscale(100%) opacity(0.4);
                    cursor: pointer;
                }
                .payment-logo:hover {
                    filter: grayscale(0%) opacity(1);
                    transform: translateY(-3px) scale(1.05);
                }
                @media (prefers-reduced-motion: reduce) {
                    .payment-logo { transition: none; }
                    .payment-logo:hover { transform: none; }
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
                
                /* BREAKPOINT 1 (Laptop/Tablet Landscape < 1240px) */
                @media (max-width: 1240px) {
                    .brand-col {
                        flex: 1 1 100%;
                        max-width: 100%;
                        margin-bottom: 1rem;
                    }
                    .nav-group {
                        flex: 1 1 100%;
                        display: grid;
                        grid-template-columns: repeat(3, minmax(0, 1fr));
                    }
                    .contact-card {
                        grid-column: 1 / -1;
                        width: 100%;
                    }
                    .footer-main { padding-top: 4rem; }
                }

                /* BREAKPOINT 2 (Tablet Portrait < 960px) */
                @media (max-width: 960px) {
                    .nav-group { display: flex; flex-direction: column; gap: 2.5rem; }
                    .nav-col,
                    .nav-col:nth-child(3),
                    .contact-card {
                        flex: 1 1 auto;
                        width: 100%;
                    }
                    .contact-card {
                        border-radius: 8px;
                        padding: 1.5rem;
                    }
                }

                /* BREAKPOINT 3 (Smartphone < 640px) */
                @media (max-width: 640px) {
                    .bottom-divider { display: none; }
                    .container { padding: 0 clamp(1.25rem, 5vw, 2rem); }
                    .footer-main { gap: 2.5rem; padding-top: 3rem; padding-bottom: 2rem; }
                    
                    /* Touch: padding generoso + separatore per ogni voce */
                    .link-list a,
                    .link-list button.link-as-a {
                        padding: 0.75rem 0;
                        width: 100%;
                        font-size: 1rem;
                        border-bottom: 1px solid var(--border-color);
                    }
                    /* Rimuove separatore sull'ultima voce di ogni lista */
                    .link-list li:last-child a,
                    .link-list li:last-child button.link-as-a { border-bottom: none; }
                    /* Nasconde la freccina e annulla lo spostamento laterale */
                    .link-list a::before,
                    .link-list button.link-as-a::before { display: none; }
                    .link-list a:hover, .link-list a:focus-visible,
                    .link-list button.link-as-a:hover,
                    .link-list button.link-as-a:focus-visible { transform: none; color: var(--text-primary); }
                    
                    .bottom-content {
                        flex-direction: column-reverse;
                        justify-content: center;
                        text-align: center;
                        padding: 2.5rem 0;
                    }
                    /* Griglia 3+3: il wrap del flex lasciava 5 loghi su una riga e 1
                       sull'altra, che sembra un errore di impaginazione. */
                    .payments {
                        display: grid;
                        grid-template-columns: repeat(3, minmax(0, 1fr));
                        justify-items: center;
                        align-items: center;
                        gap: 0.85rem 0.5rem;
                        padding: 0.7rem 0.75rem;
                    }
                    /* Etichetta come intestazione della pill: il divisore verticale non
                       ha senso quando i loghi stanno su più righe. */
                    .payment-secure {
                        grid-column: 1 / -1;
                        justify-content: center;
                        padding-inline-end: 0;
                        padding-bottom: 0.6rem;
                        border-inline-end: none;
                        border-bottom: 1px solid var(--border-color);
                        width: 100%;
                    }
                    .payment-logo img {
                        height: 20px;
                        max-width: 100%;
                    }
                    .bottom-right-cluster {
                        justify-content: center;
                        width: 100%;
                        margin-inline-end: 0;
                    }
                }

                .footer-bg-glow { display: none; }
                .footer-logo img { filter: none; }
            </style>

            <div class="footer-bg-glow"></div>
            
            <div class="container footer-main">
                <!-- Brand (Colonna 1) -->
                <div class="brand-col">
                    <a href="${esc(homeHref)}" class="footer-logo">
                        <img src="${esc(logoSrc)}" width="200" height="48" alt="${esc(t.logoAlt)}">
                    </a>
                </div>

                <!-- Gruppo Navigazione (Destra) -->
                <div class="nav-group">
                    <!-- Prodotti -->
                    <div class="nav-col">
                        <h3 class="col-title">${esc(t.headingProducts)}</h3>
                        <ul class="link-list">
                            <li><a href="${esc(staticRoot)}/${activeLang.code}/sistemi-operativi">${esc(t.prodOs)}</a></li>
                            <li><a href="${esc(staticRoot)}/${activeLang.code}/suite-office">${esc(t.prodOffice)}</a></li>
                            <li><a href="${esc(staticRoot)}/${activeLang.code}/antivirus">${esc(t.prodAntivirus)}</a></li>
                            <li><a href="${esc(staticRoot)}/${activeLang.code}/windows-server">${esc(t.prodBusiness)}</a></li>
                            <li><a href="${esc(staticRoot)}/${activeLang.code}/pacchetti">${esc(t.prodDeals)}</a></li>
                        </ul>
                    </div>

                    <!-- Supporto -->
                    <div class="nav-col">
                        <h3 class="col-title">${esc(t.headingSupport)}</h3>
                        <ul class="link-list">
                            <li><a href="${esc(consultationHref)}">${esc(t.supportConsultation)}</a></li>
                            <li><a href="${esc(staticRoot)}/${activeLang.code}/contacts">${esc(t.supportContacts)}</a></li>
                            <li><a href="${esc(staticRoot)}/${activeLang.code}/returns-and-refunds">${esc(t.supportReturns)}</a></li>
                        </ul>
                    </div>

                    <!-- Informazioni legali -->
                    <div class="nav-col">
                        <h3 class="col-title">${esc(t.headingLegal)}</h3>
                        <ul class="link-list">
                            <li><a href="${esc(staticRoot)}/${activeLang.code}/terms-and-conditions">${esc(t.supportTerms)}</a></li>
                            <li><a href="${esc(staticRoot)}/${activeLang.code}/privacy-policy">${esc(t.supportPrivacy)}</a></li>
                            <li><a href="${esc(staticRoot)}/${activeLang.code}/cookie-policy">${esc(t.supportCookies)}</a></li>
                            <li><button type="button" class="link-as-a" data-aml-cookie-settings>${esc(t.cookieManage)}</button></li>
                        </ul>
                    </div>

                    <!-- Contatti (Card Design) -->
                    <div class="contact-card">
                        <h3 class="col-title">${esc(t.headingContact)}</h3>
                        <div class="contact-items-wrapper">
                            <a href="tel:+393925580413" class="contact-item">
                                <div class="contact-icon" aria-hidden="true">
                                    <svg viewBox="0 0 24 24"><path d="M12 1a9 9 0 0 0-9 9v7c0 1.66 1.34 3 3 3h3v-8H5v-2c0-3.87 3.13-7 7-7s7 3.13 7 7v2h-4v8h3c1.66 0 3-1.34 3-3v-7a9 9 0 0 0-9-9z"/></svg>
                                </div>
                                <div class="contact-text">
                                    <span class="contact-label">${esc(t.assistanceLabel)}</span>
                                    <span class="contact-value">+39 392 558 0413</span>
                                </div>
                            </a>
                            <a href="https://wa.me/393925580413" class="contact-item" target="_blank" rel="noopener noreferrer">
                                <div class="contact-icon" aria-hidden="true">
                                    <svg viewBox="0 0 24 24"><path d="M12 2a9.6 9.6 0 0 0-8.28 14.46L2.4 21.6l5.26-1.38A9.6 9.6 0 1 0 12 2Zm0 17.2a7.55 7.55 0 0 1-3.85-1.06l-.28-.16-3.12.82.83-3.04-.18-.3A7.6 7.6 0 1 1 12 19.2Zm4.17-5.7c-.23-.12-1.35-.67-1.56-.74-.21-.08-.36-.12-.52.11-.15.23-.59.74-.73.89-.13.15-.27.17-.5.06-1.34-.67-2.22-1.2-3.1-2.72-.23-.4.23-.37.67-1.23.08-.15.04-.29-.02-.4-.05-.12-.51-1.24-.7-1.69-.19-.45-.38-.39-.52-.4h-.44c-.15 0-.4.06-.61.29-.21.23-.8.78-.8 1.9s.82 2.2.93 2.35c.12.15 1.61 2.46 3.9 3.45 1.45.63 2.02.68 2.74.58.44-.07 1.35-.55 1.54-1.08.19-.53.19-.99.13-1.08-.05-.1-.2-.15-.43-.27Z"/></svg>
                                </div>
                                <div class="contact-text">
                                    <span class="contact-label">${esc(t.whatsappLabel)}</span>
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
                        <p class="support-availability">
                            <strong>${esc(t.supportHours)}</strong>
                            ${esc(t.supportLanguage)}
                        </p>
                    </div>
                </div>
            </div>

            <!-- Footer Bottom -->
            <div class="footer-bottom">
                <div class="container">
                <div class="bottom-content">
                    <p class="copyright">
                        &copy; ${new Date().getFullYear()} ${esc(t.copyright)}
                        <span class="copyright-legal">${esc(t.legalName)} &nbsp;·&nbsp; ${esc(t.legalAddress)} &nbsp;·&nbsp; ${esc(t.vatLabel)}</span>
                    </p>
                    <div class="bottom-right-cluster">
                        <div class="payments" role="group" aria-label="${esc(t.paymentLogosAria)}">
                            <span class="payment-secure" aria-hidden="true">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                                ${esc(t.paymentSecure)}
                            </span>
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
            </div>
        `;
            this.shadowRoot.querySelector('[data-aml-cookie-settings]')?.addEventListener('click', (e) => {
                e.preventDefault();
                window.dispatchEvent(new CustomEvent('aml-open-cookie-settings'));
            });

            this.__footerUiInit = true;
        } catch (err) {
            console.error('ecommerce-footer: render failed', err);
        }
    }

}

if (!customElements.get('ecommerce-footer')) {
    customElements.define('ecommerce-footer', EcommerceFooter);
}
})();
