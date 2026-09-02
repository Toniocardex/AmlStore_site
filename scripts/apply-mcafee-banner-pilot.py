#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applica il redesign pilota "banner" alle 4 PDP McAfee italiane
(1/3/5/10 dispositivi). Idempotente: rilanciarlo non duplica nulla.

Cosa fa su ogni pagina:
  - <body> guadagna la classe .pdp-hero--banner;
  - dentro .pdp-hero entra <img.pdp-hero__banner> + la sfumatura;
  - il preload dell'immagine punta al banner (nuovo LCP);
  - <link> a css/mcafee-pilot.css e <script defer> a js/mcafee-pilot.js;
  - copy: "McAfee My Account" / "portale ufficiale McAfee" -> "sito
    ufficiale McAfee" (meta, og, JSON-LD, keylist, card, tre passi, dialog, FAQ);
  - fascia di chiusura .pdp-mc-close prima di </main>.

Dopo: lanciare scripts/bump-asset-version.py (i ?v= sono a zero).

    python scripts/apply-mcafee-banner-pilot.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUGS = [
    "mcafee-total-protection-1-device",
    "mcafee-total-protection-3-devices",
    "mcafee-total-protection-5-devices",
    "mcafee-total-protection-10-devices",
]

BANNER_IMG = (
    '        <img class="pdp-hero__banner" src="../asset/media/products/{slug}-banner.webp?v=0000000000"'
    ' alt="McAfee Total Protection — naviga, lavora, gioca al sicuro: antivirus, VPN e gestore password'
    ' in un unico abbonamento." width="1760" height="982" fetchpriority="high" decoding="async">\n'
    '        <div class="pdp-hero__banner-fade" aria-hidden="true"></div>\n'
)

CLOSE_BAND = (
    '        <section class="pdp-mc-close" aria-label="Acquista McAfee Total Protection">\n'
    '            <h2>Mettiti al sicuro ora</h2>\n'
    '            <p>Licenza McAfee originale, fattura italiana e supporto in italiano via email e '
    'WhatsApp. Garanzia di sostituzione o rimborso.</p>\n'
    '            <a class="pdp-mc-close__cta" href="#product-pricing">\n'
    '                <svg viewBox="0 0 24 24" width="19" height="19" aria-hidden="true"><path '
    'fill="currentColor" d="M7 18c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 '
    '2.45A2 2 0 0 0 8 17h12v-2H8.42a.25.25 0 0 1-.22-.37L9.1 13h7.45a2 2 0 0 0 1.75-1.03l3.58-6.49A1 1 '
    '0 0 0 21 4H5.21l-.94-2H1zm16 16c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg>\n'
    '                Aggiungi al carrello\n'
    '            </a>\n'
    '        </section>\n'
)

COPY = [
    ("Attivazione su McAfee My Account.", "Attivazione sul sito ufficiale McAfee."),
    ("portale ufficiale McAfee (McAfee My Account)", "sito ufficiale McAfee"),
    ("sul portale ufficiale McAfee e segui le istruzioni", "sul sito ufficiale McAfee e segui le istruzioni"),
    ("dispositivi sul portale ufficiale McAfee.", "dispositivi sul sito ufficiale McAfee."),
    ("Attivazione sicura e gestione ufficiale su McAfee My Account", "Attivazione sicura della licenza sul sito ufficiale McAfee"),
    ("Portale ufficiale McAfee My Account", "Sito ufficiale McAfee"),
    ("Attiva sul portale ufficiale<", "Attiva sul sito ufficiale<"),
]


def patch(slug):
    p = ROOT / "it" / f"{slug}.html"
    t = p.read_text(encoding="utf-8")
    orig = t
    notes = []

    if 'class="pdp-page pdp-hero--banner"' not in t:
        t = t.replace('<body class="pdp-page">', '<body class="pdp-page pdp-hero--banner">', 1)
        notes.append("body class")

    if 'pdp-hero__banner' not in t:
        t = t.replace(
            '    <section class="pdp-hero" aria-label="Prodotto e acquisto">\n',
            '    <section class="pdp-hero" aria-label="Prodotto e acquisto">\n' + BANNER_IMG.format(slug=slug),
            1,
        )
        notes.append("banner img")

    if f'{slug}-banner.webp' not in t.split('<body')[0]:
        t = re.sub(
            r'(<link rel="preload" as="image" href="\.\./asset/media/products/)' + re.escape(slug)
            + r'\.webp\?v=[0-9a-f]+(")',
            r'\1' + slug + r'-banner.webp?v=0000000000\2',
            t, count=1,
        )
        notes.append("preload -> banner")

    if 'css/mcafee-pilot.css' not in t:
        t = re.sub(
            r'(<link rel="stylesheet" href="\.\./css/product-pdp\.css\?v=[0-9a-f]+">)',
            r'\1\n    <link rel="stylesheet" href="../css/mcafee-pilot.css?v=0000000000">',
            t, count=1,
        )
        notes.append("css link")

    if 'js/mcafee-pilot.js' not in t:
        t = re.sub(
            r'(<script src="\.\./js/pdp-paypal-express\.js\?v=[0-9a-f]+" defer></script>)',
            r'\1\n    <script src="../js/mcafee-pilot.js?v=0000000000" defer></script>',
            t, count=1,
        )
        notes.append("js include")

    for a, b in COPY:
        t = t.replace(a, b)

    if 'pdp-mc-close' not in t:
        t = t.replace('    </main>\n', CLOSE_BAND + '    </main>\n', 1)
        notes.append("fascia chiusura")

    if t != orig:
        p.write_text(t, encoding="utf-8")
        print(f"{p.relative_to(ROOT)}: {', '.join(notes) or 'solo copy'}")
    else:
        print(f"{p.relative_to(ROOT)}: gia' a posto")


def main():
    for s in SLUGS:
        patch(s)
    print("\nOra: python scripts/bump-asset-version.py")


if __name__ == "__main__":
    main()
