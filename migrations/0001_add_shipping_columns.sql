-- Aml Store — migrazione 0001: colonne spedizione per articoli fisici (DVD/COA)
-- Da eseguire UNA SOLA VOLTA sul database D1 esistente (locale o produzione):
--   wrangler d1 execute aml-orders --file=migrations/0001_add_shipping_columns.sql
--   wrangler d1 execute aml-orders --remote --file=migrations/0001_add_shipping_columns.sql
-- Non necessaria per un database creato da zero con schema.sql (colonne gia' incluse).

ALTER TABLE orders ADD COLUMN requires_shipping      INTEGER NOT NULL DEFAULT 0;
ALTER TABLE orders ADD COLUMN shipping_address_line1 TEXT;
ALTER TABLE orders ADD COLUMN shipping_city          TEXT;
ALTER TABLE orders ADD COLUMN shipping_postal_code   TEXT;
ALTER TABLE orders ADD COLUMN shipping_province      TEXT;
ALTER TABLE orders ADD COLUMN shipping_country       TEXT;

CREATE INDEX IF NOT EXISTS idx_orders_requires_shipping ON orders(requires_shipping);
