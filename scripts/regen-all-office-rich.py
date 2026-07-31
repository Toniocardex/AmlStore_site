#!/usr/bin/env python3
"""Regenerate all Office-template rich product pages × 5 langs (+ M365 Business Standard)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_page_lib import LANGS, build_product_page, resolve_rich_content  # noqa: E402

# sku, slug, template, card_name, image fallback
DEFS = [
    ("EP2-06798", "office-2024-home", "office", "Office 2024 Home"),
    ("SC871349", "office-2024-standard", "office", "Office 2024 Standard"),
    ("EP2-06606", "office-2024-home-business", "office", "Office 2024 Home & Business"),
    ("79G-05412", "office-2021-home-student", "office", "Office 2021 Home & Student"),
    ("T5D-03485", "office-2021-home-business", "office", "Office 2021 Home & Business"),
    ("T5D-03489", "office-2021-home-business-mac", "office", "Office 2021 Home & Business Mac"),
    ("GMGF0D7FX-0002-P", "office-2021-professional-plus", "office", "Office 2021 Professional Plus"),
    ("79G-05018", "office-2019-home-student", "office", "Office 2019 Home & Student"),
    ("269-17068", "office-2019-professional-plus", "office", "Office 2019 Professional Plus"),
    ("EP2-07219", "word-2024", "office", "Word 2024"),
    ("065-09748", "excel-2024", "office", "Excel 2024"),
    ("065-09804", "powerpoint-2024", "office", "PowerPoint 2024"),
    ("5W1-04285", "outlook-2024", "office", "Outlook 2024"),
    ("DG7GMGF0PN44", "project-standard-2024", "office", "Project Standard 2024"),
    ("EP2-07001", "project-professional-2024", "office", "Project Professional 2024"),
    ("EP2-07167", "visio-standard-2024", "office", "Visio Standard 2024"),
    ("EP2-07110", "visio-professional-2024", "office", "Visio Professional 2024"),
    ("KLQ-00388", "microsoft-365-business-standard", "m365", "Microsoft 365 Business Standard"),
]

IMG = {
    "office": "microsoft-365-personal.webp",
    "m365": "microsoft-365-personal.webp",
}


def main():
    # Ensure every def has rich content (except we may add m365 later)
    missing = []
    for sku, slug, template, card_name in DEFS:
        content, _ = resolve_rich_content(slug)
        if not content and slug != "microsoft-365-business-standard":
            missing.append(slug)
    if missing:
        raise SystemExit(f"Missing rich content for: {missing}")

    for sku, slug, template, card_name in DEFS:
        content, _ = resolve_rich_content(slug)
        if not content:
            print("skip (no rich content yet)", slug)
            continue
        prod = {
            "sku": sku,
            "slug": slug,
            "template": template,
            "card_name": card_name,
            "image": IMG.get(template, "microsoft-365-personal.webp"),
        }
        for lang in LANGS:
            path = ROOT / lang / f"{slug}.html"
            html = build_product_page(lang, prod)
            if 'id="product-primary-cta"' not in html:
                raise SystemExit(f"CTA missing: {slug}/{lang}")
            if f'data-stripe-product-sku="{sku}"' not in html:
                raise SystemExit(f"SKU missing: {slug}/{lang}")
            path.write_text(html, encoding="utf-8")
        print("rich", slug, "×", len(LANGS))


if __name__ == "__main__":
    main()
