# Checklist go-live — aml-store.com

> **Prima di ogni deploy**: eseguire `python scripts/bump-asset-version.py`
> (aggiorna gli hash `?v=` di css/js nelle pagine: senza, i browser dei
> clienti tengono i file vecchi fino a 7 giorni per via della cache).

Stato al 2026-07-17. Il codice è pronto (redirect migrazione, URL senza `.html`,
fix checkout, PayPal parametrizzato). Restano i passi qui sotto, che richiedono
accessi ai pannelli (Cloudflare, PayPal, Stripe, Resend, registrar).

## 0. Database D1 — migrazione spedizione ✅ eseguita 2026-07-18

Colonne di spedizione (`requires_shipping`, `shipping_address_line1`,
`shipping_city`, `shipping_postal_code`, `shipping_province`,
`shipping_country`) applicate al D1 di produzione `aml-orders` via
`migrations/0001_add_shipping_columns.sql` — verificate presenti con
`PRAGMA table_info(orders)`. Nessuna azione ulteriore richiesta.

## 1. Secrets Cloudflare Pages (obbligatori)

Da eseguire nel progetto Pages (`aml-store`), valori **live**:

```
wrangler pages secret put TOKEN_SECRET          # stringa random ≥32 caratteri
wrangler pages secret put STRIPE_SECRET_KEY     # sk_live_...
wrangler pages secret put STRIPE_WEBHOOK_SECRET # whsec_... (webhook → /api/webhooks/stripe)
wrangler pages secret put PAYPAL_CLIENT_ID      # Client ID app PayPal LIVE
wrangler pages secret put PAYPAL_CLIENT_SECRET  # Client Secret app PayPal LIVE
wrangler pages secret put RESEND_API_KEY        # re_...
wrangler pages secret put TRUSTPILOT_BCC        # facoltativo: ...@invite.trustpilot.com
```

Note:
- `PAYPAL_BASE_URL` in wrangler.toml è già **live** (`https://api-m.paypal.com`).
  Il frontend prende il Client ID da `/api/paypal-config`: non c'è più nulla di
  hardcodato. In locale la sandbox arriva da `.dev.vars` (vedi `.dev.vars.example`).
- Webhook Stripe: crearlo sul dominio definitivo
  (`https://aml-store.com/api/webhooks/stripe`, evento `checkout.session.completed`)
  e usare il suo signing secret.

## 2. Resend (email ordini) — ⚠ DNS non configurato (verificato 2026-07-17)

`resend._domainkey.aml-store.com` e `send.aml-store.com` **non esistono**: il
dominio non è verificato su Resend e le email da `ordini@aml-store.com` non
partiranno. Su resend.com → Domains → Add `aml-store.com`, poi aggiungere al DNS
Cloudflare i record che propone (DKIM TXT + SPF/MX sul sottodominio di invio) e
attendere lo stato "Verified".

La casella di supporto/reply-to `Info@amlstore.it` è su un **dominio diverso**
(amlstore.it, MX register.it — esiste e riceve). Se non è voluto, cambiare
`REPLY_TO`/`INTERNAL_RECIPIENTS` in `functions/api/_lib/email.js`.

## 3. Taglio DNS / dominio

1. Collegare il progetto Pages al dominio `aml-store.com` (custom domain).
2. Mantenere il redirect `www.aml-store.com` → `aml-store.com` (Bulk Redirect o
   regola esistente): tutti i canonical/sitemap usano l'apex.
3. Il vecchio shop resta raggiungibile finché non si punta il DNS: fare lo
   switch solo dopo il punto 1 e 2.

## 4. Verifiche post-deploy (5 minuti)

```
curl -I https://aml-store.com/                 # 301 → /it/
curl -I https://aml-store.com/it/windows-11-pro  # 200
curl -I https://aml-store.com/it/sistema-operativo/windows-11-pro-licenza-esd-originale  # 301 un solo hop
curl -I https://aml-store.com/schema.sql       # 302 → /it/ (non deve servire il file)
curl -I https://www.aml-store.com/it/          # 301 → apex
curl    https://aml-store.com/api/paypal-config  # {"clientId":"<live>"}
```

Poi un ordine di prova reale per metodo (carta, PayPal, bonifico) e controllo
email cliente + notifica interna.

## 5. Search Console

1. Aggiungere/verificare la proprietà `aml-store.com` (dominio).
2. Inviare `https://aml-store.com/sitemap.xml` (380 URL).
3. Monitorare Copertura/Pagine per 4–8 settimane: i vecchi URL devono passare
   a "Pagina con reindirizzamento", senza 404 in crescita.

## 6. Facoltativi consigliati

- Analytics: Consent Mode v2 e cookie banner sono già pronti, ma nessun tag
  GA4/GTM è installato — decidere se aggiungerlo prima del lancio.
- CSP/HSTS in `_headers` (irrigidimento, non bloccante).
