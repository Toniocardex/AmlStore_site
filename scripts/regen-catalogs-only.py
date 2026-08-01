#!/usr/bin/env python3
"""Rebuild listing/catalog pages only (no product PDPs, no _redirects)."""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_page_lib import LANGS, build_catalog_page  # noqa: E402

spec = importlib.util.spec_from_file_location("wave3", ROOT / "scripts" / "generate-wave3.py")
wave3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wave3)

for catalog_slug, items in wave3.listing_groups().items():
    for lang in LANGS:
        path = ROOT / lang / f"{catalog_slug}.html"
        path.write_text(build_catalog_page(lang, catalog_slug, items), encoding="utf-8")
    print("catalog", catalog_slug, len(items))
