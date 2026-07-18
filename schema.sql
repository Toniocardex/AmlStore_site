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
