#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera lo sfondo dell'hero della home in AVIF + WebP, tre larghezze.

Perche' due formati: l'AVIF pesa ~25% meno a parita' di resa, ma il WebP
resta come sorgente del tag <img>, che e' anche il fallback per i browser
senza AVIF. Le tre larghezze servono al srcset con sizes="100vw" — su un
telefono si scarica la variante da 800px invece di quella da 1600.

Le qualita' sono tarate per stare sotto i ~30 KB alla larghezza massima:
l'immagine e' l'elemento LCP della home, quindi il peso conta piu' di un
dettaglio in piu' su una foto che sta comunque sotto uno scrim.

Uso:
    python scripts/build-home-hero-bg.py <sorgente.jpg>
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "asset" / "media"
STEM = "home-hero-bg"
WIDTHS = (1600, 1200, 800)
QUALITY = {"avif": dict(quality=52), "webp": dict(quality=72, method=6)}


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(2)

    src = Image.open(sys.argv[1]).convert("RGB")
    print(f"sorgente: {src.size[0]}x{src.size[1]}")

    for w in WIDTHS:
        h = round(src.size[1] * w / src.size[0])
        img = src.resize((w, h), Image.LANCZOS)
        for ext, kw in QUALITY.items():
            f = OUT / f"{STEM}-{w}.{ext}"
            img.save(f, **kw)
            print(f"  {f.name:26} {w}x{h}  {f.stat().st_size / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
