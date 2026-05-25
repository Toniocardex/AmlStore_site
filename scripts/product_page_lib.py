#!/usr/bin/env python3
"""Shared helpers for generating static product and catalog pages."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
LANGS = ("it", "en", "fr", "de", "es")
LOCALE = {"it": "it_IT", "en": "en_US", "fr": "fr_FR", "de": "de_DE", "es": "es_ES"}

BASE_LABELS = {
    "it": {
        "skip": "Vai al contenuto principale",
        "add": "Aggiungi al carrello",
        "detail": "Vedi prodotto",
        "price_label": "Il nostro prezzo",
        "tax": "Tasse incluse. Nessun costo di spedizione.",
        "sticky": "Acquisto rapido",
        "steps_title": "Consegna e attivazione",
        "step_order": "Ordine",
        "step_checkout": "Checkout sicuro",
        "step_email": "Email",
        "step_email_desc": "Codice e istruzioni in pochi minuti",
        "step_act": "Attivazione",
        "desc_suffix": "Licenza digitale originale, consegna via email in pochi minuti.",
    },
    "en": {
        "skip": "Skip to main content",
        "add": "Add to cart",
        "detail": "View product",
        "price_label": "Our price",
        "tax": "Tax included. No shipping fees.",
        "sticky": "Quick purchase",
        "steps_title": "Delivery and activation",
        "step_order": "Order",
        "step_checkout": "Secure checkout",
        "step_email": "Email",
        "step_email_desc": "Code and instructions within minutes",
        "step_act": "Activation",
        "desc_suffix": "Genuine digital licence, email delivery within minutes.",
    },
    "fr": {
        "skip": "Aller au contenu principal",
        "add": "Ajouter au panier",
        "detail": "Voir le produit",
        "price_label": "Notre prix",
        "tax": "Taxes incluses. Pas de frais de port.",
        "sticky": "Achat rapide",
        "steps_title": "Livraison et activation",
        "step_order": "Commande",
        "step_checkout": "Paiement sécurisé",
        "step_email": "E-mail",
        "step_email_desc": "Code et instructions en quelques minutes",
        "step_act": "Activation",
        "desc_suffix": "Licence numérique originale, livraison par e-mail en quelques minutes.",
    },
    "de": {
        "skip": "Zum Hauptinhalt springen",
        "add": "In den Warenkorb",
        "detail": "Produkt ansehen",
        "price_label": "Unser Preis",
        "tax": "Steuern inklusive. Keine Versandkosten.",
        "sticky": "Schnellkauf",
        "steps_title": "Lieferung und Aktivierung",
        "step_order": "Bestellung",
        "step_checkout": "Sicherer Checkout",
        "step_email": "E-Mail",
        "step_email_desc": "Code und Anleitung in wenigen Minuten",
        "step_act": "Aktivierung",
        "desc_suffix": "Originale digitale Lizenz, Lieferung per E-Mail in wenigen Minuten.",
    },
    "es": {
        "skip": "Ir al contenido principal",
        "add": "Añadir al carrito",
        "detail": "Ver producto",
        "price_label": "Nuestro precio",
        "tax": "Impuestos incluidos. Sin gastos de envío.",
        "sticky": "Compra rápida",
        "steps_title": "Entrega y activación",
        "step_order": "Pedido",
        "step_checkout": "Checkout seguro",
        "step_email": "Email",
        "step_email_desc": "Código e instrucciones en minutos",
        "step_act": "Activación",
        "desc_suffix": "Licencia digital original, entrega por email en minutos.",
    },
}

CATALOG_META = {
    "suite-office": {
        "it": ("Suite Office", "Office perpetuo, app standalone e strumenti di produttività Microsoft."),
        "en": ("Office suite", "Perpetual Office, standalone apps and Microsoft productivity tools."),
        "fr": ("Suite Office", "Office perpétuel, applications autonomes et outils Microsoft."),
        "de": ("Office-Suite", "Office-Dauerlizenzen, Einzelapps und Microsoft-Produktivität."),
        "es": ("Suite Office", "Office perpetuo, apps independientes y productividad Microsoft."),
    },
    "sistemi-operativi": {
        "it": ("Sistemi Operativi", "Licenze Windows originali con consegna digitale rapida."),
        "en": ("Operating systems", "Genuine Windows licences with fast digital delivery."),
        "fr": ("Systèmes d'exploitation", "Licences Windows officielles, livraison numérique rapide."),
        "de": ("Betriebssysteme", "Originale Windows-Lizenzen mit schneller digitaler Lieferung."),
        "es": ("Sistemas operativos", "Licencias Windows originales con entrega digital rápida."),
    },
    "pacchetti": {
        "it": ("Pacchetti", "Bundle digitali Windows, Microsoft 365 e sicurezza."),
        "en": ("Bundles", "Digital bundles: Windows, Microsoft 365 and security."),
        "fr": ("Packs", "Packs numériques Windows, Microsoft 365 et sécurité."),
        "de": ("Pakete", "Digitale Pakete: Windows, Microsoft 365 und Sicherheit."),
        "es": ("Packs", "Packs digitales Windows, Microsoft 365 y seguridad."),
    },
    "antivirus": {
        "it": ("Antivirus", "Protezione per PC e dispositivi: licenze digitali originali."),
        "en": ("Antivirus", "Protection for PCs and devices: genuine digital licences."),
        "fr": ("Antivirus", "Protection PC et appareils : licences numériques officielles."),
        "de": ("Antivirus", "Schutz für PC und Geräte: originale digitale Lizenzen."),
        "es": ("Antivirus", "Protección para PC y dispositivos: licencias digitales originales."),
    },
    "windows-server": {
        "it": ("Windows Server e SQL", "Licenze server e database Microsoft per infrastrutture."),
        "en": ("Windows Server & SQL", "Microsoft server and database licences for infrastructure."),
        "fr": ("Windows Server et SQL", "Licences serveur et base de données Microsoft."),
        "de": ("Windows Server & SQL", "Microsoft-Server- und Datenbanklizenzen."),
        "es": ("Windows Server y SQL", "Licencias de servidor y base de datos Microsoft."),
    },
    "strumenti": {
        "it": ("Strumenti e altro", "Adobe, backup cloud, formazione e software specializzato."),
        "en": ("Tools & more", "Adobe, cloud backup, training and specialised software."),
        "fr": ("Outils et plus", "Adobe, sauvegarde cloud, formation et logiciels spécialisés."),
        "de": ("Tools & mehr", "Adobe, Cloud-Backup, Schulung und Spezialsoftware."),
        "es": ("Herramientas y más", "Adobe, backup en la nube, formación y software especializado."),
    },
}

TEMPLATE_META = {
    "office": {
        "listing": "suite-office",
        "cat_label": {"it": "Suite Office", "en": "Office suite", "fr": "Suite Office", "de": "Office-Suite", "es": "Suite Office"},
        "eyebrow": {"it": "Licenza perpetua", "en": "Perpetual licence", "fr": "Licence perpétuelle", "de": "Dauerlizenz", "es": "Licencia perpetua"},
        "activation": {"it": "Portale setup.office.com", "en": "Official setup.office.com portal", "fr": "Portail setup.office.com", "de": "setup.office.com-Portal", "es": "Portal setup.office.com"},
        "brand": "Microsoft",
        "blurb": {"it": "Licenza ESD · setup.office.com", "en": "ESD licence · setup.office.com", "fr": "Licence ESD · setup.office.com", "de": "ESD-Lizenz · setup.office.com", "es": "Licencia ESD · setup.office.com"},
    },
    "m365": {
        "listing": "suite-office",
        "cat_label": {"it": "Suite Office", "en": "Office suite", "fr": "Suite Office", "de": "Office-Suite", "es": "Suite Office"},
        "eyebrow": {"it": "Abbonamento Microsoft 365", "en": "Microsoft 365 subscription", "fr": "Abonnement Microsoft 365", "de": "Microsoft-365-Abonnement", "es": "Suscripción Microsoft 365"},
        "activation": {"it": "Account Microsoft ufficiale", "en": "Official Microsoft account", "fr": "Compte Microsoft officiel", "de": "Offizielles Microsoft-Konto", "es": "Cuenta Microsoft oficial"},
        "brand": "Microsoft",
        "blurb": {"it": "Abbonamento · attivazione account Microsoft", "en": "Subscription · Microsoft account activation", "fr": "Abonnement · compte Microsoft", "de": "Abonnement · Microsoft-Konto", "es": "Suscripción · cuenta Microsoft"},
    },
    "windows": {
        "listing": "sistemi-operativi",
        "cat_label": {"it": "Sistemi Operativi", "en": "Operating systems", "fr": "Systèmes d'exploitation", "de": "Betriebssysteme", "es": "Sistemas operativos"},
        "eyebrow": {"it": "Sistema operativo", "en": "Operating system", "fr": "Système d'exploitation", "de": "Betriebssystem", "es": "Sistema operativo"},
        "activation": {"it": "Attivazione ufficiale Microsoft", "en": "Official Microsoft activation", "fr": "Activation Microsoft officielle", "de": "Offizielle Microsoft-Aktivierung", "es": "Activación oficial Microsoft"},
        "brand": "Microsoft",
        "blurb": {"it": "ESD · Attivazione immediata", "en": "ESD · Instant activation", "fr": "ESD · Activation immédiate", "de": "ESD · Sofortige Aktivierung", "es": "ESD · Activación inmediata"},
    },
    "bundle": {
        "listing": "pacchetti",
        "cat_label": {"it": "Pacchetti", "en": "Bundles", "fr": "Packs", "de": "Pakete", "es": "Packs"},
        "eyebrow": {"it": "Pacchetto digitale", "en": "Digital bundle", "fr": "Pack numérique", "de": "Digitales Paket", "es": "Pack digital"},
        "activation": {"it": "Email con codici e istruzioni", "en": "Email with codes and instructions", "fr": "E-mail avec codes et instructions", "de": "E-Mail mit Codes und Anleitung", "es": "Email con códigos e instrucciones"},
        "brand": "Microsoft",
        "blurb": {"it": "Bundle · consegna digitale", "en": "Bundle · digital delivery", "fr": "Pack · livraison numérique", "de": "Paket · digitale Lieferung", "es": "Pack · entrega digital"},
    },
    "antivirus": {
        "listing": "antivirus",
        "cat_label": {"it": "Antivirus", "en": "Antivirus", "fr": "Antivirus", "de": "Antivirus", "es": "Antivirus"},
        "eyebrow": {"it": "Antivirus", "en": "Antivirus", "fr": "Antivirus", "de": "Antivirus", "es": "Antivirus"},
        "activation": {"it": "Portale ufficiale del produttore", "en": "Official vendor portal", "fr": "Portail officiel de l'éditeur", "de": "Offizielles Herstellerportal", "es": "Portal oficial del fabricante"},
        "brand": None,
        "blurb": {"it": "Abbonamento · licenza digitale", "en": "Subscription · digital licence", "fr": "Abonnement · licence numérique", "de": "Abonnement · digitale Lizenz", "es": "Suscripción · licencia digital"},
    },
    "server": {
        "listing": "windows-server",
        "cat_label": {"it": "Windows Server e SQL", "en": "Windows Server & SQL", "fr": "Windows Server et SQL", "de": "Windows Server & SQL", "es": "Windows Server y SQL"},
        "eyebrow": {"it": "Server / database", "en": "Server / database", "fr": "Serveur / base de données", "de": "Server / Datenbank", "es": "Servidor / base de datos"},
        "activation": {"it": "Attivazione ufficiale Microsoft", "en": "Official Microsoft activation", "fr": "Activation Microsoft officielle", "de": "Offizielle Microsoft-Aktivierung", "es": "Activación oficial Microsoft"},
        "brand": "Microsoft",
        "blurb": {"it": "Licenza ESD · server/database", "en": "ESD licence · server/database", "fr": "Licence ESD · serveur/BD", "de": "ESD · Server/Datenbank", "es": "Licencia ESD · servidor/BD"},
    },
    "tool": {
        "listing": "strumenti",
        "cat_label": {"it": "Strumenti e altro", "en": "Tools & more", "fr": "Outils et plus", "de": "Tools & mehr", "es": "Herramientas y más"},
        "eyebrow": {"it": "Software professionale", "en": "Professional software", "fr": "Logiciel professionnel", "de": "Professionelle Software", "es": "Software profesional"},
        "activation": {"it": "Portale ufficiale del produttore", "en": "Official vendor portal", "fr": "Portail officiel de l'éditeur", "de": "Offizielles Herstellerportal", "es": "Portal oficial del fabricante"},
        "brand": None,
        "blurb": {"it": "Licenza digitale · consegna email", "en": "Digital licence · email delivery", "fr": "Licence numérique · e-mail", "de": "Digitale Lizenz · E-Mail", "es": "Licencia digital · email"},
    },
    "backup": {
        "listing": "strumenti",
        "cat_label": {"it": "Strumenti e altro", "en": "Tools & more", "fr": "Outils et plus", "de": "Tools & mehr", "es": "Herramientas y más"},
        "eyebrow": {"it": "Backup cloud", "en": "Cloud backup", "fr": "Sauvegarde cloud", "de": "Cloud-Backup", "es": "Backup en la nube"},
        "activation": {"it": "Portale ufficiale Acronis", "en": "Official Acronis portal", "fr": "Portail Acronis officiel", "de": "Offizielles Acronis-Portal", "es": "Portal oficial Acronis"},
        "brand": "Acronis",
        "blurb": {"it": "Backup · storage cloud incluso", "en": "Backup · cloud storage included", "fr": "Sauvegarde · cloud inclus", "de": "Backup · Cloud-Speicher", "es": "Backup · almacenamiento cloud"},
    },
    "training": {
        "listing": "strumenti",
        "cat_label": {"it": "Strumenti e altro", "en": "Tools & more", "fr": "Outils et plus", "de": "Tools & mehr", "es": "Herramientas y más"},
        "eyebrow": {"it": "Formazione", "en": "Training", "fr": "Formation", "de": "Schulung", "es": "Formación"},
        "activation": {"it": "Download digitale via email", "en": "Digital download via email", "fr": "Téléchargement par e-mail", "de": "Digitaler Download per E-Mail", "es": "Descarga digital por email"},
        "brand": "Microsoft",
        "blurb": {"it": "Guida PDF · consegna immediata", "en": "PDF guide · instant delivery", "fr": "Guide PDF · livraison immédiate", "de": "PDF-Guide · sofortige Lieferung", "es": "Guía PDF · entrega inmediata"},
    },
}


def entry(sku):
    for e in CATALOG:
        if e["sku"] == sku:
            return e
    raise KeyError(sku)


def eur_fmt(minor):
    return f"{minor / 100:.2f}".replace(".", ",")


def pct(sale, compare):
    if compare <= sale:
        return 0
    return int(round((1 - sale / compare) * 100))


def hreflang_block(slug):
    lines = []
    for lg in LANGS:
        lines.append(
            f'    <link rel="alternate" hreflang="{lg}" href="https://aml-store.com/{lg}/{slug}.html">'
        )
    lines.append(
        f'    <link rel="alternate" hreflang="x-default" href="https://aml-store.com/it/{slug}.html">'
    )
    return "\n".join(lines)


def product_card(lang, prod, labels):
    e = entry(prod["sku"])
    sale = e["unitAmountMinor"]
    compare = e["compareAtMinor"]
    disc = pct(sale, compare)
    meta = TEMPLATE_META[prod["template"]]
    name = prod["card_name"]
    blurb = prod.get("blurb") or meta["blurb"][lang]
    slug = prod["slug"]
    image = prod["image"]
    return f"""                <div
                    class="product-card"
                    data-stripe-currency="eur"
                    data-stripe-unit-amount="{sale}"
                    data-stripe-compare-at-amount="{compare}"
                    data-stripe-product-sku="{prod['sku']}"
                    data-discount-percent="{disc}"
                >
                    <a href="{slug}.html" class="product-card-body product-card--link">
                        <div class="product-card-media">
                            <img src="../asset/media/{image}" width="400" height="400" alt="{name}" decoding="async" class="product-card-img" onerror="this.src='../asset/media/home-hero-lifestyle.webp'">
                        </div>
                        <p class="product-card-name">{name}</p>
                        <p class="product-card-blurb">{blurb}</p>
                    </a>
                    <p class="product-card-price">€ {eur_fmt(sale)}</p>
                    <div class="product-card-foot">
                        <a href="{slug}.html" class="home-product-detail">{labels['detail']}</a>
                        <button type="button" class="btn-cta-primary product-card-add" data-cart-add>{labels['add']}</button>
                    </div>
                </div>
