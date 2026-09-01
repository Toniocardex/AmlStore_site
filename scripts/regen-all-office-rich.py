#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia su tutte le schede template Office + M365 Business Standard
(17 slug x 7 lingue = 119 file).

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Fino a settembre 2026 main() chiamava build_product_page() e sovrascriveva i 119
file. Eseguirlo oggi ne distruggerebbe circa meta': build_product_page() rende
24,1-60,8 KB, i file pubblicati stanno fra 53,9 e 90,8 KB, il confronto e' 119
diff su 119 (nessuna pagina coincide) e il delta e' 29,6-30,3 KB per pagina.
Non e' un bug della libreria: e' la pipeline di post-produzione che manca.
Il perche', e i cinque strati che andrebbero persi, stanno in
scripts/page_pipeline_guard.py.

Oltre alla pipeline, qui si perderebbero anche modifiche di contenuto fatte a
mano sul solo HTML, che nessun modulo di contenuto conosce:

  - microsoft-365-business-standard (7 lingue): il conteggio dispositivi nel
    <title>, in og:title e nel "name" del JSON-LD ("... 1 Anno - 15 dispositivi"
    contro "... 1 Anno | Licenza Originale"), e il passaggio da "Fattura
    Elettronica con P.IVA" a "Fattura elettronica" in cinque punti della pagina.

Quel che lo script fa ancora, e per cui va tenuto: controlla che ogni slug abbia
contenuto rich agganciato a resolve_rich_content() (era il suo check iniziale) e
verifica sulle pagine pubblicate CTA, SKU e i quattro strati. Senza effetti
collaterali, non scrive nulla.

    python scripts/regen-all-office-rich.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from page_pipeline_guard import fail_if, load, pipeline_errors  # noqa: E402
from product_page_lib import LANGS, resolve_rich_content  # noqa: E402

# sku, slug, template, card_name
DEFS = [
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
]


def main():
    missing = [slug for _, slug, _, _ in DEFS if not resolve_rich_content(slug)[0]]
    if missing:
        raise SystemExit(f"Missing rich content for: {missing}")

    errors = []
    for sku, slug, _template, _card_name in DEFS:
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

    fail_if(errors, f"OK: {len(DEFS)} slug Office/M365 x {len(LANGS)} lingue")


if __name__ == "__main__":
    main()
