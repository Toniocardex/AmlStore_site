#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia sulle 5 schede wave-2, sul catalogo suite-office, sitemap e
_redirects (5 slug x 5 lingue = 25 schede + 5 cataloghi).

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Fino a settembre 2026 main() chiamava build_page() e build_suite_office() e
sovrascriveva 25 schede piu' le 5 copie del catalogo suite-office, poi
appendeva a sitemap.xml e _redirects. Era sfuggito ai giri di disarmo
precedenti perche' non chiama build_product_page() ne' build_catalog_page(): ha
i suoi builder, piu' vecchi.

Eseguirlo oggi distruggerebbe circa il 90% di ogni pagina:

  - schede:       generato 6,4-6,8 KB,  pubblicato 57,7-90,8 KB, 25 diff su 25
  - suite-office: generato 11,8-11,9 KB, pubblicato 68,6-69,1 KB, 5 diff su 5

Tutti e quattro i marcatori di PIPELINE_MARKERS sono presenti nel pubblicato e
assenti nel generato, su tutte e 30 le pagine. Il perche', e i cinque strati
che andrebbero persi, stanno in scripts/page_pipeline_guard.py.

Non finirebbe li'. Questo script scrive URL con estensione .html, mentre
sitemap.xml e _redirects sono passati alle forme senza estensione: nessuno dei
25 URL .html e' oggi in sitemap.xml, quindi append_sitemap() ne aggiungerebbe
25 duplicati, e append_redirects() aggiungerebbe 5 regole .html gia' coperte
piu' la regola /it/office-suite, che oggi non c'e' -- probabilmente rimossa
apposta, come la /it/antivirus di generate-wave3.py che faceva loop con gli URL
puliti di Pages.

Attenzione: wave-2 e' anteriore a pt/ e nl/ e copre solo 5 lingue. Le stesse
schede sono controllate su tutte e 7 dal main() di scripts/generate-wave3.py, e
suite-office anche da scripts/regen-catalogs-only.py, che pero' non sapeva di
poter essere scavalcato da qui. Resta proprio di questo script la copertura di
sitemap e _redirects per il registro wave-2: wave3 esclude suite-office apposta
dalla sua verifica sitemap.

build_page() e build_suite_office() sono conservati solo per rimisurare il
disallineamento in memoria, come descritto in page_pipeline_guard.py. Non hanno
piu' chiamanti che scrivono.

Quel che lo script fa ancora, e per cui va tenuto: verifica che le 25 schede e
le 5 copie di suite-office esistano con i quattro strati addosso, e che
sitemap.xml e _redirects coprano il registro -- cioe' quello che
append_sitemap() e append_redirects() garantivano scrivendo. Senza effetti
collaterali, non scrive nulla.

    python scripts/generate-wave2.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from page_pipeline_guard import fail_if, load, pipeline_errors  # noqa: E402
from product_page_lib import product_card  # noqa: E402
CATALOG = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
LANGS = ("it", "en", "fr", "de", "es")
LOCALE = {"it": "it_IT", "en": "en_US", "fr": "fr_FR", "de": "de_DE", "es": "es_ES"}

WAVE2 = [
    {
        "slug": "microsoft-365-business-standard",
        "sku": "KLQ-00388",
        "template": "m365",
        "image": "microsoft-365-personal.webp",
        "card_name": "Microsoft 365 Business Standard",
        "woo_it": "/it/office-suite/microsoft-365-business-standard-1-utente-15-dispositivi",
    },
    {
        "slug": "office-2024-home",
        "sku": "EP2-06798",
        "template": "office",
        "image": "microsoft-365-personal.webp",
        "card_name": "Office 2024 Home",
        "woo_it": "/it/office-suite/microsoft-office-home-2024-pc-o-mac",
    },
    {
        "slug": "office-2021-home-student",
        "sku": "79G-05412",
        "template": "office",
        "image": "microsoft-365-personal.webp",
        "card_name": "Office 2021 Home & Student",
        "woo_it": "/it/office-suite/microsoft-office-2021-home-student-windows-o-mac",
    },
    {
        "slug": "office-2021-professional-plus",
        "sku": "GMGF0D7FX-0002-P",
        "template": "office",
        "image": "microsoft-365-personal.webp",
        "card_name": "Office 2021 Professional Plus",
        "woo_it": "/it/office-suite/microsoft-office-2021-professional-plus",
    },
    {
        "slug": "office-2019-professional-plus",
        "sku": "269-17068",
        "template": "office",
        "image": "microsoft-365-personal.webp",
        "card_name": "Office 2019 Professional Plus",
        "woo_it": "/it/office-suite/microsoft-office-2019-professional-plus",
    },
]

