-- Aml Store — D1 schema
-- Eseguire con: wrangler d1 execute aml-orders --file=schema.sql
-- Per produzione aggiungere --remote

CREATE TABLE IF NOT EXISTS orders (
    id                           TEXT PRIMARY KEY,         -- UUID v4, orderId pubblico
    idempotency_key              TEXT UNIQUE NOT NULL,     -- previene ordini doppi
    status                       TEXT NOT NULL DEFAULT 'pending_payment',
    -- status: pending_payment | paid | cancelled | refunded

    created_at                   TEXT NOT NULL,            -- ISO 8601
    paid_at                      TEXT,
    updated_at                   TEXT NOT NULL,

    -- Cliente
    customer_email               TEXT NOT NULL,
    customer_first_name          TEXT NOT NULL,
    customer_last_name           TEXT NOT NULL,
    customer_company             TEXT,
    customer_type                TEXT NOT NULL DEFAULT 'private',  -- private | business
    customer_phone               TEXT,
    customer_piva                TEXT,
    customer_sdi                 TEXT,
    customer_pec                 TEXT,
    locale                       TEXT NOT NULL DEFAULT 'it',       -- it|en|fr|de|es

    -- Spedizione (solo ordini con almeno un articolo fisico: DVD/COA)
    requires_shipping            INTEGER NOT NULL DEFAULT 0,       -- 0|1
    shipping_address_line1       TEXT,
    shipping_city                TEXT,
    shipping_postal_code         TEXT,
    shipping_province            TEXT,
    shipping_country             TEXT,

    -- Righe ordine (JSON congelato al momento dell'acquisto)
    line_items                   TEXT NOT NULL,            -- JSON: [{sku,name,qty,unit_amount,currency}]
    total_minor                  INTEGER NOT NULL,         -- centesimi (es. 1999 = €19.99)
    currency                     TEXT NOT NULL DEFAULT 'EUR',

    -- Metodo pagamento
    payment_method               TEXT NOT NULL,            -- stripe | paypal | bank_transfer

    -- Riferimenti PSP (per riconciliazione e supporto)
    stripe_session_id            TEXT,
    stripe_payment_intent        TEXT,
    paypal_order_id              TEXT,
    paypal_capture_id            TEXT,

    -- Traccia operativa
    confirmation_email_sent_at   TEXT,                    -- idempotenza: null = non ancora inviata
    confirmation_email_event_src TEXT,                    -- webhook_stripe|webhook_paypal|worker_capture|bank_transfer_created
    internal_notification_sent_at TEXT,                   -- idempotenza notifica interna ordine
    internal_notification_event_src TEXT,                 -- webhook_stripe|worker_capture|bank_transfer_created

    -- Admin panel
    archived_at                  TEXT,                    -- soft-archive (NULL = attivo)
    marked_paid_at               TEXT,                    -- timestamp conferma manuale bonifico
    marked_paid_by               TEXT,                    -- email admin da JWT
    admin_notes                  TEXT,                    -- note opzionali admin
    paid_notification_sent_at    TEXT                     -- idempotenza 2a email bonifico (pagamento confermato)
);

-- Indici per lookup rapidi
CREATE INDEX IF NOT EXISTS idx_orders_stripe_session  ON orders(stripe_session_id);
CREATE INDEX IF NOT EXISTS idx_orders_paypal_order    ON orders(paypal_order_id);
CREATE INDEX IF NOT EXISTS idx_orders_status          ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_customer_email  ON orders(customer_email);
CREATE INDEX IF NOT EXISTS idx_orders_created_at      ON orders(created_at);
CREATE INDEX IF NOT EXISTS idx_orders_archived        ON orders(archived_at);
CREATE INDEX IF NOT EXISTS idx_orders_requires_shipping ON orders(requires_shipping);

-- Magazzino prodotti fisici. Incluso anche in schema-stock-migration.sql per
-- aggiornare in sicurezza database creati prima dell'introduzione dello stock.
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

-- Tracking carrelli (analytics, fase 1 — vedi schema-cart-tracking-migration.sql
-- per l'aggiunta sicura a database creati prima di questa feature).
CREATE TABLE IF NOT EXISTS cart_sessions (
    id                   TEXT PRIMARY KEY,   -- UUID, un ciclo di vita carrello (non il browser)
    email                TEXT,               -- opzionale, agganciata dal campo email di checkout
    locale               TEXT NOT NULL DEFAULT 'it',
    country              TEXT,               -- ISO-2 da request.cf.country

    line_items           TEXT NOT NULL,      -- JSON snapshot ultimo stato: [{sku,name,qty,unit_amount_minor,currency}]
    item_count           INTEGER NOT NULL DEFAULT 0,  -- lines.length, calcolato server-side ad ogni sync
    total_minor          INTEGER NOT NULL DEFAULT 0,
    currency             TEXT NOT NULL DEFAULT 'EUR',

    created_at           TEXT NOT NULL,
    updated_at           TEXT NOT NULL,      -- ultimo sync: base per "inattivo da N ore"

    checkout_started_at  TEXT,               -- valorizzato quando è stato creato un ordine (pending_payment incluso)
    checkout_order_id    TEXT                -- FK logica a orders.id — la conversione vera si legge da orders.status
);

CREATE INDEX IF NOT EXISTS idx_cart_sessions_updated_at  ON cart_sessions(updated_at);
CREATE INDEX IF NOT EXISTS idx_cart_sessions_email       ON cart_sessions(email);
CREATE INDEX IF NOT EXISTS idx_cart_sessions_checkout_id ON cart_sessions(checkout_order_id);
CREATE INDEX IF NOT EXISTS idx_cart_sessions_country     ON cart_sessions(country);
CREATE INDEX IF NOT EXISTS idx_cart_sessions_item_count  ON cart_sessions(item_count);

-- Rate limit generico (email di checkout, IP di cart/sync). Incluso anche in
-- schema-checkout-rate-limit-migration.sql per aggiornare in sicurezza
-- database creati prima dell'introduzione del rate limit.
CREATE TABLE IF NOT EXISTS checkout_rate_buckets (
    bucket_key   TEXT NOT NULL,
    window_id    TEXT NOT NULL,
    count        INTEGER NOT NULL DEFAULT 0,
    updated_at   TEXT NOT NULL,
    PRIMARY KEY (bucket_key, window_id)
);
CREATE INDEX IF NOT EXISTS idx_rate_buckets_updated ON checkout_rate_buckets(updated_at);

-- Eventi CRO (click PayPal Express, buy-now, purchase, ecc.) oltre alle sole
-- pageview. Incluso anche in schema-analytics-events-migration.sql per
-- aggiornare in sicurezza database creati prima di questa feature.
CREATE TABLE IF NOT EXISTS analytics_events (
    id            TEXT PRIMARY KEY,
    event_name    TEXT NOT NULL,
    order_id      TEXT,
    sku           TEXT,
    visitor_hash  TEXT NOT NULL,
    created_at    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_events_name_created ON analytics_events(event_name, created_at);
CREATE INDEX IF NOT EXISTS idx_analytics_events_order        ON analytics_events(order_id);
