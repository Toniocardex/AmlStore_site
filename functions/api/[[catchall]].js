/**
 * functions/api/[[catchall]].js
 * Cloudflare Pages Function — gestisce tutte le route /api/*
 *
 * Routes pubbliche:
 *   POST /api/stripe-create-session
 *   GET  /api/stripe-return
 *   POST /api/webhooks/stripe
 *   POST /api/paypal-create-order
 *   POST /api/paypal-capture-order
 *   POST /api/bank-transfer-order
 *   GET  /api/order-status
 *
 * Routes admin (protette da Cloudflare Access + verifica JWT):
 *   GET  /api/admin/orders
 *   GET  /api/admin/orders/:id
 *   POST /api/admin/orders/:id/mark-paid
 *   POST /api/admin/orders/:id/archive
 *   POST /api/admin/orders/:id/unarchive
 */

import { generateToken, verifyToken }                    from './_lib/token.js';
import { createOrder, getOrderById, getOrderByStripeSession,
         getOrderByPaypalOrderId, setStripeSession,
         setPaypalOrderId, markPaidStripe, markPaidPaypal,
         toPublicOrder }                                  from './_lib/order.js';
import { createCheckoutSession, verifyStripeWebhook }    from './_lib/stripe.js';
import { getAccessToken, createPaypalOrder,
         capturePaypalOrder }                            from './_lib/paypal.js';
import { sendConfirmationOnce,
         sendInternalOrderNotificationOnce }             from './_lib/email.js';
import { resolveAdminAuth, listOrders, getOrderDetail,
         markBankTransferPaid, archiveOrder,
         unarchiveOrder, deleteOrder }                   from './_lib/admin.js';
import { resolveAndValidateItems }                     from './_lib/catalog.js';

/* ─── CORS ──────────────────────────────────────────────────────────────────── */

const ALLOWED_ORIGINS = [
    'https://aml-store.com',
    'http://localhost:8788',
    'http://127.0.0.1:8788',
];
const ALLOWED_LOCALES = new Set(['it', 'en', 'fr', 'de', 'es']);
const MAX_JSON_BODY_BYTES = 32 * 1024;
const MAX_ADMIN_JSON_BODY_BYTES = 4 * 1024;

function allowedOrigins(env = {}) {
    const origins = new Set(ALLOWED_ORIGINS);
    if (env.SITE_ORIGIN) origins.add(env.SITE_ORIGIN);
    return origins;
}

function corsHeaders(request, env = {}) {
    const origin = request.headers.get('Origin') || '';
    const allow  = allowedOrigins(env).has(origin) ? origin : (env.SITE_ORIGIN || ALLOWED_ORIGINS[0]);
    return {
        'Access-Control-Allow-Origin':  allow,
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    };
}

function json(data, status = 200, request = null, env = null) {
    return new Response(JSON.stringify(data), {
        status,
        headers: {
            'Content-Type': 'application/json',
            ...(request ? corsHeaders(request, env || {}) : {}),
        },
    });
}

function err(msg, status = 400, request = null, env = null) {
    return json({ error: msg }, status, request, env);
}

/* ─── Entry point Pages Function ────────────────────────────────────────────── */

export async function onRequest(context) {
    const { request, env } = context;
    const url  = new URL(request.url);
    const path = url.pathname;

    // CORS preflight
    if (request.method === 'OPTIONS') {
        return new Response(null, { status: 204, headers: corsHeaders(request, env) });
    }

    try {
        // ── Admin routes (protette da Cloudflare Access + JWT) ───────────────────
        if (path.startsWith('/api/admin/')) {
            return await handleAdminRoute(path, request, env);
        }

        // ── Routes pubbliche ─────────────────────────────────────────────────────
        if (path === '/api/stripe-create-session' && request.method === 'POST') {
            return await handleStripeCreateSession(request, env);
        }
        if (path === '/api/stripe-return' && request.method === 'GET') {
            return await handleStripeReturn(request, env);
        }
        if (path === '/api/webhooks/stripe' && request.method === 'POST') {
            return await handleStripeWebhook(request, env);
        }
        if (path === '/api/paypal-create-order' && request.method === 'POST') {
            return await handlePaypalCreateOrder(request, env);
        }
        if (path === '/api/paypal-capture-order' && request.method === 'POST') {
            return await handlePaypalCaptureOrder(request, env);
        }
        if (path === '/api/bank-transfer-order' && request.method === 'POST') {
            return await handleBankTransferOrder(request, env);
        }
        if (path === '/api/order-status' && request.method === 'GET') {
            return await handleOrderStatus(request, env);
        }
        if (path === '/api/paypal-config' && request.method === 'GET') {
            return handlePaypalConfig(request, env);
        }

        return err('Not found', 404, request);

    } catch (e) {
        console.error('[Worker] Unhandled error:', e?.message || e);
        return err('Internal server error', 500, request);
    }
}

