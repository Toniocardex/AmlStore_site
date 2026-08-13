#!/usr/bin/env python3
"""Rich content for Office standalone apps, Project and Visio 2024."""

LANGS = ("it", "en", "fr", "de", "es")


def L(**kwargs):
    return {k: kwargs[k] for k in LANGS}


def _standalone(slug, app_key, app_name, title_span, focus_it, focus_en, focus_fr, focus_de, focus_es):
    apps = [app_key]
    return {
        "apps": apps,
        "title_html": L(
            it=f'{app_name} <span>{title_span}</span>',
            en=f'{app_name} <span>{title_span}</span>',
            fr=f'{app_name} <span>{title_span}</span>',
            de=f'{app_name} <span>{title_span}</span>',
            es=f'{app_name} <span>{title_span}</span>',
        ),
        "eyebrow": L(
            it="Licenza perpetua · app standalone · ESD",
            en="Perpetual licence · standalone app · ESD",
            fr="Licence perpétuelle · app autonome · ESD",
            de="Dauerlizenz · Einzel-App · ESD",
            es="Licencia perpetua · app independiente · ESD",
        ),
        "desc": L(
            it=f"{app_name} 2024 standalone: licenza digitale originale per usare solo {app_name}, senza abbonamento. Codice e istruzioni via email dopo l'acquisto.",
            en=f"{app_name} 2024 standalone: genuine digital licence to use {app_name} alone, no subscription. Key and instructions by email after purchase.",
            fr=f"{app_name} 2024 autonome : licence numérique originale pour utiliser uniquement {app_name}, sans abonnement. Code par e-mail après l'achat.",
            de=f"{app_name} 2024 Standalone: originale digitale Lizenz nur für {app_name}, ohne Abo. Key und Anleitung per E-Mail nach dem Kauf.",
            es=f"{app_name} 2024 independiente: licencia digital original para usar solo {app_name}, sin suscripción. Clave e instrucciones por email.",
        ),
        "pills": {
            lg: [(app_key, app_name), (None, "2024"), (None, "ESD")]
            for lg in LANGS
        },
        "features_title": L(
            it=f"Solo {app_name}, senza tutta la suite",
            en=f"{app_name} only—without the full suite",
            fr=f"Uniquement {app_name}, sans toute la suite",
            de=f"Nur {app_name} — ohne die volle Suite",
            es=f"Solo {app_name}, sin toda la suite",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Standalone", f"{app_name} 2024", f"Licenza perpetua ESD dedicata a {app_name}: ideale se non ti serve l'intera suite Office."),
                ("c4", "teal", None, focus_it, f"Pensata per chi lavora soprattutto con {app_name}."),
                ("c4", "purple", "Modello", "Senza abbonamento", "Acquisto una tantum della licenza descritta, non Microsoft 365."),
                ("c4", None, "Consegna", "Digitale via email", "Product key e istruzioni dopo il pagamento."),
                ("c4", None, "Attivazione", "setup.office.com", "Attivi sul portale Microsoft e installi l'app ufficiale."),
                ("c4", "dark", "Alternativa", "Suite completa", "Se ti servono più app insieme, valuta Office 2024 Home o Home & Business."),
            ],
            "en": [
                ("c8", "blue", "Standalone", f"{app_name} 2024", f"Perpetual ESD licence for {app_name} only—ideal if you don’t need the full Office suite."),
                ("c4", "teal", None, focus_en, f"Built for people who mainly work in {app_name}."),
                ("c4", "purple", "Model", "No subscription", "One-time licence purchase as described—not Microsoft 365."),
                ("c4", None, "Delivery", "Digital by email", "Product key and instructions after payment."),
                ("c4", None, "Activation", "setup.office.com", "Activate on Microsoft’s portal and install the official app."),
                ("c4", "dark", "Alternative", "Full suite", "If you need several apps together, consider Office 2024 Home or Home & Business."),
            ],
            "fr": [
                ("c8", "blue", "Autonome", f"{app_name} 2024", f"Licence ESD perpétuelle pour {app_name} seul — si vous n'avez pas besoin de toute la suite."),
                ("c4", "teal", None, focus_fr, f"Pour ceux qui travaillent surtout avec {app_name}."),
                ("c4", "purple", "Modèle", "Sans abonnement", "Achat unique de la licence — pas Microsoft 365."),
                ("c4", None, "Livraison", "Numérique", "Clé et instructions après paiement."),
                ("c4", None, "Activation", "setup.office.com", "Activation sur le portail Microsoft et installation de l'app."),
                ("c4", "dark", "Alternative", "Suite complète", "Pour plusieurs apps, voyez Office 2024 Home ou Home & Business."),
            ],
            "de": [
                ("c8", "blue", "Standalone", f"{app_name} 2024", f"ESD-Dauerlizenz nur für {app_name} — wenn Sie nicht die volle Suite brauchen."),
                ("c4", "teal", None, focus_de, f"Für alle, die vor allem mit {app_name} arbeiten."),
                ("c4", "purple", "Modell", "Ohne Abo", "Einmalkauf der beschriebenen Lizenz — kein Microsoft 365."),
                ("c4", None, "Lieferung", "Digital", "Product Key und Anleitung nach der Zahlung."),
                ("c4", None, "Aktivierung", "setup.office.com", "Aktivierung im Microsoft-Portal und Installation der App."),
                ("c4", "dark", "Alternative", "Volle Suite", "Bei mehreren Apps eher Office 2024 Home oder Home & Business."),
            ],
            "es": [
                ("c8", "blue", "Independiente", f"{app_name} 2024", f"Licencia ESD perpetua solo para {app_name}: ideal si no necesitas toda la suite."),
                ("c4", "teal", None, focus_es, f"Pensada para quien trabaja sobre todo con {app_name}."),
                ("c4", "purple", "Modelo", "Sin suscripción", "Compra única de la licencia descrita, no Microsoft 365."),
                ("c4", None, "Entrega", "Digital", "Clave e instrucciones tras el pago."),
                ("c4", None, "Activación", "setup.office.com", "Activa en el portal Microsoft e instala la app oficial."),
                ("c4", "dark", "Alternativa", "Suite completa", "Si necesitas varias apps, valora Office 2024 Home o Home & Business."),
            ],
        },
        "apps_title": L(
            it=f"App inclusa: {app_name}",
            en=f"App included: {app_name}",
            fr=f"App incluse : {app_name}",
            de=f"Enthaltene App: {app_name}",
            es=f"App incluida: {app_name}",
        ),
        "faq": {
            "it": [
                (f"Include altre app oltre a {app_name}?", f"No: è una licenza standalone per {app_name} 2024."),
                ("È un abbonamento?", "No: licenza perpetua ESD una tantum."),
                ("Come si attiva?", "Con il codice via email su setup.office.com e installazione dell'app ufficiale."),
                ("Meglio standalone o suite?", "Scegli standalone se usi solo questa app; la suite conviene se ti servono Word, Excel e PowerPoint insieme."),
                ("Funziona offline?", "Sì, con l'app desktop installata, entro le regole Microsoft di verifica licenza."),
            ],
            "en": [
                (f"Does it include apps other than {app_name}?", f"No—it is a standalone licence for {app_name} 2024."),
                ("Is it a subscription?", "No—one-time perpetual ESD licence."),
                ("How do I activate?", "With the emailed key at setup.office.com and install the official app."),
                ("Standalone or suite?", "Choose standalone if you only need this app; a suite is better if you need Word, Excel and PowerPoint together."),
                ("Works offline?", "Yes with the desktop app installed, within Microsoft’s licence-check rules."),
            ],
            "fr": [
                (f"D'autres apps que {app_name} ?", f"Non — licence autonome pour {app_name} 2024."),
                ("Abonnement ?", "Non — licence ESD perpétuelle."),
                ("Activation ?", "Code reçu sur setup.office.com, installation de l'app officielle."),
                ("Autonome ou suite ?", "Autonome si vous n'utilisez que cette app ; suite si vous voulez Word, Excel et PowerPoint."),
                ("Hors ligne ?", "Oui avec l'app de bureau, selon les règles Microsoft."),
            ],
            "de": [
                (f"Weitere Apps außer {app_name}?", f"Nein — Standalone-Lizenz für {app_name} 2024."),
                ("Abo?", "Nein — einmalige ESD-Dauerlizenz."),
                ("Aktivierung?", "E-Mail-Key unter setup.office.com, offizielle App installieren."),
                ("Standalone oder Suite?", "Standalone bei einer App; Suite bei Word, Excel und PowerPoint zusammen."),
                ("Offline?", "Ja mit Desktop-App, gemäß Microsoft-Lizenzregeln."),
            ],
            "es": [
                (f"¿Incluye otras apps además de {app_name}?", f"No: es una licencia independiente de {app_name} 2024."),
                ("¿Es suscripción?", "No: licencia ESD perpetua de compra única."),
                ("¿Cómo se activa?", "Con la clave del email en setup.office.com e instalación de la app oficial."),
                ("¿Independiente o suite?", "Independiente si solo usas esta app; suite si necesitas Word, Excel y PowerPoint juntos."),
                ("¿Funciona sin conexión?", "Sí con la app de escritorio, según las reglas Microsoft."),
            ],
        },
    }


