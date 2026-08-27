"""Contenuti per Windows Server e SQL Server.

Composti da fatti per prodotto (versione, core, supporto) più testi per lingua, così
una correzione di licenza si fa in un punto solo invece che su sette schede × 5 lingue.

Fonti dei dati tecnici (verificate 2026-08):
- Requisiti Windows Server: learn.microsoft.com/windows-server/get-started/hardware-requirements
- Requisiti SQL Server 2022: learn.microsoft.com/sql/sql-server/install/hardware-and-software-requirements-for-installing-sql-server-2022
- Limiti core per edizione SQL: learn.microsoft.com/sql/sql-server/compute-capacity-limits-by-edition-of-sql-server
- Licenze Windows Server: microsoft.com/licensing/docs (Licensing_guide_PLT_Windows_Server_2022.pdf)

Due fatti che governano il contenuto:
- Windows Server: le CAL NON sono incluse, servono a parte per ogni utente/dispositivo.
- SQL Server con licenza per core: le CAL non servono affatto.
"""

from nl_translations import nl_text

LANGS = ("it", "en", "fr", "de", "es", "pt", "nl")

# slug -> versione, core, supporto ("dvd" = fisico in inglese, "esd" = digitale)
WINDOWS_SERVER = {
    "windows-server-2019": {"anno": "2019", "cores": 16, "media": "dvd"},
    "windows-server-2019-esd": {"anno": "2019", "cores": 16, "media": "esd"},
    "windows-server-2022": {"anno": "2022", "cores": 16, "media": "dvd"},
    "windows-server-2025": {"anno": "2025", "cores": 16, "media": "esd"},
    "windows-server-2025-dvd": {"anno": "2025", "cores": 16, "media": "dvd"},
}

SQL_SERVER = {
    "sql-server-2022-standard": {"ed": "Standard", "cores": 16, "media": "dvd"},
    "sql-server-2022-enterprise": {"ed": "Enterprise", "cores": 24, "media": "dvd"},
}

# Requisiti RAM: 2025 alza il minimo e aggiunge istruzioni CPU non presenti su hardware vecchio
WS_RAM = {
    "2019": {"it": "1 GB per Server Core, 2 GB con Desktop Experience.",
             "en": "1 GB for Server Core, 2 GB with Desktop Experience.",
             "fr": "1 Go pour Server Core, 2 Go avec Desktop Experience.",
             "de": "1 GB für Server Core, 2 GB mit Desktop Experience.",
             "es": "1 GB para Server Core, 2 GB con Desktop Experience.",
             "pt": "1 GB para Server Core, 2 GB com Desktop Experience.",
             "nl": "1 GB voor Server Core, 2 GB met Desktop Experience."},
    "2025": {"it": "2 GB per Server Core e 2 GB con Desktop Experience, 4 GB consigliati.",
             "en": "2 GB for Server Core and 2 GB with Desktop Experience, 4 GB recommended.",
             "fr": "2 Go pour Server Core et 2 Go avec Desktop Experience, 4 Go recommandés.",
             "de": "2 GB für Server Core und 2 GB mit Desktop Experience, 4 GB empfohlen.",
             "es": "2 GB para Server Core y 2 GB con Desktop Experience, 4 GB recomendados.",
             "pt": "2 GB para Server Core e 2 GB com Desktop Experience, 4 GB recomendados.",
             "nl": "2 GB voor Server Core en 2 GB met Desktop Experience, 4 GB aanbevolen."},
}
WS_RAM["2022"] = WS_RAM["2019"]

WS_CPU = {
    "2019": {"it": "Processore 64 bit da almeno 1,4 GHz, compatibile x64 con NX, DEP e SLAT.",
             "en": "64-bit processor at 1.4 GHz or faster, x64-compatible with NX, DEP and SLAT.",
             "fr": "Processeur 64 bits à 1,4 GHz minimum, compatible x64 avec NX, DEP et SLAT.",
             "de": "64-Bit-Prozessor ab 1,4 GHz, x64-kompatibel mit NX, DEP und SLAT.",
             "es": "Procesador de 64 bits desde 1,4 GHz, compatible x64 con NX, DEP y SLAT.",
             "pt": "Processador de 64 bits a partir de 1,4 GHz, compatível x64 com NX, DEP e SLAT.",
             "nl": "64-bit processor vanaf 1,4 GHz, x64-compatibel met NX, DEP en SLAT."},
    "2025": {"it": "Processore 64 bit da almeno 1,4 GHz. La versione 2025 richiede in più le istruzioni SSE4.2 e POPCNT: verifica la CPU prima di acquistare.",
             "en": "64-bit processor at 1.4 GHz or faster. The 2025 release also requires SSE4.2 and POPCNT instructions: check your CPU before buying.",
             "fr": "Processeur 64 bits à 1,4 GHz minimum. La version 2025 exige en plus les instructions SSE4.2 et POPCNT : vérifiez le processeur avant l'achat.",
             "de": "64-Bit-Prozessor ab 1,4 GHz. Version 2025 benötigt zusätzlich SSE4.2 und POPCNT: CPU vor dem Kauf prüfen.",
             "es": "Procesador de 64 bits desde 1,4 GHz. La versión 2025 exige además las instrucciones SSE4.2 y POPCNT: comprueba la CPU antes de comprar.",
             "pt": "Processador de 64 bits a partir de 1,4 GHz. A versão 2025 exige também as instruções SSE4.2 e POPCNT: verifica o processador antes de comprar.",
             "nl": "64-bit processor vanaf 1,4 GHz. Versie 2025 vereist ook de instructies SSE4.2 en POPCNT: controleer de processor vóór aankoop."},
}
WS_CPU["2022"] = WS_CPU["2019"]