/* ─── Helpers condivisi ──────────────────────────────────────────────────────── */

function totalMinorFromItems(items) {
    return items.reduce((s, i) => s + i.unit_amount_minor * i.qty, 0);
}

function isAllowedCheckoutOrigin(request, env) {
    const origin = request.headers.get('Origin') || '';
    return Boolean(origin && allowedOrigins(env).has(origin));
}

function isJsonContentType(request) {
    const type = request.headers.get('Content-Type') || '';
    return type.toLowerCase().split(';', 1)[0].trim() === 'application/json';
}

function requestBodyTooLarge(request) {
    const len = Number(request.headers.get('Content-Length') || 0);
    return Number.isFinite(len) && len > MAX_JSON_BODY_BYTES;
}

function validateCheckoutRequest(request, env) {
    if (!isAllowedCheckoutOrigin(request, env)) {
        return err('Origin non consentita', 403, request, env);
    }
    if (!isJsonContentType(request)) {
        return err('Content-Type non valido', 415, request, env);
    }
    if (requestBodyTooLarge(request)) {
        return err('Payload troppo grande', 413, request, env);
    }
    return null;
}

function adminJson(data, status = 200) {
    return new Response(JSON.stringify(data), {
        status,
        headers: { 'Content-Type': 'application/json' },
    });
}

function validateAdminMutationRequest(request, env, { requireJson = true } = {}) {
    const origin = request.headers.get('Origin') || '';
    if (!origin || !allowedOrigins(env).has(origin)) {
        return adminJson({ error: 'Forbidden', reason: 'origin_not_allowed' }, 403);
    }
    const len = Number(request.headers.get('Content-Length') || 0);
    if (Number.isFinite(len) && len > MAX_ADMIN_JSON_BODY_BYTES) {
        return adminJson({ error: 'Payload too large', reason: 'payload_too_large' }, 413);
    }
    if (requireJson && !isJsonContentType(request)) {
        return adminJson({ error: 'Unsupported Media Type', reason: 'invalid_content_type' }, 415);
    }
    return null;
}

function adminDeleteEnabled(env) {
    return String(env.ADMIN_ALLOW_DELETE_ORDERS || '') === '1';
}

function normalizeAdminNotes(v) {
    const notes = cleanString(v, 1000);
    return notes || null;
}

function validateEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(v || ''));
}

function validatePIVA(v) {
    v = String(v || '').trim();
    if (!/^\d{11}$/.test(v)) return false;
    let s = 0;
    for (let i = 0; i <= 9; i += 2) s += parseInt(v[i], 10);
    for (let j = 1; j <= 9; j += 2) {
        const d = parseInt(v[j], 10) * 2;
        s += d > 9 ? d - 9 : d;
    }
    return (10 - (s % 10)) % 10 === parseInt(v[10], 10);
}

function cleanString(v, maxLen = 120) {
    return String(v || '').trim().slice(0, maxLen);
}

function normalizeIdempotencyKey(v) {
    const key = cleanString(v, 96);
    if (!key) return crypto.randomUUID();
    if (!/^[A-Za-z0-9._:-]{8,96}$/.test(key)) {
        throw Object.assign(new Error('Idempotency key non valida'), { status: 400 });
    }
    return key;
}

