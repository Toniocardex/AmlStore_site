/**
 * Test della logica "avvisami quando torna disponibile".
 *
 * Copre le due parti pure: la normalizzazione dell'input (restock.js) e i
 * template email/pagina di annullamento (restock-email-templates.js). Il resto
 * — insert, conteggi, invio Resend — vuole D1 e va verificato su pages dev.
 *
 *     node scripts/test-restock.mjs
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

/* Stessa acrobazia di scripts/test-email-domains.mjs: i moduli in
   functions/api/_lib sono ESM, ma package.json dichiara "type": "commonjs",
   quindi Node li leggerebbe come CommonJS. Caricarli come data: URL li valuta
   come ESM senza toccare la configurazione del progetto.
   Qui serve un passo in piu': restock.js importa stock.js e rate-limit.js, e
   puntare quegli import al file su disco li farebbe ricadere in CommonJS. Le
   dipendenze vengono percio' inlinate ricorsivamente come data: URL. */
const moduleCache = new Map();

function dataUrlFor(file) {
    if (moduleCache.has(file)) return moduleCache.get(file);
    const url = new URL(`../functions/api/_lib/${file}`, import.meta.url);
    const src = readFileSync(url, 'utf-8').replace(
        /from '\.\/([\w.-]+\.js)'/g,
        (_, dep) => `from '${dataUrlFor(dep)}'`
    );
    const dataUrl = 'data:text/javascript;base64,' + Buffer.from(src).toString('base64');
    moduleCache.set(file, dataUrl);
    return dataUrl;
}

function loadModule(file) {
    return import(dataUrlFor(file));
}

const { safeRestockPath, normalizeRestockEmail, isValidRestockEmail, RESTOCK_LOCALES } =
    await loadModule('restock.js');
const { restockBackInStockEmail, restockCancelPage, restockLocale } =
    await loadModule('restock-email-templates.js');

const tests = [];
const test = (name, fn) => tests.push([name, fn]);

test('accetta le sette lingue con una PDP pubblicata', () => {
    for (const lang of ['it', 'en', 'de', 'fr', 'es', 'nl', 'pt']) {
        assert.equal(RESTOCK_LOCALES.has(lang), true, lang);
    }
    assert.equal(RESTOCK_LOCALES.has('ru'), false);
});

test('normalizza e valida l’email', () => {
    assert.equal(normalizeRestockEmail('  Mario.Rossi@Example.IT '), 'mario.rossi@example.it');
    assert.equal(isValidRestockEmail('mario.rossi@example.it'), true);
    assert.equal(isValidRestockEmail('mario.rossi@example'), false);
    assert.equal(isValidRestockEmail('non-una-email'), false);
    assert.equal(isValidRestockEmail(''), false);
});

test('il path della PDP resta interno alla lingua dichiarata', () => {
    assert.equal(
        safeRestockPath('/it/windows-11-pro-oem-dvd', 'it'),
        '/it/windows-11-pro-oem-dvd'
    );
    // Finisce dentro un'email: nessuna di queste deve poter diventare un link
    // verso l'esterno o verso un'altra lingua.
    assert.equal(safeRestockPath('https://evil.example/it/x', 'it'), '/it/');
    assert.equal(safeRestockPath('//evil.example/it/x', 'it'), '/it/');
    assert.equal(safeRestockPath('/it/../../evil', 'it'), '/it/');
    assert.equal(safeRestockPath('/en/windows-server-2022', 'it'), '/it/');
    assert.equal(safeRestockPath('', 'de'), '/de/');
    // Lingua sconosciuta = italiano, come nel resto del sito.
    assert.equal(safeRestockPath('/en/windows-server-2022', 'zz'), '/it/');
    assert.equal(safeRestockPath('/it/windows-server-2022', 'zz'), '/it/windows-server-2022');
});

test('l’email di rientro contiene prodotto, link e annullamento', () => {
    const mail = restockBackInStockEmail({
        lang: 'it',
        productName: 'Microsoft Windows 11 Professional DVD Ita OEM | FQC-10538',
        productUrl: 'https://eurolicenze.com/it/windows-11-pro-oem-dvd',
        cancelUrl: 'https://eurolicenze.com/api/restock-cancel?token=abc',
    });
    assert.match(mail.subject, /Di nuovo disponibile/);
    assert.match(mail.html, /windows-11-pro-oem-dvd/);
    assert.match(mail.html, /restock-cancel\?token=abc/);
    assert.match(mail.text, /restock-cancel\?token=abc/);
    // Nessuna newsletter mascherata: e' una notifica di servizio.
    assert.match(mail.html, /newsletter/i);
});

test('ogni lingua della PDP ha una sua copia, le altre cadono su EN', () => {
    for (const lang of ['it', 'en', 'de', 'fr', 'es', 'nl', 'pt']) {
        assert.equal(restockLocale(lang), lang, lang);
        const mail = restockBackInStockEmail({
            lang,
            productName: 'Prodotto',
            productUrl: 'https://eurolicenze.com/x',
            cancelUrl: 'https://eurolicenze.com/y',
        });
        assert.ok(mail.subject.includes('Prodotto'), lang);
        assert.ok(mail.html.length > 400, lang);
    }
    assert.equal(restockLocale('ru'), 'en');
});

