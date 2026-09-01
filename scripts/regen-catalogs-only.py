#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia sulle pagine catalogo (6 cataloghi x 7 lingue = 42 file).

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Fino a settembre 2026 il corpo del modulo chiamava build_catalog_page() e
sovrascriveva i 42 file. Era sfuggito al giro di disarmo precedente perche'
chiama build_catalog_page() e non build_product_page(), su cui era stata fatta
la ricerca.

Non era pero' l'ultimo generatore di primo stadio armato: resta armato
scripts/regen-physical-stock.py, che chiama build_product_page() e scrive le 49
pagine dei 7 SKU fisici. Non e' stato incluso in questo giro -- il commit
4f6b62c2 lo ha anzi esteso -- e va valutato a parte.

Eseguirlo oggi distruggerebbe fino a tre quarti di ogni catalogo:
build_catalog_page() rende 8,3-46,9 KB, i file pubblicati stanno fra 37,9 e
77,0 KB, il confronto e' 42 diff su 42 (nessuna pagina coincide) e il delta e'
29,5-30,2 KB per pagina. Non e' un bug della libreria: e' la pipeline di
post-produzione che manca -- tutti e quattro i marcatori di PIPELINE_MARKERS
sono presenti nel pubblicato e assenti nel generato, su tutti e 42 i file.
Il perche', e i cinque strati che andrebbero persi, stanno in
scripts/page_pipeline_guard.py.

Sovrapposizione, dichiarata: gli stessi 42 file sono gia' controllati dal main()
di scripts/generate-wave3.py, che itera lo stesso listing_groups() sulle stesse
LANGS con lo stesso pipeline_errors(). Questo script non aggiunge copertura:
resta come ingresso stretto e veloce sui soli cataloghi -- 42 file invece dei
469 piu' sitemap.xml e _redirects della passata completa di wave3 -- fedele allo
scopo per cui era nato (cataloghi soli, niente schede prodotto, niente
_redirects). Se un giorno le due verifiche divergessero, quella di wave3 e'
la piu' completa e va considerata l'autorita'.

L'elenco dei cataloghi resta preso da wave3.listing_groups(), unica fonte di
verita': nessuna lista di slug duplicata qui.

    python scripts/regen-catalogs-only.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from page_pipeline_guard import fail_if, load, pipeline_errors  # noqa: E402
from product_page_lib import LANGS  # noqa: E402

# generate-wave3.py ha un trattino nel nome: non e' importabile con `import`.
# L'exec a import-time non scrive nulla (il suo main() e' sotto __main__) e
# ricontrolla la coerenza del registro con catalog.json.
spec = importlib.util.spec_from_file_location("wave3", ROOT / "scripts" / "generate-wave3.py")
wave3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wave3)


def main():
    errors = []
    catalog_slugs = list(wave3.listing_groups())
    for catalog_slug in catalog_slugs:
        for lang in LANGS:
            html = load(lang, catalog_slug)
            if html is None:
                errors.append(f"{lang}/{catalog_slug}.html: manca il catalogo")
                continue
            errors += pipeline_errors(lang, catalog_slug, html)

    fail_if(errors, f"OK: {len(catalog_slugs)} cataloghi x {len(LANGS)} lingue")


if __name__ == "__main__":
    main()