function validateCustomer(rawCustomer, rawLang) {
    const c = rawCustomer || {};
    const lang = cleanString(rawLang || 'it', 2).toLowerCase();
    if (!ALLOWED_LOCALES.has(lang)) throw Object.assign(new Error('Lingua non valida'), { status: 400 });

    const type = cleanString(c.type || 'private', 16).toLowerCase();
    if (!['private', 'business'].includes(type)) {
        throw Object.assign(new Error('Tipo cliente non valido'), { status: 400 });
    }

    const customer = {
        type,
        firstName: cleanString(c.firstName, 80),
        lastName: cleanString(c.lastName, 80),
        email: cleanString(c.email, 254).toLowerCase(),
        phone: cleanString(c.phone, 40) || null,
        ragioneSociale: cleanString(c.ragioneSociale, 160),
        piva: cleanString(c.piva, 20).replace(/\s+/g, ''),
        sdi: cleanString(c.sdi, 20).toUpperCase(),
        pec: cleanString(c.pec, 254).toLowerCase(),
    };

    if (!customer.firstName) throw Object.assign(new Error('Nome cliente mancante'), { status: 400 });
    if (!customer.lastName) throw Object.assign(new Error('Cognome cliente mancante'), { status: 400 });
    if (!validateEmail(customer.email)) throw Object.assign(new Error('Email cliente non valida'), { status: 400 });
    if (customer.phone && customer.phone.length < 7) {
        throw Object.assign(new Error('Telefono cliente non valido'), { status: 400 });
    }

    if (type === 'business') {
        if (!customer.ragioneSociale) throw Object.assign(new Error('Ragione sociale mancante'), { status: 400 });
        if (!validatePIVA(customer.piva)) throw Object.assign(new Error('Partita IVA non valida'), { status: 400 });
        if (!customer.sdi && !customer.pec) {
            throw Object.assign(new Error('Inserire Codice SDI o PEC'), { status: 400 });
        }
        if (customer.sdi && !/^[A-Z0-9]{7}$/.test(customer.sdi)) {
            throw Object.assign(new Error('Codice SDI non valido'), { status: 400 });
        }
        if (customer.pec && !validateEmail(customer.pec)) {
            throw Object.assign(new Error('PEC non valida'), { status: 400 });
        }
    } else {
        customer.ragioneSociale = '';
        customer.piva = '';
        customer.sdi = '';
        customer.pec = '';
    }

    return { customer, lang };
}

/**
 * Costruisce i parametri ordine dal body JSON del checkout.
 */
function orderParamsFromBody(body, paymentMethod) {
    const { customer: c, lang } = validateCustomer(body.customer, body.lang);
    let items;
    try {
        items = resolveAndValidateItems(body.items);
    } catch (catalogErr) {
        throw Object.assign(new Error(catalogErr.message || 'Invalid catalog'), { status: 400 });
    }
    return {
        idempotencyKey:    normalizeIdempotencyKey(body.idempotencyKey),
        customerEmail:     c.email,
        customerFirstName: c.firstName,
        customerLastName:  c.lastName,
        customerCompany:   c.ragioneSociale || null,
        customerType:      c.type,
        customerPhone:     c.phone || null,
        customerPiva:      c.piva || null,
        customerSdi:       c.sdi || null,
        customerPec:       c.pec || null,
        locale:            lang,
        lineItems:         items,
        totalMinor:        totalMinorFromItems(items),
        currency:          (items[0]?.currency) || 'EUR',
        paymentMethod,
    };
}

/* ─── GET /api/paypal-config ────────────────────────────────────────────────── */
// Espone il Client ID PayPal (dato pubblico: finisce comunque nell'URL dell'SDK).
// Sandbox o live dipendono solo dalla config dell'ambiente: niente ID hardcodato
// nel frontend. Se non configurato il frontend disabilita PayPal con messaggio.

function handlePaypalConfig(request, env) {
    return json({ clientId: env.PAYPAL_CLIENT_ID || '' }, 200, request, env);
}

/* ─── POST /api/stripe-create-session ───────────────────────────────────────── */

function orderParamsFromBodySafe(body, paymentMethod, request, env) {
    try {
        return orderParamsFromBody(body, paymentMethod);
    } catch (e) {
        if (e.status === 400) return { error: err(e.message, 400, request, env) };
        throw e;
    }
}

