-- Una tantum su DB creati prima delle colonne DE/FR/ES:
-- npx wrangler d1 execute aml-store-d1 --local --file=migrations/002-products-eu-langs.sql

ALTER TABLE products ADD COLUMN title_de TEXT NOT NULL DEFAULT '';
ALTER TABLE products ADD COLUMN title_fr TEXT NOT NULL DEFAULT '';
ALTER TABLE products ADD COLUMN title_es TEXT NOT NULL DEFAULT '';
ALTER TABLE products ADD COLUMN description_de TEXT NOT NULL DEFAULT '';
ALTER TABLE products ADD COLUMN description_fr TEXT NOT NULL DEFAULT '';
ALTER TABLE products ADD COLUMN description_es TEXT NOT NULL DEFAULT '';

UPDATE products SET
  title_de = 'Vault Starter Kit',
  title_fr = 'Pack d''introduction Vault',
  title_es = 'Kit de inicio Vault',
  description_de = 'Digitales Einstiegspaket zum Testen von Kauf und geschütztem Download.',
  description_fr = 'Pack numérique d''introduction pour tester l''achat et le téléchargement sécurisé.',
  description_es = 'Paquete digital introductorio para probar la compra y la descarga protegida.'
WHERE slug = 'vault-starter-kit';

UPDATE products SET
  title_de = 'Compliance-Checkliste (PDF)',
  title_fr = 'Checklist conformité (PDF)',
  title_es = 'Lista de verificación de cumplimiento (PDF)',
  description_de = 'PDF mit operativer Checkliste für E-Rechnung und Aufbewahrung.',
  description_fr = 'PDF avec checklist opérationnelle pour la facturation électronique et l''archivage.',
  description_es = 'PDF con lista de verificación operativa para facturación electrónica y archivo.'
WHERE slug = 'compliance-checklist-pdf';
