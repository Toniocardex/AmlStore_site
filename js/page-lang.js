'use strict';

/** Lingue UI (allineate a cartelle /it /en /de /fr /es). */
const PAGE_LANGS = /** @type {const} */ (['it', 'en', 'de', 'fr', 'es']);

/**
 * @returns {'it'|'en'|'de'|'fr'|'es'}
 */
export function pageLang() {
  const raw = document.documentElement.getAttribute('lang') || 'it';
  const p = raw.trim().toLowerCase().slice(0, 2);
  return /** @type {'it'|'en'|'de'|'fr'|'es'} */ (
    PAGE_LANGS.includes(/** @type {*} */ (p)) ? p : 'it'
  );
}

/**
 * @param {'it'|'en'|'de'|'fr'|'es'} lang
 */
export function moneyLocale(lang) {
  const map = {
    it: 'it-IT',
    en: 'en-US',
    de: 'de-DE',
    fr: 'fr-FR',
    es: 'es-ES',
  };
  return map[lang] || 'en-US';
}
