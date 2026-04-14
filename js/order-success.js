/**
 * ES module: strict mode implicito; note solo testo statico / URL.
 */
import { pageLang } from './page-lang.js';

const LANG = pageLang();

const STR = {
  it: {
    session:
      'Parametro sessione Stripe rilevato. La verifica lato server (sessione + D1) sarà attiva in Fase 4: non mostrare dati sensibili finché il webhook non conferma il pagamento.',
  },
  en: {
    session:
      'Stripe session parameter detected. Server-side verification (session + D1) arrives in Phase 4: do not show sensitive data until the webhook confirms payment.',
  },
  de: {
    session:
      'Stripe-Sitzungsparameter erkannt. Serverseitige Prüfung (Session + D1) folgt in Phase 4: keine sensiblen Daten anzeigen, bis der Webhook die Zahlung bestätigt.',
  },
  fr: {
    session:
      'Paramètre de session Stripe détecté. La vérification côté serveur (session + D1) arrive en phase 4 : n\u2019affichez pas de données sensibles tant que le webhook n\u2019a pas confirmé le paiement.',
  },
  es: {
    session:
      'Parámetro de sesión de Stripe detectado. La verificación en servidor (sesión + D1) llegará en la fase 4: no muestre datos sensibles hasta que el webhook confirme el pago.',
  },
};

/* ── Animated check icon ──────────────────────────────────────────────────── */

function injectSuccessIcon() {
  const main = document.querySelector('main');
  const h1 = main?.querySelector('h1');
  // Ottimizzazione: idempotenza se lo script viene rivalutato
  if (!h1 || main?.querySelector('.success-icon-wrap')) return;

  const wrap = document.createElement('div');
  wrap.className = 'success-icon-wrap';

  const circle = document.createElement('div');
  circle.className = 'success-icon-circle';
  circle.innerHTML = `
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path class="success-check-path" d="M5 13l4 4L19 7"/>
    </svg>`;

  wrap.appendChild(circle);
  main.insertBefore(wrap, h1);
}

/* ── Session note ─────────────────────────────────────────────────────────── */

const url = new URL(window.location.href);
const sid = url.searchParams.get('session_id');
const el = document.getElementById('session-note');
const sessionCopy = STR[LANG]?.session ?? STR.en.session;
if (sid && el) {
  el.textContent = sessionCopy;
  el.removeAttribute('hidden');
}

injectSuccessIcon();
