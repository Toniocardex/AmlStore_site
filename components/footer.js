class EcommerceFooter extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    font-family: 'Montserrat', sans-serif;
                    --bg-color: #0a0f1a;
                    --text-main: #ffffff;
                    --text-muted: #9ca3af;
                    --accent-color: #1a5fd1;
                    --color-gradient-start: #003182;
                }

                * { box-sizing: border-box; margin: 0; padding: 0; }

                .footer-wrapper {
                    background-color: var(--bg-color);
                    color: var(--text-main);
                    position: relative;
                }

                .footer-top-border {
                    height: 4px;
                    background: linear-gradient(90deg, var(--color-gradient-start) 0%, var(--accent-color) 100%);
                    width: 100%;
                }

                .footer-content {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 4rem 4% 2rem;
                }

                .footer-grid {
                    display: grid;
                    grid-template-columns: 2fr 1fr 1fr 1.5fr;
                    gap: 3rem;
                    margin-bottom: 3rem;
                    padding-bottom: 3rem;
                    border-bottom: 1px solid rgba(255,255,255,0.1);
                }

                .footer-col h3 {
                    font-size: 16px;
                    font-weight: 700;
                    margin-bottom: 1.5rem;
                    color: var(--text-main);
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }

                .footer-col ul {
                    list-style: none;
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                }

                .footer-col a {
                    color: var(--text-muted);
                    text-decoration: none;
                    font-size: 14px;
                    font-weight: 500;
                    transition: color 0.2s, padding-left 0.2s;
                }

                .footer-col a:hover {
                    color: var(--text-main);
                    padding-left: 4px;
                }

                .footer-logo { display: inline-block; margin-bottom: 1.5rem; }
                .footer-logo img { height: 48px; width: auto; display: block; filter: brightness(0) invert(1) drop-shadow(0 0 1px rgba(255,255,255,0.2)); }

                .footer-desc {
                    color: var(--text-muted);
                    font-size: 14px;
                    line-height: 1.6;
                    margin-bottom: 1.5rem;
                }

                .contact-info { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.5rem; }
                .contact-item { display: flex; align-items: flex-start; gap: 12px; color: var(--text-muted); font-size: 14px; }
                .contact-item svg { width: 18px; height: 18px; fill: var(--text-main); flex-shrink: 0; }

                .social-links { display: flex; gap: 1rem; }
                .social-links a {
                    display: flex; align-items: center; justify-content: center;
                    width: 36px; height: 36px; border-radius: 50%;
                    background: rgba(255,255,255,0.05); color: var(--text-main);
                    transition: background 0.2s, transform 0.2s;
                }
                .social-links a svg { width: 18px; height: 18px; fill: currentColor; }
                .social-links a:hover { background: var(--accent-color); transform: translateY(-3px); }

                .footer-bottom { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }
                .copyright { color: var(--text-muted); font-size: 13px; }
                .payment-methods { display: flex; gap: 10px; }
                .payment-icon { height: 24px; width: auto; opacity: 0.6; transition: opacity 0.2s; }
                .payment-icon:hover { opacity: 1; }

                @media (max-width: 992px) {
                    .footer-grid { grid-template-columns: 1fr 1fr; gap: 2.5rem; }
                }

                @media (max-width: 576px) {
                    .footer-grid { grid-template-columns: 1fr; gap: 2.5rem; }
                    .footer-bottom { flex-direction: column; text-align: center; }
                }
            </style>

            <div class="footer-wrapper">
                <div class="footer-top-border"></div>
                <div class="footer-content">

                    <div class="footer-grid">
                        <div class="footer-col">
                            <a href="#" class="footer-logo">
                                <img src="/logo/logo-header-400.webp" alt="Aml Store Logo Bianco">
                            </a>
                            <p class="footer-desc">
                                Il tuo partner affidabile per l'acquisto di licenze software originali. Sistemi Operativi, Office e Antivirus al miglior prezzo garantito.
                            </p>
                            <div class="social-links">
                                <a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24"><path d="M14 13.5h2.5l1-4H14v-2c0-1.03 0-2 2-2h1.5V2.14c-.326-.043-1.557-.14-2.857-.14-3.55 0-5.643 2.143-5.643 5.643v3.857H6.5v4h2.5v10.5h5v-10.5z"/></svg></a>
                                <a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg></a>
                                <a href="#" aria-label="LinkedIn"><svg viewBox="0 0 24 24"><path d="M4.98 3.5c0 1.381-1.11 2.5-2.48 2.5s-2.48-1.119-2.48-2.5c0-1.38 1.11-2.5 2.48-2.5s2.48 1.12 2.48 2.5zm.02 4.5h-5v16h5v-16zm7.982 0h-4.968v16h4.969v-8.399c0-4.67 6.029-5.052 6.029 0v8.399h4.988v-10.131c0-7.88-8.922-7.593-11.018-3.714v-2.155z"/></svg></a>
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
                                    <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                                    <span>Assistenza Clienti<br>+39 02 1234 5678</span>
                                </div>
                                <div class="contact-item">
                                    <svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
                                    <span>supporto@amlstore.it<br>Rispondiamo h24</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="footer-bottom">
                        <div class="copyright">
                            &copy; 2026 Aml Store. Tutti i diritti riservati. P.IVA 12345678901.
                        </div>
                        <div class="payment-methods">
                            <svg class="payment-icon" viewBox="0 0 38 24" fill="none"><rect width="38" height="24" rx="4" fill="#1434CB"/><path d="M16.5 16h-3l1.5-10h3l-1.5 10zm11.2-9.8c-.5-.2-1.2-.3-2-.3-2.1 0-3.6 1.1-3.6 2.8 0 1.2 1.1 1.9 1.9 2.3.8.4 1.1.6 1.1 1 0 .5-.6.8-1.2.8-1.3 0-2-.3-2.7-.6l-.4-1.8c.6.3 1.5.5 2.3.5 2.2 0 3.7-1.1 3.7-2.8 0-1-.8-1.7-1.9-2.2-.7-.4-1.1-.6-1.1-1 0-.4.5-.7 1.1-.7 1 0 1.7.2 2.3.5l.5-1.5zm-15.4 9.8L10 9.8l-.8 4.2c-.1.6-.6 1-1.2 1H3v-.4c1.1-.2 2.3-.6 3.1-1.1l2.5-7.3h3.2l5 10h-4.5zM34 6h-2.5c-.6 0-1.1.3-1.4.9l-4 9.1h3.3l.6-1.8h4l.4 1.8h3l-3.4-10z" fill="#fff"/></svg>
                            <svg class="payment-icon" viewBox="0 0 38 24" fill="none"><rect width="38" height="24" rx="4" fill="#EB001B"/><circle cx="15" cy="12" r="7" fill="#F79E1B"/><circle cx="23" cy="12" r="7" fill="#FF5F00"/></svg>
                            <svg class="payment-icon" viewBox="0 0 38 24" fill="none"><rect width="38" height="24" rx="4" fill="#0079C1"/><path d="M12.5 15h3.8c.2 0 .4-.1.5-.3l2.8-11.4c0-.2-.1-.3-.3-.3H15.6c-.2 0-.4.1-.5.3l-2.4 9.4c0 .2.1.3.3.3zM25.7 15h-3c-.2 0-.4-.1-.5-.3l-.8-3.4c-.1-.3.2-.5.5-.5h2c1.7 0 2.5-.8 2.8-2.2.1-.5 0-1-.3-1.4-.4-.4-1.1-.6-2-.6h-3.3c-.2 0-.4.1-.5.3l-2 8.3c0 .2.1.3.3.3h3.2c1.3 0 2.2-.6 2.4-1.8.1-.5 0-.9-.3-1.2-.3-.3-.9-.4-1.7-.4h-.8c-.2 0-.4.1-.5.3l-.2.8c0 .2.1.3.3.3h1.2c.4 0 .7.1.8.3.1.2.1.4.1.7-.1.7-.6 1-1.4 1H25.7c.2 0 .3.1.3.3l-.3 1z" fill="#fff"/></svg>
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
