#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-shot: crea la variante McAfee Total Protection 3 dispositivi (SKU
MTP-3D-1Y, vendita 10,99 EUR, listino 34,95 EUR, sconto 69%).

La pipeline di rigenerazione PDP e' ritirata (vedi scripts/page_pipeline_guard.py):
le pagine si costruiscono clonando una scheda pubblicata e ritoccandola, non
rigenerando. Qui la sorgente e' mcafee-total-protection-5-devices.html (7 lingue),
gia' riprezzata a 14,89 EUR con scripts/set-manual-price.py.

Cosa fa (--apply per scrivere):
  1. catalog.json + functions/api/_lib/catalog.js: nuova voce MTP-3D-1Y.
  2. 7 nuove PDP  <lang>/mcafee-total-protection-3-devices.html  clonate dalla 5.
  3. Selettore .pdp-plans ricostruito a 4 chip (1/3/5/10) su TUTTE le schede
     McAfee: le 3 nuove + 1-device + 5-devices + 10-devices. Sistema anche la
     chip "5 dispositivi" rimasta a 15,44 su 1-device e 10-devices.
  4. asset/media/products/mcafee-total-protection-3-devices.{webp,jpg}: copia
     placeholder dell'immagine 5 dispositivi (la box-art riporta ancora "5
     Dispositivi": va sostituita con l'artwork 3 dispositivi reale).
  5. Card prodotto nella pagina categoria antivirus.html (7 lingue).

