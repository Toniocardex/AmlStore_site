#!/usr/bin/env python3
"""Generate remaining product pages, rebuild catalog pages, sitemap and redirects."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from product_page_lib import (  # noqa: E402
    BASE_LABELS,
    LANGS,
    ROOT as LIB_ROOT,
    TEMPLATE_META,
    build_catalog_page,
    build_product_page,
    entry,
)

assert LIB_ROOT == ROOT

CATALOG = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
BY_SKU = {e["sku"]: e for e in CATALOG}

PRESERVE_PAGES = {
    "microsoft-365-family.html",
    "microsoft-365-personal.html",
    "windows-11-home.html",
}

IMG_OFFICE = "microsoft-365-personal.webp"
IMG_WIN = "microsoft-windows-11-home.webp"

# slug, template, card_name, image (optional), brand (optional), woo_it (optional)
PRODUCT_DEFS = [
    # ── Already live (rich pages preserved; included for catalog rebuild) ──
    ("QQ2-00012", "microsoft-365-personal", "m365", "Microsoft 365 Personal", IMG_OFFICE),
    ("6GQ-00092", "microsoft-365-family", "m365", "Microsoft 365 Family", "microsoft-365-family.webp"),
    ("KW9-00642", "windows-11-home", "windows", "Windows 11 Home", IMG_WIN),
    ("FQC-10528", "windows-11-pro", "windows", "Windows 11 Pro", IMG_WIN),
    ("KW9-00136", "windows-10-home", "windows", "Windows 10 Home", IMG_WIN),
    ("FQC-08930", "windows-10-pro", "windows", "Windows 10 Pro", IMG_WIN),
    ("SC_W11HOME_M365PERS", "bundle-windows-11-home-m365-personal", "bundle", "Windows 11 Home + M365 Personal", IMG_WIN),
    ("SC_M365P_MTOTPROT_5Device", "bundle-m365-personal-mcafee", "bundle", "M365 Personal + McAfee", IMG_OFFICE),
    ("SC_M365_KPremium_5Device", "bundle-m365-personal-kaspersky", "bundle", "M365 Personal + Kaspersky", IMG_OFFICE),
    ("KLQ-00388", "microsoft-365-business-standard", "m365", "Microsoft 365 Business Standard", IMG_OFFICE),
    ("EP2-06798", "office-2024-home", "office", "Office 2024 Home", IMG_OFFICE),
    ("SC871349", "office-2024-standard", "office", "Office 2024 Standard", IMG_OFFICE),
    ("79G-05412", "office-2021-home-student", "office", "Office 2021 Home & Student", IMG_OFFICE),
    ("GMGF0D7FX-0002-P", "office-2021-professional-plus", "office", "Office 2021 Professional Plus", IMG_OFFICE),
    ("269-17068", "office-2019-professional-plus", "office", "Office 2019 Professional Plus", IMG_OFFICE),
    # ── Wave 3 — Office / produttività ──
    ("EP2-07219", "word-2024", "office", "Word 2024", IMG_OFFICE),
    ("MPN: 065-09748", "excel-2024", "office", "Excel 2024", IMG_OFFICE),
    ("065-09804", "powerpoint-2024", "office", "PowerPoint 2024", IMG_OFFICE),
    ("5W1-04285", "outlook-2024", "office", "Outlook 2024", IMG_OFFICE),
    ("EP2-06606", "office-2024-home-business", "office", "Office 2024 Home & Business", IMG_OFFICE),
    ("T5D-03485", "office-2021-home-business", "office", "Office 2021 Home & Business", IMG_OFFICE),
    ("T5D-03489", "office-2021-home-business-mac", "office", "Office 2021 Home & Business Mac", IMG_OFFICE),
    ("79G-05018", "office-2019-home-student", "office", "Office 2019 Home & Student", IMG_OFFICE),
    ("DG7GMGF0PN44", "project-standard-2024", "office", "Project Standard 2024", IMG_OFFICE),
    ("EP2-07001", "project-professional-2024", "office", "Project Professional 2024", IMG_OFFICE),
    ("EP2-07167", "visio-standard-2024", "office", "Visio Standard 2024", IMG_OFFICE),
    ("EP2-07110", "visio-professional-2024", "office", "Visio Professional 2024", IMG_OFFICE),
    # ── Windows extra ──
    ("FQC-10538", "windows-11-pro-oem-dvd", "windows", "Windows 11 Pro OEM DVD", IMG_WIN),
    ("W11_PRO_STICKER", "windows-11-pro-coa", "windows", "Windows 11 Pro COA", IMG_WIN),
    # ── Server / SQL ──
    ("P73-07788", "windows-server-2019", "server", "Windows Server 2019 Standard", IMG_WIN),
    ("P73-07788_ESD", "windows-server-2019-esd", "server", "Windows Server 2019 Standard ESD", IMG_WIN),
    ("P73-08328", "windows-server-2022", "server", "Windows Server 2022 Standard", IMG_WIN),
    ("EP2-25187", "windows-server-2025", "server", "Windows Server 2025 Standard", IMG_WIN),
    ("P73-08538", "windows-server-2025-dvd", "server", "Windows Server 2025 DVD", IMG_WIN),
    ("P6L-00076", "sql-server-2022-enterprise", "server", "SQL Server 2022 Enterprise", IMG_WIN),
    ("SC835510", "sql-server-2022-standard", "server", "SQL Server 2022 Standard", IMG_WIN),
    # ── Antivirus — ESET ──
    ("EAVH-N1-A1", "eset-nod32-1-device", "antivirus", "ESET NOD32 — 1 dispositivo", IMG_OFFICE, "ESET"),
    ("EAVH-N1-A2", "eset-nod32-2-devices", "antivirus", "ESET NOD32 — 2 dispositivi", IMG_OFFICE, "ESET"),
    ("EAVH-N1-A3", "eset-nod32-3-devices", "antivirus", "ESET NOD32 — 3 dispositivi", IMG_OFFICE, "ESET"),
    ("EAVH-N1-A5", "eset-nod32-5-devices", "antivirus", "ESET NOD32 — 5 dispositivi", IMG_OFFICE, "ESET"),
    ("EAVH-N1-A10", "eset-nod32-10-devices", "antivirus", "ESET NOD32 — 10 dispositivi", IMG_OFFICE, "ESET"),
    ("EAVH-N2-A1", "eset-nod32-1-device-2y", "antivirus", "ESET NOD32 — 1 dispositivo · 2 anni", IMG_OFFICE, "ESET"),
    # ── Norton ──
    ("21395096E7", "norton-360-standard", "antivirus", "Norton 360 Standard", IMG_OFFICE, "Norton"),
    ("P1433901", "norton-360-standard-no-sub", "antivirus", "Norton 360 Standard (no abbonamento)", IMG_OFFICE, "Norton"),
    ("NORT_360DEL_3D_1A", "norton-360-deluxe", "antivirus", "Norton 360 Deluxe — 3 dispositivi", IMG_OFFICE, "Norton"),
    ("NORT_360DEL_3D_1A-NOABB", "norton-360-deluxe-no-sub", "antivirus", "Norton 360 Deluxe (no abbonamento)", IMG_OFFICE, "Norton"),
    # ── Bitdefender ──
    ("7470A", "bitdefender-plus-1-device", "antivirus", "Bitdefender Plus — 1 dispositivo", IMG_OFFICE, "Bitdefender"),
    ("TL11012001-EN", "bitdefender-plus-3-devices", "antivirus", "Bitdefender Plus — 3 dispositivi", IMG_OFFICE, "Bitdefender"),
    ("TL11012001-EN-5D", "bitdefender-plus-5-devices", "antivirus", "Bitdefender Plus — 5 dispositivi", IMG_OFFICE, "Bitdefender"),
    ("TL11011010-DE", "bitdefender-plus-10-devices", "antivirus", "Bitdefender Plus — 10 dispositivi", IMG_OFFICE, "Bitdefender"),
    # ── Kaspersky ──
    ("KASP_STD_1D_1A", "kaspersky-standard", "antivirus", "Kaspersky Standard", IMG_OFFICE, "Kaspersky"),
    ("KASP_PLUS_1D_1A", "kaspersky-plus", "antivirus", "Kaspersky Plus", IMG_OFFICE, "Kaspersky"),
    ("KL1047TDAFS", "kaspersky-premium-1-device", "antivirus", "Kaspersky Premium — 1 dispositivo", IMG_OFFICE, "Kaspersky"),
    ("KL1047GDCFS1", "kaspersky-premium-3-devices", "antivirus", "Kaspersky Premium — 3 dispositivi", IMG_OFFICE, "Kaspersky"),
    ("KL1047GDEFS", "kaspersky-premium-5-devices", "antivirus", "Kaspersky Premium — 5 dispositivi", IMG_OFFICE, "Kaspersky"),
    ("KL1047GDKFS", "kaspersky-premium-10-devices", "antivirus", "Kaspersky Premium — 10 dispositivi", IMG_OFFICE, "Kaspersky"),
    # ── McAfee ──
    ("1108921", "mcafee-total-protection-1-device", "antivirus", "McAfee Total Protection — 1 dispositivo", IMG_OFFICE, "McAfee"),
    ("1108923", "mcafee-total-protection-5-devices", "antivirus", "McAfee Total Protection — 5 dispositivi", IMG_OFFICE, "McAfee"),
    ("MTP00MNRXRAAD", "mcafee-total-protection-10-devices", "antivirus", "McAfee Total Protection — 10 dispositivi", IMG_OFFICE, "McAfee"),
    # ── Strumenti / altro ──
    ("AD_STD_2D-1A", "adobe-acrobat-standard", "tool", "Adobe Acrobat Standard", IMG_OFFICE, "Adobe"),
    ("SC916509", "adobe-acrobat-pro", "tool", "Adobe Acrobat Pro", IMG_OFFICE, "Adobe"),
    ("B0CXZR44LP", "coreldraw-2024", "tool", "CorelDRAW Graphics Suite 2024", IMG_OFFICE, "Corel"),
    ("ACRTRIAD1D1Y", "acronis-true-image-advanced", "backup", "Acronis True Image Advanced", IMG_OFFICE, "Acronis"),
    ("SC484126", "copilot-guide-2026", "training", "Guida Copilot Premium 2026", IMG_OFFICE),
]

WOO_REDIRECTS = {
    "EP2-07219": "/it/office-suite/microsoft-word-2024-standalone",
    "EP2-06606": "/it/office-suite/microsoft-office-2024-home-business-windows-o-mac",
    "T5D-03485": "/it/office-suite/microsoft-office-2021-home-business-windows-o-mac",
    "T5D-03489": "/it/office-suite/microsoft-office-2021-home-business-mac",
    "79G-05018": "/it/office-suite/microsoft-office-2019-home-student",
    "DG7GMGF0PN44": "/it/office-suite/microsoft-project-standard-2024-windows",
    "EP2-07001": "/it/office-suite/microsoft-project-professional-2024",
    "EP2-07110": "/it/office-suite/microsoft-visio-professional-2024",
    "EP2-07167": "/it/office-suite/microsoft-visio-standard-2024",
    "21395096E7": "/it/antivirus/norton-360-standard",
    "7470A": "/it/antivirus/bitdefender-antivirus-plus",
    "KASP_STD_1D_1A": "/it/antivirus/kaspersky-standard",
    "1108921": "/it/antivirus/mcafee-total-protection",
}


def parse_def(row):
    sku, slug, template, card_name, image = row[:5]
    brand = row[5] if len(row) > 5 else None
    if sku not in BY_SKU:
        raise KeyError(f"SKU missing from catalog.json: {sku}")
    prod = {
        "sku": sku,
        "slug": slug,
        "template": template,
        "card_name": card_name,
        "image": image,
    }
    if brand:
        prod["brand"] = brand
    woo = WOO_REDIRECTS.get(sku)
    if woo:
        prod["woo_it"] = woo
    return prod


PRODUCTS = [parse_def(r) for r in PRODUCT_DEFS]
assert len(PRODUCTS) == len(BY_SKU), f"{len(PRODUCTS)} defs vs {len(BY_SKU)} catalog SKUs"


def listing_groups():
    groups = {}
    for p in PRODUCTS:
        listing = TEMPLATE_META[p["template"]]["listing"]
        groups.setdefault(listing, []).append(p)
    return groups


def append_sitemap(slugs):
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    inserts = []
    for lang in LANGS:
        for slug in slugs:
            url = f"https://aml-store.com/{lang}/{slug}.html"
            if url in text:
                continue
            inserts.append(
                f'  <url><loc>{url}</loc><changefreq>weekly</changefreq><priority>0.85</priority></url>'
            )
    if inserts:
        text = text.replace("</urlset>", "\n".join(inserts) + "\n</urlset>")
        path.write_text(text, encoding="utf-8")
    print("sitemap +", len(inserts))


def append_redirects(products):
    path = ROOT / "_redirects"
    lines = path.read_text(encoding="utf-8").rstrip().splitlines()
    existing = set(lines)
    added = 0
    extra = [
        ("/it/antivirus", "/it/antivirus.html"),
        ("/it/sistema-operativo", "/it/sistemi-operativi.html"),
    ]
    for p in products:
        woo = p.get("woo_it")
        if woo:
            rule = f"{woo} /it/{p['slug']}.html 301"
            if rule not in existing:
                lines.append(rule)
                existing.add(rule)
                added += 1
    for src, dest in extra:
        rule = f"{src} {dest} 301"
        if rule not in existing:
            lines.append(rule)
            existing.add(rule)
            added += 1
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("redirects +", added)


def main():
    new_slugs = []
    for p in PRODUCTS:
        out = ROOT / "it" / f"{p['slug']}.html"
        if out.name in PRESERVE_PAGES:
            continue
        for lang in LANGS:
            target = ROOT / lang / f"{p['slug']}.html"
            target.write_text(build_product_page(lang, p), encoding="utf-8")
        new_slugs.append(p["slug"])
        print("page", p["slug"])

    groups = listing_groups()
    catalog_slugs = []
    for catalog_slug, items in groups.items():
        catalog_slugs.append(catalog_slug)
        for lang in LANGS:
            path = ROOT / lang / f"{catalog_slug}.html"
            path.write_text(build_catalog_page(lang, catalog_slug, items), encoding="utf-8")
        print("catalog", catalog_slug, len(items), "items")

    append_sitemap(new_slugs + [s for s in catalog_slugs if s not in ("sistemi-operativi", "suite-office")])
    append_redirects(PRODUCTS)


if __name__ == "__main__":
    main()
