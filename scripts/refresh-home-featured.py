#!/usr/bin/env python3
"""Refresh homepage best sellers, Trustpilot, and recommended products ×5 langs."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from product_page_lib import BASE_LABELS, LANGS, entry, product_card  # noqa: E402

# TrustBox — Micro Review Count (widget ufficiale Trustpilot)
TRUSTPILOT_BUSINESS_UNIT_ID = "61c44c912f493a1a7cd810fa"
TRUSTPILOT_TEMPLATE_ID = "5419b6a8b0d04a076446a9ad"
TRUSTPILOT_TOKEN = "27270fde-f5a0-4937-9101-76b7ebae8a1a"

HOME_COPY = {
    "it": {
        "catalog_title": "I più venduti",
        "catalog_lede": "Le licenze più richieste, con prezzi chiari e consegna digitale immediata.",
        "hero_catalog_cta": "Esplora le soluzioni",
        "social_hidden": "Recensioni dei clienti",
        "social_fallback": (
            'Esperienze reali condivise dai clienti su '
            '<a href="https://it.trustpilot.com/review/aml-store.com" target="_blank" rel="noopener noreferrer">Trustpilot</a>.'
        ),
        "trustpilot_locale": "it-IT",
        "trustpilot_url": "https://it.trustpilot.com/review/aml-store.com",
    },
    "en": {
        "catalog_title": "Best sellers",
        "catalog_lede": "Our most popular licences with clear pricing and instant digital delivery.",
        "hero_catalog_cta": "Explore solutions",
        "social_hidden": "Customer reviews",
        "social_fallback": (
            'Real experiences shared by customers on '
            '<a href="https://www.trustpilot.com/review/aml-store.com" target="_blank" rel="noopener noreferrer">Trustpilot</a>.'
        ),
        "trustpilot_locale": "en-US",
        "trustpilot_url": "https://www.trustpilot.com/review/aml-store.com",
    },
    "fr": {
        "catalog_title": "Les plus vendus",
        "catalog_lede": "Les licences les plus demandées, prix clairs et livraison numérique immédiate.",
        "hero_catalog_cta": "Découvrir les solutions",
        "social_hidden": "Avis clients",
        "social_fallback": (
            'Expériences réelles partagées sur '
            '<a href="https://fr.trustpilot.com/review/aml-store.com" target="_blank" rel="noopener noreferrer">Trustpilot</a>.'
        ),
        "trustpilot_locale": "fr-FR",
        "trustpilot_url": "https://fr.trustpilot.com/review/aml-store.com",
    },
    "de": {
        "catalog_title": "Bestseller",
        "catalog_lede": "Beliebteste Lizenzen mit klaren Preisen und sofortiger digitaler Lieferung.",
        "hero_catalog_cta": "Lösungen entdecken",
        "social_hidden": "Kundenbewertungen",
        "social_fallback": (
            'Echte Erfahrungen von Kunden auf '
            '<a href="https://de.trustpilot.com/review/aml-store.com" target="_blank" rel="noopener noreferrer">Trustpilot</a>.'
        ),
        "trustpilot_locale": "de-DE",
        "trustpilot_url": "https://de.trustpilot.com/review/aml-store.com",
    },
    "es": {
        "catalog_title": "Los más vendidos",
        "catalog_lede": "Licencias más solicitadas, precios claros y entrega digital inmediata.",
        "hero_catalog_cta": "Explorar las soluciones",
        "social_hidden": "Opiniones de clientes",
        "social_fallback": (
            'Experiencias reales compartidas en '
            '<a href="https://es.trustpilot.com/review/aml-store.com" target="_blank" rel="noopener noreferrer">Trustpilot</a>.'
        ),
        "trustpilot_locale": "es-ES",
        "trustpilot_url": "https://es.trustpilot.com/review/aml-store.com",
    },
}

RECOMMENDED_COPY = {
    "it": {
        "title": "Prodotti consigliati",
        "lede": "Una selezione di soluzioni per produttività, lavoro e sicurezza.",
        "cta": "Esplora tutte le soluzioni →",
    },
    "en": {
        "title": "Recommended products",
        "lede": "A selection of solutions for productivity, work, and security.",
        "cta": "Explore all solutions →",
    },
    "fr": {
        "title": "Produits recommandés",
        "lede": "Une sélection de solutions pour la productivité, le travail et la sécurité.",
        "cta": "Découvrir toutes les solutions →",
    },
    "de": {
        "title": "Empfohlene Produkte",
        "lede": "Eine Auswahl an Lösungen für Produktivität, Arbeit und Sicherheit.",
        "cta": "Alle Lösungen entdecken →",
    },
    "es": {
        "title": "Productos recomendados",
        "lede": "Una selección de soluciones para productividad, trabajo y seguridad.",
        "cta": "Explorar todas las soluciones →",
    },
}

FEATURED = [
    {
        "sku": "EAVH-N1-A2",
        "slug": "eset-nod32-2-devices",
        "template": "antivirus",
        "image": "eset-nod32-2-devices.webp",
        "image_src": "../asset/media/products/eset-nod32-2-devices.webp?v=6b73ff4288",
        "card_name": {
            "it": "ESET NOD32 — 2 dispositivi",
            "en": "ESET NOD32 — 2 devices",
            "fr": "ESET NOD32 — 2 appareils",
            "de": "ESET NOD32 — 2 Geräte",
            "es": "ESET NOD32 — 2 dispositivos",
        },
        "blurb": {
            "it": "Abbonamento 12 mesi · 2 dispositivi · licenza digitale",
            "en": "12-month subscription · 2 devices · digital licence",
            "fr": "Abonnement 12 mois · 2 appareils · licence numérique",
            "de": "12-Monats-Abo · 2 Geräte · digitale Lizenz",
            "es": "Suscripción 12 meses · 2 dispositivos · licencia digital",
        },
    },
    {
        "sku": "KL1047TDAFS",
        "slug": "kaspersky-premium-1-device",
        "template": "antivirus",
        "image": "kaspersky-premium-1-device.webp",
        "image_src": "../asset/media/products/kaspersky-premium-1-device.webp?v=cd395b5601",
        "card_name": {
            "it": "Kaspersky Premium — 1 dispositivo",
            "en": "Kaspersky Premium — 1 device",
            "fr": "Kaspersky Premium — 1 appareil",
            "de": "Kaspersky Premium — 1 Gerät",
            "es": "Kaspersky Premium — 1 dispositivo",
        },
        "blurb": {
            "it": "Abbonamento 12 mesi · 1 dispositivo · licenza digitale",
            "en": "12-month subscription · 1 device · digital licence",
            "fr": "Abonnement 12 mois · 1 appareil · licence numérique",
            "de": "12-Monats-Abo · 1 Gerät · digitale Lizenz",
            "es": "Suscripción 12 meses · 1 dispositivo · licencia digital",
        },
    },
    {
        "sku": "6GQ-00092",
        "slug": "microsoft-365-family",
        "template": "m365",
        "image": "microsoft-365-family.webp",
        "image_src": "../asset/media/products/microsoft-365-family.webp?v=7503c711d3",
        "card_name": "Microsoft 365 Family",
        "blurb": {
            "it": "Abbonamento 12 mesi · fino a 6 utenti · licenza digitale",
            "en": "12-month subscription · up to 6 users · digital licence",
            "fr": "Abonnement 12 mois · jusqu'à 6 utilisateurs · licence numérique",
            "de": "12-Monats-Abo · bis zu 6 Nutzer · digitale Lizenz",
            "es": "Suscripción 12 meses · hasta 6 usuarios · licencia digital",
        },
    },
    {
        "sku": "QQ2-00012",
        "slug": "microsoft-365-personal",
        "template": "m365",
        "image": "microsoft-365-personal.webp",
        "image_src": "../asset/media/products/microsoft-365-personal.webp?v=2cfdb89700",
        "card_name": "Microsoft 365 Personal",
        "blurb": {
            "it": "Abbonamento 12 mesi · 1 utente · licenza digitale",
            "en": "12-month subscription · 1 user · digital licence",
            "fr": "Abonnement 12 mois · 1 utilisateur · licence numérique",
            "de": "12-Monats-Abo · 1 Nutzer · digitale Lizenz",
            "es": "Suscripción 12 meses · 1 usuario · licencia digital",
        },
    },
    {
        "sku": "SC_W11HOME_M365PERS",
        "slug": "bundle-windows-11-home-m365-personal",
        "template": "bundle",
        "image": "microsoft-windows-11-home.webp",
        "image_src": "../asset/media/products/bundle-windows-11-home-m365-personal.webp?v=a94f67147b",
        "card_name": {
            "it": "Windows 11 Home + M365 Personal",
            "en": "Windows 11 Home + M365 Personal",
            "fr": "Windows 11 Home + M365 Personal",
            "de": "Windows 11 Home + M365 Personal",
            "es": "Windows 11 Home + M365 Personal",
        },
        "blurb": {
            "it": "Pacchetto · Windows a vita + Office 12 mesi · 5 dispositivi",
            "en": "Bundle · lifetime Windows + 12-month Office · 5 devices",
            "fr": "Pack · Windows à vie + Office 12 mois · 5 appareils",
            "de": "Paket · Windows dauerhaft + Office 12 Monate · 5 Geräte",
            "es": "Pack · Windows de por vida + Office 12 meses · 5 dispositivos",
        },
    },
    {
        "sku": "EP2-06798",
        "slug": "office-2024-home",
        "template": "office",
        "image": "microsoft-365-personal.webp",
        "image_src": "../asset/media/products/office-2024-home.webp?v=a93041b6f5",
        "card_name": "Office 2024 Home",
        "blurb": {
            "it": "Licenza perpetua · Word, Excel, PowerPoint · PC/Mac",
            "en": "Perpetual licence · Word, Excel, PowerPoint · PC/Mac",
            "fr": "Licence perpétuelle · Word, Excel, PowerPoint · PC/Mac",
            "de": "Dauerlizenz · Word, Excel, PowerPoint · PC/Mac",
            "es": "Licencia perpetua · Word, Excel, PowerPoint · PC/Mac",
        },
        "lazy": True,
    },
]

RECOMMENDED = [
    {
        "sku": "KASP_PLUS_1D_1A",
        "slug": "kaspersky-plus",
        "template": "antivirus",
        "image": "kaspersky-plus.webp",
        "card_name": "Kaspersky Plus",
        "blurb": {
            "it": "Abbonamento 12 mesi · 1 dispositivo · licenza digitale",
            "en": "12-month subscription · 1 device · digital licence",
            "fr": "Abonnement 12 mois · 1 appareil · licence numérique",
            "de": "12-Monats-Abo · 1 Gerät · digitale Lizenz",
            "es": "Suscripción 12 meses · 1 dispositivo · licencia digital",
        },
        "lazy": True,
        "fetchpriority": "low",
    },
    {
        "sku": "NORT_360DEL_3D_1A",
        "slug": "norton-360-deluxe",
        "template": "antivirus",
        "image": "norton-360-deluxe.webp",
        "card_name": "Norton 360 Deluxe",
        "blurb": {
            "it": "Abbonamento 12 mesi · 3 dispositivi · licenza digitale",
            "en": "12-month subscription · 3 devices · digital licence",
            "fr": "Abonnement 12 mois · 3 appareils · licence numérique",
            "de": "12-Monats-Abo · 3 Geräte · digitale Lizenz",
            "es": "Suscripción 12 meses · 3 dispositivos · licencia digital",
        },
        "lazy": True,
        "fetchpriority": "low",
    },
    {
        "sku": "1108923",
        "slug": "mcafee-total-protection-5-devices",
        "template": "antivirus",
        "image": "mcafee-total-protection-5-devices.webp",
        "card_name": {
            "it": "McAfee Total Protection — 5 dispositivi",
            "en": "McAfee Total Protection — 5 devices",
            "fr": "McAfee Total Protection — 5 appareils",
            "de": "McAfee Total Protection — 5 Geräte",
            "es": "McAfee Total Protection — 5 dispositivos",
        },
        "blurb": {
            "it": "Abbonamento 12 mesi · 5 dispositivi · licenza digitale",
            "en": "12-month subscription · 5 devices · digital licence",
            "fr": "Abonnement 12 mois · 5 appareils · licence numérique",
            "de": "12-Monats-Abo · 5 Geräte · digitale Lizenz",
            "es": "Suscripción 12 meses · 5 dispositivos · licencia digital",
        },
        "lazy": True,
        "fetchpriority": "low",
    },
    {
        "sku": "EP2-06606",
        "slug": "office-2024-home-business",
        "template": "office",
        "image": "office-2024-home-business.webp",
        "card_name": "Office 2024 Home & Business",
        "blurb": {
            "it": "Licenza perpetua · Word, Excel, PowerPoint, Outlook · PC/Mac",
            "en": "Perpetual licence · Word, Excel, PowerPoint, Outlook · PC/Mac",
            "fr": "Licence perpétuelle · Word, Excel, PowerPoint, Outlook · PC/Mac",
            "de": "Dauerlizenz · Word, Excel, PowerPoint, Outlook · PC/Mac",
            "es": "Licencia perpetua · Word, Excel, PowerPoint, Outlook · PC/Mac",
        },
        "lazy": True,
        "fetchpriority": "low",
    },
]

RECOMMENDED_PRODUCTS = tuple(p["slug"] for p in RECOMMENDED)

HOME_TRUST_RE = re.compile(
    r"\n\s*<section class=\"home-trust\"[^>]*>.*?</section>\s*",
    re.DOTALL,
)

CATALOG_SECTION_RE = re.compile(
    r"<section id=\"piu-venduti\"[^>]*>.*?</section>",
    re.DOTALL,
)

HERO_CATALOG_CTA_RE = re.compile(
    r'(<a class="home-btn home-btn-ghost" href="#soluzioni">)[^<]+(</a>)',
)

PAYMENTS_STRIP_RE = re.compile(
    r"\n\s*<section class=\"home-payments-strip\"[^>]*>.*?</section>\s*",
    re.DOTALL,
)

SOCIAL_PROOF_RE = re.compile(
    r"\n\s*<section class=\"home-social-proof\"[^>]*>.*?</section>\s*",
    re.DOTALL,
)

CLOSING_RE = re.compile(
    r"\n?\s*<section class=\"home-closing\"[^>]*>.*?</section>\s*",
    re.DOTALL,
)

RECOMMENDED_SECTION_RE = re.compile(
    r"\n?\s*<section id=\"prodotti-consigliati\"[^>]*>.*?</section>\s*",
    re.DOTALL,
)


def validate_merchandising():
    featured_slugs = {p["slug"] for p in FEATURED}
    featured_skus = {p["sku"] for p in FEATURED}
    rec_slugs = {p["slug"] for p in RECOMMENDED}
    rec_skus = {p["sku"] for p in RECOMMENDED}

    if len(RECOMMENDED) != 4:
        raise SystemExit(f"RECOMMENDED must have exactly 4 products, got {len(RECOMMENDED)}")
    if tuple(p["slug"] for p in RECOMMENDED) != RECOMMENDED_PRODUCTS:
        raise SystemExit("RECOMMENDED_PRODUCTS tuple out of sync with RECOMMENDED list")

    overlap_slugs = featured_slugs & rec_slugs
    overlap_skus = featured_skus & rec_skus
    if overlap_slugs or overlap_skus:
        raise SystemExit(
            f"Recommended products overlap bestsellers: slugs={overlap_slugs} skus={overlap_skus}"
        )

    for p in FEATURED + RECOMMENDED:
        try:
            entry(p["sku"])
        except KeyError as exc:
            raise SystemExit(f"SKU not found in catalog.json: {p['sku']} ({p['slug']})") from exc
        page = ROOT / "it" / f"{p['slug']}.html"
        if not page.is_file():
            raise SystemExit(f"Product page missing: {page.relative_to(ROOT)}")


def featured_prod(lang, base):
    prod = dict(base)
    prod["href_suffix"] = ""
    name = prod.get("card_name")
    if isinstance(name, dict):
        prod["card_name"] = name[lang]
    prod["blurb"] = prod["blurb"][lang]
    return prod


def social_proof_section(lang):
    # ATTENZIONE: il TrustBox qui sotto e' morto — dal 2026-08-30 il widget non
    # e' piu' nel piano gratuito Trustpilot e l'iframe resta in caricamento a
    # vuoto. Oggi e' innocuo perche' la home non ha piu' <section
    # class="home-social-proof">, quindi SOCIAL_PROOF_RE non trova nulla e
    # questa funzione non viene mai applicata. Se la sezione viene riattivata,
    # sostituire il widget col link statico al voto: vedi
    # _trustpilot_buy_mini() in product_page_lib.py.
    copy = HOME_COPY[lang]
    return f"""
        <section class="home-social-proof" aria-labelledby="home-social-title">
            <h2 id="home-social-title" class="visually-hidden">{copy['social_hidden']}</h2>
            <p class="home-social-proof__fallback">{copy['social_fallback']}</p>
            <div
                id="trustpilot-widget"
                class="trustpilot-widget"
                data-locale="{copy['trustpilot_locale']}"
                data-template-id="{TRUSTPILOT_TEMPLATE_ID}"
                data-businessunit-id="{TRUSTPILOT_BUSINESS_UNIT_ID}"
                data-style-height="40px"
                data-style-width="100%"
                data-token="{TRUSTPILOT_TOKEN}"
                data-min-review-count="0"
                data-style-alignment="center"
            >
                <a href="{copy['trustpilot_url']}" target="_blank" rel="noopener noreferrer">Trustpilot</a>
            </div>
        </section>
