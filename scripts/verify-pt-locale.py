#!/usr/bin/env python3
"""Checks strutturali per la lingua pt dopo il retrofit."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es", "pt")
LOCALIZED_TO_PT = {
    "consulenza": "consultoria",
    "consultation": "consultoria",
    "beratung": "consultoria",
    "consultoria": "consultoria",
    "chi-siamo": "sobre-nos",
    "about-us": "sobre-nos",
    "qui-sommes-nous": "sobre-nos",
    "ueber-uns": "sobre-nos",
    "quienes-somos": "sobre-nos",
    "sobre-nos": "sobre-nos",
}
HEAD_HREFLANG = re.compile(
    r'<link rel="alternate" hreflang="([a-z]{2}|x-default)"\s+href="([^"]+)"'
)
ES_LEAK = re.compile(
    r"(¿|contraseñas|suscripción|licencia |Añadir|presupuesto|opiniones de)",
    re.I,
)


def slug_from_href(href: str) -> str:
    path = href.replace("https://eurolicenze.com/", "").strip("/")
    parts = path.split("/", 1)
    return parts[1] if len(parts) == 2 else ""


def check_page(path: Path, expect_pt_href: str | None = None) -> list[str]:
    src = path.read_text(encoding="utf-8")
    errs = []
    if path.name == "404.html":
        return errs
    tags = HEAD_HREFLANG.findall(src)
    codes = [c for c, _ in tags]
    if "pt" not in codes:
        errs.append("manca hreflang pt")
    for needed in LANGS + ("x-default",):
        if needed not in codes:
            errs.append(f"manca hreflang {needed}")
    pt_hrefs = [h for c, h in tags if c == "pt"]
    if expect_pt_href and pt_hrefs and pt_hrefs[0] != expect_pt_href:
        errs.append(f"hreflang pt atteso {expect_pt_href}, trovato {pt_hrefs[0]}")
    if path.parent.name in ("it", "en", "fr", "de", "es"):
        if '["it","en","fr","de","es"]' in src and '["it","en","fr","de","es","pt"]' not in src:
            errs.append("inLanguage array senza pt")
    if path.parent.name == "pt" and ES_LEAK.search(src):
        errs.append(f"possibile spagnolo residuo: {ES_LEAK.search(src).group(0)}")
    if "<ecommerce-header" in src and "lang-option" not in src:
        errs.append("header chrome non inlinato")
    return errs


def expected_pt(path: Path) -> str:
    stem = path.stem
    if stem == "index":
        return "https://eurolicenze.com/pt/"
    slug = LOCALIZED_TO_PT.get(stem, stem)
    return f"https://eurolicenze.com/pt/{slug}"


def main() -> int:
    problems = []
    counts = {lang: 0 for lang in LANGS}
    for lang in LANGS:
        for path in sorted((ROOT / lang).glob("*.html")):
            counts[lang] += 1
            errs = check_page(path, expected_pt(path))
            for e in errs:
                problems.append(f"{lang}/{path.name}: {e}")
    required_pt = [
        "index.html",
        "cart.html",
        "checkout.html",
        "checkout-success.html",
        "contacts.html",
        "sobre-nos.html",
        "consultoria.html",
        "privacy-policy.html",
        "cookie-policy.html",
        "terms-and-conditions.html",
        "returns-and-refunds.html",
        "microsoft-365-family.html",
        "microsoft-365-personal.html",
        "404.html",
    ]
    for name in required_pt:
        if not (ROOT / "pt" / name).exists():
            problems.append(f"manca pt/{name}")
    if not (ROOT / "asset/search-index/pt.json").exists():
        problems.append("manca asset/search-index/pt.json")
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if "https://eurolicenze.com/pt/" not in sm:
        problems.append("sitemap senza home pt")
    if "https://eurolicenze.com/pt/sobre-nos" not in sm:
        problems.append("sitemap senza sobre-nos")
    print(f"pagine per lingua: {counts}")
    print(f"problemi: {len(problems)}")
    for p in problems[:40]:
        print(" ", p)
    if len(problems) > 40:
        print(f"  ... +{len(problems) - 40}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