test('il nome prodotto viene escapato nell’HTML', () => {
    const mail = restockBackInStockEmail({
        lang: 'it',
        productName: '<script>alert(1)</script>',
        productUrl: 'https://eurolicenze.com/x',
        cancelUrl: 'https://eurolicenze.com/y',
    });
    assert.equal(mail.html.includes('<script>alert(1)</script>'), false);
    assert.match(mail.html, /&lt;script&gt;/);
});

test('la pagina di annullamento chiede conferma via POST', () => {
    const confirm = restockCancelPage({
        lang: 'it', state: 'confirm', siteOrigin: 'https://eurolicenze.com', token: 'a'.repeat(32),
    });
    // Un GET che cancellasse da solo verrebbe innescato dai prefetch dei
    // client di posta: la cancellazione deve passare da una POST esplicita.
    assert.match(confirm, /method="POST"/);
    assert.match(confirm, /name="token" value="a{32}"/);
    assert.match(confirm, /noindex/);

    const done = restockCancelPage({
        lang: 'it', state: 'done', siteOrigin: 'https://eurolicenze.com', token: '',
    });
    assert.equal(done.includes('method="POST"'), false);
});

/* ─── Ciclo di vita su SQLite vero ───────────────────────────────────────────
   Le query girano su node:sqlite con lo schema di produzione, dietro un guscio
   minimo che imita l'API D1. Serve a verificare l'assunzione portante dello
   schema: l'indice UNIQUE(sku, email) deve bloccare la seconda iscrizione dello
   stesso indirizzo, ma tollerare N righe gia' notificate (email azzerata a
   NULL) per lo stesso SKU — in SQLite i NULL non collidono fra loro. */

function d1Shim(db) {
    return {
        prepare(sql) {
            const stmt = db.prepare(sql);
            const wrap = (args) => ({
                run: async () => {
                    const r = stmt.run(...args);
                    return { meta: { changes: Number(r.changes) } };
                },
                first: async () => stmt.get(...args) ?? null,
                all: async () => ({ results: stmt.all(...args) }),
            });
            return { bind: (...args) => wrap(args), ...wrap([]) };
        },
    };
}

