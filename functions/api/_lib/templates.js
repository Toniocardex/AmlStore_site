/**
 * templates.js — template email HTML + plain text per Aml Store.
 * Inline styles obbligatori per compatibilità email client.
 * Accent: #3b82f6 (dark) / usato come unico colore per semplicità.
 */

const ACCENT      = '#3b82f6';
const ACCENT_DARK = '#003182';
const BG          = '#f5f6f8';
const CARD_BG     = '#ffffff';
const TEXT        = '#1a1a2e';
const TEXT_MUTED  = '#6b7280';
const BORDER      = '#e5e7eb';
const SUCCESS     = '#059669';

/** Stringhe localizzate */
const i18n = {
    it: {
        subject_paid:     'Ordine #{orderId} confermato — Aml Store',
        subject_pending:  'Ordine #{orderId} ricevuto — Aml Store',
        greeting:         'Grazie per il tuo ordine!',
        greeting_pending: 'Ordine ricevuto!',
        intro:            'Il tuo ordine è stato confermato e la email di consegna sarà inviata a breve.',
        intro_pending:    'Abbiamo ricevuto il tuo ordine. Procedi con il bonifico per completare l\'acquisto.',
        order_id:         'N° ordine',
        date:             'Data',
        payment:          'Pagamento',
        product:          'Prodotto',
        qty:              'Qtà',
        subtotal:         'Subtotale',
        total:            'Totale',
        method_stripe:    'Carta di credito / Stripe',
        method_paypal:    'PayPal',
        method_transfer:  'Bonifico bancario',
        transfer_title:   'Istruzioni per il bonifico',
        transfer_iban:    'IBAN',
        transfer_bene:    'Intestatario',
        transfer_bank:    'Banca',
        transfer_causale: 'Causale (obbligatoria)',
        transfer_note:    'Inserisci la causale esatta per velocizzare la conferma dell\'ordine.',
        ref_psp:          'Riferimento pagamento',
        footer_help:      'Hai domande? Contattaci:',
        footer_copy:      '© {year} AML STORE di Cardelli Antonino — P.IVA inclusa in fattura',
        cta:              'Vai al negozio',
    },
    en: {
        subject_paid:     'Order #{orderId} confirmed — Aml Store',
        subject_pending:  'Order #{orderId} received — Aml Store',
        greeting:         'Thank you for your order!',
        greeting_pending: 'Order received!',
        intro:            'Your order has been confirmed. Your digital product will be delivered shortly.',
        intro_pending:    'We received your order. Please complete the bank transfer to finalise your purchase.',
        order_id:         'Order no.',
        date:             'Date',
        payment:          'Payment',
        product:          'Product',
        qty:              'Qty',
        subtotal:         'Subtotal',
        total:            'Total',
        method_stripe:    'Credit / debit card (Stripe)',
        method_paypal:    'PayPal',
        method_transfer:  'Bank transfer',
        transfer_title:   'Bank transfer instructions',
        transfer_iban:    'IBAN',
        transfer_bene:    'Account name',
        transfer_bank:    'Bank',
        transfer_causale: 'Reference (mandatory)',
        transfer_note:    'Please use the exact reference above to speed up order confirmation.',
        ref_psp:          'Payment reference',
        footer_help:      'Questions? Contact us:',
        footer_copy:      '© {year} AML STORE di Cardelli Antonino',
        cta:              'Go to store',
    },
    fr: {
        subject_paid:     'Commande #{orderId} confirmée — Aml Store',
        subject_pending:  'Commande #{orderId} reçue — Aml Store',
        greeting:         'Merci pour votre commande !',
        greeting_pending: 'Commande reçue !',
        intro:            'Votre commande a été confirmée. La livraison sera effectuée sous peu.',
        intro_pending:    'Nous avons reçu votre commande. Veuillez effectuer le virement pour finaliser l\'achat.',
        order_id:         'N° commande',
        date:             'Date',
        payment:          'Paiement',
        product:          'Produit',
        qty:              'Qté',
        subtotal:         'Sous-total',
        total:            'Total',
        method_stripe:    'Carte bancaire / Stripe',
        method_paypal:    'PayPal',
        method_transfer:  'Virement bancaire',
        transfer_title:   'Instructions pour le virement',
        transfer_iban:    'IBAN',
        transfer_bene:    'Titulaire du compte',
        transfer_bank:    'Banque',
        transfer_causale: 'Référence (obligatoire)',
        transfer_note:    'Utilisez exactement cette référence pour accélérer la confirmation de commande.',
        ref_psp:          'Référence paiement',
        footer_help:      'Des questions ? Contactez-nous :',
        footer_copy:      '© {year} AML STORE di Cardelli Antonino',
        cta:              'Aller à la boutique',
    },
    de: {
        subject_paid:     'Bestellung #{orderId} bestätigt — Aml Store',
        subject_pending:  'Bestellung #{orderId} eingegangen — Aml Store',
        greeting:         'Vielen Dank für Ihre Bestellung!',
        greeting_pending: 'Bestellung eingegangen!',
        intro:            'Ihre Bestellung wurde bestätigt. Die Lieferung erfolgt in Kürze.',
        intro_pending:    'Wir haben Ihre Bestellung erhalten. Bitte führen Sie die Überweisung durch.',
        order_id:         'Bestellnr.',
        date:             'Datum',
        payment:          'Zahlung',
        product:          'Produkt',
        qty:              'Menge',
        subtotal:         'Zwischensumme',
        total:            'Gesamt',
        method_stripe:    'Kreditkarte / Stripe',
        method_paypal:    'PayPal',
        method_transfer:  'Banküberweisung',
        transfer_title:   'Überweisungsdetails',
        transfer_iban:    'IBAN',
        transfer_bene:    'Kontoinhaber',
        transfer_bank:    'Bank',
        transfer_causale: 'Verwendungszweck (Pflichtfeld)',
        transfer_note:    'Bitte geben Sie genau diesen Verwendungszweck an.',
        ref_psp:          'Zahlungsreferenz',
        footer_help:      'Fragen? Kontaktieren Sie uns:',
        footer_copy:      '© {year} AML STORE di Cardelli Antonino',
        cta:              'Zum Shop',
    },
    es: {
        subject_paid:     'Pedido #{orderId} confirmado — Aml Store',
        subject_pending:  'Pedido #{orderId} recibido — Aml Store',
        greeting:         '¡Gracias por su pedido!',
        greeting_pending: '¡Pedido recibido!',
        intro:            'Su pedido ha sido confirmado. La entrega se realizará en breve.',
        intro_pending:    'Hemos recibido su pedido. Realice la transferencia para completar la compra.',
        order_id:         'N.° de pedido',
        date:             'Fecha',
        payment:          'Pago',
        product:          'Producto',
        qty:              'Cant.',
        subtotal:         'Subtotal',
        total:            'Total',
        method_stripe:    'Tarjeta de crédito / Stripe',
        method_paypal:    'PayPal',
        method_transfer:  'Transferencia bancaria',
        transfer_title:   'Instrucciones para la transferencia',
        transfer_iban:    'IBAN',
        transfer_bene:    'Titular de la cuenta',
        transfer_bank:    'Banco',
        transfer_causale: 'Concepto (obligatorio)',
        transfer_note:    'Use exactamente este concepto para agilizar la confirmación del pedido.',
        ref_psp:          'Referencia de pago',
        footer_help:      '¿Preguntas? Contáctenos:',
        footer_copy:      '© {year} AML STORE di Cardelli Antonino',
        cta:              'Ir a la tienda',
    },
};

