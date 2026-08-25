#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera le 5 pagine di confronto (wave 1 SEO/GEO) in tutte le 7 lingue.

Contenuto tradotto a mano (prezzi e feature ancorati al catalogo reale,
nessun dato inventato), stessa struttura HTML in ogni lingua cosi' le
pagine restano confrontabili tra loro. Il chrome header/footer resta
vuoto (<ecommerce-header>/<ecommerce-footer> senza contenuto): lo
riempie build-inline-chrome.mjs, come per le pagine del generatore.

Uso:
    python scripts/build_compare_pages.py
Poi, come sempre dopo aver toccato pagine catalogo/confronto:
    python scripts/apply-lang-suggest-banner.py
    node scripts/build-inline-chrome.mjs   (dev server attivo)
    python scripts/bump-asset-version.py
    python scripts/rebuild-sitemap.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG_RE = re.compile(r"<[^>]+>")
LANGS = ("it", "en", "fr", "de", "es", "pt", "nl")
LOCALE = {"it": "it_IT", "en": "en_US", "fr": "fr_FR", "de": "de_DE",
          "es": "es_ES", "pt": "pt_PT", "nl": "nl_NL"}

# Stringhe condivise da tutte le pagine di confronto, per lingua.
SHARED = {
    "it": {"skip": "Vai al contenuto principale", "eyebrow": "Confronto",
           "in_practice": "In pratica", "faq_eyebrow": "Domande frequenti",
           "faq_h2": "Hai dubbi prima dell'acquisto?", "home": "Home",
           "breadcrumb_aria": "Percorso navigazione", "see_listing": "Vedi la scheda"},
    "en": {"skip": "Skip to main content", "eyebrow": "Comparison",
           "in_practice": "In practice", "faq_eyebrow": "Frequently asked questions",
           "faq_h2": "Answers before you buy", "home": "Home",
           "breadcrumb_aria": "Breadcrumb", "see_listing": "See the"},
    "fr": {"skip": "Aller au contenu principal", "eyebrow": "Comparatif",
           "in_practice": "En pratique", "faq_eyebrow": "Questions fréquentes",
           "faq_h2": "Les réponses avant d'acheter", "home": "Accueil",
           "breadcrumb_aria": "Fil d'Ariane", "see_listing": "Voir la fiche"},
    "de": {"skip": "Zum Hauptinhalt springen", "eyebrow": "Vergleich",
           "in_practice": "In der Praxis", "faq_eyebrow": "Häufig gestellte Fragen",
           "faq_h2": "Antworten vor dem Kauf", "home": "Start",
           "breadcrumb_aria": "Brotkrumen-Navigation", "see_listing": "Zur Produktseite"},
    "es": {"skip": "Ir al contenido principal", "eyebrow": "Comparativa",
           "in_practice": "En la práctica", "faq_eyebrow": "Preguntas frecuentes",
           "faq_h2": "Las respuestas antes de comprar", "home": "Inicio",
           "breadcrumb_aria": "Ruta de navegación", "see_listing": "Ver la ficha"},
    "pt": {"skip": "Ir para o conteúdo principal", "eyebrow": "Comparação",
           "in_practice": "Na prática", "faq_eyebrow": "Perguntas frequentes",
           "faq_h2": "Respostas antes de comprar", "home": "Início",
           "breadcrumb_aria": "Navegação estrutural", "see_listing": "Ver a ficha"},
    "nl": {"skip": "Naar de hoofdinhoud", "eyebrow": "Vergelijking",
           "in_practice": "In de praktijk", "faq_eyebrow": "Veelgestelde vragen",
           "faq_h2": "Antwoorden vóór u koopt", "home": "Home",
           "breadcrumb_aria": "Kruimelpad", "see_listing": "Bekijk de productpagina"},
}

CATEGORY_LABEL = {
    "sistemi-operativi": {"it": "Sistemi Operativi", "en": "Operating systems",
                           "fr": "Systèmes d'exploitation", "de": "Betriebssysteme",
                           "es": "Sistemas operativos", "pt": "Sistemas operativos",
                           "nl": "Besturingssystemen"},
    "suite-office": {"it": "Suite Office", "en": "Office suite", "fr": "Suite Office",
                      "de": "Office-Suite", "es": "Suite Office", "pt": "Suite Office",
                      "nl": "Office-suite"},
    "microsoft-365-solutions": {"it": "Microsoft 365", "en": "Microsoft 365",
                                 "fr": "Microsoft 365", "de": "Microsoft 365",
                                 "es": "Microsoft 365", "pt": "Microsoft 365",
                                 "nl": "Microsoft 365"},
    "antivirus": {"it": "Antivirus", "en": "Antivirus", "fr": "Antivirus",
                  "de": "Antivirus", "es": "Antivirus", "pt": "Antivírus", "nl": "Antivirus"},
}

ORG_JSON = ('{{ "@type": "Organization", "@id": "https://aml-store.com/#organization", '
            '"name": "Aml Store", "url": "https://aml-store.com/", '
            '"aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "4.8", '
            '"reviewCount": "94", "bestRating": "5", "worstRating": "1" }} }}')


def hreflang_block(slug):
    lines = [f'    <link rel="alternate" hreflang="{lg}" href="https://aml-store.com/{lg}/{slug}">'
             for lg in LANGS]
    lines.append(f'    <link rel="alternate" hreflang="x-default" href="https://aml-store.com/it/{slug}">')
    return "\n".join(lines)


def faq_schema(items):
    parts = []
    for it in items:
        parts.append(
            '{ "@type": "Question", "name": "%s", "acceptedAnswer": '
            '{ "@type": "Answer", "text": "%s" } }' % (
                it["q"].replace('"', '\\"'), it["a_plain"].replace('"', '\\"')
            )
        )
    return ",\n        ".join(parts)


def verdict_html(v):
    return f"""            <div class="cmp-verdict__card">
                <h3>{v['name']}</h3>
                <p>{v['blurb']}</p>
                <span class="cmp-verdict__price">{v['price']}</span>
                <a class="pdp-btn-ghost" href="{v['href']}">{v['cta']}</a>
            </div>
"""


def table_html(caption, headers, rows):
    thead = "".join(f'<th scope="col">{h}</th>' for h in headers)
    trs = []
    for row in rows:
        head, *cells = row
        tds = "".join(f"<td>{c}</td>" for c in cells)
        trs.append(f'                    <tr><th scope="row">{head}</th>{tds}</tr>')
    tbody = "\n".join(trs)
    return f"""        <div class="cmp-table-wrap">
            <table class="cmp-table">
                <caption>{caption}</caption>
                <thead>
                    <tr>{thead}</tr>
                </thead>
                <tbody>
{tbody}
                </tbody>
            </table>
        </div>
"""


def faq_html(items):
    half = (len(items) + 1) // 2
    col1, col2 = items[:half], items[half:]

    def col(items_):
        parts = []
        for it in items_:
            parts.append(f"""                    <details class="home-faq-item">
                        <summary>{it['q']}</summary>
                        <div class="home-faq-body"><p>{it['a']}</p></div>
                    </details>""")
        return "\n".join(parts)

    return f"""            <div class="home-faq-list">
                <div class="pf-faq-col">
{col(col1)}
                </div>
                <div class="pf-faq-col">
{col(col2)}
                </div>
            </div>
"""


def render(page, lang):
    s = SHARED[lang]
    slug = page["slug"]
    L = lambda d: d[lang]  # noqa: E731
    title = L(page["meta_title"])
    desc = L(page["meta_description"])
    og_desc = L(page["og_description"])
    schema_name = L(page["schema_name"])
    schema_desc = L(page["schema_description"])
    category_href = page["category_href"]
    category_label = CATEGORY_LABEL[category_href][lang]
    breadcrumb_label = L(page["breadcrumb_label"])
    hero_h1 = L(page["hero_h1"])
    hero_lede = L(page["hero_lede"])
    editorial_h2 = L(page["editorial_h2"])
    editorial_paras = "\n".join(f"                <p>{p}</p>" for p in L(page["editorial_paragraphs"]))
    disclaimer = L(page["disclaimer"])

    verdicts = "".join(verdict_html({
        "name": L(v["name"]), "blurb": L(v["blurb"]), "price": L(v["price"]),
        "cta": L(v["cta"]), "href": v["href"],
    }) for v in page["verdict"])

    table = table_html(
        L(page["table_caption"]),
        [L(h) for h in page["table_headers"]],
        [[L(cell) for cell in row] for row in page["table_rows"]],
    )

    faq_items_lang = [{"q": L(it["q"]), "a": L(it["a"])} for it in page["faq_items"]]
    faq = faq_html(faq_items_lang)
    faq_schema_items = [
        {"q": L(it["q"]), "a_plain": TAG_RE.sub("", L(it["a"]))}
        for it in page["faq_items"]
    ]
    faq_ld = faq_schema(faq_schema_items)

    hreflang = hreflang_block(slug)

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow">
    <script src="../js/consent-init.js"></script>
    <link rel="icon" href="../favicon/favicon.png" type="image/png">
    <link rel="apple-touch-icon" href="../favicon/apple-touch-icon.png">
    <link rel="canonical" href="https://aml-store.com/{lang}/{slug}">
{hreflang}
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{og_desc}">
    <meta property="og:url" content="https://aml-store.com/{lang}/{slug}">
    <meta property="og:locale" content="{LOCALE[lang]}">
    <meta property="og:image" content="{page['og_image']}">
    <link rel="stylesheet" href="../fonts/montserrat.css">
    <link rel="stylesheet" href="../css/page.css">
    <link rel="stylesheet" href="../css/header.css">
    <link rel="stylesheet" href="../css/footer.css">
    <link rel="stylesheet" href="../css/product.css">
    <link rel="stylesheet" href="../css/product-pdp.css">
    <script src="../js/theme-init.js"></script>
    <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {ORG_JSON.format()},
    {{
      "@type": "WebPage",
      "@id": "https://aml-store.com/{lang}/{slug}#webpage",
      "name": "{schema_name}",
      "description": "{schema_desc}",
      "url": "https://aml-store.com/{lang}/{slug}",
      "inLanguage": "{lang}",
      "isPartOf": {{ "@type": "WebSite", "name": "Aml Store", "url": "https://aml-store.com/" }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "{s['home']}", "item": "https://aml-store.com/{lang}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "{category_label}", "item": "https://aml-store.com/{lang}/{category_href}" }},
        {{ "@type": "ListItem", "position": 3, "name": "{breadcrumb_label}" }}
      ]
    }},
    {{
      "@type": "FAQPage",
      "inLanguage": "{lang}",
      "url": "https://aml-store.com/{lang}/{slug}",
      "mainEntity": [
        {faq_ld}
      ]
    }}
  ]
}}
    </script>
</head>
<body class="pdp-page">
    <div class="scroll-progress" aria-hidden="true"></div>
    <a class="skip-link" href="#main">{s['skip']}</a>
    <aml-lang-suggest></aml-lang-suggest>
    <ecommerce-header translate="no" class="notranslate"></ecommerce-header>

    <main id="main" class="product-page">
        <section class="pdp-hero" aria-label="{s['eyebrow']}">
            <div class="pdp-breadcrumb">
                <nav aria-label="{s['breadcrumb_aria']}">
                    <a href="/{lang}/">{s['home']}</a>
                    <span class="sep" aria-hidden="true">/</span>
                    <a href="/{lang}/{category_href}">{category_label}</a>
                    <span class="sep" aria-hidden="true">/</span>
                    <span aria-current="page">{breadcrumb_label}</span>
                </nav>
            </div>

            <div class="cmp-hero">
                <p class="cmp-hero__eyebrow">{s['eyebrow']}</p>
                <h1 class="cmp-hero__title">{hero_h1}</h1>
                <p class="cmp-hero__lede">{hero_lede}</p>
            </div>
        </section>

        <div class="pdp-page">
        <div class="cmp-verdict" style="max-width:var(--pdp-maxw);margin:0 auto;padding:0 0 8px;">
{verdicts}        </div>

{table}
        <section class="pdp-sec pdp-sec--tight">
            <p class="pdp-sec__eyebrow">{s['in_practice']}</p>
            <h2 class="pdp-sec__title">{editorial_h2}</h2>
            <div class="pdp-overview__copy">
{editorial_paras}
            </div>
        </section>

        <section class="pdp-sec pdp-sec--tight pdp-faq">
            <p class="pdp-sec__eyebrow">{s['faq_eyebrow']}</p>
            <h2 class="pdp-sec__title pdp-faq__title">{s['faq_h2']}</h2>
{faq}        </section>

        <p class="pdp-sec__sub" style="max-width:var(--pdp-maxw);margin:0 auto;padding:0 0 40px;">{disclaimer}</p>
        </div>
    </main>

    <aml-cookie-banner></aml-cookie-banner>
    <ecommerce-footer translate="no" class="notranslate"></ecommerce-footer>

    <script src="../js/locale-path.js"></script>
    <script src="../js/cart.js" defer></script>
    <script src="../components/cookie-banner.js" defer></script>
    <script src="../components/lang-suggest.js" defer></script>
    <script src="../components/header.js" defer></script>
    <script src="../components/footer.js" defer></script>
    <script src="../js/scroll-progress.js" defer></script>
