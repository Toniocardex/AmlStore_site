# ADR-0001: Evoluzione della homepage verso un modello corporate commerce

- **Stato:** Proposed
- **Data:** 2026-08-04
- **Ambito:** homepage multilingue, header e footer condivisi
- **Decision owner:** da assegnare
- **Riferimento pubblico analizzato:** <https://www.aml-store.com/it/>

## Decisioni approvate

Le seguenti decisioni sono state approvate e possono guidare l'implementazione locale:

- la homepage manterrà un equilibrio tra e-commerce e B2B con priorità editoriale indicativa **30% privati / 70% professionisti e aziende**;
- il tono resterà commerciale, con una presentazione più strutturata e corporate;
- la hero userà come CTA primaria la richiesta di consulenza e come CTA secondaria l'accesso al catalogo;
- la consulenza non userà WhatsApp come canale primario;
- la destinazione raccomandata e approvata è una pagina con modulo breve che inoltra la richiesta a `Info@amlstore.it`;
- l'indirizzo email resterà visibile come alternativa al modulo;
- WhatsApp resterà disponibile per assistenza rapida, ma non sarà la CTA corporate principale;
- ogni modifica approvata alla struttura, ai componenti o alle funzionalità dovrà essere estesa a tutte le versioni linguistiche del sito;
- per l'Italia l'assistenza sarà erogata in italiano; per tutti gli altri Paesi l'assistenza sarà erogata in inglese, indipendentemente dalla lingua dell'interfaccia;
- i nuovi componenti visuali dovranno usare i token `--aml-*` del design system esistente e non introdurre una palette o un sistema tipografico parallelo;
- il modulo può essere collegato localmente all'endpoint reale in modalità `CONSULTATION_DRY_RUN=1`, così da verificare frontend e validazione senza inviare email; le misure anti-abuso restano bloccanti prima di qualsiasi rilascio;
- commit, push su `main` e deploy richiedono sempre una richiesta esplicita successiva alla verifica locale.

## Dati e claim verificati

I seguenti dati sono stati confermati il 2026-08-05 e possono essere usati nei contenuti corporate, nel footer e nei dati strutturati:

- **marchio:** Aml Store;
- **denominazione legale:** Licensoft di Cardelli Antonino;
- **sede:** Via Trento 5/A, 20015 Parabiago (MI), Italia;
- **assistenza:** dal lunedì al venerdì, dalle 09:00 alle 19:00, ora italiana;
- **canali coperti dagli orari:** email, telefono e WhatsApp;
- **lingue dell'assistenza:** italiano per l'Italia, inglese per tutti gli altri Paesi;
- **servizi B2B effettivamente offerti:** consulenza pre-acquisto, preventivi per più postazioni, soluzioni Server, database e Microsoft 365;
- **certificazioni, partnership, testimonianze e casi cliente utilizzabili:** nessuno attualmente approvato.

Non è approvato alcuno SLA sul tempo di risposta. Le formule “Rispondiamo h24”, “risposta entro un giorno lavorativo”, “miglior prezzo garantito” e le garanzie di rimborso sintetiche non devono essere presentate come claim corporate in assenza di condizioni pubbliche e verificabili.

## Stato dell'implementazione locale

Al 2026-08-05 sono disponibili localmente, ma non ancora destinati alla produzione:

- CTA hero e pagina dedicata nelle cinque lingue, con slug localizzati;
- tre accessi coerenti alla pagina in ogni lingua: CTA primaria della hero, CTA primaria del blocco aziende/professionisti e voce dedicata nell'area Supporto del footer;
- modulo accessibile con gli stessi campi, vincoli e stati funzionali in `/it/`, `/en/`, `/fr/`, `/de/` e `/es/`;
- endpoint same-origin `POST /api/consultation-request` nella Pages Function esistente;
- validazione e normalizzazione server-side, allowlist del tipo di richiesta, limite del payload a 32 KB e honeypot;
- modalità locale `CONSULTATION_DRY_RUN=1`, che produce un riferimento ma non chiama Resend;
- template email separati dal flusso ordini: notifica interna in italiano e conferma utente localizzata;
- destinatario interno `Info@amlstore.it`; il `Reply-To` della notifica interna coincide con l'email del richiedente;
- conferma in italiano per `/it/`, in inglese per `/en/` e localizzata per `/fr/`, `/de/`, `/es/`, con indicazione che l'assistenza fuori dall'Italia risponde in inglese;
- pagine consulenza ancora impostate su `noindex,nofollow`;
- footer condiviso con denominazione legale, sede e P.IVA raccolte nella barra inferiore; nessun testo descrittivo di brand nella colonna del logo; orari e lingua effettiva dell'assistenza restano nella card contatti; la navigazione è divisa tra Prodotti, Supporto operativo e Informazioni legali;
- metadati e dati strutturati delle cinque homepage privi del claim “miglior prezzo garantito” e completati con i dati societari approvati;
- rassicurazione sintetica sul rimborso sostituita nelle cinque hero con il supporto pre e post-vendita;
- blocco aziende/professionisti riscritto nelle cinque lingue sui servizi effettivamente disponibili;
- pagine contatti allineate agli orari e alle lingue approvate, senza promessa di risposta entro un giorno lavorativo.

