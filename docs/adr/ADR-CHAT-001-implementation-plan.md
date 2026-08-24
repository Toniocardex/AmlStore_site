# ADR-CHAT-001 rev1.2 — Piano di implementazione

**Stato:** M0–M7 implementate; merged su `main`; infrastruttura di produzione e
preview deployata e isolata; **`CHAT_ENABLED=1` in produzione dal 2026-08-24**
(attivata su decisione esplicita dell'utente per test reali, con Safari
iPhone, conferma Push da desktop esterno e test di retention/purge ancora
aperti — vedi §0.3)  
**Data:** 2026-08-24  
**Specifica normativa:** `ADR-CHAT-001 — Integrated Realtime Support Chat, Admin PWA and Cloudflare Infrastructure — rev1.2`  
**Repository target:** AmlStore_site  

## 0. Stato implementazione (2026-08-24)

- **M0 — implementato localmente:** protocollo condiviso, TypeScript, Worker,
  Durable Object migrations, binding Pages/Worker, storage dev coerente, harness
  Vitest e bundle dry-run sono pronti. Il gate di deploy preview resta una
  verifica di rollout e non è stato eseguito su risorse remote.
- **M1 — implementato nel codice:** sessione guest firmata, origin/payload/order
  validation, schema D1/SQLite, creazione atomica, idempotenza, outbox con retry,
  projection, REST history/list/send/read e rate limit IP/visitor/conversazione.
- **M2 — implementato:** WebSocket guest/operatori hibernating, attachment,
  catch-up, send/read/typing, fallback REST, broadcast SupportHub, presence,
  lifecycle, assignment e riconciliazione inbox D1 sono implementati.
- **M3 — implementato nel codice:** widget guest IT/EN/FR/DE/ES e inbox admin
  responsive con deep link, reply/read/status/archive/reopen/spam/assignment e
  quick replies. Layout verificato con browser reale su desktop e 360 px.
- **M4 — implementato e verificato localmente:** state machine e timer,
  scheduled archive/purge, write gate, deletion job resumable con tombstone,
  cancellazione manuale/visitor/contatto verificato, grace period ed export.
  I test coprono purge idempotente, rifiuto delle scritture e mancata
  resurrezione dopo un evento stale.
- **M5 — implementato e verificato localmente:** PWA `/admin/support`, manifest,
  icone, service worker app-shell-only, API network-only, install prompt, deep
  link e layout mobile. Le Cache Storage non contengono API o guest data.
- **M6 — implementato nel codice:** VAPID, subscription per device, preferenze,
  soppressione per operatori visibili, notifiche per nuova conversazione,
  messaggio e assegnazione, invalidazione 404/410, badge e test Push admin.
- **M7 — implementato localmente:** metriche strutturate, feature flag,
  availability override, test automatici e runbook operativo. I gate device,
  preview/canary e load test su infrastruttura reale restano attività di rollout.

La feature resta disabilitata per default (`CHAT_ENABLED=0`). Aggiornamento
2026-08-24: non è più vero che nessuna risorsa Cloudflare sia stata toccata —
vedi §0.2 per l'infrastruttura di rollout effettivamente deployata da questa
sessione.

### 0.1 Correzioni post-review (2026-08-24)

Review del diff non committato contro l'ADR rev1.2. Cinque difetti bloccanti
corretti prima dei blocchi di test rimanenti:

1. **Stato `PENDING` mai raggiunto** (ADR §29, §74). La risposta dell'operatore
   porta ora `OPEN → PENDING` e il messaggio successivo del visitatore riporta
   `PENDING → OPEN`, con evento di stato in outbox nella stessa transazione.
2. **Resurrezione dopo purge** (ADR §69.8, §69.9). `conversationId` è
   deterministico, quindi un create tardivo ricadeva sul Durable Object svuotato
   e ne reinizializzava lo storage con projection scartata dal tombstone. Il
   gateway consulta il tombstone prima di raggiungere il DO e risponde
   `CONVERSATION_PURGED` (410); un nuovo contatto genera una conversazione nuova.
3. **Eventi di stato persi dopo un retry** (ADR §13, §16). Il drain dell'outbox
   proseguiva oltre un evento fallito: l'evento successivo alzava
   `projection_version` e il retry del precedente veniva scartato per sempre
   (es. `conversation.closed` perso ⇒ chat mai archiviata né purgata). Il drain
   si interrompe al primo errore e riparte in ordine al prossimo alarm.
4. **Retention non ancorata alla chiusura** (ADR §69.2). `closed_at` è
   persistito nello stato locale del DO; `archive_at` e `purge_at` sono
   calcolati entrambi da lì, quindi l'archiviazione non fa più ripartire la
   retention (erano 30+180 giorni invece di 180) e una `CLOSED` mai archiviata
   ha comunque una scadenza di purge.
5. **Cancellazione storico non batch-based** (ADR §69.11). Gli endpoint di
   erasure per `visitor_id` e per contatto verificato lavorano ora su batch
   limitati (`CHAT_RETENTION_BATCH_SIZE`, max 100), si limitano a bloccare le
   conversazioni e delegano la finalizzazione al retention worker. La risposta
   include `hasMore`: la procedura è ripetibile fino a completamento.

Copertura aggiunta: transizione `PENDING` in andata e ritorno, scadenze purge
ancorate a `closed_at` attraverso l'archiviazione, anti-resurrection lato
gateway. Il comportamento del punto 3 va esercitato nella failure simulation
prevista dal rollout (D1 indisponibile dopo il commit nel DO).

