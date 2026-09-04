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
 *   POST /api/paypal-express-create-order
 *   POST /api/webhooks/paypal
 *   POST /api/bank-transfer-order
 *   GET  /api/order-status
 *   GET  /api/stock
 *   POST /api/consultation-request
 *   POST /api/restock-request
 *   GET  /api/restock-cancel
 *   POST /api/restock-cancel
 *   POST /api/cart/sync
 *   POST /api/track
 *
 * Routes admin (protette da Cloudflare Access + verifica JWT):
 *   GET  /api/admin/orders
 *   GET  /api/admin/orders/:id
 *   POST /api/admin/orders/:id/mark-paid
 *   POST /api/admin/orders/:id/archive
 *   POST /api/admin/orders/:id/unarchive
 *   GET  /api/admin/stock
 *   POST /api/admin/stock
 *   GET  /api/admin/restock
 *   GET  /api/admin/carts
 *   GET  /api/admin/analytics
 */

import { generateToken, verifyToken }                    from './_lib/token.js';
import { createOrder, getOrderById, getOrderByStripeSession,
         getOrderByPaypalOrderId, getOrderByStripePaymentIntent, setStripeSession,
         setStripePaymentIntent, setPaypalOrderId, markPaidStripe, markPaidPaypal,
         setPaypalCustomerFromPayer, setStripeCustomerFromChargeDetails,
         updatePendingOrderCustomer, toPublicOrder }      from './_lib/order.js';
import { createCheckoutSession, createPaymentIntent,
         retrievePaymentIntent, verifyStripeWebhook }    from './_lib/stripe.js';
import { getAccessToken, createPaypalOrder,
         capturePaypalOrder, getPaypalOrder,
         verifyPaypalWebhookSignature }                  from './_lib/paypal.js';
import { sendConfirmationOnce,
         sendInternalOrderNotificationOnce,
         sendConsultationRequest,
         sendRestockNotifications }                      from './_lib/email.js';
import { isBlockedEmailDomain }                         from './_lib/email-domains.js';
import { createRestockRequest, pendingCountsBySku, listPendingForSku,
         findRestockByToken, cancelRestockByToken, checkRestockIpRateLimit,
         restockIpHash, RESTOCK_LOCALES }                from './_lib/restock.js';
import { restockCancelPage }                             from './_lib/restock-email-templates.js';
import { resolveAdminAuth, listOrders, getOrderDetail,
         markBankTransferPaid, archiveOrder,
         unarchiveOrder, deleteOrder }                   from './_lib/admin.js';
import { resolveAndValidateItems, itemsRequireShipping,
         getCatalogEntry }                               from './_lib/catalog.js';
import { assertCartStock, deductStockForPaidOrder, getStockQty,
         listAdminStock, setStockQty, isPhysicalSku }    from './_lib/stock.js';
import { safeParseJSON }                                 from './_lib/utils.js';
import { checkCheckoutEmailRateLimit,
         checkExpressCheckoutIpRateLimit,
         checkStripeExpressIpRateLimit }                 from './_lib/checkout-rate-limit.js';
import { upsertCartSession, markCartCheckoutStarted,
         checkCartSyncRateLimit, listCarts, getCartStats,
         normalizeHoursIdle, maybeRunCartRetention, deleteCart } from './_lib/cart.js';
import { getAnalyticsSummary, recordEvent, TRACKABLE_EVENTS } from './_lib/analytics.js';

/* ─── CORS ──────────────────────────────────────────────────────────────────── */

const ALLOWED_ORIGINS = [
    'https://eurolicenze.com',
    'https://www.eurolicenze.com',
    'http://localhost:8788',
    'http://127.0.0.1:8788',
];
const ALLOWED_LOCALES = new Set(['it', 'en', 'fr', 'de', 'es', 'pt', 'nl']);
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

function rateLimitResponse(result, request, env) {
    const status = result.status || 429;
    return new Response(
        JSON.stringify({
            error: result.message,
            code: result.code || 'CHECKOUT_RATE_LIMITED',
        }),
        {
            status,
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-store',
                'Retry-After': String(result.retryAfter || 60),
                ...corsHeaders(request, env || {}),
            },
        }
    );
}

/**
 * Rate limit email solo per nuovi checkout. Riuso stessa idempotency_key = ok.
 * @returns {Promise<Response|null>}
 */
async function gateNewCheckoutAttempt(env, request, params) {
    const existing = await env.DB
        .prepare('SELECT id FROM orders WHERE idempotency_key = ?')
        .bind(params.idempotencyKey)
        .first();
    if (existing?.id) return null;
    const limited = await checkCheckoutEmailRateLimit(env, params.customerEmail);
    if (limited) return rateLimitResponse(limited, request, env);
    return null;
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
            return await handleAdminRoute(path, request, env, context);
        }

        // ── Routes pubbliche ─────────────────────────────────────────────────────
        if (path === '/api/stripe-config' && request.method === 'GET') {
            return handleStripeConfig(request, env);
        }
        if (path === '/api/stripe-create-session' && request.method === 'POST') {
            return await handleStripeCreateSession(request, env);
        }
        if (path === '/api/create-payment-intent' && request.method === 'POST') {
            return await handleCreatePaymentIntent(request, env);
        }
        if (path === '/api/stripe-return' && request.method === 'GET') {
            return await handleStripeReturn(request, env);
        }
        if (path === '/api/stripe-intent-return' && request.method === 'GET') {
            return await handleStripeIntentReturn(request, env);
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
        if (path === '/api/paypal-express-create-order' && request.method === 'POST') {
            return await handlePaypalExpressCreateOrder(request, env);
        }
        if (path === '/api/webhooks/paypal' && request.method === 'POST') {
            return await handlePaypalWebhook(request, env);
        }
        if (path === '/api/track' && request.method === 'POST') {
            return await handleTrack(request, env);
        }
        if (path === '/api/bank-transfer-order' && request.method === 'POST') {
            return await handleBankTransferOrder(request, env);
        }
        if (path === '/api/order-status' && request.method === 'GET') {
            return await handleOrderStatus(request, env);
        }
        if (path === '/api/stock' && request.method === 'GET') {
            return await handlePublicStock(request, env);
        }
        if (path === '/api/paypal-config' && request.method === 'GET') {
            return handlePaypalConfig(request, env);
        }
        if (path === '/api/consultation-request' && request.method === 'POST') {
            return await handleConsultationRequest(request, env);
        }
        if (path === '/api/restock-request' && request.method === 'POST') {
            return await handleRestockRequest(request, env);
        }
        if (path === '/api/restock-cancel' && (request.method === 'GET' || request.method === 'POST')) {
            return await handleRestockCancel(request, env);
        }
        if (path === '/api/cart/sync' && request.method === 'POST') {
            return await handleCartSync(request, env, context);
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

function adminDeleteCartsEnabled(env) {
    return String(env.ADMIN_ALLOW_DELETE_CARTS || '') === '1';
}

function normalizeAdminNotes(v) {
    const notes = cleanString(v, 1000);
    return notes || null;
}

function validateEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(v || ''));
}

const CONSULTATION_TOPICS = new Set([
    'licences',
    'workstations',
    'microsoft-365',
    'server-database',
    'other',
]);

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

function cleanLine(v, maxLen = 120) {
    return cleanString(v, maxLen).replace(/[\r\n\t]+/g, ' ').replace(/\s{2,}/g, ' ');
}

