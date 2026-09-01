#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia sulle pagine contacts.html (7 lingue).

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Fino a settembre 2026 main() chiamava page(lang) e sovrascriveva le 7 pagine.
Era sfuggito ai giri di disarmo precedenti perche' non chiama
build_product_page(): ha un page() suo, e non e' una scheda prodotto.

Eseguirlo oggi distruggerebbe circa tre quarti di ogni pagina: page() rende
10,5-10,7 KB contro pagine pubblicate di 39,9-40,4 KB, 7 diff su 7 e un delta
di 29,4-29,7 KB. Tutti e quattro i marcatori di PIPELINE_MARKERS sono presenti
nel pubblicato e assenti nel generato, su tutte e 7. Il perche', e i cinque
strati che andrebbero persi, stanno in scripts/page_pipeline_guard.py.

COPY resta la sorgente unica dei contenuti (orari di supporto, indirizzo, IVA),
coerente con il JSON-LD e con le etichette tradotte di components/footer.js.
Ma aggiornarlo non basta piu' a propagare la modifica: rieseguire lo script
butterebbe via la post-produzione, quindi il cambiamento va riportato a mano
sulla pagina pubblicata.

Nota: il vecchio docstring diceva "it/en/fr/de/es", ma COPY contiene da tempo
tutte e 7 le lingue e tutte e 7 le contacts.html esistono. La riga era stale.

Quel che lo script fa ancora, e per cui va tenuto: verifica che le 7 pagine
esistano con i quattro strati addosso. Senza effetti collaterali, non scrive
nulla.

    python scripts/write-contacts-pages.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from page_pipeline_guard import fail_if, load, pipeline_errors  # noqa: E402

LOCALE = {"it": "it_IT", "en": "en_US", "fr": "fr_FR", "de": "de_DE", "es": "es_ES", "pt": "pt_PT", "nl": "nl_NL"}

# slug of the pre-sale "software consultation" page per locale (see components/footer.js)
CONSULTATION_SLUG = {"it": "consulenza", "en": "consultation", "fr": "consultation", "de": "beratung", "es": "consultoria", "pt": "consultoria", "nl": "consultatie"}

