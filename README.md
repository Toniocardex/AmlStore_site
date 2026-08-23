# Aml Store — sito statico multilingue

Dominio pubblico: **https://aml-store.com**

Struttura URL: ogni lingua ha la propria sottocartella (`/it/`, `/en/`, `/fr/`, `/de/`, `/es/`, `/pt/`, `/nl/`).
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
├── sitemap.xml         # Tutte le URL indicizzabili (7 lingue × pagine)
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
├── es/                 # Pagine in spagnolo
├── pt/                 # Pagine in portoghese
└── nl/                 # Pagine in olandese
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
| pagine 404 | `not-found.css` |

`product.css` è il guscio della pagina prodotto (`.product-page`, CTA sticky),
condiviso dalle schede e dalla pagina soluzioni; `product-pdp.css` è il layout
della scheda vera e propria. Nasce dalla fusione di `product-v2.css` e
`product-v3.css`, che erano due generazioni successive caricate insieme.

Per sapere cosa in un foglio non aggancia più niente:

```
node scripts/audit-css-usage.mjs --verbose css/product-pdp.css
```

## Pagine 404

Cloudflare Pages, su un URL che non esiste, serve la `404.html` **più vicina**
risalendo l'albero delle cartelle. Da qui la divisione:

| file | risponde a | ha header e footer |
|---|---|---|
| `it/404.html`, `en/…`, `fr/…`, `de/…`, `es/…`, `pt/…`, `nl/…` | i miss dentro quella lingua (`/it/qualsiasi/cosa`) | sì, pre-renderizzati come ogni altra pagina |
| `404.html` in root | solo gli URL fuori da ogni cartella lingua (`/vecchio-slug`) | no: lì la lingua non è nota, la pagina la fa scegliere |

Le sette pagine per lingua sono pagine normali del sito: `build-inline-chrome.mjs`
le prende da sé, quindi dopo averle toccate va rilanciato come per le altre.

Due vincoli, se le si modifica:

- **Path assoluti**, mai `../`: la stessa pagina risponde anche a `/it/a/b/c`,
  dove un path relativo punterebbe a una cartella che non esiste. Vale per CSS,
  JS, immagini e link. `ensureStylesheets()` in `build-inline-chrome.mjs` segue
  il prefisso che la pagina usa per `page.css`, quindi aggancia il CSS del
  chrome in modo coerente senza altre configurazioni.
- **`noindex, follow`** nel `<meta name="robots">`, e lo slug `404` è in `SKIP`
  dentro `scripts/rebuild-sitemap.py`: queste pagine rispondono 200 se aperte
  per il loro indirizzo (`/it/404`), quindi senza il noindex finirebbero
  indicizzate.

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
