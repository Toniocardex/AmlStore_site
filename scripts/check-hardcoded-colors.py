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
    "css/product-pdp.css",
    "css/home.css",
    "css/cart.css",
    "css/checkout.css",
    "css/product.css",
    "css/microsoft-365-solutions.css",
]

COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)")
VAR_CALL_RE = re.compile(r"var\((?:[^()]|\([^()]*\))*\)")
CUSTOM_PROP_RE = re.compile(r"^--[\w-]+\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))\s*;?$")
# Le ombre sono ammesse col nero/rgba letterale: non sono colori di tema, sono
# profondita'. `filter: drop-shadow(...)` e' la stessa cosa applicata a un PNG
# ritagliato (l'immagine prodotto nell'hero), quindi rientra nella stessa regola.
SHADOW_LINE_RE = re.compile(
    r"(?:box-|text-|-webkit-box-)?shadow\s*:|filter\s*:[^;]*drop-shadow\(", re.IGNORECASE
)

# Ridefinizione di un token GLOBALE con un colore letterale, fuori da page.css.
# Sintatticamente e' una dichiarazione di custom property, quindi la regola
# "le definizioni di token sono sempre ammesse" la lasciava passare — ma qui
# non si sta definendo un token: si sta schermando quello globale con un
# literal, e da quel momento il file smette di seguire il design system.
# E' esattamente cosi' che le PDP sono rimaste blu dopo il passaggio del
# brand all'arancione: .pdp-page ridichiarava --page-accent: #3267AC.
GLOBAL_TOKEN_SHADOW_RE = re.compile(
    r"^--(?:aml|page|pdp)-[\w-]+\s*:\s*(?:#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))\s*;?$"
)
TOKEN_SOURCE_FILE = "css/page.css"

# Righe riviste a mano: colori intenzionali, non hardcoding "sfuggito".
# Chiave = percorso relativo, valore = insieme di righe (trimmed) ammesse.
ALLOWLIST = {
    # product-v2.css e product-v3.css sono confluiti in product-pdp.css:
    # le due allowlist sono state unite qui sotto.
    "css/product-pdp.css": {
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
        # ── ex product-v2.css ──
        ".bento-caption { background: rgba(255, 255, 255, 0.96); }",
        "background: rgba(255, 255, 255, 0.88);",
        "rgba(255, 255, 255, 0) 0%,",
        "rgba(255, 255, 255, 0.5) 48%,",
        "#ffffff 100%",
        # Zebra striping neutro (grigio, non un colore di tema)
        "background: rgba(127, 127, 127, 0.05);",
        # Stelle di valutazione (.pdp-reviews__stars): l'ambra/oro delle stelle
        # e' una convenzione universale dei sistemi di recensione (Trustpilot
        # compreso), indipendente dalla palette del brand — non un accento
        # arancione mascherato.
        "color: #FBBF24;",
        # Verde ufficiale Trustpilot (".pdp-reviews__tp", stelle del riepilogo
        # aggregato): identita' del brand esterno, come il blu PayPal sotto —
        # non fa parte della nostra palette e non deve seguirne i token.
        "color: #059669;",
        "color: #10B981;",
    },
    "css/home.css": {
        # Testo bianco su icona/bottone colorato
        "color: #ffffff;",
        "color: #fff;",
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

    is_token_source = rel_path.replace("\\", "/") == TOKEN_SOURCE_FILE

    for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped:
            continue

        if not is_token_source and GLOBAL_TOKEN_SHADOW_RE.match(stripped):
            if stripped not in allowed:
                violations.append(
                    f"{rel_path}:{lineno}: token globale ridefinito con un literal "
                    f"(usa var(--aml-*) o aggiungi il token in {TOKEN_SOURCE_FILE}): {stripped}"
                )
            continue

        if CUSTOM_PROP_RE.match(stripped):
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
