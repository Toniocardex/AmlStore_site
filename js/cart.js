/**
 * Carrello minimale (localStorage) + evento aml-cart-changed.
 * Checkout: opzionale mappa globale AML_STRIPE_PAYMENT_LINK_BY_SKU { sku: "https://buy.stripe.com/..." }.
 * Pulsanti fuori dalla card: data-cart-source="id" punta a #id di .product-card o .pricing-card.
 */
(function (global) {
    'use strict';

    const STORAGE_KEY = 'aml-cart-v1';
    const EVT = 'aml-cart-changed';
    var flashAddedTimer = null;
    var liveRegionClearTimer = null;

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
            document.dispatchEvent(
                new CustomEvent(EVT, {
                    detail,
                    bubbles: true,
                })
            );
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
        nodes.forEach(function (b) {
            b.classList.add('is-added');
        });
        flashAddedTimer = setTimeout(function () {
            nodes.forEach(function (b) {
                b.classList.remove('is-added');
            });
            flashAddedTimer = null;
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

    function bindAddButtons(scopeRoot) {
        const scope = scopeRoot || document;
        scope.querySelectorAll('[data-cart-add]').forEach((btn) => {
            if (btn.dataset.amlCartBound) return;
            btn.dataset.amlCartBound = '1';
            btn.addEventListener('click', () => {
                const lineRoot = resolveLineRoot(btn);
                if (!lineRoot) return;
                const line = lineRoot.classList.contains('product-card')
                    ? lineFromProductCard(lineRoot)
                    : lineFromProductContext(lineRoot);
                if (!line) return;
                const next = mergeAdd(readLines(), line);
                writeLines(next);
                dispatch(next);
                announceCartAdded();
                flashCartButtonsForSource(lineRoot);
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
                const stepper = document.createElement('div');
                stepper.className = 'aml-cart-qty-stepper';

                const btnMinus = document.createElement('button');
                btnMinus.type = 'button';
                btnMinus.className = 'aml-cart-qty-btn aml-cart-qty-btn--minus';
                btnMinus.setAttribute('data-sku-qty', l.sku);
                btnMinus.setAttribute('aria-label', qtyMinusAria + ' ' + l.name);
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
                inp.setAttribute('aria-label', qtyAria + ': ' + l.name);

                const btnPlus = document.createElement('button');
                btnPlus.type = 'button';
                btnPlus.className = 'aml-cart-qty-btn aml-cart-qty-btn--plus';
                btnPlus.setAttribute('data-sku-qty', l.sku);
                btnPlus.setAttribute('aria-label', qtyPlusAria + ' ' + l.name);
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
            tbody.addEventListener('change', (e) => {
                const t = e.target;
                if (!t || !t.classList || !t.classList.contains('aml-cart-qty')) return;
                const sku = t.getAttribute('data-sku');
                setQuantity(sku, t.value);
            });
            tbody.addEventListener('click', (e) => {
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
