import { assertAdmin } from '../../lib/admin-auth.js';

export async function onRequest(context) {
  const denied = await assertAdmin(context.request, context.env);
  if (denied) return denied;
  return context.next();
}
