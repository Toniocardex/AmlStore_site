/**
 * Verifica carrello con il server e rendering tabella righe (checkout).
 * Beni digitali: qty sempre 1 — tabella solo Articolo + Importo (niente quantità/prezzo duplicati).
 * ES module: strict mode implicito; testi dinamici solo via textContent (no innerHTML su dati).
 */

import { getCart } from './cart.js';
import { moneyLocale } from './page-lang.js';

const EMPTY_CART_SVG =
  '<svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>';

function clearChildren(el) {
  while (el.firstChild) {
    el.removeChild(el.firstChild);
  }
}

/**
 * Stato vuoto checkout: markup statico SVG + copy da i18n (textContent, no interpolazione HTML).
 * @param {HTMLElement} linesWrapEl
 * @param {string} langRoot
 * @param {{ empty: string, emptyLink: string }} t
 */
function renderCheckoutEmptyState(linesWrapEl, langRoot, t) {
  clearChildren(linesWrapEl);
  const wrap = document.createElement('div');
  wrap.className = 'empty-state';
  const holder = document.createElement('div');
  holder.innerHTML = EMPTY_CART_SVG;
  const svg = holder.firstElementChild;
  if (svg) wrap.appendChild(svg);
  const p = document.createElement('p');
  p.textContent = t.empty;
  wrap.appendChild(p);
  const a = document.createElement('a');
  a.className = 'btn btn-primary';
  a.href = langRoot;
  a.textContent = t.emptyLink;
  wrap.appendChild(a);
  linesWrapEl.appendChild(wrap);
}

/**
 * @param {'it'|'en'|'de'|'fr'|'es'} lang
 * @param {number} cents
 * @param {string} [cur]
 */
function formatLineMoney(lang, cents, cur) {
  try {
    return new Intl.NumberFormat(moneyLocale(lang), {
      style: 'currency',
      currency: cur || 'EUR',
    }).format(cents / 100);
  } catch {
    return `${(cents / 100).toFixed(2)} ${cur || 'EUR'}`;
  }
}

/**
 * @param {{
 *   lang: 'it'|'en'|'de'|'fr'|'es',
 *   t: {
 *     loadErr: string,
 *     empty: string,
 *     emptyLink: string,
 *     tableHeaders: string[],
 *     totalLabel: string,
 *     lineShipSuffix?: string,
 *   },
 *   statusEl: HTMLElement,
 *   linesWrapEl: HTMLElement,
 *   formEl: HTMLFormElement | null,
 *   footerEl: HTMLElement | null,
 * }} opts
 */
export async function refreshServerCartLines(opts) {
  const { lang, t, statusEl, linesWrapEl, formEl, footerEl } = opts;
  const langRoot = `/${lang}/`;

  const cart = getCart();
  linesWrapEl.removeAttribute('hidden');

  if (cart.lines.length === 0) {
    try {
      renderCheckoutEmptyState(linesWrapEl, langRoot, t);
    } catch {
      clearChildren(linesWrapEl);
    }
    statusEl.textContent = '';
    statusEl.classList.remove('is-error');
    if (formEl) {
      formEl.hidden = true;
      formEl.removeAttribute('data-verified');
      delete formEl.dataset.linesJson;
      delete formEl.dataset.needsShipping;
      delete formEl.dataset.hasDigital;
    }
    if (footerEl) footerEl.hidden = true;
    return;
  }

  try {
    const res = await fetch('/api/cart-verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        lang,
        items: cart.lines.map((l) => ({ slug: l.slug, qty: l.qty })),
      }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      statusEl.textContent = t.loadErr;
      statusEl.classList.add('is-error');
      if (formEl) {
        formEl.hidden = true;
        formEl.removeAttribute('data-verified');
        delete formEl.dataset.linesJson;
        delete formEl.dataset.needsShipping;
        delete formEl.dataset.hasDigital;
      }
      if (footerEl) footerEl.hidden = true;
      return;
    }

    const lines = data.lines || [];
    clearChildren(linesWrapEl);
    const th = t.tableHeaders;

    const tableWrap = document.createElement('div');
    tableWrap.className = 'order-table-wrap';
    const table = document.createElement('table');
    table.className = 'order-table';

    const thead = document.createElement('thead');
    const trHead = document.createElement('tr');
    for (const h of th) {
      const thEl = document.createElement('th');
      thEl.textContent = h;
      trHead.appendChild(thEl);
    }
    thead.appendChild(trHead);
    const tbody = document.createElement('tbody');

    for (const ln of lines) {
      const tr = document.createElement('tr');

      const tdTitle = document.createElement('td');
      const baseTitle =
        typeof ln.title === 'string' ? ln.title : ln.title != null ? String(ln.title) : '';
      const rawF = typeof ln.fulfillment === 'string' ? ln.fulfillment.trim().toLowerCase() : '';
      const isPhysical = rawF === 'physical';
      const shipTag = isPhysical && t.lineShipSuffix ? ` ${t.lineShipSuffix}` : '';
      tdTitle.textContent = baseTitle + shipTag;

      const cents = typeof ln.price_cents === 'number' ? ln.price_cents : 0;
      const cur = typeof ln.currency === 'string' ? ln.currency : 'EUR';
      const qty = typeof ln.qty === 'number' && ln.qty > 0 ? ln.qty : 1;
      const tdAmount = document.createElement('td');
      tdAmount.className = 'order-line-amount';
      tdAmount.textContent = formatLineMoney(lang, cents * qty, cur);

      tr.append(tdTitle, tdAmount);
      tbody.appendChild(tr);
    }

    table.append(thead, tbody);
    tableWrap.appendChild(table);
    linesWrapEl.appendChild(tableWrap);

    const totalP = document.createElement('p');
    totalP.className = 'order-total';
    const strong = document.createElement('strong');
    strong.textContent = `${t.totalLabel}:`;
    totalP.appendChild(strong);
    totalP.appendChild(document.createTextNode(' '));
    totalP.appendChild(
      document.createTextNode(
        formatLineMoney(
          lang,
          typeof data.total_cents === 'number' ? data.total_cents : 0,
          typeof data.currency === 'string' ? data.currency : 'EUR'
        )
      )
    );
    linesWrapEl.appendChild(totalP);

    statusEl.textContent = '';
    statusEl.classList.remove('is-error');
    if (formEl) {
      formEl.hidden = false;
      formEl.dataset.verified = '1';
      try {
        formEl.dataset.linesJson = JSON.stringify(
          lines.map((l) => ({ slug: l.slug, qty: l.qty }))
        );
      } catch {
        delete formEl.dataset.linesJson;
      }
      formEl.dataset.needsShipping = data.needs_shipping === true ? '1' : '0';
      formEl.dataset.hasDigital = data.has_digital === true ? '1' : '0';
    }
    if (footerEl) footerEl.hidden = false;
  } catch {
    statusEl.textContent = t.loadErr;
    statusEl.classList.add('is-error');
    if (formEl) {
      formEl.hidden = true;
      formEl.removeAttribute('data-verified');
      delete formEl.dataset.linesJson;
      delete formEl.dataset.needsShipping;
      delete formEl.dataset.hasDigital;
    }
    if (footerEl) footerEl.hidden = true;
  }
}
