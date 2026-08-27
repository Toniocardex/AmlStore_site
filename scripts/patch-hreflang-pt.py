#!/usr/bin/env python3
"""Insert pt hreflang + JSON-LD inLanguage + home og:locale:alternate.

Scans it/en/fr/de/es HTML only (pt pages already include the sixth language).
Idempotent: skips files that already have hreflang=\"pt\".
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXISTING = ("it", "en", "fr", "de", "es")

LOCALIZED = {
    "consulenza": "consultoria",
    "consultation": "consultoria",
    "beratung": "consultoria",
    "consultoria": "consultoria",
    "chi-siamo": "sobre-nos",
    "about-us": "sobre-nos",
    "qui-sommes-nous": "sobre-nos",
    "ueber-uns": "sobre-nos",
    "quienes-somos": "sobre-nos",
}

HREFLANG_ES = re.compile(
    r'(<link rel="alternate" hreflang="es"\s+href="https://eurolicenze\.com/es/([^"]*)">)\s*'
    r'(<link rel="alternate" hreflang="x-default")',
)
INLANG_ARR = (
    ('["it","en","fr","de","es"]', '["it","en","fr","de","es","pt"]'),
    ('["it", "en", "fr", "de", "es"]', '["it", "en", "fr", "de", "es", "pt"]'),
)


def pt_slug(es_href_tail: str) -> str:
    tail = es_href_tail.strip("/")
    if not tail:
        return ""
    return LOCALIZED.get(tail, tail)


def patch_file(path: Path) -> bool:
    src = path.read_text(encoding="utf-8")
    if 'hreflang="pt"' in src:
        changed = False
        out = src
        for old, new in INLANG_ARR:
            if old in out:
                out = out.replace(old, new)
                changed = True
        if changed:
            path.write_text(out, encoding="utf-8", newline="\n" if "\r\n" not in src else None)
        return changed

    def repl(m: re.Match) -> str:
        es_tag, es_tail, xdef = m.group(1), m.group(2), m.group(3)
        slug = pt_slug(es_tail)
        href = f"https://eurolicenze.com/pt/{slug}" if slug else "https://eurolicenze.com/pt/"
        sep = "\n    " if "\n" in m.group(0) else ""
        return f'{es_tag}{sep}<link rel="alternate" hreflang="pt" href="{href}">{sep}{xdef}'

    out, n = HREFLANG_ES.subn(repl, src, count=1)
    for old, new in INLANG_ARR:
        if old in out:
            out = out.replace(old, new)
            n += 1

    if path.name == "index.html" and 'og:locale:alternate" content="pt_PT"' not in out:
        needle = '<meta property="og:locale:alternate" content="es_ES">'
        if needle in out:
            out = out.replace(
                needle,
                needle + '\n    <meta property="og:locale:alternate" content="pt_PT">',
                1,
            )
            n += 1
        else:
            # homes that list alternates without es_ES (it/en already have es)
            last_alt = '<meta property="og:locale:alternate" content="de_DE">'
            if last_alt in out and 'content="pt_PT"' not in out:
                out = out.replace(
                    last_alt,
                    last_alt + '\n    <meta property="og:locale:alternate" content="es_ES">\n    <meta property="og:locale:alternate" content="pt_PT">',
                    1,
                )
                n += 1

    if n == 0:
        return False
    newline = "\r\n" if "\r\n" in src else "\n"
    path.write_text(out.replace("\r\n", "\n").replace("\n", newline), encoding="utf-8")
    return True


def main() -> None:
    touched = 0
    skipped = []
    for lang in EXISTING:
        for path in sorted((ROOT / lang).glob("*.html")):
            before = path.read_text(encoding="utf-8")
            if patch_file(path):
                touched += 1
            elif 'hreflang="pt"' not in before and 'rel="alternate" hreflang="es"' in before:
                skipped.append(str(path))
    print(f"pagine aggiornate: {touched}")
    if skipped:
        print("ATTENZIONE, hreflang es+x-default non trovato:")
        for p in skipped:
            print(" ", p)


if __name__ == "__main__":
    main()
