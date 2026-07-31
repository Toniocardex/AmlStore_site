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
    return {
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
        "features_title": L(
            it="Project Professional 2024",
            en="Project Professional 2024",
            fr="Project Professional 2024",
            de="Project Professional 2024",
            es="Project Professional 2024",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Edizione", "Professional", "Microsoft Project Professional 2024 in licenza perpetua ESD per Windows, per scenari di project management avanzati."),
                ("c4", "teal", None, "Pianificazione avanzata", "Funzioni Professional rispetto a Standard, secondo Microsoft."),
                ("c4", "purple", "Piattaforma", "Windows", "Edizione desktop Windows."),
                ("c4", None, "Consegna", "ESD email", "Codice e istruzioni dopo il pagamento."),
                ("c4", None, "Attivazione", "Ufficiale", "Attivazione sui canali Microsoft."),
                ("c4", "dark", "Nota", "Non è Microsoft 365", "Licenza perpetua descritta in scheda, non un piano Project online in abbonamento."),
            ],
            "en": [
                ("c8", "blue", "Edition", "Professional", "Microsoft Project Professional 2024 as a perpetual ESD licence for Windows, for advanced project-management scenarios."),
                ("c4", "teal", None, "Advanced planning", "Professional features versus Standard, per Microsoft."),
                ("c4", "purple", "Platform", "Windows", "Windows desktop edition."),
                ("c4", None, "Delivery", "ESD email", "Key and instructions after payment."),
                ("c4", None, "Activation", "Official", "Activate via Microsoft channels."),
                ("c4", "dark", "Note", "Not Microsoft 365", "Perpetual licence as described—not a Project online subscription plan."),
            ],
            "fr": [
                ("c8", "blue", "Édition", "Professional", "Microsoft Project Professional 2024 en licence ESD perpétuelle pour Windows."),
                ("c4", "teal", None, "Planification avancée", "Fonctions Professional par rapport à Standard."),
                ("c4", "purple", "Plateforme", "Windows", "Édition de bureau Windows."),
                ("c4", None, "Livraison", "ESD e-mail", "Code après paiement."),
                ("c4", None, "Activation", "Officielle", "Activation via les canaux Microsoft."),
                ("c4", "dark", "Note", "Pas Microsoft 365", "Licence perpétuelle — pas un abonnement Project en ligne."),
            ],
            "de": [
                ("c8", "blue", "Edition", "Professional", "Microsoft Project Professional 2024 als ESD-Dauerlizenz für Windows."),
                ("c4", "teal", None, "Erweiterte Planung", "Professional-Funktionen gegenüber Standard."),
                ("c4", "purple", "Plattform", "Windows", "Windows-Desktop-Edition."),
                ("c4", None, "Lieferung", "ESD-E-Mail", "Key nach der Zahlung."),
                ("c4", None, "Aktivierung", "Offiziell", "Aktivierung über Microsoft-Kanäle."),
                ("c4", "dark", "Hinweis", "Kein Microsoft 365", "Dauerlizenz — kein Project-Online-Abo."),
            ],
            "es": [
                ("c8", "blue", "Edición", "Professional", "Microsoft Project Professional 2024 con licencia ESD perpetua para Windows."),
                ("c4", "teal", None, "Planificación avanzada", "Funciones Professional frente a Standard."),
                ("c4", "purple", "Plataforma", "Windows", "Edición de escritorio Windows."),
                ("c4", None, "Entrega", "ESD email", "Clave tras el pago."),
                ("c4", None, "Activación", "Oficial", "Activa por canales Microsoft."),
                ("c4", "dark", "Nota", "No es Microsoft 365", "Licencia perpetua, no un plan Project online."),
            ],
        },
        "faq": {
            "it": [
                ("Serve Project Standard o Professional?", "Professional è l'edizione più completa. Se ti basta la pianificazione base, valuta Standard."),
                ("È perpetua?", "Sì: licenza ESD una tantum."),
                ("Solo Windows?", "Sì, come da scheda."),
                ("Come si attiva?", "Codice email sui portali/istruzioni Microsoft."),
                ("Include Project Online?", "Questa scheda è la licenza desktop perpetua descritta, non un abbonamento cloud."),
            ],
            "en": [
                ("Standard or Professional?", "Professional is the fuller edition. For basic planning, consider Standard."),
                ("Is it perpetual?", "Yes—one-time ESD licence."),
                ("Windows only?", "Yes, as listed."),
                ("How do I activate?", "Emailed key via Microsoft portals/instructions."),
                ("Includes Project Online?", "This page is the perpetual desktop licence described, not a cloud subscription."),
            ],
            "fr": [
                ("Standard ou Professional ?", "Professional est plus complet ; pour l'essentiel, voyez Standard."),
                ("Perpétuelle ?", "Oui — licence ESD unique."),
                ("Windows uniquement ?", "Oui."),
                ("Activation ?", "Code reçu via Microsoft."),
                ("Project Online inclus ?", "Non — licence de bureau perpétuelle décrite ici."),
            ],
            "de": [
                ("Standard oder Professional?", "Professional ist umfangreicher; für Basis eher Standard."),
                ("Dauerhaft?", "Ja — einmalige ESD-Lizenz."),
                ("Nur Windows?", "Ja."),
                ("Aktivierung?", "E-Mail-Key über Microsoft."),
                ("Project Online?", "Nein — hier die beschriebene Desktop-Dauerlizenz."),
            ],
            "es": [
                ("¿Standard o Professional?", "Professional es la edición más completa; para lo básico, Standard."),
                ("¿Es perpetua?", "Sí: licencia ESD de compra única."),
                ("¿Solo Windows?", "Sí."),
                ("¿Cómo se activa?", "Clave del email vía Microsoft."),
                ("¿Incluye Project Online?", "No: es la licencia de escritorio perpetua descrita."),
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
