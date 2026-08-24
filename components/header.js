(function () {
    'use strict';

    /* Cache indice ricerca per lingua, condivisa tra eventuali piu' istanze dell'header. */
    const SEARCH_INDEX_CACHE = {};

    /* Range combining diacritical marks (U+0300-U+036F) costruito da codepoint
       per evitare di incorporare caratteri Unicode non stampabili nel sorgente. */
    const DIACRITICS_RE = new RegExp(
        '[' + String.fromCharCode(0x0300) + '-' + String.fromCharCode(0x036f) + ']', 'g'
    );

    function stripDiacritics(str) {
        return String(str || '').normalize('NFD').replace(DIACRITICS_RE, '');
    }

    function normalizeSearchText(str) {
        return stripDiacritics(str).toLowerCase().trim();
    }

    function rankSearchResults(entries, query) {
        const q = normalizeSearchText(query);
        if (!q) return [];
        const scored = [];
        entries.forEach((entry, idx) => {
            const name = normalizeSearchText(entry.name);
            const category = normalizeSearchText(entry.category);
            let tier = -1;
            if (name.indexOf(q) === 0) tier = 3;
            else if (name.indexOf(q) !== -1) tier = 2;
            else if (category.indexOf(q) !== -1) tier = 1;
            if (tier >= 0) scored.push({ entry, tier, idx });
        });
        scored.sort((a, b) => (b.tier - a.tier) || (a.idx - b.idx));
        return scored.slice(0, 8).map((s) => s.entry);
    }

    /* Stringhe usate dal comportamento dell'header: etichetta accessibile del
       carrello e messaggi della ricerca. Tutte le altre servivano a costruire il
       markup, che ora e' pre-renderizzato nelle pagine: vivono in
       scripts/chrome-renderer/header.js. */
    const HEADER_I18N = {
        it: {
            cartAriaEmpty: 'Carrello, nessun articolo',
            cartAriaOne: 'Carrello, 1 articolo',
            cartAriaMany: 'Carrello, {{n}} articoli',
            searchHint: 'Inizia a digitare per cercare',
            searchNoResults: 'Nessun risultato per "{{q}}"',
            supportChat: 'Chat con assistenza',
        },
        en: {
            cartAriaEmpty: 'Shopping cart, empty',
            cartAriaOne: 'Shopping cart, 1 item',
            cartAriaMany: 'Shopping cart, {{n}} items',
            searchHint: 'Start typing to search',
            searchNoResults: 'No results for "{{q}}"',
            supportChat: 'Chat with support',
        },
        fr: {
            cartAriaEmpty: 'Panier vide',
            cartAriaOne: 'Panier, 1 article',
            cartAriaMany: 'Panier, {{n}} articles',
            searchHint: 'Commencez à taper pour rechercher',
            searchNoResults: 'Aucun résultat pour « {{q}} »',
            supportChat: 'Chat avec le support',
        },
        de: {
            cartAriaEmpty: 'Warenkorb leer',
            cartAriaOne: 'Warenkorb, 1 Artikel',
            cartAriaMany: 'Warenkorb, {{n}} Artikel',
            searchHint: 'Tippen Sie, um zu suchen',
            searchNoResults: 'Keine Ergebnisse für „{{q}}"',
            supportChat: 'Support-Chat',
        },
        es: {
            cartAriaEmpty: 'Carrito vacío',
            cartAriaOne: 'Carrito, 1 artículo',
            cartAriaMany: 'Carrito, {{n}} artículos',
            searchHint: 'Empieza a escribir para buscar',
            searchNoResults: 'Sin resultados para "{{q}}"',
            supportChat: 'Chat con soporte',
        },
        pt: {
            cartAriaEmpty: 'Carrinho vazio',
            cartAriaOne: 'Carrinho, 1 artigo',
            cartAriaMany: 'Carrinho, {{n}} artigos',
            searchHint: 'Comece a escrever para pesquisar',
            searchNoResults: 'Sem resultados para "{{q}}"',
        },
        nl: {
            cartAriaEmpty: 'Winkelwagen leeg',
            cartAriaOne: 'Winkelwagen, 1 artikel',
            cartAriaMany: 'Winkelwagen, {{n}} artikelen',
            searchHint: 'Begin met typen om te zoeken',
            searchNoResults: 'Geen resultaten voor "{{q}}"',
        },
    };

    const SUPPORT_EMAIL = 'info@amlstore.it';
    const SUPPORT_WHATSAPP_URL = 'https://wa.me/393925580413';

    let supportChatRequested = false;

    function mountSupportChat() {
        if (document.querySelector('support-chat')) return;
        const mount = () => {
            if (document.querySelector('support-chat')) return;
            document.body.appendChild(document.createElement('support-chat'));
        };
        if (customElements.get('support-chat')) { mount(); return; }
        let script = document.querySelector('script[data-aml-support-chat]');
        if (!script) {
            script = document.createElement('script');
            script.src = '/components/support-chat.js?v=f5e1c83069';
            script.defer = true;
            script.dataset.amlSupportChat = '';
            document.head.appendChild(script);
        }
        script.addEventListener('load', mount, { once: true });
    }

    function ensureSupportChat() {
        if (supportChatRequested) return;
        supportChatRequested = true;
        /* Il pulsante deve comparire solo quando il backend e' davvero attivo:
           senza questo controllo il widget si iniettava su ogni pagina anche a
           CHAT_ENABLED=0, mostrando a tutti i visitatori un pulsante "Chat"
           permanentemente inerte. L'endpoint non richiede sessione ed e' lo
           stesso che il widget interroga per lo stato pubblico (ADR §45). */
        fetch('/api/chat/availability', { credentials: 'same-origin' })
            .then((response) => (response.ok ? response.json() : null))
            .then((data) => {
                if (data && data.enabled) mountSupportChat();
            })
            .catch(() => { /* rete assente o endpoint irraggiungibile: nessun widget, fail closed */ });
    }


    class EcommerceHeader extends HTMLElement {
        constructor() {
            super();
        }

        connectedCallback() {
            ensureSupportChat();
            /* locale-path.js e il markup pre-renderizzato possono arrivare dopo
               l'upgrade del custom element: si riprova per ~2s, poi si smette
               segnalando la causa invece di lasciare un timer che gira a vuoto. */
            let attemptsLeft = 40;
            const initHeader = () => {
                if (this.__headerUiInit) return;
                const S = window.AmlSite;
                const hasMarkup = Boolean(this.querySelector('.header-container'));
                if (!S || !hasMarkup) {
                    if (attemptsLeft-- <= 0) {
                        if (!S) {
                            console.error('ecommerce-header: includere ../js/locale-path.js prima di questo script.');
                        }
                        if (!hasMarkup) {
                            console.error(
                                'ecommerce-header: markup assente nella pagina. ' +
                                'Rigenerarlo con: node scripts/build-inline-chrome.mjs'
                            );
                        }
                        return;
                    }
                    if (document.readyState === 'loading') {
                        document.addEventListener('DOMContentLoaded', () => initHeader(), { once: true });
                    } else {
                        setTimeout(() => initHeader(), 50);
                    }
                    return;
                }
                this.__headerUiInit = true;

                this.setAttribute('translate', 'no');
                this.classList.add('notranslate');

                const parsed = S.parseLocalePath(window.location.pathname);
                const activeLang = parsed.activeLang;
                const t = HEADER_I18N[activeLang.code] || HEADER_I18N.it;
                const staticRoot = S.staticRootFromScriptPath('/components/header.js');

                const cartAriaForCount = (n) => {
                    const c = Number(n) || 0;
                    if (c <= 0) return t.cartAriaEmpty;
                    if (c === 1) return t.cartAriaOne;
                    return String(t.cartAriaMany).replace('{{n}}', String(c));
                };


            const toggle = this.querySelector('.mobile-toggle');
            const close = this.querySelector('.close-drawer');
            const overlay = this.querySelector('.overlay');
            const drawer = this.querySelector('.mobile-drawer');
            const langWrapper = this.querySelector('.lang-wrapper');
            const langSelector = this.querySelector('.lang-selector');
            const supportWrap = this.querySelector('.support-wrap');
            const supportTrigger = this.querySelector('.support-trigger');
                const supportPanel = this.querySelector('#header-support-panel');

            const addChatEntry = (container, className, before) => {
                if (!container || container.querySelector('[data-open-support-chat]')) return;
                const link = document.createElement('a');
                link.href = '#support-chat';
                link.className = className;
                link.dataset.openSupportChat = '';
                link.textContent = t.supportChat;
                link.addEventListener('click', (event) => {
                    event.preventDefault();
                    window.dispatchEvent(new Event('aml-support-open'));
                    closeSupport({ restoreFocus: false });
                    closeMenu();
                });
                container.insertBefore(link, before || null);
            };
            addChatEntry(supportPanel, 'support-panel__link', supportPanel?.querySelector('.support-panel__hours'));
            const drawerSupport = this.querySelector('.drawer-support-title')?.parentElement;
            addChatEntry(drawerSupport, 'drawer-support-link', drawerSupport?.querySelector('.drawer-support-hours'));

            const isSupportOpen = () => Boolean(supportWrap && supportWrap.classList.contains('open'));

            const closeSupport = ({ restoreFocus = false } = {}) => {
                if (!supportWrap || !supportTrigger || !supportPanel) return;
                supportWrap.classList.remove('open');
                supportPanel.hidden = true;
                supportTrigger.setAttribute('aria-expanded', 'false');
                if (restoreFocus) supportTrigger.focus();
            };

            const openSupport = () => {
                if (!supportWrap || !supportTrigger || !supportPanel) return;
                closeNavSubmenus();
                if (langWrapper) {
                    langWrapper.classList.remove('open');
                    if (langSelector) langSelector.setAttribute('aria-expanded', 'false');
                }
                closeSearch({ returnFocus: false });
                closeMenu();
                supportPanel.hidden = false;
                supportWrap.classList.add('open');
                supportTrigger.setAttribute('aria-expanded', 'true');
            };

            const openMenu = () => {
                closeSupport({ restoreFocus: false });
                if (langWrapper) {
                    langWrapper.classList.remove('open');
                    if (langSelector) langSelector.setAttribute('aria-expanded', 'false');
                }
                closeSearch({ returnFocus: false });
                closeNavSubmenus();
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

            const closeNavSubmenus = () => {
                [
                    ['.nav-win-wrap', '.nav-win-caret'],
                    ['.nav-office-wrap', '.nav-office-caret'],
                    ['.nav-m365-wrap', '.nav-m365-caret'],
                    ['.nav-av-wrap', '.nav-av-caret'],
                ].forEach(([wrapSel, caretSel]) => {
                    const wrap = this.querySelector(wrapSel);
                    const caret = this.querySelector(caretSel);
                    if (wrap) wrap.classList.remove('open');
                    if (caret) caret.setAttribute('aria-expanded', 'false');
                });
            };

            /* ── Ricerca prodotti ── */
            const searchToggle = this.querySelector('.search-toggle');
            const searchBackdrop = this.querySelector('.search-backdrop');
            const searchPanel = this.querySelector('.search-panel');
            const searchInput = this.querySelector('.search-input');
            const searchClose = this.querySelector('.search-close');
            const searchResultsEl = this.querySelector('.search-results');
            const searchLang = activeLang.code;
            const searchPathPrefix = parsed.pathPrefix;
            let searchDebounceTimer = null;

            const isSearchOpen = () => Boolean(searchPanel && searchPanel.classList.contains('open'));

            const renderSearchResults = (entries, query) => {
                if (!searchResultsEl) return;
                searchResultsEl.textContent = '';
                if (!query) {
                    const hint = document.createElement('p');
                    hint.className = 'search-hint';
                    hint.textContent = t.searchHint;
                    searchResultsEl.appendChild(hint);
                    return;
                }
                if (!entries.length) {
                    const empty = document.createElement('p');
                    empty.className = 'search-empty';
                    empty.textContent = t.searchNoResults.replace('{{q}}', query);
                    searchResultsEl.appendChild(empty);
                    return;
                }
                entries.forEach((entry) => {
                    const a = document.createElement('a');
                    a.className = 'search-result';
                    a.href = S.localePageUrl(searchPathPrefix, searchLang, entry.slug);

                    const thumb = document.createElement('img');
                    thumb.className = 'search-result-thumb';
                    thumb.src = `${staticRoot}${entry.image}`;
                    thumb.alt = '';
                    thumb.loading = 'lazy';
                    thumb.decoding = 'async';
                    a.appendChild(thumb);

                    const info = document.createElement('div');
                    info.className = 'search-result-info';
                    const name = document.createElement('div');
                    name.className = 'search-result-name';
                    name.textContent = entry.name;
                    const category = document.createElement('div');
                    category.className = 'search-result-category';
                    category.textContent = entry.category;
                    info.appendChild(name);
                    info.appendChild(category);
                    a.appendChild(info);

                    const price = document.createElement('span');
                    price.className = 'search-result-price';
                    price.textContent = (window.AmlCart && window.AmlCart.formatMoney)
                        ? window.AmlCart.formatMoney(entry.priceMinor, entry.currency)
                        : '';
                    a.appendChild(price);

                    searchResultsEl.appendChild(a);
                });
            };

            const runSearch = (query) => {
                const cached = SEARCH_INDEX_CACHE[searchLang];
                if (!cached) return;
                renderSearchResults(rankSearchResults(cached, query), query.trim());
            };

            const ensureSearchIndexLoaded = () => {
                if (SEARCH_INDEX_CACHE[searchLang]) return Promise.resolve(SEARCH_INDEX_CACHE[searchLang]);
                return fetch(`${staticRoot}/asset/search-index/${searchLang}.json`)
                    .then((res) => { if (!res.ok) throw new Error('HTTP ' + res.status); return res.json(); })
                    .then((data) => {
                        SEARCH_INDEX_CACHE[searchLang] = Array.isArray(data) ? data : [];
                        return SEARCH_INDEX_CACHE[searchLang];
                    })
                    .catch(() => { SEARCH_INDEX_CACHE[searchLang] = []; return []; });
            };

            const openSearch = () => {
                if (!searchPanel || !searchBackdrop) return;
                closeNavSubmenus();
                closeSupport({ restoreFocus: false });
                if (langWrapper) {
                    langWrapper.classList.remove('open');
                    if (langSelector) langSelector.setAttribute('aria-expanded', 'false');
                }
                closeMenu();
                searchPanel.classList.add('open');
                searchBackdrop.classList.add('open');
                if (searchToggle) searchToggle.setAttribute('aria-expanded', 'true');
                renderSearchResults([], '');
                ensureSearchIndexLoaded().then(() => {
                    if (searchInput && searchInput.value.trim()) runSearch(searchInput.value);
                });
                if (searchInput) setTimeout(() => searchInput.focus(), 0);
            };

            const closeSearch = ({ returnFocus = true } = {}) => {
                if (!searchPanel || !searchBackdrop) return;
                searchPanel.classList.remove('open');
                searchBackdrop.classList.remove('open');
                if (searchToggle) {
                    searchToggle.setAttribute('aria-expanded', 'false');
                    if (returnFocus) searchToggle.focus();
                }
            };

            if (supportTrigger) {
                supportTrigger.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    if (isSupportOpen()) closeSupport({ restoreFocus: false });
                    else openSupport();
                });
            }

            if (searchToggle) {
                searchToggle.addEventListener('click', (e) => {
                    e.stopPropagation();
                    if (isSearchOpen()) closeSearch();
                    else openSearch();
                });
            }
            if (searchClose) searchClose.addEventListener('click', () => closeSearch());
            if (searchBackdrop) searchBackdrop.addEventListener('click', () => closeSearch({ returnFocus: false }));
            if (searchInput) {
                searchInput.addEventListener('input', () => {
                    clearTimeout(searchDebounceTimer);
                    const value = searchInput.value;
                    searchDebounceTimer = setTimeout(() => runSearch(value), 150);
                });
                searchInput.addEventListener('keydown', (e) => {
                    if (e.key === 'ArrowDown') {
                        e.preventDefault();
                        const first = searchResultsEl && searchResultsEl.querySelector('.search-result');
                        if (first) first.focus();
                    }
                });
            }
            if (searchResultsEl) {
                searchResultsEl.addEventListener('keydown', (e) => {
                    if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
                    const items = Array.from(searchResultsEl.querySelectorAll('.search-result'));
                    const active = this.activeElement;
                    const idx = items.indexOf(active);
                    if (idx === -1) return;
                    e.preventDefault();
                    if (e.key === 'ArrowDown') {
                        (items[idx + 1] || items[idx]).focus();
                    } else if (idx === 0) {
                        if (searchInput) searchInput.focus();
                    } else {
                        items[idx - 1].focus();
                    }
                });
            }

            const langDropdown = this.querySelector('#header-lang-dropdown') || this.querySelector('.lang-dropdown');

            const closeLangMenu = ({ restoreFocus = false } = {}) => {
                if (!langWrapper || !langSelector) return;
                langWrapper.classList.remove('open');
                langSelector.setAttribute('aria-expanded', 'false');
                if (restoreFocus) langSelector.focus();
            };

            const openLangMenu = () => {
                if (!langWrapper || !langSelector) return;
                closeNavSubmenus();
                closeSupport({ restoreFocus: false });
                closeSearch({ returnFocus: false });
                langWrapper.classList.add('open');
                langSelector.setAttribute('aria-expanded', 'true');
            };

            const toggleLangMenu = (e) => {
                if (e) e.stopPropagation();
                if (!langWrapper || !langSelector) return;
                if (langWrapper.classList.contains('open')) {
                    closeLangMenu();
                } else {
                    openLangMenu();
                }
            };

            if (langSelector && langWrapper) {
                langSelector.addEventListener('click', (e) => {
                    e.stopPropagation();
                    toggleLangMenu(e);
                });
                langSelector.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowDown') {
                        e.preventDefault();
                        e.stopPropagation();
                        if (!langWrapper.classList.contains('open')) {
                            openLangMenu();
                        }
                        const target = langDropdown?.querySelector('.lang-option.active') || langDropdown?.querySelector('.lang-option');
                        if (target) target.focus();
                    }
                });
            }

            if (langDropdown) {
                langDropdown.addEventListener('keydown', (e) => {
                    const options = Array.from(langDropdown.querySelectorAll('.lang-option'));
                    const activeIdx = options.indexOf(document.activeElement);
                    if (activeIdx === -1) return;

                    if (e.key === 'ArrowDown') {
                        e.preventDefault();
                        const next = options[activeIdx + 1] || options[0];
                        next.focus();
                    } else if (e.key === 'ArrowUp') {
                        e.preventDefault();
                        if (activeIdx === 0) {
                            closeLangMenu({ restoreFocus: true });
                        } else {
                            const prev = options[activeIdx - 1];
                            prev.focus();
                        }
                    } else if (e.key === 'Escape') {
                        e.preventDefault();
                        closeLangMenu({ restoreFocus: true });
                    }
                });
            }

            /* Compact header: isteresi scrollY > 16 / < 4 */
            let compact = false;
            let compactTicking = false;
            const updateCompactState = () => {
                const y = window.scrollY || window.pageYOffset || 0;
                if (!compact && y > 16) {
                    compact = true;
                    this.classList.add('is-compact');
                    closeSupport({ restoreFocus: false });
                } else if (compact && y < 4) {
                    compact = false;
                    this.classList.remove('is-compact');
                }
                compactTicking = false;
            };
            const onCompactScroll = () => {
                if (compactTicking) return;
                compactTicking = true;
                requestAnimationFrame(updateCompactState);
            };
            updateCompactState();
            window.addEventListener('scroll', onCompactScroll, { passive: true });
            this.__compactScrollHandler = onCompactScroll;

            const publishHeaderOffset = () => {
                const h = Math.ceil(this.getBoundingClientRect().height || this.offsetHeight || 64);
                document.documentElement.style.setProperty('--aml-header-offset', h + 'px');
            };
            publishHeaderOffset();
            if (typeof ResizeObserver !== 'undefined') {
                this.__headerResizeObserver = new ResizeObserver((entries) => {
                    const entry = entries && entries[0];
                    let height = 0;
                    if (entry && entry.borderBoxSize && entry.borderBoxSize[0]) {
                        height = entry.borderBoxSize[0].blockSize;
                    } else if (entry) {
                        height = entry.contentRect.height;
                    }
                    const px = Math.ceil(height || this.getBoundingClientRect().height || 64);
                    document.documentElement.style.setProperty('--aml-header-offset', px + 'px');
                });
                this.__headerResizeObserver.observe(this);
            } else {
                window.addEventListener('resize', publishHeaderOffset, { passive: true });
                this.__headerResizeFallback = publishHeaderOffset;
            }

            /* ── Windows dropdown ── */
            const winWrap = this.querySelector('.nav-win-wrap');
            const winCaret = this.querySelector('.nav-win-caret');
            const closeWinMenu = () => {
                if (!winWrap || !winCaret) return;
                winWrap.classList.remove('open');
                winCaret.setAttribute('aria-expanded', 'false');
            };
            if (winCaret && winWrap) {
                winCaret.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    if (langWrapper) {
                        langWrapper.classList.remove('open');
                        if (langSelector) langSelector.setAttribute('aria-expanded', 'false');
                    }
                    closeSupport({ restoreFocus: false });
                    closeNavSubmenus();
                    const isOpen = winWrap.classList.toggle('open');
                    winCaret.setAttribute('aria-expanded', isOpen);
                });
                this.querySelectorAll('.nav-win-dropdown a').forEach((a) => {
                    a.addEventListener('click', closeWinMenu);
                });
            }

            /* ── Office dropdown ── */
            const officeWrap = this.querySelector('.nav-office-wrap');
            const officeCaret = this.querySelector('.nav-office-caret');
            const closeOfficeMenu = () => {
                if (!officeWrap || !officeCaret) return;
                officeWrap.classList.remove('open');
                officeCaret.setAttribute('aria-expanded', 'false');
            };
            if (officeCaret && officeWrap) {
                officeCaret.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    if (langWrapper) {
                        langWrapper.classList.remove('open');
                        if (langSelector) langSelector.setAttribute('aria-expanded', 'false');
                    }
                    closeSupport({ restoreFocus: false });
                    closeNavSubmenus();
                    const isOpen = officeWrap.classList.toggle('open');
                    officeCaret.setAttribute('aria-expanded', isOpen);
                });
                this.querySelectorAll('.nav-office-dropdown a').forEach((a) => {
                    a.addEventListener('click', closeOfficeMenu);
                });
            }

            /* ── Antivirus dropdown ── */
            const avWrap = this.querySelector('.nav-av-wrap');
            const avCaret = this.querySelector('.nav-av-caret');
            const closeAvMenu = () => {
                if (!avWrap || !avCaret) return;
                avWrap.classList.remove('open');
                avCaret.setAttribute('aria-expanded', 'false');
            };
            if (avCaret && avWrap) {
                avCaret.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    if (langWrapper) {
                        langWrapper.classList.remove('open');
                        if (langSelector) langSelector.setAttribute('aria-expanded', 'false');
                    }
                    closeSupport({ restoreFocus: false });
                    closeNavSubmenus();
                    const isOpen = avWrap.classList.toggle('open');
                    avCaret.setAttribute('aria-expanded', isOpen);
                });
                this.querySelectorAll('.nav-av-dropdown a').forEach((a) => {
                    a.addEventListener('click', closeAvMenu);
                });
            }

            /* ── Microsoft 365 dropdown ── */
            const m365Wrap = this.querySelector('.nav-m365-wrap');
            const m365Caret = this.querySelector('.nav-m365-caret');
            const closeM365Menu = () => {
                if (!m365Wrap || !m365Caret) return;
                m365Wrap.classList.remove('open');
                m365Caret.setAttribute('aria-expanded', 'false');
            };
            if (m365Caret && m365Wrap) {
                m365Caret.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    if (langWrapper) {
                        langWrapper.classList.remove('open');
                        if (langSelector) langSelector.setAttribute('aria-expanded', 'false');
                    }
                    closeSupport({ restoreFocus: false });
                    closeNavSubmenus();
                    const isOpen = m365Wrap.classList.toggle('open');
                    m365Caret.setAttribute('aria-expanded', isOpen);
                });
                this.querySelectorAll('.nav-m365-dropdown a').forEach((a) => {
                    a.addEventListener('click', closeM365Menu);
                });
            }

            /* ── Hover-intent: apertura al passaggio e tolleranza di uscita per
                  tutti i menu desktop (stessa esperienza del menu Microsoft 365).
                  Solo su dispositivi con hover reale: sul touch resta il caret. ── */
            if (window.matchMedia && window.matchMedia('(hover: hover)').matches) {
                const hoverMenus = [
                    [winWrap, winCaret],
                    [officeWrap, officeCaret],
                    [m365Wrap, m365Caret],
                    [avWrap, avCaret],
                ].filter(([w, c]) => w && c);
                let hoverCloseTimer = null;
                hoverMenus.forEach(([wrap, caret]) => {
                    wrap.addEventListener('mouseenter', () => {
                        clearTimeout(hoverCloseTimer);
                        closeSupport({ restoreFocus: false });
                        hoverMenus.forEach(([w2, c2]) => {
                            if (w2 !== wrap && w2.classList.contains('open')) {
                                w2.classList.remove('open');
                                c2.setAttribute('aria-expanded', 'false');
                            }
                        });
                        wrap.classList.add('open');
                        caret.setAttribute('aria-expanded', 'true');
                    });
                    wrap.addEventListener('mouseleave', () => {
                        clearTimeout(hoverCloseTimer);
                        hoverCloseTimer = setTimeout(() => {
                            wrap.classList.remove('open');
                            caret.setAttribute('aria-expanded', 'false');
                        }, 300);
                    });
                });
            }

            this.__docClickHandler = (e) => {
                const path = typeof e.composedPath === 'function' ? e.composedPath() : [];
                if (isSupportOpen()
                    && supportWrap
                    && !path.includes(supportWrap)) {
                    closeSupport({ restoreFocus: false });
                }
                if (searchPanel && searchToggle && isSearchOpen()
                    && !path.includes(searchPanel) && !path.includes(searchToggle)) {
                    closeSearch({ returnFocus: false });
                }
                if (langWrapper && langSelector && !path.includes(langWrapper)) {
                    langWrapper.classList.remove('open');
                    langSelector.setAttribute('aria-expanded', 'false');
                }
                [
                    ['.nav-win-wrap', '.nav-win-caret'],
                    ['.nav-office-wrap', '.nav-office-caret'],
                    ['.nav-m365-wrap', '.nav-m365-caret'],
                    ['.nav-av-wrap', '.nav-av-caret'],
                ].forEach(([wrapSel, caretSel]) => {
                    const wrap = this.querySelector(wrapSel);
                    const caret = this.querySelector(caretSel);
                    if (wrap && !path.includes(wrap)) {
                        wrap.classList.remove('open');
                        if (caret) caret.setAttribute('aria-expanded', 'false');
                    }
                });
            };
            this.__docKeydownHandler = (e) => {
                if (e.key !== 'Escape') return;
                if (isSearchOpen()) {
                    closeSearch();
                    return;
                }
                if (isSupportOpen()) {
                    closeSupport({ restoreFocus: true });
                    return;
                }
                if (langWrapper?.classList.contains('open')) {
                    langWrapper.classList.remove('open');
                    if (langSelector) {
                        langSelector.setAttribute('aria-expanded', 'false');
                        langSelector.focus();
                    }
                    return;
                }
                const submenus = [
                    ['.nav-win-wrap', '.nav-win-caret'],
                    ['.nav-office-wrap', '.nav-office-caret'],
                    ['.nav-m365-wrap', '.nav-m365-caret'],
                    ['.nav-av-wrap', '.nav-av-caret'],
                ];
                for (const [wrapSel, caretSel] of submenus) {
                    const wrap = this.querySelector(wrapSel);
                    const caret = this.querySelector(caretSel);
                    if (wrap?.classList.contains('open')) {
                        wrap.classList.remove('open');
                        if (caret) { caret.setAttribute('aria-expanded', 'false'); caret.focus(); }
                        return;
                    }
                }
                if (drawer?.classList.contains('open')) {
                    closeMenu();
                }
            };
            document.addEventListener('click', this.__docClickHandler);
            document.addEventListener('keydown', this.__docKeydownHandler);

            const cartLink = this.querySelector('a.cart-wrapper');
            const cartBadge = this.querySelector('.cart-badge');
            let prevCartQty = null;
            let cartBadgePopTimer = null;
            let cartIconNudgeTimer = null;
            const syncCartChrome = () => {
                const count =
                    window.AmlCart && typeof window.AmlCart.totalQty === 'function' ? window.AmlCart.totalQty() : 0;
                const increased = prevCartQty !== null && count > prevCartQty;

                if (cartBadge) {
                    cartBadge.textContent = count > 99 ? '99+' : String(count);
                    cartBadge.classList.toggle('is-visible', count > 0);
                    if (increased && count > 0) {
                        cartBadge.classList.remove('cart-badge-pop');
                        void cartBadge.offsetWidth;
                        cartBadge.classList.add('cart-badge-pop');
                        clearTimeout(cartBadgePopTimer);
                        cartBadgePopTimer = setTimeout(function () {
                            cartBadge.classList.remove('cart-badge-pop');
                        }, 600);
                    }
                }
                if (cartLink) {
                    cartLink.setAttribute('aria-label', cartAriaForCount(count));
                    if (increased) {
                        cartLink.classList.remove('cart-nudge');
                        void cartLink.offsetWidth;
                        cartLink.classList.add('cart-nudge');
                        clearTimeout(cartIconNudgeTimer);
                        cartIconNudgeTimer = setTimeout(function () {
                            cartLink.classList.remove('cart-nudge');
                        }, 650);
                    }
                }
                prevCartQty = count;
            };
            syncCartChrome();
            this.__syncCartChrome = syncCartChrome;
            document.addEventListener('aml-cart-changed', syncCartChrome);
            };

            initHeader();
        }

        disconnectedCallback() {
            if (typeof this.__docClickHandler === 'function') {
                document.removeEventListener('click', this.__docClickHandler);
                this.__docClickHandler = null;
            }
            if (typeof this.__docKeydownHandler === 'function') {
                document.removeEventListener('keydown', this.__docKeydownHandler);
                this.__docKeydownHandler = null;
            }
            if (typeof this.__syncCartChrome === 'function') {
                document.removeEventListener('aml-cart-changed', this.__syncCartChrome);
                this.__syncCartChrome = null;
            }
            if (typeof this.__compactScrollHandler === 'function') {
                window.removeEventListener('scroll', this.__compactScrollHandler);
                this.__compactScrollHandler = null;
            }
            if (this.__headerResizeObserver) {
                this.__headerResizeObserver.disconnect();
                this.__headerResizeObserver = null;
            }
            if (typeof this.__headerResizeFallback === 'function') {
                window.removeEventListener('resize', this.__headerResizeFallback);
                this.__headerResizeFallback = null;
            }
        }
    }

    if (!customElements.get('ecommerce-header')) {
        customElements.define('ecommerce-header', EcommerceHeader);
    }
})();
