#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inserisce la sezione "Guida all'acquisto" del mockup nella home.

Va fra "I piu' venduti" e "Garanzia e sicurezza", come nel mockup, e ne
eredita la banda scura (bg-slate-900).

Due scostamenti voluti dal mockup, entrambi per non dire il falso:
  - il mockup annuncia "2 veloci domande" ma ne implementa una sola; qui il
    testo dice una domanda, che e' quello che l'interfaccia fa davvero;
  - alla terza opzione il mockup consiglia "Windows 11 Professional + Office
    2021", che non e' un prodotto a catalogo: si rimanda a Office 2021
    Professional Plus, che esiste ed e' la licenza perpetua per il lavoro.

Le raccomandazioni stanno negli attributi data- dei bottoni, non nel JS, cosi'
restano tradotte insieme al markup (vedi js/home-guide.js).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es")

COPY = {
    "it": {
        "eyebrow": "Guida all'acquisto",
        "title": "Non sai quale licenza scegliere?",
        "lede": "Rispondi a una domanda e ti diciamo qual è il software adatto a te.",
        "question": "Chi userà il software?",
        "label": "Consigliato per te",
        "cta": "Vedi la scheda",
        "options": [
            ("Solo io (1 utente)", "microsoft-365-personal", "Microsoft 365 Personal · 12 mesi",
             "Word, Excel, PowerPoint e Outlook, 1 TB di OneDrive e Copilot, su 5 dispositivi in contemporanea."),
            ("Tutta la famiglia (fino a 6)", "microsoft-365-family", "Microsoft 365 Family · 12 mesi",
             "Fino a 6 persone, ognuna con il proprio account e 1 TB di OneDrive. Copilot resta al titolare."),
            ("Studio o lavoro", "office-2021-professional-plus", "Office 2021 Professional Plus",
             "Licenza perpetua: si paga una volta sola, senza rinnovo annuale."),
        ],
    },
    "en": {
        "eyebrow": "Buying guide",
        "title": "Not sure which licence to choose?",
        "lede": "Answer one question and we'll tell you which software suits you.",
        "question": "Who will use the software?",
        "label": "Recommended for you",
        "cta": "See the product page",
        "options": [
            ("Just me (1 user)", "microsoft-365-personal", "Microsoft 365 Personal · 12 months",
             "Word, Excel, PowerPoint and Outlook, 1 TB of OneDrive and Copilot, on 5 devices at once."),
            ("The whole family (up to 6)", "microsoft-365-family", "Microsoft 365 Family · 12 months",
             "Up to 6 people, each with their own account and 1 TB of OneDrive. Copilot stays with the subscription owner."),
            ("Study or work", "office-2021-professional-plus", "Office 2021 Professional Plus",
             "Perpetual licence: you pay once, with no yearly renewal."),
        ],
    },
    "fr": {
        "eyebrow": "Guide d'achat",
        "title": "Vous ne savez pas quelle licence choisir ?",
        "lede": "Répondez à une question et nous vous dirons quel logiciel vous convient.",
        "question": "Qui utilisera le logiciel ?",
        "label": "Recommandé pour vous",
        "cta": "Voir la fiche produit",
        "options": [
            ("Moi uniquement (1 utilisateur)", "microsoft-365-personal", "Microsoft 365 Personnel · 12 mois",
             "Word, Excel, PowerPoint et Outlook, 1 To de OneDrive et Copilot, sur 5 appareils à la fois."),
            ("Toute la famille (jusqu'à 6)", "microsoft-365-family", "Microsoft 365 Family · 12 mois",
             "Jusqu'à 6 personnes, chacune avec son compte et 1 To de OneDrive. Copilot reste au titulaire."),
            ("Études ou travail", "office-2021-professional-plus", "Office 2021 Professional Plus",
             "Licence perpétuelle : un paiement unique, sans renouvellement annuel."),
        ],
    },
    "de": {
        "eyebrow": "Kaufberatung",
        "title": "Sie wissen nicht, welche Lizenz die richtige ist?",
        "lede": "Beantworten Sie eine Frage und wir sagen Ihnen, welche Software zu Ihnen passt.",
        "question": "Wer wird die Software nutzen?",
        "label": "Für Sie empfohlen",
        "cta": "Zur Produktseite",
        "options": [
            ("Nur ich (1 Nutzer)", "microsoft-365-personal", "Microsoft 365 Personal · 12 Monate",
             "Word, Excel, PowerPoint und Outlook, 1 TB OneDrive und Copilot, auf 5 Geräten gleichzeitig."),
            ("Die ganze Familie (bis zu 6)", "microsoft-365-family", "Microsoft 365 Family · 12 Monate",
             "Bis zu 6 Personen, jede mit eigenem Konto und 1 TB OneDrive. Copilot bleibt beim Abo-Inhaber."),
            ("Studium oder Arbeit", "office-2021-professional-plus", "Office 2021 Professional Plus",
             "Dauerlizenz: einmal zahlen, keine jährliche Verlängerung."),
        ],
    },
    "es": {
        "eyebrow": "Guía de compra",
        "title": "¿No sabes qué licencia elegir?",
        "lede": "Responde a una pregunta y te decimos qué software te conviene.",
        "question": "¿Quién usará el software?",
        "label": "Recomendado para ti",
        "cta": "Ver la ficha de producto",
        "options": [
            ("Solo yo (1 usuario)", "microsoft-365-personal", "Microsoft 365 Personal · 12 meses",
             "Word, Excel, PowerPoint y Outlook, 1 TB de OneDrive y Copilot, en 5 dispositivos a la vez."),
            ("Toda la familia (hasta 6)", "microsoft-365-family", "Microsoft 365 Family · 12 meses",
             "Hasta 6 personas, cada una con su cuenta y 1 TB de OneDrive. Copilot queda para el titular."),
            ("Estudio o trabajo", "office-2021-professional-plus", "Office 2021 Professional Plus",
             "Licencia perpetua: se paga una sola vez, sin renovación anual."),
        ],
    },
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def build(lang: str) -> str:
    c = COPY[lang]
    opts = []
    for i, (label, slug, title, body) in enumerate(c["options"]):
        sel = " is-selected" if i == 0 else ""
        opts.append(
            f"""                        <button type="button" class="home-guide__option{sel}" data-guide-option
                            aria-pressed="{'true' if i == 0 else 'false'}"
                            data-guide-href="{slug}"
                            data-guide-title-value="{esc(title)}"
                            data-guide-body-value="{esc(body)}">{label}</button>"""
        )
    first = c["options"][0]
    return f"""        <section class="home-guide" aria-labelledby="home-guide-title" data-home-guide>
            <div class="home-guide__inner">
                <p class="home-section-eyebrow">{c['eyebrow']}</p>
                <h2 id="home-guide-title" class="home-section-title">{c['title']}</h2>
                <p class="home-guide__lede">{c['lede']}</p>
                <div class="home-guide__cols">
                    <div>
                        <p class="home-guide__question">{c['question']}</p>
                        <div class="home-guide__options">
{chr(10).join(opts)}
                        </div>
                    </div>
                    <div class="home-guide__result">
                        <p class="home-guide__result-label">{c['label']}</p>
                        <p class="home-guide__result-title" data-guide-title>{first[2]}</p>
                        <p class="home-guide__result-body" data-guide-body>{first[3]}</p>
                        <a class="home-btn home-btn-primary" href="{first[1]}" data-guide-link>{c['cta']}</a>
                    </div>
                </div>
            </div>
        </section>"""


SCRIPT_TAG = '    <script src="../js/home-guide.js" defer></script>\n'


def main() -> None:
    for lang in LANGS:
        path = ROOT / lang / "index.html"
        html = path.read_text(encoding="utf-8")

        if "home-guide" in html:
            print(f"{lang}: gia' presente — saltato")
            continue

        m = re.search(r'[ \t]*<section class="home-guarantee".*?</section>', html, re.S)
        if not m:
            print(f"{lang}: home-guarantee non trovata — saltato")
            continue
        html = html[: m.start()] + build(lang) + "\n\n" + html[m.start():]

        if "js/home-guide.js" not in html:
            html = html.replace("</body>", SCRIPT_TAG + "</body>", 1)

        path.write_text(html, encoding="utf-8", newline="")
        print(f"{lang}: guida all'acquisto inserita")


if __name__ == "__main__":
    main()
