# ADR-001 — Protezione antispam e antifrode del checkout

*Architettura per AML Store / Licensoft — versione completa e implementabile*

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Decisione proposta</strong></p>
<p>Adottare una difesa multilivello composta da rate limiting Cloudflare all’edge, un Checkout Guard fortemente consistente basato su Durable Object, audit persistente in D1, deduplicazione server-side, Turnstile adattivo e un gate di rischio prima della creazione degli ordini e della consegna digitale.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Campo**                    | **Valore**                                                   |
|------------------------------|--------------------------------------------------------------|
| Stato                        | Proposto                                                     |
| Data                         | 5 agosto 2026                                                |
| Ambito                       | Checkout PayPal, Stripe e bonifico; priorità iniziale PayPal |
| Sistema                      | AML Store — Cloudflare Pages Functions, D1, PayPal REST API  |
| Proprietario della decisione | Licensoft / AML Store                                        |
| Versione documento           | 1.0                                                          |

Il documento è progettato per essere implementabile direttamente nel repository Toniocardex/AmlStore_site. Le soglie iniziali sono configurazioni operative, non costanti irreversibili: devono essere distribuite in modalità osservazione, misurate e poi applicate gradualmente.

Nota legale: la sezione privacy definisce requisiti tecnici di minimizzazione e sicurezza; non sostituisce una valutazione legale o l’aggiornamento delle informative da parte del titolare del trattamento.

# 1. Sintesi esecutiva

L’incidente osservato consiste in una sequenza di ordini PayPal identici, con lo stesso indirizzo email, quantità elevata e importo di 524,75 €, generati a distanza di pochi minuti. Il sistema attuale possiede buone garanzie di integrità del pagamento, ma tratta ogni nuova chiave di idempotenza client come un nuovo ordine commerciale. Di conseguenza un attaccante può creare rumore operativo, tentare pagamenti con account compromessi, gonfiare la coda amministrativa e aumentare il rischio di contestazioni.

La decisione separa definitivamente quattro concetti oggi parzialmente sovrapposti: richiesta di checkout, tentativo di pagamento, ordine commerciale e consegna. Solo un tentativo ammesso dal motore di protezione può creare o riutilizzare un ordine; solo un pagamento verificato e una decisione di rischio favorevole possono sbloccare la consegna.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Risultato atteso</strong></p>
<p>Nel caso mostrato, il primo tentativo verrebbe registrato; il secondo richiederebbe una verifica Turnstile o riutilizzerebbe il checkout attivo; dal terzo tentativo la combinazione email/dispositivo/carrello sarebbe temporaneamente bloccata. Non verrebbero create otto righe ordine separate.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 1.1 Decisione in una frase

Inserire un gate antifrode server-side prima di createOrder() e prima della chiamata a PayPal, con contatori atomici multidimensionali, deduplicazione di checkout attivi, challenge adattiva, audit privacy-aware e riconciliazione tramite webhook verificati.

## 1.2 Principi non negoziabili

- Il frontend non è autorità per limiti, punteggio, stato del workflow o deduplicazione.

- Nessun ordine D1 viene creato prima che il Checkout Guard restituisca ALLOW o REUSE.

- Ogni chiamata esterna non idempotente usa una chiave stabile e distinta per tipo di operazione.

- Un indirizzo IP non determina da solo un blocco permanente, perché può essere condiviso.

- Nessun fingerprinting invasivo: si usa un identificatore casuale first-party e dati minimizzati.

- Le chiavi/licenze non vengono consegnate su pagamento PENDING, in revisione o non riconciliato.

- Le decisioni sono deterministiche, versionate, spiegabili e ricostruibili dall’audit log.

## 1.3 Indice

- 2\. Contesto e stato attuale

- 3\. Problema e threat model

- 4\. Requisiti

- 5\. Decisione architetturale

- 6\. Policy iniziale e risk scoring

- 7\. Modello dati

- 8\. Flussi applicativi

- 9\. Integrazione PayPal

- 10\. API e gestione errori

- 11\. Admin e operatività

- 12\. Privacy e sicurezza

- 13\. Osservabilità

- 14\. Test e criteri di accettazione

- 15\. Piano di rilascio

- 16\. Conseguenze e alternative

- 17\. Checklist implementativa

- 18\. Riferimenti

# 2. Contesto e stato attuale

## 2.1 Architettura esistente rilevante

Il repository usa un sito statico multilingue con Cloudflare Pages Functions. Tutte le route /api/\* sono gestite da functions/api/\[\[catchall\]\].js; D1 conserva gli ordini; PayPal è integrato tramite Orders API v2; il pannello amministrativo è protetto da Cloudflare Access.

| **Componente**       | **Stato attuale**                                                                          | **Valutazione**                                                     |
|----------------------|--------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| Validazione checkout | Origin allowlist, Content-Type JSON, limite payload, catalogo e prezzi risolti server-side | Solido; da mantenere prima del risk gate                            |
| Idempotenza client   | Chiave derivata da sessionStorage, metodo, email e carrello                                | Utile per retry, ma aggirabile cambiando sessione o browser         |
| Idempotenza D1       | orders.idempotency_key UNIQUE                                                              | Impedisce duplicati della stessa chiave, non abusi con chiavi nuove |
| PayPal create        | PayPal-Request-Id = orderId interno                                                        | Buono; evita duplicati PSP dello stesso ordine                      |
| PayPal capture       | Verifica status COMPLETED, importo e valuta                                                | Buono; manca idempotenza esplicita della capture e webhook PayPal   |
| Ordini pending       | createOrder() eseguito prima di PayPal create                                              | Causa principale dello spam amministrativo                          |
| Protezione bot       | Assente sul checkout; honeypot presente solo per consultation request                      | Insufficiente per operazioni monetarie                              |

## 2.2 Evidenze nel codice

- functions/api/\[\[catchall\]\].js crea la riga orders prima di invocare createPaypalOrder().

- functions/api/\_lib/order.js assegna immediatamente lo stato pending_payment.

- js/checkout.js costruisce l’idempotencyKey nel browser usando un sale in sessionStorage.

- functions/api/\_lib/paypal.js usa correttamente PayPal-Request-Id nella creazione dell’ordine.

- schema.sql non distingue tentativi, decisioni di rischio, pagamento e fulfillment.

- wrangler.toml dispone già del binding D1 e può ricevere ulteriori binding/segreti Cloudflare.

## 2.3 Problema strutturale

L’idempotenza risponde alla domanda “questa stessa operazione è già stata eseguita?”, non alla domanda “questo soggetto sta abusando del checkout?”. Un attaccante può generare nuove sessioni, nuove chiavi o variazioni minime dei dati e produrre ordini distinti. Serve quindi un controllo di frequenza e rischio basato su segnali server-side, indipendente dall’idempotencyKey fornita dal client.

# 3. Problema e threat model

## 3.1 Asset da proteggere

- Licenze digitali e inventario fisico, soprattutto prodotti ad alta rivendibilità.

- Account PayPal del merchant, tasso di contestazioni e reputazione presso il PSP.

- Tempo operativo dell’amministratore e qualità della coda ordini.

- Capacità delle API, quota D1, invii email e chiamate esterne.

- Dati personali di clienti legittimi e correttezza delle comunicazioni.

## 3.2 Abuse case principali

