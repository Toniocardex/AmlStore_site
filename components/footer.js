(function () {
    'use strict';

    const LANGS = [
    { code: 'it', label: 'IT', flag: 'it' },
    { code: 'en', label: 'EN', flag: 'gb' },
    { code: 'fr', label: 'FR', flag: 'fr' },
    { code: 'de', label: 'DE', flag: 'de' },
    { code: 'es', label: 'ES', flag: 'es' },
];

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
        assistanceLabel: 'Assistenza',
        emailSub: 'Rispondiamo h24',
        copyright: 'Aml Store. Tutti i diritti riservati. P.IVA 12345678901.',
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
        assistanceLabel: 'Support',
        emailSub: 'We respond 24/7',
        copyright: 'Aml Store. All rights reserved. VAT 12345678901.',
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
        assistanceLabel: 'Assistance',
        emailSub: 'Réponse 24h/24',
        copyright: 'Aml Store. Tous droits réservés. TVA 12345678901.',
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
        assistanceLabel: 'Support',
        emailSub: 'Wir antworten rund um die Uhr',
        copyright: 'Aml Store. Alle Rechte vorbehalten. USt-IdNr. 12345678901.',
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
        assistanceLabel: 'Asistencia',
        emailSub: 'Respondemos 24/7',
        copyright: 'Aml Store. Todos los derechos reservados. NIF 12345678901.',
    },
};

function isKnownLangCode(segment) {
    return LANGS.some((l) => l.code === segment);
}

/** Primo segmento del path che coincide con una lingua del sito (es. /repo/it/ → it). */
function detectLangCodeFromPath() {
    const segments = window.location.pathname.split('/').filter(Boolean);
    const found = segments.find((seg) => isKnownLangCode(seg));
    return found || 'it';
}

/** Prefisso URL prima della cartella lingua (es. /repo per /repo/it/). */
function pathPrefixBeforeLang(langCode) {
    const segments = window.location.pathname.split('/').filter(Boolean);
    const idx = segments.indexOf(langCode);
    if (idx <= 0) return '';
    return '/' + segments.slice(0, idx).join('/');
}

function homeHrefForLang(langCode) {
    const prefix = pathPrefixBeforeLang(langCode);
    return prefix + '/' + langCode + '/';
}

