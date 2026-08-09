/**
 * extract-chrome-css.mjs — estrae il blocco <style> dai renderer di
 * scripts/chrome-renderer/ e lo riscrive come foglio di stile esterno, con ogni
 * selettore ancorato al custom element che prima faceva da shadow host.
 *
 * Senza Shadow DOM non c'e' piu' incapsulamento, quindi l'ancoraggio a
 * `ecommerce-header` / `ecommerce-footer` ricrea lo stesso confine per via di
 * specificita'.
 *
 *   node scripts/extract-chrome-css.mjs
 *
 * Rigenera css/header.css e css/footer.css. I sorgenti sono i renderer, non i
 * componenti di components/: quelli ormai agganciano solo il comportamento e
 * non contengono piu' stili. Idempotente.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

/** Estrae il contenuto del primo blocco <style>...</style> del file. */
function extractStyleBlock(source) {
    const open = source.indexOf('<style>');
    const close = source.indexOf('</style>');
    if (open === -1 || close === -1 || close < open) {
        throw new Error('blocco <style> non trovato');
    }
    return source.slice(open + '<style>'.length, close);
}

/**
 * Riscrive una lista di selettori ancorandola al custom element.
 *   :host                    -> ecommerce-header
 *   :host(.is-compact) .x    -> ecommerce-header.is-compact .x
 *   *                        -> ecommerce-header *
 *   .nav-link                -> ecommerce-header .nav-link
 */
function scopeSelectorList(selectorList, host) {
    return selectorList
        .split(',')
        .map((raw) => {
            const sel = raw.trim();
            if (!sel) return null;

            // :host(.foo) [resto]  ->  host.foo [resto]
            const hostFn = sel.match(/^:host\(\s*([^)]+?)\s*\)\s*(.*)$/);
            if (hostFn) {
                const rest = hostFn[2].trim();
                return `${host}${hostFn[1]}${rest ? ' ' + rest : ''}`;
            }

            // :host [resto]  ->  host [resto]
            const hostPlain = sel.match(/^:host\b\s*(.*)$/);
            if (hostPlain) {
                const rest = hostPlain[1].trim();
                return `${host}${rest ? ' ' + rest : ''}`;
            }

            return `${host} ${sel}`;
        })
        .filter(Boolean)
        .join(',\n');
}

/**
 * Sostituisce i commenti con segnaposto privi di graffe. Serve a due cose:
 * evitare che una `{` o `}` dentro un commento sfasi il conteggio dei blocchi,
 * e tenere i commenti fuori dai selettori quando questi vengono riscritti.
 */
function maskComments(css) {
    const comments = [];
    const masked = css.replace(/\/\*[\s\S]*?\*\//g, (m) => {
        comments.push(m);
        return `%%C${comments.length - 1}%%`;
    });
    return { masked, comments };
}

function unmaskComments(css, comments) {
    return css.replace(/%%C(\d+)%%/g, (_, i) => comments[Number(i)]);
}

/**
 * Estrae i segnaposto di commento da un prelude, per riemetterli sopra la
 * regola invece che in mezzo al selettore.
 */
function splitPreludeComments(prelude) {
    const found = [];
    const clean = prelude.replace(/%%C\d+%%/g, (m) => {
        found.push(m);
        return '';
    });
    return { comments: found, clean };
}

/**
 * Percorre il CSS e ancora al host ogni selettore di regola, lasciando intatti
 * i preludi delle at-rule e i selettori di step dentro @keyframes.
 */
