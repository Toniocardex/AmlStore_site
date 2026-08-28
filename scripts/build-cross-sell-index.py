#!/usr/bin/env python3
"""Genera asset/cross-sell/{lang}.json — indice prodotti per il motore di cross-sell del carrello.

Da rieseguire manualmente ogni volta che cambiano pagine prodotto o prezzi
(nessun hook/CI nel repo, stesso spirito manuale di build-search-index.py e
bump-asset-version.py — vedi promemoria in GO-LIVE.md).

Fonte autoritativa dei dati mostrati: il blocco JSON-LD Product di ogni pagina
prodotto (gia' tradotto per lingua, gia' allineato al prezzo a video), come
build-search-index.py. catalog.json entra solo con join sullo SKU per la
categoria merceologica e il tipo di licenza, che il motore usa per le regole
di affinita'. Il markup della PDP fornisce il badge specifiche e il flag
`data-physical`, cioe' esattamente cio' che la riga di carrello mostra.

    python scripts/build-cross-sell-index.py
    python scripts/build-cross-sell-index.py --langs it en
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es", "pt", "nl")
OUT_DIR = ROOT / "asset" / "cross-sell"
SITE_PREFIX = "https://eurolicenze.com"

# Pagine non-prodotto — stesso set di build-search-index.py
SKIP_UTILITY = {
    "index", "cart", "checkout", "checkout-success", "account",
    "privacy-policy", "cookie-policy", "terms-and-conditions",
    "returns-and-refunds", "microsoft-365-solutions",
    "404", "chi-siamo", "about-us", "qui-sommes-nous", "ueber-uns",
    "quienes-somos", "sobre-nos", "over-ons",
    "consulenza", "consultation", "beratung", "consultoria",
    "consultatie", "contacts",
}
SKIP_CATEGORY = {
    "sistemi-operativi", "suite-office", "antivirus",
    "windows-server", "strumenti", "pacchetti",
}
# Pagine di confronto SEO (wave 1): editoriali, stesso slug in tutte le lingue.
SKIP_COMPARE = {
    "kaspersky-vs-eset-nod32", "microsoft-365-family-vs-personal",
    "norton-vs-bitdefender", "office-2024-vs-microsoft-365",
    "windows-11-home-vs-pro",
}
SKIP = SKIP_UTILITY | SKIP_CATEGORY | SKIP_COMPARE

JSONLD_RE = re.compile(
    r'<script type="application/ld\+json">\s*(.*?)\s*</script>', re.DOTALL
)
BADGE_RE = re.compile(r'<span class="pdp-badge">(.*?)</span>', re.DOTALL)
PHYSICAL_RE = re.compile(r'data-physical="true"')
TAG_RE = re.compile(r"<[^>]+>")

# categoria catalog.json -> "famiglia di bisogno". Il motore di cross-sell
# ragiona per famiglia: un carrello non deve mai ricevere il suggerimento di
# un secondo prodotto della famiglia che gia' contiene.
FAMILY_BY_CATEGORY = {
    "antivirus": "antivirus",
    "backup": "backup",
    "multimedia > photoediting": "multimedia",
    "sistema operativo > windows": "windows",
    "sistema operativo > windows > microsoft windows 11": "windows",
    "sistema operativo > windows server": "server",
    "suite office": "office",
    "suite office > microsoft 365": "m365",
    "suite office > microsoft office 2024": "office",
    "suite office > microsoft project 2024": "tools",
    "tool ufficio": "tools",
}
FAMILY_DEFAULT = "tools"

# Prodotti a fine supporto: restano in vendita sulla loro pagina, ma il carrello
# non li propone come add-on — dentro una famiglia vince il piu' economico, e
# senza questa marcatura Windows 10 Home (39,13) scavalcherebbe sempre Windows 11
# Home (61,00) come suggerimento a chi compra Office.
# Elenco volutamente minimo: estenderlo (Office 2019, 2021...) e' una scelta
# commerciale, non tecnica.
LEGACY_SLUGS = {
    "windows-10-home",
    "windows-10-pro",
}


def load_catalog_by_sku():
    data = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    return {(p.get("sku") or "").strip(): p for p in data if (p.get("sku") or "").strip()}


def find_node(graph, type_name):
    for node in graph:
        if node.get("@type") == type_name:
            return node
    return None


def relative_url(url):
    if not url:
        return ""
    return url[len(SITE_PREFIX):] if url.startswith(SITE_PREFIX) else url


def first_badge(text):
    m = BADGE_RE.search(text)
    if not m:
        return ""
    return re.sub(r"\s+", " ", html.unescape(TAG_RE.sub("", m.group(1)))).strip()


def extract_entry(html_path, catalog_by_sku):
    text = html_path.read_text(encoding="utf-8")
    m = JSONLD_RE.search(text)
    if not m:
        raise ValueError(f"nessun blocco JSON-LD trovato in {html_path}")
    graph = json.loads(m.group(1)).get("@graph", [])
    product = find_node(graph, "Product")
    if not product:
        raise ValueError(f"nessun nodo Product nel JSON-LD di {html_path}")

    sku = (product.get("sku") or "").strip()
    if not sku:
        raise ValueError(f"sku mancante nel JSON-LD di {html_path}")

    offers = product.get("offers") or {}
    price = offers.get("price")
    if price is None:
        raise ValueError(f"offers.price mancante in {html_path}")

    catalog = catalog_by_sku.get(sku) or {}
    category = (catalog.get("category") or "").strip()
    compare_at = catalog.get("compareAtMinor")
    price_minor = round(float(price) * 100)

    entry = {
        "sku": sku,
        "slug": html_path.stem,
        "name": product.get("name") or html_path.stem,
        "image": relative_url(product.get("image")),
        "priceMinor": price_minor,
        "currency": offers.get("priceCurrency") or "EUR",
        "family": FAMILY_BY_CATEGORY.get(category, FAMILY_DEFAULT),
        "type": (catalog.get("type") or "perpetual").strip(),
        "specs": first_badge(text),
    }
    # Campi opzionali: presenti solo quando aggiungono informazione, cosi' il
    # JSON scaricato dal browser resta piccolo.
    if isinstance(compare_at, int) and compare_at > price_minor:
        entry["compareAtMinor"] = compare_at
    if PHYSICAL_RE.search(text):
        entry["physical"] = True
    # I bundle contengono gia' due prodotti: come add-on sovrappongono cio' che
    # il carrello ha (la categoria del bundle e' quella del prodotto di testa,
    # non racconta il secondo). Il motore li esclude dai candidati.
    if entry["type"] == "bundle" or html_path.stem.startswith("bundle-"):
        entry["bundle"] = True
    if html_path.stem in LEGACY_SLUGS:
        entry["legacy"] = True
    return entry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--langs", nargs="+", choices=LANGS, default=list(LANGS))
    args = parser.parse_args()

    errors = []
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    catalog_by_sku = load_catalog_by_sku()

    for lang in args.langs:
        entries = []
        for html_path in sorted((ROOT / lang).glob("*.html")):
            if html_path.stem in SKIP:
                continue
            try:
                entry = extract_entry(html_path, catalog_by_sku)
            except ValueError as e:
                errors.append(str(e))
                continue
            entries.append(entry)
            # Il badge specifiche e' l'unico campo che, mancando, degraderebbe le
            # card in silenzio invece di fare fallire la build: le pipeline di
            # rigenerazione PDP perdono le patch applicate a mano, e un badge
            # rinominato azzererebbe le specifiche in tutte e 7 le lingue senza
            # che nulla lo segnali. Il prodotto resta nell'indice, ma lo script
            # esce != 0.
            if not entry["specs"]:
                errors.append(f"badge specifiche (.pdp-badge) mancante in {html_path}")

        out_path = OUT_DIR / f"{lang}.json"
        out_path.write_text(
            json.dumps(entries, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
            newline="\n",
        )
        print(f"{lang}: {len(entries)} prodotti -> {out_path.relative_to(ROOT)}")

    if errors:
        print(f"\nERRORI: {len(errors)}")
        for e in errors[:30]:
            print(" -", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
