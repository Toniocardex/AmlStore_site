/**
 * Nomi file riservati nella **root** `/{lang}/{nome}.html` (pagine storefront statiche).
 * Le schede prodotto vivono in `/{lang}/products/{slug}.html`; uno slug uguale a questi nomi
 * in root creerebbe conflitto: vietato in admin e nel build.
 */
export const RESERVED_STORE_PRODUCT_SLUGS = new Set([
  'index',
  'cart',
  'checkout',
  'account',
  'order-success',
  'p', // legacy /{lang}/p/
]);

/** @param {string} slug */
export function isReservedStoreProductSlug(slug) {
  return RESERVED_STORE_PRODUCT_SLUGS.has(String(slug || '').trim().toLowerCase());
}

/**
 * Slug URL-safe per prodotti (allineato a slug in schema.sql).
 * @param {string} input
 */
export function slugify(input) {
  const s = String(input || '')
    .normalize('NFKD')
    .replace(/\p{M}/gu, '')
    .toLowerCase();
  const out = s
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 96);
  return out || 'item';
}

/**
 * @param {string} name
 */
export function safeFilename(name) {
  const base = String(name || '').replace(/[/\\]/g, '');
  return base.replace(/[^\w.\-()+ ]/g, '_').slice(0, 180) || 'file.bin';
}

/**
 * @param {unknown} env
 * @param {string} base
 */
export async function ensureUniqueProductSlug(env, base) {
  const db = /** @type {{ prepare: Function }} */ (env).DB;
  let slug = slugify(base);
  for (let i = 0; i < 50; i += 1) {
    const candidate = i === 0 ? slug : `${slug}-${i + 1}`;
    if (isReservedStoreProductSlug(candidate)) continue;
    const row = await db.prepare('SELECT 1 AS ok FROM products WHERE slug = ? LIMIT 1').bind(candidate).first();
    if (!row) return candidate;
  }
  let fallback = `${slug}-${crypto.randomUUID().slice(0, 8)}`;
  while (isReservedStoreProductSlug(fallback)) {
    fallback = `${slug}-${crypto.randomUUID().slice(0, 8)}`;
  }
  return fallback;
}
