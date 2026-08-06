#!/usr/bin/env python3
"""Bust product-v3.css (and m365-family-pilot.css) on all HTML that references them."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def h(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:10]


def main() -> None:
    v3 = h(ROOT / "css" / "product-v3.css")
    pilot = h(ROOT / "css" / "m365-family-pilot.css")
    print("product-v3", v3, "pilot", pilot)

    n_v3 = n_pilot = 0
    for path in ROOT.rglob("*.html"):
        if ".wrangler" in path.parts or "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        if "product-v3.css" in text:
            text2, c = re.subn(
                r"(product-v3\.css\?v=)[a-f0-9]+",
                rf"\g<1>{v3}",
                text,
            )
            text = text2
            n_v3 += c
        if "m365-family-pilot.css" in text:
            text2, c = re.subn(
                r"(m365-family-pilot\.css\?v=)[a-f0-9]+",
                rf"\g<1>{pilot}",
                text,
            )
            text = text2
            n_pilot += c
        if text != orig:
            path.write_text(text, encoding="utf-8", newline="\n")

    print(f"replaced product-v3 refs={n_v3} pilot refs={n_pilot}")

    # verify personal
    t = (ROOT / "en" / "microsoft-365-personal.html").read_text(encoding="utf-8")
    m = re.search(r"product-v3\.css\?v=([a-f0-9]+)", t)
    print("en personal now", m.group(1) if m else None, "match", m.group(1) == v3 if m else False)


if __name__ == "__main__":
    main()
