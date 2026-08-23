#!/usr/bin/env python3
"""Generate static "Chi siamo" / About pages for it/en/fr/de/es — corporate layout.

Every fact here (founding year, solo operation, order count, Microsoft
Partner status, markets served) was provided directly by the site owner —
nothing here is invented. Keep it that way: if a fact changes or a new one
is added, update COPY below rather than hand-editing the generated HTML.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LOCALE = {"it": "it_IT", "en": "en_US", "fr": "fr_FR", "de": "de_DE", "es": "es_ES", "pt": "pt_PT", "nl": "nl_NL"}

SLUG = {
    "it": "chi-siamo",
    "en": "about-us",
    "fr": "qui-sommes-nous",
    "de": "ueber-uns",
    "es": "quienes-somos",
    "pt": "sobre-nos",
    "nl": "over-ons",
}

COPY = {
    "it": {
        "skip": "Vai al contenuto principale",
        "title": "Chi siamo — Aml Store",
        "description": "Aml Store è gestito da Antonino Cardelli dal 2020: licenze software sempre originali, un solo interlocutore reale, oltre 1000 ordini evasi. Microsoft Partner.",
        "home": "Home",
        "breadcrumb": "Chi siamo",
        "eyebrow": "Chi siamo",
        "h1": "Software originale, seguito di persona.",
        "lede": "Aml Store è un progetto che porto avanti da solo dal 2020: vendo licenze originali per combattere il software craccato, con un solo interlocutore reale dietro ogni ordine.",
        "h_story": "La mia storia",
        "story_p1": "Ho iniziato Aml Store con un obiettivo preciso: contrastare la diffusione di software craccato, spesso instabile, privo di aggiornamenti e di qualsiasi garanzia. Vendo esclusivamente <strong>licenze originali</strong>, con tutte le funzionalità, gli aggiornamenti e le garanzie previste dal produttore — a prezzi che restano accessibili.",
        "story_p2": "Sono <strong>Antonino Cardelli</strong> e gestisco Aml Store da solo: quando scrivi, non parli con un centralino o un ticket anonimo, ma con la persona che segue davvero il tuo ordine.",
        "stat1_value": "Dal 2020",
        "stat1_label": "In attività",
        "stat2_value": "1000+",
        "stat2_label": "Ordini reali evasi",
        "stat3_value": "Microsoft Partner",
        "stat3_label": "Certificazione ufficiale",
        "stat4_value": "EU · USA · Canada · Africa · Giappone",
        "stat4_label": "Clienti serviti nel mondo",
        "h_values": "Perché scegliere Aml Store",
        "value1_title": "Solo software originale",
        "value1_text": "Ogni licenza è autentica, con aggiornamenti e garanzie dirette del produttore — mai copie craccate o modificate.",
        "value2_title": "Un solo interlocutore",
        "value2_text": "Nessun centralino, nessuna esternalizzazione: rispondo io a ogni richiesta, dall'ordine all'attivazione.",
        "value3_title": "Prezzi onesti",
        "value3_text": "Margini ragionevoli su licenze digitali autentiche, non sconti finti su prezzi gonfiati.",
        "value4_title": "Copertura internazionale",
        "value4_text": "Ordini gestiti in Europa, Stati Uniti, Canada, Africa e, occasionalmente, fino al Giappone.",
        "h_cta": "Hai domande prima di acquistare?",
        "cta_text": "Scrivimi o richiedi una consulenza gratuita: ti rispondo di persona.",
        "cta_contact": "Contattami",
        "cta_consultation": "Richiedi una consulenza",
    },
    "en": {
        "skip": "Skip to main content",
        "title": "About us — Aml Store",
        "description": "Aml Store has been run by Antonino Cardelli since 2020: always genuine software licences, one real point of contact, 1,000+ orders fulfilled. Microsoft Partner.",
        "home": "Home",
        "breadcrumb": "About us",
        "eyebrow": "About us",
        "h1": "Genuine software, handled personally.",
        "lede": "Aml Store has been a one-person project since 2020: I sell genuine software licences to fight cracked software, and there's one real person behind every order.",
        "h_story": "My story",
        "story_p1": "I started Aml Store with a clear goal: to push back against cracked software — often unstable, unpatched and unsupported. I sell exclusively <strong>genuine licences</strong>, with the full features, updates and warranties the manufacturer provides, at prices that stay reasonable.",
        "story_p2": "I'm <strong>Antonino Cardelli</strong>, and I run Aml Store on my own: when you write in, you're not talking to a call centre or an anonymous ticket queue — you're talking to the person actually handling your order.",
        "stat1_value": "Since 2020",
        "stat1_label": "In business",
        "stat2_value": "1,000+",
        "stat2_label": "Real orders fulfilled",
        "stat3_value": "Microsoft Partner",
        "stat3_label": "Official certification",
        "stat4_value": "EU · US · Canada · Africa · Japan",
        "stat4_label": "Customers served worldwide",
        "h_values": "Why choose Aml Store",
        "value1_title": "Genuine software only",
        "value1_text": "Every licence is authentic, with the manufacturer's own updates and warranties — never cracked or modified copies.",
        "value2_title": "One point of contact",
        "value2_text": "No call centre, nothing outsourced: I answer every request myself, from order to activation.",
        "value3_title": "Honest pricing",
        "value3_text": "Reasonable margins on authentic digital licences, not fake discounts on inflated prices.",
        "value4_title": "International reach",
        "value4_text": "Orders handled across Europe, the US, Canada, Africa and, occasionally, as far as Japan.",
        "h_cta": "Questions before you buy?",
        "cta_text": "Write to me or request a free consultation — I'll answer personally.",
        "cta_contact": "Contact me",
        "cta_consultation": "Request a consultation",
    },
    "fr": {
        "skip": "Aller au contenu principal",
        "title": "Qui sommes-nous — Aml Store",
        "description": "Aml Store est géré par Antonino Cardelli depuis 2020 : des licences toujours authentiques, un seul interlocuteur réel, plus de 1000 commandes honorées. Microsoft Partner.",
        "home": "Accueil",
        "breadcrumb": "Qui sommes-nous",
        "eyebrow": "Qui sommes-nous",
        "h1": "Des logiciels authentiques, suivis personnellement.",
        "lede": "Aml Store est un projet que je gère seul depuis 2020 : je vends des licences authentiques pour lutter contre les logiciels piratés, avec une seule personne réelle derrière chaque commande.",
        "h_story": "Mon histoire",
        "story_p1": "J'ai créé Aml Store avec un objectif précis : lutter contre la diffusion de logiciels piratés, souvent instables, sans mises à jour ni garantie. Je vends exclusivement des <strong>licences authentiques</strong>, avec toutes les fonctionnalités, mises à jour et garanties prévues par l'éditeur, à des prix qui restent raisonnables.",
        "story_p2": "Je suis <strong>Antonino Cardelli</strong> et je gère Aml Store seul : quand vous m'écrivez, vous ne parlez pas à un centre d'appels ou à un ticket anonyme, mais à la personne qui suit réellement votre commande.",
        "stat1_value": "Depuis 2020",
        "stat1_label": "En activité",
        "stat2_value": "Plus de 1000",
        "stat2_label": "Commandes réelles honorées",
        "stat3_value": "Microsoft Partner",
        "stat3_label": "Certification officielle",
        "stat4_value": "UE · États-Unis · Canada · Afrique · Japon",
        "stat4_label": "Clients servis dans le monde entier",
        "h_values": "Pourquoi choisir Aml Store",
        "value1_title": "Uniquement des logiciels authentiques",
        "value1_text": "Chaque licence est authentique, avec les mises à jour et garanties directes de l'éditeur — jamais de copies piratées ou modifiées.",
        "value2_title": "Un seul interlocuteur",
        "value2_text": "Pas de centre d'appels, rien d'externalisé : je réponds moi-même à chaque demande, de la commande à l'activation.",
        "value3_title": "Des prix honnêtes",
        "value3_text": "Des marges raisonnables sur des licences numériques authentiques, pas de fausses remises sur des prix gonflés.",
        "value4_title": "Portée internationale",
        "value4_text": "Commandes gérées en Europe, aux États-Unis, au Canada, en Afrique et, occasionnellement, jusqu'au Japon.",
        "h_cta": "Des questions avant d'acheter ?",
        "cta_text": "Écrivez-moi ou demandez une consultation gratuite : je réponds personnellement.",
        "cta_contact": "Me contacter",
        "cta_consultation": "Demander une consultation",
    },
    "de": {
        "skip": "Zum Hauptinhalt springen",
        "title": "Über uns — Aml Store",
        "description": "Aml Store wird seit 2020 von Antonino Cardelli geführt: stets originale Softwarelizenzen, ein echter Ansprechpartner, über 1000 abgewickelte Bestellungen. Microsoft Partner.",
        "home": "Startseite",
        "breadcrumb": "Über uns",
        "eyebrow": "Über uns",
        "h1": "Originalsoftware, persönlich betreut.",
        "lede": "Aml Store ist seit 2020 ein Ein-Personen-Projekt: Ich verkaufe Originallizenzen im Kampf gegen gecrackte Software — mit einer echten Person hinter jeder Bestellung.",
        "h_story": "Meine Geschichte",
        "story_p1": "Ich habe Aml Store mit einem klaren Ziel gegründet: gegen die Verbreitung gecrackter Software vorzugehen — oft instabil, ohne Updates und ohne jede Garantie. Ich verkaufe ausschließlich <strong>Originallizenzen</strong> mit allen Funktionen, Updates und Garantien des Herstellers, zu Preisen, die fair bleiben.",
        "story_p2": "Ich bin <strong>Antonino Cardelli</strong> und führe Aml Store allein: Wenn Sie schreiben, sprechen Sie nicht mit einem Callcenter oder einem anonymen Ticket, sondern mit der Person, die Ihre Bestellung tatsächlich bearbeitet.",
        "stat1_value": "Seit 2020",
        "stat1_label": "Am Markt",
        "stat2_value": "Über 1000",
        "stat2_label": "Reale Bestellungen abgewickelt",
        "stat3_value": "Microsoft Partner",
        "stat3_label": "Offizielle Zertifizierung",
        "stat4_value": "EU · USA · Kanada · Afrika · Japan",
        "stat4_label": "Kunden weltweit betreut",
        "h_values": "Warum Aml Store",
        "value1_title": "Nur Originalsoftware",
        "value1_text": "Jede Lizenz ist authentisch, mit Updates und Garantien direkt vom Hersteller — niemals gecrackte oder veränderte Kopien.",
        "value2_title": "Ein einziger Ansprechpartner",
        "value2_text": "Kein Callcenter, nichts ausgelagert: Ich beantworte jede Anfrage selbst, von der Bestellung bis zur Aktivierung.",
        "value3_title": "Faire Preise",
        "value3_text": "Angemessene Margen auf echte digitale Lizenzen, keine Scheinrabatte auf aufgeblähte Preise.",
        "value4_title": "Internationale Reichweite",
        "value4_text": "Bestellungen aus Europa, den USA, Kanada, Afrika und gelegentlich sogar Japan.",
        "h_cta": "Fragen vor dem Kauf?",
        "cta_text": "Schreiben Sie mir oder fordern Sie eine kostenlose Beratung an — ich antworte persönlich.",
        "cta_contact": "Kontakt aufnehmen",
        "cta_consultation": "Beratung anfragen",
    },
    "es": {
        "skip": "Ir al contenido principal",
        "title": "Quiénes somos — Aml Store",
        "description": "Aml Store lo gestiona Antonino Cardelli desde 2020: licencias siempre originales, un único interlocutor real, más de 1000 pedidos completados. Microsoft Partner.",
        "home": "Inicio",
        "breadcrumb": "Quiénes somos",
        "eyebrow": "Quiénes somos",
        "h1": "Software original, gestionado en persona.",
        "lede": "Aml Store es un proyecto que llevo yo solo desde 2020: vendo licencias originales para combatir el software pirateado, con una sola persona real detrás de cada pedido.",
        "h_story": "Mi historia",
        "story_p1": "Empecé Aml Store con un objetivo claro: combatir la difusión de software pirateado, a menudo inestable, sin actualizaciones ni garantías. Vendo exclusivamente <strong>licencias originales</strong>, con todas las funciones, actualizaciones y garantías del fabricante, a precios que siguen siendo razonables.",
        "story_p2": "Soy <strong>Antonino Cardelli</strong> y gestiono Aml Store yo solo: cuando escribes, no hablas con un centro de llamadas ni con un ticket anónimo, sino con la persona que realmente se ocupa de tu pedido.",
        "stat1_value": "Desde 2020",
        "stat1_label": "En activo",
        "stat2_value": "Más de 1000",
        "stat2_label": "Pedidos reales completados",
        "stat3_value": "Microsoft Partner",
        "stat3_label": "Certificación oficial",
        "stat4_value": "UE · EE. UU. · Canadá · África · Japón",
        "stat4_label": "Clientes atendidos en todo el mundo",
        "h_values": "Por qué elegir Aml Store",
        "value1_title": "Solo software original",
        "value1_text": "Cada licencia es auténtica, con actualizaciones y garantías directas del fabricante — nunca copias pirateadas o modificadas.",
        "value2_title": "Un único interlocutor",
        "value2_text": "Sin centro de llamadas, nada externalizado: respondo yo mismo a cada consulta, desde el pedido hasta la activación.",
        "value3_title": "Precios honestos",
        "value3_text": "Márgenes razonables sobre licencias digitales auténticas, no descuentos falsos sobre precios inflados.",
        "value4_title": "Alcance internacional",
        "value4_text": "Pedidos gestionados en Europa, Estados Unidos, Canadá, África y, ocasionalmente, hasta Japón.",
        "h_cta": "¿Dudas antes de comprar?",
        "cta_text": "Escríbeme o solicita una consulta gratuita: te respondo en persona.",
        "cta_contact": "Contactarme",
        "cta_consultation": "Solicitar asesoramiento",
    },
    "pt": {
        "skip": "Ir para o conteúdo principal",
        "title": "Sobre nós — Aml Store",
        "description": "A Aml Store é gerida por Antonino Cardelli desde 2020: licenças sempre originais, um único interlocutor real, mais de 1000 encomendas concluídas. Microsoft Partner.",
        "home": "Início",
        "breadcrumb": "Sobre nós",
        "eyebrow": "Sobre nós",
        "h1": "Software original, acompanhado pessoalmente.",
        "lede": "A Aml Store é um projeto que levo sozinho desde 2020: vendo licenças originais para combater o software pirateado, com uma única pessoa real por detrás de cada encomenda.",
        "h_story": "A minha história",
        "story_p1": "Comecei a Aml Store com um objetivo claro: combater a difusão de software pirateado, muitas vezes instável, sem atualizações e sem qualquer garantia. Vendo exclusivamente <strong>licenças originais</strong>, com todas as funcionalidades, atualizações e garantias previstas pelo fabricante, a preços que continuam acessíveis.",
        "story_p2": "Sou <strong>Antonino Cardelli</strong> e gero a Aml Store sozinho: quando escreves, não falas com uma central de atendimento ou um ticket anónimo, mas com a pessoa que acompanha mesmo a tua encomenda.",
        "stat1_value": "Desde 2020",
        "stat1_label": "Em atividade",
        "stat2_value": "1000+",
        "stat2_label": "Encomendas reais concluídas",
        "stat3_value": "Microsoft Partner",
        "stat3_label": "Certificação oficial",
        "stat4_value": "UE · EUA · Canadá · África · Japão",
        "stat4_label": "Clientes servidos em todo o mundo",
        "h_values": "Porque escolher a Aml Store",
        "value1_title": "Apenas software original",
        "value1_text": "Cada licença é autêntica, com atualizações e garantias diretas do fabricante — nunca cópias pirateadas ou modificadas.",
        "value2_title": "Um único interlocutor",
        "value2_text": "Sem central de atendimento, nada subcontratado: respondo eu a cada pedido, desde a encomenda até à ativação.",
        "value3_title": "Preços honestos",
        "value3_text": "Margens razoáveis sobre licenças digitais autênticas, não descontos falsos sobre preços inflacionados.",
        "value4_title": "Alcance internacional",
        "value4_text": "Encomendas geridas na Europa, Estados Unidos, Canadá, África e, ocasionalmente, até ao Japão.",
        "h_cta": "Tens dúvidas antes de comprar?",
        "cta_text": "Escreve-me ou pede uma consulta gratuita: respondo eu, pessoalmente.",
        "cta_contact": "Contactar",
        "cta_consultation": "Pedir uma consulta",
    },
    "nl": {
        "skip": "Naar de hoofdinhoud",
        "title": "Over ons — Aml Store",
        "description": "Aml Store wordt sinds 2020 gerund door Antonino Cardelli: altijd originele softwarelicenties, één echt aanspreekpunt, 1.000+ afgehandelde bestellingen. Microsoft Partner.",
        "home": "Home",
        "breadcrumb": "Over ons",
        "eyebrow": "Over ons",
        "h1": "Originele software, persoonlijk begeleid.",
        "lede": "Aml Store is sinds 2020 een eenmansproject: ik verkoop originele licenties tegen gekraakte software, met één echt persoon achter elke bestelling.",
        "h_story": "Mijn verhaal",
        "story_p1": "Ik ben Aml Store gestart met een duidelijk doel: de verspreiding van gekraakte software tegengaan — vaak instabiel, zonder updates en zonder garantie. Ik verkoop uitsluitend <strong>originele licenties</strong>, met alle functies, updates en garanties van de fabrikant, tegen prijzen die redelijk blijven.",
        "story_p2": "Ik ben <strong>Antonino Cardelli</strong> en run Aml Store in mijn eentje: als u schrijft, praat u niet met een callcenter of een anoniem ticket, maar met de persoon die uw bestelling daadwerkelijk behandelt.",
        "stat1_value": "Sinds 2020",
        "stat1_label": "Actief",
        "stat2_value": "1.000+",
        "stat2_label": "Echte afgehandelde bestellingen",
        "stat3_value": "Microsoft Partner",
        "stat3_label": "Officiële certificering",
        "stat4_value": "EU · VS · Canada · Afrika · Japan",
        "stat4_label": "Klanten wereldwijd bediend",
        "h_values": "Waarom Aml Store",
        "value1_title": "Alleen originele software",
        "value1_text": "Elke licentie is authentiek, met updates en garanties van de fabrikant — nooit gekraakte of gewijzigde kopieën.",
        "value2_title": "Eén aanspreekpunt",
        "value2_text": "Geen callcenter, niets uitbesteed: ik beantwoord elk verzoek zelf, van bestelling tot activering.",
        "value3_title": "Eerlijke prijzen",
        "value3_text": "Redelijke marges op authentieke digitale licenties, geen nep-kortingen op opgeblazen prijzen.",
        "value4_title": "Internationale dekking",
        "value4_text": "Bestellingen in Europa, de VS, Canada, Afrika en af en toe tot in Japan.",
        "h_cta": "Vragen voor u koopt?",
        "cta_text": "Schrijf mij of vraag een gratis consultatie: ik antwoord persoonlijk.",
        "cta_contact": "Contact",
        "cta_consultation": "Consultatie aanvragen",
    },
}

# slug of the pre-sale "software consultation" page per locale (see components/footer.js)
CONSULTATION_SLUG = {"it": "consulenza", "en": "consultation", "fr": "consultation", "de": "beratung", "es": "consultoria", "pt": "consultoria", "nl": "consultatie"}

ICON_SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
ICON_PERSON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"></circle><path d="M4 21v-1a8 8 0 0 1 16 0v1"></path></svg>'
ICON_TAG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12.59 2H6a2 2 0 0 0-2 2v6.59a2 2 0 0 0 .59 1.41l9 9a2 2 0 0 0 2.82 0l6.59-6.59a2 2 0 0 0 0-2.82l-9-9A2 2 0 0 0 12.59 2z"></path><circle cx="7.5" cy="7.5" r="1.5"></circle></svg>'
ICON_GLOBE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M3 12h18"></path><path d="M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18z"></path></svg>'


def page(lang: str) -> str:
    t = COPY[lang]
    slug = SLUG[lang]
    url = f"https://aml-store.com/{lang}/{slug}"
    consultation_url = CONSULTATION_SLUG[lang]
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": "https://aml-store.com/#organization",
                "name": "Aml Store",
                "url": "https://aml-store.com/",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://aml-store.com/logo/logo-header-400.webp",
                },
                "email": "Info@amlstore.it",
                "telephone": "+39-392-558-0413",
                "vatID": "IT11461870963",
                "legalName": "Licensoft di Cardelli Antonino",
                "foundingDate": "2020",
                "founder": {"@type": "Person", "name": "Antonino Cardelli"},
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "Via Trento 5/A",
                    "postalCode": "20015",
                    "addressLocality": "Parabiago",
                    "addressRegion": "MI",
                    "addressCountry": "IT",
                },
            },
            {
                "@type": "WebSite",
                "@id": "https://aml-store.com/#website",
                "url": "https://aml-store.com/",
                "name": "Aml Store",
                "inLanguage": ["it", "en", "fr", "de", "es", "pt", "nl"],
                "publisher": {"@id": "https://aml-store.com/#organization"},
            },
            {
                "@type": "AboutPage",
                "@id": f"{url}#webpage",
                "url": url,
                "name": t["title"],
                "description": t["description"],
                "inLanguage": lang,
                "isPartOf": {"@id": "https://aml-store.com/#website"},
                "about": {"@id": "https://aml-store.com/#organization"},
                "mainEntity": {"@id": "https://aml-store.com/#organization"},
            },
        ],
    }
    hreflang = "\n".join(
        f'    <link rel="alternate" hreflang="{lg}" href="https://aml-store.com/{lg}/{SLUG[lg]}">'
        for lg in ("it", "en", "fr", "de", "es", "pt", "nl")
    )
    hreflang += '\n    <link rel="alternate" hreflang="x-default" href="https://aml-store.com/it/chi-siamo">'

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t['title']}</title>
    <meta name="description" content="{t['description']}">
    <meta name="robots" content="index, follow">
    <script src="../js/consent-init.js"></script>

    <link rel="icon" href="../favicon/favicon.png" type="image/png">
    <link rel="apple-touch-icon" href="../favicon/apple-touch-icon.png">
    <link rel="canonical" href="{url}">

    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Aml Store">
    <meta property="og:title" content="{t['title']}">
    <meta property="og:description" content="{t['description']}">
    <meta property="og:url" content="{url}">
    <meta property="og:locale" content="{LOCALE[lang]}">
    <meta property="og:image" content="https://aml-store.com/logo/logo-header-400.webp">

{hreflang}

    <link rel="stylesheet" href="../fonts/montserrat.css">
    <link rel="stylesheet" href="../fonts/source-serif.css">
    <link rel="stylesheet" href="../css/page.css">
    <link rel="stylesheet" href="../css/about.css">
    <script src="../js/theme-init.js"></script>
    <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}
    </script>
</head>
<body>
    <a class="skip-link" href="#main">{t['skip']}</a>

    <ecommerce-header translate="no" class="notranslate"></ecommerce-header>

    <main id="main" class="about-page">
        <nav class="about-breadcrumb" aria-label="Breadcrumb">
            <a href="./">{t['home']}</a> <span aria-hidden="true">/</span> {t['breadcrumb']}
        </nav>

        <section class="about-hero" aria-labelledby="about-title">
            <p class="about-eyebrow">{t['eyebrow']}</p>
            <h1 id="about-title" class="about-title">{t['h1']}</h1>
            <p class="about-lede">{t['lede']}</p>
        </section>

        <section class="about-section" aria-labelledby="about-story-title">
            <h2 id="about-story-title" class="about-section__heading">{t['h_story']}</h2>
            <div class="about-story-grid">
                <div class="about-story-text">
                    <p>{t['story_p1']}</p>
                    <p>{t['story_p2']}</p>
                </div>
                <div class="about-stats">
                    <div class="about-stat"><span class="about-stat__value">{t['stat1_value']}</span><span class="about-stat__label">{t['stat1_label']}</span></div>
                    <div class="about-stat"><span class="about-stat__value">{t['stat2_value']}</span><span class="about-stat__label">{t['stat2_label']}</span></div>
                    <div class="about-stat"><span class="about-stat__value">{t['stat3_value']}</span><span class="about-stat__label">{t['stat3_label']}</span></div>
                    <div class="about-stat"><span class="about-stat__value">{t['stat4_value']}</span><span class="about-stat__label">{t['stat4_label']}</span></div>
                </div>
            </div>
        </section>

        <section class="about-section" aria-labelledby="about-values-title">
            <h2 id="about-values-title" class="about-section__heading">{t['h_values']}</h2>
            <div class="about-values-grid">
                <div class="about-value-card">
                    <span class="about-value-card__icon">{ICON_SHIELD}</span>
                    <h3>{t['value1_title']}</h3>
                    <p>{t['value1_text']}</p>
                </div>
                <div class="about-value-card">
                    <span class="about-value-card__icon">{ICON_PERSON}</span>
                    <h3>{t['value2_title']}</h3>
                    <p>{t['value2_text']}</p>
                </div>
                <div class="about-value-card">
                    <span class="about-value-card__icon">{ICON_TAG}</span>
                    <h3>{t['value3_title']}</h3>
                    <p>{t['value3_text']}</p>
                </div>
                <div class="about-value-card">
                    <span class="about-value-card__icon">{ICON_GLOBE}</span>
                    <h3>{t['value4_title']}</h3>
                    <p>{t['value4_text']}</p>
                </div>
            </div>
        </section>

        <section class="about-section about-cta" aria-labelledby="about-cta-title">
            <div class="about-cta__copy">
                <h2 id="about-cta-title">{t['h_cta']}</h2>
                <p>{t['cta_text']}</p>
            </div>
            <div class="about-cta__actions">
                <a class="about-btn about-btn-primary" href="contacts">{t['cta_contact']}</a>
                <a class="about-btn about-btn-ghost" href="{consultation_url}">{t['cta_consultation']}</a>
            </div>
        </section>
    </main>

    <aml-cookie-banner></aml-cookie-banner>
    <ecommerce-footer translate="no" class="notranslate"></ecommerce-footer>

    <script src="../js/locale-path.js"></script>
    <script src="../components/cookie-banner.js" defer></script>
    <script src="../components/header.js" defer></script>
    <script src="../components/footer.js" defer></script>
</body>
</html>
"""


def main():
    for lang in COPY:
        path = ROOT / lang / f"{SLUG[lang]}.html"
        path.write_text(page(lang), encoding="utf-8")
        print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
