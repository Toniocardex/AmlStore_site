#!/usr/bin/env python3
"""Generate only nl/ PDP and catalog pages (does not rewrite live locales)."""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_page_lib import build_catalog_page, build_product_page  # noqa: E402

spec = importlib.util.spec_from_file_location("wave3", ROOT / "scripts" / "generate-wave3.py")
wave3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wave3)

LANG = "nl"
out_dir = ROOT / LANG
out_dir.mkdir(exist_ok=True)

n = 0
for p in wave3.PRODUCTS:
    if f"{p['slug']}.html" in wave3.PRESERVE_PAGES:
        continue
    path = out_dir / f"{p['slug']}.html"
    path.write_text(build_product_page(LANG, p), encoding="utf-8", newline="\n")
    n += 1
    print("pdp", path.name)

for catalog_slug, items in wave3.listing_groups().items():
    path = out_dir / f"{catalog_slug}.html"
    path.write_text(build_catalog_page(LANG, catalog_slug, items), encoding="utf-8", newline="\n")
    n += 1
    print("catalog", path.name)

print(f"wrote {n} pages in {LANG}/")
