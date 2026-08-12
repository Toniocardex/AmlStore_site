-- Aggiunge il flag bot alle pageview: prima i bot riconosciuti (Googlebot,
-- crawler SEO, ecc. — vedi BOT_UA_RE in functions/api/_lib/analytics.js)
-- venivano scartati e mai scritti; ora vengono registrati con is_bot = 1,
-- cosi' il pannello Analytics puo' mostrare il traffico bot separatamente
-- dai visitatori reali invece di farlo sparire senza lasciare traccia.
--
-- npx wrangler d1 execute aml-orders --file=schema-analytics-bot-migration.sql
-- npx wrangler d1 execute aml-orders --file=schema-analytics-bot-migration.sql --remote

ALTER TABLE page_views ADD COLUMN is_bot INTEGER NOT NULL DEFAULT 0;

CREATE INDEX IF NOT EXISTS idx_page_views_day_is_bot ON page_views(day, is_bot);
