/**
 * seo-availability.js — allinea la disponibilità dichiarata ai crawler con il
 * magazzino reale, al momento della richiesta.
 *
 * Perché serve: le pagine prodotto e i feed Merchant sono file statici, generati
 * a mano. Per gli SKU fisici (DVD/COA) dichiaravano sempre InStock / in_stock,
 * anche a magazzino vuoto: Google indicizzava "disponibile" e il checkout poi
 * rifiutava l'ordine con 409 (assertCartStock). Qui il valore viene riscritto
 * in streaming su ciò che dice D1, così il crawler vede il vero stato senza
 * dipendere dal rendering JS (js/product-stock.js resta come difesa in più).
 *
 * Tocca SOLO gli SKU fisici: i digitali sono sempre disponibili e restano
 * intatti in entrambi i canali.
 */

import { listPhysicalSkus, getStockSnapshot } from './stock.js';

/**
 * slug pagina -> SKU, per i 7 prodotti fisici (stesse coppie di
 * scripts/regen-physical-stock.py, che ne verifica l'allineamento).
 * Serve perché il JSON-LD sta in <head>, prima del data-stripe-product-sku:
 * in streaming lo SKU della pagina si saprebbe troppo tardi.
 */
export const PHYSICAL_SLUG_TO_SKU = {
    'windows-11-pro-oem-dvd': 'FQC-10538',
    'windows-11-pro-coa': 'W11_PRO_STICKER',
    'windows-server-2019': 'P73-07788',
    'windows-server-2022': 'P73-08328',
    'windows-server-2025-dvd': 'P73-08538',
    'sql-server-2022-enterprise': 'P6L-00076',
    'sql-server-2022-standard': 'SC835510',
};

const LANGS = 'it|en|fr|de|es|pt|nl';
const PRODUCT_PATH_RE = new RegExp(`^/(${LANGS})/([a-z0-9-]+?)(?:\.html)?/?$`);
const FEED_PATH_RE = new RegExp(`^/feeds/google-shopping-(?:${LANGS})\.xml$`);

/** SKU fisico servito da questo path, o null se non è una pagina fisica. */
export function physicalSkuForPath(pathname) {
    const m = PRODUCT_PATH_RE.exec(pathname || '');
    if (!m) return null;
    return PHYSICAL_SLUG_TO_SKU[m[2]] || null;
}

export function isShoppingFeedPath(pathname) {
    return FEED_PATH_RE.test(pathname || '');
}

function isHtml(response) {
    return (response.headers.get('content-type') || '').includes('text/html');
}

/** Sostituisce solo il valore della chiave "availability": nient'altro del JSON. */
function patchLdJson(json, inStock) {
    const target = inStock
        ? 'https://schema.org/InStock'
        : 'https://schema.org/OutOfStock';
    return json.replace(
        /("availability"\s*:\s*")https:\/\/schema\.org\/[A-Za-z]+(")/g,
        `$1${target}$2`
    );
}

/**
 * Bufferizza il solo blocco ld+json (non l'intera pagina: la risposta resta
 * in streaming) e ne riscrive l'availability.
 */
class LdJsonAvailabilityHandler {
    constructor(inStock) {
        this.inStock = inStock;
        this.buf = '';
    }

    text(chunk) {
        this.buf += chunk.text;
        if (!chunk.lastInTextNode) {
            chunk.remove();
            return;
        }
        const out = this.buf.includes('"availability"')
            ? patchLdJson(this.buf, this.inStock)
            : this.buf;
        this.buf = '';
        // html: true — dentro <script> il contenuto è raw text: senza questo
        // HTMLRewriter escaperebbe le & delle descrizioni rompendo il JSON.
        chunk.replace(out, { html: true });
    }
}

/** Pagina prodotto fisico: JSON-LD allineato a D1. */
export async function rewriteProductAvailability(db, sku, response) {
    if (!db || !response.ok || !isHtml(response)) return response;
    const stock = await getStockSnapshot(db);
    const inStock = (stock.get(sku) || 0) > 0;
    return new HTMLRewriter()
        .on('script[type="application/ld+json"]', new LdJsonAvailabilityHandler(inStock))
        .transform(response);
}

/** Feed Merchant: g:availability dei soli SKU fisici allineato a D1. */
export async function rewriteFeedAvailability(db, response) {
    if (!db || !response.ok) return response;
    const stock = await getStockSnapshot(db);
    const physical = new Set(listPhysicalSkus().map((p) => p.sku));

    const xml = await response.text();
    const patched = xml.replace(/<item>[\s\S]*?<\/item>/g, (block) => {
        const id = /<g:id>([^<]*)<\/g:id>/.exec(block);
        const sku = id ? id[1].trim() : '';
        if (!sku || !physical.has(sku)) return block;
        const avail = (stock.get(sku) || 0) > 0 ? 'in_stock' : 'out_of_stock';
        return block.replace(
            /<g:availability>[^<]*<\/g:availability>/,
            `<g:availability>${avail}</g:availability>`
        );
    });

    const headers = new Headers(response.headers);
    headers.delete('content-length');
    headers.delete('etag');
    return new Response(patched, { status: response.status, headers });
}
