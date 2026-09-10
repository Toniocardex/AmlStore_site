/**
 * Webhook Resend (Svix) per lo stato di consegna delle mail licenza.
 *
 * Nessuna dipendenza npm: HMAC SHA-256 come Stripe. Eventi di apertura/click
 * ignorati. Le altre mail transazionali (conferma, interna) non hanno
 * license_email_resend_id ne' tag kind=license: il webhook fa ack e non tocca nulla.
 *
 * Se email.delivered arriva prima di markLicenseEmailSent, l'id Resend non e'
 * ancora in D1: si riallinea con i tag kind=license + order_id.
 */

import { now } from './utils.js';

const SVIX_TOLERANCE_SEC = 300;

const DELIVERY_RANK = {
    accepted: 1,
    delayed: 2,
    delivered: 3,
    bounced: 4,
    complained: 4,
    failed: 4,
};

export function mappedLicenseDelivery(eventType) {
    switch (String(eventType || '')) {
        case 'email.sent': return 'accepted';
        case 'email.delivered': return 'delivered';
        case 'email.bounced': return 'bounced';
        case 'email.complained': return 'complained';
        case 'email.delivery_delayed': return 'delayed';
        case 'email.failed': return 'failed';
        default: return null;
    }
}

export function shouldUpgradeDelivery(current, next) {
    return (DELIVERY_RANK[next] || 0) > (DELIVERY_RANK[current] || 0);
}

/** Tag Resend: in send API sono `[{name,value}]`, nel webhook un oggetto. */
export function licenseOrderIdFromResendTags(tags) {
    const map = {};
    if (Array.isArray(tags)) {
        for (const t of tags) {
            if (t && t.name) map[String(t.name)] = String(t.value ?? '');
        }
    } else if (tags && typeof tags === 'object') {
        for (const [k, v] of Object.entries(tags)) map[k] = String(v ?? '');
    }
    if (map.kind !== 'license') return '';
    return String(map.order_id || '').trim().slice(0, 50);
}

function timingSafeEqualB64(a, b) {
    const left = String(a || '');
    const right = String(b || '');
    if (left.length !== right.length) return false;
    let diff = 0;
    for (let i = 0; i < left.length; i++) diff |= left.charCodeAt(i) ^ right.charCodeAt(i);
    return diff === 0;
}

function bufToB64(buf) {
    const bytes = new Uint8Array(buf);
    let s = '';
    for (const b of bytes) s += String.fromCharCode(b);
    return btoa(s);
}

/**
 * @param {string} rawBody
 * @param {{ get: (name: string) => string|null }} headers
 * @param {string} webhookSecret  — `whsec_...` dalla dashboard Resend
 */
export async function verifyResendWebhook(rawBody, headers, webhookSecret, toleranceSec = SVIX_TOLERANCE_SEC) {
    const secret = String(webhookSecret || '');
    if (!secret) throw new Error('Missing Resend webhook secret');

    const msgId = headers.get('svix-id') || '';
    const timestamp = headers.get('svix-timestamp') || '';
    const sigHeader = headers.get('svix-signature') || '';
    if (!msgId || !timestamp || !sigHeader) {
        throw new Error('Missing Svix headers');
    }

    const age = Math.floor(Date.now() / 1000) - Number(timestamp);
    if (!Number.isFinite(Number(timestamp)) || Math.abs(age) > toleranceSec) {
        throw new Error(`Resend webhook timestamp out of tolerance (${age}s)`);
    }

    const keyB64 = secret.startsWith('whsec_') ? secret.slice(6) : secret;
    const keyBytes = Uint8Array.from(atob(keyB64), (c) => c.charCodeAt(0));
    const key = await crypto.subtle.importKey(
        'raw',
        keyBytes,
        { name: 'HMAC', hash: 'SHA-256' },
        false,
        ['sign']
    );
    const signed = `${msgId}.${timestamp}.${rawBody}`;
    const sigBuf = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(signed));
    const expected = bufToB64(sigBuf);

    const candidates = sigHeader.split(/\s+/).map((part) => {
        const comma = part.indexOf(',');
        return comma === -1 ? part : part.slice(comma + 1);
    }).filter(Boolean);

    if (!candidates.some((sig) => timingSafeEqualB64(sig, expected))) {
        throw new Error('Resend webhook signature mismatch');
    }

    return JSON.parse(rawBody);
}

export async function applyLicenseEmailDelivery(db, emailId, delivery, { orderId } = {}) {
    const id = String(emailId || '').trim();
    const fallbackOrderId = String(orderId || '').trim();
    if (!delivery || (!id && !fallbackOrderId)) return { updated: false };

    let row = null;
    if (id) {
        row = await db.prepare(
            'SELECT id, license_email_delivery, license_email_resend_id FROM orders WHERE license_email_resend_id = ?'
        ).bind(id).first();
    }
    if (!row && fallbackOrderId) {
        row = await db.prepare(
            'SELECT id, license_email_delivery, license_email_resend_id FROM orders WHERE id = ?'
        ).bind(fallbackOrderId).first();
        if (row?.license_email_resend_id && id && row.license_email_resend_id !== id) {
            return { updated: false, skipped: 'other_email', orderId: row.id };
        }
    }
    if (!row) return { updated: false, skipped: 'unknown_email' };

    const nextDelivery = shouldUpgradeDelivery(row.license_email_delivery, delivery)
        ? delivery
        : (row.license_email_delivery || delivery);
    const fillResendId = Boolean(id && !row.license_email_resend_id);
    if (!shouldUpgradeDelivery(row.license_email_delivery, delivery) && !fillResendId) {
        return { updated: false, skipped: 'rank', orderId: row.id };
    }

    const ts = now();
    await db.prepare(`
        UPDATE orders
        SET license_email_delivery = ?,
            license_email_resend_id = COALESCE(license_email_resend_id, ?),
            updated_at = ?
        WHERE id = ?
    `).bind(nextDelivery, id || null, ts, row.id).run();
    return { updated: true, orderId: row.id };
}