def _project_or_visio(slug, name, edition_span, win_only, focus):
    out = {
        "apps": [],
        "title_html": L(
            it=f'{name} <span>{edition_span}</span>',
            en=f'{name} <span>{edition_span}</span>',
            fr=f'{name} <span>{edition_span}</span>',
            de=f'{name} <span>{edition_span}</span>',
            es=f'{name} <span>{edition_span}</span>',
        ),
        "eyebrow": L(
            it="Licenza perpetua · Windows · ESD" if win_only else "Licenza perpetua · ESD",
            en="Perpetual licence · Windows · ESD" if win_only else "Perpetual licence · ESD",
            fr="Licence perpétuelle · Windows · ESD" if win_only else "Licence perpétuelle · ESD",
            de="Dauerlizenz · Windows · ESD" if win_only else "Dauerlizenz · ESD",
            es="Licencia perpetua · Windows · ESD" if win_only else "Licencia perpetua · ESD",
        ),
        "desc": L(
            it=f"{name} {edition_span}: licenza digitale originale per pianificazione e diagrammi professionali (secondo Microsoft). Codice via email dopo l'acquisto.",
            en=f"{name} {edition_span}: genuine digital licence for professional planning and diagrams (per Microsoft). Key by email after purchase.",
            fr=f"{name} {edition_span} : licence numérique originale pour planification et diagrammes pro (selon Microsoft). Code par e-mail.",
            de=f"{name} {edition_span}: originale digitale Lizenz für professionelle Planung und Diagramme (laut Microsoft). Key per E-Mail.",
            es=f"{name} {edition_span}: licencia digital original para planificación y diagramas profesionales (según Microsoft). Clave por email.",
        ),
        "pills": {
            lg: [(None, name), (None, edition_span), (None, "Windows" if win_only else "ESD")]
            for lg in LANGS
        },
        "features_title": focus["features_title"],
        "features": focus["features"],
        "apps_title": L(it="", en="", fr="", de="", es=""),
        "faq": focus["faq"],
    }
    for key in (
        "desc",
        "eyebrow",
        "pills",
        "keypoints",
        "specs",
        "specs_note",
        "seo_title",
        "name",
    ):
        if key in focus:
            out[key] = focus[key]
    return out


PRODUCTS = {
    "word-2024": _standalone(
        "word-2024", "word", "Word", "2024",
        "Documenti", "Documents", "Documents", "Dokumente", "Documentos",
    ),
    "excel-2024": _standalone(
        "excel-2024", "excel", "Excel", "2024",
        "Fogli di calcolo", "Spreadsheets", "Tableurs", "Tabellen", "Hojas de cálculo",
    ),
    "powerpoint-2024": _standalone(
        "powerpoint-2024", "powerpoint", "PowerPoint", "2024",
        "Presentazioni", "Presentations", "Présentations", "Präsentationen", "Presentaciones",
    ),
    "outlook-2024": _standalone(
        "outlook-2024", "outlook", "Outlook", "2024",
        "Posta e calendario", "Mail & calendar", "Messagerie", "E-Mail & Kalender", "Correo y calendario",
    ),
}

PRODUCTS["word-2024"]["overview"] = {
    "it": {
        "eyebrow": "Descrizione",
        "title": "Crea documenti chiari e professionali con Word 2024",
        "paragraphs": [
            "Microsoft Word 2024 è l'applicazione desktop dedicata alla creazione, modifica e formattazione di documenti. Puoi usarla per lettere, relazioni, curriculum, materiale didattico e documenti aziendali, organizzando testo, immagini, tabelle e impaginazione in un unico ambiente di lavoro.",
            "Questa edizione viene fornita come licenza perpetua standalone: acquisti Word 2024 senza abbonamento e senza le altre applicazioni della suite Office. Dopo il pagamento ricevi via email il product key e le istruzioni per l'attivazione tramite i canali ufficiali Microsoft.",
        ],
    },
    "en": {
        "eyebrow": "Description",
        "title": "Create clear, professional documents with Word 2024",
        "paragraphs": [
            "Microsoft Word 2024 is the desktop application for creating, editing and formatting documents. Use it for letters, reports, CVs, learning materials and business documents, bringing text, images, tables and page layout together in one workspace.",
            "This edition is supplied as a standalone perpetual licence: you purchase Word 2024 without a subscription and without the other Office suite applications. After payment, you receive the product key and activation instructions by email for use through official Microsoft channels.",
        ],
    },
    "fr": {
        "eyebrow": "Description",
        "title": "Créez des documents clairs et professionnels avec Word 2024",
        "paragraphs": [
            "Microsoft Word 2024 est l'application de bureau conçue pour créer, modifier et mettre en forme des documents. Utilisez-la pour vos lettres, rapports, CV, supports pédagogiques et documents professionnels, avec texte, images, tableaux et mise en page dans un même espace de travail.",
            "Cette édition est fournie sous forme de licence perpétuelle autonome : vous achetez Word 2024 sans abonnement et sans les autres applications de la suite Office. Après le paiement, vous recevez par e-mail la clé produit et les instructions d'activation via les canaux officiels Microsoft.",
        ],
    },
    "de": {
        "eyebrow": "Beschreibung",
        "title": "Klare und professionelle Dokumente mit Word 2024 erstellen",
        "paragraphs": [
            "Microsoft Word 2024 ist die Desktop-Anwendung zum Erstellen, Bearbeiten und Formatieren von Dokumenten. Sie eignet sich für Briefe, Berichte, Lebensläufe, Lernmaterialien und Geschäftsdokumente und verbindet Text, Bilder, Tabellen und Seitenlayout in einer Arbeitsumgebung.",
            "Diese Edition wird als eigenständige Dauerlizenz angeboten: Sie erwerben Word 2024 ohne Abonnement und ohne die weiteren Anwendungen der Office-Suite. Nach der Zahlung erhalten Sie den Product Key und die Aktivierungsanleitung per E-Mail für die offiziellen Microsoft-Kanäle.",
        ],
    },
    "es": {
        "eyebrow": "Descripción",
        "title": "Crea documentos claros y profesionales con Word 2024",
        "paragraphs": [
            "Microsoft Word 2024 es la aplicación de escritorio para crear, editar y dar formato a documentos. Puedes utilizarla para cartas, informes, currículums, material educativo y documentos empresariales, combinando texto, imágenes, tablas y diseño de página en un único entorno de trabajo.",
            "Esta edición se suministra como licencia perpetua independiente: compras Word 2024 sin suscripción y sin las demás aplicaciones de la suite Office. Después del pago recibirás por email la clave de producto y las instrucciones de activación mediante los canales oficiales de Microsoft.",
        ],
    },
}

