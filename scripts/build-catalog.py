#!/usr/bin/env python3
"""Generate functions/api/_lib/catalog.js and catalog.json from a legacy shop CSV export (not used at runtime)."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = Path(r"c:\Users\Anton\Downloads\export-products-complete-25-05-2026_02-37.csv")
OUT_JS = ROOT / "functions" / "api" / "_lib" / "catalog.js"
OUT_JSON = ROOT / "catalog.json"


def eur_to_minor(v):
    if not v or not str(v).strip():
        return 0
    return int(round(float(v) * 100))


def infer_type(name, cat):
    n = (name or "").lower()
    if name.strip().upper().startswith("SC_") or (
        "microsoft 365 personal" in n and "windows 11" in n
    ):
        return "bundle"
    if any(
        x in n
        for x in (
            "12 mesi",
            "1 anno",
            "2 anni",
            "abbonamento",
            "mcafee",
            "kaspersky",
            "norton",
            "bitdefender",
            "eset",
            "acrobat",
            "acronis",
        )
    ) and "office 20" not in n[:20]:
        if "office 202" in n and "home" in n and "business" not in n:
            return "perpetual"
        if "office 202" in n or "project" in n or "visio" in n:
            return "perpetual"
        if "windows" in n or "server" in n or "sql" in n:
            return "perpetual"
        if "guida" in n or "copilot  " in n:
            return "perpetual"
        return "subscription"
    return "perpetual"


def disambiguate_code(code, name, counts):
    code = (code or "").strip()
    if not code:
        return code
    base = code
    if counts.get(base, 0) > 0:
        m = re.search(r"(\d+)\s*Dispositiv", name or "", re.I)
        if m:
            code = f"{base}-{m.group(1)}D"
        else:
            code = f"{base}-v{counts[base] + 1}"
    counts[base] = counts.get(base, 0) + 1
    return code


def load_entries():
    counts = {}
    entries = []
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("state") != "published":
                continue
            name = (row.get("product_name_1") or "").strip()
            if not name:
                continue
            sku = disambiguate_code(row.get("code", "").strip(), name, counts)
            sale = eur_to_minor(row.get("price_1_special") or row.get("price_1"))
            compare = eur_to_minor(row.get("price_1"))
            if sale <= 0:
                continue
            if compare < sale:
                compare = sale
            entries.append(
                {
                    "sku": sku,
                    "name": name,
                    "unitAmountMinor": sale,
                    "compareAtMinor": compare,
                    "currency": "EUR",
                    "type": infer_type(name, row.get("category_1")),
                    "category": (row.get("category_1") or "").strip(),
                }
            )
    return entries


def js_string(s):
    return json.dumps(s, ensure_ascii=False)


def write_js(entries):
    lines = [
        "/**",
        " * catalog.js — listino autoritativo Aml Store.",
        " * Generato da scripts/build-catalog.py — sorgente: export CSV listino legacy (2026-05-25).",
        " * Prezzo vendita = price_1_special; listino barrato = price_1.",
        " */",
        "",
        "/** @typedef {{ name: string, unitAmountMinor: number, compareAtMinor: number, currency: string, type: string, category: string }} CatalogEntry */",
        "",
        "/** @type {Record<string, CatalogEntry>} */",
        "export const CATALOG = {",
    ]
    for e in entries:
        lines.append(
            f"  {js_string(e['sku'])}: {{ name: {js_string(e['name'])}, "
            f"unitAmountMinor: {e['unitAmountMinor']}, compareAtMinor: {e['compareAtMinor']}, "
            f"currency: 'EUR', type: {js_string(e['type'])}, category: {js_string(e['category'])} }},"
        )
    lines.extend(
        [
            "};",
            "",
            "/** @param {string} sku */",
            "export function getCatalogEntry(sku) {",
            '    const key = String(sku || "").trim();',
            "    return key ? CATALOG[key] : null;",
            "}",
            "",
            "/**",
            " * Valida righe carrello: prezzi e nomi solo dal catalogo.",
            " * @param {Array<{sku?: string, quantity?: number}>} rawItems",
            " * @returns {Array<{sku: string, name: string, qty: number, unit_amount_minor: number, currency: string}>}",
            " */",
            "export function resolveAndValidateItems(rawItems) {",
            "    const items = [];",
            "    for (const raw of rawItems || []) {",
            '        const sku = String(raw.sku || "").trim();',
            '        if (!sku) throw new Error("SKU mancante");',
            "        const entry = getCatalogEntry(sku);",
            '        if (!entry) throw new Error(`SKU non nel catalogo: ${sku}`);',
            "        const qty = Math.max(1, Math.min(99, Number(raw.quantity) || 1));",
            "        items.push({",
            "            sku,",
            "            name: entry.name,",
            "            qty,",
            "            unit_amount_minor: entry.unitAmountMinor,",
            "            currency: entry.currency,",
            "        });",
            "    }",
            '    if (items.length === 0) throw new Error("Carrello vuoto");',
            "    return items;",
            "}",
            "",
        ]
    )
    OUT_JS.write_text("\n".join(lines), encoding="utf-8")


def write_json(entries):
    OUT_JSON.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    entries = load_entries()
    write_js(entries)
    write_json(entries)
    print(f"Wrote {len(entries)} SKUs to {OUT_JS} and {OUT_JSON}")


if __name__ == "__main__":
    main()
