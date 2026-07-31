#!/usr/bin/env python3
"""Regenerate all antivirus rich product pages × 5 langs (sample-page layout)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_content_antivirus import PRODUCTS as AV  # noqa: E402
from product_page_lib import LANGS, build_product_page, resolve_rich_content  # noqa: E402

DEFS = [
    ("EAVH-N1-A1", "eset-nod32-1-device", "ESET"),
    ("EAVH-N1-A2", "eset-nod32-2-devices", "ESET"),
    ("EAVH-N1-A3", "eset-nod32-3-devices", "ESET"),
    ("EAVH-N1-A5", "eset-nod32-5-devices", "ESET"),
    ("EAVH-N1-A10", "eset-nod32-10-devices", "ESET"),
    ("EAVH-N2-A1", "eset-nod32-1-device-2y", "ESET"),
    ("21395096E7", "norton-360-standard", "Norton"),
    ("P1433901", "norton-360-standard-no-sub", "Norton"),
    ("NORT_360DEL_3D_1A", "norton-360-deluxe", "Norton"),
    ("NORT_360DEL_3D_1A-NOABB", "norton-360-deluxe-no-sub", "Norton"),
    ("7470A", "bitdefender-plus-1-device", "Bitdefender"),
    ("TL11012001-EN", "bitdefender-plus-3-devices", "Bitdefender"),
    ("TL11012001-EN-5D", "bitdefender-plus-5-devices", "Bitdefender"),
    ("TL11011010-DE", "bitdefender-plus-10-devices", "Bitdefender"),
    ("KASP_STD_1D_1A", "kaspersky-standard", "Kaspersky"),
    ("KASP_PLUS_1D_1A", "kaspersky-plus", "Kaspersky"),
    ("KL1047TDAFS", "kaspersky-premium-1-device", "Kaspersky"),
    ("KL1047GDCFS1", "kaspersky-premium-3-devices", "Kaspersky"),
    ("KL1047GDEFS", "kaspersky-premium-5-devices", "Kaspersky"),
    ("KL1047GDKFS", "kaspersky-premium-10-devices", "Kaspersky"),
    ("1108921", "mcafee-total-protection-1-device", "McAfee"),
    ("1108923", "mcafee-total-protection-5-devices", "McAfee"),
    ("MTP00MNRXRAAD", "mcafee-total-protection-10-devices", "McAfee"),
]


def main():
    missing = [s for s in AV if s not in {d[1] for d in DEFS}]
    if missing:
        raise SystemExit(f"Content without defs: {missing}")
    for sku, slug, brand in DEFS:
        content, ui = resolve_rich_content(slug)
        if not content:
            raise SystemExit(f"No rich content for {slug}")
        prod = {
            "sku": sku,
            "slug": slug,
            "template": "antivirus",
            "card_name": content["name"]["it"],
            "image": "microsoft-365-personal.webp",
            "brand": brand,
        }
        for lang in LANGS:
            html = build_product_page(lang, prod)
            if "v2-hero__ambient" not in html:
                raise SystemExit(f"Missing sample hero ambient: {slug}/{lang}")
            if 'id="product-primary-cta"' not in html:
                raise SystemExit(f"Missing CTA: {slug}/{lang}")
            if f'data-stripe-product-sku="{sku}"' not in html:
                raise SystemExit(f"SKU mismatch: {slug}/{lang}")
            if f"products/{slug}.webp" not in html:
                raise SystemExit(f"Product image missing in HTML: {slug}/{lang}")
            (ROOT / lang / f"{slug}.html").write_text(html, encoding="utf-8")
        print("rich", slug, "×", len(LANGS))


if __name__ == "__main__":
    main()
