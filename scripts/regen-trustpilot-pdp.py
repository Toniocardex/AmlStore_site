#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia sul blocco Trustpilot di tutte le schede prodotto
(62 slug x 7 lingue = 434 file, comprese le PRESERVE_PAGES).

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Aveva due percorsi di scrittura, e nessuno dei due andava piu' bene.

1) Rigenerazione delle 61 schede non preservate. main() chiamava
   build_product_page() e sovrascriveva 427 file. Eseguirlo oggi ne
   distruggerebbe circa meta': build_product_page() rende 24,1-60,8 KB, i file
   pubblicati stanno fra 53,9 e 90,8 KB, il confronto e' 427 diff su 427
   (nessuna pagina coincide) e il delta e' 29,6-32,3 KB per pagina. Non e' un
   bug della libreria: e' la pipeline di post-produzione che manca. Il perche',
   e i cinque strati che andrebbero persi, stanno in
   scripts/page_pipeline_guard.py. Oltre alla pipeline si perderebbero anche
   FAQ JSON-LD (microsoft-365-personal), prezzi .pdp-plan aggiornati a mano
   (mcafee 5 e 10 dispositivi) e i conteggi dispositivi nei titoli e nel
   JSON-LD di 7 slug -- l'elenco completo e' nei docstring di
   regen-legacy-rich.py e regen-antivirus-rich.py.

2) patch_preserve() sulle pagine scritte a mano. Inseriva il vecchio blocco
   #trustpilot-widget cercando ancore (</div></section> prima di <hr
   class="v2-divider">, il tag <script> di product-page.js) che quelle pagine
   non hanno piu': sui fallback cadeva su </main> e </body>, cioe' appendeva
   markup in fondo alla pagina.

In piu' era gia' morto per conto suo: importa _trustpilot_script_tag da
product_page_lib, che non esiste piu'. Lanciarlo oggi dava ImportError prima di
toccare un file. E il layout che cercava di installare e' superato: il TrustBox
grande e' stato spostato nella buy card da scripts/move-trustpilot-to-buy-card.py
e oggi lo rende _trustpilot_buy_mini() come .product-trustpilot.pdp-buy-trustpilot
(_trustpilot_block() e' rimasto solo come alias deprecato). Le sue vecchie
invarianti -- id="trustpilot-widget" e trustpilot-widget.js -- oggi sono false su
tutte e 434 le pagine: erano un controllo che segnalava un layout smontato tre
volte fa.

Quel che lo script fa ancora, e per cui va tenuto: verifica che il TrustBox
attuale sia presente su tutte le schede prodotto, incluse quelle preservate --
la copertura che patch_preserve() cercava di garantire -- piu' i quattro strati.
Senza effetti collaterali, non scrive nulla.

    python scripts/regen-trustpilot-pdp.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from page_pipeline_guard import fail_if, load, pipeline_errors  # noqa: E402
from product_page_lib import LANGS  # noqa: E402

spec = importlib.util.spec_from_file_location("generate_wave3", ROOT / "scripts" / "generate-wave3.py")
gw3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gw3)

PRESERVE = gw3.PRESERVE_PAGES
PRODUCTS = gw3.PRODUCTS

# Il TrustBox come lo rende oggi _trustpilot_buy_mini(), dentro la buy card.
TRUSTPILOT_MARKERS = ("product-trustpilot", "pdp-buy-trustpilot")


def main():
    errors = []
    for p in PRODUCTS:
        slug = p["slug"]
        preserved = f"{slug}.html" in PRESERVE
        for lang in LANGS:
            html = load(lang, slug)
            if html is None:
                errors.append(f"{lang}/{slug}.html: manca il file")
                continue
            for marker in TRUSTPILOT_MARKERS:
                if marker not in html:
                    where = "pagina preservata" if preserved else "scheda generata"
                    errors.append(f"{lang}/{slug}.html ({where}): manca il TrustBox ({marker})")
            errors += pipeline_errors(lang, slug, html)

    fail_if(errors, f"OK: TrustBox su {len(PRODUCTS)} slug x {len(LANGS)} lingue "
                    f"({len(PRESERVE)} preservati inclusi)")


if __name__ == "__main__":
    main()
