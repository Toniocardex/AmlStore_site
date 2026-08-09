/**
 * audit-css-usage.mjs — dice quali regole di un foglio di stile non trovano
 * mai un elemento, caricando pagine reali in un browser.
 *
 * Non e' la "coverage" di DevTools: quella vede solo cio' che si applica al
 * primo render, quindi segna come inutilizzato tutto cio' che dipende da hover,
 * media query o interazione. Qui i selettori vengono spogliati delle pseudo-classi
 * e provati con querySelector, e quelli che dipendono da uno stato prodotto dal JS
 * (.is-*, [data-*], [open], data-theme...) sono tenuti per sicurezza.
 *
 *   node scripts/audit-css-usage.mjs css/product.css css/product-v3.css
 *   node scripts/audit-css-usage.mjs --pages=it/windows-11-pro,it/cart css/cart.css
 *   node scripts/audit-css-usage.mjs --verbose css/home.css
 *
 * Prerequisito: dev server attivo (`npm run dev`, porta 8788).
 * Senza --pages usa un campione che copre tutti i tipi di scheda prodotto.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { chromium } from 'playwright';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const BASE = process.env.AML_DEV_ORIGIN || 'http://localhost:8788';

/* Un campione per ogni layout: PDP standard, pilota, bundle, server, antivirus,
   pagine categoria e la pagina soluzioni (l'unica che carica product.css da sola). */
export const DEFAULT_PAGES = [
    'it/windows-11-pro', 'it/office-2024-home', 'it/office-2024-home-business',
    'it/microsoft-365-personal', 'it/microsoft-365-family', 'it/microsoft-365-business-standard',
    'it/kaspersky-standard', 'it/norton-360-deluxe', 'it/eset-nod32-1-device',
    'it/windows-server-2025', 'it/sql-server-2022-standard', 'it/windows-11-pro-oem-dvd',
    'it/windows-11-pro-coa', 'it/bundle-windows-11-home-m365-personal',
    'it/project-professional-2024', 'it/adobe-acrobat-pro', 'it/office-2019-home-student',
    'it/visio-standard-2024', 'it/coreldraw-2024', 'it/windows-10-pro',
    'it/office-2021-professional-plus', 'it/outlook-2024', 'it/acronis-true-image-advanced',
    'it/microsoft-365-solutions', 'it/sistemi-operativi', 'it/suite-office',
    'it/antivirus', 'it/pacchetti', 'it/strumenti', 'it/windows-server',
];

