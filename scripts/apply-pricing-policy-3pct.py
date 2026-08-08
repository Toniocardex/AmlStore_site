#!/usr/bin/env python3
"""Applica una tantum la nuova pricing policy AML STORE: +3% sul prezzo di vendita.

Vedi docs/adr/pricing-policy-3pct.md (ADR).

Formula (integer minor units, un solo arrotondamento):
    newUnitAmountMinor = floor((oldUnitAmountMinor * 103 + 50) / 100)

compareAtMinor NON riceve il +3% automaticamente: resta invariato, tranne
quando il nuovo prezzo di vendita lo supererebbe o eguaglierebbe in modo
inconsistente (compareAtMinor < newUnitAmountMinor) — in quel caso
compareAtMinor viene allineato a newUnitAmountMinor.

One-shot: la baseline pre-migrazione viene congelata in
scripts/_pricing_policy_pre_migration_snapshot.json al primo avvio. Se il
file esiste gia', lo script si rifiuta di ripartire per evitare un secondo
+3% sugli stessi prezzi (idempotenza / protezione contro doppia esecuzione).

Fonti aggiornate in un solo passaggio, tutte derivate dalla stessa mappa
SKU -> {old,new}:
  - functions/api/_lib/catalog.js  (autorita' backend)
  - catalog.json                   (artifact derivato)
  - it|en|fr|de|es/*.html          (data-stripe-*, prezzi visibili, JSON-LD,
                                     meta product:price:amount, sconto %)

Le pagine categoria/home contengono piu' SKU per file: la sostituzione e'
quindi effettuata per "blocco" (dal cluster data-stripe-* di uno SKU al
successivo), cosi' un valore numerico condiviso da due SKU diversi nello
stesso file non viene mai confuso.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_JS = ROOT / "functions" / "api" / "_lib" / "catalog.js"
CATALOG_JSON = ROOT / "catalog.json"
SNAPSHOT_PATH = ROOT / "scripts" / "_pricing_policy_pre_migration_snapshot.json"
LANGS = ("it", "en", "fr", "de", "es")

ENTRY_RE = re.compile(
    r'^(\s*"(?P<sku>[^"]+)":\s*\{\s*name:\s*"(?P<name>(?:[^"\\]|\\.)*)",\s*'
    r'unitAmountMinor:\s*(?P<unit>\d+),\s*compareAtMinor:\s*(?P<compare>\d+),\s*'
    r"currency:\s*'(?P<currency>[^']+)',\s*type:\s*\"(?P<type>[^\"]*)\",\s*"
    r'category:\s*"(?P<category>(?:[^"\\]|\\.)*)"(?P<physical>,\s*physical:\s*true)?\s*\},)\s*$',
    re.MULTILINE,
)


def apply_pricing_policy_minor(base_minor: int) -> int:
    """+3% markup, un solo arrotondamento al centesimo (integer math)."""
    return (base_minor * 103 + 50) // 100


def eur_from_minor(minor: int) -> str:
    return f"{minor // 100},{minor % 100:02d}"


def eur_dot_from_minor(minor: int) -> str:
    return f"{minor // 100}.{minor % 100:02d}"


def pct_discount(unit_minor: int, compare_minor: int) -> int:
    if compare_minor <= 0 or compare_minor <= unit_minor:
        return 0
    return round((1 - unit_minor / compare_minor) * 100)


# ---------------------------------------------------------------------------
# Step A — snapshot (baseline) + mappa SKU old -> new
# ---------------------------------------------------------------------------

def parse_catalog_js(text):
    entries = {}
    for m in ENTRY_RE.finditer(text):
        entries[m.group("sku")] = {
            "unitAmountMinor": int(m.group("unit")),
            "compareAtMinor": int(m.group("compare")),
        }
    return entries


def build_pricing_map(old_entries):
    pricing = {}
    for sku, e in old_entries.items():
        old_unit = e["unitAmountMinor"]
        old_compare = e["compareAtMinor"]
        new_unit = apply_pricing_policy_minor(old_unit)
        new_compare = old_compare
        compare_adjusted = False
        if new_compare < new_unit:
            new_compare = new_unit
            compare_adjusted = True
        pricing[sku] = {
            "old_unit": old_unit,
            "old_compare": old_compare,
            "new_unit": new_unit,
            "new_compare": new_compare,
            "old_pct": pct_discount(old_unit, old_compare),
            "new_pct": pct_discount(new_unit, new_compare),
            "compare_adjusted": compare_adjusted,
        }
    return pricing


def load_or_create_snapshot():
    if SNAPSHOT_PATH.exists():
        print(f"ERRORE: {SNAPSHOT_PATH.relative_to(ROOT)} esiste gia'.")
        print("La migrazione +3% e' one-shot ed e' gia' stata eseguita.")
        print("Se devi davvero ripeterla su una NUOVA baseline, rimuovi prima")
        print("manualmente lo snapshot (dopo aver verificato che non sia gia'")
        print("stato applicato) — azione consapevole, non automatica.")
        sys.exit(1)

    old_entries = parse_catalog_js(CATALOG_JS.read_text(encoding="utf-8"))
    if not old_entries:
        print("ERRORE: nessuna entry parsata da catalog.js — pattern regex da rivedere.")
        sys.exit(1)

    SNAPSHOT_PATH.write_text(
        json.dumps(
            {
                "_comment": "Baseline pre-migrazione ADR pricing-policy-3pct. Non modificare.",
                "formula": "newUnitAmountMinor = floor((oldUnitAmountMinor * 103 + 50) / 100)",
                "entries": old_entries,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Snapshot baseline scritto: {SNAPSHOT_PATH.relative_to(ROOT)} ({len(old_entries)} SKU)")
    return old_entries


# ---------------------------------------------------------------------------
# Step B — catalog.js
# ---------------------------------------------------------------------------

def update_catalog_js(pricing):
    text = CATALOG_JS.read_text(encoding="utf-8")

    def repl(m):
        sku = m.group("sku")
        p = pricing[sku]
        full = m.group(1)
        full = re.sub(
            r"unitAmountMinor:\s*\d+", f"unitAmountMinor: {p['new_unit']}", full, count=1
        )
        full = re.sub(
            r"compareAtMinor:\s*\d+", f"compareAtMinor: {p['new_compare']}", full, count=1
        )
        return full

    new_text, n = ENTRY_RE.subn(repl, text)
    if n != len(pricing):
        print(f"ATTENZIONE: catalog.js — attese {len(pricing)} entry aggiornate, ottenute {n}")
    CATALOG_JS.write_text(new_text, encoding="utf-8")
    print(f"catalog.js aggiornato ({n} SKU)")


# ---------------------------------------------------------------------------
# Step D — catalog.json (artifact derivato)
# ---------------------------------------------------------------------------

def update_catalog_json(pricing):
    data = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    updated = 0
    for entry in data:
        sku = entry.get("sku")
        if sku in pricing:
            p = pricing[sku]
            entry["unitAmountMinor"] = p["new_unit"]
            entry["compareAtMinor"] = p["new_compare"]
            updated += 1
    CATALOG_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    print(f"catalog.json aggiornato ({updated} SKU)")


# ---------------------------------------------------------------------------
# Step C — frontend HTML (tutte le lingue)
# ---------------------------------------------------------------------------

CLUSTER_START_RE = re.compile(r'data-stripe-currency="eur"')
SKU_ATTR_RE = re.compile(r'data-stripe-product-sku="([^"]+)"')
EUR_TOKEN_RE = re.compile(r"(€\s?)(\d+,\d{2})")
BARE_AMOUNT_ATTR_RE = re.compile(r'(aria-label=")(\d+,\d{2})(")')
UNIT_ATTR_RE = re.compile(r'(data-stripe-unit-amount=")(\d+)(")')
COMPARE_ATTR_RE = re.compile(r'(data-stripe-compare-at-amount=")(\d+)(")')
DISCOUNT_ATTR_RE = re.compile(r'(data-discount-percent=")(\d+)(")')
BADGE_PCT_RE = re.compile(r"(−)(\d+)(%)")
META_PRICE_RE = re.compile(r'(product:price:amount"\s+content=")(\d+\.\d{2})(")')
JSONLD_PRICE_RE = re.compile(r'("price":\s*")(\d+\.\d{2})(")')


def split_blocks(text):
    """Ritorna [(sku_or_None, block_text), ...] coprendo l'intero file.

    Il blocco di ciascuno SKU inizia al cluster data-stripe-currency="eur"
    (che precede sempre unit-amount/compare-at-amount/product-sku nello
    stesso tag) cosi' quegli attributi non finiscono mai nel blocco dello
    SKU precedente. Le pagine PDP con un solo SKU usano l'intero file come
    blocco, cosi' da coprire anche lo sticky-cta che precede il cluster.
    """
    starts = list(CLUSTER_START_RE.finditer(text))
    if not starts:
        return [(None, text)]
    if len(starts) == 1:
        sku_m = SKU_ATTR_RE.search(text, starts[0].start())
        sku = sku_m.group(1) if sku_m else None
        return [(sku, text)]

    blocks = []
    if starts[0].start() > 0:
        blocks.append((None, text[: starts[0].start()]))
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        block_text = text[m.start() : end]
        sku_m = SKU_ATTR_RE.search(block_text)
        sku = sku_m.group(1) if sku_m else None
        blocks.append((sku, block_text))
    return blocks


def patch_block(sku, block, pricing, stats):
    p = pricing.get(sku)
    if not p:
        stats["unknown_sku"].add(sku)
        return block

    value_map = {p["old_unit"]: p["new_unit"]}
    if p["old_compare"] != p["old_unit"]:
        value_map[p["old_compare"]] = p["new_compare"]
    old_savings = p["old_compare"] - p["old_unit"]
    new_savings = p["new_compare"] - p["new_unit"]
    if old_savings > 0:
        value_map[old_savings] = new_savings

    def eur_repl(m):
        prefix, amount_str = m.group(1), m.group(2)
        minor = round(float(amount_str.replace(",", ".")) * 100)
        if minor in value_map:
            stats["eur_subs"] += 1
            return f"{prefix}{eur_from_minor(value_map[minor])}"
        return m.group(0)

    def bare_repl(m):
        prefix, amount_str, suffix = m.group(1), m.group(2), m.group(3)
        minor = round(float(amount_str.replace(",", ".")) * 100)
        if minor in value_map:
            stats["aria_subs"] += 1
            return f"{prefix}{eur_from_minor(value_map[minor])}{suffix}"
        return m.group(0)

    block = EUR_TOKEN_RE.sub(eur_repl, block)
    block = BARE_AMOUNT_ATTR_RE.sub(bare_repl, block)
    block, n = UNIT_ATTR_RE.subn(rf"\g<1>{p['new_unit']}\g<3>", block)
    stats["unit_attr_subs"] += n
    block, n = COMPARE_ATTR_RE.subn(rf"\g<1>{p['new_compare']}\g<3>", block)
    stats["compare_attr_subs"] += n
    block, n = DISCOUNT_ATTR_RE.subn(rf"\g<1>{p['new_pct']}\g<3>", block)
    stats["discount_attr_subs"] += n
    block, n = BADGE_PCT_RE.subn(rf"\g<1>{p['new_pct']}\g<3>", block)
    stats["badge_pct_subs"] += n

    def meta_repl(m):
        stats["meta_subs"] += 1
        return f"{m.group(1)}{eur_dot_from_minor(p['new_unit'])}{m.group(3)}"

    def jsonld_repl(m):
        stats["jsonld_subs"] += 1
        return f"{m.group(1)}{eur_dot_from_minor(p['new_unit'])}{m.group(3)}"

    block = META_PRICE_RE.sub(meta_repl, block)
    block = JSONLD_PRICE_RE.sub(jsonld_repl, block)
    return block


def update_html_files(pricing):
    stats = {
        "eur_subs": 0,
        "aria_subs": 0,
        "unit_attr_subs": 0,
        "compare_attr_subs": 0,
        "discount_attr_subs": 0,
        "badge_pct_subs": 0,
        "meta_subs": 0,
        "jsonld_subs": 0,
        "unknown_sku": set(),
    }
    changed_files = []
    for lang in LANGS:
        for html_path in sorted((ROOT / lang).glob("*.html")):
            text = html_path.read_text(encoding="utf-8")
            if "data-stripe-product-sku" not in text:
                continue
            blocks = split_blocks(text)
            new_parts = []
            touched = False
            for sku, block in blocks:
                if sku is None:
                    new_parts.append(block)
                    continue
                new_block = patch_block(sku, block, pricing, stats)
                if new_block != block:
                    touched = True
                new_parts.append(new_block)
            new_text = "".join(new_parts)
            if new_text != text:
                html_path.write_text(new_text, encoding="utf-8")
                changed_files.append(str(html_path.relative_to(ROOT)))
    return changed_files, stats


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    old_entries = load_or_create_snapshot()
    pricing = build_pricing_map(old_entries)

    update_catalog_js(pricing)
    update_catalog_json(pricing)
    changed_files, stats = update_html_files(pricing)

    report_path = ROOT / "scripts" / "_pricing_policy_migration_report.json"
    report_path.write_text(
        json.dumps(
            {
                "pricing": pricing,
                "changed_html_files": sorted(changed_files),
                "substitution_stats": {k: (sorted(v) if isinstance(v, set) else v) for k, v in stats.items()},
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
        newline="\n",
    )

    print(f"\nHTML aggiornati: {len(changed_files)} file")
    print("Sostituzioni:", {k: v for k, v in stats.items() if k != "unknown_sku"})
    if stats["unknown_sku"]:
        print("SKU trovati in pagina ma assenti dal catalogo:", sorted(stats["unknown_sku"]))
    print(f"\nReport dettagliato: {report_path.relative_to(ROOT)}")
    print("\nNo price received the +3% more than once.")
    print("No psychological rounding was applied.")


if __name__ == "__main__":
    main()