L'integrazione riusa il servizio Resend già presente nel repository, ma mantiene template e funzione di invio separati dagli ordini. La consegna della notifica interna determina l'esito della richiesta; un eventuale errore della sola email di conferma non deve causare la perdita del lead. Il mittente resta temporaneamente quello Resend già verificato dal progetto (`Aml Store <ordini@aml-store.com>`): un indirizzo mittente dedicato alla consulenza richiederà una decisione e una verifica DNS/Resend esplicite.

## Contesto

La homepage attuale presenta AML Store come un e-commerce di licenze software chiaro, ordinato e rassicurante. Il percorso di acquisto, le categorie, i prodotti più venduti, i prezzi, la consegna digitale e le FAQ sono immediatamente comprensibili.

L'esperienza comunica però soprattutto una proposta retail basata su prodotto, prezzo e riduzione del rischio. L'identità dell'azienda, le competenze, il servizio e le ragioni per scegliere AML Store nel tempo restano secondari. Questo limita la capacità della homepage di:

- costruire un brand riconoscibile e difendibile;
- sostenere la vendita a professionisti e aziende;
- differenziarsi da un generico rivenditore di licenze;
- generare richieste di consulenza o preventivo;
- trasferire fiducia dall'acquisto singolo alla relazione con l'azienda.

### Evidenze della homepage attuale

- La hero usa il messaggio “La serenità di scegliere senza rischi”, efficace sul piano emotivo ma non distintivo.
- La navigazione principale è quasi interamente organizzata per famiglie di prodotto.
- “Come funziona” compare subito dopo la hero e inquadra l'esperienza come percorso di checkout.
- Il contenuto per aziende e professionisti è presente, ma limitato a un singolo blocco.
- Sei schede “I più venduti”, prezzi barrati e percentuali di sconto occupano una parte rilevante della pagina.
- La prova sociale è ridotta a un widget Trustpilot molto compatto e a un collegamento esterno.
- Il footer riporta P.IVA e contatti, ma non offre un vero percorso istituzionale.
- Su mobile la pagina non presenta overflow, ma il percorso è molto lungo e resta dominato dal catalogo.
- La console registra richieste Google Ads bloccate dalla Content Security Policy verso `pagead2.googlesyndication.com`.

## Decisione

Adotteremo per la homepage un modello **corporate commerce**: AML Store dovrà essere presentata prima come azienda competente e affidabile che aiuta persone e imprese a scegliere, acquistare e attivare software originale, mantenendo l'acquisto online come funzione primaria ma non come unica espressione del brand.

La homepage non diventerà un sito-vetrina puramente istituzionale e non nasconderà prezzi, prodotti o checkout. Il cambiamento riguarda la gerarchia: identità, destinatari, soluzioni e prove di affidabilità precederanno il catalogo promozionale.

## Principi vincolanti

1. **L'azienda precede il catalogo.** La prima schermata deve spiegare chi è AML Store, per chi lavora e quale servizio offre.
2. **Il valore non è soltanto il prezzo.** Scelta della licenza, fatturazione, consegna, attivazione e assistenza devono formare una proposta unitaria.
3. **Privati e aziende hanno percorsi distinti.** La homepage deve permettere a ciascun pubblico di riconoscersi senza creare due siti separati.
4. **Le prove devono essere verificabili.** Non sono ammessi numeri, certificazioni, partnership, autorizzazioni, SLA, testimonianze o loghi cliente non documentati.
5. **L'e-commerce resta immediatamente accessibile.** Catalogo, ricerca e carrello non devono essere indeboliti dal nuovo livello istituzionale.
6. **La struttura deve funzionare in cinque lingue.** La versione italiana potrà essere usata come pilota locale, ma ogni modifica destinata alla produzione dovrà essere estesa a `/it/`, `/en/`, `/fr/`, `/de/` e `/es/`, mantenendo parità strutturale e funzionale.
7. **Mobile first.** Il percorso corporate non deve aumentare ulteriormente la lunghezza o introdurre contenuti duplicati su schermi piccoli.
8. **La lingua dell'interfaccia non coincide sempre con la lingua dell'assistenza.** L'interfaccia e i contenuti saranno localizzati nella lingua della pagina; l'assistenza sarà in italiano per il mercato italiano e in inglese per tutti gli altri mercati.