| **ID** | **Abuso**                         | **Meccanismo**                                                   | **Impatto**                               |
|--------|-----------------------------------|------------------------------------------------------------------|-------------------------------------------|
| T1     | Spam ordini pending               | Ripetizione di create-order con nuove sessioni/chiavi            | Coda admin inutilizzabile, costi e rumore |
| T2     | Cashing out con conto compromesso | Acquisto di licenze rivendibili tramite account PayPal sottratto | Chargeback, perdita di licenze e fondi    |
| T3     | Race / click paralleli            | Richieste simultanee prima che il sistema registri il limite     | Più ordini o più operazioni PSP           |
| T4     | Rotazione identità debole         | Cambio nome/email/IP mantenendo dispositivo o carrello           | Elusione di limiti monodimensionali       |
| T5     | Replay challenge o capture        | Riutilizzo token Turnstile o richieste PayPal                    | Bypass, duplicazioni o stati incoerenti   |
| T6     | Denial of inventory               | Creazione massiva di ordini non pagati su prodotti limitati      | Stock indisponibile o metriche falsate    |
| T7     | Distributed low-and-slow          | Pochi tentativi da molti IP                                      | Evasione dei limiti solo-IP               |

## 3.3 Minacce fuori ambito

- Compromissione dell’infrastruttura PayPal o del conto merchant.

- Frode fiscale, riciclaggio o verifica KYC completa del cliente.

- Identificazione certa della persona fisica dietro un browser.

- Blocco assoluto di bot sofisticati: l’obiettivo è ridurre rischio e costo, non promettere infallibilità.

## 3.4 Classificazione OWASP

Il caso è coerente con minacce di automazione e abuso di logica applicativa: OAT-012 Cashing Out, OAT-017 Spamming e, per gli articoli con stock, OAT-021 Denial of Inventory. OWASP raccomanda limiti specifici per funzionalità, segnali oltre l’email, workflow espliciti, idempotenza e prevenzione delle race condition \[R1\]\[R2\].

# 4. Requisiti

## 4.1 Requisiti funzionali

| **ID** | **Requisito**                                                                                       |
|--------|-----------------------------------------------------------------------------------------------------|
| FR-01  | Limitare i tentativi per email normalizzata, dispositivo, IP, carrello, metodo e fascia di rischio. |
| FR-02  | Impedire la creazione di più ordini attivi equivalenti nella stessa finestra temporale.             |
| FR-03  | Richiedere Turnstile solo quando il profilo o la frequenza lo giustificano.                         |
| FR-04  | Restituire 429 con Retry-After quando un limite temporaneo è superato.                              |
| FR-05  | Persistire ogni decisione con reason codes, policy version e correlation ID.                        |
| FR-06  | Separare tentativo, pagamento, rischio, ordine e fulfillment.                                       |
| FR-07  | Riconciliare capture, refund, reversal e dispute tramite webhook PayPal verificati.                 |
| FR-08  | Mostrare nel backoffice una vista aggregata degli abusi e una coda di revisione.                    |
| FR-09  | Supportare blocchi temporanei e override puntuali, entrambi auditati.                               |
| FR-10  | Applicare limiti di quantità configurabili per SKU ad alta rivendibilità.                           |

## 4.2 Requisiti non funzionali

| **ID** | **Requisito**                                                                                                 |
|--------|---------------------------------------------------------------------------------------------------------------|
| NFR-01 | I contatori applicativi devono essere atomici e resistenti a richieste concorrenti.                           |
| NFR-02 | Il gate deve aggiungere normalmente meno di 100 ms p95, esclusi Turnstile e PSP.                              |
| NFR-03 | Il sistema deve fallire chiuso prima di creare un nuovo pagamento quando il gate è indisponibile.             |
| NFR-04 | Il flusso di capture già approvato non deve dipendere dal gate di creazione.                                  |
| NFR-05 | Nessun log antifrode deve contenere IP o email in chiaro, salvo i dati contrattuali già presenti nell’ordine. |
| NFR-06 | Policy e soglie devono essere configurabili e versionate, non disperse nel codice.                            |
| NFR-07 | L’enforcement deve poter essere attivato per fasi: observe, challenge, enforce.                               |
| NFR-08 | Ogni chiamata PSP deve poter essere ripetuta in sicurezza con la stessa chiave di operazione.                 |

# 5. Decisione architetturale

## 5.1 Difesa multilivello scelta

| **Livello**           | **Responsabilità**                                                      | **Tecnologia**                                         |
|-----------------------|-------------------------------------------------------------------------|--------------------------------------------------------|
| L0 — Edge             | Assorbire burst grossolani e bot evidenti prima del runtime applicativo | Cloudflare WAF Rate Limiting / Managed Challenge       |
| L1 — Request context  | Estrarre segnali affidabili e normalizzare il payload                   | Pages Function + CF-Connecting-IP + cookie first-party |
| L2 — Checkout Guard   | Contatori atomici, dedupe lease, blocklist e decisione frequenza        | Durable Object SQLite, Worker separato                 |
| L3 — Risk engine      | Punteggio deterministico, hard rules, challenge e review                | functions/api/\_lib/fraud.js                           |
| L4 — Audit            | Persistenza tentativi, eventi, motivazioni e collegamenti all’ordine    | Cloudflare D1                                          |
| L5 — PSP integrity    | Idempotenza, capture verificata, webhook e riconciliazione              | PayPal REST API + webhook verificati                   |
| L6 — Fulfillment gate | Consegna soltanto dopo pagamento e rischio approvati                    | Stato server-side + admin                              |

## 5.2 Perché un Durable Object

Il Rate Limiting API di Workers e le regole WAF sono veloci ma i contatori sono locali al data center e permissivi/eventualmente consistenti; Cloudflare specifica che non devono essere usati come sistema di accounting accurato \[R3\]\[R4\]. Sono eccellenti come filtro L0, non come unica autorità per il numero massimo di tentativi monetari.

Un Durable Object offre coordinamento fortemente consistente e serializza le richieste dirette allo stesso oggetto. Per il volume attuale di AML Store si sceglie un singolo oggetto logico globale “checkout-guard-v1”, protetto a monte dal WAF. Questa scelta massimizza correttezza e semplicità. Se il traffico crescerà, l’ADR dovrà essere riesaminato per uno sharding che preservi i limiti multidimensionali.

## 5.3 Topologia

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>Browser checkout</p>
<p>|</p>
<p>| POST /api/paypal-create-order</p>
<p>v</p>
<p>Cloudflare WAF / Rate Limit (L0)</p>
<p>|</p>
<p>v</p>
<p>Pages Function: validate + resolve cart + request context (L1)</p>
<p>|</p>
<p>+--&gt; Checkout Guard Durable Object (L2)</p>
<p>| |- counters / sliding windows</p>
<p>| |- active checkout leases</p>
<p>| |- temporary blocks</p>
<p>| `- ALLOW | REUSE | CHALLENGE | BLOCK</p>
<p>|</p>
<p>+--&gt; Turnstile Siteverify, solo se richiesto (L3)</p>
<p>|</p>
<p>+--&gt; D1 checkout_attempts + orders (L4)</p>
<p>|</p>
<p>+--&gt; PayPal Orders API, idempotente (L5)</p>
<p>|</p>
<p>`--&gt; fulfillment solo dopo payment + risk gate (L6)</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 5.4 Confini di autorità

| **Dato / decisione**                                     | **Autorità**                                |
|----------------------------------------------------------|---------------------------------------------|
| Prezzi, valuta, quantità consentite, caratteristiche SKU | Catalogo server-side                        |
| Numero tentativi e blocchi temporanei                    | Checkout Guard                              |
| Punteggio e reason codes                                 | Risk engine versionato                      |
| Audit e relazione tentativo–ordine                       | D1                                          |
| Stato monetario della transazione                        | PayPal + riconciliazione server-side        |
| Consegna digitale                                        | Fulfillment gate AML Store                  |
| UI e messaggi                                            | Frontend, senza poter cambiare la decisione |

## 5.5 Pipeline obbligatoria

1.  Validare origine, Content-Type e dimensione del payload.

