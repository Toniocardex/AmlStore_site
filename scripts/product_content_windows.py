#!/usr/bin/env python3
"""Rich product-page content for Windows client SKUs (excludes preserved windows-11-home)."""

from copy import deepcopy

from product_content_office import UI as OFFICE_UI

LANGS = ("it", "en", "fr", "de", "es")


def L(**kwargs):
    return {k: kwargs[k] for k in LANGS}


# Shared chrome based on Office UI, with Windows-specific steps/specs
UI = deepcopy(OFFICE_UI)
_WIN_OVERRIDES = {
    "it": {
        "apps_eyebrow": "In evidenza",
        "step2_body": "Ti inviamo la <strong>product key</strong> (e le istruzioni) via email, di solito entro pochi minuti dall'approvazione del pagamento. Per edizioni con supporto fisico (DVD/COA) segui anche quanto indicato in email.",
        "step3_body": "Attiva Windows con il codice ricevuto: Impostazioni → Sistema → Attivazione (o la procedura descritta nell'email). Usa i canali ufficiali Microsoft.",
        "spec_cpu_body": "Processore compatibile con i requisiti Microsoft della versione Windows indicata (per Windows 11 tipicamente CPU supportata nell'elenco ufficiale).",
        "spec_os_body": "Questa scheda riguarda la licenza del sistema operativo indicato. Verifica hardware e TPM/Secure Boot dove richiesto (es. Windows 11).",
        "spec_ram_body": "Windows 10: tipicamente almeno 2–4 GB. Windows 11: almeno 4 GB secondo i requisiti Microsoft aggiornati.",
        "spec_disk_body": "Spazio libero sufficiente per l'installazione/upgrade come da documentazione Microsoft (spesso decine di GB per un'installazione completa).",
    },
    "en": {
        "apps_eyebrow": "Highlights",
        "step2_body": "We email the <strong>product key</strong> (and instructions), usually within minutes after payment approval. For editions with physical media (DVD/COA), also follow the email details.",
        "step3_body": "Activate Windows with the received key: Settings → System → Activation (or the steps in the email). Use official Microsoft channels.",
        "spec_cpu_body": "A processor that meets Microsoft’s requirements for the indicated Windows version (for Windows 11, typically a CPU on Microsoft’s supported list).",
        "spec_os_body": "This page covers the indicated OS licence. Check hardware and TPM/Secure Boot where required (e.g. Windows 11).",
        "spec_ram_body": "Windows 10: typically at least 2–4 GB. Windows 11: at least 4 GB per current Microsoft requirements.",
        "spec_disk_body": "Enough free space for install/upgrade per Microsoft docs (often tens of GB for a full install).",
    },
    "fr": {
        "apps_eyebrow": "Points clés",
        "step2_body": "Nous envoyons la <strong>clé produit</strong> (et les instructions) par e-mail, en général quelques minutes après validation du paiement. Pour DVD/COA, suivez aussi l'e-mail.",
        "step3_body": "Activez Windows avec le code reçu : Paramètres → Système → Activation (ou la procédure de l'e-mail). Utilisez les canaux Microsoft officiels.",
        "spec_cpu_body": "Processeur conforme aux exigences Microsoft pour la version Windows indiquée (Windows 11 : CPU sur la liste prise en charge).",
        "spec_os_body": "Cette fiche concerne la licence du système indiqué. Vérifiez le matériel et TPM/Secure Boot si requis (ex. Windows 11).",
        "spec_ram_body": "Windows 10 : en général 2–4 Go. Windows 11 : au moins 4 Go selon Microsoft.",
        "spec_disk_body": "Espace libre suffisant pour l'installation selon la documentation Microsoft.",
    },
    "de": {
        "apps_eyebrow": "Highlights",
        "step2_body": "Wir senden den <strong>Product Key</strong> (und die Anleitung) per E-Mail, in der Regel wenige Minuten nach Zahlungsfreigabe. Bei DVD/COA zusätzlich die E-Mail beachten.",
        "step3_body": "Aktivieren Sie Windows mit dem erhaltenen Key: Einstellungen → System → Aktivierung (oder die Schritte in der E-Mail). Offizielle Microsoft-Kanäle nutzen.",
        "spec_cpu_body": "Prozessor gemäß Microsoft-Anforderungen der angegebenen Windows-Version (Windows 11: typisch CPU auf der Support-Liste).",
        "spec_os_body": "Diese Seite betrifft die genannte OS-Lizenz. Hardware sowie TPM/Secure Boot prüfen, wo erforderlich (z. B. Windows 11).",
        "spec_ram_body": "Windows 10: typisch mindestens 2–4 GB. Windows 11: mindestens 4 GB laut Microsoft.",
        "spec_disk_body": "Ausreichend freier Speicher für Installation laut Microsoft-Dokumentation.",
    },
    "es": {
        "apps_eyebrow": "Destacados",
        "step2_body": "Enviamos la <strong>clave de producto</strong> (e instrucciones) por email, normalmente en minutos tras aprobar el pago. Para DVD/COA sigue también el email.",
        "step3_body": "Activa Windows con la clave recibida: Configuración → Sistema → Activación (o los pasos del email). Usa canales oficiales Microsoft.",
        "spec_cpu_body": "Procesador compatible con los requisitos Microsoft de la versión Windows indicada (Windows 11: CPU en la lista admitida).",
        "spec_os_body": "Esta ficha cubre la licencia del sistema indicado. Comprueba hardware y TPM/Secure Boot si aplica (p. ej. Windows 11).",
        "spec_ram_body": "Windows 10: normalmente al menos 2–4 GB. Windows 11: al menos 4 GB según Microsoft.",
        "spec_disk_body": "Espacio libre suficiente para instalar según la documentación Microsoft.",
    },
}
for lg, ov in _WIN_OVERRIDES.items():
    UI[lg].update(ov)


def _pills_win11():
    return {lg: [(None, "Windows 11"), (None, "Licenza digitale"), (None, "Attivazione Microsoft")] for lg in LANGS}


def _pills_win10():
    return {lg: [(None, "Windows 10"), (None, "Licenza digitale"), (None, "32/64-bit")] for lg in LANGS}


