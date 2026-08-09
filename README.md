# Aml Store — sito statico multilingue

Dominio pubblico: **https://aml-store.com**

Struttura URL: ogni lingua ha la propria sottocartella (`/it/`, `/en/`, `/fr/`, `/de/`, `/es/`).
La root `/` reindirizza a `/it/` tramite la regola `/ /it/ 301` in `_redirects`.

Flusso: **GitHub** (questo repo) → integrazione **Cloudflare Pages** → **deploy automatico** a ogni push sul branch collegato (`main`).

## Cloudflare Pages

| Impostazione        | Valore        |
|---------------------|---------------|
| Framework preset    | Nessuno       |
| Build command       | *(vuoto)*     |
| Build output dir    | *(vuoto)*     |
| Root directory      | *(repo root)* |

Il deploy pubblica file statici dalla root; le **Pages Functions** in `functions/api/` gestiscono checkout e ordini (D1).

### Catalogo prezzi

Il sito **non usa WooCommerce**: è solo HTML/CSS/JS statico + **Pages Functions** (`functions/api/`) per checkout (Stripe, PayPal, bonifico) e ordini su **D1**.

- Listino autoritativo lato server: [`functions/api/_lib/catalog.js`](functions/api/_lib/catalog.js) — il Worker **non** si fida dei prezzi inviati dal browser.
- Rigenerare il catalogo: `python scripts/build-catalog.py` passando il CSV export (es. dal **vecchio** e-shop `www.aml-store.com`, solo come sorgente SKU/prezzi).
- Riferimento per chi crea schede prodotto: [`catalog.json`](catalog.json) in root (`data-stripe-product-sku` = colonna `code` del CSV).
- Redirect in [`_redirects`](_redirects): slug del sito precedente → nuove pagine `.html` statiche.

## Struttura cartelle

```
/
├── _redirects          # Redirect Cloudflare Pages (root → /it/, vecchi slug, ecc.)
├── _headers            # Cache-Control e security headers per Cloudflare Pages
├── robots.txt          # Sitemap: https://aml-store.com/sitemap.xml
├── sitemap.xml         # Tutte le URL indicizzabili (5 lingue × pagine)
├── components/         # Web Components (header, footer, cookie-banner)
├── css/                # Un foglio per tipo di pagina, sopra la base page.css
│                       # header.css e footer.css sono generati, non modificarli a mano
├── js/                 # Script (locale-path.js, consent-init.js, theme-init.js, cart.js…)
├── fonts/              # Montserrat self-hosted (woff2)
├── images/flags/       # SVG bandiere per selettore lingua
├── asset/              # Media (hero, immagini prodotto) e loghi pagamenti
├── logo/               # Logo header (light/dark, 200px/400px)
├── favicon/            # Favicon PNG e WebP
├── it/                 # Pagine in italiano
├── en/                 # Pagine in inglese
├── fr/                 # Pagine in francese
├── de/                 # Pagine in tedesco
└── es/                 # Pagine in spagnolo
```

## Fogli di stile

`page.css` è la base comune (token del design system, tipografia, elementi
condivisi); sopra, ogni tipo di pagina carica **un** foglio dedicato:

| pagina | fogli oltre a `page.css` |
|---|---|
| scheda prodotto | `product.css` + `product-pdp.css` |
| soluzioni M365 | `product.css` + `microsoft-365-solutions.css` |
| M365 Family | come scheda prodotto, più `m365-family-pilot.css` |
| home / carrello / checkout / contatti / consulenza / chi siamo | il foglio omonimo |

`product.css` è il guscio della pagina prodotto (`.product-page`, CTA sticky),
condiviso dalle schede e dalla pagina soluzioni; `product-pdp.css` è il layout
della scheda vera e propria. Nasce dalla fusione di `product-v2.css` e
`product-v3.css`, che erano due generazioni successive caricate insieme.

Per sapere cosa in un foglio non aggancia più niente:

```
node scripts/audit-css-usage.mjs --verbose css/product-pdp.css
```

## Header e footer

Sono **pre-renderizzati nell'HTML** di ogni pagina, non costruiti dal JS a
runtime: così i loro link stanno nel sorgente servito (crawlabili anche senza
esecuzione di JavaScript) e non c'è spostamento di layout all'arrivo degli script.

| dove | cosa | servito ai browser |
|---|---|---|
| `scripts/chrome-renderer/` | il **markup** — unica sorgente, solo build | no |
| `components/header.js`, `footer.js` | il **comportamento** (menu, ricerca, carrello) | sì |
| `css/header.css`, `css/footer.css` | gli **stili**, generati dai renderer | sì |

Chi tocca navigazione o footer deve rigenerare: vedi
[`scripts/chrome-renderer/README.md`](scripts/chrome-renderer/README.md) e la
sezione «Ordine dei comandi di build» in [`GO-LIVE.md`](GO-LIVE.md).