## Matrice degli interventi obbligatori

Questa matrice traduce la decisione in cambiamenti espliciti rispetto alla homepage esistente. “Rimuovere” indica la rimozione dalla forma o dalla posizione attuale, non necessariamente la cancellazione definitiva dell'informazione.

### Da rimuovere o ridurre

| Elemento attuale | Decisione | Motivazione |
|---|---|---|
| “Software originale” usato come principale qualificazione del brand | Ridurre | È un requisito del servizio, non un posizionamento distintivo. |
| H1 “La serenità di scegliere senza rischi” | Sostituire | È generico e costruito soprattutto sulla paura del rischio. |
| CTA hero “Come funziona” | Rimuovere dalla hero | Il processo di acquisto non deve essere il secondo messaggio più importante. |
| Sezione “Come funziona” subito dopo la hero | Spostare più in basso | Prima devono emergere azienda, pubblici, soluzioni e prove. |
| Sei schede “I più venduti” | Ridurre a un massimo di quattro | La densità attuale rende il catalogo dominante. |
| Prezzi barrati e badge sconto ripetuti | Ridurre | Devono restare informazioni commerciali, non diventare il linguaggio principale del brand. |
| Blocco Trustpilot nella forma compatta attuale | Sostituire | Un collegamento o widget di circa una riga non costituisce una prova sociale persuasiva. |
| CTA finale “Software originale. Prezzi onesti.” | Sostituire | Ripete la promessa retail senza aggiungere identità aziendale. |
| “Miglior prezzo garantito” nel footer o nei metadati | Rimuovere | Sposta il posizionamento verso il prezzo e richiede una promessa dimostrabile. |
| “Rispondiamo h24” | Rimuovere se non documentato | Deve essere sostituito da orari o tempi di risposta realistici. |
| Ripetizioni di licenze originali, consegna immediata e pagamenti sicuri | Consolidare | Le stesse rassicurazioni devono comparire una volta in una fascia di fiducia coerente. |

### Da cambiare o spostare

| Elemento attuale | Cambiamento richiesto |
|---|---|
| Hero orientata alla riduzione del rischio | Hero orientata a identità, destinatari, servizio e supporto. |
| Navigazione organizzata quasi solo per prodotto | Navigazione mista per soluzioni, pubblici, prodotti, assistenza e azienda. |
| “Esplora le categorie” | Presentare prima le esigenze e poi produttori e categorie tecniche. |
| Blocco aziende basato su “Le stesse licenze” | Proposta business basata su continuità operativa, scelta e supporto. |
| Schede prodotto basate soprattutto su prezzo e durata | Ogni scheda deve chiarire anche per chi è e quale esigenza risolve. |
| Prova sociale esterna e minimale | Valutazione, volume, testimonianze o casi verificati leggibili in pagina. |
| Chiusura promozionale | Blocco istituzionale con presentazione di AML Store e accesso a contatto e pagina aziendale. |
| Footer prevalentemente commerciale | Footer con percorsi istituzionali, dati societari e assistenza strutturata. |

### Da mantenere

I seguenti elementi non devono essere rimossi dal redesign:

- ricerca;
- carrello;
- accesso immediato al catalogo;
- prezzi e possibilità di acquisto diretto;
- informazioni su consegna e pagamenti;
- FAQ;
- contatti;
- dati fiscali e pagine legali;
- selettore lingua;
- accessibilità del menu e del percorso di checkout.

## Posizionamento e messaggio

La proposta di valore di riferimento è:

> AML Store aiuta privati, professionisti e aziende a scegliere, acquistare e attivare software originale, con fatturazione e assistenza dedicata.

Questa frase definisce la direzione editoriale, ma la formulazione definitiva dovrà essere approvata insieme ai claim legali e commerciali.

### Hero proposta

