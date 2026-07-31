#!/usr/bin/env python3
"""Rich content for Office 2021 perpetual SKUs (all 5 locales)."""

from product_content_office import APPS_HOME, APPS_HOME_BUSINESS, APPS_PRO_PLUS

LANGS = ("it", "en", "fr", "de", "es")


def L(**kwargs):
    """Build {lang: text} from keyword args it/en/fr/de/es."""
    return {k: kwargs[k] for k in LANGS}


def pills_home():
    return {lg: [("word", "Word"), ("excel", "Excel"), ("powerpoint", "PowerPoint"), (None, "PC / Mac")] for lg in LANGS}


def pills_hb():
    return {lg: [("word", "Word"), ("excel", "Excel"), ("powerpoint", "PowerPoint"), ("outlook", "Outlook")] for lg in LANGS}


def pills_mac():
    return {lg: [("word", "Word"), ("excel", "Excel"), ("powerpoint", "PowerPoint"), ("outlook", "Outlook")] for lg in LANGS}


def feats(rows_by_lang):
    return rows_by_lang


def faq(rows_by_lang):
    return rows_by_lang


PRODUCTS = {
    "office-2021-home-student": {
        "apps": APPS_HOME,
        "title_html": L(
            it='Office 2021 <span>Home &amp; Student</span>',
            en='Office 2021 <span>Home &amp; Student</span>',
            fr='Office 2021 <span>Home &amp; Student</span>',
            de='Office 2021 <span>Home &amp; Student</span>',
            es='Office 2021 <span>Home &amp; Student</span>',
        ),
        "eyebrow": L(
            it="Licenza perpetua · Windows o Mac",
            en="Perpetual licence · Windows or Mac",
            fr="Licence perpétuelle · Windows ou Mac",
            de="Dauerlizenz · Windows oder Mac",
            es="Licencia perpetua · Windows o Mac",
        ),
        "desc": L(
            it="Office 2021 Home & Student: Word, Excel e PowerPoint per casa e studio su Windows o Mac. Licenza digitale originale con consegna del codice via email.",
            en="Office 2021 Home & Student: Word, Excel and PowerPoint for home and study on Windows or Mac. Genuine digital licence with email key delivery.",
            fr="Office 2021 Home & Student : Word, Excel et PowerPoint pour la maison et les études sur Windows ou Mac. Licence numérique originale, code par e-mail.",
            de="Office 2021 Home & Student: Word, Excel und PowerPoint für Zuhause und Studium unter Windows oder Mac. Originale digitale Lizenz mit Key per E-Mail.",
            es="Office 2021 Home & Student: Word, Excel y PowerPoint para hogar y estudio en Windows o Mac. Licencia digital original con clave por email.",
        ),
        "pills": pills_home(),
        "features_title": L(
            it="Office 2021 essenziale, senza abbonamento",
            en="Essential Office 2021, no subscription",
            fr="Office 2021 essentiel, sans abonnement",
            de="Office 2021 Essential — ohne Abo",
            es="Office 2021 esencial, sin suscripción",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Licenza", "Home & Student 2021", "Licenza perpetua ESD per uso domestico e scolastico: Word, Excel e PowerPoint secondo le condizioni Microsoft 2021."),
                ("c4", "teal", None, "3 app desktop", "Documenti, fogli e presentazioni con le app classiche Office."),
                ("c4", "purple", "Piattaforma", "Windows o Mac", "Edizione per Windows e macOS supportati per Office 2021."),
                ("c4", None, "Consegna", "Digitale via email", "Codice e istruzioni dopo il pagamento."),
                ("c4", None, "Attivazione", "setup.office.com", "Attivi sul portale Microsoft e installi le app 2021."),
                ("c4", "dark", "Nota", "Versione 2021", "Suite perpetua 2021: non include gli aggiornamenti continui di Microsoft 365."),
            ],
            "en": [
                ("c8", "blue", "Licence", "Home & Student 2021", "Perpetual ESD licence for home and study: Word, Excel and PowerPoint under Microsoft 2021 terms."),
                ("c4", "teal", None, "3 desktop apps", "Documents, sheets and presentations with classic Office apps."),
                ("c4", "purple", "Platform", "Windows or Mac", "Edition for Windows and macOS supported for Office 2021."),
                ("c4", None, "Delivery", "Digital by email", "Key and instructions after payment."),
                ("c4", None, "Activation", "setup.office.com", "Activate on Microsoft’s portal and install the 2021 apps."),
                ("c4", "dark", "Note", "2021 release", "Perpetual 2021 suite—not Microsoft 365 continuous feature updates."),
            ],
            "fr": [
                ("c8", "blue", "Licence", "Home & Student 2021", "Licence ESD perpétuelle pour la maison et les études : Word, Excel et PowerPoint selon Microsoft 2021."),
                ("c4", "teal", None, "3 apps de bureau", "Documents, tableurs et présentations avec les apps Office classiques."),
                ("c4", "purple", "Plateforme", "Windows ou Mac", "Édition pour Windows et macOS pris en charge pour Office 2021."),
                ("c4", None, "Livraison", "Numérique", "Code et instructions après paiement."),
                ("c4", None, "Activation", "setup.office.com", "Activation sur le portail Microsoft et installation des apps 2021."),
                ("c4", "dark", "Note", "Version 2021", "Suite perpétuelle 2021 — pas les mises à jour continues Microsoft 365."),
            ],
            "de": [
                ("c8", "blue", "Lizenz", "Home & Student 2021", "ESD-Dauerlizenz für Zuhause und Studium: Word, Excel und PowerPoint gemäß Microsoft 2021."),
                ("c4", "teal", None, "3 Desktop-Apps", "Dokumente, Tabellen und Präsentationen mit klassischen Office-Apps."),
                ("c4", "purple", "Plattform", "Windows oder Mac", "Für Windows und macOS, die Office 2021 unterstützen."),
                ("c4", None, "Lieferung", "Digital", "Key und Anleitung nach der Zahlung."),
                ("c4", None, "Aktivierung", "setup.office.com", "Aktivierung im Microsoft-Portal und Installation der 2021-Apps."),
                ("c4", "dark", "Hinweis", "Version 2021", "Dauerlizenz-Suite 2021 — keine laufenden Microsoft-365-Updates."),
            ],
            "es": [
                ("c8", "blue", "Licencia", "Home & Student 2021", "Licencia ESD perpetua para hogar y estudio: Word, Excel y PowerPoint según Microsoft 2021."),
                ("c4", "teal", None, "3 apps de escritorio", "Documentos, hojas y presentaciones con las apps clásicas de Office."),
                ("c4", "purple", "Plataforma", "Windows o Mac", "Edición para Windows y macOS admitidos en Office 2021."),
                ("c4", None, "Entrega", "Digital", "Clave e instrucciones tras el pago."),
                ("c4", None, "Activación", "setup.office.com", "Activa en el portal Microsoft e instala las apps 2021."),
                ("c4", "dark", "Nota", "Versión 2021", "Suite perpetua 2021: no incluye actualizaciones continuas de Microsoft 365."),
            ],
        },
        "apps_title": L(
            it="App in Home & Student 2021",
            en="Apps in Home & Student 2021",
            fr="Apps Home & Student 2021",
            de="Apps in Home & Student 2021",
            es="Apps en Home & Student 2021",
        ),
        "faq": {
            "it": [
                ("Quali app include?", "Word, Excel e PowerPoint. Outlook non fa parte di Home & Student."),
                ("È un abbonamento?", "No: licenza perpetua 2021, non Microsoft 365."),
                ("Windows o Mac?", "Sì, dove indicato in scheda; segui requisiti e procedura Microsoft per la piattaforma scelta."),
                ("Come si attiva?", "Con il codice via email su setup.office.com e installazione da office.com."),
                ("Differenza con Office 2024?", "2024 è più recente. Scegli 2021 se ti serve quella generazione o le condizioni di questa scheda."),
            ],
            "en": [
                ("Which apps are included?", "Word, Excel and PowerPoint. Outlook is not part of Home & Student."),
                ("Is it a subscription?", "No—perpetual 2021 licence, not Microsoft 365."),
                ("Windows or Mac?", "Yes where indicated on this page; follow Microsoft’s requirements for your platform."),
                ("How do I activate?", "With the emailed key at setup.office.com and install via office.com."),
                ("Difference vs Office 2024?", "2024 is newer. Choose 2021 if you need that generation or this page’s offer."),
            ],
            "fr": [
                ("Quelles apps ?", "Word, Excel et PowerPoint. Outlook n'est pas inclus dans Home & Student."),
                ("Abonnement ?", "Non — licence perpétuelle 2021, pas Microsoft 365."),
                ("Windows ou Mac ?", "Oui si indiqué sur la fiche ; suivez les exigences Microsoft."),
                ("Activation ?", "Code reçu sur setup.office.com, installation via office.com."),
                ("Différence avec 2024 ?", "2024 est plus récent. Choisissez 2021 pour cette génération ou cette offre."),
            ],
            "de": [
                ("Welche Apps?", "Word, Excel und PowerPoint. Outlook gehört nicht zu Home & Student."),
                ("Abo?", "Nein — Dauerlizenz 2021, kein Microsoft 365."),
                ("Windows oder Mac?", "Ja, wenn auf der Seite angegeben; Microsoft-Anforderungen beachten."),
                ("Aktivierung?", "E-Mail-Key unter setup.office.com, Installation über office.com."),
                ("Unterschied zu 2024?", "2024 ist neuer. 2021 wählen, wenn Sie diese Generation oder dieses Angebot brauchen."),
            ],
            "es": [
                ("¿Qué apps incluye?", "Word, Excel y PowerPoint. Outlook no forma parte de Home & Student."),
                ("¿Es suscripción?", "No: licencia perpetua 2021, no Microsoft 365."),
                ("¿Windows o Mac?", "Sí donde lo indique la ficha; sigue los requisitos Microsoft."),
                ("¿Cómo se activa?", "Con la clave del email en setup.office.com e instalación desde office.com."),
                ("¿Diferencia con 2024?", "2024 es más reciente. Elige 2021 si necesitas esa generación o esta oferta."),
            ],
        },
    },
    "office-2021-home-business": {
        "apps": APPS_HOME_BUSINESS,
        "title_html": L(
            it='Office 2021 <span>Home &amp; Business</span>',
            en='Office 2021 <span>Home &amp; Business</span>',
            fr='Office 2021 <span>Home &amp; Business</span>',
            de='Office 2021 <span>Home &amp; Business</span>',
            es='Office 2021 <span>Home &amp; Business</span>',
        ),
        "eyebrow": L(
            it="Licenza perpetua · PC / Mac",
            en="Perpetual licence · PC / Mac",
            fr="Licence perpétuelle · PC / Mac",
            de="Dauerlizenz · PC / Mac",
            es="Licencia perpetua · PC / Mac",
        ),
        "desc": L(
            it="Office 2021 Home & Business: Word, Excel, PowerPoint e Outlook su PC o Mac. Licenza digitale ESD senza abbonamento, codice via email.",
            en="Office 2021 Home & Business: Word, Excel, PowerPoint and Outlook on PC or Mac. ESD digital licence, no subscription, key by email.",
            fr="Office 2021 Home & Business : Word, Excel, PowerPoint et Outlook sur PC ou Mac. Licence ESD sans abonnement, code par e-mail.",
            de="Office 2021 Home & Business: Word, Excel, PowerPoint und Outlook auf PC oder Mac. ESD-Lizenz ohne Abo, Key per E-Mail.",
            es="Office 2021 Home & Business: Word, Excel, PowerPoint y Outlook en PC o Mac. Licencia ESD sin suscripción, clave por email.",
        ),
        "pills": pills_hb(),
        "features_title": L(
            it="Casa e lavoro con Outlook 2021",
            en="Home and work with Outlook 2021",
            fr="Maison et travail avec Outlook 2021",
            de="Zuhause und Arbeit mit Outlook 2021",
            es="Hogar y trabajo con Outlook 2021",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Licenza", "Home & Business 2021", "Licenza perpetua ESD per un PC o Mac, con Outlook oltre a Word, Excel e PowerPoint."),
                ("c4", "teal", None, "Outlook incluso", "Posta, calendario e contatti con Outlook desktop."),
                ("c4", "purple", "Piattaforma", "PC o Mac", "Edizione compatibile con Windows e macOS supportati per Office 2021."),
                ("c4", None, "Consegna", "Email in pochi minuti", "Codice e istruzioni dopo il pagamento."),
                ("c4", None, "Attivazione", "Portale Microsoft", "Attivazione su setup.office.com e installazione da office.com."),
                ("c4", "dark", "Ideale per", "Professionisti", "Quando serve Outlook senza passare a Microsoft 365."),
            ],
            "en": [
                ("c8", "blue", "Licence", "Home & Business 2021", "Perpetual ESD licence for one PC or Mac, with Outlook plus Word, Excel and PowerPoint."),
                ("c4", "teal", None, "Outlook included", "Mail, calendar and contacts with desktop Outlook."),
                ("c4", "purple", "Platform", "PC or Mac", "For Windows and macOS supported for Office 2021."),
                ("c4", None, "Delivery", "Email in minutes", "Key and instructions after payment."),
                ("c4", None, "Activation", "Microsoft portal", "Activate at setup.office.com and install from office.com."),
                ("c4", "dark", "Best for", "Professionals", "When you need Outlook without moving to Microsoft 365."),
            ],
            "fr": [
                ("c8", "blue", "Licence", "Home & Business 2021", "Licence ESD perpétuelle pour un PC ou Mac, avec Outlook plus Word, Excel et PowerPoint."),
                ("c4", "teal", None, "Outlook inclus", "Messagerie, calendrier et contacts avec Outlook de bureau."),
                ("c4", "purple", "Plateforme", "PC ou Mac", "Windows et macOS pris en charge pour Office 2021."),
                ("c4", None, "Livraison", "E-mail rapide", "Code et instructions après paiement."),
                ("c4", None, "Activation", "Portail Microsoft", "Activation sur setup.office.com, installation via office.com."),
                ("c4", "dark", "Idéal pour", "Professionnels", "Quand vous voulez Outlook sans Microsoft 365."),
            ],
            "de": [
                ("c8", "blue", "Lizenz", "Home & Business 2021", "ESD-Dauerlizenz für einen PC oder Mac, mit Outlook plus Word, Excel und PowerPoint."),
                ("c4", "teal", None, "Outlook inklusive", "E-Mail, Kalender und Kontakte mit Desktop-Outlook."),
                ("c4", "purple", "Plattform", "PC oder Mac", "Für Windows und macOS mit Office-2021-Unterstützung."),
                ("c4", None, "Lieferung", "E-Mail in Minuten", "Key und Anleitung nach der Zahlung."),
                ("c4", None, "Aktivierung", "Microsoft-Portal", "Aktivierung unter setup.office.com, Installation über office.com."),
                ("c4", "dark", "Ideal für", "Selbstständige", "Outlook ohne Wechsel zu Microsoft 365."),
            ],
            "es": [
                ("c8", "blue", "Licencia", "Home & Business 2021", "Licencia ESD perpetua para un PC o Mac, con Outlook además de Word, Excel y PowerPoint."),
                ("c4", "teal", None, "Outlook incluido", "Correo, calendario y contactos con Outlook de escritorio."),
                ("c4", "purple", "Plataforma", "PC o Mac", "Para Windows y macOS admitidos en Office 2021."),
                ("c4", None, "Entrega", "Email en minutos", "Clave e instrucciones tras el pago."),
                ("c4", None, "Activación", "Portal Microsoft", "Activa en setup.office.com e instala desde office.com."),
                ("c4", "dark", "Ideal para", "Profesionales", "Cuando necesitas Outlook sin pasar a Microsoft 365."),
            ],
        },
        "apps_title": L(
            it="App in Home & Business 2021",
            en="Apps in Home & Business 2021",
            fr="Apps Home & Business 2021",
            de="Apps in Home & Business 2021",
            es="Apps en Home & Business 2021",
        ),
        "faq": {
            "it": [
                ("Differenza con Home & Student?", "Home & Business aggiunge Outlook alle tre app principali."),
                ("È perpetua?", "Sì: licenza ESD una tantum, non abbonamento Microsoft 365."),
                ("PC e Mac?", "Questa scheda copre PC/Mac come da titolo prodotto; segui le istruzioni Microsoft per la piattaforma."),
                ("Come si attiva?", "setup.office.com con il codice email, poi installazione da office.com."),
                ("Serve OneDrive 1 TB?", "No in questa edizione perpetua. Per cloud e aggiornamenti continui valuta Microsoft 365."),
            ],
            "en": [
                ("Difference vs Home & Student?", "Home & Business adds Outlook to the three core apps."),
                ("Is it perpetual?", "Yes—one-time ESD licence, not a Microsoft 365 subscription."),
                ("PC and Mac?", "This page covers PC/Mac as titled; follow Microsoft’s steps for your platform."),
                ("How do I activate?", "setup.office.com with the emailed key, then install from office.com."),
                ("Do I get 1 TB OneDrive?", "Not with this perpetual edition. For cloud and continuous updates consider Microsoft 365."),
            ],
            "fr": [
                ("Différence avec Home & Student ?", "Home & Business ajoute Outlook aux trois apps principales."),
                ("Perpétuelle ?", "Oui — licence ESD unique, pas Microsoft 365."),
                ("PC et Mac ?", "Cette fiche couvre PC/Mac ; suivez Microsoft pour votre plateforme."),
                ("Activation ?", "setup.office.com avec le code, puis office.com."),
                ("OneDrive 1 To ?", "Pas avec cette édition perpétuelle. Pour le cloud, voyez Microsoft 365."),
            ],
            "de": [
                ("Unterschied zu Home & Student?", "Home & Business ergänzt Outlook um die drei Kern-Apps."),
                ("Dauerhaft?", "Ja — einmalige ESD-Lizenz, kein Microsoft 365."),
                ("PC und Mac?", "Diese Seite deckt PC/Mac ab; Microsoft-Schritte für Ihre Plattform folgen."),
                ("Aktivierung?", "setup.office.com mit E-Mail-Key, dann office.com."),
                ("1 TB OneDrive?", "Nicht bei dieser Dauerlizenz. Für Cloud eher Microsoft 365."),
            ],
            "es": [
                ("¿Diferencia con Home & Student?", "Home & Business añade Outlook a las tres apps principales."),
                ("¿Es perpetua?", "Sí: licencia ESD de compra única, no Microsoft 365."),
                ("¿PC y Mac?", "Esta ficha cubre PC/Mac; sigue los pasos Microsoft para tu plataforma."),
                ("¿Cómo se activa?", "setup.office.com con la clave del email, luego office.com."),
                ("¿Incluye 1 TB OneDrive?", "No en esta edición perpetua. Para cloud valora Microsoft 365."),
            ],
        },
    },
    "office-2021-home-business-mac": {
        "apps": APPS_HOME_BUSINESS,
        "title_html": L(
            it='Office 2021 Home &amp; Business <span>Mac</span>',
            en='Office 2021 Home &amp; Business <span>Mac</span>',
            fr='Office 2021 Home &amp; Business <span>Mac</span>',
            de='Office 2021 Home &amp; Business <span>Mac</span>',
            es='Office 2021 Home &amp; Business <span>Mac</span>',
        ),
        "eyebrow": L(
            it="Licenza perpetua · solo Mac",
            en="Perpetual licence · Mac only",
            fr="Licence perpétuelle · Mac uniquement",
            de="Dauerlizenz · nur Mac",
            es="Licencia perpetua · solo Mac",
        ),
        "desc": L(
            it="Office 2021 Home & Business per Mac: Word, Excel, PowerPoint e Outlook. Licenza digitale ESD con consegna del codice via email.",
            en="Office 2021 Home & Business for Mac: Word, Excel, PowerPoint and Outlook. Genuine ESD licence with email key delivery.",
            fr="Office 2021 Home & Business pour Mac : Word, Excel, PowerPoint et Outlook. Licence ESD originale, code par e-mail.",
            de="Office 2021 Home & Business für Mac: Word, Excel, PowerPoint und Outlook. Originale ESD-Lizenz mit Key per E-Mail.",
            es="Office 2021 Home & Business para Mac: Word, Excel, PowerPoint y Outlook. Licencia ESD original con clave por email.",
        ),
        "pills": pills_mac(),
        "features_title": L(
            it="Home & Business 2021 pensato per Mac",
            en="Home & Business 2021 built for Mac",
            fr="Home & Business 2021 pour Mac",
            de="Home & Business 2021 für den Mac",
            es="Home & Business 2021 pensado para Mac",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Piattaforma", "Edizione Mac", "Licenza perpetua ESD Home & Business 2021 destinata a Mac, secondo le condizioni Microsoft."),
                ("c4", "teal", None, "Outlook incluso", "Posta e calendario Outlook oltre a Word, Excel e PowerPoint."),
                ("c4", "purple", "Modello", "Senza abbonamento", "Acquisto una tantum della suite 2021, non Microsoft 365."),
                ("c4", None, "Consegna", "Digitale", "Codice e istruzioni via email dopo il pagamento."),
                ("c4", None, "Attivazione", "Account Microsoft", "Attivi sul portale ufficiale e installi le app Mac da Microsoft."),
                ("c4", "dark", "Nota", "Solo Mac", "Non è la variante Windows: verifica di avere un Mac compatibile con Office 2021."),
            ],
            "en": [
                ("c8", "blue", "Platform", "Mac edition", "Perpetual ESD Home & Business 2021 licence for Mac under Microsoft’s terms."),
                ("c4", "teal", None, "Outlook included", "Outlook mail and calendar plus Word, Excel and PowerPoint."),
                ("c4", "purple", "Model", "No subscription", "One-time 2021 suite purchase—not Microsoft 365."),
                ("c4", None, "Delivery", "Digital", "Key and instructions by email after payment."),
                ("c4", None, "Activation", "Microsoft account", "Activate on the official portal and install Mac apps from Microsoft."),
                ("c4", "dark", "Note", "Mac only", "Not the Windows variant—confirm your Mac meets Office 2021 requirements."),
            ],
            "fr": [
                ("c8", "blue", "Plateforme", "Édition Mac", "Licence ESD Home & Business 2021 perpétuelle pour Mac selon Microsoft."),
                ("c4", "teal", None, "Outlook inclus", "Messagerie Outlook plus Word, Excel et PowerPoint."),
                ("c4", "purple", "Modèle", "Sans abonnement", "Achat unique de la suite 2021 — pas Microsoft 365."),
                ("c4", None, "Livraison", "Numérique", "Code et instructions par e-mail après paiement."),
                ("c4", None, "Activation", "Compte Microsoft", "Activation sur le portail officiel et installation des apps Mac."),
                ("c4", "dark", "Note", "Mac uniquement", "Ce n'est pas la variante Windows — vérifiez la compatibilité Office 2021."),
            ],
            "de": [
                ("c8", "blue", "Plattform", "Mac-Edition", "ESD-Dauerlizenz Home & Business 2021 für den Mac gemäß Microsoft."),
                ("c4", "teal", None, "Outlook inklusive", "Outlook-Mail und Kalender plus Word, Excel und PowerPoint."),
                ("c4", "purple", "Modell", "Ohne Abo", "Einmalkauf der Suite 2021 — kein Microsoft 365."),
                ("c4", None, "Lieferung", "Digital", "Key und Anleitung per E-Mail nach der Zahlung."),
                ("c4", None, "Aktivierung", "Microsoft-Konto", "Aktivierung im offiziellen Portal und Installation der Mac-Apps."),
                ("c4", "dark", "Hinweis", "Nur Mac", "Keine Windows-Variante — Mac-Kompatibilität mit Office 2021 prüfen."),
            ],
            "es": [
                ("c8", "blue", "Plataforma", "Edición Mac", "Licencia ESD perpetua Home & Business 2021 para Mac según Microsoft."),
                ("c4", "teal", None, "Outlook incluido", "Correo y calendario Outlook además de Word, Excel y PowerPoint."),
                ("c4", "purple", "Modelo", "Sin suscripción", "Compra única de la suite 2021, no Microsoft 365."),
                ("c4", None, "Entrega", "Digital", "Clave e instrucciones por email tras el pago."),
                ("c4", None, "Activación", "Cuenta Microsoft", "Activa en el portal oficial e instala las apps Mac."),
                ("c4", "dark", "Nota", "Solo Mac", "No es la variante Windows: comprueba compatibilidad con Office 2021."),
            ],
        },
        "apps_title": L(
            it="App Mac in Home & Business 2021",
            en="Mac apps in Home & Business 2021",
            fr="Apps Mac Home & Business 2021",
            de="Mac-Apps in Home & Business 2021",
            es="Apps Mac en Home & Business 2021",
        ),
        "faq": {
            "it": [
                ("È solo per Mac?", "Sì: questa scheda è l'edizione Home & Business 2021 per Mac."),
                ("Include Outlook?", "Sì, insieme a Word, Excel e PowerPoint."),
                ("È un abbonamento?", "No: licenza perpetua ESD 2021."),
                ("Come si attiva?", "Con il codice ricevuto via email sul portale Microsoft e installazione delle app Mac."),
                ("Posso usarla su Windows?", "No: per Windows scegli la scheda Home & Business PC/Mac o Windows dedicata."),
            ],
            "en": [
                ("Is it Mac only?", "Yes—this page is the Home & Business 2021 Mac edition."),
                ("Does it include Outlook?", "Yes, along with Word, Excel and PowerPoint."),
                ("Is it a subscription?", "No—perpetual ESD 2021 licence."),
                ("How do I activate?", "With the emailed key on Microsoft’s portal and install the Mac apps."),
                ("Can I use it on Windows?", "No—choose the PC/Mac or Windows Home & Business page instead."),
            ],
            "fr": [
                ("Mac uniquement ?", "Oui — édition Home & Business 2021 pour Mac."),
                ("Outlook inclus ?", "Oui, avec Word, Excel et PowerPoint."),
                ("Abonnement ?", "Non — licence ESD perpétuelle 2021."),
                ("Activation ?", "Code reçu sur le portail Microsoft, installation des apps Mac."),
                ("Sous Windows ?", "Non — choisissez la fiche PC/Mac ou Windows correspondante."),
            ],
            "de": [
                ("Nur Mac?", "Ja — Home & Business 2021 Mac-Edition."),
                ("Outlook inklusive?", "Ja, mit Word, Excel und PowerPoint."),
                ("Abo?", "Nein — ESD-Dauerlizenz 2021."),
                ("Aktivierung?", "E-Mail-Key im Microsoft-Portal, Mac-Apps installieren."),
                ("Unter Windows?", "Nein — die passende PC/Mac- oder Windows-Seite wählen."),
            ],
            "es": [
                ("¿Solo Mac?", "Sí: edición Home & Business 2021 para Mac."),
                ("¿Incluye Outlook?", "Sí, junto con Word, Excel y PowerPoint."),
                ("¿Es suscripción?", "No: licencia ESD perpetua 2021."),
                ("¿Cómo se activa?", "Con la clave del email en el portal Microsoft e instalación de las apps Mac."),
                ("¿Sirve en Windows?", "No: elige la ficha PC/Mac o Windows correspondiente."),
            ],
        },
    },
    "office-2021-professional-plus": {
        "apps": APPS_PRO_PLUS,
        "title_html": L(
            it='Office 2021 <span>Professional Plus</span>',
            en='Office 2021 <span>Professional Plus</span>',
            fr='Office 2021 <span>Professional Plus</span>',
            de='Office 2021 <span>Professional Plus</span>',
            es='Office 2021 <span>Professional Plus</span>',
        ),
        "eyebrow": L(
            it="Licenza perpetua · Professional Plus · Windows",
            en="Perpetual licence · Professional Plus · Windows",
            fr="Licence perpétuelle · Professional Plus · Windows",
            de="Dauerlizenz · Professional Plus · Windows",
            es="Licencia perpetua · Professional Plus · Windows",
        ),
        "desc": L(
            it="Office 2021 Professional Plus: suite desktop completa per Windows con licenza digitale ESD. Codice e istruzioni via email dopo l'acquisto.",
            en="Office 2021 Professional Plus: full desktop suite for Windows with a genuine ESD licence. Key and instructions by email after purchase.",
            fr="Office 2021 Professional Plus : suite de bureau complète pour Windows, licence ESD originale. Code et instructions par e-mail.",
            de="Office 2021 Professional Plus: vollständige Desktop-Suite für Windows als ESD-Lizenz. Key und Anleitung per E-Mail.",
            es="Office 2021 Professional Plus: suite de escritorio completa para Windows con licencia ESD. Clave e instrucciones por email.",
        ),
        "pills": pills_hb(),
        "features_title": L(
            it="Professional Plus 2021 senza abbonamento",
            en="Professional Plus 2021, no subscription",
            fr="Professional Plus 2021 sans abonnement",
            de="Professional Plus 2021 — ohne Abo",
            es="Professional Plus 2021 sin suscripción",
        ),
        "features": {
            "it": [
                ("c8", "blue", "Edizione", "Professional Plus", "Edizione professionale completa di Office 2021 con licenza perpetua ESD per Windows."),
                ("c4", "teal", None, "Suite ampia", "Word, Excel, PowerPoint, Outlook e OneNote tra le app tipiche Pro Plus."),
                ("c4", "purple", "Modello", "Acquisto una tantum", "Niente rinnovo annuale tipico di Microsoft 365."),
                ("c4", None, "Consegna", "Digitale", "Chiave e istruzioni via email dopo il pagamento."),
                ("c4", None, "Attivazione", "Canali Microsoft", "Attivazione e installazione tramite i portali ufficiali Microsoft."),
                ("c4", "dark", "Nota", "Windows", "Scheda orientata a Windows; verifica requisiti Microsoft per Office 2021."),
            ],
            "en": [
                ("c8", "blue", "Edition", "Professional Plus", "Full professional Office 2021 edition with a perpetual ESD licence for Windows."),
                ("c4", "teal", None, "Broad suite", "Word, Excel, PowerPoint, Outlook and OneNote among typical Pro Plus apps."),
                ("c4", "purple", "Model", "One-time purchase", "No Microsoft 365-style yearly renewal."),
                ("c4", None, "Delivery", "Digital", "Key and instructions by email after payment."),
                ("c4", None, "Activation", "Microsoft channels", "Activate and install via official Microsoft portals."),
                ("c4", "dark", "Note", "Windows", "Page aimed at Windows; check Microsoft’s Office 2021 requirements."),
            ],
            "fr": [
                ("c8", "blue", "Édition", "Professional Plus", "Édition professionnelle complète Office 2021 en licence ESD perpétuelle pour Windows."),
                ("c4", "teal", None, "Suite large", "Word, Excel, PowerPoint, Outlook et OneNote parmi les apps Pro Plus typiques."),
                ("c4", "purple", "Modèle", "Achat unique", "Pas de renouvellement annuel type Microsoft 365."),
                ("c4", None, "Livraison", "Numérique", "Clé et instructions par e-mail après paiement."),
                ("c4", None, "Activation", "Canaux Microsoft", "Activation et installation via les portails officiels."),
                ("c4", "dark", "Note", "Windows", "Fiche orientée Windows ; vérifiez les exigences Office 2021."),
            ],
            "de": [
                ("c8", "blue", "Edition", "Professional Plus", "Vollständige Professional-Edition Office 2021 als ESD-Dauerlizenz für Windows."),
                ("c4", "teal", None, "Breite Suite", "Word, Excel, PowerPoint, Outlook und OneNote u. a. typische Pro-Plus-Apps."),
                ("c4", "purple", "Modell", "Einmalkauf", "Kein Microsoft-365-Jahresabo."),
                ("c4", None, "Lieferung", "Digital", "Key und Anleitung per E-Mail nach der Zahlung."),
                ("c4", None, "Aktivierung", "Microsoft-Kanäle", "Aktivierung und Installation über offizielle Portale."),
                ("c4", "dark", "Hinweis", "Windows", "Seite für Windows; Office-2021-Anforderungen prüfen."),
            ],
            "es": [
                ("c8", "blue", "Edición", "Professional Plus", "Edición profesional completa de Office 2021 con licencia ESD perpetua para Windows."),
                ("c4", "teal", None, "Suite amplia", "Word, Excel, PowerPoint, Outlook y OneNote entre las apps Pro Plus típicas."),
                ("c4", "purple", "Modelo", "Compra única", "Sin renovación anual tipo Microsoft 365."),
                ("c4", None, "Entrega", "Digital", "Clave e instrucciones por email tras el pago."),
                ("c4", None, "Activación", "Canales Microsoft", "Activación e instalación por portales oficiales."),
                ("c4", "dark", "Nota", "Windows", "Ficha orientada a Windows; comprueba requisitos de Office 2021."),
            ],
        },
        "apps_title": L(
            it="App in Professional Plus 2021",
            en="Apps in Professional Plus 2021",
            fr="Apps Professional Plus 2021",
            de="Apps in Professional Plus 2021",
            es="Apps en Professional Plus 2021",
        ),
        "faq": {
            "it": [
                ("Cosa significa Professional Plus?", "Edizione professionale completa della linea Office 2021, tipicamente con Outlook e più app rispetto a Home & Student."),
                ("È un abbonamento?", "No: licenza perpetua ESD 2021."),
                ("Include Access o Publisher?", "Dipende dall'offerta Microsoft della licenza. In scheda indichiamo le app principali."),
                ("Come si attiva?", "Con il codice via email sui portali Microsoft (es. setup.office.com)."),
                ("Perché 2021 e non 2024?", "Se ti serve la generazione 2021 o le condizioni di questa scheda. Per funzioni più recenti valuta 2024 o Microsoft 365."),
            ],
            "en": [
                ("What does Professional Plus mean?", "Full professional Office 2021 edition, typically with Outlook and more apps than Home & Student."),
                ("Is it a subscription?", "No—perpetual ESD 2021 licence."),
                ("Does it include Access or Publisher?", "Depends on Microsoft’s offer for the licence. We list the main apps here."),
                ("How do I activate?", "With the emailed key on Microsoft portals (e.g. setup.office.com)."),
                ("Why 2021 not 2024?", "If you need the 2021 generation or this page’s offer. For newer features consider 2024 or Microsoft 365."),
            ],
            "fr": [
                ("Que signifie Professional Plus ?", "Édition pro complète d'Office 2021, typiquement avec Outlook et plus d'apps que Home & Student."),
                ("Abonnement ?", "Non — licence ESD perpétuelle 2021."),
                ("Access ou Publisher ?", "Selon l'offre Microsoft. Nous listons les apps principales."),
                ("Activation ?", "Code reçu sur les portails Microsoft (ex. setup.office.com)."),
                ("Pourquoi 2021 ?", "Si vous visez la génération 2021 ou cette offre. Pour plus récent : 2024 ou Microsoft 365."),
            ],
            "de": [
                ("Was heißt Professional Plus?", "Vollständige Professional-Edition Office 2021, typisch mit Outlook und mehr Apps als Home & Student."),
                ("Abo?", "Nein — ESD-Dauerlizenz 2021."),
                ("Access oder Publisher?", "Abhängig vom Microsoft-Angebot. Hier die Haupt-Apps."),
                ("Aktivierung?", "E-Mail-Key über Microsoft-Portale (z. B. setup.office.com)."),
                ("Warum 2021?", "Wenn Sie die Generation 2021 oder dieses Angebot brauchen. Für Neueres: 2024 oder Microsoft 365."),
            ],
            "es": [
                ("¿Qué es Professional Plus?", "Edición profesional completa de Office 2021, normalmente con Outlook y más apps que Home & Student."),
                ("¿Es suscripción?", "No: licencia ESD perpetua 2021."),
                ("¿Incluye Access o Publisher?", "Depende de la oferta Microsoft. Aquí listamos las apps principales."),
                ("¿Cómo se activa?", "Con la clave del email en los portales Microsoft (p. ej. setup.office.com)."),
                ("¿Por qué 2021?", "Si necesitas esa generación o esta oferta. Para funciones más nuevas: 2024 o Microsoft 365."),
            ],
        },
    },
}


def get_office_2021_content(slug):
    return PRODUCTS.get(slug)
