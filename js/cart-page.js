/**
 * ES module: strict mode implicito (ECMA-262); nessun binding sul `window`.
 * Ottimizzazione: event delegation su #cart-list (un solo listener vs N righe).
 */
import { getCart, removeFromCart, setCart } from './cart.js';
import { moneyLocale, pageLang } from './page-lang.js';

const LANG = pageLang();
const PLACEHOLDER_IMG = '/img/favicon/icon-32.webp';

const STR = {
  it: {
    loadErr: 'Impossibile verificare il carrello con il server.',
    empty: 'Il tuo carrello è vuoto.',
    storeCta: 'Torna al catalogo',
    digitalType: 'Download digitale',
    physicalType: 'Spedizione (prodotto fisico)',
    summaryTitle: 'Riepilogo ordine',
    amountRow: 'Importo',
    total: 'Totale',
    checkoutCta: 'Procedi al checkout',
    remove: 'Rimuovi',
    removeAria: (name) => `Rimuovi ${name} dal carrello`,
    trust1: 'Pagamento sicuro',
    trust2: 'Digitale o spedizione secondo il prodotto',
    steps: ['Carrello', 'Fatturazione', 'Pagamento', 'Conferma'],
  },
  en: {
    loadErr: 'Could not verify the cart with the server.',
    empty: 'Your cart is empty.',
    storeCta: 'Back to catalog',
    digitalType: 'Digital download',
    physicalType: 'Shipping (physical item)',
    summaryTitle: 'Order summary',
    amountRow: 'Amount',
    total: 'Total',
    checkoutCta: 'Continue to checkout',
    remove: 'Remove',
    removeAria: (name) => `Remove ${name} from cart`,
    trust1: 'Secure checkout',
    trust2: 'Digital or shipping, depending on the item',
    steps: ['Cart', 'Billing', 'Payment', 'Confirm'],
  },
  de: {
    loadErr: 'Warenkorb konnte nicht mit dem Server abgeglichen werden.',
    empty: 'Ihr Warenkorb ist leer.',
    storeCta: 'Zurück zum Katalog',
    digitalType: 'Digitaler Download',
    physicalType: 'Versand (physisches Produkt)',
    summaryTitle: 'Bestellübersicht',
    amountRow: 'Betrag',
    total: 'Gesamt',
    checkoutCta: 'Weiter zur Kasse',
    remove: 'Entfernen',
    removeAria: (name) => `${name} aus dem Warenkorb entfernen`,
    trust1: 'Sichere Zahlung',
    trust2: 'Digital oder Versand je nach Artikel',
    steps: ['Warenkorb', 'Abrechnung', 'Zahlung', 'Bestätigung'],
  },
  fr: {
    loadErr: 'Impossible de vérifier le panier avec le serveur.',
    empty: 'Votre panier est vide.',
    storeCta: 'Retour au catalogue',
    digitalType: 'Téléchargement numérique',
    physicalType: 'Livraison (produit physique)',
    summaryTitle: 'Récapitulatif',
    amountRow: 'Montant',
    total: 'Total',
    checkoutCta: 'Passer au paiement',
    remove: 'Supprimer',
    removeAria: (name) => `Retirer ${name} du panier`,
    trust1: 'Paiement sécurisé',
    trust2: 'Numérique ou livraison selon l’article',
    steps: ['Panier', 'Facturation', 'Paiement', 'Confirmation'],
  },
  es: {
    loadErr: 'No se pudo verificar el carrito con el servidor.',
    empty: 'El carrito está vacío.',
    storeCta: 'Volver al catálogo',
    digitalType: 'Descarga digital',
    physicalType: 'Envío (producto físico)',
    summaryTitle: 'Resumen',
    amountRow: 'Importe',
    total: 'Total',
    checkoutCta: 'Ir al checkout',
    remove: 'Eliminar',
    removeAria: (name) => `Quitar ${name} del carrito`,
    trust1: 'Pago seguro',
    trust2: 'Digital o envío según el artículo',
    steps: ['Carrito', 'Facturación', 'Pago', 'Confirmación'],
  },
};

const t = STR[LANG];

function formatMoney(cents, cur) {
  try {
    return new Intl.NumberFormat(moneyLocale(LANG), {
      style: 'currency',
      currency: cur || 'EUR',
    }).format(cents / 100);
  } catch {
    return `${(cents / 100).toFixed(2)} ${cur || 'EUR'}`;
  }
}

function injectSteps(activeIndex) {
  const main = document.querySelector('main');
  const h1 = main?.querySelector('h1');
  if (!h1 || main?.querySelector('.checkout-steps')) return;

  const ol = document.createElement('ol');
  ol.className = 'checkout-steps';
  ol.setAttribute('aria-label', t.steps.join(' › '));

  t.steps.forEach((label, i) => {
    const li = document.createElement('li');
    li.setAttribute('data-n', String(i + 1));
    li.textContent = label;
    if (i + 1 < activeIndex) li.className = 'step--done';
    else if (i + 1 === activeIndex) li.className = 'step--active';

    if (i < t.steps.length - 1) {
      const sep = document.createElement('span');
      sep.className = 'checkout-steps__sep';
      sep.setAttribute('aria-hidden', 'true');
      ol.appendChild(li);
      ol.appendChild(sep);
    } else {
      ol.appendChild(li);
    }
  });

  main.insertBefore(ol, h1);
}

