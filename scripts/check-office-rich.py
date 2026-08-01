#!/usr/bin/env python3
"""Smoke-check Office rich pages: prices, CTA, images, no −0% badge, multilang."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_page_lib import LANGS, entry, resolve_rich_content  # noqa: E402

errors = []
for sku, slug, template, card_name in [
    ("EP2-06798", "office-2024-home", "office", "Office 2024 Home"),
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
]:
    content, _ = resolve_rich_content(slug)
    if not content:
        errors.append(f"{slug}: no rich content")
        continue
    e = entry(sku)
    sale = e["unitAmountMinor"]
    compare = e["compareAtMinor"]
    disc = 0 if compare <= sale else int(round((1 - sale / compare) * 100))
    for lang in LANGS:
        path = ROOT / lang / f"{slug}.html"
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
            continue
        t = path.read_text(encoding="utf-8")
        if f'data-stripe-unit-amount="{sale}"' not in t:
            errors.append(f"{lang}/{slug}: unit amount mismatch")
        if f'data-stripe-compare-at-amount="{compare}"' not in t:
            errors.append(f"{lang}/{slug}: compare amount mismatch")
        if 'id="product-primary-cta"' not in t:
            errors.append(f"{lang}/{slug}: missing primary CTA")
        if 'class="v2-bento"' not in t:
            errors.append(f"{lang}/{slug}: missing bento")
        if "−0%" in t or "data-discount-percent=\"0\"></span>\n                <span class=\"v2-price-badge\">" in t:
            errors.append(f"{lang}/{slug}: zero discount badge shown")
        if disc == 0 and "v2-price-badge" in t:
            errors.append(f"{lang}/{slug}: badge present with 0% discount")
        if disc > 0 and f"−{disc}%" not in t:
            errors.append(f"{lang}/{slug}: expected −{disc}%")
        img = ROOT / "asset" / "media" / "products" / f"{slug}.webp"
        if img.exists() and f"products/{slug}.webp" not in t:
            errors.append(f"{lang}/{slug}: product image not used")
        # green badge (not accent blue only)
        if "v2-price-badge" in t and "#10b981" not in (ROOT / "css" / "microsoft-365-product.css").read_text(encoding="utf-8"):
            errors.append("css: green badge missing from stylesheet")

if errors:
    print("FAIL", len(errors))
    for err in errors[:40]:
        print(" -", err)
    sys.exit(1)
print("OK: all Office rich pages aligned across", len(LANGS), "langs")
