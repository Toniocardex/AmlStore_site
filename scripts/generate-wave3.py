#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Registro dei prodotti del sito, e guardia su schede, cataloghi, sitemap e
_redirects (62 slug x 7 lingue + 6 cataloghi x 7 lingue).

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Fino a settembre 2026 main() chiamava build_product_page() e build_catalog_page()
e sovrascriveva 427 schede + 42 cataloghi, poi appendeva a sitemap.xml e
_redirects. Eseguirlo oggi distruggerebbe circa meta' di ogni scheda e fino a
tre quarti di ogni catalogo:

  - schede:    generato 24,1-60,8 KB, pubblicato 53,9-90,8 KB, 427 diff su 427
  - cataloghi: generato  8,3-46,9 KB, pubblicato 37,9-77,0 KB,  42 diff su 42

Il delta e' quasi costante, ~30 KB per pagina, e non e' un bug della libreria:
e' la pipeline di post-produzione che manca. Il perche', e i cinque strati che
andrebbero persi, stanno in scripts/page_pipeline_guard.py. Oltre alla pipeline
si perderebbero FAQ JSON-LD (microsoft-365-personal), prezzi .pdp-plan
aggiornati a mano (mcafee 5 e 10 dispositivi) e i conteggi dispositivi nei
titoli e nel JSON-LD di 7 slug -- l'elenco completo e' nei docstring di
regen-legacy-rich.py e regen-antivirus-rich.py.

QUESTO MODULO RESTA IL REGISTRO DEI PRODOTTI e va importato: PRODUCTS,
PRESERVE_PAGES e listing_groups() sono usati da regen-catalogs-only.py,
generate-nl-only.py e regen-trustpilot-pdp.py. L'assert di coerenza con
catalog.json gira a import-time, come prima.

Quel che lo script fa ancora, e per cui va tenuto: verifica che ogni scheda e
ogni catalogo esistano con i quattro strati addosso, e che sitemap.xml e
_redirects coprano tutto il registro -- cioe' quello che append_sitemap() e
append_redirects() garantivano scrivendo. Senza effetti collaterali, non scrive
nulla.

    python scripts/generate-wave3.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from page_pipeline_guard import fail_if, load, pipeline_errors  # noqa: E402
from product_page_lib import (  # noqa: E402
    LANGS,
    ROOT as LIB_ROOT,
    TEMPLATE_META,
)

assert LIB_ROOT == ROOT

CATALOG = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
BY_SKU = {e["sku"]: e for e in CATALOG}

# Solo Family resta scritta a mano: ha sezioni su misura (postazioni, tabelle di
# confronto) che il template non genera. Personal e Windows 11 Home sono passate al
# generatore con product_content_flagship.py.
PRESERVE_PAGES = {
    "microsoft-365-family.html",
}

