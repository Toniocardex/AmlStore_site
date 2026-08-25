#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la pagina hub Microsoft 365 Solutions in tutte le 7 lingue,
stessa struttura del rebuild IT (3 piani reali con immagine, tabella di
confronto, link al confronto Family vs Personal, griglia app, FAQ).

Uso: python scripts/build_m365_solutions.py
Poi: node scripts/build-inline-chrome.mjs (dev server attivo)
     python scripts/bump-asset-version.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es", "pt", "nl")
LOCALE = {"it": "it_IT", "en": "en_US", "fr": "fr_FR", "de": "de_DE",
          "es": "es_ES", "pt": "pt_PT", "nl": "nl_NL"}
TAG_RE = re.compile(r"<[^>]+>")


def _d(it_val, en, fr, de, es, pt, nl):
    return {"it": it_val, "en": en, "fr": fr, "de": de, "es": es, "pt": pt, "nl": nl}


SHARED = {
    "it": {"skip": "Vai al contenuto principale", "home": "Home",
           "breadcrumb_aria": "Percorso navigazione", "in_practice": "In pratica",
           "faq_eyebrow": "Domande frequenti", "faq_h2": "Hai dubbi prima dell'acquisto?",
           "cta": "Vedi la scheda"},
    "en": {"skip": "Skip to main content", "home": "Home",
           "breadcrumb_aria": "Breadcrumb", "in_practice": "In practice",
           "faq_eyebrow": "Frequently asked questions", "faq_h2": "Answers before you buy",
           "cta": "See the listing"},
    "fr": {"skip": "Aller au contenu principal", "home": "Accueil",
           "breadcrumb_aria": "Fil d'Ariane", "in_practice": "En pratique",
           "faq_eyebrow": "Questions fréquentes", "faq_h2": "Les réponses avant d'acheter",
           "cta": "Voir la fiche"},
    "de": {"skip": "Zum Hauptinhalt springen", "home": "Start",
           "breadcrumb_aria": "Brotkrumen-Navigation", "in_practice": "In der Praxis",
           "faq_eyebrow": "Häufig gestellte Fragen", "faq_h2": "Antworten vor dem Kauf",
           "cta": "Zur Produktseite"},
    "es": {"skip": "Ir al contenido principal", "home": "Inicio",
           "breadcrumb_aria": "Ruta de navegación", "in_practice": "En la práctica",
           "faq_eyebrow": "Preguntas frecuentes", "faq_h2": "Las respuestas antes de comprar",
           "cta": "Ver la ficha"},
    "pt": {"skip": "Ir para o conteúdo principal", "home": "Início",
           "breadcrumb_aria": "Navegação estrutural", "in_practice": "Na prática",
           "faq_eyebrow": "Perguntas frequentes", "faq_h2": "Respostas antes de comprar",
           "cta": "Ver a ficha"},
    "nl": {"skip": "Naar de hoofdinhoud", "home": "Home",
           "breadcrumb_aria": "Kruimelpad", "in_practice": "In de praktijk",
           "faq_eyebrow": "Veelgestelde vragen", "faq_h2": "Antwoorden vóór u koopt",
           "cta": "Bekijk de productpagina"},
}

BREADCRUMB_LABEL = _d(*(["Microsoft 365"] * 7))
HERO_EYEBROW = BREADCRUMB_LABEL

