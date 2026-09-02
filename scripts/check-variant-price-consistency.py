#!/usr/bin/env python3
"""Pre-commit check: prezzi coerenti nel selettore varianti delle PDP.

Ogni PDP con selettore versione (.pdp-plan) elenca le varianti sorelle con il
loro prezzo baked-in nel link. Quel prezzo va tenuto in pari con:
  1. il prezzo della chip "is-current" della pagina sorella linkata;
  2. il data-stripe-unit-amount della pagina stessa.

La pipeline di rigenerazione PDP aggiorna la pagina di una variante ma non
sempre rigenera i link sorella sulle altre: e' cosi' che e' rimasto un
"€ 10,25" obsoleto per McAfee 1 dispositivo sulle pagine 5 e 10 dispositivi
(fix del 2026-09-02). Questo script intercetta la stessa classe di bug.

Uso:
  python scripts/check-variant-price-consistency.py          # exit 1 se trova disallineamenti
"""
import glob
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es", "pt", "nl")

PLAN_RE = re.compile(
    r'<(a|span) class="pdp-plan(?P<cur>[^"]*)"[^>]*?(?:href="(?P<href>[^"]+)")?[^>]*>'
    r'\s*<b>[^<]*</b><span>(?P<label>[^<]*)</span>\s*</(?:a|span)>'
)
PRICE_RE = re.compile(r'·\s*€\s*([\d.,]+)\s*$')
UNIT_RE = re.compile(r'data-stripe-unit-amount="(\d+)"')


def minor_from_display(txt):
    return int(round(float(txt.replace(".", "").replace(",", ".")) * 100))


def main():
    current = {}   # "it/slug.html" -> display price string of its is-current chip
    stripe_minor = {}
    pages = {}     # path -> [(is_current, href, label, price_str)]

    for lang in LANGS:
        for f in glob.glob(str(ROOT / lang / "*.html")):
            rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
            html = Path(f).read_text(encoding="utf-8")
            if "pdp-plan" not in html:
                continue
            um = UNIT_RE.search(html)
            if um:
                stripe_minor[rel] = int(um.group(1))
            rows = []
            for m in PLAN_RE.finditer(html):
                is_cur = "is-current" in m.group("cur")
                pm = PRICE_RE.search(m.group("label").strip())
                price = pm.group(1) if pm else None
                rows.append((is_cur, m.group("href"), m.group("label").strip(), price))
                if is_cur:
                    current[rel] = price
            if rows:
                pages[rel] = rows

    problems = []

    # Check 1: sibling link price vs linked page's own is-current price
    for rel, rows in sorted(pages.items()):
        for is_cur, href, label, price in rows:
            if is_cur or not href or price is None:
                continue
            target = href.strip("/") + ".html"
            tgt = current.get(target)
            if tgt is None:
                problems.append(f"{rel}: link -> /{href.strip('/')} ma la pagina non ha una chip is-current con prezzo")
            elif tgt != price:
                problems.append(f"{rel}: link a {href.strip('/')} mostra € {price}, la pagina sorella dice € {tgt}")

    # Check 2: is-current chip vs data-stripe-unit-amount on the same page
    for rel, price in sorted(current.items()):
        if price is None or rel not in stripe_minor:
            continue
        if minor_from_display(price) != stripe_minor[rel]:
            problems.append(
                f"{rel}: chip selezionata € {price} != data-stripe-unit-amount {stripe_minor[rel]}"
            )

    if problems:
        print(f"{len(problems)} disallineamenti nel selettore varianti:\n")
        for p in problems:
            print(f"  - {p}")
        return 1

    print(f"OK - {len(pages)} PDP con selettore varianti, prezzi coerenti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
