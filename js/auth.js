'use strict';

/**
 * Area account (scheletro). Integrazione futura es. Clerk o sessione server-only.
 * Nessuna dipendenza esterna in questa fase.
 */

/** @typedef {{ email?: string, subject?: string }} SessionLike */

/**
 * @returns {Promise<SessionLike | null>}
 */
export async function getSession() {
  return null;
}

export function isAuthenticated() {
  return false;
}

export async function signOut() {
  // no-op finché non c’è provider auth
}

const PREFIX = {
  it: '/it',
  en: '/en',
  de: '/de',
  fr: '/fr',
  es: '/es',
};

/**
 * URL verso cui mandare l’utente non autenticato (relativo alla lingua).
 * @param {string} returnUrl pathname + search
 * @param {'it'|'en'|'de'|'fr'|'es'} [lang]
 */
export function signInUrl(returnUrl, lang = 'it') {
  const p = PREFIX[/** @type {keyof typeof PREFIX} */ (lang)] || PREFIX.it;
  const q = encodeURIComponent(returnUrl || `${p}/`);
  return `${p}/account.html?signin=1&return=${q}`;
}
