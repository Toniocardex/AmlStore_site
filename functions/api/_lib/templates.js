/**
 * templates.js — template email HTML + plain text per Aml Store.
 * Inline styles obbligatori per compatibilità email client.
 * Palette istituzionale navy, allineata a --aml-* in css/page.css.
 */

const ACCENT       = '#3267AC';
const ACCENT_DARK  = '#14243A';
const ACCENT_SOFT  = '#EAF0F6';
const ACCENT_SOFT_BORDER = '#C7D6E5';
const BG           = '#F4F6F8';
const CARD_BG      = '#ffffff';
const TEXT         = '#152033';
const TEXT_MUTED   = '#5F6B7A';
const BORDER       = '#DCE3EA';
const SUCCESS      = '#1F7A52';
const SUCCESS_SOFT = '#E8F3ED';
const AMBER_BG     = '#FCF3D9';
const AMBER_BORDER = '#f3ce6b';
const AMBER_TEXT   = '#92400E';
const AMBER_TEXT_SOFT = '#78350f';
const GOLD         = '#8C6423';
const GOLD_SOFT    = '#F5EEDD';
const GOLD_BORDER  = '#E4D3AC';
const TEXT_FAINT   = '#8B95A3';
const HEADING_FONT = "'Montserrat',-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif";
const BODY_FONT    = "-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif";

