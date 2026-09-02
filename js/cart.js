/**
 * Carrello minimale (localStorage) + evento aml-cart-changed.
 * Pulsanti fuori dalla card: data-cart-source="id" punta a #id di .product-card o .pricing-card.
 */
(function (global) {
    'use strict';

    const STORAGE_KEY = 'aml-cart-v1';
    const EVT = 'aml-cart-changed';
    var flashAddedTimer = null;
    var liveRegionClearTimer = null;

    /* ─── Tracking carrello (analytics) — id ciclo di vita + sync server ─────────── */

    const CART_SESSION_KEY = 'aml-cart-id-v1';
    const CONSENT_KEY = 'aml-consent-v2';
    const CART_SYNC_URL = '/api/cart/sync';
    const CART_SYNC_DEBOUNCE_MS = 1500;
    var cartSyncTimer = null;

    const TRACK_URL = '/api/track';

    /** Evento CRO fire-and-forget (vedi TRACKABLE_EVENTS in functions/api/_lib/analytics.js). */
    function trackEvent(eventName, extra) {
        try {
            fetch(TRACK_URL, {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                keepalive: true,
                body: JSON.stringify(Object.assign({ event: eventName }, extra || {})),
            }).catch(() => {});
        } catch (_) { /* fetch non disponibile */ }
    }

    /* ─── Storage ──────────────────────────────────────────────────────────────── */

    function readLines() {
        try {
            const raw = global.localStorage.getItem(STORAGE_KEY);
            if (!raw) return [];
            const parsed = JSON.parse(raw);
            if (!Array.isArray(parsed)) {
                // Dato corrotto: ripulisce storage e riparte da zero
                try { global.localStorage.removeItem(STORAGE_KEY); } catch (_) {}
                return [];
            }
            return parsed;
        } catch (_) {
            // JSON.parse fallito: storage corrotto, ripulisce
            try { global.localStorage.removeItem(STORAGE_KEY); } catch (__) {}
            return [];
        }
    }

    function writeLines(lines) {
        try {
            global.localStorage.setItem(STORAGE_KEY, JSON.stringify(lines));
            return true;
        } catch (e) {
            // QuotaExceededError o accesso negato (es. Safari private)
            if (typeof console !== 'undefined') {
                console.warn('[AmlCart] localStorage write failed:', e && e.name);
            }
            return false;
        }
    }

    /* ─── Calcoli ──────────────────────────────────────────────────────────────── */

    function totalQty(lines) {
        return lines.reduce((acc, l) => acc + (Number(l.quantity) > 0 ? Number(l.quantity) : 0), 0);
    }

    function totalMinor(lines) {
        return lines.reduce((acc, l) => {
            const q = Number(l.quantity) > 0 ? Number(l.quantity) : 0;
            const cents = Number(l.unitAmount);
            if (!Number.isFinite(cents) || !Number.isFinite(q)) return acc;
            return acc + Math.round(cents) * q;
        }, 0);
    }

    /* ─── Evento ───────────────────────────────────────────────────────────────── */

    function dispatch(lines) {
        const items = lines.slice();
        const detail = { items, count: totalQty(items) };
        try {
            document.dispatchEvent(new CustomEvent(EVT, { detail, bubbles: true }));
        } catch (_) { /* SSR / tests */ }
        scheduleSync();
    }

    /* ─── Tracking carrello: consenso, id ciclo di vita, sync debounced ──────────── */
    // Statistica carrelli abbandonati (fase 1). Il carrello locale funziona sempre,
    // a prescindere dal consenso: cambia solo se lo stato viene anche inviato al
    // server. Stesso pattern di lettura consenso di js/trustpilot-widget.js.

    function hasAnalyticsConsent() {
        try {
            const raw = global.localStorage.getItem(CONSENT_KEY);
            if (!raw) return false;
            const parsed = JSON.parse(raw);
            const consent = parsed && parsed.consent;
            return Boolean(consent && consent.analytics_storage === 'granted');
        } catch (_) {
            return false;
        }
    }

    function generateCartId() {
        if (global.crypto && typeof global.crypto.randomUUID === 'function') {
            return global.crypto.randomUUID();
        }
        // Fallback RFC4122 v4 per browser senza crypto.randomUUID.
        const buf = new Uint8Array(16);
        if (global.crypto && global.crypto.getRandomValues) global.crypto.getRandomValues(buf);
        else for (let i = 0; i < 16; i++) buf[i] = Math.floor(Math.random() * 256);
        buf[6] = (buf[6] & 0x0f) | 0x40;
        buf[8] = (buf[8] & 0x3f) | 0x80;
        const hex = Array.prototype.map.call(buf, (b) => b.toString(16).padStart(2, '0')).join('');
        return hex.slice(0, 8) + '-' + hex.slice(8, 12) + '-' + hex.slice(12, 16) + '-'
             + hex.slice(16, 20) + '-' + hex.slice(20);
    }

    function readCartId() {
        try { return global.localStorage.getItem(CART_SESSION_KEY) || null; } catch (_) { return null; }
    }

    /** Crea (lazy) il cartId al primo utilizzo utile; lo persiste per il ciclo di vita corrente del carrello. */
    function ensureCartId() {
        let id = readCartId();
        if (id) return id;
        id = generateCartId();
        try { global.localStorage.setItem(CART_SESSION_KEY, id); } catch (_) { /* storage negato */ }
        return id;
    }

    /** Chiude il ciclo di vita del carrello corrente (es. dopo un acquisto): il prossimo add genera un cartId nuovo. */
    function resetCartSession() {
        try { global.localStorage.removeItem(CART_SESSION_KEY); } catch (_) { /* ignore */ }
    }

    function performSync(extra) {
        if (!hasAnalyticsConsent()) return;

        const lines = readLines();
        const email = extra && extra.email ? String(extra.email).trim().toLowerCase() : '';
        const existingId = readCartId();

        // Niente da registrare: mai toccato il carrello e nessuna email da agganciare adesso.
        if (!existingId && lines.length === 0 && !email) return;

        const cartId = ensureCartId();
        const payload = {
            cartId,
            locale: cartLang(),
            items: lines.map((l) => ({ sku: l.sku, quantity: Number(l.quantity) || 1 })),
        };
        if (email) payload.email = email;

        try {
            fetch(CART_SYNC_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                keepalive: true,
                body: JSON.stringify(payload),
            }).catch(() => {});
        } catch (_) { /* fetch non disponibile (SSR/test) */ }
    }

    // Accumula `extra` tra chiamate ravvicinate (es. dispatch() anonimo subito dopo
    // notifyEmail()): senza merge, l'ultima scheduleSync() prima dello scatto del
    // timer sovrascriverebbe silenziosamente l'email in sospeso.
    var cartSyncPendingExtra = null;

    function scheduleSync(extra) {
        if (extra) cartSyncPendingExtra = Object.assign({}, cartSyncPendingExtra, extra);
        clearTimeout(cartSyncTimer);
        cartSyncTimer = setTimeout(flushCartSync, CART_SYNC_DEBOUNCE_MS);
    }

    /** Esegue subito il sync in sospeso (se presente). Chiamato dal debounce e su pagehide. */
    function flushCartSync() {
        if (cartSyncTimer === null) return;
        clearTimeout(cartSyncTimer);
        cartSyncTimer = null;
        const extra = cartSyncPendingExtra;
        cartSyncPendingExtra = null;
        performSync(extra);
    }

    try {
        global.addEventListener('aml-consent-updated', function () { scheduleSync(); });
        // Se l'utente naviga via prima che scatti il debounce, il timer verrebbe
        // distrutto senza mai inviare nulla: pagehide forza l'invio immediato
        // (fetch keepalive:true sopravvive comunque alla navigazione).
        global.addEventListener('pagehide', flushCartSync);
    } catch (_) { /* SSR / test */ }

    /* ─── Helpers lettura dati da DOM ──────────────────────────────────────────── */

    function normalizeSku(el) {
        if (!el) return '';
        const ds = el.dataset || {};
        return String(ds.stripeProductSku || el.getAttribute('data-stripe-product-sku') || '').trim();
    }

    /** Segnale UI: richiede indirizzo di spedizione (server rivalida via catalogo). */
    function isPhysical(el) {
        if (!el) return false;
        const ds = el.dataset || {};
        return (ds.physical || el.getAttribute('data-physical') || '') === 'true';
    }

    /**
     * Converte uno SKU tipo slug (microsoft-365-personal-12m) in titolo per vetrina:
     * rimuove suffisso durata -12m/-24m, trattini → spazi, ogni segmento con iniziale maiuscola.
     * I segmenti solo numerici (365, 11) restano invariati.
     */
    function displayNameFromSku(sku) {
        let s = String(sku || '').trim();
        if (!s) return '';
        s = s.replace(/-\d+m$/i, '');
        return s
            .split('-')
            .filter(Boolean)
            .map((part) => {
                if (/^\d+$/.test(part)) return part;
                return part.charAt(0).toUpperCase() + part.slice(1).toLowerCase();
            })
            .join(' ');
    }

    /** Nome riga carrello: usa il titolo salvato se è diverso dallo SKU, altrimenti deriva dallo SKU. */
    function lineDisplayName(line) {
        const sku = String((line && line.sku) || '').trim();
        const raw = line && line.name != null ? String(line.name).trim() : '';
        if (raw && raw !== sku) return raw;
        return displayNameFromSku(sku) || sku;
    }

    function normalizeCurrency(el) {
        if (!el) return 'eur';
        const c = String(el.dataset.stripeCurrency || el.getAttribute('data-stripe-currency') || 'eur')
            .trim().toLowerCase();
        return c || 'eur';
    }

    function parseMinorAmount(el) {
        const raw = el.dataset.stripeUnitAmount || el.getAttribute('data-stripe-unit-amount');
        const n = Number(raw);
        return Number.isFinite(n) ? Math.round(n) : 0;
    }

    /**
     * Normalizza un src immagine in path assoluto (inizia con /).
     * Evita che path relativi come "../asset/..." siano broken fuori dalla pagina sorgente.
     */
    function normalizeImageSrc(src) {
        if (!src) return '';
        try {
            const url = new URL(src, global.location.href);
            // Mantieni solo path + search (no host) per portabilità multi-dominio
            return url.pathname + (url.search || '');
        } catch (_) {
            return src;
        }
    }

    function productTitleFromPage() {
        const h = document.querySelector('h1.product-title');
        if (h) return h.textContent.replace(/\s+/g, ' ').trim();
        const v2 = document.querySelector('.v2-hero__title');
        return v2 ? v2.textContent.replace(/\s+/g, ' ').trim() : '';
    }

    /** Specifiche reali (durata/dispositivi/tipo licenza) dal badge già scritto su ogni PDP — mai inventate. */
    function productSpecsFromPage() {
        const el = document.querySelector('.pdp-badges .pdp-badge:not(.pdp-badge--alt)');
        return el ? el.textContent.replace(/\s+/g, ' ').trim() : '';
    }

    function lineFromProductContext(root) {
        const sku = normalizeSku(root);
        if (!sku) return null;
        const title = productTitleFromPage();
        const name = title || displayNameFromSku(sku);
        const currency = normalizeCurrency(root);
        const unitAmount = parseMinorAmount(root);
        const imgEl = document.querySelector('.product-cover-img');
        const image = normalizeImageSrc(imgEl && imgEl.getAttribute('src'));
        const productPath = global.location.pathname || '';
        const specs = productSpecsFromPage();
        return { sku, name, currency, unitAmount, quantity: 1, image, productPath, physical: isPhysical(root), specs };
    }

    /** Blocco prezzi / card catalogo da cui leggere SKU e importo */
    function isCartLineRoot(el) {
        if (!el || !el.classList) return false;
        const cl = el.classList;
        if (cl.contains('product-card')) return true;
        if (cl.contains('pricing-card')) return true;
        if (cl.contains('v2-pricing-card')) return true;
        if (cl.contains('plan-card')) return true;
        if (cl.contains('m365-card')) return true;
        return Boolean(normalizeSku(el));
    }

    /**
     * Card "a griglia" (più prodotti diversi sulla stessa pagina): nome/immagine/link
     * vanno letti dal DOM della card stessa, mai dal contesto di pagina (h1/immagine
     * globale), che appartiene invece alla singola PDP mono-prodotto.
     */
    function isGridCard(el) {
        if (!el || !el.classList) return false;
        const cl = el.classList;
        return cl.contains('product-card')
            || cl.contains('plan-card')
            || cl.contains('m365-card')
            || cl.contains('pricing-card')
            || cl.contains('v2-pricing-card');
    }

    function resolveLineRoot(btn) {
        const id = (btn.getAttribute('data-cart-source') || '').trim();
        if (id) {
            const el = document.getElementById(id);
            if (el && isCartLineRoot(el)) return el;
        }
        const fromDom =
            btn.closest('.product-card') ||
            btn.closest('.pricing-card') ||
            btn.closest('.v2-pricing-card') ||
            btn.closest('[data-stripe-product-sku]');
        if (fromDom) return fromDom;
        const fallback = document.getElementById('product-pricing');
        return fallback && isCartLineRoot(fallback) ? fallback : null;
    }

    /* ─── Cart drawer ──────────────────────────────────────────────────────────
       Sostituisce il toast "aggiunto al carrello". Il toast confermava
       l'aggiunta e spariva dopo 4 secondi: tolto "Acquista ora" dalla PDP,
       quel messaggio effimero era diventato l'unico ponte verso il checkout.

       Riusa tutto quello che c'era gia': lo stato del carrello e le sue
       funzioni (readLines/setQuantity/removeLine/formatMoney), il motore di
       suggerimenti `AmlCrossSell.pickSuggestions` con l'indice
       asset/cross-sell/{lang}.json, e le etichette gia' tradotte del
       carrello. Le uniche stringhe nuove sono "chiudi" e "continua". */

    var DRAWER_I18N = {
        it: { titolo: 'Il Tuo Carrello', consegna: 'Consegna digitale immediata',
              subtotale: 'Subtotale prodotti', rigaCons: 'Consegna digitale', valCons: 'Immediata',
              checkout: 'Procedi al checkout', crossTit: 'Completa la tua configurazione',
              aggiungi: 'Aggiungi', rimuovi: 'Rimuovi', qty: 'Quantità',
              meno: 'Riduci quantità per', piu: 'Aumenta quantità per',
              artSing: 'Articolo', artPlur: 'Articoli', vuoto: 'Il carrello è vuoto.',
              sicuri: 'Pagamenti protetti', fattura: 'Fattura elettronica',
              chiudi: 'Chiudi', continua: 'Continua lo shopping' },
        en: { titolo: 'Your Cart', consegna: 'Immediate digital delivery',
              subtotale: 'Products subtotal', rigaCons: 'Digital delivery', valCons: 'Instant',
              checkout: 'Proceed to checkout', crossTit: 'Complete your setup',
              aggiungi: 'Add', rimuovi: 'Remove', qty: 'Quantity',
              meno: 'Decrease quantity for', piu: 'Increase quantity for',
              artSing: 'Item', artPlur: 'Items', vuoto: 'Your cart is empty.',
              sicuri: 'Secure payments', fattura: 'Invoice available',
              chiudi: 'Close', continua: 'Continue shopping' },
        fr: { titolo: 'Votre Panier', consegna: 'Livraison numérique immédiate',
              subtotale: 'Sous-total produits', rigaCons: 'Livraison numérique', valCons: 'Immédiate',
              checkout: 'Passer à la caisse', crossTit: 'Complétez votre configuration',
              aggiungi: 'Ajouter', rimuovi: 'Retirer', qty: 'Quantité',
              meno: 'Réduire la quantité pour', piu: 'Augmenter la quantité pour',
              artSing: 'Article', artPlur: 'Articles', vuoto: 'Votre panier est vide.',
              sicuri: 'Paiements sécurisés', fattura: 'Facture disponible',
              chiudi: 'Fermer', continua: 'Continuer mes achats' },
        de: { titolo: 'Ihr Warenkorb', consegna: 'Sofortige digitale Lieferung',
              subtotale: 'Zwischensumme Produkte', rigaCons: 'Digitale Lieferung', valCons: 'Sofort',
              checkout: 'Zur Kasse', crossTit: 'Vervollständigen Sie Ihre Ausstattung',
              aggiungi: 'Hinzufügen', rimuovi: 'Entfernen', qty: 'Menge',
              meno: 'Menge verringern für', piu: 'Menge erhöhen für',
              artSing: 'Artikel', artPlur: 'Artikel', vuoto: 'Ihr Warenkorb ist leer.',
              sicuri: 'Sichere Zahlungen', fattura: 'Rechnung verfügbar',
              chiudi: 'Schließen', continua: 'Weiter einkaufen' },
        es: { titolo: 'Tu Carrito', consegna: 'Entrega digital inmediata',
              subtotale: 'Subtotal de productos', rigaCons: 'Entrega digital', valCons: 'Inmediata',
              checkout: 'Ir al pago', crossTit: 'Completa tu configuración',
              aggiungi: 'Añadir', rimuovi: 'Quitar', qty: 'Cantidad',
              meno: 'Reducir cantidad para', piu: 'Aumentar cantidad para',
              artSing: 'Artículo', artPlur: 'Artículos', vuoto: 'Su carrito está vacío.',
              sicuri: 'Pagos seguros', fattura: 'Factura disponible',
              chiudi: 'Cerrar', continua: 'Seguir comprando' },
        pt: { titolo: 'O seu carrinho', consegna: 'Entrega digital imediata',
              subtotale: 'Subtotal dos produtos', rigaCons: 'Entrega digital', valCons: 'Imediata',
              checkout: 'Prosseguir para o checkout', crossTit: 'Complete a sua configuração',
              aggiungi: 'Adicionar', rimuovi: 'Remover', qty: 'Quantidade',
              meno: 'Diminuir quantidade de', piu: 'Aumentar quantidade de',
              artSing: 'Artigo', artPlur: 'Artigos', vuoto: 'O seu carrinho está vazio.',
              sicuri: 'Pagamentos seguros', fattura: 'Fatura disponível',
              chiudi: 'Fechar', continua: 'Continuar a comprar' },
        nl: { titolo: 'Uw winkelwagen', consegna: 'Directe digitale levering',
              subtotale: 'Subtotaal producten', rigaCons: 'Digitale levering', valCons: 'Direct',
              checkout: 'Doorgaan naar afrekenen', crossTit: 'Maak uw configuratie compleet',
              aggiungi: 'Toevoegen', rimuovi: 'Verwijderen', qty: 'Aantal',
              meno: 'Aantal verlagen voor', piu: 'Aantal verhogen voor',
              artSing: 'Artikel', artPlur: 'Artikelen', vuoto: 'Uw winkelwagen is leeg.',
              sicuri: 'Veilige betalingen', fattura: 'Factuur beschikbaar',
              chiudi: 'Sluiten', continua: 'Verder winkelen' },
    };

    function cartLang() {
        var m = (document.documentElement.lang || '').match(/^[a-z]{2}/i)
             || (global.location.pathname || '').match(/^\/([a-z]{2})\//);
        var code = m ? String(m[1] || m[0]).toLowerCase() : 'it';
        return DRAWER_I18N[code] ? code : 'it';
    }

    var drawerEl = null;
    var drawerPrevFocus = null;
    var drawerCatalog = null;

    var ICON_CLOSE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"'
        + ' stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
    var ICON_TRASH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"'
        + ' stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        + '<path d="M4 7h16M10 11v6M14 11v6"/><path d="M6 7l1 13h10l1-13"/>'
        + '<path d="M9 7V5a1 1 0 011-1h4a1 1 0 011 1v2"/></svg>';
    var ICON_LOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"'
        + ' aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2"/>'
        + '<path stroke-linecap="round" d="M8 10V7a4 4 0 018 0v3"/></svg>';

    function ensureDrawerStyles() {
        if (document.getElementById('aml-cart-drawer-style')) return;
        var css =
            '.aml-drawer-scrim{position:fixed;inset:0;z-index:10050;background:rgba(15,23,42,.45);'
            + 'opacity:0;transition:opacity .22s ease;}'
            + '.aml-drawer-scrim.is-open{opacity:1;}'
            + '.aml-drawer{position:fixed;top:0;right:0;bottom:0;z-index:10051;width:min(420px,100%);'
            + 'display:flex;flex-direction:column;background:var(--page-bg,#fff);'
            + 'color:var(--page-text,#0f172a);box-shadow:-8px 0 32px rgba(15,23,42,.18);'
            + 'transform:translateX(100%);transition:transform .26s cubic-bezier(.22,.61,.36,1);}'
            + '.aml-drawer.is-open{transform:translateX(0);}'
            + '@media (prefers-reduced-motion:reduce){.aml-drawer,.aml-drawer-scrim{transition:none;}}'
            + '.aml-drawer__head{flex:0 0 auto;padding:16px 18px 12px;'
            + 'border-bottom:1px solid var(--page-border,#e2e8f0);}'
            + '.aml-drawer__titlerow{display:flex;align-items:center;gap:12px;}'
            + '.aml-drawer__title{margin:0;font-size:1.05rem;font-weight:800;flex:1 1 auto;}'
            + '.aml-drawer__close{flex:0 0 auto;width:40px;height:40px;display:inline-flex;'
            + 'align-items:center;justify-content:center;border:none;border-radius:8px;'
            + 'background:transparent;color:inherit;cursor:pointer;}'
            + '.aml-drawer__close:hover{background:rgba(15,23,42,.06);}'
            + '.aml-drawer__close svg{width:20px;height:20px;}'
            + '.aml-drawer__chip{display:inline-flex;align-items:center;gap:7px;margin-top:10px;'
            + 'padding:4px 10px;border-radius:999px;font-size:.72rem;font-weight:800;'
            + 'letter-spacing:.04em;text-transform:uppercase;'
            + 'background:var(--aml-ok-bg,#E8F3ED);color:var(--aml-ok,#1F7A52);}'
            + '.aml-drawer__chip::before{content:"";width:7px;height:7px;border-radius:50%;'
            + 'background:currentColor;}'
            + '.aml-drawer__body{flex:1 1 auto;overflow-y:auto;padding:14px 18px;}'
            + '.aml-drawer__empty{margin:24px 0;color:var(--page-text-secondary,#475569);}'
            + '.aml-drawer__line{display:grid;grid-template-columns:56px 1fr;gap:12px;'
            + 'padding:12px 0;border-bottom:1px solid var(--page-border,#e2e8f0);}'
            + '.aml-drawer__line:last-of-type{border-bottom:none;}'
            + '.aml-drawer__thumb{width:56px;height:56px;object-fit:contain;border-radius:6px;}'
            + '.aml-drawer__name{margin:0;font-size:.92rem;font-weight:700;line-height:1.3;}'
            + '.aml-drawer__name a{color:inherit;text-decoration:none;}'
            + '.aml-drawer__name a:hover{text-decoration:underline;}'
            + '.aml-drawer__config{margin:2px 0 0;font-size:.8rem;'
            + 'color:var(--page-text-secondary,#475569);}'
            + '.aml-drawer__row{display:flex;align-items:center;gap:10px;margin-top:8px;}'
            + '.aml-drawer__price{font-weight:800;margin-right:auto;}'
            + '.aml-drawer__foot{flex:0 0 auto;padding:14px 18px calc(14px + env(safe-area-inset-bottom));'
            + 'border-top:1px solid var(--page-border,#e2e8f0);background:var(--page-bg,#fff);}'
            + '.aml-drawer__sum{display:flex;justify-content:space-between;font-size:.9rem;'
            + 'margin-bottom:6px;}'
            + '.aml-drawer__sum--total{font-weight:800;font-size:1rem;}'
            + '.aml-drawer__cta{display:flex;align-items:center;justify-content:center;gap:8px;'
            + 'width:100%;margin-top:10px;padding:14px 20px;border:none;border-radius:8px;'
            + 'background:var(--aml-cta-bg,#F05A10);color:var(--aml-cta-ink,#fff);'
            + 'font:inherit;font-size:.98rem;font-weight:800;text-decoration:none;cursor:pointer;}'
            + '.aml-drawer__secure{display:flex;align-items:center;justify-content:center;gap:7px;'
            + 'margin:10px 0 0;font-size:.75rem;color:var(--page-text-secondary,#475569);}'
            + '.aml-drawer__secure svg{width:14px;height:14px;flex:0 0 auto;}'
            + '.aml-drawer__back{display:block;width:100%;margin-top:8px;padding:6px;border:none;'
            + 'background:transparent;color:var(--page-text-secondary,#475569);font:inherit;'
            + 'font-size:.82rem;text-decoration:underline;cursor:pointer;}'
            + '.aml-drawer__cross{margin-top:18px;padding-top:14px;'
            + 'border-top:1px solid var(--page-border,#e2e8f0);}'
            + '.aml-drawer__cross-title{margin:0 0 10px;font-size:.72rem;font-weight:800;'
            + 'letter-spacing:.07em;text-transform:uppercase;'
            + 'color:var(--page-text-secondary,#475569);}'
            + '.aml-drawer__sugg{display:grid;grid-template-columns:44px 1fr auto;gap:10px;'
            + 'align-items:center;}'
            + '.aml-drawer__sugg>div{min-width:0;}'
            + '.aml-drawer__sugg img{width:44px;height:44px;object-fit:contain;}'
            + '.aml-drawer__sugg-name{font-size:.85rem;font-weight:700;line-height:1.25;}'
            + '.aml-drawer__sugg-specs{font-size:.75rem;color:var(--page-text-secondary,#475569);}'
            + '.aml-drawer__sugg-price{font-size:.85rem;font-weight:700;}'
            + '.aml-drawer__sugg-was{font-weight:400;text-decoration:line-through;'
            + 'color:var(--page-text-secondary,#475569);margin-left:5px;}'
            + '.aml-drawer__sugg-add{padding:8px 12px;border-radius:8px;'
            + 'border:1px solid var(--page-border,#e2e8f0);background:transparent;color:inherit;'
            + 'font:inherit;font-size:.8rem;font-weight:700;cursor:pointer;white-space:nowrap;}'
            + '.aml-drawer__sugg-add:hover{background:rgba(15,23,42,.05);}'
            // Stepper e cestino riusano le classi della pagina carrello, ma
            // css/cart.css e' incluso solo la': su PDP e categorie resterebbero
            // senza stile. Qui sono ridefiniti nell'ambito del drawer.
            + '.aml-drawer .aml-cart-qty-stepper{display:inline-flex;align-items:stretch;'
            + 'border-radius:10px;background:var(--page-bg,#fff);overflow:hidden;'
            + 'box-shadow:inset 0 0 0 1px var(--page-border,#e2e8f0);}'
            + '.aml-drawer .aml-cart-qty-stepper:focus-within{'
            + 'box-shadow:inset 0 0 0 2px var(--page-accent,#C74104);}'
            + '.aml-drawer .aml-cart-qty-btn{width:38px;min-height:38px;padding:0;border:none;'
            + 'background:transparent;color:var(--page-text-secondary,#475569);font:inherit;'
            + 'font-size:1.1rem;font-weight:800;line-height:1;cursor:pointer;'
            + 'display:inline-flex;align-items:center;justify-content:center;}'
            + '.aml-drawer .aml-cart-qty-btn:disabled{opacity:.4;cursor:default;}'
            + '.aml-drawer .aml-cart-qty{width:34px;min-height:38px;margin:0;padding:0;'
            + 'border:none;border-left:1px solid var(--page-border,#e2e8f0);'
            + 'border-right:1px solid var(--page-border,#e2e8f0);border-radius:0;'
            + 'background:transparent;color:inherit;font:inherit;font-weight:700;'
            + 'text-align:center;-moz-appearance:textfield;appearance:textfield;}'
            + '.aml-drawer .aml-cart-qty::-webkit-outer-spin-button,'
            + '.aml-drawer .aml-cart-qty::-webkit-inner-spin-button{'
            + '-webkit-appearance:none;margin:0;}'
            + '.aml-drawer .aml-cart-remove{display:inline-flex;align-items:center;'
            + 'justify-content:center;width:38px;height:38px;padding:0;border:none;'
            + 'border-radius:8px;background:transparent;'
            + 'color:var(--page-text-secondary,#475569);cursor:pointer;}'
            + '.aml-drawer .aml-cart-remove:hover{background:var(--aml-danger-bg,#FBEAE9);'
            + 'color:var(--aml-danger,#B3261E);}'
            + '.aml-drawer .aml-cart-remove svg{width:19px;height:19px;pointer-events:none;}';
        var st = document.createElement('style');
        st.id = 'aml-cart-drawer-style';
        st.textContent = css;
        document.head.appendChild(st);
    }

    function drawerCheckoutHref() {
        var lang = cartLang();
        return '/' + lang + '/checkout';
    }

    function buildDrawer() {
        if (drawerEl) return drawerEl;
        ensureDrawerStyles();
        var t = DRAWER_I18N[cartLang()];

        var scrim = document.createElement('div');
        scrim.className = 'aml-drawer-scrim';
        scrim.id = 'aml-cart-drawer-scrim';
        scrim.addEventListener('click', closeCartDrawer);

        var el = document.createElement('aside');
        el.className = 'aml-drawer';
        el.id = 'aml-cart-drawer';
        el.setAttribute('role', 'dialog');
        el.setAttribute('aria-modal', 'true');
        el.setAttribute('aria-labelledby', 'aml-cart-drawer-title');
        el.hidden = true;
        el.innerHTML =
            '<div class="aml-drawer__head">'
            + '<div class="aml-drawer__titlerow">'
            + '<h2 class="aml-drawer__title" id="aml-cart-drawer-title"></h2>'
            + '<button type="button" class="aml-drawer__close">' + ICON_CLOSE + '</button>'
            + '</div>'
            + '<span class="aml-drawer__chip"></span>'
            + '</div>'
            + '<div class="aml-drawer__body"></div>'
            + '<div class="aml-drawer__foot"></div>';
        el.querySelector('.aml-drawer__close').setAttribute('aria-label', t.chiudi);
        el.querySelector('.aml-drawer__chip').textContent = t.consegna;
        el.querySelector('.aml-drawer__close').addEventListener('click', closeCartDrawer);

        document.body.appendChild(scrim);
        document.body.appendChild(el);
        drawerEl = el;

        // Delegazione: le righe vengono ricostruite a ogni render.
        el.addEventListener('click', function (e) {
            var tgt = e.target;
            if (!tgt || !tgt.closest) return;
            var minus = tgt.closest('[data-drawer-minus]');
            var plus = tgt.closest('[data-drawer-plus]');
            var rm = tgt.closest('[data-drawer-remove]');
            var add = tgt.closest('[data-drawer-add]');
            if (minus || plus) {
                var sku = (minus || plus).getAttribute('data-sku');
                var cur = 0;
                readLines().forEach(function (l) { if (l.sku === sku) cur = Number(l.quantity) || 0; });
                var next = minus ? cur - 1 : cur + 1;
                if (next >= 1 && next <= 99) setQuantity(sku, next);
                return;
            }
            if (rm) { removeLine(rm.getAttribute('data-sku')); return; }
            if (add) {
                var payload = null;
                try { payload = JSON.parse(add.getAttribute('data-payload')); } catch (_) { payload = null; }
                if (payload && global.AmlCart && global.AmlCart.add) {
                    global.AmlCart.add(payload);
                    add.disabled = true;
                }
            }
        });

        return el;
    }

    function drawerLineNode(l, t) {
        var q = Number(l.quantity) || 0;
        var label = lineDisplayName(l);
        var node = document.createElement('div');
        node.className = 'aml-drawer__line';

        var img = document.createElement('img');
        img.className = 'aml-drawer__thumb';
        img.src = l.image || '';
        img.alt = '';
        img.loading = 'lazy';
        node.appendChild(img);

        var col = document.createElement('div');

        var name = document.createElement('p');
        name.className = 'aml-drawer__name';
        if (l.productPath) {
            var a = document.createElement('a');
            a.href = l.productPath;
            a.textContent = label;
            name.appendChild(a);
        } else {
            name.textContent = label;
        }
        col.appendChild(name);

        // Stessa deduplica della pagina carrello: la configurazione che il
        // titolo dice gia' non si ripete.
        var titolo = label.toLowerCase();
        var cfg = String(l.specs || '').split('·').map(function (s) { return s.trim(); })
            .filter(Boolean)
            .filter(function (s) { return titolo.indexOf(s.toLowerCase()) === -1; });
        if (cfg.length) {
            var p = document.createElement('p');
            p.className = 'aml-drawer__config';
            p.textContent = cfg.join(' · ');
            col.appendChild(p);
        }

        var row = document.createElement('div');
        row.className = 'aml-drawer__row';

        var price = document.createElement('span');
        price.className = 'aml-drawer__price';
        price.textContent = formatMoney(Math.round(Number(l.unitAmount) || 0) * q, l.currency);
        row.appendChild(price);

        var stepper = document.createElement('div');
        stepper.className = 'aml-cart-qty-stepper';
        stepper.setAttribute('role', 'group');
        stepper.setAttribute('aria-label', t.qty + ': ' + label);
        [['minus', '−', t.meno, q <= 1], ['plus', '+', t.piu, q >= 99]].forEach(function (spec, i) {
            if (i === 1) {
                var inp = document.createElement('input');
                inp.type = 'number';
                inp.className = 'aml-cart-qty';
                inp.min = '1'; inp.max = '99'; inp.value = String(q);
                inp.readOnly = true;
                inp.tabIndex = -1;
                inp.setAttribute('aria-hidden', 'true');
                stepper.appendChild(inp);
            }
            var b = document.createElement('button');
            b.type = 'button';
            b.className = 'aml-cart-qty-btn aml-cart-qty-btn--' + spec[0];
            b.setAttribute('data-drawer-' + spec[0], '1');
            b.setAttribute('data-sku', l.sku);
            b.setAttribute('aria-label', spec[2] + ' ' + label);
            b.disabled = spec[3];
            var seg = document.createElement('span');
            seg.setAttribute('aria-hidden', 'true');
            seg.textContent = spec[1];
            b.appendChild(seg);
            stepper.appendChild(b);
        });
        row.appendChild(stepper);

        var rm = document.createElement('button');
        rm.type = 'button';
        rm.className = 'aml-cart-remove aml-cart-remove--icon';
        rm.setAttribute('data-drawer-remove', '1');
        rm.setAttribute('data-sku', l.sku);
        rm.setAttribute('aria-label', t.rimuovi + ': ' + label);
        rm.setAttribute('title', t.rimuovi);
        rm.innerHTML = ICON_TRASH;
        row.appendChild(rm);

        col.appendChild(row);
        node.appendChild(col);
        return node;
    }

    function renderDrawerCross(body, lines, t) {
        if (!drawerCatalog || !global.AmlCrossSell || !global.AmlCrossSell.pickSuggestions) return;
        var sugg = global.AmlCrossSell.pickSuggestions(drawerCatalog, lines, 1);
        if (!sugg || !sugg.length) return;
        var s = sugg[0];

        var box = document.createElement('div');
        box.className = 'aml-drawer__cross';
        var h = document.createElement('p');
        h.className = 'aml-drawer__cross-title';
        h.textContent = t.crossTit;
        box.appendChild(h);

        var g = document.createElement('div');
        g.className = 'aml-drawer__sugg';
        var im = document.createElement('img');
        im.src = s.image || ''; im.alt = ''; im.loading = 'lazy';
        g.appendChild(im);

        var mid = document.createElement('div');
        var nm = document.createElement('div');
        nm.className = 'aml-drawer__sugg-name';
        nm.textContent = s.name || '';
        mid.appendChild(nm);
        if (s.specs) {
            var sp = document.createElement('div');
            sp.className = 'aml-drawer__sugg-specs';
            sp.textContent = s.specs;
            mid.appendChild(sp);
        }
        var pr = document.createElement('div');
        pr.className = 'aml-drawer__sugg-price';
        pr.textContent = formatMoney(s.priceMinor, s.currency);
        if (s.compareAtMinor && s.compareAtMinor > s.priceMinor) {
            var was = document.createElement('span');
            was.className = 'aml-drawer__sugg-was';
            was.textContent = formatMoney(s.compareAtMinor, s.currency);
            pr.appendChild(was);
        }
        mid.appendChild(pr);
        g.appendChild(mid);

        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'aml-drawer__sugg-add';
        btn.setAttribute('data-drawer-add', '1');
        btn.setAttribute('data-payload', JSON.stringify({
            sku: s.sku, name: s.name, currency: (s.currency || 'eur').toLowerCase(),
            unitAmount: s.priceMinor, quantity: 1, image: s.image,
            productPath: s.slug ? ('/' + cartLang() + '/' + s.slug) : '',
            physical: false, specs: s.specs || '',
        }));
        btn.textContent = '+ ' + t.aggiungi;
        g.appendChild(btn);

        box.appendChild(g);
        body.appendChild(box);
    }

    function renderDrawer() {
        if (!drawerEl) return;
        var t = DRAWER_I18N[cartLang()];
        var lines = readLines();
        var qty = totalQty(lines);
        var minor = totalMinor(lines);
        var currency = (lines[0] && lines[0].currency) || 'eur';

        drawerEl.querySelector('.aml-drawer__title').textContent =
            t.titolo + ' (' + qty + ')';

        var body = drawerEl.querySelector('.aml-drawer__body');
        var foot = drawerEl.querySelector('.aml-drawer__foot');
        body.textContent = '';
        foot.textContent = '';

        if (!lines.length) {
            var vuoto = document.createElement('p');
            vuoto.className = 'aml-drawer__empty';
            vuoto.textContent = t.vuoto;
            body.appendChild(vuoto);
            return;
        }

        lines.forEach(function (l) { body.appendChild(drawerLineNode(l, t)); });
        renderDrawerCross(body, lines, t);

        [[t.subtotale, formatMoney(minor, currency), false],
         [t.rigaCons, t.valCons, true]].forEach(function (r) {
            var d = document.createElement('div');
            d.className = 'aml-drawer__sum' + (r[2] ? '' : ' aml-drawer__sum--total');
            var a = document.createElement('span'); a.textContent = r[0];
            var b = document.createElement('span'); b.textContent = r[1];
            d.appendChild(a); d.appendChild(b);
            foot.appendChild(d);
        });

        var cta = document.createElement('a');
        cta.className = 'aml-drawer__cta';
        cta.href = drawerCheckoutHref();
        cta.textContent = t.checkout + ' →';
        foot.appendChild(cta);

        var sec = document.createElement('p');
        sec.className = 'aml-drawer__secure';
        sec.innerHTML = ICON_LOCK;
        var secTxt = document.createElement('span');
        secTxt.textContent = t.sicuri + ' · ' + t.fattura;
        sec.appendChild(secTxt);
        foot.appendChild(sec);

        var back = document.createElement('button');
        back.type = 'button';
        back.className = 'aml-drawer__back';
        back.textContent = '‹ ' + t.continua;
        back.addEventListener('click', closeCartDrawer);
        foot.appendChild(back);
    }

    function loadDrawerCross() {
        if (drawerCatalog) { renderDrawer(); return; }
        var lang = cartLang();
        var vai = function () {
            fetch('/asset/cross-sell/' + lang + '.json', { cache: 'no-cache' })
                .then(function (r) { return r.ok ? r.json() : []; })
                .then(function (d) { drawerCatalog = Array.isArray(d) ? d : []; renderDrawer(); })
                .catch(function () { drawerCatalog = []; });
        };
        if (global.AmlCrossSell && global.AmlCrossSell.pickSuggestions) { vai(); return; }
        // Il motore vive gia' nel repo ma e' incluso solo dalla pagina carrello:
        // qui si carica al primo bisogno invece di appesantire ogni pagina.
        var s = document.createElement('script');
        s.src = '/js/cart-cross-sell.js';
        s.async = true;
        s.onload = vai;
        s.onerror = function () { drawerCatalog = []; };
        document.head.appendChild(s);
    }

    // Stepper, cestino e cross-sell passano tutti da dispatch(): il drawer
    // si ridisegna dallo stato, non dal gesto che l'ha cambiato.
    document.addEventListener(EVT, function () {
        if (drawerEl && !drawerEl.hidden) renderDrawer();
    });

    function drawerKeydown(e) {
        if (e.key === 'Escape') { closeCartDrawer(); return; }
        if (e.key !== 'Tab' || !drawerEl) return;
        var f = drawerEl.querySelectorAll('a[href], button:not([disabled]), input:not([disabled])');
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }

    function openCartDrawer() {
        if (!document.body) return false;
        // Sulla pagina carrello il drawer sarebbe un doppione di cio' che
        // l'utente sta gia' guardando: li' basta il ridisegno della lista.
        if (document.getElementById('aml-cart-app')) return false;
        var el = buildDrawer();
        var scrim = document.getElementById('aml-cart-drawer-scrim');
        drawerPrevFocus = document.activeElement;
        renderDrawer();
        loadDrawerCross();
        el.hidden = false;
        document.body.style.overflow = 'hidden';
        requestAnimationFrame(function () {
            el.classList.add('is-open');
            if (scrim) scrim.classList.add('is-open');
            var close = el.querySelector('.aml-drawer__close');
            if (close) close.focus();
        });
        document.addEventListener('keydown', drawerKeydown);
        return true;
    }

    function closeCartDrawer() {
        if (!drawerEl) return;
        var scrim = document.getElementById('aml-cart-drawer-scrim');
        drawerEl.classList.remove('is-open');
        if (scrim) scrim.classList.remove('is-open');
        document.removeEventListener('keydown', drawerKeydown);
        document.body.style.overflow = '';
        var el = drawerEl;
        setTimeout(function () { if (!el.classList.contains('is-open')) el.hidden = true; }, 280);
        if (drawerPrevFocus && drawerPrevFocus.focus) {
            try { drawerPrevFocus.focus(); } catch (_) { /* elemento sparito */ }
        }
        drawerPrevFocus = null;
    }

    function announceCartAdded() {
        const main = document.querySelector('main.product-page');
        const msg = main && main.getAttribute('data-cart-added-msg');
        if (!msg) return;
        const live = document.getElementById('product-cart-live');
        if (!live) return;
        live.textContent = msg;
        clearTimeout(liveRegionClearTimer);
        liveRegionClearTimer = setTimeout(function () {
            live.textContent = '';
            liveRegionClearTimer = null;
        }, 3200);
    }

    function flashCartButtonsForSource(root) {
        if (!root) return;
        var nodes = [];
        document.querySelectorAll('[data-cart-add]').forEach(function (b) {
            if (resolveLineRoot(b) === root) nodes.push(b);
        });
        if (!nodes.length) return;
        clearTimeout(flashAddedTimer);
        nodes.forEach(function (b) { b.classList.add('is-added'); });
        flashAddedTimer = setTimeout(function () {
            nodes.forEach(function (b) { b.classList.remove('is-added'); });
            flashAddedTimer = null;
        }, 2200);
    }

    /**
     * Riga carrello per una card a griglia (product-card, plan-card, m365-card, ...):
     * nome/immagine/link letti SEMPRE dalla card stessa (mai dal contesto pagina),
     * cosi' più card con SKU diversi sulla stessa pagina non si "rubano" a vicenda i
     * dati. data-cart-image è la fonte primaria dell'immagine (stessa convenzione
     * slug->products/<slug>.webp usata ovunque); .product-card-img resta come
     * fallback per le card che mostrano già una foto prodotto inline.
     */
    function lineFromCard(root) {
        const sku = normalizeSku(root);
        if (!sku) return null;
        const nameEl = root.querySelector('.product-card-name, .plan-card__name, .m365-card__name');
        const name = (nameEl && nameEl.textContent.trim()) || displayNameFromSku(sku);
        const currency = normalizeCurrency(root);
        const unitAmount = parseMinorAmount(root);
        const cartImage = root.dataset.cartImage || root.getAttribute('data-cart-image') || '';
        const imgEl = root.querySelector('.product-card-img');
        const image = normalizeImageSrc(cartImage || (imgEl && imgEl.getAttribute('src')));
        const link = root.querySelector('a.product-card-body, .plan-card__more, .m365-card__more');
        let productPath = '';
        if (link && link.getAttribute('href')) {
            try {
                productPath = new URL(link.getAttribute('href'), global.location.href).pathname;
            } catch (_) {
                productPath = link.getAttribute('href');
            }
        }
        const blurbEl = root.querySelector('.product-card-blurb');
        const specs = blurbEl ? blurbEl.textContent.replace(/\s+/g, ' ').trim() : '';
        return { sku, name, currency, unitAmount, quantity: 1, image, productPath, physical: isPhysical(root), specs };
    }

    /* ─── Mutazioni carrello ───────────────────────────────────────────────────── */

    function mergeAdd(lines, line) {
        const next = lines.map((x) => ({ ...x }));
        const idx = next.findIndex((x) => x.sku === line.sku);
        if (idx >= 0) {
            next[idx].quantity = Number(next[idx].quantity) + Number(line.quantity || 1);
            next[idx].name = lineDisplayName({
                sku: next[idx].sku,
                name: line.name || next[idx].name,
            });
            next[idx].currency = line.currency || next[idx].currency;
            next[idx].unitAmount = line.unitAmount;
            if (line.image) next[idx].image = line.image;
            if (line.productPath) next[idx].productPath = line.productPath;
            if (line.specs) next[idx].specs = line.specs;
            next[idx].physical = Boolean(line.physical);
            return next;
        }
        next.push({
            sku: line.sku,
            name: lineDisplayName(line),
            currency: line.currency,
            unitAmount: line.unitAmount,
            quantity: Number(line.quantity) > 0 ? Number(line.quantity) : 1,
            image: line.image || '',
            productPath: line.productPath || '',
            physical: Boolean(line.physical),
            specs: line.specs || '',
        });
        return next;
    }

    function setQuantity(sku, quantity) {
        const q = Math.round(Number(quantity));
        // Guard: NaN o valore non numerico → ignora
        if (!Number.isFinite(q)) return;
        const clamped = Math.max(0, Math.min(99, q));
        const next = readLines().map((x) => ({ ...x }));
        const idx = next.findIndex((x) => x.sku === sku);
        if (idx < 0) return;
        if (clamped <= 0) next.splice(idx, 1);
        else next[idx].quantity = clamped;
        if (writeLines(next)) dispatch(next);
    }

    function removeLine(sku) {
        const next = readLines().filter((x) => x.sku !== sku);
        if (writeLines(next)) dispatch(next);
    }

    function clearCart() {
        if (writeLines([])) dispatch([]);
    }

    function formatMoney(minor, currency) {
        const cur = String(currency || 'eur').toUpperCase();
        try {
            return new Intl.NumberFormat(undefined, {
                style: 'currency', currency: cur,
                minimumFractionDigits: 2, maximumFractionDigits: 2
            }).format(minor / 100);
        } catch (_) {
            return `€ ${(minor / 100).toFixed(2)}`;
        }
    }

    /* ─── Delegazione click su [data-cart-add] ─────────────────────────────────── */
    // Unico listener sul document: gestisce bottoni presenti ora e futuri (contenuto dinamico).

    function initAddDelegation() {
        document.addEventListener('click', function (e) {
            const btn = e.target && e.target.closest ? e.target.closest('[data-cart-add]') : null;
            if (!btn) return;
            const lineRoot = resolveLineRoot(btn);
            if (!lineRoot) return;
            const line = isGridCard(lineRoot)
                ? lineFromCard(lineRoot)
                : lineFromProductContext(lineRoot);
            if (!line) return;
            const next = mergeAdd(readLines(), line);
            if (writeLines(next)) {
                dispatch(next);
                // Checkout espresso: si aggiunge al carrello e si salta dritti al
                // pagamento, niente drawer/flash che tanto non fa in tempo a vedersi.
                const redirect = btn.getAttribute('data-cart-checkout-redirect');
                if (redirect) {
                    trackEvent('buy_now_click', { sku: line.sku });
                    global.location.href = redirect;
                    return;
                }
                trackEvent('add_to_cart', { sku: line.sku });
                // Il drawer conferma l'aggiunta e porta al checkout senza
                // cambiare pagina; announceCartAdded() resta per i contesti
                // senza body (fallback).
                if (!openCartDrawer()) announceCartAdded();
                flashCartButtonsForSource(lineRoot);
            }
        });
    }

    /* ─── Pagina carrello ──────────────────────────────────────────────────────── */

    function initCartPage() {
        const mount = document.getElementById('aml-cart-app');
        if (!mount || mount.dataset.amlCartPageInit) return;
        mount.dataset.amlCartPageInit = '1';

        const emptyEl = document.getElementById('aml-cart-empty');
        const filledEl = document.getElementById('aml-cart-filled');
        const itemsEl = document.getElementById('aml-cart-lines');
        const totalEl = document.getElementById('aml-cart-total');
        const subtotalEl = document.getElementById('aml-cart-subtotal');
        const countEl = document.getElementById('aml-cart-count');
        const deliveryNoteEl = document.getElementById('aml-cart-delivery-note');
        const removeLabel = mount.getAttribute('data-label-remove') || 'Remove';
        const qtyAria = mount.getAttribute('data-qty-aria') || 'Quantity';
        const qtyMinusAria = mount.getAttribute('data-label-qty-minus') || 'Decrease quantity for';
        const qtyPlusAria = mount.getAttribute('data-label-qty-plus') || 'Increase quantity for';
        const itemSingular = mount.getAttribute('data-label-item-singular') || 'item';
        const itemPlural = mount.getAttribute('data-label-item-plural') || 'items';
        const deliveryDigital = mount.getAttribute('data-label-delivery-digital') || 'Digital delivery by email';
        const deliveryPhysical = mount.getAttribute('data-label-delivery-physical') || 'Physical shipping';
        const shippingDigital = mount.getAttribute('data-label-shipping-digital') || 'Immediate digital delivery';
        const shippingMixed = mount.getAttribute('data-label-shipping-mixed') || 'Shipping';
        const sumShipLabel = mount.getAttribute('data-label-summary-shipping') || 'Shipping';
        const sumShipValue = mount.getAttribute('data-label-summary-shipping-value') || 'Free';
        const sumDelivLabel = mount.getAttribute('data-label-summary-delivery') || 'Digital delivery';
        const sumDelivValue = mount.getAttribute('data-label-summary-delivery-value') || 'Instant';
        const deliveryLabelEl = document.getElementById('aml-cart-delivery-label');
        const deliveryValueEl = document.getElementById('aml-cart-delivery-value');

        // Cestino al posto della parola "Rimuovi": un bottone di testo
        // accanto allo stepper faceva tre riquadri in fila sulla stessa riga.
        const TRASH_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"'
            + ' stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
            + ' aria-hidden="true" focusable="false">'
            + '<path d="M4 7h16M10 11v6M14 11v6"/>'
            + '<path d="M6 7l1 13h10l1-13"/>'
            + '<path d="M9 7V5a1 1 0 011-1h4a1 1 0 011 1v2"/></svg>';

        function buildChip(text, modifier) {
            const chip = document.createElement('span');
            chip.className = 'cart-item__chip' + (modifier ? ' cart-item__chip--' + modifier : '');
            chip.textContent = text;
            return chip;
        }

        function render() {
            const lines = readLines();
            const qty = totalQty(lines);
            const minor = totalMinor(lines);
            const currency = (lines[0] && lines[0].currency) || 'eur';

            if (!itemsEl || !emptyEl || !filledEl) return;

            if (qty === 0) {
                emptyEl.hidden = false;
                filledEl.hidden = true;
                itemsEl.textContent = '';
                if (countEl) countEl.textContent = '';
                return;
            }

            emptyEl.hidden = true;
            filledEl.hidden = false;
            itemsEl.textContent = '';

            if (countEl) countEl.textContent = qty + ' ' + (qty === 1 ? itemSingular : itemPlural);
            const allDigital = lines.every((l) => !l.physical);
            if (deliveryNoteEl) {
                deliveryNoteEl.textContent = allDigital ? shippingDigital : shippingMixed;
            }
            if (deliveryLabelEl && deliveryValueEl) {
                deliveryLabelEl.textContent = allDigital ? sumDelivLabel : sumShipLabel;
                deliveryValueEl.textContent = allDigital ? sumDelivValue : sumShipValue;
            }
            // Il chip "consegna digitale" per riga ripete l'intestazione solo se
            // TUTTO il carrello e' digitale: e' li' che su mobile si puo' togliere.
            if (itemsEl) itemsEl.classList.toggle('cart-items-list--all-digital', allDigital);

            lines.forEach((l) => {
                const q = Number(l.quantity) || 0;
                const lineMinor = Math.round(Number(l.unitAmount) || 0) * q;
                const path = l.productPath || '';
                const label = lineDisplayName(l);

                const item = document.createElement('div');
                item.className = 'cart-item';

                const media = document.createElement('div');
                media.className = 'cart-item__media';
                const img = document.createElement('img');
                img.src = l.image || '../asset/media/product-cover-fallback.webp';
                img.alt = '';
                img.loading = 'lazy';
                img.decoding = 'async';
                media.appendChild(img);

                const body = document.createElement('div');
                body.className = 'cart-item__body';

                const nameEl = document.createElement('h3');
                nameEl.className = 'cart-item__name';
                if (path) {
                    const a = document.createElement('a');
                    a.href = path;
                    a.textContent = label;
                    nameEl.appendChild(a);
                } else {
                    nameEl.textContent = label;
                }
                body.appendChild(nameEl);

                // Il titolo dice gia' marca e configurazione ("Kaspersky
                // Standard 2026 · 1 dispositivo"): ripeterle nei chip
                // subito sotto era scrivere due volte la stessa cosa a un
                // millimetro di distanza. Restano i soli pezzi che il titolo
                // non contiene, come riga di testo.
                const titoloNorm = label.toLowerCase();
                const config = String(l.specs || '')
                    .split('·')
                    .map((s) => s.trim())
                    .filter(Boolean)
                    .filter((s) => titoloNorm.indexOf(s.toLowerCase()) === -1);
                if (config.length) {
                    const cfg = document.createElement('p');
                    cfg.className = 'cart-item__config';
                    cfg.textContent = config.join(' · ');
                    body.appendChild(cfg);
                }
                const chips = document.createElement('div');
                chips.className = 'cart-item__chips';
                // Modificatore distinto: su mobile il chip digitale si nasconde
                // (ridondante con l'intestazione) mentre quello di spedizione no,
                // perche' in un carrello misto dice quale articolo viaggia per posta.
                if (!allDigital) {
                    chips.appendChild(buildChip(
                        l.physical ? deliveryPhysical : deliveryDigital,
                        l.physical ? 'shipping' : 'delivery',
                    ));
                }
                if (chips.childNodes.length) body.appendChild(chips);

                const controls = document.createElement('div');
                controls.className = 'cart-item__controls';

                const price = document.createElement('div');
                price.className = 'cart-item__price';
                price.textContent = formatMoney(lineMinor, l.currency);
                controls.appendChild(price);

                const stepper = document.createElement('div');
                stepper.className = 'aml-cart-qty-stepper';
                stepper.setAttribute('role', 'group');
                stepper.setAttribute('aria-label', qtyAria + ': ' + label);

                const btnMinus = document.createElement('button');
                btnMinus.type = 'button';
                btnMinus.className = 'aml-cart-qty-btn aml-cart-qty-btn--minus';
                btnMinus.setAttribute('data-sku-qty', l.sku);
                btnMinus.setAttribute('aria-label', qtyMinusAria + ' ' + label);
                btnMinus.disabled = q <= 1;
                const segMinus = document.createElement('span');
                segMinus.setAttribute('aria-hidden', 'true');
                segMinus.textContent = '−';
                btnMinus.appendChild(segMinus);

                const inp = document.createElement('input');
                inp.type = 'number';
                inp.className = 'aml-cart-qty';
                inp.min = '1';
                inp.max = '99';
                inp.setAttribute('inputmode', 'numeric');
                inp.setAttribute('pattern', '[0-9]*');
                inp.value = String(q);
                inp.setAttribute('data-sku', l.sku);
                inp.setAttribute('aria-label', qtyAria + ': ' + label);

                const btnPlus = document.createElement('button');
                btnPlus.type = 'button';
                btnPlus.className = 'aml-cart-qty-btn aml-cart-qty-btn--plus';
                btnPlus.setAttribute('data-sku-qty', l.sku);
                btnPlus.setAttribute('aria-label', qtyPlusAria + ' ' + label);
                btnPlus.disabled = q >= 99;
                const segPlus = document.createElement('span');
                segPlus.setAttribute('aria-hidden', 'true');
                segPlus.textContent = '+';
                btnPlus.appendChild(segPlus);

                stepper.appendChild(btnMinus);
                stepper.appendChild(inp);
                stepper.appendChild(btnPlus);
                controls.appendChild(stepper);

                const rm = document.createElement('button');
                rm.type = 'button';
                rm.className = 'aml-cart-remove aml-cart-remove--icon';
                rm.setAttribute('data-sku-remove', l.sku);
                rm.setAttribute('aria-label', removeLabel + ': ' + label);
                rm.setAttribute('title', removeLabel);
                rm.innerHTML = TRASH_SVG;
                controls.appendChild(rm);

                item.appendChild(media);
                item.appendChild(body);
                item.appendChild(controls);
                itemsEl.appendChild(item);
            });

            if (totalEl) totalEl.textContent = formatMoney(minor, currency);
            if (subtotalEl) subtotalEl.textContent = formatMoney(minor, currency);
        }

        if (itemsEl && !itemsEl.dataset.amlCartDelegated) {
            itemsEl.dataset.amlCartDelegated = '1';

            // `change` per mouse/Enter; `input` + debounce per mobile (alcuni browser
            // non emettono `change` finché il campo non perde il focus).
            var qtyInputTimer = null;
            itemsEl.addEventListener('input', function (e) {
                const t = e.target;
                if (!t || !t.classList || !t.classList.contains('aml-cart-qty')) return;
                clearTimeout(qtyInputTimer);
                qtyInputTimer = setTimeout(function () {
                    qtyInputTimer = null;
                    setQuantity(t.getAttribute('data-sku'), t.value);
                }, 600);
            });

            itemsEl.addEventListener('change', function (e) {
                const t = e.target;
                if (!t || !t.classList || !t.classList.contains('aml-cart-qty')) return;
                // Cancella il debounce pendente e aggiorna subito
                clearTimeout(qtyInputTimer);
                qtyInputTimer = null;
                setQuantity(t.getAttribute('data-sku'), t.value);
            });

            // Enter sul campo qty: conferma immediata
            itemsEl.addEventListener('keydown', function (e) {
                if (e.key !== 'Enter') return;
                const t = e.target;
                if (!t || !t.classList || !t.classList.contains('aml-cart-qty')) return;
                clearTimeout(qtyInputTimer);
                qtyInputTimer = null;
                setQuantity(t.getAttribute('data-sku'), t.value);
                t.blur();
            });

            itemsEl.addEventListener('click', function (e) {
                const t = e.target;
                if (!t || !t.closest) return;
                const rm = t.closest('[data-sku-remove]');
                if (rm) {
                    removeLine(rm.getAttribute('data-sku-remove'));
                    return;
                }
                const dec = t.closest('.aml-cart-qty-btn--minus');
                if (dec && !dec.disabled) {
                    const sku = dec.getAttribute('data-sku-qty');
                    const linesNow = readLines();
                    const lineNow = linesNow.find((x) => x.sku === sku);
                    const cur = Number(lineNow && lineNow.quantity) || 0;
                    if (cur > 1) setQuantity(sku, cur - 1);
                    return;
                }
                const inc = t.closest('.aml-cart-qty-btn--plus');
                if (inc && !inc.disabled) {
                    const sku = inc.getAttribute('data-sku-qty');
                    const linesNow = readLines();
                    const lineNow = linesNow.find((x) => x.sku === sku);
                    const cur = Number(lineNow && lineNow.quantity) || 0;
                    if (cur < 99) setQuantity(sku, cur + 1);
                }
            });
        }

        document.addEventListener(EVT, render);
        render();
    }

    /* ─── API pubblica ─────────────────────────────────────────────────────────── */

    global.AmlCart = {
        getItems: readLines,
        setQuantity,
        removeLine,
        clear: clearCart,
        totalQty: () => totalQty(readLines()),
        totalMinor: () => totalMinor(readLines()),
        formatMoney,
        displayNameFromSku,
        lineDisplayName,
        /** Righe con nome mostrabile (utile a checkout / worker). */
        getItemsForCheckout: function () {
            return readLines().map((l) => ({ ...l, name: lineDisplayName(l) }));
        },
        // Mantenuto per compatibilità; la delegazione è ora automatica su document.
        bindAddButtons: function () {},
        /**
         * Aggiunge una riga costruita da un chiamante esterno (es. il motore di
         * cross-sell, che legge da asset/cross-sell/{lang}.json e non ha una card
         * DOM da cui dedurre i dati). Traccia `add_to_cart` come il flusso a
         * click sulle card. Restituisce true se il carrello è stato scritto.
         */
        add: function (line) {
            if (!line || !line.sku) return false;
            const next = mergeAdd(readLines(), line);
            if (!writeLines(next)) return false;
            dispatch(next);
            trackEvent('add_to_cart', { sku: line.sku });
            return true;
        },
        /** cartId del ciclo di vita corrente (creato al bisogno). Usato dal checkout per collegare l'ordine. */
        getCartId: ensureCartId,
        /** Chiude il ciclo di vita del cartId corrente: da chiamare dopo un acquisto completato. */
        resetCartSession: resetCartSession,
        /** Aggancia un'email (dal form di checkout) al cartId corrente, se sintatticamente valida. */
        notifyEmail: function (email) {
            if (!email) return;
            scheduleSync({ email: email });
        },
    };

    /* ─── Init ─────────────────────────────────────────────────────────────────── */

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            initAddDelegation();
            initCartPage();
            dispatch(readLines());
        });
    } else {
        initAddDelegation();
        initCartPage();
        dispatch(readLines());
    }

})(typeof window !== 'undefined' ? window : globalThis);
