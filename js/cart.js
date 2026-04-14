'use strict';

/**
 * Carrello lato client (Vanilla). Persistenza in localStorage.
 * Checkout (Fase 3+) ricostruirà i prezzi lato server da D1 — questo storage è solo UX.
 */

const STORAGE_KEY = 'aml_store_cart_v1';

/** @typedef {{ slug: string, title: string, price_cents: number, currency: string, qty: number, fulfillment?: 'digital'|'physical' }} CartLine */

/** @param {unknown} f */
function normFulfillment(f) {
  return f === 'physical' ? 'physical' : 'digital';
}

/** @returns {{ v: 1, lines: CartLine[] }} */
function emptyState() {
  return { v: 1, lines: [] };
}

/** @param {unknown} raw */
function normalizeState(raw) {
  if (!raw || typeof raw !== 'object' || !Array.isArray(raw.lines)) {
    return emptyState();
  }
  const lines = raw.lines
    .filter(
      (x) =>
        x &&
        typeof x.slug === 'string' &&
        typeof x.title === 'string' &&
        typeof x.price_cents === 'number' &&
        typeof x.currency === 'string' &&
        typeof x.qty === 'number' &&
        x.qty > 0
    )
    .map((x) => {
      const fulfillment = normFulfillment(/** @type {Record<string, unknown>} */ (x).fulfillment);
      const qRaw = typeof x.qty === 'number' ? x.qty : 1;
      const qty =
        fulfillment === 'physical'
          ? Math.min(99, Math.max(1, Math.floor(qRaw)))
          : 1;
      /** @type {CartLine} */
      const line = {
        slug: x.slug,
        title: x.title,
        price_cents: Math.round(x.price_cents),
        currency: x.currency,
        qty,
      };
      if (fulfillment === 'physical') line.fulfillment = 'physical';
      return line;
    });
  return { v: 1, lines };
}

export function getCart() {
  try {
    const raw = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
    return normalizeState(raw);
  } catch {
    return emptyState();
  }
}

/** @param {{ v: 1, lines: CartLine[] }} state */
export function setCart(state) {
  const next = normalizeState(state);
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  } catch {
    // Ottimizzazione: quota / navigazione privata — evita crash; stato su disco invariato
    return getCart();
  }
  try {
    window.dispatchEvent(new CustomEvent('aml-cart-change', { detail: next }));
  } catch {
    /* listener esterno raro */
  }
  return next;
}

/**
 * @param {{ slug: string, title: string, price_cents: number, currency: string, fulfillment?: 'digital'|'physical' }} item
 */
export function addToCart(item) {
  const cart = getCart();
  const fulfillment = normFulfillment(item.fulfillment);
  const i = cart.lines.findIndex((l) => l.slug === item.slug);
  if (i >= 0) {
    cart.lines[i].qty = 1;
    cart.lines[i].title = item.title;
    cart.lines[i].price_cents = item.price_cents;
    cart.lines[i].currency = item.currency;
    if (fulfillment === 'physical') cart.lines[i].fulfillment = 'physical';
    else delete cart.lines[i].fulfillment;
  } else {
    /** @type {CartLine} */
    const line = {
      slug: item.slug,
      title: item.title,
      price_cents: item.price_cents,
      currency: item.currency,
      qty: 1,
    };
    if (fulfillment === 'physical') line.fulfillment = 'physical';
    cart.lines.push(line);
  }
  return setCart(cart);
}

/** @param {string} slug */
export function removeFromCart(slug) {
  const cart = getCart();
  cart.lines = cart.lines.filter((l) => l.slug !== slug);
  return setCart(cart);
}

export function clearCart() {
  return setCart(emptyState());
}

/** Quantità totale articoli (somma qty). */
export function cartItemCount() {
  return getCart().lines.reduce((n, l) => n + l.qty, 0);
}