- **Eyebrow:** `Software originale per aziende, professionisti e privati`
- **H1:** `Il software giusto, per lavorare senza complicazioni`
- **Testo:** `Aiutiamo aziende, professionisti e privati a scegliere, acquistare e attivare licenze software originali, con fatturazione e assistenza dedicata.`
- **CTA primaria:** `Richiedi una consulenza`
- **CTA secondaria:** `Esplora il catalogo`
- **Fascia di fiducia:** `Sede in Italia · Fattura elettronica · Supporto pre e post-vendita · Attivazione sui portali ufficiali`

Il testo non dovrà suggerire uno status di partner ufficiale di un produttore se tale status non è documentato e autorizzato all'uso pubblico.

L'accesso al catalogo dovrà restare chiaramente visibile, ma potrà essere una CTA terziaria o una voce persistente nell'header anziché il messaggio dominante della hero.

### Destinazione della CTA di consulenza

La CTA primaria della hero dovrà aprire una pagina dedicata con un modulo breve. Il modulo raccoglierà:

- nome e cognome;
- azienda, facoltativa;
- email;
- tipo di richiesta;
- numero indicativo di postazioni, facoltativo;
- messaggio;
- consenso privacy obbligatorio.

La richiesta sarà inoltrata a `Info@amlstore.it`. La pagina mostrerà l'email come alternativa e WhatsApp come canale separato per assistenza rapida. Non saranno promessi tempi di risposta finché non verrà approvato un impegno operativo reale.

Il percorso dovrà essere disponibile in tutte le lingue del sito:

- `/it/`: interfaccia, conferma e assistenza in italiano;
- `/en/`: interfaccia, conferma e assistenza in inglese;
- `/fr/`: interfaccia in francese, conferma del modulo in francese e indicazione esplicita che la risposta dell'assistenza sarà in inglese;
- `/de/`: interfaccia in tedesco, conferma del modulo in tedesco e indicazione esplicita che la risposta dell'assistenza sarà in inglese;
- `/es/`: interfaccia in spagnolo, conferma del modulo in spagnolo e indicazione esplicita che la risposta dell'assistenza sarà in inglese.

La nota sulla lingua dell'assistenza dovrà essere visibile prima dell'invio del modulo nelle versioni francese, tedesca e spagnola. Non dovrà essere nascosta soltanto nei termini o nel messaggio di conferma.

Il submit dovrà essere protetto contro spam e abuso prima di qualsiasi deploy in produzione. La soluzione anti-spam dovrà essere approvata e configurata esplicitamente; il solo honeypot non è considerato una protezione sufficiente per un endpoint pubblico che invia email.

### Attività tecniche prima del rilascio

Il modulo è attivo soltanto nel dev server locale e usa il dry-run. Prima di disabilitare `CONSULTATION_DRY_RUN`, rimuovere `noindex` o eseguire qualsiasi deploy dovranno essere completate le attività seguenti:

- Cloudflare Turnstile;
- rate limiting per IP/periodo e test dei relativi limiti;
- decisione su persistenza minima e idempotenza delle richieste, per evitare duplicati e permettere un recupero controllato in caso di errore email;
- verifica in un ambiente non locale dell'invio Resend verso `Info@amlstore.it` e della conferma al richiedente;
- approvazione del mittente definitivo e verifica del relativo dominio in Resend, se diverso da quello attuale;
- tracciamento analytics del submit riuscito, senza includere dati personali;
- gestione dei log senza contenuti sensibili;
- verifica della Privacy Policy e dei tempi di conservazione;
- test anti-abuso e test end-to-end;
- passaggio delle pagine da `noindex` a `index, follow`, aggiornamento sitemap e verifica `hreflang` soltanto dopo l'attivazione del flusso reale.

Sono già presenti localmente il limite del payload, la validazione server-side, l'honeypot, gli stati accessibili e i messaggi localizzati. Questi controlli non sostituiscono Turnstile e rate limiting.

## Architettura informativa

### Navigazione principale

L'header dovrà offrire questi ingressi concettuali:

1. **Soluzioni**
2. **Aziende e professionisti**
3. **Prodotti**
4. **Perché AML Store**
5. **Assistenza**
6. **Azienda**

Ricerca, lingua, contatto, carrello e accesso alle categorie di prodotto resteranno disponibili. Le categorie attuali potranno essere raccolte sotto “Prodotti” tramite menu esteso, evitando di occupare l'intera navigazione primaria.

Su mobile, le voci dovranno essere raggruppate in sezioni riconoscibili e non presentate come un elenco piatto di singoli SKU.

