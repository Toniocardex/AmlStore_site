#!/usr/bin/env python3
"""Regenerate Office 2024 / 2019 rich product pages (5 SKUs × 5 langs)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_content_office import PRODUCTS as OFFICE_CONTENT  # noqa: E402
from product_page_lib import LANGS, build_product_page  # noqa: E402

# slug → (sku, card_name, image)
OFFICE_DEFS = {
    "office-2024-home": ("EP2-06798", "Office 2024 Home", "microsoft-365-personal.webp"),
    "office-2024-standard": ("SC871349", "Office 2024 Standard", "microsoft-365-personal.webp"),
    "office-2024-home-business": ("EP2-06606", "Office 2024 Home & Business", "microsoft-365-personal.webp"),
    "office-2019-home-student": ("79G-05018", "Office 2019 Home & Student", "microsoft-365-personal.webp"),
    "office-2019-professional-plus": ("269-17068", "Office 2019 Professional Plus", "microsoft-365-personal.webp"),
}


def main():
    missing = [s for s in OFFICE_CONTENT if s not in OFFICE_DEFS]
    if missing:
        raise SystemExit(f"Missing defs for: {missing}")

    for slug, (sku, card_name, image) in OFFICE_DEFS.items():
        prod = {
            "sku": sku,
            "slug": slug,
            "template": "office",
            "card_name": card_name,
            "image": image,
        }
        for lang in LANGS:
            path = ROOT / lang / f"{slug}.html"
            path.write_text(build_product_page(lang, prod), encoding="utf-8")
        print("rich", slug)


if __name__ == "__main__":
    main()
