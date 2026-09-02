#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia sulle 6 schede wave-1, sul catalogo sistemi-operativi, sitemap e
_redirects (6 slug x 5 lingue = 30 file).

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Fino a settembre 2026 main() chiamava build_page() e sovrascriveva le 30
schede, poi rifaceva le card del catalogo sistemi-operativi e appendeva a
sitemap.xml e _redirects. Era sfuggito ai giri di disarmo precedenti perche'
non chiama build_product_page(): ha un build_page() suo, piu' vecchio.

Eseguirlo oggi e' il caso peggiore di tutti. build_page() rende 6,6-6,9 KB
contro pagine pubblicate di 54,0-69,3 KB: 30 diff su 30 e un delta di
47,3-62,4 KB, cioe' circa il 90% di ogni pagina. Tutti e quattro i marcatori di
PIPELINE_MARKERS sono presenti nel pubblicato e assenti nel generato, su tutte
e 30. Il perche', e i cinque strati che andrebbero persi, stanno in
scripts/page_pipeline_guard.py.

Non finirebbe li'. Questo script scrive URL con estensione .html, mentre
sitemap.xml e _redirects sono passati alle forme senza estensione: nessuno dei
30 URL .html e' oggi in sitemap.xml, quindi append_sitemap() ne aggiungerebbe
30 duplicati, e append_redirects() aggiungerebbe 6 regole .html gia' coperte
dalle equivalenti senza estensione.

Attenzione: wave-1 e' anteriore a pt/ e nl/ e copre solo 5 lingue. Le stesse
schede sono controllate su tutte e 7 dal main() di scripts/generate-wave3.py,
che le ha nel suo registro. Resta proprio di questo script il catalogo
sistemi-operativi, che nessun altro sorveglia: wave3 lo esclude apposta dalla
sua verifica sitemap.

build_page() e' conservato solo per rimisurare il disallineamento in memoria,
come descritto in page_pipeline_guard.py. Non ha piu' chiamanti che scrivono.

Quel che lo script fa ancora, e per cui va tenuto: verifica che le 30 schede
esistano con i quattro strati addosso, che il catalogo sistemi-operativi mostri
le card dei 3 slug Windows invece dello skeleton, e che sitemap.xml e
_redirects coprano il registro -- cioe' quello che patch_sistemi_operativi(),
append_sitemap() e append_redirects() garantivano scrivendo. Senza effetti
collaterali, non scrive nulla.

    python scripts/generate-wave1.py
