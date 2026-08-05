#!/usr/bin/env python3
"""Apply homepage CTA/soluzioni plan to it|en|fr|de|es index.html."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# SVG icons reused from existing tiles
ICON_WIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="14" rx="2"></rect><path d="M8 21h8M12 18v3"></path></svg>'
ICON_OFFICE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><path d="M14 2v6h6"></path></svg>'
ICON_M365 = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19a4.5 4.5 0 0 0 0-9 6 6 0 0 0-11.4-1.5A5 5 0 0 0 6.5 19h11z"></path></svg>'
ICON_AV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
ICON_SERVER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M3 5v14a9 3 0 0 0 18 0V5"></path><path d="M3 12a9 3 0 0 0 18 0"></path></svg>'
ICON_TOOLS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>'

LANG = {
    "it": {
        "cta2": "Esplora le soluzioni",
        "h2": "Soluzioni",
        "step1": "Scegli la soluzione adatta tra le categorie (Microsoft 365, Windows, Office, sicurezza, server, Project e Visio) e apri la scheda per prezzo, durata e indicazioni di attivazione.",
        "tiles": [
            ("microsoft-365-solutions", ICON_M365, "Microsoft 365", "Personal, Family e Business"),
            ("sistemi-operativi", ICON_WIN, "Windows", "Windows 10 e 11, Home e Pro"),
            ("suite-office", ICON_OFFICE, "Office", "Da Office 2019 a Office 2024"),
            ("antivirus", ICON_AV, "Antivirus e sicurezza", "Norton, Kaspersky, Bitdefender, ESET, McAfee"),
            ("windows-server", ICON_SERVER, "Server e database", "Windows Server e SQL Server"),
            ("strumenti", ICON_TOOLS, "Project e Visio", "Project e Visio 2024"),
        ],
    },
    "en": {
        "cta2": "Explore solutions",
        "h2": "Solutions",
        "step1": "Choose the right solution from the categories (Microsoft 365, Windows, Office, security, servers, Project and Visio) and open the product page for price, term and activation guidance.",
        "tiles": [
            ("microsoft-365-solutions", ICON_M365, "Microsoft 365", "Personal, Family and Business"),
            ("sistemi-operativi", ICON_WIN, "Windows", "Windows 10 and 11, Home and Pro"),
            ("suite-office", ICON_OFFICE, "Office", "From Office 2019 to Office 2024"),
            ("antivirus", ICON_AV, "Antivirus and security", "Norton, Kaspersky, Bitdefender, ESET, McAfee"),
            ("windows-server", ICON_SERVER, "Servers and databases", "Windows Server and SQL Server"),
            ("strumenti", ICON_TOOLS, "Project and Visio", "Project and Visio 2024"),
        ],
    },
    "fr": {
        "cta2": "Découvrir les solutions",
        "h2": "Solutions",
        "step1": "Choisissez la solution adaptée parmi les catégories (Microsoft 365, Windows, Office, sécurité, serveurs, Project et Visio) et ouvrez la fiche pour le prix, la durée et l'activation.",
        "tiles": [
            ("microsoft-365-solutions", ICON_M365, "Microsoft 365", "Personal, Family et Business"),
            ("sistemi-operativi", ICON_WIN, "Windows", "Windows 10 et 11, Home et Pro"),
            ("suite-office", ICON_OFFICE, "Office", "D'Office 2019 à Office 2024"),
            ("antivirus", ICON_AV, "Antivirus et sécurité", "Norton, Kaspersky, Bitdefender, ESET, McAfee"),
            ("windows-server", ICON_SERVER, "Serveurs et bases de données", "Windows Server et SQL Server"),
            ("strumenti", ICON_TOOLS, "Project et Visio", "Project et Visio 2024"),
        ],
    },
    "de": {
        "cta2": "Lösungen entdecken",
        "h2": "Lösungen",
        "step1": "Wählen Sie die passende Lösung aus den Kategorien (Microsoft 365, Windows, Office, Sicherheit, Server, Project und Visio) und öffnen Sie die Produktseite für Preis, Laufzeit und Aktivierung.",
        "tiles": [
            ("microsoft-365-solutions", ICON_M365, "Microsoft 365", "Personal, Family und Business"),
            ("sistemi-operativi", ICON_WIN, "Windows", "Windows 10 und 11, Home und Pro"),
            ("suite-office", ICON_OFFICE, "Office", "Von Office 2019 bis Office 2024"),
            ("antivirus", ICON_AV, "Antivirus und Sicherheit", "Norton, Kaspersky, Bitdefender, ESET, McAfee"),
            ("windows-server", ICON_SERVER, "Server und Datenbanken", "Windows Server und SQL Server"),
            ("strumenti", ICON_TOOLS, "Project und Visio", "Project und Visio 2024"),
        ],
    },
    "es": {
        "cta2": "Explorar las soluciones",
        "h2": "Soluciones",
        "step1": "Elige la solución adecuada entre las categorías (Microsoft 365, Windows, Office, seguridad, servidores, Project y Visio) y abre la ficha para precio, duración e instrucciones de activación.",
        "tiles": [
            ("microsoft-365-solutions", ICON_M365, "Microsoft 365", "Personal, Family y Business"),
            ("sistemi-operativi", ICON_WIN, "Windows", "Windows 10 y 11, Home y Pro"),
            ("suite-office", ICON_OFFICE, "Office", "De Office 2019 a Office 2024"),
            ("antivirus", ICON_AV, "Antivirus y seguridad", "Norton, Kaspersky, Bitdefender, ESET, McAfee"),
            ("windows-server", ICON_SERVER, "Servidores y bases de datos", "Windows Server y SQL Server"),
            ("strumenti", ICON_TOOLS, "Project y Visio", "Project y Visio 2024"),
        ],
    },
}

HERO_CTA2_OLD = {
    "it": "Esplora il catalogo",
    "en": "Browse the catalogue",
    "fr": "Explorer le catalogue",
    "de": "Katalog entdecken",
    "es": "Explorar el catálogo",
}

CLOSING_CTA_OLD = {
    "it": "Esplora il catalogo",
    "en": "Browse the catalogue",
    "fr": "Explorer le catalogue",
    "de": "Katalog erkunden",
    "es": "Explorar el catálogo",
}


def tile_html(href: str, icon: str, name: str, desc: str) -> str:
    return f"""                <li>
                    <a href="{href}" class="home-category-tile">
                        <span class="home-category-icon" aria-hidden="true">{icon}</span>
                        <span class="home-category-copy">
                            <span class="home-category-name">{name}</span>
                            <span class="home-category-desc">{desc}</span>
                        </span>
                        <span class="home-category-arrow" aria-hidden="true">&rarr;</span>
                    </a>
                </li>"""


def categories_block(lang: str, t: dict) -> str:
    tiles = "\n".join(tile_html(*x) for x in t["tiles"])
    return f"""        <section id="soluzioni" class="home-categories" aria-labelledby="home-categories-title">
            <h2 id="home-categories-title" class="home-section-title">{t['h2']}</h2>
            <ul class="home-categories-grid">
{tiles}
            </ul>
        </section>"""


def patch_lang(lang: str) -> None:
    t = LANG[lang]
    path = ROOT / lang / "index.html"
    text = path.read_text(encoding="utf-8")

    # Hero CTA2
    old_cta = HERO_CTA2_OLD[lang]
    text2, n = re.subn(
        rf'(<a class="home-btn home-btn-ghost" href="#)catalogo(">){re.escape(old_cta)}(</a>)',
        rf'\1soluzioni\2{t["cta2"]}\3',
        text,
        count=1,
    )
    if n != 1:
        raise SystemExit(f"{lang}: hero CTA2 replace failed ({n})")
    text = text2

    # Come funziona step 1 — first <p> inside first home-step
    text2, n = re.subn(
        r'(<li class="home-step">\s*<h3>[^<]+</h3>\s*<p>)[^<]+(</p>)',
        rf"\1{t['step1']}\2",
        text,
        count=1,
    )
    if n != 1:
        raise SystemExit(f"{lang}: step1 replace failed ({n})")
    text = text2

    # Categories section
    text2, n = re.subn(
        r'        <section class="home-categories"[\s\S]*?</section>',
        categories_block(lang, t),
        text,
        count=1,
    )
    if n != 1:
        raise SystemExit(f"{lang}: categories replace failed ({n})")
    text = text2

    # Bestsellers id
    text2, n = re.subn(
        r'<section id="catalogo" class="home-catalog"',
        '<section id="piu-venduti" class="home-catalog"',
        text,
        count=1,
    )
    if n != 1:
        raise SystemExit(f"{lang}: catalogo id replace failed ({n})")
    text = text2

    # Closing CTA
    old_close = CLOSING_CTA_OLD[lang]
    text2, n = re.subn(
        rf'(<a class="home-btn home-btn-primary" href="#)catalogo(">){re.escape(old_close)}(</a>)',
        rf'\1soluzioni\2{t["cta2"]}\3',
        text,
        count=1,
    )
    if n != 1:
        raise SystemExit(f"{lang}: closing CTA replace failed ({n})")
    text = text2

    path.write_text(text, encoding="utf-8")
    print("updated", lang)


def main() -> None:
    for lang in LANG:
        patch_lang(lang)


if __name__ == "__main__":
    main()
