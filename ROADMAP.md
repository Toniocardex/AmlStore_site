# Roadmap Aml-Store.com (The Vault Edition)

Documento vivo: aggiorna **Stato avanzamento** e le checkbox dopo ogni passo completato (in chat o in commit).

## Legenda stato

| Simbolo | Significato |
|--------|---------------|
| `[ ]` | Da fare |
| `[~]` | In corso |
| `[x]` | Completato |

---

## Stato avanzamento (sintesi)

| Fase | Nome | Stato |
|------|------|--------|
| 0 | Fondamenta locale e regole | Completata |
| 1 | Primo task (wrangler, D1, `/it/` + prodotti) | Completata |
| 2 | Struttura sito multilingua e asset | Completata |
| 3 | Carrello, checkout, account | Completata |
| 4 | Stripe e Fattura24 | Da fare |
| 5 | Download Vault (R2 firmati) | Da fare |
| 6 | Admin (La Cassaforte) e bonifici | In corso |
| 7 | SEO, performance, deploy | In corso |

*Ultimo aggiornamento: 2026-04-14 — **Fase 6 (parziale):** cartella `/admin` operativa (La Cassaforte), API `/api/admin/*` con `ADMIN_API_SECRET`, prodotti/ordini su D1, upload R2 opzionale, `admin_audit_logs` sulle mutazioni prodotti; **manca** Access in prod e flusso **conferma bonifico**. **Fase 7 (parziale):** schede statiche `/{lang}/products/{slug}.html` (`npm run build:product-pages`), JSON-LD `Product` sulle schede, link dal catalogo, `cover_image` + `/img/products/`; **manca** rifinitura **layout** scheda prodotto, analytics checkout, OG 1200×630 se serve, PageSpeed/deploy finali.*

---

## Fase 0 — Fondamenta e vincoli

- [x] Regole progetto in `.cursorrules` (Vanilla, Cloudflare, Vault)
- [x] Repository Git inizializzato (branch `main`, commit iniziale con `.cursorrules`, `ROADMAP.md`, `.gitignore`)
- [x] `ROADMAP.md` presente e coerente con il progetto (aggiornare data e checkbox dopo ogni milestone, come da sezione in calce)

---

## Fase 1 — Primo task (da `.cursorrules`)

- [x] `wrangler.toml` per dominio **Aml-Store.com** (Pages + D1; R2 commentato fino alla fase download)
- [x] `schema.sql` D1: `products` (multilingua), `orders` (`cart_token` UNIQUE, `status`, `lang`, `billing_json`), `download_logs`, `admin_audit_logs`
- [x] Cartella `/it/` con `index.html` base (SEO base; `hreflang` esteso in seguito a cinque lingue)
- [x] Caricamento prodotti da D1 via **Vanilla JS** — `functions/api/products.js` → **`GET /api/products`**

---

## Fase 2 — Struttura directory e lingue storefront

- [x] `/en/` speculare a `/it/` (`index.html`, stessi pattern + switch lingua)
- [x] `/de/`, `/fr/`, `/es/` speculari (index, checkout, account, order-success) con `hreflang` a cinque lingue + switcher
- [x] `/css/style.css` unico, leggero, custom *(header lingua + hero `.webp` in Fase 2)*
- [x] `/js/cart.js`, `/js/auth.js` (carrello in `localStorage` + stub sessione / `signInUrl`)
- [x] `/img/` con risorse **.webp** (favicon + logo header `srcset`; PNG sorgente solo `img/favicon/favicon.png`)

---

## Fase 3 — Pagine core e-commerce

- [x] `checkout.html` in `/it/`, `/en/`, `/de/`, `/fr/`, `/es/` (carrello + form fatturazione elettronica SDI/PEC, prezzi da **`POST /api/cart-verify`**)
- [x] **`order-success.html`** in tutte e cinque le lingue — messaggio statico + nota se `?session_id=` (verifica server in Fase 4); Stripe `success_url` punterà qui
- [x] `account.html` in tutte e cinque le lingue (placeholder storico ordini + auth futura)
- [x] Integrazione carrello: **`POST /api/order-draft`** (ordine `pending_checkout` + `order_lines` in D1), pulsanti catalogo (HOME) → `cart.js`, **`js/nav.js`** badge carrello
- [x] **`cart.html`** in `/it/`, `/en/`, `/de/`, `/fr/`, `/es/` — revisione carrello separata dal checkout; **`js/cart-lines.js`** condiviso con `checkout.js` per `POST /api/cart-verify`

