-- Cart tracking (analytics fase 1 — carrelli abbandonati)
-- npx wrangler d1 execute aml-orders --file=schema-cart-tracking-migration.sql
-- npx wrangler d1 execute aml-orders --file=schema-cart-tracking-migration.sql --remote

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
-- schema-checkout-rate-limit-migration.sql: CREATE TABLE IF NOT EXISTS è
-- idempotente, quindi eseguire questa migration è sicuro anche se quella
-- tabella esiste già.
CREATE TABLE IF NOT EXISTS checkout_rate_buckets (
    bucket_key   TEXT NOT NULL,
    window_id    TEXT NOT NULL,
    count        INTEGER NOT NULL DEFAULT 0,
    updated_at   TEXT NOT NULL,
    PRIMARY KEY (bucket_key, window_id)
);
CREATE INDEX IF NOT EXISTS idx_rate_buckets_updated ON checkout_rate_buckets(updated_at);
