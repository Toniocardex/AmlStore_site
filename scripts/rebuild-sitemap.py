#!/usr/bin/env python3
"""Rebuild sitemap.xml from published HTML pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {
    "index",
    "404",
    "cart",
    "checkout",
    "checkout-success",
    "account",
    "privacy-policy",
    "cookie-policy",
    "terms-and-conditions",
    "returns-and-refunds",
    "microsoft-365-solutions",
}
LANGS = ("it", "en", "fr", "de", "es")

urls = []
for lang in LANGS:
    urls.append(f"https://aml-store.com/{lang}/")
for lang in LANGS:
    urls.append(f"https://aml-store.com/{lang}/contacts")
for lang in LANGS:
    for html in sorted((ROOT / lang).glob("*.html")):
        if html.stem in SKIP or html.stem == "contacts":
            continue
        # Senza estensione: /foo.html risponde 308 verso /foo, quindi il .html
        # nel sitemap indicherebbe una tappa intermedia invece della pagina.
        urls.append(f"https://aml-store.com/{lang}/{html.stem}")

urls = list(dict.fromkeys(urls))
lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
for u in urls:
    pri = "1.0" if u.endswith("/it/") else "0.85"
    lines.append(
        f"  <url><loc>{u}</loc><changefreq>weekly</changefreq><priority>{pri}</priority></url>"
    )
lines.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("sitemap entries", len(urls))
