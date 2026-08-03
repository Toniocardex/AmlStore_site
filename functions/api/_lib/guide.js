/**
 * guide.js — allegato "Guida Copilot" omaggio sugli ordini Microsoft 365.
 *
 * Il PDF non è pubblicato sul sito: vive in un bucket R2 privato (binding GUIDES)
 * e viene allegato all'email di conferma solo quando l'ordine è PAGATO e contiene
 * una licenza Microsoft 365 Personal o Family (anche dentro un bundle).
 *
 * Aggiornare la guida = ricaricare l'oggetto su R2, senza redeploy:
 *   wrangler r2 object put aml-store-guides/guida-copilot-microsoft-365.pdf \
 *     --file=<percorso-locale> --content-type=application/pdf --remote
 */

import { safeParseJSON } from './utils.js';

/** Oggetto R2 e nome con cui il cliente vede l'allegato. */
export const GUIDE_KEY      = 'guida-copilot-microsoft-365.pdf';
export const GUIDE_FILENAME = 'Guida-Copilot-Microsoft-365-Aml-Store.pdf';

/**
 * SKU che danno diritto alla guida: le due licenze M365 dirette più i bundle
 * che ne contengono una. Confronto case-insensitive.
 */
const M365_SKUS = new Set([
    'qq2-00012',                    // Microsoft 365 Personal
    '6gq-00092',                    // Microsoft 365 Family
    'sc_m365_kpremium_5device',     // Bundle M365 Personal + Kaspersky Premium
    'sc_m365p_mtotprot_5device',    // Bundle M365 Personal + McAfee Total Protection
    'sc_w11home_m365pers',          // Bundle Windows 11 Home + M365 Personal
]);

/**
 * Lingue a cui inviare la guida. La guida esiste solo in italiano: allegarla a un
 * ordine tedesco o francese sarebbe rumore. Aggiungere locale qui se in futuro
 * verranno prodotte altre edizioni.
 */
const GUIDE_LOCALES = new Set(['it']);

/**
 * True se l'ordine è pagato, è in una lingua servita e contiene almeno uno
 * degli SKU idonei.
 * @param {object} order — riga grezza D1
 */
export function orderQualifiesForGuide(order) {
    if (!order || order.status !== 'paid') return false;
    if (!GUIDE_LOCALES.has(order.locale || 'it')) return false;

    const items = safeParseJSON(order.line_items, []);
    return items.some((item) => M365_SKUS.has(String(item?.sku || '').trim().toLowerCase()));
}

/**
 * Converte un ArrayBuffer in base64 senza sforare lo stack: lo spread di un
 * Uint8Array da ~640 KB in String.fromCharCode va in RangeError, quindi si
 * procede a blocchi di 32 KB.
 */
function toBase64(buffer) {
    const bytes = new Uint8Array(buffer);
    const CHUNK = 0x8000;
    let binary = '';
    for (let i = 0; i < bytes.length; i += CHUNK) {
        binary += String.fromCharCode.apply(null, bytes.subarray(i, i + CHUNK));
    }
    return btoa(binary);
}

/**
 * Legge la guida da R2 e la restituisce nel formato allegati di Resend.
 * Restituisce null (senza sollevare) se il bucket non è configurato o l'oggetto
 * manca: l'email di conferma ordine deve partire comunque.
 *
 * @param {R2Bucket|undefined} bucket — binding env.GUIDES
 * @returns {Promise<{filename: string, content: string}|null>}
 */
export async function loadGuideAttachment(bucket) {
    if (!bucket) {
        console.warn('[guide] binding GUIDES non configurato, guida non allegata');
        return null;
    }
    try {
        const object = await bucket.get(GUIDE_KEY);
        if (!object) {
            console.warn(`[guide] oggetto R2 "${GUIDE_KEY}" non trovato, guida non allegata`);
            return null;
        }
        return {
            filename: GUIDE_FILENAME,
            content:  toBase64(await object.arrayBuffer()),
        };
    } catch (e) {
        console.error('[guide] lettura da R2 fallita, guida non allegata:', e);
        return null;
    }
}

/**
 * Aggiunge la guida al payload Resend se l'ordine ne ha diritto.
 * Mutazione volutamente non bloccante: qualsiasi problema lascia il payload
 * intatto e l'email parte lo stesso.
 */
export async function attachGuideIfEligible(payload, order, bucket) {
    if (!orderQualifiesForGuide(order)) return false;

    const attachment = await loadGuideAttachment(bucket);
    if (!attachment) return false;

    payload.attachments = [...(payload.attachments || []), attachment];
    return true;
}
