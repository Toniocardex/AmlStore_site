class EcommerceFooter extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    position: relative;
                    z-index: 1;
                    isolation: isolate;
                    font-family: 'Montserrat', sans-serif;
                    --bg-deep: #060a12;
                    --bg-mid: #0c1830;
                    --text-main: #f8fafc;
                    --text-muted: #94a3b8;
                    --accent: #1a5fd1;
                    --accent-soft: rgba(26, 95, 209, 0.22);
                    --color-gradient-start: #003182;
                    --color-gradient-end: #1a5fd1;
                }

                * { box-sizing: border-box; margin: 0; padding: 0; }

                .footer-wrapper {
                    position: relative;
                    color: var(--text-main);
                    background:
                        radial-gradient(ellipse 120% 80% at 50% -40%, rgba(26, 95, 209, 0.28), transparent 55%),
                        linear-gradient(168deg, var(--bg-deep) 0%, var(--bg-mid) 42%, #080c16 100%);
                    overflow-x: clip;
                }

                .footer-wrapper::before {
                    content: '';
                    position: absolute;
                    inset: 0;
                    z-index: 0;
                    background: radial-gradient(circle at 85% 20%, rgba(0, 49, 130, 0.18), transparent 45%);
                    pointer-events: none;
                }

                .footer-top-border,
                .footer-accent-bar {
                    position: relative;
                    z-index: 2;
                    height: 5px;
                    width: 100%;
                    background: linear-gradient(118deg, var(--color-gradient-start) 0%, #0d4bb8 50%, var(--color-gradient-end) 100%);
                    box-shadow: 0 0 28px rgba(26, 95, 209, 0.45);
                }

                .footer-inner {
                    position: relative;
                    z-index: 1;
                    max-width: 1200px;
                    margin: 0 auto;
                    width: 100%;
                    box-sizing: border-box;
                    padding-left: clamp(1.25rem, 5vw, 3.5rem);
                    padding-right: clamp(1.25rem, 5vw, 3.5rem);
                }

                .footer-upper {
                    position: relative;
                    z-index: 1;
                    padding-top: clamp(2.5rem, 5vw, 4rem);
                    padding-bottom: clamp(1.75rem, 4vw, 2.75rem);
                    background: linear-gradient(180deg, rgba(255,255,255,0.045) 0%, rgba(255,255,255,0.01) 55%, transparent 100%);
                }

                .footer-lower {
                    position: relative;
                    z-index: 1;
                    padding-top: clamp(1.25rem, 3vw, 1.75rem);
                    padding-bottom: clamp(1.75rem, 4vw, 2.75rem);
                    background: linear-gradient(180deg, #03060d 0%, #010308 55%, #00040a 100%);
                    box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
                }

                .footer-col {
                    min-width: 0;
                }

                .footer-grid {
                    display: grid;
                    grid-template-columns: 1.85fr 1fr 1fr 1.35fr;
                    align-items: start;
                    gap: clamp(2rem, 4vw, 3.25rem);
                }

                .footer-brand-card {
                    padding: clamp(1.35rem, 3vw, 1.85rem);
                    border-radius: 18px;
                    background: linear-gradient(165deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%);
                    border: 1px solid rgba(255,255,255,0.1);
                    box-shadow:
                        0 12px 40px rgba(0, 0, 0, 0.35),
                        inset 0 1px 0 rgba(255,255,255,0.1);
                }

                .footer-logo {
                    display: inline-flex;
                    margin-bottom: 1.25rem;
                    border-radius: 12px;
                    outline-offset: 4px;
                }
                .footer-logo:focus-visible {
                    outline: 2px solid var(--accent);
                }
                .footer-logo img {
                    height: 48px;
                    width: auto;
                    display: block;
                    filter: brightness(0) invert(1) drop-shadow(0 1px 2px rgba(0,0,0,0.25));
                }

                .footer-desc {
                    color: var(--text-muted);
                    font-size: 14px;
                    line-height: 1.65;
                    font-weight: 500;
                    margin-bottom: 0;
                }

                .footer-col h3 {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    font-size: 12px;
                    font-weight: 800;
                    letter-spacing: 0.16em;
                    text-transform: uppercase;
                    color: rgba(255,255,255,0.92);
                    margin-bottom: 1.35rem;
                }
                .footer-col h3::before {
                    content: '';
                    width: 4px;
                    height: 2.5rem;
                    border-radius: 3px;
                    align-self: center;
                    background: linear-gradient(180deg, var(--color-gradient-end), var(--color-gradient-start));
                    box-shadow: 0 0 12px rgba(26, 95, 209, 0.55);
                    flex-shrink: 0;
                }

                .footer-col ul {
                    list-style: none;
                    display: flex;
                    flex-direction: column;
                    gap: 0.35rem;
                }

                .footer-col a {
                    display: block;
                    color: #b8c5d6;
                    text-decoration: none;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 0.5rem 0.75rem;
                    margin: 0 -0.75rem;
                    border-radius: 10px;
                    border: 1px solid transparent;
                    transition: color 0.2s ease, background 0.2s ease, border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
                }

                .footer-col a:hover {
                    color: var(--text-main);
                    background: var(--accent-soft);
                    border-color: rgba(26, 95, 209, 0.45);
                    box-shadow: 0 4px 16px rgba(0, 35, 90, 0.2);
                    transform: translateX(4px);
                }

                .contact-info {
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                }

                .contact-item {
                    display: flex;
                    align-items: flex-start;
                    gap: 14px;
                    padding: 0.65rem 0.75rem;
                    margin: 0 -0.75rem;
                    border-radius: 14px;
                    color: var(--text-muted);
                    font-size: 14px;
                    font-weight: 500;
                    line-height: 1.45;
                    transition: background 0.2s ease, color 0.2s ease;
                }
                .contact-item:hover {
                    background: rgba(255,255,255,0.04);
                    color: #e2e8f0;
                }
                .contact-item strong {
                    color: #e2e8f0;
                    font-weight: 700;
                }

                .contact-item .icon-wrap {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 42px;
                    height: 42px;
                    flex-shrink: 0;
                    border-radius: 12px;
                    background: linear-gradient(145deg, rgba(26,95,209,0.35) 0%, rgba(0,49,130,0.5) 100%);
                    border: 1px solid rgba(255,255,255,0.12);
                    box-shadow: 0 4px 14px rgba(0, 35, 90, 0.35), inset 0 1px 0 rgba(255,255,255,0.15);
                }
                .contact-item svg {
                    width: 18px;
                    height: 18px;
                    fill: var(--text-main);
                }

                .footer-bottom {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    flex-wrap: wrap;
                    gap: 1.25rem 2rem;
                    width: 100%;
                    box-sizing: border-box;
                }

                .copyright {
                    color: #7c8a9e;
                    font-size: 12px;
                    font-weight: 500;
                    letter-spacing: 0.02em;
                    line-height: 1.5;
                    max-width: 52ch;
                }

                .payment-methods {
                    display: flex;
                    align-items: center;
                    gap: 0.65rem;
                    flex-wrap: wrap;
                }

                .payment-wrap {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 8px 12px;
                    border-radius: 12px;
                    background: rgba(255,255,255,0.05);
                    border: 1px solid rgba(255,255,255,0.08);
                    transition: background 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
                }
                .payment-wrap:hover {
                    background: rgba(255,255,255,0.1);
                    border-color: rgba(255,255,255,0.15);
                    transform: translateY(-2px);
                }

                .payment-icon {
                    height: 22px;
                    width: auto;
                    display: block;
                    opacity: 0.92;
                    transition: opacity 0.2s ease;
                }
                .payment-wrap:hover .payment-icon {
                    opacity: 1;
                }

                @media (max-width: 992px) {
                    .footer-grid {
                        grid-template-columns: 1fr 1fr;
                    }
                    .footer-grid > .footer-col:first-child {
                        grid-column: 1 / -1;
                    }
                }

                @media (max-width: 576px) {
                    .footer-grid {
                        grid-template-columns: 1fr;
                    }
                    .footer-bottom {
                        flex-direction: column;
                        text-align: center;
                    }
                    .copyright {
                        max-width: none;
                    }
                    .payment-methods {
                        justify-content: center;
                    }
                }
            </style>

            <div class="footer-wrapper">
                <div class="footer-top-border" aria-hidden="true"></div>
                <div class="footer-upper">
                    <div class="footer-inner">
                        <div class="footer-grid">
                        <div class="footer-col">
                            <div class="footer-brand-card">
                                <a href="#" class="footer-logo">
                                    <img src="/logo/logo-header-400.webp" alt="Aml Store">
                                </a>
                                <p class="footer-desc">
                                    Il tuo partner affidabile per l'acquisto di licenze software originali. Sistemi Operativi, Office e Antivirus al miglior prezzo garantito.
                                </p>
                            </div>
                        </div>
                        <div class="footer-col">
                            <h3>Prodotti</h3>
                            <ul>
                                <li><a href="#">Sistemi Operativi</a></li>
                                <li><a href="#">Pacchetto Office</a></li>
                                <li><a href="#">Antivirus & Sicurezza</a></li>
                                <li><a href="#">Software Aziendali</a></li>
                                <li><a href="#">Offerte Speciali</a></li>
                            </ul>
                        </div>
                        <div class="footer-col">
                            <h3>Supporto</h3>
                            <ul>
                                <li><a href="#">Il mio account</a></li>
                                <li><a href="#">Guida all'installazione</a></li>
                                <li><a href="#">Resi e Rimborsi</a></li>
                                <li><a href="#">Termini e Condizioni</a></li>
                                <li><a href="#">Privacy Policy</a></li>
                            </ul>
                        </div>
                        <div class="footer-col">
                            <h3>Contattaci</h3>
                            <div class="contact-info">
                                <div class="contact-item">
                                    <span class="icon-wrap" aria-hidden="true">
                                        <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                                    </span>
                                    <span>Assistenza Clienti<br><strong>+39 02 1234 5678</strong></span>
                                </div>
                                <div class="contact-item">
                                    <span class="icon-wrap" aria-hidden="true">
                                        <svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
                                    </span>
                                    <span><strong>supporto@amlstore.it</strong><br>Rispondiamo h24</span>
                                </div>
                            </div>
                        </div>
                        </div>
                    </div>
                </div>

                <div class="footer-accent-bar" aria-hidden="true"></div>

                <div class="footer-lower">
                    <div class="footer-inner">
                        <div class="footer-bottom">
                        <div class="copyright">
                            &copy; 2026 Aml Store. Tutti i diritti riservati. P.IVA 12345678901.
                        </div>
                        <div class="payment-methods">
                            <span class="payment-wrap" title="Visa">
                                <svg class="payment-icon" viewBox="0 0 38 24" fill="none" aria-hidden="true"><rect width="38" height="24" rx="4" fill="#1434CB"/><path d="M16.5 16h-3l1.5-10h3l-1.5 10zm11.2-9.8c-.5-.2-1.2-.3-2-.3-2.1 0-3.6 1.1-3.6 2.8 0 1.2 1.1 1.9 1.9 2.3.8.4 1.1.6 1.1 1 0 .5-.6.8-1.2.8-1.3 0-2-.3-2.7-.6l-.4-1.8c.6.3 1.5.5 2.3.5 2.2 0 3.7-1.1 3.7-2.8 0-1-.8-1.7-1.9-2.2-.7-.4-1.1-.6-1.1-1 0-.4.5-.7 1.1-.7 1 0 1.7.2 2.3.5l.5-1.5zm-15.4 9.8L10 9.8l-.8 4.2c-.1.6-.6 1-1.2 1H3v-.4c1.1-.2 2.3-.6 3.1-1.1l2.5-7.3h3.2l5 10h-4.5zM34 6h-2.5c-.6 0-1.1.3-1.4.9l-4 9.1h3.3l.6-1.8h4l.4 1.8h3l-3.4-10z" fill="#fff"/></svg>
                            </span>
                            <span class="payment-wrap" title="Mastercard">
                                <svg class="payment-icon" viewBox="0 0 38 24" fill="none" aria-hidden="true"><rect width="38" height="24" rx="4" fill="#EB001B"/><circle cx="15" cy="12" r="7" fill="#F79E1B"/><circle cx="23" cy="12" r="7" fill="#FF5F00"/></svg>
                            </span>
                            <span class="payment-wrap" title="PayPal">
                                <svg class="payment-icon" viewBox="0 0 38 24" fill="none" aria-hidden="true"><rect width="38" height="24" rx="4" fill="#0079C1"/><path d="M12.5 15h3.8c.2 0 .4-.1.5-.3l2.8-11.4c0-.2-.1-.3-.3-.3H15.6c-.2 0-.4.1-.5.3l-2.4 9.4c0 .2.1.3.3.3zM25.7 15h-3c-.2 0-.4-.1-.5-.3l-.8-3.4c-.1-.3.2-.5.5-.5h2c1.7 0 2.5-.8 2.8-2.2.1-.5 0-1-.3-1.4-.4-.4-1.1-.6-2-.6h-3.3c-.2 0-.4.1-.5.3l-2 8.3c0 .2.1.3.3.3h3.2c1.3 0 2.2-.6 2.4-1.8.1-.5 0-.9-.3-1.2-.3-.3-.9-.4-1.7-.4h-.8c-.2 0-.4.1-.5.3l-.2.8c0 .2.1.3.3.3h1.2c.4 0 .7.1.8.3.1.2.1.4.1.7-.1.7-.6 1-1.4 1H25.7c.2 0 .3.1.3.3l-.3 1z" fill="#fff"/></svg>
                            </span>
                        </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
}

if (!customElements.get('ecommerce-footer')) {
    customElements.define('ecommerce-footer', EcommerceFooter);
}