PRODUCTS = {
    "windows-11-pro": {
        "apps": [],
        "title_html": L(
            it='Windows 11 <span>Pro</span>',
            en='Windows 11 <span>Pro</span>',
            fr='Windows 11 <span>Pro</span>',
            de='Windows 11 <span>Pro</span>',
            es='Windows 11 <span>Pro</span>',
        ),
        "eyebrow": L(
            it="Sistema operativo · licenza ESD",
            en="Operating system · ESD licence",
            fr="Système d'exploitation · licence ESD",
            de="Betriebssystem · ESD-Lizenz",
            es="Sistema operativo · licencia ESD",
        ),
        "desc": L(
            it="Windows 11 Pro: licenza digitale originale con funzioni professionali (es. BitLocker e Desktop remoto, secondo Microsoft). Codice via email dopo l'acquisto.",
            en="Windows 11 Pro: genuine digital licence with professional features (e.g. BitLocker and Remote Desktop, per Microsoft). Key by email after purchase.",
            fr="Windows 11 Pro : licence numérique originale avec fonctions pro (ex. BitLocker et Bureau à distance, selon Microsoft). Code par e-mail.",
            de="Windows 11 Pro: originale digitale Lizenz mit Pro-Funktionen (z. B. BitLocker und Remotedesktop laut Microsoft). Key per E-Mail.",
            es="Windows 11 Pro: licencia digital original con funciones profesionales (p. ej. BitLocker y Escritorio remoto según Microsoft). Clave por email.",
        ),
        "pills": {
            "it": [(None, "Windows 11 Pro"), (None, "ESD"), (None, "BitLocker / RDP")],
            "en": [(None, "Windows 11 Pro"), (None, "ESD"), (None, "BitLocker / RDP")],
            "fr": [(None, "Windows 11 Pro"), (None, "ESD"), (None, "BitLocker / RDP")],
            "de": [(None, "Windows 11 Pro"), (None, "ESD"), (None, "BitLocker / RDP")],
            "es": [(None, "Windows 11 Pro"), (None, "ESD"), (None, "BitLocker / RDP")],
        },
        "features_title": L(
            it="Pro per lavoro e produttività",
            en="Pro for work and productivity",
            fr="Pro pour le travail",
            de="Pro für Arbeit und Produktivität",
            es="Pro para trabajo y productividad",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Edizione", "Windows 11 Pro", "Licenza Pro con strumenti pensati per professionisti e PMI, secondo le funzionalità Microsoft della edizione."),
                ("c4", "teal", None, "Sicurezza Pro", "Funzioni come BitLocker dove supportate dall'hardware e dall'edizione."),
                ("c4", "purple", "Remoto", "Desktop remoto", "Accesso remoto host secondo le capacità Pro di Windows 11."),
                ("c4", None, "Consegna", "Digitale ESD", "Product key via email dopo il pagamento."),
                ("c4", None, "Attivazione", "Ufficiale Microsoft", "Attivi da Impostazioni Windows con il codice ricevuto."),
                ("c4", "dark", "Requisiti", "Hardware Windows 11", "Verifica CPU, TPM 2.0 e Secure Boot prima dell'upgrade/installazione."),
            ],
            "en": [
                ("c8", "blue", "Edition", "Windows 11 Pro", "Pro licence with tools for professionals and SMBs, per Microsoft’s edition features."),
                ("c4", "teal", None, "Pro security", "Features such as BitLocker where hardware and edition support them."),
                ("c4", "purple", "Remote", "Remote Desktop", "Host remote access per Windows 11 Pro capabilities."),
                ("c4", None, "Delivery", "Digital ESD", "Product key by email after payment."),
                ("c4", None, "Activation", "Official Microsoft", "Activate from Windows Settings with your key."),
                ("c4", "dark", "Requirements", "Windows 11 hardware", "Check CPU, TPM 2.0 and Secure Boot before upgrade/install."),
            ],
            "fr": [
                ("c8", "blue", "Édition", "Windows 11 Pro", "Licence Pro avec outils pour pros et TPE, selon les fonctions Microsoft."),
                ("c4", "teal", None, "Sécurité Pro", "Fonctions comme BitLocker si le matériel et l'édition le permettent."),
                ("c4", "purple", "Distant", "Bureau à distance", "Accès distant hôte selon les capacités Pro."),
                ("c4", None, "Livraison", "ESD numérique", "Clé produit par e-mail après paiement."),
                ("c4", None, "Activation", "Microsoft officiel", "Activation depuis les Paramètres Windows."),
                ("c4", "dark", "Exigences", "Matériel Windows 11", "Vérifiez CPU, TPM 2.0 et Secure Boot."),
            ],
            "de": [
                ("c8", "blue", "Edition", "Windows 11 Pro", "Pro-Lizenz mit Tools für Profis und KMU gemäß Microsoft."),
                ("c4", "teal", None, "Pro-Sicherheit", "Funktionen wie BitLocker, sofern Hardware und Edition es zulassen."),
                ("c4", "purple", "Remote", "Remotedesktop", "Host-Zugriff gemäß Windows-11-Pro-Funktionen."),
                ("c4", None, "Lieferung", "Digitale ESD", "Product Key per E-Mail nach der Zahlung."),
                ("c4", None, "Aktivierung", "Offiziell Microsoft", "Aktivierung in den Windows-Einstellungen."),
                ("c4", "dark", "Anforderungen", "Windows-11-Hardware", "CPU, TPM 2.0 und Secure Boot prüfen."),
            ],
            "es": [
                ("c8", "blue", "Edición", "Windows 11 Pro", "Licencia Pro con herramientas para profesionales y pymes según Microsoft."),
                ("c4", "teal", None, "Seguridad Pro", "Funciones como BitLocker si el hardware y la edición lo permiten."),
                ("c4", "purple", "Remoto", "Escritorio remoto", "Acceso remoto host según capacidades Pro."),
                ("c4", None, "Entrega", "ESD digital", "Clave por email tras el pago."),
                ("c4", None, "Activación", "Microsoft oficial", "Activa desde Configuración de Windows."),
                ("c4", "dark", "Requisitos", "Hardware Windows 11", "Comprueba CPU, TPM 2.0 y Secure Boot."),
            ],
        },
        "apps_title": L(it="", en="", fr="", de="", es=""),
        "faq": {
            "it": [
                ("Differenza con Windows 11 Home?", "Pro aggiunge funzioni orientate al lavoro (es. BitLocker, Desktop remoto come host) rispetto a Home, secondo Microsoft."),
                ("È una licenza perpetua?", "Sì: licenza digitale ESD descritta in scheda, non un abbonamento."),
                ("Il PC è compatibile con Windows 11?", "Controlla i requisiti Microsoft (CPU, TPM 2.0, Secure Boot, RAM e storage) prima di installare."),
                ("Come si attiva?", "Impostazioni → Sistema → Attivazione con il codice ricevuto via email."),
                ("Serve reinstallare Windows?", "Dipende dal tuo caso (upgrade o installazione pulita). Segui le istruzioni email e la documentazione Microsoft."),
            ],
            "en": [
                ("Difference vs Windows 11 Home?", "Pro adds work-oriented features (e.g. BitLocker, Remote Desktop host) versus Home, per Microsoft."),
                ("Is it perpetual?", "Yes—digital ESD licence as described, not a subscription."),
                ("Is my PC Windows 11 ready?", "Check Microsoft’s requirements (CPU, TPM 2.0, Secure Boot, RAM and storage) first."),
                ("How do I activate?", "Settings → System → Activation with the emailed key."),
                ("Do I need to reinstall?", "Depends on upgrade vs clean install. Follow the email and Microsoft docs."),
            ],
            "fr": [
                ("Différence avec Home ?", "Pro ajoute des fonctions pro (ex. BitLocker, Bureau à distance hôte) par rapport à Home."),
                ("Licence perpétuelle ?", "Oui — licence ESD numérique, pas un abonnement."),
                ("PC compatible Windows 11 ?", "Vérifiez les exigences Microsoft (CPU, TPM 2.0, Secure Boot…)."),
                ("Activation ?", "Paramètres → Système → Activation avec le code reçu."),
                ("Faut-il réinstaller ?", "Selon upgrade ou installation propre ; suivez l'e-mail et Microsoft."),
            ],
            "de": [
                ("Unterschied zu Home?", "Pro ergänzt arbeitsbezogene Funktionen (z. B. BitLocker, Remotedesktop-Host) gegenüber Home."),
                ("Dauerlizenz?", "Ja — digitale ESD-Lizenz, kein Abo."),
                ("PC bereit für Windows 11?", "Microsoft-Anforderungen prüfen (CPU, TPM 2.0, Secure Boot…)."),
                ("Aktivierung?", "Einstellungen → System → Aktivierung mit dem E-Mail-Key."),
                ("Neuinstallation nötig?", "Abhängig von Upgrade oder Clean Install; E-Mail und Microsoft-Doku folgen."),
            ],
            "es": [
                ("¿Diferencia con Home?", "Pro añade funciones orientadas al trabajo (p. ej. BitLocker, Escritorio remoto host) frente a Home."),
                ("¿Es perpetua?", "Sí: licencia ESD digital, no una suscripción."),
                ("¿Mi PC es compatible con Windows 11?", "Comprueba los requisitos Microsoft (CPU, TPM 2.0, Secure Boot…)."),
                ("¿Cómo se activa?", "Configuración → Sistema → Activación con la clave del email."),
                ("¿Hay que reinstalar?", "Depende de actualización o instalación limpia; sigue el email y Microsoft."),
            ],
        },
    },
    "windows-10-home": {
        "apps": [],
        "title_html": L(
            it='Windows 10 <span>Home</span>',
            en='Windows 10 <span>Home</span>',
            fr='Windows 10 <span>Home</span>',
            de='Windows 10 <span>Home</span>',
            es='Windows 10 <span>Home</span>',
        ),
        "eyebrow": L(
            it="Sistema operativo · 32/64-bit · ESD",
            en="Operating system · 32/64-bit · ESD",
            fr="Système d'exploitation · 32/64 bits · ESD",
            de="Betriebssystem · 32/64-Bit · ESD",
            es="Sistema operativo · 32/64 bits · ESD",
        ),
        "desc": L(
            it="Windows 10 Home: licenza digitale originale 32/64-bit con consegna del codice via email. Ideale per uso domestico secondo le condizioni Microsoft.",
            en="Windows 10 Home: genuine 32/64-bit digital licence with email key delivery. Suited to home use under Microsoft’s terms.",
            fr="Windows 10 Home : licence numérique originale 32/64 bits, code par e-mail. Usage domestique selon Microsoft.",
            de="Windows 10 Home: originale 32/64-Bit-Lizenz mit Key per E-Mail. Für den Heimgebrauch gemäß Microsoft.",
            es="Windows 10 Home: licencia digital original 32/64 bits con clave por email. Uso doméstico según Microsoft.",
        ),
        "pills": _pills_win10(),
        "features_title": L(
            it="Windows 10 Home, licenza digitale",
            en="Windows 10 Home, digital licence",
            fr="Windows 10 Home, licence numérique",
            de="Windows 10 Home — digitale Lizenz",
            es="Windows 10 Home, licencia digital",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Edizione", "Home", "Edizione Home di Windows 10 per uso personale e domestico, con licenza ESD digitale."),
                ("c4", "teal", None, "32/64-bit", "Supporto architetture tipiche del prodotto Windows 10 Home."),
                ("c4", "purple", "Modello", "Senza abbonamento", "Licenza descritta in scheda, non un piano Microsoft 365."),
                ("c4", None, "Consegna", "Email", "Product key dopo il pagamento."),
                ("c4", None, "Attivazione", "Impostazioni Windows", "Attivi con il codice ricevuto sui canali Microsoft."),
                ("c4", "dark", "Nota", "Fine supporto", "Microsoft ha definito la fine del supporto per Windows 10: valuta se ti serve ancora questa versione o Windows 11."),
            ],
            "en": [
                ("c8", "blue", "Edition", "Home", "Windows 10 Home for personal and household use, with a digital ESD licence."),
                ("c4", "teal", None, "32/64-bit", "Typical architectures for the Windows 10 Home product."),
                ("c4", "purple", "Model", "No subscription", "Licence as described—not a Microsoft 365 plan."),
                ("c4", None, "Delivery", "Email", "Product key after payment."),
                ("c4", None, "Activation", "Windows Settings", "Activate with the received key via Microsoft channels."),
                ("c4", "dark", "Note", "End of support", "Microsoft has defined end of support for Windows 10—consider whether you still need this version or Windows 11."),
            ],
            "fr": [
                ("c8", "blue", "Édition", "Home", "Windows 10 Home pour usage personnel, licence ESD numérique."),
                ("c4", "teal", None, "32/64 bits", "Architectures typiques du produit Windows 10 Home."),
                ("c4", "purple", "Modèle", "Sans abonnement", "Licence décrite ici — pas Microsoft 365."),
                ("c4", None, "Livraison", "E-mail", "Clé produit après paiement."),
                ("c4", None, "Activation", "Paramètres Windows", "Activation avec le code reçu."),
                ("c4", "dark", "Note", "Fin de support", "Microsoft a fixé la fin du support de Windows 10 — évaluez Windows 11 si besoin."),
            ],
            "de": [
                ("c8", "blue", "Edition", "Home", "Windows 10 Home für den privaten Einsatz als digitale ESD-Lizenz."),
                ("c4", "teal", None, "32/64-Bit", "Typische Architekturen für Windows 10 Home."),
                ("c4", "purple", "Modell", "Ohne Abo", "Lizenz wie beschrieben — kein Microsoft 365."),
                ("c4", None, "Lieferung", "E-Mail", "Product Key nach der Zahlung."),
                ("c4", None, "Aktivierung", "Windows-Einstellungen", "Aktivierung mit dem erhaltenen Key."),
                ("c4", "dark", "Hinweis", "Support-Ende", "Microsoft hat das Support-Ende für Windows 10 definiert — ggf. Windows 11 prüfen."),
            ],
            "es": [
                ("c8", "blue", "Edición", "Home", "Windows 10 Home para uso personal con licencia ESD digital."),
                ("c4", "teal", None, "32/64 bits", "Arquitecturas típicas del producto Windows 10 Home."),
                ("c4", "purple", "Modelo", "Sin suscripción", "Licencia descrita aquí, no Microsoft 365."),
                ("c4", None, "Entrega", "Email", "Clave de producto tras el pago."),
                ("c4", None, "Activación", "Configuración Windows", "Activa con la clave recibida."),
                ("c4", "dark", "Nota", "Fin de soporte", "Microsoft ha definido el fin de soporte de Windows 10: valora si te conviene Windows 11."),
            ],
        },
        "apps_title": L(it="", en="", fr="", de="", es=""),
        "faq": {
            "it": [
                ("È Windows 10 Home o Pro?", "Questa scheda è Home. Per BitLocker/RDP host valuta Windows 10 Pro."),
                ("32 o 64-bit?", "Il prodotto indica 32/64-bit: segui le istruzioni e l'architettura del tuo PC."),
                ("Come si attiva?", "Impostazioni → Aggiornamento e sicurezza / Sistema → Attivazione con il codice email."),
                ("Posso passare a Windows 11 dopo?", "Solo se l'hardware è compatibile e secondo le regole Microsoft di upgrade."),
                ("Fine supporto Microsoft?", "Informati sulle date di fine supporto Windows 10 sul sito Microsoft prima dell'acquisto."),
            ],
            "en": [
                ("Home or Pro?", "This page is Home. For BitLocker/RDP host consider Windows 10 Pro."),
                ("32 or 64-bit?", "The product lists 32/64-bit—follow instructions and your PC architecture."),
                ("How do I activate?", "Settings → Update & Security / System → Activation with the emailed key."),
                ("Can I move to Windows 11 later?", "Only if hardware is compatible and per Microsoft upgrade rules."),
                ("End of support?", "Check Microsoft’s Windows 10 end-of-support dates before buying."),
            ],
            "fr": [
                ("Home ou Pro ?", "Cette fiche est Home. Pour BitLocker/RDP hôte, voyez Windows 10 Pro."),
                ("32 ou 64 bits ?", "Le produit indique 32/64 bits — suivez les instructions et votre PC."),
                ("Activation ?", "Paramètres → Activation avec le code reçu."),
                ("Passer à Windows 11 ?", "Uniquement si le matériel est compatible selon Microsoft."),
                ("Fin de support ?", "Consultez les dates Microsoft avant l'achat."),
            ],
            "de": [
                ("Home oder Pro?", "Diese Seite ist Home. Für BitLocker/RDP-Host eher Windows 10 Pro."),
                ("32 oder 64 Bit?", "Produkt nennt 32/64-Bit — Anleitung und PC-Architektur beachten."),
                ("Aktivierung?", "Einstellungen → Aktivierung mit dem E-Mail-Key."),
                ("Später Windows 11?", "Nur bei kompatibler Hardware laut Microsoft."),
                ("Support-Ende?", "Microsoft-Daten vor dem Kauf prüfen."),
            ],
            "es": [
                ("¿Home o Pro?", "Esta ficha es Home. Para BitLocker/RDP host valora Windows 10 Pro."),
                ("¿32 o 64 bits?", "El producto indica 32/64 bits: sigue instrucciones y la arquitectura de tu PC."),
                ("¿Cómo se activa?", "Configuración → Activación con la clave del email."),
                ("¿Pasar a Windows 11 luego?", "Solo si el hardware es compatible según Microsoft."),
                ("¿Fin de soporte?", "Consulta las fechas Microsoft antes de comprar."),
            ],
        },
    },
    "windows-10-pro": {
        "apps": [],
        "title_html": L(
            it='Windows 10 <span>Pro</span>',
            en='Windows 10 <span>Pro</span>',
            fr='Windows 10 <span>Pro</span>',
            de='Windows 10 <span>Pro</span>',
            es='Windows 10 <span>Pro</span>',
        ),
        "eyebrow": L(
            it="Sistema operativo · 32/64-bit · ESD",
            en="Operating system · 32/64-bit · ESD",
            fr="Système d'exploitation · 32/64 bits · ESD",
            de="Betriebssystem · 32/64-Bit · ESD",
            es="Sistema operativo · 32/64 bits · ESD",
        ),
        "desc": L(
            it="Windows 10 Pro: licenza digitale originale 32/64-bit con funzioni professionali (BitLocker, Desktop remoto e altro secondo Microsoft). Codice via email.",
            en="Windows 10 Pro: genuine 32/64-bit digital licence with professional features (BitLocker, Remote Desktop and more per Microsoft). Key by email.",
            fr="Windows 10 Pro : licence numérique 32/64 bits avec fonctions pro (BitLocker, Bureau à distance… selon Microsoft). Code par e-mail.",
            de="Windows 10 Pro: originale 32/64-Bit-Lizenz mit Pro-Funktionen (BitLocker, Remotedesktop u. a. laut Microsoft). Key per E-Mail.",
            es="Windows 10 Pro: licencia digital 32/64 bits con funciones profesionales (BitLocker, Escritorio remoto… según Microsoft). Clave por email.",
        ),
        "pills": {
            lg: [(None, "Windows 10 Pro"), (None, "32/64-bit"), (None, "ESD")]
            for lg in LANGS
        },
        "features_title": L(
            it="Windows 10 Pro per lavoro",
            en="Windows 10 Pro for work",
            fr="Windows 10 Pro pour le travail",
            de="Windows 10 Pro für die Arbeit",
            es="Windows 10 Pro para el trabajo",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Edizione", "Pro", "Licenza Pro con strumenti per professionisti e PMI rispetto a Home, secondo Microsoft."),
                ("c4", "teal", None, "BitLocker", "Crittografia unità dove supportata dall'hardware e dall'edizione."),
                ("c4", "purple", "Remoto", "Desktop remoto", "Host Remote Desktop tipico delle edizioni Pro."),
                ("c4", None, "Consegna", "ESD email", "Product key dopo il pagamento."),
                ("c4", None, "Attivazione", "Ufficiale", "Attivi da Impostazioni Windows."),
                ("c4", "dark", "Nota", "Supporto Windows 10", "Verifica le date di fine supporto Microsoft se pianifichi un uso a lungo termine."),
            ],
            "en": [
                ("c8", "blue", "Edition", "Pro", "Pro licence with tools for professionals and SMBs versus Home, per Microsoft."),
                ("c4", "teal", None, "BitLocker", "Drive encryption where hardware and edition support it."),
                ("c4", "purple", "Remote", "Remote Desktop", "Remote Desktop host typical of Pro editions."),
                ("c4", None, "Delivery", "ESD email", "Product key after payment."),
                ("c4", None, "Activation", "Official", "Activate from Windows Settings."),
                ("c4", "dark", "Note", "Windows 10 support", "Check Microsoft’s end-of-support dates for long-term use."),
            ],
            "fr": [
                ("c8", "blue", "Édition", "Pro", "Licence Pro avec outils pour pros/TPE par rapport à Home."),
                ("c4", "teal", None, "BitLocker", "Chiffrement si matériel et édition le permettent."),
                ("c4", "purple", "Distant", "Bureau à distance", "Hôte Remote Desktop typique des éditions Pro."),
                ("c4", None, "Livraison", "ESD e-mail", "Clé après paiement."),
                ("c4", None, "Activation", "Officielle", "Activation dans les Paramètres Windows."),
                ("c4", "dark", "Note", "Support Windows 10", "Vérifiez les dates de fin de support Microsoft."),
            ],
            "de": [
                ("c8", "blue", "Edition", "Pro", "Pro-Lizenz mit Tools für Profis/KMU gegenüber Home."),
                ("c4", "teal", None, "BitLocker", "Laufwerksverschlüsselung bei unterstützter Hardware/Edition."),
                ("c4", "purple", "Remote", "Remotedesktop", "Remotedesktop-Host typisch für Pro."),
                ("c4", None, "Lieferung", "ESD-E-Mail", "Product Key nach der Zahlung."),
                ("c4", None, "Aktivierung", "Offiziell", "Aktivierung in den Windows-Einstellungen."),
                ("c4", "dark", "Hinweis", "Windows-10-Support", "Microsoft-Support-Ende für langfristige Nutzung prüfen."),
            ],
            "es": [
                ("c8", "blue", "Edición", "Pro", "Licencia Pro con herramientas para profesionales/pymes frente a Home."),
                ("c4", "teal", None, "BitLocker", "Cifrado de unidad si el hardware y la edición lo permiten."),
                ("c4", "purple", "Remoto", "Escritorio remoto", "Host Remote Desktop típico de ediciones Pro."),
                ("c4", None, "Entrega", "ESD email", "Clave tras el pago."),
                ("c4", None, "Activación", "Oficial", "Activa desde Configuración de Windows."),
                ("c4", "dark", "Nota", "Soporte Windows 10", "Consulta las fechas de fin de soporte Microsoft."),
            ],
        },
        "apps_title": L(it="", en="", fr="", de="", es=""),
        "faq": {
            "it": [
                ("Differenza con Windows 10 Home?", "Pro include funzioni professionali aggiuntive (es. BitLocker, Desktop remoto host) rispetto a Home."),
                ("È perpetua?", "Sì: licenza ESD digitale descritta in scheda."),
                ("Come si attiva?", "Impostazioni Windows → Attivazione con il codice email."),
                ("32/64-bit?", "Segui le istruzioni e l'architettura del PC."),
                ("Passare a Windows 11?", "Solo con hardware compatibile e secondo le regole Microsoft."),
            ],
            "en": [
                ("Difference vs Home?", "Pro adds professional features (e.g. BitLocker, Remote Desktop host) versus Home."),
                ("Is it perpetual?", "Yes—digital ESD licence as described."),
                ("How do I activate?", "Windows Settings → Activation with the emailed key."),
                ("32/64-bit?", "Follow instructions and your PC architecture."),
                ("Move to Windows 11?", "Only with compatible hardware and per Microsoft rules."),
            ],
            "fr": [
                ("Différence avec Home ?", "Pro ajoute des fonctions pro (BitLocker, Bureau à distance hôte)."),
                ("Perpétuelle ?", "Oui — licence ESD numérique."),
                ("Activation ?", "Paramètres Windows → Activation avec le code."),
                ("32/64 bits ?", "Suivez les instructions et l'architecture du PC."),
                ("Passer à Windows 11 ?", "Uniquement si compatible selon Microsoft."),
            ],
            "de": [
                ("Unterschied zu Home?", "Pro ergänzt Profi-Funktionen (BitLocker, Remotedesktop-Host)."),
                ("Dauerhaft?", "Ja — digitale ESD-Lizenz."),
                ("Aktivierung?", "Windows-Einstellungen → Aktivierung mit dem Key."),
                ("32/64-Bit?", "Anleitung und PC-Architektur beachten."),
                ("Zu Windows 11?", "Nur bei kompatibler Hardware laut Microsoft."),
            ],
            "es": [
                ("¿Diferencia con Home?", "Pro añade funciones profesionales (BitLocker, Escritorio remoto host)."),
                ("¿Es perpetua?", "Sí: licencia ESD digital."),
                ("¿Cómo se activa?", "Configuración de Windows → Activación con la clave."),
                ("¿32/64 bits?", "Sigue las instrucciones y la arquitectura del PC."),
                ("¿Pasar a Windows 11?", "Solo con hardware compatible según Microsoft."),
            ],
        },
    },
    "windows-11-pro-oem-dvd": {
        "apps": [],
        "title_html": L(
            it='Windows 11 Pro <span>OEM DVD</span>',
            en='Windows 11 Pro <span>OEM DVD</span>',
            fr='Windows 11 Pro <span>OEM DVD</span>',
            de='Windows 11 Pro <span>OEM DVD</span>',
            es='Windows 11 Pro <span>OEM DVD</span>',
        ),
        "eyebrow": L(
            it="Licenza OEM · supporto DVD",
            en="OEM licence · DVD media",
            fr="Licence OEM · support DVD",
            de="OEM-Lizenz · DVD-Medium",
            es="Licencia OEM · soporte DVD",
        ),
        "desc": L(
            it="Windows 11 Pro OEM con supporto DVD: edizione Pro e supporto fisico come da scheda. Dopo l'acquisto ricevi le indicazioni via email e segui le istruzioni Microsoft.",
            en="Windows 11 Pro OEM with DVD media: Pro edition and physical media as listed. After purchase you receive email instructions and follow Microsoft’s process.",
            fr="Windows 11 Pro OEM avec DVD : édition Pro et support physique comme indiqué. Instructions par e-mail après l'achat.",
            de="Windows 11 Pro OEM mit DVD: Pro-Edition und physisches Medium laut Produktseite. Anleitung per E-Mail nach dem Kauf.",
            es="Windows 11 Pro OEM con DVD: edición Pro y soporte físico según la ficha. Instrucciones por email tras la compra.",
        ),
        "pills": {
            lg: [(None, "Windows 11 Pro"), (None, "OEM"), (None, "DVD")]
            for lg in LANGS
        },
        "features_title": L(
            it="Pro OEM con supporto DVD",
            en="Pro OEM with DVD media",
            fr="Pro OEM avec DVD",
            de="Pro OEM mit DVD",
            es="Pro OEM con DVD",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Formato", "OEM + DVD", "Edizione Windows 11 Pro OEM con supporto DVD come descritto nella scheda prodotto."),
                ("c4", "teal", None, "Edizione Pro", "Funzioni Pro (es. BitLocker, Desktop remoto) secondo Microsoft."),
                ("c4", "purple", "Consegna", "Come da ordine", "Ricevi istruzioni via email; il supporto fisico segue le modalità indicate."),
                ("c4", None, "Attivazione", "Microsoft", "Attivi Windows con la licenza/codice associati all'ordine."),
                ("c4", None, "Hardware", "Requisiti Win11", "Verifica CPU, TPM e Secure Boot prima dell'installazione."),
                ("c4", "dark", "Nota OEM", "Condizioni OEM", "Le licenze OEM hanno regole Microsoft specifiche su dispositivi e trasferimento: leggi email e termini."),
            ],
            "en": [
                ("c8", "blue", "Format", "OEM + DVD", "Windows 11 Pro OEM edition with DVD media as described on this page."),
                ("c4", "teal", None, "Pro edition", "Pro features (e.g. BitLocker, Remote Desktop) per Microsoft."),
                ("c4", "purple", "Delivery", "As ordered", "Email instructions; physical media follows the stated fulfilment."),
                ("c4", None, "Activation", "Microsoft", "Activate Windows with the licence/key tied to your order."),
                ("c4", None, "Hardware", "Win11 requirements", "Check CPU, TPM and Secure Boot before installing."),
                ("c4", "dark", "OEM note", "OEM terms", "OEM licences have specific Microsoft rules on devices and transfer—read email and terms."),
            ],
            "fr": [
                ("c8", "blue", "Format", "OEM + DVD", "Édition Windows 11 Pro OEM avec DVD comme décrit."),
                ("c4", "teal", None, "Édition Pro", "Fonctions Pro selon Microsoft."),
                ("c4", "purple", "Livraison", "Selon commande", "Instructions par e-mail ; support physique selon le mode indiqué."),
                ("c4", None, "Activation", "Microsoft", "Activation avec la licence/clé liée à la commande."),
                ("c4", None, "Matériel", "Exigences Win11", "Vérifiez CPU, TPM et Secure Boot."),
                ("c4", "dark", "Note OEM", "Conditions OEM", "Règles Microsoft spécifiques — lisez e-mail et conditions."),
            ],
            "de": [
                ("c8", "blue", "Format", "OEM + DVD", "Windows 11 Pro OEM mit DVD laut Produktseite."),
                ("c4", "teal", None, "Pro-Edition", "Pro-Funktionen laut Microsoft."),
                ("c4", "purple", "Lieferung", "Wie bestellt", "Anleitung per E-Mail; physisches Medium laut Erfüllung."),
                ("c4", None, "Aktivierung", "Microsoft", "Aktivierung mit Lizenz/Key der Bestellung."),
                ("c4", None, "Hardware", "Win11-Anforderungen", "CPU, TPM und Secure Boot prüfen."),
                ("c4", "dark", "OEM-Hinweis", "OEM-Bedingungen", "Spezielle Microsoft-Regeln — E-Mail und AGB lesen."),
            ],
            "es": [
                ("c8", "blue", "Formato", "OEM + DVD", "Edición Windows 11 Pro OEM con DVD según esta ficha."),
                ("c4", "teal", None, "Edición Pro", "Funciones Pro según Microsoft."),
                ("c4", "purple", "Entrega", "Según pedido", "Instrucciones por email; el soporte físico sigue lo indicado."),
                ("c4", None, "Activación", "Microsoft", "Activa con la licencia/clave del pedido."),
                ("c4", None, "Hardware", "Requisitos Win11", "Comprueba CPU, TPM y Secure Boot."),
                ("c4", "dark", "Nota OEM", "Condiciones OEM", "Reglas Microsoft específicas: lee email y términos."),
            ],
        },
        "apps_title": L(it="", en="", fr="", de="", es=""),
        "faq": {
            "it": [
                ("Cosa ricevo?", "Segui l'email di consegna: include istruzioni e quanto previsto per la licenza OEM e il supporto DVD."),
                ("È diversa dalla Pro ESD?", "Sì: questa scheda è OEM con DVD; la Pro ESD è solo digitale. Confronta le schede."),
                ("Come si attiva?", "Con la licenza/codice e le istruzioni ricevute, sui canali Microsoft."),
                ("Requisiti PC?", "Come per Windows 11: verifica compatibilità hardware Microsoft."),
                ("Posso trasferire la licenza?", "Le OEM hanno limiti specifici: consulta termini Microsoft e la nostra documentazione ordine."),
            ],
            "en": [
                ("What do I receive?", "Follow the delivery email—instructions and what is included for the OEM licence and DVD."),
                ("Different from Pro ESD?", "Yes—this page is OEM with DVD; Pro ESD is digital-only. Compare pages."),
                ("How do I activate?", "With the licence/key and instructions received, via Microsoft channels."),
                ("PC requirements?", "Same as Windows 11—check Microsoft hardware compatibility."),
                ("Can I transfer the licence?", "OEM has specific limits—see Microsoft terms and your order docs."),
            ],
            "fr": [
                ("Que vais-je recevoir ?", "Suivez l'e-mail de livraison pour licence OEM et DVD."),
                ("Différent de Pro ESD ?", "Oui — OEM avec DVD ; Pro ESD est 100 % numérique."),
                ("Activation ?", "Avec licence/code et instructions reçus."),
                ("Exigences PC ?", "Comme Windows 11 — compatibilité Microsoft."),
                ("Transfert de licence ?", "Limites OEM spécifiques — conditions Microsoft."),
            ],
            "de": [
                ("Was erhalte ich?", "Liefer-E-Mail zu OEM-Lizenz und DVD beachten."),
                ("Anders als Pro ESD?", "Ja — OEM mit DVD; Pro ESD ist rein digital."),
                ("Aktivierung?", "Mit erhaltener Lizenz/Key und Anleitung."),
                ("PC-Anforderungen?", "Wie Windows 11 — Microsoft-Kompatibilität prüfen."),
                ("Lizenz übertragbar?", "OEM-Grenzen — Microsoft-Bedingungen prüfen."),
            ],
            "es": [
                ("¿Qué recibo?", "Sigue el email de entrega para licencia OEM y DVD."),
                ("¿Es distinto de Pro ESD?", "Sí: OEM con DVD; Pro ESD es solo digital."),
                ("¿Cómo se activa?", "Con la licencia/clave e instrucciones recibidas."),
                ("¿Requisitos del PC?", "Como Windows 11: compatibilidad Microsoft."),
                ("¿Puedo transferir la licencia?", "Las OEM tienen límites: consulta términos Microsoft."),
            ],
        },
    },
    "windows-11-pro-coa": {
        "apps": [],
        "title_html": L(
            it='Windows 11 Pro <span>COA</span>',
            en='Windows 11 Pro <span>COA</span>',
            fr='Windows 11 Pro <span>COA</span>',
            de='Windows 11 Pro <span>COA</span>',
            es='Windows 11 Pro <span>COA</span>',
        ),
        "eyebrow": L(
            it="Licenza OEM · sticker COA",
            en="OEM licence · COA sticker",
            fr="Licence OEM · sticker COA",
            de="OEM-Lizenz · COA-Sticker",
            es="Licencia OEM · pegatina COA",
        ),
        "desc": L(
            it="Windows 11 Pro COA: licenza OEM con sticker Certificate of Authenticity. Dopo l'ordine ricevi le istruzioni via email e segui le indicazioni Microsoft.",
            en="Windows 11 Pro COA: OEM licence with Certificate of Authenticity sticker. After ordering you receive email instructions and follow Microsoft’s guidance.",
            fr="Windows 11 Pro COA : licence OEM avec sticker Certificate of Authenticity. Instructions par e-mail après commande.",
            de="Windows 11 Pro COA: OEM-Lizenz mit Certificate-of-Authenticity-Sticker. Anleitung per E-Mail nach der Bestellung.",
            es="Windows 11 Pro COA: licencia OEM con pegatina Certificate of Authenticity. Instrucciones por email tras el pedido.",
        ),
        "pills": {
            lg: [(None, "Windows 11 Pro"), (None, "OEM"), (None, "COA")]
            for lg in LANGS
        },
        "features_title": L(
            it="Pro OEM con sticker COA",
            en="Pro OEM with COA sticker",
            fr="Pro OEM avec sticker COA",
            de="Pro OEM mit COA-Sticker",
            es="Pro OEM con pegatina COA",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Formato", "COA OEM", "Licenza Windows 11 Pro OEM con sticker COA come descritto in scheda."),
                ("c4", "teal", None, "Edizione Pro", "Funzioni Pro secondo Microsoft."),
                ("c4", "purple", "Consegna", "Istruzioni + COA", "Email con indicazioni; lo sticker segue le modalità di spedizione/consegna indicate."),
                ("c4", None, "Attivazione", "Codice COA", "Usa il codice sullo sticker / istruzioni ricevute sui canali Microsoft."),
                ("c4", None, "Hardware", "Win11 ready", "Verifica requisiti Windows 11 prima dell'installazione."),
                ("c4", "dark", "Nota OEM", "Vincoli dispositivo", "Le OEM sono spesso legate al dispositivo: leggi termini e email d'ordine."),
            ],
            "en": [
                ("c8", "blue", "Format", "OEM COA", "Windows 11 Pro OEM licence with COA sticker as described."),
                ("c4", "teal", None, "Pro edition", "Pro features per Microsoft."),
                ("c4", "purple", "Delivery", "Instructions + COA", "Email guidance; sticker follows stated shipping/fulfilment."),
                ("c4", None, "Activation", "COA key", "Use the sticker key / received instructions on Microsoft channels."),
                ("c4", None, "Hardware", "Win11 ready", "Check Windows 11 requirements before installing."),
                ("c4", "dark", "OEM note", "Device binding", "OEM is often device-bound—read terms and order email."),
            ],
            "fr": [
                ("c8", "blue", "Format", "OEM COA", "Licence Windows 11 Pro OEM avec sticker COA."),
                ("c4", "teal", None, "Édition Pro", "Fonctions Pro selon Microsoft."),
                ("c4", "purple", "Livraison", "Instructions + COA", "E-mail ; sticker selon l'expédition indiquée."),
                ("c4", None, "Activation", "Clé COA", "Utilisez la clé du sticker / instructions reçues."),
                ("c4", None, "Matériel", "Win11 ready", "Vérifiez les exigences Windows 11."),
                ("c4", "dark", "Note OEM", "Appareil", "OEM souvent liée à l'appareil — lisez conditions et e-mail."),
            ],
            "de": [
                ("c8", "blue", "Format", "OEM COA", "Windows 11 Pro OEM mit COA-Sticker."),
                ("c4", "teal", None, "Pro-Edition", "Pro-Funktionen laut Microsoft."),
                ("c4", "purple", "Lieferung", "Anleitung + COA", "E-Mail; Sticker laut Versand/Erfüllung."),
                ("c4", None, "Aktivierung", "COA-Key", "Sticker-Key / erhaltene Anleitung nutzen."),
                ("c4", None, "Hardware", "Win11 ready", "Windows-11-Anforderungen prüfen."),
                ("c4", "dark", "OEM-Hinweis", "Gerät", "OEM oft gerätegebunden — AGB und E-Mail lesen."),
            ],
            "es": [
                ("c8", "blue", "Formato", "OEM COA", "Licencia Windows 11 Pro OEM con pegatina COA."),
                ("c4", "teal", None, "Edición Pro", "Funciones Pro según Microsoft."),
                ("c4", "purple", "Entrega", "Instrucciones + COA", "Email; la pegatina sigue el envío indicado."),
                ("c4", None, "Activación", "Clave COA", "Usa la clave de la pegatina / instrucciones recibidas."),
                ("c4", None, "Hardware", "Win11 ready", "Comprueba requisitos de Windows 11."),
                ("c4", "dark", "Nota OEM", "Dispositivo", "Las OEM suelen ir ligadas al dispositivo: lee términos y email."),
            ],
        },
        "apps_title": L(it="", en="", fr="", de="", es=""),
        "faq": {
            "it": [
                ("Cos'è il COA?", "Certificate of Authenticity: sticker con licenza OEM. Segui le istruzioni ricevute per l'attivazione."),
                ("Differenza con Pro ESD?", "COA/OEM implica supporto sticker e regole OEM; la Pro ESD è digitale via email."),
                ("Come si attiva?", "Con il codice sullo sticker e/o le istruzioni email, nei canali Microsoft."),
                ("Serve il DVD?", "Questa scheda è COA sticker, non la variante DVD OEM."),
                ("Trasferimento?", "Le OEM hanno limiti: consulta Microsoft e i termini dell'ordine."),
            ],
            "en": [
                ("What is the COA?", "Certificate of Authenticity—OEM sticker with the licence. Follow received instructions to activate."),
                ("Difference vs Pro ESD?", "COA/OEM involves a sticker and OEM rules; Pro ESD is digital by email."),
                ("How do I activate?", "With the sticker key and/or email instructions via Microsoft channels."),
                ("Do I need a DVD?", "This page is the COA sticker, not the OEM DVD variant."),
                ("Transfer?", "OEM has limits—see Microsoft and order terms."),
            ],
            "fr": [
                ("Qu'est-ce que le COA ?", "Certificate of Authenticity — sticker OEM. Suivez les instructions reçues."),
                ("Différence avec Pro ESD ?", "COA/OEM = sticker et règles OEM ; Pro ESD = numérique."),
                ("Activation ?", "Clé du sticker et/ou e-mail via Microsoft."),
                ("Faut-il un DVD ?", "Cette fiche est le sticker COA, pas le DVD OEM."),
                ("Transfert ?", "Limites OEM — Microsoft et conditions de commande."),
            ],
            "de": [
                ("Was ist COA?", "Certificate of Authenticity — OEM-Sticker. Erhaltene Anleitung folgen."),
                ("Unterschied zu Pro ESD?", "COA/OEM mit Sticker; Pro ESD rein digital."),
                ("Aktivierung?", "Sticker-Key und/oder E-Mail über Microsoft."),
                ("DVD nötig?", "Diese Seite ist COA-Sticker, nicht OEM-DVD."),
                ("Übertragung?", "OEM-Grenzen — Microsoft und Bestellbedingungen."),
            ],
            "es": [
                ("¿Qué es el COA?", "Certificate of Authenticity: pegatina OEM. Sigue las instrucciones recibidas."),
                ("¿Diferencia con Pro ESD?", "COA/OEM implica pegatina y reglas OEM; Pro ESD es digital."),
                ("¿Cómo se activa?", "Con la clave de la pegatina y/o el email vía Microsoft."),
                ("¿Necesito DVD?", "Esta ficha es pegatina COA, no la variante DVD OEM."),
                ("¿Transferencia?", "Las OEM tienen límites: consulta Microsoft y los términos del pedido."),
            ],
        },
    },
}


def get_windows_content(slug):
    return PRODUCTS.get(slug)