async function handleStripeCreateSession(request, env) {
    const invalidRequest = validateCheckoutRequest(request, env);
    if (invalidRequest) return invalidRequest;

    const body = await request.json().catch(() => null);
    if (!body) return err('Invalid JSON', 400, request, env);

    const paramsOrErr = orderParamsFromBodySafe(body, 'stripe', request, env);
    if (paramsOrErr.error) return paramsOrErr.error;
    const params = paramsOrErr;

    // Crea ordine in D1
    let orderId;
    try {
        orderId = await createOrder(env.DB, params);
    } catch (dbErr) {
        // UNIQUE constraint: idempotency_key già presente → riusa l'ordine esistente.
        // Si prosegue comunque con createCheckoutSession: l'Idempotency-Key Stripe
        // (= orderId) fa restituire la stessa sessione, quindi il client riceve
        // sempre una url valida anche su retry.
        if (String(dbErr).includes('UNIQUE')) {
            const existing = await env.DB
                .prepare('SELECT id, status FROM orders WHERE idempotency_key = ?')
                .bind(params.idempotencyKey).first();
            if (!existing?.id) throw dbErr;
            if (existing.status === 'paid') {
                return err('Ordine già pagato', 409, request, env);
            }
            orderId = existing.id;
        } else {
            throw dbErr;
        }
    }

    const origin     = env.SITE_ORIGIN || 'https://aml-store.com';
    const lang       = params.locale || 'it';
    const successUrl = `${origin}/api/stripe-return?sid={CHECKOUT_SESSION_ID}&lang=${lang}`;
    const cancelUrl  = `${origin}/${lang}/checkout?cancelled=1`;

    // Crea Stripe Checkout Session
    const session = await createCheckoutSession(env.STRIPE_SECRET_KEY, {
        orderId,
        customerEmail: params.customerEmail,
        lineItems:     params.lineItems,
        locale:        lang,
        successUrl,
        cancelUrl,
    });

    // Salva stripe_session_id sull'ordine
    await setStripeSession(env.DB, orderId, session.id);

    return json({ url: session.url, orderId }, 200, request, env);
}

/* ─── GET /api/stripe-return ────────────────────────────────────────────────── */
// Stripe redirige qui dopo pagamento con {CHECKOUT_SESSION_ID}
// Il Worker verifica, genera token, redirige alla thank-you page.

async function handleStripeReturn(request, env) {
    const url  = new URL(request.url);
    const sid  = url.searchParams.get('sid');
    const rawLang = (url.searchParams.get('lang') || 'it').toLowerCase();
    const lang = ALLOWED_LOCALES.has(rawLang) ? rawLang : 'it';

    const origin = env.SITE_ORIGIN || 'https://aml-store.com';

    if (!sid) {
        return Response.redirect(`${origin}/${lang}/checkout?error=missing_sid`, 302);
    }

    const order = await getOrderByStripeSession(env.DB, sid);
    if (!order) {
        return Response.redirect(`${origin}/${lang}/checkout?error=order_not_found`, 302);
    }

    const token = await generateToken(env.TOKEN_SECRET, order.id);
    const dest  = `${origin}/${lang}/checkout-success?oid=${token.oid}&exp=${token.exp}&t=${encodeURIComponent(token.t)}`;

    return Response.redirect(dest, 302);
}

/* ─── POST /api/webhooks/stripe ─────────────────────────────────────────────── */

async function handleStripeWebhook(request, env) {
    const rawBody  = await request.text();
    const sigHeader = request.headers.get('Stripe-Signature') || '';

    let event;
    try {
        event = await verifyStripeWebhook(rawBody, sigHeader, env.STRIPE_WEBHOOK_SECRET);
    } catch (e) {
        console.error('[webhook/stripe] Firma non valida:', e.message);
        return new Response('Unauthorized', { status: 401 });
    }

    // Gestiamo solo checkout.session.completed
    if (event.type === 'checkout.session.completed') {
        const session = event.data?.object;
        const stripeSessionId      = session?.id;
        const stripePaymentIntent  = session?.payment_intent;

        const order = await getOrderByStripeSession(env.DB, stripeSessionId);
        if (!order) {
            console.warn('[webhook/stripe] Ordine non trovato per session:', stripeSessionId);
            return new Response('OK', { status: 200 }); // Ack comunque a Stripe
        }

        if (order.status !== 'paid') {
            await markPaidStripe(env.DB, order.id, { stripeSessionId, stripePaymentIntent });
            // Rileggi ordine aggiornato per il template email
            const updatedOrder = await getOrderById(env.DB, order.id);
            await sendConfirmationOnce(
                env.DB, updatedOrder,
                env.RESEND_API_KEY, env.TRUSTPILOT_BCC || '',
                'webhook_stripe'
            );
            await sendInternalOrderNotificationOnce(
                env.DB, updatedOrder,
                env.RESEND_API_KEY,
                'webhook_stripe'
            );
        }
    }

    return new Response('OK', { status: 200 });
}

