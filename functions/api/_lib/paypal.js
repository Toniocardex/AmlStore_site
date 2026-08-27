/**
 * paypal.js — helper PayPal REST API per Eurolicenze Worker.
 * Usa fetch nativo, zero dipendenze npm.
 * PAYPAL_BASE_URL in wrangler.toml: sandbox o live.
 */

/**
 * Ottiene un access token PayPal (OAuth 2.0 client_credentials).
 * Il token dura ~9h; per semplicità lo rigeneriamo ad ogni request.
 * Per ottimizzare in futuro: cache in Workers KV con TTL.
 *
 * @param {string} baseUrl       — env var PAYPAL_BASE_URL
 * @param {string} clientId      — env var PAYPAL_CLIENT_ID
 * @param {string} clientSecret  — env var PAYPAL_CLIENT_SECRET
 * @returns {Promise<string>}    — access token
 */
export async function getAccessToken(baseUrl, clientId, clientSecret) {
    const credentials = btoa(`${clientId}:${clientSecret}`);

    const res = await fetch(`${baseUrl}/v1/oauth2/token`, {
        method: 'POST',
        headers: {
            'Authorization': `Basic ${credentials}`,
            'Content-Type':  'application/x-www-form-urlencoded',
        },
        body: 'grant_type=client_credentials',
    });

    const data = await res.json();
    if (!res.ok || !data.access_token) {
        throw new Error(`PayPal auth error ${res.status}: ${JSON.stringify(data)}`);
    }

    return data.access_token;
}

/**
 * Crea un ordine PayPal (intent=CAPTURE).
 *
 * @param {string} baseUrl
 * @param {string} accessToken
 * @param {object} params
 * @param {string} params.orderId         — orderId interno (per reference_id)
 * @param {string} params.totalMinorStr   — es. "19.99"
 * @param {string} params.currency        — es. "EUR"
 * @param {object[]} params.lineItems     — [{name, qty, unit_amount_minor, currency}]
 * @param {string} params.returnUrl       — URL dopo approvazione (non usato con JS SDK)
 * @param {string} params.cancelUrl
 * @returns {Promise<string>} — PayPal order ID
 */
export async function createPaypalOrder(baseUrl, accessToken, {
    orderId,
    totalMinorStr,
    currency,
    lineItems,
}) {
    const cur = (currency || 'EUR').toUpperCase();

    const body = {
        intent: 'CAPTURE',
        purchase_units: [{
            reference_id: orderId,
            amount: {
                currency_code: cur,
                value: totalMinorStr,
                breakdown: {
                    item_total: {
                        currency_code: cur,
                        value: totalMinorStr,
                    },
                },
            },
            items: lineItems.map(item => ({
                name:        (item.name || item.sku || 'Prodotto').slice(0, 127),
                quantity:    String(item.qty || 1),
                unit_amount: {
                    currency_code: cur,
                    value: (item.unit_amount_minor / 100).toFixed(2),
                },
            })),
        }],
    };

    const res = await fetch(`${baseUrl}/v2/checkout/orders`, {
        method: 'POST',
        headers: {
            'Authorization':  `Bearer ${accessToken}`,
            'Content-Type':   'application/json',
            'PayPal-Request-Id': orderId,  // idempotency key PayPal
        },
        body: JSON.stringify(body),
    });

    const data = await res.json();
    if (!res.ok || !data.id) {
        throw new Error(`PayPal create order error ${res.status}: ${JSON.stringify(data)}`);
    }

    return data.id;
}

/**
 * Cattura un ordine PayPal approvato.
 *
 * @param {string} baseUrl
 * @param {string} accessToken
 * @param {string} paypalOrderId — ID ordine PayPal (dal frontend)
 * @returns {Promise<{ captureId: string, status: string, amountValue: string, currencyCode: string, payer: {email: string, firstName: string, lastName: string} }>}
 */
