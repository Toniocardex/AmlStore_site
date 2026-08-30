#!/usr/bin/env python3
"""Cambia manualmente il prezzo di vendita di un singolo SKU e propaga la
modifica ovunque sia baked-in: catalog.json, functions/api/_lib/catalog.js
(fonte autorevole lato server per il checkout — vedi il commento "niente
prezzo/nome/valuta dal client" in functions/api/[[catchall]].js), e ogni
pagina HTML nelle 7 lingue che referenzia lo SKU (prezzo visibile, meta
product:price:amount, JSON-LD offers.price, data-stripe-unit-amount,
percentuale sconto/badge).

Riusa la stessa logica a blocchi di scripts/normalize-commercial-prices.py
(quello script serve a un altro scopo — riallineare il prezzo pubblico alla
policy commerciale quando droga per arrotondamento, non a impostare un nuovo
prezzo — ma le regex di patch sono le stesse). Differenza principale: qui
LANGS copre tutte le 7 lingue del sito (li' ne mancano 2, pt e nl).

Uso:
  python scripts/set-manual-price.py --sku 1108921 --new-minor 795
  python scripts/set-manual-price.py --sku 1108921 --new-minor 795 --apply
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_JSON = ROOT / "catalog.json"
CATALOG_JS = ROOT / "functions" / "api" / "_lib" / "catalog.js"
LANGS = ("it", "en", "fr", "de", "es", "pt", "nl")

CLUSTER_START_RE = re.compile(r'data-stripe-currency="eur"')
SKU_ATTR_RE = re.compile(r'data-stripe-product-sku="([^"]+)"')
UNIT_ATTR_RE = re.compile(r'(data-stripe-unit-amount=")(\d+)(")')
DISCOUNT_ATTR_RE = re.compile(r'(data-discount-percent=")(\d+)(")')
META_PRICE_RE = re.compile(r'(product:price:amount"\s+content=")(\d+\.\d{2})(")')
JSONLD_PRICE_RE = re.compile(r'("price":\s*")(\d+\.\d{2})(")')
EUR_TOKEN_RE = re.compile(r'(€\s?)(\d+(?:\.\d{3})*(?:,\d{2})?)')
BARE_AMOUNT_ATTR_RE = re.compile(r'(aria-label=")(\d+(?:\.\d{3})*(?:,\d{2})?)(")')
BADGE_PCT_RE = re.compile(r'(−)(\d+)(%)')


def parse_eur_minor(value):
    return round(float(value.replace(".", "").replace(",", ".")) * 100)


def format_eur_minor(minor):
    euros, cents = divmod(minor, 100)
    integer = f"{euros:,}".replace(",", ".")
    return f"{integer},{cents:02d}"


def dot_amount(minor):
    return f"{minor // 100}.{minor % 100:02d}"


def discount_percent(sale, compare):
    return round((1 - sale / compare) * 100) if compare > sale else 0


def split_blocks(text):
    starts = list(CLUSTER_START_RE.finditer(text))
    if not starts:
        return [(None, text)]
    if len(starts) == 1:
        sku_match = SKU_ATTR_RE.search(text, starts[0].start())
        return [(sku_match.group(1) if sku_match else None, text)]
    blocks = [(None, text[: starts[0].start()])] if starts[0].start() else []
    for index, start in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        block = text[start.start() : end]
        sku_match = SKU_ATTR_RE.search(block)
        blocks.append((sku_match.group(1) if sku_match else None, block))
    return blocks


def patch_block(sku, block, change):
    if sku != change["sku"]:
        return block
    old, new, compare = change["old"], change["new"], change["compare"]
    old_save, new_save = compare - old, compare - new

    if compare <= new:
        sale_node_re = re.compile(
            r'(<(?:span|p)[^>]*class="[^"]*(?:price-sale|product-card-price|pdp-final__price|sticky-cta__sale)[^"]*"[^>]*>\s*€\s*)'
            r'(\d+(?:\.\d{3})*(?:,\d{2})?)'
        )

        def sale_node_repl(match):
            if parse_eur_minor(match.group(2)) != old:
                return match.group(0)
            return match.group(1) + format_eur_minor(new)

        block = sale_node_re.sub(sale_node_repl, block)
        block = re.sub(
            r'\s*<span class="product-sticky-cta__msrp">[^<]*</span>', "", block
        )
        block = UNIT_ATTR_RE.sub(rf"\g<1>{new}\g<3>", block)
        block = DISCOUNT_ATTR_RE.sub(r"\g<1>0\g<3>", block)
        block = META_PRICE_RE.sub(rf"\g<1>{dot_amount(new)}\g<3>", block)
        block = JSONLD_PRICE_RE.sub(rf"\g<1>{dot_amount(new)}\g<3>", block)
        return block

    replacements = {old: new}
    if old_save > 0 and new_save > 0:
        replacements[old_save] = new_save

    def money_repl(match):
        minor = parse_eur_minor(match.group(2))
        replacement = replacements.get(minor)
        return match.group(0) if replacement is None else match.group(1) + format_eur_minor(replacement)

    def aria_repl(match):
        minor = parse_eur_minor(match.group(2))
        replacement = replacements.get(minor)
        return match.group(0) if replacement is None else match.group(1) + format_eur_minor(replacement) + match.group(3)

    block = EUR_TOKEN_RE.sub(money_repl, block)
    block = BARE_AMOUNT_ATTR_RE.sub(aria_repl, block)
    block = UNIT_ATTR_RE.sub(rf"\g<1>{new}\g<3>", block)
    new_discount = discount_percent(new, compare)
    block = DISCOUNT_ATTR_RE.sub(rf"\g<1>{new_discount}\g<3>", block)
    block = BADGE_PCT_RE.sub(rf"\g<1>{new_discount}\g<3>", block)
    block = META_PRICE_RE.sub(rf"\g<1>{dot_amount(new)}\g<3>", block)
    block = JSONLD_PRICE_RE.sub(rf"\g<1>{dot_amount(new)}\g<3>", block)
    return block


def update_catalog_json(change):
    entries = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    found = False
    for entry in entries:
        if entry["sku"] == change["sku"]:
            entry["unitAmountMinor"] = change["new"]
            found = True
    if not found:
        raise RuntimeError(f"SKU {change['sku']} non trovato in catalog.json")
    CATALOG_JSON.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def update_catalog_js(change):
    text = CATALOG_JS.read_text(encoding="utf-8")
    pattern = re.compile(
        rf'(^\s*{re.escape(json.dumps(change["sku"]))}:\s*\{{[^\n]*?unitAmountMinor:\s*){change["old"]}(,)',
        re.MULTILINE,
    )
    text, count = pattern.subn(rf"\g<1>{change['new']}\g<2>", text, count=1)
    if count != 1:
        raise RuntimeError(f"Impossibile aggiornare {change['sku']} in catalog.js")
    CATALOG_JS.write_text(text, encoding="utf-8")


def update_html(change):
    changed_paths = []
    for lang in LANGS:
        for path in sorted((ROOT / lang).glob("*.html")):
            text = path.read_text(encoding="utf-8")
            if "data-stripe-product-sku" not in text or change["sku"] not in text:
                continue
            patched = "".join(patch_block(sku, block, change) for sku, block in split_blocks(text))
            if patched != text:
                path.write_text(patched, encoding="utf-8")
                changed_paths.append(str(path.relative_to(ROOT)))
    return changed_paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sku", required=True)
    ap.add_argument("--new-minor", type=int, required=True, help="nuovo prezzo in centesimi")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    entries = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    entry = next((e for e in entries if e["sku"] == args.sku), None)
    if entry is None:
        raise SystemExit(f"SKU {args.sku} non trovato in catalog.json")

    old = entry["unitAmountMinor"]
    compare = entry.get("compareAtMinor", 0)
    change = {"sku": args.sku, "old": old, "new": args.new_minor, "compare": compare}

    print(f"{args.sku} ({entry['name']}): {format_eur_minor(old)} € -> {format_eur_minor(args.new_minor)} €"
          f" (confronto listino {format_eur_minor(compare)} €, nuovo sconto {discount_percent(args.new_minor, compare)}%)")

    if not args.apply:
        print("Dry-run: nessun file scritto. Rilancia con --apply.")
        return

    update_catalog_json(change)
    update_catalog_js(change)
    changed_html = update_html(change)
    print(f"catalog.json e catalog.js aggiornati; {len(changed_html)} pagine HTML aggiornate:")
    for p in changed_html:
        print(f"  {p}")


if __name__ == "__main__":
    main()
