#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cache busting: aggiunge ?v=<hash contenuto> a ogni riferimento locale css/js
nelle pagine HTML. Idempotente: rilanciarlo aggiorna solo gli hash cambiati.

Aggiorna anche i ?v= gia' presenti dentro i file JS, per gli asset caricati a
runtime (es. lo script del widget chat iniettato da components/header.js): in
HTML basta il tag, in JS il riferimento va marcato una volta a mano.

    script.src = '/components/support-chat.js?v=1';   <- marcatura iniziale
    script.src = '/components/support-chat.js?v=9f2c1ab304';  <- poi ci pensa qui

In JS si rinfrescano SOLO i path gia' marcati: lo stesso path puo' essere una
chiave di lookup invece di una URL da scaricare, e aggiungerci una query lo
romperebbe (vedi staticRootFromScriptPath in js/locale-path.js, che confronta
`pathname.endsWith('/components/header.js')`).

Da eseguire prima di ogni deploy (vedi GO-LIVE.md):
    python scripts/bump-asset-version.py
"""
import hashlib
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG_DIRS = ["it", "en", "fr", "de", "es"]
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

# Path di un asset locale, relativo (../) o assoluto (/).
# Copre css/js e immagini in-page (asset/media anche in sottocartelle, logo, favicon).
# Solo gruppi non catturanti: REF e JS_REF ci contano sopra.
ASSET_PATH = (
    r'(?:\.\./|/)(?:css|js|components|fonts|logo|favicon|images/[A-Za-z0-9._-]+|asset/[A-Za-z0-9._/-]+?)'
    r'/[A-Za-z0-9._-]+\.(?:css|js|webp|avif|jpe?g|png|svg|ico)'
)

# href/src nelle pagine, con o senza ?v= esistente.
REF = re.compile(r'((?:href|src)=")(' + ASSET_PATH + r')(?:\?v=[A-Za-z0-9]+)?(")')

# Riferimenti dentro i JS: il ?v= deve gia' esserci (vedi docstring).
JS_REF = re.compile(r'(' + ASSET_PATH + r')\?v=[A-Za-z0-9]+')

# Sorgenti JS che possono caricare asset a runtime.
JS_DIRS = ["components", "js", "admin"]
MAX_JS_PASSES = 5

def short_hash(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:10]

def write_atomic(path, text):
    """Scrive su file temporaneo e sostituisce, ritentando qualche volta.

    Su Windows il file puo' essere tenuto aperto per pochi millisecondi da
    OneDrive, dall'antivirus o dal dev server che guarda la cartella: con
    open(path, "w") diretto quel lock arriva DOPO il troncamento e lascia la
    pagina vuota. Qui l'originale resta intatto finche' il replace non riesce.
    """
    tmp = path + ".tmp-bump"
    last_error = None
    for attempt in range(5):
        try:
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            os.replace(tmp, path)
            return
        except OSError as error:
            last_error = error
            time.sleep(0.15 * (attempt + 1))
    try:
        os.remove(tmp)
    except OSError:
        pass
    raise last_error

hashes = {}
resolved = set()
missing_refs = set()

def asset_hash(site_path):
    """site_path tipo 'css/page.css' relativo alla root."""
    if site_path not in hashes:
        fs = os.path.join(ROOT, site_path.replace("/", os.sep))
        hashes[site_path] = short_hash(fs) if os.path.exists(fs) else None
    if hashes[site_path] is None:
        missing_refs.add(site_path)
    else:
        resolved.add(site_path)
    return hashes[site_path]

def site_path_of(ref):
    return ref.lstrip("./") if ref.startswith("../") else ref.lstrip("/")

def js_sources():
    found = []
    for directory in JS_DIRS:
        for base, _, files in os.walk(directory):
            found.extend(os.path.join(base, f) for f in sorted(files) if f.endswith(".js"))
    return sorted(found)

def bump_js_refs():
    """Rinfresca i ?v= dentro i JS.

    Si ripete finche' qualcosa cambia: un JS puo' referenziarne un altro e la
    riscrittura ne cambia l'hash a cascata. La cache degli hash va svuotata a
    ogni passaggio perche' i file appena riscritti hanno un hash nuovo.
    """
    def sub(m):
        ref = m.group(1)
        h = asset_hash(site_path_of(ref))
        return f"{ref}?v={h}" if h else m.group(0)

    sources = js_sources()
    updated = set()
    for _ in range(MAX_JS_PASSES):
        hashes.clear()
        stable = True
        for path in sources:
            src = open(path, encoding="utf-8").read()
            out = JS_REF.sub(sub, src)
            if out != src:
                write_atomic(path, out)
                updated.add(path)
                stable = False
        if stable:
            break
    else:
        print("ATTENZIONE: riferimenti JS non stabilizzati (ciclo o self-reference?)")
        sys.exit(1)
    hashes.clear()  # le pagine devono vedere l'hash dei JS appena riscritti
    return updated

js_touched = bump_js_refs()

pages = ["404.html"] + [
    os.path.join(d, f) for d in LANG_DIRS for f in sorted(os.listdir(d)) if f.endswith(".html")
]

touched = 0
for page in pages:
    src = open(page, encoding="utf-8").read()

    def sub(m):
        ref = m.group(2)
        h = asset_hash(site_path_of(ref))
        if not h:
            return m.group(0)  # file inesistente: lascia com'è
        return f"{m.group(1)}{ref}?v={h}{m.group(3)}"

    def sub_srcset(m):
        def one(u):
            ref = u.group(1)
            h = asset_hash(site_path_of(ref))
            return f"{ref}?v={h}" if h else ref
        return f"{m.group(1)}{SRCSET_URL.sub(one, m.group(2))}{m.group(3)}"

    out = SRCSET_ATTR.sub(sub_srcset, REF.sub(sub, src))
    if out != src:
        write_atomic(page, out)
        touched += 1

print(
    f"pagine aggiornate: {touched} | js aggiornati: {len(js_touched)}"
    f" | asset con hash: {len(resolved)}"
)
if missing_refs:
    print("ATTENZIONE, riferimenti a file inesistenti:", *sorted(missing_refs), sep="\n  - ")
    sys.exit(1)
