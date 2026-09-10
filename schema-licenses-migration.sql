-- Eurolicenze — Pool chiavi digitali + stato evasione ordine (ADR-004)
-- Eseguire con:
--   npx wrangler d1 execute aml-orders --file=schema-licenses-migration.sql
--   npx wrangler d1 execute aml-orders --file=schema-licenses-migration.sql --remote
--
-- SQLite/D1 non supporta sempre ALTER TABLE ... IF NOT EXISTS:
-- se ricevi "duplicate column name", la migrazione e' gia' applicata
-- sulle colonne; la CREATE TABLE e gli indici sono idempotenti.

CREATE TABLE IF NOT EXISTS license_keys (
    id            TEXT PRIMARY KEY,
    sku           TEXT NOT NULL,
    key_norm      TEXT NOT NULL UNIQUE,
    key_material  TEXT NOT NULL,
    status        TEXT NOT NULL DEFAULT 'available',
    order_id      TEXT,
    assigned_at   TEXT,
    emailed_at    TEXT,
    imported_at   TEXT NOT NULL,
    imported_by   TEXT
);

CREATE INDEX IF NOT EXISTS idx_license_keys_sku_status ON license_keys(sku, status);
CREATE INDEX IF NOT EXISTS idx_license_keys_order      ON license_keys(order_id);

ALTER TABLE orders ADD COLUMN license_status TEXT;
ALTER TABLE orders ADD COLUMN license_email_sent_at TEXT;
ALTER TABLE orders ADD COLUMN license_email_event_src TEXT;
ALTER TABLE orders ADD COLUMN license_email_resend_id TEXT;
ALTER TABLE orders ADD COLUMN license_email_delivery TEXT;

CREATE INDEX IF NOT EXISTS idx_orders_license_status ON orders(license_status);
CREATE INDEX IF NOT EXISTS idx_orders_license_resend ON orders(license_email_resend_id);