---

## Fase 4 — Pagamenti e fatturazione

- [ ] `functions/api/create-checkout.js`: sessione Stripe con **price_data** da D1 (niente Price ID fissi)
- [ ] Custom fields Stripe: P.IVA, SDI, PEC (o equivalente richiesto)
- [ ] `functions/api/webhook.js`: Stripe → aggiornamento ordini / trigger **Fattura24**; **invio email al titolare solo qui**, in risposta al **webhook di successo post-checkout** (es. `checkout.session.completed` con pagamento effettivamente completato — fonte di verità attendibile). **Nessun** invio email dalla pagina thank-you / redirect lato browser
- [ ] **Contenuto email titolare** (stesso handler webhook): **nome cliente**, **email cliente**, **numero ordine**, **articolo/i acquistato/i**; provider posta (es. Resend, Mailchannels, SendGrid via Worker) e secret dedicato in Cloudflare
- [ ] **Idempotenza webhook**: su retry Stripe dello stesso evento (es. stesso `event.id`), niente **doppie email**, niente **doppi** aggiornamenti ordine / Fattura24 — persistenza idempotency in D1 o controllo stato già processato
- [ ] **Sicurezza post-acquisto (cliente “furbo”)**: webhook accettato **solo** con **verifica firma** Stripe (`STRIPE_WEBHOOK_SECRET`); nessun passaggio a “pagato” o consegna digitale basato su **solo** parametri URL / localStorage / manipolazione thank-you; eventuali dettagli ordine in pagina success: **solo** dopo **conferma lato server** (es. `checkout.sessions.retrieve` + coerenza con D1), mai fiducia cieca del client; `cart_token` / riferimenti ordine **opachi e non enumerabili**; rate limiting ove utile su API sensibili (download, lookup ordine)
- [ ] Secrets Cloudflare: `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `FATTURA24_API_KEY`
- [ ] `CLERK_SECRET_KEY` solo se si usa Clerk per l’area account

---

## Fase 5 — Vault download

- [ ] `functions/api/download.js`: verifica pagamento su D1, URL firmato R2, **scadenza 15 minuti**
- [ ] Log su `download_logs` (IP, timestamp, riferimenti utili)

---

## Fase 6 — Admin (La Cassaforte) e bonifici

- [x] Cartella **`/admin`**: dashboard (`index.html`), catalogo CMS (`products.html`), `admin.css` / `admin.js` (Vanilla); sessione **Bearer** `ADMIN_API_SECRET` (commenti sicurezza: Access in prod)
- [x] **`functions/api/admin/`**: middleware auth; **`GET/POST /api/admin/products`**, **`PATCH /api/admin/products/:id`**, **`GET /api/admin/orders`**; upload file digitale **`POST …/upload`** su R2 se binding `VAULT`; lib `admin-auth`, `audit`, `slug`, `cover-image`
- [x] Scritture su **`admin_audit_logs`** su creazione/patch/upload prodotto (best-effort)
- [ ] Protezione reale con **Cloudflare Zero Trust (Access)** su `/admin/*` in produzione
- [ ] **`functions/api/admin/`** (o route dedicata): **conferma bonifico** → aggiorna D1 + Fattura24 (come da `.cursorrules` originario)

---

## Fase 7 — SEO, qualità, go-live

- [x] `hreflang` + menu lingua **a cinque lingue** (pannello in `<details>`; codice ISO nel `summary`) e `x-default` su **home, cart, checkout, account, order-success** per ogni prefisso URL
- [x] Meta description **home** per **tutte e cinque le lingue** (stesso messaggio brand, tradotto): IT, EN, DE, FR, ES — vedi `*/index.html`
- [x] **Open Graph** + **Twitter Card** (`summary_large_image`) + **JSON-LD** (`Organization` + `WebSite` con `inLanguage` BCP-47) sulle cinque home — immagine social: `logo-header-400.webp` (URL assoluto)
- [x] **Trustpilot TrustBox**: snippet ufficiale (commenti `TrustBox script` / `End TrustBox script`, `type="text/javascript"`, `src="//widget…bootstrap.min.js"`, `async`) nell’`<head>` di **tutte** le pagine pubbliche `it|en|de|fr|es` (`index`, `cart`, `checkout`, `account`, `order-success`) — i **div** widget nel body quando li generi da Trustpilot Business
- [x] **`<title>`**: home (`*/index.html`) = **`Aml-Store`** (allineati anche `og:title`, `twitter:title`, JSON-LD `name` su Organization/WebSite); altre pagine pubbliche = *nome pagina* ` — Aml-Store` (senza `.com` nel titolo scheda)
- [x] **Tema chiaro/scuro**: `data-theme` su `<html>`, `<button id="theme-toggle">` in `nav.js` (click + **aria-label** per lingua), init sincrono `theme-init.js` + variabili CSS (`prefers-color-scheme` se nessuna scelta salvata)
- [x] **Header**: link **HOME** sotto il logo; riga azioni **`.header-end`**: **Carrello** e **Account** (`.user-nav`) + **dropdown lingua** (`.lang-dropdown`) + toggle tema; seconda riga `util-nav` rimossa
- [x] **Pagina carrello** `/{lang}/cart.html` (cinque lingue): righe da `POST /api/cart-verify` via `js/cart-lines.js` + `js/cart-page.js`, CTA verso checkout; icona carrello / hero → carrello; checkout mantiene riepilogo + form (`checkout.js` usa lo stesso modulo righe)
- [~] **Checkout layout tipo Shopify**: griglia 2 colonne (`checkout-layout`), riepilogo a sinistra + **card scura** fatturazione (`checkout-form--pane`), aside **sticky** su desktop; link «modifica carrello»; **hook analytics** funnel (page view / eventi) ancora da fare
- [x] **Schede prodotto statiche** per SEO/CWV: URL `/{lang}/products/{slug}.html` generate da **`npm run build:product-pages`** (lettura D1 **locale** via wrangler; opz. `SITE_ORIGIN=`); contenuto titolo/descrizione/prezzo nel **primo HTML**; **canonical**, **hreflang** (×5 + `x-default`), **OG**, **JSON-LD `Product`** + **`Offer`**; `js/product-page.js` (carrello); rigenerare dopo cambi catalogo su D1 (snapshot prezzi/testi)
- [x] **`cover_image`** su D1 (migrazione `004`): path pubblico **`/img/products/…`** (file in repo + deploy); catalogo home mostra copertina se valorizzata; validazione server path
- [x] **Catalogo home**: link titolo prodotto → scheda statica `/{lang}/products/{slug}.html`
- [~] **Layout / design scheda prodotto** oltre al template attuale (gerarchia visiva, mobile, coerenza totale con `style.css`) — da progettare/rifinire
- [ ] Immagine OG dedicata **1200×630** se serve massima compatibilità social (le schede prodotto usano già `Product` + immagine copertina o logo)
- [ ] Test locale: `npx wrangler pages dev`
- [ ] Deploy Cloudflare Pages + verifica PageSpeed (obiettivo ~100)
- [ ] Controllo finale sicurezza (admin, download, segreti non in repo)

---

## Come aggiornare questa roadmap

1. Completato un passo: cambia `[ ]` in `[x]` (o `[~]` se lavori a metà).
2. Aggiorna la tabella **Stato avanzamento** e la data *Ultimo aggiornamento*.
3. Se aggiungi nuovi task dalle `.cursorrules` o dalla chat, inseriscili nella fase giusta con una nuova riga `[ ]`.

---

## Riferimento vincoli (riassunto)

- Frontend: **solo** HTML/CSS/JS vanilla (no React, Tailwind, jQuery).
- Backend: **Cloudflare Pages Functions** in `/functions`.
- Lingue: cartelle fisiche **`/it/`**, **`/en/`**, **`/de/`**, **`/fr/`**, **`/es/`**.