/* Uno stato che il test statico non riproduce: meglio tenere la regola. */
const STATEFUL = /\.is-|\.open\b|\[open\]|\[data-|\[aria-|data-theme|:checked|:disabled|:not\(|\.active\b|\.selected\b|\.error\b|\.loading\b|--visible\b|--active\b|--open\b|-hidden\b/;

/* Le alternative vanno dalla piu' lunga alla piu' corta: in un'alternanza vince
   la prima che combacia, quindi `focus` prima di `focus-visible` lascerebbe
   dietro un `-visible` e trasformerebbe un selettore valido in uno che non
   aggancia nulla (falso morto). */
const PSEUDO = [
    'placeholder-shown', 'focus-within', 'focus-visible', 'first-letter', 'first-line',
    'placeholder', 'backdrop', 'selection', 'disabled', 'checked', 'visited',
    'before', 'after', 'active', 'hover', 'focus', 'target', 'marker',
].join('|');

/** Toglie cio' che querySelector non puo' valutare su una pagina a riposo. */
export function testableSelector(sel) {
    return sel
        .replace(new RegExp('::?(?:' + PSEUDO + ')\\b(\\([^)]*\\))?', 'g'), '')
        .replace(/::?-(?:webkit|moz|ms)-[\w-]+(\([^)]*\))?/g, '')
        .replace(/\s+/g, ' ')
        .trim();
}

/**
 * Nomi di classe che compaiono nel JS: sono stati che il test statico non puo'
 * riprodurre (vengono aggiunti al click, allo scroll, a fine fetch...). Qualsiasi
 * regola che li nomina va tenuta, a prescindere da cosa aggancia a riposo.
 */
export function classesTouchedByJs() {
    const dirs = ['js', 'components', 'scripts/chrome-renderer'];
    const names = new Set();
    for (const d of dirs) {
        const dir = path.join(ROOT, d);
        if (!fs.existsSync(dir)) continue;
        for (const f of fs.readdirSync(dir)) {
            if (!f.endsWith('.js')) continue;
            const src = fs.readFileSync(path.join(dir, f), 'utf8');
            /* Ogni stringa quotata che ha la forma di un nome di classe. Volutamente
               generoso: una classe puo' arrivare all'elemento per vie che nessun
               pattern piu' stretto vede — p.es. product-v3.js tiene il nome in una
               variabile (`var HIDDEN_CLASS = 'pdp-nav-hidden'`), quindi cercare
               solo dentro classList.add() la perderebbe. */
            for (const m of src.matchAll(/['"`]([\w-]+(?:\s+[\w-]+)*)['"`]/g)) {
                m[1].split(/\s+/).filter((n) => /^[a-zA-Z][\w-]*$/.test(n)).forEach((n) => names.add(n));
            }
            for (const m of src.matchAll(/class="([^"]+)"/g)) {
                m[1].split(/\s+/).filter(Boolean).forEach((n) => names.add(n));
            }
        }
    }
    return names;
}

/* ── Parser a blocchi: conserva il testo originale di ogni nodo ─────────────── */

function maskComments(css) {
    const comments = [];
    const masked = css.replace(/\/\*[\s\S]*?\*\//g, (m) => {
        comments.push(m);
        return '/*' + '-'.repeat(Math.max(0, m.length - 4)) + '*/';
    });
    return { masked, comments };
}

/**
 * Divide il CSS in nodi di primo livello mantenendo gli offset, cosi' da poter
 * riemettere il testo esatto. Le at-rule con blocco (@media, @supports) vengono
 * ricorse; @keyframes resta un nodo unico.
 */
export function parseNodes(css) {
    const { masked } = maskComments(css);
    const nodes = [];
    let i = 0;

    while (i < masked.length) {
        // salta spazi, tenendoli agganciati al nodo successivo
        const startWs = i;
        while (i < masked.length && /\s/.test(masked[i])) i++;
        if (i >= masked.length) {
            if (startWs < masked.length) nodes.push({ type: 'raw', raw: css.slice(startWs) });
            break;
        }

        const braceAt = masked.indexOf('{', i);
        const semiAt = masked.indexOf(';', i);

        // at-rule senza blocco (@import, @charset)
        if (semiAt !== -1 && (braceAt === -1 || semiAt < braceAt)) {
            nodes.push({ type: 'raw', raw: css.slice(startWs, semiAt + 1) });
            i = semiAt + 1;
            continue;
        }
        if (braceAt === -1) {
            nodes.push({ type: 'raw', raw: css.slice(startWs) });
            break;
        }

        // trova la graffa di chiusura corrispondente
        let depth = 0, end = -1;
        for (let j = braceAt; j < masked.length; j++) {
            if (masked[j] === '{') depth++;
            else if (masked[j] === '}') {
                depth--;
                if (depth === 0) { end = j; break; }
            }
        }
        if (end === -1) { nodes.push({ type: 'raw', raw: css.slice(startWs) }); break; }

        // I commenti restano nel testo originale ma non fanno parte del selettore.
        const prelude = css.slice(i, braceAt).replace(/\/\*[\s\S]*?\*\//g, ' ').trim();
        const inner = css.slice(braceAt + 1, end);
        const raw = css.slice(startWs, end + 1);
        const lead = css.slice(startWs, i);

        if (/^@(-\w+-)?keyframes\b/i.test(prelude)) {
            nodes.push({ type: 'keyframes', name: prelude.split(/\s+/)[1] || '', prelude, raw, lead });
        } else if (prelude.startsWith('@')) {
            nodes.push({ type: 'atrule', prelude, children: parseNodes(inner), raw, lead });
        } else {
            nodes.push({
                type: 'rule',
                selectors: prelude.split(',').map((s) => s.trim()).filter(Boolean),
                body: inner,
                raw,
                lead,
            });
        }
        i = end + 1;
    }
    return nodes;
}

/** Tutti i selettori presenti nell'albero. */
export function collectSelectors(nodes, out = new Set()) {
    for (const n of nodes) {
        if (n.type === 'rule') n.selectors.forEach((s) => out.add(s));
        else if (n.type === 'atrule') collectSelectors(n.children, out);
    }
    return out;
}

/** Carica le pagine e restituisce l'insieme dei selettori che agganciano qualcosa. */
export async function findLiveSelectors(selectors, pages) {
    const list = [...selectors];
    const browser = await chromium.launch({ channel: process.env.AML_BROWSER_CHANNEL || 'msedge' });
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await ctx.newPage();
    await page.route('**/*.{png,jpg,jpeg,webp,avif,svg,woff2}', (r) => r.abort());

    const live = new Set();
    for (const rel of pages) {
        await page.goto(`${BASE}/${rel}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
        await page.waitForTimeout(600);
        const hits = await page.evaluate((sels) => {
            const found = [];
            for (const s of sels) {
                const t = s.testable;
                if (!t) { found.push(s.original); continue; }
                // selettore non valutabile: non lo si puo' dichiarare morto
                try { if (document.querySelector(t)) found.push(s.original); }
                catch (e) { found.push(s.original); }
            }
            return found;
        }, list.map((s) => ({ original: s, testable: testableSelector(s) })));
        hits.forEach((h) => live.add(h));
    }

    await browser.close();
    return live;
}

/**
 * Una regola si tiene se aggancia qualcosa, se dipende da uno stato, o se
 * nomina una classe che il JS manipola. In dubbio si tiene: cancellare una
 * regola viva e' una regressione invisibile, tenerne una morta costa byte.
 */
export function keepsRule(node, live, jsClasses = new Set()) {
    return node.selectors.some((s) => {
        if (live.has(s) || STATEFUL.test(s)) return true;
        for (const cls of s.matchAll(/\.([\w-]+)/g)) if (jsClasses.has(cls[1])) return true;
        return false;
    });
}

/* ── CLI ───────────────────────────────────────────────────────────────────── */

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
    const args = process.argv.slice(2);
    const verbose = args.includes('--verbose');
    const pagesArg = args.find((a) => a.startsWith('--pages='));
    const pages = pagesArg ? pagesArg.slice('--pages='.length).split(',') : DEFAULT_PAGES;
    const files = args.filter((a) => !a.startsWith('--'));
    if (!files.length) {
        console.error('uso: node scripts/audit-css-usage.mjs [--pages=a,b] [--verbose] <file.css...>');
        process.exit(2);
    }

    const trees = {};
    const all = new Set();
    for (const f of files) {
        trees[f] = parseNodes(fs.readFileSync(path.join(ROOT, f), 'utf8'));
        collectSelectors(trees[f], all);
    }
    console.log(`${all.size} selettori distinti su ${files.length} file, ${pages.length} pagine campione`);

    const live = await findLiveSelectors(all, pages);
    const jsClasses = classesTouchedByJs();
    console.log(`${jsClasses.size} nomi di classe manipolati dal JS: tenuti comunque`);

    console.log('\nfoglio                     regole   vive   morte');
    console.log('-'.repeat(52));
    for (const f of files) {
        const dead = [];
        let alive = 0;
        const walk = (nodes) => {
            for (const n of nodes) {
                if (n.type === 'rule') (keepsRule(n, live, jsClasses) ? (alive++, null) : dead.push(n.selectors.join(', ')));
                else if (n.type === 'atrule') walk(n.children);
            }
        };
        walk(trees[f]);
        console.log(
            f.replace('css/', '').padEnd(26) +
            String(alive + dead.length).padStart(6) +
            String(alive).padStart(7) +
            String(dead.length).padStart(8)
        );
        if (verbose && dead.length) console.log('  ' + dead.join('\n  '));
    }
}
