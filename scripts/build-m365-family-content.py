#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assembla la voce `microsoft-365-family` per PRODUCTS di
product_content_flagship.py a partire dall'estrazione di
extract-m365-family-content.py, e riscrive il file.

Non tocca la voce 'microsoft-365-personal' gia' presente: la ricarica dal
modulo esistente e la riserializza cosi' com'e', aggiungendo solo Family
accanto.

Uso:
    python scripts/build-m365-family-content.py           # scrive il file
    python scripts/build-m365-family-content.py --dry-run # stampa senza scrivere
"""
from __future__ import annotations

import importlib.util
import pprint
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import product_content_flagship as existing  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "extract_family", ROOT / "scripts" / "extract-m365-family-content.py"
)
extract_family = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extract_family)

LANGS = extract_family.LANGS


def by_lang(data: dict, key: str) -> dict:
    return {lang: data[lang][key] for lang in LANGS}


def build_seats(data: dict) -> dict:
    out = {}
    for lang in LANGS:
        d = data[lang]
        entry = {
            "eyebrow": d["seats_eyebrow"],
            "title": d["seats_title"],
            "sub": d["seats_sub"],
            "list_aria": d["seats_list_aria"],
            "foot": d["seats_foot"],
            "rows": d["seats_rows"],
        }
        if d.get("seats_media_src"):
            # Bump-asset-version.py ricalcola sempre l'hash e sostituisce
            # qualsiasi ?v= esistente, ma la convenzione delle altre immagini
            # (vedi _render_lifestyle_band) e' il percorso nudo: lo stesso qui.
            entry["media_src"] = d["seats_media_src"].split("?", 1)[0]
            entry["media_alt"] = d.get("seats_media_alt", "")
        out[lang] = entry
    return out


def build_compare(data: dict) -> dict:
    """
    Toglie la riga di prezzo hardcoded dall'estrazione (era "€ 79,00" /
    "€ 109,00", gia' disallineata dal listino — vedi la sessione precedente
    su questo stesso file) e la rimpiazza con `price_row` + `skus`: a render
    _render_compare la ricalcola dal catalogo, come per Personal.
    """
    out = {}
    for lang in LANGS:
        d = data[lang]
        # Riga 4 (0-indexata) e' sempre il prezzo: struttura HTML fissa,
        # verificata dall'assert in build_entry(). Taglio per indice, non per
        # testo — un match su parole tradotte sarebbe fragile e silenzioso
        # se una lingua avesse una label diversa dalle attese.
        rows = [r for i, r in enumerate(d["compare_rows"]) if i != 4]
        out[lang] = {
            "eyebrow": d["compare_eyebrow"],
            "title": d["compare_title"],
            "sub": d["compare_sub"],
            "caption": d["compare_caption"],
            "cols": d["compare_cols"],
            "rows": rows,
            "yes_label": d["compare_yes_label"],
            "no_label": d["compare_no_label"],
            "price_row": d["compare_rows"][4][0],  # label originale, per lingua
            "skus": ["QQ2-00012", "6GQ-00092"],
            "foot": d["compare_foot"],
        }
    return out


def build_stats(data: dict) -> dict:
    return {
        lang: {
            "eyebrow": data[lang]["stats_eyebrow"],
            "title": data[lang]["stats_title"],
            "sub": data[lang]["stats_sub"],
            "rows": data[lang]["stats_rows"],
        }
        for lang in LANGS
    }


def build_specs_table(data: dict) -> dict:
    return {
        lang: {
            "eyebrow": data[lang]["specs_table_eyebrow"],
            "title": data[lang]["specs_table_title"],
            "caption": data[lang]["specs_table_caption"],
            "rows": data[lang]["specs_table_rows"],
        }
        for lang in LANGS
    }


def build_roles(data: dict) -> dict:
    return {
        lang: {
            "eyebrow": data[lang]["roles_eyebrow"],
            "title": data[lang]["roles_title"],
            "sub": data[lang]["roles_sub"],
            "caption": data[lang]["roles_caption"],
            "cols": data[lang]["roles_cols"],
            "rows": data[lang]["roles_rows"],
            "yes_label": data[lang]["roles_yes_label"],
            "no_label": data[lang]["roles_no_label"],
        }
        for lang in LANGS
    }


def build_entry() -> dict:
    data = {lang: extract_family.extract(lang) for lang in LANGS}

    for lang in LANGS:
        assert len(data[lang]["compare_rows"]) == 6, (
            f"{lang}: attese 6 righe di confronto, il taglio della riga prezzo "
            "sotto assume questa forma"
        )

    return {
        # Come Personal: il badge omaggio compare qui in TUTTE le lingue con
        # un testo proprio (vedi `bonus` sotto), non solo in IT — per questo
        # non riusa copilot_bonus/COPILOT_BONUS_HTML_IT, che e' IT-only.
        "name": by_lang(data, "name"),
        "seo_title": by_lang(data, "seo_title"),
        # Un solo campo `desc` serve sia da <meta description> che da
        # paragrafo sotto l'H1 (stesso schema di Personal). La pagina
        # scritta a mano ne aveva due diversi: si tiene il testo on-page
        # (hero_desc), piu' pertinente per chi legge la scheda; il meta
        # SEO originale non sopravvive come stringa a se stante.
        "desc": by_lang(data, "hero_desc"),
        "eyebrow": by_lang(data, "eyebrow"),
        "title_html": by_lang(data, "title_html"),
        "apps_title": by_lang(data, "apps_title"),
        "apps_sub": by_lang(data, "apps_sub"),
        "apps": data["it"]["apps"],
        "keypoints": by_lang(data, "keypoints"),
        "steps": by_lang(data, "steps"),
        "steps_note": by_lang(data, "steps_note"),
        "specs_note": by_lang(data, "specs_note"),
        "specs": by_lang(data, "specs"),
        "faq": by_lang(data, "faq"),
        # Le 14 FAQ sono ANCHE organizzate in 4 gruppi con titolo nella pagina
        # originale (pdp-faq-group__title) — struttura che _render_faq_columns
        # da solo non rappresenta. `faq` resta la lista piatta (usata per il
        # JSON-LD FAQPage, che non ha bisogno dei gruppi); `faq_groups` guida
        # il rendering visivo quando presente.
        "faq_groups": by_lang(data, "faq_groups"),
        "bonus": by_lang(data, "bonus"),
        "stats": build_stats(data),
        "specs_table": build_specs_table(data),
        "roles": build_roles(data),
        "seats": build_seats(data),
        "compare": build_compare(data),
    }


def main() -> None:
    family_entry = build_entry()

    products = dict(existing.PRODUCTS)
    products["microsoft-365-family"] = family_entry

    header = (
        '"""Contenuti di Microsoft 365 Personal, Microsoft 365 Family e Windows 11 Home.\n'
        "\n"
        "Erano pagine scritte a mano (PRESERVE_PAGES): il contenuto e' stato estratto e\n"
        "portato qui, cosi' seguono il template come tutte le altre schede. Family e'\n"
        "stata portata da scripts/extract-m365-family-content.py +\n"
        "scripts/build-m365-family-content.py, non a mano: per rigenerare la voce dopo\n"
        "un cambio alle pagine sorgente, rieseguire quello script.\n"
        '"""\n\n'
    )
    body = "PRODUCTS = " + pprint.pformat(products, width=110, sort_dicts=False) + "\n"
    # get_flagship_content() e' la sola funzione che il file originale
    # esportava oltre a PRODUCTS (resolve_rich_content() in product_page_lib.py
    # la importa da qui): va riscritta insieme al dict, altrimenti il file
    # perde la sua unica API e ogni pagina agganciata a questo modulo ricade
    # sul template generico compatto senza errori visibili.
    footer = "\n\ndef get_flagship_content(slug):\n    return PRODUCTS.get(slug)\n"
    output = header + body + footer

    if "--dry-run" in sys.argv:
        print(output)
        return

    target = ROOT / "scripts" / "product_content_flagship.py"
    target.write_text(output, encoding="utf-8")
    print(f"scritto {target} — {len(products)} prodotti")


if __name__ == "__main__":
    main()
