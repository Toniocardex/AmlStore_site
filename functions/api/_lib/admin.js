/**
 * admin.js — helper per il pannello amministrativo Aml Store.
 *
 * Esporta:
 *   verifyAccessJwt(request, env)          — verifica JWT Cloudflare Access (RS256)
 *   listOrders(db, opts)                   — lista ordini paginata e filtrabile
 *   getOrderDetail(db, orderId)            — dettaglio singolo ordine
 *   markBankTransferPaid(db, orderId, ...) — transizione pending → paid + email
 *   archiveOrder(db, orderId)              — soft-archive
 *   unarchiveOrder(db, orderId)            — rimuove archive
 *
 * Variabili ambiente richieste:
 *   CF_ACCESS_TEAM_DOMAIN — es. "amlstore.cloudflareaccess.com"
 *   CF_ACCESS_AUD         — Application Audience tag (Zero Trust → Access → App → Audience)
 *   RESEND_API_KEY        — per sendPaidNotificationOnce (via email.js)
 *   TRUSTPILOT_BCC        — indirizzo BCC Trustpilot AFS
 *
 * Policy email bonifico:
 *   1. Ordine creato (pending_payment) → email IBAN via sendConfirmationOnce (no BCC Trustpilot)
 *   2. Admin marca pagato → sendPaidNotificationOnce → email "pagamento ricevuto" (BCC Trustpilot)
 */

import { now, safeParseJSON }          from './utils.js';
import { sendPaidNotificationOnce }    from './email.js';

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
        const dec = b => new TextDecoder().decode(b64urlDecode(b));
        return {
            header:  JSON.parse(dec(parts[0])),
            payload: JSON.parse(dec(parts[1])),
            parts,
        };
    } catch (_) { return null; }
}

async function fetchJwks(teamDomain) {
    const res = await fetch(
        `https://${teamDomain}/cdn-cgi/access/certs`,
        { cf: { cacheEverything: true, cacheTtl: 300 } }
    );
    if (!res.ok) throw new Error(`JWKS fetch failed: ${res.status}`);
    return res.json();
}

/**
 * Verifica il JWT Cloudflare Access.
 * Legge prima l'header Cf-Access-Jwt-Assertion (iniettato da CF sui path protetti),
 * poi il cookie CF_Authorization (inviato dal browser nelle chiamate same-origin).
 *
 * @param {Request} request
 * @param {object}  env
 * @returns {Promise<{valid: boolean, email?: string, reason?: string}>}
 */
export async function verifyAccessJwt(request, env) {
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
    if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) {
        return { valid: false, reason: 'expired' };
    }

    // 2. Audience (opzionale — la firma RS256 è la garanzia primaria)
    const expectedAud = env.CF_ACCESS_AUD;
    if (expectedAud) {
        const aud = Array.isArray(payload.aud) ? payload.aud : [payload.aud];
        if (!aud.includes(expectedAud)) {
            console.warn('[admin] AUD mismatch — JWT aud:', aud, '| expected:', expectedAud);
        }
    }

    // 3. Firma RS256 via JWKS
    const teamDomain = env.CF_ACCESS_TEAM_DOMAIN;
    if (!teamDomain) {
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
        const valid = await crypto.subtle.verify(
            'RSASSA-PKCS1-v1_5',
            cryptoKey,
            b64urlDecode(parts[2]),
            new TextEncoder().encode(`${parts[0]}.${parts[1]}`)
        );
        if (!valid) return { valid: false, reason: 'invalid_signature' };
    } catch (e) {
        console.error('[admin] JWT verify error:', e.message);
        return { valid: false, reason: 'verify_error' };
    }

    return { valid: true, email: payload.email || payload.sub || 'unknown' };
}

/* ─── Query D1 lista ordini ──────────────────────────────────────────────────── */

const PAGE_SIZE = 50;