META_TITLE = _d(
    "Quale Microsoft 365 scegliere | Aml Store",
    "Which Microsoft 365 to choose | Aml Store",
    "Quel Microsoft 365 choisir | Aml Store",
    "Welches Microsoft 365 wählen | Aml Store",
    "Qué Microsoft 365 elegir | Aml Store",
    "Que Microsoft 365 escolher | Aml Store",
    "Welke Microsoft 365 kiezen | Aml Store",
)
META_DESCRIPTION = _d(
    "Microsoft 365 Personal, Family o Business Standard: confronto prezzi, persone coperte, spazio cloud e Copilot AI per scegliere il piano giusto.",
    "Microsoft 365 Personal, Family or Business Standard: compare prices, people covered, cloud storage and Copilot AI to choose the right plan.",
    "Microsoft 365 Personal, Family ou Business Standard : comparaison des prix, des personnes couvertes, de l'espace cloud et de Copilot AI pour choisir le bon plan.",
    "Microsoft 365 Personal, Family oder Business Standard: Vergleich von Preisen, abgedeckten Personen, Cloud-Speicher und Copilot AI, um den richtigen Plan zu wählen.",
    "Microsoft 365 Personal, Family o Business Standard: compara precios, personas cubiertas, espacio en la nube y Copilot AI para elegir el plan adecuado.",
    "Microsoft 365 Personal, Family ou Business Standard: compare preços, pessoas cobertas, espaço na nuvem e Copilot AI para escolher o plano certo.",
    "Microsoft 365 Personal, Family of Business Standard: vergelijk prijzen, aantal personen, cloudopslag en Copilot AI om het juiste plan te kiezen.",
)
OG_DESCRIPTION = _d(
    "Confronto tra i piani Microsoft 365: Personal, Family e Business Standard.",
    "Comparison between the Microsoft 365 plans: Personal, Family and Business Standard.",
    "Comparaison entre les plans Microsoft 365 : Personal, Family et Business Standard.",
    "Vergleich der Microsoft-365-Pläne: Personal, Family und Business Standard.",
    "Comparación entre los planes de Microsoft 365: Personal, Family y Business Standard.",
    "Comparação entre os planos Microsoft 365: Personal, Family e Business Standard.",
    "Vergelijking tussen de Microsoft 365-abonnementen: Personal, Family en Business Standard.",
)
SCHEMA_NAME = META_TITLE  # replaced below without suffix
SCHEMA_NAME = _d(
    "Quale Microsoft 365 scegliere", "Which Microsoft 365 to choose", "Quel Microsoft 365 choisir",
    "Welches Microsoft 365 wählen", "Qué Microsoft 365 elegir", "Que Microsoft 365 escolher",
    "Welke Microsoft 365 kiezen",
)
SCHEMA_DESCRIPTION = _d(
    "Confronto tra Microsoft 365 Personal, Family e Business Standard: prezzo, persone coperte, spazio cloud e Copilot AI.",
    "Comparison between Microsoft 365 Personal, Family and Business Standard: price, people covered, cloud storage and Copilot AI.",
    "Comparaison entre Microsoft 365 Personal, Family et Business Standard : prix, personnes couvertes, espace cloud et Copilot AI.",
    "Vergleich zwischen Microsoft 365 Personal, Family und Business Standard: Preis, abgedeckte Personen, Cloud-Speicher und Copilot AI.",
    "Comparación entre Microsoft 365 Personal, Family y Business Standard: precio, personas cubiertas, espacio en la nube y Copilot AI.",
    "Comparação entre o Microsoft 365 Personal, Family e Business Standard: preço, pessoas cobertas, espaço na nuvem e Copilot AI.",
    "Vergelijking tussen Microsoft 365 Personal, Family en Business Standard: prijs, aantal personen, cloudopslag en Copilot AI.",
)
HERO_LEDE = _d(
    "Personal, Family o Business Standard: stesso principio di abbonamento, target diverso. Il piano giusto dipende da quante persone lo useranno e se ti serve la posta aziendale.",
    "Personal, Family or Business Standard: same subscription principle, different target. The right plan depends on how many people will use it and whether you need business email.",
    "Personal, Family ou Business Standard : même principe d'abonnement, cible différente. Le bon plan dépend du nombre de personnes qui l'utiliseront et si vous avez besoin de la messagerie professionnelle.",
    "Personal, Family oder Business Standard: gleiches Abo-Prinzip, unterschiedliche Zielgruppe. Der richtige Plan hängt davon ab, wie viele Personen ihn nutzen und ob Sie geschäftliche E-Mails brauchen.",
    "Personal, Family o Business Standard: mismo principio de suscripción, público distinto. El plan adecuado depende de cuántas personas lo usarán y si necesitas correo empresarial.",
    "Personal, Family ou Business Standard: mesmo princípio de subscrição, público-alvo diferente. O plano certo depende de quantas pessoas o vão usar e se precisa de email empresarial.",
    "Personal, Family of Business Standard: hetzelfde abonnementsprincipe, andere doelgroep. Het juiste plan hangt af van hoeveel personen het gebruiken en of je zakelijke e-mail nodig hebt.",
)

VERDICTS = [
    {
        "name": _d(*(["Microsoft 365 Personal"] * 7)),
        "img": "microsoft-365-personal.webp",
        "blurb": _d(
            "Per un uso individuale: 1TB su OneDrive e Copilot AI incluso.",
            "For individual use: 1TB on OneDrive and Copilot AI included.",
            "Pour un usage individuel : 1 To sur OneDrive et Copilot AI inclus.",
            "Für die Einzelnutzung: 1 TB auf OneDrive und Copilot AI inklusive.",
            "Para uso individual: 1 TB en OneDrive y Copilot AI incluido.",
            "Para uso individual: 1 TB no OneDrive e Copilot AI incluído.",
            "Voor individueel gebruik: 1 TB op OneDrive en Copilot AI inbegrepen.",
        ),
        "price": _d("€ 84,79 / anno", "€ 84,79 / year", "€ 84,79 / an", "€ 84,79 / Jahr",
                     "€ 84,79 / año", "€ 84,79 / ano", "€ 84,79 / jaar"),
        "href": "microsoft-365-personal",
    },
    {
        "name": _d(*(["Microsoft 365 Family"] * 7)),
        "img": "microsoft-365-family.webp",
        "blurb": _d(
            "Fino a 6 persone, ciascuna con il proprio 1TB. Copilot AI resta riservato al titolare.",
            "Up to 6 people, each with their own 1TB. Copilot AI stays reserved for the account holder.",
            "Jusqu'à 6 personnes, chacune avec son propre 1 To. Copilot AI reste réservé au titulaire.",
            "Bis zu 6 Personen, jede mit eigenem 1 TB. Copilot AI bleibt dem Inhaber vorbehalten.",
            "Hasta 6 personas, cada una con su propio 1 TB. Copilot AI queda reservado al titular.",
            "Até 6 pessoas, cada uma com o seu próprio 1 TB. O Copilot AI fica reservado ao titular.",
            "Tot 6 personen, elk met hun eigen 1 TB. Copilot AI blijft voorbehouden aan de accounthouder.",
        ),
        "price": _d("€ 104,95 / anno", "€ 104,95 / year", "€ 104,95 / an", "€ 104,95 / Jahr",
                     "€ 104,95 / año", "€ 104,95 / ano", "€ 104,95 / jaar"),
        "href": "microsoft-365-family",
    },
    {
        "name": _d(*(["Microsoft 365 Business Standard"] * 7)),
        "img": "microsoft-365-business-standard.webp",
        "blurb": _d(
            "Posta aziendale, Teams fino a 300 partecipanti e app Office su 15 dispositivi per utente.",
            "Business email, Teams for up to 300 participants and Office apps on 15 devices per user.",
            "Messagerie professionnelle, Teams jusqu'à 300 participants et applications Office sur 15 appareils par utilisateur.",
            "Geschäftliche E-Mail, Teams für bis zu 300 Teilnehmer und Office-Apps auf 15 Geräten pro Nutzer.",
            "Correo empresarial, Teams para hasta 300 participantes y apps de Office en 15 dispositivos por usuario.",
            "Email empresarial, Teams até 300 participantes e apps do Office em 15 dispositivos por utilizador.",
            "Zakelijke e-mail, Teams voor tot 300 deelnemers en Office-apps op 15 apparaten per gebruiker.",
        ),
        "price": _d("€ 144,90 / anno", "€ 144,90 / year", "€ 144,90 / an", "€ 144,90 / Jahr",
                     "€ 144,90 / año", "€ 144,90 / ano", "€ 144,90 / jaar"),
        "href": "microsoft-365-business-standard",
    },
]

