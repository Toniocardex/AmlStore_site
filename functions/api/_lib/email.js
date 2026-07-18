/**
 * email.js — invio email transazionale via Resend + idempotenza.
 *
 * sendConfirmationOnce   — email ordine (pending o paid). Stripe/PayPal/BT iniziale.
 * sendPaidNotificationOnce — email "pagamento ricevuto" per bonifico marcato pagato da admin.
 *
 * Entrambe sono idempotenti: controllano il flag DB prima di chiamare Resend
 * e aggiornano il flag solo dopo un 2xx. Retry sicuro.
 */

import { emailSubject, emailHtml, emailText }          from './templates.js';
import { markConfirmationEmailSent, markPaidNotificationSent,
         markInternalNotificationSent }                from './order.js';
import { safeParseJSON }                                from './utils.js';

const RESEND_API = 'https://api.resend.com/emails';
const FROM       = 'Aml Store <ordini@aml-store.com>';
const REPLY_TO   = 'Info@amlstore.it';
const INTERNAL_RECIPIENTS = ['Info@amlstore.it', 'Antonino.cardelli@outlook.it'];

/* ─── Helpers interni ────────────────────────────────────────────────────────── */

function buildRecipient(order) {
    return `${order.customer_first_name} ${order.customer_last_name} <${order.customer_email}>`;
}

function buildOrderForTemplate(order, overrides = {}) {
    const locale = order.locale || 'it';
    return {
        orderId:       order.id,
        status:        order.status,
        paymentMethod: order.payment_method,
        payment_method: order.payment_method,
        createdAt:     order.created_at,
        paidAt:        order.paid_at,
        firstName:     order.customer_first_name,
        lastName:      order.customer_last_name,
        email:         order.customer_email,
        locale,
        currency:      order.currency,
        totalMinor:    order.total_minor,
        lineItems:     safeParseJSON(order.line_items, []),
        stripe_session_id:     order.stripe_session_id,
        stripe_payment_intent: order.stripe_payment_intent,
        paypal_order_id:       order.paypal_order_id,
        paypal_capture_id:     order.paypal_capture_id,
        requiresShipping: Boolean(order.requires_shipping),
        shipping: order.requires_shipping ? {
            addressLine1: order.shipping_address_line1,
            city:         order.shipping_city,
            postalCode:   order.shipping_postal_code,
            province:     order.shipping_province,
            country:      order.shipping_country,
        } : undefined,
        ...overrides,
    };
}