PRODUCTS["project-standard-2024"] = _project_or_visio(
    "project-standard-2024",
    "Project",
    "Standard 2024",
    True,
    {
        "features_title": L(
            it="Project Standard 2024 per Windows",
            en="Project Standard 2024 for Windows",
            fr="Project Standard 2024 pour Windows",
            de="Project Standard 2024 für Windows",
            es="Project Standard 2024 para Windows",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Edizione", "Standard", "Microsoft Project Standard 2024: pianificazione progetti in licenza perpetua ESD per Windows."),
                ("c4", "teal", None, "Gestione progetti", "Pianifica attività, risorse e scadenze secondo le capacità Standard di Project."),
                ("c4", "purple", "Piattaforma", "Windows", "Edizione desktop per Windows, come da offerta Microsoft."),
                ("c4", None, "Consegna", "Digitale", "Product key via email dopo il pagamento."),
                ("c4", None, "Attivazione", "Canali Microsoft", "Attivi e installi seguendo istruzioni email e portali ufficiali."),
                ("c4", "dark", "Alternativa", "Professional", "Per funzioni avanzate valuta Project Professional 2024."),
            ],
            "en": [
                ("c8", "blue", "Edition", "Standard", "Microsoft Project Standard 2024: project planning as a perpetual ESD licence for Windows."),
                ("c4", "teal", None, "Project management", "Plan tasks, resources and deadlines within Standard Project capabilities."),
                ("c4", "purple", "Platform", "Windows", "Desktop edition for Windows per Microsoft’s offer."),
                ("c4", None, "Delivery", "Digital", "Product key by email after payment."),
                ("c4", None, "Activation", "Microsoft channels", "Activate and install via email instructions and official portals."),
                ("c4", "dark", "Alternative", "Professional", "For advanced features consider Project Professional 2024."),
            ],
            "fr": [
                ("c8", "blue", "Édition", "Standard", "Microsoft Project Standard 2024 : planification en licence ESD perpétuelle pour Windows."),
                ("c4", "teal", None, "Gestion de projet", "Tâches, ressources et échéances selon Project Standard."),
                ("c4", "purple", "Plateforme", "Windows", "Édition de bureau pour Windows."),
                ("c4", None, "Livraison", "Numérique", "Clé par e-mail après paiement."),
                ("c4", None, "Activation", "Canaux Microsoft", "Activation et installation via e-mail et portails officiels."),
                ("c4", "dark", "Alternative", "Professional", "Pour plus de fonctions, Project Professional 2024."),
            ],
            "de": [
                ("c8", "blue", "Edition", "Standard", "Microsoft Project Standard 2024: Projektplanung als ESD-Dauerlizenz für Windows."),
                ("c4", "teal", None, "Projektmanagement", "Aufgaben, Ressourcen und Termine gemäß Project Standard."),
                ("c4", "purple", "Plattform", "Windows", "Desktop-Edition für Windows."),
                ("c4", None, "Lieferung", "Digital", "Product Key per E-Mail nach der Zahlung."),
                ("c4", None, "Aktivierung", "Microsoft-Kanäle", "Aktivierung und Installation über E-Mail und offizielle Portale."),
                ("c4", "dark", "Alternative", "Professional", "Für erweiterte Funktionen Project Professional 2024."),
            ],
            "es": [
                ("c8", "blue", "Edición", "Standard", "Microsoft Project Standard 2024: planificación con licencia ESD perpetua para Windows."),
                ("c4", "teal", None, "Gestión de proyectos", "Tareas, recursos y plazos según Project Standard."),
                ("c4", "purple", "Plataforma", "Windows", "Edición de escritorio para Windows."),
                ("c4", None, "Entrega", "Digital", "Clave por email tras el pago."),
                ("c4", None, "Activación", "Canales Microsoft", "Activa e instala con email y portales oficiales."),
                ("c4", "dark", "Alternativa", "Professional", "Para funciones avanzadas, Project Professional 2024."),
            ],
        },
        "faq": {
            "it": [
                ("Differenza con Project Professional?", "Professional include funzioni più avanzate; Standard copre la pianificazione tipica. Confronta le schede Microsoft se hai dubbi."),
                ("È un abbonamento?", "No: licenza perpetua ESD."),
                ("Solo Windows?", "Sì, come da scheda prodotto Windows."),
                ("Come si attiva?", "Con il codice ricevuto via email sui canali Microsoft."),
                ("Include Visio o Office?", "No: è la licenza Project indicata, non la suite Office completa."),
            ],
            "en": [
                ("Difference vs Project Professional?", "Professional has more advanced features; Standard covers typical planning. Compare Microsoft docs if unsure."),
                ("Is it a subscription?", "No—perpetual ESD licence."),
                ("Windows only?", "Yes, as listed on this Windows product page."),
                ("How do I activate?", "With the emailed key via Microsoft channels."),
                ("Includes Visio or Office?", "No—this is the Project licence listed, not the full Office suite."),
            ],
            "fr": [
                ("Différence avec Professional ?", "Professional a plus de fonctions avancées ; Standard couvre la planification typique."),
                ("Abonnement ?", "Non — licence ESD perpétuelle."),
                ("Windows uniquement ?", "Oui, comme indiqué sur la fiche."),
                ("Activation ?", "Code reçu via les canaux Microsoft."),
                ("Inclut Visio ou Office ?", "Non — licence Project indiquée, pas la suite Office."),
            ],
            "de": [
                ("Unterschied zu Professional?", "Professional hat mehr Funktionen; Standard deckt typische Planung ab."),
                ("Abo?", "Nein — ESD-Dauerlizenz."),
                ("Nur Windows?", "Ja, laut Produktseite."),
                ("Aktivierung?", "E-Mail-Key über Microsoft-Kanäle."),
                ("Mit Visio oder Office?", "Nein — genannte Project-Lizenz, nicht die Office-Suite."),
            ],
            "es": [
                ("¿Diferencia con Professional?", "Professional tiene más funciones avanzadas; Standard cubre la planificación típica."),
                ("¿Es suscripción?", "No: licencia ESD perpetua."),
                ("¿Solo Windows?", "Sí, según esta ficha."),
                ("¿Cómo se activa?", "Con la clave del email en canales Microsoft."),
                ("¿Incluye Visio u Office?", "No: es la licencia Project indicada, no la suite Office."),
            ],
        },
    },
)

