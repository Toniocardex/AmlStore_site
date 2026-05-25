#!/usr/bin/env python3
"""Pre-commit checks: SKU/price alignment, sitemap, catalog cards."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = {e["sku"]: e for e in json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))}
SKIP = {
    "index", "cart", "checkout", "checkout-success", "account",
    "privacy-policy", "cookie-policy", "terms-and-conditions",
    "returns-and-refunds", "microsoft-365-solutions",
}
LANGS = ("it", "en", "fr", "de", "es")
errors = []


def check_product_pages():
    for lang in LANGS:
        for html in (ROOT / lang).glob("*.html"):
            if html.stem in SKIP:
                continue
            text = html.read_text(encoding="utf-8")
            skus = re.findall(r'data-stripe-product-sku="([^"]+)"', text)
            amounts = re.findall(r'data-stripe-unit-amount="(\d+)"', text)
            if not skus:
                errors.append(f"{html.relative_to(ROOT)}: no data-stripe-product-sku")
                continue
            sku = skus[0]
            if sku not in CATALOG:
                errors.append(f"{html.relative_to(ROOT)}: unknown SKU {sku}")
            if amounts and sku in CATALOG:
                if int(amounts[0]) != CATALOG[sku]["unitAmountMinor"]:
                    errors.append(
                        f"{html.relative_to(ROOT)}: price {amounts[0]} != {CATALOG[sku]['unitAmountMinor']}"
                    )
            if 'hreflang="it"' not in text and lang == "it":
                errors.append(f"{html.relative_to(ROOT)}: missing hreflang block")


def check_sitemap():
    text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", text)
    if len(locs) != len(set(locs)):
        errors.append("sitemap.xml: duplicate URLs")
    for lang in LANGS:
        for html in (ROOT / lang).glob("*.html"):
            if html.stem in SKIP:
                continue
            url = f"https://aml-store.com/{lang}/{html.stem}.html"
            if url not in locs:
                errors.append(f"sitemap missing: {url}")


def check_catalog_cards():
    for catalog in ("suite-office", "sistemi-operativi", "pacchetti", "antivirus", "windows-server", "strumenti"):
        path = ROOT / "it" / f"{catalog}.html"
        if not path.exists():
            errors.append(f"missing catalog page: {path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        cards = len(re.findall(r'class="product-card"', text))
        if cards < 1:
            errors.append(f"{path.name}: no product cards")


def main():
    check_product_pages()
    check_sitemap()
    check_catalog_cards()
    if errors:
        print("VALIDATION FAILED:", len(errors), "issue(s)")
        for e in errors[:30]:
            print(" -", e)
        if len(errors) > 30:
            print(f" ... and {len(errors) - 30} more")
        sys.exit(1)
    print("OK: product pages, sitemap and catalog checks passed")


if __name__ == "__main__":
    main()