Dopo, rilanciare a mano: build-google-shopping-feed.py, build-cross-sell-index.py,
build-search-index.py, rebuild-sitemap.py, bump-asset-version.py, e i guard
regen-antivirus-rich.py / check-variant-price-consistency.py.
"""
import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es", "pt", "nl")

NEW_SKU = "MTP-3D-1Y"
OLD_SKU = "1108923"
SRC_SLUG = "mcafee-total-protection-5-devices"
NEW_SLUG = "mcafee-total-protection-3-devices"

# prezzi in centesimi
P1, P3, P5, P10 = 795, 1099, 1489, 1844
COMPARE_3 = 3495
DISC_3 = round((1 - P3 / COMPARE_3) * 100)  # 69

WORDS = {
    "it": ("dispositivo", "dispositivi"),
    "en": ("device", "devices"),
    "es": ("dispositivo", "dispositivos"),
    "fr": ("appareil", "appareils"),
    "de": ("Gerät", "Geräte"),
    "nl": ("apparaat", "apparaten"),
    "pt": ("dispositivo", "dispositivos"),
}
SLUG_BY_N = {1: "mcafee-total-protection-1-device", 3: NEW_SLUG,
             5: "mcafee-total-protection-5-devices", 10: "mcafee-total-protection-10-devices"}
PRICE_BY_N = {1: P1, 3: P3, 5: P5, 10: P10}

PLANS_RE = re.compile(r'<div class="pdp-plans"[^>]*>.*?</div>', re.S)


def eur(minor):
    return f"{minor // 100},{minor % 100:02d}"


def build_plans(lang, current_n):
    sing, plur = WORDS[lang]
    out = ['<div class="pdp-plans" role="group" aria-labelledby="pdp-plans-label">']
    for n in (1, 3, 5, 10):
        word = sing if n == 1 else plur
        label = f'{n} {word} · € {eur(PRICE_BY_N[n])}'
        if n == current_n:
            out.append(
                f'                    <span class="pdp-plan is-current" aria-current="true">'
                f'<b>{n}</b><span>{label}</span></span>'
            )
        else:
            out.append(
                f'                    <a class="pdp-plan" href="/{lang}/{SLUG_BY_N[n]}">'
                f'<b>{n}</b><span>{label}</span></a>'
            )
    out.append('                </div>')
    return "\n".join(out)


def clone_page(lang):
    src = ROOT / lang / f"{SRC_SLUG}.html"
    t = src.read_text(encoding="utf-8")
    sing, plur = WORDS[lang]

    # 1) slug ovunque (canonical, og:url, hreflang, JSON-LD url/@id, lang dropdown,
    #    preload/img, sticky thumb). Include il link "5-devices" nel vecchio
    #    selettore, che pero' viene poi ricostruito da capo.
    t = t.replace(SRC_SLUG, NEW_SLUG)

    # 2) SKU
    t = t.replace(f'data-stripe-product-sku="{OLD_SKU}"', f'data-stripe-product-sku="{NEW_SKU}"')
    t = t.replace(f'"sku": "{OLD_SKU}"', f'"sku": "{NEW_SKU}"')
    t = t.replace(f'<code class="v2-product-code__value">{OLD_SKU}</code>',
                  f'<code class="v2-product-code__value">{NEW_SKU}</code>')

    # 3) attributi prezzo sulla buy card
    t = t.replace('data-stripe-unit-amount="1489"', f'data-stripe-unit-amount="{P3}"')
    t = t.replace('data-stripe-compare-at-amount="3995"', f'data-stripe-compare-at-amount="{COMPARE_3}"')
    t = t.replace('data-discount-percent="63"', f'data-discount-percent="{DISC_3}"')

    # 4) prezzi meta / JSON-LD (formato con punto)
    t = t.replace('content="14.89"', 'content="10.99"')
    t = t.replace('"price": "14.89"', '"price": "10.99"')

    # 5) prezzi visibili (formato con virgola, euro + spazio normale)
    t = t.replace('€ 14,89', '€ 10,99')          # sale, sticky sale, price-sale
    t = t.replace('€ 39,95', '€ 34,95')          # msrp, sticky msrp
    t = t.replace('aria-label="39,95"', 'aria-label="34,95"')
    t = t.replace('63%', f'{DISC_3}%')            # badge sconto (unico "63%" in pagina)

    # 6) conteggio dispositivi nel copy (solo "5 <parola-plurale>", mai "5 o 10")
    t = t.replace(f'5 {plur}', f'3 {plur}')

    # 7) selettore varianti: 4 chip, corrente = 3
    t = PLANS_RE.sub(lambda _m: build_plans(lang, 3), t, count=1)

    return t


def patch_sibling(lang, slug, current_n):
    p = ROOT / lang / f"{slug}.html"
    t = p.read_text(encoding="utf-8")
    new = PLANS_RE.sub(lambda _m: build_plans(lang, current_n), t, count=1)
    return p, t, new


def update_catalog_json(apply):
    path = ROOT / "catalog.json"
    entries = json.loads(path.read_text(encoding="utf-8"))
    if any(e["sku"] == NEW_SKU for e in entries):
        print("catalog.json: voce gia' presente, salto")
        return
    idx = next(i for i, e in enumerate(entries) if e["sku"] == OLD_SKU)
    entry = {
        "sku": NEW_SKU,
        "ean": "",
        "name": "McAfee Total Protection 2026 | 3 Dispositivi | 1 Anno",
        "unitAmountMinor": P3,
        "compareAtMinor": COMPARE_3,
        "currency": "EUR",
        "type": "subscription",
        "category": "antivirus",
    }
    entries.insert(idx + 1, entry)
    print(f"catalog.json: +{NEW_SKU} dopo indice {idx}")
    if apply:
        path.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_catalog_js(apply):
    path = ROOT / "functions" / "api" / "_lib" / "catalog.js"
    t = path.read_text(encoding="utf-8")
    if NEW_SKU in t:
        print("catalog.js: voce gia' presente, salto")
        return
    anchor = f'  "{OLD_SKU}": {{'
    line = (f'  "{NEW_SKU}": {{ name: "McAfee Total Protection 2026 | 3 Dispositivi | 1 Anno", '
            f'unitAmountMinor: {P3}, compareAtMinor: {COMPARE_3}, currency: \'EUR\', '
            f'type: "subscription", category: "antivirus" }},\n')
    i = t.index(anchor)
    j = t.index("\n", i) + 1
    t = t[:j] + line + t[j:]
    print(f"catalog.js: +{NEW_SKU} dopo {OLD_SKU}")
    if apply:
        path.write_text(t, encoding="utf-8")


CARD_OPEN = '                <div\n                    class="product-card"\n'


def add_category_card(lang, apply):
    p = ROOT / lang / "antivirus.html"
    t = p.read_text(encoding="utf-8")
    if f'{NEW_SLUG}.html' in t:
        print(f"{lang}/antivirus.html: card gia' presente, salto")
        return
    sku_i = t.find(f'data-stripe-product-sku="{OLD_SKU}"')
    if sku_i < 0:
        print(f"{lang}/antivirus.html: SKU {OLD_SKU} non trovato, card NON aggiunta")
        return
    start = t.rfind(CARD_OPEN, 0, sku_i)
    end = t.find(CARD_OPEN, sku_i)
    if start < 0 or end < 0:
        print(f"{lang}/antivirus.html: confini card non trovati, card NON aggiunta")
        return
    card5 = t[start:end]                       # <div ...>...</div>\n
    if 'data-stripe-product-sku="1108923"' not in card5 or not card5.rstrip().endswith("</div>"):
        print(f"{lang}/antivirus.html: card 5-dev malformata, card NON aggiunta")
        return
    sing, plur = WORDS[lang]
    card3 = card5
    card3 = card3.replace('data-stripe-unit-amount="1489"', f'data-stripe-unit-amount="{P3}"')
    card3 = card3.replace('data-stripe-compare-at-amount="3995"', f'data-stripe-compare-at-amount="{COMPARE_3}"')
    card3 = card3.replace(f'data-stripe-product-sku="{OLD_SKU}"', f'data-stripe-product-sku="{NEW_SKU}"')
    card3 = card3.replace('data-discount-percent="63"', f'data-discount-percent="{DISC_3}"')
    card3 = card3.replace(f'{SRC_SLUG}.html', f'{NEW_SLUG}.html')
    card3 = card3.replace(f'products/{SRC_SLUG}.webp', f'products/{NEW_SLUG}.webp')
    card3 = card3.replace(f'5 {plur}', f'3 {plur}')
    card3 = card3.replace('€ 14,89', '€ 10,99')
    card3 = card3.replace('€ 39,95', '€ 34,95')
    card3 = card3.replace('63%', f'{DISC_3}%')
    out = t[:end] + card3 + t[end:]
    print(f"{lang}/antivirus.html: card 3-dev inserita dopo la 5-dev")
    if apply:
        p.write_text(out, encoding="utf-8")


def copy_images(apply):
    base = ROOT / "asset" / "media" / "products"
    for ext in ("webp", "jpg"):
        s = base / f"{SRC_SLUG}.{ext}"
        d = base / f"{NEW_SLUG}.{ext}"
        if d.exists():
            print(f"immagine {d.name}: gia' presente, salto")
            continue
        print(f"immagine {d.name}: copia placeholder da {s.name}")
        if apply:
            shutil.copyfile(s, d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    apply = args.apply

    update_catalog_json(apply)
    update_catalog_js(apply)

    for lang in LANGS:
        out = clone_page(lang)
        dest = ROOT / lang / f"{NEW_SLUG}.html"
        print(f"{lang}/{NEW_SLUG}.html: {'scritta' if apply else 'anteprima'} ({len(out)} byte)")
        if apply:
            dest.write_text(out, encoding="utf-8")

    siblings = [("mcafee-total-protection-1-device", 1),
                (SRC_SLUG, 5),
                ("mcafee-total-protection-10-devices", 10)]
    for lang in LANGS:
        for slug, cur in siblings:
            p, old, new = patch_sibling(lang, slug, cur)
            if old == new:
                print(f"{lang}/{slug}.html: selettore invariato (?)")
                continue
            print(f"{lang}/{slug}.html: selettore -> 4 chip")
            if apply:
                p.write_text(new, encoding="utf-8")

    for lang in LANGS:
        add_category_card(lang, apply)

    copy_images(apply)

    if not apply:
        print("\nDry-run. Rilancia con --apply.")


if __name__ == "__main__":
    main()
