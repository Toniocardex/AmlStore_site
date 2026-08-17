#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Porta il set di sezioni della home su quello del mockup.

Mockup: hero → categorie → piu' venduti → guida all'acquisto → garanzie →
recensioni. La home aveva invece: hero → come funziona → soluzioni → business
→ piu' venduti → FAQ → recensioni → consigliati.

Quindi qui si:
  - rimuovono home-steps, home-faq e home-recommended (non previste dal mockup);
  - sostituisce home-business (blocco B2B "Per aziende e professionisti") con
    la sezione Garanzia e Sicurezza del mockup;
  - riordinano le sezioni superstiti nell'ordine del mockup.

Sui testi delle garanzie NON si usa la copy del mockup ma quella gia' in uso
nella trustbar delle schede prodotto: il mockup parla di una "Garanzia AML
Care" che sul sito non esiste e di una "risposta media < 15 minuti" che non e'
dichiarata da nessuna parte. La struttura (4 punti + occhiello + titolo) e'
invece replicata 1:1.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es")

DROP = ("home-steps", "home-faq", "home-recommended")

ICONS = {
    "house": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l9 8h-3v10h-5v-6h-2v6H6V11H3l9-8z"></path></svg>',
    "doc": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 2h8l6 6v14H6V2zm7 1.5V9h5.5L13 3.5zM8 12h8v2H8v-2zm0 4h8v2H8v-2z"></path></svg>',
    "headset": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 00-9 9v4a3 3 0 003 3h2v-8H5v1a7 7 0 1114 0v-1h-3v8h3a3 3 0 003-3v-4a9 9 0 00-9-9z"></path></svg>',
    "lock": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a5 5 0 015 5v3h1a2 2 0 012 2v8a2 2 0 01-2 2H6a2 2 0 01-2-2v-8a2 2 0 012-2h1V7a5 5 0 015-5zm0 2a3 3 0 00-3 3v3h6V7a3 3 0 00-3-3z"></path></svg>',
}

# Copy gia' in uso nella trustbar delle schede prodotto (verificata).
COPY = {
    "it": {
        "eyebrow": "Garanzia e sicurezza",
        "title": "Acquista con maggiore tranquillità",
        "lede": "Ti seguiamo passo passo fino all'attivazione completa della licenza.",
        "items": [
            ("house", "Azienda italiana", "Sede e P.IVA in Italia."),
            ("doc", "Fattura elettronica", "Disponibile per privati e aziende."),
            ("headset", "Assistenza in italiano", "Supporto post-vendita via email e WhatsApp."),
            ("lock", "Pagamenti protetti", "Elaborati tramite Stripe e PayPal."),
        ],
    },
    "en": {
        "eyebrow": "Guarantee and security",
        "title": "Buy with greater peace of mind",
        "lede": "We follow you step by step through to full licence activation.",
        "items": [
            ("house", "Italian company", "Registered office and VAT number in Italy."),
            ("doc", "Electronic invoice", "Available for individuals and businesses."),
            ("headset", "Support in Italian", "After-sales support by email and WhatsApp."),
            ("lock", "Protected payments", "Processed through Stripe and PayPal."),
        ],
    },
    "fr": {
        "eyebrow": "Garantie et sécurité",
        "title": "Achetez en toute tranquillité",
        "lede": "Nous vous accompagnons pas à pas jusqu'à l'activation complète de la licence.",
        "items": [
            ("house", "Entreprise italienne", "Siège social et numéro de TVA en Italie."),
            ("doc", "Facture électronique", "Disponible pour les particuliers et les entreprises."),
            ("headset", "Assistance en italien", "Support après-vente par e-mail et WhatsApp."),
            ("lock", "Paiements protégés", "Traités via Stripe et PayPal."),
        ],
    },
    "de": {
        "eyebrow": "Garantie und Sicherheit",
        "title": "Kaufen Sie mit mehr Sicherheit",
        "lede": "Wir begleiten Sie Schritt für Schritt bis zur vollständigen Aktivierung der Lizenz.",
        "items": [
            ("house", "Italienisches Unternehmen", "Sitz und USt-IdNr. in Italien."),
            ("doc", "Elektronische Rechnung", "Verfügbar für Privatpersonen und Unternehmen."),
            ("headset", "Support auf Italienisch", "After-Sales-Support per E-Mail und WhatsApp."),
            ("lock", "Geschützte Zahlungen", "Abgewickelt über Stripe und PayPal."),
        ],
    },
    "es": {
        "eyebrow": "Garantía y seguridad",
        "title": "Compra con mayor tranquilidad",
        "lede": "Te acompañamos paso a paso hasta la activación completa de la licencia.",
        "items": [
            ("house", "Empresa italiana", "Sede y NIF en Italia."),
            ("doc", "Factura electrónica", "Disponible para particulares y empresas."),
            ("headset", "Asistencia en italiano", "Soporte posventa por email y WhatsApp."),
            ("lock", "Pagos protegidos", "Procesados mediante Stripe y PayPal."),
        ],
    },
}


def guarantee_section(lang: str) -> str:
    c = COPY[lang]
    items = "\n".join(
        f"""                <li class="home-guarantee__item">
                    <span class="home-guarantee__icon" aria-hidden="true">{ICONS[icon]}</span>
                    <div>
                        <h3>{title}</h3>
                        <p>{body}</p>
                    </div>
                </li>"""
        for icon, title, body in c["items"]
    )
    return f"""        <section class="home-guarantee" aria-labelledby="home-guarantee-title">
            <p class="home-section-eyebrow">{c['eyebrow']}</p>
            <h2 id="home-guarantee-title" class="home-section-title">{c['title']}</h2>
            <p class="home-guarantee__lede">{c['lede']}</p>
            <ul class="home-guarantee__grid">
{items}
            </ul>
        </section>"""


SEC_RE = re.compile(r'[ \t]*<section[^>]*class="(home-[a-z-]+)[^"]*"[^>]*>.*?</section>\n?', re.S)


def main() -> None:
    for lang in LANGS:
        path = ROOT / lang / "index.html"
        html = path.read_text(encoding="utf-8")

        found: dict[str, str] = {}
        for m in SEC_RE.finditer(html):
            found.setdefault(m.group(1), m.group(0))

        missing = [k for k in ("home-hero", "home-categories", "home-catalog", "home-social-proof")
                   if k not in found]
        if missing:
            print(f"{lang}: sezioni mancanti {missing} — saltato")
            continue

        # Rimuove tutte le sezioni home-* dal main, poi le riscrive in ordine.
        start = html.index(found["home-hero"])
        last_key = max(found, key=lambda k: html.index(found[k]))
        end = html.index(found[last_key]) + len(found[last_key])

        order = [
            found["home-hero"].rstrip("\n"),
            found["home-categories"].rstrip("\n"),
            found["home-catalog"].rstrip("\n"),
            guarantee_section(lang),
            found["home-social-proof"].rstrip("\n"),
        ]
        html = html[:start] + "\n\n".join(order) + "\n" + html[end:]
        path.write_text(html, encoding="utf-8", newline="")

        dropped = [k for k in DROP if k in found]
        print(f"{lang}: rimosse {dropped}, home-business -> home-guarantee, riordinate")


if __name__ == "__main__":
    main()