/** Dati bonifico fissi */
const BANK = {
    iban:  'IT91 S062 3033 5400 0001 5095 392',
    bene:  'AML STORE di Cardelli Antonino',
    bank:  'Crédit Agricole',
};

/**
 * Formatta un importo in centesimi come stringa valuta.
 * @param {number} minor — centesimi
 * @param {string} currency — es. 'EUR'
 * @returns {string}
 */
function fmt(minor, currency) {
    try {
        return new Intl.NumberFormat('it-IT', {
            style:    'currency',
            currency: (currency || 'EUR').toUpperCase(),
        }).format(minor / 100);
    } catch (_) {
        return `€ ${(minor / 100).toFixed(2)}`;
    }
}

/**
 * Formatta una data ISO 8601 in formato leggibile.
 * @param {string} iso
 * @param {string} locale
 * @returns {string}
 */
function fmtDate(iso, locale) {
    try {
        return new Date(iso).toLocaleString(locale || 'it-IT', {
            day:    '2-digit',
            month:  'long',
            year:   'numeric',
            hour:   '2-digit',
            minute: '2-digit',
        });
    } catch (_) { return iso || ''; }
}

/**
 * Restituisce soggetto email localizzato.
 * @param {string} locale
 * @param {string} orderId
 * @param {boolean} isPaid
 * @returns {string}
 */
