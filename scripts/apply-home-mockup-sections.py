#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aggiorna le sezioni Garanzia e Sicurezza e Recensioni della home in base al mockup di riferimento.

Sezione Garanzia e Sicurezza:
  - Layout a 2 colonne su desktop: intro/Trustpilot a sinistra, 6 card a destra.
  - Badge scudo centrato al bordo inferiore.

Sezione Recensioni ("Cosa dicono i clienti"):
  - Layout a 2 colonne su desktop:
      - Sinistra: Trustpilot rating (stelle verdi + punteggio), Titolo ("Cosa dicono i clienti"), Link "Leggi tutte le recensioni ->"
      - Destra: 3 Card bianche con nome, virgola/virgoletta watermark, 5 stelle oro/ambra e citazione tra caporali.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es")

ICONS = {
    "headset": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 18v-6a9 9 0 0118 0v6"/><path d="M21 19a2 2 0 01-2 2h-1a2 2 0 01-2-2v-3a2 2 0 012-2h3zM3 19a2 2 0 002 2h1a2 2 0 002-2v-3a2 2 0 00-2-2H3z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 13V6a2 2 0 00-2-2H4a2 2 0 00-2 2v12a2 2 0 002 2h9"/><path d="M22 6l-10 7L2 6"/><path d="M17 19h5"/><path d="M19 16l3 3-3 3"/></svg>',
    "lock": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>',
    "flag": '<svg viewBox="0 0 32 32" width="26" height="26" aria-hidden="true"><g clip-path="url(#italy-flag-clip)"><circle cx="16" cy="16" r="16" fill="#ffffff"/><path d="M0 0h10.67v32H0z" fill="#009246"/><path d="M21.33 0H32v32H21.33z" fill="#ce2b37"/></g><defs><clipPath id="italy-flag-clip"><circle cx="16" cy="16" r="16"/></clipPath></defs></svg>',
    "doc": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>',
    "return": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21.5 2v6h-5M21.34 15.57a10 10 0 11-.57-8.38l5.67-5.67"/></svg>',
}

