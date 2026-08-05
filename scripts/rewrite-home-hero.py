#!/usr/bin/env python3
"""Update homepage heroes: corporate navy + 3 B2B product covers."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HEROES = {
    "it": {
        "h1": "Licensing per aziende<br>e professionisti.",
        "sub": "Consulenza, acquisto e attivazione con fatturazione italiana e assistenza dedicata — senza complessità inutili.",
        "cta1_href": "consulenza",
        "cta1": "Richiedi una consulenza",
        "cta2": "Esplora le soluzioni",
        "products_aria": "Esempi di prodotti business",
        "p1_alt": "Microsoft 365 Business Standard",
        "p2_alt": "Office 2024 Home & Business",
        "p3_alt": "Windows Server 2025 Standard",
    },
    "en": {
        "h1": "Licensing for businesses<br>and professionals.",
        "sub": "Advisory, purchase and activation with Italian invoicing and dedicated support — without unnecessary complexity.",
        "cta1_href": "consultation",
        "cta1": "Request a consultation",
        "cta2": "Explore solutions",
        "products_aria": "Business product examples",
        "p1_alt": "Microsoft 365 Business Standard",
        "p2_alt": "Office 2024 Home & Business",
        "p3_alt": "Windows Server 2025 Standard",
    },
    "fr": {
        "h1": "Licensing pour entreprises<br>et professionnels.",
        "sub": "Conseil, achat et activation avec facturation et accompagnement dédié — sans complexité inutile.",
        "cta1_href": "consultation",
        "cta1": "Demander une consultation",
        "cta2": "Découvrir les solutions",
        "products_aria": "Exemples de produits professionnels",
        "p1_alt": "Microsoft 365 Business Standard",
        "p2_alt": "Office 2024 Home & Business",
        "p3_alt": "Windows Server 2025 Standard",
    },
    "de": {
        "h1": "Licensing für Unternehmen<br>und Freiberufler.",
        "sub": "Beratung, Kauf und Aktivierung mit Rechnung und persönlicher Betreuung — ohne unnötige Komplexität.",
        "cta1_href": "beratung",
        "cta1": "Beratung anfragen",
        "cta2": "Lösungen entdecken",
        "products_aria": "Beispiele für Business-Produkte",
        "p1_alt": "Microsoft 365 Business Standard",
        "p2_alt": "Office 2024 Home & Business",
        "p3_alt": "Windows Server 2025 Standard",
    },
    "es": {
        "h1": "Licensing para empresas<br>y profesionales.",
        "sub": "Asesoramiento, compra y activación con facturación y asistencia dedicada — sin complejidad innecesaria.",
        "cta1_href": "consultoria",
        "cta1": "Solicitar asesoramiento",
        "cta2": "Explorar las soluciones",
        "products_aria": "Ejemplos de productos business",
        "p1_alt": "Microsoft 365 Business Standard",
        "p2_alt": "Office 2024 Home & Business",
        "p3_alt": "Windows Server 2025 Standard",
    },
}


def hero_html(t: dict[str, str]) -> str:
    return f"""        <section class="home-hero home-hero--corporate" aria-labelledby="home-hero-title">
            <div class="home-hero-inner">
                <div class="home-hero-content">
                    <h1 id="home-hero-title" class="home-hero-title">{t['h1']}</h1>
                    <p class="home-hero-subtitle">{t['sub']}</p>
                    <div class="home-hero-actions">
                        <a class="home-btn home-btn-primary" href="{t['cta1_href']}">{t['cta1']}</a>
                        <a class="home-btn home-btn-ghost" href="#soluzioni">{t['cta2']}</a>
                    </div>
                </div>
                <div class="home-hero-products" role="group" aria-label="{t['products_aria']}">
                    <a class="home-hero-product home-hero-product--back" href="windows-server-2025">
                        <img src="../asset/media/products/windows-server-2025.webp" width="400" height="400" alt="{t['p3_alt']}" decoding="async">
                    </a>
                    <a class="home-hero-product home-hero-product--mid" href="office-2024-home-business">
                        <img src="../asset/media/products/office-2024-home-business.webp" width="400" height="400" alt="{t['p2_alt']}" decoding="async">
                    </a>
                    <a class="home-hero-product home-hero-product--front" href="microsoft-365-business-standard">
                        <img src="../asset/media/products/microsoft-365-business-standard.webp" width="400" height="400" alt="{t['p1_alt']}" decoding="async" fetchpriority="high">
                    </a>
                </div>
            </div>
        </section>"""


def main() -> None:
    for lang, t in HEROES.items():
        path = ROOT / lang / "index.html"
        text = path.read_text(encoding="utf-8")
        text2, n = re.subn(
            r'        <section class="home-hero home-hero--corporate"[\s\S]*?</section>',
            hero_html(t),
            text,
            count=1,
        )
        if n != 1:
            raise SystemExit(f"hero replace failed for {lang}: matches={n}")
        path.write_text(text2, encoding="utf-8")
        print("updated", lang)


if __name__ == "__main__":
    main()
