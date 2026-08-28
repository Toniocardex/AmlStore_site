#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rende parlante l'aria-label del selettore lingua nell'header pre-renderizzato.

Prima diceva solo "Seleziona lingua" (tradotto): uno screen reader annunciava
il pulsante senza dire quale lingua fosse attiva, e da quando il pulsante si
riduce alla sola bandiera sotto i 480px non c'era piu' nemmeno la sigla "IT"
nel testo interno a colmare il vuoto. Ora l'aria-label nomina la lingua
corrente.

Patch chirurgica sulle pagine gia' pubblicate: tocca solo l'attributo
aria-label del <button class="lang-selector">, ancorandosi su
aria-controls="header-lang-dropdown" che ha solo quel pulsante (il <div>
del menu a tendina porta lo stesso vecchio testo ma nessun aria-controls).

La sorgente del markup — scripts/chrome-renderer/header.js — e' gia' allineata
a queste stesse stringhe, quindi `build-inline-chrome.mjs --check` resta verde.

    python scripts/patch-lang-aria-label.py [--check]

Dopo l'esecuzione lanciare `python scripts/bump-asset-version.py`.
Idempotente: le pagine gia' aggiornate vengono saltate.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ["it", "en", "fr", "de", "es", "pt", "nl"]
CHECK = "--check" in sys.argv

ANCHOR = 'aria-controls="header-lang-dropdown" aria-label="'

# vecchio testo (== selectLanguage del renderer) -> nuovo testo parlante
OLD_NEW = {
    "it": ("Seleziona lingua", "Lingua: italiano — cambia lingua"),
    "en": ("Select language", "Language: English — change language"),
    "fr": ("Choisir la langue", "Langue : français — changer de langue"),
    "de": ("Sprache wählen", "Sprache: Deutsch — Sprache ändern"),
    "es": ("Seleccionar idioma", "Idioma: español — cambiar idioma"),
    "pt": ("Selecionar idioma", "Idioma: português — mudar idioma"),
    "nl": ("Taal selecteren", "Taal: Nederlands — taal wijzigen"),
}


def main():
    changed, already, drift = 0, 0, 0
    for lang in LANGS:
        old, new = OLD_NEW[lang]
        src_frag = ANCHOR + old + '"'
        dst_frag = ANCHOR + new + '"'
        d = os.path.join(ROOT, lang)
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".html"):
                continue
            p = os.path.join(d, fn)
            with open(p, encoding="utf-8") as fh:
                html = fh.read()
            if dst_frag in html:
                already += 1
                continue
            if src_frag not in html:
                drift += 1
                print("  ATTESO NON TROVATO:", os.path.join(lang, fn))
                continue
            if CHECK:
                changed += 1
                continue
            html = html.replace(src_frag, dst_frag, 1)
            with open(p, "w", encoding="utf-8", newline="") as fh:
                fh.write(html)
            changed += 1

    verb = "da aggiornare" if CHECK else "aggiornate"
    print(f"pagine {verb}: {changed} | gia' a posto: {already} | fuori schema: {drift}")
    if drift:
        sys.exit(2)
    if CHECK and changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