TABLE_CAPTION = _d(
    "Microsoft 365: Personal, Family e Business Standard a confronto",
    "Microsoft 365: Personal, Family and Business Standard compared",
    "Microsoft 365 : Personal, Family et Business Standard comparés",
    "Microsoft 365: Personal, Family und Business Standard im Vergleich",
    "Microsoft 365: Personal, Family y Business Standard comparados",
    "Microsoft 365: Personal, Family e Business Standard comparados",
    "Microsoft 365: Personal, Family en Business Standard vergeleken",
)
TABLE_HEADERS = [
    _d("Piano", "Plan", "Plan", "Plan", "Plan", "Plano", "Plan"),
    _d("Prezzo", "Price", "Prix", "Preis", "Precio", "Preço", "Prijs"),
    _d("Persone / dispositivi", "People / devices", "Personnes / appareils", "Personen / Geräte",
       "Personas / dispositivos", "Pessoas / dispositivos", "Personen / apparaten"),
    _d("Spazio cloud", "Cloud storage", "Espace cloud", "Cloud-Speicher", "Espacio en la nube",
       "Espaço na nuvem", "Cloudopslag"),
    _d(*(["Copilot AI"] * 7)),
]
TABLE_ROWS = [
    [
        _d(*(["Personal"] * 7)),
        _d("€ 84,79 / anno", "€ 84,79 / year", "€ 84,79 / an", "€ 84,79 / Jahr", "€ 84,79 / año", "€ 84,79 / ano", "€ 84,79 / jaar"),
        _d("1 persona", "1 person", "1 personne", "1 Person", "1 persona", "1 pessoa", "1 persoon"),
        _d(*(["1 TB"] * 7)),
        _d("Incluso", "Included", "Inclus", "Enthalten", "Incluido", "Incluído", "Inbegrepen"),
    ],
    [
        _d(*(["Family"] * 7)),
        _d("€ 104,95 / anno", "€ 104,95 / year", "€ 104,95 / an", "€ 104,95 / Jahr", "€ 104,95 / año", "€ 104,95 / ano", "€ 104,95 / jaar"),
        _d("Fino a 6 persone", "Up to 6 people", "Jusqu'à 6 personnes", "Bis zu 6 Personen", "Hasta 6 personas", "Até 6 pessoas", "Tot 6 personen"),
        _d("6 TB totali (1 TB a persona)", "6TB total (1TB per person)", "6 To au total (1 To par personne)",
           "6 TB insgesamt (1 TB pro Person)", "6 TB en total (1 TB por persona)", "6 TB no total (1 TB por pessoa)",
           "6 TB in totaal (1 TB per persoon)"),
        _d("Solo per il titolare", "Account holder only", "Titulaire uniquement", "Nur für den Inhaber",
           "Solo para el titular", "Só para o titular", "Alleen voor de accounthouder"),
    ],
    [
        _d(*(["Business Standard"] * 7)),
        _d("€ 144,90 / anno", "€ 144,90 / year", "€ 144,90 / an", "€ 144,90 / Jahr", "€ 144,90 / año", "€ 144,90 / ano", "€ 144,90 / jaar"),
        _d("1 utente, fino a 15 dispositivi", "1 user, up to 15 devices", "1 utilisateur, jusqu'à 15 appareils",
           "1 Nutzer, bis zu 15 Geräte", "1 usuario, hasta 15 dispositivos", "1 utilizador, até 15 dispositivos",
           "1 gebruiker, tot 15 apparaten"),
        _d(*(["1 TB OneDrive for Business"] * 7)),
        _d("Non incluso nel piano base", "Not included in the base plan", "Non inclus dans le plan de base",
           "Im Basisplan nicht enthalten", "No incluido en el plan base", "Não incluído no plano base",
           "Niet inbegrepen in het basisplan"),
    ],
]

HUB_LINK = {
    "title": _d(*(["Microsoft 365 Family vs Personal →"] * 7)),
    "sub": _d(
        "Quante persone possono usarlo e cosa cambia nel prezzo.",
        "How many people can use it and what changes in price.",
        "Combien de personnes peuvent l'utiliser et ce qui change au niveau du prix.",
        "Wie viele Personen es nutzen können und was sich beim Preis ändert.",
        "Cuántas personas pueden usarlo y qué cambia en el precio.",
        "Quantas pessoas podem usá-lo e o que muda no preço.",
        "Hoeveel personen het kunnen gebruiken en wat er verandert in de prijs.",
    ),
    "href": "microsoft-365-family-vs-personal",
}

