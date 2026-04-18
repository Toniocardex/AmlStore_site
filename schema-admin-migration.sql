-- Aml Store — Migrazione admin panel
-- Aggiunge colonne per gestione ordini amministrativa e soft-archive.
--
-- Eseguire con:
--   npx wrangler d1 execute aml-orders --file=schema-admin-migration.sql --remote
--
-- Idempotente: usa ALTER TABLE ... IF NOT EXISTS non supportato da SQLite,
-- quindi eseguire una sola volta. In caso di errore "duplicate column" è sicuro ignorarlo.

ALTER TABLE orders ADD COLUMN archived_at              TEXT;
ALTER TABLE orders ADD COLUMN marked_paid_at           TEXT;
ALTER TABLE orders ADD COLUMN marked_paid_by           TEXT;   -- email admin da JWT
ALTER TABLE orders ADD COLUMN admin_notes              TEXT;
ALTER TABLE orders ADD COLUMN paid_notification_sent_at TEXT;  -- flag idempotenza 2a email bonifico

-- Indici aggiuntivi
CREATE INDEX IF NOT EXISTS idx_orders_archived ON orders(archived_at);
