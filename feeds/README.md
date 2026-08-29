# Feed Google Shopping

Feed prodotto per Google Merchant Center / campagne Shopping, uno per lingua.

## Rigenerazione

```
python scripts/build-google-shopping-feed.py
```

Da rieseguire ogni volta che cambiano pagine prodotto o prezzi (nessun
hook/CI: promemoria manuale come `bump-asset-version.py`). I file `*.xml`
in questa cartella sono generati — non modificarli a mano.

Opzioni:
- `--with-sale-price` — usa `compareAtMinor` come `g:price` e il prezzo reale
  come `g:sale_price` quando c'e' sconto (default: `g:price` = prezzo reale,
  nessun `sale_price`, cosi' combacia 1:1 con la landing e non innesca i
  controlli "prezzo di listino" di Google).
- `--langs it en` — genera solo alcune lingue.

## Fonte dati

- Prezzo, titolo, descrizione, URL, immagine, brand, disponibilita': blocco
  JSON-LD `Product` di ogni pagina `<lang>/<slug>.html` (gia' tradotto,
  gia' allineato al prezzo a video).
- EAN/GTIN, MPN, categoria merceologica: `catalog.json`, join sullo SKU.

62 prodotti per lingua. Bundle e alcuni antivirus non hanno GTIN ne MPN:
per quelli il feed manda `g:identifier_exists = no` (corretto per Google).

## Setup in Merchant Center

Una volta deployato, ogni feed e' raggiungibile a
`https://eurolicenze.com/feeds/google-shopping-<lang>.xml`.

In Merchant Center: **Prodotti -> Feed -> aggiungi feed**, metodo
"fetch programmato" con quell'URL. Un feed per combinazione paese/lingua.
Tutti i prezzi sono in **EUR**, quindi i paesi vanno scelti nell'area euro.
Abbinamento consigliato (modificabile in `COUNTRY_BY_LANG` nello script):

| Feed | Lingua | Paese di destinazione |
|------|--------|-----------------------|
| `google-shopping-it.xml` | it | Italia |
| `google-shopping-es.xml` | es | Spagna |
| `google-shopping-de.xml` | de | Germania (anche Austria) |
| `google-shopping-fr.xml` | fr | Francia (anche Belgio) |
| `google-shopping-nl.xml` | nl | Paesi Bassi (anche Belgio) |
| `google-shopping-pt.xml` | pt | Portogallo |
| `google-shopping-en.xml` | en | Irlanda (unico paese EUR anglofono) |

Per il Regno Unito servirebbe un listino separato in GBP: il sito non ce
l'ha, quindi il feed `en` resta in EUR/Irlanda.

## Note

- Prodotti digitali ESD: in Merchant Center impostare la spedizione a 0
  (consegna del codice via email) a livello di account/paese.
- `g:product_type` usa la tassonomia interna in italiano di `catalog.json`
  per tutte le lingue: e' un campo non mostrato agli utenti, Google
  accetta qualsiasi lingua. `g:google_product_category` invece e' sul
  percorso ufficiale Google.
- `g:item_group_id` raggruppa le varianti per numero di dispositivi
  (bitdefender-plus, eset-nod32, kaspersky-premium, mcafee-total-protection).
