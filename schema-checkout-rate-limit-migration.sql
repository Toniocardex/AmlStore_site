-- Checkout rate-limit bridge (ADR-001 Fase 0.5)
-- npx wrangler d1 execute aml-orders --file=schema-checkout-rate-limit-migration.sql
-- npx wrangler d1 execute aml-orders --file=schema-checkout-rate-limit-migration.sql --remote

CREATE TABLE IF NOT EXISTS checkout_rate_buckets (
    bucket_key TEXT NOT NULL,
    window_id  TEXT NOT NULL,
    count      INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (bucket_key, window_id)
);

CREATE INDEX IF NOT EXISTS idx_rate_buckets_updated
    ON checkout_rate_buckets(updated_at);
