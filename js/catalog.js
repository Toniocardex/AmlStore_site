/**
 * ES module: strict mode implicito; catalogo da API solo via textContent (no innerHTML su titoli/descrizioni).
 */
import { addToCart } from './cart.js';
import { moneyLocale, pageLang } from './page-lang.js';

const EMPTY_CATALOG_SVG =
  '<svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>';

const STR = {
  it: {
    loading: 'Caricamento catalogo…',
    unavailable: 'Catalogo non disponibile:',
    empty: 'Nessun prodotto attivo al momento.',
    emptyHint: 'Torna a controllare presto oppure contattaci.',
    networkPrefix: 'Rete o server:',
    httpError: (n) => `Errore HTTP ${n}`,
    loadFailed: 'Impossibile caricare il catalogo.',
    addCart: 'Aggiungi al carrello',
    trust: [
      'Download immediato',
      'Pagamento sicuro',
      'Supporto incluso',
    ],
    shipBadge: 'Prodotto fisico: al checkout servirà un indirizzo di spedizione.',
  },
  en: {
    loading: 'Loading catalog…',
    unavailable: 'Catalog unavailable:',
    empty: 'No active products at the moment.',
    emptyHint: 'Check back soon or get in touch.',
    networkPrefix: 'Network or server:',
    httpError: (n) => `HTTP error ${n}`,
    loadFailed: 'Could not load the catalog.',
    addCart: 'Add to cart',
    trust: [
      'Instant download',
      'Secure payment',
      'Support included',
    ],
    shipBadge: 'Physical item: a shipping address is required at checkout.',
  },
  de: {
    loading: 'Katalog wird geladen…',
    unavailable: 'Katalog nicht verfügbar:',
    empty: 'Derzeit keine aktiven Produkte.',
    emptyHint: 'Schauen Sie bald wieder vorbei oder kontaktieren Sie uns.',
    networkPrefix: 'Netzwerk oder Server:',
    httpError: (n) => `HTTP-Fehler ${n}`,
    loadFailed: 'Katalog konnte nicht geladen werden.',
    addCart: 'In den Warenkorb',
    trust: [
      'Sofortiger Download',
      'Sichere Zahlung',
      'Support inklusive',
    ],
    shipBadge: 'Physisches Produkt: Lieferadresse an der Kasse erforderlich.',
  },
  fr: {
    loading: 'Chargement du catalogue…',
    unavailable: 'Catalogue indisponible :',
    empty: 'Aucun produit actif pour le moment.',
    emptyHint: 'Revenez bientôt ou contactez-nous.',
    networkPrefix: 'Réseau ou serveur :',
    httpError: (n) => `Erreur HTTP ${n}`,
    loadFailed: 'Impossible de charger le catalogue.',
    addCart: 'Ajouter au panier',
    trust: [
      'Téléchargement immédiat',
      'Paiement sécurisé',
      'Support inclus',
    ],
    shipBadge: 'Produit physique : une adresse de livraison sera demandée au paiement.',
  },
  es: {
    loading: 'Cargando catálogo…',
    unavailable: 'Catálogo no disponible:',
    empty: 'No hay productos activos en este momento.',
    emptyHint: 'Vuelva pronto o contáctenos.',
    networkPrefix: 'Red o servidor:',
    httpError: (n) => `Error HTTP ${n}`,
    loadFailed: 'No se pudo cargar el catálogo.',
    addCart: 'Añadir al carrito',
    trust: [
      'Descarga inmediata',
      'Pago seguro',
      'Soporte incluido',
    ],
    shipBadge: 'Producto físico: en el checkout se pedirá dirección de envío.',
  },
};

/* Deterministic pastel gradient per slug (hashed from char codes) */
const CARD_GRADIENTS = [
  ['#3d8bfd', '#6366f1'],
  ['#8b5cf6', '#a855f7'],
  ['#06b6d4', '#3d8bfd'],
  ['#10b981', '#06b6d4'],
  ['#f59e0b', '#ef4444'],
  ['#ec4899', '#8b5cf6'],
];

const CARD_ICONS = ['📦', '📄', '🛡️', '⚡', '🔧', '🗂️'];

function slugHash(slug) {
  let h = 0;
  for (let i = 0; i < slug.length; i++) h = (h * 31 + slug.charCodeAt(i)) | 0;
  return Math.abs(h);
}

function clearChildren(el) {
  while (el.firstChild) {
    el.removeChild(el.firstChild);
  }
}

