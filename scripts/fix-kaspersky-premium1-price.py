#!/usr/bin/env python3
"""One-off fix: aumenta il prezzo di KL1047TDAFS (Kaspersky Premium | 1 Dispositivo)
da 30,89 EUR a 37,99 EUR per ripristinare la gerarchia dei piani (Premium > Plus).

Aggiorna solo i blocchi riferiti a questo SKU (antivirus.html e le PDP varianti
1/3/5/10 dispositivi), lasciando intatti altri prodotti con stesso sconto% (es. McAfee 61%).
index.html e' escluso: viene rigenerato da apply-security-first-phase2.py --home-plans.

Da eseguire una sola volta, dopo aver aggiornato catalog.json e catalog.js.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es")

SKU = "KL1047TDAFS"
OLD_UNIT, NEW_UNIT = 3089, 3799
COMPARE = 7999
OLD_PCT, NEW_PCT = 61, 53
OLD_SAVE, NEW_SAVE = "49,10", "42,00"
OLD_PRICE_COMMA, NEW_PRICE_COMMA = "30,89", "37,99"
OLD_PRICE_DOT, NEW_PRICE_DOT = "30.89", "37.99"

CLUSTER_START_RE = re.compile(r'data-stripe-currency="eur"')
SKU_ATTR_RE = re.compile(r'data-stripe-product-sku="([^"]+)"')

TARGET_FILES = ["antivirus.html", "kaspersky-premium-1-device.html"] + [
    f"kaspersky-premium-{n}-devices.html" for n in (3, 5, 10)
]


def blocks_for_file(text: str):
    starts = list(CLUSTER_START_RE.finditer(text))
    if not starts:
        return []
    if len(starts) == 1:
        m = SKU_ATTR_RE.search(text, starts[0].start())
        return [(m.group(1), 0, len(text))] if m else []
    blocks = []
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        block_text = text[m.start():end]
        sku_m = SKU_ATTR_RE.search(block_text)
        if sku_m:
            blocks.append((sku_m.group(1), m.start(), end))
    return blocks


def patch_block(block: str) -> str:
    block = block.replace(f'data-stripe-unit-amount="{OLD_UNIT}"', f'data-stripe-unit-amount="{NEW_UNIT}"')
    block = block.replace(f'data-discount-percent="{OLD_PCT}"', f'data-discount-percent="{NEW_PCT}"')
    block = block.replace(f'\u2212{OLD_PCT}%', f'\u2212{NEW_PCT}%')
    block = block.replace(f'-{OLD_PCT}%', f'-{NEW_PCT}%')
    block = block.replace(f'aria-label="{OLD_PCT}%"', f'aria-label="{NEW_PCT}%"')
    block = block.replace(OLD_PRICE_COMMA, NEW_PRICE_COMMA)
    block = block.replace(OLD_PRICE_DOT, NEW_PRICE_DOT)
    block = block.replace(OLD_SAVE, NEW_SAVE)
    return block


def patch_plan_switcher(text: str) -> str:
    """Fix the '1 dispositivo · € 30,89' cross-link shown on sibling device-count PDPs."""
    return text.replace(f'\u00b7 \u20ac {OLD_PRICE_COMMA}', f'\u00b7 \u20ac {NEW_PRICE_COMMA}')


def main():
    total = 0
    for lang in LANGS:
        for name in TARGET_FILES:
            path = ROOT / lang / name
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            blocks = blocks_for_file(text)
            target = [b for b in blocks if b[0] == SKU]
            new_text = text
            for _, start, end in reversed(target):
                original_block = text[start:end]
                new_text = new_text[:start] + patch_block(original_block) + new_text[end:]
            new_text = patch_plan_switcher(new_text)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8", newline="\n")
                total += 1
                print("patched", lang, name)
    print("files patched:", total)


if __name__ == "__main__":
    main()