COPY = {
    "it": {
        "skip": "Vai al contenuto principale",
        "title": "Contatti — Eurolicenze",
        "description": "Contatta Eurolicenze per assistenza su ordini e attivazione licenze via email, telefono o WhatsApp, dal lunedì al sabato, 08:00–19:00.",
        "home": "Home",
        "breadcrumb": "Contatti",
        "eyebrow": "Assistenza clienti",
        "h1": "Contatti",
        "lede": "Per domande su ordini, consegna digitale o attivazione delle licenze, il nostro team è a tua disposizione sui canali qui sotto.",
        "meta_hours": "Lun–Sab, 08:00–19:00",
        "meta_lang": "Assistenza in italiano",
        "h_channels": "Canali di assistenza",
        "email_label": "Email",
        "email_cta": "Scrivi una email",
        "phone_label": "Telefono",
        "phone_cta": "Chiama l'assistenza",
        "wa_label": "WhatsApp",
        "wa_cta": "Apri la chat",
        "h_company": "Dati azienda",
        "company_html": "<strong>Eurolicenze</strong>, marchio di Licensoft di Cardelli Antonino<br>Via Trento 5/A, 20015 Parabiago (MI), Italia<br>P.IVA 11461870963",
        "h_hours": "Orari e lingua",
        "hours_row1_label": "Lunedì – Sabato",
        "hours_row1_value": "08:00 – 19:00",
        "hours_row2_label": "Lingua di assistenza",
        "hours_row2_value": "Italiano",
        "h_before": "Prima di scriverci",
        "before_returns": "Resi e rimborsi",
        "before_consultation": "Consulenza software",
    },
    "en": {
        "skip": "Skip to main content",
        "title": "Contact — Eurolicenze",
        "description": "Contact Eurolicenze for order and licence activation support by email, phone or WhatsApp, Monday to Saturday, 08:00–19:00 Italy time.",
        "home": "Home",
        "breadcrumb": "Contact",
        "eyebrow": "Customer support",
        "h1": "Contact",
        "lede": "For questions about orders, digital delivery or licence activation, our team is available through the channels below.",
        "meta_hours": "Mon–Sat, 08:00–19:00 (Italy time)",
        "meta_lang": "Support in English",
        "h_channels": "Support channels",
        "email_label": "Email",
        "email_cta": "Send an email",
        "phone_label": "Phone",
        "phone_cta": "Call support",
        "wa_label": "WhatsApp",
        "wa_cta": "Open chat",
        "h_company": "Company details",
        "company_html": "<strong>Eurolicenze</strong>, a brand of Licensoft di Cardelli Antonino<br>Via Trento 5/A, 20015 Parabiago (MI), Italy<br>VAT IT11461870963",
        "h_hours": "Hours & language",
        "hours_row1_label": "Monday – Saturday",
        "hours_row1_value": "08:00 – 19:00 (Italy time)",
        "hours_row2_label": "Support language",
        "hours_row2_value": "English",
        "h_before": "Before you contact us",
        "before_returns": "Returns and refunds",
        "before_consultation": "Software consultation",
    },
    "fr": {
        "skip": "Aller au contenu principal",
        "title": "Contact — Eurolicenze",
        "description": "Contactez Eurolicenze pour l'assistance commandes et activation de licences via email, téléphone ou WhatsApp, du lundi au samedi, 08:00–19:00 heure italienne.",
        "home": "Accueil",
        "breadcrumb": "Contact",
        "eyebrow": "Assistance client",
        "h1": "Contact",
        "lede": "Pour toute question sur les commandes, la livraison numérique ou l'activation des licences, notre équipe est disponible sur les canaux ci-dessous.",
        "meta_hours": "Lun–Sam, 08:00–19:00 (heure italienne)",
        "meta_lang": "Assistance en anglais",
        "h_channels": "Canaux d'assistance",
        "email_label": "E-mail",
        "email_cta": "Écrire un e-mail",
        "phone_label": "Téléphone",
        "phone_cta": "Appeler l'assistance",
        "wa_label": "WhatsApp",
        "wa_cta": "Ouvrir la conversation",
        "h_company": "Informations société",
        "company_html": "<strong>Eurolicenze</strong>, marque de Licensoft di Cardelli Antonino<br>Via Trento 5/A, 20015 Parabiago (MI), Italie<br>TVA IT11461870963",
        "h_hours": "Horaires et langue",
        "hours_row1_label": "Lundi – Samedi",
        "hours_row1_value": "08:00 – 19:00 (heure italienne)",
        "hours_row2_label": "Langue d'assistance",
        "hours_row2_value": "Anglais",
        "h_before": "Avant de nous écrire",
        "before_returns": "Retours et remboursements",
        "before_consultation": "Conseil logiciel",
    },
    "de": {
        "skip": "Zum Hauptinhalt springen",
        "title": "Kontakt — Eurolicenze",
        "description": "Kontaktieren Sie Eurolicenze zu Bestellungen und Lizenzaktivierung per E-Mail, Telefon oder WhatsApp, Montag bis Samstag, 08:00–19:00 Uhr italienischer Zeit.",
        "home": "Startseite",
        "breadcrumb": "Kontakt",
        "eyebrow": "Kundensupport",
        "h1": "Kontakt",
        "lede": "Bei Fragen zu Bestellungen, digitaler Lieferung oder Lizenzaktivierung steht Ihnen unser Team über die folgenden Kanäle zur Verfügung.",
        "meta_hours": "Mo–Sa, 08:00–19:00 (italienische Zeit)",
        "meta_lang": "Support auf Englisch",
        "h_channels": "Support-Kanäle",
        "email_label": "E-Mail",
        "email_cta": "E-Mail schreiben",
        "phone_label": "Telefon",
        "phone_cta": "Support anrufen",
        "wa_label": "WhatsApp",
        "wa_cta": "Chat öffnen",
        "h_company": "Unternehmensdaten",
        "company_html": "<strong>Eurolicenze</strong>, eine Marke von Licensoft di Cardelli Antonino<br>Via Trento 5/A, 20015 Parabiago (MI), Italien<br>USt-IdNr. IT11461870963",
        "h_hours": "Öffnungszeiten & Sprache",
        "hours_row1_label": "Montag – Samstag",
        "hours_row1_value": "08:00 – 19:00 (italienische Zeit)",
        "hours_row2_label": "Support-Sprache",
        "hours_row2_value": "Englisch",
        "h_before": "Bevor Sie uns schreiben",
        "before_returns": "Rückgabe und Erstattung",
        "before_consultation": "Softwareberatung",
    },
    "es": {
        "skip": "Ir al contenido principal",
        "title": "Contacto — Eurolicenze",
        "description": "Contacta con Eurolicenze para asistencia de pedidos y activación de licencias por email, teléfono o WhatsApp, de lunes a sábado, 08:00–19:00 hora de Italia.",
        "home": "Inicio",
        "breadcrumb": "Contacto",
        "eyebrow": "Atención al cliente",
        "h1": "Contacto",
        "lede": "Para consultas sobre pedidos, entrega digital o activación de licencias, nuestro equipo está disponible en los canales siguientes.",
        "meta_hours": "Lun–Sáb, 08:00–19:00 (hora de Italia)",
        "meta_lang": "Asistencia en inglés",
        "h_channels": "Canales de asistencia",
        "email_label": "Email",
        "email_cta": "Enviar un email",
        "phone_label": "Teléfono",
        "phone_cta": "Llamar a asistencia",
        "wa_label": "WhatsApp",
        "wa_cta": "Abrir chat",
        "h_company": "Datos de la empresa",
        "company_html": "<strong>Eurolicenze</strong>, marca de Licensoft di Cardelli Antonino<br>Via Trento 5/A, 20015 Parabiago (MI), Italia<br>NIF-IVA IT11461870963",
        "h_hours": "Horario e idioma",
        "hours_row1_label": "Lunes – Sábado",
        "hours_row1_value": "08:00 – 19:00 (hora de Italia)",
        "hours_row2_label": "Idioma de asistencia",
        "hours_row2_value": "Inglés",
        "h_before": "Antes de escribirnos",
        "before_returns": "Devoluciones y reembolsos",
        "before_consultation": "Asesoramiento de software",
    },
    "pt": {
        "skip": "Ir para o conteúdo principal",
        "title": "Contactos — Eurolicenze",
        "description": "Contacta a Eurolicenze para assistência sobre encomendas e ativação de licenças por email, telefone ou WhatsApp, de segunda a sábado, 08:00–19:00 hora de Itália.",
        "home": "Início",
        "breadcrumb": "Contactos",
        "eyebrow": "Apoio ao cliente",
        "h1": "Contactos",
        "lede": "Para dúvidas sobre encomendas, entrega digital ou ativação de licenças, a nossa equipa está disponível através dos canais abaixo.",
        "meta_hours": "Seg–Sáb, 08:00–19:00 (hora de Itália)",
        "meta_lang": "Apoio em inglês",
        "h_channels": "Canais de apoio",
        "email_label": "Email",
        "email_cta": "Enviar um email",
        "phone_label": "Telefone",
        "phone_cta": "Ligar para o apoio",
        "wa_label": "WhatsApp",
        "wa_cta": "Abrir conversa",
        "h_company": "Dados da empresa",
        "company_html": "<strong>Eurolicenze</strong>, marca de Licensoft di Cardelli Antonino<br>Via Trento 5/A, 20015 Parabiago (MI), Itália<br>NIF IT11461870963",
        "h_hours": "Horário e idioma",
        "hours_row1_label": "Segunda – Sábado",
        "hours_row1_value": "08:00 – 19:00 (hora de Itália)",
        "hours_row2_label": "Idioma de apoio",
        "hours_row2_value": "Inglês",
        "h_before": "Antes de nos escreveres",
        "before_returns": "Devoluções e reembolsos",
        "before_consultation": "Consultoria de software",
    },
    "nl": {
        "skip": "Naar de hoofdinhoud",
        "title": "Contact — Eurolicenze",
        "description": "Neem contact op met Eurolicenze voor hulp bij bestellingen en licentieactivering via e-mail, telefoon of WhatsApp, maandag tot en met zaterdag, 08:00–19:00 Italiaanse tijd.",
        "home": "Home",
        "breadcrumb": "Contact",
        "eyebrow": "Klantenservice",
        "h1": "Contact",
        "lede": "Voor vragen over bestellingen, digitale levering of licentieactivering is ons team bereikbaar via de onderstaande kanalen.",
        "meta_hours": "Ma–za, 08:00–19:00 (Italiaanse tijd)",
        "meta_lang": "Ondersteuning in het Engels",
        "h_channels": "Ondersteuningskanalen",
        "email_label": "E-mail",
        "email_cta": "E-mail versturen",
        "phone_label": "Telefoon",
        "phone_cta": "Bellen met support",
        "wa_label": "WhatsApp",
        "wa_cta": "Chat openen",
        "h_company": "Bedrijfsgegevens",
        "company_html": "<strong>Eurolicenze</strong>, merk van Licensoft di Cardelli Antonino<br>Via Trento 5/A, 20015 Parabiago (MI), Italië<br>BTW IT11461870963",
        "h_hours": "Openingstijden en taal",
        "hours_row1_label": "Maandag – zaterdag",
        "hours_row1_value": "08:00 – 19:00 (Italiaanse tijd)",
        "hours_row2_label": "Ondersteuningstaal",
        "hours_row2_value": "Engels",
        "h_before": "Voordat u ons schrijft",
        "before_returns": "Retourneren en terugbetalingen",
        "before_consultation": "Softwareadvies",
    },
}

