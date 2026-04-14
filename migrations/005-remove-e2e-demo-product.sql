-- Rimuove eventuale prodotto di test creato durante integrazione API (slug e2e-verify-product).
DELETE FROM products WHERE slug = 'e2e-verify-product';