function consultationFromBody(body) {
    const locale = cleanLine(body?.locale || 'it', 2).toLowerCase();
    if (!ALLOWED_LOCALES.has(locale)) {
        throw Object.assign(new Error('Lingua non valida'), { status: 400 });
    }

    const firstName = cleanLine(body?.firstName, 80);
    const lastName = cleanLine(body?.lastName, 80);
    const company = cleanLine(body?.company, 160);
    const email = cleanLine(body?.email, 254).toLowerCase();
    const topic = cleanLine(body?.topic, 32).toLowerCase();
    const message = cleanString(body?.message, 4000).replace(/\0/g, '');
    const website = cleanLine(body?.website, 200);
    const sourcePathRaw = cleanLine(body?.sourcePath, 240);
    const sourcePath = sourcePathRaw.startsWith(`/${locale}/`) ? sourcePathRaw : `/${locale}/`;

    if (website) return { honeypot: true };
    if (!firstName || !lastName) {
        throw Object.assign(new Error('Nome e cognome sono obbligatori'), { status: 400 });
    }
    if (!validateEmail(email)) {
        throw Object.assign(new Error('Email non valida'), { status: 400 });
    }
    if (!CONSULTATION_TOPICS.has(topic)) {
        throw Object.assign(new Error('Tipo di richiesta non valido'), { status: 400 });
    }
    if (message.length < 20) {
        throw Object.assign(new Error('Il messaggio deve contenere almeno 20 caratteri'), { status: 400 });
    }
    if (body?.privacy !== true) {
        throw Object.assign(new Error('Consenso privacy obbligatorio'), { status: 400 });
    }

    let seats = null;
    if (body?.seats !== '' && body?.seats !== null && body?.seats !== undefined) {
        seats = Number(body.seats);
        if (!Number.isInteger(seats) || seats < 1 || seats > 100000) {
            throw Object.assign(new Error('Numero di postazioni non valido'), { status: 400 });
        }
    }

    return {
        honeypot: false,
        lead: {
            id: crypto.randomUUID(),
            receivedAt: new Date().toISOString(),
            firstName,
            lastName,
            company,
            email,
            topic,
            seats,
            message,
            locale,
            supportLanguage: locale === 'it' ? 'it' : 'en',
            sourcePath,
        },
    };
}

function normalizeIdempotencyKey(v) {
    const key = cleanString(v, 96);
    if (!key) return crypto.randomUUID();
    if (!/^[A-Za-z0-9._:-]{8,96}$/.test(key)) {
        throw Object.assign(new Error('Idempotency key non valida'), { status: 400 });
    }
    return key;
}

function validateCustomer(rawCustomer, rawLang, env) {
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
    // Messaggio volutamente generico: dire "dominio bloccato" spiegherebbe a chi
    // sta testando carte come aggirare il filtro, e a un cliente vero in falso
    // positivo serve solo sapere che deve usare un altro indirizzo.
    if (isBlockedEmailDomain(customer.email, env)) {
        throw Object.assign(new Error('Indirizzo email non accettato: usane un altro'), { status: 400 });
    }
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
 * Valida l'indirizzo di spedizione (richiesto solo se il carrello contiene
 * almeno un articolo fisico: DVD/COA — vedi catalog.js `physical`).
 */
function validateShipping(raw) {
    const s = raw || {};
    const shipping = {
        addressLine1: cleanString(s.addressLine1, 160),
        city:         cleanString(s.city, 80),
        postalCode:   cleanString(s.postalCode, 20),
        province:     cleanString(s.province, 80),
        country:      cleanString(s.country, 80),
    };
    if (!shipping.addressLine1) throw Object.assign(new Error('Indirizzo di spedizione mancante'), { status: 400 });
    if (!shipping.city) throw Object.assign(new Error('Città di spedizione mancante'), { status: 400 });
    if (!shipping.postalCode) throw Object.assign(new Error('CAP di spedizione mancante'), { status: 400 });
    if (!shipping.country) throw Object.assign(new Error('Paese di spedizione mancante'), { status: 400 });
    return shipping;
}

/**
 * Costruisce i parametri ordine dal body JSON del checkout.
 */
function orderParamsFromBody(body, paymentMethod, env) {
    const { customer: c, lang } = validateCustomer(body.customer, body.lang, env);
    let items;
    try {
        items = resolveAndValidateItems(body.items);
    } catch (catalogErr) {
        throw Object.assign(new Error(catalogErr.message || 'Invalid catalog'), { status: 400 });
    }
    const requiresShipping = itemsRequireShipping(items);
    const shipping = requiresShipping ? validateShipping(body.shipping) : null;
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
        requiresShipping,
        shipping,
    };
}

/* ─── GET /api/paypal-config ────────────────────────────────────────────────── */
// Espone il Client ID PayPal (dato pubblico: finisce comunque nell'URL dell'SDK).
// Sandbox o live dipendono solo dalla config dell'ambiente: niente ID hardcodato
// nel frontend. Se non configurato il frontend disabilita PayPal con messaggio.

function handlePaypalConfig(request, env) {
    return json({ clientId: env.PAYPAL_CLIENT_ID || '' }, 200, request, env);
}

/* ─── POST /api/consultation-request ───────────────────────────────────────── */

async function handleConsultationRequest(request, env) {
    const invalidRequest = validateCheckoutRequest(request, env);
    if (invalidRequest) return invalidRequest;

    const rawBody = await request.text();
    if (new TextEncoder().encode(rawBody).byteLength > MAX_JSON_BODY_BYTES) {
        return err('Payload troppo grande', 413, request, env);
    }

    const body = safeParseJSON(rawBody, null);
    if (!body) return err('Invalid JSON', 400, request, env);

    let normalized;
    try {
        normalized = consultationFromBody(body);
    } catch (e) {
        if (e.status === 400) return err(e.message, 400, request, env);
        throw e;
    }

    // I bot che compilano il campo honeypot ricevono una risposta neutra senza
    // invio email. Turnstile e rate limiting restano obbligatori pre-deploy.
    if (normalized.honeypot) {
        return json({ ok: true }, 200, request, env);
    }

    const lead = normalized.lead;
    const reference = lead.id.slice(0, 8).toUpperCase();

    // Sviluppo locale: valida l'intero flusso frontend/API senza inviare email.
    if (String(env.CONSULTATION_DRY_RUN || '') === '1') {
        return json({ ok: true, dryRun: true, reference }, 200, request, env);
    }

    if (!env.RESEND_API_KEY) {
        console.error('[consultation] RESEND_API_KEY non configurato');
        return err('Servizio temporaneamente non disponibile', 503, request, env);
    }

    const result = await sendConsultationRequest(lead, env.RESEND_API_KEY);
    if (!result.sent) {
        console.error('[consultation] Invio interno fallito:', result.error || 'unknown');
        return err('Impossibile inviare la richiesta', 502, request, env);
    }

    return json({
        ok: true,
        dryRun: false,
        reference,
        confirmationSent: Boolean(result.confirmationSent),
    }, 200, request, env);
}

/* ─── POST /api/restock-request ─────────────────────────────────────────────── */

/**
 * Iscrizione all'avviso "torna disponibile" su uno SKU fisico esaurito.
 *
 * Non parte nessuna email qui: l'unica che il cliente ricevera' e' quella del
 * rifornimento, inviata quando l'Admin rialza la quantita' (vedi POST
 * /api/admin/stock). Questo endpoint scrive e basta.
 */
async function handleRestockRequest(request, env) {
    const invalidRequest = validateCheckoutRequest(request, env);
    if (invalidRequest) return invalidRequest;

    // Come per le consulenze: il Content-Length puo' mancare (transfer-encoding
    // chunked) o mentire, quindi la dimensione va ricontrollata sul letto.
    const rawBody = await request.text();
    if (new TextEncoder().encode(rawBody).byteLength > MAX_JSON_BODY_BYTES) {
        return err('Payload troppo grande', 413, request, env);
    }

    const body = safeParseJSON(rawBody, null);
    if (!body) return err('Invalid JSON', 400, request, env);

    // Honeypot: risposta identica a quella di successo, nessuna scrittura.
    if (cleanLine(body.website, 200)) return json({ ok: true }, 200, request, env);

    const sku = cleanString(body.sku, 64).trim();
    if (!isPhysicalSku(sku)) return err('Prodotto non valido', 400, request, env);

    const lang = cleanString(body.lang, 2).toLowerCase();
    if (!RESTOCK_LOCALES.has(lang)) return err('Lingua non valida', 400, request, env);

    const email = cleanString(body.email, 254).toLowerCase();
    if (!validateEmail(email)) return err('Email non valida', 400, request, env);
    if (isBlockedEmailDomain(email, env)) return err('Email non valida', 400, request, env);

    if (body.privacy !== true) return err('Consenso privacy obbligatorio', 400, request, env);

    const limited = await checkRestockIpRateLimit(env, request);
    if (limited) {
        return rateLimitResponse(
            { ...limited, message: 'Troppe richieste. Riprova più tardi.', code: 'RESTOCK_RATE_LIMITED' },
            request, env
        );
    }

    // Se nel frattempo il magazzino e' rientrato, l'iscrizione non ha piu' senso:
    // il client se ne accorge da qui e ricarica la scheda invece di lasciare il
    // cliente in attesa di un'email che non arrivera' mai.
    if (await getStockQty(env.DB, sku) > 0) {
        return json({ ok: false, reason: 'in_stock' }, 409, request, env);
    }

    const ipHash = await restockIpHash(env, request);
    const result = await createRestockRequest(env.DB, {
        sku,
        email,
        lang,
        pagePath: cleanLine(body.sourcePath, 240),
        ipHash,
    });

    if (!result.ok) {
        const status = result.reason === 'db_error' ? 503 : 400;
        return err('Impossibile registrare la richiesta', status, request, env);
    }

    // `duplicate` non esce dall'endpoint: dire a chi scrive se un indirizzo era
    // gia' iscritto lo trasformerebbe in un modo per sondare gli indirizzi altrui.
    return json({ ok: true }, 200, request, env);
}

