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

Non c'è `package.json`: il deploy pubblica solo file statici dalla root del repository.

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