IMG_OFFICE = "microsoft-365-personal.webp"
IMG_WIN = "microsoft-windows-11-home.webp"
IMG_FALLBACK = "product-cover-fallback.webp"

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
    ("79G-05412", "office-2021-home-student", "office", "Office 2021 Home & Student", IMG_OFFICE),
    ("GMGF0D7FX-0002-P", "office-2021-professional-plus", "office", "Office 2021 Professional Plus", IMG_OFFICE),
    ("269-17068", "office-2019-professional-plus", "office", "Office 2019 Professional Plus", IMG_OFFICE),
    # ── Wave 3 — Office / produttività ──
    ("EP2-07219", "word-2024", "office", "Word 2024", IMG_OFFICE),
    ("065-09748", "excel-2024", "office", "Excel 2024", IMG_OFFICE),
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
    ("P73-07788", "windows-server-2019", "server", "Windows Server 2019 Standard", IMG_FALLBACK),
    ("P73-07788_ESD", "windows-server-2019-esd", "server", "Windows Server 2019 Standard ESD", IMG_FALLBACK),
    ("P73-08328", "windows-server-2022", "server", "Windows Server 2022 Standard", IMG_FALLBACK),
    ("EP2-25187", "windows-server-2025", "server", "Windows Server 2025 Standard", IMG_FALLBACK),
    ("P73-08538", "windows-server-2025-dvd", "server", "Windows Server 2025 DVD", IMG_FALLBACK),
    ("P6L-00076", "sql-server-2022-enterprise", "server", "SQL Server 2022 Enterprise", IMG_FALLBACK),
    ("SC835510", "sql-server-2022-standard", "server", "SQL Server 2022 Standard", IMG_FALLBACK),
    # ── Antivirus — ESET ──
    ("EAVH-N1-A1", "eset-nod32-1-device", "antivirus", "ESET NOD32 — 1 dispositivo", IMG_FALLBACK, "ESET"),
    ("EAVH-N1-A2", "eset-nod32-2-devices", "antivirus", "ESET NOD32 — 2 dispositivi", IMG_FALLBACK, "ESET"),
    ("EAVH-N1-A3", "eset-nod32-3-devices", "antivirus", "ESET NOD32 — 3 dispositivi", IMG_FALLBACK, "ESET"),
    ("EAVH-N1-A5", "eset-nod32-5-devices", "antivirus", "ESET NOD32 — 5 dispositivi", IMG_FALLBACK, "ESET"),
    ("EAVH-N1-A10", "eset-nod32-10-devices", "antivirus", "ESET NOD32 — 10 dispositivi", IMG_FALLBACK, "ESET"),
    ("EAVH-N2-A1", "eset-nod32-1-device-2y", "antivirus", "ESET NOD32 — 1 dispositivo · 2 anni", IMG_FALLBACK, "ESET"),
    # ── Norton ──
    ("21395096E7", "norton-360-standard", "antivirus", "Norton 360 Standard", IMG_FALLBACK, "Norton"),
    ("P1433901", "norton-360-standard-no-sub", "antivirus", "Norton 360 Standard (no abbonamento)", IMG_FALLBACK, "Norton"),
    ("NORT_360DEL_3D_1A", "norton-360-deluxe", "antivirus", "Norton 360 Deluxe — 3 dispositivi", IMG_FALLBACK, "Norton"),
    ("NORT_360DEL_3D_1A-NOABB", "norton-360-deluxe-no-sub", "antivirus", "Norton 360 Deluxe (no abbonamento)", IMG_FALLBACK, "Norton"),
    # ── Bitdefender ──
    ("7470A", "bitdefender-plus-1-device", "antivirus", "Bitdefender Plus — 1 dispositivo", IMG_FALLBACK, "Bitdefender"),
    ("TL11012001-EN", "bitdefender-plus-3-devices", "antivirus", "Bitdefender Plus — 3 dispositivi", IMG_FALLBACK, "Bitdefender"),
    ("TL11012001-EN-5D", "bitdefender-plus-5-devices", "antivirus", "Bitdefender Plus — 5 dispositivi", IMG_FALLBACK, "Bitdefender"),
    ("TL11011010-DE", "bitdefender-plus-10-devices", "antivirus", "Bitdefender Plus — 10 dispositivi", IMG_FALLBACK, "Bitdefender"),
    # ── Kaspersky ──
    ("KASP_STD_1D_1A", "kaspersky-standard", "antivirus", "Kaspersky Standard", IMG_FALLBACK, "Kaspersky"),
    ("KASP_PLUS_1D_1A", "kaspersky-plus", "antivirus", "Kaspersky Plus", IMG_FALLBACK, "Kaspersky"),
    ("KL1047TDAFS", "kaspersky-premium-1-device", "antivirus", "Kaspersky Premium — 1 dispositivo", IMG_FALLBACK, "Kaspersky"),
    ("KL1047GDCFS1", "kaspersky-premium-3-devices", "antivirus", "Kaspersky Premium — 3 dispositivi", IMG_FALLBACK, "Kaspersky"),
    ("KL1047GDEFS", "kaspersky-premium-5-devices", "antivirus", "Kaspersky Premium — 5 dispositivi", IMG_FALLBACK, "Kaspersky"),
    ("KL1047GDKFS", "kaspersky-premium-10-devices", "antivirus", "Kaspersky Premium — 10 dispositivi", IMG_FALLBACK, "Kaspersky"),
    # ── McAfee ──
    ("1108921", "mcafee-total-protection-1-device", "antivirus", "McAfee Total Protection — 1 dispositivo", IMG_FALLBACK, "McAfee"),
    ("1108923", "mcafee-total-protection-5-devices", "antivirus", "McAfee Total Protection — 5 dispositivi", IMG_FALLBACK, "McAfee"),
    ("MTP00MNRXRAAD", "mcafee-total-protection-10-devices", "antivirus", "McAfee Total Protection — 10 dispositivi", IMG_FALLBACK, "McAfee"),
    # ── Strumenti / altro ──
    ("AD_STD_2D-1A", "adobe-acrobat-standard", "tool", "Adobe Acrobat Standard", IMG_FALLBACK, "Adobe"),
    ("SC916509", "adobe-acrobat-pro", "tool", "Adobe Acrobat Pro", IMG_FALLBACK, "Adobe"),
    ("B0CXZR44LP", "coreldraw-2024", "tool", "CorelDRAW Graphics Suite 2024", IMG_FALLBACK, "Corel"),
    ("ACRTRIAD1D1Y", "acronis-true-image-advanced", "backup", "Acronis True Image Advanced", IMG_FALLBACK, "Acronis"),
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


