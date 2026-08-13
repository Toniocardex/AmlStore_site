#!/usr/bin/env python3
"""Dry-run/apply della normalizzazione commerciale dei prezzi pubblici EUR.

Uso:
  python scripts/normalize-commercial-prices.py
  python scripts/normalize-commercial-prices.py --apply
"""

import argparse
import json
import re
from pathlib import Path

from commercial_pricing import format_eur_minor, load_policy, resolve_public_price_minor

ROOT = Path(__file__).resolve().parents[1]
CATALOG_JSON = ROOT / "catalog.json"
CATALOG_JS = ROOT / "functions" / "api" / "_lib" / "catalog.js"
REPORT_PATH = ROOT / "scripts" / "_commercial_pricing_report.json"
LANGS = ("it", "en", "fr", "de", "es")

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


def dot_amount(minor):
    return f"{minor // 100}.{minor % 100:02d}"


def discount_percent(sale, compare):
    return round((1 - sale / compare) * 100) if compare > sale else 0


def format_signed_eur_minor(minor):
    sign = "+" if minor >= 0 else "-"
    return sign + format_eur_minor(abs(minor))


def make_changes(entries, policy):
    changes = {}
    report = []
    for entry in entries:
        raw = entry["unitAmountMinor"]
        proposed = resolve_public_price_minor(entry, policy)
        product_policy = policy.get("products", {}).get(entry["sku"], {})
        row = {
            "productId": entry["sku"],
            "sku": entry["sku"],
            "name": entry["name"],
            "currentPriceMinor": raw,
            "rawCalculatedPriceMinor": raw,
            "proposedPublicPriceMinor": proposed,
            "deltaAbsoluteMinor": proposed - raw,
            "deltaPercent": round(((proposed - raw) / raw) * 100, 4) if raw else 0,
            "manualOverridePresent": product_policy.get("mode") == "manual",
            "pricingMode": product_policy.get("mode", "automatic"),
        }
        report.append(row)
        if proposed != raw:
            changes[entry["sku"]] = {
                "old": raw,
                "new": proposed,
                "compare": entry.get("compareAtMinor", 0),
            }
    return changes, report


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


def patch_block(sku, block, changes):
    change = changes.get(sku)
    if not change:
        return block
    old, new, compare = change["old"], change["new"], change["compare"]
    old_save, new_save = compare - old, compare - new

    # Se il riferimento esterno non supera piu il prezzo di vendita, non va
    # trasformato ne mostrato come listino barrato. Aggiorna solo i nodi sale.
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


def update_catalog_json(entries, changes):
    for entry in entries:
        if entry["sku"] in changes:
            entry["unitAmountMinor"] = changes[entry["sku"]]["new"]
    CATALOG_JSON.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def update_catalog_js(changes):
    text = CATALOG_JS.read_text(encoding="utf-8")
    for sku, change in changes.items():
        pattern = re.compile(
            rf'(^\s*{re.escape(json.dumps(sku))}:\s*\{{[^\n]*?unitAmountMinor:\s*){change["old"]}(,)',
            re.MULTILINE,
        )
        text, count = pattern.subn(rf"\g<1>{change['new']}\g<2>", text, count=1)
        if count != 1:
            raise RuntimeError(f"Impossibile aggiornare {sku} in catalog.js")
    CATALOG_JS.write_text(text, encoding="utf-8")


def update_html(changes):
    changed_paths = []
    for lang in LANGS:
        for path in sorted((ROOT / lang).glob("*.html")):
            text = path.read_text(encoding="utf-8")
            if "data-stripe-product-sku" not in text:
                continue
            patched = "".join(patch_block(sku, block, changes) for sku, block in split_blocks(text))
            if patched != text:
                path.write_text(patched, encoding="utf-8")
                changed_paths.append(str(path.relative_to(ROOT)))
    return changed_paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="scrive catalogo e pagine")
    args = parser.parse_args()

    entries = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    policy = load_policy()
    changes, report = make_changes(entries, policy)
    payload = {
        "mode": "apply" if args.apply else "dry-run",
        "thresholdEur": 50,
        "changedProducts": len(changes),
        "products": report,
    }
    REPORT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"{'APPLY' if args.apply else 'DRY-RUN'}: {len(changes)} prezzi da aggiornare")
    for row in report:
        if row["deltaAbsoluteMinor"]:
            print(
                f"{row['sku']}: {format_eur_minor(row['currentPriceMinor'])} € -> "
                f"{format_eur_minor(row['proposedPublicPriceMinor'])} € "
                f"({format_signed_eur_minor(row['deltaAbsoluteMinor'])} €, "
                f"{row['deltaPercent']:+.2f}%)"
            )
    print(f"Report: {REPORT_PATH.relative_to(ROOT)}")

    if not args.apply:
        return
    update_catalog_json(entries, changes)
    update_catalog_js(changes)
    changed_html = update_html(changes)
    payload["changedHtmlFiles"] = changed_html
    REPORT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Cataloghi aggiornati; HTML aggiornati: {len(changed_html)}")


if __name__ == "__main__":
    main()
