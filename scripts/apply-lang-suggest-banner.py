#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inserisce <aml-lang-suggest> (banner "pagina disponibile anche in <lingua>")
in tutte le pagine con chrome condiviso (skip-link + ecommerce-header +
cookie-banner.js). Esclude 404.html e admin/, che non caricano locale-path.js.

Idempotente: salta i file che hanno gia' il tag.
Da eseguire una tantum, poi bump-asset-version.py per l'hash del nuovo file.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ["it", "en", "fr", "de", "es"]

# Skip-link e apertura header: di norma su righe separate, ma alcune pagine
# (es. de/beratung.html) hanno il chrome compattato su una riga sola.
SKIP_LINK_RE = re.compile(
    r'(<a class="skip-link"[^>]*>[^<]*</a>)\s*(<ecommerce-header)'
)
# Script cookie-banner.js: path relativo (../components/...) o assoluto
# (/components/..., usato dalle pagine 404 localizzate). Alcune pagine
# (fr/consultation, de/beratung, es/consultoria) hanno l'intero blocco
# script compattato su una riga sola, senza newline dopo il tag.
COOKIE_SCRIPT_RE = re.compile(
    r'(<script src="(?:\.\./|/)components/cookie-banner\.js(?:\?v=[A-Za-z0-9]+)?" defer></script>)'
)
LANG_SUGGEST_SCRIPT_PREFIX = {  # ../components/... salvo le 404 localizzate (path assoluto)
    "default": "../components/lang-suggest.js",
    "404": "/components/lang-suggest.js",
}


def main():
    touched = 0
    skipped = []
    for lang in LANGS:
        for path in sorted((ROOT / lang).glob("*.html")):
            src = path.read_text(encoding="utf-8")
            if "aml-lang-suggest" in src:
                continue

            out, n1 = SKIP_LINK_RE.subn(
                r'\1\n    <aml-lang-suggest></aml-lang-suggest>\n\2', src, count=1
            )

            cookie_match = COOKIE_SCRIPT_RE.search(out)
            is_absolute = bool(cookie_match) and '"/components/' in cookie_match.group(1)
            script_src = LANG_SUGGEST_SCRIPT_PREFIX["404" if is_absolute else "default"]
            out, n2 = COOKIE_SCRIPT_RE.subn(
                r'\1<script src="' + script_src + r'" defer></script>', out, count=1
            )

            if n1 != 1 or n2 != 1:
                skipped.append((str(path), n1, n2))
                continue

            path.write_text(out, encoding="utf-8", newline="\n")
            touched += 1

    print(f"pagine aggiornate: {touched}")
    if skipped:
        print("ATTENZIONE, pattern non combaciante (skip-link, cookie-script):")
        for p, n1, n2 in skipped:
            print(f"  - {p} (skip-link matches={n1}, cookie-script matches={n2})")
        sys.exit(1)


if __name__ == "__main__":
    main()
