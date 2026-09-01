#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia sulle pagine Windows Server / SQL (7 slug x 7 lingue = 49 file).

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Fino a settembre 2026 main() chiamava build_product_page() e sovrascriveva i 49
file. Eseguirlo oggi ne distruggerebbe circa meta': build_product_page() rende
24,9-30,9 KB, i file pubblicati stanno fra 54,8 e 60,7 KB, il confronto e' 49
diff su 49 (nessuna pagina coincide) e il delta e' 29,7-30,1 KB per pagina.
Non e' un bug della libreria: e' la pipeline di post-produzione che manca.
Il perche', e i cinque strati che andrebbero persi, stanno in
scripts/page_pipeline_guard.py.

Neutralizzando quei cinque strati, il residuo fra generato e pubblicato su
questi 7 slug e' zero: qui la perdita sarebbe esattamente e solo la pipeline.

Attenzione: 5 di questi 7 slug sono SKU fisici, sorvegliati anche da
scripts/regen-physical-stock.py (marcatori giacenze + mappa del middleware).

Quel che lo script fa ancora, e per cui va tenuto: la regressione per cui era
nato -- la copertina Windows 11 Home finita sulle schede Server/SQL -- ora e'
verificata sulle pagine pubblicate invece che sull'HTML appena generato, insieme
ai quattro strati. Senza effetti collaterali, non scrive nulla.

    python scripts/regen-server-pages.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from page_pipeline_guard import fail_if, load, pipeline_errors  # noqa: E402
from product_page_lib import LANGS, PRODUCT_COVER_FALLBACK  # noqa: E402

DEFS = [
    ("P73-07788", "windows-server-2019", "server", "Windows Server 2019 Standard"),
    ("P73-07788_ESD", "windows-server-2019-esd", "server", "Windows Server 2019 Standard ESD"),
    ("P73-08328", "windows-server-2022", "server", "Windows Server 2022 Standard"),
    ("EP2-25187", "windows-server-2025", "server", "Windows Server 2025 Standard"),
    ("P73-08538", "windows-server-2025-dvd", "server", "Windows Server 2025 DVD"),
    ("P6L-00076", "sql-server-2022-enterprise", "server", "SQL Server 2022 Enterprise"),
    ("SC835510", "sql-server-2022-standard", "server", "SQL Server 2022 Standard"),
]


def main():
    errors = []
    for _sku, slug, _template, _card_name in DEFS:
        for lang in LANGS:
            html = load(lang, slug)
            if html is None:
                errors.append(f"{lang}/{slug}.html: manca il file")
                continue
            if f"products/{slug}.webp" not in html and PRODUCT_COVER_FALLBACK not in html:
                errors.append(f"{lang}/{slug}.html: copertina inattesa")
            if "microsoft-windows-11-home.webp" in html:
                errors.append(f"{lang}/{slug}.html: copertina Windows 11 Home su una scheda Server/SQL")
            errors += pipeline_errors(lang, slug, html)

    fail_if(errors, f"OK: {len(DEFS)} slug Server/SQL x {len(LANGS)} lingue")


if __name__ == "__main__":
    main()
