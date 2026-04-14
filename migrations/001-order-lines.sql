-- Esegui su D1 già inizializzato (prima senza order_lines):
-- npx wrangler d1 execute aml-store-d1 --local --file=migrations/001-order-lines.sql
-- npx wrangler d1 execute aml-store-d1 --remote --file=migrations/001-order-lines.sql

CREATE TABLE IF NOT EXISTS order_lines (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL REFERENCES orders (id) ON DELETE CASCADE,
  product_id INTEGER REFERENCES products (id) ON DELETE SET NULL,
  slug TEXT NOT NULL,
  title_snapshot TEXT NOT NULL,
  qty INTEGER NOT NULL CHECK (qty > 0 AND qty <= 99),
  unit_price_cents INTEGER NOT NULL,
  currency TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_order_lines_order ON order_lines (order_id);