PRODUCTS["project-professional-2024"] = _project_or_visio(
    "project-professional-2024",
    "Project",
    "Professional 2024",
    True,
    {
        "name": L(
            it="Project Professional 2024",
            en="Project Professional 2024",
            fr="Project Professional 2024",
            de="Project Professional 2024",
            es="Project Professional 2024",
        ),
        "seo_title": L(
            it="Project Professional 2024 — licenza perpetua ESD | Aml Store",
            en="Project Professional 2024 — perpetual ESD licence | Aml Store",
            fr="Project Professional 2024 — licence ESD perpétuelle | Aml Store",
            de="Project Professional 2024 — ESD-Dauerlizenz | Aml Store",
            es="Project Professional 2024 — licencia ESD perpetua | Aml Store",
        ),
        "desc": L(
            it="Project Professional 2024: software on-premise di project management (1 PC). Licenza perpetua ESD con pianificazione avanzata, sincronizzazione con Project Online/Server e supporto LTSC (secondo Microsoft). Codice via email dopo l'acquisto.",
            en="Project Professional 2024: on-premises project management software (1 PC). Perpetual ESD licence with advanced scheduling, sync with Project Online/Server and LTSC support (per Microsoft). Key by email after purchase.",
            fr="Project Professional 2024 : logiciel de gestion de projet local (1 PC). Licence ESD perpétuelle avec planification avancée, sync Project Online/Server et support LTSC (selon Microsoft). Code par e-mail.",
            de="Project Professional 2024: lokale Projektmanagement-Software (1 PC). ESD-Dauerlizenz mit erweiterter Planung, Sync mit Project Online/Server und LTSC-Support (laut Microsoft). Key per E-Mail.",
            es="Project Professional 2024: software local de gestión de proyectos (1 PC). Licencia ESD perpetua con planificación avanzada, sync con Project Online/Server y soporte LTSC (según Microsoft). Clave por email.",
        ),
        "keypoints": {
            "it": [
                "Licenza per 1 PC (perpetua)",
                "Pianificazione e risorse avanzate",
                "Sync con Project Online / Server",
                "Compatibile LTSC e Office 2024",
            ],
            "en": [
                "Licensed for 1 PC (perpetual)",
                "Advanced scheduling & resources",
                "Sync with Project Online / Server",
                "LTSC and Office 2024 compatible",
            ],
            "fr": [
                "Licence pour 1 PC (perpétuelle)",
                "Planification et ressources avancées",
                "Sync avec Project Online / Server",
                "Compatible LTSC et Office 2024",
            ],
            "de": [
                "Lizenz für 1 PC (dauerhaft)",
                "Erweiterte Planung & Ressourcen",
                "Sync mit Project Online / Server",
                "LTSC- und Office-2024-kompatibel",
            ],
            "es": [
                "Licencia para 1 PC (perpetua)",
                "Planificación y recursos avanzados",
                "Sync con Project Online / Server",
                "Compatible LTSC y Office 2024",
            ],
        },
        "features_title": L(
            it="Cosa offre Project Professional 2024",
            en="What Project Professional 2024 offers",
            fr="Ce que propose Project Professional 2024",
            de="Was Project Professional 2024 bietet",
            es="Qué ofrece Project Professional 2024",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Edizione", "Professional · 1 PC", "Licenza perpetua on-premise per un PC Windows. Supporta LTSC ed è compatibile con Office LTSC e Office 2024 (secondo Microsoft)."),
                ("c4", "teal", None, "Programmazione automatica", "Date di inizio/fine dalle dipendenze, scenari what-if e più timeline per programmazioni complesse."),
                ("c4", "purple", None, "Risorse e team", "Gestisci assegnazioni, schede attività e collaborazione (es. presenza Teams dove previsto da Microsoft)."),
                ("c4", None, None, "Report e Gantt", "Report predefiniti (es. burn-down, risorse) e evidenziazione del percorso critico nei diagrammi di Gantt."),
                ("c4", None, "Consegna", "ESD via email", "Product key e istruzioni dopo il pagamento; attivazione sui canali Microsoft."),
                ("c4", "dark", "Nota", "Non è Project Piano 3", "Professional è perpetua e non scade dopo l'attivazione. I piani cloud (es. Piano 3) sono abbonamenti con sempre l'ultima versione."),
            ],
            "en": [
                ("c8", "blue", "Edition", "Professional · 1 PC", "Perpetual on-premises licence for one Windows PC. Supports LTSC and is compatible with Office LTSC and Office 2024 (per Microsoft)."),
                ("c4", "teal", None, "Automated scheduling", "Start/finish dates from dependencies, what-if scenarios and multiple timelines for complex schedules."),
                ("c4", "purple", None, "Resources & teams", "Manage assignments, timesheets and collaboration (e.g. Teams presence where Microsoft provides it)."),
                ("c4", None, None, "Reports & Gantt", "Built-in reports (e.g. burn-down, resources) and task-path highlighting in Gantt charts."),
                ("c4", None, "Delivery", "ESD by email", "Product key and instructions after payment; activate via Microsoft channels."),
                ("c4", "dark", "Note", "Not Project Plan 3", "Professional is perpetual and does not expire after activation. Cloud plans (e.g. Plan 3) are subscriptions that stay current."),
            ],
            "fr": [
                ("c8", "blue", "Édition", "Professional · 1 PC", "Licence perpétuelle locale pour un PC Windows. Prend en charge LTSC et est compatible avec Office LTSC et Office 2024 (selon Microsoft)."),
                ("c4", "teal", None, "Planification automatisée", "Dates début/fin selon les dépendances, scénarios what-if et plusieurs chronologies."),
                ("c4", "purple", None, "Ressources et équipes", "Affectations, feuilles de temps et collaboration (présence Teams selon Microsoft)."),
                ("c4", None, None, "Rapports et Gantt", "Rapports prédéfinis (ex. burn-down, ressources) et chemin critique dans les Gantt."),
                ("c4", None, "Livraison", "ESD par e-mail", "Clé et instructions après paiement ; activation via les canaux Microsoft."),
                ("c4", "dark", "Note", "Pas Project Plan 3", "Professional est perpétuelle après activation. Les plans cloud (ex. Plan 3) sont des abonnements toujours à jour."),
            ],
            "de": [
                ("c8", "blue", "Edition", "Professional · 1 PC", "Dauerhafte lokale Lizenz für einen Windows-PC. Unterstützt LTSC und ist kompatibel mit Office LTSC und Office 2024 (laut Microsoft)."),
                ("c4", "teal", None, "Automatisierte Planung", "Start-/Enddaten aus Abhängigkeiten, What-if-Szenarien und mehrere Zeitachsen."),
                ("c4", "purple", None, "Ressourcen & Teams", "Zuweisungen, Zeitnachweise und Zusammenarbeit (Teams-Präsenz laut Microsoft)."),
                ("c4", None, None, "Berichte & Gantt", "Vorgefertigte Berichte (z. B. Burn-down, Ressourcen) und Aufgabenpfad in Gantt-Diagrammen."),
                ("c4", None, "Lieferung", "ESD per E-Mail", "Product Key und Anleitung nach der Zahlung; Aktivierung über Microsoft-Kanäle."),
                ("c4", "dark", "Hinweis", "Kein Project Plan 3", "Professional ist nach Aktivierung dauerhaft. Cloud-Pläne (z. B. Plan 3) sind Abos mit stets aktueller Version."),
            ],
            "es": [
                ("c8", "blue", "Edición", "Professional · 1 PC", "Licencia local perpetua para un PC Windows. Compatible con LTSC y con Office LTSC y Office 2024 (según Microsoft)."),
                ("c4", "teal", None, "Programación automática", "Fechas inicio/fin por dependencias, escenarios what-if y varias líneas de tiempo."),
                ("c4", "purple", None, "Recursos y equipos", "Asignaciones, partes de horas y colaboración (presencia Teams según Microsoft)."),
                ("c4", None, None, "Informes y Gantt", "Informes predefinidos (p. ej. burn-down, recursos) y ruta crítica en diagramas de Gantt."),
                ("c4", None, "Entrega", "ESD por email", "Clave e instrucciones tras el pago; activación por canales Microsoft."),
                ("c4", "dark", "Nota", "No es Project Plan 3", "Professional es perpetua tras la activación. Los planes en la nube (p. ej. Plan 3) son suscripciones siempre actualizadas."),
            ],
        },
        "specs": {
            "it": [
                ("Processore", "1,6 GHz o superiore, dual core (secondo Microsoft)"),
                ("Sistema operativo", "Windows 11, Windows 10 o Windows Server 2019"),
                ("Memoria", "4 GB di RAM (2 GB per sistemi a 32 bit)"),
                ("Spazio su disco", "4 GB di spazio disponibile"),
            ],
            "en": [
                ("Processor", "1.6 GHz or faster, dual-core (per Microsoft)"),
                ("Operating system", "Windows 11, Windows 10 or Windows Server 2019"),
                ("Memory", "4 GB RAM (2 GB for 32-bit)"),
                ("Disk space", "4 GB available"),
            ],
            "fr": [
                ("Processeur", "1,6 GHz ou plus, dual core (selon Microsoft)"),
                ("Système d'exploitation", "Windows 11, Windows 10 ou Windows Server 2019"),
                ("Mémoire", "4 Go de RAM (2 Go en 32 bits)"),
                ("Espace disque", "4 Go disponibles"),
            ],
            "de": [
                ("Prozessor", "1,6 GHz oder schneller, Dual-Core (laut Microsoft)"),
                ("Betriebssystem", "Windows 11, Windows 10 oder Windows Server 2019"),
                ("Arbeitsspeicher", "4 GB RAM (2 GB bei 32 Bit)"),
                ("Festplatte", "4 GB frei"),
            ],
            "es": [
                ("Procesador", "1,6 GHz o superior, dual core (según Microsoft)"),
                ("Sistema operativo", "Windows 11, Windows 10 o Windows Server 2019"),
                ("Memoria", "4 GB de RAM (2 GB en 32 bits)"),
                ("Espacio en disco", "4 GB disponibles"),
            ],
        },
        "specs_note": L(
            it="Requisiti indicativi da documentazione Microsoft. Verifica sempre la compatibilità del dispositivo prima dell'acquisto.",
            en="Indicative requirements from Microsoft documentation. Always check device compatibility before purchase.",
            fr="Exigences indicatives selon Microsoft. Vérifiez toujours la compatibilité avant l'achat.",
            de="Richtwerte laut Microsoft-Dokumentation. Gerätekompatibilität vor dem Kauf prüfen.",
            es="Requisitos indicativos según Microsoft. Comprueba siempre la compatibilidad antes de comprar.",
        ),
        "faq": {
            "it": [
                ("Differenza con Project Standard 2024?", "Professional è l'edizione più completa (risorse avanzate, sync con Project Online/Server, scenari e report più ricchi). Per pianificazione tipica valuta Standard."),
                ("Differenza con Project Piano 3 (abbonamento)?", "Le funzioni di base sono simili all'acquisto, ma Piano 3 resta sempre aggiornato con abbonamento. Professional è licenza perpetua e non scade dopo l'attivazione (secondo Microsoft)."),
                ("Su quanti PC posso installarlo?", "Concesso in licenza per 1 PC, come da scheda Microsoft Store."),
                ("Serve Windows? Quali versioni?", "Sì: Windows 11, Windows 10 o Windows Server 2019 secondo i requisiti Microsoft indicati in scheda."),
                ("Come si attiva?", "Ricevi il codice via email e segui i portali/istruzioni Microsoft (es. setup.office.com)."),
            ],
            "en": [
                ("Difference vs Project Standard 2024?", "Professional is the fuller edition (advanced resources, Project Online/Server sync, richer scenarios and reports). For typical planning, consider Standard."),
                ("Difference vs Project Plan 3 (subscription)?", "Core features are similar at purchase, but Plan 3 stays current with a subscription. Professional is perpetual and does not expire after activation (per Microsoft)."),
                ("How many PCs?", "Licensed for 1 PC, as on the Microsoft Store listing."),
                ("Which Windows versions?", "Windows 11, Windows 10 or Windows Server 2019 per Microsoft’s stated requirements."),
                ("How do I activate?", "Receive the emailed key and follow Microsoft portals/instructions (e.g. setup.office.com)."),
            ],
            "fr": [
                ("Différence avec Project Standard 2024 ?", "Professional est plus complet (ressources avancées, sync Online/Server, scénarios et rapports). Pour l'essentiel, voyez Standard."),
                ("Différence avec Project Plan 3 ?", "Fonctions de base proches à l'achat ; Plan 3 reste à jour via abonnement. Professional est perpétuelle après activation (selon Microsoft)."),
                ("Combien de PC ?", "Licence pour 1 PC, comme sur Microsoft Store."),
                ("Quelles versions de Windows ?", "Windows 11, Windows 10 ou Windows Server 2019 selon Microsoft."),
                ("Activation ?", "Code reçu par e-mail puis portails/instructions Microsoft (ex. setup.office.com)."),
            ],
            "de": [
                ("Unterschied zu Project Standard 2024?", "Professional ist umfangreicher (erweiterte Ressourcen, Sync Online/Server, mehr Szenarien und Berichte). Für Basis eher Standard."),
                ("Unterschied zu Project Plan 3?", "Kernfunktionen ähnlich beim Kauf; Plan 3 bleibt per Abo aktuell. Professional ist nach Aktivierung dauerhaft (laut Microsoft)."),
                ("Wie viele PCs?", "Lizenz für 1 PC laut Microsoft Store."),
                ("Welche Windows-Versionen?", "Windows 11, Windows 10 oder Windows Server 2019 laut Microsoft."),
                ("Aktivierung?", "E-Mail-Key und Microsoft-Portale/Anleitungen (z. B. setup.office.com)."),
            ],
            "es": [
                ("¿Diferencia con Project Standard 2024?", "Professional es la edición más completa (recursos avanzados, sync Online/Server, más escenarios e informes). Para lo básico, Standard."),
                ("¿Diferencia con Project Plan 3?", "Las funciones básicas son similares al comprar; Plan 3 se actualiza con suscripción. Professional es perpetua tras la activación (según Microsoft)."),
                ("¿En cuántos PC?", "Licencia para 1 PC, según Microsoft Store."),
                ("¿Qué versiones de Windows?", "Windows 11, Windows 10 o Windows Server 2019 según Microsoft."),
                ("¿Cómo se activa?", "Clave por email y portales/instrucciones Microsoft (p. ej. setup.office.com)."),
            ],
        },
    },
)

