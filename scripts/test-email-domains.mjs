/**
 * Test del blocco domini email usa-e-getta (functions/api/_lib/email-domains.js).
 *
 * Il modulo e' ESM puro senza dipendenze da Workers, quindi si importa
 * direttamente in Node.
 *
 *     node scripts/test-email-domains.mjs
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

/* Il modulo e' ESM (come tutto functions/api/_lib), ma package.json dichiara
   "type": "commonjs", quindi Node tratterebbe il .js come CommonJS e l'import
   fallirebbe. Nei Workers il problema non esiste. Caricarlo come data: URL lo
   valuta come ESM senza toccare la configurazione del progetto ne' rinominare
   un file che in produzione funziona gia'. */
const SRC = new URL('../functions/api/_lib/email-domains.js', import.meta.url);
const { isBlockedEmailDomain, emailDomain } = await import(
    'data:text/javascript;base64,' + Buffer.from(readFileSync(SRC, 'utf-8')).toString('base64')
);

const tests = [];
const test = (name, fn) => tests.push([name, fn]);

test('blocca i domini osservati negli attacchi', () => {
    for (const d of ['analismail.com', 'blackfirsta.com', 'ishowfirstmail.com', 'firsthidden.com']) {
        assert.equal(isBlockedEmailDomain(`carolwoll1973@${d}`, {}), true, d);
    }
});

test('blocca i temp-mail noti', () => {
    assert.equal(isBlockedEmailDomain('x@mailinator.com', {}), true);
    assert.equal(isBlockedEmailDomain('x@yopmail.com', {}), true);
});

test('NON blocca i domini dei clienti veri', () => {
    // Questi sono gli indirizzi che hanno davvero comprato sul negozio.
    for (const e of ['gallozzipietro2@gmail.com', 'wano18@yahoo.de',
                     'm.manuzzi@ilsolco.it', 'cv@southerncrossdental.com',
                     'info@okriparo.it', 'antonino.cardelli@outlook.it']) {
        assert.equal(isBlockedEmailDomain(e, {}), false, e);
    }
});

test('NON blocca i servizi di inoltro per la privacy', () => {
    // Sono indirizzi permanenti di persone reali, non caselle a perdere:
    // bloccarli costerebbe vendite legittime.
    for (const e of ['a@proton.me', 'b@duck.com', 'c@icloud.com',
                     'd@simplelogin.io', 'e@anonaddy.me']) {
        assert.equal(isBlockedEmailDomain(e, {}), false, e);
    }
});

test('blocca anche i sottodomini', () => {
    assert.equal(isBlockedEmailDomain('x@mail.mailinator.com', {}), true);
    assert.equal(isBlockedEmailDomain('x@a.b.analismail.com', {}), true);
});

test('BLOCKED_EMAIL_DOMAINS aggiunge domini senza deploy', () => {
    const env = { BLOCKED_EMAIL_DOMAINS: 'cattivo.example, altro.example' };
    assert.equal(isBlockedEmailDomain('x@cattivo.example', env), true);
    assert.equal(isBlockedEmailDomain('x@altro.example', env), true);
    assert.equal(isBlockedEmailDomain('x@cattivo.example', {}), false, 'senza env non deve bloccare');
});

test('env malformata o assente non rompe nulla', () => {
    for (const env of [undefined, null, {}, { BLOCKED_EMAIL_DOMAINS: '' }, { BLOCKED_EMAIL_DOMAINS: ' , , ' }]) {
        assert.equal(isBlockedEmailDomain('x@gmail.com', env), false);
        assert.equal(isBlockedEmailDomain('x@mailinator.com', env), true);
    }
});

test('input non validi non lanciano', () => {
    for (const v of [undefined, null, '', 'senza-chiocciola', '@', 'a@']) {
        assert.equal(isBlockedEmailDomain(v, {}), false, String(v));
    }
});

test('il confronto e maiuscole/minuscole insensibile', () => {
    assert.equal(isBlockedEmailDomain('X@MailInator.COM', {}), true);
});

test('emailDomain estrae il dominio', () => {
    assert.equal(emailDomain('a.b@Example.COM'), 'example.com');
    assert.equal(emailDomain('senza'), '');
});

let failed = 0;
for (const [name, fn] of tests) {
    try {
        fn();
        console.log(`  ok   ${name}`);
    } catch (e) {
        failed++;
        console.log(`  FAIL ${name}\n       ${e.message}`);
    }
}
console.log(`\n${tests.length - failed}/${tests.length} test superati`);
process.exit(failed ? 1 : 0);
