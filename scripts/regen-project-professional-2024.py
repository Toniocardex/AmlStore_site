#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia su project-professional-2024 (1 slug x 7 lingue = 7 file).

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Fino a settembre 2026 il corpo del modulo -- non protetto da un main(), quindi
scriveva al solo `import` -- chiamava build_product_page() e sovrascriveva i 7
file. Eseguirlo oggi ne distruggerebbe circa meta': build_product_page() rende
25,5-29,5 KB, i file pubblicati stanno fra 55,5 e 59,3 KB, il confronto e' 7
diff su 7 (nessuna pagina coincide) e il delta e' 29,7-30,1 KB per pagina.
Non e' un bug della libreria: e' la pipeline di post-produzione che manca.
Il perche', e i cinque strati che andrebbero persi, stanno in
scripts/page_pipeline_guard.py.

Neutralizzando quei cinque strati, il residuo fra generato e pubblicato e' zero:
qui la perdita sarebbe esattamente e solo la pipeline. (Nota: queste 7 pagine
sono fra le poche senza il prefisso "Licenza" nel <title>.)

Quel che lo script fa ancora, e per cui va tenuto: CTA, SKU e quattro strati su
tutte e 7 le lingue, piu' i cinque riferimenti di contenuto della scheda IT che
prima si limitava a stampare -- ora sono controlli veri. Senza effetti
collaterali, non scrive nulla.

    python scripts/regen-project-professional-2024.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from page_pipeline_guard import fail_if, load, pipeline_errors  # noqa: E402
from product_page_lib import LANGS, resolve_rich_content  # noqa: E402

SKU, SLUG = "EP2-07001", "project-professional-2024"

# Riferimenti che devono restare nella scheda IT: licenza, piano cloud a
# confronto, requisiti di sistema.
IT_NEEDLES = (
    "Licenza per 1 PC",
    "Project Piano 3",
    "Windows Server 2019",
    "LTSC",
    "1,6 GHz",
)


def main():
    if not resolve_rich_content(SLUG)[0]:
        raise SystemExit(f"missing rich content per {SLUG}")

    errors = []
    for lang in LANGS:
        html = load(lang, SLUG)
        if html is None:
            errors.append(f"{lang}/{SLUG}.html: manca il file")
            continue
        if 'id="product-primary-cta"' not in html:
            errors.append(f"{lang}/{SLUG}.html: manca la CTA primaria")
        if f'data-stripe-product-sku="{SKU}"' not in html:
            errors.append(f"{lang}/{SLUG}.html: SKU diverso da {SKU}")
        errors += pipeline_errors(lang, SLUG, html)

    it = load("it", SLUG) or ""
    errors += [f"it/{SLUG}.html: manca {needle!r}" for needle in IT_NEEDLES if needle not in it]

    fail_if(errors, f"OK: {SLUG} x {len(LANGS)} lingue")


if __name__ == "__main__":
    main()
