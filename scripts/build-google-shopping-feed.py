#!/usr/bin/env python3
"""Genera feeds/google-shopping-{lang}.xml per Google Merchant Center / campagne Shopping.

Un feed RSS 2.0 (namespace g:) per ogni lingua del sito. Ogni feed va
registrato in Merchant Center con il paese di destinazione della relativa
lingua (vedi COUNTRY_BY_LANG piu' sotto) — i prezzi sono in EUR per tutte
le lingue.

Fonte autoritativa: il blocco JSON-LD Product di ogni pagina prodotto
(gia' tradotto per lingua, gia' allineato al prezzo mostrato a video) —
stessa scelta di build-search-index.py. catalog.json viene usato solo
per arricchire con EAN/GTIN, MPN e categoria merceologica, con join sullo SKU.

Da rieseguire manualmente ogni volta che cambiano pagine prodotto o prezzi
(nessun hook/CI nel repo, stesso spirito manuale di bump-asset-version.py).

    python scripts/build-google-shopping-feed.py
    python scripts/build-google-shopping-feed.py --with-sale-price
    python scripts/build-google-shopping-feed.py --langs it en
"""
import argparse
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es", "pt", "nl")
OUT_DIR = ROOT / "feeds"
SITE_PREFIX = "https://eurolicenze.com"

# Paese Merchant Center consigliato per ogni feed lingua (tutti i prezzi in EUR).
# 'en' e' in EUR: si presta all'Irlanda; per UK servirebbe un listino in GBP
# che il sito non ha.
COUNTRY_BY_LANG = {
    "it": "IT", "en": "IE", "fr": "FR", "de": "DE",
    "es": "ES", "pt": "PT", "nl": "NL",
}

# Pagine non-prodotto — stesso set di build-search-index.py (difesa in piu':
# comunque si tengono solo le pagine con nodo Product + offer con prezzo).
SKIP_UTILITY = {
    "index", "cart", "checkout", "checkout-success", "account",
    "privacy-policy", "cookie-policy", "terms-and-conditions",
    "returns-and-refunds", "microsoft-365-solutions",
    "404", "chi-siamo", "about-us", "qui-sommes-nous", "ueber-uns",
    "quienes-somos", "sobre-nos", "over-ons",
    "consulenza", "consultation", "beratung", "consultoria",
    "consultatie", "contacts",
}
SKIP_CATEGORY = {
    "sistemi-operativi", "suite-office", "antivirus",
    "windows-server", "strumenti", "pacchetti",
}
# Pagine di confronto SEO (wave 1): editoriali, stesso slug in tutte le lingue.
SKIP_COMPARE = {
    "kaspersky-vs-eset-nod32", "microsoft-365-family-vs-personal",
    "norton-vs-bitdefender", "office-2024-vs-microsoft-365",
    "windows-11-home-vs-pro",
}
SKIP = SKIP_UTILITY | SKIP_CATEGORY | SKIP_COMPARE

JSONLD_RE = re.compile(
    r'<script type="application/ld\+json">\s*(.*?)\s*</script>', re.DOTALL
)

# category catalog.json -> Google product category (percorso testuale ufficiale)
GOOGLE_CATEGORY = {
    "antivirus": "Software > Computer Software > Antivirus & Security Software",
    "backup": "Software > Computer Software > Compression & Backup Software",
    "multimedia > photoediting":
        "Software > Computer Software > Multimedia & Design Software",
    "sistema operativo > windows":
        "Software > Computer Software > Operating Systems",
    "sistema operativo > windows > microsoft windows 11":
        "Software > Computer Software > Operating Systems",
    "sistema operativo > windows server":
        "Software > Computer Software > Operating Systems",
    "suite office":
        "Software > Computer Software > Business & Productivity Software",
    "suite office > microsoft 365":
        "Software > Computer Software > Business & Productivity Software",
    "suite office > microsoft office 2024":
        "Software > Computer Software > Business & Productivity Software",
    "suite office > microsoft project 2024":
        "Software > Computer Software > Business & Productivity Software",
    "tool ufficio":
        "Software > Computer Software > Business & Productivity Software",
}
GOOGLE_CATEGORY_DEFAULT = "Software > Computer Software"

# famiglie di varianti: slug senza il conteggio dispositivi/durata -> item_group_id
VARIANT_COUNT_RE = re.compile(r"-\d+-devices?(?:-\d+y)?$|-\d+y$")

AVAILABILITY_MAP = {
    "https://schema.org/InStock": "in_stock",
    "https://schema.org/OutOfStock": "out_of_stock",
    "https://schema.org/PreOrder": "preorder",
    "https://schema.org/BackOrder": "backorder",
}


def load_catalog_by_sku():
    data = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    by_sku = {}
    for p in data:
        sku = (p.get("sku") or "").strip()
        if sku:
            by_sku[sku] = p
    return by_sku


def find_node(graph, type_name):
    for node in graph:
        if node.get("@type") == type_name:
            return node
    return None


def price_to_minor(value):
    try:
        return int(round(float(value) * 100))
    except (TypeError, ValueError):
        return None


def money(minor):
    return f"{minor / 100:.2f} EUR"


def digits(value):
    return re.sub(r"\D", "", value or "")