PRODUCTS["visio-standard-2024"] = _project_or_visio(
    "visio-standard-2024",
    "Visio",
    "Standard 2024",
    True,
    {
        "features_title": L(
            it="Visio Standard 2024",
            en="Visio Standard 2024",
            fr="Visio Standard 2024",
            de="Visio Standard 2024",
            es="Visio Standard 2024",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Edizione", "Standard", "Microsoft Visio Standard 2024: diagrammi e flussi in licenza perpetua ESD per Windows."),
                ("c4", "teal", None, "Diagrammi", "Crea schemi e flowchart secondo le capacità Standard di Visio."),
                ("c4", "purple", "Piattaforma", "Windows", "Edizione desktop Windows."),
                ("c4", None, "Consegna", "Digitale", "Product key via email."),
                ("c4", None, "Attivazione", "Microsoft", "Attivi con il codice ricevuto."),
                ("c4", "dark", "Alternativa", "Professional", "Per funzioni più avanzate valuta Visio Professional 2024."),
            ],
            "en": [
                ("c8", "blue", "Edition", "Standard", "Microsoft Visio Standard 2024: diagrams and flows as a perpetual ESD licence for Windows."),
                ("c4", "teal", None, "Diagrams", "Create charts and flowcharts within Visio Standard capabilities."),
                ("c4", "purple", "Platform", "Windows", "Windows desktop edition."),
                ("c4", None, "Delivery", "Digital", "Product key by email."),
                ("c4", None, "Activation", "Microsoft", "Activate with the received key."),
                ("c4", "dark", "Alternative", "Professional", "For more advanced features consider Visio Professional 2024."),
            ],
            "fr": [
                ("c8", "blue", "Édition", "Standard", "Microsoft Visio Standard 2024 : diagrammes en licence ESD perpétuelle pour Windows."),
                ("c4", "teal", None, "Diagrammes", "Schémas et flux selon Visio Standard."),
                ("c4", "purple", "Plateforme", "Windows", "Édition de bureau Windows."),
                ("c4", None, "Livraison", "Numérique", "Clé par e-mail."),
                ("c4", None, "Activation", "Microsoft", "Activation avec le code reçu."),
                ("c4", "dark", "Alternative", "Professional", "Pour plus de fonctions, Visio Professional 2024."),
            ],
            "de": [
                ("c8", "blue", "Edition", "Standard", "Microsoft Visio Standard 2024: Diagramme als ESD-Dauerlizenz für Windows."),
                ("c4", "teal", None, "Diagramme", "Schemata und Flussdiagramme gemäß Visio Standard."),
                ("c4", "purple", "Plattform", "Windows", "Windows-Desktop-Edition."),
                ("c4", None, "Lieferung", "Digital", "Product Key per E-Mail."),
                ("c4", None, "Aktivierung", "Microsoft", "Aktivierung mit dem erhaltenen Key."),
                ("c4", "dark", "Alternative", "Professional", "Für mehr Funktionen Visio Professional 2024."),
            ],
            "es": [
                ("c8", "blue", "Edición", "Standard", "Microsoft Visio Standard 2024: diagramas con licencia ESD perpetua para Windows."),
                ("c4", "teal", None, "Diagramas", "Esquemas y flujogramas según Visio Standard."),
                ("c4", "purple", "Plataforma", "Windows", "Edición de escritorio Windows."),
                ("c4", None, "Entrega", "Digital", "Clave por email."),
                ("c4", None, "Activación", "Microsoft", "Activa con la clave recibida."),
                ("c4", "dark", "Alternativa", "Professional", "Para más funciones, Visio Professional 2024."),
            ],
        },
        "faq": {
            "it": [
                ("Standard o Professional?", "Professional offre funzioni più avanzate; Standard è adatta a diagrammi tipici."),
                ("È perpetua?", "Sì: licenza ESD."),
                ("Solo Windows?", "Sì."),
                ("Come si attiva?", "Codice email sui canali Microsoft."),
                ("Fa parte di Office?", "È un prodotto Visio separato, non incluso automaticamente nelle suite Home."),
            ],
            "en": [
                ("Standard or Professional?", "Professional has more advanced features; Standard suits typical diagrams."),
                ("Is it perpetual?", "Yes—ESD licence."),
                ("Windows only?", "Yes."),
                ("How do I activate?", "Emailed key via Microsoft channels."),
                ("Part of Office?", "Visio is a separate product—not automatically included in Home suites."),
            ],
            "fr": [
                ("Standard ou Professional ?", "Professional est plus avancé ; Standard pour les diagrammes typiques."),
                ("Perpétuelle ?", "Oui — licence ESD."),
                ("Windows uniquement ?", "Oui."),
                ("Activation ?", "Code reçu via Microsoft."),
                ("Inclus dans Office ?", "Visio est un produit séparé, pas inclus automatiquement dans Home."),
            ],
            "de": [
                ("Standard oder Professional?", "Professional ist umfangreicher; Standard für typische Diagramme."),
                ("Dauerhaft?", "Ja — ESD-Lizenz."),
                ("Nur Windows?", "Ja."),
                ("Aktivierung?", "E-Mail-Key über Microsoft."),
                ("Teil von Office?", "Visio ist ein separates Produkt — nicht automatisch in Home-Suiten."),
            ],
            "es": [
                ("¿Standard o Professional?", "Professional es más avanzada; Standard para diagramas típicos."),
                ("¿Es perpetua?", "Sí: licencia ESD."),
                ("¿Solo Windows?", "Sí."),
                ("¿Cómo se activa?", "Clave del email vía Microsoft."),
                ("¿Va con Office?", "Visio es un producto aparte, no incluido automáticamente en Home."),
            ],
        },
    },
)

