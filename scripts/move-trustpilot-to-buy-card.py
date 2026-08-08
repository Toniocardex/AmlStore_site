#!/usr/bin/env python3
"""
Move Trustpilot Micro TrustBox into the PDP buy card (under primary CTA).

- Uses locale/url/token from product_page_lib
- Removes the large reviews section (duplicate #trustpilot-widget)
- Idempotent
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_page_lib import (  # noqa: E402
    TRUSTPILOT_BUSINESS_UNIT,
    TRUSTPILOT_FALLBACK_LEAD,
    TRUSTPILOT_LOCALE,
    TRUSTPILOT_TEMPLATE_ID,
    TRUSTPILOT_TOKEN,
)

LANGS = ("it", "en", "fr", "de", "es")


def buy_mini_html(lang: str) -> str:
    tp_locale, tp_url = TRUSTPILOT_LOCALE[lang]
    fallback_lead = TRUSTPILOT_FALLBACK_LEAD[lang]
    return (
        f'                <div class="product-trustpilot pdp-buy-trustpilot">\n'
        f'                    <p class="product-trustpilot__fallback trustpilot-fallback">{fallback_lead} <a href="{tp_url}" target="_blank" rel="noopener noreferrer">Trustpilot</a>.</p>\n'
        f'                    <div\n'
        f'                        id="trustpilot-widget"\n'
        f'                        class="trustpilot-widget"\n'
        f'                        data-locale="{tp_locale}"\n'
        f'                        data-template-id="{TRUSTPILOT_TEMPLATE_ID}"\n'
        f'                        data-businessunit-id="{TRUSTPILOT_BUSINESS_UNIT}"\n'
        f'                        data-style-height="40px"\n'
        f'                        data-style-width="100%"\n'
        f'                        data-token="{TRUSTPILOT_TOKEN}"\n'
        f'                        data-min-review-count="0"\n'
        f'                        data-style-alignment="center"\n'
        f'                    >\n'
        f'                        <a href="{tp_url}" target="_blank" rel="noopener noreferrer">Trustpilot</a>\n'
        f'                    </div>\n'
        f'                </div>\n'
    )


def remove_large_reviews(html: str) -> tuple[str, int]:
    n = 0
    # v3 reviews card (+ optional divider before)
    pat_v3 = re.compile(
        r'(?:\n[ \t]*<hr class="pdp-divider">\s*)?'
        r'\n[ \t]*<section class="pdp-sec pdp-sec--tight"[^>]*aria-labelledby="pdp-reviews-title"[^>]*>'
        r'.*?</section>\s*',
        re.DOTALL,
    )
    html2, c = pat_v3.subn("\n", html, count=1)
    html, n = html2, n + c

    # v2 standalone trustpilot section
    pat_v2 = re.compile(
        r'\n[ \t]*<section class="product-trustpilot[^"]*"[^>]*>.*?</section>\s*',
        re.DOTALL,
    )
    html2, c = pat_v2.subn("\n", html, count=1)
    html, n = html2, n + c

    # LOCAL TEST leftover comment + section without reviews title (already moved)
    pat_local = re.compile(
        r'\n[ \t]*<!-- LOCAL TEST ONLY:.*?-->\s*'
        r'(?:<section class="pdp-sec pdp-sec--tight"[^>]*>.*?</section>\s*)?',
        re.DOTALL,
    )
    html2, c = pat_local.subn("\n", html)
    html, n = html2, n + c

    return html, n


def insert_buy_mini(html: str, lang: str) -> tuple[str, bool]:
    if "pdp-buy-trustpilot" in html and 'id="trustpilot-widget"' in html:
        # Already in buy card — ensure only one widget id exists after removals
        return html, False

    snippet = buy_mini_html(lang)
    # Prefer v3 primary CTA
    m = re.search(
        r'(<button[^>]*\bid="product-primary-cta"[^>]*>.*?</button>)',
        html,
        flags=re.DOTALL,
    )
    if not m:
        return html, False

    # Avoid double-insert if somehow marked differently
    after = html[m.end() : m.end() + 200]
    if "pdp-buy-trustpilot" in after or 'id="trustpilot-widget"' in after:
        return html, False

    html = html[: m.end()] + "\n\n" + snippet + html[m.end() :]
    return html, True


def ensure_script(html: str) -> tuple[str, bool]:
    if "trustpilot-widget.js" in html:
        return html, False
    # before cookie-banner if present
    if "cookie-banner.js" in html:
        html2, n = re.subn(
            r'(\n[ \t]*<script src="[^"]*cookie-banner\.js[^"]*" defer></script>)',
            r'\n    <script src="../js/trustpilot-widget.js" defer></script>\1',
            html,
            count=1,
        )
        return (html2, True) if n else (html, False)
    html2, n = re.subn(
        r'(\n[ \t]*</body>)',
        r'\n    <script src="../js/trustpilot-widget.js" defer></script>\1',
        html,
        count=1,
    )
    return (html2, True) if n else (html, False)


def process_file(path: Path, lang: str) -> str | None:
    html = path.read_text(encoding="utf-8")
    if 'id="product-primary-cta"' not in html:
        return None
    if "pdp-buy" not in html and "product-pricing" not in html:
        return None

    orig = html
    html, _ = remove_large_reviews(html)
    html, _ = insert_buy_mini(html, lang)
    html, _ = ensure_script(html)

    # Normalize leftover LOCAL TEST comments on buy mini
    html = html.replace(
        "<!-- LOCAL TEST ONLY: mini Trustpilot in buy card — do not commit -->\n",
        "",
    )
    html = re.sub(
        r'^[ \t]*<div class="product-trustpilot pdp-buy-trustpilot"[^>]*>',
        '                <div class="product-trustpilot pdp-buy-trustpilot">',
        html,
        count=1,
        flags=re.M,
    )

    if html == orig:
        return "unchanged"
    path.write_text(html, encoding="utf-8", newline="\n")
    return "updated"


def main() -> None:
    updated = unchanged = skipped = 0
    missing_widget = []
    for lang in LANGS:
        for path in sorted((ROOT / lang).glob("*.html")):
            result = process_file(path, lang)
            if result is None:
                skipped += 1
                continue
            if result == "unchanged":
                unchanged += 1
            else:
                updated += 1
            text = path.read_text(encoding="utf-8")
            if text.count('id="trustpilot-widget"') != 1:
                missing_widget.append(f"{path}: count={text.count('id=\"trustpilot-widget\"')}")
            if "pdp-buy-trustpilot" not in text and 'id="product-primary-cta"' in text:
                missing_widget.append(f"{path}: no buy mini")

    print(f"updated={updated} unchanged={unchanged} skipped={skipped}")
    if missing_widget:
        print("issues:")
        for line in missing_widget[:30]:
            print(" ", line)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