APPS_H2 = _d(
    "Le stesse app in ogni piano", "The same apps in every plan", "Les mêmes applications dans chaque plan",
    "Dieselben Apps in jedem Plan", "Las mismas apps en cada plan", "As mesmas apps em cada plano",
    "Dezelfde apps in elk plan",
)
APPS_LEDE = _d(
    "Word, Excel, PowerPoint, Outlook, Teams e OneDrive sono incluse in tutti e tre i piani — cambia chi può usarle e con quanto spazio cloud, non le funzioni delle app stesse.",
    "Word, Excel, PowerPoint, Outlook, Teams and OneDrive are included in all three plans — what changes is who can use them and how much cloud storage, not the apps' features.",
    "Word, Excel, PowerPoint, Outlook, Teams et OneDrive sont inclus dans les trois plans — ce qui change, c'est qui peut les utiliser et avec combien d'espace cloud, pas les fonctions des applications elles-mêmes.",
    "Word, Excel, PowerPoint, Outlook, Teams und OneDrive sind in allen drei Plänen enthalten — was sich ändert, ist, wer sie nutzen kann und mit wie viel Cloud-Speicher, nicht die Funktionen der Apps selbst.",
    "Word, Excel, PowerPoint, Outlook, Teams y OneDrive están incluidos en los tres planes — lo que cambia es quién puede usarlas y con cuánto espacio en la nube, no las funciones de las propias apps.",
    "Word, Excel, PowerPoint, Outlook, Teams e OneDrive estão incluídos nos três planos — o que muda é quem as pode usar e com quanto espaço na nuvem, não as funcionalidades das próprias apps.",
    "Word, Excel, PowerPoint, Outlook, Teams en OneDrive zitten in alle drie de plannen — wat verandert is wie ze kan gebruiken en met hoeveel cloudopslag, niet de functies van de apps zelf.",
)
APP_TILES = [
    {"name": "Word", "icon": "img-aml-store_Word-Icon-FY26.svg",
     "blurb": _d("Documenti che convincono, in team.", "Documents that convince, as a team.",
                 "Des documents qui convainquent, en équipe.", "Dokumente, die überzeugen, im Team.",
                 "Documentos que convencen, en equipo.", "Documentos que convencem, em equipa.",
                 "Documenten die overtuigen, als team.")},
    {"name": "Excel", "icon": "img-aml-store_Excel-Icon-FY26.svg",
     "blurb": _d("Dati chiari, decisioni rapide.", "Clear data, faster decisions.",
                 "Des données claires, des décisions rapides.", "Klare Daten, schnellere Entscheidungen.",
                 "Datos claros, decisiones rápidas.", "Dados claros, decisões rápidas.",
                 "Duidelijke data, snellere beslissingen.")},
    {"name": "PowerPoint", "icon": "img-aml-store_PowerPoint-Icon-FY26.svg",
     "blurb": _d("Presentazioni ad alto impatto.", "High-impact presentations.",
                 "Des présentations à fort impact.", "Präsentationen mit hoher Wirkung.",
                 "Presentaciones de alto impacto.", "Apresentações de alto impacto.",
                 "Presentaties met impact.")},
    {"name": "Outlook", "icon": "img-aml-store_Outlook-Icon-FY26.svg",
     "blurb": _d("Posta e calendario sempre sincronizzati.", "Mail and calendar always in sync.",
                 "Messagerie et agenda toujours synchronisés.", "Post und Kalender immer synchron.",
                 "Correo y calendario siempre sincronizados.", "Correio e calendário sempre sincronizados.",
                 "Post en agenda altijd gesynchroniseerd.")},
    {"name": "Teams", "icon": "img-aml-store_Teams-Icon-FY26.svg",
     "blurb": _d("Riunioni e chat, un solo posto.", "Meetings and chat, one place.",
                 "Réunions et chat, un seul endroit.", "Meetings und Chat an einem Ort.",
                 "Reuniones y chat, en un solo lugar.", "Reuniões e chat, num só lugar.",
                 "Vergaderen en chatten, op één plek.")},
    {"name": "OneDrive", "icon": "img-aml-store_OneDrive-Icon-FY26.svg",
     "blurb": _d("I tuoi file al sicuro, ovunque.", "Your files safe, everywhere.",
                 "Vos fichiers en sécurité, partout.", "Ihre Dateien sicher, überall.",
                 "Tus archivos seguros, en todas partes.", "Os seus ficheiros seguros, em qualquer lugar.",
                 "Je bestanden veilig, overal.")},
]

