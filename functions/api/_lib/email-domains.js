/**
 * Blocco domini email usa-e-getta.
 *
 * Nasce da un caso reale: in tre settimane 61 degli 80 carrelli con email
 * provenivano da quattro domini temporanei, con timestamp a un minuto esatto di
 * distanza e sempre lo stesso importo alto — card testing, non clienti. Nessuno
 * di quei tentativi e' diventato un ordine pagato, ma inquinavano i dati di
 * carrello e consumavano tentativi di pagamento.
 *
 * La lista e' volutamente CORTA e basata su evidenza, non una delle liste da
 * decine di migliaia di voci che si trovano in giro: un falso positivo qui
 * costa una vendita, e su un negozio con pochi ordini al giorno pesa piu' del
 * rumore che eviterebbe.
 *
 * NON vanno inseriti i servizi di inoltro per la privacy usati da clienti veri
 * (proton.me, duck.com, icloud/hide-my-email, simplelogin, anonaddy): sono
 * indirizzi permanenti di persone reali, non caselle a perdere.
 *
 * Per aggiungere domini senza un deploy si usa la variabile d'ambiente
 * BLOCKED_EMAIL_DOMAINS (lista separata da virgole).
 */

/** Domini osservati negli attacchi + temp-mail notoriamente usa-e-getta. */
const BUILTIN_BLOCKED_DOMAINS = new Set([
    // Osservati direttamente sul negozio (agosto 2026)
    'analismail.com',
    'blackfirsta.com',
    'ishowfirstmail.com',
    'firsthidden.com',
    // Temp-mail diffusi
    'mailinator.com',
    'guerrillamail.com',
    'yopmail.com',
    '10minutemail.com',
    'tempmail.com',
    'temp-mail.org',
    'throwawaymail.com',
    'trashmail.com',
    'sharklasers.com',
    'getnada.com',
    'dispostable.com',
    'maildrop.cc',
    'fakeinbox.com',
    'mohmal.com',
    'emailondeck.com',
]);

/** Domini extra da env, per reagire a un attacco senza aspettare un deploy. */
function extraBlockedDomains(env) {
    const raw = String(env?.BLOCKED_EMAIL_DOMAINS || '').trim();
    if (!raw) return null;
    const list = raw
        .split(',')
        .map((d) => d.trim().toLowerCase())
        .filter(Boolean);
    return list.length ? new Set(list) : null;
}

/**
 * Dominio di un'email, gia' normalizzato.
 * Ritorna '' se l'indirizzo non ha una forma utilizzabile: la validazione del
 * formato resta a chi chiama, qui non si duplica.
 */
export function emailDomain(email) {
    const at = String(email || '').lastIndexOf('@');
    if (at < 0) return '';
    return String(email).slice(at + 1).trim().toLowerCase();
}

/**
 * true se l'email usa un dominio bloccato.
 *
 * Il confronto include i sottodomini (`mail.mailinator.com` conta come
 * `mailinator.com`): i servizi temp-mail ne offrono a decine proprio per
 * aggirare i filtri sul dominio esatto.
 */
export function isBlockedEmailDomain(email, env) {
    const domain = emailDomain(email);
    if (!domain) return false;

    const extra = extraBlockedDomains(env);
    const parts = domain.split('.');

    // Confronta il dominio e ogni suo suffisso: a.b.example.com -> b.example.com -> example.com
    for (let i = 0; i < parts.length - 1; i++) {
        const candidate = parts.slice(i).join('.');
        if (BUILTIN_BLOCKED_DOMAINS.has(candidate)) return true;
        if (extra && extra.has(candidate)) return true;
    }
    return false;
}
