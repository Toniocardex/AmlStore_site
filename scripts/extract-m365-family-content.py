#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estrae il contenuto di M365 Family dalle 5 pagine scritte a mano ed emette
la voce `microsoft-365-family` per PRODUCTS di product_content_flagship.py.

Perche' uno script e non copia-incolla: sono ~150 stringhe su 5 lingue. A mano
sarebbe stato un lavoro lungo e con errori silenziosi; qui il confronto fra i
conteggi delle lingue e' automatico e una discrepanza si vede subito.

Uso:
    python scripts/extract-m365-family-content.py            # stampa il dict
    python scripts/extract-m365-family-content.py --check    # solo conteggi
"""
from __future__ import annotations

import html as html_module
import pprint
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_content_office import ICON  # noqa: E402

LANGS = ("it", "en", "fr", "de", "es")
SLUG = "microsoft-365-family"

ICON_TO_KEY = {v: k for k, v in ICON.items()}


def _clean(s: str) -> str:
    """Normalizza gli spazi mantenendo il markup inline (strong, a, em...)."""
    return re.sub(r"\s+", " ", s).strip()


def _one(pattern: str, text: str, flags=re.S) -> str | None:
    m = re.search(pattern, text, flags)
    return _clean(m.group(1)) if m else None


def _all(pattern: str, text: str, flags=re.S) -> list[str]:
    return [_clean(m) for m in re.findall(pattern, text, flags)]


def _faq_pairs(scope: str) -> list[tuple[str, str | list[str]]]:
    """
    (domanda, risposta) da un blocco di .home-faq-item. La risposta e' una
    stringa se il body ha un solo <p>, altrimenti una lista di paragrafi —
    _render_faq() in product_page_lib.py sa gestire entrambe le forme (vedi
    il commento li': senza questo, una risposta a piu' paragrafi finiva
    innestata in un <p> solo, HTML non valido).
    """
    pairs = []
    for q, body in re.findall(
        r'<details class="home-faq-item">\s*<summary>(.*?)</summary>\s*'
        r'<div class="home-faq-body">(.*?)</div>',
        scope,
        re.S,
    ):
        paragraphs = _all(r"<p>(.*?)</p>", body)
        answer = paragraphs[0] if len(paragraphs) == 1 else paragraphs
        pairs.append((html_module.unescape(_clean(q)), answer))
    return pairs


def extract(lang: str) -> dict:
    path = ROOT / lang / f"{SLUG}.html"
    text = path.read_text(encoding="utf-8")
    out = {}

    out["seo_title"] = html_module.unescape(_one(r"<title>(.*?)</title>", text) or "")
    out["desc"] = html_module.unescape(
        _one(r'<meta name="description" content="(.*?)">', text) or ""
    )
    out["eyebrow"] = _one(r'<p class="pdp-eyebrow">(.*?)</p>', text)
    out["title_html"] = _one(r'<h1 class="pdp-h1[^"]*">(.*?)</h1>', text)
    # Nome piano: il titolo senza markup.
    out["name"] = _clean(re.sub(r"<[^>]+>", " ", out["title_html"] or ""))
    out["hero_desc"] = _one(r'<p class="v2-hero__desc">(.*?)</p>', text)
    bonus = _one(r'<p class="pdp-bonus">(.*?)</p>', text)
    out["bonus"] = _one(r"<span>(.*?)</span>", bonus) if bonus else None

    keylist = _one(r'<ul class="pdp-keylist">(.*?)</ul>', text) or ""
    out["keypoints"] = _all(r"<li>(.*?)</li>", keylist)

    out["steps"] = [
        (_clean(t), _clean(b))
        for t, b in re.findall(
            r'<li class="pdp-step">.*?<h3>(.*?)</h3>\s*<p>(.*?)</p>', text, re.S
        )
    ]
    steps_sec = _one(
        r'(<section class="pdp-sec" aria-labelledby="pdp-steps-title">.*?</section>)', text
    ) or ""
    out["steps_note"] = _one(r'<p class="pdp-note">.*?<span>(.*?)</span>', steps_sec)

    # "Compatibilita' e requisiti tecnici" — il generatore ha gia' questa
    # sezione (eyebrow/titolo vengono dai default UI, che per il caso
    # italiano coincidono gia' con quelli della pagina Family): serve solo
    # il sub e le 4 celle sommario/corpo, stessa forma delle FAQ.
    specs_sec = _one(
        r'(<section class="pdp-sec pdp-sec--tight pdp-acc home-faq" aria-labelledby="pdp-specs-title">.*?</section>)',
        text,
    ) or ""
    out["specs_note"] = _one(r'<p class="pdp-sec__sub">(.*?)</p>', specs_sec)
    out["specs"] = _faq_pairs(specs_sec)

    # Scope alla sezione FAQ vera: la pagina ha un secondo blocco
    # ".home-faq-item" dentro "Compatibilita' e requisiti tecnici" (estratto
    # sopra come `specs`), e senza questo taglio i suoi 4 elementi finivano
    # mescolati nell'elenco FAQ (18 invece di 14 — preso da un conteggio
    # errato durante lo sviluppo dello script, non dalla pagina).
    faq_sec = _one(
        r'(<section id="faq" class="pdp-sec home-faq" aria-labelledby="pdp-faq-title">.*?</section>)',
        text,
    ) or ""
    out["faq"] = _faq_pairs(faq_sec)  # forma piatta, tenuta per il conteggio/confronto

    # Le 14 FAQ sono organizzate in 4 gruppi con titolo (.pdp-faq-group /
    # .pdp-faq-group__title) — struttura assente dal generatore, che ha solo
    # una lista piatta. Senza questa estrazione i titoli di gruppo sparivano
    # silenziosamente: la struttura piatta contiene comunque tutte le 14
    # coppie domanda/risposta, ma non piu' l'organizzazione per argomento.
    out["faq_group_titles"] = _all(r'<h3 class="pdp-faq-group__title">(.*?)</h3>', faq_sec)
    out["faq_groups"] = [
        (_clean(title), _faq_pairs(group_html))
        for title, group_html in re.findall(
            r'<div class="pdp-faq-group">\s*<h3 class="pdp-faq-group__title">(.*?)</h3>(.*?)</div>\s*</div>',
            faq_sec,
            re.S,
        )
    ]

    icons = re.findall(r'<li class="pdp-app">\s*<img src="[^"]*?/([^"/]+?)(?:\?[^"]*)?"', text)
    out["apps"] = [ICON_TO_KEY[i] for i in icons if i in ICON_TO_KEY]
    apps_sec = _one(
        r'(<section class="pdp-sec" aria-labelledby="pdp-apps-title">.*?</section>)', text
    ) or ""
    out["apps_eyebrow"] = _one(r'<p class="pdp-sec__eyebrow">(.*?)</p>', apps_sec)
    out["apps_title"] = _one(r'<h2 id="pdp-apps-title"[^>]*>(.*?)</h2>', apps_sec)
    out["apps_sub"] = _one(r'<p class="pdp-sec__sub">(.*?)</p>', apps_sec)

    # ── "Cosa ricevi" — 4 stat card ──
    what_sec = _one(
        r'(<section class="pdp-sec" aria-labelledby="pdp-what-title">.*?</section>)', text
    ) or ""
    out["stats_eyebrow"] = _one(r'<p class="pdp-sec__eyebrow">(.*?)</p>', what_sec)
    out["stats_title"] = _one(r'<h2 id="pdp-what-title"[^>]*>(.*?)</h2>', what_sec)
    out["stats_sub"] = _one(r'<p class="pdp-sec__sub">(.*?)</p>', what_sec)
    out["stats_rows"] = [
        (_clean(v), _clean(l), _clean(n))
        for v, l, n in re.findall(
            r'<span class="pdp-stat__value">(.*?)</span>\s*'
            r'<span class="pdp-stat__label">(.*?)</span>\s*'
            r'<span class="pdp-stat__note">(.*?)</span>',
            what_sec,
            re.S,
        )
    ]

    # ── "Scheda tecnica" — tabella chiave/valore libera ──
    specs2_sec = _one(
        r'(<section class="pdp-sec pdp-sec--tight" aria-labelledby="pdp-specs2-title">.*?</section>)',
        text,
    ) or ""
    out["specs_table_eyebrow"] = _one(r'<p class="pdp-sec__eyebrow">(.*?)</p>', specs2_sec)
    out["specs_table_title"] = _one(r'<h2 id="pdp-specs2-title"[^>]*>(.*?)</h2>', specs2_sec)
    out["specs_table_caption"] = _one(r'<caption class="visually-hidden">(.*?)</caption>', specs2_sec)
    sku_placeholder = re.compile(r"^[A-Z0-9]{2,3}[A-Z0-9-]{4,}$")
    kv_rows = []
    for k, v in re.findall(
        r'<tr><th scope="row">(.*?)</th><td>(.*?)</td></tr>', specs2_sec, re.S
    ):
        v = _clean(v)
        # Il codice prodotto viene sostituito con un segnaposto: a render
        # arriva dal catalogo (vedi _render_specs_table), non resta un
        # literal che puo' disallinearsi dallo SKU vero.
        if sku_placeholder.match(v):
            v = "@sku"
        kv_rows.append((_clean(k), v))
    out["specs_table_rows"] = kv_rows

    # ── "Titolare vs Membri" — tabella a 3 colonne con hint/flag ──
    roles_sec = _one(
        r'(<section class="pdp-sec" aria-labelledby="pdp-roles-title">.*?</section>)', text
    ) or ""
    out["roles_eyebrow"] = _one(r'<p class="pdp-sec__eyebrow">(.*?)</p>', roles_sec)
    out["roles_title"] = _one(r'<h2 id="pdp-roles-title"[^>]*>(.*?)</h2>', roles_sec)
    out["roles_sub"] = _one(r'<p class="pdp-sec__sub">(.*?)</p>', roles_sec)
    out["roles_caption"] = _one(r'<caption class="visually-hidden">(.*?)</caption>', roles_sec)
    out["roles_cols"] = _all(r'<th scope="col">(.*?)</th>', roles_sec)
    out["roles_yes_label"] = _one(r'class="pdp-yes" aria-label="(.*?)"', roles_sec)
    out["roles_no_label"] = _one(r'class="pdp-no" aria-label="(.*?)"', roles_sec)

    def role_cell(v: str) -> str:
        v = _clean(v)
        if "pdp-yes" in v:
            return "yes"
        if "pdp-no" in v:
            return "no"
        return re.sub(r"<[^>]+>", "", v).strip()

    roles_rows = []
    tbody = _one(r"<tbody>(.*?)</tbody>", roles_sec) or roles_sec
    for tr_class, row_html in re.findall(
        r'<tr( class="pdp-row--flag")?>(.*?)</tr>', tbody, re.S
    ):
        flagged = bool(tr_class)
        m = re.search(r'<th scope="row">(.*?)</th>\s*(.*)', row_html, re.S)
        if not m:
            continue
        th_html, rest = m.groups()
        hint = _one(r'<span class="pdp-table__hint">(.*?)</span>', th_html)
        label = _clean(re.sub(r'<span class="pdp-table__hint">.*?</span>', "", th_html, flags=re.S))
        values = [role_cell(v) for v in re.findall(r"<td>(.*?)</td>", rest, re.S)]
        if values:
            roles_rows.append((label, hint, flagged, *values))
    out["roles_rows"] = roles_rows

    seats_sec = _one(
        r'(<section class="pdp-sec" aria-labelledby="pdp-share-title">.*?</section>)', text
    ) or ""
    out["seats_eyebrow"] = _one(r'<p class="pdp-sec__eyebrow">(.*?)</p>', seats_sec)
    out["seats_title"] = _one(r'<h2 id="pdp-share-title"[^>]*>(.*?)</h2>', seats_sec)
    out["seats_sub"] = _one(r'<p class="pdp-sec__sub"[^>]*>(.*?)</p>', seats_sec)
    out["seats_list_aria"] = _one(r'<ul class="pdp-seats" aria-label="(.*?)">', seats_sec)
    out["seats_foot"] = _one(r'<p class="pdp-seats__foot">(.*?)</p>', seats_sec)
    out["seats_media_src"] = _one(r'<figure class="pdp-split__media">\s*<img\s+src="(.*?)"', seats_sec)
    out["seats_media_alt"] = html_module.unescape(
        _one(r'<img\s+src="[^"]*"[^>]*\balt="(.*?)"', seats_sec) or ""
    )

    seats = re.findall(
        r'<li class="pdp-seat([^"]*)">.*?'
        r'<span class="pdp-seat__role">(.*?)</span>\s*'
        r'<span class="pdp-seat__quota">(.*?)</span>',
        seats_sec,
        re.S,
    )
    out["seats_rows"] = [
        (_clean(role), _clean(quota), "owner" in cls) for cls, role, quota in seats
    ]

    # Solo la sezione di confronto: la pagina ha piu' tabelle (requisiti di
    # sistema fra le altre) e senza questo taglio le righe si mescolavano.
    cmp_sec = _one(
        r'(<section class="pdp-sec" aria-labelledby="pdp-compare-title".*?</section>)', text
    ) or ""

    rows = re.findall(
        r"<tr>\s*<th scope=\"row\">(.*?)</th>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>",
        cmp_sec,
        re.S,
    )
    def cellify(v: str) -> str:
        v = _clean(v)
        if "pdp-yes" in v:
            return "yes"
        if "pdp-no" in v:
            return "no"
        return re.sub(r"<[^>]+>", "", v).strip()

    out["compare_rows"] = [
        (_clean(re.sub(r"<[^>]+>", "", a)), cellify(b), cellify(c)) for a, b, c in rows
    ]
    out["compare_cols"] = [
        c for c in _all(r'<th scope="col">(.*?)</th>', cmp_sec) if c and c != "&nbsp;"
    ]
    out["compare_eyebrow"] = _one(r'<p class="pdp-sec__eyebrow">(.*?)</p>', cmp_sec)
    out["compare_title"] = _one(r'<h2 id="pdp-compare-title"[^>]*>(.*?)</h2>', cmp_sec)
    out["compare_sub"] = _one(r'<p class="pdp-sec__sub">(.*?)</p>', cmp_sec)
    out["compare_yes_label"] = _one(r'class="pdp-yes" aria-label="(.*?)"', cmp_sec)
    out["compare_no_label"] = _one(r'class="pdp-no" aria-label="(.*?)"', cmp_sec)
    out["compare_caption"] = _one(r'<caption class="visually-hidden">(.*?)</caption>', cmp_sec)
    out["compare_foot"] = _one(r'<p class="pdp-table-foot">(.*?)</p>', cmp_sec)

    return out


def main() -> None:
    data = {lang: extract(lang) for lang in LANGS}

    counts = {
        lang: {
            k: (len(v) if isinstance(v, list) else ("ok" if v else "MANCANTE"))
            for k, v in d.items()
        }
        for lang, d in data.items()
    }
    ref = counts["it"]
    print("Conteggi per lingua (riferimento: it)")
    for lang in LANGS:
        diff = {k: (ref[k], counts[lang][k]) for k in ref if ref[k] != counts[lang][k]}
        flag = "OK" if not diff else f"DIVERGE {diff}"
        print(f"  {lang}: {counts[lang]}  -> {flag}")

    if "--check" in sys.argv:
        return

    print("\n# ---- voce da incollare in product_content_flagship.PRODUCTS ----")
    pprint.pprint({SLUG: data}, width=110, sort_dicts=False)


if __name__ == "__main__":
    main()