### Ordine target della homepage

1. **Header corporate commerce**
2. **Hero con identità, pubblico e proposta di valore**
3. **Fascia con prove di affidabilità verificabili**
4. **Percorsi per Privati, Professionisti e Aziende**
5. **Soluzioni principali organizzate per esigenza**
6. **Perché AML Store**
7. **Area aziende con consulenza o richiesta preventivo**
8. **Prodotti selezionati**
9. **Recensioni e, quando disponibili, casi reali**
10. **Come funziona**
11. **FAQ**
12. **Blocco istituzionale “Chi è AML Store”**
13. **Footer aziendale completo**

## Specifiche dei blocchi

### Percorsi per pubblico

La homepage dovrà permettere la scelta esplicita tra:

- **Privati:** acquisto semplice, consegna digitale e supporto all'attivazione;
- **Professionisti:** continuità operativa, fattura e scelta dell'edizione corretta;
- **Aziende:** più postazioni, Microsoft 365 Business, server, database e richiesta di consulenza.

Ogni percorso avrà una CTA dedicata e una destinazione coerente. Non dovranno essere presentati servizi che AML Store non è ancora in grado di erogare.

### Soluzioni

Le categorie dovranno essere riformulate come risposte a esigenze, per esempio:

- produttività e collaborazione;
- sistemi operativi e postazioni di lavoro;
- sicurezza e protezione dei dispositivi;
- infrastruttura server e database;
- strumenti professionali specialistici.

I nomi dei produttori potranno apparire come dettaglio, non come unico criterio di orientamento.

### Perché AML Store

Il blocco dovrà combinare vantaggio e prova. Ogni affermazione dovrà essere supportata da un'informazione concreta, ad esempio:

- sede e soggetto giuridico;
- disponibilità della fattura;
- canali e orari di assistenza;
- modalità di consegna;
- portali usati per l'attivazione;
- condizioni di reso e rimborso;
- metodi di pagamento e relativi provider.

Formule vaghe come “partner affidabile” non dovranno comparire senza una spiegazione immediata di cosa renda affidabile il servizio.

### Area aziende e professionisti

Il blocco attuale sarà ampliato e spostato prima del catalogo. Dovrà includere:

- problemi o scenari serviti;
- prodotti e servizi effettivamente disponibili;
- modalità di contatto;
- aspettativa realistica sui tempi di risposta;
- CTA primaria verso consulenza o preventivo;
- CTA secondaria verso server, database o soluzioni business.

Il messaggio non dovrà iniziare da “le stesse licenze”, perché questa formulazione riduce la proposta a una commodity.

Copy di riferimento da validare:

- **Titolo:** `Soluzioni software per la continuità della tua attività`
- **Testo:** `Dalla singola postazione agli ambienti server, aiutiamo professionisti e aziende a individuare edizioni, durata e modalità di licenza adatte alle loro esigenze.`
- **CTA primaria:** `Richiedi una consulenza`
- **CTA secondaria:** `Esplora le soluzioni aziendali`

### Prodotti selezionati

La homepage mostrerà al massimo quattro prodotti o offerte prioritarie per breakpoint desktop. Su mobile dovrà essere evitata una griglia a due colonne con schede troppo strette; usare una colonna, uno scorrimento orizzontale accessibile o un elenco compatto.

La selezione dovrebbe rappresentare, quando il catalogo lo consente:

- un prodotto adatto ai privati;
- un prodotto adatto ai professionisti;
- un prodotto o soluzione per aziende;
- eventualmente un bundle con una proposta chiaramente distinta.

Ogni scheda dovrà includere una breve indicazione “per chi è” o un beneficio equivalente, evitando di affidare l'intera differenziazione a prezzo, durata e percentuale di sconto.

Prezzo e acquisto resteranno visibili. Prezzo barrato, percentuale di sconto e urgenza promozionale saranno usati solo quando commercialmente e legalmente corretti, senza diventare il tratto visivo dominante della pagina.

Il catalogo completo resterà raggiungibile con una CTA esplicita.

### Prova sociale

Il widget Trustpilot nella forma compatta attuale dovrà essere rimosso o sostituito. Il nuovo blocco dovrà mostrare informazioni utili senza obbligare l'utente a lasciare il sito. Sono ammessi:

- valutazione e numero di recensioni aggiornati automaticamente;
- estratti brevi da recensioni pubbliche nel rispetto delle condizioni della piattaforma;
- testimonianze autorizzate;
- casi cliente approvati;
- loghi cliente solo con consenso all'uso.