PRODUCTS["visio-professional-2024"] = _project_or_visio(
    "visio-professional-2024",
    "Visio",
    "Professional 2024",
    True,
    {
        "features_title": L(
            it="Visio Professional 2024",
            en="Visio Professional 2024",
            fr="Visio Professional 2024",
            de="Visio Professional 2024",
            es="Visio Professional 2024",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Edizione", "Professional", "Microsoft Visio Professional 2024 in licenza perpetua ESD per Windows, per diagrammi avanzati."),
                ("c4", "teal", None, "Funzioni Pro", "Capacità Professional rispetto a Standard, secondo Microsoft."),
                ("c4", "purple", "Piattaforma", "Windows", "Edizione desktop Windows."),
                ("c4", None, "Consegna", "ESD email", "Codice dopo il pagamento."),
                ("c4", None, "Attivazione", "Ufficiale", "Attivazione sui canali Microsoft."),
                ("c4", "dark", "Nota", "Licenza desktop", "Non è un piano Visio in abbonamento Microsoft 365."),
            ],
            "en": [
                ("c8", "blue", "Edition", "Professional", "Microsoft Visio Professional 2024 as a perpetual ESD licence for Windows, for advanced diagrams."),
                ("c4", "teal", None, "Pro features", "Professional capabilities versus Standard, per Microsoft."),
                ("c4", "purple", "Platform", "Windows", "Windows desktop edition."),
                ("c4", None, "Delivery", "ESD email", "Key after payment."),
                ("c4", None, "Activation", "Official", "Activate via Microsoft channels."),
                ("c4", "dark", "Note", "Desktop licence", "Not a Visio Microsoft 365 subscription plan."),
            ],
            "fr": [
                ("c8", "blue", "Édition", "Professional", "Microsoft Visio Professional 2024 en licence ESD perpétuelle pour Windows."),
                ("c4", "teal", None, "Fonctions Pro", "Capacités Professional par rapport à Standard."),
                ("c4", "purple", "Plateforme", "Windows", "Édition de bureau Windows."),
                ("c4", None, "Livraison", "ESD e-mail", "Code après paiement."),
                ("c4", None, "Activation", "Officielle", "Activation via Microsoft."),
                ("c4", "dark", "Note", "Licence bureau", "Pas un abonnement Visio Microsoft 365."),
            ],
            "de": [
                ("c8", "blue", "Edition", "Professional", "Microsoft Visio Professional 2024 als ESD-Dauerlizenz für Windows."),
                ("c4", "teal", None, "Pro-Funktionen", "Professional-Funktionen gegenüber Standard."),
                ("c4", "purple", "Plattform", "Windows", "Windows-Desktop-Edition."),
                ("c4", None, "Lieferung", "ESD-E-Mail", "Key nach der Zahlung."),
                ("c4", None, "Aktivierung", "Offiziell", "Aktivierung über Microsoft."),
                ("c4", "dark", "Hinweis", "Desktop-Lizenz", "Kein Visio-Microsoft-365-Abo."),
            ],
            "es": [
                ("c8", "blue", "Edición", "Professional", "Microsoft Visio Professional 2024 con licencia ESD perpetua para Windows."),
                ("c4", "teal", None, "Funciones Pro", "Capacidades Professional frente a Standard."),
                ("c4", "purple", "Plataforma", "Windows", "Edición de escritorio Windows."),
                ("c4", None, "Entrega", "ESD email", "Clave tras el pago."),
                ("c4", None, "Activación", "Oficial", "Activa por canales Microsoft."),
                ("c4", "dark", "Nota", "Licencia de escritorio", "No es un plan Visio de Microsoft 365."),
            ],
        },
        "faq": {
            "it": [
                ("Differenza con Visio Standard?", "Professional offre funzioni più avanzate per diagrammi e modelli."),
                ("È perpetua?", "Sì: licenza ESD."),
                ("Solo Windows?", "Sì."),
                ("Come si attiva?", "Codice email sui canali Microsoft."),
                ("È Microsoft 365 Visio?", "No: è la licenza desktop perpetua descritta in scheda."),
            ],
            "en": [
                ("Difference vs Visio Standard?", "Professional offers more advanced diagramming and templates."),
                ("Is it perpetual?", "Yes—ESD licence."),
                ("Windows only?", "Yes."),
                ("How do I activate?", "Emailed key via Microsoft channels."),
                ("Is it Microsoft 365 Visio?", "No—this is the perpetual desktop licence described."),
            ],
            "fr": [
                ("Différence avec Standard ?", "Professional offre plus de fonctions avancées."),
                ("Perpétuelle ?", "Oui — licence ESD."),
                ("Windows uniquement ?", "Oui."),
                ("Activation ?", "Code reçu via Microsoft."),
                ("Visio Microsoft 365 ?", "Non — licence de bureau perpétuelle décrite ici."),
            ],
            "de": [
                ("Unterschied zu Standard?", "Professional bietet mehr erweiterte Funktionen."),
                ("Dauerhaft?", "Ja — ESD-Lizenz."),
                ("Nur Windows?", "Ja."),
                ("Aktivierung?", "E-Mail-Key über Microsoft."),
                ("Microsoft-365-Visio?", "Nein — hier die Desktop-Dauerlizenz."),
            ],
            "es": [
                ("¿Diferencia con Standard?", "Professional ofrece más funciones avanzadas."),
                ("¿Es perpetua?", "Sí: licencia ESD."),
                ("¿Solo Windows?", "Sí."),
                ("¿Cómo se activa?", "Clave del email vía Microsoft."),
                ("¿Es Visio de Microsoft 365?", "No: es la licencia de escritorio perpetua descrita."),
            ],
        },
    },
)


