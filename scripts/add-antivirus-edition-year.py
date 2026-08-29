#!/usr/bin/env python3
"""Patch chirurgica una tantum: aggiunge l'anno edizione (2026) ai titoli
delle schede McAfee Total Protection e Kaspersky (Standard/Plus/Premium),
su tutte le 7 lingue.

Non rigenera le pagine dal generatore (product_content_antivirus.py /
regen-antivirus-rich.py): quel percorso oggi produrrebbe anche una
regressione indipendente (perdita del prefisso "Licenza "/equivalenti nel
<title>, drift rispetto al codice attuale del generatore — vedi commit
associato) su tutti e 22 gli SKU antivirus, non solo sui 9 toccati qui.
Questo script fa solo replace letterali del nome prodotto gia' presente,
in ogni file che lo cita (PDP, pagina categoria, card home), lasciando
intatta ogni altra patch gia' presente (badge regione, lang-suggest,
markup header/footer, hash ?v=).

Dopo l'esecuzione:
    python scripts/build-google-shopping-feed.py
    python scripts/build-search-index.py
    python scripts/build-cross-sell-index.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_content_antivirus import _devices, _year, LANGS  # noqa: E402

EDITION_YEAR = 2026

# (prefix_senza_anno, prefix_con_anno, devices) — prefix e' cio' che precede
# " — {devices}" nel campo name, e cio' che precede " · {devices}" nell'H1.
PRODUCTS = [
    ("McAfee Total Protection", 1),
    ("McAfee Total Protection", 5),
    ("McAfee Total Protection", 10),
    ("Kaspersky Standard", 1),
    ("Kaspersky Plus", 1),
    ("Kaspersky Premium", 1),
    ("Kaspersky Premium", 3),
    ("Kaspersky Premium", 5),
    ("Kaspersky Premium", 10),
]

TARGET_FILES_PER_LANG = [
    "antivirus.html",
    "index.html",
    "mcafee-total-protection-1-device.html",
    "mcafee-total-protection-5-devices.html",
    "mcafee-total-protection-10-devices.html",
    "kaspersky-standard.html",
    "kaspersky-plus.html",
    "kaspersky-premium-1-device.html",
    "kaspersky-premium-3-devices.html",
    "kaspersky-premium-5-devices.html",
    "kaspersky-premium-10-devices.html",
]


def build_pairs():
    """-> {lang: [(old, new), ...]} per name completo e per title_span H1."""
    pairs = {lg: [] for lg in LANGS}
    for prefix, devices in PRODUCTS:
        d = _devices(devices)
        y = _year(1)
        for lg in LANGS:
            old_name = f"{prefix} — {d[lg]}"
            new_name = f"{prefix} {EDITION_YEAR} — {d[lg]} · {y[lg]}"
            pairs[lg].append((old_name, new_name))

            # title_span H1: prefix senza il brand principale (McAfee -> "Total
            # Protection"; Kaspersky {Tier} -> "{Tier}")
            span_prefix = prefix.split(" ", 1)[1]
            old_span = f"{span_prefix} · {d[lg]}"
            new_span = f"{span_prefix} {EDITION_YEAR} · {d[lg]}"
            pairs[lg].append((old_span, new_span))
    return pairs


def main():
    pairs = build_pairs()
    total_files = 0
    total_replacements = 0
    for lg in LANGS:
        for fname in TARGET_FILES_PER_LANG:
            path = ROOT / lg / fname
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            original = text
            file_replacements = 0
            for old, new in pairs[lg]:
                count = text.count(old)
                if count:
                    text = text.replace(old, new)
                    file_replacements += count
            if text != original:
                path.write_text(text, encoding="utf-8")
                total_files += 1
                total_replacements += file_replacements
                print(f"  {lg}/{fname}: {file_replacements} sostituzioni")
    print(f"Fatto. {total_replacements} sostituzioni in {total_files} file.")


if __name__ == "__main__":
    main()
