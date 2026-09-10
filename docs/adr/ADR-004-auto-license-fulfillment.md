# ADR-004 — Consegna automatica delle licenze digitali dal pool D1

*Specifica implementabile per Eurolicenze / Licensoft — il codice deve seguire questo documento, non il contrario.*

| Campo | Valore |
|---|---|
| Stato | Accettato |
| Data | 10 settembre 2026 |
| Ambito | Evasione post-pagamento delle licenze ESD; pool chiavi D1; email Resend; admin |
| Sistema | Cloudflare Pages Functions, D1 `aml-orders`, Resend |
| Proprietario | Licensoft / Eurolicenze |
| Versione | 1.0 |
| Relazioni | Non implementa ADR-001 (antifrode). La consegna resta **dopo** pagamento catturato, come oggi. ADR-001 §16.4 cita la consegna automatica come trigger di riesame: questa v1 non introduce account cliente, wallet, né un risk gate prima della chiave. |

## 1. Decisione in una frase

Quando un ordine è **pagato** e il pool D1 contiene chiavi **sufficienti** per tutte le righe digitali, il backend assegna quelle chiavi e invia al cliente la **stessa email di consegna** del generatore admin. Se anche una sola chiave manca, il comportamento resta **identico a oggi**: conferma ordine + notifica interna “inviare manualmente”.

## 2. Contesto

Oggi, dopo Stripe/PayPal catturato o bonifico marcato pagato:

1. email di conferma ordine al cliente (senza chiave);
2. email interna a Desk e all’indirizzo operativo: “PAGAMENTO CONFERMATO: inviare manualmente la licenza”;
3. l’operatore copia il riepilogo nel generatore `/admin/email-license-generator.html` e spedisce via Zoho.

I template di consegna esistono già in `functions/api/_lib/templates.js` (`licenseSubject`, `licenseEmailHtml`, `licenseEmailText`) e sono portati 1:1 nel generatore. Non sono usati da Resend.

In D1 non c’è un magazzino chiavi. `product_stock` è solo DVD/COA.

## 3. Principi non negoziabili

1. **Assenza di chiave = flusso attuale.** Nessuna seconda email, nessuna assegnazione, testo interno invariato (`DA INVIARE MANUALMENTE`).
2. **Presenza di chiavi sufficienti = stessa mail del generatore**, spedita da Resend, non un template nuovo.
3. **All-or-nothing sulle righe digitali.** Se l’ordine chiede 2 chiavi dello SKU A e 1 dello SKU B e ne manca una, non si assegna nulla e non si manda la mail di consegna.
4. **La conferma ordine parte sempre**, con o senza pool (come oggi). La mail licenza è **aggiuntiva**, mai sostitutiva.
5. **Solo SKU non fisici.** `physical: true` non pesca dal pool; resta Magazzino + “SPEDIRE FISICAMENTE”.
6. **Solo dopo pagamento catturato.** Bonifico `pending_payment`: nessuna chiave. PayPal/Stripe pending o importo non coerente: nessuna chiave (invariato rispetto agli hook attuali).
7. **Idempotenza.** Retry webhook e doppio capture non riassegnano e non reinviano. Una chiave ha al più un `order_id`; una riga ha al più un `emailed_at`.
8. **Niente chiavi nei log, nelle API pubbliche, nella conferma ordine.** In chiaro solo: mail al cliente, dettaglio ordine admin (Access).
9. **Pagamento non si blocca** se la tabella licenze non esiste ancora (migrazione non applicata): fail-soft sul flusso manuale.
10. **Il generatore Zoho resta** come ripiego quando il pool è vuoto o l’evasione automatica non copre.

## 4. Contratto operativo

| Situazione | Email cliente | Email interna | Pool |
|---|---|---|---|
| Pagato, pool copre tutte le qty digitali | Conferma **e** mail licenza (markup generatore) | Licenza inviata automaticamente | Chiavi `assigned` + `emailed_at` |
| Pagato, pool insufficiente o vuoto | Solo conferma (attuale) | Manuale (attuale) | Invariato |
| Pagato, solo articoli fisici | Conferma | Spedire fisicamente (attuale) | `license_status = not_applicable` |
| Pagato, misto digitale+fisico, pool copre il digitale | Conferma + mail licenza per il digitale | Digitale auto + fisico da spedire | Solo le righe digitali |
| Pagato, misto, pool non copre il digitale | Solo conferma | Digitale manuale + fisico da spedire | Nessuna assegnazione |
| Bonifico pending | IBAN (attuale) | Attendere pagamento | Nessuna |
| Mail licenza fallita dopo assegnazione | Conferma già partita | Trattare come da completare (retry, non rilasciare chiavi) | Restano `assigned`, `emailed_at` NULL |

