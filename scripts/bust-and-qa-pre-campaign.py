#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def file_hash(path: Path, n: int = 10) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:n]


def bust(html: str, css_name: str, new_v: str) -> str:
    return re.sub(
        rf"({re.escape(css_name)}\?v=)[a-f0-9]+",
        rf"\g<1>{new_v}",
        html,
    )


def main() -> None:
    v3 = file_hash(ROOT / "css" / "product-v3.css")
    pilot = file_hash(ROOT / "css" / "m365-family-pilot.css")
    print("product-v3", v3, "pilot", pilot)

    # Bust on Office + Family all langs
    for lang in ("en", "it", "fr", "de", "es"):
        for name in ("office-2024-home-business.html", "microsoft-365-family.html"):
            p = ROOT / lang / name
            t = p.read_text(encoding="utf-8")
            t2 = bust(t, "product-v3.css", v3)
            if "m365-family-pilot.css" in t2:
                t2 = bust(t2, "m365-family-pilot.css", pilot)
            if t2 != t:
                p.write_text(t2, encoding="utf-8", newline="\n")
                print("bust", p.relative_to(ROOT))

    # QA
    fails = []
    for lang in ("en", "fr"):
        t = (ROOT / lang / "microsoft-365-family.html").read_text(encoding="utf-8")
        if "Fino a 6" in t:
            fails.append(f"{lang} family still has Fino a 6")
    for lang in ("en", "it", "fr", "de", "es"):
        t = (ROOT / lang / "windows-11-home.html").read_text(encoding="utf-8")
        if ">None<" in t or 'aria-label="None"' in t:
            fails.append(f"{lang} windows-11-home still has None")
        t = (ROOT / lang / "project-standard-2024.html").read_text(encoding="utf-8")
        if "macOS" in t:
            fails.append(f"{lang} project still has macOS")
        for sku in ("office-2024-home-business.html", "microsoft-365-family.html"):
            t = (ROOT / lang / sku).read_text(encoding="utf-8")
            if "pdp-meta-row" not in t or "pdp-trust-line" not in t:
                fails.append(f"{lang}/{sku} missing meta/trust")
            if "list price" in t.lower() or "prezzo di listino" in t.lower() or "prix catalogue" in t.lower() or "listenpreis" in t.lower() or "precio de lista" in t.lower():
                fails.append(f"{lang}/{sku} still has generic list price wording")
            if "Microsoft Store (EU)" not in t and "Microsoft Store (UE)" not in t:
                fails.append(f"{lang}/{sku} missing Microsoft Store (EU/UE)")

    if fails:
        print("FAIL")
        for f in fails:
            print(" -", f)
        raise SystemExit(1)
    print("QA OK")


if __name__ == "__main__":
    main()