"""


def recommended_section(lang):
    copy = RECOMMENDED_COPY[lang]
    labels = BASE_LABELS[lang]
    cards = "".join(
        product_card(lang, featured_prod(lang, p), labels, clean_price=True) for p in RECOMMENDED
    )
    return f"""
        <section id="prodotti-consigliati" class="home-recommended" aria-labelledby="prodotti-consigliati-title">
            <div class="home-recommended__inner">
                <header class="home-recommended__intro">
                    <h2 id="prodotti-consigliati-title" class="home-section-title">{copy['title']}</h2>
                    <p class="home-catalog-lede">{copy['lede']}</p>
                </header>
                <div class="product-grid home-recommended__grid">
{cards}                </div>
                <a class="home-catalog-more" href="#soluzioni">{copy['cta']}</a>
            </div>
        </section>
"""


def patch_index(lang):
    path = ROOT / lang / "index.html"
    text = path.read_text(encoding="utf-8")
    copy = HOME_COPY[lang]
    labels = BASE_LABELS[lang]

    text = HOME_TRUST_RE.sub("\n", text)
    text = PAYMENTS_STRIP_RE.sub("\n", text)

    cards = "".join(
        product_card(lang, featured_prod(lang, p), labels, clean_price=False) for p in FEATURED
    )

    if not CATALOG_SECTION_RE.search(text):
        raise RuntimeError(f"catalog section not found in {path}")
    catalog_section = f"""<section id="piu-venduti" class="home-catalog" aria-labelledby="catalog-title">
            <h2 id="catalog-title" class="home-section-title">{copy['catalog_title']}</h2>
            <div class="home-catalog-intro">
                <p class="home-catalog-lede">{copy['catalog_lede']}</p>
            </div>
            <div class="product-grid">
{cards}            </div>
        </section>"""
    text = CATALOG_SECTION_RE.sub(catalog_section, text, count=1)

    if HERO_CATALOG_CTA_RE.search(text):
        text = HERO_CATALOG_CTA_RE.sub(
            rf"\g<1>{copy['hero_catalog_cta']}\g<2>",
            text,
            count=1,
        )

    # Drop legacy closing CTA and any previous recommended block (idempotent).
    # NOTA: la sezione "Prodotti consigliati" e' temporaneamente disattivata in
    # home (vedi apply-security-first-phase2.py). recommended_section() resta
    # disponibile per il ripristino, ma qui non viene piu' reinserita.
    text = CLOSING_RE.sub("\n", text)
    text = RECOMMENDED_SECTION_RE.sub("\n", text)

    social = social_proof_section(lang)
    if SOCIAL_PROOF_RE.search(text):
        text = SOCIAL_PROOF_RE.sub(social, text, count=1)

    path.write_text(text, encoding="utf-8")
    print("updated", path.relative_to(ROOT))


def main():
    validate_merchandising()
    for lang in LANGS:
        patch_index(lang)


if __name__ == "__main__":
    main()