T = {
    "it": {
        "ws_eyebrow": "Licenza perpetua · {cores} core",
        "ws_title": 'Windows Server <span>{anno} Standard</span>',
        "ws_name": "Windows Server {anno} Standard",
        "ws_seo": "Windows Server {anno} Standard {cores} core — Eurolicenze",
        "ws_desc": ("Windows Server {anno} Standard a 64 bit con licenza perpetua per {cores} core. "
                    "{consegna} Le CAL di accesso client non sono incluse: vanno acquistate a parte "
                    "per ogni utente o dispositivo che userà il server."),
        "ws_feat_title": "Cosa copre questa licenza",
        "ws_f1": ("Licenza per core", "Copre {cores} core",
                  "La licenza copre un server con un massimo di {cores} core fisici. Se il tuo server ne ha di più, servono licenze aggiuntive per coprirli tutti."),
        "ws_f2": ("Da sapere", "Le CAL non sono incluse",
                  "Windows Server richiede una CAL per ogni utente o dispositivo che accede al server. Non sono comprese in questa licenza e si acquistano separatamente."),
        "ws_f3": ("Virtualizzazione", "Fino a 2 ambienti server",
                  "L'edizione Standard dà diritto a due ambienti di sistema operativo, o container Windows con isolamento Hyper-V, quando tutti i core fisici sono licenziati."),
        "ws_f4": ("Ruoli", "Active Directory, Hyper-V, file e web",
                  "Include i ruoli server di Windows Server Standard: servizi di dominio Active Directory, Hyper-V, file server, stampa e IIS."),
        "ws_f5_dvd": ("Supporto", "DVD OEM in lingua inglese",
                      "Ricevi il supporto fisico OEM. L'interfaccia del sistema operativo è in inglese: tienine conto se ti serve l'italiano."),
        "ws_f5_esd": ("Consegna", "Licenza digitale via email",
                      "Ricevi codice e istruzioni via email dopo la conferma del pagamento: nessuna spedizione da attendere."),
        "ws_f6_2025": ("Novità 2025", "Aggiornamenti senza riavvio",
                       "Windows Server 2025 introduce l'hotpatching tramite Azure Arc, che riduce i riavvii pianificati, insieme ad Active Directory rafforzata e supporto NVMe nativo."),
        "sql_eyebrow": "Licenza perpetua · {cores} core",
        "sql_title": 'SQL Server <span>2022 {ed}</span>',
        "sql_name": "SQL Server 2022 {ed}",
        "sql_seo": "SQL Server 2022 {ed} {cores} core — Eurolicenze",
        "sql_desc": ("SQL Server 2022 {ed} con licenza perpetua per core ({cores} core). "
                     "Con il modello per core non servono CAL: il numero di utenti che accedono al database è illimitato. "
                     "Supporto fisico incluso, interfaccia in inglese."),
        "sql_feat_title": "Cosa comprende la licenza",
        "sql_f1": ("Modello di licenza", "Nessuna CAL da acquistare",
                   "Con la licenza per core non servono licenze di accesso client: qualunque numero di utenti o applicazioni può usare il database senza costi aggiuntivi per postazione."),
        "sql_f2": ("Capacità", "Licenza per {cores} core",
                   "Copre {cores} core. Microsoft richiede un minimo di quattro core licenziati per server o macchina virtuale."),
        "sql_f3_std": ("Limiti edizione", "Fino a 24 core",
                       "L'edizione Standard usa al massimo il minore tra 4 socket e 24 core: questa licenza da 16 core rientra ampiamente nel limite."),
        "sql_f3_ent": ("Limiti edizione", "Nessun limite di core",
                       "L'edizione Enterprise non ha limiti di core con la licenza per core, e sblocca le funzioni avanzate di alta disponibilità e analisi."),
        "sql_f4": ("Compatibilità", "Windows Server 2016 o successivo",
                   "Si installa su Windows Server 2016 e versioni successive, anche in modalità Server Core. Richiede .NET Framework 4.7.2."),
        "consegna_dvd": "Ricevi il DVD OEM originale con spedizione gratuita; l'interfaccia è in lingua inglese.",
        "consegna_esd": "Codice e istruzioni arrivano via email dopo la conferma del pagamento.",
        "spec_cpu": "Processore",
        "spec_ram": "Memoria",
        "spec_disk": "Spazio su disco",
        "spec_net": "Rete",
        "ws_disk": "Almeno 32 GB liberi sulla partizione di sistema. Server con oltre 16 GB di RAM richiedono spazio aggiuntivo per paging e file di dump.",
        "ws_net": "Adattatore Ethernet con throughput di almeno 1 Gbit/s, conforme alle specifiche PCI Express.",
        "sql_cpu": "Processore x64 da almeno 1,4 GHz, 2,0 GHz o superiore consigliato. L'installazione è supportata solo su processori x64.",
        "sql_ram": "Almeno 1 GB di RAM, con 4 GB o più consigliati e da aumentare al crescere del database.",
        "sql_disk": "Almeno 6 GB liberi. L'installazione completa di tutte le funzionalità richiede circa 8 GB.",
        "sql_os": "Sistema operativo",
        "sql_os_body": "Windows Server 2016 o successivo, oppure Windows 10 versione 1607 o successiva. Richiede .NET Framework 4.7.2.",
        "specs_note": "Valori indicativi dalla documentazione Microsoft. Verifica sempre i requisiti aggiornati prima dell'installazione.",
        "steps_title": "Ordine, consegna e attivazione",
        "step1": ("Completa l'ordine", "Paga con uno dei metodi disponibili al checkout: carta, PayPal o wallet digitali."),
        "step2_dvd": ("Ricevi il supporto", "Spediamo il DVD originale con spedizione gratuita: affidamento al corriere entro 24 ore lavorative dal pagamento."),
        "step2_esd": ("Ricevi il codice", "Product key e istruzioni arrivano via email dopo la conferma del pagamento."),
        "step3": ("Installa e attiva", "Installa il sistema e attiva la licenza tramite i canali ufficiali Microsoft, seguendo le istruzioni ricevute."),
        "faq_cal_q": "Le CAL sono incluse nel prezzo?",
        "faq_cal_a": "No. Windows Server richiede una licenza di accesso client (CAL) per ogni utente o dispositivo che usa il server, e non è compresa in questa licenza. Le CAL si acquistano separatamente e valgono per l'intero ambiente, non per singolo server.",
        "faq_core_q": "Cosa succede se il mio server ha più di {cores} core?",
        "faq_core_a": "La licenza copre {cores} core. Se il server ne ha di più devi licenziare tutti i core fisici, acquistando licenze aggiuntive. Microsoft richiede un minimo di {cores} core licenziati per server.",
        "faq_virt_q": "Quante macchine virtuali posso eseguire?",
        "faq_virt_a": "L'edizione Standard dà diritto a due ambienti di sistema operativo (o container Windows con isolamento Hyper-V) quando tutti i core fisici del server sono licenziati. Servono licenze aggiuntive oltre questo limite.",
        "faq_lang_q": "In che lingua è il sistema operativo?",
        "faq_lang_a": "Il supporto OEM è in lingua inglese: interfaccia e installazione sono in inglese. Verificalo prima dell'acquisto se ti serve l'italiano.",
        "faq_media_q": "Cosa ricevo esattamente?",
        "faq_media_a": "Ricevi il codice di licenza e le istruzioni via email dopo la conferma del pagamento. La consegna è solo digitale: non viene spedito alcun supporto fisico.",
        "faq_sqlcal_q": "Servono CAL per SQL Server?",
        "faq_sqlcal_a": "No. Con la licenza per core non sono richieste licenze di accesso client: possono usare il database quanti utenti o applicazioni vuoi, senza costi per postazione.",
        "faq_sqlos_q": "Su quali sistemi operativi si installa?",
        "faq_sqlos_a": "Su Windows Server 2016 e versioni successive, comprese le installazioni Server Core, oppure su Windows 10 versione 1607 e successive. Richiede .NET Framework 4.7.2.",
        "faq_sqlmin_q": "C'è un minimo di core da licenziare?",
        "faq_sqlmin_a": "Sì: Microsoft richiede almeno quattro core licenziati per ogni server fisico o macchina virtuale su cui installi SQL Server.",
    },
}