Deve essere previsto un fallback leggibile se lo script di terze parti viene bloccato, non carica o non riceve consenso.

### Blocco istituzionale e footer

Il blocco finale “Software originale. Prezzi onesti.” sarà sostituito da una chiusura istituzionale. Copy di riferimento da validare:

- **Titolo:** `Un partner italiano per le tue esigenze software`
- **CTA primaria:** `Conosci AML Store`
- **CTA secondaria:** `Contatta il team`

Il testo dovrà spiegare brevemente chi è AML Store, quali pubblici serve e come combina acquisto self-service e assistenza.

La homepage e il footer dovranno offrire accesso a:

- chi siamo;
- dati societari completi approvati per la pubblicazione;
- sede e contatti;
- canali e orari di assistenza;
- termini, privacy, cookie, resi e rimborsi;
- eventuali profili social o directory aziendali ufficiali.

La formula “Rispondiamo h24” dovrà essere mantenuta solo se rappresenta un impegno reale, misurabile e sostenibile. In alternativa sarà sostituita da orari o tempi medi di risposta verificati.

La formula “miglior prezzo garantito” dovrà essere rimossa dal footer e dagli altri messaggi istituzionali, salvo l'esistenza di una politica pubblica, applicabile e dimostrabile che ne definisca con precisione le condizioni.

## Direzione visiva

- Mantenere la base navy, bianco e blu, perché già coerente con affidabilità e tecnologia.
- Ridurre il peso visivo dei pattern tipici da marketplace: griglie dense, badge sconto ripetuti e CTA identiche.
- Aumentare spaziatura, gerarchia tipografica e varietà controllata delle composizioni.
- Preferire immagini proprietarie di team, assistenza, processi o ambienti reali.
- Se non sono disponibili fotografie autentiche, usare un sistema grafico di brand; non sostituire una fotografia stock generica con un'altra fotografia stock generica.
- Mantenere un'unica CTA primaria per sezione.
- Garantire che elementi decorativi e immagini non rallentino il Largest Contentful Paint.

## SEO e dati strutturati

La homepage dovrà spostare il focus da “miglior prezzo” a identità, servizio e pubblici serviti.

Esempio da validare:

- **Title:** `Software originale per privati e aziende | AML Store`
- **Description:** `Licenze software originali per privati, professionisti e aziende, con consegna digitale, fattura e assistenza dedicata.`

Lo schema `Organization` dovrà essere completato, quando i dati sono disponibili e pubblicabili, con proprietà quali:

- `legalName`;
- `address`;
- `vatID`;
- `contactPoint`;
- `sameAs`;
- eventuale `foundingDate`.

Non dovranno essere aggiunte proprietà non verificabili. Canonical, alternate language e URL con o senza `www` dovranno restare coerenti con la strategia di redirect.

## Accessibilità e responsive design

L'implementazione dovrà:

- mantenere un solo `h1` descrittivo;
- rispettare l'ordine logico dei titoli;
- garantire navigazione completa da tastiera;
- usare focus visibili e contrasto almeno WCAG AA;
- associare nomi accessibili a menu, ricerca, lingua, contatti e carrello;
- evitare carousel che avanzano automaticamente;
- offrire un fallback testuale per widget e contenuti di terze parti;
- evitare overflow orizzontale a 320 px;
- mantenere le CTA principali visibili e leggibili senza testo eccessivamente ridotto;
- ridurre la lunghezza mobile eliminando ripetizioni, non nascondendo informazioni essenziali.

## Analytics e misurazione

Prima del rilascio dovrà essere fotografata la baseline corrente. Il redesign dovrà misurare almeno:

- click sulle CTA hero;
- ingresso nei percorsi Privati, Professionisti e Aziende;
- click su richiesta consulenza o preventivo;
- apertura dei contatti;
- click verso categorie e catalogo;
- add-to-cart e completamento checkout;
- profondità di scroll;
- tasso di uscita dalla homepage;
- Core Web Vitals separati per desktop e mobile.

Le soglie numeriche saranno definite solo dopo aver verificato volumi e qualità della baseline. L'obiettivo è aumentare lead e riconoscibilità senza ridurre in modo significativo la conversione e-commerce.

La Content Security Policy dovrà essere allineata agli strumenti di misurazione effettivamente autorizzati. Le richieste verso domini pubblicitari non necessari dovranno essere rimosse; quelle necessarie dovranno essere consentite soltanto con consenso e configurazione CSP coerenti.