/* ─── POST /api/paypal-create-order ─────────────────────────────────────────── */

async function handlePaypalCreateOrder(request, env) {
    const invalidRequest = validateCheckoutRequest(request, env);
    if (invalidRequest) return invalidRequest;

    const body = await request.json().catch(() => null);
    if (!body) return err('Invalid JSON', 400, request, env);

    const paramsOrErr = orderParamsFromBodySafe(body, 'paypal', request, env);
    if (paramsOrErr.error) return paramsOrErr.error;
    const params = paramsOrErr;

    // Crea ordine in D1
    let orderId;
    try {
        orderId = await createOrder(env.DB, params);
    } catch (dbErr) {
        if (String(dbErr).includes('UNIQUE')) {
            const existing = await env.DB
                .prepare('SELECT id FROM orders WHERE idempotency_key = ?')
                .bind(params.idempotencyKey).first();
            orderId = existing?.id;
            if (!orderId) throw dbErr;
        } else {
            throw dbErr;
        }
    }

    // Crea ordine su PayPal
    const accessToken = await getAccessToken(
        env.PAYPAL_BASE_URL, env.PAYPAL_CLIENT_ID, env.PAYPAL_CLIENT_SECRET
    );

    const totalStr     = (params.totalMinor / 100).toFixed(2);
    const paypalOrderId = await createPaypalOrder(env.PAYPAL_BASE_URL, accessToken, {
        orderId,
        totalMinorStr: totalStr,
        currency:      params.currency,
        lineItems:     params.lineItems,
    });

    await setPaypalOrderId(env.DB, orderId, paypalOrderId);

    return json({ orderID: paypalOrderId, amlOrderId: orderId }, 200, request, env);
}

/* ─── POST /api/paypal-capture-order ────────────────────────────────────────── */

async function handlePaypalCaptureOrder(request, env) {
    const invalidRequest = validateCheckoutRequest(request, env);
    if (invalidRequest) return invalidRequest;

    const body = await request.json().catch(() => null);
    if (!body?.orderID) return err('orderID mancante', 400, request, env);

    const paypalOrderId = body.orderID;

    const order = await getOrderByPaypalOrderId(env.DB, paypalOrderId);
    if (!order) return err('Ordine non trovato', 404, request, env);

    // Cattura pagamento su PayPal
    const accessToken = await getAccessToken(
        env.PAYPAL_BASE_URL, env.PAYPAL_CLIENT_ID, env.PAYPAL_CLIENT_SECRET
    );
    const { captureId, status, amountValue, currencyCode } = await capturePaypalOrder(
        env.PAYPAL_BASE_URL, accessToken, paypalOrderId
    );

    if (status !== 'COMPLETED') {
        return err(`PayPal capture status: ${status}`, 402, request, env);
    }

    const capturedMinor = Math.round(Number(amountValue) * 100);
    if (
        !Number.isFinite(capturedMinor) ||
        capturedMinor !== Number(order.total_minor) ||
        String(currencyCode || '').toUpperCase() !== String(order.currency || 'EUR').toUpperCase()
    ) {
        console.error('[paypal-capture] Importo o valuta non coerenti:', {
            paypalOrderId,
            capturedMinor,
            currencyCode,
            expectedMinor: order.total_minor,
            expectedCurrency: order.currency,
        });
        return err('Importo PayPal non coerente con ordine', 409, request, env);
    }

    // Aggiorna ordine D1
    await markPaidPaypal(env.DB, order.id, { paypalOrderId, paypalCaptureId: captureId });

    // Invia email
    const updatedOrder = await getOrderById(env.DB, order.id);
    await sendConfirmationOnce(
        env.DB, updatedOrder,
        env.RESEND_API_KEY, env.TRUSTPILOT_BCC || '',
        'worker_capture'
    );
    await sendInternalOrderNotificationOnce(
        env.DB, updatedOrder,
        env.RESEND_API_KEY,
        'worker_capture'
    );

    // Genera token thank-you
    const token = await generateToken(env.TOKEN_SECRET, order.id);

    return json({ oid: token.oid, exp: token.exp, t: token.t }, 200, request, env);
}

