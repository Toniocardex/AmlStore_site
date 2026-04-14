/**
 * GET  /api/admin/products — catalogo completo (anche inattivi) per La Cassaforte.
 * POST /api/admin/products — crea prodotto su D1 (slug opzionale, generato da titolo IT).
 */
import { writeAudit } from '../../lib/audit.js';
import { normalizeCoverImagePath } from '../../lib/cover-image.js';
import { ensureUniqueProductSlug, slugify } from '../../lib/slug.js';

/** @param {unknown} v */
function str(v) {
  return typeof v === 'string' ? v.trim() : '';
}

/** @param {Record<string, unknown>} body */
function normalizeTitles(body) {
  const it = str(body.title_it);
  const en = str(body.title_en);
  const fr = str(body.title_fr);
  const de = str(body.title_de);
  const es = str(body.title_es);
  return {
    title_it: it || en || 'Prodotto',
    title_en: en || it || 'Product',
    title_fr: fr || en || it || 'Produit',
    title_de: de || en || it || 'Produkt',
    title_es: es || en || it || 'Producto',
  };
}

/** @param {Record<string, unknown>} body */
function normalizeDescriptions(body) {
  const single = str(body.description);
  const di = str(body.description_it) || single;
  const dEn = str(body.description_en) || single;
  const dFr = str(body.description_fr) || single;
  const dDe = str(body.description_de) || single;
  const dEs = str(body.description_es) || single;
  return {
    description_it: di,
    description_en: dEn,
    description_de: dDe,
    description_fr: dFr,
    description_es: dEs,
  };
}

export async function onRequestGet({ request, env }) {
  if (!env.DB) {
    return Response.json(
      { error: 'database_unconfigured', message: 'Binding D1 (DB) mancante.' },
      { status: 500, headers: { 'cache-control': 'no-store' } }
    );
  }

  const sql = `
    SELECT
      id,
      slug,
      title_it, title_en, title_de, title_fr, title_es,
      description_it, description_en, description_de, description_fr, description_es,
      price_cents,
      currency,
      cover_image,
      r2_key,
      active,
      fulfillment,
      sort_order,
      created_at
    FROM products
    ORDER BY COALESCE(sort_order, 2147483647), id
  `;

  try {
    const { results } = await env.DB.prepare(sql).all();
    return Response.json(
      { products: results ?? [] },
      { headers: { 'cache-control': 'no-store', 'content-type': 'application/json; charset=utf-8' } }
    );
  } catch (e) {
    return Response.json(
      { error: 'query_failed', message: e instanceof Error ? e.message : 'Errore D1' },
      { status: 500, headers: { 'cache-control': 'no-store' } }
    );
  }
}

export async function onRequestPost({ request, env }) {
  if (!env.DB) {
    return Response.json(
      { error: 'database_unconfigured', message: 'Binding D1 (DB) mancante.' },
      { status: 500, headers: { 'cache-control': 'no-store' } }
    );
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return Response.json({ error: 'invalid_json' }, { status: 400, headers: { 'cache-control': 'no-store' } });
  }

  if (!body || typeof body !== 'object') {
    return Response.json({ error: 'invalid_body' }, { status: 400, headers: { 'cache-control': 'no-store' } });
  }

  const o = /** @type {Record<string, unknown>} */ (body);
  const titles = normalizeTitles(o);
  const descriptions = normalizeDescriptions(o);

  const priceRaw = o.price_cents;
  const price_cents =
    typeof priceRaw === 'number' && Number.isFinite(priceRaw)
      ? Math.max(0, Math.floor(priceRaw))
      : Number.parseInt(String(priceRaw ?? ''), 10);
  if (!Number.isFinite(price_cents) || price_cents < 0) {
    return Response.json({ error: 'invalid_price_cents' }, { status: 400, headers: { 'cache-control': 'no-store' } });
  }

  const currency = str(o.currency) || 'EUR';
  const rawFul = str(o.fulfillment).toLowerCase();
  const fulfillment = rawFul === 'physical' ? 'physical' : 'digital';

  const active =
    o.active === false || o.active === 0 || o.active === '0' || o.active === 'false' ? 0 : 1;

  const sortRaw = o.sort_order;
  const sort_order =
    sortRaw === null || sortRaw === undefined || sortRaw === ''
      ? null
      : Number.isFinite(Number(sortRaw))
        ? Math.floor(Number(sortRaw))
        : null;

  const slugInput = str(o.slug);
  const baseSlug = slugInput ? slugify(slugInput) : slugify(titles.title_it);
  const slug = await ensureUniqueProductSlug(env, baseSlug);

  const coverRaw = o.cover_image;
  const cover_image =
    coverRaw === undefined || coverRaw === null || coverRaw === ''
      ? null
      : normalizeCoverImagePath(coverRaw);
  if (coverRaw !== undefined && coverRaw !== null && String(coverRaw).trim() && !cover_image) {
    return Response.json(
      { error: 'invalid_cover_image', message: 'Usa un path che inizi con /img/products/ (file nel repo, deploy Pages).' },
      { status: 400, headers: { 'cache-control': 'no-store' } }
    );
  }

  try {
    const stmt = env.DB.prepare(
      `INSERT INTO products (
        slug,
        title_it, title_en, title_de, title_fr, title_es,
        description_it, description_en, description_de, description_fr, description_es,
        price_cents, currency, cover_image, r2_key, active, fulfillment, sort_order
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?)`
    );

    const run = await stmt
      .bind(
        slug,
        titles.title_it,
        titles.title_en,
        titles.title_de,
        titles.title_fr,
        titles.title_es,
        descriptions.description_it,
        descriptions.description_en,
        descriptions.description_de,
        descriptions.description_fr,
        descriptions.description_es,
        price_cents,
        currency,
        cover_image,
        active,
        fulfillment,
        sort_order
      )
      .run();

    const id = run.meta?.last_row_id;
    if (!id) {
      return Response.json({ error: 'insert_failed' }, { status: 500, headers: { 'cache-control': 'no-store' } });
    }

    await writeAudit(env, {
      action: 'product_create',
      subject_type: 'product',
      subject_id: String(id),
      meta: { slug, price_cents, currency, fulfillment, active: Boolean(active) },
      request,
    });

    const row = await env.DB.prepare('SELECT * FROM products WHERE id = ?').bind(id).first();

    return Response.json(
      { product: row },
      { status: 201, headers: { 'cache-control': 'no-store', 'content-type': 'application/json; charset=utf-8' } }
    );
  } catch (e) {
    return Response.json(
      {
        error: 'insert_error',
        message: e instanceof Error ? e.message : 'Errore D1',
      },
      { status: 500, headers: { 'cache-control': 'no-store' } }
    );
  }
}
