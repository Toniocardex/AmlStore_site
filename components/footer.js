(function () {
    'use strict';

const FOOTER_I18N = {
    it: {
        logoAlt: 'Aml Store',
        brandDesc: 'Software originale, fatturazione italiana e supporto umano. Soluzioni per privati, professionisti e aziende.',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italia',
        supportHours: 'Lun–Ven · 09:00–19:00',
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
    },
    en: {
        logoAlt: 'Aml Store',
        brandDesc: 'Genuine software, Italian invoicing and human support. Solutions for individuals, professionals and businesses.',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italy',
        supportHours: 'Mon–Fri · 09:00–19:00 (Italy time)',
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
    },
    fr: {
        logoAlt: 'Aml Store',
        brandDesc: "Logiciels authentiques, facturation italienne et assistance humaine. Des solutions pour particuliers, professionnels et entreprises.",
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italie',
        supportHours: 'Lun–Ven · 09:00–19:00 (heure italienne)',
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
    },
    de: {
        logoAlt: 'Aml Store',
        brandDesc: 'Originalsoftware, italienische Rechnungsstellung und persönliche Unterstützung. Lösungen für Privatkunden, Fachleute und Unternehmen.',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italien',
        supportHours: 'Mo–Fr · 09:00–19:00 Uhr (italienische Zeit)',
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
    },
    es: {
        logoAlt: 'Aml Store',
        brandDesc: 'Software original, facturación italiana y asistencia humana. Soluciones para particulares, profesionales y empresas.',
        legalName: 'Licensoft di Cardelli Antonino',
        legalAddress: 'Via Trento 5/A, 20015 Parabiago (MI), Italia',
        supportHours: 'Lun–Vie · 09:00–19:00 (hora de Italia)',
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
    },
};

class EcommerceFooter extends HTMLElement {
    constructor() {
        super();
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
            /* Markup pre-renderizzato nella pagina da
               scripts/build-inline-chrome.mjs: qui resta solo il comportamento. */
            if (!this.querySelector('.site-footer')) {
                console.error(
                    'ecommerce-footer: markup assente nella pagina. ' +
                    'Rigenerarlo con: node scripts/build-inline-chrome.mjs'
                );
                return;
            }


            this.querySelector('[data-aml-cookie-settings]')?.addEventListener('click', (event) => {
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
