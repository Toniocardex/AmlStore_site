/**
 * Autenticazione API admin: Bearer ADMIN_API_SECRET (Pages / Workers env).
 * Cloudflare Access protegge l’HTML in /admin/; questo segrega le mutazioni su D1/R2.
 */

/**
 * @param {Request} request
 */
function getBearer(request) {
  const h = request.headers.get('Authorization') || '';
  const m = /^Bearer\s+(.+)$/i.exec(h.trim());
  return m ? m[1].trim() : '';
}

/**
 * @param {string} a
 * @param {string} b
 */
async function digestEqual(a, b) {
  const enc = new TextEncoder();
  const aa = await crypto.subtle.digest('SHA-256', enc.encode(a));
  const bb = await crypto.subtle.digest('SHA-256', enc.encode(b));
  return crypto.subtle.timingSafeEqual(aa, bb);
}

/**
 * @param {Request} request
 * @param {{ ADMIN_API_SECRET?: string }} env
 * @returns {Promise<Response | null>} Response di errore oppure null se autorizzato
 */
export async function assertAdmin(request, env) {
  const secret = typeof env.ADMIN_API_SECRET === 'string' ? env.ADMIN_API_SECRET.trim() : '';
  if (!secret) {
    return Response.json(
      {
        error: 'admin_not_configured',
        message:
          'Imposta il secret Pages ADMIN_API_SECRET (stesso valore usato nel CMS) oppure disabilita le route admin.',
      },
      { status: 503, headers: { 'cache-control': 'no-store' } }
    );
  }

  const bearer = getBearer(request);
  if (!bearer || !(await digestEqual(bearer, secret))) {
    return Response.json({ error: 'unauthorized' }, { status: 401, headers: { 'cache-control': 'no-store' } });
  }

  return null;
}

/**
 * @param {Request} request
 */
export function clientIp(request) {
  return request.headers.get('CF-Connecting-IP') || request.headers.get('X-Forwarded-For') || '';
}
