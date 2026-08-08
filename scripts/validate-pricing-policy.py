#!/usr/bin/env python3
"""Verifica la pricing policy ADR (+3% one-shot) — vedi docs/adr/pricing-policy-3pct.md.

1. Pricing function: casi noti dall'ADR.
2. Catalog invariants: unitAmountMinor > 0, currency EUR, compareAtMinor >= unitAmountMinor.
3. Frontend/backend parity: per ogni pagina prodotto (single-SKU) e ogni
   product-card (category/home), data-stripe-unit-amount/compare-at-amount,
   meta product:price:amount e JSON-LD price combaciano con catalog.json.
4. No stale price: nessuna pagina prodotto mostra ancora il vecchio prezzo
   pre-migrazione per il proprio SKU (snapshot come baseline).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))
import importlib.util

spec = importlib.util.spec_from_file_location(
    "pricing_policy", ROOT / "scripts" / "apply-pricing-policy-3pct.py"
)
pricing_policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pricing_policy)

CATALOG = {e["sku"]: e for e in json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))}
SNAPSHOT_PATH = ROOT / "scripts" / "_pricing_policy_pre_migration_snapshot.json"
LANGS = ("it", "en", "fr", "de", "es")

CLUSTER_START_RE = re.compile(r'data-stripe-currency="eur"')
SKU_ATTR_RE = re.compile(r'data-stripe-product-sku="([^"]+)"')
UNIT_ATTR_RE = re.compile(r'data-stripe-unit-amount="(\d+)"')
COMPARE_ATTR_RE = re.compile(r'data-stripe-compare-at-amount="(\d+)"')
META_PRICE_RE = re.compile(r'product:price:amount"\s+content="(\d+\.\d{2})"')
JSONLD_PRICE_RE = re.compile(r'"price":\s*"(\d+\.\d{2})"')

errors = []
warnings = []


def check_pricing_function():
    cases = [
        (7900, 8137),
        (5900, 6077),
        (13900, 14317),
        (10495, 10810),
        (19989, 20589),
        (34900, 35947),
        (995, 1025),
    ]
    for old, expected in cases:
        got = pricing_policy.apply_pricing_policy_minor(old)
        if got != expected:
            errors.append(f"pricing function: {old} -> {got}, atteso {expected}")


def check_catalog_invariants():
    for sku, e in CATALOG.items():
        if e["unitAmountMinor"] <= 0:
            errors.append(f"catalog {sku}: unitAmountMinor <= 0")
        if e["currency"] != "EUR":
            errors.append(f"catalog {sku}: currency {e['currency']!r} != EUR")
        if "compareAtMinor" in e and e["compareAtMinor"] < e["unitAmountMinor"]:
            errors.append(
                f"catalog {sku}: compareAtMinor {e['compareAtMinor']} < unitAmountMinor {e['unitAmountMinor']}"
            )


def check_no_double_markup():
    if not SNAPSHOT_PATH.exists():
        warnings.append("nessuno snapshot pre-migrazione trovato: skip no-double-markup check")
        return
    snap = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))["entries"]
    for sku, old in snap.items():
        cur = CATALOG.get(sku)
        if not cur:
            warnings.append(f"SKU {sku} presente nello snapshot ma non piu' in catalog.json (rimosso?)")
            continue
        expected_unit = pricing_policy.apply_pricing_policy_minor(old["unitAmountMinor"])
        if cur["unitAmountMinor"] != expected_unit:
            errors.append(
                f"catalog {sku}: unitAmountMinor {cur['unitAmountMinor']} != baseline*1.03 ({expected_unit}) "
                "— possibile doppia applicazione o valore modificato a mano"
            )
        double = pricing_policy.apply_pricing_policy_minor(expected_unit)
        if cur["unitAmountMinor"] == double and double != expected_unit:
            errors.append(f"catalog {sku}: prezzo sembra aver ricevuto il +3% due volte")


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
                if is_pdp:
                    expected_dot = pricing_policy.eur_dot_from_minor(expected["unitAmountMinor"])
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
    check_no_double_markup()
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
    print("OK: pricing policy invariants, frontend/backend parity and locale parity passed")


if __name__ == "__main__":
    main()