## Criteri di accettazione

### Contenuto e brand

- [ ] La hero identifica AML Store, i pubblici serviti e il servizio offerto.
- [ ] Il messaggio principale non è basato su prezzo o paura del rischio.
- [ ] Ogni claim corporate è documentato e approvato.
- [ ] È disponibile almeno un percorso esplicito per aziende e professionisti.
- [ ] È disponibile un accesso chiaro alle informazioni aziendali.
- [ ] “Come funziona” non compare prima dei percorsi, delle soluzioni e dell'area aziendale.
- [ ] Le rassicurazioni transazionali duplicate sono consolidate in una sola fascia coerente.
- [ ] “Miglior prezzo garantito” e “Rispondiamo h24” non compaiono senza condizioni verificabili.

### Navigazione e conversione

- [ ] Catalogo, ricerca e carrello restano raggiungibili dalla prima schermata.
- [ ] La navigazione espone sia soluzioni sia prodotti.
- [ ] La homepage mostra non più di quattro prodotti prioritari per vista desktop.
- [ ] Ogni prodotto selezionato chiarisce per chi è o quale esigenza risolve.
- [ ] La CTA di consulenza genera un contatto tracciabile e utilizzabile.
- [ ] Non vengono introdotti vicoli ciechi o link privi di destinazione reale.
- [ ] Il blocco recensioni offre contenuto utile anche senza lasciare il sito.
- [ ] La chiusura della homepage presenta AML Store invece di ripetere una promessa promozionale.

### Responsive e accessibilità

- [ ] Nessun overflow orizzontale tra 320 px e 1440 px.
- [ ] Le schede prodotto mobile restano leggibili senza zoom.
- [ ] Navigazione, FAQ, widget e CTA sono utilizzabili da tastiera.
- [ ] Focus, contrasto e gerarchia dei titoli superano la verifica manuale.
- [ ] La pagina resta comprensibile senza widget di terze parti.

### Tecnica e SEO

- [ ] Nessun nuovo errore console bloccante.
- [ ] Gli errori CSP relativi agli strumenti analytics sono risolti o la relativa integrazione è rimossa.
- [ ] Title, description, canonical e alternate language sono corretti per tutte le lingue.
- [ ] I dati strutturati contengono solo informazioni verificate.
- [ ] Le metriche Core Web Vitals non peggiorano in modo significativo rispetto alla baseline.
- [ ] Le cinque versioni linguistiche mantengono parità di struttura, funzionalità, validazione e tracciamento.
- [ ] Le pagine francese, tedesca e spagnola dichiarano prima del contatto che l'assistenza risponderà in inglese.

## Piano di implementazione

### Fase 0 — Validazione dei contenuti

1. **Completato:** denominazione legale, indirizzo e dati societari pubblicabili.
2. **Completato:** canali e orari di assistenza sostenibili; nessuno SLA di risposta approvato.
3. **Completato per lo stato attuale:** non risultano partnership, certificazioni, testimonianze o casi cliente approvati.
4. **Completato:** servizi realmente offerti ad aziende e professionisti.
5. Registrare baseline analytics, performance e conversione.

### Fase 1 — Pilota italiano

1. Aggiornare `components/header.js` e `components/footer.js`.
2. Ristrutturare `it/index.html` secondo l'ordine target.
3. Aggiornare `css/home.css` e gli eventuali asset della hero.
4. Implementare eventi analytics e fallback dei widget.
5. Verificare desktop, mobile, tastiera, SEO e checkout.

### Fase 2 — Contenuti istituzionali

1. Creare o completare le destinazioni “Azienda”, “Perché AML Store” e “Aziende e professionisti”.
2. Integrare prove sociali e contenuti verificati.
3. Completare dati strutturati e informazioni societarie.

### Fase 3 — Localizzazione

1. Adattare copy e destinazioni in `en/index.html`, `fr/index.html`, `de/index.html` ed `es/index.html`.
2. Evitare traduzioni letterali di claim e CTA quando riducono chiarezza o credibilità.
3. Estendere alle altre lingue ogni nuova pagina, campo, stato, validazione, messaggio di errore, conferma ed evento analytics introdotto nel pilota italiano.
4. Nelle versioni francese, tedesca e spagnola, comunicare prima del submit che la risposta dell'assistenza sarà fornita in inglese.
5. Verificare `hreflang`, canonical, link interni e parità funzionale.
6. Eseguire una nuova verifica visuale e tecnica per ogni lingua.