# Le altre lingue partono dall'italiano e ne sostituiscono i testi: qui sotto solo
# le chiavi tradotte, il fallback tiene il resto allineato se una manca.
T["en"] = dict(T["it"], **{
    "ws_eyebrow": "Perpetual licence · {cores} cores",
    "ws_title": 'Windows Server <span>{anno} Standard</span>',
    "ws_name": "Windows Server {anno} Standard",
    "ws_seo": "Windows Server {anno} Standard {cores} cores — Eurolicenze",
    "ws_desc": ("Windows Server {anno} Standard 64-bit with a perpetual licence for {cores} cores. "
                "{consegna} Client Access Licences are not included: you buy them separately for every "
                "user or device that will use the server."),
    "ws_feat_title": "What this licence covers",
    "ws_f1": ("Core licensing", "Covers {cores} cores",
              "The licence covers a server with up to {cores} physical cores. If your server has more, you need additional licences to cover them all."),
    "ws_f2": ("Worth knowing", "CALs are not included",
              "Windows Server needs a CAL for every user or device accessing the server. They are not part of this licence and are bought separately."),
    "ws_f3": ("Virtualisation", "Up to 2 server environments",
              "Standard edition grants two operating system environments, or Windows containers with Hyper-V isolation, once every physical core is licensed."),
    "ws_f4": ("Roles", "Active Directory, Hyper-V, file and web",
              "Includes the Windows Server Standard roles: Active Directory Domain Services, Hyper-V, file and print server, and IIS."),
    "ws_f5_dvd": ("Media", "OEM DVD in English",
                  "You receive the physical OEM media. The operating system interface is in English — worth checking if you need another language."),
    "ws_f5_esd": ("Delivery", "Digital licence by email",
                  "Key and instructions arrive by email once your payment is confirmed: nothing to wait for in the post."),
    "ws_f6_2025": ("New in 2025", "Updates without restarting",
                   "Windows Server 2025 adds hotpatching through Azure Arc, cutting planned reboots, alongside a hardened Active Directory and native NVMe support."),
    "sql_eyebrow": "Perpetual licence · {cores} cores",
    "sql_name": "SQL Server 2022 {ed}",
    "sql_seo": "SQL Server 2022 {ed} {cores} cores — Eurolicenze",
    "sql_desc": ("SQL Server 2022 {ed} with a perpetual per-core licence ({cores} cores). "
                 "Per-core licensing needs no CALs: any number of users can reach the database. "
                 "Physical media included, English interface."),
    "sql_feat_title": "What the licence includes",
    "sql_f1": ("Licensing model", "No CALs to buy",
               "Per-core licensing requires no client access licences: any number of users or applications can use the database with no extra per-seat cost."),
    "sql_f2": ("Capacity", "Licence for {cores} cores",
               "Covers {cores} cores. Microsoft requires a minimum of four licensed cores per server or virtual machine."),
    "sql_f3_std": ("Edition limits", "Up to 24 cores",
                   "Standard edition uses at most the lesser of 4 sockets or 24 cores: this 16-core licence sits comfortably inside that limit."),
    "sql_f3_ent": ("Edition limits", "No core limit",
                   "Enterprise edition has no core limit under per-core licensing, and unlocks the advanced high-availability and analytics features."),
    "sql_f4": ("Compatibility", "Windows Server 2016 or later",
               "Installs on Windows Server 2016 and later, including Server Core. Requires .NET Framework 4.7.2."),
    "consegna_dvd": "You receive the genuine OEM DVD with free shipping; the interface is in English.",
    "consegna_esd": "Key and instructions arrive by email once your payment is confirmed.",
    "spec_cpu": "Processor", "spec_ram": "Memory", "spec_disk": "Disk space", "spec_net": "Network",
    "ws_disk": "At least 32 GB free on the system partition. Servers with more than 16 GB of RAM need extra room for paging and dump files.",
    "ws_net": "Ethernet adapter with at least 1 Gbps throughput, compliant with the PCI Express specification.",
    "sql_cpu": "x64 processor at 1.4 GHz or faster, 2.0 GHz or above recommended. Installation is supported on x64 processors only.",
    "sql_ram": "At least 1 GB of RAM, 4 GB or more recommended and increasing as the database grows.",
    "sql_disk": "At least 6 GB free. A full install of every feature needs around 8 GB.",
    "sql_os": "Operating system",
    "sql_os_body": "Windows Server 2016 or later, or Windows 10 version 1607 or later. Requires .NET Framework 4.7.2.",
    "specs_note": "Indicative figures from Microsoft documentation. Always check the current requirements before installing.",
    "steps_title": "Order, delivery and activation",
    "step1": ("Complete your order", "Pay with any method available at checkout: card, PayPal or digital wallets."),
    "step2_dvd": ("Receive the media", "We ship the genuine DVD with free shipping: handed to the courier within 24 business hours of payment."),
    "step2_esd": ("Receive the key", "Product key and instructions arrive by email once your payment is confirmed."),
    "step3": ("Install and activate", "Install the system and activate the licence through official Microsoft channels, following the instructions you receive."),
    "faq_cal_q": "Are CALs included in the price?",
    "faq_cal_a": "No. Windows Server requires a Client Access Licence for every user or device using the server, and it is not part of this licence. CALs are bought separately and cover your whole environment rather than a single server.",
    "faq_core_q": "What if my server has more than {cores} cores?",
    "faq_core_a": "The licence covers {cores} cores. If your server has more, every physical core must be licensed, so you buy additional licences. Microsoft requires a minimum of {cores} licensed cores per server.",
    "faq_virt_q": "How many virtual machines can I run?",
    "faq_virt_a": "Standard edition grants two operating system environments (or Windows containers with Hyper-V isolation) once every physical core in the server is licensed. Beyond that you need additional licences.",
    "faq_lang_q": "What language is the operating system in?",
    "faq_lang_a": "The OEM media is English: the interface and setup are in English. Check this before ordering if you need another language.",
    "faq_media_q": "What exactly do I receive?",
    "faq_media_a": "You receive the licence key and instructions by email once your payment is confirmed. Delivery is digital only: no physical media is shipped.",
    "faq_sqlcal_q": "Do I need CALs for SQL Server?",
    "faq_sqlcal_a": "No. Per-core licensing requires no client access licences: as many users or applications as you like can use the database, with no per-seat cost.",
    "faq_sqlos_q": "Which operating systems can I install it on?",
    "faq_sqlos_a": "Windows Server 2016 and later, including Server Core installations, or Windows 10 version 1607 and later. Requires .NET Framework 4.7.2.",
    "faq_sqlmin_q": "Is there a minimum number of cores to license?",
    "faq_sqlmin_a": "Yes: Microsoft requires at least four licensed cores for every physical server or virtual machine running SQL Server.",
})

T["fr"] = dict(T["it"], **{
    "ws_eyebrow": "Licence perpétuelle · {cores} cœurs",
    "ws_name": "Windows Server {anno} Standard",
    "ws_seo": "Windows Server {anno} Standard {cores} cœurs — Eurolicenze",
    "ws_desc": ("Windows Server {anno} Standard 64 bits avec licence perpétuelle pour {cores} cœurs. "
                "{consegna} Les licences d'accès client ne sont pas incluses : elles s'achètent à part "
                "pour chaque utilisateur ou appareil qui utilisera le serveur."),
    "ws_feat_title": "Ce que couvre cette licence",
    "ws_f1": ("Licence par cœur", "Couvre {cores} cœurs",
              "La licence couvre un serveur avec au maximum {cores} cœurs physiques. Si le vôtre en compte davantage, des licences supplémentaires sont nécessaires."),
    "ws_f2": ("À savoir", "Les CAL ne sont pas incluses",
              "Windows Server exige une CAL par utilisateur ou appareil accédant au serveur. Elle n'est pas comprise dans cette licence et s'achète séparément."),
    "ws_f3": ("Virtualisation", "Jusqu'à 2 environnements serveur",
              "L'édition Standard donne droit à deux environnements de système d'exploitation, ou conteneurs Windows avec isolation Hyper-V, dès lors que tous les cœurs physiques sont licenciés."),
    "ws_f4": ("Rôles", "Active Directory, Hyper-V, fichiers et web",
              "Inclut les rôles de Windows Server Standard : services de domaine Active Directory, Hyper-V, serveur de fichiers et d'impression, IIS."),
    "ws_f5_dvd": ("Support", "DVD OEM en anglais",
                  "Vous recevez le support physique OEM. L'interface du système est en anglais : vérifiez-le si vous avez besoin du français."),
    "ws_f5_esd": ("Livraison", "Licence numérique par e-mail",
                  "Clé et instructions arrivent par e-mail après confirmation du paiement : rien à attendre par la poste."),
    "ws_f6_2025": ("Nouveautés 2025", "Mises à jour sans redémarrage",
                   "Windows Server 2025 apporte le hotpatching via Azure Arc, qui réduit les redémarrages planifiés, ainsi qu'un Active Directory renforcé et la prise en charge native NVMe."),
    "sql_eyebrow": "Licence perpétuelle · {cores} cœurs",
    "sql_name": "SQL Server 2022 {ed}",
    "sql_seo": "SQL Server 2022 {ed} {cores} cœurs — Eurolicenze",
    "sql_desc": ("SQL Server 2022 {ed} avec licence perpétuelle par cœur ({cores} cœurs). "
                 "Le modèle par cœur ne nécessite aucune CAL : le nombre d'utilisateurs accédant à la base est illimité. "
                 "Support physique inclus, interface en anglais."),
    "sql_feat_title": "Ce que comprend la licence",
    "sql_f1": ("Modèle de licence", "Aucune CAL à acheter",
               "La licence par cœur n'exige pas de licences d'accès client : autant d'utilisateurs ou d'applications que vous voulez peuvent utiliser la base, sans coût par poste."),
    "sql_f2": ("Capacité", "Licence pour {cores} cœurs",
               "Couvre {cores} cœurs. Microsoft impose un minimum de quatre cœurs licenciés par serveur ou machine virtuelle."),
    "sql_f3_std": ("Limites d'édition", "Jusqu'à 24 cœurs",
                   "L'édition Standard utilise au maximum le plus petit entre 4 sockets et 24 cœurs : cette licence de 16 cœurs reste largement dans la limite."),
    "sql_f3_ent": ("Limites d'édition", "Aucune limite de cœurs",
                   "L'édition Enterprise n'a pas de limite de cœurs avec la licence par cœur, et débloque les fonctions avancées de haute disponibilité et d'analyse."),
    "sql_f4": ("Compatibilité", "Windows Server 2016 ou ultérieur",
               "S'installe sur Windows Server 2016 et versions ultérieures, y compris Server Core. Nécessite .NET Framework 4.7.2."),
    "consegna_dvd": "Vous recevez le DVD OEM original en livraison gratuite ; l'interface est en anglais.",
    "consegna_esd": "Clé et instructions arrivent par e-mail après confirmation du paiement.",
    "spec_cpu": "Processeur", "spec_ram": "Mémoire", "spec_disk": "Espace disque", "spec_net": "Réseau",
    "ws_disk": "Au moins 32 Go libres sur la partition système. Les serveurs de plus de 16 Go de RAM demandent de l'espace supplémentaire pour la pagination et les fichiers de vidage.",
    "ws_net": "Adaptateur Ethernet d'au moins 1 Gbit/s, conforme aux spécifications PCI Express.",
    "sql_cpu": "Processeur x64 à 1,4 GHz minimum, 2,0 GHz ou plus recommandé. L'installation n'est prise en charge que sur processeurs x64.",
    "sql_ram": "Au moins 1 Go de RAM, 4 Go ou plus recommandés et à augmenter avec la taille de la base.",
    "sql_disk": "Au moins 6 Go libres. Une installation complète de toutes les fonctionnalités demande environ 8 Go.",
    "sql_os": "Système d'exploitation",
    "sql_os_body": "Windows Server 2016 ou ultérieur, ou Windows 10 version 1607 ou ultérieure. Nécessite .NET Framework 4.7.2.",
    "specs_note": "Valeurs indicatives issues de la documentation Microsoft. Vérifiez toujours les prérequis à jour avant l'installation.",
    "steps_title": "Commande, livraison et activation",
    "step1": ("Finalisez la commande", "Payez avec l'un des moyens disponibles au checkout : carte, PayPal ou portefeuilles numériques."),
    "step2_dvd": ("Recevez le support", "Nous expédions le DVD original en livraison gratuite : remise au transporteur sous 24 heures ouvrées après paiement."),
    "step2_esd": ("Recevez la clé", "Clé de produit et instructions arrivent par e-mail après confirmation du paiement."),
    "step3": ("Installez et activez", "Installez le système et activez la licence via les canaux officiels Microsoft, en suivant les instructions reçues."),
    "faq_cal_q": "Les CAL sont-elles incluses dans le prix ?",
    "faq_cal_a": "Non. Windows Server exige une licence d'accès client pour chaque utilisateur ou appareil utilisant le serveur, et elle n'est pas comprise ici. Les CAL s'achètent séparément et couvrent tout votre environnement, pas un seul serveur.",
    "faq_core_q": "Que se passe-t-il si mon serveur a plus de {cores} cœurs ?",
    "faq_core_a": "La licence couvre {cores} cœurs. Si le serveur en compte davantage, tous les cœurs physiques doivent être licenciés : il faut donc des licences supplémentaires. Microsoft impose un minimum de {cores} cœurs licenciés par serveur.",
    "faq_virt_q": "Combien de machines virtuelles puis-je exécuter ?",
    "faq_virt_a": "L'édition Standard donne droit à deux environnements de système d'exploitation (ou conteneurs Windows avec isolation Hyper-V) dès lors que tous les cœurs physiques du serveur sont licenciés. Au-delà, des licences supplémentaires sont nécessaires.",
    "faq_lang_q": "Dans quelle langue est le système d'exploitation ?",
    "faq_lang_a": "Le support OEM est en anglais : l'interface et l'installation sont en anglais. Vérifiez-le avant de commander si vous avez besoin d'une autre langue.",
    "faq_media_q": "Que reçois-je exactement ?",
    "faq_media_a": "Vous recevez la clé de licence et les instructions par e-mail après confirmation du paiement. La livraison est uniquement numérique : aucun support physique n'est expédié.",
    "faq_sqlcal_q": "Faut-il des CAL pour SQL Server ?",
    "faq_sqlcal_a": "Non. La licence par cœur n'exige aucune licence d'accès client : autant d'utilisateurs ou d'applications que vous le souhaitez peuvent utiliser la base, sans coût par poste.",
    "faq_sqlos_q": "Sur quels systèmes d'exploitation puis-je l'installer ?",
    "faq_sqlos_a": "Windows Server 2016 et versions ultérieures, y compris les installations Server Core, ou Windows 10 version 1607 et ultérieure. Nécessite .NET Framework 4.7.2.",
    "faq_sqlmin_q": "Y a-t-il un minimum de cœurs à licencier ?",
    "faq_sqlmin_a": "Oui : Microsoft impose au moins quatre cœurs licenciés pour chaque serveur physique ou machine virtuelle exécutant SQL Server.",
})