Corretti anche due difetti trovati collaudando il widget dal vivo, non dalla
review statica: la riconnessione della socket non ripartiva riaprendo il
pannello dopo averlo chiuso, e il cron di retention girava sul D1 configurato
a prescindere da `CHAT_ENABLED`, quindi in produzione avrebbe interrogato
`aml-orders` ogni 15 minuti anche a feature spenta.

### 0.2 Infrastruttura di rollout deployata (2026-08-24)

Merge di `chat/adr-chat-001` su `main` (conflitti solo sull'hash `?v=` di
`header.js` nelle pagine HTML — il branch non tocca mai il contenuto reale,
risolti tenendo `main` e rigenerando gli hash). Da qui in poi non è più
un'implementazione solo locale: sono state create ed esercitate risorse
Cloudflare reali, sia in preview sia in produzione.

**Widget storefront corretto prima del deploy.** Il widget si iniettava su
ogni pagina indipendentemente da `CHAT_ENABLED`: un pulsante "Chat"
permanentemente inerte sarebbe comparso a ogni visitatore del sito dal primo
minuto del merge. `ensureSupportChat()` ora interroga
`/api/chat/availability` (lo stesso endpoint pubblico usato dal widget per lo
stato online/offline, nessuna sessione richiesta) e monta lo script solo se
`enabled` è vero; un fallimento di rete non mostra il widget (fail closed).
Verificato con Playwright su dev server isolati per entrambi gli scenari.

**Ambiente preview** (branch, mai promosso a produzione):
- D1 `aml-store-preview` (id `07947b6c-2b3a-418e-8c33-2d745bbccfda`), fisicamente
  separato da `aml-orders`: schema commerce completo + `migrations/0002_chat_core.sql`,
  zero dati reali;
- Worker `aml-support-realtime-preview` deployato (`wrangler deploy --env
  preview` da `workers/support-realtime`), `CHAT_ENABLED=1` **solo qui**,
  cron attivo sul D1 preview;
- secret dedicati sul Worker (`CHAT_GUEST_SESSION_SECRET`,
  `CHAT_CONTACT_LOOKUP_SECRET`, `VAPID_PRIVATE_KEY`) e sul progetto Pages
  ambiente preview (stessi due HMAC + `TOKEN_SECRET` di test, mai il valore
  reale);
- `wrangler.toml` root, sezione `[env.preview]`: binding D1/DO/R2 e vars
  ridichiarati per intero (le sezioni `[env.x]` di Wrangler non ereditano dal
  top-level — verificato sulla documentazione Cloudflare prima di scrivere,
  non assunto), `SITE_ORIGIN` sull'alias di branch
  `chat-adr-chat-001.amlstore-site.pages.dev`, `PAYPAL_BASE_URL` sandbox
  (mai LIVE su una build di preview).
- **Non ancora fatto:** nessuna build di preview è mai stata generata (il
  merge è andato direttamente su `main`, non è stato pushato il branch);
  Cloudflare Access non copre l'hostname `.pages.dev` (l'app esistente è
  scoped su `aml-store.com`), quindi `/admin/support` su un'eventuale
  preview risponderebbe 401 finché non si aggiunge un'app Access dedicata
  dalla dashboard.

**Ambiente produzione:**
- Worker `aml-support-realtime` deployato (non solo dichiarato: il binding
  `script_name` nel `wrangler.toml` root era scritto da settimane ma puntava
  a uno script inesistente — il primo push del merge ha fatto fallire la
  build con `Error 8000109: Script aml-support-realtime not found`.
  Cloudflare non ha promosso il deployment fallito, il sito ha continuato a
  servire l'ultima build buona, zero downtime reale. Il binding è stato
  temporaneamente rimosso per sbloccare il deploy, poi il Worker è stato
  effettivamente deployato e il binding riattivato in un commit successivo,
  build verificata `success` via API);