function clearChildren(el) {
  while (el.firstChild) {
    el.removeChild(el.firstChild);
  }
}

/** @param {string} slug @param {string} title */
function safeLineStrings(slug, title) {
  const s = typeof slug === 'string' ? slug : '';
  const n = typeof title === 'string' ? title : title != null ? String(title) : '';
  return { slug: s, title: n };
}

function bindCartRemoveDelegation(listRoot) {
  listRoot.addEventListener('click', (ev) => {
    const tEl = /** @type {HTMLElement} */ (ev.target);
    const btn = tEl.closest?.('.btn-remove-cart');
    if (!btn || !listRoot.contains(btn)) return;
    const art = btn.closest('.cart-item');
    const slug = art?.getAttribute('data-slug');
    if (!slug) return;
    try {
      removeFromCart(slug);
      void renderCart();
    } catch {
      /* removeFromCart / render non devono bloccare l’interazione */
    }
  });
}

async function renderCart() {
  const listEl = document.getElementById('cart-list');
  const emptyEl = document.getElementById('cart-empty-state');
  const summaryEl = document.getElementById('cart-summary-section');
  const totEl = document.getElementById('cart-total');
  const statusEl = document.getElementById('cart-page-status');
  const tmpl = document.getElementById('cart-item-template');
  const storeLink = document.getElementById('cart-empty-store-link');

  if (!listEl || !emptyEl || !summaryEl || !totEl || !statusEl || !tmpl || !storeLink) return;

  if (!listEl.dataset.delegationBound) {
    listEl.dataset.delegationBound = '1';
    bindCartRemoveDelegation(listEl);
  }

  const cart = getCart();
  clearChildren(listEl);
  statusEl.textContent = '';
  statusEl.classList.remove('is-error');
  statusEl.hidden = true;

  /* Evita flash “carrello vuoto” se ci sono righe (prima della risposta API). */
  if (cart.lines.length > 0) {
    emptyEl.hidden = true;
  }

  if (cart.lines.length === 0) {
    emptyEl.hidden = false;
    summaryEl.hidden = true;
    totEl.textContent = formatMoney(0, 'EUR');
    return;
  }

  emptyEl.hidden = true;
  summaryEl.hidden = false;

  try {
    const res = await fetch('/api/cart-verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        lang: LANG,
        items: cart.lines.map((l) => ({ slug: l.slug, qty: l.qty })),
      }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      statusEl.textContent = t.loadErr;
      statusEl.classList.add('is-error');
      statusEl.hidden = false;
      summaryEl.hidden = true;
      return;
    }

    const lines = data.lines || [];
    const fragment = document.createDocumentFragment();
    const cur = data.currency || 'EUR';

    for (const ln of lines) {
      const { slug, title } = safeLineStrings(ln.slug, ln.title);
      if (!slug) continue;

      const node = tmpl.content.cloneNode(true);
      const rootArticle = node.querySelector('.cart-item');
      const img = node.querySelector('.cart-item-img');
      const nameEl = node.querySelector('.cart-item-name');
      const typeEl = node.querySelector('.cart-item-type');
      const priceEl = node.querySelector('.cart-item-price');
      const amountLabelEl = node.querySelector('.cart-item-amount-label');
      const btn = node.querySelector('.btn-remove-cart');

      if (rootArticle) rootArticle.setAttribute('data-slug', slug);

      if (img) {
        img.src = PLACEHOLDER_IMG;
        img.alt = '';
        img.width = 80;
        img.height = 80;
      }
      if (nameEl) nameEl.textContent = title;
      if (typeEl) {
        const rawF =
          typeof ln.fulfillment === 'string' ? ln.fulfillment.trim().toLowerCase() : '';
        typeEl.textContent = rawF === 'physical' ? t.physicalType : t.digitalType;
      }
      if (amountLabelEl) amountLabelEl.textContent = t.amountRow;
      const qty = typeof ln.qty === 'number' && ln.qty > 0 ? ln.qty : 1;
      const cents = typeof ln.price_cents === 'number' ? ln.price_cents : 0;
      const curLn = typeof ln.currency === 'string' ? ln.currency : 'EUR';
      const lineTotal = cents * qty;
      if (priceEl) priceEl.textContent = formatMoney(lineTotal, curLn);
      if (btn) {
        btn.textContent = t.remove;
        btn.setAttribute('aria-label', t.removeAria(title));
      }
      fragment.appendChild(node);
    }

    listEl.appendChild(fragment);

    totEl.textContent = formatMoney(data.total_cents, cur);
  } catch {
    statusEl.textContent = t.loadErr;
    statusEl.classList.add('is-error');
    statusEl.hidden = false;
    summaryEl.hidden = true;
  }
}

injectSteps(1);

window.addEventListener('aml-cart-change', () => {
  void renderCart();
});

void renderCart();
