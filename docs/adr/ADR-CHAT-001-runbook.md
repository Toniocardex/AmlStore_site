# ADR-CHAT-001 rev1.2 — Runbook operativo

## Invarianti

- Il pubblico è esclusivamente guest: nessun account, login, password o magic link.
- `customer_id` resta sempre `NULL`.
- Timeline e ordine autorevoli vivono nel Conversation Durable Object.
- D1 è solo query model globale.
- Disabilitare la feature non autorizza cancellazioni o rollback distruttivi.

## Sviluppo locale

1. Copiare le variabili chat da `.dev.vars.example` a `.dev.vars` e sostituire tutti i secret di esempio.
2. Generare VAPID con `npx web-push generate-vapid-keys`.
3. Avviare `npm run dev:support` e `npm run dev` in due terminali.
4. Eseguire `npm run dev:db` dopo il primo avvio per inizializzare tutti i database Miniflare.
5. Verificare `/api/chat/availability`, `/admin/support/` e il trigger locale `/cdn-cgi/local/scheduled` del Worker.

Pages e Worker condividono `.wrangler/state-chat` soltanto in locale, perché devono vedere lo stesso D1. Lo storage resta fisicamente locale e non è il database production.

## Ambienti Cloudflare

Development, preview e production devono avere identificativi distinti per:

- D1;
- namespace Durable Object/Worker;
- `CHAT_GUEST_SESSION_SECRET` e `CHAT_CONTACT_LOOKUP_SECRET`;
- coppia VAPID;
- URL e policy Cloudflare Access.

Non riutilizzare mai database ID o secret production nei file preview. I file versionati contengono solo nomi di binding e valori non segreti. Gli ID reali preview vanno impostati nella configurazione dell'ambiente Cloudflare prima del primo deploy.

## Deploy

**Stato 2026-08-24:** passi 1–5 completati sia in preview sia in produzione
(dettaglio in `docs/adr/ADR-CHAT-001-implementation-plan.md` §0.2: D1 migrato,
secret e VAPID impostati — valori distinti tra preview e produzione — Worker e
Pages deployati). `CHAT_ENABLED` resta `0` ovunque: il passo 7 non è ancora
iniziato, in attesa della checklist di sicurezza/dispositivo/carico.

Ordine obbligatorio:

1. eseguire migration D1 additive;
2. configurare secret Worker (`CHAT_GUEST_SESSION_SECRET`, `CHAT_CONTACT_LOOKUP_SECRET`, `VAPID_PRIVATE_KEY`);
3. configurare `VAPID_PUBLIC_KEY` e `VAPID_SUBJECT` sia su Worker sia su Pages;
4. deployare `aml-support-realtime` e attendere lo smoke test dei Durable Object;
5. deployare Pages;
6. lasciare `CHAT_ENABLED=0` durante smoke e Access verification;
7. abilitare prima preview, poi production con rollback window monitorata.

Gate prima di `CHAT_ENABLED=1`:

- typecheck e tutte le suite verdi;
- Worker dry-run e Pages Functions build verdi;
- sessione guest firmata, create-first-message e projection D1 verificati;
- Access obbligatorio su ogni route `/admin/*`;
- PWA installabile e Cache Storage priva di API/messaggi/ordini;
- Push reale verificata almeno su un desktop e uno smartphone installato;
- scheduled archive/purge eseguito su dati sintetici.

## Rollback

1. impostare `CHAT_ENABLED=0` per bloccare nuove sessioni e scritture pubbliche;
2. mantenere disponibili Access admin, export e retention/purge;
3. ripristinare il precedente bundle Pages/Worker senza eseguire downgrade D1 distruttivi;
4. lasciare attivi i deletion job già oltre il grace period;
5. riconciliare outbox e job prima di riabilitare.

Non cancellare tabelle, namespace Durable Object o tombstone durante un rollback applicativo.

## Failure purge

Stati job:

```text
PENDING → GATED → DO_DELETED → COMPLETE
```

- `PENDING`: D1 deve essere marcato `PURGE_PENDING`, poi il DO attiva il write gate.
- `GATED`: al termine del grace period il Worker chiama `deleteAll()`.
- `DO_DELETED`: il contenuto DO è già eliminato; il retry deve creare il tombstone e rimuovere la projection D1.
- `COMPLETE`: SupportHub è stato notificato e la pipeline è conclusa.

Controllare `attempts`, `next_attempt_at` e `last_error` senza loggare body o contatti. Un job `GATED` con scadenza futura può essere annullato; dopo l'avvio di `deleteAll()` non è più reversibile.

## Rotazione VAPID

La coppia public/private deve essere ruotata insieme. Una nuova public key richiede nuove browser subscription: distribuire prima il codice che gestisce la nuova configurazione, aggiornare Worker e Pages nello stesso change window, quindi chiedere agli operatori di riattivare le notifiche. Non loggare mai la private key.

## Osservabilità

I log strutturati `[chat-metric]` espongono i contatori e le latenze normative dell'ADR senza body, email o dati di contatto. Allarmare almeno su:

- crescita di `chat_projection_retry_total`;
- `chat_push_failed_total` non transitorio;
- `chat_purge_failed_total`;
- `chat_error_total`;
- p95 di persistence, projection, push e purge oltre gli obiettivi ADR.

## Device matrix

Prima del rollout production verificare manualmente:

- Chrome e Edge desktop Windows;
- Chrome Android;
- Safari iPhone come Home Screen Web App.

Per ogni dispositivo: installazione, sessione Access, permesso Push da gesto esplicito, ricezione, badge, click/deep link, reconnect, sessione scaduta, screen lock e app terminata.
