#!/usr/bin/env python3
"""Insert nl hreflang + JSON-LD inLanguage + home og:locale:alternate.

Scans it/en/fr/de/es/pt. Idempotent if hreflang=\"nl\" is already present.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXISTING = ("it", "en", "fr", "de", "es", "pt")

LOCALIZED = {
    "consulenza": "consultatie",
    "consultation": "consultatie",
    "beratung": "consultatie",
    "consultoria": "consultatie",
    "chi-siamo": "over-ons",
    "about-us": "over-ons",
    "qui-sommes-nous": "over-ons",
    "ueber-uns": "over-ons",
    "quienes-somos": "over-ons",
    "sobre-nos": "over-ons",
}

HREFLANG_PT = re.compile(
    r'(<link rel="alternate" hreflang="pt"\s+href="https://aml-store\.com/pt/([^"]*)">)\s*'
    r'(<link rel="alternate" hreflang="x-default")',
)
INLANG_ARR = (
    ('["it","en","fr","de","es","pt"]', '["it","en","fr","de","es","pt","nl"]'),
    ('["it", "en", "fr", "de", "es", "pt"]', '["it", "en", "fr", "de", "es", "pt", "nl"]'),
)


def nl_slug(pt_href_tail: str) -> str:
    tail = pt_href_tail.strip("/")
    if not tail:
        return ""
    return LOCALIZED.get(tail, tail)


def patch_file(path: Path) -> bool:
    src = path.read_text(encoding="utf-8")
    if 'hreflang="nl"' in src:
        changed = False
        out = src
        for old, new in INLANG_ARR:
            if old in out:
                out = out.replace(old, new)
                changed = True
        if changed:
            newline = "\r\n" if "\r\n" in src else "\n"
            path.write_text(out.replace("\r\n", "\n").replace("\n", newline), encoding="utf-8")
        return changed

    def repl(m: re.Match) -> str:
        pt_tag, pt_tail, xdef = m.group(1), m.group(2), m.group(3)
        slug = nl_slug(pt_tail)
        href = f"https://aml-store.com/nl/{slug}" if slug else "https://aml-store.com/nl/"
        sep = "\n    " if "\n" in m.group(0) else ""
        return f'{pt_tag}{sep}<link rel="alternate" hreflang="nl" href="{href}">{sep}{xdef}'

    out, n = HREFLANG_PT.subn(repl, src, count=1)
    for old, new in INLANG_ARR:
        if old in out:
            out = out.replace(old, new)
            n += 1

    if path.name == "index.html" and 'og:locale:alternate" content="nl_NL"' not in out:
        needle = '<meta property="og:locale:alternate" content="pt_PT">'
        if needle in out:
            out = out.replace(
                needle,
                needle + '\n    <meta property="og:locale:alternate" content="nl_NL">',
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
            elif 'hreflang="nl"' not in before and 'rel="alternate" hreflang="pt"' in before:
                skipped.append(str(path.relative_to(ROOT)))
    print(f"pagine aggiornate: {touched}")
    if skipped:
        print("ATTENZIONE, hreflang pt+x-default non trovato:")
        for p in skipped:
            print(" ", p)


if __name__ == "__main__":
    main()