T["de"] = dict(T["it"], **{
    "ws_eyebrow": "Dauerlizenz · {cores} Kerne",
    "ws_name": "Windows Server {anno} Standard",
    "ws_seo": "Windows Server {anno} Standard {cores} Kerne — Eurolicenze",
    "ws_desc": ("Windows Server {anno} Standard 64-Bit mit Dauerlizenz für {cores} Kerne. "
                "{consegna} Clientzugriffslizenzen sind nicht enthalten: Sie kaufst du separat für "
                "jeden Benutzer oder jedes Gerät, das den Server nutzt."),
    "ws_feat_title": "Was diese Lizenz abdeckt",
    "ws_f1": ("Kernlizenzierung", "Deckt {cores} Kerne ab",
              "Die Lizenz deckt einen Server mit maximal {cores} physischen Kernen ab. Hat dein Server mehr, brauchst du zusätzliche Lizenzen."),
    "ws_f2": ("Wichtig zu wissen", "CALs sind nicht enthalten",
              "Windows Server benötigt eine CAL für jeden Benutzer oder jedes Gerät mit Serverzugriff. Sie ist in dieser Lizenz nicht enthalten und wird separat gekauft."),
    "ws_f3": ("Virtualisierung", "Bis zu 2 Serverumgebungen",
              "Die Standard Edition gewährt zwei Betriebssystemumgebungen oder Windows-Container mit Hyper-V-Isolierung, sobald alle physischen Kerne lizenziert sind."),
    "ws_f4": ("Rollen", "Active Directory, Hyper-V, Datei und Web",
              "Enthält die Rollen von Windows Server Standard: Active Directory-Domänendienste, Hyper-V, Datei- und Druckserver sowie IIS."),
    "ws_f5_dvd": ("Medium", "OEM-DVD in englischer Sprache",
                  "Du erhältst das physische OEM-Medium. Die Oberfläche des Betriebssystems ist englisch — prüfe das, falls du eine andere Sprache brauchst."),
    "ws_f5_esd": ("Lieferung", "Digitale Lizenz per E-Mail",
                  "Key und Anleitung kommen nach der Zahlungsbestätigung per E-Mail: kein Warten auf den Versand."),
    "ws_f6_2025": ("Neu in 2025", "Updates ohne Neustart",
                   "Windows Server 2025 bringt Hotpatching über Azure Arc, was geplante Neustarts reduziert, dazu ein gehärtetes Active Directory und native NVMe-Unterstützung."),
    "sql_eyebrow": "Dauerlizenz · {cores} Kerne",
    "sql_name": "SQL Server 2022 {ed}",
    "sql_seo": "SQL Server 2022 {ed} {cores} Kerne — Eurolicenze",
    "sql_desc": ("SQL Server 2022 {ed} mit Dauerlizenz pro Kern ({cores} Kerne). "
                 "Beim Kernmodell sind keine CALs nötig: beliebig viele Benutzer können auf die Datenbank zugreifen. "
                 "Physisches Medium enthalten, englische Oberfläche."),
    "sql_feat_title": "Was die Lizenz umfasst",
    "sql_f1": ("Lizenzmodell", "Keine CALs nötig",
               "Die Kernlizenzierung benötigt keine Clientzugriffslizenzen: beliebig viele Benutzer oder Anwendungen können die Datenbank ohne Kosten pro Arbeitsplatz nutzen."),
    "sql_f2": ("Kapazität", "Lizenz für {cores} Kerne",
               "Deckt {cores} Kerne ab. Microsoft verlangt mindestens vier lizenzierte Kerne pro Server oder virtueller Maschine."),
    "sql_f3_std": ("Editionsgrenzen", "Bis zu 24 Kerne",
                   "Die Standard Edition nutzt höchstens den kleineren Wert aus 4 Sockeln und 24 Kernen: diese 16-Kern-Lizenz liegt deutlich darunter."),
    "sql_f3_ent": ("Editionsgrenzen", "Keine Kernbegrenzung",
                   "Die Enterprise Edition hat bei Kernlizenzierung keine Kernbegrenzung und schaltet die erweiterten Funktionen für Hochverfügbarkeit und Analyse frei."),
    "sql_f4": ("Kompatibilität", "Windows Server 2016 oder neuer",
               "Installierbar auf Windows Server 2016 und neuer, auch als Server Core. Erfordert .NET Framework 4.7.2."),
    "consegna_dvd": "Du erhältst die originale OEM-DVD mit kostenlosem Versand; die Oberfläche ist englisch.",
    "consegna_esd": "Key und Anleitung kommen nach der Zahlungsbestätigung per E-Mail.",
    "spec_cpu": "Prozessor", "spec_ram": "Arbeitsspeicher", "spec_disk": "Speicherplatz", "spec_net": "Netzwerk",
    "ws_disk": "Mindestens 32 GB frei auf der Systempartition. Server mit mehr als 16 GB RAM brauchen zusätzlichen Platz für Auslagerung und Dumpdateien.",
    "ws_net": "Ethernet-Adapter mit mindestens 1 Gbit/s Durchsatz, konform zur PCI-Express-Spezifikation.",
    "sql_cpu": "x64-Prozessor ab 1,4 GHz, 2,0 GHz oder schneller empfohlen. Die Installation wird nur auf x64-Prozessoren unterstützt.",
    "sql_ram": "Mindestens 1 GB RAM, 4 GB oder mehr empfohlen und mit wachsender Datenbank zu erhöhen.",
    "sql_disk": "Mindestens 6 GB frei. Eine vollständige Installation aller Funktionen benötigt rund 8 GB.",
    "sql_os": "Betriebssystem",
    "sql_os_body": "Windows Server 2016 oder neuer, oder Windows 10 Version 1607 oder neuer. Erfordert .NET Framework 4.7.2.",
    "specs_note": "Richtwerte aus der Microsoft-Dokumentation. Prüfe vor der Installation immer die aktuellen Anforderungen.",
    "steps_title": "Bestellung, Lieferung und Aktivierung",
    "step1": ("Bestellung abschließen", "Zahle mit einer der Methoden im Checkout: Karte, PayPal oder digitale Wallets."),
    "step2_dvd": ("Medium erhalten", "Wir versenden die originale DVD kostenlos: Übergabe an den Versanddienst innerhalb von 24 Werktagsstunden nach Zahlung."),
    "step2_esd": ("Key erhalten", "Product Key und Anleitung kommen nach der Zahlungsbestätigung per E-Mail."),
    "step3": ("Installieren und aktivieren", "Installiere das System und aktiviere die Lizenz über die offiziellen Microsoft-Kanäle, gemäß der erhaltenen Anleitung."),
    "faq_cal_q": "Sind CALs im Preis enthalten?",
    "faq_cal_a": "Nein. Windows Server benötigt eine Clientzugriffslizenz für jeden Benutzer oder jedes Gerät, das den Server nutzt, und sie ist hier nicht enthalten. CALs werden separat gekauft und gelten für die gesamte Umgebung, nicht für einen einzelnen Server.",
    "faq_core_q": "Was, wenn mein Server mehr als {cores} Kerne hat?",
    "faq_core_a": "Die Lizenz deckt {cores} Kerne ab. Hat der Server mehr, müssen alle physischen Kerne lizenziert werden — dafür brauchst du zusätzliche Lizenzen. Microsoft verlangt mindestens {cores} lizenzierte Kerne pro Server.",
    "faq_virt_q": "Wie viele virtuelle Maschinen darf ich betreiben?",
    "faq_virt_a": "Die Standard Edition gewährt zwei Betriebssystemumgebungen (oder Windows-Container mit Hyper-V-Isolierung), sobald alle physischen Kerne des Servers lizenziert sind. Darüber hinaus sind zusätzliche Lizenzen nötig.",
    "faq_lang_q": "In welcher Sprache ist das Betriebssystem?",
    "faq_lang_a": "Das OEM-Medium ist englisch: Oberfläche und Installation sind auf Englisch. Prüfe das vor der Bestellung, falls du eine andere Sprache brauchst.",
    "faq_media_q": "Was erhalte ich genau?",
    "faq_media_a": "Du erhältst den Lizenzschlüssel und die Anleitung per E-Mail nach der Zahlungsbestätigung. Die Lieferung ist rein digital: es wird kein physisches Medium versendet.",
    "faq_sqlcal_q": "Brauche ich CALs für SQL Server?",
    "faq_sqlcal_a": "Nein. Die Kernlizenzierung erfordert keine Clientzugriffslizenzen: beliebig viele Benutzer oder Anwendungen können die Datenbank nutzen, ohne Kosten pro Arbeitsplatz.",
    "faq_sqlos_q": "Auf welchen Betriebssystemen kann ich installieren?",
    "faq_sqlos_a": "Windows Server 2016 und neuer, einschließlich Server-Core-Installationen, oder Windows 10 Version 1607 und neuer. Erfordert .NET Framework 4.7.2.",
    "faq_sqlmin_q": "Gibt es eine Mindestanzahl zu lizenzierender Kerne?",
    "faq_sqlmin_a": "Ja: Microsoft verlangt mindestens vier lizenzierte Kerne für jeden physischen Server oder jede virtuelle Maschine mit SQL Server.",
})