"""


def build_product_page(lang, prod):
    e = entry(prod["sku"])
    slug = prod["slug"]
    sku = prod["sku"]
    sale = e["unitAmountMinor"]
    compare = e["compareAtMinor"]
    disc = pct(sale, compare)
    labels = BASE_LABELS[lang]
    meta = TEMPLATE_META[prod["template"]]
    short = prod["card_name"]
    brand = prod.get("brand") or meta["brand"] or "Microsoft"
    cat_slug = meta["listing"]
    cat_name = meta["cat_label"][lang]
    eyebrow = meta["eyebrow"][lang]
    act_step = meta["activation"][lang]
    desc = f"{short}. {labels['desc_suffix']}"
    price_dec = f"{sale / 100:.2f}"
    og_image = prod["image"]

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Product",
                "@id": f"https://aml-store.com/{lang}/{slug}.html#product",
                "name": short,
                "sku": sku,
                "inLanguage": lang,
                "url": f"https://aml-store.com/{lang}/{slug}.html",
                "image": f"https://aml-store.com/asset/media/{og_image}",
                "description": desc,
                "brand": {"@type": "Brand", "name": brand},
                "offers": {
                    "@type": "Offer",
                    "url": f"https://aml-store.com/{lang}/{slug}.html",
                    "priceCurrency": "EUR",
                    "price": price_dec,
                    "availability": "https://schema.org/InStock",
                    "itemCondition": "https://schema.org/NewCondition",
                },
            }
        ],
    }

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{short} — Aml Store</title>
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://aml-store.com/{lang}/{slug}.html">
    <meta property="og:type" content="product">
    <meta property="og:site_name" content="Aml Store">
    <meta property="og:title" content="{short} — Aml Store">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="https://aml-store.com/{lang}/{slug}.html">
    <meta property="og:locale" content="{LOCALE[lang]}">
    <meta property="og:image" content="https://aml-store.com/asset/media/{og_image}">
    <meta property="product:price:amount" content="{price_dec}">
    <meta property="product:price:currency" content="EUR">
{hreflang_block(slug)}
    <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
    </script>
    <script src="../js/consent-init.js"></script>
    <link rel="icon" href="../favicon/favicon.png" type="image/png">
    <link rel="stylesheet" href="../fonts/montserrat.css">
    <link rel="stylesheet" href="../css/page.css">
    <link rel="stylesheet" href="../css/product.css">
    <link rel="stylesheet" href="../css/microsoft-365-product.css">
    <script src="../js/theme-init.js"></script>
</head>
<body>
    <a class="skip-link" href="#main">{labels['skip']}</a>
    <ecommerce-header translate="no" class="notranslate"></ecommerce-header>
    <div id="product-sticky-cta" class="product-sticky-cta" role="region" aria-label="{labels['sticky']}" aria-hidden="true">
        <div class="product-sticky-cta__inner">
            <span class="product-sticky-cta__title">{short}</span>
            <div class="product-sticky-cta__prices" aria-hidden="true">
                <span class="product-sticky-cta__msrp">€ {eur_fmt(compare)}</span>
                <span class="product-sticky-cta__sale">€ {eur_fmt(sale)}</span>
            </div>
            <button type="button" class="btn-primary" data-cart-add data-cart-source="sticky-cta">{labels['add']}</button>
        </div>
    </div>
    <section class="v2-hero" aria-label="Prodotto">
        <div class="v2-breadcrumb">
            <nav aria-label="Breadcrumb">
                <a href="/{lang}/">Home</a><span class="sep">/</span>
                <a href="/{lang}/{cat_slug}.html">{cat_name}</a><span class="sep">/</span>
                <span aria-current="page">{short}</span>
            </nav>
        </div>
        <div class="v2-hero__inner">
            <div class="v2-hero__left">
                <p class="v2-hero__eyebrow">{eyebrow}</p>
                <h1 class="v2-hero__title">{short}</h1>
                <p class="v2-hero__desc">{desc}</p>
            </div>
            <div class="v2-hero__right">
                <img class="v2-hero__cover" src="../asset/media/{og_image}" width="400" height="400" alt="" fetchpriority="high" decoding="async">
            </div>
        </div>
    </section>
    <div class="v2-pricing-wrap">
        <div id="product-pricing" class="v2-pricing-card"
            data-stripe-currency="eur"
            data-stripe-unit-amount="{sale}"
            data-stripe-compare-at-amount="{compare}"
            data-stripe-product-sku="{sku}"
            data-discount-percent="{disc}">
            <div class="v2-price-label">{labels['price_label']}</div>
            <div class="v2-price-row">
                <span class="v2-price-msrp">€ {eur_fmt(compare)}</span>
                <span class="v2-price-sale">€ {eur_fmt(sale)}</span>
                <span class="v2-price-badge">−{disc}%</span>
            </div>
            <div class="v2-price-tax">{labels['tax']}</div>
            <button type="button" class="v2-btn-primary" data-cart-add data-cart-source="product-pricing">{labels['add']}</button>
        </div>
    </div>
    <main id="main" class="product-page" data-cart-added-msg="{labels['add']}">
        <section class="product-process-steps" aria-labelledby="steps-title">
            <h2 id="steps-title">{labels['steps_title']}</h2>
            <ol class="product-process-steps__list">
                <li><strong>{labels['step_order']}</strong> — {labels['step_checkout']}</li>
                <li><strong>{labels['step_email']}</strong> — {labels['step_email_desc']}</li>
                <li><strong>{labels['step_act']}</strong> — {act_step}</li>
            </ol>
        </section>
    </main>
    <aml-cookie-banner></aml-cookie-banner>
    <ecommerce-footer translate="no" class="notranslate"></ecommerce-footer>
    <script src="../js/locale-path.js"></script>
    <script src="../js/cart.js" defer></script>
    <script src="../js/product-page.js" defer></script>
    <script src="../components/cookie-banner.js" defer></script>
    <script src="../components/header.js" defer></script>
    <script src="../components/footer.js" defer></script>
</body>
</html>
"""