2.  Validare cliente e risolvere articoli/prezzi/stock esclusivamente server-side.

3.  Estrarre requestId, cfRay, IP affidabile, dispositivo first-party e user-agent minimizzato.

4.  Calcolare HMAC per email/IP/dispositivo e cartHash canonico.

5.  Applicare policy SKU e hard cap di quantità prima del PSP.

6.  Interrogare Checkout Guard per dedupe, contatori e blocchi.

7.  Se CHALLENGE, verificare Turnstile server-side e rivalutare lo stesso challengeId.

8.  Persistire checkout_attempts con decisione e policy_version.

9.  Creare o riutilizzare ordine D1 e PayPal solo dopo ALLOW/REUSE.

10. Catturare con idempotenza distinta; verificare status, importo, valuta e dati payer disponibili.

11. Determinare risk_status post-payment e sbloccare o trattenere il fulfillment.

12. Riconciliare eventi asincroni tramite webhook PayPal verificato e idempotente.

# 6. Policy iniziale e risk scoring

## 6.1 Regole di frequenza iniziali

| **Dimensione**                             | **Finestra** | **Soglia**   | **Azione**                                  |
|--------------------------------------------|--------------|--------------|---------------------------------------------|
| Email normalizzata                         | 10 minuti    | 2° tentativo | Turnstile se non già superato               |
| Email normalizzata                         | 30 minuti    | 3 tentativi  | Blocco 60 minuti                            |
| Email normalizzata                         | 24 ore       | 8 tentativi  | Blocco 24 ore + alert                       |
| Dispositivo                                | 30 minuti    | 3 tentativi  | Blocco 60 minuti                            |
| Dispositivo                                | 24 ore       | 10 tentativi | Blocco 24 ore                               |
| IP                                         | 30 minuti    | 6 tentativi  | Challenge; non blocco permanente da solo    |
| IP                                         | 24 ore       | 20 tentativi | Blocco 6 ore salvo traffico condiviso noto  |
| Stesso carrello + dispositivo              | 30 minuti    | 2 tentativi  | Riusa checkout attivo o blocca nuovo ordine |
| Alta esposizione: totale ≥ 200 € o qty ≥ 3 | 60 minuti    | 2 tentativi  | Challenge al primo retry; poi blocco        |
| Capture stesso PayPal order                | 15 minuti    | 5 richieste  | 429; una sola transizione di successo       |

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Ordine delle regole</strong></p>
<p>Hard block, blocklist e limiti di frequenza prevalgono sul punteggio. Il risk score non può trasformare un BLOCK in ALLOW; può solo aumentare il livello di controllo.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 6.2 Deduplicazione server-side

La chiave di idempotenza client resta utile, ma viene affiancata da una lease server-side. Il Checkout Guard conserva per 30 minuti una lease per la combinazione dispositivo + email + cartHash + metodo. Una richiesta concorrente o ripetuta riceve REUSE e non crea una nuova riga ordine.

Per la stessa email e lo stesso carrello da un dispositivo differente non vengono restituiti riferimenti PSP esistenti; il sistema risponde con ALREADY_PENDING oppure richiede challenge. Questo evita di usare l’email, che non è autenticazione, come chiave per accedere a una sessione PayPal iniziata altrove.

## 6.3 Punteggio di rischio v1

| **Segnale**                                            | **Punti** | **Note**                                       |
|--------------------------------------------------------|-----------|------------------------------------------------|
| Totale 200–499,99 €                                    | +20       | Calcolato dal server                           |
| Totale ≥ 500 €                                         | +35       | Non cumulativo con la fascia precedente        |
| Quantità totale 3–4                                    | +20       | Per beni digitali ad alta rivendibilità        |
| Quantità totale ≥ 5                                    | +35       | Non cumulativo con la fascia precedente        |
| Nessun ordine paid storico per l’email                 | +10       | Segnale debole, mai sufficiente da solo        |
| Secondo tentativo in 10 minuti                         | +15       | Oltre al controllo di frequenza                |
| Nome modificato più volte con stessa email/dispositivo | +15       | Come negli screenshot; solo segnale secondario |
| Email checkout diversa dall’email payer PayPal         | +35       | Valutazione post-capture; forza review         |
| Seller protection non idonea, se disponibile           | +25       | Non usare come unico criterio                  |
| Precedente dispute/reversal associato                  | +60       | Forza review o block                           |
| Almeno 3 ordini paid senza contestazioni               | −20       | Minimo score finale 0                          |
| Turnstile fallito o token riutilizzato                 | Hard fail | Non è un semplice punteggio                    |

| **Score** | **Decisione pre-PSP** | **Decisione post-payment**                                      |
|-----------|-----------------------|-----------------------------------------------------------------|
| 0–29      | ALLOW                 | Fulfillment se capture COMPLETED                                |
| 30–49     | CHALLENGE             | Fulfillment se challenge e capture validi                       |
| 50–69     | CHALLENGE_STRICT      | Una sola operazione; review se presente un segnale payer        |
| ≥ 70      | BLOCK_TEMPORARY       | Nessuna nuova creazione PSP; revisione manuale se già catturato |

## 6.4 Policy per SKU

Le quantità non devono essere hardcodate nel motore antifrode. Il catalogo deve poter dichiarare una policy per prodotto, per esempio:

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>fraudPolicy: {</p>
<p>publicCheckoutMaxQty: 2,</p>
<p>challengeFromQty: 2,</p>
<p>highResaleValue: true,</p>
<p>manualReviewFromTotalMinor: 30000</p>
<p>}</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

Per Microsoft 365 Family, una quantità di 5 unità da un nuovo cliente deve essere rifiutata dal checkout pubblico con invito a richiedere un preventivo commerciale. Questo riduce il rischio senza dipendere dal rilevamento dell’attaccante.

## 6.5 Policy mode

| **Modalità** | **Comportamento**                                                                           |
|--------------|---------------------------------------------------------------------------------------------|
| observe      | Calcola e registra decisione teorica, ma non blocca; WAF resta attivo.                      |
| challenge    | Applica Turnstile e dedupe; i block sono registrati ma solo i casi estremi vengono fermati. |
| enforce      | Applica tutte le soglie, i blocchi temporanei e il fulfillment gate.                        |

# 7. Modello dati

## 7.1 Separazione degli stati

Il singolo campo orders.status non è sufficiente per descrivere correttamente pagamento, rischio e consegna. La decisione introduce tre assi indipendenti:

| **Asse**           | **Valori minimi**                                                 |
|--------------------|-------------------------------------------------------------------|
| payment_status     | pending \| approved \| captured \| denied \| refunded \| reversed |
| risk_status        | unassessed \| approved \| challenge_required \| review \| blocked |
| fulfillment_status | not_ready \| ready \| fulfilled \| cancelled                      |

Durante la migrazione, il campo status esistente viene mantenuto come compatibilità e derivato dai nuovi campi. Il codice nuovo non deve usarlo come unica autorità.

## 7.2 Tabella checkout_attempts

