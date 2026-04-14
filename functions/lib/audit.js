import { clientIp } from './admin-auth.js';

/**
 * @param {unknown} env
 * @param {{
 *   action: string;
 *   actor?: string;
 *   subject_type?: string;
 *   subject_id?: string;
 *   meta?: unknown;
 *   request?: Request;
 * }} row
 */
export async function writeAudit(env, row) {
  const db = /** @type {{ prepare: Function }} */ (env).DB;
  if (!db) return;
  const ip = row.request ? clientIp(row.request) : '';
  const meta_json =
    row.meta === undefined || row.meta === null ? null : JSON.stringify(row.meta);
  try {
    await db
      .prepare(
        `INSERT INTO admin_audit_logs (action, actor, subject_type, subject_id, meta_json, client_ip)
         VALUES (?, ?, ?, ?, ?, ?)`
      )
      .bind(
        row.action,
        row.actor ?? 'admin_bearer',
        row.subject_type ?? null,
        row.subject_id ?? null,
        meta_json,
        ip || null
      )
      .run();
  } catch {
    /* audit non deve bloccare il flusso principale */
  }
}