T["es"] = dict(T["it"], **{
    "ws_eyebrow": "Licencia perpetua · {cores} núcleos",
    "ws_name": "Windows Server {anno} Standard",
    "ws_seo": "Windows Server {anno} Standard {cores} núcleos — Eurolicenze",
    "ws_desc": ("Windows Server {anno} Standard de 64 bits con licencia perpetua para {cores} núcleos. "
                "{consegna} Las CAL de acceso de cliente no están incluidas: se compran aparte para "
                "cada usuario o dispositivo que vaya a usar el servidor."),
    "ws_feat_title": "Qué cubre esta licencia",
    "ws_f1": ("Licencia por núcleo", "Cubre {cores} núcleos",
              "La licencia cubre un servidor con un máximo de {cores} núcleos físicos. Si el tuyo tiene más, necesitas licencias adicionales."),
    "ws_f2": ("Conviene saberlo", "Las CAL no están incluidas",
              "Windows Server exige una CAL por cada usuario o dispositivo que accede al servidor. No está incluida en esta licencia y se compra por separado."),
    "ws_f3": ("Virtualización", "Hasta 2 entornos de servidor",
              "La edición Standard da derecho a dos entornos de sistema operativo, o contenedores Windows con aislamiento Hyper-V, cuando todos los núcleos físicos están licenciados."),
    "ws_f4": ("Roles", "Active Directory, Hyper-V, archivos y web",
              "Incluye los roles de Windows Server Standard: servicios de dominio de Active Directory, Hyper-V, servidor de archivos e impresión, e IIS."),
    "ws_f5_dvd": ("Soporte", "DVD OEM en inglés",
                  "Recibes el soporte físico OEM. La interfaz del sistema está en inglés: tenlo en cuenta si necesitas otro idioma."),
    "ws_f5_esd": ("Entrega", "Licencia digital por email",
                  "Clave e instrucciones llegan por email tras confirmar el pago: nada que esperar por correo."),
    "ws_f6_2025": ("Novedades 2025", "Actualizaciones sin reiniciar",
                   "Windows Server 2025 incorpora hotpatching mediante Azure Arc, que reduce los reinicios planificados, junto a un Active Directory reforzado y soporte NVMe nativo."),
    "sql_eyebrow": "Licencia perpetua · {cores} núcleos",
    "sql_name": "SQL Server 2022 {ed}",
    "sql_seo": "SQL Server 2022 {ed} {cores} núcleos — Eurolicenze",
    "sql_desc": ("SQL Server 2022 {ed} con licencia perpetua por núcleo ({cores} núcleos). "
                 "Con el modelo por núcleo no hacen falta CAL: el número de usuarios que acceden a la base de datos es ilimitado. "
                 "Soporte físico incluido, interfaz en inglés."),
    "sql_feat_title": "Qué incluye la licencia",
    "sql_f1": ("Modelo de licencia", "Sin CAL que comprar",
               "La licencia por núcleo no requiere licencias de acceso de cliente: cualquier número de usuarios o aplicaciones puede usar la base de datos sin coste por puesto."),
    "sql_f2": ("Capacidad", "Licencia para {cores} núcleos",
               "Cubre {cores} núcleos. Microsoft exige un mínimo de cuatro núcleos licenciados por servidor o máquina virtual."),
    "sql_f3_std": ("Límites de edición", "Hasta 24 núcleos",
                   "La edición Standard usa como máximo el menor entre 4 sockets y 24 núcleos: esta licencia de 16 núcleos queda holgadamente dentro del límite."),
    "sql_f3_ent": ("Límites de edición", "Sin límite de núcleos",
                   "La edición Enterprise no tiene límite de núcleos con la licencia por núcleo, y desbloquea las funciones avanzadas de alta disponibilidad y análisis."),
    "sql_f4": ("Compatibilidad", "Windows Server 2016 o posterior",
               "Se instala en Windows Server 2016 y versiones posteriores, incluido Server Core. Requiere .NET Framework 4.7.2."),
    "consegna_dvd": "Recibes el DVD OEM original con envío gratuito; la interfaz está en inglés.",
    "consegna_esd": "Clave e instrucciones llegan por email tras confirmar el pago.",
    "spec_cpu": "Procesador", "spec_ram": "Memoria", "spec_disk": "Espacio en disco", "spec_net": "Red",
    "ws_disk": "Al menos 32 GB libres en la partición del sistema. Los servidores con más de 16 GB de RAM necesitan espacio adicional para paginación y volcados.",
    "ws_net": "Adaptador Ethernet de al menos 1 Gbit/s, conforme a las especificaciones PCI Express.",
    "sql_cpu": "Procesador x64 desde 1,4 GHz, 2,0 GHz o superior recomendado. La instalación solo se admite en procesadores x64.",
    "sql_ram": "Al menos 1 GB de RAM, 4 GB o más recomendados y a aumentar según crezca la base de datos.",
    "sql_disk": "Al menos 6 GB libres. La instalación completa de todas las funciones requiere unos 8 GB.",
    "sql_os": "Sistema operativo",
    "sql_os_body": "Windows Server 2016 o posterior, o Windows 10 versión 1607 o posterior. Requiere .NET Framework 4.7.2.",
    "specs_note": "Valores orientativos de la documentación de Microsoft. Comprueba siempre los requisitos actualizados antes de instalar.",
    "steps_title": "Pedido, entrega y activación",
    "step1": ("Completa el pedido", "Paga con cualquiera de los métodos disponibles en el checkout: tarjeta, PayPal o carteras digitales."),
    "step2_dvd": ("Recibe el soporte", "Enviamos el DVD original con envío gratuito: entrega al transportista en 24 horas laborables tras el pago."),
    "step2_esd": ("Recibe la clave", "Clave de producto e instrucciones llegan por email tras confirmar el pago."),
    "step3": ("Instala y activa", "Instala el sistema y activa la licencia por los canales oficiales de Microsoft, siguiendo las instrucciones recibidas."),
    "faq_cal_q": "¿Las CAL están incluidas en el precio?",
    "faq_cal_a": "No. Windows Server requiere una licencia de acceso de cliente por cada usuario o dispositivo que use el servidor, y no está incluida aquí. Las CAL se compran aparte y cubren todo el entorno, no un servidor concreto.",
    "faq_core_q": "¿Qué pasa si mi servidor tiene más de {cores} núcleos?",
    "faq_core_a": "La licencia cubre {cores} núcleos. Si el servidor tiene más, hay que licenciar todos los núcleos físicos comprando licencias adicionales. Microsoft exige un mínimo de {cores} núcleos licenciados por servidor.",
    "faq_virt_q": "¿Cuántas máquinas virtuales puedo ejecutar?",
    "faq_virt_a": "La edición Standard da derecho a dos entornos de sistema operativo (o contenedores Windows con aislamiento Hyper-V) cuando todos los núcleos físicos del servidor están licenciados. Por encima de eso hacen falta licencias adicionales.",
    "faq_lang_q": "¿En qué idioma está el sistema operativo?",
    "faq_lang_a": "El soporte OEM está en inglés: la interfaz y la instalación son en inglés. Compruébalo antes de comprar si necesitas otro idioma.",
    "faq_media_q": "¿Qué recibo exactamente?",
    "faq_media_a": "Recibes la clave de licencia y las instrucciones por email tras confirmar el pago. La entrega es solo digital: no se envía ningún soporte físico.",
    "faq_sqlcal_q": "¿Hacen falta CAL para SQL Server?",
    "faq_sqlcal_a": "No. La licencia por núcleo no requiere licencias de acceso de cliente: pueden usar la base de datos cuantos usuarios o aplicaciones quieras, sin coste por puesto.",
    "faq_sqlos_q": "¿En qué sistemas operativos se instala?",
    "faq_sqlos_a": "En Windows Server 2016 y versiones posteriores, incluidas las instalaciones Server Core, o en Windows 10 versión 1607 y posteriores. Requiere .NET Framework 4.7.2.",
    "faq_sqlmin_q": "¿Hay un mínimo de núcleos a licenciar?",
    "faq_sqlmin_a": "Sí: Microsoft exige al menos cuatro núcleos licenciados por cada servidor físico o máquina virtual con SQL Server.",
})

