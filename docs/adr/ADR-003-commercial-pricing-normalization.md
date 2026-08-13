# ADR-003 — Normalizzazione commerciale dei prezzi pubblici EUR

## Decisione

Il prezzo economicamente sostenibile resta il risultato del calcolo interno,
inclusa la maggiorazione per i costi di pagamento. Prima di essere pubblicato,
il prezzo viene trasformato dalla policy centrale in
`scripts/commercial_pricing.py`.

- sotto 50 € il prezzo resta invariato;
- da 50 € in su il prezzo EUR viene arrotondato per eccesso all'euro intero;
- l'arrotondamento non si applica a MSRP/listini esterni (`compareAtMinor`);
- override manuali ed esclusioni `preserve-cents` sono dichiarati per SKU in
  `scripts/commercial-pricing-policy.json`;
- un override manuale può discostarsi dal calcolo automatico quando approvato
  come decisione commerciale esplicita;
- valute diverse da EUR conservano il comportamento corrente.

Il valore finale in `catalog.json` e `functions/api/_lib/catalog.js` è l'unico
prezzo usato da pagine, carrello, checkout, ordini ed email. Per equilibrio
visivo e coerenza fra card e riepiloghi, il frontend mostra sempre due decimali:
il valore commerciale resta intero (per esempio 144,00 €), mentre i prodotti
low-ticket mantengono i propri centesimi effettivi.

## Migrazione e verifica

`scripts/normalize-commercial-prices.py` produce sempre prima il report
`scripts/_commercial_pricing_report.json`. Senza flag opera in dry-run; con
`--apply` aggiorna cataloghi e copie statiche SKU-aware. Il report include SKU,
nome, valore grezzo, proposta, delta assoluto/percentuale e presenza di override.

La policy e la coerenza frontend/backend sono verificate da:

```text
python scripts/test-commercial-pricing.py
python scripts/validate-pricing-policy.py
```

Gli indici di ricerca vanno rigenerati dopo l'applicazione con
`python scripts/build-search-index.py`.
