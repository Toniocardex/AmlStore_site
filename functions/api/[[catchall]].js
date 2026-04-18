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
import { sendConfirmationOnce }                          from './_lib/email.js';
import { verifyAccessJwt, listOrders, getOrderDetail,
         markBankTransferPaid, archiveOrder,
         unarchiveOrder }                                from './_lib/admin.js';

/* ─── CORS ──────────────────────────────────────────────────────────────────── */

const ALLOWED_ORIGINS = ['https://aml-store.com', 'http://localhost:8788'];

function corsHeaders(request) {
    const origin = request.headers.get('Origin') || '';
    const allow  = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
    return {
        'Access-Control-Allow-Origin':  allow,
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    };
}

function json(data, status = 200, request = null) {
    return new Response(JSON.stringify(data), {
        status,
        headers: {
            'Content-Type': 'application/json',
            ...(request ? corsHeaders(request) : {}),
        },
    });
}

function err(msg, status = 400, request = null) {
    return json({ error: msg }, status, request);
}

/* ─── Entry point Pages Function ────────────────────────────────────────────── */

export async function onRequest(context) {
    const { request, env } = context;
    const url  = new URL(request.url);
    const path = url.pathname;

    // CORS preflight
    if (request.method === 'OPTIONS') {
        return new Response(null, { status: 204, headers: corsHeaders(request) });
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

        return err('Not found', 404, request);

    } catch (e) {
        console.error('[Worker] Unhandled error:', e?.message || e);
        return err('Internal server error', 500, request);
    }
}

/* ─── Helpers condivisi ──────────────────────────────────────────────────────── */

/**
 * Normalizza i line_items dal frontend al formato interno.
 * Il frontend invia gli item del cart.js (unitAmount in centesimi, quantity).
 */
function normalizeItems(rawItems) {
    return (rawItems || []).map(item => ({
        sku:               item.sku || '',
        name:              item.name || item.sku || 'Prodotto',
        qty:               Number(item.quantity) || 1,
        unit_amount_minor: Math.round(Number(item.unitAmount || item.unit_amount_minor) || 0),
        currency:          (item.currency || 'EUR').toUpperCase(),
    }));
}

function totalMinorFromItems(items) {
    return items.reduce((s, i) => s + i.unit_amount_minor * i.qty, 0);
}

/**
 * Costruisce i parametri ordine dal body JSON del checkout.
 */
function orderParamsFromBody(body, paymentMethod) {
    const c = body.customer || {};
    const items = normalizeItems(body.items);
    return {
        idempotencyKey:    body.idempotencyKey || crypto.randomUUID(),
        customerEmail:     (c.email || '').trim().toLowerCase(),
        customerFirstName: (c.firstName || '').trim(),
        customerLastName:  (c.lastName  || '').trim(),
        customerCompany:   (c.ragioneSociale || '').trim() || null,
        customerType:      c.type     || 'private',
        customerPhone:     c.phone    || null,
        customerPiva:      c.piva     || null,
        customerSdi:       c.sdi      || null,
        customerPec:       c.pec      || null,
        locale:            body.lang  || 'it',
        lineItems:         items,
        totalMinor:        totalMinorFromItems(items),
        currency:          (items[0]?.currency) || 'EUR',
        paymentMethod,
    };
}

/* ─── POST /api/stripe-create-session ───────────────────────────────────────── */

async function handleStripeCreateSession(request, env) {
    const body = await request.json().catch(() => null);
    if (!body) return err('Invalid JSON', 400, request);

    const params = orderParamsFromBody(body, 'stripe');
    if (!params.customerEmail) return err('Email cliente mancante', 400, request);

    // Crea ordine in D1
    let orderId;
    try {
        orderId = await createOrder(env.DB, params);
    } catch (dbErr) {
        // UNIQUE constraint: idempotency_key già presente → cerca ordine esistente
        if (String(dbErr).includes('UNIQUE')) {
            const existing = await env.DB
                .prepare('SELECT id, stripe_session_id FROM orders WHERE idempotency_key = ?')
                .bind(params.idempotencyKey).first();
            if (existing?.stripe_session_id) {
                // Recupera URL sessione Stripe esistente (non ancora completata)
                return json({ orderId: existing.id }, 200, request);
            }
            orderId = existing?.id;
        } else {
            throw dbErr;
        }
    }

    const origin     = env.SITE_ORIGIN || 'https://aml-store.com';
    const lang       = params.locale || 'it';
    const successUrl = `${origin}/api/stripe-return?sid={CHECKOUT_SESSION_ID}&lang=${lang}`;
    const cancelUrl  = `${origin}/${lang}/checkout.html?cancelled=1`;

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

    return json({ url: session.url, orderId }, 200, request);
}

