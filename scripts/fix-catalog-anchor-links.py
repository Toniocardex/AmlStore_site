#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-shot: ripunta i CTA "torna al catalogo" da #soluzioni (sezione rimossa) a #piu-venduti."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es")
PAGES = ("cart.html", "checkout.html")

for lang in LANGS:
    for page in PAGES:
        path = ROOT / lang / page
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        old = f'/{lang}/#soluzioni'
        if old not in html:
            continue
        html = html.replace(old, f'/{lang}/#piu-venduti')
        path.write_text(html, encoding="utf-8", newline="\n")
        print("fixed", lang, page)
