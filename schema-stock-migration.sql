-- Aml Store — Magazzino prodotti fisici (DVD/COA)
-- Eseguire con:
--   npx wrangler d1 execute aml-orders --file=schema-stock-migration.sql
--   npx wrangler d1 execute aml-orders --file=schema-stock-migration.sql --remote
--
-- Nessun seed qty: riga assente = 0 in lettura (non vendibile finché Admin non imposta).

CREATE TABLE IF NOT EXISTS product_stock (
    sku         TEXT PRIMARY KEY,
    qty         INTEGER NOT NULL CHECK (qty >= 0),
    updated_at  TEXT NOT NULL,
    updated_by  TEXT
);

CREATE TABLE IF NOT EXISTS stock_deductions (
    order_id     TEXT PRIMARY KEY,
    deducted_at  TEXT NOT NULL
);
