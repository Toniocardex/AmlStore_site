#!/usr/bin/env python3
"""Regenerate the 7 physical SKU product pages (all langs) with data-physical + stock UI."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_page_lib import LANGS, PRODUCT_COVER_FALLBACK, build_product_page  # noqa: E402

IMG = PRODUCT_COVER_FALLBACK

DEFS = [
    ("FQC-10538", "windows-11-pro-oem-dvd", "windows", "Windows 11 Pro OEM DVD"),
    ("W11_PRO_STICKER", "windows-11-pro-coa", "windows", "Windows 11 Pro COA"),
    ("P73-07788", "windows-server-2019", "server", "Windows Server 2019 Standard"),
    ("P73-08328", "windows-server-2022", "server", "Windows Server 2022 Standard"),
    ("P73-08538", "windows-server-2025-dvd", "server", "Windows Server 2025 DVD"),
    ("P6L-00076", "sql-server-2022-enterprise", "server", "SQL Server 2022 Enterprise"),
    ("SC835510", "sql-server-2022-standard", "server", "SQL Server 2022 Standard"),
]


def check_middleware_map():
    """DEFS e PHYSICAL_SLUG_TO_SKU devono coincidere.

    functions/api/_lib/seo-availability.js usa quella mappa per sapere quale SKU
    interrogare quando serve una pagina fisica: se qui si aggiunge uno slug e la'
    no, la pagina torna a dichiarare la disponibilita' statica ai crawler senza
    che nulla fallisca. Meglio rompere qui.
    """
    src = (ROOT / "functions" / "api" / "_lib" / "seo-availability.js").read_text(encoding="utf-8")
    block = src.split("PHYSICAL_SLUG_TO_SKU = {", 1)[1].split("};", 1)[0]
    js_pairs = dict(re.findall(r"'([^']+)':\s*'([^']+)'", block))
    py_pairs = {slug: sku for sku, slug, _, _ in DEFS}
    if js_pairs != py_pairs:
        raise SystemExit(
            "PHYSICAL_SLUG_TO_SKU disallineata con DEFS:\n"
            f"  solo in JS: {sorted(set(js_pairs.items()) - set(py_pairs.items()))}\n"
            f"  solo in PY: {sorted(set(py_pairs.items()) - set(js_pairs.items()))}"
        )


def main():
    check_middleware_map()
    for sku, slug, template, card_name in DEFS:
        prod = {
            "sku": sku,
            "slug": slug,
            "template": template,
            "card_name": card_name,
            "image": IMG,
        }
        for lang in LANGS:
            path = ROOT / lang / f"{slug}.html"
            html = build_product_page(lang, prod)
            if 'data-physical="true"' not in html:
                raise SystemExit(f"MISSING data-physical: {slug}/{lang}")
            if "v2-stock" not in html:
                raise SystemExit(f"MISSING v2-stock: {slug}/{lang}")
            if "product-stock.js" not in html:
                raise SystemExit(f"MISSING product-stock.js: {slug}/{lang}")
            path.write_text(html, encoding="utf-8")
        print("physical", slug, "×", len(LANGS))


if __name__ == "__main__":
    main()
