/**
 * GET /api/products?lang=it|en|de|fr|es
 * Legge il catalogo pubblico (HOME) da D1 — solo prodotti attivi.
 */
import { normalizeLang, SQL_DESCRIPTION, SQL_TITLE } from '../lib/product-i18n.js';

export async function onRequestGet({ request, env }) {
  if (!env.DB) {
    return Response.json(
      { error: 'database_unconfigured', message: 'Binding D1 (DB) mancante.' },
      { status: 500 }
    );
  }

  const url = new URL(request.url);
  const lang = normalizeLang(url.searchParams.get('lang'));

  const sql = `
    SELECT
      id,
      slug,
      ${SQL_TITLE} AS title,
      ${SQL_DESCRIPTION} AS description,
      price_cents,
      currency,
      cover_image,
      fulfillment
    FROM products
    WHERE active = 1
    ORDER BY COALESCE(sort_order, 2147483647), id
  `;

  try {
    const stmt = env.DB.prepare(sql).bind(lang);
    const { results } = await stmt.all();
    return Response.json(
      {
        lang,
        products: results ?? [],
      },
      {
        headers: {
          'cache-control': 'public, max-age=60',
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
