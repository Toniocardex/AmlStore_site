#!/usr/bin/env python3
"""Regenerate all product PDPs with Trustpilot block; patch preserved pages."""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_page_lib import (  # noqa: E402
    LANGS,
    _trustpilot_block,
    _trustpilot_script_tag,
    build_product_page,
)

spec = importlib.util.spec_from_file_location("generate_wave3", ROOT / "scripts" / "generate-wave3.py")
gw3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gw3)

PRESERVE = gw3.PRESERVE_PAGES
PRODUCTS = gw3.PRODUCTS


def patch_preserve(path: Path, lang: str) -> bool:
    html = path.read_text(encoding="utf-8")
    already = 'id="trustpilot-widget"' in html and "trustpilot-widget.js" in html
    if already:
        return False

    block = _trustpilot_block(lang)
    script = _trustpilot_script_tag()
    changed = False

    if 'id="trustpilot-widget"' not in html:
        # After steps section, before divider (allow blank lines)
        m = re.search(
            r"(</div>\s*</section>)\s*(<hr class=\"v2-divider\">)",
            html,
            flags=re.MULTILINE,
        )
        if m:
            html = html[: m.start()] + m.group(1) + "\n" + block + m.group(2) + html[m.end() :]
            changed = True
        else:
            html = html.replace("</main>", block + "    </main>", 1)
            changed = True

    if "trustpilot-widget.js" not in html:
        html2, n = re.subn(
            r'(<script src="../js/product-page\.js[^"]*" defer></script>)',
            script + r"    \1",
            html,
            count=1,
        )
        if n:
            html = html2
            changed = True
        else:
            html = html.replace("</body>", script + "</body>", 1)
            changed = True

    if changed:
        path.write_text(html, encoding="utf-8")
    return changed


def main():
    rebuilt = 0
    for p in PRODUCTS:
        fname = f"{p['slug']}.html"
        if fname in PRESERVE:
            continue
        for lang in LANGS:
            target = ROOT / lang / fname
            html = build_product_page(lang, p)
            if 'id="trustpilot-widget"' not in html:
                raise SystemExit(f"missing trustpilot in build: {fname}/{lang}")
            if "trustpilot-widget.js" not in html:
                raise SystemExit(f"missing trustpilot script: {fname}/{lang}")
            target.write_text(html, encoding="utf-8")
        rebuilt += 1
        print("rebuild", p["slug"])

    patched = 0
    for fname in sorted(PRESERVE):
        slug = fname.replace(".html", "")
        for lang in LANGS:
            path = ROOT / lang / fname
            if not path.exists():
                print("missing preserve", lang, fname)
                continue
            if patch_preserve(path, lang):
                patched += 1
                print("patch", lang, slug)
            else:
                print("skip", lang, slug)

    print(f"done rebuild={rebuilt} patch_ops={patched}")


if __name__ == "__main__":
    main()
