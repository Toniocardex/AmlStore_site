/**
 * Percorso pubblico immagine catalogo: solo sotto /img/products/ (anti path traversal).
 * I file vanno committati nel repo sotto `img/products/` e pubblicati con il deploy Pages.
 * @param {unknown} v
 * @returns {string | null}
 */
export function normalizeCoverImagePath(v) {
  if (typeof v !== 'string') return null;
  const s = v.trim();
  if (!s) return null;
  if (!s.startsWith('/img/products/')) return null;
  if (s.includes('..') || s.includes('\\') || s.includes('\0')) return null;
  if (s.length > 512) return null;
  return s;
}