export async function capturePaypalOrder(baseUrl, accessToken, paypalOrderId) {
    const res = await fetch(`${baseUrl}/v2/checkout/orders/${paypalOrderId}/capture`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type':  'application/json',
        },
        body: '{}',
    });

    const data = await res.json();
    if (!res.ok) {
        throw new Error(`PayPal capture error ${res.status}: ${JSON.stringify(data)}`);
    }

    // Estrai capture ID dalla prima purchase_unit
    const capture = data?.purchase_units?.[0]?.payments?.captures?.[0] || {};
    const captureId = capture.id || null;
    // Identità del payer restituita da PayPal (l'Express checkout non passa mai
    // da un form nostro: è l'unica fonte per nome/email del cliente).
    const payer = {
        email:     data?.payer?.email_address || '',
        firstName: data?.payer?.name?.given_name || '',
        lastName:  data?.payer?.name?.surname || '',
    };
    return {
        captureId,
        status: data.status,
        amountValue: capture.amount?.value || '',
        currencyCode: capture.amount?.currency_code || '',
        payer,
    };
}

/**
 * Recupera i dettagli di un ordine PayPal (incluso il payer) senza catturarlo.
 * Usato dal webhook per riconciliare ordini il cui capture client-side non è
 * mai arrivato: la risorsa PAYMENT.CAPTURE.COMPLETED del webhook non include
 * il payer (sta solo sull'Order), quindi va richiesto a parte.
 *
 * @param {string} baseUrl
 * @param {string} accessToken
 * @param {string} paypalOrderId
 * @returns {Promise<{ status: string, payer: {email: string, firstName: string, lastName: string} }>}
 */
export async function getPaypalOrder(baseUrl, accessToken, paypalOrderId) {
    const res = await fetch(`${baseUrl}/v2/checkout/orders/${paypalOrderId}`, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${accessToken}` },
    });
    const data = await res.json();
    if (!res.ok) {
        throw new Error(`PayPal get order error ${res.status}: ${JSON.stringify(data)}`);
    }
    return {
        status: data.status,
        payer: {
            email:     data?.payer?.email_address || '',
            firstName: data?.payer?.name?.given_name || '',
            lastName:  data?.payer?.name?.surname || '',
        },
    };
}

/**
 * Verifica la firma di un webhook PayPal chiamando l'endpoint ufficiale
 * v1/notifications/verify-webhook-signature (PayPal non usa un HMAC locale
 * come Stripe: la verifica va fatta lato loro).
 *
 * @param {string} baseUrl
 * @param {string} accessToken
 * @param {object} headers  — header HTTP della richiesta webhook (oggetto piatto, chiavi lowercase)
 * @param {string} webhookId — env var PAYPAL_WEBHOOK_ID (configurato nel dashboard PayPal)
 * @param {string} rawBody   — corpo grezzo della richiesta webhook (stringa)
 * @returns {Promise<boolean>}
 */
export async function verifyPaypalWebhookSignature(baseUrl, accessToken, headers, webhookId, rawBody) {
    if (!webhookId) return false;

    let event;
    try {
        event = JSON.parse(rawBody);
    } catch (_) {
        return false;
    }

    const body = {
        transmission_id:   headers['paypal-transmission-id'],
        transmission_time: headers['paypal-transmission-time'],
        cert_url:           headers['paypal-cert-url'],
        auth_algo:           headers['paypal-auth-algo'],
        transmission_sig:   headers['paypal-transmission-sig'],
        webhook_id:          webhookId,
        webhook_event:       event,
    };

    if (!body.transmission_id || !body.transmission_time || !body.cert_url ||
        !body.auth_algo || !body.transmission_sig) {
        return false;
    }

    const res = await fetch(`${baseUrl}/v1/notifications/verify-webhook-signature`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type':  'application/json',
        },
        body: JSON.stringify(body),
    });

    const data = await res.json().catch(() => null);
    return Boolean(res.ok && data?.verification_status === 'SUCCESS');
}
