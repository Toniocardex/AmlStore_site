-- Aml Store — Richieste "Avvisami quando torna disponibile" (solo SKU fisici)
-- Eseguire con:
--   npx wrangler d1 execute aml-orders --file=schema-restock-migration.sql
--   npx wrangler d1 execute aml-orders --file=schema-restock-migration.sql --remote
--
-- Ciclo di vita di una riga:
--   1. iscrizione       -> email valorizzata, notified_at NULL  (= domanda in attesa)
--   2. rifornimento     -> notified_at valorizzato, email azzerata a NULL
--   3. annullamento     -> riga cancellata
--
-- L'email viene messa a NULL subito dopo l'invio: il dato personale serve solo
-- per quella singola notifica, mentre la riga resta come segnale di domanda
-- storica (quante richieste ha raccolto uno SKU, e quanto e' rimasto scoperto).
-- L'indice unico tollera piu' righe notificate per lo stesso SKU perche' in
-- SQLite i NULL non collidono fra loro in un UNIQUE.

CREATE TABLE IF NOT EXISTS restock_requests (
    id           TEXT PRIMARY KEY,
    sku          TEXT NOT NULL,
    email        TEXT,
    lang         TEXT NOT NULL DEFAULT 'it',
    page_path    TEXT,
    token        TEXT NOT NULL UNIQUE,
    created_at   TEXT NOT NULL,
    notified_at  TEXT,
    ip_hash      TEXT
);

-- Una sola iscrizione in attesa per (SKU, email): il secondo invio dallo stesso
-- indirizzo non deve gonfiare il conteggio della domanda.
CREATE UNIQUE INDEX IF NOT EXISTS idx_restock_sku_email
    ON restock_requests(sku, email);

-- Lettura calda: "chi e' in attesa per questo SKU".
CREATE INDEX IF NOT EXISTS idx_restock_pending
    ON restock_requests(sku, notified_at);