function esc(str) {
    return String(str || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function formatMoney(minor, currency) {
    try {
        return new Intl.NumberFormat('it-IT', {
            style: 'currency',
            currency: (currency || 'EUR').toUpperCase(),
        }).format(Number(minor || 0) / 100);
    } catch (_) {
        return 'EUR ' + (Number(minor || 0) / 100).toFixed(2);
    }
}

function methodLabel(method) {
    return {
        stripe: 'Carta / Stripe',
        paypal: 'PayPal',
        bank_transfer: 'Bonifico bancario',
    }[method] || method || 'N/D';
}

function internalSubject(order) {
    const paid = order.status === 'paid';
    const prefix = paid ? 'Nuovo ordine pagato' : 'Nuovo ordine bonifico';
    const action = paid ? 'inviare licenza' : 'attendere pagamento';
    return `[Aml Store] ${prefix} ${order.id} - ${action}`;
}

function internalOrderHtml(order) {
    const items = safeParseJSON(order.line_items, []);
    const isPaid = order.status === 'paid';
    const actionText = isPaid
        ? 'PAGAMENTO CONFERMATO: inviare manualmente la licenza al cliente.'
        : 'BONIFICO IN ATTESA: non inviare la licenza finche il pagamento non risulta ricevuto.';

    const rows = items.map((item) => {
        const qty = Number(item.qty || item.quantity || 1);
        const unit = Number(item.unit_amount_minor || item.unitAmount || 0);
        const subMinor = Math.round(unit) * qty;
        const actionLabel = item.physical
            ? '<span style="color:#1d4ed8">SPEDIRE FISICAMENTE</span>'
            : '<span style="color:#b45309">DA INVIARE MANUALMENTE</span>';
        return `
            <tr>
                <td style="padding:10px;border-bottom:1px solid #e5e7eb">${esc(item.name || item.sku || 'Prodotto')}</td>
                <td style="padding:10px;border-bottom:1px solid #e5e7eb;font-family:monospace">${esc(item.sku || 'N/D')}</td>
                <td style="padding:10px;border-bottom:1px solid #e5e7eb;text-align:center">${qty}</td>
                <td style="padding:10px;border-bottom:1px solid #e5e7eb;text-align:right">${formatMoney(subMinor, order.currency)}</td>
                <td style="padding:10px;border-bottom:1px solid #e5e7eb;font-weight:700">${actionLabel}</td>
            </tr>`;
    }).join('');

    const shippingBlock = order.requires_shipping ? `
          <h2 style="font-size:16px;margin:18px 0 10px">Indirizzo di spedizione</h2>
          <p style="margin:0 0 18px;padding:12px;background:#eff6ff;border:1px solid #bfdbfe;border-radius:6px;color:#1e3a8a">
            ${esc(order.shipping_address_line1)}<br>
            ${esc(order.shipping_postal_code)} ${esc(order.shipping_city)}${order.shipping_province ? ' (' + esc(order.shipping_province) + ')' : ''}<br>
            ${esc(order.shipping_country)}
          </p>` : '';

    return `<!DOCTYPE html>
<html lang="it">
<head><meta charset="UTF-8"><title>${esc(internalSubject(order))}</title></head>
<body style="margin:0;background:#f5f6f8;font-family:Arial,sans-serif;color:#1f2937">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:24px;background:#f5f6f8">
    <tr><td align="center">
      <table width="760" cellpadding="0" cellspacing="0" style="width:100%;max-width:760px;background:#fff;border:1px solid #e5e7eb;border-radius:8px;overflow:hidden">
        <tr><td style="background:#111827;color:#fff;padding:18px 24px">
          <h1 style="font-size:20px;margin:0">Nuovo ordine Aml Store</h1>
          <p style="margin:6px 0 0;color:#d1d5db">${esc(actionText)}</p>
        </td></tr>
        <tr><td style="padding:22px 24px">
          <h2 style="font-size:16px;margin:0 0 10px">Riepilogo ordine</h2>
          <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:18px">
            ${infoRow('Numero ordine', order.id)}
            ${infoRow('Stato', order.status)}
            ${infoRow('Metodo pagamento', methodLabel(order.payment_method))}
            ${infoRow('Totale', formatMoney(order.total_minor, order.currency))}
            ${infoRow('Cliente', `${order.customer_first_name || ''} ${order.customer_last_name || ''}`.trim())}
            ${infoRow('Email cliente', order.customer_email)}
            ${infoRow('Telefono', order.customer_phone || 'N/D')}
          </table>

          <h2 style="font-size:16px;margin:18px 0 10px">Articoli acquistati</h2>
          <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #e5e7eb;border-collapse:collapse">
            <thead>
              <tr style="background:#f9fafb">
                <th style="padding:10px;text-align:left">Prodotto</th>
                <th style="padding:10px;text-align:left">ID articolo / SKU</th>
                <th style="padding:10px;text-align:center">Qta</th>
                <th style="padding:10px;text-align:right">Subtotale</th>
                <th style="padding:10px;text-align:left">Licenza</th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
          ${shippingBlock}
          <p style="margin:18px 0 0;padding:12px;background:#fffbeb;border:1px solid #fcd34d;border-radius:6px;color:#92400e">
            ${esc(actionText)}
          </p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>`;
}

function internalOrderText(order) {
    const items = safeParseJSON(order.line_items, []);
    const isPaid = order.status === 'paid';
    const actionText = isPaid
        ? 'PAGAMENTO CONFERMATO: inviare manualmente la licenza al cliente.'
        : 'BONIFICO IN ATTESA: non inviare la licenza finche il pagamento non risulta ricevuto.';

    const lines = [
        'Nuovo ordine Aml Store',
        actionText,
        '',
        `Numero ordine: ${order.id}`,
        `Stato: ${order.status}`,
        `Metodo pagamento: ${methodLabel(order.payment_method)}`,
        `Totale: ${formatMoney(order.total_minor, order.currency)}`,
        `Cliente: ${order.customer_first_name || ''} ${order.customer_last_name || ''}`.trim(),
        `Email cliente: ${order.customer_email}`,
        `Telefono: ${order.customer_phone || 'N/D'}`,
        '',
        'Articoli acquistati:',
    ];

    items.forEach((item) => {
        const qty = Number(item.qty || item.quantity || 1);
        const unit = Number(item.unit_amount_minor || item.unitAmount || 0);
        const subMinor = Math.round(unit) * qty;
        lines.push(
            `- ${item.name || item.sku || 'Prodotto'}`,
            `  ID articolo / SKU: ${item.sku || 'N/D'}`,
            `  Quantita: ${qty}`,
            `  Subtotale: ${formatMoney(subMinor, order.currency)}`,
            `  Licenza: ${item.physical ? 'SPEDIRE FISICAMENTE' : 'DA INVIARE MANUALMENTE'}`,
        );
    });

    if (order.requires_shipping) {
        lines.push(
            '',
            'Indirizzo di spedizione:',
            order.shipping_address_line1,
            `${order.shipping_postal_code} ${order.shipping_city}${order.shipping_province ? ' (' + order.shipping_province + ')' : ''}`,
            order.shipping_country,
        );
    }

    lines.push('', actionText);
    return lines.join('\n');
}

function infoRow(label, value) {
    return `<tr>
        <td style="padding:4px 0;color:#6b7280;width:170px">${esc(label)}</td>
        <td style="padding:4px 0;font-weight:700">${esc(value || 'N/D')}</td>
    </tr>`;
}

async function callResend(apiKey, payload) {
    let res;
    try {
        res = await fetch(RESEND_API, {
            method:  'POST',
            headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
            body:    JSON.stringify(payload),
        });
    } catch (e) {
        console.error('[email] Resend network error:', e);
        return { ok: false, error: 'network_error' };
    }
    if (!res.ok) {
        const body = await res.text().catch(() => '');
        console.error(`[email] Resend HTTP ${res.status}:`, body);
        return { ok: false, error: `resend_http_${res.status}` };
    }
    return { ok: true };
}

/* ─── Export pubblici ────────────────────────────────────────────────────────── */

/**
 * Invia l'email di conferma ordine al massimo una volta.
 * Usata per: Stripe paid (via webhook), PayPal paid (via capture), BT creato (pending).
 *
 * BCC Trustpilot incluso solo se isPaid=true.
 *
 * @param {D1Database} db
 * @param {object}  order         — riga grezza D1
 * @param {string}  resendApiKey
 * @param {string}  trustpilotBcc — '' se non configurato
 * @param {string}  eventSrc      — es. 'webhook_stripe', 'bank_transfer_created', ...
 */
export async function sendConfirmationOnce(db, order, resendApiKey, trustpilotBcc, eventSrc) {
    if (order.confirmation_email_sent_at) return { sent: false, skipped: true };
    if (!resendApiKey) {
        console.warn('[email] RESEND_API_KEY non configurato');
        return { sent: false, error: 'no_resend_key' };
    }

    const isPaid  = order.status === 'paid';
    const locale  = order.locale || 'it';
    const tpl     = buildOrderForTemplate(order, {
        causale: order.payment_method === 'bank_transfer' ? order.id : undefined,
    });

    const payload = {
        from:     FROM,
        to:       [buildRecipient(order)],
        subject:  emailSubject(locale, order.id, isPaid),
        html:     emailHtml(tpl, isPaid),
        text:     emailText(tpl, isPaid),
        reply_to: REPLY_TO,
    };
    if (trustpilotBcc && isPaid) payload.bcc = [trustpilotBcc];

    const { ok, error } = await callResend(resendApiKey, payload);
    if (!ok) return { sent: false, error };

    try {
        await markConfirmationEmailSent(db, order.id, eventSrc);
    } catch (e) {
        console.error('[email] Impossibile aggiornare confirmation_email_sent_at:', e);
    }

    return { sent: true };
}

/**
 * Invia una notifica operativa interna per evasione manuale licenza.
 * Destinatari fissi: Info@amlstore.it e Antonino.cardelli@outlook.it.
 */
export async function sendInternalOrderNotificationOnce(db, order, resendApiKey, eventSrc) {
    if (order.internal_notification_sent_at) return { sent: false, skipped: true };
    if (!resendApiKey) {
        console.warn('[email] RESEND_API_KEY non configurato, notifica interna non inviata');
        return { sent: false, error: 'no_resend_key' };
    }

    const payload = {
        from:     FROM,
        to:       INTERNAL_RECIPIENTS,
        subject:  internalSubject(order),
        html:     internalOrderHtml(order),
        text:     internalOrderText(order),
        reply_to: REPLY_TO,
    };

    const { ok, error } = await callResend(resendApiKey, payload);
    if (!ok) return { sent: false, error };

    try {
        await markInternalNotificationSent(db, order.id, eventSrc);
    } catch (e) {
        console.error('[email] Impossibile aggiornare internal_notification_sent_at:', e);
    }

    return { sent: true };
}

/**
 * Invia la email "pagamento ricevuto" per ordini bonifico marcati pagati dall'admin.
 * Usa il flag paid_notification_sent_at (separato da confirmation_email_sent_at).
 * BCC Trustpilot SEMPRE incluso (ordine effettivamente pagato).
 *
 * @param {D1Database} db
 * @param {object}  order         — riga grezza D1 (già aggiornata a status='paid')
 * @param {string}  resendApiKey
 * @param {string}  trustpilotBcc
 */
export async function sendPaidNotificationOnce(db, order, resendApiKey, trustpilotBcc) {
    if (order.paid_notification_sent_at) return { sent: false, skipped: true };
    if (!resendApiKey) {
        console.warn('[email] RESEND_API_KEY non configurato, email non inviata');
        return { sent: false, error: 'no_resend_key' };
    }

    const locale = order.locale || 'it';
    const tpl    = buildOrderForTemplate(order, { status: 'paid', causale: undefined });

    const payload = {
        from:     FROM,
        to:       [buildRecipient(order)],
        subject:  emailSubject(locale, order.id, true),
        html:     emailHtml(tpl, true),
        text:     emailText(tpl, true),
        reply_to: REPLY_TO,
    };
    if (trustpilotBcc) payload.bcc = [trustpilotBcc];

    const { ok, error } = await callResend(resendApiKey, payload);
    if (!ok) return { sent: false, error };

    try {
        await markPaidNotificationSent(db, order.id);
    } catch (e) {
        console.error('[email] Impossibile aggiornare paid_notification_sent_at:', e);
    }

    return { sent: true };
}
