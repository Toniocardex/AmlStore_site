#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sostituisce l'hero della home con la versione consumer del mockup.

L'hero corporate ("Licensing per aziende e professionisti", CTA consulenza)
lascia il posto a quello del mockup: promessa di consegna 2-15 minuti, taglio
casa/studio/famiglia.

La home e' scritta a mano, non generata: come gli altri script di patch della
home (rewrite-home-hero.py, refresh-home-featured.py) qui si sostituisce solo
il nodo <section class="home-hero ..."> lasciando intatto il resto.

Sfondo fotografico (asset/media/home-hero-bg-*.avif|webp, generati da
scripts/build-home-hero-bg.py) al posto della scena con la scatola prodotto:
nell'hero restano solo titolo, sottotitolo e CTA.

L'immagine e' un <picture> con AVIF + WebP e tre larghezze, non un
background-image CSS: cosi' e' l'elemento LCP, il browser la trova subito
nell'HTML e puo' darle fetchpriority alto. width/height espliciti evitano
il layout shift.

Due scostamenti dal mockup richiesti dopo la prima resa:
  - niente badge in cima (nel mockup "Rivenditore Autorizzato"): toglie una
    riga a schermi stretti e l'affermazione non era comunque replicabile;
  - una sola CTA. Le due affiancate del mockup, con etichette lunghe come
    "Scopri Microsoft 365 Personal", sfondavano sotto i ~400px.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es")

COPY = {
    "it": {
        "h1_a": "Protezione originale", "h1_b": "consegna in 5–15 minuti.",
        "sub": "Antivirus e abbonamenti digitali originali. Attivazione sui portali ufficiali, assistenza in italiano, fattura disponibile.",
        "cta1": "Vedi l'antivirus",
    },
    "en": {
        "h1_a": "Genuine protection", "h1_b": "delivered in 5–15 minutes.",
        "sub": "Original antivirus and digital subscriptions. Official-portal activation, human support, invoices available.",
        "cta1": "See antivirus",
    },
    "fr": {
        "h1_a": "Protection originale", "h1_b": "livrée en 5–15 minutes.",
        "sub": "Antivirus et abonnements numériques originaux. Activation sur les portails officiels, assistance humaine, facture disponible.",
        "cta1": "Voir l'antivirus",
    },
    "de": {
        "h1_a": "Originaler Schutz", "h1_b": "in 5–15 Minuten geliefert.",
        "sub": "Originales Antivirus und digitale Abos. Aktivierung auf offiziellen Portalen, persönlicher Support, Rechnung verfügbar.",
        "cta1": "Antivirus ansehen",
    },
    "es": {
        "h1_a": "Protección original", "h1_b": "entrega en 5–15 minutos.",
        "sub": "Antivirus y suscripciones digitales originales. Activación en portales oficiales, asistencia humana, factura disponible.",
        "cta1": "Ver antivirus",
    },
}

# Slug della scheda antivirus.
PERSONAL = "antivirus"


def build(lang: str) -> str:
    c = COPY[lang]
    return f"""        <section class="home-hero home-hero--consumer" aria-labelledby="home-hero-title">
            <picture class="home-hero__bg">
                <source type="image/avif" srcset="../asset/media/home-hero-bg-800.avif 800w, ../asset/media/home-hero-bg-1200.avif 1200w, ../asset/media/home-hero-bg-1600.avif 1600w" sizes="100vw">
                <source type="image/webp" srcset="../asset/media/home-hero-bg-800.webp 800w, ../asset/media/home-hero-bg-1200.webp 1200w, ../asset/media/home-hero-bg-1600.webp 1600w" sizes="100vw">
                <img src="../asset/media/home-hero-bg-1600.webp" width="1600" height="678" alt="" fetchpriority="high" decoding="async">
            </picture>
            <div class="home-hero-inner">
                <div class="home-hero-content">
                    <h1 id="home-hero-title" class="home-hero-title">{c['h1_a']}<br><span class="home-hero__accent">{c['h1_b']}</span></h1>
                    <p class="home-hero-subtitle">{c['sub']}</p>
                    <div class="home-hero-actions">
                        <a class="home-btn home-btn-primary" href="{PERSONAL}">{c['cta1']}</a>
                    </div>
                </div>
            </div>
        </section>"""


HERO_RE = re.compile(r'[ \t]*<section class="home-hero[^"]*"[^>]*>.*?</section>', re.S)


def main() -> None:
    for lang in LANGS:
        path = ROOT / lang / "index.html"
        html = path.read_text(encoding="utf-8")
        new, n = HERO_RE.subn(build(lang), html, count=1)
        if n != 1:
            print(f"{lang}: hero NON trovato — saltato")
            continue
        path.write_text(new, encoding="utf-8", newline="")
        print(f"{lang}: hero sostituito")


if __name__ == "__main__":
    main()
