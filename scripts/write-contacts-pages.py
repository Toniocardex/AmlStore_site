#!/usr/bin/env python3
"""Generate static contacts.html for it/en/fr/de/es (direct channels only)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LOCALE = {"it": "it_IT", "en": "en_US", "fr": "fr_FR", "de": "de_DE", "es": "es_ES"}

COPY = {
    "it": {
        "skip": "Vai al contenuto principale",
        "title": "Contatti — Aml Store",
        "description": "Contatta Aml Store per assistenza su ordini e attivazione licenze: email e WhatsApp. Risposta tipica entro 1 giorno lavorativo.",
        "h1": "Contatti",
        "intro": "Per domande su ordini, consegna digitale o attivazione delle licenze, scrivici tramite i canali qui sotto. Ti rispondiamo di solito entro <strong>1 giorno lavorativo</strong>.",
        "h_channels": "Canali di assistenza",
        "email_label": "Email",
        "wa_label": "WhatsApp / telefono",
        "h_company": "Dati azienda",
        "company": "<strong>Aml Store</strong> — P.IVA 11461870963",
        "cta_email": "Scrivi una email",
        "cta_wa": "Apri WhatsApp",
    },
    "en": {
        "skip": "Skip to main content",
        "title": "Contact — Aml Store",
        "description": "Contact Aml Store for order and licence activation support by email or WhatsApp. Typical reply within 1 business day.",
        "h1": "Contact",
        "intro": "For questions about orders, digital delivery or licence activation, reach us through the channels below. We typically reply within <strong>1 business day</strong>.",
        "h_channels": "Support channels",
        "email_label": "Email",
        "wa_label": "WhatsApp / phone",
        "h_company": "Company details",
        "company": "<strong>Aml Store</strong> — VAT 11461870963",
        "cta_email": "Send an email",
        "cta_wa": "Open WhatsApp",
    },
    "fr": {
        "skip": "Aller au contenu principal",
        "title": "Contact — Aml Store",
        "description": "Contactez Aml Store pour l'assistance commandes et activation de licences : e-mail et WhatsApp. Réponse typique sous 1 jour ouvré.",
        "h1": "Contact",
        "intro": "Pour les questions sur les commandes, la livraison numérique ou l'activation des licences, utilisez les canaux ci-dessous. Nous répondons en général sous <strong>1 jour ouvré</strong>.",
        "h_channels": "Canaux d'assistance",
        "email_label": "E-mail",
        "wa_label": "WhatsApp / téléphone",
        "h_company": "Informations société",
        "company": "<strong>Aml Store</strong> — TVA 11461870963",
        "cta_email": "Écrire un e-mail",
        "cta_wa": "Ouvrir WhatsApp",
    },
    "de": {
        "skip": "Zum Hauptinhalt springen",
        "title": "Kontakt — Aml Store",
        "description": "Kontaktieren Sie Aml Store zu Bestellungen und Lizenzaktivierung per E-Mail oder WhatsApp. Typische Antwort innerhalb von 1 Werktag.",
        "h1": "Kontakt",
        "intro": "Bei Fragen zu Bestellungen, digitaler Lieferung oder Lizenzaktivierung erreichen Sie uns über die folgenden Kanäle. Wir antworten in der Regel innerhalb von <strong>1 Werktag</strong>.",
        "h_channels": "Support-Kanäle",
        "email_label": "E-Mail",
        "wa_label": "WhatsApp / Telefon",
        "h_company": "Unternehmensdaten",
        "company": "<strong>Aml Store</strong> — USt-IdNr. 11461870963",
        "cta_email": "E-Mail schreiben",
        "cta_wa": "WhatsApp öffnen",
    },
    "es": {
        "skip": "Ir al contenido principal",
        "title": "Contacto — Aml Store",
        "description": "Contacta con Aml Store para asistencia de pedidos y activación de licencias por email o WhatsApp. Respuesta habitual en 1 día laborable.",
        "h1": "Contacto",
        "intro": "Para consultas sobre pedidos, entrega digital o activación de licencias, usa los canales siguientes. Solemos responder en <strong>1 día laborable</strong>.",
        "h_channels": "Canales de asistencia",
        "email_label": "Email",
        "wa_label": "WhatsApp / teléfono",
        "h_company": "Datos de la empresa",
        "company": "<strong>Aml Store</strong> — NIF 11461870963",
        "cta_email": "Enviar un email",
        "cta_wa": "Abrir WhatsApp",
    },
}


def page(lang: str) -> str:
    t = COPY[lang]
    url = f"https://aml-store.com/{lang}/contacts"
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
                        "availableLanguage": ["it", "en", "fr", "de", "es"],
                    }
                ],
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
    <link rel="stylesheet" href="../css/page.css">
    <script src="../js/theme-init.js"></script>
    <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}
    </script>
</head>
<body>
    <a class="skip-link" href="#main">{t['skip']}</a>

    <ecommerce-header translate="no" class="notranslate"></ecommerce-header>

    <main id="main" class="legal-doc contacts-page">
        <h1>{t['h1']}</h1>
        <p>{t['intro']}</p>

        <h2>{t['h_channels']}</h2>
        <ul class="contacts-channels">
            <li>
                <span class="contacts-channels__label">{t['email_label']}</span>
                <a href="mailto:Info@amlstore.it">Info@amlstore.it</a>
                <span class="contacts-channels__cta"> — {t['cta_email']}</span>
            </li>
            <li>
                <span class="contacts-channels__label">{t['wa_label']}</span>
                <a class="account-phone" href="https://wa.me/393925580413" target="_blank" rel="noopener noreferrer">+39 392 558 0413</a>
                <span class="contacts-channels__cta"> — {t['cta_wa']}</span>
            </li>
        </ul>

        <h2>{t['h_company']}</h2>
        <p>{t['company']}</p>
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
