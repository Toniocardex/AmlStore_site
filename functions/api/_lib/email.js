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
import { markConfirmationEmailSent, markPaidNotificationSent } from './order.js';
import { safeParseJSON }                                from './utils.js';

const RESEND_API = 'https://api.resend.com/emails';
const FROM       = 'Aml Store <ordini@aml-store.com>';
const REPLY_TO   = 'Info@amlstore.it';

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
        ...overrides,
    };
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
