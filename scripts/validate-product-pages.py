#!/usr/bin/env python3
"""Pre-commit checks: product identifiers, prices, sitemap and catalog cards."""
import html as html_lib
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
    "contacts",
    "404", "chi-siamo", "about-us", "qui-sommes-nous", "ueber-uns", "quienes-somos",
    "consulenza", "consultation", "beratung", "consultoria",
    "suite-office", "sistemi-operativi", "pacchetti",
    "antivirus", "windows-server", "strumenti",
}
LANGS = ("it", "en", "fr", "de", "es")
INTERNAL_SKUS = {
    "SC_W11HOME_M365PERS",
    "SC_M365P_MTOTPROT_5Device",
    "SC_M365_KPremium_5Device",
    "SC835510",
    "W11_PRO_STICKER",
    "P73-07788_ESD",
}
JSON_LD_RE = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)
VISIBLE_CODE_RE = re.compile(
    r'<p\b[^>]*class=["\'][^"\']*\bv2-product-code\b[^"\']*["\'][^>]*>.*?'
    r'<code\b[^>]*class=["\'][^"\']*\bv2-product-code__value\b[^"\']*["\'][^>]*>'
    r'([^<]+)</code>.*?</p>',
    re.IGNORECASE | re.DOTALL,
)
errors = []


def product_json_ld(text, page):
    products = []
    for raw in JSON_LD_RE.findall(text):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{page}: invalid JSON-LD ({exc.msg})")
            continue
        nodes = data.get("@graph", []) if isinstance(data, dict) else []
        if isinstance(data, dict) and data.get("@type") == "Product":
            nodes = [data]
        for node in nodes:
            node_type = node.get("@type") if isinstance(node, dict) else None
            if node_type == "Product" or isinstance(node_type, list) and "Product" in node_type:
                products.append(node)
    if len(products) != 1:
        errors.append(f"{page}: expected 1 Product JSON-LD entity, found {len(products)}")
        return None
    return products[0]


def check_catalog_identifiers():
    for sku, item in CATALOG.items():
        mpn = item.get("mpn")
        is_microsoft = item["name"].startswith("Microsoft ")
        if sku in INTERNAL_SKUS and mpn:
            errors.append(f"catalog.json: internal SKU {sku} must not define mpn")
        if is_microsoft and sku not in INTERNAL_SKUS and mpn != sku:
            errors.append(f"catalog.json: Microsoft SKU {sku} must define matching mpn")
        if mpn and not is_microsoft:
            errors.append(f"catalog.json: non-Microsoft SKU {sku} must not define mpn")
        if mpn and mpn != sku:
            errors.append(f"catalog.json: mpn {mpn} != SKU {sku}")


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
                continue
            page = html.relative_to(ROOT)
            expected = CATALOG[sku]

            if 'class="v2-faq"' in text:
                errors.append(f"{page}: legacy FAQ markup is still present")
            if 'class="home-faq-list"' in text:
                faq_items = text.count('class="home-faq-item"')
                faq_bodies = text.count('class="home-faq-body"')
                if faq_items < 1 or faq_items != faq_bodies:
                    errors.append(
                        f"{page}: FAQ items/bodies mismatch ({faq_items}/{faq_bodies})"
                    )
                if '../js/faq.js' not in text:
                    errors.append(f"{page}: shared FAQ script is missing")

            visible_codes = [html_lib.unescape(code.strip()) for code in VISIBLE_CODE_RE.findall(text)]
            if visible_codes != [sku]:
                errors.append(f"{page}: visible product code {visible_codes or 'missing'} != {sku}")

            # Con il passaggio allo stile del concept il codice articolo e' salito
            # nella riga badge sopra il titolo (vedi .pdp-badges in
            # product_page_lib.py): l'ordine atteso e' badge+codice, H1, descrizione.
            badges_position = text.find('class="pdp-badges"')
            title_start = text.find("<h1")
            title_end = text.find("</h1>")
            code_position = text.find('class="v2-product-code"')
            desc_position = text.find('class="v2-hero__desc"')
            if not (0 <= badges_position < code_position < title_start):
                errors.append(f"{page}: product code must sit in the badge row above the H1")
            if not (0 <= title_end < desc_position):
                errors.append(f"{page}: description must follow the H1")

            product = product_json_ld(text, page)
            if product:
                if product.get("sku") != sku:
                    errors.append(f"{page}: JSON-LD sku {product.get('sku')!r} != {sku}")
                expected_mpn = expected.get("mpn")
                if expected_mpn and product.get("mpn") != expected_mpn:
                    errors.append(f"{page}: JSON-LD mpn {product.get('mpn')!r} != {expected_mpn}")
                if not expected_mpn and "mpn" in product:
                    errors.append(f"{page}: unexpected JSON-LD mpn {product.get('mpn')!r}")
                if expected["name"].startswith("Microsoft "):
                    brand = product.get("brand")
                    brand_name = brand.get("name") if isinstance(brand, dict) else brand
                    if brand_name != "Microsoft":
                        errors.append(f"{page}: Microsoft product has brand {brand_name!r}")
                for identifier in ("gtin", "gtin8", "gtin12", "gtin13", "gtin14"):
                    if identifier in product:
                        errors.append(f"{page}: unverified {identifier} must not be published")

            if amounts and sku in CATALOG:
                if int(amounts[0]) != expected["unitAmountMinor"]:
                    errors.append(
                        f"{page}: price {amounts[0]} != {expected['unitAmountMinor']}"
                    )
            if 'hreflang="it"' not in text and lang == "it":
                errors.append(f"{html.relative_to(ROOT)}: missing hreflang block")


def check_sitemap():
    text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", text)
    if len(locs) != len(set(locs)):
        errors.append("sitemap.xml: duplicate URLs")
    for lang in LANGS:
        for page in (ROOT / lang).glob("*.html"):
            if page.stem in SKIP:
                continue
            page_text = page.read_text(encoding="utf-8")
            canonical = re.search(
                r'<link\b[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']',
                page_text,
                re.IGNORECASE,
            )
            if not canonical:
                errors.append(f"{page.relative_to(ROOT)}: missing canonical URL")
                continue
            url = html_lib.unescape(canonical.group(1))
            if url not in locs:
                errors.append(f"sitemap missing canonical: {url}")


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
    check_catalog_identifiers()
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
