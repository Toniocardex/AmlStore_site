#!/usr/bin/env python3
"""Generate static contacts.html for it/en/fr/de/es — corporate layout.

Content (support hours, address, VAT) matches the JSON-LD below and the
translated labels already used in components/footer.js, so this stays a
single source of truth for the five language variants.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LOCALE = {"it": "it_IT", "en": "en_US", "fr": "fr_FR", "de": "de_DE", "es": "es_ES"}

# slug of the pre-sale "software consultation" page per locale (see components/footer.js)
CONSULTATION_SLUG = {"it": "consulenza", "en": "consultation", "fr": "consultation", "de": "beratung", "es": "consultoria"}

COPY = {
    "it": {
        "skip": "Vai al contenuto principale",
        "title": "Contatti — Aml Store",
        "description": "Contatta Aml Store per assistenza su ordini e attivazione licenze via email, telefono o WhatsApp, dal lunedì al venerdì, 09:00–19:00.",
        "home": "Home",
        "breadcrumb": "Contatti",
        "eyebrow": "Assistenza clienti",
        "h1": "Contatti",
        "lede": "Per domande su ordini, consegna digitale o attivazione delle licenze, il nostro team è a tua disposizione sui canali qui sotto.",
        "meta_hours": "Lun–Ven, 09:00–19:00",
        "meta_lang": "Assistenza in italiano",
        "h_channels": "Canali di assistenza",
        "email_label": "Email",
        "email_cta": "Scrivi una email",
        "phone_label": "Telefono",
        "phone_cta": "Chiama l'assistenza",
        "wa_label": "WhatsApp",
        "wa_cta": "Apri la chat",
        "h_company": "Dati azienda",
        "company_html": "<strong>Aml Store</strong>, marchio di Licensoft di Cardelli Antonino<br>Via Trento 5/A, 20015 Parabiago (MI), Italia<br>P.IVA 11461870963",
        "h_hours": "Orari e lingua",
        "hours_row1_label": "Lunedì – Venerdì",
        "hours_row1_value": "09:00 – 19:00",
        "hours_row2_label": "Lingua di assistenza",
        "hours_row2_value": "Italiano",
        "h_before": "Prima di scriverci",
        "before_returns": "Resi e rimborsi",
        "before_consultation": "Consulenza software",
    },
    "en": {
        "skip": "Skip to main content",
        "title": "Contact — Aml Store",
        "description": "Contact Aml Store for order and licence activation support by email, phone or WhatsApp, Monday to Friday, 09:00–19:00 Italy time.",
        "home": "Home",
        "breadcrumb": "Contact",
        "eyebrow": "Customer support",
        "h1": "Contact",
        "lede": "For questions about orders, digital delivery or licence activation, our team is available through the channels below.",
        "meta_hours": "Mon–Fri, 09:00–19:00 (Italy time)",
        "meta_lang": "Support in English",
        "h_channels": "Support channels",
        "email_label": "Email",
        "email_cta": "Send an email",
        "phone_label": "Phone",
        "phone_cta": "Call support",
        "wa_label": "WhatsApp",
        "wa_cta": "Open chat",
        "h_company": "Company details",
        "company_html": "<strong>Aml Store</strong>, a brand of Licensoft di Cardelli Antonino<br>Via Trento 5/A, 20015 Parabiago (MI), Italy<br>VAT IT11461870963",
        "h_hours": "Hours & language",
        "hours_row1_label": "Monday – Friday",
        "hours_row1_value": "09:00 – 19:00 (Italy time)",
        "hours_row2_label": "Support language",
        "hours_row2_value": "English",
        "h_before": "Before you contact us",
        "before_returns": "Returns and refunds",
        "before_consultation": "Software consultation",
    },
    "fr": {
        "skip": "Aller au contenu principal",
        "title": "Contact — Aml Store",
        "description": "Contactez Aml Store pour l'assistance commandes et activation de licences via email, téléphone ou WhatsApp, du lundi au vendredi, 09:00–19:00 heure italienne.",
        "home": "Accueil",
        "breadcrumb": "Contact",
        "eyebrow": "Assistance client",
        "h1": "Contact",
        "lede": "Pour toute question sur les commandes, la livraison numérique ou l'activation des licences, notre équipe est disponible sur les canaux ci-dessous.",
        "meta_hours": "Lun–Ven, 09:00–19:00 (heure italienne)",
        "meta_lang": "Assistance en anglais",
        "h_channels": "Canaux d'assistance",
        "email_label": "E-mail",
        "email_cta": "Écrire un e-mail",
        "phone_label": "Téléphone",
        "phone_cta": "Appeler l'assistance",
        "wa_label": "WhatsApp",
        "wa_cta": "Ouvrir la conversation",
        "h_company": "Informations société",
        "company_html": "<strong>Aml Store</strong>, marque de Licensoft di Cardelli Antonino<br>Via Trento 5/A, 20015 Parabiago (MI), Italie<br>TVA IT11461870963",
        "h_hours": "Horaires et langue",
        "hours_row1_label": "Lundi – Vendredi",
        "hours_row1_value": "09:00 – 19:00 (heure italienne)",
        "hours_row2_label": "Langue d'assistance",
        "hours_row2_value": "Anglais",
        "h_before": "Avant de nous écrire",
        "before_returns": "Retours et remboursements",
        "before_consultation": "Conseil logiciel",
    },
    "de": {
        "skip": "Zum Hauptinhalt springen",
        "title": "Kontakt — Aml Store",
        "description": "Kontaktieren Sie Aml Store zu Bestellungen und Lizenzaktivierung per E-Mail, Telefon oder WhatsApp, Montag bis Freitag, 09:00–19:00 Uhr italienischer Zeit.",
        "home": "Startseite",
        "breadcrumb": "Kontakt",
        "eyebrow": "Kundensupport",
        "h1": "Kontakt",
        "lede": "Bei Fragen zu Bestellungen, digitaler Lieferung oder Lizenzaktivierung steht Ihnen unser Team über die folgenden Kanäle zur Verfügung.",
        "meta_hours": "Mo–Fr, 09:00–19:00 (italienische Zeit)",
        "meta_lang": "Support auf Englisch",
        "h_channels": "Support-Kanäle",
        "email_label": "E-Mail",
        "email_cta": "E-Mail schreiben",
        "phone_label": "Telefon",
        "phone_cta": "Support anrufen",
        "wa_label": "WhatsApp",
        "wa_cta": "Chat öffnen",
        "h_company": "Unternehmensdaten",
        "company_html": "<strong>Aml Store</strong>, eine Marke von Licensoft di Cardelli Antonino<br>Via Trento 5/A, 20015 Parabiago (MI), Italien<br>USt-IdNr. IT11461870963",
        "h_hours": "Öffnungszeiten & Sprache",
        "hours_row1_label": "Montag – Freitag",
        "hours_row1_value": "09:00 – 19:00 (italienische Zeit)",
        "hours_row2_label": "Support-Sprache",
        "hours_row2_value": "Englisch",
        "h_before": "Bevor Sie uns schreiben",
        "before_returns": "Rückgabe und Erstattung",
        "before_consultation": "Softwareberatung",
    },
    "es": {
        "skip": "Ir al contenido principal",
        "title": "Contacto — Aml Store",
        "description": "Contacta con Aml Store para asistencia de pedidos y activación de licencias por email, teléfono o WhatsApp, de lunes a viernes, 09:00–19:00 hora de Italia.",
        "home": "Inicio",
        "breadcrumb": "Contacto",
        "eyebrow": "Atención al cliente",
        "h1": "Contacto",
        "lede": "Para consultas sobre pedidos, entrega digital o activación de licencias, nuestro equipo está disponible en los canales siguientes.",
        "meta_hours": "Lun–Vie, 09:00–19:00 (hora de Italia)",
        "meta_lang": "Asistencia en inglés",
        "h_channels": "Canales de asistencia",
        "email_label": "Email",
        "email_cta": "Enviar un email",
        "phone_label": "Teléfono",
        "phone_cta": "Llamar a asistencia",
        "wa_label": "WhatsApp",
        "wa_cta": "Abrir chat",
        "h_company": "Datos de la empresa",
        "company_html": "<strong>Aml Store</strong>, marca de Licensoft di Cardelli Antonino<br>Via Trento 5/A, 20015 Parabiago (MI), Italia<br>NIF-IVA IT11461870963",
        "h_hours": "Horario e idioma",
        "hours_row1_label": "Lunes – Viernes",
        "hours_row1_value": "09:00 – 19:00 (hora de Italia)",
        "hours_row2_label": "Idioma de asistencia",
        "hours_row2_value": "Inglés",
        "h_before": "Antes de escribirnos",
        "before_returns": "Devoluciones y reembolsos",
        "before_consultation": "Asesoramiento de software",
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
    url = f"https://aml-store.com/{lang}/contacts"
    consultation_url = f"{CONSULTATION_SLUG[lang]}"
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
                "contactPoint": [
                    {
                        "@type": "ContactPoint",
                        "contactType": "customer support",
                        "email": "Info@amlstore.it",
                        "telephone": "+39-392-558-0413",
                        "availableLanguage": ["it", "en"],
                        "hoursAvailable": {
                            "@type": "OpeningHoursSpecification",
                            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                            "opens": "09:00",
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
                "@id": "https://aml-store.com/#website",
                "url": "https://aml-store.com/",
                "name": "Aml Store",
                "inLanguage": ["it", "en", "fr", "de", "es"],
                "publisher": {"@id": "https://aml-store.com/#organization"},
            },
            {
                "@type": "ContactPage",
                "@id": f"{url}#webpage",
                "url": url,
                "name": t["title"],
                "description": t["description"],
                "inLanguage": lang,
                "isPartOf": {"@id": "https://aml-store.com/#website"},
                "about": {"@id": "https://aml-store.com/#organization"},
            },
        ],
    }
    hreflang = "\n".join(
        f'    <link rel="alternate" hreflang="{lg}" href="https://aml-store.com/{lg}/contacts">'
        for lg in ("it", "en", "fr", "de", "es")
    )
    hreflang += '\n    <link rel="alternate" hreflang="x-default" href="https://aml-store.com/it/contacts">'

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
                    <a class="contacts-channel-card__value" href="mailto:Info@amlstore.it">Info@amlstore.it</a>
                    <a class="contacts-channel-card__hint" href="mailto:Info@amlstore.it">{t['email_cta']}</a>
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
    for lang in COPY:
        path = ROOT / lang / "contacts.html"
        path.write_text(page(lang), encoding="utf-8")
        print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