LABELS = {
    "it": {
        "skip": "Vai al contenuto principale",
        "add": "Aggiungi al carrello",
        "detail": "Vedi prodotto",
        "price_label": "Il nostro prezzo",
        "tax": "Tasse incluse. Nessun costo di spedizione.",
        "office_cat": "Suite Office",
        "office_eyebrow": "Licenza perpetua",
        "m365_eyebrow": "Abbonamento Microsoft 365",
        "sticky": "Acquisto rapido",
        "steps_title": "Consegna e attivazione",
        "step_order": "Ordine",
        "step_checkout": "Checkout sicuro",
        "step_email": "Email",
        "step_email_desc": "Codice e istruzioni in 2–15 minuti",
        "step_act": "Attivazione",
        "step_act_office": "Portale setup.office.com",
        "step_act_m365": "Account Microsoft ufficiale",
        "desc_suffix": "Licenza digitale originale, consegna via email in 2–15 minuti.",
        "suite_title": "Suite Office",
        "suite_lede": "Office perpetuo e piani Microsoft 365: licenze digitali originali con attivazione ufficiale Microsoft.",
    },
    "en": {
        "skip": "Skip to main content",
        "add": "Add to cart",
        "detail": "View product",
        "price_label": "Our price",
        "tax": "Tax included. No shipping fees.",
        "office_cat": "Office suite",
        "office_eyebrow": "Perpetual licence",
        "m365_eyebrow": "Microsoft 365 subscription",
        "sticky": "Quick purchase",
        "steps_title": "Delivery and activation",
        "step_order": "Order",
        "step_checkout": "Secure checkout",
        "step_email": "Email",
        "step_email_desc": "Code and instructions within 2–15 minutes",
        "step_act": "Activation",
        "step_act_office": "Official setup.office.com portal",
        "step_act_m365": "Official Microsoft account",
        "desc_suffix": "Genuine digital licence, email delivery within 2–15 minutes.",
        "suite_title": "Office suite",
        "suite_lede": "Perpetual Office and Microsoft 365 plans: genuine digital licences with official Microsoft activation.",
    },
    "fr": {
        "skip": "Aller au contenu principal",
        "add": "Ajouter au panier",
        "detail": "Voir le produit",
        "price_label": "Notre prix",
        "tax": "Taxes incluses. Pas de frais de port.",
        "office_cat": "Suite Office",
        "office_eyebrow": "Licence perpétuelle",
        "m365_eyebrow": "Abonnement Microsoft 365",
        "sticky": "Achat rapide",
        "steps_title": "Livraison et activation",
        "step_order": "Commande",
        "step_checkout": "Paiement sécurisé",
        "step_email": "E-mail",
        "step_email_desc": "Code et instructions en 2–15 minutes",
        "step_act": "Activation",
        "step_act_office": "Portail officiel setup.office.com",
        "step_act_m365": "Compte Microsoft officiel",
        "desc_suffix": "Licence numérique originale, livraison par e-mail en 2–15 minutes.",
        "suite_title": "Suite Office",
        "suite_lede": "Office perpétuel et Microsoft 365 : licences numériques officielles avec activation Microsoft.",
    },
    "de": {
        "skip": "Zum Hauptinhalt springen",
        "add": "In den Warenkorb",
        "detail": "Produkt ansehen",
        "price_label": "Unser Preis",
        "tax": "Steuern inklusive. Keine Versandkosten.",
        "office_cat": "Office-Suite",
        "office_eyebrow": "Dauerlizenz",
        "m365_eyebrow": "Microsoft-365-Abonnement",
        "sticky": "Schnellkauf",
        "steps_title": "Lieferung und Aktivierung",
        "step_order": "Bestellung",
        "step_checkout": "Sicherer Checkout",
        "step_email": "E-Mail",
        "step_email_desc": "Code und Anleitung in 2–15 Minuten",
        "step_act": "Aktivierung",
        "step_act_office": "Offizielles setup.office.com-Portal",
        "step_act_m365": "Offizielles Microsoft-Konto",
        "desc_suffix": "Originale digitale Lizenz, Lieferung per E-Mail in 2–15 Minuten.",
        "suite_title": "Office-Suite",
        "suite_lede": "Office-Dauerlizenzen und Microsoft-365-Pläne: originale digitale Lizenzen mit offizieller Microsoft-Aktivierung.",
    },
    "es": {
        "skip": "Ir al contenido principal",
        "add": "Añadir al carrito",
        "detail": "Ver producto",
        "price_label": "Nuestro precio",
        "tax": "Impuestos incluidos. Sin gastos de envío.",
        "office_cat": "Suite Office",
        "office_eyebrow": "Licencia perpetua",
        "m365_eyebrow": "Suscripción Microsoft 365",
        "sticky": "Compra rápida",
        "steps_title": "Entrega y activación",
        "step_order": "Pedido",
        "step_checkout": "Checkout seguro",
        "step_email": "Email",
        "step_email_desc": "Código e instrucciones en minutos",
        "step_act": "Activación",
        "step_act_office": "Portal oficial setup.office.com",
        "step_act_m365": "Cuenta Microsoft oficial",
        "desc_suffix": "Licencia digital original, entrega por email en minutos.",
        "suite_title": "Suite Office",
        "suite_lede": "Office perpetuo y Microsoft 365: licencias digitales originales con activación oficial Microsoft.",
    },
}

