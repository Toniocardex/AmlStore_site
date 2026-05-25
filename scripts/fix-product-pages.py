#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FAMILY_FILES = list(ROOT.glob("*/microsoft-365-family.html"))
PERSONAL_FILES = list(ROOT.glob("*/microsoft-365-personal.html"))


def fix_family(text):
    text = text.replace('"sku": "microsoft-365-family-12m"', '"sku": "6GQ-00092"')
    text = text.replace('data-stripe-product-sku="microsoft-365-family-12m"', 'data-stripe-product-sku="6GQ-00092"')
    text = text.replace('data-stripe-unit-amount="9900"', 'data-stripe-unit-amount="10495"')
    text = text.replace('product-sticky-cta__sale">€ 99,00', 'product-sticky-cta__sale">€ 104,95')
    text = text.replace('v2-price-sale" aria-label="Prezzo scontato 99 euro">€ 99,00', 'v2-price-sale" aria-label="Prezzo scontato 104,95 euro">€ 104,95')
    text = text.replace('v2-price-sale" aria-label="Sale price 99 euros">€ 99.00', 'v2-price-sale" aria-label="Sale price 104.95 euros">€ 104.95')
    text = text.replace('v2-price-sale" aria-label="Prix réduit 99 euros">€ 99,00', 'v2-price-sale" aria-label="Prix réduit 104,95 euros">€ 104,95')
    text = text.replace('v2-price-sale" aria-label="Reduzierter Preis 99 Euro">€ 99,00', 'v2-price-sale" aria-label="Reduzierter Preis 104,95 Euro">€ 104,95')
    text = text.replace('v2-price-sale" aria-label="Precio rebajado 99 euros">€ 99,00', 'v2-price-sale" aria-label="Precio rebajado 104,95 euros">€ 104,95')
    text = text.replace('−23%', '−19%')
    text = text.replace('− 23%', '− 19%')
    text = text.replace('23%', '19%')  # risky - only in discount badge context
    text = text.replace('Risparmi <strong>€ 30</strong>', 'Risparmi <strong>€ 24,05</strong>')
    text = text.replace('Save <strong>€30</strong>', 'Save <strong>€24.05</strong>')
    return text


def fix_personal(text):
    text = text.replace('"sku": "microsoft-365-personal-12m"', '"sku": "QQ2-00012"')
    text = text.replace('data-stripe-product-sku="microsoft-365-personal-12m"', 'data-stripe-product-sku="QQ2-00012"')
    text = text.replace('data-stripe-unit-amount="7400"', 'data-stripe-unit-amount="7900"')
    text = text.replace('product-sticky-cta__sale">€ 74,00', 'product-sticky-cta__sale">€ 79,00')
    text = text.replace('v2-price-sale" aria-label="Prezzo scontato 74 euro">€ 74,00', 'v2-price-sale" aria-label="Prezzo scontato 79 euro">€ 79,00')
    text = text.replace('v2-price-sale" aria-label="Sale price 74 euros">€ 74.00', 'v2-price-sale" aria-label="Sale price 79 euros">€ 79.00')
    text = text.replace('v2-price-sale" aria-label="Prix réduit 74 euros">€ 74,00', 'v2-price-sale" aria-label="Prix réduit 79 euros">€ 79,00')
    text = text.replace('v2-price-sale" aria-label="Reduzierter Preis 74 Euro">€ 74,00', 'v2-price-sale" aria-label="Reduzierter Preis 79 Euro">€ 79,00')
    text = text.replace('v2-price-sale" aria-label="Precio rebajado 74 euros">€ 74,00', 'v2-price-sale" aria-label="Precio rebajado 79 euros">€ 79,00')
    text = text.replace('−25%', '−20%')
    text = text.replace('Risparmi <strong>€ 25</strong>', 'Risparmi <strong>€ 20</strong>')
    text = text.replace('Save <strong>€25</strong>', 'Save <strong>€20</strong>')
    text = text.replace('Économisez <strong>25 €</strong>', 'Économisez <strong>20 €</strong>')
    text = text.replace('Sparen Sie <strong>25 €</strong>', 'Sparen Sie <strong>20 €</strong>')
    text = text.replace('Ahorra <strong>25 €</strong>', 'Ahorra <strong>20 €</strong>')
    return text


def main():
    for p in FAMILY_FILES:
        t = p.read_text(encoding="utf-8")
        p.write_text(fix_family(t), encoding="utf-8")
        print("family", p)
    for p in PERSONAL_FILES:
        t = p.read_text(encoding="utf-8")
        p.write_text(fix_personal(t), encoding="utf-8")
        print("personal", p)
    for lang in ("it", "en", "fr", "de", "es"):
        p = ROOT / lang / "index.html"
        t = p.read_text(encoding="utf-8")
        t = fix_family(fix_personal(t))
        p.write_text(t, encoding="utf-8")
        print("index", p)


if __name__ == "__main__":
    main()
