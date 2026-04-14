/**
 * PATCH /api/admin/products/:id
 * Aggiornamento parziale campi prodotto (whitelist).
 */
import { writeAudit } from '../../../lib/audit.js';
import { normalizeCoverImagePath } from '../../../lib/cover-image.js';
import { ensureUniqueProductSlug, isReservedStoreProductSlug, slugify } from '../../../lib/slug.js';

/** @param {unknown} v */
function str(v) {
  return typeof v === 'string' ? v.trim() : '';
}

/**
 * @param {{ env: unknown, request: Request, params: Record<string, string> }} ctx
 */
export async function onRequestPatch(ctx) {
  const { request, env, params } = ctx;
  if (!env.DB) {
    return Response.json(
      { error: 'database_unconfigured', message: 'Binding D1 (DB) mancante.' },
      { status: 500, headers: { 'cache-control': 'no-store' } }
    );
  }

  const id = Number.parseInt(String(params.id || ''), 10);
  if (!Number.isFinite(id) || id <= 0) {
    return Response.json({ error: 'invalid_id' }, { status: 400, headers: { 'cache-control': 'no-store' } });
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
  const existing = await env.DB.prepare('SELECT id, slug FROM products WHERE id = ?').bind(id).first();
  if (!existing) {
    return Response.json({ error: 'not_found' }, { status: 404, headers: { 'cache-control': 'no-store' } });
  }

  const sets = [];
  const values = [];

  const maybeStr = (key, col) => {
    if (!(key in o)) return;
    sets.push(`${col} = ?`);
    values.push(str(o[key]));
  };

  maybeStr('title_it', 'title_it');
  maybeStr('title_en', 'title_en');
  maybeStr('title_de', 'title_de');
  maybeStr('title_fr', 'title_fr');
  maybeStr('title_es', 'title_es');
  maybeStr('description_it', 'description_it');
  maybeStr('description_en', 'description_en');
  maybeStr('description_de', 'description_de');
  maybeStr('description_fr', 'description_fr');
  maybeStr('description_es', 'description_es');

  if ('price_cents' in o) {
    const raw = o.price_cents;
    const n =
      typeof raw === 'number' && Number.isFinite(raw)
        ? Math.floor(raw)
        : Number.parseInt(String(raw ?? ''), 10);
    if (!Number.isFinite(n) || n < 0) {
      return Response.json({ error: 'invalid_price_cents' }, { status: 400, headers: { 'cache-control': 'no-store' } });
    }
    sets.push('price_cents = ?');
    values.push(n);
  }

  if ('currency' in o) {
    sets.push('currency = ?');
    values.push(str(o.currency) || 'EUR');
  }

  if ('fulfillment' in o) {
    const f = str(o.fulfillment).toLowerCase();
    sets.push('fulfillment = ?');
    values.push(f === 'physical' ? 'physical' : 'digital');
  }

  if ('active' in o) {
    const a = o.active === false || o.active === 0 || o.active === '0' || o.active === 'false' ? 0 : 1;
    sets.push('active = ?');
    values.push(a);
  }

  if ('sort_order' in o) {
    const raw = o.sort_order;
    if (raw === null || raw === '' || raw === undefined) {
      sets.push('sort_order = NULL');
    } else {
      const n = Number.parseInt(String(raw), 10);
      if (!Number.isFinite(n)) {
        return Response.json({ error: 'invalid_sort_order' }, { status: 400, headers: { 'cache-control': 'no-store' } });
      }
      sets.push('sort_order = ?');
      values.push(n);
    }
  }

  if ('r2_key' in o) {
    const rk = o.r2_key;
    if (rk === null || rk === '') {
      sets.push('r2_key = NULL');
    } else {
      sets.push('r2_key = ?');
      values.push(str(rk));
    }
  }

  if ('cover_image' in o) {
    const raw = o.cover_image;
    if (raw === null || raw === '') {
      sets.push('cover_image = NULL');
    } else {
      const ck = normalizeCoverImagePath(raw);
      if (!ck) {
        return Response.json(
          {
            error: 'invalid_cover_image',
            message: 'Usa un path che inizi con /img/products/ (file statico nel deploy).',
          },
          { status: 400, headers: { 'cache-control': 'no-store' } }
        );
      }
      sets.push('cover_image = ?');
      values.push(ck);
    }
  }

  if ('slug' in o) {
    let next = slugify(str(o.slug));
    if (!next) next = slugify(String(existing.slug));
    const clash = await env.DB.prepare('SELECT id FROM products WHERE slug = ? AND id != ? LIMIT 1')
      .bind(next, id)
      .first();
    if (clash) {
      next = await ensureUniqueProductSlug(env, next);
    } else if (isReservedStoreProductSlug(next)) {
      return Response.json(
        {
          error: 'reserved_slug',
          message:
            'Questo slug coincide con una pagina del sito (es. carrello, checkout). Scegline un altro.',
        },
        { status: 400, headers: { 'cache-control': 'no-store' } }
      );
    }
    sets.push('slug = ?');
    values.push(next);
  }

  if (sets.length === 0) {
    return Response.json({ error: 'empty_patch' }, { status: 400, headers: { 'cache-control': 'no-store' } });
  }

  const sql = `UPDATE products SET ${sets.join(', ')} WHERE id = ?`;
  values.push(id);

  try {
    await env.DB.prepare(sql).bind(...values).run();
    await writeAudit(env, {
      action: 'product_patch',
      subject_type: 'product',
      subject_id: String(id),
      meta: { fields: sets.slice(0, -1) },
      request,
    });
    const row = await env.DB.prepare('SELECT * FROM products WHERE id = ?').bind(id).first();
    return Response.json(
      { product: row },
      { headers: { 'cache-control': 'no-store', 'content-type': 'application/json; charset=utf-8' } }
    );
  } catch (e) {
    return Response.json(
      { error: 'update_failed', message: e instanceof Error ? e.message : 'Errore D1' },
      { status: 500, headers: { 'cache-control': 'no-store' } }
    );
  }
}
