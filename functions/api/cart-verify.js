/**
 * POST /api/cart-verify
 * Body JSON: { lang?: "it"|"en"|"de"|"fr"|"es", items: [{ slug, qty }] }
 * Ricalcola prezzi e titoli da D1 (fonte di verità). Unisce righe duplicate per slug.
 */
import { normalizeLang, pickTitle } from '../lib/product-i18n.js';

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
  const rawItems = body?.items;
  if (!Array.isArray(rawItems) || rawItems.length === 0) {
    return Response.json({ error: 'empty_cart' }, { status: 400 });
  }

  const merged = new Map();
  for (const row of rawItems) {
    if (!row || typeof row.slug !== 'string' || !row.slug.trim()) continue;
    const slug = row.slug.trim();
    const q = Math.min(99, Math.max(1, Math.floor(Number(row.qty) || 1)));
    merged.set(slug, (merged.get(slug) || 0) + q);
  }

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
    const stmt = env.DB.prepare(sql).bind(...slugs);
    const { results } = await stmt.all();
    const bySlug = new Map((results ?? []).map((r) => [r.slug, r]));

    const lines = [];
    let total_cents = 0;
    let currency = 'EUR';

    for (const slug of slugs) {
      const row = bySlug.get(slug);
      if (!row) {
        return Response.json({ error: 'unknown_slug', slug }, { status: 400 });
      }
      const qty = merged.get(slug);
      const title = pickTitle(row, lang);
      const rawFul = typeof row.fulfillment === 'string' ? row.fulfillment.trim().toLowerCase() : '';
      const fulfillment = rawFul === 'physical' ? 'physical' : 'digital';
      lines.push({
        slug,
        title,
        price_cents: row.price_cents,
        currency: row.currency,
        qty,
        fulfillment,
      });
      total_cents += row.price_cents * qty;
      currency = row.currency;
    }

    const needs_shipping = lines.some((l) => l.fulfillment === 'physical');
    const has_digital = lines.some((l) => l.fulfillment === 'digital');

    return Response.json(
      { lang, lines, total_cents, currency, needs_shipping, has_digital },
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
        error: 'query_failed',
        message: e instanceof Error ? e.message : 'Errore D1',
      },
      { status: 500 }
    );
  }
}
