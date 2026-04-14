-- Tipo consegna: digital | physical (spedizione).
-- DB esistenti: npx wrangler d1 execute aml-store-d1 --local --file=migrations/003-products-fulfillment.sql

ALTER TABLE products ADD COLUMN fulfillment TEXT NOT NULL DEFAULT 'digital';

-- Demo: un PDF digitale + un articolo fisico di test (spedizione)
UPDATE products SET fulfillment = 'digital' WHERE slug = 'vault-starter-kit';
UPDATE products SET fulfillment = 'physical' WHERE slug = 'compliance-checklist-pdf';
