/**
 * ES module: strict mode implicito; messaggi server solo via textContent.
 */
import { clearCart } from './cart.js';
import { pageLang } from './page-lang.js';
import { refreshServerCartLines } from './cart-lines.js';

const LANG = pageLang();

const STR = {
  it: {
    loadErr: 'Impossibile verificare il carrello con il server.',
    empty: 'Il carrello è vuoto.',
    emptyLink: 'Torna al catalogo',
    submit: 'Registra ordine (pagamento Stripe in Fase 4)',
    submitting: 'Invio in corso…',
    success: (id) =>
      `Ordine #${id} registrato. Il pagamento con carta sarà attivato nella prossima fase. Il carrello è stato svuotato.`,
    errGeneric: 'Richiesta non riuscita.',
    valEmail: "Inserisci un'email valida.",
    valFields: 'Controlla i campi evidenziati.',
    tableHeaders: ['Articolo', 'Importo'],
    totalLabel: 'Totale',
    steps: ['Carrello', 'Fatturazione', 'Pagamento', 'Conferma'],
    hintEmail: 'Riceverai la conferma su questo indirizzo.',
    hintSdi: 'Codice Destinatario a 7 caratteri (es. ABCDE12). Usa 0000000 se non disponibile.',
    hintPec: 'Obbligatoria se il codice SDI è 0000000.',
    errEmail: "Inserisci un'email valida.",
    errSdi: 'Il codice SDI deve essere di 7 caratteri alfanumerici.',
    errPec: "Inserisci un'email PEC valida.",
    lineShipSuffix: '(consegna fisica)',
    bannerMixed:
      "Carrello misto: l'indirizzo qui sotto serve per i prodotti fisici; i digitali restano sulla tua email.",
    bannerShippingOnly:
      "Inserisci l'indirizzo per la consegna dei prodotti fisici.",
    addressLegend: 'Indirizzo',
    addressLegendShip: 'Indirizzo di spedizione',
  },
  en: {
    loadErr: 'Could not verify the cart with the server.',
    empty: 'Your cart is empty.',
    emptyLink: 'Back to catalog',
    submit: 'Place order (Stripe payment in Phase 4)',
    submitting: 'Sending…',
    success: (id) =>
      `Order #${id} recorded. Card payment will be enabled in the next phase. Your cart has been cleared.`,
    errGeneric: 'Request failed.',
    valEmail: 'Enter a valid email address.',
    valFields: 'Please fix the highlighted fields.',
    tableHeaders: ['Item', 'Amount'],
    totalLabel: 'Total',
    steps: ['Cart', 'Billing', 'Payment', 'Confirm'],
    hintEmail: 'You will receive the confirmation at this address.',
    hintSdi: '7-character Recipient Code (e.g. ABCDE12). Use 0000000 if not available.',
    hintPec: 'Required if SDI code is 0000000.',
    errEmail: 'Enter a valid email address.',
    errSdi: 'SDI code must be exactly 7 alphanumeric characters.',
    errPec: 'Enter a valid PEC email address.',
    lineShipSuffix: '(physical shipping)',
    bannerMixed:
      'Mixed cart: the address below is for physical items only; digital items use your email.',
    bannerShippingOnly: 'Enter the shipping address for physical items.',
    addressLegend: 'Address',
    addressLegendShip: 'Shipping address',
  },
  de: {
    loadErr: 'Warenkorb konnte nicht mit dem Server abgeglichen werden.',
    empty: 'Ihr Warenkorb ist leer.',
    emptyLink: 'Zurück zum Katalog',
    submit: 'Bestellung speichern (Stripe-Zahlung in Phase 4)',
    submitting: 'Wird gesendet…',
    success: (id) =>
      `Bestellung #${id} erfasst. Kartenzahlung wird in der nächsten Phase aktiviert. Warenkorb wurde geleert.`,
    errGeneric: 'Anfrage fehlgeschlagen.',
    valEmail: 'Bitte eine gültige E-Mail eingeben.',
    valFields: 'Bitte die markierten Felder prüfen.',
    tableHeaders: ['Artikel', 'Betrag'],
    totalLabel: 'Gesamt',
    steps: ['Warenkorb', 'Abrechnung', 'Zahlung', 'Bestätigung'],
    hintEmail: 'Die Bestätigung wird an diese Adresse gesendet.',
    hintSdi: '7-stelliger Empfängercode (z.B. ABCDE12). Verwenden Sie 0000000 falls nicht verfügbar.',
    hintPec: 'Erforderlich, wenn der SDI-Code 0000000 ist.',
    errEmail: 'Bitte eine gültige E-Mail eingeben.',
    errSdi: 'Der SDI-Code muss genau 7 alphanumerische Zeichen haben.',
    errPec: 'Bitte eine gültige PEC-E-Mail eingeben.',
    lineShipSuffix: '(physische Lieferung)',
    bannerMixed:
      'Gemischter Warenkorb: die Adresse unten gilt für physische Artikel; digitale Inhalte per E-Mail.',
    bannerShippingOnly: 'Lieferadresse für physische Artikel eingeben.',
    addressLegend: 'Adresse',
    addressLegendShip: 'Lieferadresse',
  },
  fr: {
    loadErr: 'Impossible de vérifier le panier avec le serveur.',
    empty: 'Votre panier est vide.',
    emptyLink: 'Retourner au catalogue',
    submit: 'Enregistrer la commande (paiement Stripe en phase 4)',
    submitting: 'Envoi en cours…',
    success: (id) =>
      `Commande n°${id} enregistrée. Le paiement par carte sera activé à la prochaine étape. Le panier a été vidé.`,
    errGeneric: 'La requête a échoué.',
    valEmail: 'Saisissez une adresse e-mail valide.',
    valFields: 'Corrigez les champs surlignés.',
    tableHeaders: ['Article', 'Montant'],
    totalLabel: 'Total',
    steps: ['Panier', 'Facturation', 'Paiement', 'Confirmation'],
    hintEmail: 'La confirmation sera envoyée à cette adresse.',
    hintSdi: 'Code Destinataire à 7 caractères (ex. ABCDE12). Utilisez 0000000 si indisponible.',
    hintPec: 'Obligatoire si le code SDI est 0000000.',
    errEmail: 'Saisissez une adresse e-mail valide.',
    errSdi: 'Le code SDI doit comporter exactement 7 caractères alphanumériques.',
    errPec: 'Saisissez une adresse PEC valide.',
    lineShipSuffix: '(livraison physique)',
    bannerMixed:
      'Panier mixte : l’adresse ci-dessous sert aux produits physiques ; les produits numériques restent sur votre e-mail.',
    bannerShippingOnly: 'Indiquez l’adresse de livraison pour les produits physiques.',
    addressLegend: 'Adresse',
    addressLegendShip: 'Adresse de livraison',
  },
  es: {
    loadErr: 'No se pudo verificar el carrito con el servidor.',
    empty: 'El carrito está vacío.',
    emptyLink: 'Volver al catálogo',
    submit: 'Registrar pedido (pago Stripe en fase 4)',
    submitting: 'Enviando…',
    success: (id) =>
      `Pedido #${id} registrado. El pago con tarjeta se activará en la siguiente fase. El carrito se ha vaciado.`,
    errGeneric: 'La solicitud ha fallado.',
    valEmail: 'Introduzca un correo electrónico válido.',
    valFields: 'Revise los campos resaltados.',
    tableHeaders: ['Artículo', 'Importe'],
    totalLabel: 'Total',
    steps: ['Carrito', 'Facturación', 'Pago', 'Confirmación'],
    hintEmail: 'Recibirá la confirmación en esta dirección.',
    hintSdi: 'Código Destinatario de 7 caracteres (p. ej. ABCDE12). Use 0000000 si no está disponible.',
    hintPec: 'Obligatorio si el código SDI es 0000000.',
    errEmail: 'Introduzca una dirección de correo válida.',
    errSdi: 'El código SDI debe tener exactamente 7 caracteres alfanuméricos.',
    errPec: 'Introduzca una dirección PEC válida.',
    lineShipSuffix: '(envío físico)',
    bannerMixed:
      'Carrito mixto: la dirección inferior es para productos físicos; los digitales usan su correo.',
    bannerShippingOnly: 'Indique la dirección de envío para los productos físicos.',
    addressLegend: 'Dirección',
    addressLegendShip: 'Dirección de envío',
  },
};