/* ─── POST /api/bank-transfer-order ─────────────────────────────────────────── */

async function handleBankTransferOrder(request, env) {
    const invalidRequest = validateCheckoutRequest(request, env);
    if (invalidRequest) return invalidRequest;

    const body = await request.json().catch(() => null);
    if (!body) return err('Invalid JSON', 400, request, env);

    const paramsOrErr = orderParamsFromBodySafe(body, 'bank_transfer', request, env);
    if (paramsOrErr.error) return paramsOrErr.error;
    const params = paramsOrErr;

    // Crea ordine in D1
    let orderId;
    try {
        orderId = await createOrder(env.DB, params);
    } catch (dbErr) {
        if (String(dbErr).includes('UNIQUE')) {
            const existing = await env.DB
                .prepare('SELECT id FROM orders WHERE idempotency_key = ?')
                .bind(params.idempotencyKey).first();
            orderId = existing?.id;
            if (!orderId) throw dbErr;
        } else {
            throw dbErr;
        }
    }

    // Per il bonifico invia subito email "ordine ricevuto + istruzioni IBAN"
    // (status = pending_payment, isPaid = false nel template → mostra IBAN + causale)
    const newOrder = await getOrderById(env.DB, orderId);
    await sendConfirmationOnce(
        env.DB, newOrder,
        env.RESEND_API_KEY, env.TRUSTPILOT_BCC || '',
        'bank_transfer_created'
    );
    await sendInternalOrderNotificationOnce(
        env.DB, newOrder,
        env.RESEND_API_KEY,
        'bank_transfer_created'
    );

    // Genera token thank-you
    const token = await generateToken(env.TOKEN_SECRET, orderId);

    return json({
        oid:     token.oid,
        exp:     token.exp,
        t:       token.t,
        causale: orderId,  // mostrato anche in pagina
    }, 200, request, env);
}

/* ─── Admin routes ───────────────────────────────────────────────────────────── */

/**
 * Middleware + dispatcher per tutte le route /api/admin/*
 * Ogni richiesta viene prima autenticata via JWT Cloudflare Access.
 * Le API admin sono same-origin (no CORS aggiuntivo): la UI è su /admin/
 * protetto dallo stesso Cloudflare Access Policy.
 */
