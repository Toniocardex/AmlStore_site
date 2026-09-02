#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia sulle schede antivirus (23 slug x 7 lingue = 161 file).

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Fino a settembre 2026 main() chiamava build_product_page() e sovrascriveva i 161
file. Eseguirlo oggi ne distruggerebbe circa meta': build_product_page() rende
26,0-31,4 KB, i file pubblicati stanno fra 56,0 e 61,3 KB, il confronto e' 161
diff su 161 (nessuna pagina coincide) e il delta e' 29,7-30,2 KB per pagina.
Non e' un bug della libreria: e' la pipeline di post-produzione che manca.
Il perche', e i cinque strati che andrebbero persi, stanno in
scripts/page_pipeline_guard.py.

Oltre alla pipeline, qui il generatore e le pagine divergono anche nel merito,
in tutte e due le direzioni:

  - mcafee-total-protection-5-devices e -10-devices (7 lingue ciascuno): il
    prezzo del piano "1 dispositivo" nel selettore .pdp-plan e' aggiornato solo
    sull'HTML (10,25 EUR); il generatore lo ricalcolerebbe a 7,95 EUR, cioe'
    riporterebbe indietro un prezzo in vetrina.
  - bitdefender-plus-* in es (4 slug): qui e' il contrario, sul disco c'e' una
    riga di copy mezza italiana ("Tecnologia Photon per analisi veloces sin
    ralentizaciones") che nel generatore e' gia' corretta. Va sistemata con una
    patch mirata sull'HTML, non rigenerando (vedi
    scripts/add-antivirus-edition-year.py per la forma di quelle patch).

Quel che lo script fa ancora, e per cui va tenuto: controlla che ogni slug con
contenuto in product_content_antivirus.py abbia una definizione qui (era il suo
check di copertura) e verifica sulle pagine pubblicate hero, CTA, SKU,
copertina di prodotto e i quattro strati. Senza effetti collaterali, non scrive
nulla.

    python scripts/regen-antivirus-rich.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from page_pipeline_guard import fail_if, load, pipeline_errors  # noqa: E402
from product_content_antivirus import PRODUCTS as AV  # noqa: E402
from product_page_lib import LANGS, resolve_rich_content  # noqa: E402

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
    orphans = [s for s in AV if s not in {d[1] for d in DEFS}]
    if orphans:
        raise SystemExit(f"Content without defs: {orphans}")

    errors = []
    for sku, slug, _brand in DEFS:
        if not resolve_rich_content(slug)[0]:
            errors.append(f"{slug}: nessun contenuto rich")
            continue
        for lang in LANGS:
            html = load(lang, slug)
            if html is None:
                errors.append(f"{lang}/{slug}.html: manca il file")
                continue
            if "pdp-hero" not in html:
                errors.append(f"{lang}/{slug}.html: manca l'hero .pdp-hero")
            if 'id="product-primary-cta"' not in html:
                errors.append(f"{lang}/{slug}.html: manca la CTA primaria")
            if f'data-stripe-product-sku="{sku}"' not in html:
                errors.append(f"{lang}/{slug}.html: SKU diverso da {sku}")
            if f"products/{slug}.webp" not in html:
                errors.append(f"{lang}/{slug}.html: manca la copertina products/{slug}.webp")
            errors += pipeline_errors(lang, slug, html)

    fail_if(errors, f"OK: {len(DEFS)} slug antivirus x {len(LANGS)} lingue")


if __name__ == "__main__":
    main()
