#!/usr/bin/env python3
"""Port hand-written pages to nl/ from en/. Strips chrome; inserts hreflang nl.

USO UNA TANTUM — NON RIESEGUIRE. Serviva a creare le 12 pagine "a mano" di
`nl/` partendo da `en/`. Da allora quelle pagine sono state tradotte e rifinite
direttamente in HTML, e la tabella EN_NL qui sotto non le riproduce piu':
rilanciarlo su `nl/index.html` perderebbe ~140 frasi olandesi e ne
reintrodurrebbe ~100 in inglese, e ristripperebbe l'header/footer inline
(che va poi ricostruito con `node scripts/build-inline-chrome.mjs`).

Le 12 pagine sono ora sorgente: si modificano nei file `nl/*.html`. Le altre 67
pagine di `nl/` restano invece generate, da `scripts/generate-nl-only.py` piu'
le traduzioni in `scripts/nl_translations.py`.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HEADER_RE = re.compile(r"(<ecommerce-header\b[^>]*>)[\s\S]*?(</ecommerce-header>)", re.I)
FOOTER_RE = re.compile(r"(<ecommerce-footer\b[^>]*>)[\s\S]*?(</ecommerce-footer>)", re.I)

EN_NL = [
    # Residui trovati rileggendo le pagine portate: senza queste coppie
    # tornerebbero in inglese alla prossima esecuzione dello script.
    ("ESET NOD32 — 2 devices", "ESET NOD32 — 2 apparaten"),
    ("Stripe and PayPal", "Stripe en PayPal"),
    (">Security<", ">Beveiliging<"),
    (">12 months<", ">12 maanden<"),
    (">Up to 6<", ">Tot 6<"),
    ("Support:", "Ondersteuning:"),
    ("Skip to main content", "Naar de hoofdinhoud"),
    ("Complete your purchase securely at Eurolicenze.", "Rond uw aankoop veilig af bij Eurolicenze."),
    ("Your order has been received. Thank you for shopping at Eurolicenze.", "Uw bestelling is ontvangen. Bedankt voor uw aankoop bij Eurolicenze."),
    ("Shopping cart — Eurolicenze", "Winkelwagen — Eurolicenze"),
    ("Order confirmed — Eurolicenze", "Bestelling bevestigd — Eurolicenze"),
    ("Page not found — Eurolicenze", "Pagina niet gevonden — Eurolicenze"),
    ("The page you are looking for does not exist or has moved. Search for a product, browse the categories or go back to the Eurolicenze home page.",
     "De pagina die u zoekt bestaat niet of is verplaatst. Zoek een product, bekijk de categorieën of ga terug naar de homepage van Eurolicenze."),
    ("Privacy policy — Eurolicenze", "Privacybeleid — Eurolicenze"),
    ("Eurolicenze privacy policy: data controller, purposes, your rights under the GDPR, and contact details.",
     "Privacybeleid van Eurolicenze: verwerkingsverantwoordelijke, doeleinden, uw rechten onder de AVG en contactgegevens."),
    ("Cookie policy — Eurolicenze", "Cookiebeleid — Eurolicenze"),
    ("Terms and conditions — Eurolicenze", "Algemene voorwaarden — Eurolicenze"),
    ("Returns and refunds — Eurolicenze", "Retourneren en terugbetalingen — Eurolicenze"),
    ("Software consultation — Eurolicenze", "Softwareadvies — Eurolicenze"),
    ("Tell us about your software needs. Eurolicenze helps individuals, professionals and businesses identify suitable licences and solutions.",
     "Vertel ons wat u nodig hebt. Eurolicenze helpt particulieren, professionals en bedrijven bij het kiezen van geschikte licenties en oplossingen."),
    ("Your Cart", "Uw winkelwagen"),
    ("Review your software before the licences are sent instantly by email.",
     "Controleer uw software voordat de licenties per e-mail worden verzonden."),
    ("Your cart is empty.", "Uw winkelwagen is leeg."),
    ("Back to catalogue", "Terug naar de catalogus"),
    ("Software licence details", "Gegevens van de softwarelicentie"),
    ("Why buy from Eurolicenze with confidence", "Waarom u met vertrouwen bij Eurolicenze koopt"),
    ("Fast email delivery", "Snelle levering per e-mail"),
    ("Receive your official licence code and instructions within minutes of purchase.",
     "Ontvang uw officiële licentiecode en instructies binnen enkele minuten na aankoop."),
    ("Activation guarantee", "Activeringsgarantie"),
    ("Genuine licences: in case of activation issues, replacement or refund.",
     "Originele licenties: bij activeringsproblemen vervanging of terugbetaling."),
    ("Customer support", "Klantenservice"),
    ("Email and WhatsApp support for activation and installation.",
     "Ondersteuning via e-mail en WhatsApp voor activering en installatie."),
    ("Secure payments", "Veilige betalingen"),
    ("Transactions encrypted via official banking networks and PayPal.",
     "Transacties versleuteld via officiële banknetwerken en PayPal."),
    ("Order summary", "Besteloverzicht"),
    ("Products subtotal", "Subtotaal producten"),
    ("Checkout progress", "Checkoutvoortgang"),
    ("Step 1: Cart, completed", "Stap 1: Winkelwagen, voltooid"),
    ("Step 1: Cart, current step", "Stap 1: Winkelwagen, huidige stap"),
    ("Step 2: Checkout, not yet reached", "Stap 2: Checkout, nog niet bereikt"),
    ("Step 2: Checkout, current step", "Stap 2: Checkout, huidige stap"),
    ("Step 3: Confirmation, not yet reached", "Stap 3: Bevestiging, nog niet bereikt"),
    ("Confirmation", "Bevestiging"),
    ("Customer type", "Klanttype"),
    ("First name", "Voornaam"),
    ("Last name", "Achternaam"),
    ("Company name", "Bedrijfsnaam"),
    ("VAT number (Italian P.IVA)", "Btw-nummer (Italiaanse P.IVA)"),
    ("Shipping address", "Verzendadres"),
    ("Address (street and number)", "Adres (straat en huisnummer)"),
    ("Postal code", "Postcode"),
    ("State / Province", "Provincie / staat"),
    ("Payment method", "Betaalmethode"),
    ("Proceed to secure payment", "Doorgaan naar veilige betaling"),
    ("Confirm order", "Bestelling bevestigen"),
    ("required", "verplicht"),
    ("(optional)", "(optioneel)"),
    ("Digital delivery via email", "Digitale levering per e-mail"),
    ("Home delivery", "Levering aan huis"),
    ("Immediate digital delivery", "Directe digitale levering"),
    ("Shipping included", "Verzending inbegrepen"),
    ("data-label-remove=\"Remove\"", "data-label-remove=\"Verwijderen\""),
    ("data-qty-aria=\"Quantity\"", "data-qty-aria=\"Aantal\""),
    ("data-label-qty-minus=\"Decrease quantity for\"", "data-label-qty-minus=\"Aantal verlagen voor\""),
    ("data-label-qty-plus=\"Increase quantity for\"", "data-label-qty-plus=\"Aantal verhogen voor\""),
    ("data-label-item-singular=\"Item\"", "data-label-item-singular=\"Artikel\""),
    ("data-label-item-plural=\"Items\"", "data-label-item-plural=\"Artikelen\""),
    ("Privacy policy", "Privacybeleid"),
    ("Cookie policy", "Cookiebeleid"),
    ("Terms and conditions", "Algemene voorwaarden"),
    ("Returns and refunds", "Retourneren en terugbetalingen"),
    ("Software consultation", "Softwareadvies"),
    ("About us", "Over ons"),
]


def strip_chrome(html: str) -> str:
    html = HEADER_RE.sub(r"\1</ecommerce-header>", html)
    html = FOOTER_RE.sub(r"\1</ecommerce-footer>", html)
    return html


def remap(html: str, slug: str) -> str:
    html = html.replace('lang="en"', 'lang="nl"', 1)
    html = html.replace('content="en_US"', 'content="nl_NL"')
    html = html.replace('"inLanguage":"en"', '"inLanguage":"nl"')
    html = html.replace('"inLanguage": "en"', '"inLanguage": "nl"')
    html = html.replace(
        '["it","en","fr","de","es","pt"]',
        '["it","en","fr","de","es","pt","nl"]',
    )
    dest = f"https://eurolicenze.com/nl/{slug}" if slug else "https://eurolicenze.com/nl/"
    if 'hreflang="nl"' not in html:
        html = re.sub(
            r'(<link rel="alternate" hreflang="pt" href="https://eurolicenze\.com/pt/[^"]*">)\s*'
            r'(<link rel="alternate" hreflang="x-default")',
            rf'\1\n    <link rel="alternate" hreflang="nl" href="{dest}">\n    \2',
            html,
            count=1,
        )
    html = re.sub(
        r'(<link rel="canonical" href=")https://eurolicenze\.com/en/[^"]*(")',
        rf"\1{dest}\2",
        html,
        count=1,
    )
    html = html.replace("https://eurolicenze.com/en/" + (slug or ""), dest)
    html = html.replace('href="/en/', 'href="/nl/')
    html = html.replace("/nl/about-us", "/nl/over-ons")
    html = html.replace("/nl/consultation", "/nl/consultatie")
    return html


def apply_tr(html: str) -> str:
    for src, dst in sorted(EN_NL, key=lambda p: len(p[0]), reverse=True):
        html = html.replace(src, dst)
    # Congiunzione fra i due link legali del checkout: sta su righe separate,
    # con un'indentazione che non conviene fissare in una coppia EN_NL.
    html = re.sub(r"(</a>\s+)and(\s+<a\b)", r"\1en\2", html)
    return html


def port(src_name: str, dest_name: str, slug: str) -> None:
    src = ROOT / "en" / src_name
    dest = ROOT / "nl" / dest_name
    html = src.read_text(encoding="utf-8")
    html = strip_chrome(html)
    html = remap(html, slug)
    html = apply_tr(html)
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(html, encoding="utf-8", newline="\n")
    print("wrote", dest.relative_to(ROOT), dest.stat().st_size)


def main() -> None:
    jobs = [
        ("index.html", "index.html", ""),
        ("404.html", "404.html", "404"),
        ("cart.html", "cart.html", "cart"),
        ("checkout.html", "checkout.html", "checkout"),
        ("checkout-success.html", "checkout-success.html", "checkout-success"),
        ("privacy-policy.html", "privacy-policy.html", "privacy-policy"),
        ("cookie-policy.html", "cookie-policy.html", "cookie-policy"),
        ("terms-and-conditions.html", "terms-and-conditions.html", "terms-and-conditions"),
        ("returns-and-refunds.html", "returns-and-refunds.html", "returns-and-refunds"),
        ("consultation.html", "consultatie.html", "consultatie"),
        ("microsoft-365-solutions.html", "microsoft-365-solutions.html", "microsoft-365-solutions"),
        ("microsoft-365-family.html", "microsoft-365-family.html", "microsoft-365-family"),
    ]
    for src, dest, slug in jobs:
        port(src, dest, slug)


if __name__ == "__main__":
    main()
