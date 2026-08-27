#!/usr/bin/env python3
"""Port it/microsoft-365-family.html (pdp pilot) to en/fr/de/es."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "it" / "microsoft-365-family.html"

# (italian, translation) — applied longest-first
# Structural path/lang handled separately per locale.

EN = [
    # Meta / JSON-LD descriptions
    (
        "Microsoft 365 Family per 12 mesi, fino a 6 persone del gruppo famiglia: app Microsoft 365 e 1 TB OneDrive a persona. Copilot è riservato al titolare. Codice digitale via email in 5–15 minuti dal pagamento.",
        "Microsoft 365 Family for 12 months, for up to 6 people in a Microsoft family group: Microsoft 365 apps and 1 TB OneDrive each. Copilot is for the subscription owner only. Digital code by email within 5–15 minutes of payment.",
    ),
    ("Microsoft 365 Family — 12 mesi", "Microsoft 365 Family — 12 months"),
    (
        "L'email di consegna parte dopo la conferma del pagamento, di norma entro 5–15 minuti; in rari casi servono alcuni minuti in più per le verifiche del pagamento. Se dopo 30 minuti non hai ricevuto nulla, controlla anche spam e posta indesiderata e scrivi a Desk@eurolicenze.com indicando prodotto acquistato ed email usata per l'ordine.",
        "The delivery email is sent after payment confirmation, usually within 5–15 minutes; in rare cases a few extra minutes are needed for payment checks. If after 30 minutes you have received nothing, check spam/junk and email Desk@eurolicenze.com with the product purchased and the email used for the order.",
    ),
    (
        "Ricevi la product key di Microsoft 365 Family e le istruzioni per riscattarla sui portali ufficiali Microsoft. La consegna è solo digitale: non viene spedito alcun supporto fisico e non ci sono costi di spedizione.",
        "You receive the Microsoft 365 Family product key and instructions to redeem it on official Microsoft portals. Delivery is digital only: nothing physical is shipped and there are no shipping fees.",
    ),
    (
        "Al checkout sono disponibili carta, PayPal e wallet digitali come Apple Pay e Google Pay dove abilitati. L'elaborazione del pagamento è gestita in modo sicuro tramite Stripe.",
        "At checkout you can pay by card, PayPal and digital wallets such as Apple Pay and Google Pay where enabled. Payment processing is handled securely via Stripe.",
    ),
    (
        "Sì. Al checkout scegli il profilo Azienda e inserisci partita IVA e Codice SDI oppure PEC: la fattura elettronica viene emessa su quei dati. Se ti serve dopo l'ordine, scrivi a Desk@eurolicenze.com indicando l'email usata per l'ordine e il numero d'ordine.",
        "Yes. At checkout choose the Business profile and enter your VAT details: we issue a VAT invoice on those details. If you need it after the order, email Desk@eurolicenze.com with the order email and order number.",
    ),
    (
        "Vai su setup.office.com/Home, accedi con il tuo account Microsoft, inserisci il codice ricevuto via email e segui la procedura guidata. Al termine installa le app da office.com.",
        "Go to setup.office.com/Home, sign in with your Microsoft account, enter the code received by email and follow the guided setup. Then install the apps from office.com.",
    ),
    (
        "Sì: il riscatto avviene su setup.office.com con il tuo account Microsoft. Se su quell'account è già attivo un abbonamento Microsoft 365, il comportamento (estensione o conversione del piano) segue le regole Microsoft mostrate durante il riscatto. Scegli l'account con attenzione: la licenza resta associata a quello usato al momento del riscatto.",
        "Yes: redemption happens on setup.office.com with your Microsoft account. If that account already has an active Microsoft 365 subscription, the outcome (extension or plan conversion) follows Microsoft's rules shown during redemption. Choose the account carefully: the licence stays tied to the account used at redemption.",
    ),
    (
        "Dopo l'attivazione sul tuo account Microsoft, usa le funzioni di condivisione del piano Family nell'area account Microsoft / abbonamenti, come indicato da Microsoft per il periodo di validità della licenza.",
        "After activation on your Microsoft account, use the Family plan sharing features in the Microsoft account / subscriptions area, as directed by Microsoft for the licence term.",
    ),
    (
        "No. Le funzionalità Copilot comprese nel piano sono utilizzabili dal titolare dell'abbonamento. Gli altri cinque membri ricevono le app Microsoft 365, 1 TB di OneDrive ciascuno e Microsoft Defender, ma non le funzionalità AI.",
        "No. Copilot features included in the plan are available to the subscription owner. The other five members get Microsoft 365 apps, 1 TB of OneDrive each and Microsoft Defender, but not the AI features.",
    ),
    (
        "No. Ogni persona usa il proprio account Microsoft, con documenti, email, impostazioni e spazio OneDrive separati. La condivisione di singoli file o cartelle resta una scelta volontaria di chi li possiede.",
        "No. Each person uses their own Microsoft account, with separate documents, email, settings and OneDrive space. Sharing individual files or folders remains a voluntary choice by the owner.",
    ),
    (
        "Sì: con le app desktop installate puoi lavorare offline; servono comunque connessione e accesso periodici per la verifica della licenza, aggiornamenti e servizi cloud come OneDrive, come descritto da Microsoft.",
        "Yes: with the desktop apps installed you can work offline; periodic connection and sign-in are still required for licence checks, updates and cloud services such as OneDrive, as described by Microsoft.",
    ),
    (
        "Family è pensato per condividere il piano con il tuo gruppo famiglia Microsoft (fino a 6 persone), ciascuna con account e spazio OneDrive distinti. Personal copre un solo utente con 1 TB, secondo le condizioni Microsoft aggiornate.",
        "Family is designed to share the plan with your Microsoft family group (up to 6 people), each with a separate account and OneDrive space. Personal covers a single user with 1 TB, subject to Microsoft's current terms.",
    ),
    (
        "No. Il codice attiva Microsoft 365 Family per 12 mesi con un pagamento una tantum: Eurolicenze non addebita nulla automaticamente alla scadenza. Eventuali opzioni di rinnovo si gestiscono separatamente, direttamente nell'account Microsoft.",
        "No. The code activates Microsoft 365 Family for 12 months with a one-time payment: Eurolicenze does not charge anything automatically at expiry. Any renewal options are managed separately in your Microsoft account.",
    ),
    (
        "Sì, puoi riscattarlo sullo stesso account che ha già Microsoft 365 Family attivo. Il modo in cui viene applicato (estensione della durata attuale o avvio di un nuovo periodo) segue le regole Microsoft mostrate al momento del riscatto su setup.office.com, non è qualcosa che decidiamo noi come rivenditore.",
        "Yes, you can redeem it on the same account that already has Microsoft 365 Family active. How it is applied (extending the current term or starting a new period) follows Microsoft's rules shown at redemption on setup.office.com — it is not something we decide as a reseller.",
    ),
    (
        "Scrivici indicando numero d'ordine ed eventuale messaggio di errore. Verifichiamo il caso e, se viene confermato un difetto imputabile a noi o al fornitore della chiave, proponiamo sostituzione o rimborso nei tempi usuali di elaborazione. Assistenza: Desk@eurolicenze.com — +39 392 558 0413.",
        "Contact us with your order number and any error message. We review the case and, if a defect attributable to us or the key supplier is confirmed, we offer a replacement or refund within usual processing times. Support: Desk@eurolicenze.com — +39 392 558 0413.",
    ),
    # UI chrome
    ("Vai al contenuto principale", "Skip to main content"),
    ("Acquisto rapido", "Quick purchase"),
    ("Microsoft 365 Family · 12 mesi", "Microsoft 365 Family · 12 months"),
    ("Acquista ora", "Buy now"),
    ("Prodotto e acquisto", "Product and purchase"),
    ("Percorso navigazione", "Breadcrumb"),
    ("Abbonamento digitale · 12 mesi", "Digital subscription · 12 months"),
    ("Codice articolo:", "Product code:"),
    ("Microsoft 365 Family — grafica del prodotto", "Microsoft 365 Family — product artwork"),
    (
        "Microsoft 365 per te e altre cinque persone, con app complete e 1 TB di OneDrive personale per ciascun membro. Copilot è incluso per il titolare dell'abbonamento.",
        "Microsoft 365 for you and five other people, with full apps and 1 TB of personal OneDrive for each member. Copilot is included for the subscription owner.",
    ),
    ("Fino a 6 persone, ognuna con il proprio account Microsoft", "Up to 6 people, each with their own Microsoft account"),
    ("1 TB di OneDrive a persona, file e impostazioni separati", "1 TB of OneDrive per person, separate files and settings"),
    ("App desktop sempre aggiornate su PC, Mac, tablet e telefono", "Desktop apps always up to date on PC, Mac, tablet and phone"),
    ("Copilot per il titolare <em>— non condiviso con gli altri membri</em>", "Copilot for the owner <em>— not shared with other members</em>"),
    ("Prezzo Eurolicenze", "Eurolicenze price"),
    ("Prezzi", "Prices"),
    ("Prezzo scontato 104,95 euro", "Sale price 104.95 euros"),
    ("Prezzo originale 129 euro", "Original price 129 euros"),
    ("Sconto 19 percento", "19 percent off"),
    (
        "IVA inclusa, nessun costo di spedizione. Risparmi <strong>€ 24,05</strong> rispetto al Microsoft Store (€ 129,00).",
        "Tax included. No shipping fees. You save <strong>€ 24,05</strong> versus the Microsoft Store (€ 129,00).",
    ),
    ("Aggiungi al carrello", "Add to cart"),
    ("Codice via email in 5–15 minuti dalla conferma del pagamento", "Code by email within 5–15 minutes of payment confirmation"),
    (
        "<strong>Incluso con l'acquisto:</strong> guida PDF all'utilizzo di Copilot, via email dopo l'ordine",
        "<strong>Included with your purchase:</strong> Copilot PDF guide, sent by email after the order",
    ),
    ("Attivazione sui portali ufficiali Microsoft", "Activation on official Microsoft portals"),
    ("Assistenza in italiano dopo l'acquisto", "Support after you buy"),
    ("Fattura elettronica disponibile", "VAT invoice available"),
    ("Metodi di pagamento accettati", "Accepted payment methods"),
    (
        "Pagamenti protetti tramite <strong>Stripe</strong> e <strong>PayPal</strong>",
        "Secure payments via <strong>Stripe</strong> and <strong>PayPal</strong>",
    ),
    ("Azienda italiana", "European retailer"),
    ("Sede e P.IVA in Italia", "Registered in Italy"),
    ("Fattura elettronica", "Invoice available"),
    ("Disponibile per privati e aziende", "VAT invoice for businesses"),
    ("Assistenza in italiano", "Written support"),
    ("Supporto post-vendita via email", "Email and WhatsApp"),
    ("Pagamenti protetti", "Secure payments"),
    ("Elaborati tramite Stripe e PayPal", "Processed via Stripe and PayPal"),
    ('data-cart-added-msg="Prodotto aggiunto al carrello."', 'data-cart-added-msg="Product added to cart."'),
    ("Cosa ricevi", "What you get"),
    ("Sei persone, account e spazi separati", "Six people, separate accounts and storage"),
    (
        "Microsoft 365 Family è pensato per essere condiviso: ogni persona lavora sul proprio account, con il proprio spazio cloud.",
        "Microsoft 365 Family is built to be shared: each person works on their own account, with their own cloud storage.",
    ),
    ("Persone incluse", "People included"),
    ("Titolare più 5 membri invitati, ognuno con account Microsoft separato.", "Owner plus 5 invited members, each with a separate Microsoft account."),
    ("OneDrive a persona", "OneDrive per person"),
    ("Fino a 6 TB complessivi sul piano, non condivisi automaticamente.", "Up to 6 TB total on the plan, not shared automatically."),
    ("Durata", "Term"),
    ("Pagamento una tantum su Eurolicenze, senza addebiti ricorrenti da parte nostra.", "One-time payment on Eurolicenze, with no recurring charges from us."),
    ("Dispositivi per persona", "Devices per person"),
    ("Accesso contemporaneo su PC, Mac, tablet e telefono, secondo le regole Microsoft.", "Simultaneous access on PC, Mac, tablet and phone, subject to Microsoft rules."),
    ("Specifiche del prodotto", "Product specifications"),
    ("Scheda tecnica", "Tech sheet"),
    ("Specifiche tecniche e commerciali di Microsoft 365 Family", "Technical and commercial specifications for Microsoft 365 Family"),
    ("Prodotto", "Product"),
    ("Utenti", "Users"),
    ("Fino a 6 persone", "Up to 6 people"),
    ("Fino a 6", "Up to 6"),
    ("Archiviazione", "Storage"),
    ("1 TB OneDrive per persona", "1 TB OneDrive per person"),
    ("Dispositivi", "Devices"),
    ("Fino a 5 contemporanei per persona", "Up to 5 simultaneous per person"),
    ("Incluso per il titolare dell'abbonamento", "Included for the subscription owner"),
    ("Consegna", "Delivery"),
    ("Codice digitale via email", "Digital code by email"),
    ("Attivazione", "Activation"),
    ("Account Microsoft, su setup.office.com", "Microsoft account, on setup.office.com"),
    ("Rinnovo", "Renewal"),
    ("Nuova attivazione o estensione secondo le regole Microsoft", "New activation or extension per Microsoft rules"),
    ("Codice prodotto", "Product code"),
    ("Fatturazione", "Billing"),
    ("IVA inclusa, fattura elettronica disponibile", "Tax included, VAT invoice available"),
    ("Chi riceve cosa", "Who gets what"),
    ("Un abbonamento condiviso, sei esperienze separate", "One shared subscription, six separate experiences"),
    (
        "Ogni persona utilizza il proprio account Microsoft. Documenti, email, fotografie e spazio cloud non vengono condivisi automaticamente con gli altri membri. L'unica differenza reale riguarda le funzionalità Copilot.",
        "Each person uses their own Microsoft account. Documents, email, photos and cloud storage are not shared automatically with other members. The only real difference is Copilot features.",
    ),
    ("Confronto tra titolare dell'abbonamento e altri membri del gruppo famiglia", "Comparison between subscription owner and other family group members"),
    ("Funzionalità", "Feature"),
    ("Titolare", "Owner"),
    ("Altri 5 membri", "Other 5 members"),
    ("Incluso", "Included"),
    ("Non incluso", "Not included"),
    ("Word, Excel, PowerPoint e Outlook", "Word, Excel, PowerPoint and Outlook"),
    ("1 TB di OneDrive personale", "1 TB of personal OneDrive"),
    ("Account, file e impostazioni separati", "Separate accounts, files and settings"),
    ("Installazione su più dispositivi", "Install on multiple devices"),
    ("Funzionalità Copilot", "Copilot features"),
    ("Le funzioni AI comprese nel piano restano al proprietario dell'abbonamento.", "AI features included in the plan stay with the subscription owner."),
    ("App incluse", "Apps included"),
    ("Tutte le app che usi, su tutti i tuoi dispositivi", "All the apps you use, on all your devices"),
    (
        "Installa le applicazioni desktop supportate e continua a lavorare anche offline. I documenti possono essere sincronizzati tramite OneDrive.",
        "Install the supported desktop apps and keep working offline. Documents can sync via OneDrive.",
    ),
    ("Solo titolare", "Owner only"),
    ("Vedi tutte le app incluse", "See all included apps"),
    ("Famiglia che usa laptop e dispositivi insieme in un ambiente domestico luminoso e moderno.", "Family using laptops and devices together in a bright, modern home."),
    ("Condivisione", "Sharing"),
    ("Un piano, account separati", "One plan, separate accounts"),
    (
        "Inviti fino a cinque persone dal tuo account Microsoft. Ognuna riceve il proprio spazio cloud, le proprie app e le proprie impostazioni: nessuno vede i documenti degli altri.",
        "Invite up to five people from your Microsoft account. Each gets their own cloud storage, apps and settings: nobody sees anyone else's documents.",
    ),
    ("Le sei postazioni del piano", "The six seats on the plan"),
    ("Membro 2", "Member 2"),
    ("Membro 3", "Member 3"),
    ("Membro 4", "Member 4"),
    ("Membro 5", "Member 5"),
    ("Membro 6", "Member 6"),
    ("Tutti ricevono le stesse app. Cambia solo Copilot, che resta al titolare.", "Everyone gets the same apps. Only Copilot differs — it stays with the owner."),
    ("Quale scegliere", "Which to choose"),
    ("Confronta i piani Microsoft 365", "Compare Microsoft 365 plans"),
    (
        "La differenza non è la potenza delle app: è quante persone useranno davvero il piano.",
        "The difference is not app power: it is how many people will actually use the plan.",
    ),
    ("Confronto tra Microsoft 365 Personal e Microsoft 365 Family", "Comparison between Microsoft 365 Personal and Microsoft 365 Family"),
    ("Persone", "People"),
    ("Spazio OneDrive", "OneDrive storage"),
    ("1 TB a persona", "1 TB per person"),
    ("Account separati per ogni utente", "Separate account per user"),
    ("Non previsto", "Not applicable"),
    ("Prezzo su Eurolicenze", "Eurolicenze price"),
    ("Ideale per", "Best for"),
    ("Chi usa Office da solo", "Someone using Office alone"),
    ("Due o più persone", "Two or more people"),
    (
        'Scegli Family se almeno due persone useranno realmente le app o lo spazio OneDrive. Altrimenti valuta <a href="/en/microsoft-365-personal">Microsoft 365 Personal</a>.',
        'Choose Family if at least two people will really use the apps or OneDrive storage. Otherwise consider <a href="/en/microsoft-365-personal">Microsoft 365 Personal</a>.',
    ),
    ("Come funziona", "How it works"),
    ("Tre passi per iniziare", "Three steps to get started"),
    ("Completa l'ordine", "Complete your order"),
    ("Paga con uno dei metodi disponibili al checkout: carta, PayPal o wallet digitali.", "Pay with one of the methods available at checkout: card, PayPal or digital wallets."),
    ("Ricevi il codice", "Receive your code"),
    ("Product key e istruzioni arrivano via email in 5–15 minuti dalla conferma del pagamento.", "Product key and instructions arrive by email within 5–15 minutes of payment confirmation."),
    ("Attiva su Microsoft", "Activate on Microsoft"),
    (
        'Accedi con il tuo account e riscatta il codice su <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com</a>, poi installa le app da <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.',
        'Sign in with your account and redeem the code on <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com</a>, then install the apps from <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.',
    ),
    (
        "<strong>Controlla di usare l'account Microsoft corretto:</strong> la licenza viene associata all'account scelto durante il riscatto e non può essere spostata successivamente.",
        "<strong>Make sure you use the correct Microsoft account:</strong> the licence is tied to the account chosen at redemption and cannot be moved later.",
    ),
    ("Cosa dicono i clienti", "What customers say"),
    (
        "Le recensioni sono pubblicate e verificate da Trustpilot: le leggi direttamente sulla piattaforma, senza filtri da parte nostra.",
        "Reviews are published and verified by Trustpilot: you read them on the platform, with no filtering by us.",
    ),
    (
        'Esperienze reali dei clienti su Trustpilot. <a href="https://www.trustpilot.com/review/aml-store.com" target="_blank" rel="noopener noreferrer">Trustpilot</a>',
        'Real customer experiences on Trustpilot. <a href="https://www.trustpilot.com/review/aml-store.com" target="_blank" rel="noopener noreferrer">Trustpilot</a>',
    ),
    ("Leggi tutte le recensioni", "Read all reviews"),
    ("Acquista con maggiore tranquillità", "Buy with more peace of mind"),
    ("Rivenditore europeo", "European retailer"),
    ("Eurolicenze ha sede legale in Italia", "Eurolicenze is legally registered in Italy"),
    ("Fattura disponibile", "Invoice available"),
    ("Documentazione per privati e aziende", "Documentation for individuals and businesses"),
    ("Supporto scritto", "Written support"),
    ("Assistenza via email e WhatsApp", "Support via email and WhatsApp"),
    ("Transazioni tramite Stripe e PayPal", "Transactions via Stripe and PayPal"),
    ("Domande frequenti", "Frequently asked questions"),
    ("Le risposte prima dell'acquisto", "Answers before you buy"),
    ("Acquisto e consegna", "Purchase and delivery"),
    ("Quando ricevo il codice dopo il pagamento?", "When do I receive the code after payment?"),
    (
        "L'email di consegna parte dopo la conferma del pagamento, di norma entro 5–15 minuti; in rari casi servono alcuni minuti in più per le verifiche del pagamento.",
        "The delivery email is sent after payment confirmation, usually within 5–15 minutes; in rare cases a few extra minutes are needed for payment checks.",
    ),
    (
        'Se dopo <strong>30 minuti</strong> non hai ricevuto nulla, controlla anche spam e posta indesiderata e scrivi a <a href="mailto:Desk@eurolicenze.com">Desk@eurolicenze.com</a> indicando prodotto acquistato ed email usata per l\'ordine.',
        'If after <strong>30 minutes</strong> you have received nothing, also check spam/junk and email <a href="mailto:Desk@eurolicenze.com">Desk@eurolicenze.com</a> with the product purchased and the email used for the order.',
    ),
    ("Cosa ricevo esattamente nell'email?", "What exactly do I receive in the email?"),
    (
        "Ricevi la <strong>product key</strong> di Microsoft 365 Family e le istruzioni per riscattarla sui portali ufficiali Microsoft.",
        "You receive the Microsoft 365 Family <strong>product key</strong> and instructions to redeem it on official Microsoft portals.",
    ),
    (
        "La consegna è solo digitale: non viene spedito alcun supporto fisico e non ci sono costi di spedizione.",
        "Delivery is digital only: nothing physical is shipped and there are no shipping fees.",
    ),
    ("Quali metodi di pagamento posso usare?", "Which payment methods can I use?"),
    (
        'Al checkout sono disponibili carta, PayPal e wallet digitali come Apple Pay e Google Pay dove abilitati. L\'elaborazione del pagamento è gestita in modo sicuro tramite <strong>Stripe</strong>.',
        'At checkout you can pay by card, PayPal and digital wallets such as Apple Pay and Google Pay where enabled. Payment processing is handled securely via <strong>Stripe</strong>.',
    ),
    ("Posso avere la fattura elettronica?", "Can I get a VAT invoice?"),
    (
        "Sì. Al checkout scegli il profilo <strong>Azienda</strong> e inserisci partita IVA e Codice SDI oppure PEC: la fattura elettronica viene emessa su quei dati.",
        "Yes. At checkout choose the <strong>Business</strong> profile and enter your VAT details: we issue a VAT invoice on those details.",
    ),
    (
        'Se ti serve dopo l\'ordine, scrivi a <a href="mailto:Desk@eurolicenze.com">Desk@eurolicenze.com</a> indicando l\'email usata per l\'ordine e il numero d\'ordine.',
        'If you need it after the order, email <a href="mailto:Desk@eurolicenze.com">Desk@eurolicenze.com</a> with the order email and order number.',
    ),
    ("Attivazione e account", "Activation and account"),
    ("Come si attiva Microsoft 365 Family dopo l'acquisto?", "How do I activate Microsoft 365 Family after purchase?"),
    (
        'Vai su <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com/Home</a>, accedi con il tuo account Microsoft, inserisci il codice ricevuto via email e segui la procedura guidata. Al termine installa le app da <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.',
        'Go to <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com/Home</a>, sign in with your Microsoft account, enter the code received by email and follow the guided setup. Then install the apps from <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.',
    ),
    ("Posso riscattare il codice su un account Microsoft che uso già?", "Can I redeem the code on a Microsoft account I already use?"),
    (
        "Sì: il riscatto avviene su setup.office.com con il tuo account Microsoft. Se su quell'account è già attivo un abbonamento Microsoft 365, il comportamento (estensione o conversione del piano) segue le regole Microsoft mostrate durante il riscatto.",
        "Yes: redemption happens on setup.office.com with your Microsoft account. If that account already has an active Microsoft 365 subscription, the outcome (extension or plan conversion) follows Microsoft's rules shown during redemption.",
    ),
    (
        "<strong>Scegli l'account con attenzione:</strong> la licenza resta associata a quello usato al momento del riscatto.",
        "<strong>Choose the account carefully:</strong> the licence stays tied to the one used at redemption.",
    ),
    ("Membri e funzionalità", "Members and features"),
    ("Come si invitano altri membri dopo l'acquisto?", "How do I invite other members after purchase?"),
    ("Copilot è disponibile per tutti i membri?", "Is Copilot available to all members?"),
    (
        "No. Le funzionalità Copilot comprese nel piano sono utilizzabili dal <strong>titolare dell'abbonamento</strong>.",
        "No. Copilot features included in the plan are available to the <strong>subscription owner</strong>.",
    ),
    (
        "Gli altri cinque membri ricevono le app Microsoft 365, 1 TB di OneDrive ciascuno e Microsoft Defender, ma non le funzionalità AI.",
        "The other five members get Microsoft 365 apps, 1 TB of OneDrive each and Microsoft Defender, but not the AI features.",
    ),
    ("I file sono condivisi automaticamente tra i membri?", "Are files shared automatically between members?"),
    ("Si possono usare le app Office anche offline?", "Can I use Office apps offline too?"),
    (
        "Sì: con le app desktop installate puoi lavorare offline; servono comunque connessione e accesso periodici per la verifica della licenza, aggiornamenti e servizi cloud come OneDrive.",
        "Yes: with the desktop apps installed you can work offline; periodic connection and sign-in are still required for licence checks, updates and cloud services such as OneDrive.",
    ),
    ("Scelta del piano e assistenza", "Plan choice and support"),
    ("Qual è la differenza tra Microsoft 365 Family e Personal?", "What is the difference between Microsoft 365 Family and Personal?"),
    ("Il codice si rinnova automaticamente dopo 12 mesi?", "Does the code renew automatically after 12 months?"),
    ("Posso usare il codice per rinnovare un abbonamento Family già attivo?", "Can I use the code to renew an active Family subscription?"),
    ("Cosa succede se il codice non funziona?", "What if the code does not work?"),
    (
        "Scrivici indicando numero d'ordine ed eventuale messaggio di errore. Verifichiamo il caso e, se viene confermato un difetto imputabile a noi o al fornitore della chiave, proponiamo sostituzione o rimborso nei tempi usuali di elaborazione.",
        "Contact us with your order number and any error message. We review the case and, if a defect attributable to us or the key supplier is confirmed, we offer a replacement or refund within usual processing times.",
    ),
    (
        'Assistenza: <a href="mailto:Desk@eurolicenze.com">Desk@eurolicenze.com</a> — +39 392 558 0413.',
        'Support: <a href="mailto:Desk@eurolicenze.com">Desk@eurolicenze.com</a> — +39 392 558 0413.',
    ),
    ("Requisiti di sistema", "System requirements"),
    ("Compatibilità e requisiti tecnici", "Compatibility and technical requirements"),
    (
        "Valori indicativi da documentazione Microsoft. Verifica sempre i requisiti aggiornati sulla scheda ufficiale Microsoft prima dell'installazione.",
        "Indicative values from Microsoft documentation. Always check the latest requirements on the official Microsoft product page before installing.",
    ),
    ("Sistemi operativi supportati", "Supported operating systems"),
    (
        "Windows 10 o versioni successive; le tre versioni più recenti di macOS; iOS e Android nelle versioni supportate da Microsoft.",
        "Windows 10 or later; the three most recent versions of macOS; iOS and Android in versions supported by Microsoft.",
    ),
    ("Processore e memoria", "Processor and memory"),
    (
        "Windows: processore a 1,6 GHz o superiore, due core. Mac: processore Intel o Apple Silicon compatibile con la versione di macOS supportata.",
        "Windows: 1.6 GHz or faster processor, two cores. Mac: Intel or Apple Silicon processor compatible with the supported macOS version.",
    ),
    (
        "Memoria: 4 GB di RAM per le versioni a 64 bit, 2 GB per quelle a 32 bit.",
        "Memory: 4 GB RAM for 64-bit versions, 2 GB for 32-bit versions.",
    ),
    ("Spazio su disco", "Disk space"),
    (
        "Circa 4 GB di spazio disponibile su Windows e circa 10 GB su macOS, a seconda delle app installate.",
        "About 4 GB free space on Windows and about 10 GB on macOS, depending on the apps installed.",
    ),
    ("Connessione e account Microsoft", "Connection and Microsoft account"),
    (
        "Servono un account Microsoft e una connessione internet per riscatto, attivazione, aggiornamenti e servizi cloud. Le app desktop installate funzionano anche offline, con verifiche periodiche della licenza.",
        "A Microsoft account and an internet connection are required for redemption, activation, updates and cloud services. Installed desktop apps also work offline, with periodic licence checks.",
    ),
    ("Microsoft 365 per tutta la famiglia", "Microsoft 365 for the whole family"),
    (
        "12 mesi · Fino a 6 persone · 1 TB ciascuno · Codice via email in 5–15 minuti.",
        "12 months · Up to 6 people · 1 TB each · Code by email in 5–15 minutes.",
    ),
    ("IVA inclusa, anziché € 129,00", "Tax included, instead of € 129,00"),
    ("12 mesi", "12 months"),
]

# FR/DE/ES will be generated similarly — to keep this file maintainable we load
# additional locale packs from adjacent dicts below.

FR = [
    (
        "Microsoft 365 Family per 12 mesi, fino a 6 persone del gruppo famiglia: app Microsoft 365 e 1 TB OneDrive a persona. Copilot è riservato al titolare. Codice digitale via email in 5–15 minuti dal pagamento.",
        "Microsoft 365 Famille pour 12 mois, jusqu'à 6 personnes du groupe famille Microsoft : apps Microsoft 365 et 1 To OneDrive par personne. Copilot est réservé au titulaire. Code numérique par e-mail sous 5 à 15 minutes après paiement.",
    ),
    ("Microsoft 365 Family — 12 mesi", "Microsoft 365 Family — 12 mois"),
    ("Vai al contenuto principale", "Aller au contenu principal"),
    ("Acquisto rapido", "Achat rapide"),
    ("Microsoft 365 Family · 12 mesi", "Microsoft 365 Family · 12 mois"),
    ("Acquista ora", "Acheter"),
    ("Prodotto e acquisto", "Produit et achat"),
    ("Percorso navigazione", "Fil d'Ariane"),
    ("Abbonamento digitale · 12 mesi", "Abonnement numérique · 12 mois"),
    ("Codice articolo:", "Code produit :"),
    ("Microsoft 365 Family — grafica del prodotto", "Microsoft 365 Family — visuel du produit"),
    (
        "Microsoft 365 per te e altre cinque persone, con app complete e 1 TB di OneDrive personale per ciascun membro. Copilot è incluso per il titolare dell'abbonamento.",
        "Microsoft 365 pour vous et cinq autres personnes, avec des apps complètes et 1 To d'OneDrive personnel pour chaque membre. Copilot est inclus pour le titulaire de l'abonnement.",
    ),
    ("Fino a 6 persone, ognuna con il proprio account Microsoft", "Jusqu'à 6 personnes, chacune avec son compte Microsoft"),
    ("1 TB di OneDrive a persona, file e impostazioni separati", "1 To d'OneDrive par personne, fichiers et paramètres séparés"),
    ("App desktop sempre aggiornate su PC, Mac, tablet e telefono", "Apps de bureau toujours à jour sur PC, Mac, tablette et téléphone"),
    ("Copilot per il titolare <em>— non condiviso con gli altri membri</em>", "Copilot pour le titulaire <em>— non partagé avec les autres membres</em>"),
    ("Prezzo Eurolicenze", "Prix Eurolicenze"),
    ("Prezzi", "Prix"),
    ("Prezzo scontato 104,95 euro", "Prix réduit 104,95 euros"),
    ("Prezzo originale 129 euro", "Prix d'origine 129 euros"),
    ("Sconto 19 percento", "Remise de 19 pour cent"),
    (
        "IVA inclusa, nessun costo di spedizione. Risparmi <strong>€ 24,05</strong> rispetto al Microsoft Store (€ 129,00).",
        "TVA incluse, aucun frais de livraison. Vous économisez <strong>€ 24,05</strong> par rapport au Microsoft Store (€ 129,00).",
    ),
    ("Aggiungi al carrello", "Ajouter au panier"),
    ("Codice via email in 5–15 minuti dalla conferma del pagamento", "Code par e-mail sous 5 à 15 minutes après confirmation du paiement"),
    (
        "<strong>Incluso con l'acquisto:</strong> guida PDF all'utilizzo di Copilot, via email dopo l'ordine",
        "<strong>Inclus avec l'achat :</strong> guide PDF Copilot, envoyé par e-mail après la commande",
    ),
    ("Attivazione sui portali ufficiali Microsoft", "Activation sur les portails officiels Microsoft"),
    ("Assistenza in italiano dopo l'acquisto", "Assistance après l'achat"),
    ("Fattura elettronica disponibile", "Facture disponible"),
    ("Metodi di pagamento accettati", "Moyens de paiement acceptés"),
    (
        "Pagamenti protetti tramite <strong>Stripe</strong> e <strong>PayPal</strong>",
        "Paiements sécurisés via <strong>Stripe</strong> et <strong>PayPal</strong>",
    ),
    ("Azienda italiana", "Revendeur européen"),
    ("Sede e P.IVA in Italia", "Basé en Italie"),
    ("Fattura elettronica", "Facture disponible"),
    ("Disponibile per privati e aziende", "TVA pour les entreprises"),
    ("Assistenza in italiano", "Support par écrit"),
    ("Supporto post-vendita via email", "E-mail et WhatsApp"),
    ("Pagamenti protetti", "Paiements sécurisés"),
    ("Elaborati tramite Stripe e PayPal", "Via Stripe et PayPal"),
    ('data-cart-added-msg="Prodotto aggiunto al carrello."', 'data-cart-added-msg="Produit ajouté au panier."'),
    ("Cosa ricevi", "Ce que vous recevez"),
    ("Sei persone, account e spazi separati", "Six personnes, comptes et espaces séparés"),
    (
        "Microsoft 365 Family è pensato per essere condiviso: ogni persona lavora sul proprio account, con il proprio spazio cloud.",
        "Microsoft 365 Family est conçu pour être partagé : chaque personne travaille sur son propre compte, avec son propre espace cloud.",
    ),
    ("Persone incluse", "Personnes incluses"),
    ("Titolare più 5 membri invitati, ognuno con account Microsoft separato.", "Titulaire plus 5 membres invités, chacun avec un compte Microsoft séparé."),
    ("OneDrive a persona", "OneDrive par personne"),
    ("Fino a 6 TB complessivi sul piano, non condivisi automaticamente.", "Jusqu'à 6 To au total sur le plan, non partagés automatiquement."),
    ("Durata", "Durée"),
    ("Pagamento una tantum su Eurolicenze, senza addebiti ricorrenti da parte nostra.", "Paiement unique sur Eurolicenze, sans prélèvement récurrent de notre part."),
    ("Dispositivi per persona", "Appareils par personne"),
    ("Accesso contemporaneo su PC, Mac, tablet e telefono, secondo le regole Microsoft.", "Accès simultané sur PC, Mac, tablette et téléphone, selon les règles Microsoft."),
    ("Specifiche del prodotto", "Spécifications du produit"),
    ("Scheda tecnica", "Fiche technique"),
    ("Specifiche tecniche e commerciali di Microsoft 365 Family", "Spécifications techniques et commerciales de Microsoft 365 Family"),
    ("Prodotto", "Produit"),
    ("Utenti", "Utilisateurs"),
    ("Fino a 6 persone", "Jusqu'à 6 personnes"),
    ("Fino a 6", "Jusqu'à 6"),
    ("Archiviazione", "Stockage"),
    ("1 TB OneDrive per persona", "1 To OneDrive par personne"),
    ("Dispositivi", "Appareils"),
    ("Fino a 5 contemporanei per persona", "Jusqu'à 5 simultanés par personne"),
    ("Incluso per il titolare dell'abbonamento", "Inclus pour le titulaire de l'abonnement"),
    ("Consegna", "Livraison"),
    ("Codice digitale via email", "Code numérique par e-mail"),
    ("Attivazione", "Activation"),
    ("Account Microsoft, su setup.office.com", "Compte Microsoft, sur setup.office.com"),
    ("Rinnovo", "Renouvellement"),
    ("Nuova attivazione o estensione secondo le regole Microsoft", "Nouvelle activation ou prolongation selon les règles Microsoft"),
    ("Codice prodotto", "Code produit"),
    ("Fatturazione", "Facturation"),
    ("IVA inclusa, fattura elettronica disponibile", "TVA incluse, facture disponible"),
    ("Chi riceve cosa", "Qui reçoit quoi"),
    ("Un abbonamento condiviso, sei esperienze separate", "Un abonnement partagé, six expériences séparées"),
    (
        "Ogni persona utilizza il proprio account Microsoft. Documenti, email, fotografie e spazio cloud non vengono condivisi automaticamente con gli altri membri. L'unica differenza reale riguarda le funzionalità Copilot.",
        "Chaque personne utilise son propre compte Microsoft. Documents, e-mails, photos et espace cloud ne sont pas partagés automatiquement avec les autres membres. La seule vraie différence concerne les fonctions Copilot.",
    ),
    ("Confronto tra titolare dell'abbonamento e altri membri del gruppo famiglia", "Comparaison entre le titulaire de l'abonnement et les autres membres du groupe famille"),
    ("Funzionalità", "Fonctionnalité"),
    ("Titolare", "Titulaire"),
    ("Altri 5 membri", "5 autres membres"),
    ("Incluso", "Inclus"),
    ("Non incluso", "Non inclus"),
    ("Word, Excel, PowerPoint e Outlook", "Word, Excel, PowerPoint et Outlook"),
    ("1 TB di OneDrive personale", "1 To d'OneDrive personnel"),
    ("Account, file e impostazioni separati", "Comptes, fichiers et paramètres séparés"),
    ("Installazione su più dispositivi", "Installation sur plusieurs appareils"),
    ("Funzionalità Copilot", "Fonctions Copilot"),
    ("Le funzioni AI comprese nel piano restano al proprietario dell'abbonamento.", "Les fonctions d'IA incluses dans le plan restent au propriétaire de l'abonnement."),
    ("App incluse", "Apps incluses"),
    ("Tutte le app che usi, su tutti i tuoi dispositivi", "Toutes les apps que vous utilisez, sur tous vos appareils"),
    (
        "Installa le applicazioni desktop supportate e continua a lavorare anche offline. I documenti possono essere sincronizzati tramite OneDrive.",
        "Installez les applications de bureau prises en charge et continuez à travailler hors ligne. Les documents peuvent être synchronisés via OneDrive.",
    ),
    ("Solo titolare", "Titulaire uniquement"),
    ("Vedi tutte le app incluse", "Voir toutes les apps incluses"),
    ("Famiglia che usa laptop e dispositivi insieme in un ambiente domestico luminoso e moderno.", "Famille utilisant ordinateurs et appareils ensemble dans un intérieur lumineux et moderne."),
    ("Condivisione", "Partage"),
    ("Un piano, account separati", "Un plan, des comptes séparés"),
    (
        "Inviti fino a cinque persone dal tuo account Microsoft. Ognuna riceve il proprio spazio cloud, le proprie app e le proprie impostazioni: nessuno vede i documenti degli altri.",
        "Invitez jusqu'à cinq personnes depuis votre compte Microsoft. Chacune reçoit son propre espace cloud, ses apps et ses paramètres : personne ne voit les documents des autres.",
    ),
    ("Le sei postazioni del piano", "Les six places du plan"),
    ("Membro 2", "Membre 2"),
    ("Membro 3", "Membre 3"),
    ("Membro 4", "Membre 4"),
    ("Membro 5", "Membre 5"),
    ("Membro 6", "Membre 6"),
    ("Tutti ricevono le stesse app. Cambia solo Copilot, che resta al titolare.", "Tout le monde reçoit les mêmes apps. Seul Copilot diffère — il reste au titulaire."),
    ("Quale scegliere", "Lequel choisir"),
    ("Confronta i piani Microsoft 365", "Comparer les plans Microsoft 365"),
    (
        "La differenza non è la potenza delle app: è quante persone useranno davvero il piano.",
        "La différence n'est pas la puissance des apps : c'est le nombre de personnes qui utiliseront vraiment le plan.",
    ),
    ("Confronto tra Microsoft 365 Personal e Microsoft 365 Family", "Comparaison entre Microsoft 365 Personal et Microsoft 365 Family"),
    ("Persone", "Personnes"),
    ("Spazio OneDrive", "Espace OneDrive"),
    ("1 TB a persona", "1 To par personne"),
    ("Account separati per ogni utente", "Compte séparé par utilisateur"),
    ("Non previsto", "Non applicable"),
    ("Prezzo su Eurolicenze", "Prix sur Eurolicenze"),
    ("Ideale per", "Idéal pour"),
    ("Chi usa Office da solo", "Qui utilise Office seul"),
    ("Due o più persone", "Deux personnes ou plus"),
    (
        'Scegli Family se almeno due persone useranno realmente le app o lo spazio OneDrive. Altrimenti valuta <a href="/fr/microsoft-365-personal">Microsoft 365 Personal</a>.',
        'Choisissez Family si au moins deux personnes utiliseront réellement les apps ou l\'espace OneDrive. Sinon, voyez <a href="/fr/microsoft-365-personal">Microsoft 365 Personal</a>.',
    ),
    ("Come funziona", "Comment ça marche"),
    ("Tre passi per iniziare", "Trois étapes pour commencer"),
    ("Completa l'ordine", "Finalisez la commande"),
    ("Paga con uno dei metodi disponibili al checkout: carta, PayPal o wallet digitali.", "Payez avec l'un des moyens disponibles au paiement : carte, PayPal ou portefeuilles numériques."),
    ("Ricevi il codice", "Recevez le code"),
    ("Product key e istruzioni arrivano via email in 5–15 minuti dalla conferma del pagamento.", "La clé produit et les instructions arrivent par e-mail sous 5 à 15 minutes après confirmation du paiement."),
    ("Attiva su Microsoft", "Activez chez Microsoft"),
    (
        'Accedi con il tuo account e riscatta il codice su <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com</a>, poi installa le app da <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.',
        'Connectez-vous avec votre compte et utilisez le code sur <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com</a>, puis installez les apps depuis <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.',
    ),
    (
        "<strong>Controlla di usare l'account Microsoft corretto:</strong> la licenza viene associata all'account scelto durante il riscatto e non può essere spostata successivamente.",
        "<strong>Vérifiez d'utiliser le bon compte Microsoft :</strong> la licence est associée au compte choisi lors de l'activation et ne peut pas être déplacée ensuite.",
    ),
    ("Cosa dicono i clienti", "Ce que disent les clients"),
    (
        "Le recensioni sono pubblicate e verificate da Trustpilot: le leggi direttamente sulla piattaforma, senza filtri da parte nostra.",
        "Les avis sont publiés et vérifiés par Trustpilot : vous les lisez directement sur la plateforme, sans filtre de notre part.",
    ),
    (
        'Esperienze reali dei clienti su Trustpilot. <a href="https://fr.trustpilot.com/review/aml-store.com" target="_blank" rel="noopener noreferrer">Trustpilot</a>',
        'Expériences réelles des clients sur Trustpilot. <a href="https://fr.trustpilot.com/review/aml-store.com" target="_blank" rel="noopener noreferrer">Trustpilot</a>',
    ),
    ("Leggi tutte le recensioni", "Lire tous les avis"),
    ("Acquista con maggiore tranquillità", "Achetez plus sereinement"),
    ("Rivenditore europeo", "Revendeur européen"),
    ("Eurolicenze ha sede legale in Italia", "Eurolicenze a son siège légal en Italie"),
    ("Fattura disponibile", "Facture disponible"),
    ("Documentazione per privati e aziende", "Documentation pour particuliers et entreprises"),
    ("Supporto scritto", "Support par écrit"),
    ("Assistenza via email e WhatsApp", "Assistance par e-mail et WhatsApp"),
    ("Transazioni tramite Stripe e PayPal", "Transactions via Stripe et PayPal"),
    ("Domande frequenti", "Questions fréquentes"),
    ("Le risposte prima dell'acquisto", "Les réponses avant l'achat"),
    ("Acquisto e consegna", "Achat et livraison"),
    ("Quando ricevo il codice dopo il pagamento?", "Quand vais-je recevoir le code après le paiement ?"),
    (
        "L'email di consegna parte dopo la conferma del pagamento, di norma entro 5–15 minuti; in rari casi servono alcuni minuti in più per le verifiche del pagamento.",
        "L'e-mail de livraison part après confirmation du paiement, en général sous 5 à 15 minutes ; dans de rares cas, quelques minutes supplémentaires sont nécessaires pour les vérifications.",
    ),
    (
        'Se dopo <strong>30 minuti</strong> non hai ricevuto nulla, controlla anche spam e posta indesiderata e scrivi a <a href="mailto:Desk@eurolicenze.com">Desk@eurolicenze.com</a> indicando prodotto acquistato ed email usata per l\'ordine.',
        'Si après <strong>30 minutes</strong> vous n\'avez rien reçu, vérifiez aussi les indésirables et écrivez à <a href="mailto:Desk@eurolicenze.com">Desk@eurolicenze.com</a> en indiquant le produit acheté et l\'e-mail utilisé pour la commande.',
    ),
    ("Cosa ricevo esattamente nell'email?", "Que vais-je exactement recevoir dans l'e-mail ?"),
    (
        "Ricevi la <strong>product key</strong> di Microsoft 365 Family e le istruzioni per riscattarla sui portali ufficiali Microsoft.",
        "Vous recevez la <strong>clé produit</strong> Microsoft 365 Family et les instructions pour l'activer sur les portails officiels Microsoft.",
    ),
    (
        "La consegna è solo digitale: non viene spedito alcun supporto fisico e non ci sono costi di spedizione.",
        "La livraison est uniquement numérique : aucun support physique n'est expédié et il n'y a pas de frais de port.",
    ),
    ("Quali metodi di pagamento posso usare?", "Quels moyens de paiement puis-je utiliser ?"),
    (
        'Al checkout sono disponibili carta, PayPal e wallet digitali come Apple Pay e Google Pay dove abilitati. L\'elaborazione del pagamento è gestita in modo sicuro tramite <strong>Stripe</strong>.',
        'Au paiement sont disponibles carte, PayPal et portefeuilles numériques comme Apple Pay et Google Pay lorsqu\'ils sont activés. Le paiement est traité de façon sécurisée via <strong>Stripe</strong>.',
    ),
    ("Posso avere la fattura elettronica?", "Puis-je obtenir une facture ?"),
    (
        "Sì. Al checkout scegli il profilo <strong>Azienda</strong> e inserisci partita IVA e Codice SDI oppure PEC: la fattura elettronica viene emessa su quei dati.",
        "Oui. Au paiement, choisissez le profil <strong>Entreprise</strong> et saisissez vos données de TVA : la facture est émise sur ces informations.",
    ),
    (
        'Se ti serve dopo l\'ordine, scrivi a <a href="mailto:Desk@eurolicenze.com">Desk@eurolicenze.com</a> indicando l\'email usata per l\'ordine e il numero d\'ordine.',
        'Si vous en avez besoin après la commande, écrivez à <a href="mailto:Desk@eurolicenze.com">Desk@eurolicenze.com</a> en indiquant l\'e-mail de commande et le numéro de commande.',
    ),
    ("Attivazione e account", "Activation et compte"),
    ("Come si attiva Microsoft 365 Family dopo l'acquisto?", "Comment activer Microsoft 365 Family après l'achat ?"),
    (
        'Vai su <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com/Home</a>, accedi con il tuo account Microsoft, inserisci il codice ricevuto via email e segui la procedura guidata. Al termine installa le app da <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.',
        'Allez sur <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com/Home</a>, connectez-vous avec votre compte Microsoft, saisissez le code reçu par e-mail et suivez l\'assistant. Ensuite, installez les apps depuis <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.',
    ),
    ("Posso riscattare il codice su un account Microsoft che uso già?", "Puis-je utiliser le code sur un compte Microsoft que j'utilise déjà ?"),
    (
        "Sì: il riscatto avviene su setup.office.com con il tuo account Microsoft. Se su quell'account è già attivo un abbonamento Microsoft 365, il comportamento (estensione o conversione del piano) segue le regole Microsoft mostrate durante il riscatto.",
        "Oui : l'activation se fait sur setup.office.com avec votre compte Microsoft. Si un abonnement Microsoft 365 est déjà actif sur ce compte, le comportement (prolongation ou conversion) suit les règles Microsoft affichées pendant l'activation.",
    ),
    (
        "<strong>Scegli l'account con attenzione:</strong> la licenza resta associata a quello usato al momento del riscatto.",
        "<strong>Choisissez le compte avec attention :</strong> la licence reste associée à celui utilisé lors de l'activation.",
    ),
    ("Membri e funzionalità", "Membres et fonctionnalités"),
    ("Come si invitano altri membri dopo l'acquisto?", "Comment inviter d'autres membres après l'achat ?"),
    (
        "Dopo l'attivazione sul tuo account Microsoft, usa le funzioni di condivisione del piano Family nell'area account Microsoft / abbonamenti, come indicato da Microsoft per il periodo di validità della licenza.",
        "Après activation sur votre compte Microsoft, utilisez les fonctions de partage du plan Family dans la zone compte Microsoft / abonnements, comme indiqué par Microsoft pour la durée de la licence.",
    ),
    ("Copilot è disponibile per tutti i membri?", "Copilot est-il disponible pour tous les membres ?"),
    (
        "No. Le funzionalità Copilot comprese nel piano sono utilizzabili dal <strong>titolare dell'abbonamento</strong>.",
        "Non. Les fonctions Copilot incluses dans le plan sont utilisables par le <strong>titulaire de l'abonnement</strong>.",
    ),
    (
        "Gli altri cinque membri ricevono le app Microsoft 365, 1 TB di OneDrive ciascuno e Microsoft Defender, ma non le funzionalità AI.",
        "Les cinq autres membres reçoivent les apps Microsoft 365, 1 To d'OneDrive chacun et Microsoft Defender, mais pas les fonctions d'IA.",
    ),
    ("I file sono condivisi automaticamente tra i membri?", "Les fichiers sont-ils partagés automatiquement entre les membres ?"),
    (
        "No. Ogni persona usa il proprio account Microsoft, con documenti, email, impostazioni e spazio OneDrive separati. La condivisione di singoli file o cartelle resta una scelta volontaria di chi li possiede.",
        "Non. Chaque personne utilise son propre compte Microsoft, avec documents, e-mails, paramètres et espace OneDrive séparés. Le partage de fichiers ou dossiers individuels reste un choix volontaire du propriétaire.",
    ),
    ("Si possono usare le app Office anche offline?", "Peut-on utiliser les apps Office hors ligne ?"),
    (
        "Sì: con le app desktop installate puoi lavorare offline; servono comunque connessione e accesso periodici per la verifica della licenza, aggiornamenti e servizi cloud come OneDrive.",
        "Oui : avec les apps de bureau installées, vous pouvez travailler hors ligne ; une connexion et une connexion périodiques restent nécessaires pour la vérification de licence, les mises à jour et les services cloud comme OneDrive.",
    ),
    ("Scelta del piano e assistenza", "Choix du plan et assistance"),
    ("Qual è la differenza tra Microsoft 365 Family e Personal?", "Quelle est la différence entre Microsoft 365 Family et Personal ?"),
    (
        "Family è pensato per condividere il piano con il tuo gruppo famiglia Microsoft (fino a 6 persone), ciascuna con account e spazio OneDrive distinti. Personal copre un solo utente con 1 TB, secondo le condizioni Microsoft aggiornate.",
        "Family est conçu pour partager le plan avec votre groupe famille Microsoft (jusqu'à 6 personnes), chacune avec un compte et un espace OneDrive distincts. Personal couvre un seul utilisateur avec 1 To, selon les conditions Microsoft à jour.",
    ),
    ("Il codice si rinnova automaticamente dopo 12 mesi?", "Le code se renouvelle-t-il automatiquement après 12 mois ?"),
    (
        "No. Il codice attiva Microsoft 365 Family per 12 mesi con un pagamento una tantum: Eurolicenze non addebita nulla automaticamente alla scadenza. Eventuali opzioni di rinnovo si gestiscono separatamente, direttamente nell'account Microsoft.",
        "Non. Le code active Microsoft 365 Family pour 12 mois avec un paiement unique : Eurolicenze ne prélève rien automatiquement à l'échéance. Les options de renouvellement éventuelles se gèrent séparément dans le compte Microsoft.",
    ),
    ("Posso usare il codice per rinnovare un abbonamento Family già attivo?", "Puis-je utiliser le code pour renouveler un abonnement Family déjà actif ?"),
    (
        "Sì, puoi riscattarlo sullo stesso account che ha già Microsoft 365 Family attivo. Il modo in cui viene applicato (estensione della durata attuale o avvio di un nuovo periodo) segue le regole Microsoft mostrate al momento del riscatto su setup.office.com, non è qualcosa che decidiamo noi come rivenditore.",
        "Oui, vous pouvez l'activer sur le même compte qui a déjà Microsoft 365 Family. La façon dont il s'applique (prolongation de la durée actuelle ou nouveau période) suit les règles Microsoft affichées lors de l'activation sur setup.office.com — ce n'est pas nous qui le décidons en tant que revendeur.",
    ),
    ("Cosa succede se il codice non funziona?", "Que se passe-t-il si le code ne fonctionne pas ?"),
    (
        "Scrivici indicando numero d'ordine ed eventuale messaggio di errore. Verifichiamo il caso e, se viene confermato un difetto imputabile a noi o al fornitore della chiave, proponiamo sostituzione o rimborso nei tempi usuali di elaborazione.",
        "Écrivez-nous en indiquant le numéro de commande et le message d'erreur éventuel. Nous examinons le cas et, si un défaut imputable à nous ou au fournisseur de la clé est confirmé, nous proposons un remplacement ou un remboursement dans les délais habituels.",
    ),
    (
        'Assistenza: <a href="mailto:Desk@eurolicenze.com">Desk@eurolicenze.com</a> — +39 392 558 0413.',
        'Assistance : <a href="mailto:Desk@eurolicenze.com">Desk@eurolicenze.com</a> — +39 392 558 0413.',
    ),
    ("Requisiti di sistema", "Configuration requise"),
    ("Compatibilità e requisiti tecnici", "Compatibilité et exigences techniques"),
    (
        "Valori indicativi da documentazione Microsoft. Verifica sempre i requisiti aggiornati sulla scheda ufficiale Microsoft prima dell'installazione.",
        "Valeurs indicatives d'après la documentation Microsoft. Vérifiez toujours les exigences à jour sur la fiche Microsoft officielle avant l'installation.",
    ),
    ("Sistemi operativi supportati", "Systèmes d'exploitation pris en charge"),
    (
        "Windows 10 o versioni successive; le tre versioni più recenti di macOS; iOS e Android nelle versioni supportate da Microsoft.",
        "Windows 10 ou versions ultérieures ; les trois versions les plus récentes de macOS ; iOS et Android dans les versions prises en charge par Microsoft.",
    ),
    ("Processore e memoria", "Processeur et mémoire"),
    (
        "Windows: processore a 1,6 GHz o superiore, due core. Mac: processore Intel o Apple Silicon compatibile con la versione di macOS supportata.",
        "Windows : processeur 1,6 GHz ou plus, deux cœurs. Mac : processeur Intel ou Apple Silicon compatible avec la version de macOS prise en charge.",
    ),
    (
        "Memoria: 4 GB di RAM per le versioni a 64 bit, 2 GB per quelle a 32 bit.",
        "Mémoire : 4 Go de RAM pour les versions 64 bits, 2 Go pour les versions 32 bits.",
    ),
    ("Spazio su disco", "Espace disque"),
    (
        "Circa 4 GB di spazio disponibile su Windows e circa 10 GB su macOS, a seconda delle app installate.",
        "Environ 4 Go d'espace libre sous Windows et environ 10 Go sous macOS, selon les apps installées.",
    ),
    ("Connessione e account Microsoft", "Connexion et compte Microsoft"),
    (
        "Servono un account Microsoft e una connessione internet per riscatto, attivazione, aggiornamenti e servizi cloud. Le app desktop installate funzionano anche offline, con verifiche periodiche della licenza.",
        "Un compte Microsoft et une connexion Internet sont nécessaires pour l'activation, les mises à jour et les services cloud. Les apps de bureau installées fonctionnent aussi hors ligne, avec des vérifications périodiques de licence.",
    ),
    ("Microsoft 365 per tutta la famiglia", "Microsoft 365 pour toute la famille"),
    (
        "12 mesi · Fino a 6 persone · 1 TB ciascuno · Codice via email in 5–15 minuti.",
        "12 mois · Jusqu'à 6 personnes · 1 To chacun · Code par e-mail sous 5 à 15 minutes.",
    ),
    ("IVA inclusa, anziché € 129,00", "TVA incluse, au lieu de € 129,00"),
    ("12 mesi", "12 mois"),
    # JSON-LD FAQ strings (shorter variants already covered above where identical)
    (
        "L'email di consegna parte dopo la conferma del pagamento, di norma entro 5–15 minuti; in rari casi servono alcuni minuti in più per le verifiche del pagamento. Se dopo 30 minuti non hai ricevuto nulla, controlla anche spam e posta indesiderata e scrivi a Desk@eurolicenze.com indicando prodotto acquistato ed email usata per l'ordine.",
        "L'e-mail de livraison part après confirmation du paiement, en général sous 5 à 15 minutes ; dans de rares cas, quelques minutes supplémentaires sont nécessaires. Si après 30 minutes vous n'avez rien reçu, vérifiez aussi les indésirables et écrivez à Desk@eurolicenze.com en indiquant le produit acheté et l'e-mail utilisé pour la commande.",
    ),
    (
        "Ricevi la product key di Microsoft 365 Family e le istruzioni per riscattarla sui portali ufficiali Microsoft. La consegna è solo digitale: non viene spedito alcun supporto fisico e non ci sono costi di spedizione.",
        "Vous recevez la clé produit Microsoft 365 Family et les instructions pour l'activer sur les portails officiels Microsoft. La livraison est uniquement numérique : aucun support physique n'est expédié et il n'y a pas de frais de port.",
    ),
    (
        "Al checkout sono disponibili carta, PayPal e wallet digitali come Apple Pay e Google Pay dove abilitati. L'elaborazione del pagamento è gestita in modo sicuro tramite Stripe.",
        "Au paiement sont disponibles carte, PayPal et portefeuilles numériques comme Apple Pay et Google Pay lorsqu'ils sont activés. Le paiement est traité de façon sécurisée via Stripe.",
    ),
    (
        "Sì. Al checkout scegli il profilo Azienda e inserisci partita IVA e Codice SDI oppure PEC: la fattura elettronica viene emessa su quei dati. Se ti serve dopo l'ordine, scrivi a Desk@eurolicenze.com indicando l'email usata per l'ordine e il numero d'ordine.",
        "Oui. Au paiement, choisissez le profil Entreprise et saisissez vos données de TVA : la facture est émise sur ces informations. Si vous en avez besoin après la commande, écrivez à Desk@eurolicenze.com en indiquant l'e-mail de commande et le numéro de commande.",
    ),
    (
        "Vai su setup.office.com/Home, accedi con il tuo account Microsoft, inserisci il codice ricevuto via email e segui la procedura guidata. Al termine installa le app da office.com.",
        "Allez sur setup.office.com/Home, connectez-vous avec votre compte Microsoft, saisissez le code reçu par e-mail et suivez l'assistant. Ensuite, installez les apps depuis office.com.",
    ),
    (
        "Sì: il riscatto avviene su setup.office.com con il tuo account Microsoft. Se su quell'account è già attivo un abbonamento Microsoft 365, il comportamento (estensione o conversione del piano) segue le regole Microsoft mostrate durante il riscatto. Scegli l'account con attenzione: la licenza resta associata a quello usato al momento del riscatto.",
        "Oui : l'activation se fait sur setup.office.com avec votre compte Microsoft. Si un abonnement Microsoft 365 est déjà actif, le comportement suit les règles Microsoft affichées pendant l'activation. Choisissez le compte avec attention : la licence reste associée à celui utilisé lors de l'activation.",
    ),
    (
        "No. Le funzionalità Copilot comprese nel piano sono utilizzabili dal titolare dell'abbonamento. Gli altri cinque membri ricevono le app Microsoft 365, 1 TB di OneDrive ciascuno e Microsoft Defender, ma non le funzionalità AI.",
        "Non. Les fonctions Copilot incluses dans le plan sont utilisables par le titulaire de l'abonnement. Les cinq autres membres reçoivent les apps Microsoft 365, 1 To d'OneDrive chacun et Microsoft Defender, mais pas les fonctions d'IA.",
    ),
    (
        "Sì: con le app desktop installate puoi lavorare offline; servono comunque connessione e accesso periodici per la verifica della licenza, aggiornamenti e servizi cloud come OneDrive, come descritto da Microsoft.",
        "Oui : avec les apps de bureau installées, vous pouvez travailler hors ligne ; une connexion périodique reste nécessaire pour la vérification de licence, les mises à jour et les services cloud comme OneDrive, comme décrit par Microsoft.",
    ),
    (
        "Scrivici indicando numero d'ordine ed eventuale messaggio di errore. Verifichiamo il caso e, se viene confermato un difetto imputabile a noi o al fornitore della chiave, proponiamo sostituzione o rimborso nei tempi usuali di elaborazione. Assistenza: Desk@eurolicenze.com — +39 392 558 0413.",
        "Écrivez-nous en indiquant le numéro de commande et le message d'erreur éventuel. Nous examinons le cas et, si un défaut imputable à nous ou au fournisseur de la clé est confirmé, nous proposons un remplacement ou un remboursement dans les délais habituels. Assistance : Desk@eurolicenze.com — +39 392 558 0413.",
    ),
]


def apply_pairs(text: str, pairs: list[tuple[str, str]]) -> str:
    for src, dst in sorted(pairs, key=lambda p: len(p[0]), reverse=True):
        if src not in text:
            # allow missing for locale-specific path variants already rewritten
            continue
        text = text.replace(src, dst)
    return text


def localize(html: str, lang: str, og: str, tp_host: str, tp_locale: str, pairs: list[tuple[str, str]]) -> str:
    out = html
    out = out.replace('lang="it"', f'lang="{lang}"', 1)
    out = out.replace("og:locale\" content=\"it_IT\"", f"og:locale\" content=\"{og}\"")
    out = out.replace('"inLanguage": "it"', f'"inLanguage": "{lang}"')
    out = out.replace("https://eurolicenze.com/it/", f"https://eurolicenze.com/{lang}/")
    # Keep x-default on Italian after the path rewrite above
    out = out.replace(
        f'hreflang="x-default" href="https://eurolicenze.com/{lang}/microsoft-365-family"',
        'hreflang="x-default" href="https://eurolicenze.com/it/microsoft-365-family"',
    )
    out = out.replace('href="/it/', f'href="/{lang}/')
    out = out.replace("https://it.trustpilot.com/review/aml-store.com", f"https://{tp_host}/review/aml-store.com")
    out = out.replace('data-locale="it-IT"', f'data-locale="{tp_locale}"')
    # Personal link path already handled by /it/ -> /lang/ above; EN Personal path fix in pairs
    out = apply_pairs(out, pairs)
    return out


def leftover_italian(html: str) -> list[str]:
    markers = [
        "Vai al", "Acquista", "Aggiungi", "Abbonamento digitale", "Codice articolo",
        "Prezzo AML", "Cosa ricevi", "Scheda tecnica", "Titolare", "Membro ",
        "Domande frequenti", "fattura elettronica", "Assistenza in italiano",
        "Azienda italiana", "mesi", "Persone incluse", "Come funziona",
    ]
    hits = []
    for m in markers:
        if m in html:
            hits.append(m)
    return hits


def main() -> None:
    src = SRC.read_text(encoding="utf-8")
    configs = [
        ("en", "en_GB", "www.trustpilot.com", "en-US", EN),
        ("fr", "fr_FR", "fr.trustpilot.com", "fr-FR", FR),
    ]
    # DE and ES packs loaded from sibling module files if present, else warn
    try:
        from port_m365_family_de_es import DE, ES  # type: ignore
        configs.append(("de", "de_DE", "de.trustpilot.com", "de-DE", DE))
        configs.append(("es", "es_ES", "es.trustpilot.com", "es-ES", ES))
    except ImportError:
        print("WARNING: DE/ES pack missing — only EN/FR written")

    for lang, og, tp_host, tp_locale, pairs in configs:
        out = localize(src, lang, og, tp_host, tp_locale, pairs)
        # Fix Personal link if still pointing wrong (EN pairs already set /en/)
        path = ROOT / lang / "microsoft-365-family.html"
        path.write_text(out, encoding="utf-8", newline="\n")
        left = leftover_italian(out)
        print(f"{lang}: wrote {path.relative_to(ROOT)} ({len(out)} bytes) leftovers={left[:8]}")


if __name__ == "__main__":
    main()
