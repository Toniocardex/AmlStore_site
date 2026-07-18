#!/usr/bin/env python3
"""Genera asset/search-index/{lang}.json per la ricerca prodotti nell'header.

Da rieseguire manualmente ogni volta che si aggiungono/modificano pagine
prodotto (nessun hook/CI nel repo, stesso spirito manuale di
bump-asset-version.py — vedi promemoria in GO-LIVE.md).

Estrae name/sku/image/prezzo/categoria dal blocco JSON-LD di ogni pagina
prodotto (fonte autoritativa, gia' richiesta per SEO/schema.org, tradotta
per lingua) — NON usa catalog.json, i cui nomi sono spesso disallineati
dai titoli reali delle pagine.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es")

# Pagine utility (nessun prodotto) — stesso set di validate-product-pages.py
SKIP_UTILITY = {
    "index", "cart", "checkout", "checkout-success", "account",
    "privacy-policy", "cookie-policy", "terms-and-conditions",
    "returns-and-refunds", "microsoft-365-solutions",
}
# Pagine categoria/listino (elencano prodotti, non sono un prodotto)
SKIP_CATEGORY = {
    "sistemi-operativi", "suite-office", "antivirus",
    "windows-server", "strumenti", "pacchetti",
}
SKIP = SKIP_UTILITY | SKIP_CATEGORY

JSONLD_RE = re.compile(
    r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
    re.DOTALL,
)

SITE_PREFIX = "https://aml-store.com"


def find_node(graph, type_name):
    for node in graph:
        if node.get("@type") == type_name:
            return node
    return None


def extract_category(graph):
    breadcrumb = find_node(graph, "BreadcrumbList")
    if not breadcrumb:
        return None
    for item in breadcrumb.get("itemListElement", []):
        if item.get("position") == 2:
            return item.get("name")
    return None


def relative_image(url):
    if not url:
        return ""
    if url.startswith(SITE_PREFIX):
        return url[len(SITE_PREFIX):]
    return url


def extract_entry(html_path):
    text = html_path.read_text(encoding="utf-8")
    m = JSONLD_RE.search(text)
    if not m:
        raise ValueError(f"nessun blocco JSON-LD trovato in {html_path}")
    data = json.loads(m.group(1))
    graph = data.get("@graph", [])
    product = find_node(graph, "Product")
    if not product:
        raise ValueError(f"nessun nodo Product nel JSON-LD di {html_path}")
    offers = product.get("offers") or {}
    price = offers.get("price")
    if price is None:
        raise ValueError(f"offers.price mancante in {html_path}")
    category = extract_category(graph)
    if not category:
        raise ValueError(f"categoria (BreadcrumbList position 2) mancante in {html_path}")

    return {
        "slug": html_path.stem,
        "name": product.get("name") or html_path.stem,
        "category": category,
        "priceMinor": round(float(price) * 100),
        "currency": offers.get("priceCurrency") or "EUR",
        "image": relative_image(product.get("image")),
    }


def main():
    errors = []
    out_dir = ROOT / "asset" / "search-index"
    out_dir.mkdir(parents=True, exist_ok=True)

    for lang in LANGS:
        entries = []
        for html_path in sorted((ROOT / lang).glob("*.html")):
            if html_path.stem in SKIP:
                continue
            try:
                entries.append(extract_entry(html_path))
            except ValueError as e:
                errors.append(str(e))

        out_path = out_dir / f"{lang}.json"
        out_path.write_text(
            json.dumps(entries, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
            newline="\n",
        )
        print(f"{lang}: {len(entries)} prodotti -> {out_path.relative_to(ROOT)}")

    if errors:
        print(f"\nERRORI: {len(errors)}")
        for e in errors[:30]:
            print(" -", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
