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
        "h1_a": "Il tuo software", "h1_b": "pronto in 2–15 minuti.",
        "sub": "Licenze digitali 100% originali per la tua casa, lo studio e la famiglia. "
               "Attivazione immediata, nessun rinnovo automatico nascosto.",
        "cta1": "Scopri Microsoft 365 Personal",
    },
    "en": {
        "h1_a": "Your software", "h1_b": "ready in 2–15 minutes.",
        "sub": "100% genuine digital licences for your home, your studies and your family. "
               "Instant activation, no hidden auto-renewal.",
        "cta1": "Discover Microsoft 365 Personal",
    },
    "fr": {
        "h1_a": "Votre logiciel", "h1_b": "prêt en 2–15 minutes.",
        "sub": "Des licences numériques 100 % originales pour votre maison, vos études et votre famille. "
               "Activation immédiate, sans renouvellement automatique caché.",
        "cta1": "Découvrir Microsoft 365 Personnel",
    },
    "de": {
        "h1_a": "Ihre Software", "h1_b": "in 2–15 Minuten bereit.",
        "sub": "Zu 100 % originale digitale Lizenzen für Zuhause, Studium und Familie. "
               "Sofortige Aktivierung, keine versteckte automatische Verlängerung.",
        "cta1": "Microsoft 365 Personal entdecken",
    },
    "es": {
        "h1_a": "Tu software", "h1_b": "listo en 2–15 minutos.",
        "sub": "Licencias digitales 100 % originales para tu casa, tus estudios y tu familia. "
               "Activación inmediata, sin renovación automática oculta.",
        "cta1": "Descubre Microsoft 365 Personal",
    },
}

# Slug della scheda M365 Personal per lingua (le altre lingue usano lo stesso).
PERSONAL = "microsoft-365-personal"


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
