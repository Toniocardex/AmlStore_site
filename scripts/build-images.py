#!/usr/bin/env python3
"""
Rigenera favicon da img/favicon/favicon.png.
Opzionale: da img/logo/logo-header-400.webp rigenera logo-header-200.webp e le varianti *-light.webp per tema scuro (build_logo_light.py).
Richiede: pip install pillow
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC_FAVICON = ROOT / "img" / "favicon" / "favicon.png"
OUT_FAV = ROOT / "img" / "favicon"
OUT_LOGO = ROOT / "img" / "logo"
SRC_LOGO_HI = OUT_LOGO / "logo-header-400.webp"


def save_webp(im: Image.Image, path: Path, quality: int = 88) -> None:
    im.save(path, "WEBP", quality=quality, method=6)


def build_favicon() -> None:
    fav = Image.open(SRC_FAVICON).convert("RGBA")
    i32 = fav.resize((32, 32), Image.Resampling.LANCZOS)
    save_webp(i32, OUT_FAV / "icon-32.webp", quality=82)

    apple = fav.resize((180, 180), Image.Resampling.LANCZOS)
    apple.save(OUT_FAV / "apple-touch-icon.png", "PNG", optimize=True)

    i48 = fav.resize((48, 48), Image.Resampling.LANCZOS)
    i16 = fav.resize((16, 16), Image.Resampling.LANCZOS)
    i48.save(
        ROOT / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
        append_images=[i32, i16],
    )


def sync_logo_200_from_400() -> None:
    """Se esiste solo il master 400px, ricava il 200px per srcset."""
    if not SRC_LOGO_HI.is_file():
        print("Skip logo: manca img/logo/logo-header-400.webp (sostituiscilo a mano se aggiorni il brand).")
        return
    hi = Image.open(SRC_LOGO_HI).convert("RGBA")
    w400, h400 = hi.size
    if w400 < 1:
        return
    aspect = h400 / w400
    w200 = 200
    h200 = max(1, int(round(w200 * aspect)))
    lo = hi.resize((w200, h200), Image.Resampling.LANCZOS)
    save_webp(lo, OUT_LOGO / "logo-header-200.webp", quality=88)
    print("OK: logo-header-200.webp (da logo-header-400.webp)")


def build_logo_light_variant() -> None:
    """Variante header per tema scuro (blu da favicon, testo chiaro)."""
    script = ROOT / "scripts" / "build_logo_light.py"
    if not script.is_file() or not SRC_LOGO_HI.is_file():
        print("Skip logo light: manca script o logo-header-400.webp.")
        return
    subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)


def main() -> None:
    if not SRC_FAVICON.is_file():
        raise SystemExit(f"Manca sorgente favicon: {SRC_FAVICON}")
    OUT_FAV.mkdir(parents=True, exist_ok=True)
    OUT_LOGO.mkdir(parents=True, exist_ok=True)
    build_favicon()
    print("OK: favicon (icon-32.webp, apple-touch-icon.png, /favicon.ico)")
    sync_logo_200_from_400()
    build_logo_light_variant()


if __name__ == "__main__":
    main()
