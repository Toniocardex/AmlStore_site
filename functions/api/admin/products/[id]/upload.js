/**
 * POST /api/admin/products/:id/upload
 * multipart/form-data: campo "file" — salva su R2 (binding VAULT) e aggiorna products.r2_key.
 */
import { writeAudit } from '../../../../lib/audit.js';
import { safeFilename } from '../../../../lib/slug.js';

/**
 * @param {unknown} env
 */
function maxBytes(env) {
  const raw = /** @type {{ ADMIN_UPLOAD_MAX_BYTES?: string }} */ (env).ADMIN_UPLOAD_MAX_BYTES;
  const n = Number.parseInt(String(raw || ''), 10);
  if (Number.isFinite(n) && n > 0) return Math.min(n, 250 * 1024 * 1024);
  return 50 * 1024 * 1024;
}

/**
 * @param {{ env: unknown, request: Request, params: Record<string, string> }} ctx
 */
export async function onRequestPost(ctx) {
  const { request, env, params } = ctx;
  const vault = env.VAULT;
  if (!vault) {
    return Response.json(
      {
        error: 'r2_unconfigured',
        message: 'Binding R2 (VAULT) non configurato: decommentare r2_buckets in wrangler.toml e ridistribuire.',
      },
      { status: 501, headers: { 'cache-control': 'no-store' } }
    );
  }

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

  const row = await env.DB.prepare('SELECT id FROM products WHERE id = ?').bind(id).first();
  if (!row) {
    return Response.json({ error: 'not_found' }, { status: 404, headers: { 'cache-control': 'no-store' } });
  }

  let form;
  try {
    form = await request.formData();
  } catch {
    return Response.json({ error: 'invalid_multipart' }, { status: 400, headers: { 'cache-control': 'no-store' } });
  }

  const file = form.get('file');
  if (!(file instanceof File) || file.size <= 0) {
    return Response.json({ error: 'missing_file' }, { status: 400, headers: { 'cache-control': 'no-store' } });
  }

  const cap = maxBytes(env);
  if (file.size > cap) {
    return Response.json({ error: 'file_too_large', max_bytes: cap }, { status: 413, headers: { 'cache-control': 'no-store' } });
  }

  const name = safeFilename(file.name);
  const key = `vault/products/${id}/${name}`;

  try {
    await vault.put(key, file.stream(), {
      httpMetadata: { contentType: file.type || 'application/octet-stream' },
    });

    await env.DB.prepare('UPDATE products SET r2_key = ? WHERE id = ?').bind(key, id).run();

    await writeAudit(env, {
      action: 'product_upload',
      subject_type: 'product',
      subject_id: String(id),
      meta: { r2_key: key, size: file.size },
      request,
    });

    const product = await env.DB.prepare('SELECT id, slug, r2_key FROM products WHERE id = ?').bind(id).first();

    return Response.json(
      { ok: true, r2_key: key, product },
      { headers: { 'cache-control': 'no-store', 'content-type': 'application/json; charset=utf-8' } }
    );
  } catch (e) {
    return Response.json(
      { error: 'upload_failed', message: e instanceof Error ? e.message : 'Errore R2' },
      { status: 500, headers: { 'cache-control': 'no-store' } }
    );
  }
}
