#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sostituisce la nota testuale pagamenti (.pf-pay-note) con i loghi (.pdp-pay)
su tutte le pagine prodotto rich, allineandole al layout della pagina pilota
(office-2024-home-business).

Patch mirata sull'HTML esistente, non una rigenerazione: i generatori
(regen-*.py / build_product_page) sono disallineati dal pre-render di
header/footer introdotto separatamente e riscriverebbero l'intera pagina
alla versione vecchia (senza header/footer inline, senza hash ?v=).

Da eseguire una tantum, poi bump-asset-version.py per gli hash dei loghi.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_page_lib import V3_UI, _render_payment_logos  # noqa: E402

LANGS = ["it", "en", "fr", "de", "es"]

BLOCK_RE = re.compile(
    r'                <p class="pf-pay-note">\n'
    r'                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
    r'<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>'
    r'<path stroke-linecap="round" stroke-linejoin="round" d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>\n'
    r'                    .*?\n'
    r'                </p>'
)


def main():
    touched = 0
    skipped = []
    for lang in LANGS:
        replacement = _render_payment_logos(V3_UI[lang])
        for path in sorted((ROOT / lang).glob("*.html")):
            src = path.read_text(encoding="utf-8")
            if 'class="pf-pay-note"' not in src:
                continue
            out, n = BLOCK_RE.subn(replacement, src)
            if n != 1:
                skipped.append((str(path), n))
                continue
            path.write_text(out, encoding="utf-8", newline="\n")
            touched += 1

    print(f"pagine aggiornate: {touched}")
    if skipped:
        print("ATTENZIONE, pf-pay-note trovato ma pattern non combaciante:")
        for p, n in skipped:
            print(f"  - {p} ({n} match)")
        sys.exit(1)


if __name__ == "__main__":
    main()
