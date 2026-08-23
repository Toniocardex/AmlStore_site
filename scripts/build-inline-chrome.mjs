/**
 * build-inline-chrome.mjs — pre-renderizza header e footer dentro l'HTML servito.
 *
 * Prima header.js e footer.js costruivano il proprio markup a runtime dentro uno
 * Shadow DOM: l'HTML pubblicato conteneva solo i tag vuoti `<ecommerce-header>` e
 * `<ecommerce-footer>`, quindi nessun crawler che non esegua JS vedeva la
 * navigazione ne' i link del footer, e il loro ingresso tardivo produceva CLS.
 *
 * Questo script scrive quel markup direttamente nelle pagine, come light DOM.
 *
 * Il markup e' generato da `scripts/chrome-renderer/` (vedi il README li' dentro):
 * sono i componenti nella versione che renderizzava, serviti al posto di quelli
 * di `components/` solo durante la build. Girano in un browser vero sull'URL
 * reale della pagina, quindi lingua e voce di menu attiva risultano corrette e
 * il markup e' esattamente quello che il sito produceva prima della conversione.
 *
 * Prerequisito: dev server attivo (`npm run dev`, porta 8788).
 *
 *   node scripts/build-inline-chrome.mjs
 *   node scripts/build-inline-chrome.mjs --check    # non scrive, esce !=0 se disallineato
 *
 * Dopo l'esecuzione lanciare `python scripts/bump-asset-version.py`.
 * Idempotente: rilanciarlo riscrive il markup al posto di quello precedente.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const BASE = process.env.AML_DEV_ORIGIN || 'http://localhost:8788';
const LANGS = ['it', 'en', 'fr', 'de', 'es', 'pt', 'nl'];
const CHECK_ONLY = process.argv.includes('--check');

/* I fogli di stile estratti dai componenti, da agganciare in <head>. Il
   prefisso non e' qui: lo detta la pagina, vedi ensureStylesheets(). */
const CHROME_STYLESHEETS = ['css/header.css', 'css/footer.css'];

/** it/windows-11-pro.html -> /it/windows-11-pro ; it/index.html -> /it/ */
function urlForPage(rel) {
    const [lang, file] = rel.split('/');
    return file === 'index.html' ? `/${lang}/` : `/${lang}/${file.replace(/\.html$/, '')}`;
}

function listPages() {
    const out = [];
    for (const lang of LANGS) {
        for (const f of fs.readdirSync(path.join(ROOT, lang)).sort()) {
            if (f.endsWith('.html')) out.push(`${lang}/${f}`);
        }
    }
    return out;
}

/**
 * Sostituisce il contenuto di <tag ...>...</tag> mantenendo il tag di apertura
 * cosi' com'e'. Funziona sia sul tag vuoto sia su uno gia' popolato da un giro
 * precedente, il che rende lo script rilanciabile.
 */
function replaceElementContent(html, tag, markup) {
    const re = new RegExp(`(<${tag}\\b[^>]*>)[\\s\\S]*?(</${tag}>)`);
    if (!re.test(html)) throw new Error(`<${tag}> non trovato`);
    return html.replace(re, (_, open, close) => `${open}${markup}${close}`);
}

/** Le pagine sono in CRLF: va rilevato e conservato, o il diff esplode. */
const eolOf = (html) => (html.includes('\r\n') ? '\r\n' : '\n');
const toEol = (text, eol) => text.replace(/\r?\n/g, eol);

/** Il <link> a page.css: e' l'ancora a cui si agganciano i fogli del chrome. */
const PAGE_CSS_LINK = /<link rel="stylesheet" href="(\.\.\/|\/)css\/page\.css(?:\?v=[^"]*)?">/;

/** Aggancia i fogli di stile del chrome subito dopo page.css, una volta sola. */
function ensureStylesheets(html) {
    let out = html;
    const eol = eolOf(html);

    // Quasi tutte le pagine indirizzano gli asset con `../`, ma le 404.html per
    // lingua devono farlo dalla root: Pages le serve anche per URL profondi
    // (/it/a/b/c), dove un path relativo punterebbe a una cartella inesistente.
    // Il prefisso dei fogli del chrome segue quello che la pagina usa per
    // page.css, invece di essere deciso qui.
    const probe = out.match(PAGE_CSS_LINK);
    if (!probe) throw new Error('link a page.css non trovato: non so dove agganciare il CSS del chrome');
    const prefix = probe[1];

    // A ritroso: ogni link si infila subito dopo page.css, quindi partendo
    // dall'ultimo l'ordine finale in <head> resta quello dell'array.
    for (const name of [...CHROME_STYLESHEETS].reverse()) {
        const href = prefix + name;
        const already = new RegExp(`href="${href.replace(/[.*+?^$()|[\]\\]/g, '\\$&')}(\\?v=[^"]*)?"`);
        if (already.test(out)) continue;
        const anchor = out.match(PAGE_CSS_LINK);

        // Alcune pagine hanno piu' <link> sulla stessa riga: in quel caso il
        // nuovo tag va accodato li', non su una riga nuova con rientro.
        const lineStart = out.lastIndexOf('\n', anchor.index) + 1;
        const before = out.slice(lineStart, anchor.index);
        const insertion = /^[ \t]*$/.test(before)
            ? `${anchor[0]}${eol}${before}<link rel="stylesheet" href="${href}">`
            : `${anchor[0]}<link rel="stylesheet" href="${href}">`;
        out = out.replace(anchor[0], insertion);
    }
    return out;
}

