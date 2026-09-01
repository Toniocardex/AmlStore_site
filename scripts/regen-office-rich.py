#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia sulle 4 pagine Office 2024 / 2019 (4 slug x 7 lingue = 28 file).

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Fino a settembre 2026 main() chiamava build_product_page() e sovrascriveva i 28
file. Eseguirlo oggi ne distruggerebbe circa meta': build_product_page() rende
27,9-34,9 KB, i file pubblicati stanno fra 57,8 e 64,9 KB, il confronto e' 28
diff su 28 (nessuna pagina coincide) e il delta e' 29,7-30,3 KB per pagina.
Non e' un bug della libreria: e' la pipeline di post-produzione che manca.
Il perche', e i cinque strati che andrebbero persi, stanno in
scripts/page_pipeline_guard.py.

Neutralizzando quei cinque strati, il residuo fra generato e pubblicato su
questi 4 slug e' zero: qui la perdita sarebbe esattamente e solo la pipeline.

Quel che lo script fa ancora, e per cui va tenuto: controlla che ogni slug con
contenuto in product_content_office.py abbia una definizione qui (era il suo
check di copertura), e verifica sulle pagine pubblicate CTA, SKU e i quattro
strati. Senza effetti collaterali, non scrive nulla.

    python scripts/regen-office-rich.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from page_pipeline_guard import fail_if, load, pipeline_errors  # noqa: E402
from product_content_office import PRODUCTS as OFFICE_CONTENT  # noqa: E402
from product_page_lib import LANGS  # noqa: E402

# slug -> (sku, card_name, image)
OFFICE_DEFS = {
    "office-2024-home": ("EP2-06798", "Office 2024 Home", "microsoft-365-personal.webp"),
    "office-2024-home-business": ("EP2-06606", "Office 2024 Home & Business", "microsoft-365-personal.webp"),
    "office-2019-home-student": ("79G-05018", "Office 2019 Home & Student", "microsoft-365-personal.webp"),
    "office-2019-professional-plus": ("269-17068", "Office 2019 Professional Plus", "microsoft-365-personal.webp"),
}


def main():
    missing = [s for s in OFFICE_CONTENT if s not in OFFICE_DEFS]
    if missing:
        raise SystemExit(f"Missing defs for: {missing}")

    errors = []
    for slug, (sku, _card_name, _image) in OFFICE_DEFS.items():
        for lang in LANGS:
            html = load(lang, slug)
            if html is None:
                errors.append(f"{lang}/{slug}.html: manca il file")
                continue
            if 'id="product-primary-cta"' not in html:
                errors.append(f"{lang}/{slug}.html: manca la CTA primaria")
            if f'data-stripe-product-sku="{sku}"' not in html:
                errors.append(f"{lang}/{slug}.html: SKU diverso da {sku}")
            errors += pipeline_errors(lang, slug, html)

    fail_if(errors, f"OK: {len(OFFICE_DEFS)} slug Office x {len(LANGS)} lingue")


if __name__ == "__main__":
    main()
