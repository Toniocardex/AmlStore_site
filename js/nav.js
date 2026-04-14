/**
 * ES module: strict mode implicito; badge e tema senza binding globali.
 */
import { cartItemCount } from './cart.js';
import { pageLang } from './page-lang.js';

const THEME_KEY = 'aml-theme';

const LANG = pageLang();

function getStoredTheme() {
  try {
    const v = localStorage.getItem(THEME_KEY);
    return v === 'light' || v === 'dark' ? v : null;
  } catch {
    return null;
  }
}

function getEffectiveTheme() {
  const attr = document.documentElement.getAttribute('data-theme');
  if (attr === 'light' || attr === 'dark') return attr;
  return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
}

/* ── Theme toggle ─────────────────────────────────────────────────────────── */
/* Il <button id="theme-toggle"> è HTML statico.
   Il CSS guida sole/luna via html[data-theme].
   Qui gestiamo solo: click handler + aria-label aggiornato. */

const THEME_LABELS = {
  it: { toLight: 'Passa al tema chiaro', toDark: 'Passa al tema scuro' },
  en: { toLight: 'Switch to light theme', toDark: 'Switch to dark theme' },
  de: { toLight: 'Zum hellen Modus wechseln', toDark: 'Zum dunklen Modus wechseln' },
  fr: { toLight: 'Passer au thème clair', toDark: 'Passer au thème sombre' },
  es: { toLight: 'Cambiar a tema claro', toDark: 'Cambiar a tema oscuro' },
};

function initThemeToggle() {
  const btn = document.getElementById('theme-toggle');
  if (!btn) return;
  const L = THEME_LABELS[LANG] || THEME_LABELS.en;

  function syncAriaLabel() {
    btn.setAttribute('aria-label', getEffectiveTheme() === 'dark' ? L.toLight : L.toDark);
  }

  btn.addEventListener('click', () => {
    const next = getEffectiveTheme() === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem(THEME_KEY, next); } catch (_) {}
    syncAriaLabel();
  });

  window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', () => {
    if (!getStoredTheme()) {
      document.documentElement.removeAttribute('data-theme');
      syncAriaLabel();
    }
  });

  syncAriaLabel();
}

/* ── Cart badge ───────────────────────────────────────────────────────────── */

let lastCartItemCount = null;

function triggerCartNavPulse() {
  try {
    const link = document.getElementById('cart-badge')?.closest('a.user-nav-link');
    if (!link) return;
    link.classList.remove('cart-nav-pulse');
    void link.offsetWidth;
    link.classList.add('cart-nav-pulse');
    window.setTimeout(() => link.classList.remove('cart-nav-pulse'), 600);
  } catch {
    /* DOM / reflow non deve bloccare la navigazione */
  }
}

function refreshBadge() {
  try {
    const wrap = document.getElementById('cart-badge');
    if (!wrap) return;
    const n = cartItemCount();
    if (lastCartItemCount !== null && n > lastCartItemCount) triggerCartNavPulse();
    lastCartItemCount = n;

    const labels = {
      it: 'articoli nel carrello',
      en: 'items in cart',
      de: 'Artikel im Warenkorb',
      fr: 'articles dans le panier',
      es: 'artículos en el carrito',
    };

    if (n > 0) {
      wrap.textContent = String(n);
      wrap.removeAttribute('hidden');
      wrap.setAttribute('aria-label', `${n} ${labels[LANG] || labels.en}`);
    } else {
      wrap.setAttribute('hidden', '');
      wrap.textContent = '';
      wrap.removeAttribute('aria-label');
    }
  } catch {
    /* localStorage / DOM: evita crash pagina su badge */
  }
}

/* ── Sticky header scroll ─────────────────────────────────────────────────── */

function initStickyHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 10);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

/* ── Boot ─────────────────────────────────────────────────────────────────── */

initThemeToggle();
initStickyHeaderScroll();
window.addEventListener('aml-cart-change', refreshBadge);
refreshBadge();