GUARANTEE_COPY = {
    "it": {
        "eyebrow": "Garanzia e sicurezza",
        "title": "Acquista in sicurezza, dall'ordine all'attivazione",
        "lede": "Licenze digitali, pagamenti protetti e assistenza italiana prima e dopo l'acquisto.",
        "tp_score": "4,8/5 su Trustpilot",
        "tp_count": "94 recensioni",
        "mini_items": [
            ("flag", "Azienda italiana", "Sede e P.IVA in Italia"),
            ("lock", "Pagamenti sicuri", "Stripe e PayPal"),
        ],
        "about_text": "Scopri chi siamo",
        "about_href": "/it/chi-siamo",
        "cards": [
            ("headset", "Assistenza in italiano", "Supporto post-vendita via email e WhatsApp."),
            ("mail", "Consegna in 2-15 minuti", "La licenza arriva via email subito dopo il pagamento."),
            ("lock", "Pagamenti protetti", "Transazioni sicure con Stripe e PayPal."),
            ("flag", "Azienda italiana", "Sede e P.IVA in Italia. Massima trasparenza."),
            ("doc", "Fattura elettronica", "Fattura disponibile per privati e aziende."),
            ("return", "14 giorni di recesso", "Diritto di recesso per i consumatori UE."),
        ],
    },
    "en": {
        "eyebrow": "Guarantee and security",
        "title": "Buy with confidence, from order to activation",
        "lede": "Digital licences, protected payments and Italian support before and after purchase.",
        "tp_score": "4.8/5 on Trustpilot",
        "tp_count": "94 reviews",
        "mini_items": [
            ("flag", "Italian company", "Office & VAT in Italy"),
            ("lock", "Secure payments", "Stripe and PayPal"),
        ],
        "about_text": "About us",
        "about_href": "/en/about-us",
        "cards": [
            ("headset", "Support in Italian", "After-sales support via email and WhatsApp."),
            ("mail", "Delivery in 2-15 minutes", "Licence delivered via email right after payment."),
            ("lock", "Protected payments", "Secure transactions with Stripe and PayPal."),
            ("flag", "Italian company", "Office & VAT number in Italy. Full transparency."),
            ("doc", "Electronic invoice", "Invoice available for individuals and businesses."),
            ("return", "14-day right of withdrawal", "Right of withdrawal for EU consumers."),
        ],
    },
    "fr": {
        "eyebrow": "Garantie et sécurité",
        "title": "Achetez en toute sécurité, de la commande à l'activation",
        "lede": "Licences numériques, paiements protégés et assistance en italien avant et après l'achat.",
        "tp_score": "4,8/5 sur Trustpilot",
        "tp_count": "94 avis",
        "mini_items": [
            ("flag", "Entreprise italienne", "Siège et TVA en Italie"),
            ("lock", "Paiements sécurisés", "Stripe et PayPal"),
        ],
        "about_text": "Qui sommes-nous",
        "about_href": "/fr/qui-sommes-nous",
        "cards": [
            ("headset", "Assistance en italien", "Support après-vente par e-mail et WhatsApp."),
            ("mail", "Livraison en 2-15 minutes", "La licence arrive par e-mail immédiatement après le paiement."),
            ("lock", "Paiements protégés", "Transactions sécurisées avec Stripe et PayPal."),
            ("flag", "Entreprise italienne", "Siège et numéro de TVA en Italie. Transparence maximale."),
            ("doc", "Facture électronique", "Facture disponible pour particuliers et entreprises."),
            ("return", "14 jours de rétractation", "Droit de rétractation pour les consommateurs UE."),
        ],
    },
    "de": {
        "eyebrow": "Garantie und Sicherheit",
        "title": "Sicher kaufen, von der Bestellung bis zur Aktivierung",
        "lede": "Digitale Lizenzen, geschützte Zahlungen und italienischer Support vor und nach dem Kauf.",
        "tp_score": "4,8/5 auf Trustpilot",
        "tp_count": "94 Bewertungen",
        "mini_items": [
            ("flag", "Italienisches Unternehmen", "Sitz & USt-IdNr. in Italien"),
            ("lock", "Sichere Zahlungen", "Stripe und PayPal"),
        ],
        "about_text": "Über uns",
        "about_href": "/de/ueber-uns",
        "cards": [
            ("headset", "Support auf Italienisch", "Kundendienst per E-Mail und WhatsApp."),
            ("mail", "Lieferung in 2-15 Minuten", "Die Lizenz kommt direkt nach der Zahlung per E-Mail."),
            ("lock", "Geschützte Zahlungen", "Sichere Transaktionen mit Stripe und PayPal."),
            ("flag", "Italienisches Unternehmen", "Sitz und USt-IdNr. in Italien. Volle Transparenz."),
            ("doc", "Elektronische Rechnung", "Rechnung für Privatpersonen und Unternehmen verfügbar."),
            ("return", "14 Tage Rückgaberecht", "Widerrufsrecht für EU-Verbraucher."),
        ],
    },
    "es": {
        "eyebrow": "Garantía y seguridad",
        "title": "Compra con seguridad, desde el pedido hasta la activación",
        "lede": "Licencias digitales, pagos protegidos y asistencia en italiano antes y después de la compra.",
        "tp_score": "4,8/5 en Trustpilot",
        "tp_count": "94 opiniones",
        "mini_items": [
            ("flag", "Empresa italiana", "Sede y NIF en Italia"),
            ("lock", "Pagos seguros", "Stripe y PayPal"),
        ],
        "about_text": "Quiénes somos",
        "about_href": "/es/quienes-somos",
        "cards": [
            ("headset", "Asistencia en italiano", "Soporte posventa por correo electrónico y WhatsApp."),
            ("mail", "Entrega en 2-15 minutos", "La licencia llega por correo inmediatamente tras el pago."),
            ("lock", "Pagos protegidos", "Transacciones seguras con Stripe y PayPal."),
            ("flag", "Empresa italiana", "Sede y NIF en Italia. Máxima transparencia."),
            ("doc", "Factura electrónica", "Factura disponible para particulares y empresas."),
            ("return", "14 días de desistimiento", "Derecho de desistimiento para consumidores UE."),
        ],
    },
}

