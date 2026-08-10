-- Aggiunge il tracking di "quale lingua avrebbe suggerito il banner
-- <aml-lang-suggest>" alle pageview esistenti. Calcolato server-side da
-- Accept-Language (functions/api/_lib/analytics.js), stesso algoritmo del
-- componente client (components/lang-suggest.js): copre il 100% delle
-- pageview, non solo quelle in cui il banner arriva a montarsi lato client.
--
-- npx wrangler d1 execute aml-orders --file=schema-lang-suggest-migration.sql
-- npx wrangler d1 execute aml-orders --file=schema-lang-suggest-migration.sql --remote

ALTER TABLE page_views ADD COLUMN suggested_lang TEXT;

CREATE INDEX IF NOT EXISTS idx_page_views_day_suggested_lang ON page_views(day, suggested_lang);
