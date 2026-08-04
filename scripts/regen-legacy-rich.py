#!/usr/bin/env python3
"""Rigenera le 6 pagine ex template compatto (product-v2.css) sul template
rich (product-v3.css): Adobe Acrobat Pro/Standard, CorelDRAW 2024, Acronis
True Image Advanced, bundle M365 Personal + Kaspersky/McAfee.

Contenuto in product_content_tools.py / product_content_bundles.py, agganciato
a resolve_rich_content() in product_page_lib.py. Definizioni prodotto
identiche a quelle in generate-wave3.py (stesso sku/template/card_name/image),
cosi' il catalogo non deve essere toccato — solo le 6 pagine prodotto.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from product_page_lib import LANGS, build_product_page  # noqa: E402

IMG_OFFICE = "microsoft-365-personal.webp"
IMG_FALLBACK = "product-cover-fallback.webp"

IMG_WIN = "microsoft-windows-11-home.webp"

PRODUCTS = [
    {"sku": "SC_M365P_MTOTPROT_5Device", "slug": "bundle-m365-personal-mcafee", "template": "bundle", "card_name": "M365 Personal + McAfee", "image": IMG_OFFICE},
    {"sku": "SC_M365_KPremium_5Device", "slug": "bundle-m365-personal-kaspersky", "template": "bundle", "card_name": "M365 Personal + Kaspersky", "image": IMG_OFFICE},
    {"sku": "AD_STD_2D-1A", "slug": "adobe-acrobat-standard", "template": "tool", "card_name": "Adobe Acrobat Standard", "image": IMG_FALLBACK, "brand": "Adobe"},
    {"sku": "SC916509", "slug": "adobe-acrobat-pro", "template": "tool", "card_name": "Adobe Acrobat Pro", "image": IMG_FALLBACK, "brand": "Adobe"},
    {"sku": "B0CXZR44LP", "slug": "coreldraw-2024", "template": "tool", "card_name": "CorelDRAW Graphics Suite 2024", "image": IMG_FALLBACK, "brand": "Corel"},
    {"sku": "ACRTRIAD1D1Y", "slug": "acronis-true-image-advanced", "template": "backup", "card_name": "Acronis True Image Advanced", "image": IMG_FALLBACK, "brand": "Acronis"},
    # Gia' sul template rich ma mai agganciata a resolve_rich_content(): l'HTML
    # su disco derivava (prima di oggi) da una modifica manuale, non dal
    # generatore — rischio di regressione silenziosa a ogni rigenerazione futura.
    {"sku": "SC_W11HOME_M365PERS", "slug": "bundle-windows-11-home-m365-personal", "template": "bundle", "card_name": "Windows 11 Home + M365 Personal", "image": IMG_WIN},
    # Riscritta solo per aggiungere il badge omaggio guida Copilot (copilot_bonus),
    # assente nel generatore fino ad ora: nessun'altra modifica di contenuto.
    {"sku": "QQ2-00012", "slug": "microsoft-365-personal", "template": "m365", "card_name": "Microsoft 365 Personal", "image": IMG_OFFICE},
]


def main():
    for prod in PRODUCTS:
        for lang in LANGS:
            target = ROOT / lang / f"{prod['slug']}.html"
            target.write_text(build_product_page(lang, prod), encoding="utf-8")
        print("page", prod["slug"])


if __name__ == "__main__":
    main()
