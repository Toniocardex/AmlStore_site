-- Eventi CRO oltre alle sole pageview già tracciate in page_views: click su
-- PayPal Express, buy-now, esiti PayPal, purchase. Stesso modello privacy
-- delle pageview — nessun cookie, visitor_hash HMAC che ruota ogni giorno,
-- fail-open (mai nel path critico di un acquisto). Vedi TRACKABLE_EVENTS in
-- functions/api/_lib/analytics.js per l'elenco degli event_name ammessi.
--
-- npx wrangler d1 execute aml-orders --file=schema-analytics-events-migration.sql
-- npx wrangler d1 execute aml-orders --file=schema-analytics-events-migration.sql --remote

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