T["pt"] = dict(T["it"], **{
    "ws_eyebrow": "Licença perpétua · {cores} núcleos",
    "ws_name": "Windows Server {anno} Standard",
    "ws_seo": "Windows Server {anno} Standard {cores} núcleos — Eurolicenze",
    "ws_desc": ("Windows Server {anno} Standard de 64 bits com licença perpétua para {cores} núcleos. "
                "{consegna} As CAL de acesso de cliente não estão incluídas: compram-se em separado para "
                "cada utilizador ou dispositivo que vá usar o servidor."),
    "ws_feat_title": "O que esta licença cobre",
    "ws_f1": ("Licença por núcleo", "Cobre {cores} núcleos",
              "A licença cobre um servidor com um máximo de {cores} núcleos físicos. Se o teu servidor tiver mais, precisas de licenças adicionais para os cobrir todos."),
    "ws_f2": ("Bom saber", "As CAL não estão incluídas",
              "O Windows Server exige uma CAL para cada utilizador ou dispositivo que acede ao servidor. Não estão incluídas nesta licença e compram-se em separado."),
    "ws_f3": ("Virtualização", "Até 2 ambientes de servidor",
              "A edição Standard dá direito a dois ambientes de sistema operativo, ou contentores Windows com isolamento Hyper-V, quando todos os núcleos físicos estão licenciados."),
    "ws_f4": ("Funções", "Active Directory, Hyper-V, ficheiros e web",
              "Inclui as funções do Windows Server Standard: serviços de domínio Active Directory, Hyper-V, servidor de ficheiros e impressão, e IIS."),
    "ws_f5_dvd": ("Suporte", "DVD OEM em inglês",
                  "Recebes o suporte físico OEM. A interface do sistema operativo está em inglês: tem isso em conta se precisares de português."),
    "ws_f5_esd": ("Entrega", "Licença digital por email",
                  "Código e instruções chegam por email após a confirmação do pagamento: nada para esperar pelo correio."),
    "ws_f6_2025": ("Novidades 2025", "Atualizações sem reiniciar",
                   "O Windows Server 2025 introduz o hotpatching através do Azure Arc, que reduz os reinícios planeados, além de um Active Directory reforçado e suporte NVMe nativo."),
    "sql_eyebrow": "Licença perpétua · {cores} núcleos",
    "sql_name": "SQL Server 2022 {ed}",
    "sql_seo": "SQL Server 2022 {ed} {cores} núcleos — Eurolicenze",
    "sql_desc": ("SQL Server 2022 {ed} com licença perpétua por núcleo ({cores} núcleos). "
                 "Com o modelo por núcleo não são necessárias CAL: o número de utilizadores que acedem à base de dados é ilimitado. "
                 "Suporte físico incluído, interface em inglês."),
    "sql_feat_title": "O que a licença inclui",
    "sql_f1": ("Modelo de licenciamento", "Sem CAL para comprar",
               "A licença por núcleo não exige licenças de acesso de cliente: qualquer número de utilizadores ou aplicações pode usar a base de dados sem custo por posto."),
    "sql_f2": ("Capacidade", "Licença para {cores} núcleos",
               "Cobre {cores} núcleos. A Microsoft exige um mínimo de quatro núcleos licenciados por servidor ou máquina virtual."),
    "sql_f3_std": ("Limites de edição", "Até 24 núcleos",
                   "A edição Standard usa no máximo o menor entre 4 sockets e 24 núcleos: esta licença de 16 núcleos fica bem dentro do limite."),
    "sql_f3_ent": ("Limites de edição", "Sem limite de núcleos",
                   "A edição Enterprise não tem limite de núcleos com a licença por núcleo, e desbloqueia as funções avançadas de alta disponibilidade e análise."),
    "sql_f4": ("Compatibilidade", "Windows Server 2016 ou posterior",
               "Instala-se em Windows Server 2016 e versões posteriores, incluindo Server Core. Requer .NET Framework 4.7.2."),
    "consegna_dvd": "Recebes o DVD OEM original com envio gratuito; a interface está em inglês.",
    "consegna_esd": "Código e instruções chegam por email após a confirmação do pagamento.",
    "spec_cpu": "Processador", "spec_ram": "Memória", "spec_disk": "Espaço em disco", "spec_net": "Rede",
    "ws_disk": "Pelo menos 32 GB livres na partição do sistema. Servidores com mais de 16 GB de RAM precisam de espaço adicional para paginação e ficheiros de despejo.",
    "ws_net": "Adaptador Ethernet com um débito de pelo menos 1 Gbit/s, conforme as especificações PCI Express.",
    "sql_cpu": "Processador x64 a partir de 1,4 GHz, recomenda-se 2,0 GHz ou superior. A instalação só é suportada em processadores x64.",
    "sql_ram": "Pelo menos 1 GB de RAM, recomendando-se 4 GB ou mais e aumentando com o crescimento da base de dados.",
    "sql_disk": "Pelo menos 6 GB livres. A instalação completa de todas as funcionalidades requer cerca de 8 GB.",
    "sql_os": "Sistema operativo",
    "sql_os_body": "Windows Server 2016 ou posterior, ou Windows 10 versão 1607 ou posterior. Requer .NET Framework 4.7.2.",
    "specs_note": "Valores indicativos da documentação da Microsoft. Verifica sempre os requisitos atualizados antes de instalar.",
    "steps_title": "Encomenda, entrega e ativação",
    "step1": ("Conclui a encomenda", "Paga com um dos métodos disponíveis no checkout: cartão, PayPal ou carteiras digitais."),
    "step2_dvd": ("Recebe o suporte", "Enviamos o DVD original com envio gratuito: entregue à transportadora até 24 horas úteis após o pagamento."),
    "step2_esd": ("Recebe o código", "O código do produto e as instruções chegam por email após a confirmação do pagamento."),
    "step3": ("Instala e ativa", "Instala o sistema e ativa a licença através dos canais oficiais da Microsoft, seguindo as instruções recebidas."),
    "faq_cal_q": "As CAL estão incluídas no preço?",
    "faq_cal_a": "Não. O Windows Server exige uma licença de acesso de cliente (CAL) para cada utilizador ou dispositivo que usa o servidor, e não está incluída nesta licença. As CAL compram-se em separado e valem para todo o ambiente, não para um único servidor.",
    "faq_core_q": "O que acontece se o meu servidor tiver mais de {cores} núcleos?",
    "faq_core_a": "A licença cobre {cores} núcleos. Se o servidor tiver mais, tens de licenciar todos os núcleos físicos, comprando licenças adicionais. A Microsoft exige um mínimo de {cores} núcleos licenciados por servidor.",
    "faq_virt_q": "Quantas máquinas virtuais posso executar?",
    "faq_virt_a": "A edição Standard dá direito a dois ambientes de sistema operativo (ou contentores Windows com isolamento Hyper-V) quando todos os núcleos físicos do servidor estão licenciados. Além deste limite são necessárias licenças adicionais.",
    "faq_lang_q": "Em que idioma está o sistema operativo?",
    "faq_lang_a": "O suporte OEM está em inglês: a interface e a instalação são em inglês. Verifica isto antes de comprar se precisares de português.",
    "faq_media_q": "O que recebo exatamente?",
    "faq_media_a": "Recebes o código de licença e as instruções por email após a confirmação do pagamento. A entrega é apenas digital: não é enviado nenhum suporte físico.",
    "faq_sqlcal_q": "É preciso CAL para o SQL Server?",
    "faq_sqlcal_a": "Não. Com a licença por núcleo não são exigidas licenças de acesso de cliente: podem usar a base de dados quantos utilizadores ou aplicações quiseres, sem custo por posto.",
    "faq_sqlos_q": "Em que sistemas operativos se instala?",
    "faq_sqlos_a": "Em Windows Server 2016 e versões posteriores, incluindo instalações Server Core, ou em Windows 10 versão 1607 e posteriores. Requer .NET Framework 4.7.2.",
    "faq_sqlmin_q": "Há um mínimo de núcleos a licenciar?",
    "faq_sqlmin_a": "Sim: a Microsoft exige pelo menos quatro núcleos licenciados para cada servidor físico ou máquina virtual que execute o SQL Server.",
})