| **Colonna**                          | **Tipo**      | **Scopo**                                                           |
|--------------------------------------|---------------|---------------------------------------------------------------------|
| id                                   | TEXT PK       | UUID server-side del tentativo                                      |
| created_at / updated_at / expires_at | TEXT ISO-8601 | Lifecycle e retention                                               |
| request_id / cf_ray                  | TEXT          | Correlazione tecnica                                                |
| payment_method                       | TEXT          | paypal \| stripe \| bank_transfer                                   |
| email_hash / device_hash / ip_hash   | TEXT          | HMAC-SHA256 versionato; nessun valore in chiaro                     |
| hash_version                         | INTEGER       | Rotazione del segreto HMAC                                          |
| session_hash / user_agent_hash       | TEXT          | Segnali minimizzati                                                 |
| cart_hash                            | TEXT          | Carrello canonico risolto server-side                               |
| total_minor / total_qty / currency   | INTEGER/TEXT  | Esposizione economica                                               |
| policy_version                       | TEXT          | Regole utilizzate                                                   |
| risk_score / risk_level              | INTEGER/TEXT  | Esito spiegabile                                                    |
| decision                             | TEXT          | allow \| reuse \| challenge \| block \| review                      |
| reason_codes                         | TEXT JSON     | Codici macchina, non messaggi liberi                                |
| challenge_id / challenge_status      | TEXT          | Turnstile single-use                                                |
| order_id / paypal_order_id           | TEXT          | Relazione con risorse create                                        |
| status                               | TEXT          | received \| allowed \| psp_created \| captured \| blocked \| failed |

## 7.3 Tabelle di supporto

| **Tabella**         | **Scopo**                                           | **Vincoli**                                           |
|---------------------|-----------------------------------------------------|-------------------------------------------------------|
| fraud_blocks        | Blocchi temporanei o manuali per dimensione hashata | expires_at obbligatorio salvo blocco manuale motivato |
| payment_events      | Webhook PayPal idempotenti                          | event_id UNIQUE; body ridotto o hashato               |
| fraud_admin_actions | Approve, block, unblock, override                   | Append-only; actor e timestamp obbligatori            |

## 7.4 Estensioni orders

| **Colonna**                                       | **Scopo**                                                         |
|---------------------------------------------------|-------------------------------------------------------------------|
| checkout_attempt_id                               | Collega l’ordine al tentativo ammesso                             |
| payment_status / risk_status / fulfillment_status | Stati separati                                                    |
| risk_score / risk_reasons / risk_policy_version   | Decisione al momento dell’ordine                                  |
| paypal_payer_id                                   | Riconciliazione e supporto                                        |
| paypal_payer_email                                | Confronto operativo; retention pari all’ordine e accesso limitato |
| payer_email_match                                 | same \| different \| unavailable                                  |
| reviewed_at / reviewed_by / review_decision       | Audit revisione manuale                                           |
| capture_request_id                                | Idempotenza distinta della capture                                |

## 7.5 Migrazione SQL proposta

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>-- schema-fraud-protection-migration.sql</p>
<p>CREATE TABLE IF NOT EXISTS checkout_attempts (</p>
<p>id TEXT PRIMARY KEY,</p>
<p>created_at TEXT NOT NULL,</p>
<p>updated_at TEXT NOT NULL,</p>
<p>expires_at TEXT NOT NULL,</p>
<p>request_id TEXT NOT NULL,</p>
<p>cf_ray TEXT,</p>
<p>payment_method TEXT NOT NULL,</p>
<p>email_hash TEXT NOT NULL,</p>
<p>device_hash TEXT,</p>
<p>ip_hash TEXT NOT NULL,</p>
<p>hash_version INTEGER NOT NULL DEFAULT 1,</p>
<p>session_hash TEXT,</p>
<p>user_agent_hash TEXT,</p>
<p>cart_hash TEXT NOT NULL,</p>
<p>total_minor INTEGER NOT NULL,</p>
<p>total_qty INTEGER NOT NULL,</p>
<p>currency TEXT NOT NULL,</p>
<p>policy_version TEXT NOT NULL,</p>
<p>risk_score INTEGER NOT NULL DEFAULT 0,</p>
<p>risk_level TEXT NOT NULL,</p>
<p>decision TEXT NOT NULL,</p>
<p>reason_codes TEXT NOT NULL DEFAULT '[]',</p>
<p>challenge_id TEXT,</p>
<p>challenge_status TEXT,</p>
<p>order_id TEXT,</p>
<p>paypal_order_id TEXT,</p>
<p>status TEXT NOT NULL</p>
<p>);</p>
<p>CREATE INDEX IF NOT EXISTS idx_attempts_email_created</p>
<p>ON checkout_attempts(email_hash, created_at);</p>
<p>CREATE INDEX IF NOT EXISTS idx_attempts_device_created</p>
<p>ON checkout_attempts(device_hash, created_at);</p>
<p>CREATE INDEX IF NOT EXISTS idx_attempts_ip_created</p>
<p>ON checkout_attempts(ip_hash, created_at);</p>
<p>CREATE INDEX IF NOT EXISTS idx_attempts_cart_created</p>
<p>ON checkout_attempts(cart_hash, created_at);</p>
<p>CREATE INDEX IF NOT EXISTS idx_attempts_order</p>
<p>ON checkout_attempts(order_id);</p>
<p>CREATE TABLE IF NOT EXISTS fraud_blocks (</p>
<p>id TEXT PRIMARY KEY,</p>
<p>dimension TEXT NOT NULL,</p>
<p>identifier_hash TEXT NOT NULL,</p>
<p>reason_code TEXT NOT NULL,</p>
<p>source TEXT NOT NULL,</p>
<p>created_at TEXT NOT NULL,</p>
<p>expires_at TEXT,</p>
<p>created_by TEXT,</p>
<p>active INTEGER NOT NULL DEFAULT 1,</p>
<p>UNIQUE(dimension, identifier_hash, active)</p>
<p>);</p>
<p>CREATE TABLE IF NOT EXISTS payment_events (</p>
<p>event_id TEXT PRIMARY KEY,</p>
<p>event_type TEXT NOT NULL,</p>
<p>resource_id TEXT,</p>
<p>order_id TEXT,</p>
<p>received_at TEXT NOT NULL,</p>
<p>processed_at TEXT,</p>
<p>processing_status TEXT NOT NULL,</p>
<p>payload_sha256 TEXT NOT NULL</p>
<p>);</p>
<p>ALTER TABLE orders ADD COLUMN checkout_attempt_id TEXT;</p>
<p>ALTER TABLE orders ADD COLUMN payment_status TEXT NOT NULL DEFAULT 'pending';</p>
<p>ALTER TABLE orders ADD COLUMN risk_status TEXT NOT NULL DEFAULT 'unassessed';</p>
<p>ALTER TABLE orders ADD COLUMN fulfillment_status TEXT NOT NULL DEFAULT 'not_ready';</p>
<p>ALTER TABLE orders ADD COLUMN risk_score INTEGER NOT NULL DEFAULT 0;</p>
<p>ALTER TABLE orders ADD COLUMN risk_reasons TEXT NOT NULL DEFAULT '[]';</p>
<p>ALTER TABLE orders ADD COLUMN risk_policy_version TEXT;</p>
<p>ALTER TABLE orders ADD COLUMN paypal_payer_id TEXT;</p>
<p>ALTER TABLE orders ADD COLUMN paypal_payer_email TEXT;</p>
<p>ALTER TABLE orders ADD COLUMN payer_email_match TEXT;</p>
<p>ALTER TABLE orders ADD COLUMN capture_request_id TEXT;</p>
<p>ALTER TABLE orders ADD COLUMN reviewed_at TEXT;</p>
<p>ALTER TABLE orders ADD COLUMN reviewed_by TEXT;</p>
<p>ALTER TABLE orders ADD COLUMN review_decision TEXT;</p>
<p>CREATE UNIQUE INDEX IF NOT EXISTS idx_orders_attempt_unique</p>
<p>ON orders(checkout_attempt_id)</p>
<p>WHERE checkout_attempt_id IS NOT NULL;</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 7.6 HMAC degli identificatori