/**
 * Lista ordini con filtri opzionali e paginazione.
 * Esegue COUNT e SELECT in parallelo per ridurre latenza D1.
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

    if (!includeArchived)  conditions.push('archived_at IS NULL');
    if (status)            { conditions.push('status = ?');          bindings.push(status); }
    if (paymentMethod)     { conditions.push('payment_method = ?');  bindings.push(paymentMethod); }
    if (search) {
        const q = `%${search}%`;
        conditions.push('(id LIKE ? OR customer_email LIKE ? OR customer_first_name LIKE ? OR customer_last_name LIKE ? OR customer_company LIKE ?)');
        bindings.push(q, q, q, q, q);
    }

    const where = conditions.length ? 'WHERE ' + conditions.join(' AND ') : '';

    // COUNT e SELECT in parallelo
    const [countRow, rows] = await Promise.all([
        db.prepare(`SELECT COUNT(*) as n FROM orders ${where}`)
          .bind(...bindings).first(),
        db.prepare(`
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
        `).bind(...bindings, PAGE_SIZE, offset).all(),
    ]);

    return {
        orders:   (rows.results || []).map(formatAdminOrder),
        total:    countRow?.n ?? 0,
        page:     Math.max(1, page),
        pageSize: PAGE_SIZE,
    };
}

/**
 * Dettaglio completo di un singolo ordine.
 */
export async function getOrderDetail(db, orderId) {
    const row = await db.prepare('SELECT * FROM orders WHERE id = ?').bind(orderId).first();
    return row ? formatAdminOrder(row) : null;
}

function formatAdminOrder(row) {
    return {
        orderId:                 row.id,
        status:                  row.status,
        paymentMethod:           row.payment_method,
        createdAt:               row.created_at,
        paidAt:                  row.paid_at,
        updatedAt:               row.updated_at,
        archivedAt:              row.archived_at              || null,
        markedPaidAt:            row.marked_paid_at           || null,
        markedPaidBy:            row.marked_paid_by           || null,
        adminNotes:              row.admin_notes              || null,
        customer: {
            email:     row.customer_email,
            firstName: row.customer_first_name,
            lastName:  row.customer_last_name,
            company:   row.customer_company  || null,
            type:      row.customer_type     || 'private',
            phone:     row.customer_phone    || null,
            piva:      row.customer_piva     || null,
            sdi:       row.customer_sdi      || null,
            pec:       row.customer_pec      || null,
        },
        locale:                  row.locale,
        lineItems:               safeParseJSON(row.line_items, []),
        totalMinor:              row.total_minor,
        currency:                row.currency,
        stripeSessionId:         row.stripe_session_id         || null,
        stripePaymentIntent:     row.stripe_payment_intent     || null,
        paypalOrderId:           row.paypal_order_id           || null,
        paypalCaptureId:         row.paypal_capture_id         || null,
        confirmationEmailSentAt: row.confirmation_email_sent_at || null,
        paidNotificationSentAt:  row.paid_notification_sent_at  || null,
    };
}

/* ─── Azioni admin ───────────────────────────────────────────────────────────── */

/**
 * Segna un ordine bank_transfer pending come pagato.
 * Atomico: WHERE status='pending_payment' AND payment_method='bank_transfer'.
 * Se changes === 0 → ordine non trovato, già pagato o metodo diverso.
 */
export async function markBankTransferPaid(db, orderId, actorEmail, notes, resendApiKey, trustpilotBcc) {
    const ts = now();

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

    if ((result.meta?.changes ?? 0) === 0) {
        const existing = await db
            .prepare('SELECT id, status, payment_method FROM orders WHERE id = ?')
            .bind(orderId).first();
        if (!existing)                                   return { ok: false, reason: 'order_not_found' };
        if (existing.payment_method !== 'bank_transfer') return { ok: false, reason: 'not_bank_transfer' };
        if (existing.status === 'paid')                  return { ok: false, reason: 'already_paid' };
        return { ok: false, reason: 'update_failed' };
    }

    const order = await db.prepare('SELECT * FROM orders WHERE id = ?').bind(orderId).first();
    if (!order) return { ok: true };

    const emailResult = await sendPaidNotificationOnce(db, order, resendApiKey, trustpilotBcc);
    return { ok: true, emailResult };
}

/** Soft-archive un ordine. */
export async function archiveOrder(db, orderId) {
    const ts = now();
    await db.prepare(
        'UPDATE orders SET archived_at = ?, updated_at = ? WHERE id = ?'
    ).bind(ts, ts, orderId).run();
}

/** Rimuove il flag di archivio. */
export async function unarchiveOrder(db, orderId) {
    await db.prepare(
        'UPDATE orders SET archived_at = NULL, updated_at = ? WHERE id = ?'
    ).bind(now(), orderId).run();
}
