#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia sulle pagine dei 7 SKU fisici (7 slug x 7 lingue = 49 file).

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Fino a settembre 2026 main() chiamava build_product_page() e sovrascriveva i 49
file. Eseguirlo oggi ne distruggerebbe circa meta': build_product_page() rende
24,6-31,9 KB, i file pubblicati stanno fra 54,4 e 61,7 KB, il confronto e' 49
diff su 49 (nessuna pagina coincide) e il delta e' 29,7-30,1 KB per pagina --
tutti e quattro i marcatori di PIPELINE_MARKERS sono presenti nel pubblicato e
assenti nel generato, su tutti e 49 i file. Non e' un bug della libreria: e' la
pipeline di post-produzione che manca. Il perche', e i cinque strati che
andrebbero persi, stanno in scripts/page_pipeline_guard.py.

Qui la posta e' piu' alta che altrove. Queste 49 pagine sono l'unico punto in
cui la disponibilita' dichiarata ai crawler viene riscritta a runtime da
functions/_middleware.js: una rigenerazione le riporterebbe alla baseline
statica, e il mismatch con il magazzino reale e' esattamente il bug che il
commit 4f6b62c2 ha chiuso.

Sovrapposizione, dichiarata: 5 dei 7 slug (i Server/SQL) sono controllati anche
da scripts/regen-server-pages.py, e tutti e 7 dal main() di
scripts/generate-wave3.py. Restano propri di questo script i due slug Windows
11 fisici (OEM DVD, COA) e soprattutto i due controlli sotto, che nessun altro
fa.

Quel che lo script fa ancora, e per cui va tenuto -- gli stessi due controlli
per cui era nato, spostati dall'HTML appena generato alle pagine pubblicate:

  1. i marcatori giacenze: data-physical="true", v2-stock e product-stock.js
     devono essere su tutte e 49 le pagine, altrimenti la UI di magazzino e il
     fetch client-side non partono;
  2. la mappa del middleware: DEFS e PHYSICAL_SLUG_TO_SKU in
     functions/api/_lib/seo-availability.js devono coincidere, altrimenti un
     nuovo slug fisico torna a dichiarare la disponibilita' statica ai crawler
     senza che nulla fallisca.

Senza effetti collaterali, non scrive nulla.

    python scripts/regen-physical-stock.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from page_pipeline_guard import fail_if, load, pipeline_errors  # noqa: E402
from product_page_lib import LANGS  # noqa: E402

DEFS = [
    ("FQC-10538", "windows-11-pro-oem-dvd", "windows", "Windows 11 Pro OEM DVD"),
    ("W11_PRO_STICKER", "windows-11-pro-coa", "windows", "Windows 11 Pro COA"),
    ("P73-07788", "windows-server-2019", "server", "Windows Server 2019 Standard"),
    ("P73-08328", "windows-server-2022", "server", "Windows Server 2022 Standard"),
    ("P73-08538", "windows-server-2025-dvd", "server", "Windows Server 2025 DVD"),
    ("P6L-00076", "sql-server-2022-enterprise", "server", "SQL Server 2022 Enterprise"),
    ("SC835510", "sql-server-2022-standard", "server", "SQL Server 2022 Standard"),
]

# Marcatori senza i quali la UI di magazzino non si accende sulla pagina servita.
STOCK_MARKERS = (
    ('data-physical="true"', "data-physical"),
    ("v2-stock", "v2-stock"),
    ("product-stock.js", "product-stock.js"),
)

SEO_AVAILABILITY_JS = ROOT / "functions" / "api" / "_lib" / "seo-availability.js"


def check_middleware_map():
    """DEFS e PHYSICAL_SLUG_TO_SKU devono coincidere.

    seo-availability.js usa quella mappa per sapere quale SKU interrogare quando
    serve una pagina fisica: se qui si aggiunge uno slug e la' no, la pagina
    torna a dichiarare la disponibilita' statica ai crawler senza che nulla
    fallisca. Meglio rompere qui.
    """
    if not SEO_AVAILABILITY_JS.exists():
        # Il file arriva con 4f6b62c2. Su un branch che non lo contiene ancora
        # non c'e' mappa da confrontare: si dichiara il salto, non si finge OK.
        print("NOTA: seo-availability.js assente, controllo mappa middleware saltato")
        return []
    src = SEO_AVAILABILITY_JS.read_text(encoding="utf-8")
    block = src.split("PHYSICAL_SLUG_TO_SKU = {", 1)[1].split("};", 1)[0]
    js_pairs = dict(re.findall(r"'([^']+)':\s*'([^']+)'", block))
    py_pairs = {slug: sku for sku, slug, _, _ in DEFS}
    if js_pairs == py_pairs:
        return []
    return [
        "PHYSICAL_SLUG_TO_SKU disallineata con DEFS: "
        f"solo in JS {sorted(set(js_pairs.items()) - set(py_pairs.items()))}, "
        f"solo in PY {sorted(set(py_pairs.items()) - set(js_pairs.items()))}"
    ]


def main():
    errors = check_middleware_map()
    for _sku, slug, _template, _card_name in DEFS:
        for lang in LANGS:
            html = load(lang, slug)
            if html is None:
                errors.append(f"{lang}/{slug}.html: manca il file")
                continue
            for marker, label in STOCK_MARKERS:
                if marker not in html:
                    errors.append(f"{lang}/{slug}.html: manca il marcatore giacenze '{label}'")
            errors += pipeline_errors(lang, slug, html)

    fail_if(errors, f"OK: {len(DEFS)} SKU fisici x {len(LANGS)} lingue")


if __name__ == "__main__":
    main()
