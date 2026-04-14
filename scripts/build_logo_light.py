#!/usr/bin/env python3
"""
Crea varianti header logo per sfondo scuro da logo-header-400.webp:
- aree blu/navy → blu brand letto da img/favicon/favicon.png (media)
- testo/ombre scure → grigi chiari (anti-alias preservato)

Output: logo-header-400-light.webp, logo-header-200-light.webp (stesso aspect).
Richiede: pip install pillow
"""
from __future__ import annotations

import colorsys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC_LOGO = ROOT / "img" / "logo" / "logo-header-400.webp"
SRC_FAVICON = ROOT / "img" / "favicon" / "favicon.png"
OUT_DIR = ROOT / "img" / "logo"
OUT_400 = OUT_DIR / "logo-header-400-light.webp"
OUT_200 = OUT_DIR / "logo-header-200-light.webp"


def brand_blue_from_favicon() -> tuple[int, int, int]:
    im = Image.open(SRC_FAVICON).convert("RGBA")
    px = im.load()
    w, h = im.size
    rs: list[int] = []
    gs: list[int] = []
    bs: list[int] = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 128:
                continue
            rs.append(r)
            gs.append(g)
            bs.append(b)
    if not rs:
        return 28, 96, 231
    return (
        round(sum(rs) / len(rs)),
        round(sum(gs) / len(gs)),
        round(sum(bs) / len(bs)),
    )


def transform_pixel(
    r: int,
    g: int,
    b: int,
    a: int,
    br: int,
    bg: int,
    bb: int,
) -> tuple[int, int, int, int]:
    if a < 25:
        return r, g, b, a

    rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
    h_, s, v = colorsys.rgb_to_hsv(rf, gf, bf)

    # Blu grafico (navy nel master), intervallo calibrato sui campioni reali
    is_blue_shape = s > 0.10 and 0.48 < h_ < 0.68 and v < 0.96
    if is_blue_shape:
        brf, bgf, bbf = br / 255.0, bg / 255.0, bb / 255.0
        hb, sb, vb = colorsys.rgb_to_hsv(brf, bgf, bbf)
        out_v = min(1.0, max(0.22, v * (vb / 0.52) * 1.02))
        out_s = min(1.0, max(sb * 0.95, s * 0.92))
        nr, ng, nb = colorsys.hsv_to_rgb(hb, out_s, out_v)
        return int(nr * 255), int(ng * 255), int(nb * 255), a

    # Testo / grigi scuri → chiaro (mappa luminanza su [188, 252])
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    if lum < 118:
        t = lum / 118.0
        out = int(round(252 - t * 54))
        out = max(188, min(252, out))
        return out, out, out, a

    return r, g, b, a


def save_webp(im: Image.Image, path: Path, quality: int = 90) -> None:
    im.save(path, "WEBP", quality=quality, method=6)


def main() -> None:
    br, bg, bb = brand_blue_from_favicon()
    print(f"Blu brand da favicon (media RGB): ({br}, {bg}, {bb})")

    im = Image.open(SRC_LOGO).convert("RGBA")
    w, h = im.size
    src = im.load()
    out = Image.new("RGBA", (w, h))
    dst = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            dst[x, y] = transform_pixel(r, g, b, a, br, bg, bb)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    save_webp(out, OUT_400, quality=90)
    print(f"OK: {OUT_400.relative_to(ROOT)}")

    w200 = 200
    h200 = max(1, int(round(w200 * (h / w))))
    lo = out.resize((w200, h200), Image.Resampling.LANCZOS)
    save_webp(lo, OUT_200, quality=88)
    print(f"OK: {OUT_200.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
