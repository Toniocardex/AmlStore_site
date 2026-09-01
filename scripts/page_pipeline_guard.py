#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Perche' i generatori di pagina sono stati ritirati, e cosa controllano adesso.

build_product_page() / build_catalog_page() sono il PRIMO STADIO di una pipeline.
Le pagine pubblicate ne hanno attraversati altri quattro, piu' una modifica senza
script. Rieseguire un generatore sopra i file veri non "riallinea" niente: butta
via tutti gli stadi successivi. Misurato su tutte le pagine prodotto e catalogo
del sito (settembre 2026): zero file coincidono, il generato sta fra 8 e 61 KB,
il pubblicato fra 38 e 91 KB, e il delta e' quasi costante, ~30 KB per pagina.

Gli stadi che una rigenerazione cancellerebbe:

  1. header/footer pre-renderizzati nel light DOM -> scripts/build-inline-chrome.mjs
     Il grosso dei ~30 KB. Il markup lo produce scripts/chrome-renderer/ in un
     browser vero contro il dev server, quindi non e' riproducibile da Python.
     Ha gia' un proprietario e un `--check`.
  2. cache busting ?v=<hash> su ogni asset locale -> scripts/bump-asset-version.py
     Gli hash dipendono dal contenuto di css/ e js/: dentro il template
     marcirebbero al primo asset che cambia.
  3. banner <aml-lang-suggest> + components/lang-suggest.js
     -> scripts/apply-lang-suggest-banner.py
  4. chip "Regione di attivazione" nella buy card
     -> scripts/add-activation-region-badge.py (copy solo it/en/fr/de/es)

E, senza nessuno script che lo sappia rifare:

  5. il prefisso localizzato "Licenza / Licence / Lizenz / Licencia / Licenca /
     Licentie" su <title> e og:title (commit 904e3816). Non e' ricostruibile da
     una rigenerazione: andrebbe perso e basta.

Gli stadi 1 e 2 sono artefatti derivati da altri file. Duplicarli dentro
product_page_lib.py per "riallineare" il generatore li renderebbe una copia
stantia. Per rimettere in piedi una pagina si usa git, non una rigenerazione.

Quel che questi script fanno ancora, e per cui vanno tenuti: verificano sulle
pagine pubblicate le invarianti che prima verificavano sull'HTML appena
generato. Nessuno scrive piu' nulla.

Per rimisurare il disallineamento (senza toccare i file) basta confrontare in
memoria build_product_page(lang, prod) con lang/<slug>.html.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Marcatori dei quattro strati di post-produzione. Se cadono, qualcuno ha
# ripassato un generatore di primo stadio sopra le pagine.
PIPELINE_MARKERS = (
    ("header inline", "header-utility__inner"),
    ("footer inline", "site-footer"),
    ("cache busting ?v=", "?v="),
    ("banner lang-suggest", "aml-lang-suggest"),
)


def page_path(lang, slug):
    return ROOT / lang / f"{slug}.html"


def load(lang, slug):
    """HTML della pagina pubblicata, o None se il file non esiste."""
    path = page_path(lang, slug)
    return path.read_text(encoding="utf-8") if path.exists() else None


def pipeline_errors(lang, slug, html):
    """Errori sugli strati di post-produzione, con il sospetto gia' formulato."""
    return [
        f"{lang}/{slug}.html: manca lo strato '{label}' ({marker}) "
        "-- pagina probabilmente sovrascritta da un generatore"
        for label, marker in PIPELINE_MARKERS
        if marker not in html
    ]


def fail_if(errors, ok_message):
    """Chiude lo script: SystemExit con l'elenco, oppure la riga di conferma."""
    if errors:
        raise SystemExit("Pagine non conformi:\n  " + "\n  ".join(errors))
    print(ok_message)
