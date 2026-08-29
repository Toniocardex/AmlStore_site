#!/usr/bin/env python3
"""Genera un gemello .jpg per ogni immagine prodotto .webp in asset/media/products/.

Perche': Google Merchant Center segnala "Codifica dell'immagine non valida
[image_link]" su alcune schede pur essendo i file .webp validi (verificato:
VP8 standard, header HTTP/Content-Type corretti). E' un problema noto e
ricorrente del validatore immagini di Google con WebP, non un file corrotto
lato nostro — la soluzione pratica e' offrire a Google Merchant Center un
.jpg invece del .webp nel feed, lasciando il sito (schede prodotto) invariato
sul .webp per le performance.

Il file .jpg viene salvato accanto all'originale, stesso nome, per essere
servito dalla stessa cartella statica quando il sito viene ridistribuito.
build-google-shopping-feed.py preferisce il .jpg se presente per g:image_link.

Incrementale: salta i file gia' convertiti e piu' recenti del sorgente.

    python scripts/convert-product-images-to-jpg.py
    python scripts/convert-product-images-to-jpg.py --force
"""
import argparse
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_DIR = ROOT / "asset" / "media" / "products"
JPEG_QUALITY = 90


def convert_one(webp_path: Path, force: bool) -> str:
    jpg_path = webp_path.with_suffix(".jpg")
    if not force and jpg_path.exists() and jpg_path.stat().st_mtime >= webp_path.stat().st_mtime:
        return "skip"

    im = Image.open(webp_path)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    elif im.mode != "RGB":
        im = im.convert("RGB")

    im.save(jpg_path, "JPEG", quality=JPEG_QUALITY, optimize=True)
    return "written"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="riconverti anche i .jpg gia' aggiornati")
    args = ap.parse_args()

    webp_files = sorted(PRODUCTS_DIR.glob("*.webp"))
    if not webp_files:
        print(f"Nessun .webp trovato in {PRODUCTS_DIR}", file=sys.stderr)
        return 1

    counts = {"written": 0, "skip": 0}
    for webp_path in webp_files:
        status = convert_one(webp_path, args.force)
        counts[status] += 1
        if status == "written":
            print(f"  {webp_path.name} -> {webp_path.with_suffix('.jpg').name}")

    print(f"Fatto. {counts['written']} convertiti, {counts['skip']} gia' aggiornati.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
