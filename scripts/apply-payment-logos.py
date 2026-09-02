#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia sulla migrazione della nota pagamenti (una tantum, gia' esaurita).

RITIRATO: questo script non modifica piu' le pagine.

Non condivideva il difetto degli altri regen-*: non chiamava mai
build_product_page(), faceva una sostituzione mirata dentro l'HTML esistente
(.pf-pay-note -> .pdp-pay) e lo diceva gia' nel suo docstring. Il motivo per cui
va in pensione e' un altro: non ha piu' niente da fare, e il suo unico effetto
possibile ormai sarebbe un danno.

  - `.pf-pay-note`, la sua sorgente, non compare piu' su nessuna delle pagine
    del sito: la migrazione e' andata a termine (commit d92ad113, 309 pagine);
  - `.pdp-pay`, la sua destinazione, non c'e' piu' nemmeno lei: quell'area della
    buy card e' stata rifatta e oggi ospita il blocco PayPal Express
    (.pdp-paypal-express, reso da product_page_lib._render_paypal_express);
  - di conseguenza il suo BLOCK_RE non combacia con nulla. L'unico esito
    raggiungibile era `pagine aggiornate: 0`;
  - e girava solo su it/en/fr/de/es: pt e nl non erano mai coperte.

_render_payment_logos() in product_page_lib.py aveva qui il suo unico chiamante:
ora e' codice morto ed e' un candidato alla rimozione, insieme alle chiavi
`payments_aria` / loghi in V3_UI se non le usa nessun altro.

Quel che lo script fa ancora, e per cui va tenuto: verifica che la migrazione
resti chiusa in entrambe le direzioni -- nessuna pagina e' tornata alla nota
testuale, e nessuna espone il blocco loghi ormai sostituito. Senza effetti
collaterali, non scrive nulla.

    python scripts/apply-payment-logos.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from page_pipeline_guard import fail_if  # noqa: E402
from product_page_lib import LANGS  # noqa: E402

# (marcatore, perche' non deve esserci)
OBSOLETE = (
    ('class="pf-pay-note"', "nota pagamenti testuale, sostituita nel commit d92ad113"),
    ('class="pdp-pay"', "blocco loghi pagamenti, sostituito dal blocco PayPal Express"),
)


def main():
    errors = []
    checked = 0
    for lang in LANGS:
        for path in sorted((ROOT / lang).glob("*.html")):
            checked += 1
            src = path.read_text(encoding="utf-8")
            for marker, why in OBSOLETE:
                if marker in src:
                    errors.append(f"{lang}/{path.name}: {marker} e' ricomparso -- {why}")

    fail_if(errors, f"OK: {checked} pagine, nessun residuo della nota pagamenti")


if __name__ == "__main__":
    main()