const t = STR[LANG];

/* ── Utility ──────────────────────────────────────────────────────────────── */

function readBilling() {
  const inv = document.querySelector('input[name="invoice_type"]:checked')?.value || 'individual';
  return {
    invoice_type: inv,
    company_name: document.getElementById('company_name')?.value?.trim() || '',
    vat_id: document.getElementById('vat_id')?.value?.trim() || '',
    first_name: document.getElementById('first_name')?.value?.trim() || '',
    last_name: document.getElementById('last_name')?.value?.trim() || '',
    fiscal_code: document.getElementById('fiscal_code')?.value?.trim() || '',
    street: document.getElementById('street')?.value?.trim() || '',
    postal_code: document.getElementById('postal_code')?.value?.trim() || '',
    city: document.getElementById('city')?.value?.trim() || '',
    province: document.getElementById('province')?.value?.trim() || '',
    country: document.getElementById('country')?.value?.trim() || 'IT',
    sdi_code: document.getElementById('sdi_code')?.value?.trim().toUpperCase() || '',
    pec: document.getElementById('pec')?.value?.trim() || '',
    phone: document.getElementById('phone')?.value?.trim() || '',
  };
}

function setFieldError(id, on) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.toggle('field-invalid', Boolean(on));
  const hint = document.getElementById(`hint-${id}`);
  if (hint) hint.classList.toggle('field-hint--error', Boolean(on));
}