/* ─── GET|POST /api/restock-cancel ──────────────────────────────────────────── */

/**
 * Annullamento dell'avviso dal link in fondo all'email.
 * GET mostra la conferma, POST cancella: un GET che cancellasse da solo
 * verrebbe innescato anche dai prefetch dei client di posta.
 */
async function handleRestockCancel(request, env) {
    const html = (body, status = 200) => new Response(body, {
        status,
        headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' },
    });

    const origin = env.SITE_ORIGIN || 'https://eurolicenze.com';
    const url = new URL(request.url);

    // La lingua della riga e' la fonte buona, ma se la riga non esiste piu'
    // resta solo quella del link: senza, chi si era iscritto da una PDP tedesca
    // leggerebbe in italiano che l'avviso non c'e' piu'.
    const hintedLang = cleanString(url.searchParams.get('lang'), 2).toLowerCase();
    const fallbackLang = RESTOCK_LOCALES.has(hintedLang) ? hintedLang : 'it';

    let token = '';
    if (request.method === 'POST') {
        const form = await request.formData().catch(() => null);
        token = cleanLine(form?.get('token'), 64);
    } else {
        token = cleanLine(url.searchParams.get('token'), 64);
    }

    const row = await findRestockByToken(env.DB, token);
    if (!row) {
        return html(
            restockCancelPage({ lang: fallbackLang, state: 'gone', siteOrigin: origin, token }),
            404
        );
    }

    const lang = RESTOCK_LOCALES.has(row.lang) ? row.lang : 'it';

    if (request.method === 'GET') {
        return html(restockCancelPage({ lang, state: 'confirm', siteOrigin: origin, token }));
    }

    await cancelRestockByToken(env.DB, token);
    return html(restockCancelPage({ lang, state: 'done', siteOrigin: origin, token }));
}

/* ─── POST /api/stripe-create-session ───────────────────────────────────────── */

async function orderParamsFromBodySafe(body, paymentMethod, request, env) {
    try {
        const params = orderParamsFromBody(body, paymentMethod, env);
        try {
            await assertCartStock(env.DB, params.lineItems);
        } catch (stockErr) {
            const status = stockErr.status || 409;
            return {
                error: err(stockErr.message || 'Stock insufficiente', status, request, env),
            };
        }
        return params;
    } catch (e) {
        if (e.status === 400) return { error: err(e.message, 400, request, env) };
        throw e;
    }
}

/**
 * Righe e importo da usare quando si riusa un ordine gia' presente in D1.
 *
 * Il PSP va sempre istruito con quanto e' SALVATO sull'ordine, mai con il
 * ricalcolo della richiesta corrente. Entro le 24 ore la cosa non si nota —
 * l'Idempotency-Key Stripe (= orderId) fa rigiocare la stessa sessione/PI — ma
 * quelle chiavi scadono: passato un giorno, la stessa idempotency_key produce un
 * PSP object NUOVO, calcolato sulle righe nuove, agganciato a una riga ordine che
 * contiene ancora le vecchie. Da li' in poi l'importo addebitato e le licenze
 * evase divergono.
 *
 * Prendere il dato salvato risolve anche il caso ostile: chi rigiocasse la stessa
 * chiave con un carrello piu' caro verrebbe comunque addebitato — e servito —
 * secondo l'ordine originale.
 *
 * @returns {{lineItems: object[], totalMinor: number, currency: string}}
 */
function reusedOrderAmounts(existingOrder, recomputed) {
    const lineItems  = safeParseJSON(existingOrder?.line_items, null);
    const totalMinor = Number(existingOrder?.total_minor);

    // Riga malformata o incompleta (SELECT senza le colonne): meglio il ricalcolo
    // che un importo nullo.
    if (!Array.isArray(lineItems) || !lineItems.length || !Number.isFinite(totalMinor)) {
        return recomputed;
    }

    if (totalMinor !== recomputed.totalMinor) {
        console.warn('[checkout] riuso ordine con totale diverso dal ricalcolo:', {
            orderId:  existingOrder.id,
            salvato:  totalMinor,
            corrente: recomputed.totalMinor,
        });
    }

    return {
        lineItems,
        totalMinor,
        currency: existingOrder.currency || recomputed.currency,
    };
}

/** Collega il cartId (se presente nel body) all'ordine appena creato. Non deve mai bloccare il checkout. */
async function linkCartCheckoutStarted(env, body, orderId) {
    const cartId = String(body?.cartId || '').trim();
    if (!CART_ID_RE.test(cartId)) return;
    try {
        await markCartCheckoutStarted(env.DB, cartId, orderId);
    } catch (e) {
        console.warn('[cart] markCartCheckoutStarted failed:', orderId, e?.message || e);
    }
}

async function deductStockForOrderRow(db, order) {
    if (!order?.id) return;
    const items = safeParseJSON(order.line_items, []);
    try {
        await deductStockForPaidOrder(db, order.id, items);
    } catch (e) {
        console.warn('[stock] deduct after paid failed:', order.id, e?.message || e);
    }
}

async function handlePublicStock(request, env) {
    const sku = new URL(request.url).searchParams.get('sku') || '';
    const key = String(sku).trim();
    if (!key || !isPhysicalSku(key)) {
        return json({ error: 'Not found' }, 404, request, env);
    }
    const qty = await getStockQty(env.DB, key);
    const res = json({ sku: key, qty, physical: true }, 200, request, env);
    const headers = new Headers(res.headers);
    headers.set('Cache-Control', 'public, max-age=30');
    return new Response(res.body, { status: 200, headers });
}

/* ─── POST /api/cart/sync ────────────────────────────────────────────────────── */
// Tracking carrelli (analytics fase 1). Endpoint pubblico, non autenticato:
// niente prezzo/nome/valuta dal client — le righe passano sempre dal catalogo
// server (resolveAndValidateItems), come per il checkout.

const CART_ID_RE      = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const CART_EMAIL_RE   = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const CART_MAX_ITEMS  = 50;

