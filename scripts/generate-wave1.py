#!/usr/bin/env python3
"""Generate wave-1 product pages, catalog cards, sitemap entries, redirects."""
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
            f'    <link rel="alternate" hreflang="{lg}" href="https://aml-store.com/{lg}/{slug}.html">'
        )
    lines.append(
        f'    <link rel="alternate" hreflang="x-default" href="https://aml-store.com/it/{slug}.html">'
    )
    return "\n".join(lines)


def product_card(lang, slug, sku, short_name, blurb, labels):
    e = entry(sku)
    sale = e["unitAmountMinor"]
    compare = e["compareAtMinor"]
    disc = pct(sale, compare)
    return f"""                <div
                    class="product-card"
                    data-stripe-currency="eur"
                    data-stripe-unit-amount="{sale}"
                    data-stripe-compare-at-amount="{compare}"
                    data-stripe-product-sku="{sku}"
                    data-discount-percent="{disc}"
                >
                    <a href="{slug}.html" class="product-card-body product-card--link">
                        <div class="product-card-media">
                            <img src="../asset/media/microsoft-windows-11-home.webp" width="400" height="400" alt="{short_name}" decoding="async" class="product-card-img" onerror="this.src='../asset/media/home-hero-lifestyle.webp'">
                        </div>
                        <p class="product-card-name">{short_name}</p>
                        <p class="product-card-blurb">{blurb}</p>
                    </a>
                    <p class="product-card-price">€ {eur_fmt(sale)}</p>
                    <div class="product-card-foot">
                        <a href="{slug}.html" class="home-product-detail">{labels['detail']}</a>
                        <button type="button" class="btn-cta-primary product-card-add" data-cart-add>{labels['add']}</button>
                    </div>
                </div>
"""


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
        f"{short}. Licenza digitale originale, consegna via email in pochi minuti."
        if lang == "it"
        else f"{short}. Genuine digital licence, email delivery within minutes."
    )

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
                "image": f"https://aml-store.com/asset/media/{prod['image']}",
                "description": desc,
                "brand": {"@type": "Brand", "name": "Microsoft"},
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
    <meta property="og:image" content="https://aml-store.com/asset/media/{prod['image']}">
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
                <li><strong>{'Email' if lang == 'it' else 'Email'}</strong> — {'Codice e istruzioni in pochi minuti' if lang == 'it' else 'Code and instructions within minutes'}</li>
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


def patch_sistemi_operativi():
    os_products = [p for p in WAVE1 if p["template"] == "windows"]
    for lang in LANGS:
        path = ROOT / lang / "sistemi-operativi.html"
        text = path.read_text(encoding="utf-8")
        labels = LABELS[lang]
        cards = []
        for p in os_products:
            e = entry(p["sku"])
            short = p["slug"].replace("-", " ").title().replace("Windows 11 Pro", "Windows 11 Pro").replace("Windows 10 Home", "Windows 10 Home")
            if p["slug"] == "windows-11-pro":
                short = "Windows 11 Pro"
            elif p["slug"] == "windows-10-home":
                short = "Windows 10 Home"
            elif p["slug"] == "windows-10-pro":
                short = "Windows 10 Pro"
            blurb = "ESD · " + ("Attivazione immediata" if lang == "it" else "Instant activation")
            cards.append(product_card(lang, p["slug"], p["sku"], short, blurb, labels))
        skeleton = re.search(
            r"\n                <div class=\"product-card\">\n                    <div class=\"skeleton-img\">.*?</div>\n                </div>\n                <div class=\"product-card\">.*?</div>\n            </div>",
            text,
            re.S,
        )
        if skeleton:
            replacement = "\n" + "\n".join(cards) + "\n            </div>"
            text = text[: skeleton.start()] + replacement + text[skeleton.end() :]
            path.write_text(text, encoding="utf-8")
            print("patched", path)


def append_sitemap():
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    inserts = []
    for lang in LANGS:
        for p in WAVE1:
            url = f"https://aml-store.com/{lang}/{p['slug']}.html"
            if url in text:
                continue
            inserts.append(
                f'  <url><loc>{url}</loc><changefreq>weekly</changefreq><priority>0.85</priority></url>'
            )
    if inserts:
        text = text.replace("</urlset>", "\n".join(inserts) + "\n</urlset>")
        path.write_text(text, encoding="utf-8")
        print("sitemap +", len(inserts))


def append_redirects():
    path = ROOT / "_redirects"
    lines = path.read_text(encoding="utf-8").rstrip().splitlines()
    existing = set(lines)
    for p in WAVE1:
        if "woo_it" not in p:
            continue
        rule = f"{p['woo_it']} /it/{p['slug']}.html 301"
        if rule not in existing:
            lines.append(rule)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("redirects updated")


def main():
    for lang in LANGS:
        for p in WAVE1:
            out = ROOT / lang / f"{p['slug']}.html"
            out.write_text(build_page(lang, p), encoding="utf-8")
            print("page", out.relative_to(ROOT))
    patch_sistemi_operativi()
    append_sitemap()
    append_redirects()


if __name__ == "__main__":
    main()