"""
import json
import math
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

WAVE1 = [
    {
        "slug": "windows-11-pro",
        "sku": "FQC-10528",
        "template": "windows",
        "image": "microsoft-windows-11-home.webp",
        "woo_it": "/it/sistema-operativo/microsoft-windows-11-professional-licenza-esd-originale",
    },
    {
        "slug": "windows-10-home",
        "sku": "KW9-00136",
        "template": "windows",
        "image": "microsoft-windows-11-home.webp",
        "woo_it": "/it/sistema-operativo/microsoft-windows-10-home",
    },
    {
        "slug": "windows-10-pro",
        "sku": "FQC-08930",
        "template": "windows",
        "image": "microsoft-windows-11-home.webp",
        "woo_it": "/it/sistema-operativo/microsoft-windows-10-professional",
    },
    {
        "slug": "bundle-windows-11-home-m365-personal",
        "sku": "SC_W11HOME_M365PERS",
        "template": "bundle",
        "image": "microsoft-windows-11-home.webp",
        "woo_it": "/it/sistema-operativo/microsoft-windows-11-home-microsoft-365-personal-5-dispositivi-1-anno",
    },
    {
        "slug": "bundle-m365-personal-mcafee",
        "sku": "SC_M365P_MTOTPROT_5Device",
        "template": "bundle",
        "image": "microsoft-365-personal.webp",
        "woo_it": "/it/office-suite/microsoft-office-365-personal-mcafee-total-protection-5-dispositivi-1-anno",
    },
    {
        "slug": "bundle-m365-personal-kaspersky",
        "sku": "SC_M365_KPremium_5Device",
        "template": "bundle",
        "image": "microsoft-365-personal.webp",
        "woo_it": "/it/office-suite/microsoft-office-365-personal-kaspersky-premium-5-dispositivi-1-anno",
    },
]

LABELS = {
    "it": {
        "skip": "Vai al contenuto principale",
        "add": "Aggiungi al carrello",
        "detail": "Vedi prodotto",
        "price_label": "Il nostro prezzo",
        "tax": "Tasse incluse. Nessun costo di spedizione.",
        "os_cat": "Sistemi Operativi",
        "office_cat": "Office",
        "bundle_eyebrow": "Pacchetto digitale",
        "os_eyebrow": "Sistema operativo",
        "sticky": "Acquisto rapido",
    },
    "en": {
        "skip": "Skip to main content",
        "add": "Add to cart",
        "detail": "View product",
        "price_label": "Our price",
        "tax": "Tax included. No shipping fees.",
        "os_cat": "Operating systems",
        "office_cat": "Office",
        "bundle_eyebrow": "Digital bundle",
        "os_eyebrow": "Operating system",
        "sticky": "Quick purchase",
    },
    "fr": {
        "skip": "Aller au contenu principal",
        "add": "Ajouter au panier",
        "detail": "Voir le produit",
        "price_label": "Notre prix",
        "tax": "Taxes incluses. Pas de frais de port.",
        "os_cat": "Systèmes d'exploitation",
        "office_cat": "Office",
        "bundle_eyebrow": "Pack numérique",
        "os_eyebrow": "Système d'exploitation",
        "sticky": "Achat rapide",
    },
    "de": {
        "skip": "Zum Hauptinhalt springen",
        "add": "In den Warenkorb",
        "detail": "Produkt ansehen",
        "price_label": "Unser Preis",
        "tax": "Steuern inklusive. Keine Versandkosten.",
        "os_cat": "Betriebssysteme",
        "office_cat": "Office",
        "bundle_eyebrow": "Digitales Paket",
        "os_eyebrow": "Betriebssystem",
        "sticky": "Schnellkauf",
    },
    "es": {
        "skip": "Ir al contenido principal",
        "add": "Añadir al carrito",
        "detail": "Ver producto",
        "price_label": "Nuestro precio",
        "tax": "Impuestos incluidos. Sin gastos de envío.",
        "os_cat": "Sistemas operativos",
        "office_cat": "Office",
        "bundle_eyebrow": "Pack digital",
        "os_eyebrow": "Sistema operativo",
        "sticky": "Compra rápida",
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


def hreflang_block(lang, slug):
    lines = []
    for lg in LANGS:
        lines.append(
            f'    <link rel="alternate" hreflang="{lg}" href="https://eurolicenze.com/{lg}/{slug}">'
        )
    lines.append(
        f'    <link rel="alternate" hreflang="x-default" href="https://eurolicenze.com/it/{slug}">'
    )
    return "\n".join(lines)


def build_page(lang, prod):
    e = entry(prod["sku"])
    slug = prod["slug"]
    sku = prod["sku"]
    sale = e["unitAmountMinor"]
    compare = e["compareAtMinor"]
    disc = pct(sale, compare)
    labels = LABELS[lang]
    is_bundle = prod["template"] == "bundle"
    short = e["name"].split("|")[0].strip()
    if len(short) > 48:
        short = short[:45] + "…"
    cat_link = "microsoft-365-solutions.html" if is_bundle else "sistemi-operativi.html"
    cat_name = labels["office_cat"] if is_bundle else labels["os_cat"]
    eyebrow = labels["bundle_eyebrow"] if is_bundle else labels["os_eyebrow"]
    price_dec = f"{sale / 100:.2f}"
    compare_dec = f"{compare / 100:.2f}"
    desc = (
        f"{short}. Licenza digitale originale, consegna via email in 2–15 minuti."
        if lang == "it"
        else f"{short}. Genuine digital licence, email delivery within 2–15 minutes."
    )

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
{hreflang_block(lang, slug)}
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
                <a href="/{lang}/{cat_link}">{cat_name}</a><span class="sep">/</span>
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
            <h2 id="steps-title">{'Consegna e attivazione' if lang == 'it' else 'Delivery and activation'}</h2>
            <ol class="product-process-steps__list">
                <li><strong>{'Ordine' if lang == 'it' else 'Order'}</strong> — {'Checkout sicuro' if lang == 'it' else 'Secure checkout'}</li>
                <li><strong>{'Email' if lang == 'it' else 'Email'}</strong> — {'Codice e istruzioni in 2–15 minuti' if lang == 'it' else 'Code and instructions within 2–15 minutes'}</li>
                <li><strong>{'Attivazione' if lang == 'it' else 'Activation'}</strong> — {'Portale ufficiale Microsoft' if lang == 'it' else 'Official Microsoft portal'}</li>
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


def check_sistemi_operativi():
    """Le card dei 3 slug Windows devono essere sul catalogo, non lo skeleton.

    patch_sistemi_operativi() le scriveva sostituendo il blocco skeleton: se lo
    skeleton tornasse, il catalogo mostrerebbe segnaposto al posto dei prodotti.
    """
    errors = []
    os_slugs = [p["slug"] for p in WAVE1 if p["template"] == "windows"]
    for lang in LANGS:
        html = load(lang, "sistemi-operativi")
        if html is None:
            errors.append(f"{lang}/sistemi-operativi.html: manca il catalogo")
            continue
        for slug in os_slugs:
            if slug not in html:
                errors.append(f"{lang}/sistemi-operativi.html: manca la card {slug}")
        if "skeleton-img" in html:
            errors.append(f"{lang}/sistemi-operativi.html: skeleton non sostituito dalle card")
        errors += pipeline_errors(lang, "sistemi-operativi", html)
    return errors


def check_sitemap():
    """Le 30 schede devono essere in sitemap.xml, nella forma senza estensione."""
    text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    return [
        f"sitemap.xml: manca {lang}/{p['slug']}"
        for lang in LANGS
        for p in WAVE1
        if f"<loc>https://eurolicenze.com/{lang}/{p['slug']}</loc>" not in text
    ]


def check_redirects():
    """Ogni slug con woo_it deve avere la sua regola, con o senza estensione."""
    text = (ROOT / "_redirects").read_text(encoding="utf-8")
    errors = []
    for p in WAVE1:
        woo = p.get("woo_it")
        if not woo:
            continue
        if f"{woo} /it/{p['slug']} 301" not in text and f"{woo} /it/{p['slug']}.html 301" not in text:
            errors.append(f"_redirects: manca la regola per {woo}")
    return errors


def main():
    errors = []
    for lang in LANGS:
        for p in WAVE1:
            html = load(lang, p["slug"])
            if html is None:
                errors.append(f"{lang}/{p['slug']}.html: manca il file")
                continue
            errors += pipeline_errors(lang, p["slug"], html)

    errors += check_sistemi_operativi()
    errors += check_sitemap()
    errors += check_redirects()

    fail_if(errors, f"OK: {len(WAVE1)} schede wave-1 x {len(LANGS)} lingue, "
                    "catalogo sistemi-operativi, sitemap e _redirects allineati")


if __name__ == "__main__":
    main()
