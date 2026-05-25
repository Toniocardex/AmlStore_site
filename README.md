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
├── components/         # Web Components riutilizzabili (header, footer, cookie-banner)
├── css/                # Fogli di stile (page.css, home.css, product.css, cart.css)
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