async function handleCartSync(request, env, context) {
    const invalidRequest = validateCheckoutRequest(request, env);
    if (invalidRequest) return invalidRequest;

    const limited = await checkCartSyncRateLimit(env, request);
    if (limited) {
        return rateLimitResponse(
            { ...limited, message: 'Too many requests', code: 'CART_SYNC_RATE_LIMITED' },
            request, env
        );
    }

    const body = await request.json().catch(() => null);
    if (!body) return err('Invalid JSON', 400, request, env);

    const cartId = String(body.cartId || '').trim();
    if (!CART_ID_RE.test(cartId)) return err('cartId non valido', 400, request, env);

    const rawItems = Array.isArray(body.items) ? body.items : [];
    if (rawItems.length > CART_MAX_ITEMS) return err('Troppi articoli', 400, request, env);

    let items;
    try {
        items = rawItems.length ? resolveAndValidateItems(rawItems) : [];
    } catch (catalogErr) {
        return err(catalogErr.message || 'Invalid catalog', 400, request, env);
    }

    let email = String(body.email || '').trim().toLowerCase();
    if (email && (email.length > 254 || !CART_EMAIL_RE.test(email))) {
        return err('Email non valida', 400, request, env);
    }
    // Il carrello non viene rifiutato, si scarta solo l'email: e' da questa
    // porta che sono entrati i carrelli di card testing, e tenerli fuori da
    // cart_sessions evita di sporcare i dati di recupero. Rifiutare l'intera
    // sync sarebbe sbagliato: qui l'email e' facoltativa e il blocco vero sta
    // sulla creazione dell'ordine, dove costa qualcosa all'attaccante.
    if (email && isBlockedEmailDomain(email, env)) email = null;
    if (!email) email = null;

    const rawLocale = String(body.locale || 'it').toLowerCase();
    const locale = ALLOWED_LOCALES.has(rawLocale) ? rawLocale : 'it';
    const country = request.cf?.country || null;

    await upsertCartSession(env.DB, {
        id:          cartId,
        email,
        locale,
        country,
        lineItems:   items,
        totalMinor:  totalMinorFromItems(items),
        currency:    items[0]?.currency || 'EUR',
    });

    // Pulizia dei carrelli scaduti: dopo la risposta, al piu' una volta all'ora
    // e con gate a inizio ora, per non aggiungere una scrittura D1 a ogni sync.
    maybeRunCartRetention(context, { cheapGate: true });

    return json({ ok: true }, 200, request, env);
}

async function handleStripeCreateSession(request, env) {
    const invalidRequest = validateCheckoutRequest(request, env);
    if (invalidRequest) return invalidRequest;

    const body = await request.json().catch(() => null);
    if (!body) return err('Invalid JSON', 400, request, env);

    const paramsOrErr = await orderParamsFromBodySafe(body, 'stripe', request, env);
    if (paramsOrErr.error) return paramsOrErr.error;
    const params = paramsOrErr;

    const rateGate = await gateNewCheckoutAttempt(env, request, params);
    if (rateGate) return rateGate;

    // Crea ordine in D1
    let orderId;
    let amounts = {
        lineItems:  params.lineItems,
        totalMinor: params.totalMinor,
        currency:   params.currency,
    };
    try {
        orderId = await createOrder(env.DB, params);
    } catch (dbErr) {
        // UNIQUE constraint: idempotency_key già presente → riusa l'ordine esistente.
        // Si prosegue comunque con createCheckoutSession: l'Idempotency-Key Stripe
        // (= orderId) fa restituire la stessa sessione, quindi il client riceve
        // sempre una url valida anche su retry.
        if (String(dbErr).includes('UNIQUE')) {
            const existing = await env.DB
                .prepare('SELECT id, status, line_items, total_minor, currency FROM orders WHERE idempotency_key = ?')
                .bind(params.idempotencyKey).first();
            if (!existing?.id) throw dbErr;
            if (existing.status === 'paid') {
                return err('Ordine già pagato', 409, request, env);
            }
            orderId = existing.id;
            // Stessa email e stesso carrello = stessa chiave: se l'utente torna
            // indietro e cambia i dati (tipicamente Privato → Azienda), senza
            // questo riallineamento P.IVA e SDI non arriverebbero mai in D1.
            await updatePendingOrderCustomer(env.DB, orderId, params);
            amounts = reusedOrderAmounts(existing, amounts);
        } else {
            throw dbErr;
        }
    }
    await linkCartCheckoutStarted(env, body, orderId);

    const origin     = env.SITE_ORIGIN || 'https://eurolicenze.com';
    const lang       = params.locale || 'it';
    const successUrl = `${origin}/api/stripe-return?sid={CHECKOUT_SESSION_ID}&lang=${lang}`;
    const cancelUrl  = `${origin}/${lang}/checkout?cancelled=1`;

    // Crea Stripe Checkout Session
    const session = await createCheckoutSession(env.STRIPE_SECRET_KEY, {
        orderId,
        customerEmail: params.customerEmail,
        lineItems:     amounts.lineItems,
        locale:        lang,
        successUrl,
        cancelUrl,
    });

    // Salva stripe_session_id sull'ordine
    await setStripeSession(env.DB, orderId, session.id);

    return json({ url: session.url, orderId }, 200, request, env);
}

/* ─── GET /api/stripe-config ────────────────────────────────────────────────── */
// Espone la publishable key Stripe (dato pubblico: finisce comunque nel client).
// Se non configurata il frontend nasconde Express Checkout + Payment Element e
// tiene solo PayPal / Bonifico.

function handleStripeConfig(request, env) {
    return json({ publishableKey: env.STRIPE_PUBLISHABLE_KEY || '' }, 200, request, env);
}

/* ─── POST /api/create-payment-intent ──────────────────────────────────────── */
// Flusso on-page (Express Checkout Element + Payment Element). L'importo è sempre
// ricalcolato server-side dal catalogo. Due modalità:
//   mode:'manual'  → il form anagrafico è compilato e validato (anche B2B)
//   mode:'express' → wallet 1-click, cliente placeholder valorizzato dal webhook