EDITORIAL_H2 = _d(
    "Come scegliere in base a chi lo userà", "How to choose based on who'll use it",
    "Comment choisir selon qui l'utilisera", "Wie Sie je nach Nutzerkreis wählen",
    "Cómo elegir según quién lo vaya a usar", "Como escolher consoante quem o vai usar",
    "Hoe kies je op basis van wie het gebruikt",
)
EDITORIAL_PARAGRAPHS = _d(
    [
        "Se sei l'unica persona che userà l'abbonamento, Personal ha il prezzo più basso e include comunque Copilot AI e 1TB di spazio.",
        'Se lo condividi in famiglia, Family costa 20,16 € in più all\'anno ma copre fino a 6 persone con 1TB ciascuna — il conto completo è nel confronto <a href="microsoft-365-family-vs-personal">Family vs Personal</a>.',
        "Se ti serve la posta aziendale con dominio personalizzato (nome@tuaazienda.it), Teams per riunioni fino a 300 partecipanti e vuoi gestire più licenze per un team, Business Standard è pensato per questo: nessuno dei due piani consumer include la posta aziendale.",
    ],
    [
        "If you're the only person who'll use the subscription, Personal has the lowest price and still includes Copilot AI and 1TB of storage.",
        'If you share it with family, Family costs €20.16 more a year but covers up to 6 people with 1TB each — the full breakdown is in the <a href="microsoft-365-family-vs-personal">Family vs Personal</a> comparison.',
        "If you need business email with a custom domain (name@yourcompany.com), Teams for meetings up to 300 participants, and want to manage multiple licences for a team, Business Standard is built for that: neither consumer plan includes business email.",
    ],
    [
        "Si vous êtes la seule personne à utiliser l'abonnement, Personal a le prix le plus bas et inclut quand même Copilot AI et 1 To d'espace.",
        'Si vous le partagez en famille, Family coûte 20,16 € de plus par an mais couvre jusqu\'à 6 personnes avec 1 To chacune — le détail complet est dans le comparatif <a href="microsoft-365-family-vs-personal">Family vs Personal</a>.',
        "Si vous avez besoin d'une messagerie professionnelle avec domaine personnalisé (nom@votreentreprise.fr), de Teams pour des réunions jusqu'à 300 participants et souhaitez gérer plusieurs licences pour une équipe, Business Standard est conçu pour cela : aucun des deux plans grand public n'inclut la messagerie professionnelle.",
    ],
    [
        "Wenn Sie die einzige Person sind, die das Abo nutzt, hat Personal den niedrigsten Preis und enthält trotzdem Copilot AI und 1 TB Speicher.",
        'Wenn Sie es mit der Familie teilen, kostet Family 20,16 € mehr pro Jahr, deckt aber bis zu 6 Personen mit je 1 TB ab — die vollständige Rechnung finden Sie im Vergleich <a href="microsoft-365-family-vs-personal">Family vs Personal</a>.',
        "Wenn Sie geschäftliche E-Mail mit eigener Domain (name@ihrunternehmen.de), Teams für Meetings mit bis zu 300 Teilnehmern brauchen und mehrere Lizenzen für ein Team verwalten möchten, ist Business Standard genau dafür gemacht: Keiner der beiden Consumer-Pläne enthält geschäftliche E-Mail.",
    ],
    [
        "Si eres la única persona que usará la suscripción, Personal tiene el precio más bajo y aun así incluye Copilot AI y 1 TB de espacio.",
        'Si lo compartes en familia, Family cuesta 20,16 € más al año pero cubre hasta 6 personas con 1 TB cada una — el cálculo completo está en la comparativa <a href="microsoft-365-family-vs-personal">Family vs Personal</a>.',
        "Si necesitas correo empresarial con dominio propio (nombre@tuempresa.com), Teams para reuniones de hasta 300 participantes y quieres gestionar varias licencias para un equipo, Business Standard está pensado para eso: ninguno de los dos planes de consumo incluye correo empresarial.",
    ],
    [
        "Se é a única pessoa que vai usar a subscrição, o Personal tem o preço mais baixo e mesmo assim inclui o Copilot AI e 1 TB de espaço.",
        'Se o partilha em família, o Family custa mais 20,16 € por ano mas cobre até 6 pessoas com 1 TB cada — a conta completa está na comparação <a href="microsoft-365-family-vs-personal">Family vs Personal</a>.',
        "Se precisa de email empresarial com domínio próprio (nome@suaempresa.pt), Teams para reuniões até 300 participantes e quer gerir várias licenças para uma equipa, o Business Standard foi pensado para isso: nenhum dos dois planos de consumo inclui email empresarial.",
    ],
    [
        "Ben jij de enige die het abonnement gebruikt, dan heeft Personal de laagste prijs en toch Copilot AI en 1 TB opslag inbegrepen.",
        'Deel je het met het gezin, dan kost Family € 20,16 meer per jaar maar dekt het tot 6 personen met elk 1 TB — de volledige berekening staat in de vergelijking <a href="microsoft-365-family-vs-personal">Family vs Personal</a>.',
        "Heb je zakelijke e-mail met een eigen domein nodig (naam@jebedrijf.nl), Teams voor vergaderingen tot 300 deelnemers, en wil je meerdere licenties voor een team beheren, dan is Business Standard daarvoor gemaakt: geen van beide consumentenplannen bevat zakelijke e-mail.",
    ],
)