/** Testo sicuro per innerHTML / attributi tra doppi apici (vanilla, no librerie). */
function escapeHtml(text) {
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

/** Prefisso path statici (es. /repo) ricavato dallo script components/footer.js (ok con defer e sottopath Pages). */
function amlStaticRootFromFooterScript() {
    const needle = '/components/footer.js';
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

class EcommerceFooter extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        if (this.__footerUiInit) return;

        this.setAttribute('translate', 'no');
        this.classList.add('notranslate');

        const langCode = detectLangCodeFromPath();
        const activeLang = LANGS.find((l) => l.code === langCode) || LANGS[0];
        const t = FOOTER_I18N[activeLang.code] || FOOTER_I18N.it;
        const homeHref = homeHrefForLang(activeLang.code);
        const esc = escapeHtml;
        const staticRoot = amlStaticRootFromFooterScript();
        const logoSrc = `${staticRoot}/logo/logo-header-400.webp`;

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
                    --accent: #3b82f6; /* Blu elegante */
                    --accent-hover: #60a5fa;
                    --glow-color: rgba(59, 130, 246, 0.15);
                    
                    position: relative;
                    z-index: 10;
                    border-top: 1px solid var(--border-color);
                    background-color: var(--bg-base);
                    color: var(--text-primary);
                    overflow: hidden;
                }

                * { box-sizing: border-box; margin: 0; padding: 0; }

                /* Effetto Glow di sfondo molto sottile */
                .footer-bg-glow {
                    position: absolute;
                    top: 0;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 80%;
                    height: 300px;
                    background: radial-gradient(ellipse at top, var(--glow-color) 0%, transparent 70%);
                    pointer-events: none;
                    z-index: 0;
                }

                .container {
                    position: relative;
                    z-index: 1;
                    max-width: 1280px;
                    margin: 0 auto;
                    padding: 0 clamp(1.5rem, 5vw, 4rem);
                }

                /* --- GRIGLIA PRINCIPALE --- */
                .footer-main {
                    padding: 5rem 0 4rem;
                    display: grid;
                    grid-template-columns: 2fr 1fr 1fr 1.5fr;
                    gap: 3rem 2rem;
                }

                /* BRAND COLUMN */
                .brand-col {
                    padding-right: 2rem;
                }

                .footer-logo {
                    display: inline-block;
                    margin-bottom: 1.5rem;
                    border-radius: 6px;
                    transition: opacity 0.2s ease;
                }

                .footer-logo:hover {
                    opacity: 0.9;
                }

                .footer-logo:focus-visible {
                    outline: 2px solid var(--accent);
                    outline-offset: 4px;
                }

                .footer-logo img {
                    height: 44px;
                    width: auto;
                    display: block;
                    /* Assicuriamo che il logo diventi bianco se è nero nativamente */
                    filter: brightness(0) invert(1); 
                }

                .brand-desc {
                    color: var(--text-secondary);
                    font-size: 0.95rem;
                    line-height: 1.7;
                    font-weight: 500;
                    max-width: 400px;
                }

                /* TITOLI COLONNE */
                h3.col-title {
                    font-size: 0.75rem;
                    font-weight: 700;
                    color: var(--text-primary);
                    text-transform: uppercase;
                    letter-spacing: 0.15em;
                    margin-bottom: 1.75rem;
                    opacity: 0.9;
                }

                /* LINK LISTE */
                .link-list {
                    list-style: none;
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                }

                .link-list a {
                    color: var(--text-secondary);
                    text-decoration: none;
                    font-size: 0.95rem;
                    font-weight: 500;
                    display: inline-flex;
                    align-items: center;
                    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
                }

                .link-list a:hover,
                .link-list a:focus-visible {
                    color: var(--accent-hover);
                    transform: translateX(6px);
                }

                /* CONTATTI */
                .contact-wrapper {
                    display: flex;
                    flex-direction: column;
                    gap: 1.5rem;
                }

                .contact-item {
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                }

                .contact-icon {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 40px;
                    height: 40px;
                    border-radius: 10px;
                    background: rgba(255, 255, 255, 0.03);
                    border: 1px solid var(--border-color);
                    color: var(--text-primary);
                    flex-shrink: 0;
                    transition: background 0.2s ease, border-color 0.2s ease;
                }
                
                .contact-item:hover .contact-icon {
                    background: rgba(255, 255, 255, 0.08);
                    border-color: rgba(255, 255, 255, 0.15);
                }

                .contact-icon svg {
                    width: 18px;
                    height: 18px;
                    fill: currentColor;
                }

                .contact-text {
                    display: flex;
                    flex-direction: column;
                    gap: 0.2rem;
                }

                .contact-label {
                    font-size: 0.75rem;
                    font-weight: 600;
                    color: var(--text-muted);
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                }

                .contact-value {
                    font-size: 0.95rem;
                    font-weight: 600;
                    color: var(--text-primary);
                    text-decoration: none;
                    transition: color 0.2s ease;
                }

                a.contact-value:hover {
                    color: var(--accent-hover);
                }

                /* --- BARRA INFERIORE --- */
                .footer-bottom {
                    border-top: 1px solid var(--border-color);
                    background-color: var(--bg-surface);
                }

                .bottom-content {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 1.5rem clamp(1.5rem, 5vw, 4rem);
                    flex-wrap: wrap;
                    gap: 1.5rem;
                }

                .copyright {
                    color: var(--text-muted);
                    font-size: 0.85rem;
                    font-weight: 500;
                }

                /* PAGAMENTI */
                .payments {
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                    flex-wrap: wrap;
                }

                .payment-badge {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 0.4rem 0.75rem;
                    border-radius: 6px;
                    background: rgba(255, 255, 255, 0.03);
                    border: 1px solid var(--border-color);
                    transition: all 0.2s ease;
                    /* Grayscale iniziale per un look minimal, a colori in hover */
                    filter: grayscale(100%) opacity(0.6);
                }

                .payment-badge:hover {
                    background: rgba(255, 255, 255, 0.06);
                    border-color: rgba(255, 255, 255, 0.15);
                    filter: grayscale(0%) opacity(1);
                    transform: translateY(-2px);
                }

                .payment-badge svg {
                    height: 18px;
                    width: auto;
                    display: block;
                }

                /* --- RESPONSIVE DESIGN --- */
                @media (max-width: 1024px) {
                    .footer-main {
                        grid-template-columns: 1fr 1fr;
                    }
                    .brand-col {
                        grid-column: 1 / -1;
                        padding-right: 0;
                        margin-bottom: 1rem;
                    }
                    .brand-desc {
                        max-width: 600px;
                    }
                }

                @media (max-width: 640px) {
                    .footer-main {
                        grid-template-columns: 1fr;
                        gap: 2.5rem;
                        padding: 4rem 0 3rem;
                    }
                    .bottom-content {
                        flex-direction: column;
                        justify-content: center;
                        text-align: center;
                    }
                    .payments {
                        justify-content: center;
                    }
                }
            </style>

            <div class="footer-bg-glow"></div>
            
            <div class="container footer-main">
                <!-- Brand -->
                <div class="brand-col">
                    <a href="${esc(homeHref)}" class="footer-logo">
                        <!-- Testo visibile nell'anteprima in caso di assenza immagine locale -->
                        <img src="${esc(logoSrc)}" width="200" height="48" alt="${esc(t.logoAlt)}">
                    </a>
                    <p class="brand-desc">
                        ${esc(t.brandDesc)}
                    </p>
                </div>

                <!-- Prodotti -->
                <div>
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
                <div>
                    <h3 class="col-title">${esc(t.headingSupport)}</h3>
                    <ul class="link-list">
                        <li><a href="#">${esc(t.supportMyAccount)}</a></li>
                        <li><a href="#">${esc(t.supportInstallGuide)}</a></li>
                        <li><a href="#">${esc(t.supportReturns)}</a></li>
                        <li><a href="#">${esc(t.supportTerms)}</a></li>
                        <li><a href="#">${esc(t.supportPrivacy)}</a></li>
                    </ul>
                </div>

                <!-- Contatti -->
                <div>
                    <h3 class="col-title">${esc(t.headingContact)}</h3>
                    <div class="contact-wrapper">
                        <div class="contact-item">
                            <div class="contact-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                            </div>
                            <div class="contact-text">
                                <span class="contact-label">${esc(t.assistanceLabel)}</span>
                                <span class="contact-value">+39 02 1234 5678</span>
                            </div>
                        </div>
                        <div class="contact-item">
                            <div class="contact-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
                            </div>
                            <div class="contact-text">
                                <span class="contact-label">${esc(t.emailSub)}</span>
                                <a href="mailto:Info@amlstore.it" class="contact-value">Info@amlstore.it</a>
                            </div>
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
                    <div class="payments">
                        <div class="payment-badge" title="Visa">
                            <svg viewBox="0 0 38 24" fill="none" aria-hidden="true"><rect width="38" height="24" rx="4" fill="#1434CB"/><path d="M16.5 16h-3l1.5-10h3l-1.5 10zm11.2-9.8c-.5-.2-1.2-.3-2-.3-2.1 0-3.6 1.1-3.6 2.8 0 1.2 1.1 1.9 1.9 2.3.8.4 1.1.6 1.1 1 0 .5-.6.8-1.2.8-1.3 0-2-.3-2.7-.6l-.4-1.8c.6.3 1.5.5 2.3.5 2.2 0 3.7-1.1 3.7-2.8 0-1-.8-1.7-1.9-2.2-.7-.4-1.1-.6-1.1-1 0-.4.5-.7 1.1-.7 1 0 1.7.2 2.3.5l.5-1.5zm-15.4 9.8L10 9.8l-.8 4.2c-.1.6-.6 1-1.2 1H3v-.4c1.1-.2 2.3-.6 3.1-1.1l2.5-7.3h3.2l5 10h-4.5zM34 6h-2.5c-.6 0-1.1.3-1.4.9l-4 9.1h3.3l.6-1.8h4l.4 1.8h3l-3.4-10z" fill="#fff"/></svg>
                        </div>
                        <div class="payment-badge" title="Mastercard">
                            <svg viewBox="0 0 38 24" fill="none" aria-hidden="true"><rect width="38" height="24" rx="4" fill="#EB001B"/><circle cx="15" cy="12" r="7" fill="#F79E1B"/><circle cx="23" cy="12" r="7" fill="#FF5F00"/></svg>
                        </div>
                        <div class="payment-badge" title="PayPal">
                            <svg viewBox="0 0 38 24" fill="none" aria-hidden="true"><rect width="38" height="24" rx="4" fill="#0079C1"/><path d="M12.5 15h3.8c.2 0 .4-.1.5-.3l2.8-11.4c0-.2-.1-.3-.3-.3H15.6c-.2 0-.4.1-.5.3l-2.4 9.4c0 .2.1.3.3.3zM25.7 15h-3c-.2 0-.4-.1-.5-.3l-.8-3.4c-.1-.3.2-.5.5-.5h2c1.7 0 2.5-.8 2.8-2.2.1-.5 0-1-.3-1.4-.4-.4-1.1-.6-2-.6h-3.3c-.2 0-.4.1-.5.3l-2 8.3c0 .2.1.3.3.3h3.2c1.3 0 2.2-.6 2.4-1.8.1-.5 0-.9-.3-1.2-.3-.3-.9-.4-1.7-.4h-.8c-.2 0-.4.1-.5.3l-.2.8c0 .2.1.3.3.3h1.2c.4 0 .7.1.8.3.1.2.1.4.1.7-.1.7-.6 1-1.4 1H25.7c.2 0 .3.1.3.3l-.3 1z" fill="#fff"/></svg>
                        </div>
                    </div>
                </div>
            </div>
        `;
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