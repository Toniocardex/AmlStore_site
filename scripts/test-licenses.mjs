/**
 * Test della logica pura del pool licenze (ADR-004).
 *
 * Assegnazione D1 e Resend si verificano su pages dev. Qui: parse, maschera,
 * bisogno digitale, attivazione, fail-soft schema.
 *
 *     node scripts/test-licenses.mjs
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

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

const {
    parseLicenseKeys,
    licenseKeyNorm,
    maskLicenseKey,
    digitalNeedFromItems,
    activationFromProductName,
    isLicensesSchemaMissing,
    isDigitalSku,
    capKeysToNeed,
    coversDigitalNeed,
    licenseDeliveryState,
} = await loadModule('licenses.js');

const tests = [];
const test = (name, fn) => tests.push([name, fn]);

test('parse: una chiave per riga, ignora vuote e commenti', () => {
    const { keys, skipped } = parseLicenseKeys('# header\n\nAAAAA-BBBBB-CCCCC-DDDDD-EEEEE\n  \nFFFFF-11111-22222-33333-44444\n');
    assert.equal(keys.length, 2);
    assert.equal(keys[0].material, 'AAAAA-BBBBB-CCCCC-DDDDD-EEEEE');
    assert.equal(skipped.empty >= 2, true);
});

test('parse: dedup case-insensitive', () => {
    const { keys, skipped } = parseLicenseKeys('ABCDE-12345\nabcde-12345\nABCDE-12345\n');
    assert.equal(keys.length, 1);
    assert.equal(skipped.duplicate, 2);
});

test('parse: scarta troppo corte', () => {
    const { keys, skipped } = parseLicenseKeys('abc\nVALID-KEY-01\n');
    assert.equal(keys.length, 1);
    assert.equal(skipped.invalid >= 1, true);
});

test('licenseKeyNorm lower+trim', () => {
    assert.equal(licenseKeyNorm('  AbC  '), 'abc');
});

test('maskLicenseKey non espone il centro', () => {
    const masked = maskLicenseKey('AAAAA-BBBBB-CCCCC-DDDDD-EEEEE');
    assert.equal(masked.includes('BBBBB'), false);
    assert.equal(masked.startsWith('AAAA'), true);
    assert.equal(masked.endsWith('EEEE'), true);
});

test('digitalNeedFromItems ignora i fisici', () => {
    const needed = digitalNeedFromItems([
        { sku: 'QQ2-00012', qty: 2 },
        { sku: 'FQC-10538', qty: 1, physical: true },
    ]);
    assert.equal(needed.get('QQ2-00012'), 2);
    assert.equal(needed.has('FQC-10538'), false);
});

test('digitalNeedFromItems somma qty sullo stesso SKU', () => {
    const needed = digitalNeedFromItems([
        { sku: 'QQ2-00012', qty: 1 },
        { sku: 'QQ2-00012', quantity: 2 },
    ]);
    assert.equal(needed.get('QQ2-00012'), 3);
});

test('digitalNeedFromItems non assegna piu chiavi della qty checkout (max 99/riga)', () => {
    const needed = digitalNeedFromItems([
        { sku: 'QQ2-00012', qty: 500 },
    ]);
    assert.equal(needed.get('QQ2-00012'), 99);
});

test('coversDigitalNeed e falso se manca una chiave', () => {
    const needed = new Map([['A', 2]]);
    assert.equal(coversDigitalNeed([{ sku: 'A' }], needed), false);
    assert.equal(coversDigitalNeed([{ sku: 'A' }, { sku: 'A' }], needed), true);
});

test('licenseDeliveryState distingue spedita e mail mancante', () => {
    assert.equal(licenseDeliveryState({
        emailSentAt: '2026-09-10T17:28:16.112Z', keysAssigned: 1, keysEmailed: 1,
    }), 'sent');
    assert.equal(licenseDeliveryState({
        emailSentAt: null, keysAssigned: 1, keysEmailed: 0,
    }), 'email_missing');
    assert.equal(licenseDeliveryState({
        eventSrc: 'sending:webhook_stripe', keysAssigned: 1, keysEmailed: 0,
    }), 'sending');
});

test('activationFromProductName allinea il generatore', () => {
    assert.equal(activationFromProductName('Microsoft 365 Personal'), 'office');
    assert.equal(activationFromProductName('Kaspersky Premium'), 'kaspersky');
    assert.equal(activationFromProductName('Windows 11 Pro'), 'windows');
    assert.equal(activationFromProductName('Windows Server 2022'), 'windows_server');
    assert.equal(activationFromProductName('ESET HOME Security'), 'eset');
});

test('isDigitalSku: ESD si, DVD no', () => {
    assert.equal(isDigitalSku('QQ2-00012'), true);
    assert.equal(isDigitalSku('FQC-10538'), false);
    assert.equal(isDigitalSku('SKU-INESISTENTE'), false);
});

test('isLicensesSchemaMissing riconosce D1 senza tabella', () => {
    assert.equal(isLicensesSchemaMissing(new Error('no such table: license_keys')), true);
    assert.equal(isLicensesSchemaMissing(new Error('no such column: license_status')), true);
    assert.equal(isLicensesSchemaMissing(new Error('UNIQUE constraint failed')), false);
});

test('capKeysToNeed tiene al massimo la qty per SKU', () => {
    const needed = new Map([['A', 1], ['B', 2]]);
    const { kept, extras } = capKeysToNeed([
        { id: '1', sku: 'A' },
        { id: '2', sku: 'A' },
        { id: '3', sku: 'B' },
        { id: '4', sku: 'B' },
        { id: '5', sku: 'B' },
        { id: '6', sku: 'C' },
    ], needed);
    assert.deepEqual(kept.map((k) => k.id), ['1', '3', '4']);
    assert.deepEqual(extras.map((k) => k.id), ['2', '5', '6']);
});

test('schema-licenses-migration.sql crea la tabella e le colonne', () => {
    const schema = readFileSync(new URL('../schema-licenses-migration.sql', import.meta.url), 'utf-8');
    assert.match(schema, /CREATE TABLE IF NOT EXISTS license_keys/);
    assert.match(schema, /ALTER TABLE orders ADD COLUMN license_status/);
    assert.match(schema, /key_norm/);
});

test('ADR-004 esiste come specifica', () => {
    const adr = readFileSync(new URL('../docs/adr/ADR-004-auto-license-fulfillment.md', import.meta.url), 'utf-8');
    assert.match(adr, /All-or-nothing/);
    assert.match(adr, /licenseEmailHtml/);
    assert.match(adr, /Assenza di chiave = flusso attuale/);
});

let failed = 0;
for (const [name, fn] of tests) {
    try {
        await fn();
        console.log('ok  ', name);
    } catch (e) {
        failed += 1;
        console.error('FAIL', name);
        console.error('    ', e.message);
    }
}

if (failed) {
    console.error('\n' + failed + ' test falliti');
    process.exit(1);
}
console.log('\nOK: ' + tests.length + ' test licenze');