REVIEWS_COPY = {
    "it": {
        "tp_count": "4,8/5 su 94 recensioni",
        "title": "Cosa dicono i clienti",
        "cta": "Leggi tutte le recensioni",
        "tp_url": "https://it.trustpilot.com/review/aml-store.com",
        "reviews": [
            ("Roberto Galoppini", "Ho appena acquistato una copia di Microsoft 365, il codice è arrivato 2 minuti dopo il pagamento, ho potuto rinnovare il mio account per 1 anno, azienda superlativa!!"),
            ("Laura Ceccacci", "Il prodotto è arrivato in tempo reale, il supporto da parte del fornitore è eccezionale, davvero un serio distributore da tenere in considerazione per il futuro."),
            ("Mario", "Miglior prezzo del web per il prodotto originale, assistenza tempestiva e competente, fornitura via email immediata e nessun problema di attivazione."),
        ]
    },
    "en": {
        "tp_count": "4.8/5 from 94 reviews",
        "title": "What our customers say",
        "cta": "Read all reviews",
        "tp_url": "https://www.trustpilot.com/review/aml-store.com",
        "reviews": [
            ("Roberto Galoppini", "I just bought a copy of Microsoft 365, the code arrived 2 minutes after payment, I was able to renew my account for 1 year, superb company!!"),
            ("Laura Ceccacci", "The product arrived in real time, support from the supplier is exceptional, truly a reliable dealer to keep in mind for the future."),
            ("Mario", "Best price on the web for the genuine product, prompt and knowledgeable support, immediate delivery by email and no activation issues."),
        ]
    },
    "fr": {
        "tp_count": "4,8/5 sur 94 avis",
        "title": "Ce que disent nos clients",
        "cta": "Lire tous les avis",
        "tp_url": "https://fr.trustpilot.com/review/aml-store.com",
        "reviews": [
            ("Roberto Galoppini", "Je viens d'acheter une copie de Microsoft 365, le code est arrivé 2 minutes après le paiement, j'ai pu renouveler mon compte pour 1 an, entreprise excellente !!"),
            ("Laura Ceccacci", "Le produit est arrivé en temps réel, le support du fournisseur est exceptionnel, vraiment un distributeur sérieux à garder en tête pour l'avenir."),
            ("Mario", "Meilleur prix du web pour le produit original, assistance rapide et compétente, livraison immédiate par e-mail et aucun problème d'activation."),
        ]
    },
    "de": {
        "tp_count": "4,8/5 bei 94 Bewertungen",
        "title": "Was unsere Kunden sagen",
        "cta": "Alle Bewertungen lesen",
        "tp_url": "https://de.trustpilot.com/review/aml-store.com",
        "reviews": [
            ("Roberto Galoppini", "Ich habe gerade eine Kopie von Microsoft 365 gekauft, der Code kam 2 Minuten nach der Zahlung an, ich konnte mein Konto für 1 Jahr verlängern, hervorragendes Unternehmen!!"),
            ("Laura Ceccacci", "Das Produkt kam in Echtzeit an, der Support des Anbieters ist außergewöhnlich, wirklich ein seriöser Händler, den man sich für die Zukunft merken sollte."),
            ("Mario", "Bester Preis im Web für das Originalprodukt, schneller und kompetenter Support, sofortige Lieferung per E-Mail und keine Probleme bei der Aktivierung."),
        ]
    },
    "es": {
        "tp_count": "4,8/5 sobre 94 opiniones",
        "title": "Lo que dicen nuestros clientes",
        "cta": "Leer todas las opiniones",
        "tp_url": "https://es.trustpilot.com/review/aml-store.com",
        "reviews": [
            ("Roberto Galoppini", "Acabo de comprar una copia de Microsoft 365, el código llegó 2 minutos después del pago, pude renovar mi cuenta por 1 año, ¡empresa excelente!!"),
            ("Laura Ceccacci", "El producto llegó en tiempo real, el soporte por parte del proveedor es excepcional, un distribuidor realmente serio a tener en cuenta para el futuro."),
            ("Mario", "Mejor precio de la web para el producto original, asistencia rápida y competente, entrega inmediata por email y sin problemas de activación."),
        ]
    }
}


