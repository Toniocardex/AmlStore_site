class EcommerceHeader extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        // Il template è completamente incapsulato nella logica del componente
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    position: relative;
                    z-index: 1000;
                    --h-height: 80px;
                    --color-gradient-start: #003182;
                    --color-gradient-end: #1a5fd1;
                    --text-dark: #1a1a1a;
                    --text-light: #ffffff;
                    --text-grey: #666666;
                }

                * {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                    font-family: 'Montserrat', sans-serif;
                }

                .header-container {
                    position: relative;
                    height: var(--h-height);
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
                    overflow: hidden;
                }

                .bg-colored {
                    position: absolute;
                    top: 0; left: 0; right: 0; bottom: 0;
                    background: linear-gradient(135deg, var(--color-gradient-start) 0%, var(--color-gradient-end) 100%);
                    z-index: 1;
                }

                .bg-white {
                    position: absolute;
                    top: 0; left: 0; bottom: 0;
                    width: 55%;
                    background: #ffffff;
                    clip-path: polygon(0 0, calc(100% - 75px) 0, 100% 100%, 0 100%);
                    z-index: 2;
                }

                .content-wrapper {
                    position: relative;
                    z-index: 3;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    padding: 0 4%;
                }

                .left-section {
                    display: flex;
                    align-items: center;
                    gap: 2rem;
                    flex: 1;
                }

                .logo {
                    display: flex;
                    align-items: center;
                    text-decoration: none;
                }
                .logo img {
                    height: 64px;
                    width: auto;
                    display: block;
                    object-fit: contain;
                }

                .nav-links {
                    display: flex;
                    gap: 1.5rem;
                }
                .nav-links a {
                    text-decoration: none;
                    color: var(--text-grey);
                    font-weight: 600;
                    font-size: 14px;
                    transition: color 0.2s;
                }
                .nav-links a.active {
                    color: var(--text-dark);
                    position: relative;
                }
                .nav-links a:hover {
                    color: var(--text-dark);
                }

                .right-section {
                    display: flex;
                    align-items: center;
                    gap: 1.5rem;
                    color: var(--text-light);
                }

                .phone-number {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    font-size: 13px;
                    font-weight: 600;
                    opacity: 0.9;
                }
                .phone-number svg {
                    width: 14px;
                    height: 14px;
                    fill: currentColor;
                }

                .lang-selector {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    font-size: 13px;
                    font-weight: 600;
                    cursor: pointer;
                    opacity: 0.9;
                    transition: opacity 0.2s;
                }
                .lang-selector:hover {
                    opacity: 1;
                }
                .flag-icon {
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    border: 1px solid rgba(255,255,255,0.2);
                }
                .chevron-down {
                    width: 10px;
                    height: 10px;
                    fill: currentColor;
                }

                .cart-wrapper {
                    position: relative;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    opacity: 0.9;
                    transition: opacity 0.2s, transform 0.2s;
                }
                .cart-wrapper:hover {
                    opacity: 1;
                    transform: scale(1.05);
                }
                .cart-wrapper svg {
                    width: 22px;
                    height: 22px;
                    fill: currentColor;
                }
                .cart-badge {
                    position: absolute;
                    top: -6px;
                    right: -8px;
                    background: #ff4757;
                    color: white;
                    font-size: 10px;
                    font-weight: 800;
                    height: 16px;
                    min-width: 16px;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 0 4px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                }

                .btn-signin {
                    background: var(--text-light);
                    color: var(--color-gradient-start);
                    border: none;
                    padding: 10px 24px;
                    border-radius: 20px;
                    font-weight: 700;
                    font-size: 14px;
                    cursor: pointer;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                    transition: transform 0.2s, box-shadow 0.2s;
                }
                .btn-signin:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 6px 15px rgba(0,0,0,0.15);
                }

                .mobile-toggle {
                    display: none;
                    background: none;
                    border: none;
                    cursor: pointer;
                    color: var(--text-dark);
                }
                .mobile-toggle svg {
                    width: 28px;
                    height: 28px;
                    stroke: currentColor;
                    stroke-width: 2;
                    stroke-linecap: round;
                }

                @media (max-width: 1100px) {
                    .bg-white { width: 50%; }
                    .nav-links { display: none; }
                    .mobile-toggle { display: block; }
                }

                @media (max-width: 768px) {
                    .bg-colored { display: none; }
                    .bg-white { width: 100%; clip-path: none; }
                    .header-container { padding: 0 15px; }

                    .logo img { height: 46px; }

                    .left-section { gap: 1rem; }
                    .right-section { gap: 0.75rem; color: var(--color-gradient-start); }

                    .phone-number { display: none; }
                    .lang-selector .flag-icon { border-color: rgba(0,0,0,0.1); }

                    .btn-signin {
                        background: var(--color-gradient-start);
                        color: white;
                        padding: 6px 12px;
                        font-size: 13px;
                    }
                }

                .mobile-drawer {
                    position: fixed;
                    top: 0; left: -100%;
                    width: 80%; max-width: 320px; height: 100vh;
                    background: white;
                    z-index: 2000;
                    box-shadow: 5px 0 20px rgba(0,0,0,0.1);
                    transition: left 0.3s ease;
                    padding: 2rem;
                    display: flex; flex-direction: column; gap: 2rem;
                }
                .mobile-drawer.open { left: 0; }
                .overlay {
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(0,0,0,0.5); z-index: 1999;
                    opacity: 0; pointer-events: none; transition: opacity 0.3s;
                }
                .overlay.open { opacity: 1; pointer-events: auto; }
                .close-drawer { align-self: flex-end; background: none; border: none; cursor: pointer; }
                .close-drawer svg { width: 24px; height: 24px; }
            </style>

            <div class="header-container">
                <div class="bg-colored"></div>
                <div class="bg-white"></div>
                <div class="content-wrapper">
                    <div class="left-section">
                        <button class="mobile-toggle" aria-label="Menu">
                            <svg viewBox="0 0 24 24"><path d="M3 12h18M3 6h18M3 18h18"></path></svg>
                        </button>
                        <a href="#" class="logo">
                            <img src="logo/logo-header-400.webp" alt="Aml Store Logo">
                        </a>
                        <nav class="nav-links">
                            <a href="#" class="active">Home</a>
                            <a href="#">Sistemi Operativi</a>
                            <a href="#">Office</a>
                            <a href="#">Antivirus</a>
                        </nav>
                    </div>
                    <div class="right-section">
                        <div class="phone-number">
                            <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                            ASSISTENZA &nbsp; +39 02 1234 5678
                        </div>
                        <div class="lang-selector">
                            <div class="flag-icon" style="background: url('https://flagcdn.com/w40/it.png') center/cover no-repeat;"></div>
                            IT
                            <svg class="chevron-down" viewBox="0 0 24 24"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>
                        </div>
                        <div class="cart-wrapper">
                            <svg viewBox="0 0 24 24"><path d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z"/></svg>
                            <div class="cart-badge">2</div>
                        </div>
                        <button class="btn-signin">Accedi</button>
                    </div>
                </div>
            </div>

            <div class="overlay"></div>
            <div class="mobile-drawer">
                <button class="close-drawer"><svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg></button>
                <nav style="display:flex; flex-direction:column; gap:1.5rem; font-weight:700;">
                    <a href="#" style="color:#333; text-decoration:none;">Home</a>
                    <a href="#" style="color:#333; text-decoration:none;">Sistemi Operativi</a>
                    <a href="#" style="color:#333; text-decoration:none;">Office</a>
                    <a href="#" style="color:#333; text-decoration:none;">Antivirus</a>
                </nav>
                <div style="margin-top:auto; font-size:14px; color:#666;">
                    Assistenza: +39 02 1234 5678
                </div>
            </div>
        `;
    }

    connectedCallback() {
        const toggle = this.shadowRoot.querySelector('.mobile-toggle');
        const close = this.shadowRoot.querySelector('.close-drawer');
        const overlay = this.shadowRoot.querySelector('.overlay');
        const drawer = this.shadowRoot.querySelector('.mobile-drawer');

        const openMenu = () => {
            drawer.classList.add('open');
            overlay.classList.add('open');
        };

        const closeMenu = () => {
            drawer.classList.remove('open');
            overlay.classList.remove('open');
        };

        if (toggle) toggle.addEventListener('click', openMenu);
        if (close) close.addEventListener('click', closeMenu);
        if (overlay) overlay.addEventListener('click', closeMenu);
    }
}

if (!customElements.get('ecommerce-header')) {
    customElements.define('ecommerce-header', EcommerceHeader);
}
