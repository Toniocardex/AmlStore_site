#!/usr/bin/env python3
"""Verifica la normalizzazione commerciale dei prezzi pubblici EUR.

1. Pricing function: soglia, arrotondamento, override ed esclusioni.
2. Catalog invariants: importi validi e prezzi EUR >= 50 in euro interi.
3. Frontend/backend parity: per ogni pagina prodotto (single-SKU) e ogni
   product-card (category/home), data-stripe-unit-amount/compare-at-amount,
   meta product:price:amount e JSON-LD price combaciano con catalog.json.
4. Parita dei prezzi fra le cinque lingue.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))
from commercial_pricing import (  # noqa: E402
    CLEAN_INTEGER_PRICE_THRESHOLD_MINOR_EUR,
    format_eur_minor,
    load_policy,
    normalize_commercial_price_minor,
    resolve_public_price_minor,
)

CATALOG = {e["sku"]: e for e in json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))}
POLICY = load_policy()
LANGS = ("it", "en", "fr", "de", "es", "pt", "nl")

CLUSTER_START_RE = re.compile(r'data-stripe-currency="eur"')
SKU_ATTR_RE = re.compile(r'data-stripe-product-sku="([^"]+)"')
UNIT_ATTR_RE = re.compile(r'data-stripe-unit-amount="(\d+)"')
COMPARE_ATTR_RE = re.compile(r'data-stripe-compare-at-amount="(\d+)"')
META_PRICE_RE = re.compile(r'product:price:amount"\s+content="(\d+\.\d{2})"')
JSONLD_PRICE_RE = re.compile(r'"price":\s*"(\d+\.\d{2})"')
VISIBLE_PRICE_RE = re.compile(
    r'class="[^"]*(?:price-sale|product-card-price|sticky-cta__sale|pdp-final__price)[^"]*"'
    # Alcune card (plan-card/m365-card) avvolgono la cifra in uno <span data-plan-price>
    # separato dal simbolo € per poterla aggiornare via JS senza toccare il resto del nodo:
    # il simbolo resta comunque adiacente e visibile, quindi va accettato un tag intermedio.
    r'[^>]*>\s*€\s*(?:<[^>]+>\s*)?([\d.]+(?:,\d{2})?)'
)

errors = []
warnings = []


def check_pricing_function():
    cases = [
        (0, 0),
        (1990, 1990),
        (4999, 4999),
        (5000, 5000),
        (5001, 5100),
        (8137, 8200),
        (14317, 14400),
        (71069, 71100),
        (134827, 134900),
    ]
    for raw, expected in cases:
        got = normalize_commercial_price_minor(raw)
        if got != expected:
            errors.append(f"pricing function: {raw} -> {got}, atteso {expected}")


def check_catalog_invariants():
    for sku, e in CATALOG.items():
        if e["unitAmountMinor"] <= 0:
            errors.append(f"catalog {sku}: unitAmountMinor <= 0")
        if e["currency"] != "EUR":
            errors.append(f"catalog {sku}: currency {e['currency']!r} != EUR")
        if e.get("compareAtMinor", 0) < 0:
            errors.append(f"catalog {sku}: compareAtMinor negativo")
        mode = POLICY.get("products", {}).get(sku, {}).get("mode", "automatic")
        if mode == "manual" and resolve_public_price_minor(e, POLICY) != e["unitAmountMinor"]:
            errors.append(f"catalog {sku}: prezzo diverso dall'override manuale approvato")
        if (
            e["currency"] == "EUR"
            and e["unitAmountMinor"] >= CLEAN_INTEGER_PRICE_THRESHOLD_MINOR_EUR
            and mode != "preserve-cents"
            and e["unitAmountMinor"] % 100
        ):
            errors.append(f"catalog {sku}: prezzo >= 50 EUR con centesimi arbitrari")


def blocks_for_file(text):
    starts = list(CLUSTER_START_RE.finditer(text))
    if not starts:
        return []
    if len(starts) == 1:
        m = SKU_ATTR_RE.search(text, starts[0].start())
        return [(m.group(1), text)] if m else []
    blocks = []
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        block_text = text[m.start() : end]
        sku_m = SKU_ATTR_RE.search(block_text)
        if sku_m:
            blocks.append((sku_m.group(1), block_text))
    return blocks


def check_frontend_backend_parity():
    for lang in LANGS:
        for html_path in sorted((ROOT / lang).glob("*.html")):
            text = html_path.read_text(encoding="utf-8")
            if "data-stripe-product-sku" not in text:
                continue
            rel = html_path.relative_to(ROOT)
            is_pdp = len(SKU_ATTR_RE.findall(text)) == 1
            for sku, block in blocks_for_file(text):
                expected = CATALOG.get(sku)
                if not expected:
                    errors.append(f"{rel}: SKU sconosciuto {sku}")
                    continue
                unit_matches = UNIT_ATTR_RE.findall(block)
                for u in unit_matches:
                    if int(u) != expected["unitAmountMinor"]:
                        errors.append(
                            f"{rel} [{sku}]: data-stripe-unit-amount {u} != catalogo {expected['unitAmountMinor']}"
                        )
                compare_matches = COMPARE_ATTR_RE.findall(block)
                for c in compare_matches:
                    if int(c) != expected["compareAtMinor"]:
                        errors.append(
                            f"{rel} [{sku}]: data-stripe-compare-at-amount {c} != catalogo {expected['compareAtMinor']}"
                        )
                expected_visible = format_eur_minor(expected["unitAmountMinor"])
                visible_prices = VISIBLE_PRICE_RE.findall(block)
                if expected_visible not in visible_prices:
                    errors.append(
                        f"{rel} [{sku}]: prezzo visibile {visible_prices[:5]} non contiene {expected_visible}"
                    )
                if is_pdp:
                    expected_dot = f"{expected['unitAmountMinor'] // 100}.{expected['unitAmountMinor'] % 100:02d}"
                    for m in META_PRICE_RE.finditer(block):
                        if m.group(1) != expected_dot:
                            errors.append(f"{rel} [{sku}]: meta price {m.group(1)} != {expected_dot}")
                    for m in JSONLD_PRICE_RE.finditer(block):
                        if m.group(1) != expected_dot:
                            errors.append(f"{rel} [{sku}]: JSON-LD price {m.group(1)} != {expected_dot}")


def check_locale_parity():
    """Stesso SKU deve avere lo stesso unitAmountMinor in tutte le lingue (I9)."""
    per_lang = {lang: {} for lang in LANGS}
    for lang in LANGS:
        for html_path in sorted((ROOT / lang).glob("*.html")):
            text = html_path.read_text(encoding="utf-8")
            if len(SKU_ATTR_RE.findall(text)) != 1:
                continue
            sku_m = SKU_ATTR_RE.search(text)
            unit_m = UNIT_ATTR_RE.search(text)
            if sku_m and unit_m:
                per_lang[lang][sku_m.group(1)] = int(unit_m.group(1))
    all_skus = set()
    for d in per_lang.values():
        all_skus |= set(d.keys())
    for sku in sorted(all_skus):
        values = {lang: per_lang[lang].get(sku) for lang in LANGS if sku in per_lang[lang]}
        if len(set(values.values())) > 1:
            errors.append(f"locale parity {sku}: valori diversi tra lingue: {values}")


def main():
    check_pricing_function()
    check_catalog_invariants()
    check_frontend_backend_parity()
    check_locale_parity()

    for w in warnings:
        print("WARNING:", w)

    if errors:
        print(f"VALIDATION FAILED: {len(errors)} issue(s)")
        for e in errors[:50]:
            print(" -", e)
        if len(errors) > 50:
            print(f" ... and {len(errors) - 50} more")
        sys.exit(1)
    print("OK: commercial pricing, frontend/backend parity and locale parity passed")


if __name__ == "__main__":
    main()
