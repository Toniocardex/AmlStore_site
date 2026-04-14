# Aml Store — sito statico

Entry point in root: **`index.html`** (ad esempio `https://tuodominio.pages.dev/`).

Flusso: **GitHub** (questo repo) → integrazione **Cloudflare Pages** → **deploy automatico** a ogni push sul branch collegato (es. `main`).

## Cloudflare Pages

| Impostazione        | Valore        |
|---------------------|---------------|
| Framework preset    | Nessuno       |
| Build command       | *(vuoto)*     |
| Build output dir    | *(vuoto)*     |
| Root directory      | *(repo root)* |

Non c’è `package.json`: il deploy pubblica solo file statici dalla root del repository.
