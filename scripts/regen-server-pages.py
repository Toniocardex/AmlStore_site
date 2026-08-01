#!/usr/bin/env python3
"""Regenerate Windows Server / SQL compact product pages (correct product covers)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_page_lib import LANGS, PRODUCT_COVER_FALLBACK, build_product_page  # noqa: E402

DEFS = [
    ("P73-07788", "windows-server-2019", "server", "Windows Server 2019 Standard"),
    ("P73-07788_ESD", "windows-server-2019-esd", "server", "Windows Server 2019 Standard ESD"),
    ("P73-08328", "windows-server-2022", "server", "Windows Server 2022 Standard"),
    ("EP2-25187", "windows-server-2025", "server", "Windows Server 2025 Standard"),
    ("P73-08538", "windows-server-2025-dvd", "server", "Windows Server 2025 DVD"),
    ("P6L-00076", "sql-server-2022-enterprise", "server", "SQL Server 2022 Enterprise"),
    ("SC835510", "sql-server-2022-standard", "server", "SQL Server 2022 Standard"),
]


def main():
    for sku, slug, template, card_name in DEFS:
        prod = {
            "sku": sku,
            "slug": slug,
            "template": template,
            "card_name": card_name,
            "image": PRODUCT_COVER_FALLBACK,
        }
        for lang in LANGS:
            path = ROOT / lang / f"{slug}.html"
            html = build_product_page(lang, prod)
            if f"products/{slug}.webp" not in html and PRODUCT_COVER_FALLBACK not in html:
                raise SystemExit(f"unexpected cover on {slug}/{lang}")
            if "microsoft-windows-11-home.webp" in html:
                raise SystemExit(f"Win11 Home cover still present: {slug}/{lang}")
            path.write_text(html, encoding="utf-8")
        print("server", slug, "×", len(LANGS))


if __name__ == "__main__":
    main()