Non usare SHA-256 semplice per email o IP: entrambi hanno spazio di ricerca ridotto e sarebbero reversibili per dizionario. Usare HMAC-SHA-256 con FRAUD_HASH_SECRET, prefisso di dominio e versione.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>async function hmacIdentifier(secret, kind, normalizedValue, version = 1) {</p>
<p>const key = await crypto.subtle.importKey(</p>
<p>'raw', new TextEncoder().encode(secret),</p>
<p>{ name: 'HMAC', hash: 'SHA-256' }, false, ['sign']</p>
<p>);</p>
<p>const payload = `${version}:${kind}:${normalizedValue}`;</p>
<p>const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(payload));</p>
<p>return [...new Uint8Array(sig)].map(b =&gt; b.toString(16).padStart(2, '0')).join('');</p>
<p>}</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 8. Flussi applicativi

## 8.1 Creazione ordine PayPal

| **Passo** | **Componente**  | **Azione**                                                                               |
|-----------|-----------------|------------------------------------------------------------------------------------------|
| 1         | Frontend        | Valida UX, invia idempotencyKey, customer, items, lang e challenge response se presente. |
| 2         | Pages Function  | Valida request e risolve carrello/prezzi/stock server-side.                              |
| 3         | Request context | Genera requestId; legge CF-Connecting-IP, cf-ray e cookie aml_device.                    |
| 4         | Fraud library   | Normalizza, calcola HMAC/cartHash e applica policy SKU.                                  |
| 5         | Checkout Guard  | Consuma atomicamente i contatori e controlla lease/blocklist.                            |
| 6a        | Guard           | REUSE: restituisce l’ordine attivo solo alla stessa lease/device.                        |
| 6b        | Guard           | CHALLENGE: emette challengeId con TTL 5 minuti.                                          |
| 6c        | Guard           | BLOCK: risponde 429/403 senza creare order o chiamare PayPal.                            |
| 7         | Turnstile       | Siteverify server-side; verifica success, hostname e action.                             |
| 8         | D1              | Registra checkout_attempts e crea orders solo su ALLOW.                                  |
| 9         | PayPal          | Crea order con PayPal-Request-Id stabile e aggiorna D1/lease.                            |

## 8.2 Challenge adattiva

Il primo request che richiede verifica non deve essere contato due volte quando il browser riprova con il token. Il server restituisce un challengeId opaco. Il Checkout Guard memorizza l’evento e, al retry, riconosce lo stesso challengeId, verifica che non sia scaduto o già consumato e converte la decisione in ALLOW senza aggiungere un nuovo tentativo indipendente.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>HTTP 403</p>
<p>{</p>
<p>"code": "CHALLENGE_REQUIRED",</p>
<p>"challengeId": "opaque-signed-id",</p>
<p>"message": "Please complete the security verification."</p>
<p>}</p>
<p>Retry body additions:</p>
<p>{</p>
<p>"challengeId": "opaque-signed-id",</p>
<p>"turnstileToken": "..."</p>
<p>}</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

Turnstile richiede obbligatoriamente la validazione Siteverify server-side; i token sono monouso e scadono dopo 300 secondi \[R5\]. Il backend deve verificare anche hostname e action=checkout_paypal.

## 8.3 Capture PayPal

- Recuperare l’ordine esclusivamente tramite paypal_order_id già associato in D1.

- Rifiutare capture se risk_status è blocked o se l’ordine non è nello stato atteso.

- Inviare PayPal-Request-Id distinto dalla create, per esempio AML-XXXX:CAPTURE.

- Gestire timeout: ripetere la stessa capture request, mai generarne una nuova con chiave diversa.

- Accettare fulfillment solo con stato COMPLETED, importo e valuta coerenti.

- Estrarre payer ID/email e seller protection quando disponibili; aggiornare il risk engine post-payment.

- Se D1 fallisce dopo una capture riuscita, mostrare “pagamento in elaborazione” e affidarsi al webhook per la riconciliazione.

## 8.4 Flusso di fulfillment

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>payment_status == captured</p>
<p>AND risk_status == approved</p>
<p>AND fulfillment_status == ready</p>
<p>=&gt; può iniziare la consegna</p>
<p>Qualsiasi altra combinazione</p>
<p>=&gt; nessuna chiave/licenza inviata</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

La mail “pagamento ricevuto” può essere inviata durante una revisione, ma deve essere distinta dalla comunicazione che contiene o abilita la licenza. Il sistema non deve promettere consegna immediata quando risk_status=review.

## 8.5 Bonifico e Stripe

Il gate deve essere condiviso da tutti gli endpoint che creano una risorsa commerciale o inviano email. Le soglie possono variare per metodo: il bonifico ha minore rischio di chargeback immediato ma è vulnerabile allo spam; Stripe dispone di propri segnali antifrode ma deve comunque rispettare dedupe, quantità e limiti applicativi.

# 9. Integrazione PayPal

## 9.1 Idempotenza per tipo di operazione

| **Operazione** | **PayPal-Request-Id**          | **Persistenza**                               |
|----------------|--------------------------------|-----------------------------------------------|
| Create order   | orderId interno o UUID stabile | orders.paypal_order_id                        |
| Capture order  | capture_request_id distinto    | orders.capture_request_id + paypal_capture_id |
| Refund         | refund_request_id distinto     | tabella refund/evento dedicata                |

PayPal documenta che PayPal-Request-Id rende idempotenti le POST supportate e raccomanda un valore univoco per tipo di chiamata; richieste simultanee con la stessa chiave possono far fallire la seconda, quindi il chiamante deve trattare il risultato come retry e interrogare lo stato \[R6\].

## 9.2 Webhook obbligatori

| **Evento**                        | **Azione AML Store**                                                  |
|-----------------------------------|-----------------------------------------------------------------------|
| PAYMENT.CAPTURE.COMPLETED         | Conferma payment_status=captured; valuta fulfillment gate.            |
| PAYMENT.CAPTURE.PENDING           | Mantiene not_ready; nessuna consegna.                                 |
| PAYMENT.CAPTURE.DENIED            | Marca denied e annulla fulfillment.                                   |
| PAYMENT.CAPTURE.REFUNDED          | Marca refunded; revoca o annota la licenza se possibile.              |
| PAYMENT.CAPTURE.REVERSED          | Marca reversed; alert immediato.                                      |
| CUSTOMER.DISPUTE.CREATED          | Apre caso antifrode, collega payer/capture, blocca segnali associati. |
| CUSTOMER.DISPUTE.UPDATED/RESOLVED | Aggiorna esito e storico del rischio.                                 |

## 9.3 Verifica webhook

La route /api/webhooks/paypal deve leggere il body originale, verificare la firma con l’endpoint PayPal verify-webhook-signature e il PAYPAL_WEBHOOK_ID, quindi inserire payment_events con event_id UNIQUE. Senza verifica non esiste garanzia che il mittente sia PayPal \[R7\]\[R8\].

La prima implementazione sceglie la verifica postback per ridurre il rischio di errori crittografici custom. L’endpoint deve rispondere 2xx solo dopo aver persistito in modo sicuro l’evento o aver riconosciuto un duplicato; PayPal ritenta le consegne non confermate \[R7\].

## 9.4 Correzioni a functions/api/\_lib/paypal.js

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>export async function capturePaypalOrder(baseUrl, token, paypalOrderId, requestId) {</p>
<p>const res = await fetch(`${baseUrl}/v2/checkout/orders/${paypalOrderId}/capture`, {</p>
<p>method: 'POST',</p>
<p>headers: {</p>
<p>Authorization: `Bearer ${token}`,</p>
<p>'Content-Type': 'application/json',</p>
<p>'PayPal-Request-Id': requestId,</p>
<p>},</p>
<p>body: '{}',</p>
<p>});</p>
<p>// Restituire anche payer, seller protection e debug_id normalizzati.</p>
<p>// Non loggare il payload completo in produzione.</p>
<p>}</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 10. API e gestione errori

