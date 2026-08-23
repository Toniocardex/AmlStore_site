#!/usr/bin/env python3
"""Elenca le stringhe di prodotto che finirebbero in olandese ancora in inglese.

Importa tutti i moduli `product_content_*`: la costruzione dei contenuti passa
per `nl_translations.nl_text()`, che registra in `MISSING` ogni stringa senza
traduzione. Il controllo copre quindi tutti i percorsi — `L()`, `backfill_lang()`
e le tabelle per-lingua costruite a mano, come `product_content_server.T`.

    python scripts/check-nl-translations.py           # riepilogo
    python scripts/check-nl-translations.py --list    # una stringa per riga
    python scripts/check-nl-translations.py --json F  # dump per tooling

Esce con 1 se resta qualcosa da tradurre, cosi' e' usabile in CI.
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

MODULES = (
    "product_page_lib",
    "product_content_office",
    "product_content_antivirus",
    "product_content_bundles",
    "product_content_flagship",
    "product_content_office_2021",
    "product_content_office_apps",
    "product_content_server",
    "product_content_tools",
    "product_content_windows",
)


def main() -> int:
    for name in MODULES:
        importlib.import_module(name)

    from nl_translations import MISSING, NL

    rows = sorted(MISSING, key=lambda s: (len(s), s))

    if "--json" in sys.argv:
        dest = sys.argv[sys.argv.index("--json") + 1]
        payload = [{"en": s} for s in rows]
        Path(dest).write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    if "--list" in sys.argv:
        for s in rows:
            print(s)

    residue = sum(len(s) for s in rows)
    print(f"tradotte: {len(NL)} | non tradotte: {len(rows)} | caratteri residui: {residue}")
    return 1 if rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
