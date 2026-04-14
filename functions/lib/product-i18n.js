/** Lingue storefront / ordine (ISO 639-1, cartelle URL). */
const PRODUCT_LANGS = /** @type {const} */ ([
  'it',
  'en',
  'de',
  'fr',
  'es',
]);

/**
 * @param {unknown} raw
 * @returns {'it'|'en'|'de'|'fr'|'es'}
 */
export function normalizeLang(raw) {
  const s = typeof raw === 'string' ? raw.trim().toLowerCase().slice(0, 2) : '';
  return /** @type {'it'|'en'|'de'|'fr'|'es'} */ (
    PRODUCT_LANGS.includes(/** @type {*} */ (s)) ? s : 'it'
  );
}

/** @param {Record<string, unknown>} row */
export function pickTitle(row, lang) {
  switch (lang) {
    case 'en':
      return String(row.title_en ?? '');
    case 'de':
      return String(row.title_de ?? '');
    case 'fr':
      return String(row.title_fr ?? '');
    case 'es':
      return String(row.title_es ?? '');
    default:
      return String(row.title_it ?? '');
  }
}

/** Espressioni SQL per SELECT (bind ?1 = lang). */
export const SQL_TITLE = `
  CASE ?1
    WHEN 'it' THEN title_it
    WHEN 'en' THEN title_en
    WHEN 'de' THEN title_de
    WHEN 'fr' THEN title_fr
    WHEN 'es' THEN title_es
    ELSE title_it
  END
`;

export const SQL_DESCRIPTION = `
  CASE ?1
    WHEN 'it' THEN description_it
    WHEN 'en' THEN description_en
    WHEN 'de' THEN description_de
    WHEN 'fr' THEN description_fr
    WHEN 'es' THEN description_es
    ELSE description_it
  END
`;
