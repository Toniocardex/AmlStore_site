#!/usr/bin/env python3
"""Generic helper to backfill a missing language in per-language content maps.

Motivazione: molti moduli `product_content_*.py` costruiscono dizionari
letterali `{"it": ..., "en": ..., "fr": ..., "de": ..., "es": ...}` per ogni
campo di ogni prodotto (title_html, eyebrow, desc, faq, features, ...).
Tradurre a mano *ogni* campo opzionale per pt (e in futuro nl) su ~80 SKU non
è sostenibile in un solo giro; le chiavi davvero indicizzate senza fallback
da `product_page_lib.py` (title_html, eyebrow, desc, faq) vanno tradotte a
mano perché sono le più visibili/SEO-critiche, ma tutti gli altri campi
per-lingua (features, keypoints, specs, steps, pills, name, ...) possono
ereditare in modo sicuro il valore della lingua più vicina (es) invece di
far esplodere il generatore con un KeyError silenzioso in produzione.

`backfill_lang` cammina ricorsivamente una struttura dict/list/tuple e, per
ogni dict le cui chiavi sono un sottoinsieme dei codici lingua noti, copia
`obj[source]` in `obj[target]` se `target` è assente. Non tocca nulla se
`target` è già presente (le traduzioni scritte a mano vincono sempre).
"""

_LANG_CODES = {"it", "en", "fr", "de", "es", "pt", "nl"}


def backfill_lang(obj, target="pt", source="es", _seen=None, translate=None):
    """Copia `source` in `target` dove `target` manca.

    `translate` e' una callable opzionale applicata al valore copiato: serve
    a nl, dove il fallback grezzo sull'inglese lasciava la copy di prodotto
    non tradotta. Vedi scripts/nl_translations.py.
    """
    if _seen is None:
        _seen = set()
    oid = id(obj)
    if oid in _seen:
        return
    if isinstance(obj, dict):
        _seen.add(oid)
        keys = set(obj.keys())
        if keys and keys <= _LANG_CODES and source in obj and target not in obj:
            value = obj[source]
            obj[target] = translate(value) if translate is not None else value
        for v in list(obj.values()):
            backfill_lang(v, target, source, _seen, translate)
    elif isinstance(obj, list):
        _seen.add(oid)
        for v in obj:
            backfill_lang(v, target, source, _seen, translate)
    elif isinstance(obj, tuple):
        for v in obj:
            backfill_lang(v, target, source, _seen, translate)
