-- Aml Store - Migrazione notifiche interne ordine
-- Aggiunge flag idempotenti per evitare doppie email operative interne.
--
-- Eseguire con:
--   npx wrangler d1 execute aml-orders --file=schema-internal-notification-migration.sql --remote
--
-- SQLite/D1 non supporta sempre ALTER TABLE ... IF NOT EXISTS:
-- se ricevi "duplicate column name", la migrazione e' gia' applicata.

ALTER TABLE orders ADD COLUMN internal_notification_sent_at TEXT;
ALTER TABLE orders ADD COLUMN internal_notification_event_src TEXT;