FAQ_ITEMS = [
    {
        "q": _d("Copilot AI è incluso anche in Business Standard?", "Is Copilot AI included in Business Standard too?",
                "Copilot AI est-il aussi inclus dans Business Standard ?", "Ist Copilot AI auch in Business Standard enthalten?",
                "¿Copilot AI también está incluido en Business Standard?", "O Copilot AI também está incluído no Business Standard?",
                "Zit Copilot AI ook bij Business Standard?"),
        "a": _d(
            "No: la scheda del prodotto non lo include nel piano base — Copilot per le aziende è un componente aggiuntivo separato in Microsoft 365.",
            "No: the product listing doesn't include it in the base plan — Copilot for business is a separate add-on in Microsoft 365.",
            "Non : la fiche du produit ne l'inclut pas dans le plan de base — Copilot pour les entreprises est un composant additionnel séparé dans Microsoft 365.",
            "Nein: Die Produktseite enthält es nicht im Basisplan — Copilot für Unternehmen ist ein separates Zusatzmodul in Microsoft 365.",
            "No: la ficha del producto no lo incluye en el plan base — Copilot para empresas es un complemento independiente en Microsoft 365.",
            "Não: a ficha do produto não o inclui no plano base — o Copilot para empresas é um complemento separado no Microsoft 365.",
            "Nee: de productpagina bevat het niet in het basisplan — Copilot voor bedrijven is een aparte invoegtoepassing in Microsoft 365.",
        ),
    },
    {
        "q": _d("Business Standard include la posta con il mio dominio aziendale?", "Does Business Standard include email on my company domain?",
                "Business Standard inclut-il la messagerie sur mon domaine d'entreprise ?", "Enthält Business Standard E-Mail auf meiner Unternehmensdomain?",
                "¿Business Standard incluye correo con mi dominio de empresa?", "O Business Standard inclui email com o meu domínio empresarial?",
                "Bevat Business Standard e-mail op mijn bedrijfsdomein?"),
        "a": _d(
            "Sì, tramite Exchange Online: caselle da 50 GB su un dominio personalizzato (es. nome@tuaazienda.it), secondo la scheda del prodotto.",
            "Yes, via Exchange Online: 50GB mailboxes on a custom domain (e.g. name@yourcompany.com), according to the product listing.",
            "Oui, via Exchange Online : boîtes de 50 Go sur un domaine personnalisé (ex. nom@votreentreprise.fr), selon la fiche du produit.",
            "Ja, über Exchange Online: 50-GB-Postfächer auf einer eigenen Domain (z. B. name@ihrunternehmen.de), laut Produktseite.",
            "Sí, a través de Exchange Online: buzones de 50 GB en un dominio personalizado (p. ej. nombre@tuempresa.com), según la ficha del producto.",
            "Sim, através do Exchange Online: caixas de correio de 50 GB num domínio personalizado (ex. nome@suaempresa.pt), segundo a ficha do produto.",
            "Ja, via Exchange Online: postbussen van 50 GB op een aangepast domein (bijv. naam@jebedrijf.nl), volgens de productpagina.",
        ),
    },
    {
        "q": _d("Posso acquistare più licenze Business Standard per il mio team?", "Can I buy multiple Business Standard licences for my team?",
                "Puis-je acheter plusieurs licences Business Standard pour mon équipe ?", "Kann ich mehrere Business-Standard-Lizenzen für mein Team kaufen?",
                "¿Puedo comprar varias licencias de Business Standard para mi equipo?", "Posso comprar várias licenças Business Standard para a minha equipa?",
                "Kan ik meerdere Business Standard-licenties kopen voor mijn team?"),
        "a": _d(
            'Sì, ogni licenza copre 1 utente su fino a 15 dispositivi; per volumi elevati o un preventivo su misura scrivi a <a href="mailto:info@amlstore.it">info@amlstore.it</a>.',
            'Yes, each licence covers 1 user on up to 15 devices; for high volumes or a custom quote, email <a href="mailto:info@amlstore.it">info@amlstore.it</a>.',
            'Oui, chaque licence couvre 1 utilisateur sur jusqu\'à 15 appareils ; pour des volumes importants ou un devis sur mesure, écrivez à <a href="mailto:info@amlstore.it">info@amlstore.it</a>.',
            'Ja, jede Lizenz deckt 1 Nutzer auf bis zu 15 Geräten ab; für hohe Volumen oder ein individuelles Angebot schreiben Sie an <a href="mailto:info@amlstore.it">info@amlstore.it</a>.',
            'Sí, cada licencia cubre 1 usuario en hasta 15 dispositivos; para volúmenes altos o un presupuesto a medida, escribe a <a href="mailto:info@amlstore.it">info@amlstore.it</a>.',
            'Sim, cada licença cobre 1 utilizador em até 15 dispositivos; para volumes elevados ou um orçamento à medida, escreva para <a href="mailto:info@amlstore.it">info@amlstore.it</a>.',
            'Ja, elke licentie dekt 1 gebruiker op tot 15 apparaten; voor grote volumes of een offerte op maat mail je naar <a href="mailto:info@amlstore.it">info@amlstore.it</a>.',
        ),
    },
    {
        "q": _d("Qual è la differenza tra Family e Personal?", "What's the difference between Family and Personal?",
                "Quelle est la différence entre Family et Personal ?", "Was ist der Unterschied zwischen Family und Personal?",
                "¿Cuál es la diferencia entre Family y Personal?", "Qual é a diferença entre o Family e o Personal?",
                "Wat is het verschil tussen Family en Personal?"),
        "a": _d(
            'Family copre fino a 6 persone con 1TB di spazio ciascuna, Personal solo una — vedi il confronto completo <a href="microsoft-365-family-vs-personal">Family vs Personal</a>.',
            'Family covers up to 6 people with 1TB each, Personal just one — see the full <a href="microsoft-365-family-vs-personal">Family vs Personal</a> comparison.',
            'Family couvre jusqu\'à 6 personnes avec 1 To chacune, Personal une seule — voir le comparatif complet <a href="microsoft-365-family-vs-personal">Family vs Personal</a>.',
            'Family deckt bis zu 6 Personen mit je 1 TB ab, Personal nur eine — siehe den vollständigen Vergleich <a href="microsoft-365-family-vs-personal">Family vs Personal</a>.',
            'Family cubre hasta 6 personas con 1 TB cada una, Personal solo una — consulta la comparación completa <a href="microsoft-365-family-vs-personal">Family vs Personal</a>.',
            'O Family cobre até 6 pessoas com 1 TB cada, o Personal apenas uma — veja a comparação completa <a href="microsoft-365-family-vs-personal">Family vs Personal</a>.',
            'Family dekt tot 6 personen met elk 1 TB, Personal maar één — bekijk de volledige vergelijking <a href="microsoft-365-family-vs-personal">Family vs Personal</a>.',
        ),
    },
    {
        "q": _d("Ho bisogno di licenze per molte postazioni: come funziona?", "I need licences for many seats: how does it work?",
                "J'ai besoin de licences pour de nombreux postes : comment ça marche ?", "Ich brauche Lizenzen für viele Arbeitsplätze: wie funktioniert das?",
                "Necesito licencias para muchos puestos: ¿cómo funciona?", "Preciso de licenças para muitos postos: como funciona?",
                "Ik heb licenties nodig voor veel werkplekken: hoe werkt dat?"),
        "a": _d(
            'Scrivici a <a href="mailto:info@amlstore.it">info@amlstore.it</a> con il numero di postazioni e il piano che ti interessa: prepariamo un preventivo allineato alle offerte Microsoft per i volumi.',
            'Email <a href="mailto:info@amlstore.it">info@amlstore.it</a> with the number of seats and the plan you\'re interested in: we\'ll prepare a quote aligned with Microsoft\'s volume offers.',
            'Écrivez-nous à <a href="mailto:info@amlstore.it">info@amlstore.it</a> avec le nombre de postes et le plan qui vous intéresse : nous préparons un devis aligné sur les offres Microsoft pour les volumes.',
            'Schreiben Sie uns an <a href="mailto:info@amlstore.it">info@amlstore.it</a> mit der Anzahl der Arbeitsplätze und dem gewünschten Plan: Wir erstellen ein Angebot passend zu den Microsoft-Volumenangeboten.',
            'Escríbenos a <a href="mailto:info@amlstore.it">info@amlstore.it</a> con el número de puestos y el plan que te interesa: preparamos un presupuesto alineado con las ofertas de volumen de Microsoft.',
            'Escreva-nos para <a href="mailto:info@amlstore.it">info@amlstore.it</a> com o número de postos e o plano que lhe interessa: preparamos um orçamento alinhado com as ofertas de volume da Microsoft.',
            'Mail ons op <a href="mailto:info@amlstore.it">info@amlstore.it</a> met het aantal werkplekken en het gewenste plan: we maken een offerte op basis van de Microsoft-volumeaanbiedingen.',
        ),
    },
]