function scopeCssMasked(css, host) {
    let out = '';
    let buf = '';
    let depth = 0;
    // Stack dei contesti aperti: 'keyframes' silenzia lo scoping degli step.
    const context = [];

    for (let i = 0; i < css.length; i++) {
        const ch = css[i];

        if (ch === '{') {
            const prelude = buf;
            const trimmed = prelude.trim();
            buf = '';

            // I commenti vanno tolti dal prelude prima di qualsiasi decisione:
            // un commento davanti a una @media ne nasconderebbe la chiocciola.
            const { comments, clean } = splitPreludeComments(trimmed);
            const selector = clean.trim();

            if (selector.startsWith('@')) {
                // At-rule con blocco: il prelude passa cosi' com'e'.
                context.push(/^@(-\w+-)?keyframes\b/.test(selector) ? 'keyframes' : 'at');
                out += prelude + '{';
            } else if (context[context.length - 1] === 'keyframes') {
                // Step di keyframe (from / to / 40%): non va ancorato.
                context.push('rule');
                out += prelude + '{';
            } else if (depth > 0 && context[context.length - 1] === 'rule') {
                // Blocco annidato dentro una regola: qui non ne esistono, ma
                // se comparissero vanno lasciati stare.
                context.push('rule');
                out += prelude + '{';
            } else {
                const indent = (prelude.match(/^\s*/) || [''])[0];
                context.push('rule');
                const lead = comments.length ? comments.map((c) => indent + c.trim()).join('\n') + '\n' : '';
                out += lead + indent + scopeSelectorList(selector, host) + ' {';
            }
            depth++;
            continue;
        }

        if (ch === '}') {
            out += buf + '}';
            buf = '';
            depth--;
            context.pop();
            continue;
        }

        buf += ch;
    }

    return out + buf;
}

/** Maschera i commenti, ancora i selettori, rimette i commenti. */
function scopeCss(css, host) {
    const { masked, comments } = maskComments(css);
    return unmaskComments(scopeCssMasked(masked, host), comments);
}

/** Normalizza l'indentazione: il CSS nel template era rientrato di 20 spazi. */
function dedent(css) {
    const lines = css.split('\n');
    const indents = lines
        .filter((l) => l.trim())
        .map((l) => (l.match(/^ */) || [''])[0].length);
    const min = indents.length ? Math.min(...indents) : 0;
    return lines.map((l) => l.slice(min)).join('\n').trim() + '\n';
}

/**
 * Interpolazioni `${...}` che nel template erano calcolate a runtime. In un
 * foglio esterno le URL si risolvono rispetto al CSS stesso, quindi il percorso
 * relativo da `css/` e' equivalente e non dipende dalla profondita' della pagina.
 */
const INTERPOLATIONS = {
    '${esc(footerBgSrc)}': '../asset/media/aml_store_media_background_footer.avif',
    '${esc(footerBgMobileSrc)}': '../asset/media/aml_store_media_background_footer_mobile.avif',
};

function resolveInterpolations(css, file) {
    let out = css;
    for (const [needle, value] of Object.entries(INTERPOLATIONS)) {
        out = out.split(needle).join(value);
    }
    const left = out.match(/\$\{[^}]*\}/g);
    if (left) {
        throw new Error(
            `${file}: interpolazioni non risolte (${[...new Set(left)].join(', ')}). ` +
            'Aggiungerle a INTERPOLATIONS in scripts/extract-chrome-css.mjs.'
        );
    }
    return out;
}

const TARGETS = [
    {
        component: 'scripts/chrome-renderer/header.js',
        stylesheet: 'css/header.css',
        host: 'ecommerce-header',
        title: 'header del sito',
    },
    {
        component: 'scripts/chrome-renderer/footer.js',
        stylesheet: 'css/footer.css',
        host: 'ecommerce-footer',
        title: 'footer del sito',
    },
];

for (const t of TARGETS) {
    const source = fs.readFileSync(path.join(ROOT, t.component), 'utf8');
    const raw = extractStyleBlock(source);
    const scoped = resolveInterpolations(scopeCss(dedent(raw), t.host), t.stylesheet);

    const header =
        `/* ${t.stylesheet.split('/').pop()} — stili del ${t.title}.\n` +
        `   Generato da scripts/extract-chrome-css.mjs a partire dal blocco <style>\n` +
        `   di ${t.component}. Ogni selettore e' ancorato a \`${t.host}\`: prima\n` +
        `   l'isolamento lo dava lo Shadow DOM, ora lo da' l'ancoraggio al custom element.\n` +
        `   Non modificare a mano: le modifiche vanno fatte nel renderer e poi rigenerate. */\n\n`;

    // CRLF come gli altri fogli del repo, a prescindere dai fine riga del sorgente.
    const out = (header + scoped).replace(/\r?\n/g, '\r\n');
    fs.writeFileSync(path.join(ROOT, t.stylesheet), out, 'utf8');
    console.log(
        `${t.stylesheet.padEnd(16)} <- ${t.component.padEnd(34)} ` +
        `${(Buffer.byteLength(out) / 1024).toFixed(1)} KB`
    );
}
