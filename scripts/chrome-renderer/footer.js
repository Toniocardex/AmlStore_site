(function () {
    'use strict';

const FOOTER_I18N = {
    it: {
        logoAlt: 'Aml Store',
        brandDesc: 'Software originale, fatturazione italiana e supporto umano. Soluzioni per privati, professionisti e aziende.',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italia',
        supportHours: 'Lun–Sab · 08:00–19:00',
        supportLanguage: 'Assistenza in italiano',
        headingCatalog: 'Catalogo',
        headingCompany: 'Azienda',
        headingSupport: 'Supporto',
        footerNavAria: 'Navigazione nel piè di pagina',
        legalNavAria: 'Informazioni legali',
        prodOs: 'Windows',
        prodOffice: 'Office',
        prodM365: 'Microsoft 365',
        prodAntivirus: 'Antivirus',
        companyAbout: 'Chi siamo',
        aboutSlug: 'chi-siamo',
        companyConsultation: 'Consulenza software',
        consultationSlug: 'consulenza',
        companyBusiness: 'Soluzioni business',
        companyReviews: 'Recensioni',
        companyContacts: 'Contatti',
        supportHow: 'Come funziona',
        supportAssistance: 'Assistenza',
        supportReturns: 'Resi e rimborsi',
        supportTerms: 'Termini e condizioni',
        supportPrivacy: 'Privacy',
        supportCookies: 'Cookie',
        cookieManage: 'Gestisci preferenze cookie',
        phoneLabel: 'Telefono',
        emailLabel: 'Email',
        copyright: 'Aml Store. Tutti i diritti riservati.',
        vatLabel: 'P.IVA 11461870963',
        trademarkDisclaimer: 'I nomi di prodotto, i loghi e i marchi citati appartengono ai rispettivi proprietari e sono usati a scopo identificativo/illustrativo. Aml Store non è affiliata né sponsorizzata dai titolari dei marchi.',
        paymentsLabel: 'Metodi di pagamento accettati',
    },
    en: {
        logoAlt: 'Aml Store',
        brandDesc: 'Genuine software, Italian invoicing and human support. Solutions for individuals, professionals and businesses.',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italy',
        supportHours: 'Mon–Sat · 08:00–19:00 (Italy time)',
        supportLanguage: 'Support in English',
        headingCatalog: 'Catalog',
        headingCompany: 'Company',
        headingSupport: 'Support',
        footerNavAria: 'Footer navigation',
        legalNavAria: 'Legal information',
        prodOs: 'Windows',
        prodOffice: 'Office',
        prodM365: 'Microsoft 365',
        prodAntivirus: 'Antivirus',
        companyAbout: 'About us',
        aboutSlug: 'about-us',
        companyConsultation: 'Software consultation',
        consultationSlug: 'consultation',
        companyBusiness: 'Business solutions',
        companyReviews: 'Reviews',
        companyContacts: 'Contact',
        supportHow: 'How it works',
        supportAssistance: 'Customer support',
        supportReturns: 'Returns and refunds',
        supportTerms: 'Terms and conditions',
        supportPrivacy: 'Privacy',
        supportCookies: 'Cookies',
        cookieManage: 'Manage cookie preferences',
        phoneLabel: 'Phone',
        emailLabel: 'Email',
        copyright: 'Aml Store. All rights reserved.',
        vatLabel: 'VAT 11461870963',
        trademarkDisclaimer: 'Product names, logos and trademarks mentioned belong to their respective owners and are used for identification/illustrative purposes only. Aml Store is not affiliated with or sponsored by the trademark owners.',
        paymentsLabel: 'Accepted payment methods',
    },
    fr: {
        logoAlt: 'Aml Store',
        brandDesc: "Logiciels authentiques, facturation italienne et assistance humaine. Des solutions pour particuliers, professionnels et entreprises.",
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italie',
        supportHours: 'Lun–Sam · 08:00–19:00 (heure italienne)',
        supportLanguage: 'Assistance en anglais',
        headingCatalog: 'Catalogue',
        headingCompany: 'Entreprise',
        headingSupport: 'Assistance',
        footerNavAria: 'Navigation du pied de page',
        legalNavAria: 'Informations légales',
        prodOs: 'Windows',
        prodOffice: 'Office',
        prodM365: 'Microsoft 365',
        prodAntivirus: 'Antivirus',
        companyAbout: 'Qui sommes-nous',
        aboutSlug: 'qui-sommes-nous',
        companyConsultation: 'Conseil logiciel',
        consultationSlug: 'consultation',
        companyBusiness: 'Solutions professionnelles',
        companyReviews: 'Avis',
        companyContacts: 'Contact',
        supportHow: 'Comment ça marche',
        supportAssistance: 'Assistance client',
        supportReturns: 'Retours et remboursements',
        supportTerms: 'Conditions générales',
        supportPrivacy: 'Confidentialité',
        supportCookies: 'Cookies',
        cookieManage: 'Gérer les préférences cookies',
        phoneLabel: 'Téléphone',
        emailLabel: 'E-mail',
        copyright: 'Aml Store. Tous droits réservés.',
        vatLabel: 'TVA 11461870963',
        trademarkDisclaimer: 'Les noms de produits, logos et marques mentionnés appartiennent à leurs propriétaires respectifs et sont utilisés à des fins d’identification/illustration uniquement. Aml Store n’est affiliée ni sponsorisée par les titulaires des marques.',
        paymentsLabel: 'Moyens de paiement acceptés',
    },
    de: {
        logoAlt: 'Aml Store',
        brandDesc: 'Originalsoftware, italienische Rechnungsstellung und persönliche Unterstützung. Lösungen für Privatkunden, Fachleute und Unternehmen.',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italien',
        supportHours: 'Mo–Sa · 08:00–19:00 Uhr (italienische Zeit)',
        supportLanguage: 'Support auf Englisch',
        headingCatalog: 'Katalog',
        headingCompany: 'Unternehmen',
        headingSupport: 'Support',
        footerNavAria: 'Navigation in der Fußzeile',
        legalNavAria: 'Rechtliche Informationen',
        prodOs: 'Windows',
        prodOffice: 'Office',
        prodM365: 'Microsoft 365',
        prodAntivirus: 'Antivirus',
        companyAbout: 'Über uns',
        aboutSlug: 'ueber-uns',
        companyConsultation: 'Softwareberatung',
        consultationSlug: 'beratung',
        companyBusiness: 'Business-Lösungen',
        companyReviews: 'Bewertungen',
        companyContacts: 'Kontakt',
        supportHow: 'So funktioniert es',
        supportAssistance: 'Kundensupport',
        supportReturns: 'Rückgabe und Erstattung',
        supportTerms: 'Allgemeine Geschäftsbedingungen',
        supportPrivacy: 'Datenschutz',
        supportCookies: 'Cookies',
        cookieManage: 'Cookie-Einstellungen',
        phoneLabel: 'Telefon',
        emailLabel: 'E-Mail',
        copyright: 'Aml Store. Alle Rechte vorbehalten.',
        vatLabel: 'USt-IdNr. 11461870963',
        trademarkDisclaimer: 'Erwähnte Produktnamen, Logos und Marken sind Eigentum ihrer jeweiligen Inhaber und dienen nur zu Identifikations-/Illustrationszwecken. Aml Store ist weder mit den Markeninhabern verbunden noch von ihnen gesponsert.',
        paymentsLabel: 'Akzeptierte Zahlungsmethoden',
    },
    es: {
        logoAlt: 'Aml Store',
        brandDesc: 'Software original, facturación italiana y asistencia humana. Soluciones para particulares, profesionales y empresas.',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italia',
        supportHours: 'Lun–Sáb · 08:00–19:00 (hora de Italia)',
        supportLanguage: 'Asistencia en inglés',
        headingCatalog: 'Catálogo',
        headingCompany: 'Empresa',
        headingSupport: 'Soporte',
        footerNavAria: 'Navegación del pie de página',
        legalNavAria: 'Información legal',
        prodOs: 'Windows',
        prodOffice: 'Office',
        prodM365: 'Microsoft 365',
        prodAntivirus: 'Antivirus',
        companyAbout: 'Quiénes somos',
        aboutSlug: 'quienes-somos',
        companyConsultation: 'Asesoramiento de software',
        consultationSlug: 'consultoria',
        companyBusiness: 'Soluciones empresariales',
        companyReviews: 'Reseñas',
        companyContacts: 'Contacto',
        supportHow: 'Cómo funciona',
        supportAssistance: 'Atención al cliente',
        supportReturns: 'Devoluciones y reembolsos',
        supportTerms: 'Términos y condiciones',
        supportPrivacy: 'Privacidad',
        supportCookies: 'Cookies',
        cookieManage: 'Gestionar preferencias de cookies',
        phoneLabel: 'Teléfono',
        emailLabel: 'Email',
        copyright: 'Aml Store. Todos los derechos reservados.',
        vatLabel: 'NIF 11461870963',
        trademarkDisclaimer: 'Los nombres de producto, logotipos y marcas mencionados pertenecen a sus respectivos propietarios y se usan solo con fines identificativos/ilustrativos. Aml Store no está afiliada ni patrocinada por los titulares de las marcas.',
        paymentsLabel: 'Métodos de pago aceptados',
    },
    pt: {
        logoAlt: 'Aml Store',
        brandDesc: 'Software original, faturação italiana e suporte humano. Soluções para particulares, profissionais e empresas.',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Itália',
        supportHours: 'Seg–Sáb · 08:00–19:00 (hora de Itália)',
        supportLanguage: 'Suporte em inglês',
        headingCatalog: 'Catálogo',
        headingCompany: 'Empresa',
        headingSupport: 'Suporte',
        footerNavAria: 'Navegação do rodapé',
        legalNavAria: 'Informações legais',
        prodOs: 'Windows',
        prodOffice: 'Office',
        prodM365: 'Microsoft 365',
        prodAntivirus: 'Antivírus',
        companyAbout: 'Sobre nós',
        aboutSlug: 'sobre-nos',
        companyConsultation: 'Consultoria de software',
        consultationSlug: 'consultoria',
        companyBusiness: 'Soluções empresariais',
        companyReviews: 'Avaliações',
        companyContacts: 'Contactos',
        supportHow: 'Como funciona',
        supportAssistance: 'Apoio ao cliente',
        supportReturns: 'Devoluções e reembolsos',
        supportTerms: 'Termos e condições',
        supportPrivacy: 'Privacidade',
        supportCookies: 'Cookies',
        cookieManage: 'Gerir preferências de cookies',
        phoneLabel: 'Telefone',
        emailLabel: 'Email',
        copyright: 'Aml Store. Todos os direitos reservados.',
        vatLabel: 'NIF 11461870963',
        trademarkDisclaimer: 'Os nomes de produto, logótipos e marcas mencionados pertencem aos respetivos proprietários e são usados apenas para fins identificativos/ilustrativos. A Aml Store não é afiliada nem patrocinada pelos titulares das marcas.',
        paymentsLabel: 'Métodos de pagamento aceites',
    },
    nl: {
        logoAlt: 'Aml Store',
        brandDesc: 'Originele software, Italiaanse facturatie en menselijke ondersteuning. Oplossingen voor particulieren, professionals en bedrijven.',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italië',
        supportHours: 'Ma–za · 08:00–19:00 (Italiaanse tijd)',
        supportLanguage: 'Ondersteuning in het Engels',
        headingCatalog: 'Catalogus',
        headingCompany: 'Bedrijf',
        headingSupport: 'Ondersteuning',
        footerNavAria: 'Voettekstnavigatie',
        legalNavAria: 'Juridische informatie',
        prodOs: 'Windows',
        prodOffice: 'Office',
        prodM365: 'Microsoft 365',
        prodAntivirus: 'Antivirus',
        companyAbout: 'Over ons',
        aboutSlug: 'over-ons',
        companyConsultation: 'Softwareadvies',
        consultationSlug: 'consultatie',
        companyBusiness: 'Zakelijke oplossingen',
        companyReviews: 'Beoordelingen',
        companyContacts: 'Contact',
        supportHow: 'Hoe het werkt',
        supportAssistance: 'Klantenservice',
        supportReturns: 'Retourneren en terugbetalingen',
        supportTerms: 'Algemene voorwaarden',
        supportPrivacy: 'Privacy',
        supportCookies: 'Cookies',
        cookieManage: 'Cookievoorkeuren beheren',
        phoneLabel: 'Telefoon',
        emailLabel: 'E-mail',
        copyright: 'Aml Store. Alle rechten voorbehouden.',
        vatLabel: 'BTW 11461870963',
        trademarkDisclaimer: 'De genoemde productnamen, logo’s en merken zijn eigendom van hun respectieve houders en worden alleen gebruikt ter identificatie/illustratie. Aml Store is niet gelieerd aan of gesponsord door de merkhouders.',
        paymentsLabel: 'Geaccepteerde betaalmethoden',
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
        const aboutHref = S.localePageUrl(parsed.pathPrefix, activeLang.code, t.aboutSlug);
        const esc = S.escapeHtmlAttr;
        const staticRoot = S.staticRootFromScriptPath('/components/footer.js');
        const pageHref = (slug) => `${staticRoot}/${activeLang.code}/${slug}`;
        const reviewHost = activeLang.code === 'en' ? 'www.trustpilot.com' : `${activeLang.code}.trustpilot.com`;
        const reviewsHref = `https://${reviewHost}/review/aml-store.com`;
        const logoSrc = `${staticRoot}/logo/logo-header-400-light.webp`;
        const footerBgSrc = `${staticRoot}/asset/media/aml_store_media_background_footer.avif`;
        const footerBgMobileSrc = `${staticRoot}/asset/media/aml_store_media_background_footer_mobile.avif`;

        try {
            this.shadowRoot.innerHTML = `
                <style>
                    :host {
                        display: block;
                        position: relative;
                        z-index: 10;
                        background: var(--aml-navy, #0A1830);
                        color: #c6d1df;
                        font-family: var(--aml-font-sans, 'Montserrat', sans-serif);
                    }

                    * { box-sizing: border-box; }

                    .site-footer {
                        position: relative;
                        isolation: isolate;
                        overflow: hidden;
                        background-color: var(--aml-navy, #0A1830);
                        background-image: url("${esc(footerBgMobileSrc)}");
                        background-repeat: no-repeat;
                        background-size: cover;
                        background-position: center bottom;
                        color: #c6d1df;
                        border-top: 1px solid rgba(255, 255, 255, 0.08);
                    }

                    @media (min-width: 768px) {
                        .site-footer {
                            background-image: url("${esc(footerBgSrc)}");
                            background-position: right bottom;
                        }
                    }

                    /* Echo soft: geometria residuale, testo sempre leggibile */
                    .site-footer::before {
                        content: "";
                        position: absolute;
                        inset: 0;
                        z-index: 0;
                        pointer-events: none;
                        background: rgba(10, 24, 48, 0.82);
                    }

                    .site-footer > * {
                        position: relative;
                        z-index: 1;
                    }

                    .container {
                        width: min(var(--aml-maxw, 1180px), calc(100% - (2 * var(--aml-gutter, 2rem))));
                        margin-inline: auto;
                    }

                    .footer-main {
                        display: grid;
                        grid-template-columns: minmax(260px, 1.45fr) repeat(3, minmax(140px, 1fr));
                        gap: clamp(2.5rem, 5vw, 4.75rem);
                        padding-block: clamp(3.75rem, 6vw, 5rem) clamp(3.25rem, 5vw, 4.25rem);
                    }

                    .brand-col {
                        min-width: 0;
                        max-width: 360px;
                    }

                    .footer-logo {
                        display: inline-flex;
                        margin-bottom: 1.25rem;
                        border-radius: var(--aml-radius-sm, 6px);
                    }

                    .footer-logo img {
                        display: block;
                        width: 145px;
                        height: auto;
                    }

                    .footer-logo:focus-visible,
                    a:focus-visible,
                    button:focus-visible {
                        outline: 2px solid #ffffff;
                        outline-offset: 4px;
                    }

                    .brand-desc {
                        max-width: 335px;
                        margin: 0;
                        color: #aebdce;
                        font-size: 0.82rem;
                        line-height: 1.75;
                    }

                    .brand-contacts {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 0.35rem 1rem;
                        margin-top: 1.2rem;
                    }

                    .brand-contacts a {
                        color: #dce6f1;
                        font-size: 0.76rem;
                        font-weight: 600;
                        text-decoration: none;
                    }

                    .brand-support {
                        margin: 0.8rem 0 0;
                        color: #8fa2b7;
                        font-size: 0.7rem;
                        line-height: 1.65;
                    }

                    .brand-support span { display: block; }

                    /* Badge metodi di pagamento — micro-card bianche responsive e pulite */
                    .footer-pay {
                        display: flex;
                        align-items: center;
                        flex-wrap: wrap;
                        gap: 6px;
                        margin-top: 1.25rem;
                        max-width: 100%;
                    }

                    .footer-pay__logo {
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        flex-shrink: 0;
                        height: 26px;
                        padding: 3px 7px;
                        background: #ffffff;
                        border-radius: 5px;
                        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
                        transition: transform 0.15s ease, box-shadow 0.15s ease;
                    }

                    .footer-pay__logo:hover {
                        transform: translateY(-1px);
                        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.18);
                    }

                    .footer-pay__logo img {
                        height: 14px;
                        width: auto;
                        max-width: 38px;
                        object-fit: contain;
                        display: block;
                    }

                    .footer-nav {
                        display: contents;
                    }

                    .nav-col { min-width: 0; }

                    .col-title {
                        margin: 0 0 1.15rem;
                        color: #ffffff;
                        font-size: 0.72rem;
                        font-weight: 750;
                        line-height: 1.25;
                        letter-spacing: 0.08em;
                        text-transform: uppercase;
                    }

                    .link-list {
                        display: flex;
                        flex-direction: column;
                        gap: 0.55rem;
                        margin: 0;
                        padding: 0;
                        list-style: none;
                    }

                    .link-list a,
                    .link-list button {
                        display: inline;
                        width: fit-content;
                        margin: 0;
                        padding: 0.12rem 0;
                        border: 0;
                        background: none;
                        color: #b8c7d8;
                        font: inherit;
                        font-size: 0.8rem;
                        font-weight: 500;
                        line-height: 1.5;
                        text-align: left;
                        text-decoration: none;
                        cursor: pointer;
                        transition: color 160ms ease;
                    }

                    .link-list a:hover,
                    .link-list button:hover {
                        color: #ffffff;
                        text-decoration: underline;
                        text-decoration-color: var(--aml-brand, #3267AC);
                        text-underline-offset: 0.25rem;
                    }

                    .footer-bottom {
                        border-top: 1px solid rgba(255, 255, 255, 0.13);
                    }

                    .footer-bottom-inner {
                        display: flex;
                        align-items: flex-start;
                        justify-content: space-between;
                        gap: 2rem;
                        padding-block: 1.35rem 1.55rem;
                    }

                    .copyright {
                        max-width: 680px;
                        margin: 0;
                        color: #8fa2b7;
                        font-size: 0.68rem;
                        line-height: 1.65;
                    }

                    .copyright-legal { display: block; }

                    .legal-links {
                        display: flex;
                        flex-wrap: wrap;
                        justify-content: flex-end;
                        gap: 0.35rem 1rem;
                    }

                    .legal-links a,
                    .legal-links button {
                        margin: 0;
                        padding: 0;
                        border: 0;
                        background: none;
                        color: #8fa2b7;
                        font: inherit;
                        font-size: 0.68rem;
                        line-height: 1.5;
                        text-decoration: none;
                        cursor: pointer;
                    }

                    .legal-links a:hover,
                    .legal-links button:hover {
                        color: #ffffff;
                        text-decoration: underline;
                        text-underline-offset: 0.2rem;
                    }

                    @media (max-width: 900px) {
                        .footer-main {
                            grid-template-columns: repeat(2, minmax(0, 1fr));
                            gap: 2.75rem clamp(2rem, 8vw, 4rem);
                        }

                        .brand-col {
                            grid-column: 1 / -1;
                            max-width: 520px;
                        }
                    }

                    @media (max-width: 560px) {
                        .container {
                            width: min(100% - 2rem, var(--aml-maxw, 1180px));
                        }

                        .footer-main {
                            grid-template-columns: 1fr;
                            gap: 2.25rem;
                            padding-block: 3.25rem 2.75rem;
                        }

                        .brand-col { grid-column: auto; }

                        .link-list { gap: 0.4rem; }

                        .link-list a,
                        .link-list button {
                            min-height: 2rem;
                            display: inline-flex;
                            align-items: center;
                        }

                        .footer-bottom-inner {
                            flex-direction: column;
                            gap: 1rem;
                            padding-block: 1.3rem 1.5rem;
                        }

                        .legal-links {
                            justify-content: flex-start;
                            gap: 0.25rem 0.5rem;
                        }

                        .legal-links a,
                        .legal-links button {
                            display: inline-flex;
                            align-items: center;
                            min-height: 2.75rem;
                            padding-inline: 0.25rem;
                        }
                    }

                    @media (prefers-reduced-motion: reduce) {
                        .link-list a,
                        .link-list button { transition: none; }
                    }
                </style>

                <footer class="site-footer">
                    <div class="container footer-main">
                        <div class="brand-col">
                            <a href="${esc(homeHref)}" class="footer-logo">
                                <img src="${esc(logoSrc)}" width="288" height="96" alt="${esc(t.logoAlt)}">
                            </a>
                            <p class="brand-desc">${esc(t.brandDesc)}</p>
                            <div class="brand-contacts">
                                <a href="tel:+393925580413" aria-label="${esc(t.phoneLabel)}: +39 392 558 0413">+39 392 558 0413</a>
                                <a href="mailto:Info@amlstore.it" aria-label="${esc(t.emailLabel)}: Info@amlstore.it">Info@amlstore.it</a>
                            </div>
                            <p class="brand-support">
                                <span>${esc(t.supportHours)}</span>
                                <span>${esc(t.supportLanguage)}</span>
                            </p>
                            <div class="footer-pay" role="group" aria-label="${esc(t.paymentsLabel)}">
                                <span class="footer-pay__logo" data-brand="Visa"><img src="${esc(staticRoot)}/asset/payments_logo/img-aml-store_Visa_logo.svg" alt="Visa" width="30" height="14" loading="lazy" decoding="async"></span>
                                <span class="footer-pay__logo" data-brand="Mastercard"><img src="${esc(staticRoot)}/asset/payments_logo/img-aml-store_Mastercard_logo.svg" alt="Mastercard" width="30" height="14" loading="lazy" decoding="async"></span>
                                <span class="footer-pay__logo" data-brand="PayPal"><img src="${esc(staticRoot)}/asset/payments_logo/img-aml-store_PayPal-logo.svg" alt="PayPal" width="40" height="14" loading="lazy" decoding="async"></span>
                                <span class="footer-pay__logo" data-brand="Apple Pay"><img src="${esc(staticRoot)}/asset/payments_logo/img-aml-store_Apple_Pay_logo.svg" alt="Apple Pay" width="30" height="14" loading="lazy" decoding="async"></span>
                                <span class="footer-pay__logo" data-brand="Google Pay"><img src="${esc(staticRoot)}/asset/payments_logo/img-aml-store_Google_Pay_Logo.svg" alt="Google Pay" width="30" height="14" loading="lazy" decoding="async"></span>
                                <span class="footer-pay__logo" data-brand="Stripe"><img src="${esc(staticRoot)}/asset/payments_logo/img-aml-store_Stripe_Logo.svg" alt="Stripe" width="30" height="14" loading="lazy" decoding="async"></span>
                            </div>
                        </div>

                        <nav class="footer-nav" aria-label="${esc(t.footerNavAria)}">
                            <section class="nav-col" aria-labelledby="footer-catalog-${esc(activeLang.code)}">
                                <h2 id="footer-catalog-${esc(activeLang.code)}" class="col-title">${esc(t.headingCatalog)}</h2>
                                <ul class="link-list">
                                    <li><a href="${esc(pageHref('antivirus'))}">${esc(t.prodAntivirus)}</a></li>
                                    <li><a href="${esc(pageHref('microsoft-365-solutions'))}">${esc(t.prodM365)}</a></li>
                                    <li><a href="${esc(pageHref('sistemi-operativi'))}">${esc(t.prodOs)}</a></li>
                                    <li><a href="${esc(pageHref('suite-office'))}">${esc(t.prodOffice)}</a></li>
                                </ul>
                            </section>

                            <section class="nav-col" aria-labelledby="footer-company-${esc(activeLang.code)}">
                                <h2 id="footer-company-${esc(activeLang.code)}" class="col-title">${esc(t.headingCompany)}</h2>
                                <ul class="link-list">
                                    <li><a href="${esc(aboutHref)}">${esc(t.companyAbout)}</a></li>
                                    <li><a href="${esc(consultationHref)}">${esc(t.companyConsultation)}</a></li>
                                    <li><a href="${esc(pageHref('windows-server'))}">${esc(t.companyBusiness)}</a></li>
                                    <li><a href="${esc(reviewsHref)}" target="_blank" rel="noopener noreferrer">${esc(t.companyReviews)}</a></li>
                                    <li><a href="${esc(pageHref('contacts'))}">${esc(t.companyContacts)}</a></li>
                                </ul>
                            </section>

                            <section class="nav-col" aria-labelledby="footer-support-${esc(activeLang.code)}">
                                <h2 id="footer-support-${esc(activeLang.code)}" class="col-title">${esc(t.headingSupport)}</h2>
                                <ul class="link-list">
                                    <li><a href="${esc(homeHref)}#come-funziona">${esc(t.supportHow)}</a></li>
                                    <li><a href="https://wa.me/393925580413" target="_blank" rel="noopener noreferrer">${esc(t.supportAssistance)}</a></li>
                                    <li><a href="${esc(pageHref('terms-and-conditions'))}">${esc(t.supportTerms)}</a></li>
                                    <li><a href="${esc(pageHref('returns-and-refunds'))}">${esc(t.supportReturns)}</a></li>
                                </ul>
                            </section>
                        </nav>
                    </div>

                    <div class="footer-bottom">
                        <div class="container footer-bottom-inner">
                            <p class="copyright">
                                &copy; ${new Date().getFullYear()} ${esc(t.copyright)}
                                <span class="copyright-legal">${esc(t.legalName)} · ${esc(t.legalAddress)} · ${esc(t.vatLabel)}</span>
                                <span class="copyright-legal">${esc(t.trademarkDisclaimer)}</span>
                            </p>
                            <nav class="legal-links" aria-label="${esc(t.legalNavAria)}">
                                <a href="${esc(pageHref('privacy-policy'))}">${esc(t.supportPrivacy)}</a>
                                <a href="${esc(pageHref('cookie-policy'))}">${esc(t.supportCookies)}</a>
                                <a href="${esc(pageHref('terms-and-conditions'))}">${esc(t.supportTerms)}</a>
                                <button type="button" data-aml-cookie-settings>${esc(t.cookieManage)}</button>
                            </nav>
                        </div>
                    </div>
                </footer>
            `;

            this.shadowRoot.querySelector('[data-aml-cookie-settings]')?.addEventListener('click', (event) => {
                event.preventDefault();
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