**Parziale non si autoinvia.** Meglio una mail in meno che una consegna incompleta e chiavi già bruciate.

## 5. Schema D1

### 5.1 `license_keys`

| Colonna | Tipo | Note |
|---|---|---|
| `id` | TEXT PK | id opaco (`lk_` + hex) |
| `sku` | TEXT NOT NULL | SKU catalogo |
| `key_norm` | TEXT NOT NULL UNIQUE | `trim` + lower; dedup import |
| `key_material` | TEXT NOT NULL | originale trimmed, mai loggato |
| `status` | TEXT NOT NULL | `available` \| `assigned` |
| `order_id` | TEXT | valorizzato se `assigned` |
| `assigned_at` | TEXT ISO | |
| `emailed_at` | TEXT | NULL = non ancora nella mail di consegna |
| `imported_at` | TEXT NOT NULL | |
| `imported_by` | TEXT | email admin JWT |

Indici: `(sku, status)`, `order_id`.

Assegnazione atomica (un statement SQLite, `status = 'available'` nella WHERE). Due worker concorrenti non prendono la stessa riga.

### 5.2 Colonne su `orders`

| Colonna | Note |
|---|---|
| `license_status` | `pending` \| `fulfilled` \| `not_applicable`. NULL = ordini precedenti alla feature |
| `license_email_sent_at` | prima mail di consegna riuscita (COALESCE, non blocca un eventuale retry su chiavi non ancora `emailed_at`) |
| `license_email_event_src` | es. `webhook_stripe`, `worker_capture`, `license_import` |

`pending` = ordine pagato con almeno una riga digitale non ancora coperta. Non si usa `partial` in v1: o si evadono tutte le digitali, o si resta `pending`.

File: `schema-licenses-migration.sql` (ALTER + CREATE per DB esistenti) e gli stessi oggetti in `schema.sql`. `scripts/dev-d1-init.py` applica CREATE e ALTER ignorando `duplicate column`.

## 6. Flusso runtime

Dopo lo stesso momento in cui oggi si fa `deductStockForOrderRow` (ordine già `paid`):

```
deduct stock fisico (invariato, idempotente)
→ tentativo assign all-or-nothing sulle qty digitali
→ se assegnato tutto: sendLicenseDeliveryOnce (markup generatore)
→ sendConfirmationOnce / sendPaidNotificationOnce (invariato, idempotente)
→ sendInternalOrderNotificationOnce (testo in base all’esito)
```

Innesti obbligatori (stesso helper, anche sui retry):

- `fulfilPaidStripeOrder`
- `handlePaypalCaptureOrder`
- webhook PayPal `PAYMENT.CAPTURE.COMPLETED`
- `markBankTransferPaid` **prima** della mail interna

La mail licenza e l’assegnazione stanno **fuori** dal `if (wasUnpaid)` / `if (status !== 'paid')` delle email di conferma, come lo stock: un retry deve poter completare `emailed_at` se la prima mail licenza è fallita.

### 6.1 Import chiavi

`POST /api/admin/licenses/import` **solo** inserisce nel pool (`available`). Non tocca gli ordini già pagati.

La pesca dal pool avviene **solo** sugli hook di pagamento catturato (§6): il prossimo ordine pagato con chiavi sufficienti riceve la mail del generatore.

`POST /api/webhooks/resend` (firma Svix) aggiorna `license_email_delivery` (`delivered` / `bounced` / …) sulla riga che ha `license_email_resend_id`. Se il webhook arriva prima di `markLicenseEmailSent`, fallback sui tag `kind=license` + `order_id` (e si memorizza l’id Resend). Senza `RESEND_WEBHOOK_SECRET` l’invio licenza continua; il feed resta su “Accettata Resend”.

## 7. Email

### 7.1 Consegna licenza

`sendLicenseDeliveryOnce` in `email.js`:

- `from` / `reply_to` come le altre transazionali (`Eurolicenze <ordini@eurolicenze.com>`, `Desk@eurolicenze.com`);
- corpo: `licenseSubject` / `licenseEmailHtml` / `licenseEmailText`;
- `items[]`: `{ productName, sku, key, activation }` con `activation` dalla stessa euristica del generatore (`detectActivation` sul nome prodotto);
- niente BCC Trustpilot (resta sulla conferma pagata);
- se `customer_email` vuoto: non inviare, chiavi restano assigned, retry successivo.