export function emailSubject(locale, orderId, isPaid) {
    const t = i18n[locale] || i18n.it;
    const tpl = isPaid ? t.subject_paid : t.subject_pending;
    return tpl.replace('{orderId}', orderId);
}

/**
 * Genera il corpo HTML dell'email.
 *
 * @param {object} order       — da toPublicOrder() + dati completi
 * @param {boolean} isPaid
 * @returns {string} HTML
 */
export function emailHtml(order, isPaid) {
    const locale = order.locale || 'it';
    const t      = i18n[locale] || i18n.it;
    const year   = new Date().getFullYear();

    const methodLabel = {
        stripe:        t.method_stripe,
        paypal:        t.method_paypal,
        bank_transfer: t.method_transfer,
    }[order.payment_method] || order.payment_method;

    // Righe prodotto
    const lineItemsRows = (order.lineItems || []).map(item => {
        const qty      = item.qty || item.quantity || 1;
        const unit     = item.unit_amount_minor || item.unitAmount || 0;
        const subMinor = Math.round(unit) * qty;
        return `
        <tr>
          <td style="padding:10px 12px;border-bottom:1px solid ${BORDER};font-size:14px;color:${TEXT}">
            ${escHtml(item.name || item.sku || '')}<br>
            <span style="font-size:12px;color:${TEXT_MUTED}">${escHtml(item.sku || '')}</span>
          </td>
          <td style="padding:10px 12px;border-bottom:1px solid ${BORDER};font-size:14px;color:${TEXT};text-align:center">${qty}</td>
          <td style="padding:10px 12px;border-bottom:1px solid ${BORDER};font-size:14px;color:${TEXT};text-align:right;white-space:nowrap">${fmt(subMinor, order.currency)}</td>
        </tr>`;
    }).join('');

    // Sezione bonifico (solo se pending + bank_transfer)
    const transferSection = (!isPaid && order.payment_method === 'bank_transfer') ? `
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:24px;background:#fffbeb;border:1px solid #fcd34d;border-radius:6px">
      <tr><td style="padding:16px 20px">
        <p style="margin:0 0 12px;font-size:15px;font-weight:700;color:#92400e">${t.transfer_title}</p>
        ${bankRow(t.transfer_iban,    BANK.iban)}
        ${bankRow(t.transfer_bene,    BANK.bene)}
        ${bankRow(t.transfer_bank,    BANK.bank)}
        ${bankRow(t.transfer_causale, order.orderId, true)}
        <p style="margin:12px 0 0;font-size:12px;color:#78350f">${t.transfer_note}</p>
      </td></tr>
    </table>` : '';

    // Riferimento PSP (solo se pagato)
    let pspRef = '';
    if (isPaid) {
        const ref = order.payment_method === 'stripe'  ? (order.stripe_payment_intent || order.stripe_session_id)
                  : order.payment_method === 'paypal'  ? (order.paypal_capture_id     || order.paypal_order_id)
                  : null;
        if (ref) {
            pspRef = `<p style="font-size:12px;color:${TEXT_MUTED};margin:4px 0 0">${t.ref_psp}: <code style="font-size:11px">${escHtml(ref)}</code></p>`;
        }
    }

    const heading  = isPaid ? t.greeting         : t.greeting_pending;
    const introTxt = isPaid ? t.intro             : t.intro_pending;
    const badge    = isPaid
        ? `<span style="display:inline-block;background:${SUCCESS};color:#fff;font-size:12px;font-weight:700;padding:3px 10px;border-radius:20px;letter-spacing:.3px">✓ ${methodLabel}</span>`
        : `<span style="display:inline-block;background:#fbbf24;color:#1a1a2e;font-size:12px;font-weight:700;padding:3px 10px;border-radius:20px;letter-spacing:.3px">⏳ ${methodLabel}</span>`;

    return `<!DOCTYPE html>
<html lang="${escHtml(locale)}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${emailSubject(locale, order.orderId, isPaid)}</title>
</head>
<body style="margin:0;padding:0;background:${BG};font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background:${BG};padding:32px 16px">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%">

  <!-- Logo header -->
  <tr><td style="background:${TEXT};border-radius:8px 8px 0 0;padding:20px 32px;text-align:center">
    <img src="https://aml-store.com/logo/logo-header-400.webp" alt="Aml Store" width="140" height="auto"
         style="display:inline-block;vertical-align:middle;max-width:140px">
  </td></tr>

  <!-- Body card -->
  <tr><td style="background:${CARD_BG};padding:32px 32px 24px;border-left:1px solid ${BORDER};border-right:1px solid ${BORDER}">

    <h1 style="margin:0 0 8px;font-size:22px;font-weight:700;color:${TEXT}">${heading}</h1>
    <p style="margin:0 0 20px;font-size:15px;color:${TEXT_MUTED}">${introTxt}</p>

    <!-- Info ordine -->
    <table width="100%" cellpadding="0" cellspacing="0" style="background:${BG};border-radius:6px;margin-bottom:20px">
      <tr><td style="padding:16px 20px">
        <p style="margin:0 0 6px;font-size:13px;color:${TEXT_MUTED};text-transform:uppercase;letter-spacing:.5px">${t.order_id}</p>
        <p style="margin:0 0 12px;font-size:20px;font-weight:800;color:${ACCENT_DARK};font-family:monospace,monospace">${escHtml(order.orderId)}</p>
        <p style="margin:0 0 4px;font-size:13px;color:${TEXT_MUTED}">${t.date}: <strong style="color:${TEXT}">${fmtDate(order.createdAt, locale)}</strong></p>
        <p style="margin:0;font-size:13px;color:${TEXT_MUTED}">${t.payment}: ${badge}</p>
        ${pspRef}
      </td></tr>
    </table>

    <!-- Righe prodotto -->
    <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid ${BORDER};border-radius:6px;overflow:hidden;margin-bottom:8px">
      <thead>
        <tr style="background:${BG}">
          <th style="padding:10px 12px;font-size:12px;color:${TEXT_MUTED};text-align:left;font-weight:600;text-transform:uppercase;letter-spacing:.4px">${t.product}</th>
          <th style="padding:10px 12px;font-size:12px;color:${TEXT_MUTED};text-align:center;font-weight:600;text-transform:uppercase;letter-spacing:.4px">${t.qty}</th>
          <th style="padding:10px 12px;font-size:12px;color:${TEXT_MUTED};text-align:right;font-weight:600;text-transform:uppercase;letter-spacing:.4px">${t.subtotal}</th>
        </tr>
      </thead>
      <tbody>${lineItemsRows}</tbody>
    </table>

    <!-- Totale -->
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:4px">
      <tr>
        <td style="padding:12px 12px;font-size:15px;font-weight:700;color:${TEXT};text-align:right">
          ${t.total}: <span style="font-size:18px;color:${ACCENT_DARK}">${fmt(order.totalMinor, order.currency)}</span>
        </td>
      </tr>
    </table>

    ${transferSection}

  </td></tr>

  <!-- CTA -->
  <tr><td style="background:${CARD_BG};padding:0 32px 28px;border-left:1px solid ${BORDER};border-right:1px solid ${BORDER};text-align:center">
    <a href="https://aml-store.com/${escHtml(locale)}/"
       style="display:inline-block;background:${ACCENT};color:#fff;font-size:14px;font-weight:700;text-decoration:none;padding:12px 28px;border-radius:6px">${t.cta}</a>
  </td></tr>

  <!-- Footer -->
  <tr><td style="background:#f0f2f5;border-radius:0 0 8px 8px;padding:18px 32px;border:1px solid ${BORDER};border-top:none;text-align:center">
    <p style="margin:0 0 6px;font-size:13px;color:${TEXT_MUTED}">${t.footer_help} <a href="mailto:Info@amlstore.it" style="color:${ACCENT}">Info@amlstore.it</a></p>
    <p style="margin:0;font-size:11px;color:#9ca3af">${t.footer_copy.replace('{year}', year)}</p>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>`;
}