## 10.1 Contratto di risposta

| **HTTP** | **code**               | **Significato**                                   | **Comportamento frontend**                                 |
|----------|------------------------|---------------------------------------------------|------------------------------------------------------------|
| 200      | OK / REUSED            | Order PayPal creato o riutilizzato                | Apre PayPal Buttons normalmente                            |
| 403      | CHALLENGE_REQUIRED     | Serve verifica umana                              | Esegue Turnstile e ritenta una volta                       |
| 403      | CHECKOUT_BLOCKED       | Blocco manuale o hard rule                        | Messaggio generico + supporto                              |
| 409      | ALREADY_PENDING        | Checkout equivalente attivo altrove               | Invita ad attendere o riprendere sul dispositivo originale |
| 422      | POLICY_REJECTED        | Quantità/SKU non consentita nel checkout pubblico | Mostra alternativa commerciale                             |
| 429      | CHECKOUT_RATE_LIMITED  | Soglia temporale superata                         | Rispetta Retry-After; disabilita retry                     |
| 503      | PROTECTION_UNAVAILABLE | Guard non disponibile                             | Nessun ordine creato; riprovare più tardi                  |

## 10.2 Header obbligatori

- Cache-Control: no-store su tutte le risposte checkout e webhook.

- Retry-After sui 429, espresso in secondi.

- X-Request-ID generato server-side e riportato nei log.

- Set-Cookie per aml_device: Secure; HttpOnly; SameSite=Lax; Path=/; Max-Age configurato.

- Nessun reason code interno dettagliato nel messaggio umano; il code macchina può restare generico.

## 10.3 Modifica CORS

Poiché checkout e API sono same-origin, il cookie viene inviato automaticamente. Non serve esporre un header device al JavaScript. Se si introduce X-Checkout-Session, aggiungerlo esplicitamente ad Access-Control-Allow-Headers, ma non usarlo come prova di identità.

## 10.4 Pseudocodice del nuovo handler

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>async function handlePaypalCreateOrder(request, env) {</p>
<p>assertBasicRequest(request, env);</p>
<p>const body = await readAndValidateBody(request);</p>
<p>const params = await resolveOrderParams(body, 'paypal', env);</p>
<p>const ctx = await buildFraudContext(request, params, env);</p>
<p>const guard = await evaluateCheckoutGuard(env.CHECKOUT_GUARD, ctx);</p>
<p>if (guard.decision === 'BLOCK') return rateLimited(guard.retryAfter);</p>
<p>if (guard.decision === 'CHALLENGE') {</p>
<p>const verified = await verifyTurnstileOrRequestChallenge(body, ctx, guard, env);</p>
<p>if (!verified.allowed) return verified.response;</p>
<p>}</p>
<p>if (guard.decision === 'REUSE') return json(guard.publicReuseResponse);</p>
<p>const attemptId = crypto.randomUUID();</p>
<p>await insertCheckoutAttempt(env.DB, attemptId, ctx, guard);</p>
<p>try {</p>
<p>const orderId = await createOrderFromApprovedAttempt(env.DB, attemptId, params);</p>
<p>const paypalId = await createPaypalOrderIdempotently(orderId, params, env);</p>
<p>await linkAttemptAndCommitLease(env, attemptId, orderId, paypalId, guard.leaseToken);</p>
<p>return json({ orderID: paypalId, amlOrderId: orderId });</p>
<p>} catch (error) {</p>
<p>await markAttemptFailedAndReleaseLease(env, attemptId, guard.leaseToken, error);</p>
<p>throw error;</p>
<p>}</p>
<p>}</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 11. Admin e operatività

## 11.1 Nuove viste

| **Vista**           | **Contenuto**                                                                        |
|---------------------|--------------------------------------------------------------------------------------|
| Tentativi sospetti  | Gruppi per email hash/dispositivo/carrello con conteggio, intervallo e reason codes. |
| Revisione pagamenti | Ordini captured con risk_status=review e confronto email checkout/payer.             |
| Blocchi attivi      | Dimensione, durata, motivo, sorgente automatica/manuale e operatore.                 |
| Eventi PayPal       | Webhook recenti, duplicati, errori di verifica e stato elaborazione.                 |

## 11.2 Presentazione degli ordini spam

La lista principale non deve mostrare ogni tentativo non ammesso come ordine. I tentativi restano in una vista tecnica aggregata. Per esempio: “8 tentativi in 9 minuti — stesso email hash, stesso carrello, 5× Microsoft 365 Family — 7 bloccati, 1 pending”.

## 11.3 Azioni amministrative

- Approve order: approvazione puntuale dell’ordine, non allowlist globale del cliente.

- Block 1h / 24h / 7d: blocco temporaneo su email, dispositivo o combinazione; l’IP da solo richiede motivazione.

- Unblock: conserva l’azione precedente e aggiunge un evento di revoca.

- Refund / mark refunded: usa chiave idempotente e attende riconciliazione PayPal.

- Export evidence: produce un dossier senza segreti, utile per contestazioni.

## 11.4 Runbook incidente

13. Verificare che gli ordini siano pending/review e che nessuna licenza sia stata consegnata.

14. Applicare blocco temporaneo a email hash e dispositivo; usare IP solo come segnale aggiuntivo.

15. Controllare PayPal order/capture e la presenza di dispute.

16. Se il pagamento è catturato e contestato, sospendere fulfillment e seguire la procedura PayPal.

17. Annotare il caso e aggiornare policy/threshold solo dopo verifica dei falsi positivi.

# 12. Privacy e sicurezza

## 12.1 Minimizzazione

Il GDPR richiede finalità determinate, minimizzazione, limitazione della conservazione e misure tecniche adeguate al rischio \[R9\]. Il sistema raccoglie solo segnali necessari a prevenire abuso del checkout e non li riutilizza per marketing o profilazione commerciale.

| **Dato**             | **Trattamento deciso**                                                                           |
|----------------------|--------------------------------------------------------------------------------------------------|
| Email tentativo      | Normalizzata e HMAC in checkout_attempts; in chiaro resta solo nell’ordine contrattuale ammesso. |
| IP                   | Letto da CF-Connecting-IP, HMAC immediato; non persistito in chiaro nel database antifrode.      |
| Dispositivo          | UUID casuale first-party; nessun canvas/audio/font fingerprinting.                               |
| User-Agent           | Hash o categoria ridotta; evitare stringa completa se non necessaria.                            |
| Paese/ASN Cloudflare | Solo segnale secondario e aggregato; nessun blocco geografico automatico.                        |
| Payer PayPal         | Accesso limitato al supporto/revisione; retention collegata all’ordine.                          |

## 12.2 Cookie e fingerprinting

La decisione rifiuta fingerprinting passivo invasivo. Il Garante italiano ha ribadito nel 2026 che tecniche di fingerprinting non strettamente necessarie e basate su dati estesi del dispositivo non possono essere automaticamente assimilate a cookie tecnici \[R10\]. AML Store usa un identificatore casuale first-party, documentato nell’informativa e sottoposto a verifica legale della corretta base e classificazione.

## 12.3 Retention iniziale

| **Categoria**                         | **Retention proposta**                                            |
|---------------------------------------|-------------------------------------------------------------------|
| checkout_attempts dettagliati         | 90 giorni                                                         |
| eventi Turnstile e rate limit tecnici | 30 giorni                                                         |
| blocchi automatici scaduti            | 90 giorni dopo la scadenza                                        |
| metriche aggregate non identificative | 12 mesi                                                           |
| dati ordine/pagamento                 | Policy contabile e contrattuale separata, invariata da questo ADR |

La retention deve essere eseguita da una procedura schedulata e verificata con test. Non basta dichiararla nell’informativa.