La localizzazione non è considerata un miglioramento facoltativo successivo: è una condizione necessaria prima di commit e push destinati alla produzione. La versione italiana può precedere le altre soltanto durante il lavoro e la verifica locale.

### Fase 4 — Rilascio e osservazione

1. Rilasciare con possibilità di confronto rispetto alla baseline.
2. Monitorare lead, conversione e comportamento per un periodo statisticamente utile.
3. Correggere attriti senza ripristinare automaticamente la densità promozionale precedente.

## Impatto previsto sui file

L'elenco è indicativo e dovrà essere confermato durante l'implementazione:

- `it/index.html`
- `en/index.html`
- `fr/index.html`
- `de/index.html`
- `es/index.html`
- `it/consulenza.html`
- `en/consultation.html`
- `fr/consultation.html`
- `de/beratung.html`
- `es/consultoria.html`
- `css/consultation.css`
- `js/consultation-form.js`
- `js/locale-path.js`
- `functions/api/[[catchall]].js`
- `functions/api/_lib/email.js`
- `functions/api/_lib/consultation-email-templates.js`
- `.dev.vars.example`
- `components/header.js`
- `components/footer.js`
- `css/home.css`
- eventuali nuovi asset sotto `asset/`
- `sitemap.xml` e pagine di destinazione, se vengono aggiunte nuove URL
- `_headers`, se viene corretta la Content Security Policy

## Conseguenze

### Positive

- Maggiore riconoscibilità del brand.
- Migliore leggibilità dell'offerta per professionisti e aziende.
- Possibilità di generare lead oltre agli ordini self-service.
- Minore dipendenza competitiva da prezzo e sconto.
- Fiducia costruita su informazioni e prove, non soltanto su rassicurazioni.

### Negative e costi

- Maggiore lavoro editoriale e necessità di mantenere contenuti istituzionali aggiornati.
- Complessità aggiuntiva nella navigazione e nella localizzazione.
- Necessità di produrre o approvare asset, testimonianze e dati aziendali.
- Rischio di ridurre click immediati sui prodotti se la componente corporate diventa troppo invasiva.
- Necessità di misurare due conversioni diverse: vendita self-service e lead assistito.

### Mitigazioni

- Mantenere ricerca, prodotti e carrello sempre accessibili.
- Validare prima il pilota italiano.
- Usare contenuti modulari e riutilizzabili.
- Confrontare conversione e-commerce e lead con una baseline reale.
- Non pubblicare sezioni prive di prove o destinazioni complete.

## Alternative considerate

### Mantenere la homepage attuale

Scartata come direzione strategica perché conserva una buona usabilità commerciale, ma non risolve la debole differenziazione né il posizionamento B2B.

### Applicare soltanto un restyling visivo

Scartata perché colori, fotografia e tipografia non possono compensare una gerarchia editoriale ancora centrata su categorie, prezzi e sconti.

### Trasformare il sito in una vetrina corporate

Scartata perché indebolirebbe un percorso e-commerce già funzionante e aumenterebbe l'attrito per chi vuole acquistare in autonomia.

### Creare un sito B2B separato

Non adottata in questa fase. Frammenterebbe brand, SEO, contenuti e manutenzione prima di aver validato la domanda business sulla homepage esistente.

## Non obiettivi

Questo ADR non decide:

- un rebranding completo di nome o logo;
- la riprogettazione del checkout;
- nuovi accordi commerciali con produttori;
- l'introduzione di servizi non ancora erogati;
- target numerici di conversione prima della raccolta della baseline;
- la revisione completa di tutte le schede prodotto.

## Questioni aperte prima dell'accettazione

1. Quali eventi analytics sono già disponibili e qual è la baseline?
2. Google Ads richiede realmente le chiamate attualmente bloccate dalla CSP?
3. Quali nuove pagine istituzionali devono essere create prima della nuova homepage?
4. Il mittente Resend deve restare quello già verificato oppure va creato un indirizzo dedicato alle consulenze?
5. Le richieste devono essere persistite in D1 oltre all'invio email, e per quale periodo di conservazione?

## Condizione per il passaggio ad Accepted

L'ADR potrà passare da **Proposed** ad **Accepted** quando saranno approvati:

- posizionamento e copy principale;
- dati societari e claim pubblicabili;
- servizi destinati ad aziende e professionisti;
- architettura di navigazione;
- destinazioni delle CTA;
- piano di misurazione e baseline;
- responsabilità editoriale per le cinque lingue.
