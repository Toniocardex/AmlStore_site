/**
 * admin.js — helper per il pannello amministrativo Aml Store.
 *
 * Esporta:
 *   verifyAccessJwt(request, env)          — verifica JWT Cloudflare Access
 *   listOrders(db, opts)                   — lista ordini paginata e filtrabile
 *   getOrderDetail(db, orderId)            — dettaglio singolo ordine
 *   markBankTransferPaid(db, orderId, ...) — transizione pending → paid + email
 *   archiveOrder(db, orderId)              — soft-archive
 *   unarchiveOrder(db, orderId)            — rimuove archive
 *
 * Variabili ambiente richieste:
 *   CF_ACCESS_TEAM_DOMAIN — es. "amlstore.cloudflareaccess.com"
 *   CF_ACCESS_AUD         — Application Audience tag (da Zero Trust → Access → App)
 *   RESEND_API_KEY        — per sendPaidNotificationOnce
 *   TRUSTPILOT_BCC        — indirizzo BCC Trustpilot AFS
 *
 * Policy email bonifico:
 *   1. Ordine creato (pending_payment) → email IBAN inviata via sendConfirmationOnce
 *      → confirmation_email_sent_at valorizzato, NESSUN BCC Trustpilot
 *   2. Admin marca pagato → sendPaidNotificationOnce → email "pagamento ricevuto"
 *      → paid_notification_sent_at valorizzato, BCC Trustpilot incluso
 *   In questo modo Trustpilot riceve l'invito solo quando l'ordine è effettivamente pagato.
 */

import { emailSubject, emailHtml, emailText } from './templates.js';

/* ─── JWT Cloudflare Access ──────────────────────────────────────────────────── */

function b64urlDecode(str) {
    const b64 = str.replace(/-/g, '+').replace(/_/g, '/');
    const pad  = b64 + '='.repeat((4 - b64.length % 4) % 4);
    const bin  = atob(pad);
    return Uint8Array.from(bin, c => c.charCodeAt(0));
}

function parseJwt(token) {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    try {
        const dec  = b => new TextDecoder().decode(b64urlDecode(b));
        return {
            header:  JSON.parse(dec(parts[0])),
            payload: JSON.parse(dec(parts[1])),
            parts,
        };
    } catch (_) { return null; }
}

async function fetchJwks(teamDomain) {
    const url = `https://${teamDomain}/cdn-cgi/access/certs`;
    const res = await fetch(url, { cf: { cacheEverything: true, cacheTtl: 300 } });
    if (!res.ok) throw new Error(`JWKS fetch failed: ${res.status}`);
    return res.json();
}

/**
 * Verifica il JWT Cloudflare Access presente nell'header Cf-Access-Jwt-Assertion.
 *
 * @param {Request} request
 * @param {object}  env — deve contenere CF_ACCESS_TEAM_DOMAIN e CF_ACCESS_AUD
 * @returns {Promise<{valid: boolean, email?: string, reason?: string}>}
 */
