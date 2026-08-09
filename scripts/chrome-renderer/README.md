# chrome-renderer — sorgente del markup di header e footer

Questi due file **non vengono mai serviti ai browser**. Sono la versione dei web
component precedente alla conversione in light DOM: costruiscono il markup di
header e footer dentro uno Shadow DOM.

`scripts/build-inline-chrome.mjs` li inietta al posto di `components/*.js`
mentre carica ogni pagina, legge il markup che producono e lo scrive nell'HTML.

Divisione dei ruoli dopo la conversione:

| file | ruolo | arriva al browser |
|---|---|---|
| `scripts/chrome-renderer/header.js` | genera il **markup** (solo build) | no |
| `components/header.js` | aggancia il **comportamento** al markup gia' presente | sì |
| `css/header.css` | gli **stili**, estratti da qui con `extract-chrome-css.mjs` | sì |

## Come modificare la navigazione o il footer

1. Modificare il template in **questi** file (è l'unico posto in cui il markup esiste).
2. Se sono cambiati anche gli stili, rigenerare i fogli:
   `node scripts/extract-chrome-css.mjs`
3. Rigenerare il markup nelle pagine (serve il dev server attivo):
   `node scripts/build-inline-chrome.mjs`
4. Aggiornare gli hash di cache: `python scripts/bump-asset-version.py`

Il codice di comportamento presente in questi file è un residuo della versione
precedente e non viene usato: durante la build serve solo il template. Il
comportamento vivo è quello di `components/`.