- `CHAT_DB` del Worker di produzione punta al D1 reale `aml-orders`, come da
  disegno ADR §4.8 (stesso fisico dell'e-commerce, non un secondo database);
- **`migrations/0002_chat_core.sql` applicata a `aml-orders`** in questa
  sessione (era stata applicata solo al D1 preview e a quello locale — gap
  scoperto mentre si documentava questo stato, non prima). Additiva,
  verificata: le 8 tabelle `chat_*` sono state create, `orders` resta
  intatta (le righe reali non sono state toccate);
- secret di produzione impostati, **valori diversi da quelli preview**:
  `CHAT_GUEST_SESSION_SECRET`, `CHAT_CONTACT_LOOKUP_SECRET`,
  `VAPID_PRIVATE_KEY` sul Worker; gli stessi due HMAC sulle secret Pages
  produzione; `TOKEN_SECRET` invece riusa di proposito il valore già
  esistente (firma gli stessi ordini, per disegno);
- `VAPID_PUBLIC_KEY` di produzione nel `wrangler.toml` root;
- `CHAT_ENABLED` resta `"0"` in produzione. **Decisione esplicita
  2026-08-24:** proposto di attivarlo, l'utente ha scelto di completare
  prima la checklist di sicurezza/dispositivo/carico. Il flag non va a `"1"`
  finché quella checklist non è chiusa — vedi il commento accanto alla
  variabile nel `wrangler.toml` e §11 più sotto.

Rispetto alla sequenza di deploy in §13: i passi 1–4 e 7–8 sono completi (D1
migrato, Worker distribuito sia preview sia produzione, binding Pages
configurato per entrambi, produzione deployata con feature disabilitata). I
passi 5, 6, 9, 10 (smoke test admin interno, abilitazione in preview,
abilitazione solo admin/internal, rollout progressivo storefront) restano
da fare, in quest'ordine, e nessuno di essi implica accendere il flag in
produzione prima che la checklist di §11 sia chiusa.

### 0.3 Checklist di sicurezza e dispositivi (2026-08-24)

Contro il gate «prima di `CHAT_ENABLED=1`» del runbook:

- **Suite di sicurezza automatica** (`8c7babaa`, estesa in `5120ed21`):
  origin validation, sessione guest obbligatoria (REST e WS), rifiuto
  visitorId iniettato, enumerazione conversazioni (404 identico per
  conversazione altrui vs inesistente), Access 401 senza JWT e con JWT
  scaduto (incluso bypass dev fuori localhost), rate limit sia a livello DO
  (20 msg/min/conversazione) sia a livello gateway D1 (burst distribuito su
  più conversazioni), invariante `customer_id` sempre `NULL`, corpo del
  messaggio mai interpretato/alterato lato server (difesa reale contro XSS è
  solo client-side, verificata sia isolata sia end-to-end guest→admin reale:
  mai `.innerHTML`, solo `.textContent`), idempotenza `clientMessageId` sotto
  50 richieste concorrenti, handshake WebSocket malformato (426) e fuzzing
  payload WS (frame binari, JSON invalido, tipo comando sconosciuto,
  conversationId incoerente) senza side-effect né caduta della connessione.
- **Device matrix desktop:** Chrome ed Edge reali (non emulati) verificati:
  installazione PWA, sessione Access, Cache Storage priva di API/messaggi,
  reconnect. La sola sottoscrizione Push reale (`pushManager.subscribe()`)
  fallisce con `AbortError` su entrambi i browser in questa macchina di
  sviluppo — diagnosticato come blocco di rete/policy locale verso il
  servizio push di Google, non un difetto del prodotto (corretta anche
  un'assunzione errata della review iniziale: il blocco è dato dalla
  modalità **headless**, non dall'incognito, che invece funziona).
- **Device matrix Android:** checklist completa a 10 passi (installazione,
  Access, permesso Push da gesto esplicito, ricezione Push reale, badge,
  deep link dalla notifica, reconnect Wi-Fi, sessione scaduta, notifica a
  schermo bloccato, notifica ad app terminata) eseguita dall'utente su
  dispositivo Android reale — **esito: tutti i passi verificati senza
  problemi**. La ricezione Push reale qui conferma che il blocco osservato
  su desktop è specifico di questa macchina/rete di sviluppo e non del
  Worker/VAPID: sulla rete mobile reale la sottoscrizione e la consegna
  funzionano. Questo chiude la clausola «almeno... uno smartphone
  installato» del gate Push del runbook.
- **Load test sintetico (2026-08-24):** 30 guest concorrenti (arrivo
  scaglionato su 0–3s, ciascuno: creazione conversazione REST + 2 messaggi
  di follow-up via WebSocket), più un osservatore admin sul fan-out
  SupportHub, eseguito contro il Worker/Pages dev locali (stesso codice di
  preview/produzione). 25/30 completate senza errori con latenze buone
  (creazione REST p50 691ms/p95 2,7s; invio WS p50 268ms/p95 762ms; fan-out
  verso admin p50 13ms). 1 richiesta respinta con 429 correttamente — i 30
  guest condividevano lo stesso IP locale, quindi hanno urtato il limite di
  30 creazioni/10min per IP (limitatore anti-abuso che funziona come
  previsto). **4 richieste fallite con 500**, causa isolata nei log via
  l'API di osservabilità locale di Wrangler: `D1_ERROR: database is locked:
  SQLITE_BUSY` sulla scrittura concorrente del contatore di rate-limit
  condiviso (`chat_rate_buckets`). Il retry dell'outbox ha comunque
  recuperato tutto il resto: le 25 conversazioni riuscite hanno
  `last_seq`/`projection_version` coerenti su D1, nessun dato perso o
  proiezione incompleta. **Effetto collaterale non recuperato da solo:**
  dopo il burst il binding D1 del server dev condiviso è rimasto bloccato
  (`Network connection lost` su ogni creazione successiva), richiedendo un
  riavvio dei processi `wrangler dev` per sbloccarsi — riavvio non ancora
  eseguito su decisione esplicita dell'utente (sessione 2026-08-24: "no, va
  bene così"), quindi il recupero non è stato confermato.
  **Non verificato:** se questa contesa/blocco si riproduce sul D1 reale di
  Cloudflare in edge (servizio distribuito) o è specifica del simulatore
  SQLite locale di Miniflare condiviso da due processi `wrangler dev`
  separati (Pages + Worker) sullo stesso file — scenario esplicitamente
  locale per disegno (vedi runbook, sezione «Sviluppo locale»).
  **Valutazione del rischio (2026-08-24):** l'utente giudica lo scenario di
  30 creazioni concorrenti nello stesso istante non rappresentativo del
  traffico reale del negozio, e non lo considera bloccante per l'attivazione.
  Resta comunque non verificato se un blocco della connessione D1 analogo
  possa presentarsi anche a concorrenza molto più bassa (es. 2-3 conversazioni
  aperte nello stesso secondo, o un guest che scrive mentre gira il cron di
  retention) — non testato a quella scala né confermato contro un D1 di
  preview reale.
- **Test retention/purge su dati sintetici: non completato.** Il piano
  prevedeva chiudere una conversazione reale, retrodatare `archive_at` e
  `purge_at` su D1 per simulare il tempo trascorso, e verificare l'intera
  pipeline PENDING→GATED→DO_DELETED→COMPLETE contro il Worker locale. Il
  test è stato interrotto dal blocco D1 sopra descritto prima di poter
  eseguire anche solo la creazione della conversazione di prova; non è
  stato ancora rieseguito.
- **Non ancora fatto:** Safari iPhone come Home Screen Web App (nessun
  dispositivo/emulatore macOS disponibile in questa sessione); conferma
  della sottoscrizione Push reale da un desktop **non** vincolato dalla
  rete/policy di questa macchina di sviluppo; riesecuzione del load test e
  del test di retention/purge dopo il riavvio dei dev server.

### 0.4 Attivazione in produzione (2026-08-24)

`CHAT_ENABLED` passato a `"1"` sia nel Worker `aml-support-realtime`
(deployato) sia nel progetto Pages (`wrangler.toml` root, commit `840d0341`,
deploy Pages `c01708ff` su `main`), su richiesta esplicita dell'utente dopo
aver valutato i gap residui (§0.3) come accettabili per iniziare test reali.
Verificato subito dopo il deploy:

- `/api/chat/availability` in produzione risponde `enabled:true`;
- il widget compare sull'homepage reale dopo la chiusura del banner cookie
  (nascosto correttamente finché il banner è aperto);
- un messaggio guest reale inviato dal widget produce `POST
  /api/chat/conversations → 201`, nessun errore di rete;
- la conversazione di test è visibile su D1 di produzione (query `--remote`)
  ed è stata effettivamente **ricevuta e risposta da un operatore** tramite
  il pannello admin nello stesso arco di tempo — primo giro completo
  guest→admin confermato su infrastruttura reale, non solo in locale.

Restano da chiudere, ora con priorità più bassa rispetto a un blocco
pre-attivazione ma comunque aperti: Safari iPhone, conferma Push da desktop
esterno a questa rete, test di retention/purge, e la domanda se il blocco D1
sotto scrittura concorrente osservato nel load test locale (§0.3) possa
presentarsi in produzione anche a bassa concorrenza.

## 1. Obiettivo

Implementare, per incrementi verificabili, la piattaforma di supporto prevista
dall'ADR senza introdurre account cliente o servizi SaaS di live chat.

Il primo incremento end-to-end obbligatorio è:

```text
signed guest session
→ first-message atomic create
→ ConversationDurableObject
→ transactional outbox
→ D1 projection
```

Il piano non autorizza deviazioni dagli invarianti guest-only. Ogni modifica
futura a identità cliente, login o recupero cross-device richiederà una nuova
ADR.

## 2. Invarianti non negoziabili

1. Il pubblico è esclusivamente guest.
2. Non esistono account, password, magic link o email-as-identity.
3. `customer_id` resta `NULL` in tutti i flow della rev1.2.
4. Il `visitorId` è generato server-side con randomness crittografica.
5. Il browser non invia un `visitorId` autorevole.
6. Nome ed email sono metadati di contatto non verificati, salvo esplicita
   verifica server-side.
7. Aprire il widget non crea conversazioni, righe D1 o storage DO.
8. Conversazione, primo messaggio e outbox sono creati atomicamente.
9. Nessun ACK positivo precede il commit persistente.
10. La timeline completa vive soltanto nello SQLite del ConversationDO.
11. D1 è il query model globale, non il bus realtime e non la timeline.
12. Il SupportHubDO è advisory: la correttezza deriva dalla reconciliation D1.
13. Il funzionamento normale è WebSocket event-driven, senza polling periodico.
14. Una failure D1, Hub o Push non può cancellare un messaggio già committato.
15. Il purge è idempotente e impedisce la resurrezione tramite tombstone.
16. Gli endpoint admin riusano Cloudflare Access e non introducono una seconda
    autenticazione amministrativa.

## 3. Baseline del repository e conseguenze

Il repository è attualmente:

- sito statico multilingue HTML/CSS/vanilla JS;
- Cloudflare Pages con Pages Functions;
- router pubblico concentrato in `functions/api/[[catchall]].js`;
- D1 esistente con binding `DB` e dati ordini/e-commerce;
- admin statico in `/admin`, protetto da Cloudflare Access;
- viste admin hash-based, senza router applicativo;
- nessun Durable Object, WebSocket, Service Worker o manifest PWA;
- test automatici limitati alla pricing policy.

Conseguenze della baseline:

- il realtime sarà un Worker separato, come richiesto da Cloudflare Pages;
- le nuove Pages Functions useranno route specifiche e moduli isolati, senza
  ampliare ulteriormente il catch-all esistente;
- `/admin/support` sarà una sezione dedicata dello stesso backoffice e
  condividerà identità Access e design token;
- il widget sarà un Web Component vanilla JS condiviso dalle cinque lingue;
- TypeScript verrà introdotto soltanto per il nuovo dominio chat e per il
  protocollo condiviso;
- la pipeline esistente delle pagine statiche continuerà a produrre asset
  committati e verificabili.

## 4. Decisioni implementative fissate dal piano

### 4.1 Identificatori

Usare `crypto.randomUUID()` con prefissi di dominio:

```text
vis_<uuid>
conv_<uuid>
msg_<uuid>
evt_<uuid>
req_<uuid>
op_<uuid>
dev_<uuid>
```

Gli ID non codificano timestamp, email, IP o altri dati personali. L'ordine
autorevole dei messaggi è sempre `conversationId + seq`.

### 4.2 Cookie guest

Nome production consigliato:

```text
__Host-aml_chat_guest
```

Formato logico:

```text
v1.<base64url({ visitorId, issuedAt, expiresAt })>.<HMAC-SHA-256 signature>
```

Attributi production:

```text
Secure; HttpOnly; SameSite=Lax; Path=/; Max-Age=CHAT_GUEST_SESSION_DAYS
```

Policy:

- `POST /api/chat/session` emette il cookie se assente o invalido;
- nessuna sessione viene salvata in D1;
- un cookie valido viene rinnovato soltanto durante attività chat autorizzata
  quando resta meno del 20% della durata configurata;
- una normale pageview non rinnova l'identità guest;
- una richiesta a una conversazione esistente con cookie invalido restituisce
  `UNAUTHORIZED`, senza creare silenziosamente un nuovo visitor;
- localhost usa un nome cookie distinto e omette `Secure` solo in sviluppo.

Secret dedicato: `CHAT_GUEST_SESSION_SECRET`.

### 4.3 Contact lookup hash

Normalizzazione MVP:

```text
trim
→ Unicode NFKC
→ lowercase
→ validation
→ HMAC-SHA-256(CHAT_CONTACT_LOOKUP_SECRET, normalizedEmail)
```

Non usare hash non keyed: una lista di email comuni sarebbe enumerabile.

La rotazione del secret avverrà con una procedura batch che ricalcola il valore
dalla `contact_email` ancora presente. La procedura deve completare prima della
rimozione del secret precedente. Nessun hash o indirizzo viene scritto nei log.

### 4.4 Order association

Il payload può includere soltanto un order token firmato, non un `orderId`
considerato attendibile. Il Pages gateway:

1. verifica firma e scadenza tramite il dominio ordini esistente;
2. verifica che l'ordine esista;
3. passa al ConversationDO un contesto interno già validato;
4. non permette al guest di interrogare ordini tramite email o numero ordine.

Per la prima versione si riusa il formato token ordine già esistente. Un token
scaduto non associa automaticamente l'ordine; l'operatore potrà associarlo
server-side dall'admin.

### 4.5 Versionamento projection

`last_seq` resta la sequence dei messaggi. Verrà aggiunto un contatore monotono
`projection_version` per tutte le mutazioni persistenti della conversazione,
incluse chiusura, assegnazione, read state e riapertura.

Regole D1:

```text
message projection: incoming last_seq > stored last_seq
state projection:   incoming projection_version > stored projection_version
tombstone exists:   discard every incoming projection
```

Questo chiarisce gli eventi di stato che non generano un nuovo messaggio.

### 4.6 Transazioni ConversationDO

Non usare `BEGIN`/`COMMIT` tramite `sql.exec()`. Le scritture atomiche SQLite
usano `ctx.storage.transactionSync()`.

Il primo messaggio inserisce nella stessa transazione:

- metadata locali e stato `OPEN`;
- messaggio con `seq = 1`;
- participant state iniziale;
- evento outbox `conversation.created`/`message.created` coerente.

Il risultato viene ACKato solo dopo il ritorno positivo della transazione.

### 4.7 Purge gate

Tutte le mutazioni di una conversazione transitano dal relativo ConversationDO.
Il purge è una procedura a due fasi:

1. D1 passa condizionalmente a `PURGE_PENDING`;
2. il DO attiva e persiste il write gate locale;
3. il DO rifiuta comandi e chiude i socket interessati;
4. il DO esegue `deleteAll()`;
5. una transazione D1 crea/aggiorna il tombstone ed elimina la projection;
6. il SupportHub riceve `conversation.purged`;
7. il deletion job passa a `COMPLETE`.

Il passaggio D1 è il primo gate osservabile; il gate nel DO impedisce nuovi ACK.
Solo dopo la cancellazione dello stato autorevole nel DO vengono scritti il
tombstone e rimossa la projection, così un retry riparte dallo stato del job
senza rendere nuovamente visibile la conversazione.

### 4.8 Database D1

Per evitare un secondo database non necessario, `CHAT_DB` punta allo stesso D1
fisico dell'e-commerce nell'ambiente corrispondente. Il Worker usa un binding
dedicato `CHAT_DB`; Pages continua a usare `DB`.

Development, preview e production devono però usare database fisici distinti.

### 4.9 Compatibility date

Il Worker realtime usa una compatibility date almeno `2026-02-24`, così
`ctx.storage.deleteAll()` elimina anche gli alarm attivi. La data concreta sarà
fissata alla data di introduzione del Worker e aggiornata solo con test.

## 5. Architettura target

```text
Storefront guest                     /admin/support
      │                                     │
      ├── HTTPS same-origin                 ├── HTTPS same-origin
      └── WSS same-origin                   └── WSS same-origin
                    │
                    ▼
             Pages Functions
        guest/admin auth + validation
                    │
        external Durable Object bindings
             ┌──────┴────────┐
             ▼               ▼
 ConversationDurableObject  SupportHubDO
 one per conversation       one per store
 SQLite + sockets + outbox  admin sockets/presence
             │               │
             └──────┬────────┘
                    ▼
              D1 query model
                    │
                    ├── inbox/lifecycle
                    ├── operators/preferences
                    ├── push subscriptions
                    └── purge tombstones/jobs
```

## 6. Struttura sorgenti prevista

```text
support/
├── shared/
│   ├── protocol.ts
│   ├── schemas.ts
│   ├── errors.ts
│   ├── ids.ts
│   └── lifecycle.ts
│
workers/
└── support-realtime/
    ├── wrangler.toml
    ├── src/
    │   ├── index.ts
    │   ├── conversation-do.ts
    │   ├── support-hub-do.ts
    │   ├── local-schema.ts
    │   ├── projection.ts
    │   ├── outbox.ts
    │   ├── retention.ts
    │   ├── push.ts
    │   └── observability.ts
    └── test/

functions/
├── _lib/
│   └── chat/
│       ├── guest-session.ts
│       ├── origin.ts
│       ├── contact.ts
│       ├── order-context.ts
│       ├── responses.ts
│       └── gateway.ts
├── api/chat/[[path]].ts
└── admin/api/support/[[path]].ts

admin/support/
├── index.html
├── support.css
├── support.js
├── manifest.webmanifest
└── icons/

admin/sw.js
components/support-chat.js
css/support-chat.css
migrations/
├── 0002_chat_core.sql
├── 0003_chat_operations.sql
└── 0004_chat_push.sql
```

I numeri definitivi delle migration dipendono dalla riconciliazione iniziale
dello stato migration locale/remoto.

## 7. Modello dati

### 7.1 SQLite del ConversationDO

Tabelle normative:

- `messages` — timeline, sequence, idempotenza;
- `participant_state` — `last_read_seq` per visitor/operator;
- `outbox` — projection D1 e notifica Hub indipendenti;
- `conversation_local_state` — status, visitor ownership, write gate,
  projection version e metadata minimi.

Vincoli aggiuntivi:

- `UNIQUE(sender_id, client_message_id)`;
- messaggi plain text da 1 a `CHAT_MAX_MESSAGE_LENGTH`;
- `visitor_id` locale impostato una sola volta;
- nessuna email necessaria per autorizzare il socket;
- outbox processata in batch limitato;
- retry con backoff persistito e alarm singolo.

### 7.2 D1

Tabelle core:

- `chat_conversations` — schema ADR più `projection_version`;
- `chat_conversation_tombstones` — incluso nella migration core anche se il DDL
  è riportato separatamente nella rev1.2;
- `chat_operators` — UUID operatore, email Access normalizzata, stato ed enabled;
- `chat_operator_preferences` — notifiche, sound, preview e disponibilità;
- `chat_push_subscriptions` — un record per device/endpoint;
- `chat_deletion_jobs` — cancellazioni guest/contatto resumable;
- `chat_rate_buckets` — limiti globali non gestibili nel singolo ConversationDO.

`chat_deletion_jobs` conserva il selector necessario solo finché il job è
attivo. A completamento il selector viene rimosso e resta un audit minimale
senza body, email o visitor ID in chiaro.

### 7.3 Authority map

| Dato | Autorità |
|---|---|
| Identità guest | Cookie firmato verificato dal ChatGateway |
| Ownership conversazione | Visitor ID persistito nel ConversationDO |
| Timeline e ordine messaggi | SQLite ConversationDO |
| Idempotenza messaggi | SQLite ConversationDO |
| Stato operativo conversazione | ConversationDO, proiettato in D1 |
| Inbox e query globali | D1 |
| Scheduling archive/purge | Campi lifecycle D1 + scheduled Worker |
| Anti-resurrection | Tombstone D1 |
| Realtime operatori | SupportHubDO advisory |
| Ordini/prodotti | Dominio e-commerce esistente |
| Admin identity | Cloudflare Access |
| Push subscriptions | D1 |

## 8. API pianificate

### 8.1 Guest

```text
POST /api/chat/session
GET  /api/chat/availability
GET  /api/chat/conversations
POST /api/chat/conversations
GET  /api/chat/conversations/:id
GET  /api/chat/conversations/:id/messages?beforeSeq=&limit=
POST /api/chat/conversations/:id/messages
POST /api/chat/conversations/:id/read
GET  /api/chat/conversations/:id/ws?lastKnownSeq=
```

Regole:

- `POST /conversations` richiede primo messaggio e `clientMessageId`;
- `POST /:id/messages` è il fallback HTTP idempotente del WebSocket;
- ogni lettura/mutazione risolve ownership dal cookie;
- `visitorId` nel body/query è rifiutato con `INVALID_PAYLOAD`;
- response sensibili includono `Cache-Control: no-store`;
- mutazioni richiedono origin consentita e JSON;
- gli errori usano l'envelope versione 1 dell'ADR.

### 8.2 Admin

```text
GET    /admin/api/support/conversations
GET    /admin/api/support/conversations/:id
GET    /admin/api/support/conversations/:id/messages
POST   /admin/api/support/conversations/:id/messages
POST   /admin/api/support/conversations/:id/read
PATCH  /admin/api/support/conversations/:id/status
PATCH  /admin/api/support/conversations/:id/assignment
POST   /admin/api/support/conversations/:id/archive
POST   /admin/api/support/conversations/:id/reopen
POST   /admin/api/support/conversations/:id/spam
GET    /admin/api/support/conversations/:id/export
DELETE /admin/api/support/conversations/:id
POST   /admin/api/support/guests/:visitorId/deletion-jobs
POST   /admin/api/support/contacts/deletion-jobs
GET    /admin/api/support/deletion-jobs/:id
GET    /admin/api/support/ws
GET    /admin/api/support/profile
PATCH  /admin/api/support/profile
POST   /admin/api/support/push/subscriptions
DELETE /admin/api/support/push/subscriptions/:id
POST   /admin/api/support/push/test
```

Tutti gli endpoint:

- verificano Cloudflare Access con l'helper esistente;
- mappano l'email Access a un `operator_id` D1;
- applicano i permessi `support.*`;
- proteggono le mutazioni con Origin/Content-Type/payload limits;
- non loggano body, email o dettagli ordine.

### 8.3 Deep link admin

URL canonico:

```text
/admin/support/conversations/{conversationId}
```

Verrà aggiunta una route Pages specifica che serve l'app shell di supporto per
i deep link, mantenendo l'URL. Prima dell'implementazione UI verrà eseguito uno
spike locale per validare il rewrite attraverso la middleware globale esistente.
Non si farà affidamento su una regola `_redirects` non verificata.

## 9. Protocollo realtime

Comandi guest/admin iniziali:

```text
message.send
message.read
typing.started
typing.stopped
conversation.close
conversation.reopen
conversation.archive
conversation.spam
operator.assignment
operator.presence
```

Eventi:

```text
conversation.created
conversation.updated
conversation.reopened
conversation.closed
conversation.archived
conversation.spam_marked
conversation.purge_requested
conversation.purged
message.created
message.read
typing.started
typing.stopped
operator.presence
operator.assignment
support.unread_changed
```

Ogni envelope include `v`, `type`, ID correlativi e timestamp server. Gli input
remoti passano sempre da validazione runtime condivisa.

Il reconnect usa backoff esponenziale con jitter, massimo 30 secondi. Dopo il
reconnect admin:

```text
connect hub
→ fetch inbox D1
→ replace/reconcile local state
→ resume realtime events
```

## 10. Milestone di implementazione

### M0 — Fondazioni e spike Cloudflare

Deliverable:

- struttura TypeScript e protocollo condiviso;
- Worker `support-realtime` con due classi SQLite-backed;
- migration DO `new_sqlite_classes`;
- binding Pages esterni e `CHAT_DB` Worker;
- configurazioni dev/preview/prod separate;
- comando locale per eseguire Pages e Worker insieme;
- spike deep-link `/admin/support/conversations/:id`;
- spike `web-push` nel runtime Worker;
- riconciliazione dello stato D1 migrations esistente.

Gate:

- deploy di preview senza risorse production;
- Pages raggiunge entrambi i DO tramite binding;
- test smoke locale e typecheck verdi.

### M1 — Sessione guest e persistenza atomica

Deliverable:

- cookie guest stateless firmato;
- validazione Origin, payload e contatti;
- verifica order token;
- D1 core schema e tombstone;
- schema SQLite ConversationDO;
- create-with-first-message atomico;
- idempotenza `clientMessageId`;
- outbox, projection D1 e alarm retry;
- REST history, list e HTTP message fallback;
- rate limit IP/visitor/conversation;
- logging strutturato senza contenuto.

Gate:

- aprire il widget/sessione non crea storage chat;
- duplicate send produce un solo messaggio;
- ACK solo dopo commit;
- D1/Hub failure simulata non perde il messaggio;
- un visitor non legge la conversazione di un altro.

### M2 — Realtime guest e SupportHub

Deliverable:

- WebSocket Hibernation ConversationDO;
- socket attachment con ruolo e participant key;
- history catch-up da `lastKnownSeq`;
- read cursor e typing throttled;
- SupportHubDO con socket operatori e presence;
- reconnect/reconciliation senza polling;
- availability pubblica separata dalla connessione operatore.

Gate:

- guest e operatore scambiano messaggi realtime;
- eviction/hibernation non perde ownership o stato;
- reconnect recupera esattamente i messaggi mancanti;
- Hub offline degrada a D1 reconciliation.

### M3 — Widget storefront e inbox admin

Deliverable storefront:

- Web Component `support-chat` localizzato IT/EN/FR/DE/ES;
- launcher e integrazione nel support panel esistente;
- stati CLOSED/CONNECTING/ONLINE/RECONNECTING/OFFLINE/ERROR;
- context page/locale/product validato server-side;
- draft locale, nessun falso stato "inviato" offline;
- script di build/iniezione ripetibile per tutte le pagine.

Deliverable admin:

- `/admin/support` e link dalla navigazione admin esistente;
- inbox cursor-based con sezioni ADR;
- desktop tre colonne;
- mobile stack Inbox → Conversation → Guest details;
- reply, read, close, reopen, archive, spam, assignment;
- guest/order/product context;
- quick replies che inseriscono testo senza inviarlo;
- deep link conversazione.

Gate:

- UI accessibile solo tramite Access;
- contenuto messaggi renderizzato con `textContent`/escaping;
- nessun `dangerouslySetInnerHTML` equivalente sui messaggi;
- layout verificato almeno a 360 px, tablet e desktop.

### M4 — Lifecycle, retention e cancellazione

Deliverable:

- state machine completa;
- calcolo e validazione server-side dei timer;
- scheduled archive pass;
- scheduled purge pass batch-based;
- write gate `PURGE_PENDING`;
- `deleteAll()`, tombstone e finalizzazione D1;
- retry dopo failure in ogni passaggio;
- delete manuale e grace period;
- export conversazione;
- deletion jobs per visitor e contatto verificato;
- cleanup tombstone compatibile con la massima età dei retry.

Gate:

- archive/purge idempotenti;
- nessun contenuto recuperabile dopo purge;
- evento stale non ricrea la conversazione;
- una conversazione `PURGE_PENDING` non accetta messaggi;
- cancellare chat non modifica ordini/prodotti.

### M5 — PWA

Deliverable:

- manifest con start URL `/admin/support` e scope `/admin/`;
- icone installabili;
- service worker `/admin/sw.js`;
- cache versionata del solo app shell;
- network-only/no-store per API, messaggi, ordini e guest data;
- notification click e focus/navigate della finestra esistente;
- gestione sessione Access scaduta con ritorno al deep link.

Gate:

- installabilità Chrome/Edge/Android/iOS Home Screen;
- nessun dato sensibile presente nelle Cache Storage entries;
- aggiornamento service worker senza app shell bloccata.

### M6 — Web Push e badge

Deliverable:

- VAPID keys e subject come secret/config;
- registrazione e rimozione device;
- preferences operatore;
- policy visible/hidden/disconnected;
- push privacy preview on/off;
- invalidazione subscription su errori permanenti;
- badge = numero conversazioni non lette;
- test push manuale admin.

Gate:

- push failure non influenza ACK o stato conversazione;
- click apre la conversazione corretta;
- device multipli dello stesso operatore funzionano;
- badge viene azzerato correttamente.

### M7 — Hardening e rollout

Deliverable:

- metriche e dashboard operative;
- failure simulation D1/Hub/Push;
- load test sui pattern realistici;
- security test completi;
- runbook deploy, rollback, VAPID rotation e purge failure;
- feature flag `CHAT_ENABLED` e availability override;
- rollout interno, una lingua, poi tutte le lingue.

Gate:

- checklist MVP ADR interamente verde;
- nessun errore critico nei log preview/canary;
- target di latenza misurati o deviazioni documentate;
- procedure di rollback provate senza cancellazioni distruttive.

## 11. Strategia test

### Unit

- cookie encode/verify/expiry/tampering/renewal;
- email normalization e lookup HMAC;
- ID e protocol envelope;
- runtime validation;
- state machine e permessi;
- message limits e plain text;
- rate-limit windows;
- projection ordering con `last_seq` e `projection_version`;
- retention timestamp e configurazione invalida;
- tombstone discard.

### Durable Object integration

- first-message transaction rollback;
- duplicate `clientMessageId`;
- sequence concorrenti;
- outbox partial success e retry;
- alarm at-least-once;
- hibernation/eviction reconstruction;
- socket authorization attachment;
- archive/reopen;
- manual/automatic purge;
- D1 failure dopo `deleteAll()`;
- retry purge con DO già vuoto;
- stale projection dopo tombstone.

### Pages Functions integration

- cookie assente/valido/scaduto/manomesso;
- Origin e content type;
- cross-visitor enumeration;
- order token valido/scaduto/manomesso;
- Cloudflare Access valido/non valido;
- permessi operatori;
- cursor pagination stabile;
- header `Cache-Control: no-store`.

### E2E Playwright

- nuovo guest e primo messaggio;
- operatore riceve e risponde;
- reconnect guest/admin;
- HTTP fallback;
- close/reopen;
- cross-browser = nuovo visitor senza storico;
- deep link admin;
- sessione Access scaduta;
- offline draft e messaggio non inviato;
- service worker non cachea API.

### Device manuali

- Chrome e Edge Windows;
- Chrome Android;
- Safari iPhone come PWA installata;
- push con schermo bloccato e app terminata;
- badge e notification click.

## 12. Configurazione e secret

Binding Worker:

```text
CHAT_CONVERSATIONS
SUPPORT_HUB
CHAT_DB
```

Binding Pages verso Worker esterno:

```text
CHAT_CONVERSATIONS
SUPPORT_HUB
```

Secret:

```text
CHAT_GUEST_SESSION_SECRET
CHAT_CONTACT_LOOKUP_SECRET
VAPID_PRIVATE_KEY
VAPID_SUBJECT
```

Vars:

```text
CHAT_ENABLED
CHAT_GUEST_SESSION_DAYS
CHAT_GUEST_COOKIE_NAME
CHAT_ARCHIVE_AFTER_DAYS
CHAT_RETENTION_DAYS
CHAT_SPAM_RETENTION_DAYS
CHAT_DELETE_GRACE_DAYS
CHAT_TOMBSTONE_RETENTION_DAYS
CHAT_RETENTION_BATCH_SIZE
CHAT_MAX_MESSAGE_LENGTH
VAPID_PUBLIC_KEY
SITE_ORIGIN
```

La validazione startup/deploy deve imporre:

```text
CHAT_ARCHIVE_AFTER_DAYS < CHAT_RETENTION_DAYS
CHAT_RETENTION_BATCH_SIZE within safe bounds
CHAT_MAX_MESSAGE_LENGTH = 4000 for MVP
all required secrets present outside local test mode
```

## 13. Deployment e rollback

Ordine di deploy:

1. applicare migration D1 additive;
2. distribuire Worker e namespace DO;
3. configurare binding Pages preview;
4. distribuire Pages con `CHAT_ENABLED=0`;
5. eseguire smoke test admin interno;
6. abilitare chat in preview;
7. configurare production binding/secrets;
8. deploy production con feature disabilitata;
9. abilitare solo admin/internal test;
10. abilitare storefront progressivamente.

Rollback applicativo:

- disabilitare nuove sessioni/conversazioni con `CHAT_ENABLED=0`;
- mantenere disponibili admin, history e purge;
- non eliminare namespace o tabelle durante un rollback;
- tornare al Worker precedente tramite deployment rollback;
- applicare migration distruttive solo in una release separata e dopo backup.

## 14. Sequenza consigliata dei primi commit

1. `chat: add protocol, config validation and test harness`
2. `chat: add external durable object worker skeleton`
3. `chat: add D1 core schema and projection repository`
4. `chat: add signed guest session gateway`
5. `chat: add atomic first-message conversation creation`
6. `chat: add transactional outbox and retries`
7. `chat: add guest REST history and authorization`
8. `chat: add websocket hibernation and reconnect`
9. `chat: add support hub and admin reconciliation`
10. `chat: add storefront widget and admin inbox`
11. `chat: add retention and purge pipeline`
12. `chat: add PWA, push and operational hardening`

Ogni commit deve lasciare typecheck e test verdi e non deve richiedere risorse
production per essere verificato localmente.

## 15. Definition of Done complessiva

L'implementazione è completa soltanto quando:

- tutti i criteri MVP della rev1.2 sono tracciati da test automatico o prova
  manuale documentata;
- il guest non può accedere a conversazioni di altri visitor;
- nessun flow valorizza `customer_id`;
- il sistema funziona senza polling;
- D1/Hub/Push failure non perde messaggi;
- purge e tombstone sono provati con retry e failure intermedie;
- l'admin mobile è installabile e utilizzabile come PWA;
- le API sensibili non sono cacheate;
- logging e metriche non contengono body o dati personali non necessari;
- preview e production usano binding, namespace, database e secret separati.