### 7.2 Interna

Se `fulfillment.status === 'fulfilled'`: oggetto e corpo dicono che la licenza è partita in automatico; per riga digitale “INVIATA AUTOMATICAMENTE”; i fisici restano “SPEDIRE FISICAMENTE”.

Altrimenti: **copy attuale**, incluse le stringhe `DA INVIARE MANUALMENTE` e `inviare manualmente la licenza` (vincolo per `scripts/validate-order-notifications.py`).

## 8. API admin (Cloudflare Access)

| Route | Ruolo |
|---|---|
| `GET /api/admin/licenses` | Riepilogo pool + feed invii automatici (senza materiale chiavi) |
| `GET /api/admin/licenses?sku=` | Chiavi **disponibili mascherate** |
| `POST /api/admin/licenses/import` | `{ sku, keys }` testo o array; duplicati `key_norm` ignorati |
| `POST /api/admin/licenses/revoke` | Solo `available` |
| `GET /api/admin/orders/:id` | + `licenseStatus`, `licenseEmailSentAt`, chiavi assegnate **in chiaro** |
| `POST /api/admin/orders/:id/fulfill` | Riprova orchestratore su ordine già `paid` |

Import: max 500 chiavi, lunghezza max 256, scarta vuote/`#`. SKU deve esistere in catalogo e non essere `physical`.

`listOrders` espone `licenseStatus` (badge in lista).

## 9. UI admin

Nuova tab **Licenze** (`#licenses`): import, tabella pool, elimina disponibili, feed invii automatici (Resend accettato vs email non partita). Magazzino resta **solo fisico**.

Dettaglio ordine: stato evasione, chiavi, pulsante Riprova se `paid` e non `fulfilled`. Link al generatore invariato.

## 10. Sicurezza e limiti

- Admin = stesso JWT Access delle altre mutation (`validateAdminMutationRequest` + origin).
- Chiavi disponibili in lista: maschera (prime 4 + ultime 4).
- Nessun endpoint pubblico di stock digitale.
- Fail-soft se `no such table: license_keys` o colonna `license_*` assente.
- Non cifrare a riposo in v1 (D1 già non pubblico; Access sull’admin). Documentato come debito.

## 11. Test e go-live

- `scripts/test-licenses.mjs`: parse, dedup, `digitalNeedFromItems`, all-or-nothing (logica pura). Incluso in `npm test`.
- `validate-order-notifications.py` resta verde sul ramo manuale.
- Verifica locale (`pages dev` + `npm run dev:db`):
  1. SKU senza pool → solo conferma + interna manuale;
  2. import + ordine pagato → seconda mail markup generatore, interna auto;
  3. retry webhook → niente doppia chiave / doppia mail licenza;
  4. SKU fisico → pool ignorato.
- Migrazione D1 **remote** prima che il codice nuovo sia l’unico in produzione.

## 12. Ordine di implementazione

1. Schema + `dev-d1-init.py` + nota `wrangler.toml`
2. `functions/api/_lib/licenses.js` + test
3. `sendLicenseDeliveryOnce` + interna condizionale
4. Helper post-pagamento negli innesti §6
5. Route admin
6. Tab Licenze + dettaglio ordine
7. Test locale end-to-end

## 13. Fuori da questa v1

- Cifratura chiavi a riposo
- Revoca/rilascio su refund
- Scorte digitali in vetrina o JSON-LD
- Unire conferma e licenza in un’unica mail
- Risk gate ADR-001 prima della chiave
- Account cliente / wallet
- Invio automatico di articoli fisici

## 14. Checklist implementativa

- [x] `schema-licenses-migration.sql` + colonne/tabella in `schema.sql`
- [x] `licenses.js` all-or-nothing + fail-soft
- [x] Resend usa i tre export `license*` di `templates.js`
- [x] Stripe, PayPal (capture + webhook), bonifico mark-paid
- [x] Conferma ordine invariata in assenza di pool
- [x] Interna invariata in assenza di pool
- [x] Admin import / revoke / fulfill / dettaglio
- [x] Test unitari + `npm test` (`test:licenses`)
- [x] `wrangler d1 execute` locale e remote — applicata il 2026-09-10 su `aml-orders` (produzione) e `aml-store-preview`
