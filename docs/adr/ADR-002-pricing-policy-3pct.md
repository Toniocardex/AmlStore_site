# ADR-002 — Pricing Policy: applicazione markup strutturale del 3%

> Nota: la trasformazione del risultato grezzo in prezzo pubblico è ora
> disciplinata da ADR-003. La maggiorazione del 3% resta un input economico,
> ma non determina più i centesimi esposti al cliente.

Status: Accepted
Project: AML STORE
Repository: `Toniocardex/AmlStore_site`
Date: 2026-08-08
Decision type: Pricing / Catalog / Checkout / Frontend consistency

## Contesto

AML STORE adotta una nuova politica di pricing. I prezzi di vendita
presenti nel catalogo al 2026-08-08 sono stati incrementati del 3%.
L'obiettivo commerciale è duplice:

1. incorporare nel prezzo di vendita una quota equivalente alla tariffa
   di pagamento presa come riferimento;
2. abbandonare deliberatamente il ricorso sistematico ai classici prezzi
   psicologici (`19,99 €`, `59,99 €`, `199,99 €`, ecc.).

Il nuovo listino mantiene i prezzi matematicamente risultanti dal
calcolo, anche quando generano valori apparentemente insoliti come
`81,37 €` o `184,37 €`. Non sono stati normalizzati verso `.99`, `.95`,
`.90`, interi o altre soglie psicologiche: è una scelta intenzionale.

## Decisione

Per ogni prezzo di vendita corrente:

```
newUnitAmountMinor = floor((oldUnitAmountMinor * 103 + 50) / 100)
```

Integer math sui minor units (centesimi), un solo arrotondamento, NON la
formula di gross-up `prezzo / 0,97`. Vedi `apply_pricing_policy_minor()`
in [`scripts/apply-pricing-policy-3pct.py`](../../scripts/apply-pricing-policy-3pct.py).

Il markup è una politica di listino, non una payment surcharge: il
prezzo pubblico è identico su Stripe, PayPal e bonifico bancario. Non
esiste alcun `+3%` applicato nel checkout o nei payment adapter.

`compareAtMinor` NON riceve automaticamente il +3% (rappresenta un
prezzo di confronto/listino, non il prezzo soggetto alla nuova policy).
Quando `newUnitAmountMinor > compareAtMinor` (può succedere quando
`compareAtMinor === unitAmountMinor` prima della migrazione),
`compareAtMinor` viene allineato a `newUnitAmountMinor`.

## Migrazione (one-shot)

Lo script [`scripts/apply-pricing-policy-3pct.py`](../../scripts/apply-pricing-policy-3pct.py):

1. congela la baseline pre-migrazione in
   `scripts/_pricing_policy_pre_migration_snapshot.json` e si rifiuta di
   ripartire se quel file esiste già (protezione contro doppia
   applicazione);
2. aggiorna `functions/api/_lib/catalog.js` (autorità backend) e
   `catalog.json` (artifact derivato);
3. aggiorna, in modo SKU-aware (non global string replace), tutte le
   rappresentazioni pubbliche del prezzo in `it/en/fr/de/es/*.html`:
   `data-stripe-unit-amount`, `data-stripe-compare-at-amount`,
   `data-discount-percent`, prezzi visibili (`€ X,XX`), `aria-label`,
   `meta[property="product:price:amount"]`, `"price"` in JSON-LD;
4. scrive un report (`scripts/_pricing_policy_migration_report.json`)
   con la mappa old→new per SKU e i contatori di sostituzione.

`scripts/build-catalog.py` (legacy, rigenera da un CSV esterno non
versionato) applica ora la stessa `apply_pricing_policy_minor()` così da
non poter reintrodurre accidentalmente i prezzi pre-migrazione se
rieseguito. `scripts/align-catalog-prices.py` resta un artefatto storico
(hardcoded pairs per un singolo bump precedente) e non va esteso: per
futuri cambi di prezzo su tutto il catalogo usare l'approccio SKU-aware
di `apply-pricing-policy-3pct.py`.

## Validazione

[`scripts/validate-pricing-policy.py`](../../scripts/validate-pricing-policy.py)
verifica: casi noti della funzione di pricing, invarianti di catalogo
(`unitAmountMinor > 0`, `currency === 'EUR'`,
`compareAtMinor >= unitAmountMinor`), parità frontend/backend per ogni
pagina prodotto e card categoria/home, parità tra le 5 lingue, e assenza
di doppia applicazione del +3% rispetto allo snapshot baseline.

## Non-goals

Nessuna modifica a commissioni PayPal/Stripe, payment surcharge, cambio
valuta, IVA dinamica, pricing per paese o per metodo di pagamento,
pricing differenziato, dynamic pricing, psychological pricing, o
modifica del provider di pagamento.