def guarantee_section(lang: str) -> str:
    c = GUARANTEE_COPY[lang]

    cards_html = []
    for icon_key, title, body in c["cards"]:
        cards_html.append(f"""                <li class="home-guarantee__card">
                    <div class="home-guarantee__card-icon" aria-hidden="true">{ICONS[icon_key]}</div>
                    <h3 class="home-guarantee__card-title">{title}</h3>
                    <p class="home-guarantee__card-body">{body}</p>
                </li>""")
    cards_str = "\n".join(cards_html)

    mini_items_html = []
    for icon_key, title, sub in c["mini_items"]:
        mini_items_html.append(f"""                    <div class="home-guarantee__mini-item">
                        <span class="home-guarantee__mini-icon" aria-hidden="true">{ICONS[icon_key]}</span>
                        <div>
                            <strong>{title}</strong>
                            <small>{sub}</small>
                        </div>
                    </div>""")
    mini_str = "\n".join(mini_items_html)

    return f"""        <section class="home-guarantee" aria-labelledby="home-guarantee-title">
            <svg class="home-guarantee__watermark" viewBox="0 0 300 300" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.2">
                <path d="M150 20 L250 60 V150 C250 220 150 270 150 270 C150 270 50 220 50 150 V60 Z" opacity="0.08"/>
                <path d="M110 145 L135 170 L190 115" opacity="0.08" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="60" cy="220" r="25" opacity="0.06"/>
                <path d="M50 215 L57 225 L72 210" opacity="0.06"/>
                <rect x="220" y="30" width="30" height="35" rx="4" opacity="0.06"/>
            </svg>
            <div class="home-guarantee__inner">
                <div class="home-guarantee__intro">
                    <p class="home-section-eyebrow">{c['eyebrow']}</p>
                    <h2 id="home-guarantee-title" class="home-section-title">{c['title']}</h2>
                    <p class="home-guarantee__lede">{c['lede']}</p>
                    <hr class="home-guarantee__divider" />
                    <div class="home-guarantee__tp">
                        <div class="home-guarantee__tp-stars" aria-hidden="true">
                            <svg viewBox="0 0 120 24" width="100" height="20">
                                <g fill="#00b67a">
                                    <rect x="0" y="2" width="20" height="20" rx="2"/>
                                    <rect x="24" y="2" width="20" height="20" rx="2"/>
                                    <rect x="48" y="2" width="20" height="20" rx="2"/>
                                    <rect x="72" y="2" width="20" height="20" rx="2"/>
                                    <rect x="96" y="2" width="20" height="20" rx="2"/>
                                </g>
                                <g fill="#ffffff">
                                    <path d="M10 5.5l1.54 3.12 3.44.5-2.49 2.43.59 3.43L10 13.36l-3.08 1.62.59-3.43-2.49-2.43 3.44-.5z"/>
                                    <path d="M34 5.5l1.54 3.12 3.44.5-2.49 2.43.59 3.43L34 13.36l-3.08 1.62.59-3.43-2.49-2.43 3.44-.5z"/>
                                    <path d="M58 5.5l1.54 3.12 3.44.5-2.49 2.43.59 3.43L58 13.36l-3.08 1.62.59-3.43-2.49-2.43 3.44-.5z"/>
                                    <path d="M82 5.5l1.54 3.12 3.44.5-2.49 2.43.59 3.43L82 13.36l-3.08 1.62.59-3.43-2.49-2.43 3.44-.5z"/>
                                    <path d="M106 5.5l1.54 3.12 3.44.5-2.49 2.43.59 3.43L106 13.36l-3.08 1.62.59-3.43-2.49-2.43 3.44-.5z"/>
                                </g>
                            </svg>
                        </div>
                        <span class="home-guarantee__tp-score">{c['tp_score']}</span>
                        <span class="home-guarantee__tp-count">{c['tp_count']}</span>
                    </div>
                    <div class="home-guarantee__mini-trust">
{mini_str}
                    </div>
                    <a href="{c['about_href']}" class="home-guarantee__about-link">{c['about_text']} <span aria-hidden="true">&rarr;</span></a>
                </div>
                <ul class="home-guarantee__grid">
{cards_str}
                </ul>
            </div>
        </section>"""