PRODUCTS["microsoft-365-business-standard"] = {
    "apps": ["word", "excel", "powerpoint", "outlook", "onenote"],
    "title_html": L(
        it='Microsoft 365 <span>Business Standard</span>',
        en='Microsoft 365 <span>Business Standard</span>',
        fr='Microsoft 365 <span>Business Standard</span>',
        de='Microsoft 365 <span>Business Standard</span>',
        es='Microsoft 365 <span>Business Standard</span>',
    ),
    "eyebrow": L(
        it="Abbonamento Microsoft 365 · Business",
        en="Microsoft 365 subscription · Business",
        fr="Abonnement Microsoft 365 · Business",
        de="Microsoft-365-Abonnement · Business",
        es="Suscripción Microsoft 365 · Business",
    ),
    "desc": L(
        it="Microsoft 365 Business Standard: app Office premium per le aziende, con servizi cloud secondo l'offerta Microsoft del piano. Consegna del codice via email dopo l'acquisto.",
        en="Microsoft 365 Business Standard: premium Office apps for business, with cloud services per Microsoft’s plan offer. Key delivered by email after purchase.",
        fr="Microsoft 365 Business Standard : apps Office premium pour les entreprises, services cloud selon l'offre Microsoft. Code par e-mail après l'achat.",
        de="Microsoft 365 Business Standard: Premium-Office-Apps für Unternehmen mit Cloud-Diensten laut Microsoft-Plan. Key per E-Mail nach dem Kauf.",
        es="Microsoft 365 Business Standard: apps Office premium para empresas, con servicios cloud según el plan Microsoft. Clave por email tras la compra.",
    ),
    "pills": {
        lg: [("outlook", "Business"), ("word", "Apps desktop"), (None, "Cloud")]
        for lg in LANGS
    },
    "features_title": L(
        it="Business Standard per team e PMI",
        en="Business Standard for teams and SMBs",
        fr="Business Standard pour équipes et TPE/PME",
        de="Business Standard für Teams und KMU",
        es="Business Standard para equipos y pymes",
    ),
    "features": {
        "it": [
            ("c8", "blue", "Piano", "Business Standard", "Abbonamento Microsoft 365 pensato per uso aziendale, con app desktop e servizi cloud secondo le condizioni Microsoft del piano."),
            ("c4", "teal", None, "App Office", "Word, Excel, PowerPoint, Outlook e altre app incluse nel piano, dove previste da Microsoft."),
            ("c4", "purple", "Cloud", "Servizi online", "Funzioni cloud e collaborazione tipiche di Microsoft 365 Business, come da offerta ufficiale."),
            ("c4", None, "Consegna", "Digitale", "Codice e istruzioni via email dopo il pagamento."),
            ("c4", None, "Attivazione", "Account Microsoft", "Attivi sul portale ufficiale e associ l'abbonamento all'account aziendale."),
            ("c4", "dark", "Nota", "Non è perpetua", "A differenza di Office 2024/2021, è un abbonamento: durata e rinnovo seguono le condizioni d'ordine e Microsoft."),
        ],
        "en": [
            ("c8", "blue", "Plan", "Business Standard", "Microsoft 365 subscription for business use, with desktop apps and cloud services per Microsoft’s plan terms."),
            ("c4", "teal", None, "Office apps", "Word, Excel, PowerPoint, Outlook and other apps included in the plan where Microsoft provides them."),
            ("c4", "purple", "Cloud", "Online services", "Cloud and collaboration features typical of Microsoft 365 Business, per the official offer."),
            ("c4", None, "Delivery", "Digital", "Key and instructions by email after payment."),
            ("c4", None, "Activation", "Microsoft account", "Activate on the official portal and link the subscription to the business account."),
            ("c4", "dark", "Note", "Not perpetual", "Unlike Office 2024/2021, this is a subscription—term and renewal follow order and Microsoft terms."),
        ],
        "fr": [
            ("c8", "blue", "Offre", "Business Standard", "Abonnement Microsoft 365 pour usage pro, apps de bureau et cloud selon Microsoft."),
            ("c4", "teal", None, "Apps Office", "Word, Excel, PowerPoint, Outlook et autres apps du plan."),
            ("c4", "purple", "Cloud", "Services en ligne", "Fonctions cloud et collaboration Microsoft 365 Business."),
            ("c4", None, "Livraison", "Numérique", "Code par e-mail après paiement."),
            ("c4", None, "Activation", "Compte Microsoft", "Activation sur le portail officiel."),
            ("c4", "dark", "Note", "Pas perpétuel", "Contrairement à Office 2024/2021, c'est un abonnement."),
        ],
        "de": [
            ("c8", "blue", "Plan", "Business Standard", "Microsoft-365-Abonnement für den Unternehmenseinsatz mit Desktop-Apps und Cloud laut Microsoft."),
            ("c4", "teal", None, "Office-Apps", "Word, Excel, PowerPoint, Outlook u. a. Apps des Plans."),
            ("c4", "purple", "Cloud", "Onlinedienste", "Cloud- und Kollaborationsfunktionen von Microsoft 365 Business."),
            ("c4", None, "Lieferung", "Digital", "Key per E-Mail nach der Zahlung."),
            ("c4", None, "Aktivierung", "Microsoft-Konto", "Aktivierung im offiziellen Portal."),
            ("c4", "dark", "Hinweis", "Keine Dauerlizenz", "Im Gegensatz zu Office 2024/2021 ein Abonnement."),
        ],
        "es": [
            ("c8", "blue", "Plan", "Business Standard", "Suscripción Microsoft 365 para uso empresarial, con apps de escritorio y cloud según Microsoft."),
            ("c4", "teal", None, "Apps Office", "Word, Excel, PowerPoint, Outlook y otras apps del plan."),
            ("c4", "purple", "Cloud", "Servicios online", "Funciones cloud y colaboración de Microsoft 365 Business."),
            ("c4", None, "Entrega", "Digital", "Clave por email tras el pago."),
            ("c4", None, "Activación", "Cuenta Microsoft", "Activa en el portal oficial."),
            ("c4", "dark", "Nota", "No es perpetua", "A diferencia de Office 2024/2021, es una suscripción."),
        ],
    },
    "apps_title": L(
        it="App tipiche del piano",
        en="Typical apps in the plan",
        fr="Apps typiques du plan",
        de="Typische Apps im Plan",
        es="Apps típicas del plan",
    ),
    "faq": {
        "it": [
            ("È un abbonamento o una licenza perpetua?", "È un abbonamento Microsoft 365 Business Standard, non una licenza Office perpetua."),
            ("Differenza con Microsoft 365 Personal?", "Business Standard è pensato per uso aziendale; Personal è per uso individuale. Confronta le schede e le condizioni Microsoft."),
            ("Quanti utenti/dispositivi?", "Segui le condizioni Microsoft del piano Business Standard indicate in scheda (es. riferimenti a utente/dispositivi)."),
            ("Come si attiva?", "Con il codice e le istruzioni via email sul portale ufficiale Microsoft."),
            ("Include Teams?", "Le app e i servizi inclusi dipendono dall'offerta Microsoft del piano al momento dell'acquisto; verifica email e documentazione ufficiale."),
        ],
        "en": [
            ("Subscription or perpetual?", "It is a Microsoft 365 Business Standard subscription, not a perpetual Office licence."),
            ("Difference vs Microsoft 365 Personal?", "Business Standard is for business use; Personal is for individual use. Compare pages and Microsoft terms."),
            ("Users/devices?", "Follow Microsoft’s Business Standard plan terms shown on the page (e.g. user/device references)."),
            ("How do I activate?", "With the emailed key and instructions on Microsoft’s official portal."),
            ("Includes Teams?", "Included apps/services depend on Microsoft’s plan offer at purchase—check email and official docs."),
        ],
        "fr": [
            ("Abonnement ou perpétuel ?", "Abonnement Microsoft 365 Business Standard, pas une licence Office perpétuelle."),
            ("Différence avec Personal ?", "Business Standard est pour l'entreprise ; Personal pour un usage individuel."),
            ("Utilisateurs/appareils ?", "Selon les conditions Microsoft Business Standard indiquées."),
            ("Activation ?", "Code et instructions reçus sur le portail Microsoft."),
            ("Teams inclus ?", "Selon l'offre Microsoft du plan au moment de l'achat."),
        ],
        "de": [
            ("Abo oder Dauerlizenz?", "Microsoft-365-Business-Standard-Abonnement, keine Office-Dauerlizenz."),
            ("Unterschied zu Personal?", "Business Standard für Unternehmen; Personal für Privatnutzer."),
            ("Nutzer/Geräte?", "Gemäß Microsoft Business Standard auf der Seite."),
            ("Aktivierung?", "E-Mail-Key und Anleitung im Microsoft-Portal."),
            ("Teams inklusive?", "Abhängig vom Microsoft-Angebot zum Kaufzeitpunkt."),
        ],
        "es": [
            ("¿Suscripción o perpetua?", "Es una suscripción Microsoft 365 Business Standard, no una licencia Office perpetua."),
            ("¿Diferencia con Personal?", "Business Standard es para empresas; Personal para uso individual."),
            ("¿Usuarios/dispositivos?", "Según las condiciones Microsoft Business Standard de la ficha."),
            ("¿Cómo se activa?", "Con la clave e instrucciones del email en el portal Microsoft."),
            ("¿Incluye Teams?", "Depende de la oferta Microsoft del plan en el momento de la compra."),
        ],
    },
}


def get_office_apps_content(slug):
    return PRODUCTS.get(slug)