async function handleAdminRoute(path, request, env) {
    // ── Autenticazione JWT ────────────────────────────────────────────────────
    const jwt = await resolveAdminAuth(request, env);
    if (!jwt.valid) {
        console.warn('[admin] JWT non valido:', jwt.reason);
        return new Response(JSON.stringify({ error: 'Unauthorized', reason: jwt.reason }), {
            status: 401,
            headers: { 'Content-Type': 'application/json' },
        });
    }
    const actorEmail = jwt.email;

    // Sotto-path dopo /api/admin
    const sub = path.slice('/api/admin'.length); // es. '/orders' o '/orders/AML-xxx/mark-paid'

    // ── GET /api/admin/orders ─────────────────────────────────────────────────
    if (sub === '/orders' && request.method === 'GET') {
        const qs              = new URL(request.url).searchParams;
        const result = await listOrders(env.DB, {
            page:            Number(qs.get('page'))   || 1,
            status:          qs.get('status')          || '',
            paymentMethod:   qs.get('paymentMethod')   || '',
            search:          qs.get('search')          || '',
            includeArchived: qs.get('archived') === '1',
        });
        result.capabilities = { deleteOrders: adminDeleteEnabled(env) };
        return new Response(JSON.stringify(result), {
            headers: { 'Content-Type': 'application/json' },
        });
    }

    // ── GET /api/admin/orders/:id ─────────────────────────────────────────────
    const detailMatch = sub.match(/^\/orders\/([^/]+)$/);
    if (detailMatch && request.method === 'GET') {
        const orderId = detailMatch[1];
        const order   = await getOrderDetail(env.DB, orderId);
        if (!order) {
            return new Response(JSON.stringify({ error: 'Order not found' }), {
                status: 404, headers: { 'Content-Type': 'application/json' },
            });
        }
        return new Response(JSON.stringify(order), {
            headers: { 'Content-Type': 'application/json' },
        });
    }

    // ── POST /api/admin/orders/:id/mark-paid ─────────────────────────────────
    const markPaidMatch = sub.match(/^\/orders\/([^/]+)\/mark-paid$/);
    if (markPaidMatch && request.method === 'POST') {
        const invalidRequest = validateAdminMutationRequest(request, env);
        if (invalidRequest) return invalidRequest;

        const orderId = markPaidMatch[1];
        const body    = await request.json().catch(() => ({}));
        const notes   = normalizeAdminNotes(body.notes);

        const result = await markBankTransferPaid(
            env.DB, orderId, actorEmail, notes,
            env.RESEND_API_KEY || '', env.TRUSTPILOT_BCC || ''
        );

        const status = result.ok ? 200 : (result.reason === 'order_not_found' ? 404 : 409);
        return new Response(JSON.stringify(result), {
            status, headers: { 'Content-Type': 'application/json' },
        });
    }

    // ── POST /api/admin/orders/:id/archive ────────────────────────────────────
    const archiveMatch = sub.match(/^\/orders\/([^/]+)\/archive$/);
    if (archiveMatch && request.method === 'POST') {
        const invalidRequest = validateAdminMutationRequest(request, env);
        if (invalidRequest) return invalidRequest;

        await archiveOrder(env.DB, archiveMatch[1]);
        return new Response(JSON.stringify({ ok: true }), {
            headers: { 'Content-Type': 'application/json' },
        });
    }

    // ── POST /api/admin/orders/:id/unarchive ──────────────────────────────────
    const unarchiveMatch = sub.match(/^\/orders\/([^/]+)\/unarchive$/);
    if (unarchiveMatch && request.method === 'POST') {
        const invalidRequest = validateAdminMutationRequest(request, env);
        if (invalidRequest) return invalidRequest;

        await unarchiveOrder(env.DB, unarchiveMatch[1]);
        return new Response(JSON.stringify({ ok: true }), {
            headers: { 'Content-Type': 'application/json' },
        });
    }

    // ── DELETE /api/admin/orders/:id ──────────────────────────────────────────
    const deleteMatch = sub.match(/^\/orders\/([^/]+)$/);
    if (deleteMatch && request.method === 'DELETE') {
        const invalidRequest = validateAdminMutationRequest(request, env, { requireJson: false });
        if (invalidRequest) return invalidRequest;
        if (!adminDeleteEnabled(env)) {
            return adminJson({ ok: false, error: 'Delete disabled', reason: 'delete_disabled' }, 403);
        }

        const orderId = deleteMatch[1];
        const result  = await deleteOrder(env.DB, orderId);
        const status  = result.ok ? 200 : (result.reason === 'order_not_found' ? 404 : 409);
        return new Response(JSON.stringify(result), {
            status, headers: { 'Content-Type': 'application/json' },
        });
    }

    return new Response(JSON.stringify({ error: 'Not found' }), {
        status: 404, headers: { 'Content-Type': 'application/json' },
    });
}

/* ─── GET /api/order-status ─────────────────────────────────────────────────── */

async function handleOrderStatus(request, env) {
    const url = new URL(request.url);
    const oid = url.searchParams.get('oid');
    const exp = url.searchParams.get('exp');
    const t   = url.searchParams.get('t');

    // Verifica token
    const check = await verifyToken(env.TOKEN_SECRET, oid, exp, t);
    if (!check.valid) {
        const status = check.reason === 'expired' ? 410 : 401;
        return err(check.reason || 'invalid_token', status, request);
    }

    const order = await getOrderById(env.DB, oid);
    if (!order) return err('order_not_found', 404, request);

    return json(toPublicOrder(order), 200, request);
}