function clearFieldErrors() {
  document.querySelectorAll('.field-invalid').forEach((el) => el.classList.remove('field-invalid'));
  document.querySelectorAll('.field-hint--error').forEach((el) => el.classList.remove('field-hint--error'));
}

/* ── Progress steps ───────────────────────────────────────────────────────── */

function injectSteps(activeIndex) {
  const main = document.querySelector('main');
  const h1 = main?.querySelector('h1');
  // Ottimizzazione: evita duplicazione se lo script viene rivalutato
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

/* ── Inline field hints ───────────────────────────────────────────────────── */

function addFieldHint(fieldId, hintText) {
  const el = document.getElementById(fieldId);
  if (!el) return;
  const hint = document.createElement('p');
  hint.className = 'field-hint';
  hint.id = `hint-${fieldId}`;
  hint.textContent = hintText;
  el.parentNode.appendChild(hint);
}

function initHints() {
  addFieldHint('email', t.hintEmail);
  addFieldHint('sdi_code', t.hintSdi);
  addFieldHint('pec', t.hintPec);
}

/* ── Inline validation on blur ────────────────────────────────────────────── */

function initInlineValidation() {
  const emailEl = document.getElementById('email');
  if (emailEl) {
    emailEl.addEventListener('blur', () => {
      const val = emailEl.value.trim();
      if (!val) return;
      const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
      setFieldError('email', !valid);
      const hint = document.getElementById('hint-email');
      if (hint) hint.textContent = valid ? t.hintEmail : t.errEmail;
    });
    emailEl.addEventListener('input', () => {
      if (emailEl.classList.contains('field-invalid')) {
        const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailEl.value.trim());
        setFieldError('email', !valid);
        const hint = document.getElementById('hint-email');
        if (hint) hint.textContent = valid ? t.hintEmail : t.errEmail;
      }
    });
  }

  const sdiEl = document.getElementById('sdi_code');
  if (sdiEl) {
    sdiEl.addEventListener('blur', () => {
      if (sdiEl.disabled) return;
      const val = sdiEl.value.trim();
      if (!val) return;
      const valid = /^[A-Za-z0-9]{7}$/.test(val);
      setFieldError('sdi_code', !valid);
      const hint = document.getElementById('hint-sdi_code');
      if (hint) hint.textContent = valid ? t.hintSdi : t.errSdi;
    });
  }

  const pecEl = document.getElementById('pec');
  if (pecEl) {
    pecEl.addEventListener('blur', () => {
      if (pecEl.disabled) return;
      const sdi = document.getElementById('sdi_code')?.value?.trim().toUpperCase() || '';
      const val = pecEl.value.trim();
      if (sdi !== '0000000' || !val) return;
      const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
      setFieldError('pec', !valid);
      const hint = document.getElementById('hint-pec');
      if (hint) hint.textContent = valid ? t.hintPec : t.errPec;
    });
  }
}

async function verifyCart() {
  const status = document.getElementById('checkout-status');
  const form = document.getElementById('checkout-form');
  const linesWrap = document.getElementById('checkout-lines');
  if (!status || !form || !linesWrap) return;

  const lineT = {
    loadErr: t.loadErr,
    empty: t.empty,
    emptyLink: t.emptyLink,
    tableHeaders: t.tableHeaders,
    totalLabel: t.totalLabel,
    lineShipSuffix: t.lineShipSuffix,
  };

  try {
    await refreshServerCartLines({
      lang: LANG,
      t: lineT,
      statusEl: status,
      linesWrapEl: linesWrap,
      formEl: form,
      footerEl: null,
    });
    applyCheckoutFormState();
  } catch {
    status.textContent = t.loadErr;
    status.classList.add('is-error');
  }
}

/* ── Form submit ──────────────────────────────────────────────────────────── */

