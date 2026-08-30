#!/usr/bin/env python3
"""Patch chirurgica una tantum: aggiunge il blocco Trustpilot nella buy card
di ogni pagina prodotto (PDP), nelle 7 lingue.

NOTA (2026-08-30): quando e' stato scritto inseriva il micro TrustBox
ufficiale; quel widget e' poi uscito dal piano gratuito Trustpilot ed e'
stato sostituito dal link statico al voto (vedi
replace-trustpilot-widget-with-score.py). Questo script resta valido: legge
il frammento da _trustpilot_buy_mini(), quindi oggi inserirebbe la versione
statica, non il widget morto.

Il generatore (product_page_lib.py, funzione build_rich_product_page) lo
inserisce gia' per le pagine future — vedi _trustpilot_buy_mini() e il suo
punto di chiamata dopo la lista <ul class="pdp-assur">. Le 434 pagine PDP
gia' sul disco (62 prodotti x 7 lingue) sono pero' precedenti a quella
funzione e non lo hanno mai avuto: lo script inserisce lo stesso frammento
subito dopo </ul>, senza toccare nient'altro (niente rigenerazione della
pagina — vedi la nota sul rischio "Licenza " nel titolo scoperta durante
il giro sull'anno edizione antivirus).

Usa scripts/product_page_lib.py come unica fonte del frammento HTML
(_trustpilot_buy_mini), cosi' la patch e il generatore restano identici.

    python scripts/add-pdp-trustpilot-widget.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_page_lib import LANGS, _trustpilot_buy_mini  # noqa: E402

ASSUR_CLOSE_RE = re.compile(
    r'( {16}<ul class="pdp-assur">\n(?:.*\n)*? {16}</ul>\n)'
)


def patch_file(path: Path, widget_html: str) -> str:
    text = path.read_text(encoding="utf-8")
    if "pdp-buy-trustpilot" in text:
        return "skip (gia' presente)"
    match = ASSUR_CLOSE_RE.search(text)
    if not match:
        return "ATTENZIONE: <ul class=\"pdp-assur\"> non trovato"
    if len(ASSUR_CLOSE_RE.findall(text)) != 1:
        return "ATTENZIONE: piu' di un blocco pdp-assur, salto"
    insert_at = match.end()
    new_text = text[:insert_at] + widget_html + text[insert_at:]
    path.write_text(new_text, encoding="utf-8")
    return "ok"


def main():
    counts = {"ok": 0, "skip": 0}
    problems = []
    for lang in LANGS:
        widget_html = _trustpilot_buy_mini(lang)
        for path in sorted((ROOT / lang).glob("*.html")):
            if 'id="product-primary-cta"' not in path.read_text(encoding="utf-8"):
                continue
            result = patch_file(path, widget_html)
            if result == "ok":
                counts["ok"] += 1
            elif result.startswith("skip"):
                counts["skip"] += 1
            else:
                problems.append(f"{path.relative_to(ROOT)}: {result}")

    print(f"Fatto. {counts['ok']} pagine patchate, {counts['skip']} gia' a posto.")
    if problems:
        print(f"{len(problems)} problemi:")
        for p in problems:
            print(f"  {p}")


if __name__ == "__main__":
    main()
