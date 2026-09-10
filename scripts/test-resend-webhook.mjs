/**
 * Firma Svix Resend + ranking stato consegna.
 *     node scripts/test-resend-webhook.mjs
 */
import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
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

const {
    verifyResendWebhook,
    mappedLicenseDelivery,
    shouldUpgradeDelivery,
    applyLicenseEmailDelivery,
    licenseOrderIdFromResendTags,
} = await import(dataUrlFor('resend-webhook.js'));

const tests = [];
const test = (name, fn) => tests.push([name, fn]);

function orderDbMock(store) {
    return {
        prepare(sql) {
            return {
                bind(...args) {
                    return {
                        first: async () => {
                            if (/license_email_resend_id = \?/.test(sql)) {
                                return store.license_email_resend_id === args[0]
                                    ? { ...store }
                                    : null;
                            }
                            if (/WHERE id = \?/.test(sql)) {
                                return store.id === args[0] ? { ...store } : null;
                            }
                            return null;
                        },
                        run: async () => {
                            if (/UPDATE/i.test(sql)) {
                                store.license_email_delivery = args[0];
                                if (!store.license_email_resend_id && args[1]) {
                                    store.license_email_resend_id = args[1];
                                }
                            }
                            return {};
                        },
                    };
                },
            };
        },
    };
}

test('mappedLicenseDelivery', () => {
    assert.equal(mappedLicenseDelivery('email.sent'), 'accepted');
    assert.equal(mappedLicenseDelivery('email.delivered'), 'delivered');
    assert.equal(mappedLicenseDelivery('email.bounced'), 'bounced');
    assert.equal(mappedLicenseDelivery('email.opened'), null);
    assert.equal(mappedLicenseDelivery('email.clicked'), null);
});

test('shouldUpgradeDelivery non degrada bounce a delivered', () => {
    assert.equal(shouldUpgradeDelivery('accepted', 'delivered'), true);
    assert.equal(shouldUpgradeDelivery('delivered', 'bounced'), true);
    assert.equal(shouldUpgradeDelivery('bounced', 'delivered'), false);
    assert.equal(shouldUpgradeDelivery('delivered', 'accepted'), false);
});

test('licenseOrderIdFromResendTags solo con kind=license', () => {
    assert.equal(licenseOrderIdFromResendTags({ kind: 'license', order_id: 'EL-1' }), 'EL-1');
    assert.equal(licenseOrderIdFromResendTags([
        { name: 'kind', value: 'license' },
        { name: 'order_id', value: 'EL-1' },
    ]), 'EL-1');
    assert.equal(licenseOrderIdFromResendTags({ order_id: 'EL-1' }), '');
    assert.equal(licenseOrderIdFromResendTags({ kind: 'confirm', order_id: 'EL-1' }), '');
    assert.equal(licenseOrderIdFromResendTags(null), '');
});

test('applyLicenseEmailDelivery ignora email sconosciute', async () => {
    const db = {
        prepare() {
            return {
                bind() {
                    return {
                        first: async () => null,
                        run: async () => { throw new Error('non deve aggiornare'); },
                    };
                },
            };
        },
    };
    const r = await applyLicenseEmailDelivery(db, 'missing', 'delivered');
    assert.equal(r.updated, false);
    assert.equal(r.skipped, 'unknown_email');
});

test('applyLicenseEmailDelivery aggiorna solo se lo stato peggiora o avanza', async () => {
    const store = { id: 'EL-1', license_email_delivery: 'accepted', license_email_resend_id: 're_1' };
    const r1 = await applyLicenseEmailDelivery(orderDbMock(store), 're_1', 'delivered');
    assert.equal(r1.updated, true);
    assert.equal(store.license_email_delivery, 'delivered');
    const r2 = await applyLicenseEmailDelivery(orderDbMock(store), 're_1', 'accepted');
    assert.equal(r2.updated, false);
    assert.equal(store.license_email_delivery, 'delivered');
});

test('applyLicenseEmailDelivery fallback sul tag order_id se manca resend_id', async () => {
    const store = { id: 'EL-1', license_email_delivery: null, license_email_resend_id: null };
    const r = await applyLicenseEmailDelivery(orderDbMock(store), 're_late', 'delivered', {
        orderId: 'EL-1',
    });
    assert.equal(r.updated, true);
    assert.equal(store.license_email_delivery, 'delivered');
    assert.equal(store.license_email_resend_id, 're_late');
});

test('applyLicenseEmailDelivery non usa order_id se l\'ordine ha un altro id Resend', async () => {
    const store = { id: 'EL-1', license_email_delivery: 'accepted', license_email_resend_id: 're_old' };
    const r = await applyLicenseEmailDelivery(orderDbMock(store), 're_other', 'bounced', {
        orderId: 'EL-1',
    });
    assert.equal(r.updated, false);
    assert.equal(r.skipped, 'other_email');
    assert.equal(store.license_email_delivery, 'accepted');
});

test('verifyResendWebhook accetta firma Svix valida', async () => {
    const key = Buffer.from('test-secret-bytes-32-chars-long!!');
    const secret = 'whsec_' + key.toString('base64');
    const body = '{"type":"email.delivered","data":{"email_id":"abc"}}';
    const id = 'msg_test_1';
    const ts = String(Math.floor(Date.now() / 1000));
    const sig = createHmac('sha256', key).update(`${id}.${ts}.${body}`).digest('base64');
    const headers = new Headers({
        'svix-id': id,
        'svix-timestamp': ts,
        'svix-signature': `v1,${sig}`,
    });
    const event = await verifyResendWebhook(body, headers, secret);
    assert.equal(event.type, 'email.delivered');
    assert.equal(event.data.email_id, 'abc');
});

test('verifyResendWebhook rifiuta firma errata', async () => {
    const headers = new Headers({
        'svix-id': 'msg_x',
        'svix-timestamp': String(Math.floor(Date.now() / 1000)),
        'svix-signature': 'v1,aaaa',
    });
    await assert.rejects(
        () => verifyResendWebhook('{}', headers, 'whsec_' + Buffer.from('x').toString('base64')),
        /mismatch/
    );
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
console.log('\nOK: ' + tests.length + ' test webhook Resend');
