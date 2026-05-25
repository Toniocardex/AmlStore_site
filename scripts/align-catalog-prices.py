#!/usr/bin/env python3
"""Align HTML data-stripe-* and visible prices with catalog SKUs (CSV source)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es")

REPLACEMENTS = [
    # Personal: SKU + price
    ("data-stripe-product-sku=\"microsoft-365-personal-12m\"", 'data-stripe-product-sku="QQ2-00012"'),
    ('data-stripe-product-sku="microsoft-365-personal-12m"', 'data-stripe-product-sku="QQ2-00012"'),
    ("data-stripe-unit-amount=\"7400\"", 'data-stripe-unit-amount="7900"'),
    ('data-stripe-unit-amount="7400"', 'data-stripe-unit-amount="7900"'),
    ('"price": "74.00"', '"price": "79.00"'),
    ('content="74.00"', 'content="79.00"'),
    ("data-discount-percent=\"25\"", 'data-discount-percent="20"'),
    ('data-discount-percent="25"', 'data-discount-percent="20"'),
    # Family
    ("data-stripe-product-sku=\"microsoft-365-family-12m\"", 'data-stripe-product-sku="6GQ-00092"'),
    ('data-stripe-product-sku="microsoft-365-family-12m"', 'data-stripe-product-sku="6GQ-00092"'),
    ("data-stripe-unit-amount=\"9900\"", 'data-stripe-unit-amount="10495"'),
    ('data-stripe-unit-amount="9900"', 'data-stripe-unit-amount="10495"'),
    ('"price": "99.00"', '"price": "104.95"'),
    ('content="99.00"', 'content="104.95"'),
    ("data-discount-percent=\"23\"", 'data-discount-percent="19"'),
    ('data-discount-percent="23"', 'data-discount-percent="19"'),
]

# Locale-specific visible prices (IT/EN/FR/DE/ES patterns)
PRICE_VISIBLE = [
    ("€ 74,00", "€ 79,00"),
    ("€74,00", "€79,00"),
    ("€ 99,00", "€ 104,95"),  # only on family pages - careful on index mixed
]

def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if "microsoft-365-family" in path.name:
        text = text.replace("€ 99,00", "€ 104,95").replace("99 euro", "104,95 euro")
        text = text.replace("Prezzo scontato 99 euro", "Prezzo scontato 104,95 euro")
        text = text.replace("−23%", "−19%")
    if "microsoft-365-personal" in path.name or (
        "index.html" in path.name and "product-card" in text
    ):
        pass  # personal handled below per file type
    if "microsoft-365-personal" in path.name:
        text = text.replace("€ 74,00", "€ 79,00").replace("74 euro", "79 euro")
        text = text.replace("Prezzo scontato 74 euro", "Prezzo scontato 79 euro")
        text = text.replace("−25%", "−20%")
    if path.name == "index.html":
        # index has both products - targeted replace via stripe amounts already done
        text = text.replace(
            'data-stripe-unit-amount="9900"\n                data-stripe-compare-at-amount="12900"\n                data-stripe-product-sku="6GQ-00092"',
            'data-stripe-unit-amount="10495"\n                data-stripe-compare-at-amount="12900"\n                data-stripe-product-sku="6GQ-00092"',
        )
        text = text.replace(
            '<p class="product-card-price">€ 99,00</p>',
            '<p class="product-card-price">€ 104,95</p>',
            1,
        )
        text = text.replace(
            '<p class="product-card-price">€ 74,00</p>',
            '<p class="product-card-price">€ 79,00</p>',
            1,
        )
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    changed = []
    for lang in LANGS:
        d = ROOT / lang
        for html in d.glob("*.html"):
            if patch_file(html):
                changed.append(str(html.relative_to(ROOT)))
    print("Updated", len(changed), "files")
    for c in changed:
        print(" ", c)


if __name__ == "__main__":
    main()
