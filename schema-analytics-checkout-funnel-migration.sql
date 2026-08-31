-- Funnel di checkout — posizione raggiunta dal cliente prima di fermarsi.
--
-- Aggiunge cart_id ad analytics_events: senza questa colonna gli eventi del
-- funnel restano aggregati e non si possono ricollegare al carrello che li ha
-- generati. Con il join su cart_sessions(id) si risponde alla domanda che
-- conta davvero — "questo carrello abbandonato, fin dove era arrivato?" — e si
-- recupera anche l'email, che cart_sessions aggancia dal campo email del
-- checkout (vedi notifyEmail() in js/cart.js).
--
-- ATTENZIONE: ALTER TABLE ... ADD COLUMN non e' idempotente in SQLite (non
-- esiste IF NOT EXISTS per le colonne). Va eseguita UNA SOLA VOLTA per
-- ambiente: una seconda esecuzione fallisce con "duplicate column name".
-- L'indice invece e' ripetibile.
--
-- npx wrangler d1 execute aml-orders --file=schema-analytics-checkout-funnel-migration.sql
-- npx wrangler d1 execute aml-orders --file=schema-analytics-checkout-funnel-migration.sql --remote

ALTER TABLE analytics_events ADD COLUMN cart_id TEXT;

CREATE INDEX IF NOT EXISTS idx_analytics_events_cart ON analytics_events(cart_id);

-- Il funnel si legge per event_name in ordine di posizione:
--   checkout_view             arrivo sul checkout con carrello non vuoto
--   checkout_contact_started  primo dato anagrafico digitato
--   checkout_contact_completed anagrafica valida: la sezione pagamento si sblocca
--   checkout_payment_started  interazione con la sezione pagamento
--   checkout_pay_clicked      click sul bottone di pagamento
--   purchase                  ordine andato a buon fine (gia' tracciato)