## 12.4 Segreti e accesso

- FRAUD_HASH_SECRET e TURNSTILE_SECRET_KEY come Cloudflare secrets, mai nel repository.

- PAYPAL_WEBHOOK_ID come variabile di ambiente; secret e client secret già server-side.

- Ruoli admin: sola lettura, revisore e amministratore; approvazioni e blocchi richiedono identità Cloudflare Access.

- Log redatti: niente token Turnstile, credenziali, payload PayPal completo o email/IP in chiaro.

- Rotazione HMAC versionata con periodo di doppia lettura; non sovrascrivere la storia senza piano.

# 13. Osservabilità

## 13.1 Log strutturati

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>{</p>
<p>"event": "checkout_guard_decision",</p>
<p>"requestId": "...",</p>
<p>"cfRay": "...",</p>
<p>"paymentMethod": "paypal",</p>
<p>"decision": "BLOCK",</p>
<p>"riskScore": 85,</p>
<p>"reasonCodes": ["EMAIL_30M_LIMIT", "HIGH_QTY", "HIGH_TOTAL"],</p>
<p>"policyVersion": "fraud-v1",</p>
<p>"counts": { "email30m": 4, "device30m": 4, "ip30m": 5 },</p>
<p>"latencyMs": 18</p>
<p>}</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

Il log non contiene email, IP, nome o token. Gli hash completi non devono essere emessi nei log generali; è sufficiente un correlation key tronco non reversibile.

## 13.2 Metriche minime

- checkout_create_requests_total per metodo.

- guard_decisions_total per ALLOW/REUSE/CHALLENGE/BLOCK.

- turnstile_requested, passed, failed, expired e duplicate.

- duplicate_orders_suppressed_total.

- pending_orders_created / completed_payments ratio.

- manual_review_approved / rejected e tempo medio di revisione.

- PayPal disputes, reversals e refund per 100 pagamenti.

- false_positive_overrides, misurato sugli override manuali.

## 13.3 Alert iniziali

| **Condizione**                                | **Severità**                               |
|-----------------------------------------------|--------------------------------------------|
| Più di 10 BLOCK in 5 minuti                   | Warning — possibile campagna automatizzata |
| Più di 3 tentativi ≥ 500 € in 10 minuti       | High                                       |
| Webhook signature failure                     | High                                       |
| Capture COMPLETED ma aggiornamento D1 fallito | Critical — riconciliazione necessaria      |
| Guard 5xx \> 1% per 5 minuti                  | High — checkout bloccato                   |
| Tasso challenge failure \> 30%                | Warning — bot o problema UX                |

## 13.4 Obiettivi di successo

- Riduzione ≥ 95% delle righe ordine pending generate da burst ripetuti.

- Un solo ordine/PayPal order per retry equivalente sullo stesso dispositivo.

- Nessuna consegna su PAYMENT.CAPTURE.PENDING o risk_status=review.

- Falsi positivi confermati inferiori all’1% dei checkout legittimi dopo tuning.

# 14. Test e criteri di accettazione

## 14.1 Test unitari

- Normalizzazione email, IP, device e carrello canonico.

- Calcolo score e precedenza delle hard rule.

- Policy SKU e limiti quantità.

- Reason codes stabili per ogni scenario.

- HMAC deterministico per versione e separazione tra domini email/ip/device.

- Mapping stati payment/risk/fulfillment.

## 14.2 Test di concorrenza

| **Scenario**                                            | **Esito atteso**                                                      |
|---------------------------------------------------------|-----------------------------------------------------------------------|
| 20 create simultanee stessa lease                       | 1 ALLOW, 19 REUSE/BLOCK; una sola riga orders e un solo PayPal order. |
| 4 sessioni diverse, stessa email/dispositivo, 30 minuti | Massimo 2 attraversano challenge; le successive 429.                  |
| Stessa IP, email e device differenti                    | Challenge progressiva; evitare blocco permanente solo-IP.             |
| Retry dopo timeout PayPal create                        | Stesso PayPal order tramite identico PayPal-Request-Id.               |
| Retry capture dopo timeout                              | Una sola capture; stato recuperabile.                                 |

## 14.3 Test Turnstile

- Token valido, action e hostname corretti: challenge passa una sola volta.

- Token scaduto, duplicato, action errata o hostname errato: rifiuto.

- Siteverify timeout: 503 e nessuna creazione ordine quando challenge è richiesta.

- Test key Cloudflare in locale/preview; secret di produzione mai usato nei test.

## 14.4 Test PayPal e webhook

- Sandbox: create, approve, capture, refund e negative testing.

- Webhook firma valida, firma invalida, event_id duplicato e ordine non trovato.

- PAYMENT.CAPTURE.PENDING non sblocca fulfillment.

- Mismatch importo/valuta produce 409 e alert.

- Dispute webhook collega il capture e porta risk_status a review/blocked.

## 14.5 Criteri di accettazione principali

| **ID** | **Criterio**                                                                                                            |
|--------|-------------------------------------------------------------------------------------------------------------------------|
| AC-01  | Otto tentativi identici in 10 minuti producono al massimo un ordine attivo e almeno cinque risposte bloccate/challenge. |
| AC-02  | Nessuna chiamata PayPal viene eseguita se Checkout Guard restituisce BLOCK.                                             |
| AC-03  | Un refresh o doppio click non crea un nuovo ordine.                                                                     |
| AC-04  | Le richieste concorrenti non superano la soglia configurata.                                                            |
| AC-05  | Il database antifrode non contiene email o IP in chiaro.                                                                |
| AC-06  | Un webhook falso non modifica alcun ordine.                                                                             |
| AC-07  | La coda admin raggruppa i tentativi bloccati e mostra una sola entità operativa.                                        |
| AC-08  | La consegna è impossibile finché payment_status e risk_status non sono approvati.                                       |

# 15. Piano di rilascio

## 15.1 Fase 0 — mitigazione immediata

- Aggiungere WAF Rate Limiting su /api/paypal-create-order e /api/paypal-capture-order.

- Impostare publicCheckoutMaxQty=2 per SKU digitali consumer ad alta rivendibilità.

- Bloccare temporaneamente le identità dell’incidente attuale.

- Nascondere o aggregare in admin i pending duplicati non pagati.

## 15.2 Fase 1 — modello e dedupe

- Applicare schema-fraud-protection-migration.sql.

- Aggiungere request context, HMAC, checkout_attempts e policy configurabile.

- Introdurre aml_device cookie e deduplicazione server-side.

- Deploy in FRAUD_PROTECTION_MODE=observe per almeno 48 ore.

## 15.3 Fase 2 — enforcement atomico e Turnstile

- Creare Worker separato workers/checkout-guard con Durable Object SQLite.

- Bind CHECKOUT_GUARD al progetto Pages; Cloudflare Pages supporta binding a un DO deployato da un Worker separato \[R11\].

- Integrare challenge adattiva e Siteverify.

- Passare da observe a challenge, poi enforce dopo verifica metriche.

## 15.4 Fase 3 — PayPal e backoffice

- Aggiungere idempotenza capture e webhook PayPal verificati.

- Separare payment/risk/fulfillment status.

- Implementare coda review, blocchi e audit admin.

- Aggiungere alert e report settimanale dei falsi positivi.

## 15.5 Feature flags e segreti

| **Nome**              | **Tipo**          | **Scopo**                       |
|-----------------------|-------------------|---------------------------------|
| FRAUD_PROTECTION_MODE | var               | observe \| challenge \| enforce |
| FRAUD_POLICY_VERSION  | var               | fraud-v1                        |
| FRAUD_HASH_VERSION    | var               | Versione HMAC attiva            |
| FRAUD_HASH_SECRET     | secret            | HMAC identificatori             |
| TURNSTILE_SITE_KEY    | var               | Chiave pubblica widget          |
| TURNSTILE_SECRET_KEY  | secret            | Siteverify                      |
| PAYPAL_WEBHOOK_ID     | var/secret config | Verifica webhook                |
| CHECKOUT_GUARD        | binding           | Durable Object namespace        |