# Le chiavi non elencate qui sotto ereditano l'inglese passando da nl_text():
# cosi' la traduzione olandese vive in scripts/nl_translations.py come per gli
# altri moduli, invece di restare inglese silenziosamente.
T["nl"] = dict({k: nl_text(v) for k, v in T["en"].items()}, **{
    "ws_eyebrow": "Permanente licentie · {cores} cores",
    "ws_name": "Windows Server {anno} Standard",
    "ws_seo": "Windows Server {anno} Standard {cores} cores — Eurolicenze",
    "ws_desc": ("Windows Server {anno} Standard 64-bit met een permanente licentie voor {cores} cores. "
                "{consegna} Client Access Licenses zijn niet inbegrepen: die koopt u apart voor "
                "elke gebruiker of elk apparaat dat de server gebruikt."),
    "ws_feat_title": "Wat deze licentie dekt",
    "ws_f1": ("Core-licenties", "Dekt {cores} cores",
              "De licentie dekt een server met maximaal {cores} fysieke cores. Heeft uw server er meer, dan hebt u extra licenties nodig om ze allemaal te dekken."),
    "ws_f2": ("Goed om te weten", "CAL’s zijn niet inbegrepen",
              "Windows Server vereist een CAL voor elke gebruiker of elk apparaat dat toegang heeft tot de server. Die zitten niet in deze licentie en worden apart gekocht."),
    "ws_f3": ("Virtualisatie", "Maximaal 2 serveromgevingen",
              "De Standard-editie geeft recht op twee besturingssysteemomgevingen, of Windows-containers met Hyper-V-isolatie, zodra elke fysieke core is gelicentieerd."),
    "ws_f4": ("Rollen", "Active Directory, Hyper-V, bestanden en web",
              "Bevat de rollen van Windows Server Standard: Active Directory Domain Services, Hyper-V, bestands- en printserver, en IIS."),
    "ws_f5_dvd": ("Media", "OEM-dvd in het Engels",
                  "U ontvangt de fysieke OEM-media. De interface van het besturingssysteem is Engels — controleer dit als u een andere taal nodig hebt."),
    "ws_f5_esd": ("Levering", "Digitale licentie per e-mail",
                  "Sleutel en instructies komen per e-mail na bevestiging van de betaling: niets om per post af te wachten."),
    "ws_f6_2025": ("Nieuw in 2025", "Updates zonder herstart",
                   "Windows Server 2025 voegt hotpatching via Azure Arc toe, wat geplande herstarts vermindert, plus een versterkte Active Directory en native NVMe-ondersteuning."),
    "sql_eyebrow": "Permanente licentie · {cores} cores",
    "sql_name": "SQL Server 2022 {ed}",
    "sql_seo": "SQL Server 2022 {ed} {cores} cores — Eurolicenze",
    "sql_desc": ("SQL Server 2022 {ed} met een permanente per-core-licentie ({cores} cores). "
                 "Per-core-licenties vereisen geen CAL’s: elk aantal gebruikers kan de database gebruiken. "
                 "Fysieke media inbegrepen, Engelse interface."),
    "sql_feat_title": "Wat de licentie omvat",
    "sql_f1": ("Licentiemodel", "Geen CAL’s te kopen",
               "Per-core-licenties vereisen geen client access licenses: elk aantal gebruikers of toepassingen kan de database gebruiken zonder extra kosten per werkplek."),
    "sql_f2": ("Capaciteit", "Licentie voor {cores} cores",
               "Dekt {cores} cores. Microsoft vereist minimaal vier gelicentieerde cores per server of virtuele machine."),
    "sql_f3_std": ("Editielimieten", "Maximaal 24 cores",
                   "De Standard-editie gebruikt hoogstens het kleinste van 4 sockets of 24 cores: deze 16-core-licentie valt ruim binnen die limiet."),
    "sql_f3_ent": ("Editielimieten", "Geen core-limiet",
                   "De Enterprise-editie heeft geen core-limiet bij per-core-licenties en ontgrendelt de geavanceerde high-availability- en analyticsfuncties."),
    "consegna_dvd": "U ontvangt de originele OEM-dvd met gratis verzending; de interface is in het Engels.",
    "consegna_esd": "Code en instructies komen per e-mail na bevestiging van de betaling.",
    "spec_cpu": "Processor", "spec_ram": "Geheugen", "spec_disk": "Schijfruimte", "spec_net": "Netwerk",
    "steps_title": "Bestelling, levering en activering",
    "step1": ("Rond uw bestelling af", "Betaal met een van de methoden in de checkout: kaart, PayPal of digitale wallets."),
    "step2_dvd": ("Ontvang de media", "Wij verzenden de originele dvd met gratis verzending: overdracht aan de koerier binnen 24 werkuren na betaling."),
    "step2_esd": ("Ontvang de sleutel", "Productsleutel en instructies komen per e-mail na bevestiging van de betaling."),
    "step3": ("Installeren en activeren", "Installeer het systeem en activeer de licentie via de officiële Microsoft-kanalen, volgens de ontvangen instructies."),
    "faq_cal_q": "Zijn CAL’s bij de prijs inbegrepen?",
    "faq_cal_a": "Nee. Windows Server vereist een Client Access License voor elke gebruiker of elk apparaat dat de server gebruikt, en die zit niet in deze licentie. CAL’s koopt u apart; ze dekken uw hele omgeving, niet één server.",
    "faq_core_q": "Wat als mijn server meer dan {cores} cores heeft?",
    "faq_core_a": "De licentie dekt {cores} cores. Heeft uw server er meer, dan moet elke fysieke core worden gelicentieerd, dus koopt u extra licenties. Microsoft vereist minimaal {cores} gelicentieerde cores per server.",
    "faq_virt_q": "Hoeveel virtuele machines kan ik draaien?",
    "faq_virt_a": "De Standard-editie geeft recht op twee besturingssysteemomgevingen (of Windows-containers met Hyper-V-isolatie) zodra elke fysieke core van de server is gelicentieerd. Daarboven hebt u extra licenties nodig.",
    "faq_lang_q": "In welke taal is het besturingssysteem?",
    "faq_lang_a": "De OEM-media zijn in het Engels: interface en installatie zijn Engels. Controleer dit vóór aankoop als u een andere taal nodig hebt.",
    "faq_media_q": "Wat ontvang ik precies?",
    "faq_media_a": "U ontvangt de licentiecode en instructies per e-mail na bevestiging van de betaling. Levering is alleen digitaal: er wordt geen fysieke media meegestuurd.",
    "faq_sqlcal_q": "Heb ik CAL’s nodig voor SQL Server?",
    "faq_sqlcal_a": "Nee. Per-core-licenties vereisen geen client access licenses: zoveel gebruikers of toepassingen als u wilt kunnen de database gebruiken, zonder kosten per werkplek.",
    "faq_sqlos_q": "Op welke besturingssystemen kan ik het installeren?",
    "faq_sqlos_a": "Windows Server 2016 en later, inclusief Server Core-installaties, of Windows 10 versie 1607 en later. Vereist .NET Framework 4.7.2.",
    "faq_sqlmin_q": "Is er een minimumaantal cores om te licentiëren?",
    "faq_sqlmin_a": "Ja: Microsoft vereist minstens vier gelicentieerde cores voor elke fysieke server of virtuele machine die SQL Server uitvoert.",
    "ws_disk": "Minstens 32 GB vrij op de systeempartitie. Servers met meer dan 16 GB RAM hebben extra ruimte nodig voor paging- en dumpbestanden.",
    "ws_net": "Ethernet-adapter met minstens 1 Gbps, conform de PCI Express-specificatie.",
    "sql_cpu": "x64-processor van 1,4 GHz of sneller, 2,0 GHz of hoger aanbevolen. Installatie wordt alleen ondersteund op x64-processors.",
    "sql_ram": "Minstens 1 GB RAM, 4 GB of meer aanbevolen en oplopend naarmate de database groeit.",
    "sql_disk": "Minstens 6 GB vrij. Een volledige installatie van alle functies vraagt ongeveer 8 GB.",
    "sql_os": "Besturingssysteem",
    "sql_os_body": "Windows Server 2016 of later, of Windows 10 versie 1607 of later. Vereist .NET Framework 4.7.2.",
    "specs_note": "Indicatieve cijfers uit de Microsoft-documentatie. Controleer altijd de actuele eisen vóór installatie.",
})

