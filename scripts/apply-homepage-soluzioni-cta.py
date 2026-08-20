#!/usr/bin/env python3
"""Apply homepage CTA/soluzioni plan to it|en|fr|de|es index.html."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# SVG icons reused from existing tiles
ICON_WIN = '<svg viewBox="0 0 14 14" fill="currentColor"><path d="m 5.91827,7.331731 v 4.694712 L 1,11.348557 V 7.331731 h 4.91827 z m 0,-5.358174 V 6.725962 H 1 V 2.651443 z M 13,7.331731 V 13 L 6.45913,12.098557 V 7.331731 H 13 z M 13,1 V 6.725962 H 6.45913 V 1.901443 z"></path></svg>'
ICON_OFFICE = '<svg viewBox="0 0 50 50" fill="currentColor"><path d="M43 11.11v27.6c0 2.54-1.73 4.77-4.21 5.43l-8.63 2.41c.5-.94.78-2.02.78-3.16V5.65c0-.86-.19-1.68-.53-2.42l8.45 2.47C41.29 6.37 43 8.6 43 11.11zM28.94 37v6.39c0 1.99-1.19 3.72-2.96 4.33-.43.1-.87.15-1.31.15-1 0-2-.26-2.92-.76L13.45 42c-1.04-.64-1.52-1.86-1.19-3.04.33-1.17 1.38-1.96 2.6-1.96H28.94zM28.94 5.65v5.72l-10.28 3.64c-.99.36-1.66 1.3-1.66 2.36v13.36c0 1.09-.59 2.1-1.54 2.62l-4.07 2.27C10.94 35.88 10.44 36 9.95 36c-.51 0-1.03-.14-1.49-.41C7.54 35.05 7 34.1 7 33.05V14.83c0-1.93 1.04-3.72 2.72-4.68L22.8 2.71c1.08-.61 2.28-.83 3.45-.65.07.06.16.11.26.14C27.72 2.6 28.94 3.82 28.94 5.65z"></path></svg>'
ICON_M365 = '<svg viewBox="0 0 50 50" fill="currentColor"><path d="M20.13,32.5c-2.79-1.69-4.53-4.77-4.53-8.04V8.9c0-1.63,0.39-3.19,1.11-4.57L7.54,9.88C4.74,11.57,3,14.65,3,17.92v14.15c0,1.59,0.42,3.14,1.16,4.5c0.69,1.12,1.67,2.06,2.88,2.74c2.53,1.42,5.51,1.36,7.98-0.15l8.02-4.9L20.13,32.5z M42.84,27.14l-8.44-5.05v2.29c0,3.25-1.72,6.33-4.49,8.02l-13.84,8.47c-1.52,0.93-3.19,1.42-4.87,1.46l8.93,5.41c1.5,0.91,3.19,1.36,4.87,1.36s3.37-0.45,4.87-1.36l9.08-5.5l3.52-2.13c0.27-0.16,0.53-0.34,0.78-0.54c0.08-0.05,0.16-0.11,0.23-0.16c0.65-0.53,1.23-1.13,1.71-1.79c0.02-0.03,0.04-0.06,0.06-0.09c0.77-1.19,1.2-2.59,1.19-4.06C46.43,30.85,45.09,28.48,42.84,27.14z M42.46,9.88l-9.57-5.79l-3.02-1.83C29.45,2,29.01,1.79,28.56,1.61c-0.49-0.21-1-0.37-1.51-0.47c-1.84-0.38-3.76-0.08-5.46,0.89c-2.5,1.43-3.99,3.99-3.99,6.87v9.6l2.8-1.65c2.84-1.67,6.36-1.66,9.19,0.03l14.28,8.54c1.29,0.78,2.35,1.81,3.12,3.02L47,17.92C47,14.65,45.26,11.57,42.46,9.88z"></path></svg>'
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
