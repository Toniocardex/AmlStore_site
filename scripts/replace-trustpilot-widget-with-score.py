#!/usr/bin/env python3
"""Patch chirurgica una tantum: sostituisce il TrustBox Trustpilot con un
link statico al voto reale, in tutte le pagine gia' sul disco (PDP + carrello),
e rimuove il loader JS ormai inutile.

Perche': dal 2026-08-30 il widget TrustBox non e' piu' incluso nel piano
gratuito Trustpilot. L'iframe restava in caricamento a vuoto — verificato in
produzione su eurolicenze.com e aprendo l'URL del TrustBox da solo. Il voto
resta comunque mostrabile come dato statico: e' lo stesso 4,8/5 su 94
recensioni gia' presente nella barra header di ogni pagina, sulla home e
nell'aggregateRating del JSON-LD.

Il frammento HTML viene letto da scripts/product_page_lib.py
(_trustpilot_buy_mini), unica fonte, cosi' patch e generatore non divergono.
Le pagine carrello hanno un wrapper diverso (.cart-summary__trust) e una
indentazione piu' profonda: qui si sostituisce solo il blocco interno del
widget, preservando indentazione e wrapper di ciascuna pagina.

    python scripts/replace-trustpilot-widget-with-score.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_page_lib import (  # noqa: E402
    LANGS,
    TRUSTPILOT_LOCALE,
    TRUSTPILOT_REVIEW_COUNT,
    TRUSTPILOT_REVIEWS_WORD,
    TRUSTPILOT_SCORE,
    TRUSTPILOT_SCORE_EN,
    TRUSTPILOT_SCORE_LEAD,
)

# Blocco interno del widget: dal <div id="trustpilot-widget" fino al </div>
# che lo chiude, incluso il link "Trustpilot" di ripiego che conteneva.
WIDGET_RE = re.compile(
    r'( *)<div\n\s*id="trustpilot-widget"[\s\S]*?'
    r'<a href="[^"]+"[^>]*>Trustpilot</a>\n\s*</div>\n'
)

# Riga dello script loader, con o senza hash di cache-busting.
LOADER_RE = re.compile(
    r'[ \t]*<script src="\.\./js/trustpilot-widget\.js(?:\?v=[A-Za-z0-9]+)?" defer></script>\r?\n'
)


def score_anchor(lang, indent):
    """Stesso markup di _trustpilot_buy_mini, con l'indentazione della pagina."""
    _, tp_url = TRUSTPILOT_LOCALE[lang]
    score = TRUSTPILOT_SCORE_EN if lang == "en" else TRUSTPILOT_SCORE
    lead = TRUSTPILOT_SCORE_LEAD[lang]
    reviews = TRUSTPILOT_REVIEWS_WORD[lang]
    return (
        f'{indent}<a class="tp-score" href="{tp_url}" target="_blank" rel="noopener noreferrer">\n'
        f'{indent}    <span class="tp-score__star" aria-hidden="true">★</span>\n'
        f'{indent}    <span class="tp-score__value">{score}/5 {lead} Trustpilot</span>\n'
        f'{indent}    <span class="tp-score__count">{TRUSTPILOT_REVIEW_COUNT} {reviews}</span>\n'
        f"{indent}</a>\n"
    )


def main():
    widgets = loaders = 0
    touched = set()
    problems = []

    for lang in LANGS:
        for path in sorted((ROOT / lang).glob("*.html")):
            text = original = path.read_text(encoding="utf-8")

            matches = WIDGET_RE.findall(text)
            if len(matches) > 1:
                problems.append(f"{path.relative_to(ROOT)}: {len(matches)} widget, salto")
                continue
            if matches:
                text = WIDGET_RE.sub(lambda m: score_anchor(lang, m.group(1)), text)
                widgets += 1

            text, n_loader = LOADER_RE.subn("", text)
            loaders += n_loader

            if text != original:
                path.write_text(text, encoding="utf-8")
                touched.add(str(path.relative_to(ROOT)))

    print(f"Fatto. {widgets} widget sostituiti, {loaders} tag loader rimossi, "
          f"{len(touched)} file toccati.")
    if problems:
        print(f"{len(problems)} problemi:")
        for p in problems:
            print(f"  {p}")


if __name__ == "__main__":
    main()