ICON_EMAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 16.42v2.83a1.5 1.5 0 0 1-1.63 1.5 14.87 14.87 0 0 1-6.48-2.31 14.66 14.66 0 0 1-4.5-4.5 14.87 14.87 0 0 1-2.31-6.51A1.5 1.5 0 0 1 7.57 5h2.83a1.5 1.5 0 0 1 1.5 1.29c.1.79.29 1.56.56 2.3a1.5 1.5 0 0 1-.34 1.58l-1.2 1.2a12 12 0 0 0 4.5 4.5l1.2-1.2a1.5 1.5 0 0 1 1.58-.34c.74.27 1.51.46 2.3.56A1.5 1.5 0 0 1 21 16.42z"/></svg>'
ICON_CHAT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-4.8 7.6 8.5 8.5 0 0 1-8.9-.9L3 20l1.8-4.3a8.38 8.38 0 0 1-.8-3.7 8.5 8.5 0 0 1 8.5-8.5h.3a8.48 8.48 0 0 1 8.2 8.5z"/></svg>'
ICON_BUILDING = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 21V5a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v16"/><path d="M14 9h4a1 1 0 0 1 1 1v11"/><path d="M3 21h18"/><path d="M9 7h.01M9 11h.01M9 15h.01"/></svg>'
ICON_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
ICON_HOURS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
ICON_ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def page(lang: str) -> str:
    t = COPY[lang]
    url = f"https://eurolicenze.com/{lang}/contacts"
    consultation_url = f"{CONSULTATION_SLUG[lang]}"
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": "https://eurolicenze.com/#organization",
                "name": "Eurolicenze",
                "url": "https://eurolicenze.com/",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://eurolicenze.com/logo/logo-header-400.webp",
                },
                "email": "Desk@eurolicenze.com",
                "telephone": "+39-392-558-0413",
                "vatID": "IT11461870963",
                "contactPoint": [
                    {
                        "@type": "ContactPoint",
                        "contactType": "customer support",
                        "email": "Desk@eurolicenze.com",
                        "telephone": "+39-392-558-0413",
                        "availableLanguage": ["it", "en"],
                        "hoursAvailable": {
                            "@type": "OpeningHoursSpecification",
                            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                            "opens": "08:00",
                            "closes": "19:00",
                        },
                    }
                ],
                "legalName": "Licensoft di Cardelli Antonino",
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
                "@id": "https://eurolicenze.com/#website",
                "url": "https://eurolicenze.com/",
                "name": "Eurolicenze",
                "inLanguage": ["it", "en", "fr", "de", "es", "pt", "nl"],
                "publisher": {"@id": "https://eurolicenze.com/#organization"},
            },
            {
                "@type": "ContactPage",
                "@id": f"{url}#webpage",
                "url": url,
                "name": t["title"],
                "description": t["description"],
                "inLanguage": lang,
                "isPartOf": {"@id": "https://eurolicenze.com/#website"},
                "about": {"@id": "https://eurolicenze.com/#organization"},
            },
        ],
    }
    hreflang = "\n".join(
        f'    <link rel="alternate" hreflang="{lg}" href="https://eurolicenze.com/{lg}/contacts">'
        for lg in ("it", "en", "fr", "de", "es", "pt", "nl")
    )
    hreflang += '\n    <link rel="alternate" hreflang="x-default" href="https://eurolicenze.com/it/contacts">'

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
    <meta property="og:site_name" content="Eurolicenze">
    <meta property="og:title" content="{t['title']}">
    <meta property="og:description" content="{t['description']}">
    <meta property="og:url" content="{url}">
    <meta property="og:locale" content="{LOCALE[lang]}">
    <meta property="og:image" content="https://eurolicenze.com/logo/logo-header-400.webp">

