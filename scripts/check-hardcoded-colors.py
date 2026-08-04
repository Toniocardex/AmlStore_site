#!/usr/bin/env python3
"""Guardrail anti-regressione: vieta nuovi colori hardcoded (hex/rgba) nei file
CSS del design system, fuori da page.css (dove vivono i token --aml-*).

Regole:
- Le dichiarazioni di custom property (`--nome: #hex;`) sono sempre ammesse:
  sono la definizione dei token, non un consumo hardcoded.
- I fallback dentro var(--token, #hex) sono ignorati: var() risolve sempre
  al token reale (sempre definito), il fallback e' inerte.
- Le righe con box-shadow/text-shadow sono ammesse: ombre ed elevazioni non
  sono mai il tipo di bug (testo illeggibile) che questo script cerca.
- Tutto il resto deve comparire nell'allowlist esplicita sotto (casi rivisti
  a mano: fasce sempre scure con testo bianco, badge/pulsanti con testo
  bianco su sfondo colorato, blu ufficiale PayPal, pannelli "glass" chiari).

Uso: eseguito insieme a validate-product-pages.py prima di ogni deploy.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGET_FILES = [
    "css/product-v3.css",
    "css/product-v2.css",
    "css/home.css",
    "css/cart.css",
    "css/checkout.css",
    "css/product.css",
    "css/microsoft-365-solutions.css",
]

COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)")
VAR_CALL_RE = re.compile(r"var\((?:[^()]|\([^()]*\))*\)")
CUSTOM_PROP_RE = re.compile(r"^--[\w-]+\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))\s*;?$")
SHADOW_LINE_RE = re.compile(r"(?:box-|text-|-webkit-box-)?shadow\s*:", re.IGNORECASE)

# Righe riviste a mano: colori intenzionali, non hardcoding "sfuggito".
# Chiave = percorso relativo, valore = insieme di righe (trimmed) ammesse.
ALLOWLIST = {
    "css/product-v3.css": {
        # Badge sconto: nascosto sitewide (.pdp-page .pdp-price-badge { display:none }),
        # colori mai visibili — codice morto innocuo, non vale il rischio di toccarlo.
        "background: rgba(6, 78, 59, 0.55);",
        "border: 1px solid rgba(6, 95, 70, 0.7);",
        "color: #34d399;",
        # Testo bianco su sfondo colorato (bottone/badge accent, cerchio step numerato)
        "color: #fff;",
        "color: #ffffff;",
        # Fascia navy sempre scura (.pdp-final / .pf-institutional): scelta editoriale
        # fissa, non un'inversione di tema — vedi commenti nel file.
        "color: rgba(255, 255, 255, 0.72);",
        "color: rgba(255, 255, 255, 0.55);",
        "border-inline-start: 2px solid rgba(255, 255, 255, 0.25);",
        # Didascalia "glass" chiara sopra la fascia lifestyle
        "background: rgba(255, 255, 255, 0.96);",
        # Bordo di accento decorativo sull'item FAQ aperto
        "border-color: #9eb9d7;",
    },
    "css/product-v2.css": {
        "background: rgba(255, 255, 255, 0.96);",
        ".bento-caption { background: rgba(255, 255, 255, 0.96); }",
        "background: rgba(255, 255, 255, 0.88);",
        "rgba(255, 255, 255, 0) 0%,",
        "rgba(255, 255, 255, 0.5) 48%,",
        "#ffffff 100%",
        "color: #fff;",
        "color: #ffffff;",
        # Zebra striping neutro (grigio, non un colore di tema)
        "background: rgba(127, 127, 127, 0.05);",
    },
    "css/home.css": {
        # Hero fotografico full-bleed: overlay scuro sempre presente sopra la foto,
        # non e' un residuo del tema scuro — vedi commento nel file.
        "background: #050505;",
        "rgba(5, 5, 5, 0.94) 0%,",
        "rgba(5, 5, 5, 0.78) 38%,",
        "rgba(5, 5, 5, 0.30) 65%,",
        "rgba(5, 5, 5, 0.08) 100%",
        "color: rgba(250, 250, 250, 0.65);",
        "background: rgba(250, 250, 250, 0.35);",
        "color: #fafafa;",
        "color: rgba(250, 250, 250, 0.78);",
        "background: rgba(255, 255, 255, 0.08);",
        "color: rgba(255, 255, 255, 0.90);",
        "border: 1px solid rgba(255, 255, 255, 0.22);",
        "background: rgba(255, 255, 255, 0.14);",
        "border-color: rgba(255, 255, 255, 0.32);",
        "background: rgba(5, 5, 5, 0.62);",
        "border-top: 1px solid rgba(255, 255, 255, 0.07);",
        "color: rgba(250, 250, 250, 0.80);",
        "border-left: 1px solid rgba(255, 255, 255, 0.1);",
        "background: rgba(5, 5, 5, 0.92);",
        # Card chiara (bianco -> grigio chiarissimo), non un bug di contrasto
        "background: linear-gradient(145deg, #ffffff 0%, #f4f4f5 100%);",
        # Testo bianco su icona/bottone colorato
        "color: #ffffff;",
        "color: #fff;",
        # Fascia navy sempre scura (.home-institutional), stesso pattern di
        # .pf-institutional sulle pagine prodotto — testo bianco intenzionale.
        "border-inline-start: 2px solid rgba(255, 255, 255, 0.25);",
        "color: rgba(255, 255, 255, 0.72);",
    },
    "css/cart.css": {
        # Testo/outline bianco sul bottone primario (sfondo accent) — vedi .cart-btn-primary
        "color: #ffffff;",
        "outline: 2px solid #ffffff;",
    },
    "css/checkout.css": {
        # Testo bianco su badge/bottone colorato
        "color: #fff;",
        "color: #ffffff;",
        # Blu ufficiale PayPal (brand color imposto dal loro design system)
        "background: #003087;",
        # Spinner di caricamento sul bottone accent: anello bianco traslucido
        "border: 2px solid rgba(255, 255, 255, 0.4);",
        "border-top-color: #fff;",
    },
    "css/product.css": {
        # Testo bianco sul bottone accent (.btn-primary)
        "color: #ffffff;",
        # Stato "aggiunto al carrello": verde di successo, non un colore di tema
        "background: linear-gradient(135deg, var(--pp-success) 0%, #059669 100%);",
        # Ombra della barra sticky quando visibile
        "0 14px 34px rgba(0, 0, 0, 0.09);",
    },
    "css/microsoft-365-solutions.css": {
        # Icona bianca sul badge navy delle path-card (.m365sol-path-icon)
        "color: #fff;",
    },
}


def strip_var_fallbacks(line: str) -> str:
    return VAR_CALL_RE.sub("", line)


def check_file(rel_path: str) -> list[str]:
    path = ROOT / rel_path
    if not path.exists():
        return [f"{rel_path}: file non trovato"]

    allowed = ALLOWLIST.get(rel_path, set())
    violations = []

    for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped or CUSTOM_PROP_RE.match(stripped):
            continue
        if SHADOW_LINE_RE.search(stripped):
            continue

        scanned = strip_var_fallbacks(stripped)
        if not COLOR_RE.search(scanned):
            continue
        if stripped in allowed:
            continue

        violations.append(f"{rel_path}:{lineno}: {stripped}")

    return violations


def main():
    all_violations = []
    for rel_path in TARGET_FILES:
        all_violations.extend(check_file(rel_path))

    if all_violations:
        print("HARDCODED COLOR CHECK FAILED:", len(all_violations), "issue(s)")
        for v in all_violations[:50]:
            print(" -", v)
        if len(all_violations) > 50:
            print(f" ... and {len(all_violations) - 50} more")
        print("\nSe il colore e' intenzionale (fascia sempre scura, testo bianco su")
        print("bottone accent, brand color di terzi...) aggiungilo all'ALLOWLIST in")
        print("scripts/check-hardcoded-colors.py con un commento che spiega perche'.")
        sys.exit(1)

    print("OK: nessun colore hardcoded fuori dall'allowlist")


if __name__ == "__main__":
    main()
