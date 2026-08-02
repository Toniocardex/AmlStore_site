#!/usr/bin/env python3
"""Regenerate Office 2021 + Windows rich pages (all 5 langs). Skips windows-11-home (preserved)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_page_lib import LANGS, build_product_page  # noqa: E402

DEFS = [
    # Office 2021
    ("79G-05412", "office-2021-home-student", "office", "Office 2021 Home & Student"),
    ("T5D-03485", "office-2021-home-business", "office", "Office 2021 Home & Business"),
    ("T5D-03489", "office-2021-home-business-mac", "office", "Office 2021 Home & Business Mac"),
    ("GMGF0D7FX-0002-P", "office-2021-professional-plus", "office", "Office 2021 Professional Plus"),
    # Windows (not windows-11-home — PRESERVE_PAGES)
    ("FQC-10528", "windows-11-pro", "windows", "Windows 11 Pro"),
    ("KW9-00136", "windows-10-home", "windows", "Windows 10 Home"),
    ("FQC-08930", "windows-10-pro", "windows", "Windows 10 Pro"),
    ("FQC-10538", "windows-11-pro-oem-dvd", "windows", "Windows 11 Pro OEM DVD"),
    ("W11_PRO_STICKER", "windows-11-pro-coa", "windows", "Windows 11 Pro COA"),
]

IMG = {
    "office": "microsoft-365-personal.webp",
    "windows": "microsoft-windows-11-home.webp",
}


def main():
    for sku, slug, template, card_name in DEFS:
        prod = {
            "sku": sku,
            "slug": slug,
            "template": template,
            "card_name": card_name,
            "image": IMG[template],
        }
        for lang in LANGS:
            path = ROOT / lang / f"{slug}.html"
            html = build_product_page(lang, prod)
            if 'class="pdp-cards"' not in html:
                raise SystemExit(f"rich markup missing for {slug}/{lang}")
            path.write_text(html, encoding="utf-8")
        print("rich", slug, "×", len(LANGS))


if __name__ == "__main__":
    main()
