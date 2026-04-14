/**
 * GET /api/admin/orders?limit=50
 * Lista ordini da D1 (area proprietario / La Cassaforte).
 */

export async function onRequestGet({ request, env }) {
  if (!env.DB) {
    return Response.json(
      { error: 'database_unconfigured', message: 'Binding D1 (DB) mancante.' },
      { status: 500, headers: { 'cache-control': 'no-store' } }
    );
  }

  const url = new URL(request.url);
  const lim = Math.min(200, Math.max(1, Number.parseInt(url.searchParams.get('limit') || '50', 10) || 50));

  const sql = `
    SELECT
      id,
      cart_token,
      status,
      lang,
      customer_email,
      total_cents,
      currency,
      stripe_session_id,
      created_at,
      updated_at
    FROM orders
    ORDER BY id DESC
    LIMIT ?
  `;

  try {
    const { results } = await env.DB.prepare(sql).bind(lim).all();
    return Response.json(
      { orders: results ?? [] },
      { headers: { 'cache-control': 'no-store', 'content-type': 'application/json; charset=utf-8' } }
    );
  } catch (e) {
    return Response.json(
      { error: 'query_failed', message: e instanceof Error ? e.message : 'Errore D1' },
      { status: 500, headers: { 'cache-control': 'no-store' } }
    );
  }
}
