#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia sulle pagine Office 2021 + Windows (9 slug x 7 lingue = 63 file).

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Fino a settembre 2026 main() chiamava build_product_page() e sovrascriveva i 63
file. Eseguirlo oggi ne distruggerebbe circa meta': build_product_page() rende
24,2-32,9 KB, i file pubblicati stanno fra 54,0 e 62,9 KB, il confronto e' 63
diff su 63 (nessuna pagina coincide) e il delta e' 29,7-30,3 KB per pagina.
Non e' un bug della libreria: e' la pipeline di post-produzione che manca.
Il perche', e i cinque strati che andrebbero persi, stanno in
scripts/page_pipeline_guard.py.

Neutralizzando quei cinque strati, il residuo fra generato e pubblicato su
questi 9 slug e' zero: qui la perdita sarebbe esattamente e solo la pipeline.
(Il prefisso "Licenza" e' su 56 di queste 63 pagine.)

Quel che lo script fa ancora, e per cui va tenuto: verifica sulle pagine
pubblicate il markup rich (.pdp-cards, era il suo unico check), lo SKU e i
quattro strati. Senza effetti collaterali, non scrive nulla.

    python scripts/regen-office2021-windows-rich.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from page_pipeline_guard import fail_if, load, pipeline_errors  # noqa: E402
from product_page_lib import LANGS  # noqa: E402

DEFS = [
    # Office 2021
    ("79G-05412", "office-2021-home-student", "office", "Office 2021 Home & Student"),
    ("T5D-03485", "office-2021-home-business", "office", "Office 2021 Home & Business"),
    ("T5D-03489", "office-2021-home-business-mac", "office", "Office 2021 Home & Business Mac"),
    ("GMGF0D7FX-0002-P", "office-2021-professional-plus", "office", "Office 2021 Professional Plus"),
    # Windows (windows-11-home no: contenuto in product_content_flagship,
    # sorvegliata da regen-legacy-rich.py insieme a Personal e Family)
    ("FQC-10528", "windows-11-pro", "windows", "Windows 11 Pro"),
    ("KW9-00136", "windows-10-home", "windows", "Windows 10 Home"),
    ("FQC-08930", "windows-10-pro", "windows", "Windows 10 Pro"),
    ("FQC-10538", "windows-11-pro-oem-dvd", "windows", "Windows 11 Pro OEM DVD"),
    ("W11_PRO_STICKER", "windows-11-pro-coa", "windows", "Windows 11 Pro COA"),
]


def main():
    errors = []
    for sku, slug, _template, _card_name in DEFS:
        for lang in LANGS:
            html = load(lang, slug)
            if html is None:
                errors.append(f"{lang}/{slug}.html: manca il file")
                continue
            if 'class="pdp-cards"' not in html:
                errors.append(f"{lang}/{slug}.html: manca il markup rich (.pdp-cards)")
            if f'data-stripe-product-sku="{sku}"' not in html:
                errors.append(f"{lang}/{slug}.html: SKU diverso da {sku}")
            errors += pipeline_errors(lang, slug, html)

    fail_if(errors, f"OK: {len(DEFS)} slug Office 2021/Windows x {len(LANGS)} lingue")


if __name__ == "__main__":
    main()
