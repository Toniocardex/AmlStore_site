/**
 * Scheda prodotto statica: legge payload JSON e usa cart.js (stesso storage del catalogo).
 * Barra CTA mobile: visibile quando il pulsante principale esce dal viewport (solo sotto i 768px).
 */
import { addToCart } from './cart.js';

function main() {
  const payloadEl = document.getElementById('product-payload');
  const mainBtn = document.getElementById('product-add-cart');
  if (!payloadEl || !mainBtn) return;

  let payload;
  try {
    payload = JSON.parse(payloadEl.textContent || '{}');
  } catch {
    return;
  }

  const slug = typeof payload.slug === 'string' ? payload.slug : '';
  const title = typeof payload.title === 'string' ? payload.title : '';
  const price_cents =
    typeof payload.price_cents === 'number' && Number.isFinite(payload.price_cents)
      ? Math.round(payload.price_cents)
      : 0;
  const currency = typeof payload.currency === 'string' ? payload.currency : 'EUR';
  const rawF = typeof payload.fulfillment === 'string' ? payload.fulfillment.trim().toLowerCase() : '';
  const fulfillment = rawF === 'physical' ? 'physical' : 'digital';

  if (!slug || !title) return;

  const stickyBtn = document.getElementById('product-add-cart-sticky');
  const stickyBar = document.getElementById('product-sticky-cta');

  const pulseDisabled = () => {
    const btns = [mainBtn, stickyBtn].filter(Boolean);
    for (const b of btns) {
      b.disabled = true;
    }
    window.setTimeout(() => {
      for (const b of btns) {
        b.disabled = false;
      }
    }, 520);
  };

  const add = () => {
    try {
      addToCart({ slug, title, price_cents, currency, fulfillment });
    } catch {
      /* ignore */
    }
    pulseDisabled();
  };

  mainBtn.addEventListener('click', add);
  if (stickyBtn) stickyBtn.addEventListener('click', add);

  if (!stickyBar || typeof IntersectionObserver === 'undefined') return;

  const mq = window.matchMedia('(max-width: 767px)');

  const setStickyVisible = (visible) => {
    stickyBar.classList.toggle('is-visible', visible);
    document.body.classList.toggle('product-sticky-cta-on', visible);
    if ('inert' in stickyBar) {
      stickyBar.inert = !visible;
    }
  };

  let io;

  const bindObserver = () => {
    if (io) {
      io.disconnect();
      io = undefined;
    }
    if (!mq.matches) {
      setStickyVisible(false);
      return;
    }
    io = new IntersectionObserver(
      ([e]) => {
        if (!e) return;
        setStickyVisible(!e.isIntersecting);
      },
      { root: null, rootMargin: '0px 0px -40px 0px', threshold: 0 }
    );
    io.observe(mainBtn);
  };

  bindObserver();
  mq.addEventListener('change', bindObserver);
}

main();
