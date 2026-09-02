#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aggiunge la plan-card McAfee 3 dispositivi (SKU MTP-3D-1Y) al Protection
Selector della home, in tutte e 7 le lingue.

Il pannello McAfee di .home-protect e' a card statiche (niente <select>, quello
ce l'ha solo Kaspersky Premium): la card d3 va inserita nell'HTML fra d1 e d5.
La griglia passa da 3 a 4 colonne via la classe .plan-grid--count-4 (regola
aggiunta a mano in css/home.css).

Idempotente: se la card d3 c'e' gia', salta.

    python scripts/add-mcafee-3-devices-home-card.py --apply
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es", "pt", "nl")

DEVICE_PL = {"it": "dispositivi", "en": "devices", "fr": "appareils",
             "de": "Geräte", "es": "dispositivos", "pt": "dispositivos", "nl": "apparaten"}
ROLE_3 = {
    "it": "Protezione multi-dispositivo", "en": "Multi-device protection",
    "fr": "Protection multi-appareils", "de": "Schutz für mehrere Geräte",
    "es": "Protección multidispositivo", "pt": "Proteção multi-dispositivo",
    "nl": "Bescherming voor meerdere apparaten",
}
IDEAL_3 = {
    "it": "coppie e piccole famiglie", "en": "couples and small families",
    "fr": "couples et petites familles", "de": "Paare und kleine Familien",
    "es": "parejas y familias pequeñas", "pt": "casais e famílias pequenas",
    "nl": "koppels en kleine gezinnen",
}

PANEL_RE = re.compile(r'<div class="plan-grid[^"]*" data-protect-brand-panel="mcafee"[^>]*>')
D5_RE = re.compile(r'\n(\s*)<article class="plan-card plan-card--brand-mcafee is-featured" data-plan="d5".*?</article>', re.S)


def build_d3(lang, d5_html, indent):
    c = d5_html
    c = c.replace(' is-featured" data-plan="d5" data-devices="5" data-default-featured',
                  '" data-plan="d3" data-devices="3"')
    c = c.replace('data-stripe-unit-amount="1489"', 'data-stripe-unit-amount="1099"')
    c = c.replace('data-stripe-compare-at-amount="3995"', 'data-stripe-compare-at-amount="3495"')
    c = c.replace('data-stripe-product-sku="1108923"', 'data-stripe-product-sku="MTP-3D-1Y"')
    c = c.replace('data-discount-percent="63"', 'data-discount-percent="69"')
    c = c.replace('products/mcafee-total-protection-5-devices.webp', 'products/mcafee-total-protection-3-devices.webp')
    c = c.replace('<span data-plan-price>14,89</span>', '<span data-plan-price>10,99</span>')
    c = c.replace('data-plan-msrp>€ 39,95<', 'data-plan-msrp>€ 34,95<')
    pl = DEVICE_PL[lang]
    c = c.replace(f'plan-card__devices-pill">5 {pl}<', f'plan-card__devices-pill">3 {pl}<')
    c = c.replace(f'plan-card__role">{_role5(lang)}<', f'plan-card__role">{ROLE_3[lang]}<')
    c = re.sub(r'(plan-card__ideal"><strong>[^<]+</strong>\s*<span>)[^<]+(</span>)',
               rf'\g<1>{IDEAL_3[lang]}\g<2>', c)
    c = c.replace('data-plan-more href="mcafee-total-protection-5-devices"',
                  'data-plan-more href="mcafee-total-protection-3-devices"')
    return f"\n{indent}" + c.strip()


def _role5(lang):
    return {"it": "Protezione consigliata", "en": "Recommended protection",
            "fr": "Protection conseillée", "de": "Empfohlener Schutz",
            "es": "Protección recomendada", "pt": "Proteção recomendada",
            "nl": "Aanbevolen bescherming"}[lang]


def patch(lang, apply):
    p = ROOT / lang / "index.html"
    t = p.read_text(encoding="utf-8")
    if 'plan-card--brand-mcafee" data-plan="d3"' in t:
        print(f"{lang}/index.html: card d3 gia' presente, salto")
        return
    pm = PANEL_RE.search(t)
    if not pm:
        print(f"{lang}/index.html: pannello McAfee non trovato")
        return
    dm = D5_RE.search(t, pm.end())
    if not dm:
        print(f"{lang}/index.html: card d5 McAfee non trovata")
        return
    indent = dm.group(1)
    d3 = build_d3(lang, dm.group(0).lstrip("\n"), indent)
    # inserisci d3 subito PRIMA della d5
    out = t[:dm.start()] + d3 + t[dm.start():]
    # classe griglia -> count-4 (solo sul pannello McAfee)
    out = out.replace('<div class="plan-grid" data-protect-brand-panel="mcafee"',
                      '<div class="plan-grid plan-grid--count-4" data-protect-brand-panel="mcafee"', 1)
    if out == t:
        print(f"{lang}/index.html: nessun cambiamento")
        return
    print(f"{lang}/index.html: card d3 inserita + griglia count-4")
    if apply:
        p.write_text(out, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    for lang in LANGS:
        patch(lang, args.apply)
    if not args.apply:
        print("\nDry-run. Rilancia con --apply.")


if __name__ == "__main__":
    main()
