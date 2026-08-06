#!/usr/bin/env python3
"""Apply pre-campaign buy-card + copy fixes (one-shot)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OFFICE = {
    "en": {
        "price_old": "Tax included. No shipping fees. You save <strong>€ 120,00</strong> versus the list price (€ 299,00).",
        "price_new": "Tax included. No shipping fees. You save <strong>€ 120,00</strong> versus Microsoft Store (EU) (€ 299,00).",
        "meta_aria": "Licence details",
        "meta": '<strong>Activation region</strong> European Union / EEA',
        "trust": "VAT included · Business invoice available · Secure payment · Email delivery · Activation support",
    },
    "it": {
        "price_old": "Tasse incluse. Nessun costo di spedizione. Risparmi <strong>€ 120,00</strong> rispetto al prezzo di listino (€ 299,00).",
        "price_new": "Tasse incluse. Nessun costo di spedizione. Risparmi <strong>€ 120,00</strong> rispetto al Microsoft Store (UE) (€ 299,00).",
        "meta_aria": "Dettagli licenza",
        "meta": "<strong>Regione di attivazione</strong> Unione Europea / SEE",
        "trust": "IVA inclusa · Fattura per aziende · Pagamento sicuro · Consegna email · Supporto attivazione",
    },
    "fr": {
        "price_old": "Taxes incluses. Pas de frais de port. Vous économisez <strong>€ 120,00</strong> par rapport au prix catalogue (€ 299,00).",
        "price_new": "Taxes incluses. Pas de frais de port. Vous économisez <strong>€ 120,00</strong> par rapport au Microsoft Store (UE) (€ 299,00).",
        "meta_aria": "Détails de la licence",
        "meta": "<strong>Zone d'activation</strong> Union européenne / EEE",
        "trust": "TVA incluse · Facture entreprise · Paiement sécurisé · Livraison e-mail · Aide à l'activation",
    },
    "de": {
        "price_old": "Steuern inklusive. Keine Versandkosten. Sie sparen <strong>€ 120,00</strong> gegenüber dem Listenpreis (€ 299,00).",
        "price_new": "Steuern inklusive. Keine Versandkosten. Sie sparen <strong>€ 120,00</strong> gegenüber Microsoft Store (EU) (€ 299,00).",
        "meta_aria": "Lizenzdetails",
        "meta": "<strong>Aktivierungsregion</strong> Europäische Union / EWR",
        "trust": "MwSt. inkl. · Firmenrechnung · Sichere Zahlung · E-Mail-Lieferung · Aktivierungs-Support",
    },
    "es": {
        "price_old": "Impuestos incluidos. Sin gastos de envío. Ahorras <strong>€ 120,00</strong> respecto al precio de lista (€ 299,00).",
        "price_new": "Impuestos incluidos. Sin gastos de envío. Ahorras <strong>€ 120,00</strong> respecto al Microsoft Store (UE) (€ 299,00).",
        "meta_aria": "Detalles de la licencia",
        "meta": "<strong>Región de activación</strong> Unión Europea / EEE",
        "trust": "IVA incluido · Factura empresas · Pago seguro · Entrega por email · Soporte de activación",
    },
}

FAMILY_PRICE = {
    "en": (
        "Tax included. No shipping fees. You save <strong>€ 24,05</strong> versus the Microsoft Store (€ 129,00).",
        "Tax included. No shipping fees. You save <strong>€ 24,05</strong> versus Microsoft Store (EU) (€ 129,00).",
    ),
    "it": (
        "IVA inclusa, nessun costo di spedizione. Risparmi <strong>€ 24,05</strong> rispetto al Microsoft Store (€ 129,00).",
        "IVA inclusa, nessun costo di spedizione. Risparmi <strong>€ 24,05</strong> rispetto al Microsoft Store (UE) (€ 129,00).",
    ),
    "fr": (
        "TVA incluse, aucun frais de livraison. Vous économisez <strong>€ 24,05</strong> par rapport au Microsoft Store (€ 129,00).",
        "TVA incluse, aucun frais de livraison. Vous économisez <strong>€ 24,05</strong> par rapport au Microsoft Store (UE) (€ 129,00).",
    ),
    "de": (
        "Steuern inklusive. Keine Versandkosten. Sie sparen <strong>€ 24,05</strong> gegenüber dem Microsoft Store (€ 129,00).",
        "Steuern inklusive. Keine Versandkosten. Sie sparen <strong>€ 24,05</strong> gegenüber Microsoft Store (EU) (€ 129,00).",
    ),
    "es": (
        "Impuestos incluidos. Sin gastos de envío. Ahorras <strong>€ 24,05</strong> respecto a Microsoft Store (€ 129,00).",
        "Impuestos incluidos. Sin gastos de envío. Ahorras <strong>€ 24,05</strong> respecto al Microsoft Store (UE) (€ 129,00).",
    ),
}

FAMILY_SPEC = {
    "en": ('<tr><th scope="row">Billing</th>',
           '<tr><th scope="row">Activation region</th><td>European Union / EEA</td></tr>\n                        <tr><th scope="row">Billing</th>'),
    "it": ('<tr><th scope="row">Fatturazione</th>',
           '<tr><th scope="row">Regione di attivazione</th><td>Unione Europea / SEE</td></tr>\n                        <tr><th scope="row">Fatturazione</th>'),
    "fr": ('<tr><th scope="row">Facturation</th>',
           '<tr><th scope="row">Zone d\'activation</th><td>Union européenne / EEE</td></tr>\n                        <tr><th scope="row">Facturation</th>'),
    "de": ('<tr><th scope="row">Abrechnung</th>',
           '<tr><th scope="row">Aktivierungsregion</th><td>Europäische Union / EWR</td></tr>\n                        <tr><th scope="row">Abrechnung</th>'),
    "es": ('<tr><th scope="row">Facturación</th>',
           '<tr><th scope="row">Región de activación</th><td>Unión Europea / EEE</td></tr>\n                        <tr><th scope="row">Facturación</th>'),
}

# Detect family billing row keys if FR/DE/ES differ
FAMILY_SPEC_FALLBACK_SEARCH = {
    "fr": ["Facturation", "Fatturazione", "Billing"],
    "de": ["Abrechnung", "Fakturierung", "Billing", "Fatturazione"],
    "es": ["Facturación", "Billing", "Fatturazione"],
}


def inject_buy_card(html: str, loc: dict) -> str:
    if "pdp-meta-row" in html:
        return html  # already done
    note = f'<p class="pdp-price-note">{loc["price_old"]}</p>'
    note_new = f'<p class="pdp-price-note">{loc["price_new"]}</p>'
    if note not in html:
        raise SystemExit(f"price note not found for locale content: {loc['price_old'][:40]}...")
    meta = (
        f'{note_new}\n\n'
        f'                <p class="pdp-meta-row" role="group" aria-label="{loc["meta_aria"]}">\n'
        f'                    <span class="pdp-meta-chip">{loc["meta"]}</span>\n'
        f'                </p>'
    )
    html = html.replace(note, meta, 1)

    # Insert trust line after primary CTA button closing tag, before delivery
    marker = 'id="product-primary-cta"'
    idx = html.find(marker)
    if idx < 0:
        raise SystemExit("product-primary-cta not found")
    # Find end of this button
    end_btn = html.find("</button>", idx)
    if end_btn < 0:
        raise SystemExit("cta button end not found")
    end_btn += len("</button>")
    trust = (
        f'\n\n                <p class="pdp-trust-line">{loc["trust"]}</p>'
    )
    html = html[:end_btn] + trust + html[end_btn:]
    return html


def fix_office(lang: str) -> None:
    path = ROOT / lang / "office-2024-home-business.html"
    text = path.read_text(encoding="utf-8")
    text = inject_buy_card(text, OFFICE[lang])
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"office {lang}: ok")


def fix_family(lang: str) -> None:
    path = ROOT / lang / "microsoft-365-family.html"
    text = path.read_text(encoding="utf-8")
    loc = dict(OFFICE[lang])  # meta/trust/aria same
    old_p, new_p = FAMILY_PRICE[lang]
    loc["price_old"] = old_p
    loc["price_new"] = new_p
    text = inject_buy_card(text, loc)

    # Specs row
    if "Activation region" not in text and "Regione di attivazione" not in text and "Zone d'activation" not in text and "Aktivierungsregion" not in text and "Región de activación" not in text:
        needle, repl = FAMILY_SPEC[lang]
        if needle not in text:
            # try fallbacks for translated billing label
            found = False
            for label in FAMILY_SPEC_FALLBACK_SEARCH.get(lang, []):
                n = f'<tr><th scope="row">{label}</th>'
                if n in text:
                    text = text.replace(
                        n,
                        f'<tr><th scope="row">{loc["meta"].split("</strong>")[0].replace("<strong>", "")}</th><td>{loc["meta"].split("</strong>", 1)[1].strip()}</td></tr>\n                        ' + n,
                        1,
                    )
                    found = True
                    break
            if not found:
                # Insert before last row of specs table - look for Codice prodotto / Product code
                for code_label in ("Product code", "Codice prodotto", "Code produit", "Produktcode", "Código de producto"):
                    n = f'<tr><th scope="row">{code_label}</th>'
                    if n in text:
                        region_label = loc["meta"].split("</strong>")[0].replace("<strong>", "").strip()
                        region_val = loc["meta"].split("</strong>", 1)[1].strip()
                        text = text.replace(
                            n,
                            f'<tr><th scope="row">{region_label}</th><td>{region_val}</td></tr>\n                        {n}',
                            1,
                        )
                        found = True
                        break
                if not found:
                    raise SystemExit(f"family specs insert failed for {lang}")
        else:
            text = text.replace(needle, repl, 1)

    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"family {lang}: ok")


def main() -> None:
    for lang in ("en", "it", "fr", "de", "es"):
        fix_office(lang)
        fix_family(lang)


if __name__ == "__main__":
    main()