DISCLAIMER = _d(
    "Microsoft, Microsoft 365, Office, Outlook, Teams, OneDrive, Copilot e i relativi marchi sono di Microsoft Corporation. Contenuto informativo Aml Store: funzionalità, limiti e disponibilità seguono sempre il prodotto Microsoft acquistato.",
    "Microsoft, Microsoft 365, Office, Outlook, Teams, OneDrive, Copilot and related marks are property of Microsoft Corporation. Informational content by Aml Store: features, limits and availability always follow the Microsoft product purchased.",
    "Microsoft, Microsoft 365, Office, Outlook, Teams, OneDrive, Copilot et les marques associées appartiennent à Microsoft Corporation. Contenu informatif Aml Store : fonctionnalités, limites et disponibilité suivent toujours le produit Microsoft acheté.",
    "Microsoft, Microsoft 365, Office, Outlook, Teams, OneDrive, Copilot und die zugehörigen Marken sind Eigentum der Microsoft Corporation. Informativer Inhalt von Aml Store: Funktionen, Grenzen und Verfügbarkeit richten sich stets nach dem gekauften Microsoft-Produkt.",
    "Microsoft, Microsoft 365, Office, Outlook, Teams, OneDrive, Copilot y las marcas relacionadas son propiedad de Microsoft Corporation. Contenido informativo de Aml Store: funciones, límites y disponibilidad siguen siempre el producto Microsoft adquirido.",
    "Microsoft, Microsoft 365, Office, Outlook, Teams, OneDrive, Copilot e as marcas relacionadas são propriedade da Microsoft Corporation. Conteúdo informativo da Aml Store: funcionalidades, limites e disponibilidade seguem sempre o produto Microsoft adquirido.",
    "Microsoft, Microsoft 365, Office, Outlook, Teams, OneDrive, Copilot en de bijbehorende merken zijn eigendom van Microsoft Corporation. Informatieve inhoud van Aml Store: functies, limieten en beschikbaarheid volgen altijd het aangeschafte Microsoft-product.",
)


def hreflang_block(slug):
    lines = [f'    <link rel="alternate" hreflang="{lg}" href="https://aml-store.com/{lg}/{slug}">'
             for lg in LANGS]
    lines.append(f'    <link rel="alternate" hreflang="x-default" href="https://aml-store.com/it/{slug}">')
    return "\n".join(lines)


def faq_schema(lang):
    parts = []
    for it in FAQ_ITEMS:
        q = it["q"][lang]
        a_plain = TAG_RE.sub("", it["a"][lang])
        parts.append(
            '{ "@type": "Question", "name": "%s", "acceptedAnswer": '
            '{ "@type": "Answer", "text": "%s" } }' % (q.replace('"', '\\"'), a_plain.replace('"', '\\"'))
        )
    return ",\n        ".join(parts)


def render(lang):
    s = SHARED[lang]
    slug = "microsoft-365-solutions"
    verdict_html = "".join(f"""            <div class="cmp-verdict__card">
                <img class="cmp-verdict__img" src="../asset/media/products/{v['img']}" width="64" height="64" alt="" loading="lazy" decoding="async">
                <h3>{v['name'][lang]}</h3>
                <p>{v['blurb'][lang]}</p>
                <span class="cmp-verdict__price">{v['price'][lang]}</span>
                <a class="pdp-btn-primary" href="{v['href']}">{s['cta']}</a>
            </div>
""" for v in VERDICTS)

    thead = "".join(f'<th scope="col">{h[lang]}</th>' for h in TABLE_HEADERS)
    trs = []
    for row in TABLE_ROWS:
        head, *cells = row
        tds = "".join(f"<td>{c[lang]}</td>" for c in cells)
        trs.append(f'                    <tr><th scope="row">{head[lang]}</th>{tds}</tr>')
    tbody = "\n".join(trs)

    tiles_html = "".join(f"""                <div class="m365sol-app-tile">
                    <div class="m365sol-app-icon" aria-hidden="true"><img src="../asset/icon/{t['icon']}" width="48" height="48" alt="" loading="lazy" decoding="async"></div>
                    <h3>{t['name']}</h3>
                    <p>{t['blurb'][lang]}</p>
                </div>
""" for t in APP_TILES)

    paras = "\n".join(f"                <p>{p}</p>" for p in EDITORIAL_PARAGRAPHS[lang])

    half = (len(FAQ_ITEMS) + 1) // 2
    def faq_col(items):
        return "\n".join(f"""                    <details class="home-faq-item">
                        <summary>{it['q'][lang]}</summary>
                        <div class="home-faq-body"><p>{it['a'][lang]}</p></div>
                    </details>""" for it in items)
    faq_html = f"""            <div class="home-faq-list">
                <div class="pf-faq-col">
{faq_col(FAQ_ITEMS[:half])}
                </div>
                <div class="pf-faq-col">
{faq_col(FAQ_ITEMS[half:])}
                </div>
            </div>
"""

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{META_TITLE[lang]}</title>
    <meta name="description" content="{META_DESCRIPTION[lang]}">
    <meta name="robots" content="index, follow">
    <script src="../js/consent-init.js"></script>
    <link rel="icon" href="../favicon/favicon.png" type="image/png">
    <link rel="apple-touch-icon" href="../favicon/apple-touch-icon.png">
    <link rel="canonical" href="https://aml-store.com/{lang}/{slug}">
{hreflang_block(slug)}
    <meta property="og:type" content="website">
    <meta property="og:title" content="{META_TITLE[lang]}">
    <meta property="og:description" content="{OG_DESCRIPTION[lang]}">
    <meta property="og:url" content="https://aml-store.com/{lang}/{slug}">
    <meta property="og:locale" content="{LOCALE[lang]}">
    <meta property="og:image" content="https://aml-store.com/asset/media/products/microsoft-365-family.webp">
    <link rel="stylesheet" href="../fonts/montserrat.css">
    <link rel="stylesheet" href="../css/page.css">
    <link rel="stylesheet" href="../css/header.css">
    <link rel="stylesheet" href="../css/footer.css">
    <link rel="stylesheet" href="../css/product.css">
    <link rel="stylesheet" href="../css/product-pdp.css">
    <link rel="stylesheet" href="../css/microsoft-365-solutions.css">
    <script src="../js/theme-init.js"></script>
    <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{ "@type": "Organization", "@id": "https://aml-store.com/#organization", "name": "Aml Store", "url": "https://aml-store.com/", "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "94", "bestRating": "5", "worstRating": "1" }} }},
    {{
      "@type": "WebPage",
      "@id": "https://aml-store.com/{lang}/{slug}#webpage",
      "name": "{SCHEMA_NAME[lang]}",
      "description": "{SCHEMA_DESCRIPTION[lang]}",
      "url": "https://aml-store.com/{lang}/{slug}",
      "inLanguage": "{lang}",
      "isPartOf": {{ "@type": "WebSite", "name": "Aml Store", "url": "https://aml-store.com/" }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "{s['home']}", "item": "https://aml-store.com/{lang}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "{BREADCRUMB_LABEL[lang]}" }}
      ]
    }},
    {{
      "@type": "FAQPage",
      "inLanguage": "{lang}",
      "url": "https://aml-store.com/{lang}/{slug}",
      "mainEntity": [
        {faq_schema(lang)}
      ]
    }}
  ]
}}
    </script>