async function handleCreatePaymentIntent(request, env) {
    const invalidRequest = validateCheckoutRequest(request, env);
    if (invalidRequest) return invalidRequest;

    if (!env.STRIPE_SECRET_KEY) {
        return err('Pagamento con carta non disponibile', 503, request, env);
    }

    const body = await request.json().catch(() => null);
    if (!body) return err('Invalid JSON', 400, request, env);

    const mode = body.mode === 'express' ? 'express' : 'manual';

    let orderId, amountMinor, currency, locale, receiptEmail;

    if (mode === 'manual') {
        const paramsOrErr = await orderParamsFromBodySafe(body, 'stripe', request, env);
        if (paramsOrErr.error) return paramsOrErr.error;
        const params = paramsOrErr;

        const rateGate = await gateNewCheckoutAttempt(env, request, params);
        if (rateGate) return rateGate;

        let amounts = {
            lineItems:  params.lineItems,
            totalMinor: params.totalMinor,
            currency:   params.currency,
        };

        try {
            orderId = await createOrder(env.DB, params);
        } catch (dbErr) {
            if (String(dbErr).includes('UNIQUE')) {
                const existing = await env.DB
                    .prepare('SELECT id, status, line_items, total_minor, currency FROM orders WHERE idempotency_key = ?')
                    .bind(params.idempotencyKey).first();
                if (!existing?.id) throw dbErr;
                if (existing.status === 'paid') return err('Ordine già pagato', 409, request, env);
                orderId = existing.id;

                // Il Payment Element viene rimontato ogni volta che cambiano i dati
                // cliente, ma l'idempotency key dipende solo da email e carrello:
                // correggere il cognome, o passare a "Azienda" tenendo la stessa
                // email, ricade sulla stessa chiave. Senza questo riallineamento i
                // dati nuovi (P.IVA, SDI, ragione sociale) andrebbero persi e
                // l'ordine resterebbe registrato come privato.
                await updatePendingOrderCustomer(env.DB, orderId, params);
                amounts = reusedOrderAmounts(existing, amounts);
            } else {
                throw dbErr;
            }
        }

        amountMinor  = amounts.totalMinor;
        currency     = amounts.currency;
        locale       = params.locale || 'it';
        receiptEmail = params.customerEmail;
    } else {
        // Kill switch: permette di spegnere il solo wallet 1-click da Cloudflare
        // senza un nuovo deploy, lasciando in piedi carta manuale/PayPal/bonifico.
        if (String(env.STRIPE_EXPRESS_ENABLED ?? '1') !== '1') {
            return err('Express Checkout non disponibile', 503, request, env);
        }

        let items;
        try {
            items = resolveAndValidateItems(body.items);
        } catch (catalogErr) {
            return err(catalogErr.message || 'Invalid catalog', 400, request, env);
        }
        if (itemsRequireShipping(items)) {
            return err('Express Checkout non disponibile per articoli con spedizione fisica', 400, request, env);
        }

        // L'email del wallet e' obbligatoria (ExpressCheckoutElement e' montato con
        // emailRequired: true). Due motivi, entrambi vincolanti:
        //  1) la licenza viene emessa a mano dopo i controlli antifrode: un ordine
        //     pagato senza destinatario non e' evadibile e il cliente non e'
        //     contattabile (Apple/Google Pay non comunicano l'email a Stripe se
        //     l'Element non la richiede, quindi non c'e' nemmeno un fallback);
        //  2) senza email questo path resterebbe fuori dal freno primario per
        //     email — che e' fail-closed — lasciando solo un limite per IP
        //     (ADR-001 §3.2 T7: "pochi tentativi da molti IP").
        const walletEmail = cleanString(body.walletEmail, 254).toLowerCase();
        if (!validateEmail(walletEmail)) {
            return err('Email del wallet mancante o non valida', 400, request, env);
        }
        const walletName = cleanLine(body.walletName, 160);

        try {
            await assertCartStock(env.DB, items);
        } catch (stockErr) {
            return err(stockErr.message || 'Stock insufficiente', stockErr.status || 409, request, env);
        }

        const rawLang = String(body.lang || 'it').toLowerCase();
        locale = ALLOWED_LOCALES.has(rawLang) ? rawLang : 'it';
        const idempotencyKey = normalizeIdempotencyKey(body.idempotencyKey);

        const existing = await env.DB
            .prepare('SELECT id, status, line_items, total_minor, currency FROM orders WHERE idempotency_key = ?')
            .bind(idempotencyKey).first();
        if (existing?.status === 'paid') return err('Ordine già pagato', 409, request, env);
        if (!existing?.id) {
            // Stesso ordine dei controlli del path manuale: prima l'email
            // (primario, fail-closed), poi l'IP (secondario).
            const emailGate = await checkCheckoutEmailRateLimit(env, walletEmail);
            if (emailGate) return rateLimitResponse(emailGate, request, env);
            const ipGate = await checkStripeExpressIpRateLimit(env, request);
            if (ipGate) return rateLimitResponse(ipGate, request, env);
        }

        const nameParts = walletName.split(/\s+/).filter(Boolean);
        const walletFirstName = nameParts.shift() || '';
        const walletLastName  = nameParts.join(' ');

        // Riga ordine riusata, se c'e': l'importo del PaymentIntent va preso da li'.
        let reused = existing?.id ? existing : null;

        try {
            orderId = existing?.id || await createOrder(env.DB, {
                idempotencyKey,
                customerEmail:     walletEmail,
                customerFirstName: walletFirstName,
                customerLastName:  walletLastName,
                customerCompany:   null,
                customerType:      'private',
                customerPhone:     null,
                customerPiva:      null,
                customerSdi:       null,
                customerPec:       null,
                locale,
                lineItems:         items,
                totalMinor:        totalMinorFromItems(items),
                currency:          items[0].currency,
                paymentMethod:     'stripe',
                requiresShipping:  false,
                shipping:          null,
            });
        } catch (dbErr) {
            if (String(dbErr).includes('UNIQUE')) {
                const row = await env.DB
                    .prepare('SELECT id, line_items, total_minor, currency FROM orders WHERE idempotency_key = ?')
                    .bind(idempotencyKey).first();
                orderId = row?.id;
                if (!orderId) throw dbErr;
                reused = row;
            } else {
                throw dbErr;
            }
        }

        const amounts = reused
            ? reusedOrderAmounts(reused, {
                lineItems:  items,
                totalMinor: totalMinorFromItems(items),
                currency:   items[0].currency,
            })
            : { totalMinor: totalMinorFromItems(items), currency: items[0].currency };

        amountMinor  = amounts.totalMinor;
        currency     = amounts.currency;
        // Passato a Stripe: e' anche un segnale in piu' per Radar, che su un
        // PaymentIntent senza email/nome ha molti meno appigli che su una
        // Checkout Session (dove customer_email era sempre valorizzata).
        receiptEmail = walletEmail;
    }

    await linkCartCheckoutStarted(env, body, orderId);

    // Express: Apple/Google Pay viaggiano come `card`, Link e Amazon Pay sono
    // tipi a se' e senza di loro il wallet fallirebbe in conferma.
    // Manuale: solo `card`. Cosi' il Payment Element mostra i campi carta e
    // basta — niente riga di tab, niente tendina — e la sezione dice davvero
    // quello che l'etichetta promette ("Carta di credito o debito").
    // Express: Apple/Google Pay viaggiano come `card`, Link e Amazon Pay sono
    // tipi a se'. Manuale: il metodo lo sceglie il radio del checkout, e il
    // PaymentIntent nasce con quel solo tipo — cosi' il Payment Element rende
    // una interfaccia sola, senza riga di tab ne' tendina di overflow.
    // Allowlist chiusa: il tipo arriva dal client e non va passato a Stripe
    // cosi' com'e'. SEPA e Klarna sono a notifica differita e la loro riga nel
    // checkout lo dichiara ("la licenza parte alla conferma").
    const MANUAL_METHODS = new Set(['card', 'sepa_debit', 'klarna']);
    const chiesto = String(body.method || 'card');
    const methods = mode === 'express'
        ? ['card', 'link', 'amazon_pay', 'paypal']
        : [MANUAL_METHODS.has(chiesto) ? chiesto : 'card'];

    const pi = await createPaymentIntent(env.STRIPE_SECRET_KEY, {
        orderId,
        amountMinor,
        currency,
        receiptEmail,
        locale,
        methods,
    });
    await setStripePaymentIntent(env.DB, orderId, pi.id);

    if (mode === 'express') {
        await recordEvent(env, request, { eventName: 'stripe_express_click', orderId });
    }

    return json({ clientSecret: pi.client_secret, orderId }, 200, request, env);
}

/* ─── GET /api/stripe-return ────────────────────────────────────────────────── */
// Stripe redirige qui dopo pagamento con {CHECKOUT_SESSION_ID}
// Il Worker verifica, genera token, redirige alla thank-you page.

