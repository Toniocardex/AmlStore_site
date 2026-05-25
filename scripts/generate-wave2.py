#!/usr/bin/env python3
"""Generate wave-2 product pages (Office perpetual + M365 Business), suite-office catalog, sitemap, redirects."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
        "slug": "office-2024-standard",
        "sku": "SC871349",
        "template": "office",
        "image": "microsoft-365-personal.webp",
        "card_name": "Office 2024 Standard",
        "woo_it": "/it/office-suite/microsoft-office-2024-standard",
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
        "step_email_desc": "Codice e istruzioni in pochi minuti",
        "step_act": "Attivazione",
        "step_act_office": "Portale setup.office.com",
        "step_act_m365": "Account Microsoft ufficiale",
        "desc_suffix": "Licenza digitale originale, consegna via email in pochi minuti.",
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
        "step_email_desc": "Code and instructions within minutes",
        "step_act": "Activation",
        "step_act_office": "Official setup.office.com portal",
        "step_act_m365": "Official Microsoft account",
        "desc_suffix": "Genuine digital licence, email delivery within minutes.",
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
        "step_email_desc": "Code et instructions en quelques minutes",
        "step_act": "Activation",
        "step_act_office": "Portail officiel setup.office.com",
        "step_act_m365": "Compte Microsoft officiel",
        "desc_suffix": "Licence numérique originale, livraison par e-mail en quelques minutes.",
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
        "step_email_desc": "Code und Anleitung in wenigen Minuten",
        "step_act": "Aktivierung",
        "step_act_office": "Offizielles setup.office.com-Portal",
        "step_act_m365": "Offizielles Microsoft-Konto",
        "desc_suffix": "Originale digitale Lizenz, Lieferung per E-Mail in wenigen Minuten.",
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
            f'    <link rel="alternate" hreflang="{lg}" href="https://aml-store.com/{lg}/{slug}.html">'
        )
    lines.append(
        f'    <link rel="alternate" hreflang="x-default" href="https://aml-store.com/it/{slug}.html">'
    )
    return "\n".join(lines)


def card_blurb(lang, prod):
    slug = prod["slug"]
    if slug in CARD_BLURBS:
        return CARD_BLURBS[slug][lang]
    return CARD_BLURBS["default_office"][lang]


def product_card(lang, prod, labels):
    e = entry(prod["sku"])
    sale = e["unitAmountMinor"]
    compare = e["compareAtMinor"]
    disc = pct(sale, compare)
    name = prod["card_name"]
    blurb = card_blurb(lang, prod)
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
    cards = "".join(product_card(lang, p, labels) for p in WAVE2)
    meta_desc = labels["suite_lede"]
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{labels['suite_title']} | Aml Store</title>
    <meta name="description" content="{meta_desc}">
    <meta name="robots" content="index, follow">
    <script src="../js/consent-init.js"></script>
    <link rel="icon" href="../favicon/favicon.png" type="image/png">
    <link rel="apple-touch-icon" href="../favicon/apple-touch-icon.png">
    <link rel="canonical" href="https://aml-store.com/{lang}/suite-office.html">
{hreflang_block("suite-office")}
    <meta property="og:type" content="website">
    <meta property="og:title" content="{labels['suite_title']} | Aml Store">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:url" content="https://aml-store.com/{lang}/suite-office.html">
    <meta property="og:locale" content="{LOCALE[lang]}">
    <meta property="og:image" content="https://aml-store.com/asset/media/microsoft-365-personal.webp">
    <link rel="stylesheet" href="../fonts/montserrat.css">
    <link rel="stylesheet" href="../css/page.css">
    <link rel="stylesheet" href="../css/home.css">
    <script src="../js/theme-init.js"></script>
    <script type="application/ld+json">
    {{"@context":"https://schema.org","@type":"CollectionPage","name":"{labels['suite_title']}","description":"{meta_desc}","url":"https://aml-store.com/{lang}/suite-office.html","inLanguage":"{lang}","isPartOf":{{"@type":"WebSite","name":"Aml Store","url":"https://aml-store.com/"}}}}
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


def append_sitemap():
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    inserts = []
    slugs = ["suite-office"] + [p["slug"] for p in WAVE2]
    for lang in LANGS:
        for slug in slugs:
            url = f"https://aml-store.com/{lang}/{slug}.html"
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
    added = 0
    for p in WAVE2:
        woo = p.get("woo_it")
        if not woo:
            continue
        rule = f"{woo} /it/{p['slug']}.html 301"
        if rule not in existing:
            lines.append(rule)
            existing.add(rule)
            added += 1
    suite_rule = "/it/office-suite /it/suite-office.html 301"
    if suite_rule not in existing:
        lines.append(suite_rule)
        added += 1
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("redirects +", added)


def main():
    for lang in LANGS:
        suite_path = ROOT / lang / "suite-office.html"
        suite_path.write_text(build_suite_office(lang), encoding="utf-8")
        print("catalog", suite_path.relative_to(ROOT))
        for p in WAVE2:
            out = ROOT / lang / f"{p['slug']}.html"
            out.write_text(build_page(lang, p), encoding="utf-8")
            print("page", out.relative_to(ROOT))
    append_sitemap()
    append_redirects()


if __name__ == "__main__":
    main()