/**
 * Genera plain text fallback.
 * @param {object} order
 * @param {boolean} isPaid
 * @returns {string}
 */
export function emailText(order, isPaid) {
    const locale = order.locale || 'it';
    const t      = i18n[locale] || i18n.it;

    const heading  = isPaid ? t.greeting : t.greeting_pending;
    const introTxt = isPaid ? t.intro    : t.intro_pending;

    const methodLabel = {
        stripe:        t.method_stripe,
        paypal:        t.method_paypal,
        bank_transfer: t.method_transfer,
    }[order.payment_method] || order.payment_method;

    let lines = [
        `Aml Store`,
        `${heading}`,
        ``,
        introTxt,
        ``,
        `${t.order_id}: ${order.orderId}`,
        `${t.date}: ${fmtDate(order.createdAt, locale)}`,
        `${t.payment}: ${methodLabel}`,
        ``,
        `--- ${t.product} ---`,
    ];

    (order.lineItems || []).forEach(item => {
        const qty      = item.qty || item.quantity || 1;
        const unit     = item.unit_amount_minor || item.unitAmount || 0;
        const subMinor = Math.round(unit) * qty;
        lines.push(`${item.name || item.sku}  x${qty}  ${fmt(subMinor, order.currency)}`);
    });

    lines.push(``, `${t.total}: ${fmt(order.totalMinor, order.currency)}`);

    if (!isPaid && order.payment_method === 'bank_transfer') {
        lines.push(
            ``,
            `--- ${t.transfer_title} ---`,
            `${t.transfer_iban}: ${BANK.iban}`,
            `${t.transfer_bene}: ${BANK.bene}`,
            `${t.transfer_bank}: ${BANK.bank}`,
            `${t.transfer_causale}: ${order.orderId}`,
            t.transfer_note,
        );
    }

    lines.push(``, `${t.footer_help} Info@amlstore.it`, `https://aml-store.com/${locale}/`);

    return lines.join('\n');
}

/** Escape HTML per sicurezza nei template. */
function escHtml(str) {
    return String(str || '')
        .replace(/&/g,  '&amp;')
        .replace(/</g,  '&lt;')
        .replace(/>/g,  '&gt;')
        .replace(/"/g,  '&quot;');
}

/** Riga tabella bonifico. */
function bankRow(label, value, highlight = false) {
    const color  = highlight ? '#92400e' : '#374151';
    const weight = highlight ? '700' : '400';
    return `<p style="margin:0 0 6px;font-size:13px;color:${TEXT_MUTED}">${escHtml(label)}: <strong style="color:${color};font-weight:${weight};font-family:monospace,monospace">${escHtml(value)}</strong></p>`;
}
