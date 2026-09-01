#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia sulle 10 schede ex template compatto e flagship
(10 slug x 7 lingue = 70 file): Adobe Acrobat Pro/Standard, CorelDRAW 2024,
Acronis True Image Advanced, i tre bundle, M365 Personal/Family, Windows 11 Home.

RITIRATO COME GENERATORE: questo script non riscrive piu' le pagine.

Fino a settembre 2026 main() chiamava build_product_page() e sovrascriveva i 70
file. Eseguirlo oggi ne distruggerebbe circa meta': build_product_page() rende
25,2-46,0 KB, i file pubblicati stanno fra 55,0 e 76,0 KB, il confronto e' 70
diff su 70 (nessuna pagina coincide) e il delta e' 29,7-33,3 KB per pagina.
Non e' un bug della libreria: e' la pipeline di post-produzione che manca.
Il perche', e i cinque strati che andrebbero persi, stanno in
scripts/page_pipeline_guard.py.

Questo e' l'elenco con il residuo di contenuto piu' pesante di tutti: oltre alla
pipeline si perderebbero modifiche che vivono solo nell'HTML.

  - microsoft-365-personal e microsoft-365-family (7 lingue ciascuna): un blocco
    FAQPage in JSON-LD che il generatore non produce. Rigenerare cancella dati
    strutturati gia' indicizzati.
  - microsoft-365-family (7 lingue): anche i prezzi nel selettore .pdp-plan e i
    ritocchi al titolo. E' l'unica pagina in PRESERVE_PAGES di generate-wave3.py,
    cioe' quella che il resto della pipeline tratta come scritta a mano; averla
    qui fra i prodotti "rigenerabili" era gia' una contraddizione.
  - acronis-true-image-advanced, adobe-acrobat-pro, adobe-acrobat-standard,
    bundle-m365-personal-kaspersky, bundle-m365-personal-mcafee,
    bundle-windows-11-home-m365-personal (7 lingue ciascuna): il conteggio
    dispositivi aggiunto a mano al "name" del JSON-LD e ai titoli
    (es. "Adobe Acrobat Pro - 2 dispositivi").

I commenti storici sulle singole voci restano nella tabella qui sotto: dicono
perche' ogni pagina era finita nel generatore, ed e' un contesto che serve
ancora a chi tocca il contenuto in product_content_*.py.

Quel che lo script fa ancora, e per cui va tenuto: verifica sulle pagine
pubblicate CTA, SKU e i quattro strati. Senza effetti collaterali, non scrive
nulla.

    python scripts/regen-legacy-rich.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from page_pipeline_guard import fail_if, load, pipeline_errors  # noqa: E402
from product_page_lib import LANGS  # noqa: E402

IMG_OFFICE = "microsoft-365-personal.webp"
IMG_FALLBACK = "product-cover-fallback.webp"

IMG_WIN = "microsoft-windows-11-home.webp"

PRODUCTS = [
    {"sku": "SC_M365P_MTOTPROT_5Device", "slug": "bundle-m365-personal-mcafee", "template": "bundle", "card_name": "M365 Personal + McAfee", "image": IMG_OFFICE},
    {"sku": "SC_M365_KPremium_5Device", "slug": "bundle-m365-personal-kaspersky", "template": "bundle", "card_name": "M365 Personal + Kaspersky", "image": IMG_OFFICE},
    {"sku": "AD_STD_2D-1A", "slug": "adobe-acrobat-standard", "template": "tool", "card_name": "Adobe Acrobat Standard", "image": IMG_FALLBACK, "brand": "Adobe"},
    {"sku": "SC916509", "slug": "adobe-acrobat-pro", "template": "tool", "card_name": "Adobe Acrobat Pro", "image": IMG_FALLBACK, "brand": "Adobe"},
    {"sku": "B0CXZR44LP", "slug": "coreldraw-2024", "template": "tool", "card_name": "CorelDRAW Graphics Suite 2024", "image": IMG_FALLBACK, "brand": "Corel"},
    {"sku": "ACRTRIAD1D1Y", "slug": "acronis-true-image-advanced", "template": "backup", "card_name": "Acronis True Image Advanced", "image": IMG_FALLBACK, "brand": "Acronis"},
    # Gia' sul template rich ma mai agganciata a resolve_rich_content(): l'HTML
    # su disco derivava da una modifica manuale, non dal generatore.
    {"sku": "SC_W11HOME_M365PERS", "slug": "bundle-windows-11-home-m365-personal", "template": "bundle", "card_name": "Windows 11 Home + M365 Personal", "image": IMG_WIN},
    # Riscritta a suo tempo solo per aggiungere il badge omaggio guida Copilot
    # (copilot_bonus), assente nel generatore fino ad allora.
    {"sku": "QQ2-00012", "slug": "microsoft-365-personal", "template": "m365", "card_name": "Microsoft 365 Personal", "image": IMG_OFFICE},
    # Era l'ultima pagina PRESERVE_PAGES fuori dal generatore (port_m365_family_locales.py,
    # poi superseduto): il contenuto e' stato estratto con
    # scripts/extract-m365-family-content.py + scripts/build-m365-family-content.py
    # e vive in product_content_flagship.PRODUCTS['microsoft-365-family'].
    # Resta comunque in PRESERVE_PAGES per generate-wave3.py.
    {"sku": "6GQ-00092", "slug": "microsoft-365-family", "template": "m365", "card_name": "Microsoft 365 Family", "image": "microsoft-365-family.webp"},
    # Ultima pagina rimasta sul layout vecchio: era in PRESERVE_PAGES, ne e'
    # uscita quando il contenuto e' finito in product_content_flagship, ma
    # nessuno script la rigenerava piu' -- l'HTML su disco era ancora quello
    # scritto a mano (eyebrow con trattino, codice sotto il titolo, CTA
    # singola, blocco pagamenti proprio).
    {"sku": "KW9-00642", "slug": "windows-11-home", "template": "windows", "card_name": "Windows 11 Home", "image": IMG_WIN},
]


def main():
    errors = []
    for prod in PRODUCTS:
        slug, sku = prod["slug"], prod["sku"]
        for lang in LANGS:
            html = load(lang, slug)
            if html is None:
                errors.append(f"{lang}/{slug}.html: manca il file")
                continue
            if 'id="product-primary-cta"' not in html:
                errors.append(f"{lang}/{slug}.html: manca la CTA primaria")
            if f'data-stripe-product-sku="{sku}"' not in html:
                errors.append(f"{lang}/{slug}.html: SKU diverso da {sku}")
            errors += pipeline_errors(lang, slug, html)

    fail_if(errors, f"OK: {len(PRODUCTS)} slug legacy/flagship x {len(LANGS)} lingue")


if __name__ == "__main__":
    main()
