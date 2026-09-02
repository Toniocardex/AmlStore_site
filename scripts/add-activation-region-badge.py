#!/usr/bin/env python3
"""Add Activation region EU/EEA badge to all product buy cards."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COPY = {
    "en": {
        "aria": "Licence details",
        "label": "Activation region",
        "value": "European Union / EEA",
    },
    "it": {
        "aria": "Dettagli licenza",
        "label": "Regione di attivazione",
        "value": "Unione Europea / SEE",
    },
    "fr": {
        "aria": "Détails de la licence",
        "label": "Zone d'activation",
        "value": "Union européenne / EEE",
    },
    "de": {
        "aria": "Lizenzdetails",
        "label": "Aktivierungsregion",
        "value": "Europäische Union / EWR",
    },
    "es": {
        "aria": "Detalles de la licencia",
        "label": "Región de activación",
        "value": "Unión Europea / EEE",
    },
    # pt e nl mancavano del tutto: per questo le loro 124 PDP sono rimaste
    # senza regione di attivazione fino al 2026-09-02. Etichette e valori non
    # sono tradotti qui per la prima volta, esistono gia' nelle tabelle
    # specifiche delle pagine Microsoft 365.
    "pt": {
        "aria": "Detalhes da licença",
        "label": "Região de ativação",
        "value": "União Europeia / EEE",
    },
    "nl": {
        "aria": "Licentiegegevens",
        "label": "Activeringsregio",
        "value": "Europese Unie / EER",
    },
}

META_BLOCK = """\
                <p class="pdp-meta-row" role="group" aria-label="{aria}">
                    <span class="pdp-meta-chip"><strong>{label}</strong> {value}</span>
                </p>
"""


def is_product_page(text: str) -> bool:
    return 'class="pdp-buy"' in text or "class='pdp-buy'" in text or re.search(
        r'id="product-pricing"[^>]*class="[^"]*pdp-buy', text
    ) is not None or re.search(
        r'class="pdp-buy"[^>]*id="product-pricing"', text
    ) is not None or (
        'id="product-pricing"' in text and "pdp-buy" in text
    )


def has_badge(text: str) -> bool:
    # Dopo il redesign buy card v4 (scripts/apply-buycard-v4.py) il badge non
    # e' piu' un chip riquadrato ma la riga inline .pdp-region: senza questo
    # secondo controllo lo script crederebbe che manchi e rimetterebbe il chip
    # grigio che il redesign ha appena tolto.
    if 'class="pdp-region"' in text:
        return True
    return "pdp-meta-row" in text and "pdp-meta-chip" in text


def insert_badge(text: str, lang: str) -> str:
    if has_badge(text):
        return text
    c = COPY[lang]
    block = META_BLOCK.format(**c)

    # Prefer: after last pdp-price-note before primary CTA
    cta = re.search(
        r'\n([ \t]*)<button[^>]*id="product-primary-cta"[^>]*>',
        text,
    )
    if not cta:
        # sticky-only pages unlikely; try any pdp-btn-primary with data-cart-add inside product-pricing
        cta = re.search(
            r'\n([ \t]*)<button[^>]*class="[^"]*pdp-btn-primary[^"]*"[^>]*data-cart-add[^>]*>',
            text,
        )
    if not cta:
        raise ValueError("no CTA button found")

    indent = cta.group(1)
    # Rebuild block with detected indent
    block = (
        f'{indent}<p class="pdp-meta-row" role="group" aria-label="{c["aria"]}">\n'
        f'{indent}    <span class="pdp-meta-chip"><strong>{c["label"]}</strong> {c["value"]}</span>\n'
        f'{indent}</p>\n\n'
    )
    return text[: cta.start()] + "\n" + block + text[cta.start() + 1 :]


def main() -> None:
    updated = []
    skipped = []
    failed = []
    for lang in COPY:
        for path in sorted((ROOT / lang).glob("*.html")):
            text = path.read_text(encoding="utf-8")
            if not is_product_page(text):
                continue
            if has_badge(text):
                skipped.append(path)
                continue
            try:
                new = insert_badge(text, lang)
            except ValueError as e:
                failed.append((path, str(e)))
                continue
            path.write_text(new, encoding="utf-8", newline="\n")
            updated.append(path)

    print(f"updated={len(updated)} skipped={len(skipped)} failed={len(failed)}")
    for p, err in failed:
        print("FAIL", p.relative_to(ROOT), err)
    # Verify
    missing = []
    for lang in COPY:
        for path in (ROOT / lang).glob("*.html"):
            text = path.read_text(encoding="utf-8")
            if is_product_page(text) and not has_badge(text):
                missing.append(path.relative_to(ROOT))
    print(f"still_missing={len(missing)}")
    for m in missing[:20]:
        print(" ", m)


if __name__ == "__main__":
    main()