async function onSubmit(ev) {
  ev.preventDefault();
  const form = document.getElementById('checkout-form');
  const status = document.getElementById('checkout-status');
  const btn = document.getElementById('checkout-submit');
  if (!form || !status || !btn || form.dataset.verified !== '1') return;

  clearFieldErrors();
  const email = document.getElementById('email')?.value?.trim() || '';
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    status.textContent = t.valEmail;
    status.classList.add('is-error');
    setFieldError('email', true);
    return;
  }

  const billing = readBilling();
  let items;
  try {
    items = JSON.parse(form.dataset.linesJson || '[]');
  } catch {
    status.textContent = t.errGeneric;
    status.classList.add('is-error');
    return;
  }

  btn.disabled = true;
  btn.textContent = t.submitting;
  status.classList.remove('is-error');

  try {
    const res = await fetch('/api/order-draft', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ lang: LANG, email, billing, items }),
    });
    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      if (data.fields && Array.isArray(data.fields)) {
        for (const f of data.fields) {
          if (typeof f !== 'string') continue;
          const id = f === 'pec_format' ? 'pec' : f;
          if (document.getElementById(id)) setFieldError(id, true);
        }
        status.textContent = t.valFields;
      } else {
        status.textContent =
          typeof data.message === 'string' ? data.message : t.errGeneric;
      }
      status.classList.add('is-error');
      return;
    }

    try {
      clearCart();
    } catch {
      /* clearCart non deve bloccare la conferma UI */
    }
    status.classList.remove('is-error');
    const orderId =
      data.order_id != null && (typeof data.order_id === 'string' || typeof data.order_id === 'number')
        ? String(data.order_id)
        : '—';
    status.textContent = t.success(orderId);
    form.hidden = true;
    document.getElementById('checkout-lines')?.setAttribute('hidden', '');
    try {
      window.dispatchEvent(new CustomEvent('aml-cart-change'));
    } catch {
      /* listener esterni */
    }
  } catch {
    status.textContent = t.errGeneric;
    status.classList.add('is-error');
  } finally {
    btn.disabled = false;
    btn.textContent = t.submit;
  }
}

/* ── Invoice type toggle ──────────────────────────────────────────────────── */

function syncInvoiceFields() {
  const company = document.querySelector(
    'input[name="invoice_type"][value="company"]'
  )?.checked;

  document.getElementById('block-company-extra')?.toggleAttribute('hidden', !company);
  document.getElementById('fieldset-einvoice')?.toggleAttribute('hidden', !company);
  document.getElementById('block-fiscal-private')?.toggleAttribute('hidden', company);
  const fiscal = document.getElementById('fiscal_code');
  if (fiscal) fiscal.disabled = Boolean(company);

  const einvoiceFieldIds = ['company_name', 'vat_id', 'sdi_code', 'pec'];
  for (const id of einvoiceFieldIds) {
    const el = document.getElementById(id);
    if (!el) continue;
    if (!company) {
      el.disabled = true;
      el.required = false;
    } else {
      el.disabled = false;
      if (id === 'company_name' || id === 'vat_id' || id === 'sdi_code') {
        el.required = true;
      }
    }
  }

  for (const id of ['first_name', 'last_name']) {
    const el = document.getElementById(id);
    if (el) el.required = true;
  }
  const phoneEl = document.getElementById('phone');
  if (phoneEl) phoneEl.required = false;
}

/** Indirizzo visibile se serve spedizione (fisico) o fattura aziendale (P.IVA). */
function syncAddressAndBanner() {
  const form = document.getElementById('checkout-form');
  const fieldset = document.getElementById('fieldset-address');
  const legend = document.getElementById('address-fieldset-legend');
  const banner = document.getElementById('checkout-fulfillment-banner');
  if (!form || !fieldset) return;

  const needsShipping = form.dataset.needsShipping === '1';
  const hasDigital = form.dataset.hasDigital === '1';
  const company = document.querySelector(
    'input[name="invoice_type"][value="company"]'
  )?.checked;

  const addressRequired = Boolean(needsShipping || company);

  fieldset.toggleAttribute('hidden', !addressRequired);

  for (const id of ['street', 'postal_code', 'city', 'country', 'province']) {
    const el = document.getElementById(id);
    if (!el) continue;
    if (!addressRequired) {
      el.disabled = true;
      el.required = false;
    } else {
      el.disabled = false;
      if (id !== 'province') el.required = true;
    }
  }

  if (legend) {
    legend.textContent = needsShipping ? t.addressLegendShip : t.addressLegend;
  }

  if (banner) {
    if (!needsShipping) {
      banner.hidden = true;
      banner.textContent = '';
    } else if (hasDigital) {
      banner.hidden = false;
      banner.textContent = t.bannerMixed;
    } else {
      banner.hidden = false;
      banner.textContent = t.bannerShippingOnly;
    }
  }
}

function applyCheckoutFormState() {
  syncInvoiceFields();
  syncAddressAndBanner();
}

/* ── Boot ─────────────────────────────────────────────────────────────────── */

injectSteps(2);
initHints();
initInlineValidation();

document.querySelectorAll('input[name="invoice_type"]').forEach((r) => {
  r.addEventListener('change', applyCheckoutFormState);
});
applyCheckoutFormState();

document.getElementById('checkout-form')?.addEventListener('submit', onSubmit);
window.addEventListener('aml-cart-change', () => {
  void verifyCart();
});
verifyCart();