def prefer_jpg(image_url):
    """Riscrive un URL .webp in .jpg se il gemello locale esiste.

    Google Merchant Center segnala talvolta "Codifica dell'immagine non
    valida" su .webp validi (problema noto del suo validatore, non file
    corrotti). I gemelli .jpg sono generati da
    scripts/convert-product-images-to-jpg.py; il sito continua a usare il
    .webp originale, solo il feed punta al .jpg.
    """
    if not image_url.endswith(".webp") or not image_url.startswith(SITE_PREFIX):
        return image_url
    rel_path = image_url[len(SITE_PREFIX):].lstrip("/")
    local_jpg = ROOT / Path(rel_path).with_suffix(".jpg")
    if local_jpg.exists():
        return image_url[: -len(".webp")] + ".jpg"
    return image_url


def slug_of(path):
    return path.stem


def item_group_id(slug):
    base = VARIANT_COUNT_RE.sub("", slug)
    return base if base != slug else None


def build_item(html_path, lang, catalog, with_sale_price):
    text = html_path.read_text(encoding="utf-8")
    m = JSONLD_RE.search(text)
    if not m:
        return None
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError as exc:
        print(f"  ! JSON-LD illeggibile in {html_path.name}: {exc}", file=sys.stderr)
        return None
    graph = data.get("@graph", [])
    product = find_node(graph, "Product")
    if not product:
        return None
    offers = product.get("offers") or {}
    unit_minor = price_to_minor(offers.get("price"))
    if unit_minor is None:
        return None

    sku = (product.get("sku") or "").strip()
    cat_entry = catalog.get(sku, {})
    slug = slug_of(html_path)

    fields = []
    fields.append(("g:id", sku or slug))
    fields.append(("title", (product.get("name") or "").strip()[:150]))
    fields.append(("description", (product.get("description") or "").strip()[:5000]))
    fields.append(("link", product.get("url") or f"{SITE_PREFIX}/{lang}/{slug}"))
    image = prefer_jpg(product.get("image") or "")
    if image:
        fields.append(("g:image_link", image))
    fields.append(("g:availability",
                   AVAILABILITY_MAP.get(offers.get("availability"), "in_stock")))

    compare_minor = cat_entry.get("compareAtMinor")
    if with_sale_price and compare_minor and compare_minor > unit_minor:
        fields.append(("g:price", money(compare_minor)))
        fields.append(("g:sale_price", money(unit_minor)))
    else:
        fields.append(("g:price", money(unit_minor)))

    fields.append(("g:condition", "new"))
    fields.append(("g:adult", "no"))

    brand = ((product.get("brand") or {}).get("name") or "").strip()
    if brand:
        fields.append(("g:brand", brand))

    gtin = digits(cat_entry.get("ean"))
    mpn = (product.get("mpn") or cat_entry.get("mpn") or "").strip()
    if gtin:
        fields.append(("g:gtin", gtin))
    if mpn:
        fields.append(("g:mpn", mpn))
    if not gtin and not mpn:
        fields.append(("g:identifier_exists", "no"))

    fields.append(("g:google_product_category",
                   GOOGLE_CATEGORY.get(cat_entry.get("category"),
                                       GOOGLE_CATEGORY_DEFAULT)))
    product_type = cat_entry.get("category")
    if product_type:
        fields.append(("g:product_type",
                       " > ".join(part.strip().title()
                                  for part in product_type.split(">"))))

    group = item_group_id(slug)
    if group:
        fields.append(("g:item_group_id", group))

    return fields


def render_feed(lang, items):
    country = COUNTRY_BY_LANG.get(lang, "")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">',
        "  <channel>",
        f"    <title>Eurolicenze - Google Shopping ({lang}"
        f"{' / ' + country if country else ''})</title>",
        f"    <link>{SITE_PREFIX}/{lang}/</link>",
        "    <description>Licenze software originali con consegna del codice "
        "via email.</description>",
    ]
    for fields in items:
        lines.append("    <item>")
        for tag, value in fields:
            lines.append(f"      <{tag}>{escape(str(value))}</{tag}>")
        lines.append("    </item>")
    lines.append("  </channel>")
    lines.append("</rss>")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--langs", nargs="+", choices=LANGS, default=list(LANGS))
    ap.add_argument("--with-sale-price", action="store_true",
                    help="usa compareAtMinor come g:price e il prezzo reale come "
                         "g:sale_price quando c'e' uno sconto")
    args = ap.parse_args()

    catalog = load_catalog_by_sku()
    OUT_DIR.mkdir(exist_ok=True)

    total = 0
    for lang in args.langs:
        lang_dir = ROOT / lang
        if not lang_dir.is_dir():
            print(f"! cartella lingua mancante: {lang}", file=sys.stderr)
            continue
        items = []
        for html_path in sorted(lang_dir.glob("*.html")):
            if slug_of(html_path) in SKIP:
                continue
            fields = build_item(html_path, lang, catalog, args.with_sale_price)
            if fields:
                items.append(fields)
        out_path = OUT_DIR / f"google-shopping-{lang}.xml"
        out_path.write_text(render_feed(lang, items), encoding="utf-8")
        total += len(items)
        rel = out_path.relative_to(ROOT).as_posix()
        print(f"  {rel}: {len(items)} prodotti")

    print(f"Fatto. {total} righe prodotto su {len(args.langs)} feed in {OUT_DIR.relative_to(ROOT).as_posix()}/")


if __name__ == "__main__":
    main()