/* ─── GET /api/stripe-return ────────────────────────────────────────────────── */
// Stripe redirige qui dopo pagamento con {CHECKOUT_SESSION_ID}
// Il Worker verifica, genera token, redirige alla thank-you page.

async function handleStripeReturn(request, env) {
    const url  = new URL(request.url);
    const sid  = url.searchParams.get('sid');
    const lang = url.searchParams.get('lang') || 'it';

    const origin = env.SITE_ORIGIN || 'https://aml-store.com';

    if (!sid) {
        return Response.redirect(`${origin}/${lang}/checkout.html?error=missing_sid`, 302);
    }

    const order = await getOrderByStripeSession(env.DB, sid);
    if (!order) {
        return Response.redirect(`${origin}/${lang}/checkout.html?error=order_not_found`, 302);
    }

    const token = await generateToken(env.TOKEN_SECRET, order.id);
    const dest  = `${origin}/${lang}/checkout-success.html?oid=${token.oid}&exp=${token.exp}&t=${encodeURIComponent(token.t)}`;

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
        }
    }

    return new Response('OK', { status: 200 });
}

/* ─── POST /api/paypal-create-order ─────────────────────────────────────────── */

async function handlePaypalCreateOrder(request, env) {
    const body = await request.json().catch(() => null);
    if (!body) return err('Invalid JSON', 400, request);

    const params = orderParamsFromBody(body, 'paypal');
    if (!params.customerEmail) return err('Email cliente mancante', 400, request);

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

    return json({ orderID: paypalOrderId, amlOrderId: orderId }, 200, request);
}

/* ─── POST /api/paypal-capture-order ────────────────────────────────────────── */

async function handlePaypalCaptureOrder(request, env) {
    const body = await request.json().catch(() => null);
    if (!body?.orderID) return err('orderID mancante', 400, request);

    const paypalOrderId = body.orderID;

    const order = await getOrderByPaypalOrderId(env.DB, paypalOrderId);
    if (!order) return err('Ordine non trovato', 404, request);

    // Cattura pagamento su PayPal
    const accessToken = await getAccessToken(
        env.PAYPAL_BASE_URL, env.PAYPAL_CLIENT_ID, env.PAYPAL_CLIENT_SECRET
    );
    const { captureId, status } = await capturePaypalOrder(
        env.PAYPAL_BASE_URL, accessToken, paypalOrderId
    );

    if (status !== 'COMPLETED') {
        return err(`PayPal capture status: ${status}`, 402, request);
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

    // Genera token thank-you
    const token = await generateToken(env.TOKEN_SECRET, order.id);

    return json({ oid: token.oid, exp: token.exp, t: token.t }, 200, request);
}

/* ─── POST /api/bank-transfer-order ─────────────────────────────────────────── */

async function handleBankTransferOrder(request, env) {
    const body = await request.json().catch(() => null);
    if (!body) return err('Invalid JSON', 400, request);

    const params = orderParamsFromBody(body, 'bank_transfer');
    if (!params.customerEmail) return err('Email cliente mancante', 400, request);

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

    // Genera token thank-you
    const token = await generateToken(env.TOKEN_SECRET, orderId);

    return json({
        oid:     token.oid,
        exp:     token.exp,
        t:       token.t,
        causale: orderId,  // mostrato anche in pagina
    }, 200, request);
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
    const jwt = await verifyAccessJwt(request, env);
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
        const orderId = markPaidMatch[1];
        const body    = await request.json().catch(() => ({}));
        const notes   = body.notes || null;

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
        await archiveOrder(env.DB, archiveMatch[1]);
        return new Response(JSON.stringify({ ok: true }), {
            headers: { 'Content-Type': 'application/json' },
        });
    }

    // ── POST /api/admin/orders/:id/unarchive ──────────────────────────────────
    const unarchiveMatch = sub.match(/^\/orders\/([^/]+)\/unarchive$/);
    if (unarchiveMatch && request.method === 'POST') {
        await unarchiveOrder(env.DB, unarchiveMatch[1]);
        return new Response(JSON.stringify({ ok: true }), {
            headers: { 'Content-Type': 'application/json' },
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
