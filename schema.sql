-- D1 schema — Aml-Store.com (multilingua, Vault, audit)
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT NOT NULL UNIQUE,
  title_it TEXT NOT NULL,
  title_en TEXT NOT NULL,
  title_de TEXT NOT NULL,
  title_fr TEXT NOT NULL,
  title_es TEXT NOT NULL,
  description_it TEXT NOT NULL DEFAULT '',
  description_en TEXT NOT NULL DEFAULT '',
  description_de TEXT NOT NULL DEFAULT '',
  description_fr TEXT NOT NULL DEFAULT '',
  description_es TEXT NOT NULL DEFAULT '',
  price_cents INTEGER NOT NULL CHECK (price_cents >= 0),
  currency TEXT NOT NULL DEFAULT 'EUR',
  cover_image TEXT,
  r2_key TEXT,
  active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
  fulfillment TEXT NOT NULL DEFAULT 'digital',
  sort_order INTEGER,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_products_active_sort
  ON products (active, sort_order, id);

CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cart_token TEXT NOT NULL UNIQUE,
  status TEXT NOT NULL,
  lang TEXT NOT NULL,
  billing_json TEXT NOT NULL,
  customer_email TEXT,
  total_cents INTEGER,
  currency TEXT,
  stripe_session_id TEXT,
  stripe_payment_intent TEXT,
  idempotency_key TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_orders_status ON orders (status);
CREATE INDEX IF NOT EXISTS idx_orders_stripe_session ON orders (stripe_session_id);

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

CREATE TABLE IF NOT EXISTS download_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL REFERENCES orders (id) ON DELETE CASCADE,
  product_id INTEGER NOT NULL REFERENCES products (id) ON DELETE CASCADE,
  client_ip TEXT,
  user_agent TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_download_logs_order ON download_logs (order_id);

CREATE TABLE IF NOT EXISTS admin_audit_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  action TEXT NOT NULL,
  actor TEXT,
  subject_type TEXT,
  subject_id TEXT,
  meta_json TEXT,
  client_ip TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_admin_audit_created ON admin_audit_logs (created_at DESC);

-- Dati di esempio (solo sviluppo / demo catalogo HOME; idempotente su slug)
INSERT OR IGNORE INTO products (
  slug,
  title_it, title_en, title_de, title_fr, title_es,
  description_it, description_en, description_de, description_fr, description_es,
  price_cents, currency, r2_key, active, fulfillment, sort_order
)
VALUES
  (
    'vault-starter-kit',
    'Vault Starter Kit',
    'Vault Starter Kit',
    'Vault Starter Kit',
    'Pack d''introduction Vault',
    'Kit de inicio Vault',
    'Pacchetto digitale introduttivo per testare il flusso acquisto e download protetto.',
    'Introductory digital bundle to exercise purchase and protected download flow.',
    'Digitales Einstiegspaket zum Testen von Kauf und geschütztem Download.',
    'Pack numérique d''introduction pour tester l''achat et le téléchargement sécurisé.',
    'Paquete digital introductorio para probar la compra y la descarga protegida.',
    1990,
    'EUR',
    NULL,
    1,
    'digital',
    10
  ),
  (
    'compliance-checklist-pdf',
    'Checklist conformità (PDF)',
    'Compliance checklist (PDF)',
    'Compliance-Checkliste (PDF)',
    'Checklist conformité (PDF)',
    'Lista de verificación de cumplimiento (PDF)',
    'PDF con checklist operativa per fatturazione elettronica e conservazione documenti.',
    'Operational PDF checklist for e-invoicing and document retention.',
    'PDF mit operativer Checkliste für E-Rechnung und Aufbewahrung.',
    'PDF avec checklist opérationnelle pour la facturation électronique et l''archivage.',
    'PDF con lista de verificación operativa para facturación electrónica y archivo.',
    490,
    'EUR',
    NULL,
    1,
    'physical',
    20
  );