</head>
<body class="pdp-page">
    <div class="scroll-progress" aria-hidden="true"></div>
    <a class="skip-link" href="#main">{s['skip']}</a>
    <aml-lang-suggest></aml-lang-suggest>
    <ecommerce-header translate="no" class="notranslate"></ecommerce-header>

    <main id="main" class="product-page">
        <section class="pdp-hero" aria-label="{HERO_EYEBROW[lang]}">
            <div class="pdp-breadcrumb">
                <nav aria-label="{s['breadcrumb_aria']}">
                    <a href="/{lang}/">{s['home']}</a>
                    <span class="sep" aria-hidden="true">/</span>
                    <span aria-current="page">{BREADCRUMB_LABEL[lang]}</span>
                </nav>
            </div>

            <div class="cmp-hero">
                <p class="cmp-hero__eyebrow">{HERO_EYEBROW[lang]}</p>
                <h1 class="cmp-hero__title">{SCHEMA_NAME[lang]}</h1>
                <p class="cmp-hero__lede">{HERO_LEDE[lang]}</p>
            </div>
        </section>

        <div class="pdp-page">
        <div class="cmp-verdict cmp-verdict--3" style="max-width:var(--pdp-maxw);margin:0 auto;padding:0 0 8px;">
{verdict_html}        </div>

        <div class="cmp-table-wrap">
            <table class="cmp-table">
                <caption>{TABLE_CAPTION[lang]}</caption>
                <thead>
                    <tr>{thead}</tr>
                </thead>
                <tbody>
{tbody}
                </tbody>
            </table>
        </div>

        <div class="hub-guide__links" style="max-width:var(--pdp-maxw);margin:20px auto 0;">
            <a class="hub-guide__link-card" href="{HUB_LINK['href']}">
                <strong>{HUB_LINK['title'][lang]}</strong>
                <span>{HUB_LINK['sub'][lang]}</span>
            </a>
        </div>

        <section class="m365sol-apps" aria-labelledby="m365sol-apps-title" style="padding-top:clamp(32px,5vw,48px);">
            <div class="m365sol-apps-head">
                <h2 id="m365sol-apps-title">{APPS_H2[lang]}</h2>
                <p>{APPS_LEDE[lang]}</p>
            </div>
            <div class="m365sol-apps-grid">
{tiles_html}            </div>
        </section>

        <section class="pdp-sec pdp-sec--tight">
            <p class="pdp-sec__eyebrow">{s['in_practice']}</p>
            <h2 class="pdp-sec__title">{EDITORIAL_H2[lang]}</h2>
            <div class="pdp-overview__copy">
{paras}
            </div>
        </section>

        <section class="pdp-sec pdp-sec--tight pdp-faq">
            <p class="pdp-sec__eyebrow">{s['faq_eyebrow']}</p>
            <h2 class="pdp-sec__title pdp-faq__title">{s['faq_h2']}</h2>
{faq_html}        </section>

        <p class="pdp-sec__sub" style="max-width:var(--pdp-maxw);margin:0 auto;padding:0 0 40px;">{DISCLAIMER[lang]}</p>
        </div>
    </main>

    <aml-cookie-banner></aml-cookie-banner>
    <ecommerce-footer translate="no" class="notranslate"></ecommerce-footer>

    <script src="../js/locale-path.js"></script>
    <script src="../js/cart.js" defer></script>
    <script src="../components/cookie-banner.js" defer></script>
    <script src="../components/lang-suggest.js" defer></script>
    <script src="../components/header.js" defer></script>
    <script src="../components/footer.js" defer></script>
    <script src="../js/scroll-progress.js" defer></script>
</body>
</html>
"""


if __name__ == "__main__":
    for lang in LANGS:
        out_dir = ROOT / lang
        path = out_dir / "microsoft-365-solutions.html"
        path.write_text(render(lang), encoding="utf-8", newline="\n")
    print(f"pagine scritte: {len(LANGS)}")
