#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_page_lib import LANGS, build_product_page, resolve_rich_content  # noqa: E402

sku, slug = "EP2-07001", "project-professional-2024"
content, _ = resolve_rich_content(slug)
if not content:
    raise SystemExit("missing rich content")

prod = {
    "sku": sku,
    "slug": slug,
    "template": "office",
    "card_name": "Project Professional 2024",
    "image": "microsoft-365-personal.webp",
}

for lang in LANGS:
    path = ROOT / lang / f"{slug}.html"
    html = build_product_page(lang, prod)
    if 'id="product-primary-cta"' not in html:
        raise SystemExit(f"CTA missing: {lang}")
    if f'data-stripe-product-sku="{sku}"' not in html:
        raise SystemExit(f"SKU missing: {lang}")
    path.write_text(html, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))

it = (ROOT / "it" / f"{slug}.html").read_text(encoding="utf-8")
for needle in (
    "Licenza per 1 PC",
    "Project Piano 3",
    "Windows Server 2019",
    "LTSC",
    "1,6 GHz",
):
    print(f"  IT has {needle!r}: {needle in it}")