from lang_backfill import backfill_lang
backfill_lang(WS_RAM, target="nl", source="en", translate=nl_text)
backfill_lang(WS_CPU, target="nl", source="en", translate=nl_text)


def _ws(slug, cfg):
    """Compone la scheda di un Windows Server nelle 5 lingue."""
    anno, cores, media = cfg["anno"], cfg["cores"], cfg["media"]
    dvd = media == "dvd"
    out = {k: {} for k in ("name", "seo_title", "desc", "eyebrow", "title_html",
                           "features_title", "pills", "features", "steps", "steps_title",
                           "specs", "specs_note", "faq")}
    for lg in LANGS:
        t = T[lg]
        f = dict(anno=anno, cores=cores)
        out["name"][lg] = t["ws_name"].format(**f)
        out["seo_title"][lg] = t["ws_seo"].format(**f)
        out["eyebrow"][lg] = t["ws_eyebrow"].format(**f)
        out["title_html"][lg] = T["it"]["ws_title"].format(**f)
        out["desc"][lg] = t["ws_desc"].format(consegna=t["consegna_dvd" if dvd else "consegna_esd"], **f)
        out["features_title"][lg] = t["ws_feat_title"]

        pills = [(None, f"{cores} core" if lg == "it" else f"{cores} cores"), (None, "64-bit")]
        pills.append((None, t["ws_eyebrow"].format(**f).split(" · ")[0]))
        pills.append((None, "DVD OEM (EN)" if dvd else "ESD"))
        out["pills"][lg] = pills

        feats = [t["ws_f1"], t["ws_f2"], t["ws_f3"], t["ws_f4"],
                 t["ws_f5_dvd"] if dvd else t["ws_f5_esd"]]
        if anno == "2025":
            feats.append(t["ws_f6_2025"])
        out["features"][lg] = [("c4", "", lab, tit.format(**f), body.format(**f))
                               for lab, tit, body in feats]

        out["steps_title"][lg] = t["steps_title"]
        out["steps"][lg] = [t["step1"], t["step2_dvd"] if dvd else t["step2_esd"], t["step3"]]
        out["specs"][lg] = [
            (t["spec_cpu"], WS_CPU[anno][lg]),
            (t["spec_ram"], WS_RAM[anno][lg]),
            (t["spec_disk"], t["ws_disk"]),
            (t["spec_net"], t["ws_net"]),
        ]
        out["specs_note"][lg] = t["specs_note"]

        faq = [(t["faq_cal_q"], t["faq_cal_a"]),
               (t["faq_core_q"].format(**f), t["faq_core_a"].format(**f)),
               (t["faq_virt_q"], t["faq_virt_a"])]
        faq.append((t["faq_lang_q"], t["faq_lang_a"]) if dvd else (t["faq_media_q"], t["faq_media_a"]))
        out["faq"][lg] = faq
    return out


def _sql(slug, cfg):
    """Compone la scheda di un SQL Server nelle 5 lingue."""
    ed, cores = cfg["ed"], cfg["cores"]
    std = ed == "Standard"
    out = {k: {} for k in ("name", "seo_title", "desc", "eyebrow", "title_html",
                           "features_title", "pills", "features", "steps", "steps_title",
                           "specs", "specs_note", "faq")}
    for lg in LANGS:
        t = T[lg]
        f = dict(ed=ed, cores=cores)
        out["name"][lg] = t["sql_name"].format(**f)
        out["seo_title"][lg] = t["sql_seo"].format(**f)
        out["eyebrow"][lg] = t["sql_eyebrow"].format(**f)
        out["title_html"][lg] = T["it"]["sql_title"].format(**f)
        out["desc"][lg] = t["sql_desc"].format(**f)
        out["features_title"][lg] = t["sql_feat_title"]
        out["pills"][lg] = [(None, ed), (None, f"{cores} core" if lg == "it" else f"{cores} cores"),
                            (None, t["sql_eyebrow"].format(**f).split(" · ")[0]), (None, "DVD (EN)")]

        feats = [t["sql_f1"], t["sql_f2"], t["sql_f3_std"] if std else t["sql_f3_ent"], t["sql_f4"]]
        out["features"][lg] = [("c4", "", lab, tit.format(**f), body.format(**f))
                               for lab, tit, body in feats]

        out["steps_title"][lg] = t["steps_title"]
        out["steps"][lg] = [t["step1"], t["step2_dvd"], t["step3"]]
        out["specs"][lg] = [
            (t["spec_cpu"], t["sql_cpu"]),
            (t["spec_ram"], t["sql_ram"]),
            (t["spec_disk"], t["sql_disk"]),
            (t["sql_os"], t["sql_os_body"]),
        ]
        out["specs_note"][lg] = t["specs_note"]
        out["faq"][lg] = [
            (t["faq_sqlcal_q"], t["faq_sqlcal_a"]),
            (t["faq_sqlmin_q"], t["faq_sqlmin_a"]),
            (t["faq_sqlos_q"], t["faq_sqlos_a"]),
            (t["faq_lang_q"], t["faq_lang_a"]),
        ]
    return out


PRODUCTS = {slug: _ws(slug, cfg) for slug, cfg in WINDOWS_SERVER.items()}
PRODUCTS.update({slug: _sql(slug, cfg) for slug, cfg in SQL_SERVER.items()})


def get_server_content(slug):
    return PRODUCTS.get(slug)