{hreflang}

    <link rel="stylesheet" href="../fonts/montserrat.css">
    <link rel="stylesheet" href="../fonts/source-serif.css">
    <link rel="stylesheet" href="../css/page.css">
    <link rel="stylesheet" href="../css/contacts.css">
    <script src="../js/theme-init.js"></script>
    <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}
    </script>
</head>
<body>
    <a class="skip-link" href="#main">{t['skip']}</a>

    <ecommerce-header translate="no" class="notranslate"></ecommerce-header>

    <main id="main" class="contacts-page">
        <nav class="contacts-breadcrumb" aria-label="Breadcrumb">
            <a href="./">{t['home']}</a> <span aria-hidden="true">/</span> {t['breadcrumb']}
        </nav>

        <section class="contacts-hero" aria-labelledby="contacts-title">
            <p class="contacts-eyebrow">{t['eyebrow']}</p>
            <h1 id="contacts-title" class="contacts-title">{t['h1']}</h1>
            <p class="contacts-lede">{t['lede']}</p>
            <ul class="contacts-meta">
                <li>{ICON_CLOCK}<span>{t['meta_hours']}</span></li>
                <li>{ICON_CHAT}<span>{t['meta_lang']}</span></li>
            </ul>
        </section>

        <section class="contacts-section" aria-labelledby="contacts-channels-title">
            <h2 id="contacts-channels-title" class="contacts-section__heading">{t['h_channels']}</h2>
            <div class="contacts-channel-grid">
                <div class="contacts-channel-card">
                    <span class="contacts-channel-card__icon">{ICON_EMAIL}</span>
                    <span class="contacts-channel-card__label">{t['email_label']}</span>
                    <a class="contacts-channel-card__value" href="mailto:Desk@eurolicenze.com">Desk@eurolicenze.com</a>
                    <a class="contacts-channel-card__hint" href="mailto:Desk@eurolicenze.com">{t['email_cta']}</a>
                </div>
                <div class="contacts-channel-card">
                    <span class="contacts-channel-card__icon">{ICON_PHONE}</span>
                    <span class="contacts-channel-card__label">{t['phone_label']}</span>
                    <a class="contacts-channel-card__value account-phone" href="tel:+393925580413">+39 392 558 0413</a>
                    <a class="contacts-channel-card__hint" href="tel:+393925580413">{t['phone_cta']}</a>
                </div>
                <div class="contacts-channel-card">
                    <span class="contacts-channel-card__icon">{ICON_CHAT}</span>
                    <span class="contacts-channel-card__label">{t['wa_label']}</span>
                    <a class="contacts-channel-card__value" href="https://wa.me/393925580413" target="_blank" rel="noopener noreferrer">+39 392 558 0413</a>
                    <a class="contacts-channel-card__hint" href="https://wa.me/393925580413" target="_blank" rel="noopener noreferrer">{t['wa_cta']}</a>
                </div>
            </div>
        </section>

        <section class="contacts-section">
            <div class="contacts-info-grid">
                <div class="contacts-info-card">
                    <div class="contacts-info-card__head">{ICON_BUILDING}<h2>{t['h_company']}</h2></div>
                    <address>{t['company_html']}</address>
                </div>
                <div class="contacts-info-card">
                    <div class="contacts-info-card__head">{ICON_HOURS}<h2>{t['h_hours']}</h2></div>
                    <div class="contacts-hours-rows">
                        <div class="contacts-hours-row"><span>{t['hours_row1_label']}</span><strong>{t['hours_row1_value']}</strong></div>
                        <div class="contacts-hours-row"><span>{t['hours_row2_label']}</span><strong>{t['hours_row2_value']}</strong></div>
                    </div>
                </div>
            </div>
        </section>

        <section class="contacts-section" aria-labelledby="contacts-before-title">
            <h2 id="contacts-before-title" class="contacts-section__heading">{t['h_before']}</h2>
            <div class="contacts-quicklinks">
                <a class="contacts-quicklink-card" href="returns-and-refunds">
                    <span>{t['before_returns']}</span>
                    {ICON_ARROW}
                </a>
                <a class="contacts-quicklink-card" href="{consultation_url}">
                    <span>{t['before_consultation']}</span>
                    {ICON_ARROW}
                </a>
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
    errors = []
    for lang in COPY:
        html = load(lang, "contacts")
        if html is None:
            errors.append(f"{lang}/contacts.html: manca la pagina contatti")
            continue
        errors += pipeline_errors(lang, "contacts", html)

    fail_if(errors, f"OK: pagina contatti x {len(COPY)} lingue")


if __name__ == "__main__":
    main()
