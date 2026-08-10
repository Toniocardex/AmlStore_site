-- Analytics interna (visite giornaliere, provenienza) — tracking server-side
-- via functions/_middleware.js, nessun cookie, nessun ID persistente.
-- npx wrangler d1 execute aml-orders --file=schema-analytics-migration.sql
-- npx wrangler d1 execute aml-orders --file=schema-analytics-migration.sql --remote

CREATE TABLE IF NOT EXISTS page_views (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    day           TEXT NOT NULL,   -- 'YYYY-MM-DD' UTC, per aggregazioni
    ts            TEXT NOT NULL,   -- ISO timestamp esatto
    path          TEXT NOT NULL,   -- pathname pulito (senza query string)
    locale        TEXT,
    referrer_host TEXT,            -- hostname del Referer; NULL se diretto o same-site
    utm_source    TEXT,
    country       TEXT,            -- ISO-2 da request.cf.country
    device        TEXT,            -- 'mobile' | 'tablet' | 'desktop'
    visitor_hash  TEXT NOT NULL    -- HMAC(ip+ua, salt-per-giorno) — non riconducibile all'IP
);

CREATE INDEX IF NOT EXISTS idx_page_views_day         ON page_views(day);
CREATE INDEX IF NOT EXISTS idx_page_views_day_path     ON page_views(day, path);
CREATE INDEX IF NOT EXISTS idx_page_views_day_referrer ON page_views(day, referrer_host);
CREATE INDEX IF NOT EXISTS idx_page_views_day_visitor  ON page_views(day, visitor_hash);
