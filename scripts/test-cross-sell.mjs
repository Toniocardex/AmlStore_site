/**
 * Test del motore di cross-sell del carrello (js/cart-cross-sell.js).
 *
 * Gira su Node senza dipendenze: il modulo si carica anche fuori dal browser
 * (esce prima di toccare il DOM) ed espone pickSuggestions su globalThis.
 * I casi usano l'indice reale asset/cross-sell/it.json, cosi' una regressione
 * nei dati generati da build-cross-sell-index.py si vede subito.
 *
 *     node scripts/test-cross-sell.mjs
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

await import(new URL('../js/cart-cross-sell.js', import.meta.url));
const { pickSuggestions } = globalThis.AmlCrossSell;

const catalog = JSON.parse(readFileSync(join(ROOT, 'asset', 'cross-sell', 'it.json'), 'utf-8'));
const bySku = new Map(catalog.map((p) => [p.sku, p]));
const bySlug = new Map(catalog.map((p) => [p.slug, p]));

/** Riga di carrello a partire da uno slug dell'indice. */
function line(slug, quantity = 1) {
    const p = bySlug.get(slug);
    assert.ok(p, `slug non nell'indice: ${slug}`);
    return {
        sku: p.sku,
        name: p.name,
        currency: p.currency,
        unitAmount: p.priceMinor,
        quantity,
        physical: Boolean(p.physical),
    };
}

const tests = [];
function test(name, fn) { tests.push([name, fn]); }

test('carrello vuoto: nessun suggerimento', () => {
    assert.deepEqual(pickSuggestions(catalog, []), []);
});

test('indice vuoto o assente: nessun suggerimento', () => {
    assert.deepEqual(pickSuggestions([], [line('windows-11-pro')]), []);
    assert.deepEqual(pickSuggestions(null, [line('windows-11-pro')]), []);
});

test('Windows nel carrello: primo suggerimento antivirus, mai un altro Windows', () => {
    const picks = pickSuggestions(catalog, [line('windows-11-pro')]);
    assert.equal(picks.length, 3);
    assert.equal(picks[0].family, 'antivirus');
    assert.ok(!picks.some((p) => p.family === 'windows'));
});

test('una sola proposta per famiglia', () => {
    const picks = pickSuggestions(catalog, [line('windows-11-pro')]);
    const families = picks.map((p) => p.family);
    assert.equal(new Set(families).size, families.length);
});

test("mai lo sku gia' presente nel carrello", () => {
    const cart = [line('windows-11-pro'), line('kaspersky-premium-5-devices')];
    const inCart = new Set(cart.map((l) => l.sku));
    assert.ok(!pickSuggestions(catalog, cart).some((p) => inCart.has(p.sku)));
});

test("famiglia gia' nel carrello esclusa: con antivirus dentro non se ne propone un altro", () => {
    const picks = pickSuggestions(catalog, [line('kaspersky-premium-5-devices')]);
    assert.ok(picks.length > 0);
    assert.ok(!picks.some((p) => p.family === 'antivirus'));
});

test('nessun bundle fra i candidati', () => {
    for (const slug of ['windows-11-pro', 'kaspersky-premium-5-devices', 'microsoft-365-family']) {
        assert.ok(!pickSuggestions(catalog, [line(slug)]).some((p) => p.bundle));
    }
});

test('nessun prodotto a fine supporto fra i candidati', () => {
    for (const slug of ['microsoft-365-family', 'excel-2024', 'kaspersky-premium-5-devices']) {
        assert.ok(!pickSuggestions(catalog, [line(slug)]).some((p) => p.legacy));
    }
});

test('a chi compra Office il Windows proposto e\' l\'11 Home, non il 10', () => {
    for (const slug of ['microsoft-365-family', 'excel-2024']) {
        const win = pickSuggestions(catalog, [line(slug)]).find((p) => p.family === 'windows');
        if (win) assert.equal(win.slug, 'windows-11-home', `carrello ${slug} -> ${win.slug}`);
    }
});

test('windows resta l\'ultima delle proposte a un carrello Office', () => {
    const picks = pickSuggestions(catalog, [line('microsoft-365-family')]);
    const i = picks.findIndex((p) => p.family === 'windows');
    if (i >= 0) assert.equal(i, picks.length - 1, 'windows non e\' in coda');
});

test('carrello tutto digitale: nessun prodotto fisico proposto', () => {
    const picks = pickSuggestions(catalog, [line('microsoft-365-family')]);
    assert.ok(picks.every((p) => !p.physical));
});

test("add-on piu' caro del pezzo forte del carrello: mai in prima posizione", () => {
    const cart = [line('windows-11-home')];
    const maxUnit = cart[0].unitAmount;
    const picks = pickSuggestions(catalog, cart);
    assert.ok(picks[0].priceMinor <= maxUnit,
        `primo suggerimento ${picks[0].sku} a ${picks[0].priceMinor} sopra ${maxUnit}`);
});

test("risultato deterministico a parita' di carrello", () => {
    const cart = [line('microsoft-365-personal')];
    const a = pickSuggestions(catalog, cart).map((p) => p.sku);
    const b = pickSuggestions(catalog, cart).map((p) => p.sku);
    assert.deepEqual(a, b);
});

test('limite rispettato', () => {
    assert.equal(pickSuggestions(catalog, [line('windows-11-pro')], 1).length, 1);
    assert.ok(pickSuggestions(catalog, [line('windows-11-pro')], 10).length <= 8);
});

test('sku sconosciuto nel carrello: ripiego senza errori', () => {
    const picks = pickSuggestions(catalog, [{ sku: 'SKU-FANTASMA', unitAmount: 9900, quantity: 1 }]);
    assert.ok(picks.length > 0);
    assert.ok(picks.every((p) => bySku.has(p.sku)));
});

test('carrello con tutte le famiglie complementari: nessun doppione, mai un crash', () => {
    const cart = [
        line('windows-11-pro'),
        line('kaspersky-premium-5-devices'),
        line('microsoft-365-family'),
        line('acronis-true-image-advanced'),
        line('adobe-acrobat-pro'),
    ];
    const inCart = new Set(cart.map((l) => l.sku));
    const picks = pickSuggestions(catalog, cart);
    assert.ok(!picks.some((p) => inCart.has(p.sku)));
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