def check_sitemap(slugs):
    """Ogni URL del registro deve gia' stare in sitemap.xml.

    Era quello che append_sitemap() otteneva appendendo: se una voce manca, la
    pagina esiste ma nessuno la dichiara ai crawler.
    """
    text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    return [
        f"sitemap.xml: manca https://eurolicenze.com/{lang}/{slug}"
        for lang in LANGS
        for slug in slugs
        if f"https://eurolicenze.com/{lang}/{slug}" not in text
    ]


def check_redirects(products):
    """Ogni vecchio URL WooCommerce deve avere la sua 301.

    Era quello che append_redirects() otteneva appendendo. Le destinazioni sono
    senza estensione (Pages serve *.html agli URL puliti); la variante .html
    conta comunque come coperta. Nessuna regola /it/antivirus -> antivirus.html:
    va in loop con gli URL puliti di Pages.
    """
    text = (ROOT / "_redirects").read_text(encoding="utf-8")
    lines = set(text.rstrip().splitlines())
    errors = []
    for p in products:
        woo = p.get("woo_it")
        if not woo:
            continue
        if (f"{woo} /it/{p['slug']} 301" not in lines
                and f"{woo} /it/{p['slug']}.html 301" not in lines):
            errors.append(f"_redirects: manca la 301 {woo} -> /it/{p['slug']}")
    return errors


def main():
    errors = []
    page_slugs = []
    # Le PRESERVE_PAGES sono scritte a mano, ma la pipeline le attraversa come
    # tutte le altre: vanno controllate anche loro.
    for p in PRODUCTS:
        slug = p["slug"]
        page_slugs.append(slug)
        for lang in LANGS:
            html = load(lang, slug)
            if html is None:
                errors.append(f"{lang}/{slug}.html: manca il file")
                continue
            errors += pipeline_errors(lang, slug, html)

    catalog_slugs = []
    for catalog_slug in listing_groups():
        catalog_slugs.append(catalog_slug)
        for lang in LANGS:
            html = load(lang, catalog_slug)
            if html is None:
                errors.append(f"{lang}/{catalog_slug}.html: manca il catalogo")
                continue
            errors += pipeline_errors(lang, catalog_slug, html)

    errors += check_sitemap(
        page_slugs + [s for s in catalog_slugs if s not in ("sistemi-operativi", "suite-office")]
    )
    errors += check_redirects(PRODUCTS)

    fail_if(errors, f"OK: {len(PRODUCTS)} schede + {len(catalog_slugs)} cataloghi "
                    f"x {len(LANGS)} lingue, sitemap e _redirects allineati")


if __name__ == "__main__":
    main()