const stripStyle = (html) => html.replace(/\s*<style>[\s\S]*?<\/style>\s*/, '\n');

/**
 * Per il confronto si ignorano gli hash `?v=`: li aggiunge
 * bump-asset-version.py *dopo* questo script, anche dentro il markup appena
 * inlinato (logo, bandiere). Senza questa normalizzazione ogni pagina
 * risulterebbe disallineata subito dopo un bump.
 */
const ignoreAssetHashes = (html) => html.replace(/\?v=[A-Za-z0-9]+/g, '');

async function main() {
    // --only=<sottostringa> restringe il giro, utile per provare su poche pagine.
    const onlyArg = process.argv.find((a) => a.startsWith('--only='));
    const only = onlyArg ? onlyArg.slice('--only='.length) : null;
    const pages = listPages().filter((p) => !only || p.includes(only));
    console.log(`${pages.length} pagine da elaborare — sorgente markup: ${BASE}`);

    const browser = await chromium.launch({ channel: process.env.AML_BROWSER_CHANNEL || 'msedge' });
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await ctx.newPage();
    // Le immagini non servono: interessa solo il DOM prodotto dai componenti.
    await page.route('**/*.{png,jpg,jpeg,webp,avif,svg,woff2}', (r) => r.abort());

    // I componenti di components/ ormai agganciano solo il comportamento e non
    // producono markup: al loro posto va servito il renderer, che invece lo genera.
    for (const name of ['header', 'footer']) {
        const body = fs.readFileSync(path.join(ROOT, 'scripts/chrome-renderer', `${name}.js`), 'utf8');
        await page.route(`**/components/${name}.js*`, (route) =>
            route.fulfill({ status: 200, contentType: 'application/javascript; charset=utf-8', body })
        );
    }

    let written = 0;
    let stale = 0;
    const problems = [];

    for (const [i, rel] of pages.entries()) {
        const url = BASE + urlForPage(rel);
        try {
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
            await page.waitForFunction(
                () => {
                    const h = document.querySelector('ecommerce-header');
                    const f = document.querySelector('ecommerce-footer');
                    return h?.shadowRoot?.innerHTML?.length > 2000 && f?.shadowRoot?.innerHTML?.length > 2000;
                },
                { timeout: 20000 }
            );

            const { header, footer } = await page.evaluate(() => ({
                header: document.querySelector('ecommerce-header').shadowRoot.innerHTML,
                footer: document.querySelector('ecommerce-footer').shadowRoot.innerHTML,
            }));

            const file = path.join(ROOT, rel);
            const src = fs.readFileSync(file, 'utf8');
            const eol = eolOf(src);
            let out = replaceElementContent(src, 'ecommerce-header', toEol(stripStyle(header), eol));
            out = replaceElementContent(out, 'ecommerce-footer', toEol(stripStyle(footer), eol));
            out = ensureStylesheets(out);

            if (ignoreAssetHashes(out) !== ignoreAssetHashes(src)) {
                stale++;
                if (!CHECK_ONLY) {
                    fs.writeFileSync(file, out, 'utf8');
                    written++;
                }
            }
        } catch (e) {
            problems.push(`${rel}: ${e.message.split('\n')[0]}`);
        }

        if ((i + 1) % 50 === 0 || i === pages.length - 1) {
            process.stdout.write(`  ${i + 1}/${pages.length}\r`);
        }
    }

    await browser.close();
    console.log('');

    if (problems.length) {
        console.error(`\n${problems.length} pagine non elaborate:`);
        problems.slice(0, 20).forEach((p) => console.error('  ' + p));
        process.exitCode = 1;
        return;
    }

    if (CHECK_ONLY) {
        console.log(stale ? `${stale} pagine disallineate: rilanciare senza --check` : 'tutte le pagine allineate');
        process.exitCode = stale ? 1 : 0;
    } else {
        console.log(`${written} pagine aggiornate su ${pages.length}`);
        console.log('Ora: python scripts/bump-asset-version.py');
    }
}

main();