## 15.6 Rollback

Il rollback non deve eliminare tabelle o dati. Impostare FRAUD_PROTECTION_MODE=observe disattiva l’enforcement mantenendo audit e WAF. Se il Durable Object è indisponibile in produzione, il kill switch temporaneo può consentire solo checkout sotto una soglia economica molto bassa; questa eccezione deve essere esplicita, limitata nel tempo e registrata. Il default resta fail closed per nuove operazioni monetarie.

# 16. Conseguenze e alternative

## 16.1 Conseguenze positive

- Riduzione drastica dello spam di ordini e delle chiamate PSP inutili.

- Controlli resistenti a race condition e retry concorrenti.

- Decisioni spiegabili e adattabili senza introdurre machine learning opaco.

- Migliore prova operativa in caso di dispute PayPal.

- Separazione corretta tra pagamento e consegna digitale.

- Base riutilizzabile per Stripe, bonifico, richieste commerciali e futuri metodi.

## 16.2 Costi e rischi introdotti

- Nuovo Worker Durable Object, binding e pipeline di deploy locale più complessa.

- Possibili falsi positivi iniziali, soprattutto su reti mobili/NAT e acquisti multipli legittimi.

- Latenza aggiuntiva e dipendenza da Turnstile nei casi sospetti.

- Necessità di monitoraggio, retention automatica e revisione periodica delle policy.

- Migrazione dello stato ordine e modifiche al backoffice.

## 16.3 Alternative considerate

| **Alternativa**                                 | **Esito**                         | **Motivazione**                                                               |
|-------------------------------------------------|-----------------------------------|-------------------------------------------------------------------------------|
| Solo debounce/disabilitazione pulsante frontend | Rifiutata                         | Aggirabile chiamando direttamente l’API o aprendo nuove sessioni.             |
| Solo idempotencyKey client + UNIQUE D1          | Rifiutata                         | Non limita nuove chiavi e non identifica abuso cross-session.                 |
| Solo WAF Rate Limiting                          | Rifiutata come autorità unica     | Contatori per data center e pochi segnali business; utile come L0.            |
| Workers Rate Limiting API come unico contatore  | Rifiutata                         | Permissiva/eventualmente consistente e locale; non accounting preciso \[R3\]. |
| Contatori esclusivamente D1                     | Rifiutata per enforcement stretto | Possibili race/check-then-act e carico globale; D1 resta audit.               |
| KV per contatori                                | Rifiutata                         | Consistenza eventuale non adatta al limite massimo esatto.                    |
| Servizio antifrode SaaS completo                | Rinviata                          | Costo, lock-in e privacy non giustificati per il volume attuale.              |
| Fingerprinting avanzato                         | Rifiutata                         | Rischio privacy e complessità; non necessario per v1.                         |
| PayPal AUTHORIZE per tutti gli ordini           | Rinviata                          | Cambia il checkout e la gestione autorizzazioni; prima bloccare a monte.      |

## 16.4 Trigger di riesame ADR

- Traffico checkout tale da rendere il singolo Durable Object un collo di bottiglia.

- Falsi positivi superiori all’1% per due settimane.

- Aumento significativo di frodi distribuite che ruotano email e dispositivi.

- Introduzione di account cliente, wallet o consegna automatica istantanea delle chiavi.

- Adozione di PayPal authorization/capture differita o di un provider antifrode esterno.

# 17. Checklist implementativa

## 17.1 Repository e schema

- [ ] Creare docs/adr/ADR-001-checkout-antifrode.md.

- [ ] Aggiungere migration SQL e script di inizializzazione locale.

- [ ] Estendere order.js con stati separati e transizioni condizionali.

## 17.2 Protezione

- [ ] Aggiungere fraud.js, request-context.js e turnstile.js.

- [ ] Creare Worker checkout-guard e binding Pages.

- [ ] Implementare HMAC versionato e cookie aml_device.

- [ ] Applicare policy a PayPal, Stripe e bonifico prima di createOrder().

## 17.3 PayPal

- [ ] Aggiungere PayPal-Request-Id alla capture.

- [ ] Aggiungere webhook verificato e payment_events.

- [ ] Estrarre payer/seller protection in modo difensivo.

## 17.4 Frontend e admin

- [ ] Gestire CHALLENGE_REQUIRED, 429 e Retry-After.

- [ ] Render Turnstile in modalità execute/interaction-only.

- [ ] Aggiungere viste tentativi, review e blocchi.

- [ ] Separare email di ricezione pagamento da consegna licenza.

## 17.5 Operazioni

- [ ] Creare WAF rules e testarle prima in log/challenge.

- [ ] Configurare segreti e variabili per preview e production.

- [ ] Definire retention job, alert e dashboard.

- [ ] Eseguire rollout observe → challenge → enforce.

# 18. Riferimenti

**\[R1\]** [<u>OWASP — Business Logic Security Cheat Sheet</u>](https://cheatsheetseries.owasp.org/cheatsheets/Business_Logic_Security_Cheat_Sheet.html)

**\[R2\]** [<u>OWASP — Automated Threats to Web Applications / Cashing Out</u>](https://owasp.org/www-project-automated-threats-to-web-applications/)

**\[R3\]** [<u>Cloudflare Workers — Rate Limiting API: locality and accuracy</u>](https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/)

**\[R4\]** [<u>Cloudflare WAF — How request rates are calculated</u>](https://developers.cloudflare.com/waf/rate-limiting-rules/request-rate/)

**\[R5\]** [<u>Cloudflare Turnstile — Server-side token validation</u>](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/)

**\[R6\]** [<u>PayPal REST API — Idempotency</u>](https://developer.paypal.com/api/rest/reference/idempotency/)

**\[R7\]** [<u>PayPal — Webhooks overview and delivery semantics</u>](https://developer.paypal.com/api/rest/webhooks)

**\[R8\]** [<u>PayPal — Verify webhook signature API</u>](https://developer.paypal.com/api/webhooks/v1/verify-webhook-signature-post/)

**\[R9\]** [<u>Regolamento (UE) 2016/679 — articoli 5 e 32</u>](https://eur-lex.europa.eu/legal-content/IT-EN/TXT/?uri=CELEX:32016R0679)

**\[R10\]** [<u>Garante Privacy — Provvedimento 17 aprile 2026, fingerprinting e stretta necessità</u>](https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10241537)

**\[R11\]** [<u>Cloudflare Pages Functions — Bindings e Durable Objects</u>](https://developers.cloudflare.com/pages/functions/bindings/)

## 18.1 Fonti del repository analizzate

- functions/api/\[\[catchall\]\].js — routing e flussi PayPal/Stripe/bonifico.

- functions/api/\_lib/order.js — creazione e transizioni ordini D1.

- functions/api/\_lib/paypal.js — Orders API e PayPal-Request-Id sulla create.

- js/checkout.js — idempotenza client e PayPal Buttons.

- schema.sql — schema D1 corrente.

- wrangler.toml — binding e configurazione Cloudflare.

- package.json — toolchain Wrangler e assenza attuale di test automatizzati.

## 18.2 Decisione finale proposta

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>APPROVARE ADR-001</strong></p>
<p>Procedere con la soluzione multilivello. La priorità tecnica è spostare il controllo prima di createOrder(), introdurre un’autorità atomica per i tentativi e impedire che “tentativo” e “ordine commerciale” siano la stessa entità.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>
