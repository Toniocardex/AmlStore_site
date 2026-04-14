/**
 * POST /api/order-draft
 * Crea ordine in D1 (status pending_checkout) + righe, prezzi solo da D1.
 * Body: { lang, email, billing: {...}, items: [{ slug, qty }] }
 */

import { normalizeLang, pickTitle } from '../lib/product-i18n.js';

const SDI_LEN = 7;

/**
 * @param {unknown} b
 * @param {{ needsShipping: boolean }} ctx
 */
function validateBilling(b, ctx) {
  const err = [];
  if (!b || typeof b !== 'object') {
    err.push('billing_required');
    return err;
  }
  const o = /** @type {Record<string, unknown>} */ (b);
  const str = (k) => (typeof o[k] === 'string' ? o[k].trim() : '');

  const isCompany = str('invoice_type') === 'company';
  const addressRequired = ctx.needsShipping || isCompany;
  if (addressRequired) {
    if (!str('street')) err.push('street');
    if (!str('postal_code')) err.push('postal_code');
    if (!str('city')) err.push('city');
    if (!str('country')) err.push('country');
  }

  if (!str('first_name')) err.push('first_name');
  if (!str('last_name')) err.push('last_name');

  const inv = isCompany ? 'company' : 'individual';
  if (inv === 'company') {
    if (!str('company_name')) err.push('company_name');
    if (!str('vat_id')) err.push('vat_id');
    const sdi = str('sdi_code').toUpperCase();
    if (sdi.length !== SDI_LEN || !/^[A-Z0-9]{7}$/.test(sdi)) {
      err.push('sdi_code');
    }
    const pec = str('pec');
    if (sdi === '0000000') {
      if (!pec || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(pec)) err.push('pec');
    } else if (pec && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(pec)) {
      err.push('pec_format');
    }
  }

  return err;
}

function mergeItems(rawItems) {
  const merged = new Map();
  if (!Array.isArray(rawItems)) return merged;
  for (const row of rawItems) {
    if (!row || typeof row.slug !== 'string' || !row.slug.trim()) continue;
    const slug = row.slug.trim();
    const q = Math.min(99, Math.max(1, Math.floor(Number(row.qty) || 1)));
    merged.set(slug, (merged.get(slug) || 0) + q);
  }
  return merged;
}

export async function onRequestPost({ request, env }) {
  if (!env.DB) {
    return Response.json(
      { error: 'database_unconfigured', message: 'Binding D1 (DB) mancante.' },
      { status: 500 }
    );
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return Response.json({ error: 'invalid_json' }, { status: 400 });
  }

  const lang = normalizeLang(body?.lang);
  const email = typeof body?.email === 'string' ? body.email.trim() : '';
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return Response.json({ error: 'invalid_email' }, { status: 400 });
  }

  const merged = mergeItems(body?.items);
  if (merged.size === 0) {
    return Response.json({ error: 'empty_cart' }, { status: 400 });
  }

  const slugs = [...merged.keys()];
  const ph = slugs.map(() => '?').join(', ');
  const sql = `
    SELECT id, slug, title_it, title_en, title_de, title_fr, title_es, price_cents, currency, fulfillment
    FROM products
    WHERE active = 1 AND slug IN (${ph})
  `;

  try {
    const { results } = await env.DB.prepare(sql).bind(...slugs).all();
    const bySlug = new Map((results ?? []).map((r) => [r.slug, r]));

    const needsShipping = (results ?? []).some((r) => {
      const f = typeof r.fulfillment === 'string' ? r.fulfillment.trim().toLowerCase() : '';
      return f === 'physical';
    });

    const billErr = validateBilling(body?.billing, { needsShipping });
    if (billErr.length) {
      return Response.json({ error: 'invalid_billing', fields: billErr }, { status: 400 });
    }

    const lines = [];
    let total_cents = 0;
    let currency = 'EUR';

    for (const slug of slugs) {
      const row = bySlug.get(slug);
      if (!row) {
        return Response.json({ error: 'unknown_slug', slug }, { status: 400 });
      }
      const qty = merged.get(slug);
      const title_snapshot = pickTitle(row, lang);
      lines.push({
        product_id: row.id,
        slug,
        title_snapshot,
        qty,
        unit_price_cents: row.price_cents,
        currency: row.currency,
      });
      total_cents += row.price_cents * qty;
      currency = row.currency;
    }

    const rawBill = body.billing && typeof body.billing === 'object' ? body.billing : {};
    const billing = { ...rawBill, cart_needs_shipping: needsShipping };
    const billing_json = JSON.stringify(billing);
    const cart_token = crypto.randomUUID();

    const insOrder = env.DB
      .prepare(
        `INSERT INTO orders (cart_token, status, lang, billing_json, customer_email, total_cents, currency, updated_at)
         VALUES (?, 'pending_checkout', ?, ?, ?, ?, ?, datetime('now'))`
      )
      .bind(cart_token, lang, billing_json, email, total_cents, currency);

    const runResult = await insOrder.run();
    const order_id = runResult.meta?.last_row_id;
    if (!order_id) {
      return Response.json({ error: 'insert_failed' }, { status: 500 });
    }

    const stmts = lines.map((ln) =>
      env.DB
        .prepare(
          `INSERT INTO order_lines (order_id, product_id, slug, title_snapshot, qty, unit_price_cents, currency)
           VALUES (?, ?, ?, ?, ?, ?, ?)`
        )
        .bind(
          order_id,
          ln.product_id,
          ln.slug,
          ln.title_snapshot,
          ln.qty,
          ln.unit_price_cents,
          ln.currency
        )
    );

    await env.DB.batch(stmts);

    return Response.json(
      {
        order_id,
        status: 'pending_checkout',
        total_cents,
        currency,
      },
      {
        headers: {
          'cache-control': 'no-store',
          'content-type': 'application/json; charset=utf-8',
        },
      }
    );
  } catch (e) {
    return Response.json(
      {
        error: 'order_failed',
        message: e instanceof Error ? e.message : 'Errore D1',
      },
      { status: 500 }
    );
  }
}