export async function verifyAccessJwt(request, env) {
    // Cloudflare Access injects Cf-Access-Jwt-Assertion for protected paths.
    // For same-origin API calls from the browser, fall back to the CF_Authorization
    // cookie that CF Access sets after authentication.
    let token = request.headers.get('Cf-Access-Jwt-Assertion');
    if (!token) {
        const cookieHeader = request.headers.get('Cookie') || '';
        const match = cookieHeader.match(/(?:^|;\s*)CF_Authorization=([^;]+)/);
        token = match ? match[1] : null;
    }
    if (!token) return { valid: false, reason: 'missing_jwt' };

    const parsed = parseJwt(token);
    if (!parsed) return { valid: false, reason: 'malformed_jwt' };

    const { header, payload, parts } = parsed;

    // 1. Scadenza
    const nowSec = Math.floor(Date.now() / 1000);
    if (payload.exp && payload.exp < nowSec) {
        return { valid: false, reason: 'expired' };
    }

    // 2. Audience
    const expectedAud = env.CF_ACCESS_AUD;
    if (expectedAud) {
        const aud = Array.isArray(payload.aud) ? payload.aud : [payload.aud];
        if (!aud.includes(expectedAud)) {
            return { valid: false, reason: 'invalid_aud' };
        }
    }

    // 3. Firma RS256 via JWKS
    const teamDomain = env.CF_ACCESS_TEAM_DOMAIN;
    if (!teamDomain) {
        // Configurazione mancante: log + rifiuto (non bypassabile in prod)
        console.error('[admin] CF_ACCESS_TEAM_DOMAIN non configurato');
        return { valid: false, reason: 'misconfigured' };
    }

    let jwks;
    try {
        jwks = await fetchJwks(teamDomain);
    } catch (e) {
        console.error('[admin] JWKS fetch error:', e.message);
        return { valid: false, reason: 'jwks_fetch_error' };
    }

    const jwk = jwks.keys?.find(k => k.kid === header.kid);
    if (!jwk) return { valid: false, reason: 'key_not_found' };

    try {
        const cryptoKey = await crypto.subtle.importKey(
            'jwk', jwk,
            { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' },
            false, ['verify']
        );
        const signingInput = new TextEncoder().encode(`${parts[0]}.${parts[1]}`);
        const signature    = b64urlDecode(parts[2]);
        const valid = await crypto.subtle.verify(
            'RSASSA-PKCS1-v1_5', cryptoKey, signature, signingInput
        );
        if (!valid) return { valid: false, reason: 'invalid_signature' };
    } catch (e) {
        console.error('[admin] JWT verify error:', e.message);
        return { valid: false, reason: 'verify_error' };
    }

    return {
        valid: true,
        email: payload.email || payload.sub || 'unknown',
    };
}

/* ─── Query D1 lista ordini ──────────────────────────────────────────────────── */

const PAGE_SIZE = 50;

/**
 * Lista ordini con filtri opzionali e paginazione.
 *
 * @param {D1Database} db
 * @param {object} opts
 * @param {number}  [opts.page=1]
 * @param {string}  [opts.status='']          — '' = tutti
 * @param {string}  [opts.paymentMethod='']   — '' = tutti
 * @param {string}  [opts.search='']          — cerca su id, email, nome, cognome, azienda
 * @param {boolean} [opts.includeArchived=false]
 * @returns {Promise<{orders, total, page, pageSize}>}
 */
export async function listOrders(db, {
    page            = 1,
    status          = '',
    paymentMethod   = '',
    search          = '',
    includeArchived = false,
} = {}) {
    const offset     = (Math.max(1, page) - 1) * PAGE_SIZE;
    const conditions = [];
    const bindings   = [];

    if (!includeArchived) {
        conditions.push('archived_at IS NULL');
    }
    if (status) {
        conditions.push('status = ?');
        bindings.push(status);
    }
    if (paymentMethod) {
        conditions.push('payment_method = ?');
        bindings.push(paymentMethod);
    }
    if (search) {
        const q = `%${search}%`;
        conditions.push(
            '(id LIKE ? OR customer_email LIKE ? OR customer_first_name LIKE ? OR customer_last_name LIKE ? OR customer_company LIKE ?)'
        );
        bindings.push(q, q, q, q, q);
    }

    const where = conditions.length ? 'WHERE ' + conditions.join(' AND ') : '';

    const countRow = await db
        .prepare(`SELECT COUNT(*) as n FROM orders ${where}`)
        .bind(...bindings)
        .first();
    const total = countRow?.n ?? 0;

    const rows = await db
        .prepare(`
            SELECT id, status, payment_method, created_at, paid_at, updated_at,
                   customer_email, customer_first_name, customer_last_name,
                   customer_company, customer_type, locale,
                   total_minor, currency,
                   stripe_session_id, stripe_payment_intent,
                   paypal_order_id, paypal_capture_id,
                   confirmation_email_sent_at, paid_notification_sent_at,
                   archived_at, marked_paid_at, marked_paid_by, admin_notes,
                   line_items
            FROM orders ${where}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        `)
        .bind(...bindings, PAGE_SIZE, offset)
        .all();

    return {
        orders:   (rows.results || []).map(formatAdminOrder),
        total,
        page:     Math.max(1, page),
        pageSize: PAGE_SIZE,
    };
}

/**
 * Dettaglio completo di un singolo ordine.
 * @param {D1Database} db
 * @param {string} orderId
 * @returns {Promise<object|null>}
 */
export async function getOrderDetail(db, orderId) {
    const row = await db
        .prepare('SELECT * FROM orders WHERE id = ?')
        .bind(orderId)
        .first();
    return row ? formatAdminOrder(row) : null;
}

function formatAdminOrder(row) {
    let lineItems = [];
    try { lineItems = JSON.parse(row.line_items || '[]'); } catch (_) {}
    return {
        orderId:                    row.id,
        status:                     row.status,
        paymentMethod:              row.payment_method,
        createdAt:                  row.created_at,
        paidAt:                     row.paid_at,
        updatedAt:                  row.updated_at,
        archivedAt:                 row.archived_at,
        markedPaidAt:               row.marked_paid_at,
        markedPaidBy:               row.marked_paid_by,
        adminNotes:                 row.admin_notes,
        customer: {
            email:     row.customer_email,
            firstName: row.customer_first_name,
            lastName:  row.customer_last_name,
            company:   row.customer_company   || null,
            type:      row.customer_type      || 'private',
            phone:     row.customer_phone     || null,
            piva:      row.customer_piva      || null,
            sdi:       row.customer_sdi       || null,
            pec:       row.customer_pec       || null,
        },
        locale:                     row.locale,
        lineItems,
        totalMinor:                 row.total_minor,
        currency:                   row.currency,
        stripeSessionId:            row.stripe_session_id            || null,
        stripePaymentIntent:        row.stripe_payment_intent        || null,
        paypalOrderId:              row.paypal_order_id              || null,
        paypalCaptureId:            row.paypal_capture_id            || null,
        confirmationEmailSentAt:    row.confirmation_email_sent_at   || null,
        paidNotificationSentAt:     row.paid_notification_sent_at    || null,
    };
}

/* ─── Azioni admin ───────────────────────────────────────────────────────────── */

/**
 * Segna un ordine bank_transfer pending come pagato.
 *
 * Atomico: la UPDATE ha WHERE status='pending_payment' AND payment_method='bank_transfer'
 * per evitare doppia esecuzione. Se meta.changes === 0 → già pagato o non trovato.
 *
 * Side-effect: invia email "pagamento ricevuto" con BCC Trustpilot (idempotente via
 * paid_notification_sent_at).
 *
 * @param {D1Database} db
 * @param {string}     orderId
 * @param {string}     actorEmail  — email admin dal JWT (per audit)
 * @param {string|null} notes      — note opzionali visibili solo in admin
 * @param {string}     resendApiKey
 * @param {string}     trustpilotBcc
 * @returns {Promise<{ok: boolean, reason?: string, emailResult?: object}>}
 */
export async function markBankTransferPaid(db, orderId, actorEmail, notes, resendApiKey, trustpilotBcc) {
    const ts = new Date().toISOString();

    const result = await db.prepare(`
        UPDATE orders
        SET status         = 'paid',
            paid_at        = ?,
            updated_at     = ?,
            marked_paid_at = ?,
            marked_paid_by = ?,
            admin_notes    = CASE WHEN ? IS NOT NULL THEN ? ELSE admin_notes END
        WHERE id = ?
          AND status         = 'pending_payment'
          AND payment_method = 'bank_transfer'
    `).bind(ts, ts, ts, actorEmail, notes || null, notes || null, orderId).run();

    const changed = result.meta?.changes ?? 0;
    if (changed === 0) {
        // Nessuna riga modificata: capire perché
        const existing = await db
            .prepare('SELECT id, status, payment_method FROM orders WHERE id = ?')
            .bind(orderId).first();
        if (!existing)                                  return { ok: false, reason: 'order_not_found' };
        if (existing.payment_method !== 'bank_transfer') return { ok: false, reason: 'not_bank_transfer' };
        if (existing.status === 'paid')                  return { ok: false, reason: 'already_paid' };
        return { ok: false, reason: 'update_failed' };
    }

    // Rilegge ordine aggiornato
    const order = await db.prepare('SELECT * FROM orders WHERE id = ?').bind(orderId).first();
    if (!order) return { ok: true }; // aggiornato ma non riletto: anomalia non bloccante

    // Invia email "pagamento ricevuto" con BCC Trustpilot
    const emailResult = await sendPaidNotificationOnce(
        db, order, resendApiKey, trustpilotBcc
    );

    return { ok: true, emailResult };
}

/**
 * Soft-archive un ordine (non lo cancella dal DB).
 */
export async function archiveOrder(db, orderId) {
    const ts = new Date().toISOString();
    await db.prepare(
        'UPDATE orders SET archived_at = ?, updated_at = ? WHERE id = ?'
    ).bind(ts, ts, orderId).run();
}

/**
 * Rimuove il flag di archivio (ripristina visibilità nella lista ordini).
 */
export async function unarchiveOrder(db, orderId) {
    const ts = new Date().toISOString();
    await db.prepare(
        'UPDATE orders SET archived_at = NULL, updated_at = ? WHERE id = ?'
    ).bind(ts, orderId).run();
}

/* ─── Email pagamento confermato (bonifico) ──────────────────────────────────── */

/**
 * Invia la email di "pagamento ricevuto" per ordini bonifico ora paid.
 * Usa il flag paid_notification_sent_at per idempotenza (separato da
 * confirmation_email_sent_at usato per la mail iniziale pending).
 *
 * @param {D1Database} db
 * @param {object}     order         — riga grezza D1
 * @param {string}     resendApiKey
 * @param {string}     trustpilotBcc — '' se non configurato
 * @returns {Promise<{sent: boolean, skipped?: boolean, error?: string}>}
 */
async function sendPaidNotificationOnce(db, order, resendApiKey, trustpilotBcc) {
    if (order.paid_notification_sent_at) return { sent: false, skipped: true };
    if (!resendApiKey) {
        console.warn('[admin/email] RESEND_API_KEY non configurato, email non inviata');
        return { sent: false, error: 'no_resend_key' };
    }

    const locale = order.locale || 'it';
    const orderForTemplate = {
        orderId:       order.id,
        status:        'paid',
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
        causale:       undefined,   // non mostrato nella mail "pagato"
    };

    const payload = {
        from:     'Aml Store <ordini@aml-store.com>',
        to:       [`${order.customer_first_name} ${order.customer_last_name} <${order.customer_email}>`],
        subject:  emailSubject(locale, order.id, true),
        html:     emailHtml(orderForTemplate, true),
        text:     emailText(orderForTemplate, true),
        reply_to: 'Info@amlstore.it',
    };

    // BCC Trustpilot: incluso perché ora l'ordine è effettivamente pagato
    if (trustpilotBcc) payload.bcc = [trustpilotBcc];

    let res;
    try {
        res = await fetch('https://api.resend.com/emails', {
            method:  'POST',
            headers: { 'Authorization': `Bearer ${resendApiKey}`, 'Content-Type': 'application/json' },
            body:    JSON.stringify(payload),
        });
    } catch (e) {
        console.error('[admin/email] Network error:', e);
        return { sent: false, error: 'network_error' };
    }

    if (!res.ok) {
        const body = await res.text().catch(() => '');
        console.error(`[admin/email] Resend HTTP ${res.status}:`, body);
        return { sent: false, error: `resend_${res.status}` };
    }

    // Solo dopo 2xx: aggiorna flag idempotenza
    try {
        const ts = new Date().toISOString();
        await db.prepare(
            'UPDATE orders SET paid_notification_sent_at = ?, updated_at = ? WHERE id = ?'
        ).bind(ts, ts, order.id).run();
    } catch (e) {
        console.error('[admin/email] DB flag update error:', e);
    }

    return { sent: true };
}

function safeParseJSON(raw, fallback) {
    try { return JSON.parse(raw || 'null') ?? fallback; } catch (_) { return fallback; }
}