def reviews_section(lang: str) -> str:
    c = REVIEWS_COPY[lang]
    cards = []
    for name, quote in c["reviews"]:
        cards.append(f"""                    <li class="home-reviews__card">
                        <div class="home-reviews__card-head">
                            <span class="home-reviews__name">{name}</span>
                            <span class="home-reviews__quote-icon" aria-hidden="true">“</span>
                        </div>
                        <span class="home-reviews__stars-amber" aria-hidden="true">★★★★★</span>
                        <p>«{quote}»</p>
                    </li>""")
    cards_str = "\n".join(cards)

    return f"""        <section class="home-reviews" aria-labelledby="home-reviews-title">
            <div class="home-reviews__inner">
                <div class="home-reviews__intro">
                    <h2 id="home-reviews-title" class="home-section-title">{c['title']}</h2>
                    <a class="home-reviews__cta" href="{c['tp_url']}" target="_blank" rel="noopener noreferrer">{c['cta']} <span aria-hidden="true">&rarr;</span></a>
                </div>
                <ul class="home-reviews__grid">
{cards_str}
                </ul>
            </div>
        </section>"""


def main() -> None:
    SEC_GUARANTEE_RE = re.compile(r'[ \t]*<section class="home-guarantee".*?</section>', re.S)
    SEC_REVIEWS_RE = re.compile(r'[ \t]*<section class="home-reviews".*?</section>', re.S)
    SEC_RECOMMENDED_RE = re.compile(r'\n?[ \t]*<section (?:id="prodotti-consigliati"|class="home-recommended").*?</section>', re.S)
    SEC_CATEGORIES_RE = re.compile(r'\n?[ \t]*<section (?:id="soluzioni"|class="home-categories").*?</section>', re.S)
    SEC_BUSINESS_RE = re.compile(r'\n?[ \t]*<section [^>]*class="home-business".*?</section>', re.S)

    for lang in LANGS:
        path = ROOT / lang / "index.html"
        html = path.read_text(encoding="utf-8")

        # Update Guarantee section
        m_guar = SEC_GUARANTEE_RE.search(html)
        if m_guar:
            html = html[:m_guar.start()] + guarantee_section(lang) + html[m_guar.end():]

        # Update Reviews section
        m_rev = SEC_REVIEWS_RE.search(html)
        if m_rev:
            html = html[:m_rev.start()] + reviews_section(lang) + html[m_rev.end():]

        # Remove Recommended products section if present
        m_rec = SEC_RECOMMENDED_RE.search(html)
        if m_rec:
            html = html[:m_rec.start()] + html[m_rec.end():]

        # Remove Categories and Business sections if present
        html = SEC_CATEGORIES_RE.sub('', html)
        html = SEC_BUSINESS_RE.sub('', html)

        path.write_text(html, encoding="utf-8", newline="")
        print(f"{lang}: sezioni Garanzia e Recensioni aggiornate; Altre soluzioni, Per aziende e Prodotti consigliati rimossi.")


if __name__ == "__main__":
    main()
