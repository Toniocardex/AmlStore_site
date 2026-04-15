/**
 * Carrello minimale (localStorage) + evento aml-cart-changed.
 * Checkout: opzionale mappa globale AML_STRIPE_PAYMENT_LINK_BY_SKU { sku: "https://buy.stripe.com/..." }.
 * Pulsanti fuori dalla card: data-cart-source="id" punta a #id di .product-card o .pricing-card.
 */
(function (global) {
    'use strict';

    const STORAGE_KEY = 'aml-cart-v1';
    const EVT = 'aml-cart-changed';

    function readLines() {
        try {
            const raw = global.localStorage.getItem(STORAGE_KEY);
            if (!raw) return [];
            const parsed = JSON.parse(raw);
            return Array.isArray(parsed) ? parsed : [];
        } catch (_) {
            return [];
        }
    }

    function writeLines(lines) {
        global.localStorage.setItem(STORAGE_KEY, JSON.stringify(lines));
    }

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

    function dispatch(lines) {
        const items = lines.slice();
        const detail = { items, count: totalQty(items) };
        try {
            document.dispatchEvent(new CustomEvent(EVT, { detail }));
        } catch (_) {
            /* SSR / tests */
        }
    }

    function normalizeSku(el) {
        if (!el) return '';
        const ds = el.dataset || {};
        return String(ds.stripeProductSku || el.getAttribute('data-stripe-product-sku') || '').trim();
    }

    function normalizeCurrency(el) {
        if (!el) return 'eur';
        const c = String(el.dataset.stripeCurrency || el.getAttribute('data-stripe-currency') || 'eur')
            .trim()
            .toLowerCase();
        return c || 'eur';
    }

    function parseMinorAmount(el) {
        const raw = el.dataset.stripeUnitAmount || el.getAttribute('data-stripe-unit-amount');
        const n = Number(raw);
        return Number.isFinite(n) ? Math.round(n) : 0;
    }

    function productTitleFromPage() {
        const h = document.querySelector('h1.product-title');
        return h ? h.textContent.replace(/\s+/g, ' ').trim() : '';
    }

    function lineFromProductContext(root) {
        const sku = normalizeSku(root);
        if (!sku) return null;
        const name = productTitleFromPage() || sku;
        const currency = normalizeCurrency(root);
        const unitAmount = parseMinorAmount(root);
        const imgEl = document.querySelector('.product-cover-img');
        const image = imgEl && imgEl.getAttribute('src') ? imgEl.getAttribute('src') : '';
        const productPath = global.location.pathname || '';
        return { sku, name, currency, unitAmount, quantity: 1, image, productPath };
    }

    function resolveLineRoot(btn) {
        const id = (btn.getAttribute('data-cart-source') || '').trim();
        if (id) {
            const el = document.getElementById(id);
            if (el && (el.classList.contains('pricing-card') || el.classList.contains('product-card'))) return el;
        }
        return btn.closest('.product-card') || btn.closest('.pricing-card');
    }

    function announceCartAdded() {
        const main = document.querySelector('main.product-page');
        const msg = main && main.getAttribute('data-cart-added-msg');
        if (!msg) return;
        let live = document.getElementById('product-cart-live');
        if (!live) return;
        live.textContent = msg;
        global.clearTimeout(global.__amlCartLiveClear);
        global.__amlCartLiveClear = global.setTimeout(function () {
            live.textContent = '';
        }, 3200);
    }

    function flashCartButtonsForSource(root) {
        if (!root || !root.id) return;
        const idAttr =
            global.CSS && typeof global.CSS.escape === 'function'
                ? global.CSS.escape(root.id)
                : root.id.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
        const sel = '[data-cart-add][data-cart-source="' + idAttr + '"]';
        global.clearTimeout(global.__amlCartFlashT);
        document.querySelectorAll(sel).forEach(function (b) {
            b.classList.add('is-added');
        });
        global.__amlCartFlashT = global.setTimeout(function () {
            document.querySelectorAll(sel).forEach(function (b) {
                b.classList.remove('is-added');
            });
        }, 2200);
    }

    function lineFromProductCard(root) {
        const sku = normalizeSku(root);
        if (!sku) return null;
        const nameEl = root.querySelector('.product-card-name');
        const name = (nameEl && nameEl.textContent.trim()) || sku;
        const currency = normalizeCurrency(root);
        const unitAmount = parseMinorAmount(root);
        const imgEl = root.querySelector('.product-card-img');
        const image = imgEl && imgEl.getAttribute('src') ? imgEl.getAttribute('src') : '';
        const link = root.querySelector('a.product-card-body');
        let productPath = '';
        if (link && link.getAttribute('href')) {
            try {
                productPath = new URL(link.getAttribute('href'), global.location.href).pathname;
            } catch (_) {
                productPath = link.getAttribute('href');
            }
        }
        return { sku, name, currency, unitAmount, quantity: 1, image, productPath };
    }

    function mergeAdd(lines, line) {
        const next = lines.map((x) => ({ ...x }));
        const idx = next.findIndex((x) => x.sku === line.sku);
        if (idx >= 0) {
            next[idx].quantity = Number(next[idx].quantity) + Number(line.quantity || 1);
            next[idx].name = line.name || next[idx].name;
            next[idx].currency = line.currency || next[idx].currency;
            next[idx].unitAmount = line.unitAmount;
            if (line.image) next[idx].image = line.image;
            if (line.productPath) next[idx].productPath = line.productPath;
            return next;
        }
        next.push({
            sku: line.sku,
            name: line.name,
            currency: line.currency,
            unitAmount: line.unitAmount,
            quantity: Number(line.quantity) > 0 ? Number(line.quantity) : 1,
            image: line.image || '',
            productPath: line.productPath || '',
        });
        return next;
    }

    function paymentMap() {
        const m = global.AML_STRIPE_PAYMENT_LINK_BY_SKU;
        return m && typeof m === 'object' ? m : {};
    }

    function stripeUrlForCart(lines) {
        if (lines.length !== 1) return '';
        const u = paymentMap()[lines[0].sku];
        if (typeof u !== 'string' || !u.startsWith('https://')) return '';
        return u;
    }

    function formatMoney(minor, currency) {
        const cur = String(currency || 'eur').toUpperCase();
        try {
            return new Intl.NumberFormat(undefined, { style: 'currency', currency: cur }).format(minor / 100);
        } catch (_) {
            return `€ ${(minor / 100).toFixed(2)}`;
        }
    }

    function mailtoOrder(lines) {
        const linesText = lines
            .map((l) => {
                const q = Number(l.quantity) || 0;
                return `${q}x ${l.name} (${l.sku}) — ${formatMoney(Math.round(Number(l.unitAmount) || 0) * q, l.currency)}`;
            })
            .join('\n');
        const sub = encodeURIComponent('Aml Store — cart order request');
        const body = encodeURIComponent(
            `Hello,\n\nI would like to place the following order:\n\n${linesText}\n\nIndicative total: ${formatMoney(totalMinor(lines), lines[0] && lines[0].currency)}\n`
        );
        return `mailto:Info@amlstore.it?subject=${sub}&body=${body}`;
    }

    function bindAddButtons(root) {
        const scope = root || document;
        scope.querySelectorAll('[data-cart-add]').forEach((btn) => {
            if (btn.dataset.amlCartBound) return;
            btn.dataset.amlCartBound = '1';
            btn.addEventListener('click', () => {
                const root = resolveLineRoot(btn);
                let line = null;
                if (!root) return;
                if (root.classList.contains('product-card')) line = lineFromProductCard(root);
                else line = lineFromProductContext(root);
                if (!line) return;
                const next = mergeAdd(readLines(), line);
                writeLines(next);
                dispatch(next);
                announceCartAdded();
                flashCartButtonsForSource(root);
            });
        });
    }

    function setQuantity(sku, quantity) {
        const q = Math.max(0, Math.min(99, Math.round(Number(quantity))));
        const next = readLines().map((x) => ({ ...x }));
        const idx = next.findIndex((x) => x.sku === sku);
        if (idx < 0) return;
        if (q <= 0) next.splice(idx, 1);
        else next[idx].quantity = q;
        writeLines(next);
        dispatch(next);
    }

    function removeLine(sku) {
        const next = readLines().filter((x) => x.sku !== sku);
        writeLines(next);
        dispatch(next);
    }

    function clearCart() {
        writeLines([]);
        dispatch([]);
    }

    function initCartPage() {
        const mount = document.getElementById('aml-cart-app');
        if (!mount || mount.dataset.amlCartPageInit) return;
        mount.dataset.amlCartPageInit = '1';

        const emptyEl = document.getElementById('aml-cart-empty');
        const filledEl = document.getElementById('aml-cart-filled');
        const tbody = document.getElementById('aml-cart-lines');
        const totalEl = document.getElementById('aml-cart-total');
        const stripeBtn = document.getElementById('aml-cart-stripe');
        const mailBtn = document.getElementById('aml-cart-mail');
        const multiNote = document.getElementById('aml-cart-multi-note');
        const removeLabel = mount.getAttribute('data-label-remove') || 'Remove';
        const qtyAria = mount.getAttribute('data-qty-aria') || 'Quantity';

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

                const tdName = document.createElement('td');
                tdName.className = 'aml-cart-col-name';
                if (path) {
                    const a = document.createElement('a');
                    a.href = path;
                    a.textContent = l.name;
                    tdName.appendChild(a);
                } else {
                    tdName.textContent = l.name;
                }

                const tdQty = document.createElement('td');
                tdQty.className = 'aml-cart-col-qty';
                const label = document.createElement('label');
                label.className = 'aml-cart-qty-label';
                const inv = document.createElement('span');
                inv.className = 'visually-hidden';
                inv.textContent = qtyAria;
                const inp = document.createElement('input');
                inp.type = 'number';
                inp.className = 'aml-cart-qty';
                inp.min = '1';
                inp.max = '99';
                inp.value = String(q);
                inp.setAttribute('data-sku', l.sku);
                inp.setAttribute('aria-label', qtyAria);
                label.appendChild(inv);
                label.appendChild(inp);
                tdQty.appendChild(label);

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

            const stripeUrl = stripeUrlForCart(lines);
            if (stripeBtn) {
                if (stripeUrl && lines.length === 1) {
                    stripeBtn.hidden = false;
                    stripeBtn.setAttribute('href', stripeUrl);
                    stripeBtn.setAttribute('rel', 'noopener noreferrer');
                } else {
                    stripeBtn.hidden = true;
                    stripeBtn.removeAttribute('href');
                    stripeBtn.removeAttribute('rel');
                }
            }
            if (multiNote) multiNote.hidden = lines.length < 2;
            if (mailBtn) mailBtn.setAttribute('href', mailtoOrder(lines));
        }

        if (tbody && !tbody.dataset.amlCartDelegated) {
            tbody.dataset.amlCartDelegated = '1';
            tbody.addEventListener('change', (e) => {
                const t = e.target;
                if (!t || !t.classList || !t.classList.contains('aml-cart-qty')) return;
                const sku = t.getAttribute('data-sku');
                setQuantity(sku, t.value);
            });
            tbody.addEventListener('click', (e) => {
                const t = e.target;
                if (!t || !t.closest) return;
                const btn = t.closest('[data-sku-remove]');
                if (!btn) return;
                removeLine(btn.getAttribute('data-sku-remove'));
            });
        }

        document.addEventListener(EVT, render);
        const clearBtn = document.getElementById('aml-cart-clear');
        if (clearBtn && !clearBtn.dataset.amlCartClearBound) {
            clearBtn.dataset.amlCartClearBound = '1';
            clearBtn.addEventListener('click', () => {
                clearCart();
            });
        }
        render();
    }

    const api = {
        getItems: readLines,
        setQuantity,
        removeLine,
        clear: clearCart,
        totalQty: () => totalQty(readLines()),
        totalMinor: () => totalMinor(readLines()),
        stripeUrlForCurrentCart: () => stripeUrlForCart(readLines()),
        mailtoOrderUrl: () => mailtoOrder(readLines()),
        bindAddButtons,
        formatMoney,
    };

    global.AmlCart = api;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            bindAddButtons(document);
            initCartPage();
            dispatch(readLines());
        });
    } else {
        bindAddButtons(document);
        initCartPage();
        dispatch(readLines());
    }
})(typeof window !== 'undefined' ? window : globalThis);
