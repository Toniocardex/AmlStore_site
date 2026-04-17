/**
 * order.js — helper D1 per la gestione ordini Aml Store.
 */

function now() {
    return new Date().toISOString();
}

/**
 * Crea un nuovo ordine con status 'pending_payment'.
 * Lancia un errore se idempotency_key già presente (UNIQUE constraint D1).
 *
 * @param {D1Database} db
 * @param {object} params
 * @returns {Promise<string>} orderId
 */
export async function createOrder(db, {
    idempotencyKey,
    customerEmail,
    customerFirstName,
    customerLastName,
    customerCompany,
    customerType,
    customerPhone,
    customerPiva,
    customerSdi,
    customerPec,
    locale,
    lineItems,       // array of objects
    totalMinor,
    currency,
    paymentMethod,
}) {
    // Genera ID breve leggibile: AML- + 8 caratteri uppercase alfanumerici
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // no I,O,0,1 (ambigui)
    const arr = new Uint8Array(8);
    crypto.getRandomValues(arr);
    const shortId = 'AML-' + Array.from(arr).map(b => chars[b % chars.length]).join('');
    const id = shortId;
    const ts = now();

    await db.prepare(`
        INSERT INTO orders (
            id, idempotency_key, status, created_at, updated_at,
            customer_email, customer_first_name, customer_last_name,
            customer_company, customer_type, customer_phone,
            customer_piva, customer_sdi, customer_pec, locale,
            line_items, total_minor, currency, payment_method
        ) VALUES (
            ?, ?, 'pending_payment', ?, ?,
            ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?, ?
        )
    `).bind(
        id, idempotencyKey, ts, ts,
        customerEmail, customerFirstName, customerLastName,
        customerCompany || null, customerType || 'private', customerPhone || null,
        customerPiva || null, customerSdi || null, customerPec || null, locale || 'it',
        JSON.stringify(lineItems), totalMinor, currency || 'EUR', paymentMethod
    ).run();

    return id;
}

/**
 * Recupera un ordine per ID.
 * @param {D1Database} db
 * @param {string} orderId
 * @returns {Promise<object|null>}
 */
export async function getOrderById(db, orderId) {
    return db.prepare('SELECT * FROM orders WHERE id = ?').bind(orderId).first();
}

/**
 * Recupera un ordine per stripe_session_id.
 * @param {D1Database} db
 * @param {string} sessionId
 * @returns {Promise<object|null>}
 */
export async function getOrderByStripeSession(db, sessionId) {
    return db.prepare('SELECT * FROM orders WHERE stripe_session_id = ?').bind(sessionId).first();
}

/**
 * Recupera un ordine per paypal_order_id.
 * @param {D1Database} db
 * @param {string} paypalOrderId
 * @returns {Promise<object|null>}
 */
export async function getOrderByPaypalOrderId(db, paypalOrderId) {
    return db.prepare('SELECT * FROM orders WHERE paypal_order_id = ?').bind(paypalOrderId).first();
}

/**
 * Aggiorna lo stripe_session_id su un ordine appena creato.
 * @param {D1Database} db
 * @param {string} orderId
 * @param {string} stripeSessionId
 */
export async function setStripeSession(db, orderId, stripeSessionId) {
    await db.prepare(`
        UPDATE orders SET stripe_session_id = ?, updated_at = ? WHERE id = ?
    `).bind(stripeSessionId, now(), orderId).run();
}

/**
 * Promuove un ordine a 'paid' con i riferimenti PSP Stripe.
 * @param {D1Database} db
 * @param {string} orderId
 * @param {object} params
 */
export async function markPaidStripe(db, orderId, { stripeSessionId, stripePaymentIntent }) {
    const ts = now();
    await db.prepare(`
        UPDATE orders
        SET status = 'paid', paid_at = ?, updated_at = ?,
            stripe_session_id = ?, stripe_payment_intent = ?
        WHERE id = ?
    `).bind(ts, ts, stripeSessionId || null, stripePaymentIntent || null, orderId).run();
}

/**
 * Promuove un ordine a 'paid' con i riferimenti PSP PayPal.
 * @param {D1Database} db
 * @param {string} orderId
 * @param {object} params
 */
export async function markPaidPaypal(db, orderId, { paypalOrderId, paypalCaptureId }) {
    const ts = now();
    await db.prepare(`
        UPDATE orders
        SET status = 'paid', paid_at = ?, updated_at = ?,
            paypal_order_id = ?, paypal_capture_id = ?
        WHERE id = ?
    `).bind(ts, ts, paypalOrderId || null, paypalCaptureId || null, orderId).run();
}

/**
 * Aggiorna il paypal_order_id su un ordine pending.
 * @param {D1Database} db
 * @param {string} orderId
 * @param {string} paypalOrderId
 */
export async function setPaypalOrderId(db, orderId, paypalOrderId) {
    await db.prepare(`
        UPDATE orders SET paypal_order_id = ?, updated_at = ? WHERE id = ?
    `).bind(paypalOrderId, now(), orderId).run();
}

/**
 * Marca la email di conferma come inviata (idempotenza).
 * @param {D1Database} db
 * @param {string} orderId
 * @param {string} eventSrc — es. 'webhook_stripe', 'worker_capture', ecc.
 */
export async function markConfirmationEmailSent(db, orderId, eventSrc) {
    const ts = now();
    await db.prepare(`
        UPDATE orders
        SET confirmation_email_sent_at = ?, confirmation_email_event_src = ?, updated_at = ?
        WHERE id = ?
    `).bind(ts, eventSrc, ts, orderId).run();
}

/**
 * Restituisce solo i campi pubblici di un ordine (per la thank-you page).
 * Non espone dati fiscali, PSP interni, ecc.
 * @param {object} order — riga grezza da D1
 * @returns {object}
 */
export function toPublicOrder(order) {
    if (!order) return null;
    return {
        orderId:       order.id,
        status:        order.status,
        paymentMethod: order.payment_method,
        createdAt:     order.created_at,
        paidAt:        order.paid_at,
        firstName:     order.customer_first_name,
        lastName:      order.customer_last_name,
        email:         order.customer_email,
        locale:        order.locale,
        lineItems:     safeParseLineItems(order.line_items),
        totalMinor:    order.total_minor,
        currency:      order.currency,
        // Causale solo per bonifico
        causale:       order.payment_method === 'bank_transfer' ? order.id : undefined,
    };
}

function safeParseLineItems(raw) {
    try { return JSON.parse(raw || '[]'); } catch (_) { return []; }
}