/** Stringhe localizzate */
const i18n = {
    it: {
        subject_paid:     'Ordine #{orderId} confermato — Aml Store',
        subject_pending:  'Ordine #{orderId} ricevuto — Aml Store',
        order_eyebrow:    'Riepilogo ordine',
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
        shipping_title:   'Indirizzo di spedizione',
        guide_attached:   'In allegato trovi in omaggio la Guida Copilot per Microsoft 365 (PDF).',
        footer_tagline:   'Licenze digitali originali · aml-store.com',
        license_subject:  'La tua licenza — ordine #{orderId} — Aml Store',
        license_eyebrow:  'Licenza digitale',
        license_greeting: 'Ecco la tua licenza, {name}!',
        license_intro:    'Grazie per il tuo acquisto. Qui sotto trovi la chiave del tuo prodotto, pronta per l\'attivazione.',
        license_key_label: 'Chiave prodotto',
        license_copy_hint: 'Tocca per selezionare e copiare',
        activation_eyebrow: 'Come attivare',
        license_note:     'Conserva questa email: la chiave è personale ed è associata al tuo ordine.',
        license_help:     'Hai bisogno di assistenza con l\'attivazione? Scrivici:',
    },
    en: {
        subject_paid:     'Order #{orderId} confirmed — Aml Store',
        subject_pending:  'Order #{orderId} received — Aml Store',
        order_eyebrow:    'Order summary',
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
        shipping_title:   'Shipping address',
        guide_attached:   'Attached you\'ll find our free Copilot for Microsoft 365 guide (PDF).',
        footer_tagline:   'Genuine digital licences · aml-store.com',
        license_subject:  'Your licence — order #{orderId} — Aml Store',
        license_eyebrow:  'Digital licence',
        license_greeting: 'Here is your licence, {name}!',
        license_intro:    'Thank you for your purchase. Below is your product key, ready to activate.',
        license_key_label: 'Product key',
        license_copy_hint: 'Tap to select and copy',
        activation_eyebrow: 'How to activate',
        license_note:     'Keep this email: the key is personal and tied to your order.',
        license_help:     'Need help activating it? Contact us:',
    },
    fr: {
        subject_paid:     'Commande #{orderId} confirmée — Aml Store',
        subject_pending:  'Commande #{orderId} reçue — Aml Store',
        order_eyebrow:    'Récapitulatif de commande',
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
        shipping_title:   'Adresse de livraison',
        guide_attached:   'Vous trouverez en pièce jointe notre guide gratuit Copilot pour Microsoft 365 (PDF).',
        footer_tagline:   'Licences numériques originales · aml-store.com',
        license_subject:  'Votre licence — commande #{orderId} — Aml Store',
        license_eyebrow:  'Licence numérique',
        license_greeting: 'Voici votre licence, {name} !',
        license_intro:    'Merci pour votre achat. Vous trouverez ci-dessous la clé de votre produit, prête à activer.',
        license_key_label: 'Clé produit',
        license_copy_hint: 'Appuyez pour sélectionner et copier',
        activation_eyebrow: 'Comment activer',
        license_note:     'Conservez cet e-mail : la clé est personnelle et liée à votre commande.',
        license_help:     'Besoin d\'aide pour l\'activation ? Contactez-nous :',
    },
    de: {
        subject_paid:     'Bestellung #{orderId} bestätigt — Aml Store',
        subject_pending:  'Bestellung #{orderId} eingegangen — Aml Store',
        order_eyebrow:    'Bestellübersicht',
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
        shipping_title:   'Lieferadresse',
        guide_attached:   'Im Anhang finden Sie unseren kostenlosen Copilot-Leitfaden für Microsoft 365 (PDF).',
        footer_tagline:   'Originale digitale Lizenzen · aml-store.com',
        license_subject:  'Ihre Lizenz — Bestellung #{orderId} — Aml Store',
        license_eyebrow:  'Digitale Lizenz',
        license_greeting: 'Hier ist Ihre Lizenz, {name}!',
        license_intro:    'Vielen Dank für Ihren Kauf. Unten finden Sie Ihren Produktschlüssel, bereit zur Aktivierung.',
        license_key_label: 'Produktschlüssel',
        license_copy_hint: 'Zum Markieren und Kopieren tippen',
        activation_eyebrow: 'So aktivieren Sie',
        license_note:     'Bewahren Sie diese E-Mail auf: Der Schlüssel ist persönlich und Ihrer Bestellung zugeordnet.',
        license_help:     'Brauchen Sie Hilfe bei der Aktivierung? Kontaktieren Sie uns:',
    },
    es: {
        subject_paid:     'Pedido #{orderId} confirmado — Aml Store',
        subject_pending:  'Pedido #{orderId} recibido — Aml Store',
        order_eyebrow:    'Resumen del pedido',
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
        shipping_title:   'Dirección de envío',
        guide_attached:   'Adjuntamos nuestra guía gratuita de Copilot para Microsoft 365 (PDF).',
        footer_tagline:   'Licencias digitales originales · aml-store.com',
        license_subject:  'Su licencia — pedido #{orderId} — Aml Store',
        license_eyebrow:  'Licencia digital',
        license_greeting: '¡Aquí tiene su licencia, {name}!',
        license_intro:    'Gracias por su compra. A continuación encontrará la clave de su producto, lista para activar.',
        license_key_label: 'Clave de producto',
        license_copy_hint: 'Toca para seleccionar y copiar',
        activation_eyebrow: 'Cómo activar',
        license_note:     'Conserve este correo: la clave es personal y está asociada a su pedido.',
        license_help:     '¿Necesita ayuda con la activación? Contáctenos:',
    },
    pt: {
        subject_paid:     'Pedido #{orderId} confirmado — Aml Store',
        subject_pending:  'Pedido #{orderId} recebido — Aml Store',
        order_eyebrow:    'Resumo do pedido',
        greeting:         'Obrigado pelo seu pedido!',
        greeting_pending: 'Pedido recebido!',
        intro:            'O seu pedido foi confirmado. A entrega será feita em breve.',
        intro_pending:    'Recebemos o seu pedido. Efetue a transferência bancária para concluir a compra.',
        order_id:         'N.º do pedido',
        date:             'Data',
        payment:          'Pagamento',
        product:          'Produto',
        qty:              'Qtd.',
        subtotal:         'Subtotal',
        total:            'Total',
        method_stripe:    'Cartão de crédito / Stripe',
        method_paypal:    'PayPal',
        method_transfer:  'Transferência bancária',
        transfer_title:   'Instruções para a transferência',
        transfer_iban:    'IBAN',
        transfer_bene:    'Titular da conta',
        transfer_bank:    'Banco',
        transfer_causale: 'Referência (obrigatória)',
        transfer_note:    'Use exatamente esta referência para agilizar a confirmação do pedido.',
        ref_psp:          'Referência de pagamento',
        footer_help:      'Tem dúvidas? Contacte-nos:',
        footer_copy:      '© {year} AML STORE di Cardelli Antonino',
        cta:              'Ir para a loja',
        shipping_title:   'Endereço de envio',
        guide_attached:   'Em anexo encontra, como oferta, o nosso guia Copilot para Microsoft 365 (PDF).',
        footer_tagline:   'Licenças digitais originais · aml-store.com',
        license_subject:  'A sua licença — pedido #{orderId} — Aml Store',
        license_eyebrow:  'Licença digital',
        license_greeting: 'Aqui está a sua licença, {name}!',
        license_intro:    'Obrigado pela sua compra. Abaixo encontra a chave do seu produto, pronta para ativação.',
        license_key_label: 'Chave do produto',
        license_copy_hint: 'Toque para selecionar e copiar',
        activation_eyebrow: 'Como ativar',
        license_note:     'Guarde este email: a chave é pessoal e está associada ao seu pedido.',
        license_help:     'Precisa de ajuda com a ativação? Contacte-nos:',
    },
    nl: {
        subject_paid:     'Bestelling #{orderId} bevestigd — Aml Store',
        subject_pending:  'Bestelling #{orderId} ontvangen — Aml Store',
        order_eyebrow:    'Besteloverzicht',
        greeting:         'Bedankt voor uw bestelling!',
        greeting_pending: 'Bestelling ontvangen!',
        intro:            'Uw bestelling is bevestigd. De levering volgt binnenkort.',
        intro_pending:    'We hebben uw bestelling ontvangen. Voer de bankoverschrijving uit om de aankoop af te ronden.',
        order_id:         'Bestelnr.',
        date:             'Datum',
        payment:          'Betaling',
        product:          'Product',
        qty:              'Aantal',
        subtotal:         'Subtotaal',
        total:            'Totaal',
        method_stripe:    'Creditcard / Stripe',
        method_paypal:    'PayPal',
        method_transfer:  'Bankoverschrijving',
        transfer_title:   'Instructies voor de overschrijving',
        transfer_iban:    'IBAN',
        transfer_bene:    'Rekeninghouder',
        transfer_bank:    'Bank',
        transfer_causale: 'Omschrijving (verplicht)',
        transfer_note:    'Gebruik precies deze omschrijving zodat we de bestelling sneller kunnen bevestigen.',
        ref_psp:          'Betalingsreferentie',
        footer_help:      'Vragen? Neem contact met ons op:',
        footer_copy:      '© {year} AML STORE di Cardelli Antonino',
        cta:              'Naar de winkel',
        shipping_title:   'Verzendadres',
        guide_attached:   'Als extraatje vindt u in de bijlage onze Copilot-gids voor Microsoft 365 (PDF).',
        footer_tagline:   'Originele digitale licenties · aml-store.com',
        license_subject:  'Uw licentie — bestelling #{orderId} — Aml Store',
        license_eyebrow:  'Digitale licentie',
        license_greeting: 'Hier is uw licentie, {name}!',
        license_intro:    'Bedankt voor uw aankoop. Hieronder vindt u de productsleutel, klaar voor activering.',
        license_key_label: 'Productsleutel',
        license_copy_hint: 'Tik om te selecteren en te kopiëren',
        activation_eyebrow: 'Hoe activeren',
        license_note:     'Bewaar deze e-mail: de sleutel is persoonlijk en gekoppeld aan uw bestelling.',
        license_help:     'Hulp nodig bij de activering? Neem contact met ons op:',
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
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
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
 * @param {boolean} guideAttached — true se la guida Copilot omaggio è allegata a questa email
 * @returns {string} HTML
 */
export function emailHtml(order, isPaid, guideAttached = false) {
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
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:20px;background:${AMBER_BG};border:1px solid ${AMBER_BORDER};border-radius:12px">
      <tr><td style="padding:18px 22px">
        <p style="margin:0 0 14px;font-size:14px;font-weight:700;color:${AMBER_TEXT};text-transform:uppercase;letter-spacing:.4px">🏦 ${t.transfer_title}</p>
        ${bankRow(t.transfer_iban,    BANK.iban)}
        ${bankRow(t.transfer_bene,    BANK.bene)}
        ${bankRow(t.transfer_bank,    BANK.bank)}
        ${bankRow(t.transfer_causale, order.orderId, true)}
        <p style="margin:14px 0 0;padding-top:12px;border-top:1px solid ${AMBER_BORDER};font-size:12px;color:${AMBER_TEXT_SOFT};line-height:1.5">${t.transfer_note}</p>
      </td></tr>
    </table>` : '';

    // Indirizzo di spedizione (solo articoli fisici: DVD/COA)
    const shippingSection = (order.requiresShipping && order.shipping) ? `
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:16px;background:${BG};border-radius:12px">
      <tr><td style="padding:16px 20px">
        <p style="margin:0 0 6px;font-size:12px;font-weight:700;color:${TEXT_MUTED};text-transform:uppercase;letter-spacing:.5px">${t.shipping_title}</p>
        <p style="margin:0;font-size:14px;color:${TEXT};line-height:1.6">
          ${escHtml(order.shipping.addressLine1)}<br>
          ${escHtml(order.shipping.postalCode)} ${escHtml(order.shipping.city)}${order.shipping.province ? ' (' + escHtml(order.shipping.province) + ')' : ''}<br>
          ${escHtml(order.shipping.country)}
        </p>
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
        ? `<span style="display:inline-block;background:${SUCCESS};color:#fff;font-size:12px;font-weight:700;padding:4px 12px;border-radius:20px;letter-spacing:.3px">✓ ${methodLabel}</span>`
        : `<span style="display:inline-block;background:#fbbf24;color:#78350f;font-size:12px;font-weight:700;padding:4px 12px;border-radius:20px;letter-spacing:.3px">⏳ ${methodLabel}</span>`;

    // Icona di stato accanto al titolo: cerchio pieno con segno di spunta/orologio
    const statusIcon = isPaid
        ? `<td width="40" valign="top" style="padding-right:12px">
             <table cellpadding="0" cellspacing="0"><tr><td width="36" height="36" align="center" valign="middle" style="background:${SUCCESS_SOFT};border-radius:50%;font-size:18px;color:${SUCCESS}">✓</td></tr></table>
           </td>`
        : `<td width="40" valign="top" style="padding-right:12px">
             <table cellpadding="0" cellspacing="0"><tr><td width="36" height="36" align="center" valign="middle" style="background:#fef3c7;border-radius:50%;font-size:16px;color:${AMBER_TEXT}">⏳</td></tr></table>
           </td>`;

    return `<!DOCTYPE html>
<html lang="${escHtml(locale)}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${emailSubject(locale, order.orderId, isPaid)}</title>
<style>
  @font-face{font-family:'Montserrat';src:url('https://eurolicenze.com/fonts/montserrat-latin-700.woff2') format('woff2');font-weight:700}
  @font-face{font-family:'Montserrat';src:url('https://eurolicenze.com/fonts/montserrat-latin-800.woff2') format('woff2');font-weight:800}
</style>
</head>
<body style="margin:0;padding:0;background:${BG};font-family:${BODY_FONT}">
<table width="100%" cellpadding="0" cellspacing="0" style="background:${BG};padding:32px 16px">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;box-shadow:0 6px 28px rgba(0,49,130,0.1)">

  <!-- Logo header -->
  <tr><td style="background:${ACCENT_DARK};border-top:4px solid ${GOLD};border-radius:10px 10px 0 0;padding:22px 32px;text-align:center">
    <table cellpadding="0" cellspacing="0" style="display:inline-block;background:#ffffff;border-radius:8px;padding:8px 16px">
      <tr><td>
        <img src="https://eurolicenze.com/logo/logo-header-400.webp" alt="Aml Store" width="140" height="auto"
             style="display:block;max-width:140px">
      </td></tr>
    </table>
  </td></tr>

  <!-- Body card -->
  <tr><td style="background:${CARD_BG};padding:36px 32px 28px;border-left:1px solid ${BORDER};border-right:1px solid ${BORDER}">

    <p style="margin:0 0 12px;font-size:11px;font-weight:700;color:${GOLD};text-transform:uppercase;letter-spacing:1.1px">${t.order_eyebrow} · Aml Store</p>

    <table cellpadding="0" cellspacing="0" style="margin-bottom:22px">
      <tr>
        ${statusIcon}
        <td valign="middle">
          <h1 style="margin:0 0 4px;font-family:${HEADING_FONT};font-size:23px;font-weight:800;color:${TEXT};letter-spacing:-.2px">${heading}</h1>
          <p style="margin:0;font-size:14.5px;color:${TEXT_MUTED};line-height:1.5">${introTxt}</p>
        </td>
      </tr>
    </table>

    <!-- Info ordine -->
    <table width="100%" cellpadding="0" cellspacing="0" style="background:${CARD_BG};border:1px solid ${BORDER};border-left:4px solid ${ACCENT_DARK};border-radius:12px;margin-bottom:22px">
      <tr><td style="padding:18px 22px">
        <p style="margin:0 0 5px;font-size:11.5px;color:${TEXT_MUTED};text-transform:uppercase;letter-spacing:.6px;font-weight:600">${t.order_id}</p>
        <p style="margin:0 0 14px;font-size:21px;font-weight:800;color:${ACCENT_DARK};font-family:'SFMono-Regular',Consolas,monospace">${escHtml(order.orderId)}</p>
        <p style="margin:0 0 6px;font-size:13px;color:${TEXT_MUTED}">${t.date}: <strong style="color:${TEXT}">${fmtDate(order.createdAt, locale)}</strong></p>
        <p style="margin:0;font-size:13px;color:${TEXT_MUTED}">${t.payment}: ${badge}</p>
        ${pspRef}
      </td></tr>
    </table>

    <!-- Righe prodotto -->
    <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid ${BORDER};border-radius:12px;overflow:hidden;margin-bottom:4px">
      <thead>
        <tr style="background:${ACCENT_SOFT}">
          <th style="padding:11px 14px;font-size:11.5px;color:${ACCENT_DARK};text-align:left;font-weight:700;text-transform:uppercase;letter-spacing:.5px">${t.product}</th>
          <th style="padding:11px 14px;font-size:11.5px;color:${ACCENT_DARK};text-align:center;font-weight:700;text-transform:uppercase;letter-spacing:.5px">${t.qty}</th>
          <th style="padding:11px 14px;font-size:11.5px;color:${ACCENT_DARK};text-align:right;font-weight:700;text-transform:uppercase;letter-spacing:.5px">${t.subtotal}</th>
        </tr>
      </thead>
      <tbody>${lineItemsRows}</tbody>
    </table>

    <!-- Totale -->
    <table width="100%" cellpadding="0" cellspacing="0" style="background:${BG};border-radius:0 0 10px 10px;margin-bottom:4px">
      <tr>
        <td style="padding:14px 16px;font-size:14px;font-weight:700;color:${TEXT};text-align:right">
          ${t.total}&nbsp; <span style="font-family:${HEADING_FONT};font-size:20px;font-weight:800;color:${ACCENT_DARK}">${fmt(order.totalMinor, order.currency)}</span>
        </td>
      </tr>
    </table>

    ${shippingSection}
    ${transferSection}
    ${guideAttached ? `
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:20px;background:${ACCENT_SOFT};border:1px solid ${ACCENT_SOFT_BORDER};border-radius:12px">
      <tr>
        <td width="44" valign="middle" style="padding:16px 0 16px 18px;font-size:20px">🎁</td>
        <td valign="middle" style="padding:16px 18px 16px 10px;font-size:14px;color:${ACCENT_DARK};line-height:1.5">${t.guide_attached}</td>
      </tr>
    </table>` : ''}

  </td></tr>

  <!-- CTA -->
  <tr><td style="background:${CARD_BG};padding:6px 32px 32px;border-left:1px solid ${BORDER};border-right:1px solid ${BORDER};text-align:center">
    <a href="https://eurolicenze.com/${escHtml(locale)}/"
       style="display:inline-block;background:${ACCENT_DARK};color:#fff;font-size:14.5px;font-weight:700;text-decoration:none;padding:14px 32px;border-radius:8px;box-shadow:0 6px 18px rgba(0,49,130,0.3)">${t.cta}</a>
  </td></tr>

  <!-- Footer -->
  <tr><td style="background:#f0f2f5;border-radius:0 0 10px 10px;padding:22px 32px;border:1px solid ${BORDER};border-top:none;text-align:center">
    <p style="margin:0 0 8px;font-size:13px;color:${TEXT_MUTED}">${t.footer_help} <a href="mailto:Info@amlstore.it" style="color:${ACCENT_DARK};font-weight:600">Info@amlstore.it</a></p>
    <p style="margin:0 0 10px;font-size:11px;color:#9ca3af">${t.footer_copy.replace('{year}', year)}</p>
    <p style="margin:0;font-size:10.5px;color:#b0b5bd;letter-spacing:.3px">${t.footer_tagline}</p>
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
 * @param {boolean} guideAttached — true se la guida Copilot omaggio è allegata a questa email
 * @returns {string}
 */
export function emailText(order, isPaid, guideAttached = false) {
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

    if (order.requiresShipping && order.shipping) {
        lines.push(
            ``,
            `--- ${t.shipping_title} ---`,
            order.shipping.addressLine1,
            `${order.shipping.postalCode} ${order.shipping.city}${order.shipping.province ? ' (' + order.shipping.province + ')' : ''}`,
            order.shipping.country,
        );
    }

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

    if (guideAttached) {
        lines.push(``, `📎 ${t.guide_attached}`);
    }

    lines.push(``, `${t.footer_help} Info@amlstore.it`, `https://eurolicenze.com/${locale}/`);

    return lines.join('\n');
}

/**
 * Istruzioni/pulsante di attivazione per tipo di prodotto, da allegare sotto
 * la chiave nell'email di consegna licenza. Le voci "button" rimandano al
 * portale ufficiale del produttore; le voci "text" restano informative
 * quando l'attivazione avviene lato sistema operativo (nessun link esterno).
 * Fonti: catalog.json (categorie prodotto) e le pagine prodotto in
 * it/en/fr/de/es (sezione "Come si attiva?" / step "Attivazione").
 */
function activationLabels(portal) {
    return {
        it: `Attiva su ${portal} →`,
        en: `Activate on ${portal} →`,
        fr: `Activer sur ${portal} →`,
        de: `Aktivieren auf ${portal} →`,
        es: `Activar en ${portal} →`,
        pt: `Ativar em ${portal} →`,
        nl: `Activeren op ${portal} →`,
    };
}

const ACTIVATION = {
    windows: {
        kind: 'text',
        text: {
            it: 'Impostazioni → Sistema → Attivazione con il codice sopra. Usa i canali ufficiali Microsoft.',
            en: 'Settings → System → Activation using the code above. Use official Microsoft channels.',
            fr: 'Paramètres → Système → Activation avec le code ci-dessus. Utilisez les canaux officiels Microsoft.',
            de: 'Einstellungen → System → Aktivierung mit dem obigen Code. Nutzen Sie die offiziellen Microsoft-Kanäle.',
            es: 'Configuración → Sistema → Activación con el código anterior. Use los canales oficiales de Microsoft.',
            pt: 'Definições → Sistema → Ativação com o código acima. Use os canais oficiais da Microsoft.',
            nl: 'Instellingen → Systeem → Activering met de code hierboven. Gebruik de officiële Microsoft-kanalen.',
        },
    },
    windows_server: {
        kind: 'text',
        text: {
            it: 'Installa il sistema e attiva la licenza con il codice sopra tramite i canali ufficiali Microsoft.',
            en: 'Install the system and activate the licence with the code above via official Microsoft channels.',
            fr: 'Installez le système et activez la licence avec le code ci-dessus via les canaux officiels Microsoft.',
            de: 'Installieren Sie das System und aktivieren Sie die Lizenz mit dem obigen Code über die offiziellen Microsoft-Kanäle.',
            es: 'Instale el sistema y active la licencia con el código anterior a través de los canales oficiales de Microsoft.',
            pt: 'Instale o sistema e ative a licença com o código acima através dos canais oficiais da Microsoft.',
            nl: 'Installeer het systeem en activeer de licentie met de code hierboven via de officiële Microsoft-kanalen.',
        },
    },
    office: {
        kind: 'button',
        url: 'https://setup.office.com/Home',
        label: activationLabels('setup.office.com'),
        note: {
            it: 'Poi installa le app da office.com.',
            en: 'Then install the apps from office.com.',
            fr: 'Puis installez les applications depuis office.com.',
            de: 'Installieren Sie dann die Apps von office.com.',
            es: 'Luego instale las aplicaciones desde office.com.',
            pt: 'Depois instale as aplicações a partir de office.com.',
            nl: 'Installeer daarna de apps via office.com.',
        },
    },
    kaspersky: { kind: 'button', url: 'https://my.kaspersky.com',           label: activationLabels('My Kaspersky') },
    norton:    { kind: 'button', url: 'https://my.norton.com',              label: activationLabels('My Norton') },
    mcafee:    { kind: 'button', url: 'https://www.mcafee.com/my-account/', label: activationLabels('McAfee My Account') },
    eset:      { kind: 'button', url: 'https://home.eset.com',              label: activationLabels('ESET HOME') },
    adobe:     { kind: 'button', url: 'https://account.adobe.com',          label: activationLabels('account Adobe') },
    acronis:   { kind: 'button', url: 'https://account.acronis.com',        label: activationLabels('account Acronis') },
    corel:     { kind: 'button', url: 'https://www.coreldraw.com',          label: activationLabels('account Corel') },
};

/**
 * Genera il blocco HTML di attivazione (pulsante o box informativo) da
 * inserire sotto la chiave prodotto in una card licenseEmailHtml.
 * @param {string} [key] — chiave in ACTIVATION, es. 'windows', 'office', 'kaspersky'
 * @param {string} locale
 * @param {string} eyebrow — etichetta localizzata "Come attivare"
 * @returns {string}
 */
function activationBlock(key, locale, eyebrow) {
    const a = ACTIVATION[key];
    if (!a) return '';
    if (a.kind === 'button') {
        const label = a.label[locale] || a.label.it;
        const note  = a.note ? (a.note[locale] || a.note.it) : '';
        return `
        <table cellpadding="0" cellspacing="0" style="margin-top:16px">
          <tr><td>
            <a href="${a.url}" target="_blank" rel="noopener noreferrer" style="display:inline-block;background:${GOLD};color:#fff;font-size:13px;font-weight:700;text-decoration:none;padding:11px 22px;border-radius:8px;letter-spacing:.1px">${escHtml(label)}</a>
          </td></tr>
        </table>
        ${note ? `<p style="margin:9px 0 0;font-size:12px;color:${TEXT_MUTED}">${escHtml(note)}</p>` : ''}`;
    }
    const text = a.text[locale] || a.text.it;
    return `
        <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:16px;background:${GOLD_SOFT};border:1px solid ${GOLD_BORDER};border-radius:8px">
          <tr><td style="padding:12px 14px">
            <p style="margin:0 0 3px;font-size:10.5px;font-weight:700;color:${GOLD};text-transform:uppercase;letter-spacing:.6px">${escHtml(eyebrow)}</p>
            <p style="margin:0;font-size:12.5px;color:#6b5530;line-height:1.55">${escHtml(text)}</p>
          </td></tr>
        </table>`;
}

/**
 * Soggetto email di consegna licenza (evasione manuale).
 * @param {string} locale
 * @param {string} orderId
 * @returns {string}
 */
export function licenseSubject(locale, orderId) {
    const t = i18n[locale] || i18n.it;
    return t.license_subject.replace('{orderId}', orderId);
}

/**
 * Genera il corpo HTML dell'email di consegna licenza, per evasione manuale
 * (vedi sendInternalOrderNotificationOnce in email.js — l'ammin riceve una
 * notifica interna e invia questa email al cliente a mano, chiave alla mano).
 *
 * @param {object} data
 * @param {string} data.locale
 * @param {string} data.orderId
 * @param {string} data.name — nome del cliente
 * @param {Array<{productName:string, sku?:string, key:string, activation?:string}>} data.items
 *   — `activation` è opzionale: chiave in ACTIVATION (es. 'windows', 'office',
 *   'kaspersky') per aggiungere un pulsante o un box di istruzioni sotto la chiave.
 * @returns {string} HTML
 */
export function licenseEmailHtml({ locale, orderId, name, items }) {
    locale = locale || 'it';
    const t    = i18n[locale] || i18n.it;
    const year = new Date().getFullYear();

    const greeting = t.license_greeting.replace('{name}', escHtml(name || ''));
    const list  = items || [];
    const multi = list.length > 1;

    const cards = list.map((item, i) => `
    <table width="100%" cellpadding="0" cellspacing="0" style="background:${CARD_BG};border:1px solid ${BORDER};border-radius:12px;margin-bottom:14px">
      <tr><td style="padding:20px 22px">
        <table cellpadding="0" cellspacing="0" style="width:100%;margin-bottom:14px">
          <tr>
            ${multi ? `<td width="26" valign="top" style="padding-right:10px;padding-top:1px">
              <table cellpadding="0" cellspacing="0"><tr><td width="22" height="22" align="center" valign="middle" style="background:${ACCENT_DARK};border-radius:50%;font-family:${HEADING_FONT};font-size:11px;font-weight:700;color:#fff">${i + 1}</td></tr></table>
            </td>` : ''}
            <td valign="top">
              <p style="margin:0 0 2px;font-size:15.5px;font-weight:700;color:${TEXT}">${escHtml(item.productName || '')}</p>
              ${item.sku ? `<p style="margin:0;font-size:11.5px;color:${TEXT_FAINT};font-family:'SFMono-Regular',Consolas,monospace;letter-spacing:.2px">${escHtml(item.sku)}</p>` : ''}
            </td>
          </tr>
        </table>

        <p style="margin:0 0 6px;font-size:11px;color:${TEXT_MUTED};text-transform:uppercase;letter-spacing:.6px;font-weight:600">${t.license_key_label}</p>
        <table width="100%" cellpadding="0" cellspacing="0" style="background:${BG};border:1px solid ${BORDER};border-radius:9px">
          <tr><td style="padding:13px 16px">
            <span style="font-family:'SFMono-Regular',Consolas,monospace;font-size:17px;font-weight:700;color:${ACCENT_DARK};letter-spacing:.6px;word-break:break-all">${escHtml(item.key || '')}</span>
          </td></tr>
        </table>
        <p style="margin:6px 2px 0;font-size:11px;color:${TEXT_FAINT};font-style:italic">${t.license_copy_hint}</p>

        ${activationBlock(item.activation, locale, t.activation_eyebrow)}
      </td></tr>
    </table>`).join('');

    return `<!DOCTYPE html>
<html lang="${escHtml(locale)}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${licenseSubject(locale, orderId)}</title>
<style>
  @font-face{font-family:'Montserrat';src:url('https://eurolicenze.com/fonts/montserrat-latin-700.woff2') format('woff2');font-weight:700}
  @font-face{font-family:'Montserrat';src:url('https://eurolicenze.com/fonts/montserrat-latin-800.woff2') format('woff2');font-weight:800}
</style>
</head>
<body style="margin:0;padding:0;background:${BG};font-family:${BODY_FONT}">
<table width="100%" cellpadding="0" cellspacing="0" style="background:${BG};padding:32px 16px">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;box-shadow:0 6px 28px rgba(20,36,58,0.12)">

  <!-- Logo header -->
  <tr><td style="background:${ACCENT_DARK};border-top:4px solid ${GOLD};border-radius:10px 10px 0 0;padding:22px 32px;text-align:center">
    <table cellpadding="0" cellspacing="0" style="display:inline-block;background:#ffffff;border-radius:8px;padding:8px 16px">
      <tr><td>
        <img src="https://eurolicenze.com/logo/logo-header-400.webp" alt="Aml Store" width="140" height="auto"
             style="display:block;max-width:140px">
      </td></tr>
    </table>
  </td></tr>

  <!-- Body card -->
  <tr><td style="background:${CARD_BG};padding:36px 32px 28px;border-left:1px solid ${BORDER};border-right:1px solid ${BORDER}">

    <p style="margin:0 0 12px;font-size:11px;font-weight:700;color:${GOLD};text-transform:uppercase;letter-spacing:1.1px">${t.license_eyebrow} · Aml Store</p>

    <table cellpadding="0" cellspacing="0" style="margin-bottom:24px">
      <tr>
        <td width="40" valign="top" style="padding-right:12px">
          <table cellpadding="0" cellspacing="0"><tr><td width="36" height="36" align="center" valign="middle" style="background:${SUCCESS_SOFT};border-radius:50%;font-size:18px;color:${SUCCESS}">🔑</td></tr></table>
        </td>
        <td valign="middle">
          <h1 style="margin:0 0 4px;font-family:${HEADING_FONT};font-size:23px;font-weight:800;color:${TEXT};letter-spacing:-.2px">${greeting}</h1>
          <p style="margin:0;font-size:14.5px;color:${TEXT_MUTED};line-height:1.5">${t.license_intro}</p>
        </td>
      </tr>
    </table>

    <table cellpadding="0" cellspacing="0" style="width:100%;margin-bottom:24px;padding-bottom:20px;border-bottom:1px dashed ${BORDER}">
      <tr>
        <td>
          <p style="margin:0 0 5px;font-size:11px;color:${TEXT_MUTED};text-transform:uppercase;letter-spacing:.6px;font-weight:600">${t.order_id}</p>
          <p style="margin:0;font-size:17px;font-weight:800;color:${ACCENT_DARK};font-family:'SFMono-Regular',Consolas,monospace;letter-spacing:.2px">${escHtml(orderId)}</p>
        </td>
      </tr>
    </table>

    ${cards}

    <p style="margin:20px 0 0;font-size:12px;color:${TEXT_MUTED};line-height:1.5">🔒&nbsp; ${t.license_note}</p>

  </td></tr>

  <!-- Footer -->
  <tr><td style="background:#f0f2f5;border-radius:0 0 10px 10px;padding:22px 32px;border:1px solid ${BORDER};border-top:none;text-align:center">
    <p style="margin:0 0 8px;font-size:13px;color:${TEXT_MUTED}">${t.license_help} <a href="mailto:Info@amlstore.it" style="color:${ACCENT_DARK};font-weight:600">Info@amlstore.it</a></p>
    <p style="margin:0 0 10px;font-size:11px;color:#9ca3af">${t.footer_copy.replace('{year}', year)}</p>
    <p style="margin:0;font-size:10.5px;color:#b0b5bd;letter-spacing:.3px">${t.footer_tagline}</p>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>`;
}

/**
 * Genera plain text fallback per l'email di consegna licenza.
 * @param {object} data — vedi licenseEmailHtml
 * @returns {string}
 */
export function licenseEmailText({ locale, orderId, name, items }) {
    locale = locale || 'it';
    const t = i18n[locale] || i18n.it;

    const lines = [
        `Aml Store`,
        t.license_greeting.replace('{name}', name || ''),
        ``,
        t.license_intro,
        ``,
        `${t.order_id}: ${orderId}`,
        ``,
    ];

    (items || []).forEach(item => {
        lines.push(`${item.productName}${item.sku ? ' (' + item.sku + ')' : ''}`);
        lines.push(`${t.license_key_label}: ${item.key}`);
        const a = ACTIVATION[item.activation];
        if (a) {
            if (a.kind === 'button') {
                const label = a.label[locale] || a.label.it;
                lines.push(`${label} ${a.url}`);
                if (a.note) lines.push(a.note[locale] || a.note.it);
            } else {
                lines.push(`${t.activation_eyebrow}: ${a.text[locale] || a.text.it}`);
            }
        }
        lines.push(``);
    });

    lines.push(t.license_note, ``, `${t.license_help} Info@amlstore.it`);

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