/** @param {unknown} p @returns {{ slug: string, title: string, description: string, price_cents: number, currency: string, fulfillment: 'digital'|'physical', cover_image: string } | null} */
function normalizeProduct(p) {
  if (!p || typeof p !== 'object') return null;
  const o = /** @type {Record<string, unknown>} */ (p);
  if (typeof o.slug !== 'string' || !o.slug) return null;
  const title =
    typeof o.title === 'string' ? o.title : o.title != null ? String(o.title) : '';
  const description = typeof o.description === 'string' ? o.description : '';
  const raw = o.price_cents;
  const price_cents =
    typeof raw === 'number' && Number.isFinite(raw) ? Math.round(raw) : 0;
  const currency = typeof o.currency === 'string' ? o.currency : 'EUR';
  const rawF = typeof o.fulfillment === 'string' ? o.fulfillment.trim().toLowerCase() : '';
  const fulfillment = rawF === 'physical' ? 'physical' : 'digital';
  const ci = typeof o.cover_image === 'string' ? o.cover_image.trim() : '';
  const cover_image =
    ci && ci.startsWith('/img/products/') && !ci.includes('..') ? ci : '';
  return { slug: o.slug, title, description, price_cents, currency, fulfillment, cover_image };
}

function formatMoney(cents, currency, lang) {
  const cur = currency || 'EUR';
  try {
    return new Intl.NumberFormat(moneyLocale(lang), {
      style: 'currency',
      currency: cur,
    }).format(cents / 100);
  } catch {
    return `${(cents / 100).toFixed(2)} ${cur}`;
  }
}

function buildSkeleton(count) {
  const root = document.createElement('div');
  root.className = 'catalog-skeleton';
  root.setAttribute('aria-hidden', 'true');
  for (let i = 0; i < count; i += 1) {
    const card = document.createElement('div');
    card.className = 'catalog-skeleton__card';
    const visual = document.createElement('div');
    visual.className = 'catalog-skeleton__line';
    visual.style.cssText = 'height:5.5rem;border-radius:8px;margin:-1.25rem -1.35rem 1rem;';
    const l1 = document.createElement('div');
    l1.className = 'catalog-skeleton__line catalog-skeleton__line--short';
    const l2 = document.createElement('div');
    l2.className = 'catalog-skeleton__line catalog-skeleton__line--title';
    const l3 = document.createElement('div');
    l3.className = 'catalog-skeleton__line catalog-skeleton__line--text';
    const l4 = document.createElement('div');
    l4.className = 'catalog-skeleton__line catalog-skeleton__line--text catalog-skeleton__line--narrow';
    const btn = document.createElement('div');
    btn.className = 'catalog-skeleton__btn';
    card.append(visual, l1, l2, l3, l4, btn);
    root.appendChild(card);
  }
  return root;
}

function renderCatalog(container, products, lang) {
  const t = STR[lang];
  clearChildren(container);
  let i = 0;
  for (const raw of products) {
    const p = normalizeProduct(raw);
    if (!p) continue;
    const li = document.createElement('li');
    li.className = 'catalog-item-enter';
    li.style.setProperty('--stagger', `${Math.min(i * 0.055, 0.55)}s`);

    /* Visual header: immagine statica /img/products/… oppure gradiente + icona */
    const h = slugHash(p.slug);
    const [c1, c2] = CARD_GRADIENTS[h % CARD_GRADIENTS.length];
    const icon = CARD_ICONS[h % CARD_ICONS.length];

    const visual = document.createElement('div');
    visual.className = 'catalog-card-visual';
    visual.setAttribute('aria-hidden', 'true');

    const paintGradientIcon = () => {
      while (visual.firstChild) visual.removeChild(visual.firstChild);
      visual.classList.remove('catalog-card-visual--photo');
      visual.style.background = `linear-gradient(135deg, ${c1}33 0%, ${c2}22 100%)`;
      const iconSpan = document.createElement('span');
      iconSpan.textContent = icon;
      visual.appendChild(iconSpan);
    };

    if (p.cover_image) {
      visual.classList.add('catalog-card-visual--photo');
      visual.style.background = 'transparent';
      const img = document.createElement('img');
      img.className = 'catalog-card-visual__img';
      img.src = p.cover_image;
      img.alt = '';
      img.width = 880;
      img.height = 308;
      img.decoding = 'async';
      img.loading = 'lazy';
      img.addEventListener('error', () => {
        paintGradientIcon();
      });
      visual.appendChild(img);
    } else {
      paintGradientIcon();
    }

    const slug = document.createElement('p');
    slug.className = 'slug';
    slug.textContent = p.slug;

    const h2 = document.createElement('h2');
    const titleLink = document.createElement('a');
    titleLink.className = 'catalog-card-title-link';
    titleLink.href = `/${lang}/products/${encodeURIComponent(p.slug)}.html`;
    titleLink.textContent = p.title;
    h2.appendChild(titleLink);

    const desc = document.createElement('p');
    desc.textContent = p.description || '';

    let shipNote = null;
    if (p.fulfillment === 'physical') {
      shipNote = document.createElement('p');
      shipNote.className = 'catalog-fulfillment';
      shipNote.textContent = t.shipBadge;
    }

    const price = document.createElement('p');
    price.className = 'price';
    price.textContent = formatMoney(p.price_cents, p.currency, lang);

    const actions = document.createElement('div');
    actions.className = 'catalog-actions';
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'btn btn-primary btn-catalog-add';
    btn.textContent = t.addCart;
    btn.addEventListener('click', () => {
      try {
        addToCart({
          slug: p.slug,
          title: p.title,
          price_cents: p.price_cents,
          currency: p.currency,
          fulfillment: p.fulfillment,
        });
      } catch {
        /* storage pieno / errore cart: non bloccare il click */
      }
      btn.disabled = true;
      window.setTimeout(() => {
        btn.disabled = false;
      }, 520);
    });
    actions.appendChild(btn);

    li.append(visual, slug, h2, desc, ...(shipNote ? [shipNote] : []), price, actions);
    container.appendChild(li);
    i += 1;
  }
}

