#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia sulla sola locale nl/ (61 schede + 6 cataloghi).

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Fino a settembre 2026 il corpo del modulo -- non protetto da un main(), quindi
scriveva al solo `import` -- chiamava build_product_page() e build_catalog_page()
e sovrascriveva le 67 pagine olandesi. Eseguirlo oggi ne distruggerebbe circa
meta': build_product_page() rende 24,6-53,4 KB, i file pubblicati stanno fra
54,2 e 83,3 KB, il confronto e' 61 diff su 61 (nessuna pagina coincide) e il
delta e' 29,6-32,0 KB per pagina. Non e' un bug della libreria: e' la pipeline
di post-produzione che manca. Il perche', e i cinque strati che andrebbero
persi, stanno in scripts/page_pipeline_guard.py.

Due cose specifiche di nl/:

  - il quarto strato (chip "Regione di attivazione") qui non c'e' su nessuna
    pagina: scripts/add-activation-region-badge.py non ha le copy pt e nl. Le
    pagine olandesi sono quindi disallineate dalle altre cinque lingue, ma la
    cura e' aggiungere quelle copy a quello script, non rigenerare;
  - il prefisso "Licentie" nel <title> c'e' su 59 pagine su 61, e nessuno
    script lo sa rifare.

Oltre alla pipeline si perderebbero le stesse modifiche a mano delle altre
lingue: FAQ JSON-LD su microsoft-365-personal, prezzi .pdp-plan su mcafee 5 e 10
dispositivi, conteggi dispositivi nei titoli e nel JSON-LD di 7 slug.

Le pagine olandesi scritte a mano (fuori dal generatore fin dall'inizio) sono
un'altra cosa e stanno in scripts/write-nl-hand-pages.py.

Quel che lo script fa ancora, e per cui va tenuto: verifica che nl/ abbia tutte
le schede e tutti i cataloghi del registro, e che il primo, il secondo e il
terzo strato ci siano; il chip regione e' segnalato a parte come lacuna nota.
Senza effetti collaterali, non scrive nulla.

    python scripts/generate-nl-only.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from page_pipeline_guard import fail_if, load, pipeline_errors  # noqa: E402

spec = importlib.util.spec_from_file_location("wave3", ROOT / "scripts" / "generate-wave3.py")
wave3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wave3)

LANG = "nl"


def main():
    errors = []
    missing_badge = 0

    slugs = [p["slug"] for p in wave3.PRODUCTS
             if f"{p['slug']}.html" not in wave3.PRESERVE_PAGES]
    slugs += list(wave3.listing_groups())

    for slug in slugs:
        html = load(LANG, slug)
        if html is None:
            errors.append(f"{LANG}/{slug}.html: manca il file")
            continue
        errors += pipeline_errors(LANG, slug, html)
        if "pdp-meta-chip" not in html:
            missing_badge += 1

    fail_if(errors, f"OK: {len(slugs)} pagine in {LANG}/ "
                    f"({missing_badge} senza chip regione, lacuna nota di "
                    "add-activation-region-badge.py)")


if __name__ == "__main__":
    main()