async function handleStripeReturn(request, env) {
    const url  = new URL(request.url);
    const sid  = url.searchParams.get('sid');
    const rawLang = (url.searchParams.get('lang') || 'it').toLowerCase();
    const lang = ALLOWED_LOCALES.has(rawLang) ? rawLang : 'it';

    const origin = env.SITE_ORIGIN || 'https://eurolicenze.com';

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

/* ─── GET /api/stripe-intent-return ─────────────────────────────────────────── */
// Ritorno del flusso on-page (Payment Element / Express Checkout Element).
// Usato sia come `return_url` nei casi 3DS con redirect (Stripe aggiunge
// ?payment_intent=…), sia chiamato da checkout.js dopo un confirmPayment
// risolto senza redirect. Il webhook resta la fonte di verità per l'evasione.

// Stati in cui il cliente ha fatto la sua parte e il denaro è impegnato: va
// portato alla thank-you page, non rimandato al form.
//   succeeded        → incassato
//   processing       → metodi a notifica differita (SEPA, Bancontact, Klarna e
//                      carte che settlano in modo asincrono). Con
//                      automatic_payment_methods questi stati sono all'ordine
//                      del giorno; rimbalzarli indietro significa mostrare un
//                      errore a chi ha appena pagato, e invitarlo a ripagare.
//   requires_capture → cattura manuale, oggi non usata: incluso perché anche lì
//                      i fondi sono autorizzati.
// Restano esclusi requires_payment_method / requires_action / canceled, dove
// l'utente deve davvero rifare qualcosa.
const SETTLED_PI_STATUSES = new Set(['succeeded', 'processing', 'requires_capture']);

async function handleStripeIntentReturn(request, env) {
    const url     = new URL(request.url);
    const piId    = url.searchParams.get('payment_intent');
    const rawLang = (url.searchParams.get('lang') || 'it').toLowerCase();
    const lang    = ALLOWED_LOCALES.has(rawLang) ? rawLang : 'it';
    const origin  = env.SITE_ORIGIN || 'https://eurolicenze.com';

    if (!piId) {
        return Response.redirect(`${origin}/${lang}/checkout?error=missing_pi`, 302);
    }

    let pi;
    try {
        pi = await retrievePaymentIntent(env.STRIPE_SECRET_KEY, piId);
    } catch (e) {
        console.error('[stripe-intent-return] retrieve fallito:', e.message);
        return Response.redirect(`${origin}/${lang}/checkout?error=pi_lookup`, 302);
    }

    if (!SETTLED_PI_STATUSES.has(pi.status)) {
        return Response.redirect(`${origin}/${lang}/checkout?error=payment_${pi.status || 'incomplete'}`, 302);
    }

    const order = await getOrderByStripePaymentIntent(env.DB, pi.id);
    if (!order) {
        return Response.redirect(`${origin}/${lang}/checkout?error=order_not_found`, 302);
    }

    const token = await generateToken(env.TOKEN_SECRET, order.id);
    const dest  = `${origin}/${lang}/checkout-success?oid=${token.oid}&exp=${token.exp}&t=${encodeURIComponent(token.t)}`;
    return Response.redirect(dest, 302);
}

/* ─── POST /api/webhooks/stripe ─────────────────────────────────────────────── */

// Evasione ordine Stripe: mark-paid + deduct stock + email conferma/interna.
// Idempotente (dedup via stock_deductions e *_sent_at). Condivisa dai rami
// checkout.session.completed e payment_intent.succeeded del webhook.
async function fulfilPaidStripeOrder(env, order, eventSrc) {
    const wasUnpaid = order.status !== 'paid';
    const updatedOrder = await getOrderById(env.DB, order.id);
    await deductStockForOrderRow(env.DB, updatedOrder || order);
    if (wasUnpaid) {
        await sendConfirmationOnce(
            env.DB, updatedOrder,
            env.RESEND_API_KEY, env.TRUSTPILOT_BCC || '',
            eventSrc, env.GUIDES
        );
        await sendInternalOrderNotificationOnce(
            env.DB, updatedOrder, env.RESEND_API_KEY, eventSrc
        );
    }
}

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

    // Checkout ospitato (redirect legacy)
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
        }
        await fulfilPaidStripeOrder(env, order, 'webhook_stripe');
    }

    // Flusso on-page (Payment Element / Express Checkout Element)
    if (event.type === 'payment_intent.succeeded') {
        const pi = event.data?.object;
        const piId = pi?.id;

        const order = await getOrderByStripePaymentIntent(env.DB, piId);
        if (!order) {
            console.warn('[webhook/stripe] Ordine non trovato per payment_intent:', piId);
            return new Response('OK', { status: 200 }); // Ack comunque a Stripe
        }

        // Rete di sicurezza: dal passaggio all'Express Element con emailRequired
        // l'ordine nasce gia' con l'email del wallet, quindi qui non dovrebbe mai
        // entrare. Resta per gli ordini creati prima di quel cambio.
        // NB: i payload dei webhook non sono mai espansi — `pi.latest_charge` e'
        // una stringa e `pi.charges` non esiste piu' dalla API 2022-11-15 — quindi
        // i billing_details vanno letti con una GET esplicita, non dall'evento.
        if (!order.customer_email) {
            try {
                const full   = await retrievePaymentIntent(env.STRIPE_SECRET_KEY, piId);
                const charge = full?.latest_charge;
                const bd     = (charge && typeof charge === 'object') ? (charge.billing_details || {}) : {};
                const email  = full?.receipt_email || bd.email || '';
                if (email) {
                    await setStripeCustomerFromChargeDetails(env.DB, order.id, { email, name: bd.name });
                } else {
                    console.error('[webhook/stripe] Ordine pagato senza email cliente:', order.id);
                }
            } catch (e) {
                console.error('[webhook/stripe] Recupero billing_details fallito:', order.id, e?.message || e);
            }
        }

        if (order.status !== 'paid') {
            await markPaidStripe(env.DB, order.id, { stripePaymentIntent: piId });
        }
        await fulfilPaidStripeOrder(env, order, 'webhook_stripe_pi');

        if (order.status !== 'paid') {
            await recordEvent(env, request, { eventName: 'purchase', orderId: order.id });
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

    const paramsOrErr = await orderParamsFromBodySafe(body, 'paypal', request, env);
    if (paramsOrErr.error) return paramsOrErr.error;
    const params = paramsOrErr;

    const rateGate = await gateNewCheckoutAttempt(env, request, params);
    if (rateGate) return rateGate;

    // Crea ordine in D1
    let orderId;
    let amounts = {
        lineItems:  params.lineItems,
        totalMinor: params.totalMinor,
        currency:   params.currency,
    };
    try {
        orderId = await createOrder(env.DB, params);
    } catch (dbErr) {
        if (String(dbErr).includes('UNIQUE')) {
            const existing = await env.DB
                .prepare('SELECT id, line_items, total_minor, currency FROM orders WHERE idempotency_key = ?')
                .bind(params.idempotencyKey).first();
            orderId = existing?.id;
            if (!orderId) throw dbErr;
            // Vedi handleCreatePaymentIntent: la chiave non copre i dati fiscali,
            // quindi il riuso deve riallinearli o vanno persi.
            await updatePendingOrderCustomer(env.DB, orderId, params);
            amounts = reusedOrderAmounts(existing, amounts);
        } else {
            throw dbErr;
        }
    }
    await linkCartCheckoutStarted(env, body, orderId);

    // Crea ordine su PayPal
    const accessToken = await getAccessToken(
        env.PAYPAL_BASE_URL, env.PAYPAL_CLIENT_ID, env.PAYPAL_CLIENT_SECRET
    );

    const totalStr     = (amounts.totalMinor / 100).toFixed(2);
    const paypalOrderId = await createPaypalOrder(env.PAYPAL_BASE_URL, accessToken, {
        orderId,
        totalMinorStr: totalStr,
        currency:      amounts.currency,
        lineItems:     amounts.lineItems,
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
    const { captureId, status, amountValue, currencyCode, payer } = await capturePaypalOrder(
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

    // Express checkout: nessun form nostro è mai stato compilato, il cliente
    // è ancora il placeholder ('') creato da handlePaypalExpressCreateOrder.
    // L'unica fonte per nome/email è il payer restituito da PayPal qui.
    if (!order.customer_email && payer?.email) {
        await setPaypalCustomerFromPayer(env.DB, order.id, payer);
    }

    // Aggiorna ordine D1
    await markPaidPaypal(env.DB, order.id, { paypalOrderId, paypalCaptureId: captureId });

    // Invia email
    const updatedOrder = await getOrderById(env.DB, order.id);
    await deductStockForOrderRow(env.DB, updatedOrder || order);
    await sendConfirmationOnce(
        env.DB, updatedOrder,
        env.RESEND_API_KEY, env.TRUSTPILOT_BCC || '',
        'worker_capture', env.GUIDES
    );
    await sendInternalOrderNotificationOnce(
        env.DB, updatedOrder,
        env.RESEND_API_KEY,
        'worker_capture'
    );
    await recordEvent(env, request, { eventName: 'purchase', orderId: order.id });

    // Genera token thank-you
    const token = await generateToken(env.TOKEN_SECRET, order.id);

    return json({ oid: token.oid, exp: token.exp, t: token.t }, 200, request, env);
}

/* ─── POST /api/paypal-express-create-order ─────────────────────────────────── */
// Bottone Express sulla PDP: crea l'ordine con cliente placeholder (nessun
// form compilato) e l'ordine PayPal in un colpo solo. Il capture riusa
// /api/paypal-capture-order sopra, che valorizza il cliente dal payer.

async function handlePaypalExpressCreateOrder(request, env) {
    const invalidRequest = validateCheckoutRequest(request, env);
    if (invalidRequest) return invalidRequest;

    const body = await request.json().catch(() => null);
    if (!body) return err('Invalid JSON', 400, request, env);

    let items;
    try {
        items = resolveAndValidateItems(body.items);
    } catch (catalogErr) {
        return err(catalogErr.message || 'Invalid catalog', 400, request, env);
    }
    if (itemsRequireShipping(items)) {
        return err('PayPal Express non disponibile per articoli con spedizione fisica', 400, request, env);
    }

    const rawLang = String(body.lang || 'it').toLowerCase();
    const lang = ALLOWED_LOCALES.has(rawLang) ? rawLang : 'it';
    const idempotencyKey = normalizeIdempotencyKey(body.idempotencyKey);

    // Riuso ordine esistente su retry della stessa idempotency_key, altrimenti
    // limite per IP: niente email disponibile a questo punto del flusso.
    const existing = await env.DB
        .prepare('SELECT id, line_items, total_minor, currency FROM orders WHERE idempotency_key = ?')
        .bind(idempotencyKey).first();
    if (!existing?.id) {
        const rateGate = await checkExpressCheckoutIpRateLimit(env, request);
        if (rateGate) return rateLimitResponse(rateGate, request, env);
    }

    let orderId;
    let reused = existing?.id ? existing : null;
    try {
        orderId = await createOrder(env.DB, {
            idempotencyKey,
            customerEmail:     '',
            customerFirstName: '',
            customerLastName:  '',
            customerCompany:   null,
            customerType:      'private',
            customerPhone:     null,
            customerPiva:      null,
            customerSdi:       null,
            customerPec:       null,
            locale:            lang,
            lineItems:         items,
            totalMinor:        totalMinorFromItems(items),
            currency:          items[0].currency,
            paymentMethod:     'paypal',
            requiresShipping:  false,
            shipping:          null,
        });
    } catch (dbErr) {
        if (String(dbErr).includes('UNIQUE')) {
            const row = await env.DB
                .prepare('SELECT id, line_items, total_minor, currency FROM orders WHERE idempotency_key = ?')
                .bind(idempotencyKey).first();
            orderId = row?.id;
            if (!orderId) throw dbErr;
            reused = row;
        } else {
            throw dbErr;
        }
    }
    await linkCartCheckoutStarted(env, body, orderId);

    const accessToken = await getAccessToken(
        env.PAYPAL_BASE_URL, env.PAYPAL_CLIENT_ID, env.PAYPAL_CLIENT_SECRET
    );

    const recomputed = {
        lineItems:  items,
        totalMinor: totalMinorFromItems(items),
        currency:   items[0].currency,
    };
    const amounts = reused ? reusedOrderAmounts(reused, recomputed) : recomputed;

    const totalStr = (amounts.totalMinor / 100).toFixed(2);
    const paypalOrderId = await createPaypalOrder(env.PAYPAL_BASE_URL, accessToken, {
        orderId,
        totalMinorStr: totalStr,
        currency:      amounts.currency,
        lineItems:     amounts.lineItems,
    });

    await setPaypalOrderId(env.DB, orderId, paypalOrderId);
    await recordEvent(env, request, {
        eventName: 'paypal_express_click',
        orderId,
        sku: items[0]?.sku,
    });

    return json({ orderID: paypalOrderId, amlOrderId: orderId }, 200, request, env);
}

/* ─── POST /api/webhooks/paypal ─────────────────────────────────────────────── */
// Rete di sicurezza per il capture client-side (sia checkout tradizionale sia
// Express): se il redirect dopo l'approvazione fallisce, il webhook riconcilia
// comunque l'ordine. Idempotente sullo stesso pattern del webhook Stripe.

async function handlePaypalWebhook(request, env) {
    const rawBody = await request.text();

    const headers = {};
    for (const [k, v] of request.headers.entries()) headers[k.toLowerCase()] = v;

    let accessToken;
    try {
        accessToken = await getAccessToken(
            env.PAYPAL_BASE_URL, env.PAYPAL_CLIENT_ID, env.PAYPAL_CLIENT_SECRET
        );
    } catch (e) {
        console.error('[webhook/paypal] Impossibile ottenere access token:', e?.message || e);
        return new Response('Service unavailable', { status: 503 });
    }

    let verified = false;
    try {
        verified = await verifyPaypalWebhookSignature(
            env.PAYPAL_BASE_URL, accessToken, headers, env.PAYPAL_WEBHOOK_ID, rawBody
        );
    } catch (e) {
        console.error('[webhook/paypal] Verifica firma fallita:', e?.message || e);
    }
    if (!verified) {
        console.error('[webhook/paypal] Firma non valida o webhook non configurato');
        return new Response('Unauthorized', { status: 401 });
    }

    const event = safeParseJSON(rawBody, null);
    if (!event) return new Response('Invalid JSON', { status: 400 });

    if (event.event_type === 'PAYMENT.CAPTURE.COMPLETED') {
        const resource = event.resource || {};
        const paypalOrderId = resource?.supplementary_data?.related_ids?.order_id;
        if (!paypalOrderId) {
            console.warn('[webhook/paypal] Nessun order_id nella risorsa capture');
            return new Response('OK', { status: 200 });
        }

        const order = await getOrderByPaypalOrderId(env.DB, paypalOrderId);
        if (!order) {
            console.warn('[webhook/paypal] Ordine non trovato per PayPal order:', paypalOrderId);
            return new Response('OK', { status: 200 }); // Ack comunque a PayPal
        }

        if (order.status !== 'paid') {
            const captureId = resource.id || null;
            const amountValue = resource.amount?.value || '';
            const currencyCode = resource.amount?.currency_code || '';
            const capturedMinor = Math.round(Number(amountValue) * 100);

            if (
                !Number.isFinite(capturedMinor) ||
                capturedMinor !== Number(order.total_minor) ||
                String(currencyCode || '').toUpperCase() !== String(order.currency || 'EUR').toUpperCase()
            ) {
                console.error('[webhook/paypal] Importo o valuta non coerenti:', {
                    paypalOrderId, capturedMinor, currencyCode,
                    expectedMinor: order.total_minor, expectedCurrency: order.currency,
                });
                return new Response('OK', { status: 200 }); // Ack: non fulfillare, ma non far ritentare PayPal all'infinito
            }

            // Express checkout mai completato lato client: recupera il payer
            // dall'Order (la risorsa Capture del webhook non lo include).
            if (!order.customer_email) {
                try {
                    const { payer } = await getPaypalOrder(env.PAYPAL_BASE_URL, accessToken, paypalOrderId);
                    if (payer?.email) await setPaypalCustomerFromPayer(env.DB, order.id, payer);
                } catch (e) {
                    console.warn('[webhook/paypal] Recupero payer fallito:', e?.message || e);
                }
            }

            await markPaidPaypal(env.DB, order.id, { paypalOrderId, paypalCaptureId: captureId });
        }

        // Stock: sempre (idempotente via stock_deductions), anche su retry webhook.
        const updatedOrder = await getOrderById(env.DB, order.id);
        await deductStockForOrderRow(env.DB, updatedOrder || order);
        if (order.status !== 'paid') {
            await sendConfirmationOnce(
                env.DB, updatedOrder,
                env.RESEND_API_KEY, env.TRUSTPILOT_BCC || '',
                'webhook_paypal', env.GUIDES
            );
            await sendInternalOrderNotificationOnce(
                env.DB, updatedOrder,
                env.RESEND_API_KEY,
                'webhook_paypal'
            );
            await recordEvent(env, request, { eventName: 'purchase', orderId: order.id });
        }
    }

    return new Response('OK', { status: 200 });
}

/* ─── POST /api/track ────────────────────────────────────────────────────────── */
// Eventi CRO lato client (click PayPal Express, esiti, buy-now). Fail-open e
// permissivo di proposito, come le pageview: un tracking rotto non deve mai
// bloccare o rallentare l'utente. 'purchase' non è accettato qui — è scritto
// solo server-side dagli handler di capture/webhook.

async function handleTrack(request, env) {
    try {
        if (!isJsonContentType(request)) return new Response(null, { status: 204 });
        if (requestBodyTooLarge(request)) return new Response(null, { status: 204 });

        const body = await request.json().catch(() => null);
        const eventName = String(body?.event || '');
        if (!TRACKABLE_EVENTS.has(eventName)) return new Response(null, { status: 204 });

        const orderId = body?.orderId ? cleanString(body.orderId, 40) : undefined;
        const sku     = body?.sku ? cleanString(body.sku, 64) : undefined;
        // cartId lega l'evento alla riga di cart_sessions: e' cosi' che il funnel
        // diventa leggibile per singolo carrello abbandonato, non solo aggregato.
        const cartId  = body?.cartId ? cleanString(body.cartId, 64) : undefined;
        await recordEvent(env, request, { eventName, orderId, sku, cartId });
    } catch (e) {
        console.warn('[track] fallito (fail-open):', e?.message || e);
    }
    return new Response(null, { status: 204 });
}

/* ─── POST /api/bank-transfer-order ─────────────────────────────────────────── */

async function handleBankTransferOrder(request, env) {
    const invalidRequest = validateCheckoutRequest(request, env);
    if (invalidRequest) return invalidRequest;

    const body = await request.json().catch(() => null);
    if (!body) return err('Invalid JSON', 400, request, env);

    const paramsOrErr = await orderParamsFromBodySafe(body, 'bank_transfer', request, env);
    if (paramsOrErr.error) return paramsOrErr.error;
    const params = paramsOrErr;

    const rateGate = await gateNewCheckoutAttempt(env, request, params);
    if (rateGate) return rateGate;

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
            // Vedi handleCreatePaymentIntent: la chiave non copre i dati fiscali,
            // quindi il riuso deve riallinearli o vanno persi. Qui conta doppio:
            // l'email col riepilogo bonifico parte subito dopo, e la fattura la
            // si emette su questi campi.
            await updatePendingOrderCustomer(env.DB, orderId, params);
        } else {
            throw dbErr;
        }
    }
    await linkCartCheckoutStarted(env, body, orderId);

    // Per il bonifico invia subito email "ordine ricevuto + istruzioni IBAN"
    // (status = pending_payment, isPaid = false nel template → mostra IBAN + causale)
    const newOrder = await getOrderById(env.DB, orderId);
    await sendConfirmationOnce(
        env.DB, newOrder,
        env.RESEND_API_KEY, env.TRUSTPILOT_BCC || '',
        'bank_transfer_created', env.GUIDES
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
async function handleAdminRoute(path, request, env, context) {
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
    const sub = path.slice('/api/admin'.length); // es. '/orders' o '/orders/EL-xxx/mark-paid'

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
            env.RESEND_API_KEY || '', env.TRUSTPILOT_BCC || '', env.GUIDES
        );

        // Deduct anche su already_paid (idempotente): recupera stock se il primo
        // mark-paid era andato a buon fine senza scalare il magazzino.
        if (result.ok || result.reason === 'already_paid') {
            const paidOrder = await getOrderById(env.DB, orderId);
            await deductStockForOrderRow(env.DB, paidOrder);
        }

        const status = result.ok ? 200 : (result.reason === 'order_not_found' ? 404 : 409);
        return new Response(JSON.stringify(result), {
            status, headers: { 'Content-Type': 'application/json' },
        });
    }

    // ── GET /api/admin/stock ──────────────────────────────────────────────────
    if (sub === '/stock' && request.method === 'GET') {
        // Le richieste "avvisami" in attesa viaggiano con la riga di magazzino:
        // e' il numero che serve per decidere quanto riordinare, e va letto
        // accanto alla quantita', non in una pagina separata.
        const [items, pending] = await Promise.all([
            listAdminStock(env.DB),
            pendingCountsBySku(env.DB),
        ]);
        const withPending = items.map((item) => ({
            ...item,
            pending: pending.get(item.sku)?.pending || 0,
            pendingLastAt: pending.get(item.sku)?.lastAt || null,
        }));
        return new Response(JSON.stringify({ items: withPending }), {
            headers: { 'Content-Type': 'application/json' },
        });
    }

    // ── POST /api/admin/stock ─────────────────────────────────────────────────
    if (sub === '/stock' && request.method === 'POST') {
        const invalidRequest = validateAdminMutationRequest(request, env);
        if (invalidRequest) return invalidRequest;

        const body = await request.json().catch(() => ({}));
        try {
            const saved = await setStockQty(env.DB, body.sku, body.qty, actorEmail);

            // Rientro da esaurito: e' l'unico momento in cui partono gli avvisi.
            // Fuori dalla risposta (waitUntil) perche' il salvataggio della
            // quantita' non deve aspettare Resend per dirsi riuscito.
            let notifying = 0;
            if (saved.previousQty <= 0 && saved.qty > 0) {
                const pending = await pendingCountsBySku(env.DB);
                notifying = pending.get(saved.sku)?.pending || 0;
                if (notifying > 0) {
                    const entry = getCatalogEntry(saved.sku);
                    context.waitUntil(
                        sendRestockNotifications(
                            env.DB, saved.sku, entry?.name || saved.sku,
                            env.RESEND_API_KEY || '', env.SITE_ORIGIN || ''
                        ).catch((e) => console.error('[restock] invio fallito:', e?.message || e))
                    );
                }
            }

            return new Response(JSON.stringify({ ok: true, item: saved, notifying }), {
                headers: { 'Content-Type': 'application/json' },
            });
        } catch (e) {
            const status = e.reason === 'not_physical' ? 400
                : e.reason === 'invalid_qty' ? 400
                : 400;
            return adminJson({ ok: false, error: e.message, reason: e.reason || 'error' }, status);
        }
    }

    // ── GET /api/admin/restock?sku= ───────────────────────────────────────────
    if (sub === '/restock' && request.method === 'GET') {
        const sku = new URL(request.url).searchParams.get('sku') || '';
        if (!isPhysicalSku(sku)) {
            return adminJson({ error: 'SKU non fisico o non in catalogo', reason: 'not_physical' }, 400);
        }
        try {
            const items = await listPendingForSku(env.DB, sku);
            return new Response(JSON.stringify({ sku, items }), {
                headers: { 'Content-Type': 'application/json' },
            });
        } catch (e) {
            console.warn('[restock] lista non disponibile:', e?.message || e);
            return new Response(JSON.stringify({ sku, items: [] }), {
                headers: { 'Content-Type': 'application/json' },
            });
        }
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

    // ── GET /api/admin/carts ──────────────────────────────────────────────────
    if (sub === '/carts' && request.method === 'GET') {
        const qs   = new URL(request.url).searchParams;
        const days = qs.has('days') ? Number(qs.get('days')) : 30;
        // Unica soglia per lista, statistiche ed etichette: viene rimandata al
        // client, che non deve avere una copia propria del valore.
        const hoursIdle = normalizeHoursIdle(qs.get('hoursIdle') ?? undefined);

        const [result, stats] = await Promise.all([
            listCarts(env.DB, {
                page:      Number(qs.get('page')) || 1,
                status:    qs.get('status') || 'abandoned',
                hoursIdle,
                hasEmail:  qs.get('hasEmail') === '1' ? true : (qs.get('hasEmail') === '0' ? false : undefined),
                country:   qs.get('country') || '',
                days,
            }),
            getCartStats(env.DB, { days, hoursIdle }),
        ]);
        result.stats = stats;
        result.hoursIdle = hoursIdle;
        result.capabilities = { deleteCarts: adminDeleteCartsEnabled(env) };

        // Anche in periodi di poco traffico la pulizia trova un'occasione per girare.
        maybeRunCartRetention(context);

        return new Response(JSON.stringify(result), {
            headers: { 'Content-Type': 'application/json' },
        });
    }

    // ── DELETE /api/admin/carts/:id ─────────────────────────────────────────────
    const deleteCartMatch = sub.match(/^\/carts\/([^/]+)$/);
    if (deleteCartMatch && request.method === 'DELETE') {
        const invalidRequest = validateAdminMutationRequest(request, env, { requireJson: false });
        if (invalidRequest) return invalidRequest;
        if (!adminDeleteCartsEnabled(env)) {
            return adminJson({ ok: false, error: 'Delete disabled', reason: 'delete_disabled' }, 403);
        }

        const cartId = deleteCartMatch[1];
        const result = await deleteCart(env.DB, cartId);
        const status = result.ok ? 200 : (result.reason === 'cart_not_found' ? 404 : 409);
        return new Response(JSON.stringify(result), {
            status, headers: { 'Content-Type': 'application/json' },
        });
    }

    // ── GET /api/admin/analytics ──────────────────────────────────────────────
    if (sub === '/analytics' && request.method === 'GET') {
        const qs          = new URL(request.url).searchParams;
        const days        = qs.has('days') ? Number(qs.get('days')) : 30;
        const includeBots = qs.get('bots') === 'include';

        const summary = await getAnalyticsSummary(env.DB, { days, includeBots });
        return new Response(JSON.stringify(summary), {
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
        const status  = result.ok
            ? 200
            : (result.reason === 'order_not_found' ? 404 : 409);
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