CARD_BLURBS = {
    "microsoft-365-business-standard": {
        "it": "1 utente · 15 dispositivi · abbonamento",
        "en": "1 user · 15 devices · subscription",
        "fr": "1 utilisateur · 15 appareils · abonnement",
        "de": "1 Nutzer · 15 Geräte · Abonnement",
        "es": "1 usuario · 15 dispositivos · suscripción",
    },
    "default_office": {
        "it": "Licenza ESD · Attivazione setup.office.com",
        "en": "ESD licence · setup.office.com activation",
        "fr": "Licence ESD · activation setup.office.com",
        "de": "ESD-Lizenz · Aktivierung setup.office.com",
        "es": "Licencia ESD · activación setup.office.com",
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
            f'    <link rel="alternate" hreflang="{lg}" href="https://eurolicenze.com/{lg}/{slug}">'
        )
    lines.append(
        f'    <link rel="alternate" hreflang="x-default" href="https://eurolicenze.com/it/{slug}">'
    )
    return "\n".join(lines)


def card_blurb(lang, prod):
    slug = prod["slug"]
    if slug in CARD_BLURBS:
        return CARD_BLURBS[slug][lang]
    return CARD_BLURBS["default_office"][lang]


def build_page(lang, prod):
    e = entry(prod["sku"])
    slug = prod["slug"]
    sku = prod["sku"]
    sale = e["unitAmountMinor"]
    compare = e["compareAtMinor"]
    disc = pct(sale, compare)
    labels = LABELS[lang]
    is_m365 = prod["template"] == "m365"
    short = prod["card_name"]
    eyebrow = labels["m365_eyebrow"] if is_m365 else labels["office_eyebrow"]
    act_step = labels["step_act_m365"] if is_m365 else labels["step_act_office"]
    desc = f"{short}. {labels['desc_suffix']}"
    price_dec = f"{sale / 100:.2f}"
    compare_dec = f"{compare / 100:.2f}"

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Product",
                "@id": f"https://eurolicenze.com/{lang}/{slug}#product",
                "name": short,
                "sku": sku,
                "inLanguage": lang,
                "url": f"https://eurolicenze.com/{lang}/{slug}",
                "image": f"https://eurolicenze.com/asset/media/{prod['image']}",
                "description": desc,
                "brand": {"@type": "Brand", "name": "Microsoft"},
                "offers": {
                    "@type": "Offer",
                    "url": f"https://eurolicenze.com/{lang}/{slug}",
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
    <title>{short} — Eurolicenze</title>
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://eurolicenze.com/{lang}/{slug}">
    <meta property="og:type" content="product">
    <meta property="og:site_name" content="Eurolicenze">
    <meta property="og:title" content="{short} — Eurolicenze">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="https://eurolicenze.com/{lang}/{slug}">
    <meta property="og:locale" content="{LOCALE[lang]}">
    <meta property="og:image" content="https://eurolicenze.com/asset/media/{prod['image']}">
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
    <link rel="stylesheet" href="../css/product-pdp.css">
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
                <a href="/{lang}/suite-office.html">{labels['office_cat']}</a><span class="sep">/</span>
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
                <img class="v2-hero__cover" src="../asset/media/{prod['image']}" width="400" height="400" alt="" fetchpriority="high" decoding="async">
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


def build_suite_office(lang):
    labels = LABELS[lang]
    cards = "".join(
        product_card(lang, {**p, "blurb": card_blurb(lang, p)}, labels) for p in WAVE2
    )
    meta_desc = labels["suite_lede"]
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{labels['suite_title']} | Eurolicenze</title>
    <meta name="description" content="{meta_desc}">
    <meta name="robots" content="index, follow">
    <script src="../js/consent-init.js"></script>
    <link rel="icon" href="../favicon/favicon.png" type="image/png">
    <link rel="apple-touch-icon" href="../favicon/apple-touch-icon.png">
    <link rel="canonical" href="https://eurolicenze.com/{lang}/suite-office.html">
{hreflang_block("suite-office")}
    <meta property="og:type" content="website">
    <meta property="og:title" content="{labels['suite_title']} | Eurolicenze">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:url" content="https://eurolicenze.com/{lang}/suite-office.html">
    <meta property="og:locale" content="{LOCALE[lang]}">
    <meta property="og:image" content="https://eurolicenze.com/asset/media/microsoft-365-personal.webp">
    <link rel="stylesheet" href="../fonts/montserrat.css">
    <link rel="stylesheet" href="../css/page.css">
    <link rel="stylesheet" href="../css/home.css">
    <script src="../js/theme-init.js"></script>
    <script type="application/ld+json">
    {{"@context":"https://schema.org","@type":"CollectionPage","name":"{labels['suite_title']}","description":"{meta_desc}","url":"https://eurolicenze.com/{lang}/suite-office.html","inLanguage":"{lang}","isPartOf":{{"@type":"WebSite","name":"Eurolicenze","url":"https://eurolicenze.com/"}}}}
    </script>
</head>
<body>
    <div class="scroll-progress" aria-hidden="true"></div>
    <a class="skip-link" href="#main">{labels['skip']}</a>
    <ecommerce-header translate="no" class="notranslate"></ecommerce-header>
    <main id="main" class="home-page">
        <section class="home-catalog" aria-labelledby="catalog-title" style="padding-top: 120px;">
            <h1 id="catalog-title" class="home-section-title">{labels['suite_title']}</h1>
            <p style="text-align: center; color: var(--text-muted); margin-bottom: 48px; font-size: 1.1rem; max-width: 640px; margin-left: auto; margin-right: auto;">
                {labels['suite_lede']}
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


def check_sitemap():
    """Le 25 schede e suite-office devono essere in sitemap.xml, senza estensione."""
    text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    slugs = ["suite-office"] + [p["slug"] for p in WAVE2]
    return [
        f"sitemap.xml: manca {lang}/{slug}"
        for lang in LANGS
        for slug in slugs
        if f"https://eurolicenze.com/{lang}/{slug}" not in text
    ]


def check_redirects():
    """Ogni slug con woo_it deve avere la sua regola, con o senza estensione."""
    text = (ROOT / "_redirects").read_text(encoding="utf-8")
    errors = []
    for p in WAVE2:
        woo = p.get("woo_it")
        if not woo:
            continue
        if f"{woo} /it/{p['slug']} 301" not in text and f"{woo} /it/{p['slug']}.html 301" not in text:
            errors.append(f"_redirects: manca la regola per {woo}")
    return errors


def main():
    errors = []
    for lang in LANGS:
        html = load(lang, "suite-office")
        if html is None:
            errors.append(f"{lang}/suite-office.html: manca il catalogo")
        else:
            errors += pipeline_errors(lang, "suite-office", html)
        for p in WAVE2:
            page = load(lang, p["slug"])
            if page is None:
                errors.append(f"{lang}/{p['slug']}.html: manca il file")
                continue
            errors += pipeline_errors(lang, p["slug"], page)

    errors += check_sitemap()
    errors += check_redirects()

    fail_if(errors, f"OK: {len(WAVE2)} schede wave-2 + catalogo suite-office "
                    f"x {len(LANGS)} lingue, sitemap e _redirects allineati")


if __name__ == "__main__":
    main()
