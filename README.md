# Aml-Store.com — The Vault Edition

Repository del sito **Aml-Store.com**: e-commerce internazionale per **beni digitali**, con focus su sicurezza (“Vault”), prestazioni e conformità fiscale (Italia / UE). Sulle **home** (`*/index.html`): **`<title>Aml-Store</title>`** (stesso su tutte e cinque le lingue), meta description brand (tradotta), **Open Graph** / **Twitter Card** / **JSON-LD** (`Organization` + `WebSite`, `name` **Aml-Store**); immagine social: `https://Aml-Store.com/img/logo/logo-header-400.webp`. Le altre pagine (`cart`, `checkout`, `account`, `order-success`) usano il titolo *Sezione — Aml-Store*.

Questo repo corrisponde al progetto GitHub [**AmlStore_site**](https://github.com/Toniocardex/AmlStore_site).

---

## Cosa c’è dentro

| Area | Tecnologia / approccio |
|------|-------------------------|
| Frontend | **HTML, CSS e JavaScript vanilla** (ES6+). Tipografia **Inter** self-hosted (WOFF2, subset latin + latin-ext). Nessun framework. |
| Hosting & API | **Cloudflare Pages** + **Pages Functions** (`/functions`). |
| Dati | **D1** (SQLite edge) — prodotti multilingua, ordini, log download, audit admin. |
| File digitali | **R2** — oggetti privati, consegna tramite **URL firmati** a scadenza breve. |
| Pagamenti | **Stripe** — sessione checkout con prezzi letti da D1 (`price_data`, niente Price ID fissi). |
| Fatturazione | **Fattura24** (integrazione via webhook / flussi ordine). |

Lingue: struttura a cartelle **`/it/`**, **`/en/`**, **`/de/`**, **`/fr/`**, **`/es/`** (pagine speculari; `hreflang` + menu lingua compatto **`<details class="lang-dropdown">`** con nomi localizzati nel pannello). Link alla root di ogni lingua in nav: etichetta **`HOME`** (stesso testo in tutte le lingue). L’`<header class="site-header">` ha **`translate="no"`** sul blocco lingua così i traduttori automatici del browser non alterano codici lingua (**IT**, **ES**) né le etichette della chrome.

### Tema chiaro / scuro

- **`js/theme-init.js`**: script **sincrono** subito dopo `<meta charset>` nell’`<head>` di ogni pagina pubblica — legge `localStorage` (`aml-theme` = `light` | `dark`) e imposta `data-theme` su `<html>` **prima** del paint, per ridurre il flash.
- **`js/nav.js`**: badge carrello; **toggle tema** (`<button id="theme-toggle" type="button">`, sole/luna via CSS) in **`.header-end`** dopo `.lang-dropdown`; etichette **aria-label** Chiaro/Scuro (o Light/Dark) per lingua; tema da **`prefers-color-scheme`** finché l’utente non salva una scelta in `localStorage`.

---

## Architettura prevista (directory)

```
/
├── it/ , en/ , de/ , fr/ , es/   # index, cart, checkout, account, order-success (mirror)
├── css/               # style.css custom, leggero
├── fonts/             # Inter .woff2 + OFL (no Google Fonts runtime)
├── js/                # cart.js, auth.js
├── img/
│   ├── favicon/       # sorgente PNG + icon-32.webp, apple-touch (ICO solo in root)
│   └── logo/          # header WebP (srcset 200 / 400)
├── functions/         # API Pages (products, checkout, webhook, download, admin)
├── admin/             # CMS / bonifici (protezione Cloudflare Access)
├── wrangler.toml
├── _headers           # cache lungo su /fonts (Cloudflare Pages)
└── schema.sql         # schema D1
```

I dettagli operativi e le regole di sviluppo sono in [`.cursorrules`](.cursorrules).

---

## Roadmap

Piano di lavoro e checklist per fase: **[`ROADMAP.md`](ROADMAP.md)**.

---

## Sviluppo locale

```bash
npm install
# Applica lo schema D1 in locale (una volta, o dopo modifiche a schema.sql)
npm run db:local
# Se il DB locale esisteva prima della tabella order_lines:
# npx wrangler d1 execute aml-store-d1 --local --file=migrations/001-order-lines.sql
# Colonna fulfillment su products (digitale / fisico); se la colonna esiste già, ignora l’errore “duplicate column”:
# npx wrangler d1 execute aml-store-d1 --local --file=migrations/003-products-fulfillment.sql
# Copertina catalogo (path /img/products/… su D1); se la colonna esiste già, ignora “duplicate column”:
# npx wrangler d1 execute aml-store-d1 --local --file=migrations/004-products-cover-image.sql
# Opzionale: rimuove prodotto demo slug e2e-verify-product (solo se presente):
# npx wrangler d1 execute aml-store-d1 --local --file=migrations/005-remove-e2e-demo-product.sql
# Pagine prodotto statiche (HTML per /it/products/{slug}.html …) da D1 locale — eseguire prima del commit/deploy:
# npm run build:product-pages
# Opzionale: SITE_ORIGIN=https://tuodominio.it npm run build:product-pages
# (Il prezzo/testo nelle schede HTML è lo snapshot al momento della generazione: rigenera dopo cambi su D1.)
# Avvio Pages + Functions + asset statici
npm run dev
```

- **HOME** (root lingua): **`/it/`**, **`/en/`**, **`/de/`**, **`/fr/`**, **`/es/`** (es. `http://127.0.0.1:8788/it/`). **Carrello**: `/it/cart.html`; **checkout**: `/it/checkout.html` (e speculari per le altre lingue). Porta predefinita di wrangler **8788**; se occupata, wrangler ne sceglie un’altra.
- API catalogo: `GET /api/products?lang=it` (valori supportati tra gli altri: `en`, `de`, `fr`, `es`).
- Carrello / checkout: `POST /api/cart-verify` (prezzi da D1), `POST /api/order-draft` (ordine `pending_checkout` + righe `order_lines`). Pagine: `cart.html`, `checkout.html`, `order-success.html`, `account.html` sotto ogni prefisso lingua.
- Carrello / auth (scheletro): [`js/cart.js`](js/cart.js), [`js/auth.js`](js/auth.js).

### Immagini (favicon e logo)

- **Favicon:** sorgente `img/favicon/favicon.png`. `npm run build:images` produce `icon-32.webp`, `apple-touch-icon.png` e `/favicon.ico`.
- **Logo:** asset committati `img/logo/logo-header-200.webp` e `logo-header-400.webp`. Per un rebrand sostituisci prima il **400px** (export dal design), poi esegui `npm run build:images` per rigenerare il **200px** e le varianti **`logo-header-*-light.webp`** (testo chiaro + blu brand dalla media di `favicon.png`, vedi [`scripts/build_logo_light.py`](scripts/build_logo_light.py)).

```bash
pip install pillow
npm run build:images
```

### Tipografia (performance)

Font **Inter** in `/fonts/` (pesi **400** e **600**, subset **latin** + **latin-ext** per le lingue storefront). `font-display: swap`, **preload** dei due file 400 nelle home (`it` / `en` / `de` / `fr` / `es`), `unicode-range` nel CSS così il browser scarica solo i glifi necessari. Licenza: [`fonts/OFL-Inter.txt`](fonts/OFL-Inter.txt).

Per aggiornare i file WOFF2: pacchetto `@fontsource/inter` su [jsDelivr](https://www.jsdelivr.com/package/npm/@fontsource/inter) → cartella `files/`, stessi nomi o aggiorna `style.css` + preload.

**D1 in cloud:** crea il database con `npx wrangler d1 create aml-store-d1`, copia l’UUID in `wrangler.toml` (`database_id`) al posto del placeholder, poi applica lo schema in remoto con `npx wrangler d1 execute aml-store-d1 --remote --file=schema.sql`.

Per variabili e segreti (Stripe, Fattura24, email, ecc.) usa la dashboard Cloudflare (**Settings → Functions → Secrets**) oppure `wrangler secret put …`. **Non** committare chiavi: vedi [`.gitignore`](.gitignore) (es. `.dev.vars`).

---

## Sicurezza (sintesi “Vault”)

- Download solo dopo verifica ordine su **D1**, con link **firmati** e TTL breve (es. 15 minuti).
- Area **admin** protetta (es. **Cloudflare Access**); audit su `admin_audit_logs`.
- Notifiche e stato “pagato”: logica **attendibile** lato server (es. **webhook Stripe** firmato), non basata solo sulla pagina di ringraziamento.

---

## Trustpilot (TrustBox)

Lo **script bootstrap v5** è già nell’`<head>` di ogni pagina in `it/`, `en/`, `de/`, `fr/`, `es/` (`index.html`, `checkout.html`, `account.html`, `order-success.html`), nello stesso formato fornito da Trustpilot: commenti `<!-- TrustBox script -->` / `<!-- End TrustBox script -->` e `src="//widget.trustpilot.com/bootstrap/v5/tp.widget.bootstrap.min.js"` con `type="text/javascript"` e **`async`**.

Quando sei pronto: dalla dashboard **Trustpilot Business** genera lo snippet del widget (markup con `class="trustpilot-widget"` e attributi `data-*`) e incollalo nel **`<body>`** nel punto che preferisci (es. footer della HOME, colonna checkout). **Non** reinserire un secondo script bootstrap sulla stessa pagina.

---

## Licenza e contributi

Progetto proprietario / uso interno salvo diversa indicazione. Per modifiche strutturali seguire la roadmap e le convenzioni in `.cursorrules`.
