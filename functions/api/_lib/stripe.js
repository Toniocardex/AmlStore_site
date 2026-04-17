/**
 * stripe.js — helper Stripe per Aml Store Worker.
 * Usa fetch nativo (no Stripe SDK, zero dipendenze npm).
 */

const STRIPE_API = 'https://api.stripe.com/v1';

/**
 * Crea una Stripe Checkout Session.
 *
 * @param {string} stripeSecretKey — env var STRIPE_SECRET_KEY
 * @param {object} params
 * @param {string} params.orderId         — orderId interno (per metadata e idempotency)
 * @param {string} params.customerEmail
 * @param {object[]} params.lineItems     — [{name, qty, unit_amount_minor, currency}]
 * @param {string} params.locale          — it|en|fr|de|es
 * @param {string} params.successUrl      — URL a cui Stripe redirige dopo pagamento
 * @param {string} params.cancelUrl       — URL a cui Stripe redirige se annullato
 * @returns {Promise<{ id: string, url: string }>}
 */
export async function createCheckoutSession(stripeSecretKey, {
    orderId,
    customerEmail,
    lineItems,
    locale,
    successUrl,
    cancelUrl,
}) {
    // Stripe usa application/x-www-form-urlencoded
    const params = new URLSearchParams();

    params.set('mode', 'payment');
    params.set('customer_email', customerEmail);
    params.set('success_url', successUrl);
    params.set('cancel_url', cancelUrl);
    params.set('locale', stripeLocale(locale));
    params.set('metadata[order_id]', orderId);
    params.set('metadata[locale]', locale);
    params.set('payment_intent_data[metadata][order_id]', orderId);

    // Righe ordine
    lineItems.forEach(function(item, i) {
        params.set(`line_items[${i}][price_data][currency]`,     (item.currency || 'eur').toLowerCase());
        params.set(`line_items[${i}][price_data][unit_amount]`,  String(item.unit_amount_minor || 0));
        params.set(`line_items[${i}][price_data][product_data][name]`, item.name || item.sku || 'Prodotto');
        params.set(`line_items[${i}][quantity]`,                 String(item.qty || 1));
    });

    const res = await fetch(`${STRIPE_API}/checkout/sessions`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${stripeSecretKey}`,
            'Content-Type':  'application/x-www-form-urlencoded',
            'Idempotency-Key': orderId,  // orderId come idempotency key Stripe
        },
        body: params.toString(),
    });

    const data = await res.json();
    if (!res.ok) {
        throw new Error(`Stripe error ${res.status}: ${data?.error?.message || JSON.stringify(data)}`);
    }

    return { id: data.id, url: data.url };
}

/**
 * Verifica la firma di un webhook Stripe.
 * Implementazione manuale HMAC-SHA256 (algoritmo v1 di Stripe).
 *
 * @param {string} rawBody          — corpo raw della request (string)
 * @param {string} signatureHeader  — header 'Stripe-Signature'
 * @param {string} webhookSecret    — env var STRIPE_WEBHOOK_SECRET (whsec_...)
 * @param {number} [toleranceSec=300]
 * @returns {Promise<object>} — evento Stripe parsed
 * @throws {Error} se firma non valida o timestamp fuori tolleranza
 */
export async function verifyStripeWebhook(rawBody, signatureHeader, webhookSecret, toleranceSec = 300) {
    if (!signatureHeader) throw new Error('Missing Stripe-Signature header');

    // Parsing header: "t=1234,v1=abc,v1=def"
    const parts = Object.fromEntries(
        signatureHeader.split(',').map(p => p.split('='))
    );
    const timestamp = parts['t'];
    const v1Sigs    = signatureHeader.split(',')
        .filter(p => p.startsWith('v1='))
        .map(p => p.slice(3));

    if (!timestamp || v1Sigs.length === 0) {
        throw new Error('Invalid Stripe-Signature format');
    }

    // Controllo tolleranza temporale
    const age = Math.floor(Date.now() / 1000) - Number(timestamp);
    if (Math.abs(age) > toleranceSec) {
        throw new Error(`Stripe webhook timestamp out of tolerance (${age}s)`);
    }

    // Calcola firma attesa
    const payload    = `${timestamp}.${rawBody}`;
    const key        = await crypto.subtle.importKey(
        'raw',
        new TextEncoder().encode(webhookSecret),
        { name: 'HMAC', hash: 'SHA-256' },
        false,
        ['sign']
    );
    const sigBuf     = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(payload));
    const expectedHex = Array.from(new Uint8Array(sigBuf))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');

    if (!v1Sigs.includes(expectedHex)) {
        throw new Error('Stripe webhook signature mismatch');
    }

    return JSON.parse(rawBody);
}

/**
 * Mappa locale sito → locale Stripe.
 * @param {string} lang
 * @returns {string}
 */
function stripeLocale(lang) {
    const map = { it: 'it', en: 'en', fr: 'fr', de: 'de', es: 'es' };
    return map[lang] || 'it';
}