</body>
</html>
"""


def _d(it_val, en, fr, de, es, pt, nl):
    return {"it": it_val, "en": en, "fr": fr, "de": de, "es": es, "pt": pt, "nl": nl}


PAGES = [
    {
        "slug": "windows-11-home-vs-pro",
        "category_href": "sistemi-operativi",
        "og_image": "https://aml-store.com/asset/media/products/windows-11-pro.webp",
        "meta_title": _d(
            "Windows 11 Home o Pro: quale scegliere | Aml Store",
            "Windows 11 Home or Pro: which one to choose | Aml Store",
            "Windows 11 Home ou Pro : lequel choisir | Aml Store",
            "Windows 11 Home oder Pro: welche Wahl | Aml Store",
            "Windows 11 Home o Pro: ¿cuál elegir? | Aml Store",
            "Windows 11 Home ou Pro: qual escolher | Aml Store",
            "Windows 11 Home of Pro: wat kies je | Aml Store",
        ),
        "meta_description": _d(
            "Windows 11 Home vs Pro: differenze reali (BitLocker, Desktop remoto, Hyper-V), prezzi e quale versione scegliere per uso privato o lavoro.",
            "Windows 11 Home vs Pro: real differences (BitLocker, Remote Desktop, Hyper-V), prices and which edition to choose for personal use or work.",
            "Windows 11 Home vs Pro : différences réelles (BitLocker, Bureau à distance, Hyper-V), prix et quelle édition choisir pour un usage privé ou professionnel.",
            "Windows 11 Home vs. Pro: echte Unterschiede (BitLocker, Remotedesktop, Hyper-V), Preise und welche Edition sich für privat oder Arbeit eignet.",
            "Windows 11 Home vs Pro: diferencias reales (BitLocker, Escritorio remoto, Hyper-V), precios y qué edición elegir para uso privado o de trabajo.",
            "Windows 11 Home vs Pro: diferenças reais (BitLocker, Ambiente de Trabalho Remoto, Hyper-V), preços e qual edição escolher para uso privado ou profissional.",
            "Windows 11 Home vs Pro: echte verschillen (BitLocker, Extern bureaublad, Hyper-V), prijzen en welke editie te kiezen voor privé of werk.",
        ),
        "og_description": _d(
            "Differenze reali tra Windows 11 Home e Pro, prezzi e quale versione scegliere.",
            "Real differences between Windows 11 Home and Pro, prices and which edition to choose.",
            "Différences réelles entre Windows 11 Home et Pro, prix et quelle édition choisir.",
            "Echte Unterschiede zwischen Windows 11 Home und Pro, Preise und welche Edition passt.",
            "Diferencias reales entre Windows 11 Home y Pro, precios y qué edición elegir.",
            "Diferenças reais entre o Windows 11 Home e o Pro, preços e qual edição escolher.",
            "Echte verschillen tussen Windows 11 Home en Pro, prijzen en welke editie je moet kiezen.",
        ),
        "schema_name": _d(
            "Windows 11 Home o Pro: quale scegliere",
            "Windows 11 Home or Pro: which one to choose",
            "Windows 11 Home ou Pro : lequel choisir",
            "Windows 11 Home oder Pro: welche Wahl",
            "Windows 11 Home o Pro: ¿cuál elegir?",
            "Windows 11 Home ou Pro: qual escolher",
            "Windows 11 Home of Pro: wat kies je",
        ),
        "schema_description": _d(
            "Confronto tra Windows 11 Home e Pro: differenze, prezzi e a chi conviene ciascuna edizione.",
            "Comparison between Windows 11 Home and Pro: differences, prices and who each edition suits best.",
            "Comparaison entre Windows 11 Home et Pro : différences, prix et à qui convient chaque édition.",
            "Vergleich zwischen Windows 11 Home und Pro: Unterschiede, Preise und wem welche Edition passt.",
            "Comparación entre Windows 11 Home y Pro: diferencias, precios y a quién le conviene cada edición.",
            "Comparação entre o Windows 11 Home e o Pro: diferenças, preços e a quem convém cada edição.",
            "Vergelijking tussen Windows 11 Home en Pro: verschillen, prijzen en voor wie elke editie geschikt is.",
        ),
        "breadcrumb_label": _d(*(["Windows 11 Home vs Pro"] * 7)),
        "hero_h1": _d(
            "Windows 11 Home o Pro: quale scegliere",
            "Windows 11 Home or Pro: which one to choose",
            "Windows 11 Home ou Pro : lequel choisir",
            "Windows 11 Home oder Pro: welche Wahl?",
            "Windows 11 Home o Pro: ¿cuál elegir?",
            "Windows 11 Home ou Pro: qual escolher",
            "Windows 11 Home of Pro: wat kies je",
        ),
        "hero_lede": _d(
            "Stesso sistema operativo, stessi requisiti hardware. La differenza è nelle funzioni orientate al lavoro che Pro aggiunge — utili solo se sai già che ti servono.",
            "Same operating system, same hardware requirements. The difference is in the work-oriented features Pro adds — useful only if you already know you need them.",
            "Même système d'exploitation, mêmes prérequis matériels. La différence tient aux fonctions orientées travail que Pro ajoute — utiles seulement si vous savez déjà en avoir besoin.",
            "Gleiches Betriebssystem, gleiche Hardwarevoraussetzungen. Der Unterschied liegt in den arbeitsorientierten Funktionen, die Pro ergänzt — nützlich nur, wenn Sie schon wissen, dass Sie sie brauchen.",
            "Mismo sistema operativo, mismos requisitos de hardware. La diferencia está en las funciones orientadas al trabajo que añade Pro — útiles solo si ya sabes que las necesitas.",
            "Mesmo sistema operativo, mesmos requisitos de hardware. A diferença está nas funcionalidades orientadas para o trabalho que o Pro acrescenta — úteis só se já souber que precisa delas.",
            "Hetzelfde besturingssysteem, dezelfde hardware-eisen. Het verschil zit in de werkgerichte functies die Pro toevoegt — alleen nuttig als je al weet dat je ze nodig hebt.",
        ),
        "verdict": [
            {
                "name": _d(*(["Windows 11 Home"] * 7)),
                "blurb": _d(
                    "Per uso privato: navigazione, studio, streaming, gaming. Nessuna funzione business, stesso motore di Windows 11.",
                    "For personal use: browsing, study, streaming, gaming. No business features, same Windows 11 engine.",
                    "Pour un usage privé : navigation, études, streaming, jeu. Aucune fonction professionnelle, même moteur que Windows 11.",
                    "Für die private Nutzung: Surfen, Lernen, Streaming, Gaming. Keine Business-Funktionen, gleiche Windows-11-Engine.",
                    "Para uso privado: navegación, estudio, streaming, gaming. Sin funciones empresariales, mismo motor que Windows 11.",
                    "Para uso privado: navegação, estudo, streaming, gaming. Sem funcionalidades empresariais, mesmo motor do Windows 11.",
                    "Voor privégebruik: surfen, studeren, streamen, gamen. Geen zakelijke functies, dezelfde Windows 11-engine.",
                ),
                "price": _d(
                    "€ 61,00 — licenza ESD", "€ 61,00 — ESD licence", "€ 61,00 — licence ESD",
                    "€ 61,00 — ESD-Lizenz", "€ 61,00 — licencia ESD", "€ 61,00 — licença ESD",
                    "€ 61,00 — ESD-licentie",
                ),
                "cta": _d(
                    "Vedi la scheda Home", "See the Home listing", "Voir la fiche Home",
                    "Zur Home-Produktseite", "Ver la ficha de Home", "Ver a ficha do Home",
                    "Bekijk de Home-productpagina",
                ),
                "href": "windows-11-home",
            },
            {
                "name": _d(*(["Windows 11 Pro"] * 7)),
                "blurb": _d(
                    "Per chi lavora dal PC: crittografia BitLocker, accesso remoto come host, gestione più adatta a contesti aziendali.",
                    "For those who work from their PC: BitLocker encryption, remote access as host, management better suited to business contexts.",
                    "Pour ceux qui travaillent depuis leur PC : chiffrement BitLocker, accès à distance en tant qu'hôte, gestion plus adaptée aux contextes professionnels.",
                    "Für alle, die vom PC aus arbeiten: BitLocker-Verschlüsselung, Fernzugriff als Host, für Unternehmensumgebungen besser geeignete Verwaltung.",
                    "Para quienes trabajan desde el PC: cifrado BitLocker, acceso remoto como host, gestión más adecuada para entornos empresariales.",
                    "Para quem trabalha a partir do PC: encriptação BitLocker, acesso remoto como anfitrião, gestão mais adequada a contextos empresariais.",
                    "Voor wie vanaf de pc werkt: BitLocker-versleuteling, externe toegang als host, beheer dat beter past bij zakelijke omgevingen.",
                ),
                "price": _d(
                    "€ 99,00 — licenza ESD", "€ 99,00 — ESD licence", "€ 99,00 — licence ESD",
                    "€ 99,00 — ESD-Lizenz", "€ 99,00 — licencia ESD", "€ 99,00 — licença ESD",
                    "€ 99,00 — ESD-licentie",
                ),
                "cta": _d(
                    "Vedi la scheda Pro", "See the Pro listing", "Voir la fiche Pro",
                    "Zur Pro-Produktseite", "Ver la ficha de Pro", "Ver a ficha do Pro",
                    "Bekijk de Pro-productpagina",
                ),
                "href": "windows-11-pro",
            },
        ],
        "table_caption": _d(
            "Windows 11 Home vs Pro, differenze secondo Microsoft",
            "Windows 11 Home vs Pro, differences according to Microsoft",
            "Windows 11 Home vs Pro, différences selon Microsoft",
            "Windows 11 Home vs. Pro, Unterschiede laut Microsoft",
            "Windows 11 Home vs Pro, diferencias según Microsoft",
            "Windows 11 Home vs Pro, diferenças segundo a Microsoft",
            "Windows 11 Home vs Pro, verschillen volgens Microsoft",
        ),
        "table_headers": [
            _d("Caratteristica", "Feature", "Caractéristique", "Funktion", "Característica", "Característica", "Kenmerk"),
            _d(*(["Home"] * 7)),
            _d(*(["Pro"] * 7)),
        ],
        "table_rows": [
            [
                _d("Prezzo su Aml Store", "Price on Aml Store", "Prix sur Aml Store", "Preis bei Aml Store", "Precio en Aml Store", "Preço na Aml Store", "Prijs bij Aml Store"),
                _d(*(["€ 61,00"] * 7)),
                _d(*(["€ 99,00"] * 7)),
            ],
            [
                _d("Tipo di licenza", "Licence type", "Type de licence", "Lizenztyp", "Tipo de licencia", "Tipo de licença", "Licentietype"),
                _d(
                    "ESD digitale, perpetua", "Digital ESD, perpetual", "ESD numérique, perpétuelle",
                    "Digitale ESD, unbefristet", "ESD digital, perpetua", "ESD digital, perpétua",
                    "Digitale ESD, permanent",
                ),
                _d(
                    "ESD digitale, perpetua", "Digital ESD, perpetual", "ESD numérique, perpétuelle",
                    "Digitale ESD, unbefristet", "ESD digital, perpetua", "ESD digital, perpétua",
                    "Digitale ESD, permanent",
                ),
            ],
            [
                _d(
                    "BitLocker (crittografia disco)", "BitLocker (drive encryption)", "BitLocker (chiffrement du disque)",
                    "BitLocker (Festplattenverschlüsselung)", "BitLocker (cifrado de disco)", "BitLocker (encriptação do disco)",
                    "BitLocker (schijfversleuteling)",
                ),
                _d("No", "No", "Non", "Nein", "No", "Não", "Nee"),
                _d("Sì", "Yes", "Oui", "Ja", "Sí", "Sim", "Ja"),
            ],
            [
                _d(
                    "Desktop remoto come host", "Remote Desktop as host", "Bureau à distance en tant qu'hôte",
                    "Remotedesktop als Host", "Escritorio remoto como host", "Ambiente de Trabalho Remoto como anfitrião",
                    "Extern bureaublad als host",
                ),
                _d("No", "No", "Non", "Nein", "No", "Não", "Nee"),
                _d("Sì", "Yes", "Oui", "Ja", "Sí", "Sim", "Ja"),
            ],
            [
                _d(*(["Hyper-V / Windows Sandbox"] * 7)),
                _d("No", "No", "Non", "Nein", "No", "Não", "Nee"),
                _d("Sì", "Yes", "Oui", "Ja", "Sí", "Sim", "Ja"),
            ],
            [
                _d(
                    "Accesso a domini aziendali (Entra/Business)", "Access to business domains (Entra/Business)",
                    "Accès aux domaines professionnels (Entra/Business)", "Zugriff auf Unternehmensdomänen (Entra/Business)",
                    "Acceso a dominios empresariales (Entra/Business)", "Acesso a domínios empresariais (Entra/Business)",
                    "Toegang tot zakelijke domeinen (Entra/Business)",
                ),
                _d("No", "No", "Non", "Nein", "No", "Não", "Nee"),
                _d("Sì", "Yes", "Oui", "Ja", "Sí", "Sim", "Ja"),
            ],
            [
                _d("Requisiti hardware", "Hardware requirements", "Prérequis matériels", "Hardwarevoraussetzungen", "Requisitos de hardware", "Requisitos de hardware", "Hardware-eisen"),
                _d(
                    "CPU compatibile, TPM 2.0, Secure Boot, 4 GB RAM+", "Compatible CPU, TPM 2.0, Secure Boot, 4 GB+ RAM",
                    "CPU compatible, TPM 2.0, Secure Boot, 4 Go de RAM+", "Kompatible CPU, TPM 2.0, Secure Boot, 4 GB+ RAM",
                    "CPU compatible, TPM 2.0, Secure Boot, 4 GB+ de RAM", "CPU compatível, TPM 2.0, Secure Boot, 4 GB+ de RAM",
                    "Compatibele cpu, TPM 2.0, Secure Boot, 4 GB+ RAM",
                ),
                _d(
                    "Uguali a Home", "Same as Home", "Identiques à Home", "Wie bei Home", "Iguales a Home",
                    "Iguais ao Home", "Gelijk aan Home",
                ),
            ],
        ],
        "editorial_h2": _d(
            "Quando Pro fa davvero la differenza",
            "When Pro really makes a difference",
            "Quand Pro fait vraiment la différence",
            "Wann Pro wirklich den Unterschied macht",
            "Cuándo Pro marca realmente la diferencia",
            "Quando o Pro faz mesmo a diferença",
            "Wanneer Pro echt het verschil maakt",
        ),
        "editorial_paragraphs": _d(
            [
                "Se usi il PC per navigare, lavorare con Office, guardare contenuti in streaming o giocare, Windows 11 Home copre tutto: è lo stesso sistema operativo, con lo stesso motore grafico e le stesse app.",
                "Pro ha senso quando ti serve almeno una di queste funzioni: crittografare il disco con BitLocker, collegarti al tuo PC da remoto usandolo come host, eseguire macchine virtuali con Hyper-V, oppure collegare il dispositivo a un dominio o account aziendale Microsoft Entra.",
                "Non esiste una versione \"più veloce\" o \"più stabile\": le prestazioni sono identiche, cambia solo il set di funzioni disponibile secondo l'edizione.",
            ],
            [
                "If you use your PC to browse, work with Office, watch streaming content or play games, Windows 11 Home covers everything: it's the same operating system, with the same graphics engine and the same apps.",
                "Pro makes sense when you need at least one of these: encrypting your drive with BitLocker, connecting to your PC remotely using it as a host, running virtual machines with Hyper-V, or joining the device to a domain or Microsoft Entra business account.",
                "There's no \"faster\" or \"more stable\" version: performance is identical, only the available feature set changes with the edition.",
            ],
            [
                "Si vous utilisez votre PC pour naviguer, travailler avec Office, regarder du contenu en streaming ou jouer, Windows 11 Home couvre tout : c'est le même système d'exploitation, avec le même moteur graphique et les mêmes applications.",
                "Pro a du sens si vous avez besoin d'au moins l'une de ces fonctions : chiffrer le disque avec BitLocker, vous connecter à votre PC à distance en l'utilisant comme hôte, exécuter des machines virtuelles avec Hyper-V, ou joindre l'appareil à un domaine ou à un compte professionnel Microsoft Entra.",
                "Il n'existe pas de version « plus rapide » ou « plus stable » : les performances sont identiques, seul l'ensemble de fonctions disponibles change selon l'édition.",
            ],
            [
                "Wenn Sie Ihren PC zum Surfen, für die Arbeit mit Office, zum Streamen oder Spielen nutzen, deckt Windows 11 Home alles ab: Es ist dasselbe Betriebssystem mit derselben Grafik-Engine und denselben Apps.",
                "Pro ist sinnvoll, wenn Sie mindestens eine dieser Funktionen benötigen: die Festplatte mit BitLocker verschlüsseln, sich remote mit Ihrem PC als Host verbinden, virtuelle Maschinen mit Hyper-V ausführen oder das Gerät mit einer Domäne oder einem geschäftlichen Microsoft-Entra-Konto verbinden.",
                "Es gibt keine \"schnellere\" oder \"stabilere\" Version: Die Leistung ist identisch, nur der verfügbare Funktionsumfang ändert sich je nach Edition.",
            ],
            [
                "Si usas tu PC para navegar, trabajar con Office, ver contenido en streaming o jugar, Windows 11 Home lo cubre todo: es el mismo sistema operativo, con el mismo motor gráfico y las mismas apps.",
                "Pro tiene sentido si necesitas al menos una de estas funciones: cifrar el disco con BitLocker, conectarte a tu PC de forma remota usándolo como host, ejecutar máquinas virtuales con Hyper-V, o unir el dispositivo a un dominio o cuenta empresarial de Microsoft Entra.",
                "No existe una versión \"más rápida\" o \"más estable\": el rendimiento es idéntico, solo cambia el conjunto de funciones disponibles según la edición.",
            ],
            [
                "Se usa o seu PC para navegar, trabalhar com o Office, ver conteúdos em streaming ou jogar, o Windows 11 Home cobre tudo: é o mesmo sistema operativo, com o mesmo motor gráfico e as mesmas apps.",
                "O Pro faz sentido se precisar de pelo menos uma destas funcionalidades: encriptar o disco com o BitLocker, ligar-se remotamente ao seu PC usando-o como anfitrião, executar máquinas virtuais com o Hyper-V, ou associar o dispositivo a um domínio ou conta empresarial Microsoft Entra.",
                "Não existe uma versão \"mais rápida\" ou \"mais estável\": o desempenho é idêntico, só muda o conjunto de funcionalidades disponíveis consoante a edição.",
            ],
            [
                "Als je je pc gebruikt om te surfen, met Office te werken, te streamen of te gamen, dekt Windows 11 Home alles: het is hetzelfde besturingssysteem, met dezelfde grafische engine en dezelfde apps.",
                "Pro is zinvol als je minstens een van deze functies nodig hebt: de schijf versleutelen met BitLocker, op afstand verbinding maken met je pc als host, virtuele machines draaien met Hyper-V, of het apparaat koppelen aan een domein of zakelijk Microsoft Entra-account.",
                "Er bestaat geen \"snellere\" of \"stabielere\" versie: de prestaties zijn identiek, alleen de beschikbare functieset verschilt per editie.",
            ],
        ),
        "faq_items": [
            {
                "q": _d(
                    "Qual è la differenza principale tra Home e Pro?", "What's the main difference between Home and Pro?",
                    "Quelle est la principale différence entre Home et Pro ?", "Was ist der Hauptunterschied zwischen Home und Pro?",
                    "¿Cuál es la principal diferencia entre Home y Pro?", "Qual é a principal diferença entre o Home e o Pro?",
                    "Wat is het belangrijkste verschil tussen Home en Pro?",
                ),
                "a": _d(
                    "Pro aggiunge funzioni orientate al lavoro non presenti in Home: BitLocker per la crittografia del disco e Desktop remoto come host, secondo Microsoft.",
                    "Pro adds work-oriented features not present in Home: BitLocker for drive encryption and Remote Desktop as host, according to Microsoft.",
                    "Pro ajoute des fonctions orientées travail absentes de Home : BitLocker pour le chiffrement du disque et le Bureau à distance en tant qu'hôte, selon Microsoft.",
                    "Pro ergänzt arbeitsorientierte Funktionen, die in Home fehlen: BitLocker zur Festplattenverschlüsselung und Remotedesktop als Host, laut Microsoft.",
                    "Pro añade funciones orientadas al trabajo que no están en Home: BitLocker para cifrar el disco y Escritorio remoto como host, según Microsoft.",
                    "O Pro acrescenta funcionalidades orientadas para o trabalho que não existem no Home: BitLocker para encriptação do disco e Ambiente de Trabalho Remoto como anfitrião, segundo a Microsoft.",
                    "Pro voegt werkgerichte functies toe die niet in Home zitten: BitLocker voor schijfversleuteling en Extern bureaublad als host, volgens Microsoft.",
                ),
            },
            {
                "q": _d(
                    "Posso passare da Home a Pro in un secondo momento?", "Can I upgrade from Home to Pro later?",
                    "Puis-je passer de Home à Pro plus tard ?", "Kann ich später von Home auf Pro upgraden?",
                    "¿Puedo pasar de Home a Pro más adelante?", "Posso passar do Home para o Pro mais tarde?",
                    "Kan ik later upgraden van Home naar Pro?",
                ),
                "a": _d(
                    "Sì, Microsoft consente l'upgrade in-place con una chiave Pro, senza reinstallare Windows né perdere i dati.",
                    "Yes, Microsoft allows an in-place upgrade with a Pro key, without reinstalling Windows or losing your data.",
                    "Oui, Microsoft permet une mise à niveau sur place avec une clé Pro, sans réinstaller Windows ni perdre vos données.",
                    "Ja, Microsoft erlaubt ein In-Place-Upgrade mit einem Pro-Schlüssel, ohne Windows neu zu installieren oder Daten zu verlieren.",
                    "Sí, Microsoft permite una actualización in situ con una clave Pro, sin reinstalar Windows ni perder tus datos.",
                    "Sim, a Microsoft permite uma atualização no local com uma chave Pro, sem reinstalar o Windows nem perder os dados.",
                    "Ja, Microsoft staat een in-place upgrade met een Pro-key toe, zonder Windows opnieuw te installeren of gegevens te verliezen.",
                ),
            },
            {
                "q": _d(
                    "Serve Windows 11 Pro per giocare?", "Do I need Windows 11 Pro for gaming?",
                    "Ai-je besoin de Windows 11 Pro pour jouer ?", "Brauche ich Windows 11 Pro zum Spielen?",
                    "¿Necesito Windows 11 Pro para jugar?", "Preciso do Windows 11 Pro para jogar?",
                    "Heb ik Windows 11 Pro nodig om te gamen?",
                ),
                "a": _d(
                    "No: per la maggior parte degli usi privati, gaming incluso, Windows 11 Home è sufficiente.",
                    "No: for most personal uses, gaming included, Windows 11 Home is enough.",
                    "Non : pour la plupart des usages privés, jeu inclus, Windows 11 Home suffit.",
                    "Nein: Für die meisten privaten Anwendungen, Gaming eingeschlossen, reicht Windows 11 Home.",
                    "No: para la mayoría de los usos privados, gaming incluido, Windows 11 Home es suficiente.",
                    "Não: para a maioria dos usos privados, incluindo jogos, o Windows 11 Home é suficiente.",
                    "Nee: voor de meeste privégebruik, gamen inbegrepen, is Windows 11 Home voldoende.",
                ),
            },
            {
                "q": _d(
                    "Quale scegliere per un'azienda o un professionista?", "Which should a business or professional choose?",
                    "Que doit choisir une entreprise ou un professionnel ?", "Was sollten Unternehmen oder Fachleute wählen?",
                    "¿Qué debería elegir una empresa o un profesional?", "O que deve escolher uma empresa ou um profissional?",
                    "Wat moet een bedrijf of professional kiezen?",
                ),
                "a": _d(
                    "Pro, per le funzioni di sicurezza e gestione dispositivi (BitLocker, accesso a domini aziendali) pensate per contesti di lavoro.",
                    "Pro, for the security and device-management features (BitLocker, access to business domains) built for work contexts.",
                    "Pro, pour les fonctions de sécurité et de gestion des appareils (BitLocker, accès aux domaines professionnels) pensées pour un contexte de travail.",
                    "Pro, wegen der Sicherheits- und Geräteverwaltungsfunktionen (BitLocker, Zugriff auf Unternehmensdomänen), die für Arbeitsumgebungen gedacht sind.",
                    "Pro, por las funciones de seguridad y gestión de dispositivos (BitLocker, acceso a dominios empresariales) pensadas para entornos de trabajo.",
                    "O Pro, pelas funcionalidades de segurança e gestão de dispositivos (BitLocker, acesso a domínios empresariais) pensadas para contextos de trabalho.",
                    "Pro, vanwege de beveiligings- en apparaatbeheerfuncties (BitLocker, toegang tot zakelijke domeinen) die voor werkomgevingen zijn gemaakt.",
                ),
            },
            {
                "q": _d(
                    "I requisiti hardware sono diversi tra Home e Pro?", "Are the hardware requirements different between Home and Pro?",
                    "Les prérequis matériels sont-ils différents entre Home et Pro ?", "Unterscheiden sich die Hardwarevoraussetzungen zwischen Home und Pro?",
                    "¿Los requisitos de hardware son distintos entre Home y Pro?", "Os requisitos de hardware são diferentes entre o Home e o Pro?",
                    "Zijn de hardware-eisen anders tussen Home en Pro?",
                ),
                "a": _d(
                    "No, sono gli stessi: CPU compatibile, TPM 2.0, Secure Boot e almeno 4 GB di RAM secondo i requisiti Microsoft aggiornati.",
                    "No, they're the same: compatible CPU, TPM 2.0, Secure Boot and at least 4 GB of RAM according to Microsoft's current requirements.",
                    "Non, ils sont identiques : CPU compatible, TPM 2.0, Secure Boot et au moins 4 Go de RAM selon les exigences Microsoft actuelles.",
                    "Nein, sie sind identisch: kompatible CPU, TPM 2.0, Secure Boot und mindestens 4 GB RAM gemäß den aktuellen Microsoft-Anforderungen.",
                    "No, son los mismos: CPU compatible, TPM 2.0, Secure Boot y al menos 4 GB de RAM según los requisitos actuales de Microsoft.",
                    "Não, são os mesmos: CPU compatível, TPM 2.0, Secure Boot e pelo menos 4 GB de RAM segundo os requisitos atuais da Microsoft.",
                    "Nee, ze zijn hetzelfde: compatibele cpu, TPM 2.0, Secure Boot en minstens 4 GB RAM volgens de actuele Microsoft-vereisten.",
                ),
            },
            {
                "q": _d(
                    "Esiste anche una versione OEM DVD o con adesivo COA?", "Is there also an OEM DVD or COA sticker version?",
                    "Existe-t-il aussi une version DVD OEM ou avec autocollant COA ?", "Gibt es auch eine OEM-DVD- oder COA-Aufkleber-Version?",
                    "¿Existe también una versión en DVD OEM o con pegatina COA?", "Também existe uma versão em DVD OEM ou com autocolante COA?",
                    "Bestaat er ook een OEM-dvd- of COA-stickerversie?",
                ),
                "a": _d(
                    'Sì per Pro: oltre alla licenza ESD via email, in catalogo trovi la variante <a href="windows-11-pro-oem-dvd">OEM DVD</a> e quella con <a href="windows-11-pro-coa">adesivo COA</a> — stesso sistema operativo, formato di consegna diverso.',
                    'Yes for Pro: besides the ESD licence by email, the catalogue also has the <a href="windows-11-pro-oem-dvd">OEM DVD</a> variant and the one with a <a href="windows-11-pro-coa">COA sticker</a> — same operating system, different delivery format.',
                    'Oui pour Pro : en plus de la licence ESD par email, le catalogue propose aussi la variante <a href="windows-11-pro-oem-dvd">DVD OEM</a> et celle avec <a href="windows-11-pro-coa">autocollant COA</a> — même système d\'exploitation, format de livraison différent.',
                    'Ja, bei Pro: Neben der ESD-Lizenz per E-Mail gibt es im Katalog auch die Variante <a href="windows-11-pro-oem-dvd">OEM-DVD</a> und die mit <a href="windows-11-pro-coa">COA-Aufkleber</a> — gleiches Betriebssystem, anderes Lieferformat.',
                    'Sí, para Pro: además de la licencia ESD por email, el catálogo también tiene la variante en <a href="windows-11-pro-oem-dvd">DVD OEM</a> y la que lleva <a href="windows-11-pro-coa">pegatina COA</a> — mismo sistema operativo, formato de entrega distinto.',
                    'Sim, para o Pro: além da licença ESD por email, o catálogo também tem a variante em <a href="windows-11-pro-oem-dvd">DVD OEM</a> e a que tem <a href="windows-11-pro-coa">autocolante COA</a> — mesmo sistema operativo, formato de entrega diferente.',
                    'Ja, voor Pro: naast de ESD-licentie per e-mail heeft de catalogus ook de <a href="windows-11-pro-oem-dvd">OEM-dvd</a>-variant en die met <a href="windows-11-pro-coa">COA-sticker</a> — hetzelfde besturingssysteem, ander leveringsformaat.',
                ),
            },
        ],
        "disclaimer": _d(
            "Microsoft, Windows e i relativi marchi sono di Microsoft Corporation. Contenuto informativo Aml Store: funzionalità e requisiti seguono sempre la documentazione Microsoft aggiornata.",
            "Microsoft, Windows and related marks are property of Microsoft Corporation. Informational content by Aml Store: features and requirements always follow current Microsoft documentation.",
            "Microsoft, Windows et les marques associées appartiennent à Microsoft Corporation. Contenu informatif Aml Store : fonctionnalités et prérequis suivent toujours la documentation Microsoft à jour.",
            "Microsoft, Windows und die zugehörigen Marken sind Eigentum der Microsoft Corporation. Informativer Inhalt von Aml Store: Funktionen und Voraussetzungen richten sich stets nach der aktuellen Microsoft-Dokumentation.",
            "Microsoft, Windows y las marcas relacionadas son propiedad de Microsoft Corporation. Contenido informativo de Aml Store: las funciones y requisitos siguen siempre la documentación actual de Microsoft.",
            "Microsoft, Windows e as marcas relacionadas são propriedade da Microsoft Corporation. Conteúdo informativo da Aml Store: funcionalidades e requisitos seguem sempre a documentação atual da Microsoft.",
            "Microsoft, Windows en de bijbehorende merken zijn eigendom van Microsoft Corporation. Informatieve inhoud van Aml Store: functies en vereisten volgen altijd de actuele Microsoft-documentatie.",
        ),
    },
    {
        "slug": "office-2024-vs-microsoft-365",
        "category_href": "suite-office",
        "og_image": "https://aml-store.com/asset/media/products/microsoft-365-personal.webp",
        "meta_title": _d(
            "Office 2024 o Microsoft 365: licenza o abbonamento | Aml Store",
            "Office 2024 or Microsoft 365: licence or subscription | Aml Store",
            "Office 2024 ou Microsoft 365 : licence ou abonnement | Aml Store",
            "Office 2024 oder Microsoft 365: Lizenz oder Abo | Aml Store",
            "Office 2024 o Microsoft 365: licencia o suscripción | Aml Store",
            "Office 2024 ou Microsoft 365: licença ou subscrição | Aml Store",
            "Office 2024 of Microsoft 365: licentie of abonnement | Aml Store",
        ),
        "meta_description": _d(
            "Office 2024 vs Microsoft 365: differenza tra licenza perpetua e abbonamento, prezzi, Copilot AI e spazio cloud. Quale conviene in base a come lo usi.",
            "Office 2024 vs Microsoft 365: difference between a one-time licence and a subscription, prices, Copilot AI and cloud storage. Which one pays off depends on how you use it.",
            "Office 2024 vs Microsoft 365 : différence entre licence unique et abonnement, prix, Copilot AI et espace cloud. Ce qui est le plus rentable selon votre usage.",
            "Office 2024 vs. Microsoft 365: Unterschied zwischen Einmallizenz und Abo, Preise, Copilot AI und Cloud-Speicher. Was sich lohnt, hängt von der Nutzung ab.",
            "Office 2024 vs Microsoft 365: diferencia entre licencia única y suscripción, precios, Copilot AI y espacio en la nube. Qué compensa según cómo lo uses.",
            "Office 2024 vs Microsoft 365: diferença entre licença única e subscrição, preços, Copilot AI e espaço na nuvem. O que compensa depende de como o usa.",
            "Office 2024 vs Microsoft 365: verschil tussen eenmalige licentie en abonnement, prijzen, Copilot AI en cloudopslag. Wat loont hangt af van je gebruik.",
        ),
        "og_description": _d(
            "Differenza tra Office 2024 (licenza perpetua) e Microsoft 365 (abbonamento): prezzi e quale conviene.",
            "Difference between Office 2024 (one-time licence) and Microsoft 365 (subscription): prices and which one pays off.",
            "Différence entre Office 2024 (licence unique) et Microsoft 365 (abonnement) : prix et ce qui est le plus rentable.",
            "Unterschied zwischen Office 2024 (Einmallizenz) und Microsoft 365 (Abo): Preise und was sich lohnt.",
            "Diferencia entre Office 2024 (licencia única) y Microsoft 365 (suscripción): precios y qué compensa.",
            "Diferença entre o Office 2024 (licença única) e o Microsoft 365 (subscrição): preços e o que compensa.",
            "Verschil tussen Office 2024 (eenmalige licentie) en Microsoft 365 (abonnement): prijzen en wat loont.",
        ),
        "schema_name": _d(
            "Office 2024 o Microsoft 365: licenza o abbonamento",
            "Office 2024 or Microsoft 365: licence or subscription",
            "Office 2024 ou Microsoft 365 : licence ou abonnement",
            "Office 2024 oder Microsoft 365: Lizenz oder Abo",
            "Office 2024 o Microsoft 365: licencia o suscripción",
            "Office 2024 ou Microsoft 365: licença ou subscrição",
            "Office 2024 of Microsoft 365: licentie of abonnement",
        ),
        "schema_description": _d(
            "Confronto tra Office 2024 (licenza perpetua) e Microsoft 365 (abbonamento): cosa include ciascuno e quale conviene.",
            "Comparison between Office 2024 (one-time licence) and Microsoft 365 (subscription): what each includes and which one pays off.",
            "Comparaison entre Office 2024 (licence unique) et Microsoft 365 (abonnement) : ce que chacun inclut et ce qui est le plus rentable.",
            "Vergleich zwischen Office 2024 (Einmallizenz) und Microsoft 365 (Abo): was jeweils enthalten ist und was sich lohnt.",
            "Comparación entre Office 2024 (licencia única) y Microsoft 365 (suscripción): qué incluye cada uno y qué compensa.",
            "Comparação entre o Office 2024 (licença única) e o Microsoft 365 (subscrição): o que cada um inclui e o que compensa.",
            "Vergelijking tussen Office 2024 (eenmalige licentie) en Microsoft 365 (abonnement): wat elk bevat en wat loont.",
        ),
        "breadcrumb_label": _d(*(["Office 2024 vs Microsoft 365"] * 7)),
        "hero_h1": _d(
            "Office 2024 o Microsoft 365: licenza o abbonamento?",
            "Office 2024 or Microsoft 365: licence or subscription?",
            "Office 2024 ou Microsoft 365 : licence ou abonnement ?",
            "Office 2024 oder Microsoft 365: Lizenz oder Abo?",
            "Office 2024 o Microsoft 365: ¿licencia o suscripción?",
            "Office 2024 ou Microsoft 365: licença ou subscrição?",
            "Office 2024 of Microsoft 365: licentie of abonnement?",
        ),
        "hero_lede": _d(
            "Stesse app di base, filosofia opposta: Office 2024 si paga una volta e resta quello. Microsoft 365 è un abbonamento che aggiunge Copilot AI, spazio cloud e aggiornamenti continui.",
            "Same core apps, opposite philosophy: Office 2024 is paid once and stays as it is. Microsoft 365 is a subscription that adds Copilot AI, cloud storage and continuous updates.",
            "Mêmes applications de base, philosophie opposée : Office 2024 se paie une fois et reste tel quel. Microsoft 365 est un abonnement qui ajoute Copilot AI, de l'espace cloud et des mises à jour continues.",
            "Gleiche Kern-Apps, entgegengesetzte Philosophie: Office 2024 wird einmal bezahlt und bleibt so. Microsoft 365 ist ein Abo, das Copilot AI, Cloud-Speicher und laufende Updates hinzufügt.",
            "Mismas apps básicas, filosofía opuesta: Office 2024 se paga una vez y se queda tal cual. Microsoft 365 es una suscripción que añade Copilot AI, espacio en la nube y actualizaciones continuas.",
            "As mesmas apps base, filosofia oposta: o Office 2024 paga-se uma vez e fica como está. O Microsoft 365 é uma subscrição que acrescenta Copilot AI, espaço na nuvem e atualizações contínuas.",
            "Dezelfde basisapps, tegenovergestelde filosofie: Office 2024 betaal je één keer en blijft zoals het is. Microsoft 365 is een abonnement met Copilot AI, cloudopslag en doorlopende updates.",
        ),
        "verdict": [
            {
                "name": _d(*(["Office 2024 Home"] * 7)),
                "blurb": _d(
                    "Un solo pagamento, nessun rinnovo. Word, Excel, PowerPoint per PC o Mac così come sono oggi.",
                    "One payment, no renewal. Word, Excel and PowerPoint for PC or Mac, exactly as they are today.",
                    "Un seul paiement, aucun renouvellement. Word, Excel et PowerPoint pour PC ou Mac, tels qu'ils sont aujourd'hui.",
                    "Eine einzige Zahlung, keine Verlängerung. Word, Excel und PowerPoint für PC oder Mac, so wie sie heute sind.",
                    "Un solo pago, sin renovaciones. Word, Excel y PowerPoint para PC o Mac, tal como son hoy.",
                    "Um único pagamento, sem renovações. Word, Excel e PowerPoint para PC ou Mac, tal como estão hoje.",
                    "Eén betaling, geen verlenging. Word, Excel en PowerPoint voor pc of Mac, zoals ze vandaag zijn.",
                ),
                "price": _d(
                    "€ 134,00 — licenza perpetua", "€ 134,00 — one-time licence", "€ 134,00 — licence unique",
                    "€ 134,00 — Einmallizenz", "€ 134,00 — licencia única", "€ 134,00 — licença única",
                    "€ 134,00 — eenmalige licentie",
                ),
                "cta": _d(
                    "Vedi la scheda", "See the listing", "Voir la fiche", "Zur Produktseite",
                    "Ver la ficha", "Ver a ficha", "Bekijk de productpagina",
                ),
                "href": "office-2024-home",
            },
            {
                "name": _d(*(["Microsoft 365 Personal"] * 7)),
                "blurb": _d(
                    "Abbonamento annuale: app sempre aggiornate, 1TB di spazio OneDrive e Copilot AI incluso.",
                    "Annual subscription: always up to date apps, 1TB of OneDrive storage and Copilot AI included.",
                    "Abonnement annuel : applications toujours à jour, 1 To d'espace OneDrive et Copilot AI inclus.",
                    "Jahresabo: immer aktuelle Apps, 1 TB OneDrive-Speicher und Copilot AI inklusive.",
                    "Suscripción anual: apps siempre actualizadas, 1 TB de espacio en OneDrive y Copilot AI incluido.",
                    "Subscrição anual: apps sempre atualizadas, 1 TB de espaço no OneDrive e Copilot AI incluído.",
                    "Jaarabonnement: altijd actuele apps, 1 TB OneDrive-opslag en Copilot AI inbegrepen.",
                ),
                "price": _d(
                    "€ 84,79 / anno", "€ 84,79 / year", "€ 84,79 / an", "€ 84,79 / Jahr",
                    "€ 84,79 / año", "€ 84,79 / ano", "€ 84,79 / jaar",
                ),
                "cta": _d(
                    "Vedi la scheda", "See the listing", "Voir la fiche", "Zur Produktseite",
                    "Ver la ficha", "Ver a ficha", "Bekijk de productpagina",
                ),
                "href": "microsoft-365-personal",
            },
        ],
        "table_caption": _d(*(["Office 2024 Home vs Microsoft 365 Personal"] * 7)),
        "table_headers": [
            _d("Caratteristica", "Feature", "Caractéristique", "Funktion", "Característica", "Característica", "Kenmerk"),
            _d(*(["Office 2024 Home"] * 7)),
            _d(*(["Microsoft 365 Personal"] * 7)),
        ],
        "table_rows": [
            [
                _d("Prezzo", "Price", "Prix", "Preis", "Precio", "Preço", "Prijs"),
                _d("€ 134,00 una tantum", "€ 134,00 one-time", "€ 134,00 une fois", "€ 134,00 einmalig", "€ 134,00 pago único", "€ 134,00 pagamento único", "€ 134,00 eenmalig"),
                _d("€ 84,79 / anno", "€ 84,79 / year", "€ 84,79 / an", "€ 84,79 / Jahr", "€ 84,79 / año", "€ 84,79 / ano", "€ 84,79 / jaar"),
            ],
            [
                _d("Formula", "Model", "Modèle", "Modell", "Modelo", "Modelo", "Model"),
                _d("Licenza perpetua", "One-time licence", "Licence unique", "Einmallizenz", "Licencia única", "Licença única", "Eenmalige licentie"),
                _d("Abbonamento", "Subscription", "Abonnement", "Abo", "Suscripción", "Subscrição", "Abonnement"),
            ],
            [
                _d("App incluse", "Apps included", "Applications incluses", "Enthaltene Apps", "Apps incluidas", "Apps incluídas", "Inbegrepen apps"),
                _d(*(["Word, Excel, PowerPoint"] * 7)),
                _d(*(["Word, Excel, PowerPoint, Outlook, Teams"] * 7)),
            ],
            [
                _d("Aggiornamenti", "Updates", "Mises à jour", "Updates", "Actualizaciones", "Atualizações", "Updates"),
                _d("Solo sicurezza", "Security only", "Sécurité uniquement", "Nur Sicherheit", "Solo seguridad", "Só segurança", "Alleen beveiliging"),
                _d("Funzioni nuove incluse", "New features included", "Nouvelles fonctions incluses", "Neue Funktionen inklusive", "Nuevas funciones incluidas", "Novas funcionalidades incluídas", "Nieuwe functies inbegrepen"),
            ],
            [
                _d("Spazio cloud OneDrive", "OneDrive cloud storage", "Espace cloud OneDrive", "OneDrive-Cloud-Speicher", "Espacio en la nube OneDrive", "Espaço na nuvem OneDrive", "OneDrive-cloudopslag"),
                _d("Non incluso", "Not included", "Non inclus", "Nicht enthalten", "No incluido", "Não incluído", "Niet inbegrepen"),
                _d(*(["1 TB"] * 7)),
            ],
            [
                _d(*(["Copilot AI"] * 7)),
                _d("Non incluso", "Not included", "Non inclus", "Nicht enthalten", "No incluido", "Não incluído", "Niet inbegrepen"),
                _d("Incluso", "Included", "Inclus", "Enthalten", "Incluido", "Incluído", "Inbegrepen"),
            ],
            [
                _d("Piattaforme", "Platforms", "Plateformes", "Plattformen", "Plataformas", "Plataformas", "Platforms"),
                _d(*(["PC / Mac"] * 7)),
                _d("PC / Mac / mobile", "PC / Mac / mobile", "PC / Mac / mobile", "PC / Mac / mobil", "PC / Mac / móvil", "PC / Mac / móvel", "Pc / Mac / mobiel"),
            ],
        ],
        "editorial_h2": _d(
            "Quale conviene, in base a come lo usi",
            "Which one pays off, depending on how you use it",
            "Ce qui est le plus rentable, selon votre usage",
            "Was sich lohnt, je nach Nutzung",
            "Qué compensa, según cómo lo uses",
            "O que compensa, consoante o uso",
            "Wat loont, afhankelijk van je gebruik",
        ),
        "editorial_paragraphs": _d(
            [
                "Se ti servono solo Word, Excel e PowerPoint per lavori occasionali e non ti interessano Copilot o lo spazio cloud, Office 2024 è la scelta più semplice: un pagamento e non ci pensi più.",
                "Se invece usi Office quotidianamente, vuoi restare aggiornato senza pensarci, ti serve backup automatico dei file su OneDrive o vuoi provare Copilot AI nelle app, Microsoft 365 offre di più a fronte di un costo ricorrente.",
                'Chi condivide l\'abbonamento con la famiglia trova invece più conveniente <a href="microsoft-365-family">Microsoft 365 Family</a>: stesso principio di Personal, fino a 6 persone.',
            ],
            [
                "If you only need Word, Excel and PowerPoint for occasional work and don't care about Copilot or cloud storage, Office 2024 is the simplest choice: one payment and you're done.",
                "If you use Office daily, want to stay up to date without thinking about it, need automatic file backup on OneDrive, or want to try Copilot AI in the apps, Microsoft 365 offers more in exchange for a recurring cost.",
                'If you\'re sharing the subscription with your family, <a href="microsoft-365-family">Microsoft 365 Family</a> is more cost-effective: same principle as Personal, up to 6 people.',
            ],
            [
                "Si vous n'avez besoin que de Word, Excel et PowerPoint pour un usage occasionnel et que Copilot ou l'espace cloud ne vous intéressent pas, Office 2024 est le choix le plus simple : un paiement, et vous n'y pensez plus.",
                "Si vous utilisez Office quotidiennement, voulez rester à jour sans y penser, avez besoin d'une sauvegarde automatique des fichiers sur OneDrive ou voulez essayer Copilot AI dans les applications, Microsoft 365 offre plus pour un coût récurrent.",
                'Ceux qui partagent l\'abonnement en famille trouveront <a href="microsoft-365-family">Microsoft 365 Family</a> plus avantageux : même principe que Personal, jusqu\'à 6 personnes.',
            ],
            [
                "Wenn Sie nur Word, Excel und PowerPoint für gelegentliche Arbeiten brauchen und Copilot oder Cloud-Speicher keine Rolle spielen, ist Office 2024 die einfachste Wahl: einmal zahlen, nicht mehr daran denken.",
                "Wenn Sie Office täglich nutzen, ohne Nachdenken aktuell bleiben wollen, eine automatische Dateisicherung auf OneDrive brauchen oder Copilot AI in den Apps ausprobieren möchten, bietet Microsoft 365 mehr gegen einen wiederkehrenden Preis.",
                'Wer das Abo mit der Familie teilt, findet <a href="microsoft-365-family">Microsoft 365 Family</a> günstiger: gleiches Prinzip wie Personal, bis zu 6 Personen.',
            ],
            [
                "Si solo necesitas Word, Excel y PowerPoint para trabajos ocasionales y no te interesan Copilot ni el espacio en la nube, Office 2024 es la opción más sencilla: un pago y no vuelves a pensarlo.",
                "Si usas Office a diario, quieres estar siempre actualizado sin pensarlo, necesitas copia de seguridad automática de archivos en OneDrive o quieres probar Copilot AI en las apps, Microsoft 365 ofrece más a cambio de un coste recurrente.",
                'Quien comparte la suscripción con la familia encontrará más rentable <a href="microsoft-365-family">Microsoft 365 Family</a>: mismo principio que Personal, hasta 6 personas.',
            ],
            [
                "Se só precisa do Word, Excel e PowerPoint para trabalhos ocasionais e o Copilot ou o espaço na nuvem não lhe interessam, o Office 2024 é a escolha mais simples: um pagamento e não pensa mais nisso.",
                "Se usa o Office diariamente, quer manter-se atualizado sem pensar nisso, precisa de cópia de segurança automática dos ficheiros no OneDrive ou quer experimentar o Copilot AI nas apps, o Microsoft 365 oferece mais em troca de um custo recorrente.",
                'Quem partilha a subscrição com a família considera mais vantajoso o <a href="microsoft-365-family">Microsoft 365 Family</a>: mesmo princípio do Personal, até 6 pessoas.',
            ],
            [
                "Heb je alleen Word, Excel en PowerPoint nodig voor incidenteel werk en interesseren Copilot of cloudopslag je niet, dan is Office 2024 de eenvoudigste keuze: één betaling en je hoeft er niet meer aan te denken.",
                "Gebruik je Office dagelijks, wil je moeiteloos up-to-date blijven, heb je automatische bestandsback-up op OneDrive nodig of wil je Copilot AI in de apps proberen, dan biedt Microsoft 365 meer in ruil voor een terugkerende kost.",
                'Wie het abonnement met het gezin deelt, vindt <a href="microsoft-365-family">Microsoft 365 Family</a> voordeliger: hetzelfde principe als Personal, tot 6 personen.',
            ],
        ),
        "faq_items": [
            {
                "q": _d(
                    "Office 2024 riceve gli stessi aggiornamenti di Microsoft 365?", "Does Office 2024 get the same updates as Microsoft 365?",
                    "Office 2024 reçoit-il les mêmes mises à jour que Microsoft 365 ?", "Erhält Office 2024 dieselben Updates wie Microsoft 365?",
                    "¿Office 2024 recibe las mismas actualizaciones que Microsoft 365?", "O Office 2024 recebe as mesmas atualizações que o Microsoft 365?",
                    "Krijgt Office 2024 dezelfde updates als Microsoft 365?",
                ),
                "a": _d(
                    "No: Office 2024 riceve aggiornamenti di sicurezza ma non le nuove funzioni introdotte via abbonamento, incluso Copilot — quelle restano esclusive di Microsoft 365, secondo Microsoft.",
                    "No: Office 2024 receives security updates but not the new features rolled out via subscription, Copilot included — those remain exclusive to Microsoft 365, according to Microsoft.",
                    "Non : Office 2024 reçoit des mises à jour de sécurité mais pas les nouvelles fonctions introduites via abonnement, Copilot inclus — celles-ci restent exclusives à Microsoft 365, selon Microsoft.",
                    "Nein: Office 2024 erhält Sicherheitsupdates, aber nicht die neuen Funktionen, die über das Abo eingeführt werden, Copilot eingeschlossen — diese bleiben laut Microsoft Microsoft 365 vorbehalten.",
                    "No: Office 2024 recibe actualizaciones de seguridad pero no las nuevas funciones que se lanzan vía suscripción, Copilot incluido — esas quedan exclusivas de Microsoft 365, según Microsoft.",
                    "Não: o Office 2024 recebe atualizações de segurança mas não as novas funcionalidades lançadas via subscrição, incluindo o Copilot — essas ficam exclusivas do Microsoft 365, segundo a Microsoft.",
                    "Nee: Office 2024 krijgt beveiligingsupdates maar niet de nieuwe functies die via het abonnement worden uitgebracht, Copilot inbegrepen — die blijven exclusief voor Microsoft 365, volgens Microsoft.",
                ),
            },
            {
                "q": _d(
                    "Conviene di più pagare una volta sola o abbonarsi?", "Is it better to pay once or subscribe?",
                    "Vaut-il mieux payer une fois ou s'abonner ?", "Lohnt es sich mehr, einmal zu zahlen oder ein Abo abzuschließen?",
                    "¿Compensa más pagar una vez o suscribirse?", "Compensa mais pagar de uma vez ou subscrever?",
                    "Is het voordeliger om één keer te betalen of een abonnement te nemen?",
                ),
                "a": _d(
                    "Dipende dall'orizzonte temporale: Office 2024 Home costa 134 € una tantum, Microsoft 365 Personal 84,79 € all'anno. Sopra i 2 anni la licenza perpetua costa meno, ma perde Copilot AI e lo spazio cloud incluso.",
                    "It depends on your time horizon: Office 2024 Home costs €134 once, Microsoft 365 Personal €84.79 a year. Past 2 years the one-time licence costs less, but you lose Copilot AI and the included cloud storage.",
                    "Cela dépend de votre horizon temporel : Office 2024 Home coûte 134 € une fois, Microsoft 365 Personal 84,79 € par an. Au-delà de 2 ans, la licence unique coûte moins cher, mais vous perdez Copilot AI et l'espace cloud inclus.",
                    "Das hängt vom Zeithorizont ab: Office 2024 Home kostet einmalig 134 €, Microsoft 365 Personal 84,79 € im Jahr. Nach 2 Jahren ist die Einmallizenz günstiger, verliert aber Copilot AI und den enthaltenen Cloud-Speicher.",
                    "Depende del horizonte temporal: Office 2024 Home cuesta 134 € de una vez, Microsoft 365 Personal 84,79 € al año. Pasados los 2 años, la licencia única cuesta menos, pero pierde Copilot AI y el espacio en la nube incluido.",
                    "Depende do horizonte temporal: o Office 2024 Home custa 134 € de uma vez, o Microsoft 365 Personal 84,79 € por ano. Acima de 2 anos, a licença única custa menos, mas perde o Copilot AI e o espaço na nuvem incluído.",
                    "Dat hangt af van je tijdshorizon: Office 2024 Home kost eenmalig € 134, Microsoft 365 Personal € 84,79 per jaar. Na 2 jaar is de eenmalige licentie goedkoper, maar mis je Copilot AI en de inbegrepen cloudopslag.",
                ),
            },
            {
                "q": _d(
                    "Cosa succede se non rinnovo Microsoft 365?", "What happens if I stop paying for Microsoft 365?",
                    "Que se passe-t-il si j'arrête de payer Microsoft 365 ?", "Was passiert, wenn ich Microsoft 365 nicht mehr bezahle?",
                    "¿Qué pasa si dejo de pagar Microsoft 365?", "O que acontece se deixar de pagar o Microsoft 365?",
                    "Wat gebeurt er als ik stop met betalen voor Microsoft 365?",
                ),
                "a": _d(
                    "Le app passano in modalità di sola visualizzazione e lo spazio cloud oltre i limiti gratuiti resta di sola lettura, secondo le condizioni Microsoft — i file restano tuoi.",
                    "The apps switch to view-only mode and cloud storage beyond the free limits becomes read-only, according to Microsoft's terms — your files stay yours.",
                    "Les applications passent en mode lecture seule et l'espace cloud au-delà des limites gratuites devient également en lecture seule, selon les conditions Microsoft — vos fichiers restent les vôtres.",
                    "Die Apps wechseln in den reinen Anzeigemodus, und Cloud-Speicher über die kostenlosen Grenzen hinaus wird laut Microsoft-Bedingungen nur noch lesbar — Ihre Dateien bleiben Ihnen erhalten.",
                    "Las apps pasan a modo de solo lectura y el espacio en la nube por encima de los límites gratuitos también queda en solo lectura, según las condiciones de Microsoft — tus archivos siguen siendo tuyos.",
                    "As apps passam a modo só de leitura e o espaço na nuvem acima dos limites gratuitos também fica só de leitura, segundo as condições da Microsoft — os ficheiros continuam seus.",
                    "De apps schakelen over naar alleen-lezen en cloudopslag boven de gratis limieten wordt eveneens alleen-lezen, volgens de voorwaarden van Microsoft — je bestanden blijven van jou.",
                ),
            },
            {
                "q": _d(
                    "Office 2024 Home include anche Outlook?", "Does Office 2024 Home include Outlook too?",
                    "Office 2024 Home inclut-il aussi Outlook ?", "Ist bei Office 2024 Home auch Outlook enthalten?",
                    "¿Office 2024 Home incluye también Outlook?", "O Office 2024 Home também inclui o Outlook?",
                    "Zit Outlook ook bij Office 2024 Home?",
                ),
                "a": _d(
                    'No: Outlook è incluso nella variante <a href="office-2024-home-business">Office 2024 Home &amp; Business</a>, non nella Home.',
                    'No: Outlook is included in the <a href="office-2024-home-business">Office 2024 Home &amp; Business</a> variant, not in Home.',
                    'Non : Outlook est inclus dans la variante <a href="office-2024-home-business">Office 2024 Home &amp; Business</a>, pas dans Home.',
                    'Nein: Outlook ist in der Variante <a href="office-2024-home-business">Office 2024 Home &amp; Business</a> enthalten, nicht in Home.',
                    'No: Outlook está incluido en la variante <a href="office-2024-home-business">Office 2024 Home &amp; Business</a>, no en Home.',
                    'Não: o Outlook está incluído na variante <a href="office-2024-home-business">Office 2024 Home &amp; Business</a>, não no Home.',
                    'Nee: Outlook zit bij de variant <a href="office-2024-home-business">Office 2024 Home &amp; Business</a>, niet bij Home.',
                ),
            },
        ],
        "disclaimer": _d(
            "Microsoft, Microsoft 365, Office, Copilot e i relativi marchi sono di Microsoft Corporation. Contenuto informativo Aml Store: funzionalità e condizioni seguono sempre il prodotto Microsoft acquistato.",
            "Microsoft, Microsoft 365, Office, Copilot and related marks are property of Microsoft Corporation. Informational content by Aml Store: features and terms always follow the Microsoft product purchased.",
            "Microsoft, Microsoft 365, Office, Copilot et les marques associées appartiennent à Microsoft Corporation. Contenu informatif Aml Store : fonctionnalités et conditions suivent toujours le produit Microsoft acheté.",
            "Microsoft, Microsoft 365, Office, Copilot und die zugehörigen Marken sind Eigentum der Microsoft Corporation. Informativer Inhalt von Aml Store: Funktionen und Bedingungen richten sich stets nach dem gekauften Microsoft-Produkt.",
            "Microsoft, Microsoft 365, Office, Copilot y las marcas relacionadas son propiedad de Microsoft Corporation. Contenido informativo de Aml Store: las funciones y condiciones siguen siempre el producto Microsoft adquirido.",
            "Microsoft, Microsoft 365, Office, Copilot e as marcas relacionadas são propriedade da Microsoft Corporation. Conteúdo informativo da Aml Store: funcionalidades e condições seguem sempre o produto Microsoft adquirido.",
            "Microsoft, Microsoft 365, Office, Copilot en de bijbehorende merken zijn eigendom van Microsoft Corporation. Informatieve inhoud van Aml Store: functies en voorwaarden volgen altijd het aangeschafte Microsoft-product.",
        ),
    },
    {
        "slug": "microsoft-365-family-vs-personal",
        "category_href": "microsoft-365-solutions",
        "og_image": "https://aml-store.com/asset/media/products/microsoft-365-family.webp",
        "meta_title": _d(
            "Microsoft 365 Family o Personal: quale scegliere | Aml Store",
            "Microsoft 365 Family or Personal: which one to choose | Aml Store",
            "Microsoft 365 Family ou Personal : lequel choisir | Aml Store",
            "Microsoft 365 Family oder Personal: welche Wahl | Aml Store",
            "Microsoft 365 Family o Personal: cuál elegir | Aml Store",
            "Microsoft 365 Family ou Personal: qual escolher | Aml Store",
            "Microsoft 365 Family of Personal: wat kies je | Aml Store",
        ),
        "meta_description": _d(
            "Microsoft 365 Family vs Personal: quante persone possono usarlo, spazio cloud, Copilot AI e differenza di prezzo. Guida alla scelta.",
            "Microsoft 365 Family vs Personal: how many people can use it, cloud storage, Copilot AI and the price difference. A guide to choosing.",
            "Microsoft 365 Family vs Personal : combien de personnes peuvent l'utiliser, espace cloud, Copilot AI et différence de prix. Guide pour choisir.",
            "Microsoft 365 Family vs. Personal: wie viele Personen es nutzen können, Cloud-Speicher, Copilot AI und der Preisunterschied. Ein Leitfaden zur Wahl.",
            "Microsoft 365 Family vs Personal: cuántas personas pueden usarlo, espacio en la nube, Copilot AI y diferencia de precio. Guía para elegir.",
            "Microsoft 365 Family vs Personal: quantas pessoas podem usá-lo, espaço na nuvem, Copilot AI e diferença de preço. Guia para escolher.",
            "Microsoft 365 Family vs Personal: hoeveel personen het kunnen gebruiken, cloudopslag, Copilot AI en het prijsverschil. Een gids om te kiezen.",
        ),
        "og_description": _d(
            "Differenza tra Microsoft 365 Family e Personal: persone coperte, spazio cloud, Copilot AI e prezzo.",
            "Difference between Microsoft 365 Family and Personal: people covered, cloud storage, Copilot AI and price.",
            "Différence entre Microsoft 365 Family et Personal : personnes couvertes, espace cloud, Copilot AI et prix.",
            "Unterschied zwischen Microsoft 365 Family und Personal: abgedeckte Personen, Cloud-Speicher, Copilot AI und Preis.",
            "Diferencia entre Microsoft 365 Family y Personal: personas cubiertas, espacio en la nube, Copilot AI y precio.",
            "Diferença entre o Microsoft 365 Family e o Personal: pessoas cobertas, espaço na nuvem, Copilot AI e preço.",
            "Verschil tussen Microsoft 365 Family en Personal: aantal personen, cloudopslag, Copilot AI en prijs.",
        ),
        "schema_name": _d(
            "Microsoft 365 Family o Personal: quale scegliere",
            "Microsoft 365 Family or Personal: which one to choose",
            "Microsoft 365 Family ou Personal : lequel choisir",
            "Microsoft 365 Family oder Personal: welche Wahl",
            "Microsoft 365 Family o Personal: cuál elegir",
            "Microsoft 365 Family ou Personal: qual escolher",
            "Microsoft 365 Family of Personal: wat kies je",
        ),
        "schema_description": _d(
            "Confronto tra Microsoft 365 Family e Personal: persone coperte, spazio cloud e Copilot AI.",
            "Comparison between Microsoft 365 Family and Personal: people covered, cloud storage and Copilot AI.",
            "Comparaison entre Microsoft 365 Family et Personal : personnes couvertes, espace cloud et Copilot AI.",
            "Vergleich zwischen Microsoft 365 Family und Personal: abgedeckte Personen, Cloud-Speicher und Copilot AI.",
            "Comparación entre Microsoft 365 Family y Personal: personas cubiertas, espacio en la nube y Copilot AI.",
            "Comparação entre o Microsoft 365 Family e o Personal: pessoas cobertas, espaço na nuvem e Copilot AI.",
            "Vergelijking tussen Microsoft 365 Family en Personal: aantal personen, cloudopslag en Copilot AI.",
        ),
        "breadcrumb_label": _d(*(["Family vs Personal"] * 7)),
        "hero_h1": _d(
            "Microsoft 365 Family o Personal: quale scegliere",
            "Microsoft 365 Family or Personal: which one to choose",
            "Microsoft 365 Family ou Personal : lequel choisir",
            "Microsoft 365 Family oder Personal: welche Wahl",
            "Microsoft 365 Family o Personal: cuál elegir",
            "Microsoft 365 Family ou Personal: qual escolher",
            "Microsoft 365 Family of Personal: wat kies je",
        ),
        "hero_lede": _d(
            "Stesse app, stesso principio di abbonamento. Cambia quante persone puoi coprire con un solo pagamento — e chi, tra loro, ottiene davvero Copilot AI.",
            "Same apps, same subscription principle. What changes is how many people you can cover with a single payment — and which of them actually gets Copilot AI.",
            "Mêmes applications, même principe d'abonnement. Ce qui change, c'est le nombre de personnes couvertes par un seul paiement — et qui, parmi elles, obtient vraiment Copilot AI.",
            "Gleiche Apps, gleiches Abo-Prinzip. Was sich ändert, ist die Anzahl der Personen, die mit einer einzigen Zahlung abgedeckt sind — und wer davon wirklich Copilot AI erhält.",
            "Mismas apps, mismo principio de suscripción. Lo que cambia es cuántas personas puedes cubrir con un solo pago — y quién de ellas obtiene realmente Copilot AI.",
            "As mesmas apps, o mesmo princípio de subscrição. O que muda é quantas pessoas consegue cobrir com um único pagamento — e qual delas obtém realmente o Copilot AI.",
            "Dezelfde apps, hetzelfde abonnementsprincipe. Wat verandert, is hoeveel personen je met één betaling dekt — en wie van hen echt Copilot AI krijgt.",
        ),
        "verdict": [
            {
                "name": _d(*(["Microsoft 365 Personal"] * 7)),
                "blurb": _d(
                    "Un solo account, 1TB di spazio OneDrive e Copilot AI. Pensato per chi lo usa da solo.",
                    "One account, 1TB of OneDrive storage and Copilot AI. Built for solo use.",
                    "Un seul compte, 1 To d'espace OneDrive et Copilot AI. Pensé pour un usage individuel.",
                    "Ein Konto, 1 TB OneDrive-Speicher und Copilot AI. Für die Einzelnutzung gedacht.",
                    "Una sola cuenta, 1 TB de espacio en OneDrive y Copilot AI. Pensado para uso individual.",
                    "Uma única conta, 1 TB de espaço no OneDrive e Copilot AI. Pensado para uso individual.",
                    "Eén account, 1 TB OneDrive-opslag en Copilot AI. Gemaakt voor individueel gebruik.",
                ),
                "price": _d(
                    "€ 84,79 / anno", "€ 84,79 / year", "€ 84,79 / an", "€ 84,79 / Jahr",
                    "€ 84,79 / año", "€ 84,79 / ano", "€ 84,79 / jaar",
                ),
                "cta": _d(
                    "Vedi la scheda", "See the listing", "Voir la fiche", "Zur Produktseite",
                    "Ver la ficha", "Ver a ficha", "Bekijk de productpagina",
                ),
                "href": "microsoft-365-personal",
            },
            {
                "name": _d(*(["Microsoft 365 Family"] * 7)),
                "blurb": _d(
                    "Fino a 6 persone, ciascuna con 1TB proprio. Copilot AI resta riservato al titolare.",
                    "Up to 6 people, each with their own 1TB. Copilot AI stays reserved for the account holder.",
                    "Jusqu'à 6 personnes, chacune avec son propre 1 To. Copilot AI reste réservé au titulaire.",
                    "Bis zu 6 Personen, jede mit eigenem 1 TB. Copilot AI bleibt dem Inhaber vorbehalten.",
                    "Hasta 6 personas, cada una con su propio 1 TB. Copilot AI queda reservado al titular.",
                    "Até 6 pessoas, cada uma com o seu próprio 1 TB. O Copilot AI fica reservado ao titular.",
                    "Tot 6 personen, elk met hun eigen 1 TB. Copilot AI blijft voorbehouden aan de accounthouder.",
                ),
                "price": _d(
                    "€ 104,95 / anno", "€ 104,95 / year", "€ 104,95 / an", "€ 104,95 / Jahr",
                    "€ 104,95 / año", "€ 104,95 / ano", "€ 104,95 / jaar",
                ),
                "cta": _d(
                    "Vedi la scheda", "See the listing", "Voir la fiche", "Zur Produktseite",
                    "Ver la ficha", "Ver a ficha", "Bekijk de productpagina",
                ),
                "href": "microsoft-365-family",
            },
        ],
        "table_caption": _d(*(["Microsoft 365 Personal vs Family"] * 7)),
        "table_headers": [
            _d("Caratteristica", "Feature", "Caractéristique", "Funktion", "Característica", "Característica", "Kenmerk"),
            _d(*(["Personal"] * 7)),
            _d(*(["Family"] * 7)),
        ],
        "table_rows": [
            [
                _d("Prezzo", "Price", "Prix", "Preis", "Precio", "Preço", "Prijs"),
                _d("€ 84,79 / anno", "€ 84,79 / year", "€ 84,79 / an", "€ 84,79 / Jahr", "€ 84,79 / año", "€ 84,79 / ano", "€ 84,79 / jaar"),
                _d("€ 104,95 / anno", "€ 104,95 / year", "€ 104,95 / an", "€ 104,95 / Jahr", "€ 104,95 / año", "€ 104,95 / ano", "€ 104,95 / jaar"),
            ],
            [
                _d("Persone coperte", "People covered", "Personnes couvertes", "Abgedeckte Personen", "Personas cubiertas", "Pessoas cobertas", "Aantal personen"),
                _d(*(["1"] * 7)),
                _d("Fino a 6", "Up to 6", "Jusqu'à 6", "Bis zu 6", "Hasta 6", "Até 6", "Tot 6"),
            ],
            [
                _d("Spazio OneDrive", "OneDrive storage", "Espace OneDrive", "OneDrive-Speicher", "Espacio OneDrive", "Espaço OneDrive", "OneDrive-opslag"),
                _d(*(["1 TB"] * 7)),
                _d(
                    "6 TB totali (1 TB a persona)", "6 TB total (1 TB per person)", "6 To au total (1 To par personne)",
                    "6 TB insgesamt (1 TB pro Person)", "6 TB en total (1 TB por persona)", "6 TB no total (1 TB por pessoa)",
                    "6 TB in totaal (1 TB per persoon)",
                ),
            ],
            [
                _d(*(["Copilot AI"] * 7)),
                _d("Incluso", "Included", "Inclus", "Enthalten", "Incluido", "Incluído", "Inbegrepen"),
                _d(
                    "Solo per il titolare", "Account holder only", "Titulaire uniquement", "Nur für den Inhaber",
                    "Solo para el titular", "Só para o titular", "Alleen voor de accounthouder",
                ),
            ],
            [
                _d("App Office incluse", "Office apps included", "Applications Office incluses", "Enthaltene Office-Apps", "Apps de Office incluidas", "Apps do Office incluídas", "Inbegrepen Office-apps"),
                _d(*(["Word, Excel, PowerPoint, Outlook, Teams"] * 7)),
                _d(
                    "Stesse app per ogni membro", "Same apps for every member", "Mêmes applications pour chaque membre",
                    "Gleiche Apps für jedes Mitglied", "Mismas apps para cada miembro", "Mesmas apps para cada membro",
                    "Dezelfde apps voor elk lid",
                ),
            ],
            [
                _d(
                    "Costo per persona (uso pieno)", "Cost per person (full use)", "Coût par personne (usage complet)",
                    "Kosten pro Person (volle Nutzung)", "Coste por persona (uso completo)", "Custo por pessoa (uso total)",
                    "Kosten per persoon (volledig gebruik)",
                ),
                _d("€ 84,79", "€ 84,79", "€ 84,79", "€ 84,79", "€ 84,79", "€ 84,79", "€ 84,79"),
                _d(
                    "da € 17,49 (in 6)", "from € 17,49 (with 6)", "à partir de € 17,49 (à 6)",
                    "ab € 17,49 (bei 6 Personen)", "desde € 17,49 (entre 6)", "a partir de € 17,49 (com 6)",
                    "vanaf € 17,49 (bij 6)",
                ),
            ],
        ],
        "editorial_h2": _d(
            "Il conto che conviene fare prima",
            "The maths worth doing first",
            "Le calcul à faire avant tout",
            "Die Rechnung, die sich vorher lohnt",
            "La cuenta que conviene hacer antes",
            "As contas que compensa fazer antes",
            "De rekensom die je vooraf moet maken",
        ),
        "editorial_paragraphs": _d(
            [
                "Personal ha senso se sei l'unica persona che userà l'abbonamento: paghi meno in assoluto e hai comunque Copilot AI e 1TB tutti per te.",
                "Family conviene già da due persone in su: il costo aggiuntivo rispetto a Personal (+20,16 €/anno) copre fino a 5 account in più, ciascuno con il proprio spazio cloud separato — non condiviso in un unico pool.",
                "L'unico limite da conoscere prima di acquistare: Copilot AI nelle app resta riservato al titolare dell'abbonamento Family, secondo la scheda del prodotto — gli altri membri hanno le app Office complete ma senza Copilot incluso.",
            ],
            [
                "Personal makes sense if you're the only one who'll use the subscription: you pay less overall and still get Copilot AI and 1TB all to yourself.",
                "Family pays off from two people upward: the extra cost over Personal (+€20.16/year) covers up to 5 more accounts, each with its own separate cloud storage — not shared from a single pool.",
                "The one limit worth knowing before buying: Copilot AI in the apps stays reserved for the Family subscription holder, according to the product listing — the other members get the full Office apps but without Copilot included.",
            ],
            [
                "Personal a du sens si vous êtes la seule personne à utiliser l'abonnement : vous payez moins au total et gardez Copilot AI et 1 To rien que pour vous.",
                "Family devient rentable dès deux personnes : le surcoût par rapport à Personal (+20,16 €/an) couvre jusqu'à 5 comptes supplémentaires, chacun avec son propre espace cloud séparé — non partagé dans un seul pool.",
                "La seule limite à connaître avant d'acheter : Copilot AI dans les applications reste réservé au titulaire de l'abonnement Family, selon la fiche du produit — les autres membres ont les applications Office complètes mais sans Copilot inclus.",
            ],
            [
                "Personal ist sinnvoll, wenn Sie die einzige Person sind, die das Abo nutzt: Sie zahlen insgesamt weniger und haben trotzdem Copilot AI und 1 TB ganz für sich.",
                "Family lohnt sich schon ab zwei Personen: Der Aufpreis gegenüber Personal (+20,16 €/Jahr) deckt bis zu 5 weitere Konten ab, jedes mit eigenem separatem Cloud-Speicher — nicht aus einem gemeinsamen Pool.",
                "Die einzige Einschränkung, die man vor dem Kauf kennen sollte: Copilot AI in den Apps bleibt laut Produktseite dem Inhaber des Family-Abos vorbehalten — die anderen Mitglieder erhalten die vollständigen Office-Apps, aber ohne Copilot.",
            ],
            [
                "Personal tiene sentido si eres la única persona que usará la suscripción: pagas menos en total y aun así tienes Copilot AI y 1 TB solo para ti.",
                "Family compensa ya desde dos personas: el coste adicional respecto a Personal (+20,16 €/año) cubre hasta 5 cuentas más, cada una con su propio espacio en la nube independiente — no compartido en un único conjunto.",
                "El único límite que conviene conocer antes de comprar: Copilot AI en las apps queda reservado al titular de la suscripción Family, según la ficha del producto — los demás miembros tienen las apps de Office completas pero sin Copilot incluido.",
            ],
            [
                "O Personal faz sentido se for a única pessoa a usar a subscrição: paga menos no total e continua a ter o Copilot AI e 1 TB só para si.",
                "O Family compensa já a partir de duas pessoas: o custo adicional face ao Personal (+20,16 €/ano) cobre até mais 5 contas, cada uma com o seu próprio espaço na nuvem separado — não partilhado num único conjunto.",
                "O único limite a conhecer antes de comprar: o Copilot AI nas apps fica reservado ao titular da subscrição Family, segundo a ficha do produto — os outros membros têm as apps do Office completas mas sem o Copilot incluído.",
            ],
            [
                "Personal is zinvol als jij de enige bent die het abonnement gebruikt: je betaalt in totaal minder en hebt toch Copilot AI en 1 TB helemaal voor jezelf.",
                "Family loont al vanaf twee personen: de meerprijs ten opzichte van Personal (+€20,16/jaar) dekt tot 5 extra accounts, elk met eigen aparte cloudopslag — niet gedeeld uit één pool.",
                "De enige beperking die je vooraf moet weten: Copilot AI in de apps blijft voorbehouden aan de houder van het Family-abonnement, volgens de productpagina — de andere leden krijgen de volledige Office-apps maar zonder Copilot.",
            ],
        ),
        "faq_items": [
            {
                "q": _d(
                    "Quante persone possono usare Microsoft 365 Family?", "How many people can use Microsoft 365 Family?",
                    "Combien de personnes peuvent utiliser Microsoft 365 Family ?", "Wie viele Personen können Microsoft 365 Family nutzen?",
                    "¿Cuántas personas pueden usar Microsoft 365 Family?", "Quantas pessoas podem usar o Microsoft 365 Family?",
                    "Hoeveel personen kunnen Microsoft 365 Family gebruiken?",
                ),
                "a": _d(
                    "Fino a 6 persone, ciascuna con il proprio account Microsoft, la propria installazione delle app e 1TB di spazio OneDrive personale.",
                    "Up to 6 people, each with their own Microsoft account, their own app installation and 1TB of personal OneDrive storage.",
                    "Jusqu'à 6 personnes, chacune avec son propre compte Microsoft, sa propre installation des applications et 1 To d'espace OneDrive personnel.",
                    "Bis zu 6 Personen, jede mit eigenem Microsoft-Konto, eigener App-Installation und 1 TB persönlichem OneDrive-Speicher.",
                    "Hasta 6 personas, cada una con su propia cuenta Microsoft, su propia instalación de las apps y 1 TB de espacio OneDrive personal.",
                    "Até 6 pessoas, cada uma com a sua própria conta Microsoft, a sua própria instalação das apps e 1 TB de espaço OneDrive pessoal.",
                    "Tot 6 personen, elk met een eigen Microsoft-account, een eigen app-installatie en 1 TB persoonlijke OneDrive-opslag.",
                ),
            },
            {
                "q": _d(
                    "Copilot AI è incluso per tutti i membri della Family?", "Is Copilot AI included for every Family member?",
                    "Copilot AI est-il inclus pour tous les membres de Family ?", "Ist Copilot AI für alle Family-Mitglieder enthalten?",
                    "¿Copilot AI está incluido para todos los miembros de Family?", "O Copilot AI está incluído para todos os membros do Family?",
                    "Is Copilot AI inbegrepen voor alle Family-leden?",
                ),
                "a": _d(
                    "No: secondo la scheda del prodotto, Copilot AI è incluso solo per il titolare dell'abbonamento Family, non per gli altri membri invitati.",
                    "No: according to the product listing, Copilot AI is included only for the Family subscription holder, not for the other invited members.",
                    "Non : selon la fiche du produit, Copilot AI est inclus uniquement pour le titulaire de l'abonnement Family, pas pour les autres membres invités.",
                    "Nein: Laut Produktseite ist Copilot AI nur für den Inhaber des Family-Abos enthalten, nicht für die anderen eingeladenen Mitglieder.",
                    "No: según la ficha del producto, Copilot AI está incluido solo para el titular de la suscripción Family, no para los demás miembros invitados.",
                    "Não: segundo a ficha do produto, o Copilot AI está incluído apenas para o titular da subscrição Family, não para os outros membros convidados.",
                    "Nee: volgens de productpagina is Copilot AI alleen inbegrepen voor de houder van het Family-abonnement, niet voor de andere uitgenodigde leden.",
                ),
            },
            {
                "q": _d(
                    "Conviene Family anche se in casa siamo solo in due?", "Does Family pay off even if it's just two of us at home?",
                    "Family est-il rentable même si nous ne sommes que deux à la maison ?", "Lohnt sich Family auch, wenn wir zu Hause nur zu zweit sind?",
                    "¿Compensa Family aunque en casa seamos solo dos?", "Compensa o Family mesmo que em casa sejamos só dois?",
                    "Loont Family ook als we thuis maar met z'n tweeën zijn?",
                ),
                "a": _d(
                    "Sì: Family costa 104,95 € contro 84,79 € di un singolo Personal — con 2 persone il costo per utente scende, e resta più conveniente di due abbonamenti Personal separati.",
                    "Yes: Family costs € 104,95 against € 84,79 for a single Personal — with 2 people the cost per user drops, and it stays cheaper than two separate Personal subscriptions.",
                    "Oui : Family coûte 104,95 € contre 84,79 € pour un seul Personal — à 2 personnes le coût par utilisateur baisse, et reste plus avantageux que deux abonnements Personal séparés.",
                    "Ja: Family kostet 104,95 € gegenüber 84,79 € für ein einzelnes Personal — bei 2 Personen sinken die Kosten pro Nutzer, und es bleibt günstiger als zwei separate Personal-Abos.",
                    "Sí: Family cuesta 104,95 € frente a 84,79 € de un Personal individual — con 2 personas el coste por usuario baja, y sigue siendo más económico que dos suscripciones Personal separadas.",
                    "Sim: o Family custa 104,95 € contra 84,79 € de um Personal individual — com 2 pessoas o custo por utilizador desce, e continua mais vantajoso do que duas subscrições Personal separadas.",
                    "Ja: Family kost € 104,95 tegenover € 84,79 voor een los Personal-abonnement — bij 2 personen daalt de kost per gebruiker, en dat blijft voordeliger dan twee losse Personal-abonnementen.",
                ),
            },
            {
                "q": _d(
                    "Ogni membro della Family ha il proprio spazio cloud separato?", "Does each Family member get their own separate cloud storage?",
                    "Chaque membre de Family dispose-t-il de son propre espace cloud séparé ?", "Hat jedes Family-Mitglied seinen eigenen separaten Cloud-Speicher?",
                    "¿Cada miembro de Family tiene su propio espacio en la nube independiente?", "Cada membro do Family tem o seu próprio espaço na nuvem separado?",
                    "Heeft elk Family-lid zijn eigen aparte cloudopslag?",
                ),
                "a": _d(
                    "Sì: i 6TB totali sono ripartiti in 1TB per ciascuna persona invitata, non condivisi in un unico spazio comune.",
                    "Yes: the 6TB total is split into 1TB for each invited person, not shared in a single common space.",
                    "Oui : les 6 To au total sont répartis en 1 To pour chaque personne invitée, non partagés dans un espace commun unique.",
                    "Ja: Die insgesamt 6 TB werden auf 1 TB pro eingeladener Person aufgeteilt, nicht aus einem gemeinsamen Speicher geteilt.",
                    "Sí: los 6 TB totales se reparten en 1 TB para cada persona invitada, no compartidos en un único espacio común.",
                    "Sim: os 6 TB totais são divididos em 1 TB para cada pessoa convidada, não partilhados num único espaço comum.",
                    "Ja: de 6 TB in totaal wordt verdeeld in 1 TB per uitgenodigde persoon, niet gedeeld in één gezamenlijke ruimte.",
                ),
            },
        ],
        "disclaimer": _d(
            "Microsoft, Microsoft 365, Copilot, OneDrive e i relativi marchi sono di Microsoft Corporation. Contenuto informativo Aml Store: condizioni e limiti seguono sempre il prodotto Microsoft acquistato.",
            "Microsoft, Microsoft 365, Copilot, OneDrive and related marks are property of Microsoft Corporation. Informational content by Aml Store: terms and limits always follow the Microsoft product purchased.",
            "Microsoft, Microsoft 365, Copilot, OneDrive et les marques associées appartiennent à Microsoft Corporation. Contenu informatif Aml Store : conditions et limites suivent toujours le produit Microsoft acheté.",
            "Microsoft, Microsoft 365, Copilot, OneDrive und die zugehörigen Marken sind Eigentum der Microsoft Corporation. Informativer Inhalt von Aml Store: Bedingungen und Grenzen richten sich stets nach dem gekauften Microsoft-Produkt.",
            "Microsoft, Microsoft 365, Copilot, OneDrive y las marcas relacionadas son propiedad de Microsoft Corporation. Contenido informativo de Aml Store: condiciones y límites siguen siempre el producto Microsoft adquirido.",
            "Microsoft, Microsoft 365, Copilot, OneDrive e as marcas relacionadas são propriedade da Microsoft Corporation. Conteúdo informativo da Aml Store: condições e limites seguem sempre o produto Microsoft adquirido.",
            "Microsoft, Microsoft 365, Copilot, OneDrive en de bijbehorende merken zijn eigendom van Microsoft Corporation. Informatieve inhoud van Aml Store: voorwaarden en limieten volgen altijd het aangeschafte Microsoft-product.",
        ),
    },
    {
        "slug": "kaspersky-vs-eset-nod32",
        "category_href": "antivirus",
        "og_image": "https://aml-store.com/asset/media/products/kaspersky-standard.webp",
        "meta_title": _d(
            "Kaspersky o ESET NOD32: quale antivirus scegliere | Aml Store",
            "Kaspersky or ESET NOD32: which antivirus to choose | Aml Store",
            "Kaspersky ou ESET NOD32 : quel antivirus choisir | Aml Store",
            "Kaspersky oder ESET NOD32: welches Antivirenprogramm | Aml Store",
            "Kaspersky o ESET NOD32: qué antivirus elegir | Aml Store",
            "Kaspersky ou ESET NOD32: qual antivírus escolher | Aml Store",
            "Kaspersky of ESET NOD32: welke antivirus kiezen | Aml Store",
        ),
        "meta_description": _d(
            "Kaspersky vs ESET NOD32: protezione bancaria e ottimizzazione PC contro un motore leggero a basso impatto. Prezzi e differenze per scegliere.",
            "Kaspersky vs ESET NOD32: banking protection and PC optimisation versus a lightweight, low-impact engine. Prices and differences to help you choose.",
            "Kaspersky vs ESET NOD32 : protection bancaire et optimisation du PC contre un moteur léger à faible impact. Prix et différences pour choisir.",
            "Kaspersky vs. ESET NOD32: Banking-Schutz und PC-Optimierung gegen eine schlanke, ressourcenschonende Engine. Preise und Unterschiede zur Auswahl.",
            "Kaspersky vs ESET NOD32: protección bancaria y optimización de PC frente a un motor ligero de bajo impacto. Precios y diferencias para elegir.",
            "Kaspersky vs ESET NOD32: proteção bancária e otimização do PC contra um motor leve de baixo impacto. Preços e diferenças para escolher.",
            "Kaspersky vs ESET NOD32: bankbescherming en pc-optimalisatie tegenover een lichte engine met lage impact. Prijzen en verschillen om te kiezen.",
        ),
        "og_description": _d(
            "Differenza tra Kaspersky Standard ed ESET NOD32: cosa include ciascuno e a chi conviene.",
            "Difference between Kaspersky Standard and ESET NOD32: what each includes and who it suits.",
            "Différence entre Kaspersky Standard et ESET NOD32 : ce que chacun inclut et à qui il convient.",
            "Unterschied zwischen Kaspersky Standard und ESET NOD32: was jeweils enthalten ist und wem es passt.",
            "Diferencia entre Kaspersky Standard y ESET NOD32: qué incluye cada uno y a quién conviene.",
            "Diferença entre o Kaspersky Standard e o ESET NOD32: o que cada um inclui e a quem convém.",
            "Verschil tussen Kaspersky Standard en ESET NOD32: wat elk bevat en voor wie het geschikt is.",
        ),
        "schema_name": _d(
            "Kaspersky o ESET NOD32: quale antivirus scegliere",
            "Kaspersky or ESET NOD32: which antivirus to choose",
            "Kaspersky ou ESET NOD32 : quel antivirus choisir",
            "Kaspersky oder ESET NOD32: welches Antivirenprogramm",
            "Kaspersky o ESET NOD32: qué antivirus elegir",
            "Kaspersky ou ESET NOD32: qual antivírus escolher",
            "Kaspersky of ESET NOD32: welke antivirus kiezen",
        ),
        "schema_description": _d(
            "Confronto tra Kaspersky Standard ed ESET NOD32 Antivirus: protezione, impatto sulle risorse e prezzo.",
            "Comparison between Kaspersky Standard and ESET NOD32 Antivirus: protection, resource impact and price.",
            "Comparaison entre Kaspersky Standard et ESET NOD32 Antivirus : protection, impact sur les ressources et prix.",
            "Vergleich zwischen Kaspersky Standard und ESET NOD32 Antivirus: Schutz, Ressourcenbelastung und Preis.",
            "Comparación entre Kaspersky Standard y ESET NOD32 Antivirus: protección, impacto en los recursos y precio.",
            "Comparação entre o Kaspersky Standard e o ESET NOD32 Antivírus: proteção, impacto nos recursos e preço.",
            "Vergelijking tussen Kaspersky Standard en ESET NOD32 Antivirus: bescherming, impact op systeembronnen en prijs.",
        ),
        "breadcrumb_label": _d(*(["Kaspersky vs ESET NOD32"] * 7)),
        "hero_h1": _d(
            "Kaspersky o ESET NOD32: quale antivirus scegliere",
            "Kaspersky or ESET NOD32: which antivirus to choose",
            "Kaspersky ou ESET NOD32 : quel antivirus choisir",
            "Kaspersky oder ESET NOD32: welches Antivirenprogramm wählen",
            "Kaspersky o ESET NOD32: qué antivirus elegir",
            "Kaspersky ou ESET NOD32: qual antivírus escolher",
            "Kaspersky of ESET NOD32: welke antivirus kiezen",
        ),
        "hero_lede": _d(
            "Due filosofie diverse: Kaspersky punta su protezione bancaria e strumenti di ottimizzazione, ESET NOD32 su un motore leggero pensato per non rallentare il PC.",
            "Two different philosophies: Kaspersky focuses on banking protection and optimisation tools, ESET NOD32 on a lightweight engine designed not to slow down your PC.",
            "Deux philosophies différentes : Kaspersky mise sur la protection bancaire et des outils d'optimisation, ESET NOD32 sur un moteur léger conçu pour ne pas ralentir le PC.",
            "Zwei unterschiedliche Philosophien: Kaspersky setzt auf Banking-Schutz und Optimierungstools, ESET NOD32 auf eine schlanke Engine, die den PC nicht ausbremsen soll.",
            "Dos filosofías distintas: Kaspersky apuesta por la protección bancaria y herramientas de optimización, ESET NOD32 por un motor ligero pensado para no ralentizar el PC.",
            "Duas filosofias diferentes: o Kaspersky aposta na proteção bancária e em ferramentas de otimização, o ESET NOD32 num motor leve pensado para não abrandar o PC.",
            "Twee verschillende filosofieën: Kaspersky zet in op bankbescherming en optimalisatietools, ESET NOD32 op een lichte engine die de pc niet mag vertragen.",
        ),
        "verdict": [
            {
                "name": _d(*(["Kaspersky Standard"] * 7)),
                "blurb": _d(
                    "Protezione real-time, navigazione bancaria protetta e strumenti di ottimizzazione PC inclusi.",
                    "Real-time protection, protected banking browsing and PC optimisation tools included.",
                    "Protection en temps réel, navigation bancaire protégée et outils d'optimisation du PC inclus.",
                    "Echtzeitschutz, geschütztes Banking-Browsing und PC-Optimierungstools inklusive.",
                    "Protección en tiempo real, navegación bancaria protegida y herramientas de optimización de PC incluidas.",
                    "Proteção em tempo real, navegação bancária protegida e ferramentas de otimização do PC incluídas.",
                    "Realtime bescherming, beveiligd bankieren en pc-optimalisatietools inbegrepen.",
                ),
                "price": _d(
                    "€ 19,56 — 1 dispositivo / 1 anno", "€ 19,56 — 1 device / 1 year", "€ 19,56 — 1 appareil / 1 an",
                    "€ 19,56 — 1 Gerät / 1 Jahr", "€ 19,56 — 1 dispositivo / 1 año", "€ 19,56 — 1 dispositivo / 1 ano",
                    "€ 19,56 — 1 apparaat / 1 jaar",
                ),
                "cta": _d(
                    "Vedi la scheda", "See the listing", "Voir la fiche", "Zur Produktseite",
                    "Ver la ficha", "Ver a ficha", "Bekijk de productpagina",
                ),
                "href": "kaspersky-standard",
            },
            {
                "name": _d(*(["ESET NOD32"] * 7)),
                "blurb": _d(
                    "Protezione proattiva con scansioni rapide e impatto minimo sulle risorse del PC.",
                    "Proactive protection with fast scans and minimal impact on PC resources.",
                    "Protection proactive avec analyses rapides et impact minimal sur les ressources du PC.",
                    "Proaktiver Schutz mit schnellen Scans und minimaler Belastung der PC-Ressourcen.",
                    "Protección proactiva con análisis rápidos e impacto mínimo en los recursos del PC.",
                    "Proteção proativa com análises rápidas e impacto mínimo nos recursos do PC.",
                    "Proactieve bescherming met snelle scans en minimale impact op de pc-bronnen.",
                ),
                "price": _d(
                    "€ 22,65 — 1 dispositivo / 1 anno", "€ 22,65 — 1 device / 1 year", "€ 22,65 — 1 appareil / 1 an",
                    "€ 22,65 — 1 Gerät / 1 Jahr", "€ 22,65 — 1 dispositivo / 1 año", "€ 22,65 — 1 dispositivo / 1 ano",
                    "€ 22,65 — 1 apparaat / 1 jaar",
                ),
                "cta": _d(
                    "Vedi la scheda", "See the listing", "Voir la fiche", "Zur Produktseite",
                    "Ver la ficha", "Ver a ficha", "Bekijk de productpagina",
                ),
                "href": "eset-nod32-1-device",
            },
        ],
        "table_caption": _d(
            "Kaspersky Standard vs ESET NOD32, 1 dispositivo / 1 anno",
            "Kaspersky Standard vs ESET NOD32, 1 device / 1 year",
            "Kaspersky Standard vs ESET NOD32, 1 appareil / 1 an",
            "Kaspersky Standard vs. ESET NOD32, 1 Gerät / 1 Jahr",
            "Kaspersky Standard vs ESET NOD32, 1 dispositivo / 1 año",
            "Kaspersky Standard vs ESET NOD32, 1 dispositivo / 1 ano",
            "Kaspersky Standard vs ESET NOD32, 1 apparaat / 1 jaar",
        ),
        "table_headers": [
            _d("Caratteristica", "Feature", "Caractéristique", "Funktion", "Característica", "Característica", "Kenmerk"),
            _d(*(["Kaspersky Standard"] * 7)),
            _d(*(["ESET NOD32"] * 7)),
        ],
        "table_rows": [
            [
                _d("Prezzo", "Price", "Prix", "Preis", "Precio", "Preço", "Prijs"),
                _d(*(["€ 19,56"] * 7)),
                _d(*(["€ 22,65"] * 7)),
            ],
            [
                _d(
                    "Protezione virus/malware/ransomware", "Virus/malware/ransomware protection", "Protection virus/malware/ransomware",
                    "Schutz vor Viren/Malware/Ransomware", "Protección virus/malware/ransomware", "Proteção contra vírus/malware/ransomware",
                    "Bescherming tegen virussen/malware/ransomware",
                ),
                _d("Sì", "Yes", "Oui", "Ja", "Sí", "Sim", "Ja"),
                _d("Sì", "Yes", "Oui", "Ja", "Sí", "Sim", "Ja"),
            ],
            [
                _d(
                    "Protezione dati bancari", "Banking data protection", "Protection des données bancaires",
                    "Schutz von Bankdaten", "Protección de datos bancarios", "Proteção de dados bancários",
                    "Bescherming van bankgegevens",
                ),
                _d("Sì", "Yes", "Oui", "Ja", "Sí", "Sim", "Ja"),
                _d(
                    "Non specificata in scheda", "Not stated on listing", "Non précisé sur la fiche",
                    "Auf der Produktseite nicht angegeben", "No especificada en la ficha", "Não especificada na ficha",
                    "Niet vermeld op productpagina",
                ),
            ],
            [
                _d(
                    "Ottimizzazione PC inclusa", "PC optimisation included", "Optimisation PC incluse",
                    "PC-Optimierung enthalten", "Optimización de PC incluida", "Otimização do PC incluída",
                    "Pc-optimalisatie inbegrepen",
                ),
                _d("Sì", "Yes", "Oui", "Ja", "Sí", "Sim", "Ja"),
                _d(
                    "Non specificata in scheda", "Not stated on listing", "Non précisé sur la fiche",
                    "Auf der Produktseite nicht angegeben", "No especificada en la ficha", "Não especificada na ficha",
                    "Niet vermeld op productpagina",
                ),
            ],
            [
                _d(
                    "Focus dichiarato dal produttore", "Focus stated by the maker", "Priorité affichée par l'éditeur",
                    "Vom Hersteller angegebener Fokus", "Enfoque declarado por el fabricante", "Foco declarado pelo fabricante",
                    "Door de fabrikant genoemde focus",
                ),
                _d(
                    "Protezione completa", "Full protection", "Protection complète", "Umfassender Schutz",
                    "Protección completa", "Proteção completa", "Volledige bescherming",
                ),
                _d(
                    "Basso impatto sulle risorse", "Low resource impact", "Faible impact sur les ressources",
                    "Geringe Ressourcenbelastung", "Bajo impacto en los recursos", "Baixo impacto nos recursos",
                    "Lage impact op systeembronnen",
                ),
            ],
            [
                _d("Attivazione", "Activation", "Activation", "Aktivierung", "Activación", "Ativação", "Activering"),
                _d(*(["My Kaspersky"] * 7)),
                _d(*(["ESET HOME"] * 7)),
            ],
            [
                _d(
                    "Varianti dispositivi disponibili", "Device variants available", "Variantes d'appareils disponibles",
                    "Verfügbare Gerätevarianten", "Variantes de dispositivos disponibles", "Variantes de dispositivos disponíveis",
                    "Beschikbare apparaatvarianten",
                ),
                _d(
                    "1 (Standard/Plus/Premium a prezzi diversi)", "1 (Standard/Plus/Premium at different prices)",
                    "1 (Standard/Plus/Premium à prix différents)", "1 (Standard/Plus/Premium zu unterschiedlichen Preisen)",
                    "1 (Standard/Plus/Premium a distintos precios)", "1 (Standard/Plus/Premium a preços diferentes)",
                    "1 (Standard/Plus/Premium tegen verschillende prijzen)",
                ),
                _d(*(["1, 2, 3, 5, 10"] * 7)),
            ],
        ],
        "editorial_h2": _d(
            "A chi conviene l'uno o l'altro",
            "Who each one suits",
            "À qui l'un ou l'autre convient",
            "Wem das eine oder das andere passt",
            "A quién le conviene uno u otro",
            "A quem convém cada um",
            "Voor wie het ene of het andere geschikt is",
        ),
        "editorial_paragraphs": _d(
            [
                "Se fai acquisti online spesso o vuoi anche strumenti per mantenere il PC pulito e veloce, Kaspersky Standard copre entrambe le esigenze in un unico pacchetto.",
                "Se invece il PC non è recente, lo usi per gaming o lavori dove ogni rallentamento si nota, ESET NOD32 è pensato apposta per scansioni rapide e un impatto minimo sulle risorse, secondo ESET.",
                "Entrambe le marche offrono licenze da 1 a 10 dispositivi: se devi coprire più PC in famiglia, il prezzo per dispositivo scende con le varianti multi-device in catalogo.",
            ],
            [
                "If you shop online often or also want tools to keep your PC clean and fast, Kaspersky Standard covers both needs in a single package.",
                "If instead your PC isn't recent, you use it for gaming or work where every slowdown is noticeable, ESET NOD32 is built specifically for fast scans and minimal resource impact, according to ESET.",
                "Both brands offer licences from 1 to 10 devices: if you need to cover several PCs at home, the price per device drops with the multi-device variants in the catalogue.",
            ],
            [
                "Si vous faites souvent des achats en ligne ou voulez aussi des outils pour garder votre PC propre et rapide, Kaspersky Standard couvre les deux besoins dans un seul pack.",
                "Si en revanche votre PC n'est pas récent, que vous l'utilisez pour le jeu ou pour des tâches où chaque ralentissement se remarque, ESET NOD32 est pensé spécifiquement pour des analyses rapides et un impact minimal sur les ressources, selon ESET.",
                "Les deux marques proposent des licences de 1 à 10 appareils : si vous devez couvrir plusieurs PC à la maison, le prix par appareil baisse avec les variantes multi-appareils du catalogue.",
            ],
            [
                "Wenn Sie oft online einkaufen oder auch Tools wollen, um Ihren PC sauber und schnell zu halten, deckt Kaspersky Standard beide Bedürfnisse in einem Paket ab.",
                "Ist Ihr PC dagegen nicht mehr neu, nutzen Sie ihn zum Gaming oder für Arbeiten, bei denen jede Verlangsamung auffällt, ist ESET NOD32 laut ESET speziell für schnelle Scans und minimale Ressourcenbelastung ausgelegt.",
                "Beide Marken bieten Lizenzen für 1 bis 10 Geräte: Wenn Sie mehrere PCs in der Familie abdecken müssen, sinkt der Preis pro Gerät mit den Multi-Device-Varianten im Katalog.",
            ],
            [
                "Si haces compras online a menudo o también quieres herramientas para mantener el PC limpio y rápido, Kaspersky Standard cubre ambas necesidades en un solo paquete.",
                "Si en cambio tu PC no es reciente, lo usas para gaming o para trabajos donde cualquier ralentización se nota, ESET NOD32 está pensado precisamente para análisis rápidos e impacto mínimo en los recursos, según ESET.",
                "Ambas marcas ofrecen licencias de 1 a 10 dispositivos: si necesitas cubrir varios PC en familia, el precio por dispositivo baja con las variantes multidispositivo del catálogo.",
            ],
            [
                "Se faz compras online com frequência ou também quer ferramentas para manter o PC limpo e rápido, o Kaspersky Standard cobre as duas necessidades num único pacote.",
                "Se, pelo contrário, o seu PC não é recente, usa-o para jogos ou para trabalhos onde qualquer lentidão se nota, o ESET NOD32 é pensado especificamente para análises rápidas e impacto mínimo nos recursos, segundo a ESET.",
                "Ambas as marcas oferecem licenças de 1 a 10 dispositivos: se precisar de cobrir vários PC em família, o preço por dispositivo desce com as variantes multidispositivo no catálogo.",
            ],
            [
                "Als je vaak online winkelt of ook tools wilt om je pc schoon en snel te houden, dekt Kaspersky Standard beide behoeften in één pakket.",
                "Is je pc daarentegen niet recent, gebruik je hem voor gaming of voor werk waarbij elke vertraging opvalt, dan is ESET NOD32 volgens ESET specifiek gemaakt voor snelle scans en minimale impact op de systeembronnen.",
                "Beide merken bieden licenties van 1 tot 10 apparaten: moet je meerdere pc's in het gezin dekken, dan daalt de prijs per apparaat met de multi-device-varianten in de catalogus.",
            ],
        ),
        "faq_items": [
            {
                "q": _d(
                    "Qual è il più leggero tra Kaspersky ed ESET NOD32?", "Which is lighter, Kaspersky or ESET NOD32?",
                    "Lequel est le plus léger entre Kaspersky et ESET NOD32 ?", "Was ist leichter, Kaspersky oder ESET NOD32?",
                    "¿Cuál es más ligero, Kaspersky o ESET NOD32?", "Qual é o mais leve, o Kaspersky ou o ESET NOD32?",
                    "Wat is lichter, Kaspersky of ESET NOD32?",
                ),
                "a": _d(
                    "ESET NOD32 è posizionato dal produttore su scansioni rapide e basso impatto sulle risorse — indicato per PC meno recenti o per il gaming.",
                    "ESET NOD32 is positioned by its maker around fast scans and low resource impact — worth considering for older PCs or gaming.",
                    "ESET NOD32 est positionné par son éditeur sur des analyses rapides et un faible impact sur les ressources — à envisager pour un PC moins récent ou pour le jeu.",
                    "ESET NOD32 ist vom Hersteller auf schnelle Scans und geringe Ressourcenbelastung ausgelegt — empfehlenswert für ältere PCs oder zum Gaming.",
                    "ESET NOD32 está posicionado por el fabricante en torno a análisis rápidos y bajo impacto en los recursos — recomendable para PC menos recientes o para gaming.",
                    "O ESET NOD32 é posicionado pelo fabricante em torno de análises rápidas e baixo impacto nos recursos — indicado para PCs menos recentes ou para jogos.",
                    "ESET NOD32 wordt door de fabrikant gepositioneerd rond snelle scans en lage impact op systeembronnen — de moeite waard bij een oudere pc of voor gaming.",
                ),
            },
            {
                "q": _d(
                    "Kaspersky protegge anche gli acquisti online?", "Does Kaspersky also protect online purchases?",
                    "Kaspersky protège-t-il aussi les achats en ligne ?", "Schützt Kaspersky auch Online-Einkäufe?",
                    "¿Kaspersky también protege las compras online?", "O Kaspersky também protege as compras online?",
                    "Beschermt Kaspersky ook online aankopen?",
                ),
                "a": _d(
                    "Sì: Kaspersky include strumenti dedicati alla navigazione protetta e alla difesa dei dati bancari durante gli acquisti, secondo la scheda del prodotto.",
                    "Yes: Kaspersky includes tools dedicated to protected browsing and defending banking data during purchases, according to the product listing.",
                    "Oui : Kaspersky inclut des outils dédiés à la navigation protégée et à la défense des données bancaires pendant les achats, selon la fiche du produit.",
                    "Ja: Kaspersky enthält laut Produktseite Tools für geschütztes Browsing und den Schutz von Bankdaten beim Einkaufen.",
                    "Sí: Kaspersky incluye herramientas dedicadas a la navegación protegida y a la defensa de los datos bancarios durante las compras, según la ficha del producto.",
                    "Sim: o Kaspersky inclui ferramentas dedicadas à navegação protegida e à defesa de dados bancários durante as compras, segundo a ficha do produto.",
                    "Ja: Kaspersky bevat volgens de productpagina tools voor beveiligd surfen en de bescherming van bankgegevens tijdens aankopen.",
                ),
            },
            {
                "q": _d(
                    "Kaspersky Plus o Premium aggiungono funzioni rispetto a Standard?", "Do Kaspersky Plus or Premium add features over Standard?",
                    "Kaspersky Plus ou Premium ajoutent-ils des fonctions par rapport à Standard ?", "Bieten Kaspersky Plus oder Premium mehr Funktionen als Standard?",
                    "¿Kaspersky Plus o Premium añaden funciones respecto a Standard?", "O Kaspersky Plus ou Premium acrescentam funcionalidades em relação ao Standard?",
                    "Voegen Kaspersky Plus of Premium functies toe ten opzichte van Standard?",
                ),
                "a": _d(
                    "Sono tre livelli della stessa linea Kaspersky con prezzo crescente; verifica sulla scheda del piano specifico cosa è incluso prima di scegliere quello più costoso.",
                    "They're three tiers of the same Kaspersky line with increasing price; check the specific plan's listing for what's included before choosing the pricier one.",
                    "Ce sont trois niveaux de la même gamme Kaspersky à prix croissant ; vérifiez sur la fiche du plan spécifique ce qui est inclus avant de choisir le plus cher.",
                    "Es handelt sich um drei Stufen derselben Kaspersky-Linie mit steigendem Preis; prüfen Sie auf der Seite des jeweiligen Plans, was enthalten ist, bevor Sie die teurere Variante wählen.",
                    "Son tres niveles de la misma línea Kaspersky con precio creciente; comprueba en la ficha del plan específico qué incluye antes de elegir el más caro.",
                    "São três níveis da mesma linha Kaspersky com preço crescente; verifique na ficha do plano específico o que está incluído antes de escolher o mais caro.",
                    "Het zijn drie niveaus van dezelfde Kaspersky-lijn met oplopende prijs; controleer op de productpagina van het specifieke plan wat is inbegrepen voordat je voor de duurdere variant kiest.",
                ),
            },
            {
                "q": _d(
                    "Posso proteggere più dispositivi con la stessa licenza?", "Can I protect more than one device with the same licence?",
                    "Puis-je protéger plusieurs appareils avec la même licence ?", "Kann ich mit derselben Lizenz mehrere Geräte schützen?",
                    "¿Puedo proteger varios dispositivos con la misma licencia?", "Posso proteger vários dispositivos com a mesma licença?",
                    "Kan ik meerdere apparaten beschermen met dezelfde licentie?",
                ),
                "a": _d(
                    "Sì, entrambe le marche hanno varianti da 1 a 10 dispositivi sulla stessa licenza annuale in catalogo.",
                    "Yes, both brands have variants from 1 to 10 devices on the same annual licence in the catalogue.",
                    "Oui, les deux marques proposent des variantes de 1 à 10 appareils sur la même licence annuelle du catalogue.",
                    "Ja, beide Marken bieten im Katalog Varianten für 1 bis 10 Geräte auf derselben Jahreslizenz.",
                    "Sí, ambas marcas tienen variantes de 1 a 10 dispositivos con la misma licencia anual en el catálogo.",
                    "Sim, ambas as marcas têm variantes de 1 a 10 dispositivos na mesma licença anual no catálogo.",
                    "Ja, beide merken hebben in de catalogus varianten van 1 tot 10 apparaten op dezelfde jaarlicentie.",
                ),
            },
        ],
        "disclaimer": _d(
            "Kaspersky ed ESET sono marchi dei rispettivi produttori. Contenuto informativo Aml Store: funzionalità e condizioni seguono sempre il prodotto acquistato.",
            "Kaspersky and ESET are trademarks of their respective makers. Informational content by Aml Store: features and terms always follow the product purchased.",
            "Kaspersky et ESET sont des marques de leurs éditeurs respectifs. Contenu informatif Aml Store : fonctionnalités et conditions suivent toujours le produit acheté.",
            "Kaspersky und ESET sind Marken ihrer jeweiligen Hersteller. Informativer Inhalt von Aml Store: Funktionen und Bedingungen richten sich stets nach dem gekauften Produkt.",
            "Kaspersky y ESET son marcas de sus respectivos fabricantes. Contenido informativo de Aml Store: funciones y condiciones siguen siempre el producto adquirido.",
            "Kaspersky e ESET são marcas dos respetivos fabricantes. Conteúdo informativo da Aml Store: funcionalidades e condições seguem sempre o produto adquirido.",
            "Kaspersky en ESET zijn merken van hun respectieve fabrikanten. Informatieve inhoud van Aml Store: functies en voorwaarden volgen altijd het aangeschafte product.",
        ),
    },
    {
        "slug": "norton-vs-bitdefender",
        "category_href": "antivirus",
        "og_image": "https://aml-store.com/asset/media/products/norton-360-standard.webp",
        "meta_title": _d(
            "Norton o Bitdefender: quale antivirus scegliere | Aml Store",
            "Norton or Bitdefender: which antivirus to choose | Aml Store",
            "Norton ou Bitdefender : quel antivirus choisir | Aml Store",
            "Norton oder Bitdefender: welches Antivirenprogramm | Aml Store",
            "Norton o Bitdefender: qué antivirus elegir | Aml Store",
            "Norton ou Bitdefender: qual antivírus escolher | Aml Store",
            "Norton of Bitdefender: welke antivirus kiezen | Aml Store",
        ),
        "meta_description": _d(
            "Norton 360 vs Bitdefender Plus: VPN e backup cloud inclusi contro un motore leggero anti-phishing. Prezzi e differenze per scegliere.",
            "Norton 360 vs Bitdefender Plus: VPN and cloud backup included versus a lightweight anti-phishing engine. Prices and differences to help you choose.",
            "Norton 360 vs Bitdefender Plus : VPN et sauvegarde cloud inclus contre un moteur léger anti-phishing. Prix et différences pour choisir.",
            "Norton 360 vs. Bitdefender Plus: VPN und Cloud-Backup inklusive gegen eine schlanke Anti-Phishing-Engine. Preise und Unterschiede zur Auswahl.",
            "Norton 360 vs Bitdefender Plus: VPN y copia de seguridad en la nube incluidas frente a un motor ligero antiphishing. Precios y diferencias para elegir.",
            "Norton 360 vs Bitdefender Plus: VPN e cópia de segurança na nuvem incluídas contra um motor leve antiphishing. Preços e diferenças para escolher.",
            "Norton 360 vs Bitdefender Plus: VPN en cloudback-up inbegrepen tegenover een lichte anti-phishing-engine. Prijzen en verschillen om te kiezen.",
        ),
        "og_description": _d(
            "Differenza tra Norton 360 Standard e Bitdefender Plus: cosa include ciascuno e a chi conviene.",
            "Difference between Norton 360 Standard and Bitdefender Plus: what each includes and who it suits.",
            "Différence entre Norton 360 Standard et Bitdefender Plus : ce que chacun inclut et à qui il convient.",
            "Unterschied zwischen Norton 360 Standard und Bitdefender Plus: was jeweils enthalten ist und wem es passt.",
            "Diferencia entre Norton 360 Standard y Bitdefender Plus: qué incluye cada uno y a quién conviene.",
            "Diferença entre o Norton 360 Standard e o Bitdefender Plus: o que cada um inclui e a quem convém.",
            "Verschil tussen Norton 360 Standard en Bitdefender Plus: wat elk bevat en voor wie het geschikt is.",
        ),
        "schema_name": _d(
            "Norton o Bitdefender: quale antivirus scegliere",
            "Norton or Bitdefender: which antivirus to choose",
            "Norton ou Bitdefender : quel antivirus choisir",
            "Norton oder Bitdefender: welches Antivirenprogramm",
            "Norton o Bitdefender: qué antivirus elegir",
            "Norton ou Bitdefender: qual antivírus escolher",
            "Norton of Bitdefender: welke antivirus kiezen",
        ),
        "schema_description": _d(
            "Confronto tra Norton 360 Standard e Bitdefender Plus: VPN, backup cloud e impatto sulle risorse.",
            "Comparison between Norton 360 Standard and Bitdefender Plus: VPN, cloud backup and resource impact.",
            "Comparaison entre Norton 360 Standard et Bitdefender Plus : VPN, sauvegarde cloud et impact sur les ressources.",
            "Vergleich zwischen Norton 360 Standard und Bitdefender Plus: VPN, Cloud-Backup und Ressourcenbelastung.",
            "Comparación entre Norton 360 Standard y Bitdefender Plus: VPN, copia de seguridad en la nube e impacto en los recursos.",
            "Comparação entre o Norton 360 Standard e o Bitdefender Plus: VPN, cópia de segurança na nuvem e impacto nos recursos.",
            "Vergelijking tussen Norton 360 Standard en Bitdefender Plus: VPN, cloudback-up en impact op systeembronnen.",
        ),
        "breadcrumb_label": _d(*(["Norton vs Bitdefender"] * 7)),
        "hero_h1": _d(
            "Norton o Bitdefender: quale antivirus scegliere",
            "Norton or Bitdefender: which antivirus to choose",
            "Norton ou Bitdefender : quel antivirus choisir",
            "Norton oder Bitdefender: welches Antivirenprogramm wählen",
            "Norton o Bitdefender: qué antivirus elegir",
            "Norton ou Bitdefender: qual antivírus escolher",
            "Norton of Bitdefender: welke antivirus kiezen",
        ),
        "hero_lede": _d(
            "Norton 360 punta su una suite completa con VPN e backup cloud inclusi. Bitdefender Plus punta su un motore leggero e un filtro web anti-phishing efficace.",
            "Norton 360 focuses on a full suite with VPN and cloud backup included. Bitdefender Plus focuses on a lightweight engine and an effective anti-phishing web filter.",
            "Norton 360 mise sur une suite complète avec VPN et sauvegarde cloud inclus. Bitdefender Plus mise sur un moteur léger et un filtre web anti-phishing efficace.",
            "Norton 360 setzt auf eine umfassende Suite mit VPN und Cloud-Backup inklusive. Bitdefender Plus setzt auf eine schlanke Engine und einen wirksamen Anti-Phishing-Webfilter.",
            "Norton 360 apuesta por una suite completa con VPN y copia de seguridad en la nube incluidas. Bitdefender Plus apuesta por un motor ligero y un filtro web antiphishing eficaz.",
            "O Norton 360 aposta numa suite completa com VPN e cópia de segurança na nuvem incluídas. O Bitdefender Plus aposta num motor leve e num filtro web antiphishing eficaz.",
            "Norton 360 zet in op een volledige suite met VPN en cloudback-up inbegrepen. Bitdefender Plus zet in op een lichte engine en een doeltreffend anti-phishing-webfilter.",
        ),
        "verdict": [
            {
                "name": _d(*(["Norton 360 Standard"] * 7)),
                "blurb": _d(
                    "Protezione, VPN illimitata e 10 GB di backup cloud incluso in un solo abbonamento.",
                    "Protection, unlimited VPN and 10 GB of cloud backup included in a single subscription.",
                    "Protection, VPN illimité et 10 Go de sauvegarde cloud inclus dans un seul abonnement.",
                    "Schutz, unbegrenztes VPN und 10 GB Cloud-Backup in einem einzigen Abo enthalten.",
                    "Protección, VPN ilimitada y 10 GB de copia de seguridad en la nube incluidos en una sola suscripción.",
                    "Proteção, VPN ilimitada e 10 GB de cópia de segurança na nuvem incluídos numa única subscrição.",
                    "Bescherming, onbeperkte VPN en 10 GB cloudback-up inbegrepen in één abonnement.",
                ),
                "price": _d(
                    "€ 15,44 — 1 dispositivo / 1 anno", "€ 15,44 — 1 device / 1 year", "€ 15,44 — 1 appareil / 1 an",
                    "€ 15,44 — 1 Gerät / 1 Jahr", "€ 15,44 — 1 dispositivo / 1 año", "€ 15,44 — 1 dispositivo / 1 ano",
                    "€ 15,44 — 1 apparaat / 1 jaar",
                ),
                "cta": _d(
                    "Vedi la scheda", "See the listing", "Voir la fiche", "Zur Produktseite",
                    "Ver la ficha", "Ver a ficha", "Bekijk de productpagina",
                ),
                "href": "norton-360-standard",
            },
            {
                "name": _d(*(["Bitdefender Plus"] * 7)),
                "blurb": _d(
                    "Protezione real-time con motore Photon a basso impatto e filtro web anti-phishing.",
                    "Real-time protection with the low-impact Photon engine and an anti-phishing web filter.",
                    "Protection en temps réel avec le moteur Photon à faible impact et un filtre web anti-phishing.",
                    "Echtzeitschutz mit der ressourcenschonenden Photon-Engine und einem Anti-Phishing-Webfilter.",
                    "Protección en tiempo real con el motor Photon de bajo impacto y un filtro web antiphishing.",
                    "Proteção em tempo real com o motor Photon de baixo impacto e um filtro web antiphishing.",
                    "Realtime bescherming met de lichte Photon-engine en een anti-phishing-webfilter.",
                ),
                "price": _d(
                    "€ 20,59 — 1 dispositivo / 1 anno", "€ 20,59 — 1 device / 1 year", "€ 20,59 — 1 appareil / 1 an",
                    "€ 20,59 — 1 Gerät / 1 Jahr", "€ 20,59 — 1 dispositivo / 1 año", "€ 20,59 — 1 dispositivo / 1 ano",
                    "€ 20,59 — 1 apparaat / 1 jaar",
                ),
                "cta": _d(
                    "Vedi la scheda", "See the listing", "Voir la fiche", "Zur Produktseite",
                    "Ver la ficha", "Ver a ficha", "Bekijk de productpagina",
                ),
                "href": "bitdefender-plus-1-device",
            },
        ],
        "table_caption": _d(
            "Norton 360 Standard vs Bitdefender Plus, 1 dispositivo / 1 anno",
            "Norton 360 Standard vs Bitdefender Plus, 1 device / 1 year",
            "Norton 360 Standard vs Bitdefender Plus, 1 appareil / 1 an",
            "Norton 360 Standard vs. Bitdefender Plus, 1 Gerät / 1 Jahr",
            "Norton 360 Standard vs Bitdefender Plus, 1 dispositivo / 1 año",
            "Norton 360 Standard vs Bitdefender Plus, 1 dispositivo / 1 ano",
            "Norton 360 Standard vs Bitdefender Plus, 1 apparaat / 1 jaar",
        ),
        "table_headers": [
            _d("Caratteristica", "Feature", "Caractéristique", "Funktion", "Característica", "Característica", "Kenmerk"),
            _d(*(["Norton 360 Standard"] * 7)),
            _d(*(["Bitdefender Plus"] * 7)),
        ],
        "table_rows": [
            [
                _d("Prezzo", "Price", "Prix", "Preis", "Precio", "Preço", "Prijs"),
                _d(*(["€ 15,44"] * 7)),
                _d(*(["€ 20,59"] * 7)),
            ],
            [
                _d(
                    "Protezione virus/malware/ransomware", "Virus/malware/ransomware protection", "Protection virus/malware/ransomware",
                    "Schutz vor Viren/Malware/Ransomware", "Protección virus/malware/ransomware", "Proteção contra vírus/malware/ransomware",
                    "Bescherming tegen virussen/malware/ransomware",
                ),
                _d("Sì", "Yes", "Oui", "Ja", "Sí", "Sim", "Ja"),
                _d("Sì", "Yes", "Oui", "Ja", "Sí", "Sim", "Ja"),
            ],
            [
                _d("VPN inclusa", "VPN included", "VPN inclus", "VPN enthalten", "VPN incluida", "VPN incluída", "VPN inbegrepen"),
                _d(
                    "Sì, illimitata", "Yes, unlimited", "Oui, illimité", "Ja, unbegrenzt", "Sí, ilimitada", "Sim, ilimitada", "Ja, onbeperkt",
                ),
                _d(
                    "Non specificata in scheda", "Not stated on listing", "Non précisé sur la fiche",
                    "Auf der Produktseite nicht angegeben", "No especificada en la ficha", "Não especificada na ficha",
                    "Niet vermeld op productpagina",
                ),
            ],
            [
                _d(
                    "Backup cloud incluso", "Cloud backup included", "Sauvegarde cloud incluse", "Cloud-Backup enthalten",
                    "Copia de seguridad en la nube incluida", "Cópia de segurança na nuvem incluída", "Cloudback-up inbegrepen",
                ),
                _d(*(["10 GB"] * 7)),
                _d(
                    "Non incluso", "Not included", "Non incluse", "Nicht enthalten", "No incluida", "Não incluída",
                    "Niet inbegrepen",
                ),
            ],
            [
                _d(
                    "Filtro web anti-phishing", "Anti-phishing web filter", "Filtre web anti-phishing", "Anti-Phishing-Webfilter",
                    "Filtro web antiphishing", "Filtro web antiphishing", "Anti-phishing-webfilter",
                ),
                _d(
                    "Non specificato in scheda", "Not stated on listing", "Non précisé sur la fiche",
                    "Auf der Produktseite nicht angegeben", "No especificado en la ficha", "Não especificado na ficha",
                    "Niet vermeld op productpagina",
                ),
                _d("Sì", "Yes", "Oui", "Ja", "Sí", "Sim", "Ja"),
            ],
            [
                _d(
                    "Motore a basso impatto", "Low-impact engine", "Moteur à faible impact", "Ressourcenschonende Engine",
                    "Motor de bajo impacto", "Motor de baixo impacto", "Lichte engine",
                ),
                _d(
                    "Non specificato in scheda", "Not stated on listing", "Non précisé sur la fiche",
                    "Auf der Produktseite nicht angegeben", "No especificado en la ficha", "Não especificado na ficha",
                    "Niet vermeld op productpagina",
                ),
                _d(
                    "Sì (tecnologia Photon)", "Yes (Photon technology)", "Oui (technologie Photon)", "Ja (Photon-Technologie)",
                    "Sí (tecnología Photon)", "Sim (tecnologia Photon)", "Ja (Photon-technologie)",
                ),
            ],
            [
                _d(
                    "Variante senza rinnovo automatico", "No-auto-renewal variant", "Variante sans renouvellement automatique",
                    "Variante ohne automatische Verlängerung", "Variante sin renovación automática", "Variante sem renovação automática",
                    "Variant zonder automatische verlenging",
                ),
                _d(
                    "Sì, disponibile in catalogo", "Yes, available in the catalogue", "Oui, disponible dans le catalogue",
                    "Ja, im Katalog erhältlich", "Sí, disponible en el catálogo", "Sim, disponível no catálogo",
                    "Ja, beschikbaar in de catalogus",
                ),
                _d(
                    "Non disponibile", "Not available", "Non disponible", "Nicht verfügbar", "No disponible",
                    "Não disponível", "Niet beschikbaar",
                ),
            ],
            [
                _d("Attivazione", "Activation", "Activation", "Aktivierung", "Activación", "Ativação", "Activering"),
                _d(*(["My Norton"] * 7)),
                _d(*(["Bitdefender Central"] * 7)),
            ],
        ],
        "editorial_h2": _d(
            "A chi conviene l'uno o l'altro",
            "Who each one suits",
            "À qui l'un ou l'autre convient",
            "Wem das eine oder das andere passt",
            "A quién le conviene uno u otro",
            "A quem convém cada um",
            "Voor wie het ene of het andere geschikt is",
        ),
        "editorial_paragraphs": _d(
            [
                "Se vuoi tutto in un solo abbonamento — antivirus, VPN per le reti Wi-Fi pubbliche e un backup automatico dei file — Norton 360 Standard evita di dover acquistare questi strumenti separatamente.",
                "Se invece cerchi solo un antivirus reattivo che non appesantisca il PC e blocchi i siti di phishing durante la navigazione, Bitdefender Plus è più mirato e costa comunque meno di una VPN e un antivirus comprati a parte.",
                "Chi non vuole il rinnovo automatico dell'abbonamento trova in catalogo anche la variante Norton 360 Standard senza abbonamento, allo stesso livello di protezione.",
            ],
            [
                "If you want everything in a single subscription — antivirus, VPN for public Wi-Fi networks and automatic file backup — Norton 360 Standard saves you from buying these tools separately.",
                "If instead you're just after a responsive antivirus that doesn't weigh down your PC and blocks phishing sites while browsing, Bitdefender Plus is more targeted and still costs less than a VPN and antivirus bought separately.",
                "If you don't want the subscription to auto-renew, the catalogue also has the Norton 360 Standard variant without auto-renewal, at the same level of protection.",
            ],
            [
                "Si vous voulez tout dans un seul abonnement — antivirus, VPN pour les réseaux Wi-Fi publics et sauvegarde automatique des fichiers — Norton 360 Standard vous évite d'acheter ces outils séparément.",
                "Si vous cherchez plutôt un antivirus réactif qui n'alourdit pas le PC et bloque les sites de phishing pendant la navigation, Bitdefender Plus est plus ciblé et coûte de toute façon moins cher qu'un VPN et un antivirus achetés séparément.",
                "Ceux qui ne veulent pas du renouvellement automatique de l'abonnement trouveront aussi au catalogue la variante Norton 360 Standard sans abonnement, au même niveau de protection.",
            ],
            [
                "Wenn Sie alles in einem Abo wollen — Antivirus, VPN für öffentliche WLAN-Netze und automatisches Datei-Backup — erspart Ihnen Norton 360 Standard den separaten Kauf dieser Tools.",
                "Suchen Sie dagegen nur ein reaktionsschnelles Antivirenprogramm, das den PC nicht belastet und Phishing-Seiten beim Surfen blockiert, ist Bitdefender Plus gezielter und kostet trotzdem weniger als VPN und Antivirus separat gekauft.",
                "Wer die automatische Verlängerung des Abos nicht möchte, findet im Katalog auch die Variante Norton 360 Standard ohne Abo, mit demselben Schutzniveau.",
            ],
            [
                "Si quieres todo en una sola suscripción — antivirus, VPN para redes Wi-Fi públicas y copia de seguridad automática de archivos — Norton 360 Standard te evita comprar estas herramientas por separado.",
                "Si en cambio buscas solo un antivirus ágil que no sobrecargue el PC y bloquee los sitios de phishing durante la navegación, Bitdefender Plus está más enfocado y de todos modos cuesta menos que una VPN y un antivirus comprados por separado.",
                "Quien no quiera la renovación automática de la suscripción encontrará también en el catálogo la variante Norton 360 Standard sin suscripción, con el mismo nivel de protección.",
            ],
            [
                "Se quer tudo numa única subscrição — antivírus, VPN para redes Wi-Fi públicas e cópia de segurança automática de ficheiros — o Norton 360 Standard evita ter de comprar estas ferramentas em separado.",
                "Se, pelo contrário, procura apenas um antivírus ágil que não sobrecarregue o PC e bloqueie sites de phishing durante a navegação, o Bitdefender Plus é mais direcionado e mesmo assim custa menos do que uma VPN e um antivírus comprados em separado.",
                "Quem não quiser a renovação automática da subscrição encontra também no catálogo a variante Norton 360 Standard sem subscrição, com o mesmo nível de proteção.",
            ],
            [
                "Wil je alles in één abonnement — antivirus, VPN voor openbare wifi-netwerken en automatische bestandsback-up — dan bespaart Norton 360 Standard je de aparte aankoop van deze tools.",
                "Zoek je daarentegen alleen een responsieve antivirus die de pc niet vertraagt en phishingsites tijdens het surfen blokkeert, dan is Bitdefender Plus gerichter en toch nog goedkoper dan een los gekochte VPN en antivirus.",
                "Wie geen automatische verlenging van het abonnement wil, vindt in de catalogus ook de variant Norton 360 Standard zonder abonnement, met hetzelfde beschermingsniveau.",
            ],
        ),
        "faq_items": [
            {
                "q": _d(
                    "Norton 360 include una VPN?", "Does Norton 360 include a VPN?",
                    "Norton 360 inclut-il un VPN ?", "Enthält Norton 360 ein VPN?",
                    "¿Norton 360 incluye una VPN?", "O Norton 360 inclui uma VPN?",
                    "Bevat Norton 360 een VPN?",
                ),
                "a": _d(
                    "Sì, Secure VPN illimitata è inclusa nel prezzo base di Norton 360 Standard, secondo la scheda del prodotto.",
                    "Yes, unlimited Secure VPN is included in the base price of Norton 360 Standard, according to the product listing.",
                    "Oui, le VPN sécurisé illimité est inclus dans le prix de base de Norton 360 Standard, selon la fiche du produit.",
                    "Ja, das unbegrenzte Secure VPN ist laut Produktseite im Grundpreis von Norton 360 Standard enthalten.",
                    "Sí, la Secure VPN ilimitada está incluida en el precio base de Norton 360 Standard, según la ficha del producto.",
                    "Sim, a Secure VPN ilimitada está incluída no preço base do Norton 360 Standard, segundo a ficha do produto.",
                    "Ja, onbeperkte Secure VPN is inbegrepen in de basisprijs van Norton 360 Standard, volgens de productpagina.",
                ),
            },
            {
                "q": _d(
                    "Bitdefender Plus include il backup cloud?", "Does Bitdefender Plus include cloud backup?",
                    "Bitdefender Plus inclut-il la sauvegarde cloud ?", "Enthält Bitdefender Plus ein Cloud-Backup?",
                    "¿Bitdefender Plus incluye copia de seguridad en la nube?", "O Bitdefender Plus inclui cópia de segurança na nuvem?",
                    "Bevat Bitdefender Plus cloudback-up?",
                ),
                "a": _d(
                    "No, il backup cloud da 10 GB è una funzione di Norton 360; Bitdefender Plus si concentra su protezione anti-malware, motore leggero e filtro web.",
                    "No, the 10 GB cloud backup is a Norton 360 feature; Bitdefender Plus focuses on anti-malware protection, a lightweight engine and web filtering.",
                    "Non, la sauvegarde cloud de 10 Go est une fonction de Norton 360 ; Bitdefender Plus se concentre sur la protection anti-malware, un moteur léger et le filtrage web.",
                    "Nein, das 10-GB-Cloud-Backup ist eine Funktion von Norton 360; Bitdefender Plus konzentriert sich auf Anti-Malware-Schutz, eine schlanke Engine und Webfilterung.",
                    "No, la copia de seguridad en la nube de 10 GB es una función de Norton 360; Bitdefender Plus se centra en protección antimalware, un motor ligero y filtrado web.",
                    "Não, a cópia de segurança na nuvem de 10 GB é uma funcionalidade do Norton 360; o Bitdefender Plus foca-se em proteção antimalware, motor leve e filtragem web.",
                    "Nee, de cloudback-up van 10 GB is een functie van Norton 360; Bitdefender Plus richt zich op antimalwarebescherming, een lichte engine en webfiltering.",
                ),
            },
            {
                "q": _d(
                    "Norton 360 si può acquistare senza rinnovo automatico?", "Can I buy Norton 360 without auto-renewal?",
                    "Peut-on acheter Norton 360 sans renouvellement automatique ?", "Kann man Norton 360 ohne automatische Verlängerung kaufen?",
                    "¿Se puede comprar Norton 360 sin renovación automática?", "É possível comprar o Norton 360 sem renovação automática?",
                    "Kan ik Norton 360 kopen zonder automatische verlenging?",
                ),
                "a": _d(
                    "Sì, in catalogo è disponibile anche la variante Norton 360 Standard senza abbonamento, a un prezzo leggermente diverso dalla versione con rinnovo automatico.",
                    "Yes, the catalogue also has the Norton 360 Standard variant without a subscription, at a slightly different price from the auto-renewing version.",
                    "Oui, le catalogue propose aussi la variante Norton 360 Standard sans abonnement, à un prix légèrement différent de la version avec renouvellement automatique.",
                    "Ja, im Katalog gibt es auch die Variante Norton 360 Standard ohne Abo, zu einem leicht abweichenden Preis gegenüber der Version mit automatischer Verlängerung.",
                    "Sí, en el catálogo también está disponible la variante Norton 360 Standard sin suscripción, a un precio ligeramente distinto de la versión con renovación automática.",
                    "Sim, no catálogo também está disponível a variante Norton 360 Standard sem subscrição, a um preço ligeiramente diferente da versão com renovação automática.",
                    "Ja, de catalogus heeft ook de variant Norton 360 Standard zonder abonnement, tegen een iets andere prijs dan de versie met automatische verlenging.",
                ),
            },
            {
                "q": _d(
                    "Quale dei due rallenta meno il PC?", "Which of the two slows down the PC less?",
                    "Lequel des deux ralentit le moins le PC ?", "Welches der beiden bremst den PC weniger aus?",
                    "¿Cuál de los dos ralentiza menos el PC?", "Qual dos dois abranda menos o PC?",
                    "Welke van de twee vertraagt de pc minder?",
                ),
                "a": _d(
                    "Bitdefender usa la tecnologia Photon, pensata da Bitdefender per adattare l'uso delle risorse all'hardware del computer senza rallentamenti.",
                    "Bitdefender uses Photon technology, designed by Bitdefender to adapt resource usage to the computer's hardware without slowdowns.",
                    "Bitdefender utilise la technologie Photon, conçue par Bitdefender pour adapter l'usage des ressources au matériel de l'ordinateur sans ralentissement.",
                    "Bitdefender nutzt die Photon-Technologie, die laut Bitdefender die Ressourcennutzung an die Hardware des Computers anpasst, ohne den PC zu verlangsamen.",
                    "Bitdefender usa la tecnología Photon, diseñada por Bitdefender para adaptar el uso de los recursos al hardware del ordenador sin ralentizaciones.",
                    "O Bitdefender usa a tecnologia Photon, pensada pela Bitdefender para adaptar o uso dos recursos ao hardware do computador sem abrandamentos.",
                    "Bitdefender gebruikt Photon-technologie, door Bitdefender ontworpen om het gebruik van systeembronnen aan te passen aan de hardware van de computer zonder vertragingen.",
                ),
            },
        ],
        "disclaimer": _d(
            "Norton e Bitdefender sono marchi dei rispettivi produttori. Contenuto informativo Aml Store: funzionalità e condizioni seguono sempre il prodotto acquistato.",
            "Norton and Bitdefender are trademarks of their respective makers. Informational content by Aml Store: features and terms always follow the product purchased.",
            "Norton et Bitdefender sont des marques de leurs éditeurs respectifs. Contenu informatif Aml Store : fonctionnalités et conditions suivent toujours le produit acheté.",
            "Norton und Bitdefender sind Marken ihrer jeweiligen Hersteller. Informativer Inhalt von Aml Store: Funktionen und Bedingungen richten sich stets nach dem gekauften Produkt.",
            "Norton y Bitdefender son marcas de sus respectivos fabricantes. Contenido informativo de Aml Store: funciones y condiciones siguen siempre el producto adquirido.",
            "Norton e Bitdefender são marcas dos respetivos fabricantes. Conteúdo informativo da Aml Store: funcionalidades e condições seguem sempre o produto adquirido.",
            "Norton en Bitdefender zijn merken van hun respectieve fabrikanten. Informatieve inhoud van Aml Store: functies en voorwaarden volgen altijd het aangeschafte product.",
        ),
    },
]


if __name__ == "__main__":
    count = 0
    for page in PAGES:
        for lang in LANGS:
            out_dir = ROOT / lang
            out_dir.mkdir(exist_ok=True)
            path = out_dir / f"{page['slug']}.html"
            path.write_text(render(page, lang), encoding="utf-8", newline="\n")
            count += 1
    print(f"pagine scritte: {count} ({len(PAGES)} confronti x {len(LANGS)} lingue)")