def build_catalog_page(lang, catalog_slug, products):
    labels = BASE_LABELS[lang]
    title, lede = CATALOG_META[catalog_slug][lang]
    cards = "".join(product_card(lang, p, labels) for p in products)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Aml Store</title>
    <meta name="description" content="{lede}">
    <meta name="robots" content="index, follow">
    <script src="../js/consent-init.js"></script>
    <link rel="icon" href="../favicon/favicon.png" type="image/png">
    <link rel="apple-touch-icon" href="../favicon/apple-touch-icon.png">
    <link rel="canonical" href="https://aml-store.com/{lang}/{catalog_slug}.html">
{hreflang_block(catalog_slug)}
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title} | Aml Store">
    <meta property="og:description" content="{lede}">
    <meta property="og:url" content="https://aml-store.com/{lang}/{catalog_slug}.html">
    <meta property="og:locale" content="{LOCALE[lang]}">
    <meta property="og:image" content="https://aml-store.com/asset/media/microsoft-365-personal.webp">
    <link rel="stylesheet" href="../fonts/montserrat.css">
    <link rel="stylesheet" href="../css/page.css">
    <link rel="stylesheet" href="../css/home.css">
    <script src="../js/theme-init.js"></script>
    <script type="application/ld+json">
    {{"@context":"https://schema.org","@type":"CollectionPage","name":"{title}","description":"{lede}","url":"https://aml-store.com/{lang}/{catalog_slug}.html","inLanguage":"{lang}","isPartOf":{{"@type":"WebSite","name":"Aml Store","url":"https://aml-store.com/"}}}}
    </script>
</head>
<body>
    <div class="scroll-progress" aria-hidden="true"></div>
    <a class="skip-link" href="#main">{labels['skip']}</a>
    <ecommerce-header translate="no" class="notranslate"></ecommerce-header>
    <main id="main" class="home-page">
        <section class="home-catalog" aria-labelledby="catalog-title" style="padding-top: 120px;">
            <h1 id="catalog-title" class="home-section-title">{title}</h1>
            <p style="text-align: center; color: var(--text-muted); margin-bottom: 48px; font-size: 1.1rem; max-width: 640px; margin-left: auto; margin-right: auto;">
                {lede}
            </p>
            <div class="product-grid">
{cards}
            </div>
        </section>
    </main>
    <aml-cookie-banner></aml-cookie-banner>
    <ecommerce-footer translate="no" class="notranslate"></ecommerce-footer>
    <script src="../js/locale-path.js"></script>
    <script src="../js/cart.js" defer></script>
    <script src="../components/cookie-banner.js" defer></script>
    <script src="../components/header.js" defer></script>
    <script src="../components/footer.js" defer></script>
</body>
</html>
"""