function renderEmptyCatalog(status, t) {
  status.classList.remove('visually-hidden');
  clearChildren(status);
  const wrap = document.createElement('div');
  wrap.className = 'empty-state';
  const holder = document.createElement('div');
  holder.innerHTML = EMPTY_CATALOG_SVG;
  const svg = holder.firstElementChild;
  if (svg) wrap.appendChild(svg);
  const p1 = document.createElement('p');
  p1.textContent = t.empty;
  wrap.appendChild(p1);
  const p2 = document.createElement('p');
  p2.style.fontSize = '0.8125rem';
  p2.textContent = t.emptyHint;
  wrap.appendChild(p2);
  status.appendChild(wrap);
}

function injectTrustBar(lang) {
  const t = STR[lang];
  const hero = document.querySelector('.hero__actions');
  if (!hero) return;

  const bar = document.createElement('div');
  bar.className = 'trust-bar';
  bar.setAttribute('aria-label', 'Garanzie');

  const icons = [
    /* Download */
    `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>`,
    /* Lock */
    `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>`,
    /* Headphones */
    `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3z"/><path d="M3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>`,
  ];

  t.trust.forEach((label, idx) => {
    const item = document.createElement('span');
    item.className = 'trust-bar__item';
    const holder = document.createElement('span');
    holder.innerHTML = icons[idx];
    const svg = holder.firstElementChild;
    const lab = document.createElement('span');
    lab.textContent = label;
    if (svg) item.appendChild(svg);
    item.appendChild(lab);
    bar.appendChild(item);
  });

  hero.after(bar);
}

async function main() {
  const lang = pageLang();
  const t = STR[lang];
  const status = document.getElementById('catalog-status');
  const list = document.getElementById('catalog-list');

  if (!status || !list) return;

  injectTrustBar(lang);

  let skeleton = null;
  const removeSkeleton = () => {
    if (skeleton && skeleton.parentNode) {
      skeleton.remove();
      skeleton = null;
    }
  };

  list.setAttribute('aria-busy', 'true');
  skeleton = buildSkeleton(6);
  status.before(skeleton);
  status.textContent = t.loading;
  status.classList.add('visually-hidden');
  status.hidden = false;
  status.classList.remove('is-error');

  try {
    const res = await fetch(`/api/products?lang=${encodeURIComponent(lang)}`, {
      headers: { Accept: 'application/json' },
    });
    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      removeSkeleton();
      status.classList.remove('visually-hidden');
      const msg =
        typeof data.message === 'string'
          ? data.message
          : t.httpError(res.status);
      status.textContent = `${t.unavailable} ${msg}`;
      status.classList.add('is-error');
      return;
    }

    const products = Array.isArray(data.products) ? data.products : [];
    if (products.length === 0) {
      removeSkeleton();
      renderEmptyCatalog(status, t);
      list.hidden = true;
      return;
    }

    removeSkeleton();
    status.textContent = '';
    status.classList.remove('visually-hidden');
    status.hidden = true;

    renderCatalog(list, products, lang);
    list.hidden = false;
  } catch (e) {
    removeSkeleton();
    status.classList.remove('visually-hidden');
    status.textContent =
      e instanceof Error
        ? `${t.networkPrefix} ${e.message}`
        : t.loadFailed;
    status.classList.add('is-error');
  } finally {
    list.removeAttribute('aria-busy');
  }
}

main();
