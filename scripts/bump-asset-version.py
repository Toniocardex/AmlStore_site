#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cache busting: aggiunge ?v=<hash contenuto> a ogni riferimento locale css/js
nelle pagine HTML. Idempotente: rilanciarlo aggiorna solo gli hash cambiati.

Da eseguire prima di ogni deploy (vedi GO-LIVE.md):
    python scripts/bump-asset-version.py
"""
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG_DIRS = ["it", "en", "fr", "de", "es", "pt", "nl"]
os.chdir(ROOT)

# Un asset dentro srcset: stessa forma dei riferimenti href/src, ma la lista e'
# separata da virgole e ogni voce ha un descrittore (800w, 2x...). Senza questo
# le varianti responsive non venivano mai invalidate in cache.
SRCSET_ATTR = re.compile(r'(srcset=")([^"]+)(")')
SRCSET_URL = re.compile(
    r'((?:\.\./|/)(?:asset|images)/[A-Za-z0-9._/-]+?'
    r'/?[A-Za-z0-9._-]+\.(?:webp|avif|jpe?g|png|svg))'
    r'(?:\?v=[A-Za-z0-9]+)?'
)

# href/src verso asset locali (relativi ../ o assoluti /), con o senza ?v= esistente.
# Copre css/js e immagini in-page (asset/media anche in sottocartelle, logo, favicon).
REF = re.compile(
    r'((?:href|src)=")'
    r'((?:\.\./|/)(?:css|js|components|fonts|logo|favicon|images/[A-Za-z0-9._-]+|asset/[A-Za-z0-9._/-]+?)'
    r'/[A-Za-z0-9._-]+\.(?:css|js|webp|avif|jpe?g|png|svg|ico))'
    r'(?:\?v=[A-Za-z0-9]+)?(")'
)

def short_hash(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:10]

hashes = {}

def asset_hash(site_path):
    """site_path tipo 'css/page.css' relativo alla root."""
    if site_path not in hashes:
        fs = os.path.join(ROOT, site_path.replace("/", os.sep))
        hashes[site_path] = short_hash(fs) if os.path.exists(fs) else None
    return hashes[site_path]

pages = ["404.html"] + [
    os.path.join(d, f) for d in LANG_DIRS for f in sorted(os.listdir(d)) if f.endswith(".html")
]

touched = 0
for page in pages:
    src = open(page, encoding="utf-8").read()

    def sub(m):
        ref = m.group(2)
        site_path = ref.lstrip("./") if ref.startswith("../") else ref.lstrip("/")
        h = asset_hash(site_path)
        if not h:
            return m.group(0)  # file inesistente: lascia com'è
        return f"{m.group(1)}{ref}?v={h}{m.group(3)}"

    def sub_srcset(m):
        def one(u):
            ref = u.group(1)
            site_path = ref.lstrip("./") if ref.startswith("../") else ref.lstrip("/")
            h = asset_hash(site_path)
            return f"{ref}?v={h}" if h else ref
        return f"{m.group(1)}{SRCSET_URL.sub(one, m.group(2))}{m.group(3)}"

    out = SRCSET_ATTR.sub(sub_srcset, REF.sub(sub, src))
    if out != src:
        open(page, "w", encoding="utf-8", newline="\n").write(out)
        touched += 1

missing = [p for p, h in hashes.items() if h is None]
print(f"pagine aggiornate: {touched} | asset con hash: {sum(1 for h in hashes.values() if h)}")
if missing:
    print("ATTENZIONE, riferimenti a file inesistenti:", *missing, sep="\n  - ")
    sys.exit(1)