async function runDbTests() {
    let DatabaseSync;
    try {
        ({ DatabaseSync } = await import('node:sqlite'));
    } catch (_) {
        console.log('  --  node:sqlite non disponibile, test sul ciclo di vita saltati');
        return 0;
    }

    const { createRestockRequest, pendingBatchesForSku, markRestockNotified,
            pendingCountsBySku, cancelRestockByToken, findRestockByToken } =
        await loadModule('restock.js');

    const schema = readFileSync(new URL('../schema-restock-migration.sql', import.meta.url), 'utf-8');
    const db = new DatabaseSync(':memory:');
    db.exec(schema);
    const d1 = d1Shim(db);

    // FQC-10538 = Windows 11 Pro OEM DVD, uno degli SKU fisici in catalogo.
    const sku = 'FQC-10538';
    const base = { sku, lang: 'it', pagePath: '/it/windows-11-pro-oem-dvd', ipHash: null };

    let failures = 0;
    // `await fn()`: diversi controlli qui sono asincroni, e senza await un
    // assert fallito diventerebbe una promise rifiutata fuori dal try — cioe'
    // un test verde che non ha verificato niente.
    const check = async (name, fn) => {
        try {
            await fn();
            console.log(`  ok  ${name}`);
        } catch (e) {
            failures++;
            console.error(`FAIL  ${name}`);
            console.error(`      ${e.message}`);
        }
    };

    const first = await createRestockRequest(d1, { ...base, email: 'Anna@Example.it' });
    const dup = await createRestockRequest(d1, { ...base, email: 'anna@example.it' });
    const second = await createRestockRequest(d1, { ...base, email: 'bruno@example.it' });

    await check('la seconda iscrizione dello stesso indirizzo non crea una riga', () => {
        assert.equal(first.ok && first.duplicate === false, true);
        assert.equal(dup.ok && dup.duplicate === true, true);
        assert.equal(second.duplicate, false);
        const counts = db.prepare('SELECT COUNT(*) AS n FROM restock_requests').get();
        assert.equal(Number(counts.n), 2);
    });

    await check('lo SKU digitale viene rifiutato prima di toccare il database', async () => {
        const bad = await createRestockRequest(d1, { ...base, sku: 'KASPERSKY_PLUS', email: 'c@example.it' });
        assert.equal(bad.ok, false);
    });

    const batches = await pendingBatchesForSku(d1, sku);
    await check('i destinatari escono in ordine di iscrizione', () => {
        assert.equal(batches.length, 1);
        assert.deepEqual(batches[0].map((r) => r.email), ['anna@example.it', 'bruno@example.it']);
        assert.match(batches[0][0].token, /^[0-9a-f]{32}$/);
    });

    await markRestockNotified(d1, batches[0].map((r) => r.id));

    await check('dopo l’invio l’indirizzo sparisce e la coda si svuota', async () => {
        const rows = db.prepare('SELECT email, notified_at FROM restock_requests').all();
        assert.equal(rows.every((r) => r.email === null && r.notified_at), true);
        const counts = await pendingCountsBySku(d1);
        assert.equal(counts.get(sku), undefined);
        assert.deepEqual(await pendingBatchesForSku(d1, sku), []);
    });

    await check('piu’ righe notificate sullo stesso SKU convivono (UNIQUE ignora i NULL)', () => {
        const rows = db.prepare('SELECT COUNT(*) AS n FROM restock_requests WHERE sku = ?').all(sku);
        assert.equal(Number(rows[0].n), 2);
    });

    await check('chi si riscrive dopo essere stato avvisato riparte da capo', async () => {
        const again = await createRestockRequest(d1, { ...base, email: 'anna@example.it' });
        assert.equal(again.ok && again.duplicate === false, true);
        const counts = await pendingCountsBySku(d1);
        assert.equal(counts.get(sku).pending, 1);
    });

    await check('se il batch Resend viene rifiutato si ripiega sugli invii singoli', async () => {
        /* E' il percorso che in dev non si puo' esercitare (nessuna
           RESEND_API_KEY in .dev.vars): qui il DB e' vero, solo fetch e'
           finto. Serve a garantire che un rifiuto dell'endpoint batch non si
           traduca in "nessuno viene avvisato". */
        const db2 = new DatabaseSync(':memory:');
        db2.exec(schema);
        const d2 = d1Shim(db2);
        await createRestockRequest(d2, { ...base, email: 'uno@example.it' });
        await createRestockRequest(d2, { ...base, email: 'due@example.it' });

        const calls = [];
        const realFetch = globalThis.fetch;
        globalThis.fetch = async (url, init) => {
            calls.push(String(url));
            const batch = String(url).endsWith('/batch');
            return new Response(batch ? 'unsupported field' : '{}', { status: batch ? 422 : 200 });
        };
        try {
            const { sendRestockNotifications } = await loadModule('email.js');
            const res = await sendRestockNotifications(
                d2, sku, 'Windows 11 Pro OEM DVD', 'chiave-finta', 'https://eurolicenze.com'
            );
            assert.equal(res.sent, 2);
            assert.equal(res.failed, 0);
            assert.equal(calls.filter((u) => u.endsWith('/batch')).length, 1);
            assert.equal(calls.filter((u) => !u.endsWith('/batch')).length, 2);
            const rows = db2.prepare('SELECT email, notified_at FROM restock_requests').all();
            assert.equal(rows.every((r) => r.email === null && r.notified_at), true);
        } finally {
            globalThis.fetch = realFetch;
        }
        db2.close();
    });

    await check('se anche gli invii singoli falliscono la coda resta intatta', async () => {
        const db3 = new DatabaseSync(':memory:');
        db3.exec(schema);
        const d3 = d1Shim(db3);
        await createRestockRequest(d3, { ...base, email: 'tre@example.it' });

        const realFetch = globalThis.fetch;
        globalThis.fetch = async () => new Response('down', { status: 500 });
        try {
            const { sendRestockNotifications } = await loadModule('email.js');
            const res = await sendRestockNotifications(
                d3, sku, 'Windows 11 Pro OEM DVD', 'chiave-finta', 'https://eurolicenze.com'
            );
            assert.equal(res.sent, 0);
            assert.equal(res.failed, 1);
            // Nessuno e' stato avvisato: l'iscrizione deve restare in coda per
            // il prossimo salvataggio del magazzino.
            const row = db3.prepare('SELECT email, notified_at FROM restock_requests').get();
            assert.equal(row.email, 'tre@example.it');
            assert.equal(row.notified_at, null);
        } finally {
            globalThis.fetch = realFetch;
        }
        db3.close();
    });

    await check('l’annullamento cancella la riga per davvero', async () => {
        const pending = (await pendingBatchesForSku(d1, sku))[0][0];
        assert.equal(await cancelRestockByToken(d1, pending.token), true);
        assert.equal(await findRestockByToken(d1, pending.token), null);
        // Idempotente: il secondo clic sullo stesso link non e' un errore.
        assert.equal(await cancelRestockByToken(d1, pending.token), false);
    });

    db.close();
    return failures;
}

let failed = 0;
for (const [name, fn] of tests) {
    try {
        fn();
        console.log(`  ok  ${name}`);
    } catch (e) {
        failed++;
        console.error(`FAIL  ${name}`);
        console.error(`      ${e.message}`);
    }
}

failed += await runDbTests();

console.log(failed ? `\n${failed} test falliti` : '\nTutti i test superati');
process.exit(failed ? 1 : 0);
