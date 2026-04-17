/**
 * email.js — invio email transazionale via Resend + idempotenza.
 *
 * sendConfirmationOnce:
 *   1. Controlla confirmation_email_sent_at in D1 → se già valorizzato, skip.
 *   2. Costruisce payload Resend con HTML + plain text + BCC Trustpilot.
 *   3. Chiama Resend API.
 *   4. Solo se 2xx: aggiorna confirmation_email_sent_at in D1.
 *   5. Se Resend fallisce: non aggiorna il flag → retry sicuro.
 */

import { emailSubject, emailHtml, emailText } from './templates.js';
import { markConfirmationEmailSent }           from './order.js';

const RESEND_API = 'https://api.resend.com/emails';
const FROM       = 'Aml Store <ordini@aml-store.com>';

/**
 * Invia l'email di conferma ordine al massimo una volta.
 * Thread-safe a livello di singola Worker invocation grazie al flag DB.
 *
 * @param {D1Database} db
 * @param {object}     order        — riga grezza da D1 (non toPublicOrder)
 * @param {string}     resendApiKey — env var RESEND_API_KEY
 * @param {string}     trustpilotBcc — env var TRUSTPILOT_BCC (può essere '')
 * @param {string}     eventSrc     — es. 'webhook_stripe', 'worker_capture', ...
 * @returns {Promise<{ sent: boolean, skipped?: boolean, error?: string }>}
 */
export async function sendConfirmationOnce(db, order, resendApiKey, trustpilotBcc, eventSrc) {
    // ── Idempotenza: già inviata? ──────────────────────────────────────────────
    if (order.confirmation_email_sent_at) {
        return { sent: false, skipped: true };
    }

    const isPaid  = order.status === 'paid';
    const locale  = order.locale  || 'it';

    // Costruiamo un "order arricchito" per i template
    const orderForTemplate = {
        orderId:       order.id,
        status:        order.status,
        paymentMethod: order.payment_method,
        createdAt:     order.created_at,
        paidAt:        order.paid_at,
        firstName:     order.customer_first_name,
        lastName:      order.customer_last_name,
        email:         order.customer_email,
        locale:        locale,
        currency:      order.currency,
        totalMinor:    order.total_minor,
        lineItems:     safeParseJSON(order.line_items, []),
        causale:       order.payment_method === 'bank_transfer' ? order.id : undefined,
        // Campi PSP per plain text / template
        stripe_session_id:      order.stripe_session_id,
        stripe_payment_intent:  order.stripe_payment_intent,
        paypal_order_id:        order.paypal_order_id,
        paypal_capture_id:      order.paypal_capture_id,
    };

    // ── Payload Resend ─────────────────────────────────────────────────────────
    const payload = {
        from:    FROM,
        to:      [`${order.customer_first_name} ${order.customer_last_name} <${order.customer_email}>`],
        subject: emailSubject(locale, order.id, isPaid),
        html:    emailHtml(orderForTemplate, isPaid),
        text:    emailText(orderForTemplate, isPaid),
        // Reply-To admin
        reply_to: 'Info@amlstore.it',
    };

    // BCC Trustpilot solo se lo slot è configurato e l'ordine è pagato
    // (non ha senso invitare a recensire un ordine non ancora pagato)
    if (trustpilotBcc && isPaid) {
        payload.bcc = [trustpilotBcc];
    }

    // ── Chiama Resend ──────────────────────────────────────────────────────────
    let resendRes;
    try {
        resendRes = await fetch(RESEND_API, {
            method:  'POST',
            headers: {
                'Authorization': `Bearer ${resendApiKey}`,
                'Content-Type':  'application/json',
            },
            body: JSON.stringify(payload),
        });
    } catch (networkErr) {
        console.error('[email] Resend network error:', networkErr);
        return { sent: false, error: 'network_error' };
    }

    if (!resendRes.ok) {
        const body = await resendRes.text().catch(() => '');
        console.error(`[email] Resend HTTP ${resendRes.status}:`, body);
        return { sent: false, error: `resend_http_${resendRes.status}` };
    }

    // ── Solo dopo 2xx: aggiorna flag idempotenza ───────────────────────────────
    try {
        await markConfirmationEmailSent(db, order.id, eventSrc);
    } catch (dbErr) {
        // Email inviata ma flag non aggiornato → log per debug, non bloccare
        console.error('[email] Impossibile aggiornare confirmation_email_sent_at:', dbErr);
    }

    return { sent: true };
}

function safeParseJSON(raw, fallback) {
    try { return JSON.parse(raw || 'null') ?? fallback; } catch (_) { return fallback; }
}
