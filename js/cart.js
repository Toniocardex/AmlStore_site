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
    }

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
        return { sku, name, currency, unitAmount, quantity: 1, image, productPath, physical: isPhysical(root) };
    }

    /** Blocco prezzi / card catalogo da cui leggere SKU e importo */
    function isCartLineRoot(el) {
        if (!el || !el.classList) return false;
        const cl = el.classList;
        if (cl.contains('product-card')) return true;
        if (cl.contains('pricing-card')) return true;
        if (cl.contains('v2-pricing-card')) return true;
        return Boolean(normalizeSku(el));
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

    /* ─── Toast "aggiunto al carrello" ─────────────────────────────────────────── */
    // Feedback visivo immediato su ogni pagina con bottoni [data-cart-add]:
    // il solo badge nell'header non è abbastanza visibile.

    var TOAST_I18N = {
        it: { added: 'Aggiunto al carrello', view: 'Vai al carrello' },
        en: { added: 'Added to cart', view: 'View cart' },
        fr: { added: 'Ajouté au panier', view: 'Voir le panier' },
        de: { added: 'Zum Warenkorb hinzugefügt', view: 'Warenkorb ansehen' },
        es: { added: 'Añadido al carrito', view: 'Ver carrito' },
    };
    var toastHideTimer = null;

    function toastLang() {
        var m = (document.documentElement.lang || '').match(/^[a-z]{2}/i)
             || (global.location.pathname || '').match(/^\/([a-z]{2})\//);
        var code = m ? String(m[1] || m[0]).toLowerCase() : 'it';
        return TOAST_I18N[code] ? code : 'it';
    }

    function ensureToastStyles() {
        if (document.getElementById('aml-cart-toast-style')) return;
        var css = ''
            + '.aml-cart-toast{position:fixed;left:50%;bottom:24px;transform:translate(-50%,16px);'
            + 'display:flex;align-items:center;gap:12px;max-width:min(92vw,420px);padding:13px 16px;'
            + 'background:rgba(17,24,39,0.92);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);'
            + 'color:#f9fafb;border:1px solid rgba(255,255,255,0.12);border-radius:8px;'
            + 'box-shadow:0 12px 32px rgba(0,0,0,0.35);z-index:1200;opacity:0;pointer-events:none;'
            + 'font-family:inherit;font-size:0.92rem;line-height:1.35;'
            + 'transition:opacity 0.25s ease,transform 0.25s ease;}'
            + '.aml-cart-toast.is-visible{opacity:1;transform:translate(-50%,0);pointer-events:auto;}'
            + '@media (min-width:640px){.aml-cart-toast{left:auto;right:24px;transform:translate(0,16px);}'
            + '.aml-cart-toast.is-visible{transform:translate(0,0);}}'
            + '.aml-cart-toast__check{flex-shrink:0;display:flex;align-items:center;justify-content:center;'
            + 'width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#10b981,#059669);}'
            + '.aml-cart-toast__check svg{width:16px;height:16px;stroke:#fff;stroke-width:3;fill:none;'
            + 'stroke-linecap:round;stroke-linejoin:round;}'
            + '.aml-cart-toast__body{min-width:0;}'
            + '.aml-cart-toast__title{font-weight:700;}'
            + '.aml-cart-toast__name{color:#d1d5db;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;'
            + 'max-width:260px;}'
            + '.aml-cart-toast__link{flex-shrink:0;margin-left:4px;color:#7cc0ff;font-weight:700;'
            + 'text-decoration:none;white-space:nowrap;}'
            + '.aml-cart-toast__link:hover{text-decoration:underline;}'
            + '.aml-cart-toast__link:focus-visible{outline:2px solid #7cc0ff;outline-offset:3px;border-radius:4px;}'
            + '@media (prefers-reduced-motion:reduce){.aml-cart-toast{transition:opacity 0.2s ease;'
            + 'transform:translate(-50%,0);}'
            + '@media (min-width:640px){.aml-cart-toast{transform:none;}}}';
        var style = document.createElement('style');
        style.id = 'aml-cart-toast-style';
        style.textContent = css;
        document.head.appendChild(style);
    }

    function ensureToastEl() {
        var el = document.getElementById('aml-cart-toast');
        if (el) return el;
        ensureToastStyles();
        var lang = toastLang();
        var t = TOAST_I18N[lang];

        el = document.createElement('div');
        el.id = 'aml-cart-toast';
        el.className = 'aml-cart-toast';
        el.setAttribute('role', 'status');
        el.setAttribute('aria-live', 'polite');

        var check = document.createElement('span');
        check.className = 'aml-cart-toast__check';
        check.setAttribute('aria-hidden', 'true');
        check.innerHTML = '<svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>';

        var body = document.createElement('div');
        body.className = 'aml-cart-toast__body';
        var title = document.createElement('div');
        title.className = 'aml-cart-toast__title';
        title.textContent = t.added;
        var name = document.createElement('div');
        name.className = 'aml-cart-toast__name';
        body.appendChild(title);
        body.appendChild(name);

        var link = document.createElement('a');
        link.className = 'aml-cart-toast__link';
        link.href = '/' + lang + '/cart';
        link.textContent = t.view + ' →';

        el.appendChild(check);
        el.appendChild(body);
        el.appendChild(link);

        // Click fuori dal link = chiudi subito
        el.addEventListener('click', function (e) {
            if (e.target && e.target.closest && e.target.closest('a')) return;
            hideCartToast();
        });

        document.body.appendChild(el);
        return el;
    }

    function hideCartToast() {
        var el = document.getElementById('aml-cart-toast');
        if (el) el.classList.remove('is-visible');
        clearTimeout(toastHideTimer);
        toastHideTimer = null;
    }

    function showCartToast(line) {
        var el = ensureToastEl();
        var nameEl = el.querySelector('.aml-cart-toast__name');
        if (nameEl) nameEl.textContent = lineDisplayName(line);
        // Riapparizione pulita anche se già visibile (riavvia transizione e timer)
        el.classList.remove('is-visible');
        void el.offsetWidth; // reflow per riavviare la transizione
        el.classList.add('is-visible');
        clearTimeout(toastHideTimer);
        toastHideTimer = setTimeout(hideCartToast, 4000);
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

    function lineFromProductCard(root) {
        const sku = normalizeSku(root);
        if (!sku) return null;
        const nameEl = root.querySelector('.product-card-name');
        const name = (nameEl && nameEl.textContent.trim()) || displayNameFromSku(sku);
        const currency = normalizeCurrency(root);
        const unitAmount = parseMinorAmount(root);
        const imgEl = root.querySelector('.product-card-img');
        const image = normalizeImageSrc(imgEl && imgEl.getAttribute('src'));
        const link = root.querySelector('a.product-card-body');
        let productPath = '';
        if (link && link.getAttribute('href')) {
            try {
                productPath = new URL(link.getAttribute('href'), global.location.href).pathname;
            } catch (_) {
                productPath = link.getAttribute('href');
            }
        }
        return { sku, name, currency, unitAmount, quantity: 1, image, productPath, physical: isPhysical(root) };
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
            return new Intl.NumberFormat(undefined, { style: 'currency', currency: cur }).format(minor / 100);
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
            const line = lineRoot.classList.contains('product-card')
                ? lineFromProductCard(lineRoot)
                : lineFromProductContext(lineRoot);
            if (!line) return;
            const next = mergeAdd(readLines(), line);
            if (writeLines(next)) {
                dispatch(next);
                // Il toast ha role="status": annuncia già ai lettori di schermo.
                // announceCartAdded() resta per le pagine senza body (fallback).
                if (document.body) showCartToast(line);
                else announceCartAdded();
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
        const tbody = document.getElementById('aml-cart-lines');
        const totalEl = document.getElementById('aml-cart-total');
        const removeLabel = mount.getAttribute('data-label-remove') || 'Remove';
        const qtyAria = mount.getAttribute('data-qty-aria') || 'Quantity';
        const qtyMinusAria = mount.getAttribute('data-label-qty-minus') || 'Decrease quantity for';
        const qtyPlusAria = mount.getAttribute('data-label-qty-plus') || 'Increase quantity for';

        function render() {
            const lines = readLines();
            const qty = totalQty(lines);
            const minor = totalMinor(lines);
            const currency = (lines[0] && lines[0].currency) || 'eur';

            if (!tbody || !emptyEl || !filledEl) return;

            if (qty === 0) {
                emptyEl.hidden = false;
                filledEl.hidden = true;
                tbody.textContent = '';
                return;
            }

            emptyEl.hidden = true;
            filledEl.hidden = false;
            tbody.textContent = '';

            lines.forEach((l) => {
                const tr = document.createElement('tr');
                const q = Number(l.quantity) || 0;
                const lineMinor = Math.round(Number(l.unitAmount) || 0) * q;
                const path = l.productPath || '';
                const label = lineDisplayName(l);

                const tdName = document.createElement('td');
                tdName.className = 'aml-cart-col-name';
                if (path) {
                    const a = document.createElement('a');
                    a.href = path;
                    a.textContent = label;
                    tdName.appendChild(a);
                } else {
                    tdName.textContent = label;
                }

                const tdQty = document.createElement('td');
                tdQty.className = 'aml-cart-col-qty';
                const stepper = document.createElement('div');
                stepper.className = 'aml-cart-qty-stepper';

                const btnMinus = document.createElement('button');
                btnMinus.type = 'button';
                btnMinus.className = 'aml-cart-qty-btn aml-cart-qty-btn--minus';
                btnMinus.setAttribute('data-sku-qty', l.sku);
                btnMinus.setAttribute('aria-label', qtyMinusAria + ' ' + label);
                btnMinus.disabled = q <= 1;
                btnMinus.appendChild(document.createTextNode('\u2212'));

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
                btnPlus.appendChild(document.createTextNode('+'));

                stepper.appendChild(btnMinus);
                stepper.appendChild(inp);
                stepper.appendChild(btnPlus);
                tdQty.appendChild(stepper);

                const tdPrice = document.createElement('td');
                tdPrice.className = 'aml-cart-col-price';
                tdPrice.textContent = formatMoney(lineMinor, l.currency);

                const tdRm = document.createElement('td');
                tdRm.className = 'aml-cart-col-remove';
                const rm = document.createElement('button');
                rm.type = 'button';
                rm.className = 'aml-cart-remove';
                rm.setAttribute('data-sku-remove', l.sku);
                rm.textContent = removeLabel;
                tdRm.appendChild(rm);

                tr.appendChild(tdName);
                tr.appendChild(tdQty);
                tr.appendChild(tdPrice);
                tr.appendChild(tdRm);
                tbody.appendChild(tr);
            });

            if (totalEl) totalEl.textContent = formatMoney(minor, currency);
        }

        if (tbody && !tbody.dataset.amlCartDelegated) {
            tbody.dataset.amlCartDelegated = '1';

            // `change` per mouse/Enter; `input` + debounce per mobile (alcuni browser
            // non emettono `change` finché il campo non perde il focus).
            var qtyInputTimer = null;
            tbody.addEventListener('input', function (e) {
                const t = e.target;
                if (!t || !t.classList || !t.classList.contains('aml-cart-qty')) return;
                clearTimeout(qtyInputTimer);
                qtyInputTimer = setTimeout(function () {
                    qtyInputTimer = null;
                    setQuantity(t.getAttribute('data-sku'), t.value);
                }, 600);
            });

            tbody.addEventListener('change', function (e) {
                const t = e.target;
                if (!t || !t.classList || !t.classList.contains('aml-cart-qty')) return;
                // Cancella il debounce pendente e aggiorna subito
                clearTimeout(qtyInputTimer);
                qtyInputTimer = null;
                setQuantity(t.getAttribute('data-sku'), t.value);
            });

            // Enter sul campo qty: conferma immediata
            tbody.addEventListener('keydown', function (e) {
                if (e.key !== 'Enter') return;
                const t = e.target;
                if (!t || !t.classList || !t.classList.contains('aml-cart-qty')) return;
                clearTimeout(qtyInputTimer);
                qtyInputTimer = null;
                setQuantity(t.getAttribute('data-sku'), t.value);
                t.blur();
            });

            tbody.addEventListener('click', function (e) {
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
