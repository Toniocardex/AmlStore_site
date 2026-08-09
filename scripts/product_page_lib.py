#!/usr/bin/env python3
"""Shared helpers for generating static product and catalog pages."""
import html as html_module
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
LANGS = ("it", "en", "fr", "de", "es")
LOCALE = {"it": "it_IT", "en": "en_US", "fr": "fr_FR", "de": "de_DE", "es": "es_ES"}

# Neutro brand (non usare cover di un altro SKU come placeholder).
PRODUCT_COVER_FALLBACK = "product-cover-fallback.webp"
PRODUCT_COVER_FALLBACK_SRC = f"../asset/media/{PRODUCT_COVER_FALLBACK}"
PRODUCT_COVER_FALLBACK_ABS = f"https://aml-store.com/asset/media/{PRODUCT_COVER_FALLBACK}"

# Allineato a functions/api/_lib/catalog.js (physical: true)
PHYSICAL_SKUS = frozenset({
    "FQC-10538",
    "P73-08328",
    "P73-08538",
    "P73-07788",
    "W11_PRO_STICKER",
    "P6L-00076",
    "SC835510",
})

STOCK_I18N = {
    "it": {
        "available": "Disponibilità: {n}",
        "low": "Ultime {n} unità",
        "out": "Non disponibile",
        "error": "Disponibilità da verificare",
    },
    "en": {
        "available": "Availability: {n}",
        "low": "Last {n} units",
        "out": "Out of stock",
        "error": "Availability to be confirmed",
    },
    "fr": {
        "available": "Disponibilité : {n}",
        "low": "Dernières {n} unités",
        "out": "Indisponible",
        "error": "Disponibilité à vérifier",
    },
    "de": {
        "available": "Verfügbarkeit: {n}",
        "low": "Letzte {n} Einheiten",
        "out": "Nicht verfügbar",
        "error": "Verfügbarkeit prüfen",
    },
    "es": {
        "available": "Disponibilidad: {n}",
        "low": "Últimas {n} unidades",
        "out": "No disponible",
        "error": "Disponibilidad por confirmar",
    },
}


def is_physical_sku(sku):
    return str(sku or "").strip() in PHYSICAL_SKUS


def _stock_block_html(lang, sku):
    """Placeholder stock row + data-i18n for product-stock.js (physical only)."""
    if not is_physical_sku(sku):
        return ""
    t = STOCK_I18N[lang]
    return f"""                <p class="v2-stock" data-stock-status="loading" aria-live="polite"
                    data-stock-available="{t['available']}"
                    data-stock-low="{t['low']}"
                    data-stock-out="{t['out']}"
                    data-stock-error="{t['error']}">
                    <span class="v2-stock__dot" aria-hidden="true"></span>
                    <span class="v2-stock__text"></span>
                </p>
"""


def _physical_attr(sku):
    return '\n            data-physical="true"' if is_physical_sku(sku) else ""


def _stock_script_tag(sku):
    if not is_physical_sku(sku):
        return ""
    return '    <script src="../js/product-stock.js" defer></script>\n'


TRUSTPILOT_LOCALE = {
    "it": ("it-IT", "https://it.trustpilot.com/review/aml-store.com"),
    "en": ("en-US", "https://www.trustpilot.com/review/aml-store.com"),
    "fr": ("fr-FR", "https://fr.trustpilot.com/review/aml-store.com"),
    "de": ("de-DE", "https://de.trustpilot.com/review/aml-store.com"),
    "es": ("es-ES", "https://es.trustpilot.com/review/aml-store.com"),
}

TRUSTPILOT_I18N = {
    "it": {
        "title": "Recensioni dei clienti",
        "fallback": "Esperienze reali dei clienti su Trustpilot.",
    },
    "en": {
        "title": "Customer reviews",
        "fallback": "Real customer experiences on Trustpilot.",
    },
    "fr": {
        "title": "Avis clients",
        "fallback": "Expériences réelles des clients sur Trustpilot.",
    },
    "de": {
        "title": "Kundenbewertungen",
        "fallback": "Echte Kundenerfahrungen auf Trustpilot.",
    },
    "es": {
        "title": "Opiniones de clientes",
        "fallback": "Experiencias reales de clientes en Trustpilot.",
    },
}

TRUSTPILOT_FALLBACK_LEAD = {
    "it": "Esperienze reali condivise dai clienti su",
    "en": "Real experiences shared by customers on",
    "fr": "Expériences réelles partagées sur",
    "de": "Echte Erfahrungen von Kunden auf",
    "es": "Experiencias reales compartidas en",
}

TRUSTPILOT_BUSINESS_UNIT = "61c44c912f493a1a7cd810fa"
TRUSTPILOT_TEMPLATE_ID = "5419b6a8b0d04a076446a9ad"
TRUSTPILOT_TOKEN = "27270fde-f5a0-4937-9101-76b7ebae8a1a"


def _trustpilot_buy_mini(lang):
    """Micro TrustBox nella buy card (sotto CTA)."""
    tp_locale, tp_url = TRUSTPILOT_LOCALE[lang]
    fallback_lead = TRUSTPILOT_FALLBACK_LEAD[lang]
    return f"""                <div class="product-trustpilot pdp-buy-trustpilot">
                    <p class="product-trustpilot__fallback trustpilot-fallback">{fallback_lead} <a href="{tp_url}" target="_blank" rel="noopener noreferrer">Trustpilot</a>.</p>
                    <div
                        id="trustpilot-widget"
                        class="trustpilot-widget"
                        data-locale="{tp_locale}"
                        data-template-id="{TRUSTPILOT_TEMPLATE_ID}"
                        data-businessunit-id="{TRUSTPILOT_BUSINESS_UNIT}"
                        data-style-height="40px"
                        data-style-width="100%"
                        data-token="{TRUSTPILOT_TOKEN}"
                        data-min-review-count="0"
                        data-style-alignment="center"
                    >
                        <a href="{tp_url}" target="_blank" rel="noopener noreferrer">Trustpilot</a>
                    </div>
                </div>
"""


def _trustpilot_block(lang):
    """Deprecated layout: prefer _trustpilot_buy_mini nella buy card."""
    return _trustpilot_buy_mini(lang)


def _trustpilot_inner(lang):
    """Compat: stesso markup del mini in buy card (senza wrapper extra di sezione)."""
    return _trustpilot_buy_mini(lang).rstrip() + "\n"


def _trustpilot_script_tag():
    return '    <script src="../js/trustpilot-widget.js" defer></script>\n'


# Override copy per SKU fisici (tax/passi) — non tocca licenze digitali
PHYSICAL_LABELS = {
    "it": {
        "tax": "Tasse incluse. Articolo fisico con spedizione gratuita (non consegna solo digitale). Affidamento al corriere entro 24 ore lavorative dopo il pagamento.",
        "steps_title": "Ordine, spedizione e attivazione",
        "step_email": "Spedizione del supporto",
        "step_email_desc": "Affidamento al corriere entro 24 ore lavorative; conferma ordine via email",
        "desc_suffix": "Articolo fisico con spedizione gratuita: affidamento al corriere entro 24 ore lavorative. Conferma d'ordine via email.",
    },
    "en": {
        "tax": "Tax included. Physical product with free shipping (not digital-only delivery). Handed to the courier within 24 business hours after payment.",
        "steps_title": "Order, shipping and activation",
        "step_email": "Media shipping",
        "step_email_desc": "Handed to the courier within 24 business hours; order confirmation by email",
        "desc_suffix": "Physical product with free shipping: handed to the courier within 24 business hours. Order confirmation by email.",
    },
    "fr": {
        "tax": "Taxes incluses. Article physique avec livraison gratuite (pas une livraison uniquement numérique). Remise au transporteur sous 24 heures ouvrées après paiement.",
        "steps_title": "Commande, expédition et activation",
        "step_email": "Expédition du support",
        "step_email_desc": "Remise au transporteur sous 24 heures ouvrées ; confirmation de commande par e-mail",
        "desc_suffix": "Article physique avec livraison gratuite : remise au transporteur sous 24 heures ouvrées. Confirmation de commande par e-mail.",
    },
    "de": {
        "tax": "Steuern inklusive. Physischer Artikel mit kostenlosem Versand (keine rein digitale Lieferung). Übergabe an den Versanddienst innerhalb von 24 Werktagsstunden nach Zahlung.",
        "steps_title": "Bestellung, Versand und Aktivierung",
        "step_email": "Versand des Mediums",
        "step_email_desc": "Übergabe an den Versanddienst innerhalb von 24 Werktagsstunden; Bestellbestätigung per E-Mail",
        "desc_suffix": "Physischer Artikel mit kostenlosem Versand: Übergabe an den Versanddienst innerhalb von 24 Werktagsstunden. Bestellbestätigung per E-Mail.",
    },
    "es": {
        "tax": "Impuestos incluidos. Artículo físico con envío gratuito (no es entrega solo digital). Entrega al transportista en 24 horas laborables tras el pago.",
        "steps_title": "Pedido, envío y activación",
        "step_email": "Envío del soporte",
        "step_email_desc": "Entrega al transportista en 24 horas laborables; confirmación del pedido por email",
        "desc_suffix": "Artículo físico con envío gratuito: entrega al transportista en 24 horas laborables. Confirmación del pedido por email.",
    },
}

PHYSICAL_UI = {
    "it": {
        "step2_title": "Spedizione del supporto",
        "step2_body": "Spediamo il <strong>supporto fisico</strong> con <strong>spedizione gratuita</strong>: affidamento al corriere entro <strong>24 ore lavorative</strong> dopo il pagamento — non è una consegna solo digitale. Ricevi anche la <strong>conferma d'ordine</strong> via email (con tracking quando disponibile).",
        "step3_title": "Attivazione",
        "step3_body": "Attiva Windows con la licenza/codice associati all'ordine: Impostazioni → Sistema → Attivazione (o la procedura indicata). Usa i canali ufficiali Microsoft.",
    },
    "en": {
        "step2_title": "Media shipping",
        "step2_body": "We ship the <strong>physical media</strong> with <strong>free shipping</strong>: handed to the courier within <strong>24 business hours</strong> after payment — not digital-only delivery. You also receive an <strong>order confirmation</strong> by email (with tracking when available).",
        "step3_title": "Activation",
        "step3_body": "Activate Windows with the licence/key for your order: Settings → System → Activation (or the stated procedure). Use official Microsoft channels.",
    },
    "fr": {
        "step2_title": "Expédition du support",
        "step2_body": "Nous expédions le <strong>support physique</strong> en <strong>livraison gratuite</strong> : remise au transporteur sous <strong>24 heures ouvrées</strong> après paiement — ce n'est pas une livraison uniquement numérique. Vous recevez aussi une <strong>confirmation de commande</strong> par e-mail (avec suivi si disponible).",
        "step3_title": "Activation",
        "step3_body": "Activez Windows avec la licence/clé liée à la commande : Paramètres → Système → Activation (ou la procédure indiquée). Utilisez les canaux Microsoft officiels.",
    },
    "de": {
        "step2_title": "Versand des Mediums",
        "step2_body": "Wir versenden das <strong>physische Medium</strong> mit <strong>kostenlosem Versand</strong>: Übergabe an den Versanddienst innerhalb von <strong>24 Werktagsstunden</strong> nach Zahlung — keine rein digitale Lieferung. Sie erhalten außerdem eine <strong>Bestellbestätigung</strong> per E-Mail (mit Tracking, falls verfügbar).",
        "step3_title": "Aktivierung",
        "step3_body": "Aktivieren Sie Windows mit der Lizenz/dem Key der Bestellung: Einstellungen → System → Aktivierung (oder die angegebene Prozedur). Offizielle Microsoft-Kanäle nutzen.",
    },
    "es": {
        "step2_title": "Envío del soporte",
        "step2_body": "Enviamos el <strong>soporte físico</strong> con <strong>envío gratuito</strong>: entrega al transportista en <strong>24 horas laborables</strong> tras el pago — no es una entrega solo digital. También recibes la <strong>confirmación del pedido</strong> por email (con tracking cuando esté disponible).",
        "step3_title": "Activación",
        "step3_body": "Activa Windows con la licencia/clave del pedido: Configuración → Sistema → Activación (o el procedimiento indicado). Usa canales oficiales Microsoft.",
    },
}


# ── Layout v3 (scheda prodotto standard) ────────────────────────────────────
# Stringhe condivise da tutte le categorie: stanno qui e non nei moduli
# product_content_*, così una sola definizione serve office, windows e antivirus.
# Tono: diretto, seconda persona, orientato alla conversione.
V3_UI = {
    "it": {
        "delivery_line": "Codice via email in 5–15 minuti dalla conferma del pagamento",
        "assur_1": "Attivazione sui portali ufficiali",
        "assur_2": "Consegna digitale, nessuna spedizione",
        "assur_3": "Assistenza in italiano dopo l'acquisto",
        "assur_4": "Pagamenti gestiti da Stripe e PayPal",
        "assur_5": "Fattura elettronica disponibile",
        "receive_eyebrow": "Cosa ricevi",
        "apps_more": "Vedi tutte le app incluse",
        "reviews_title": "Cosa dicono i clienti",
        "reviews_lead": "Le recensioni sono pubblicate e verificate da Trustpilot: le leggi direttamente sulla piattaforma, senza filtri da parte nostra.",
        "reviews_cta": "Leggi tutte le recensioni",
        "specs_title": "Compatibilità e requisiti tecnici",
        "faq_title": "Le risposte prima dell'acquisto",
        "final_title": "Tutto pronto per iniziare",
        "final_tax": "IVA inclusa",
        "final_instead": "anziché",
        "sticky_buy": "Acquista ora",
        "pay_note": "Pagamenti protetti tramite <strong>Stripe</strong> e <strong>PayPal</strong>",
        "trust_1_t": "Azienda italiana", "trust_1_d": "Sede e P.IVA in Italia",
        "trust_2_t": "Fattura elettronica", "trust_2_d": "Disponibile per privati e aziende",
        "trust_3_t": "Assistenza in italiano", "trust_3_d": "Supporto post-vendita via email",
        "trust_4_t": "Pagamenti protetti", "trust_4_d": "Elaborati tramite Stripe e PayPal",
        "inst_title": "Acquista con maggiore tranquillità",
        "inst_1_t": "Rivenditore europeo", "inst_1_d": "AML Store ha sede legale in Italia",
        "inst_2_t": "Fattura disponibile", "inst_2_d": "Documentazione per privati e aziende",
        "inst_3_t": "Supporto scritto", "inst_3_d": "Assistenza via email e WhatsApp",
        "inst_4_t": "Pagamenti protetti", "inst_4_d": "Transazioni tramite Stripe e PayPal",
    },
    "en": {
        "delivery_line": "Key by email 5–15 minutes after your payment is confirmed",
        "assur_1": "Activation on official portals",
        "assur_2": "Digital delivery, nothing to ship",
        "assur_3": "Support after you buy",
        "assur_4": "Payments handled by Stripe and PayPal",
        "assur_5": "Invoice available",
        "receive_eyebrow": "What you get",
        "apps_more": "See all included apps",
        "reviews_title": "What customers say",
        "reviews_lead": "Reviews are published and verified by Trustpilot: read them straight on the platform, with nothing filtered by us.",
        "reviews_cta": "Read all reviews",
        "specs_title": "Compatibility and technical requirements",
        "faq_title": "Answers before you buy",
        "final_title": "Ready when you are",
        "final_tax": "VAT included",
        "final_instead": "instead of",
        "sticky_buy": "Buy now",
        "pay_note": "Secure payments via <strong>Stripe</strong> and <strong>PayPal</strong>",
        "trust_1_t": "European retailer", "trust_1_d": "Registered in Italy",
        "trust_2_t": "Invoice available", "trust_2_d": "VAT invoice for businesses",
        "trust_3_t": "Written support", "trust_3_d": "Email and WhatsApp",
        "trust_4_t": "Secure payments", "trust_4_d": "Processed via Stripe and PayPal",
        "inst_title": "Buy with more peace of mind",
        "inst_1_t": "European retailer", "inst_1_d": "AML Store is registered in Italy",
        "inst_2_t": "Invoice available", "inst_2_d": "Documentation for individuals and businesses",
        "inst_3_t": "Written support", "inst_3_d": "Support via email and WhatsApp",
        "inst_4_t": "Secure payments", "inst_4_d": "Processed via Stripe and PayPal",
    },
    "fr": {
        "delivery_line": "Clé par e-mail sous 5 à 15 minutes après confirmation du paiement",
        "assur_1": "Activation sur les portails officiels",
        "assur_2": "Livraison numérique, rien à expédier",
        "assur_3": "Assistance après l'achat",
        "assur_4": "Paiements gérés par Stripe et PayPal",
        "assur_5": "Facture disponible",
        "receive_eyebrow": "Ce que vous recevez",
        "apps_more": "Voir toutes les applications incluses",
        "reviews_title": "Ce que disent les clients",
        "reviews_lead": "Les avis sont publiés et vérifiés par Trustpilot : lisez-les directement sur la plateforme, sans filtre de notre part.",
        "reviews_cta": "Lire tous les avis",
        "specs_title": "Compatibilité et configuration requise",
        "faq_title": "Les réponses avant d'acheter",
        "final_title": "Tout est prêt pour démarrer",
        "final_tax": "TVA incluse",
        "final_instead": "au lieu de",
        "sticky_buy": "Acheter",
        "pay_note": "Paiements sécurisés via <strong>Stripe</strong> et <strong>PayPal</strong>",
        "trust_1_t": "Revendeur européen", "trust_1_d": "Basé en Italie",
        "trust_2_t": "Facture disponible", "trust_2_d": "TVA pour les entreprises",
        "trust_3_t": "Support par écrit", "trust_3_d": "E-mail et WhatsApp",
        "trust_4_t": "Paiements sécurisés", "trust_4_d": "Via Stripe et PayPal",
        "inst_title": "Achetez en toute confiance",
        "inst_1_t": "Revendeur européen", "inst_1_d": "AML Store a son siège en Italie",
        "inst_2_t": "Facture disponible", "inst_2_d": "Documents pour particuliers et entreprises",
        "inst_3_t": "Support par écrit", "inst_3_d": "Assistance par e-mail et WhatsApp",
        "inst_4_t": "Paiements sécurisés", "inst_4_d": "Traités via Stripe et PayPal",
    },
    "de": {
        "delivery_line": "Key per E-Mail, 5–15 Minuten nach Zahlungsbestätigung",
        "assur_1": "Aktivierung über offizielle Portale",
        "assur_2": "Digitale Lieferung, kein Versand",
        "assur_3": "Support nach dem Kauf",
        "assur_4": "Zahlungen über Stripe und PayPal",
        "assur_5": "Rechnung verfügbar",
        "receive_eyebrow": "Das bekommst du",
        "apps_more": "Alle enthaltenen Apps ansehen",
        "reviews_title": "Was Kunden sagen",
        "reviews_lead": "Die Bewertungen werden von Trustpilot veröffentlicht und geprüft: Du liest sie direkt auf der Plattform, ungefiltert von uns.",
        "reviews_cta": "Alle Bewertungen lesen",
        "specs_title": "Kompatibilität und Systemvoraussetzungen",
        "faq_title": "Antworten vor dem Kauf",
        "final_title": "Alles bereit zum Loslegen",
        "final_tax": "inkl. MwSt.",
        "final_instead": "statt",
        "sticky_buy": "Jetzt kaufen",
        "pay_note": "Sichere Zahlungen über <strong>Stripe</strong> und <strong>PayPal</strong>",
        "trust_1_t": "Europäischer Händler", "trust_1_d": "Sitz in Italien",
        "trust_2_t": "Rechnung verfügbar", "trust_2_d": "MwSt.-Rechnung für Firmen",
        "trust_3_t": "Schriftlicher Support", "trust_3_d": "E-Mail und WhatsApp",
        "trust_4_t": "Sichere Zahlungen", "trust_4_d": "Über Stripe und PayPal",
        "inst_title": "Kaufen mit mehr Sicherheit",
        "inst_1_t": "Europäischer Händler", "inst_1_d": "AML Store hat seinen Sitz in Italien",
        "inst_2_t": "Rechnung verfügbar", "inst_2_d": "Unterlagen für Privatpersonen und Unternehmen",
        "inst_3_t": "Schriftlicher Support", "inst_3_d": "Support per E-Mail und WhatsApp",
        "inst_4_t": "Sichere Zahlungen", "inst_4_d": "Abgewickelt über Stripe und PayPal",
    },
    "es": {
        "delivery_line": "Clave por email en 5–15 minutos tras confirmar el pago",
        "assur_1": "Activación en portales oficiales",
        "assur_2": "Entrega digital, sin envío",
        "assur_3": "Asistencia tras la compra",
        "assur_4": "Pagos gestionados por Stripe y PayPal",
        "assur_5": "Factura disponible",
        "receive_eyebrow": "Qué recibes",
        "apps_more": "Ver todas las apps incluidas",
        "reviews_title": "Lo que dicen los clientes",
        "reviews_lead": "Las reseñas las publica y verifica Trustpilot: las lees directamente en la plataforma, sin filtros por nuestra parte.",
        "reviews_cta": "Leer todas las reseñas",
        "specs_title": "Compatibilidad y requisitos técnicos",
        "faq_title": "Las respuestas antes de comprar",
        "final_title": "Todo listo para empezar",
        "final_tax": "IVA incluido",
        "final_instead": "en lugar de",
        "sticky_buy": "Comprar ahora",
        "pay_note": "Pagos seguros mediante <strong>Stripe</strong> y <strong>PayPal</strong>",
        "trust_1_t": "Distribuidor europeo", "trust_1_d": "Con sede en Italia",
        "trust_2_t": "Factura disponible", "trust_2_d": "IVA para empresas",
        "trust_3_t": "Soporte por escrito", "trust_3_d": "Email y WhatsApp",
        "trust_4_t": "Pagos seguros", "trust_4_d": "A través de Stripe y PayPal",
        "inst_title": "Compra con más tranquilidad",
        "inst_1_t": "Distribuidor europeo", "inst_1_d": "AML Store tiene su sede en Italia",
        "inst_2_t": "Factura disponible", "inst_2_d": "Documentación para particulares y empresas",
        "inst_3_t": "Soporte por escrito", "inst_3_d": "Asistencia por email y WhatsApp",
        "inst_4_t": "Pagos seguros", "inst_4_d": "Procesados a través de Stripe y PayPal",
    },
}

# SKU fisici (DVD/COA): niente "codice via email", si spedisce un supporto.
V3_PHYSICAL_UI = {
    "it": {
        "delivery_line": "Affidamento al corriere entro 24 ore lavorative dal pagamento",
        "assur_2": "Supporto fisico spedito, non solo digitale",
    },
    "en": {
        "delivery_line": "Handed to the courier within 24 business hours of payment",
        "assur_2": "Physical media shipped, not digital-only",
    },
    "fr": {
        "delivery_line": "Remise au transporteur sous 24 heures ouvrées après paiement",
        "assur_2": "Support physique expédié, pas seulement numérique",
    },
    "de": {
        "delivery_line": "Übergabe an den Versanddienst innerhalb von 24 Werktagsstunden nach Zahlung",
        "assur_2": "Physisches Medium wird versendet, nicht nur digital",
    },
    "es": {
        "delivery_line": "Entrega al transportista en 24 horas laborables tras el pago",
        "assur_2": "Soporte físico enviado, no solo digital",
    },
}


def _v3_for(lang, sku):
    """Stringhe del layout v3, con override per gli SKU fisici."""
    v3 = dict(V3_UI[lang])
    if is_physical_sku(sku):
        v3.update(V3_PHYSICAL_UI[lang])
    return v3


def _labels_for(lang, sku):
    labels = dict(BASE_LABELS[lang])
    if is_physical_sku(sku):
        labels.update(PHYSICAL_LABELS[lang])
    return labels


def _ui_for(lang, sku, ui_map):
    ui = dict(ui_map[lang])
    if is_physical_sku(sku):
        ui.update(PHYSICAL_UI[lang])
    return ui


BASE_LABELS = {
    "it": {
        "skip": "Vai al contenuto principale",
        "product_code": "Codice articolo",
        "add": "Aggiungi al carrello",
        "detail": "Vedi prodotto",
        "price_label": "Prezzo AML Store",
        "tax": "Tasse incluse. Nessun costo di spedizione.",
        "sticky": "Acquisto rapido",
        "steps_title": "Consegna e attivazione",
        "step_order": "Ordine",
        "step_checkout": "Checkout sicuro",
        "step_email": "Email",
        "step_email_desc": "Codice e istruzioni in pochi minuti",
        "step_act": "Attivazione",
        "desc_suffix": "Licenza digitale originale, consegna via email in pochi minuti.",
    },
    "en": {
        "skip": "Skip to main content",
        "product_code": "Product code",
        "add": "Add to cart",
        "detail": "View product",
        "price_label": "AML Store price",
        "tax": "Tax included. No shipping fees.",
        "sticky": "Quick purchase",
        "steps_title": "Delivery and activation",
        "step_order": "Order",
        "step_checkout": "Secure checkout",
        "step_email": "Email",
        "step_email_desc": "Code and instructions within minutes",
        "step_act": "Activation",
        "desc_suffix": "Genuine digital licence, email delivery within minutes.",
    },
    "fr": {
        "skip": "Aller au contenu principal",
        "product_code": "Référence produit",
        "add": "Ajouter au panier",
        "detail": "Voir le produit",
        "price_label": "Prix AML Store",
        "tax": "Taxes incluses. Pas de frais de port.",
        "sticky": "Achat rapide",
        "steps_title": "Livraison et activation",
        "step_order": "Commande",
        "step_checkout": "Paiement sécurisé",
        "step_email": "E-mail",
        "step_email_desc": "Code et instructions en quelques minutes",
        "step_act": "Activation",
        "desc_suffix": "Licence numérique originale, livraison par e-mail en quelques minutes.",
    },
    "de": {
        "skip": "Zum Hauptinhalt springen",
        "product_code": "Artikelnummer",
        "add": "In den Warenkorb",
        "detail": "Produkt ansehen",
        "price_label": "AML Store-Preis",
        "tax": "Steuern inklusive. Keine Versandkosten.",
        "sticky": "Schnellkauf",
        "steps_title": "Lieferung und Aktivierung",
        "step_order": "Bestellung",
        "step_checkout": "Sicherer Checkout",
        "step_email": "E-Mail",
        "step_email_desc": "Code und Anleitung in wenigen Minuten",
        "step_act": "Aktivierung",
        "desc_suffix": "Originale digitale Lizenz, Lieferung per E-Mail in wenigen Minuten.",
    },
    "es": {
        "skip": "Ir al contenido principal",
        "product_code": "Código de producto",
        "add": "Añadir al carrito",
        "detail": "Ver producto",
        "price_label": "Precio AML Store",
        "tax": "Impuestos incluidos. Sin gastos de envío.",
        "sticky": "Compra rápida",
        "steps_title": "Entrega y activación",
        "step_order": "Pedido",
        "step_checkout": "Checkout seguro",
        "step_email": "Email",
        "step_email_desc": "Código e instrucciones en minutos",
        "step_act": "Activación",
        "desc_suffix": "Licencia digital original, entrega por email en minutos.",
    },
}

CATALOG_META = {
    "suite-office": {
        "it": ("Suite Office", "Office perpetuo, app standalone e strumenti di produttività Microsoft."),
        "en": ("Office suite", "Perpetual Office, standalone apps and Microsoft productivity tools."),
        "fr": ("Suite Office", "Office perpétuel, applications autonomes et outils Microsoft."),
        "de": ("Office-Suite", "Office-Dauerlizenzen, Einzelapps und Microsoft-Produktivität."),
        "es": ("Suite Office", "Office perpetuo, apps independientes y productividad Microsoft."),
    },
    "sistemi-operativi": {
        "it": ("Sistemi Operativi", "Licenze Windows originali con consegna digitale rapida."),
        "en": ("Operating systems", "Genuine Windows licences with fast digital delivery."),
        "fr": ("Systèmes d'exploitation", "Licences Windows officielles, livraison numérique rapide."),
        "de": ("Betriebssysteme", "Originale Windows-Lizenzen mit schneller digitaler Lieferung."),
        "es": ("Sistemas operativos", "Licencias Windows originales con entrega digital rápida."),
    },
    "pacchetti": {
        "it": ("Pacchetti", "Bundle digitali Windows, Microsoft 365 e sicurezza."),
        "en": ("Bundles", "Digital bundles: Windows, Microsoft 365 and security."),
        "fr": ("Packs", "Packs numériques Windows, Microsoft 365 et sécurité."),
        "de": ("Pakete", "Digitale Pakete: Windows, Microsoft 365 und Sicherheit."),
        "es": ("Packs", "Packs digitales Windows, Microsoft 365 y seguridad."),
    },
    "antivirus": {
        "it": ("Antivirus", "Protezione per PC e dispositivi: licenze digitali originali."),
        "en": ("Antivirus", "Protection for PCs and devices: genuine digital licences."),
        "fr": ("Antivirus", "Protection PC et appareils : licences numériques officielles."),
        "de": ("Antivirus", "Schutz für PC und Geräte: originale digitale Lizenzen."),
        "es": ("Antivirus", "Protección para PC y dispositivos: licencias digitales originales."),
    },
    "windows-server": {
        "it": ("Windows Server e SQL", "Licenze server e database Microsoft per infrastrutture."),
        "en": ("Windows Server & SQL", "Microsoft server and database licences for infrastructure."),
        "fr": ("Windows Server et SQL", "Licences serveur et base de données Microsoft."),
        "de": ("Windows Server & SQL", "Microsoft-Server- und Datenbanklizenzen."),
        "es": ("Windows Server y SQL", "Licencias de servidor y base de datos Microsoft."),
    },
    "strumenti": {
        "it": ("Strumenti e altro", "Adobe, backup cloud, formazione e software specializzato."),
        "en": ("Tools & more", "Adobe, cloud backup, training and specialised software."),
        "fr": ("Outils et plus", "Adobe, sauvegarde cloud, formation et logiciels spécialisés."),
        "de": ("Tools & mehr", "Adobe, Cloud-Backup, Schulung und Spezialsoftware."),
        "es": ("Herramientas y más", "Adobe, backup en la nube, formación y software especializado."),
    },
}

TEMPLATE_META = {
    "office": {
        "listing": "suite-office",
        "cat_label": {"it": "Suite Office", "en": "Office suite", "fr": "Suite Office", "de": "Office-Suite", "es": "Suite Office"},
        "eyebrow": {"it": "Licenza perpetua", "en": "Perpetual licence", "fr": "Licence perpétuelle", "de": "Dauerlizenz", "es": "Licencia perpetua"},
        "activation": {"it": "Portale setup.office.com", "en": "Official setup.office.com portal", "fr": "Portail setup.office.com", "de": "setup.office.com-Portal", "es": "Portal setup.office.com"},
        "brand": "Microsoft",
        "blurb": {"it": "Licenza ESD · setup.office.com", "en": "ESD licence · setup.office.com", "fr": "Licence ESD · setup.office.com", "de": "ESD-Lizenz · setup.office.com", "es": "Licencia ESD · setup.office.com"},
    },
    "m365": {
        "listing": "suite-office",
        "cat_label": {"it": "Suite Office", "en": "Office suite", "fr": "Suite Office", "de": "Office-Suite", "es": "Suite Office"},
        "eyebrow": {"it": "Abbonamento Microsoft 365", "en": "Microsoft 365 subscription", "fr": "Abonnement Microsoft 365", "de": "Microsoft-365-Abonnement", "es": "Suscripción Microsoft 365"},
        "activation": {"it": "Account Microsoft ufficiale", "en": "Official Microsoft account", "fr": "Compte Microsoft officiel", "de": "Offizielles Microsoft-Konto", "es": "Cuenta Microsoft oficial"},
        "brand": "Microsoft",
        "blurb": {"it": "Abbonamento · attivazione account Microsoft", "en": "Subscription · Microsoft account activation", "fr": "Abonnement · compte Microsoft", "de": "Abonnement · Microsoft-Konto", "es": "Suscripción · cuenta Microsoft"},
    },
    "windows": {
        "listing": "sistemi-operativi",
        "cat_label": {"it": "Sistemi Operativi", "en": "Operating systems", "fr": "Systèmes d'exploitation", "de": "Betriebssysteme", "es": "Sistemas operativos"},
        "eyebrow": {"it": "Sistema operativo", "en": "Operating system", "fr": "Système d'exploitation", "de": "Betriebssystem", "es": "Sistema operativo"},
        "activation": {"it": "Attivazione ufficiale Microsoft", "en": "Official Microsoft activation", "fr": "Activation Microsoft officielle", "de": "Offizielle Microsoft-Aktivierung", "es": "Activación oficial Microsoft"},
        "brand": "Microsoft",
        "blurb": {"it": "ESD · Attivazione immediata", "en": "ESD · Instant activation", "fr": "ESD · Activation immédiate", "de": "ESD · Sofortige Aktivierung", "es": "ESD · Activación inmediata"},
    },
    "bundle": {
        "listing": "pacchetti",
        "cat_label": {"it": "Pacchetti", "en": "Bundles", "fr": "Packs", "de": "Pakete", "es": "Packs"},
        "eyebrow": {"it": "Pacchetto digitale", "en": "Digital bundle", "fr": "Pack numérique", "de": "Digitales Paket", "es": "Pack digital"},
        "activation": {"it": "Email con codici e istruzioni", "en": "Email with codes and instructions", "fr": "E-mail avec codes et instructions", "de": "E-Mail mit Codes und Anleitung", "es": "Email con códigos e instrucciones"},
        "brand": "Microsoft",
        "blurb": {"it": "Bundle · consegna digitale", "en": "Bundle · digital delivery", "fr": "Pack · livraison numérique", "de": "Paket · digitale Lieferung", "es": "Pack · entrega digital"},
    },
    "antivirus": {
        "listing": "antivirus",
        "cat_label": {"it": "Antivirus", "en": "Antivirus", "fr": "Antivirus", "de": "Antivirus", "es": "Antivirus"},
        "eyebrow": {"it": "Antivirus", "en": "Antivirus", "fr": "Antivirus", "de": "Antivirus", "es": "Antivirus"},
        "activation": {"it": "Portale ufficiale del produttore", "en": "Official vendor portal", "fr": "Portail officiel de l'éditeur", "de": "Offizielles Herstellerportal", "es": "Portal oficial del fabricante"},
        "brand": None,
        "blurb": {"it": "Abbonamento · licenza digitale", "en": "Subscription · digital licence", "fr": "Abonnement · licence numérique", "de": "Abonnement · digitale Lizenz", "es": "Suscripción · licencia digital"},
    },
    "server": {
        "listing": "windows-server",
        "cat_label": {"it": "Windows Server e SQL", "en": "Windows Server & SQL", "fr": "Windows Server et SQL", "de": "Windows Server & SQL", "es": "Windows Server y SQL"},
        "eyebrow": {"it": "Server / database", "en": "Server / database", "fr": "Serveur / base de données", "de": "Server / Datenbank", "es": "Servidor / base de datos"},
        "activation": {"it": "Attivazione ufficiale Microsoft", "en": "Official Microsoft activation", "fr": "Activation Microsoft officielle", "de": "Offizielle Microsoft-Aktivierung", "es": "Activación oficial Microsoft"},
        "brand": "Microsoft",
        "blurb": {"it": "Licenza ESD · server/database", "en": "ESD licence · server/database", "fr": "Licence ESD · serveur/BD", "de": "ESD · Server/Datenbank", "es": "Licencia ESD · servidor/BD"},
    },
    "tool": {
        "listing": "strumenti",
        "cat_label": {"it": "Strumenti e altro", "en": "Tools & more", "fr": "Outils et plus", "de": "Tools & mehr", "es": "Herramientas y más"},
        "eyebrow": {"it": "Software professionale", "en": "Professional software", "fr": "Logiciel professionnel", "de": "Professionelle Software", "es": "Software profesional"},
        "activation": {"it": "Portale ufficiale del produttore", "en": "Official vendor portal", "fr": "Portail officiel de l'éditeur", "de": "Offizielles Herstellerportal", "es": "Portal oficial del fabricante"},
        "brand": None,
        "blurb": {"it": "Licenza digitale · consegna email", "en": "Digital licence · email delivery", "fr": "Licence numérique · e-mail", "de": "Digitale Lizenz · E-Mail", "es": "Licencia digital · email"},
    },
    "backup": {
        "listing": "strumenti",
        "cat_label": {"it": "Strumenti e altro", "en": "Tools & more", "fr": "Outils et plus", "de": "Tools & mehr", "es": "Herramientas y más"},
        "eyebrow": {"it": "Backup cloud", "en": "Cloud backup", "fr": "Sauvegarde cloud", "de": "Cloud-Backup", "es": "Backup en la nube"},
        "activation": {"it": "Portale ufficiale Acronis", "en": "Official Acronis portal", "fr": "Portail Acronis officiel", "de": "Offizielles Acronis-Portal", "es": "Portal oficial Acronis"},
        "brand": "Acronis",
        "blurb": {"it": "Backup · storage cloud incluso", "en": "Backup · cloud storage included", "fr": "Sauvegarde · cloud inclus", "de": "Backup · Cloud-Speicher", "es": "Backup · almacenamiento cloud"},
    },
    "training": {
        "listing": "strumenti",
        "cat_label": {"it": "Strumenti e altro", "en": "Tools & more", "fr": "Outils et plus", "de": "Tools & mehr", "es": "Herramientas y más"},
        "eyebrow": {"it": "Formazione", "en": "Training", "fr": "Formation", "de": "Schulung", "es": "Formación"},
        "activation": {"it": "Download digitale via email", "en": "Digital download via email", "fr": "Téléchargement par e-mail", "de": "Digitaler Download per E-Mail", "es": "Descarga digital por email"},
        "brand": "Microsoft",
        "blurb": {"it": "Guida PDF · consegna immediata", "en": "PDF guide · instant delivery", "fr": "Guide PDF · livraison immédiate", "de": "PDF-Guide · sofortige Lieferung", "es": "Guía PDF · entrega inmediata"},
    },
}


def entry(sku):
    for e in CATALOG:
        if e["sku"] == sku:
            return e
    raise KeyError(sku)


def product_code_html(labels, sku):
    return (
        f'<p class="v2-product-code"><span>{html_module.escape(labels["product_code"])}:</span> '
        f'<code class="v2-product-code__value">{html_module.escape(sku)}</code></p>'
    )


def eur_fmt(minor):
    return f"{minor / 100:.2f}".replace(".", ",")


def pct(sale, compare):
    if compare <= sale:
        return 0
    return int(round((1 - sale / compare) * 100))


def hreflang_block(slug):
    lines = []
    for lg in LANGS:
        lines.append(
            f'    <link rel="alternate" hreflang="{lg}" href="https://aml-store.com/{lg}/{slug}">'
        )
    lines.append(
        f'    <link rel="alternate" hreflang="x-default" href="https://aml-store.com/it/{slug}">'
    )
    return "\n".join(lines)


def product_card_price_block(sale, compare, disc, clean=False):
    if disc > 0 and not clean:
        return f"""                    <div class="product-card-price-block">
                        <div class="product-card-price-block__row">
                            <span class="product-card-price-block__msrp">€ {eur_fmt(compare)}</span>
                            <span class="product-card-price-block__sale">€ {eur_fmt(sale)}</span>
                            <span class="product-card-price-block__save">−{disc}%</span>
                        </div>
                    </div>"""
    return f"""                    <p class="product-card-price">€ {eur_fmt(sale)}</p>"""


def product_card(lang, prod, labels, clean_price=False):
    e = entry(prod["sku"])
    sale = e["unitAmountMinor"]
    compare = e["compareAtMinor"]
    disc = pct(sale, compare)
    meta = TEMPLATE_META[prod["template"]]
    name = prod["card_name"]
    blurb_raw = prod.get("blurb")
    if isinstance(blurb_raw, dict):
        blurb = blurb_raw.get(lang) or meta["blurb"][lang]
    elif blurb_raw:
        blurb = blurb_raw
    else:
        blurb = meta["blurb"][lang]
    slug = prod["slug"]
    image = prod["image"]
    href_suffix = prod.get("href_suffix", ".html")
    href = f"{slug}{href_suffix}"
    image_src = prod.get("image_src") or _product_image_src(slug, image)
    lazy_attr = ' loading="lazy"' if prod.get("lazy") else ""
    fp = prod.get("fetchpriority")
    fp_attr = f' fetchpriority="{fp}"' if fp in ("high", "low", "auto") else ""
    price_html = product_card_price_block(sale, compare, disc, clean=clean_price)
    return f"""                <div
                    class="product-card"
                    data-stripe-currency="eur"
                    data-stripe-unit-amount="{sale}"
                    data-stripe-compare-at-amount="{compare}"
                    data-stripe-product-sku="{prod['sku']}"
                    data-discount-percent="{disc}"
                >
                    <a href="{href}" class="product-card-body product-card--link">
                        <div class="product-card-media">
                            <img src="{image_src}" width="400" height="400" alt="{name}" decoding="async"{lazy_attr}{fp_attr} class="product-card-img" onerror="this.onerror=null;this.src='{PRODUCT_COVER_FALLBACK_SRC}'">
                        </div>
                        <p class="product-card-name">{name}</p>
                        <p class="product-card-blurb">{blurb}</p>
                    </a>
{price_html}
                    <div class="product-card-foot">
                        <button type="button" class="btn-cta-primary product-card-add" data-cart-add>{labels['add']}</button>
                    </div>
                </div>
"""


PAYMENT_LOGOS = [
    ("img-aml-store_Visa_logo.svg", "Visa"),
    ("img-aml-store_Mastercard_logo.svg", "Mastercard"),
    ("img-aml-store_PayPal-logo.svg", "PayPal"),
    ("img-aml-store_Apple_Pay_logo.svg", "Apple Pay"),
    ("img-aml-store_Google_Pay_Logo.svg", "Google Pay"),
    ("img-aml-store_Stripe_Logo.svg", "Stripe"),
]

CART_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" width="20" height="20">'
    '<path fill="currentColor" d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z"/>'
    "</svg>"
)


def _product_image_src(slug, fallback_image=None):
    """Prefer products/{slug}.webp; never silently reuse another SKU's box art."""
    product_path = ROOT / "asset" / "media" / "products" / f"{slug}.webp"
    if product_path.exists():
        return f"../asset/media/products/{slug}.webp"
    if fallback_image:
        stem = Path(fallback_image).stem
        # Accept only a media file that clearly belongs to this slug.
        if stem == slug or stem.startswith(f"{slug}-"):
            media_path = ROOT / "asset" / "media" / fallback_image
            if media_path.exists():
                return f"../asset/media/{fallback_image}"
    return PRODUCT_COVER_FALLBACK_SRC


def _icon_src(key):
    from product_content_office import ICON

    return f"../asset/icon/{ICON[key]}"


def _render_pills(pills):
    parts = []
    for icon_key, label in pills:
        icon_html = ""
        if icon_key:
            icon_html = (
                f'<img src="{_icon_src(icon_key)}" width="18" height="18" alt="" '
                f'loading="lazy" decoding="async">'
            )
        parts.append(
            f"""                        <span class="v2-pill">
                            {icon_html}
                            {label}
                        </span>"""
        )
    return "\n".join(parts)


def _render_features(features):
    parts = []
    for span, tone, label, title, body in features:
        tone_cls = f" v2-bento__cell--{tone}" if tone else ""
        label_html = f'<p class="v2-bento__label">{label}</p>' if label else ""
        parts.append(
            f"""                <div class="v2-bento__cell v2-bento__cell--{span}{tone_cls}" role="listitem">
                    {label_html}
                    <h3 class="v2-bento__title">{title}</h3>
                    <p class="v2-bento__body">{body}</p>
                </div>"""
        )
    return "\n".join(parts)


def _render_lifestyle_band(lifestyle, lang):
    """Full-bleed lifestyle band (Win11 gallery CWV pattern). Optional per SKU."""
    if not lifestyle:
        return ""
    img = lifestyle["image"]
    img_640 = lifestyle.get("image_640")
    w = int(lifestyle.get("width") or 1024)
    h = int(lifestyle.get("height") or 640)
    alt = lifestyle["alt"][lang]
    kicker = lifestyle["kicker"][lang]
    title = lifestyle["title"][lang]
    body = lifestyle["body"][lang]
    # Di norma le foto lifestyle stanno sotto products/. `image_root: ""` serve alle
    # immagini che vivono direttamente in asset/media/ (es. windows-11-home).
    root = lifestyle.get("image_root", "products/")
    src = f"../asset/media/{root}{img}"
    srcset_attrs = ""
    if img_640 and img_640 != img:
        src_640 = f"../asset/media/{root}{img_640}"
        srcset_attrs = f'\n                    srcset="{src_640} 640w, {src} {w}w"\n                    sizes="100vw"'
    return f"""        <hr class="v2-divider">
        <section class="v2-section v2-section--gallery" aria-label="{title}">
            <figure class="bento-figure">
                <img
                    class="bento-img"
                    src="{src}"{srcset_attrs}
                    width="{w}"
                    height="{h}"
                    alt="{alt}"
                    loading="lazy"
                    decoding="async"
                >
                <figcaption class="bento-caption">
                    <span class="bento-kicker">{kicker}</span>
                    <h3 class="bento-title">{title}</h3>
                    <p class="bento-text">{body}</p>
                </figcaption>
            </figure>
        </section>
        <hr class="v2-divider">
"""


def _render_apps(app_keys, labels_map=None):
    names = {
        "word": "Word",
        "excel": "Excel",
        "powerpoint": "PowerPoint",
        "outlook": "Outlook",
        "onenote": "OneNote",
    }
    parts = []
    for key in app_keys:
        parts.append(
            f"""                <div class="v2-app-item">
                    <img src="{_icon_src(key)}" width="48" height="48" alt="" loading="lazy" decoding="async">
                    {names.get(key, key.title())}
                </div>"""
        )
    return "\n".join(parts)


def _render_faq(faq_items):
    parts = []
    for q, a in faq_items:
        parts.append(
            f"""                <details class="home-faq-item">
                    <summary>{q}</summary>
                    <div class="home-faq-body">
                        <p>{a}</p>
                    </div>
                </details>"""
        )
    return "\n".join(parts)


def _render_faq_columns(faq_items):
    """Due colonne indipendenti (non una griglia a righe): aprire una risposta
    in una non allunga più la riga né lascia un buco vuoto nell'altra. Taglio
    sequenziale (non alternato), così l'ordine di lettura/tab resta naturale
    anche su mobile, dove le colonne collassano in una sola (vedi CSS
    .pf-faq-col { display: contents }, product-v3.css)."""
    half = (len(faq_items) + 1) // 2
    col1, col2 = faq_items[:half], faq_items[half:]
    return (
        '                <div class="pf-faq-col">\n'
        f"{_render_faq(col1)}\n"
        "                </div>\n"
        '                <div class="pf-faq-col">\n'
        f"{_render_faq(col2)}\n"
        "                </div>"
    )


def _render_steps_block(ui, content, lang):
    """3 install/order steps — content['steps'][lang] overrides UI defaults."""
    custom = (content.get("steps") or {}).get(lang)
    if custom and len(custom) >= 3:
        items = custom[:3]
        titles = [t for t, _ in items]
        bodies = [b for _, b in items]
    else:
        titles = [ui["step1_title"], ui["step2_title"], ui["step3_title"]]
        bodies = [ui["step1_body"], ui["step2_body"], ui["step3_body"]]
    how_title = (content.get("steps_title") or {}).get(lang) or ui["how_title"]
    parts = [
        f"""        <section class="v2-section" aria-labelledby="v2-steps-title">
            <p class="v2-eyebrow">{ui['how_eyebrow']}</p>
            <h2 id="v2-steps-title" class="v2-section-title">{how_title}</h2>
            <div class="v2-steps">"""
    ]
    for i, (title, body) in enumerate(zip(titles, bodies), start=1):
        parts.append(
            f"""                <div class="v2-step">
                    <div class="v2-step__num" aria-hidden="true">{i}</div>
                    <h3 class="v2-step__title">{title}</h3>
                    <p class="v2-step__body">{body}</p>
                </div>"""
        )
    parts.append("            </div>\n        </section>")
    return "\n".join(parts)


def _render_specs_block(ui, content, lang):
    """4 requirement cells — content['specs'][lang] overrides UI defaults."""
    custom = (content.get("specs") or {}).get(lang)
    note = (content.get("specs_note") or {}).get(lang) or ui["specs_note"]
    if custom and len(custom) >= 4:
        cells = custom[:4]
    else:
        cells = [
            (ui["spec_cpu"], ui["spec_cpu_body"]),
            (ui["spec_os"], ui["spec_os_body"]),
            (ui["spec_ram"], ui["spec_ram_body"]),
            (ui["spec_disk"], ui["spec_disk_body"]),
        ]
    items = "\n".join(
        f"""                <div class="v2-specs-item">
                    <h3>{title}</h3>
                    <p>{body}</p>
                </div>"""
        for title, body in cells
    )
    return f"""        <section class="v2-section v2-section--tight" aria-labelledby="v2-specs-title">
            <p class="v2-eyebrow">{ui['specs_eyebrow']}</p>
            <h2 id="v2-specs-title" class="v2-section-title" style="margin-bottom:8px;">{ui['specs_title']}</h2>
            <p style="font-size:.85rem;color:rgba(255,255,255,0.5);margin:0 0 32px;">{note}</p>
            <div class="v2-specs-grid">
{items}
            </div>
        </section>"""


def _render_payment_row(ui):
    logos = "\n".join(
        f'                        <span class="v2-payment-logo" title="{alt}">'
        f'<img src="../asset/payments_logo/{fname}" alt="{alt}" loading="lazy" decoding="async"></span>'
        for fname, alt in PAYMENT_LOGOS
    )
    return f"""                    <div class="v2-payment-row" role="group" aria-label="{ui['payments_aria']}">
{logos}
                    </div>"""


LOCK_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
    '<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>'
    '<path stroke-linecap="round" stroke-linejoin="round" d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'
)


def _render_pay_note(v3):
    """Sostituisce i 6 loghi pagamento nel pannello acquisto con una riga di
    testo: nel punto più importante della pagina i loghi sono rumore, non
    informazione (restano nel checkout/footer)."""
    return f"""                <p class="pf-pay-note">
                    {LOCK_ICON}
                    {v3['pay_note']}
                </p>"""


TRUSTBAR_ICONS = [
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M3 21h18M4 21V8l8-5 8 5v13M9 21v-6h6v6"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M6 2h9l5 5v15H6zM15 2v5h5M9 13h6M9 17h6"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M12 1a9 9 0 0 0-9 9v7c0 1.66 1.34 3 3 3h2v-8H5v-2a7 7 0 0 1 14 0v2h-3v8h2c1.66 0 3-1.34 3-3v-7a9 9 0 0 0-9-9z"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path stroke-linecap="round" stroke-linejoin="round" d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
]


def _render_trustbar(v3):
    """Fascia di fiducia sotto l'hero: azienda/fatturazione/supporto/pagamenti.
    Generica, non legata a un prodotto — uguale su tutte le pagine."""
    items = "\n".join(
        f"""            <div class="pf-trustbar__item">
                <span class="pf-trustbar__icon" aria-hidden="true">{icon}</span>
                <span class="pf-trustbar__text"><strong>{v3[f'trust_{i}_t']}</strong><span>{v3[f'trust_{i}_d']}</span></span>
            </div>"""
        for i, icon in enumerate(TRUSTBAR_ICONS, start=1)
    )
    return f"""    <div class="pf-trustbar">
        <div class="pf-trustbar__inner">
{items}
        </div>
    </div>
"""


def _render_institutional(v3):
    """Fascia navy prima delle FAQ: stesso messaggio di fiducia, con più peso
    visivo. Generica, non legata a un prodotto — uguale su tutte le pagine."""
    items = "\n".join(
        f"""                    <li><strong>{v3[f'inst_{i}_t']}</strong><span>{v3[f'inst_{i}_d']}</span></li>"""
        for i in (1, 2, 3, 4)
    )
    return f"""        <div class="pf-institutional">
            <div class="pf-institutional__inner">
                <h2 class="pf-institutional__title">{v3['inst_title']}</h2>
                <ul class="pf-institutional__grid">
{items}
                </ul>
            </div>
        </div>
"""


# ── Renderer del layout v3 ──────────────────────────────────────────────────

MAIL_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
    '<path stroke-linecap="round" stroke-linejoin="round" d="M3 8l9 6 9-6M4 5h16a1 1 0 011 1v12a1 1 0 '
    '01-1 1H4a1 1 0 01-1-1V6a1 1 0 011-1z"/></svg>'
)

GIFT_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
    '<path stroke-linecap="round" stroke-linejoin="round" d="M20 12v10H4V12M2 7h20v5H2V7zm10 15V7m0 0a2.5 '
    '2.5 0 10-2.5-2.5A2.5 2.5 0 0012 7zm0 0a2.5 2.5 0 102.5-2.5A2.5 2.5 0 0012 7z"/></svg>'
)

# Testo del badge omaggio guida Copilot: solo italiano perche' la guida esiste
# solo in quella lingua (vedi functions/api/_lib/guide.js GUIDE_LOCALES) — un
# ordine EN/FR/DE/ES non la riceve, quindi il badge non deve promettergliela.
COPILOT_BONUS_HTML_IT = (
    f'                <p class="pdp-bonus">\n'
    f'                    {GIFT_ICON}\n'
    f'                    <span><strong>In regalo:</strong> Guida Copilot per Microsoft 365 '
    f'(PDF, via email dopo l\'acquisto)</span>\n'
    f'                </p>\n'
)


def _render_assur(v3):
    return "\n".join(
        f"                            <li>{v3[k]}</li>"
        for k in ("assur_1", "assur_2", "assur_3", "assur_4", "assur_5")
    )


def _render_keypoints(content, lang):
    """
    Checklist dell'hero. Usa `keypoints` se il prodotto li fornisce, altrimenti i
    titoli delle prime quattro feature: sono già frasi-beneficio brevi. Le card più
    in basso ripetono quei titoli ma con il corpo, quindi è un riassunto seguito dal
    dettaglio, non la stessa informazione due volte allo stesso livello.
    """
    points = (content.get("keypoints") or {}).get(lang)
    if not points:
        points = [f[3] for f in content["features"][lang][:4]]
    rows = "\n".join(
        f"                            <li>{p}</li>" for p in points
    )
    return f"""                        <ul class="pdp-keylist">
{rows}
                        </ul>"""


def _render_cards(features):
    """features: (span, tone, label, title, body) — span e tone del vecchio bento non servono."""
    parts = []
    for item in features:
        label, title, body = item[2], item[3], item[4]
        label_html = (
            f'                    <p class="pdp-card__label">{label}</p>\n' if label else ""
        )
        parts.append(
            f"""                <li class="pdp-card">
{label_html}                    <h3 class="pdp-card__title">{title}</h3>
                    <p class="pdp-card__body">{body}</p>
                </li>"""
        )
    return "\n".join(parts)


APP_NAMES = {
    "word": "Word", "excel": "Excel", "powerpoint": "PowerPoint", "outlook": "Outlook",
    "onenote": "OneNote", "onedrive": "OneDrive", "teams": "Teams", "defender": "Defender",
    "copilot": "Copilot", "designer": "Designer", "clipchamp": "Clipchamp",
    "publisher": "Publisher", "access": "Access",
}


def _app_item(key, indent):
    pad = " " * indent
    return (
        f"{pad}<li class=\"pdp-app\">\n"
        f"{pad}    <img src=\"{_icon_src(key)}\" width=\"48\" height=\"48\" alt=\"\" loading=\"lazy\" decoding=\"async\">\n"
        f"{pad}    {APP_NAMES.get(key, key.title())}\n"
        f"{pad}</li>"
    )


def _render_apps_v3(app_keys, v3):
    """Fino a 6 app in evidenza, le altre in un pannello espandibile."""
    primary, extra = app_keys[:6], app_keys[6:]
    main = "\n".join(_app_item(k, 20) for k in primary)
    block = f"""                <ul class="pdp-apps">
{main}
                </ul>"""
    if not extra:
        return block
    more = "\n".join(_app_item(k, 28) for k in extra)
    return f"""{block}
                <details class="pdp-apps-more">
                    <summary>{v3['apps_more']}</summary>
                    <div class="pdp-apps-more__body">
                        <ul class="pdp-apps">
{more}
                        </ul>
                    </div>
                </details>"""


def _render_steps_v3(ui, content, lang):
    """content['steps'][lang] ha la precedenza sui default UI (es. spedizione di un DVD)."""
    custom = (content.get("steps") or {}).get(lang)
    if custom and len(custom) >= 3:
        pairs = custom[:3]
    else:
        pairs = [(ui[f"step{n}_title"], ui[f"step{n}_body"]) for n in (1, 2, 3)]
    return "\n".join(
        f"""                <li class="pdp-step">
                    <div>
                        <h3>{title}</h3>
                        <p>{body}</p>
                    </div>
                </li>"""
        for title, body in pairs
    )


def _render_specs_v3(ui, content, lang):
    """content['specs'][lang] ha la precedenza sui default UI. Due colonne
    indipendenti come le FAQ (vedi _render_faq_columns): stesso motivo."""
    custom = (content.get("specs") or {}).get(lang)
    if custom and len(custom) >= 4:
        cells = custom[:4]
    else:
        cells = [(ui[f"spec_{k}"], ui[f"spec_{k}_body"]) for k in ("cpu", "os", "ram", "disk")]
    return _render_faq_columns(cells)


def build_rich_product_page(lang, prod, content, ui_map=None):
    if ui_map is None:
        from product_content_office import UI as ui_map

    e = entry(prod["sku"])
    slug = prod["slug"]
    sku = prod["sku"]
    sale = e["unitAmountMinor"]
    compare = e["compareAtMinor"]
    disc = pct(sale, compare)
    save = compare - sale
    labels = _labels_for(lang, sku)
    ui = _ui_for(lang, sku, ui_map)
    meta = TEMPLATE_META[prod["template"]]
    short = (content.get("name") or {}).get(lang) or prod["card_name"]
    seo_title = (content.get("seo_title") or {}).get(lang) or f"{short} — Aml Store"
    brand = prod.get("brand") or meta["brand"] or "Microsoft"
    cat_slug = meta["listing"]
    cat_name = meta["cat_label"][lang]
    desc = content["desc"][lang]
    desc_attr = html_module.escape(desc, quote=True)
    seo_title_attr = html_module.escape(seo_title, quote=True)
    eyebrow = content["eyebrow"][lang]
    title_html = content["title_html"][lang]
    price_dec = f"{sale / 100:.2f}"
    img_src = _product_image_src(slug, prod["image"])
    og_image_abs = (
        f"https://aml-store.com/asset/media/products/{slug}.webp"
        if (ROOT / "asset" / "media" / "products" / f"{slug}.webp").exists()
        else f"https://aml-store.com/asset/media/{prod['image']}"
    )
    page_url = f"https://aml-store.com/{lang}/{slug}"
    badge_html = (
        f'<span class="pdp-price-badge" aria-label="−{disc}%">−{disc}%</span>'
        if disc > 0
        else ""
    )
    msrp_html = (
        f'<span class="pdp-price-msrp" aria-label="{eur_fmt(compare)}">€ {eur_fmt(compare)}</span>'
        if disc > 0
        else ""
    )
    # Il risparmio è una frase dentro la nota prezzo, non più un blocco a sé.
    save_html = ""
    if save > 0:
        save_html = (
            f" {ui['save_prefix']} <strong>€ {eur_fmt(save)}</strong> "
            f"{ui['save_vs']} (€ {eur_fmt(compare)})."
        )
    final_instead_html = f", {_v3_for(lang, sku)['final_instead']} € {eur_fmt(compare)}" if save > 0 else ""

    faq_entities = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in content["faq"][lang]
    ]

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": "https://aml-store.com/#organization",
                "name": "Aml Store",
                "url": "https://aml-store.com/",
            },
            {
                "@type": "Product",
                "@id": f"{page_url}#product",
                "name": short,
                "sku": sku,
                **({"mpn": e["mpn"]} if e.get("mpn") else {}),
                "inLanguage": lang,
                "url": page_url,
                "image": og_image_abs,
                "description": desc,
                "brand": {"@type": "Brand", "name": brand},
                "offers": {
                    "@type": "Offer",
                    "url": page_url,
                    "priceCurrency": "EUR",
                    "price": price_dec,
                    "availability": "https://schema.org/InStock",
                    "itemCondition": "https://schema.org/NewCondition",
                    "seller": {"@id": "https://aml-store.com/#organization"},
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"https://aml-store.com/{lang}/"},
                    {"@type": "ListItem", "position": 2, "name": cat_name, "item": f"https://aml-store.com/{lang}/{cat_slug}"},
                    {"@type": "ListItem", "position": 3, "name": short},
                ],
            },
            {
                "@type": "FAQPage",
                "inLanguage": lang,
                "url": page_url,
                "mainEntity": faq_entities,
            },
        ],
    }

    v3 = _v3_for(lang, sku)
    keypoints_html = _render_keypoints(content, lang)
    steps_title = (content.get('steps_title') or {}).get(lang) or ui['how_title']
    specs_note = (content.get('specs_note') or {}).get(lang) or ui['specs_note']
    bonus_html = COPILOT_BONUS_HTML_IT if (content.get("copilot_bonus") and lang == "it") else ""

    # Sezioni condizionali: compaiono solo se il prodotto fornisce i dati.
    apps_block = ""
    if content.get("apps"):
        apps_block = f"""        <hr class="pdp-divider">

        <section class="pdp-sec" aria-labelledby="pdp-apps-title">
            <p class="pdp-sec__eyebrow">{ui['apps_eyebrow']}</p>
            <h2 id="pdp-apps-title" class="pdp-sec__title">{content['apps_title'][lang]}</h2>
{_render_apps_v3(content['apps'], v3)}
        </section>
"""

    lifestyle_block = _render_lifestyle_band(content.get("lifestyle"), lang)

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{seo_title_attr}</title>
    <meta name="description" content="{desc_attr}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{page_url}">
    <meta property="og:type" content="product">
    <meta property="og:site_name" content="Aml Store">
    <meta property="og:title" content="{seo_title_attr}">
    <meta property="og:description" content="{desc_attr}">
    <meta property="og:url" content="{page_url}">
    <meta property="og:locale" content="{LOCALE[lang]}">
    <meta property="og:image" content="{og_image_abs}">
    <meta property="product:price:amount" content="{price_dec}">
    <meta property="product:price:currency" content="EUR">
{hreflang_block(slug)}
    <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
    </script>
    <script src="../js/consent-init.js"></script>
    <link rel="icon" href="../favicon/favicon.png" type="image/png">
    <link rel="apple-touch-icon" href="../favicon/apple-touch-icon.png">
    <link rel="preload" as="image" href="{img_src}" fetchpriority="high" type="image/webp">
    <link rel="stylesheet" href="../fonts/montserrat.css">
    <link rel="stylesheet" href="../css/page.css">
    <link rel="stylesheet" href="../css/header.css">
    <link rel="stylesheet" href="../css/footer.css">
    <link rel="stylesheet" href="../css/product.css">
    <link rel="stylesheet" href="../css/product-pdp.css">
    <script src="../js/theme-init.js"></script>
</head>
<body class="pdp-page">
    <a class="skip-link" href="#main">{labels['skip']}</a>
    <ecommerce-header translate="no" class="notranslate"></ecommerce-header>
    <div id="product-sticky-cta" class="product-sticky-cta" role="region" aria-label="{labels['sticky']}" aria-hidden="true">
        <div class="product-sticky-cta__inner">
            <span class="product-sticky-cta__title">{short}</span>
            <div class="product-sticky-cta__prices" aria-hidden="true">
                <span class="product-sticky-cta__msrp">€ {eur_fmt(compare)}</span>
                <span class="product-sticky-cta__sale">€ {eur_fmt(sale)}</span>
            </div>
            <button type="button" class="btn-primary" data-cart-add data-cart-source="product-pricing" data-pdp-buy-now>
                {CART_ICON}
                {v3['sticky_buy']}
            </button>
        </div>
    </div>

    <section class="pdp-hero" aria-label="{ui['hero_aria']}">

        <div class="pdp-breadcrumb">
            <nav aria-label="{ui['breadcrumb_nav']}">
                <a href="/{lang}/">Home</a>
                <span class="sep" aria-hidden="true">/</span>
                <a href="/{lang}/{cat_slug}">{cat_name}</a>
                <span class="sep" aria-hidden="true">/</span>
                <span aria-current="page">{short}</span>
            </nav>
        </div>

        <div class="pdp-hero__inner">
            <div class="pdp-hero__info">
                <p class="pdp-eyebrow">{eyebrow}</p>
                <h1 class="pdp-h1 v2-hero__title">{title_html}</h1>
                {product_code_html(labels, sku)}

                <div class="pdp-hero__split">
                    <figure class="pdp-media">
                        <img class="pdp-media__img product-cover-img" src="{img_src}" width="400" height="400" alt="{short}" fetchpriority="high" decoding="async">
                    </figure>
                    <div class="pdp-hero__text">
                        <p class="v2-hero__desc">{desc}</p>
{keypoints_html}
                    </div>
                </div>
            </div>

            <div id="product-pricing" class="pdp-buy"
                data-stripe-currency="eur"
                data-stripe-unit-amount="{sale}"
                data-stripe-compare-at-amount="{compare}"
                data-stripe-product-sku="{sku}"
                data-discount-percent="{disc}"{_physical_attr(sku)}>
                <p class="pdp-buy__label">{labels['price_label']}</p>

                <div class="pdp-price-row" role="group" aria-label="{ui['prices_aria']}">
                    <span class="pdp-price-sale">€ {eur_fmt(sale)}</span>
                    {msrp_html}
                    {badge_html}
                </div>
                <p class="pdp-price-note">{labels['tax']}{save_html}</p>
{_stock_block_html(lang, sku)}
                <button type="button" id="product-primary-cta" class="pdp-btn-primary" data-cart-add data-cart-source="product-pricing">
                    {CART_ICON}
                    {labels['add']}
                </button>

{_trustpilot_buy_mini(lang)}
                <p class="pdp-delivery">
                    {MAIL_ICON}
                    {v3['delivery_line']}
                </p>
{bonus_html}
                <ul class="pdp-assur">
{_render_assur(v3)}
                </ul>
{_render_pay_note(v3)}
            </div>
        </div>
    </section>
{_render_trustbar(v3)}
    <main id="main" class="product-page" data-cart-added-msg="{ui['cart_added']}">
        <div id="product-cart-live" class="visually-hidden" aria-live="polite" aria-atomic="true"></div>

        <section class="pdp-sec" aria-labelledby="pdp-features-title">
            <p class="pdp-sec__eyebrow">{ui['features_eyebrow']}</p>
            <h2 id="pdp-features-title" class="pdp-sec__title">{content['features_title'][lang]}</h2>
            <ul class="pdp-cards">
{_render_cards(content['features'][lang])}
            </ul>
        </section>

{apps_block}{lifestyle_block}        <hr class="pdp-divider">

        <section class="pdp-sec" aria-labelledby="pdp-steps-title">
            <p class="pdp-sec__eyebrow">{ui['how_eyebrow']}</p>
            <h2 id="pdp-steps-title" class="pdp-sec__title">{steps_title}</h2>
            <ol class="pdp-steps">
{_render_steps_v3(ui, content, lang)}
            </ol>
        </section>

{_render_institutional(v3)}
        <section id="faq" class="pdp-sec home-faq" aria-labelledby="pdp-faq-title">
            <p class="pdp-sec__eyebrow">{ui['faq_eyebrow']}</p>
            <h2 id="pdp-faq-title" class="pdp-sec__title pdp-faq__title">{v3['faq_title']}</h2>
            <div class="home-faq-list">
{_render_faq_columns(content['faq'][lang])}
            </div>
        </section>

        <hr class="pdp-divider">

        <section class="pdp-sec pdp-sec--tight pdp-acc home-faq" aria-labelledby="pdp-specs-title">
            <p class="pdp-sec__eyebrow">{ui['specs_eyebrow']}</p>
            <h2 id="pdp-specs-title" class="pdp-sec__title pdp-faq__title">{v3['specs_title']}</h2>
            <p class="pdp-sec__sub">{specs_note}</p>
            <div class="home-faq-list">
{_render_specs_v3(ui, content, lang)}
            </div>
        </section>

        <section class="pdp-final" aria-labelledby="pdp-final-title">
            <div class="pdp-final__inner">
                <div>
                    <h2 id="pdp-final-title">{v3['final_title']}</h2>
                    <p>{short} — {v3['delivery_line']}</p>
                    <span class="pdp-final__price">€ {eur_fmt(sale)} <small>{v3['final_tax']}{final_instead_html}</small></span>
                </div>
                <button type="button" class="pdp-btn-primary" data-cart-add data-cart-source="product-pricing">
                    {CART_ICON}
                    {labels['add']}
                </button>
            </div>
        </section>
    </main>
    <aml-cookie-banner></aml-cookie-banner>
    <ecommerce-footer translate="no" class="notranslate"></ecommerce-footer>
    <script src="../js/locale-path.js"></script>
    <script src="../js/cart.js" defer></script>
    <script src="../js/faq.js" defer></script>
    <script src="../js/product-page.js" defer></script>
    <script src="../js/product-v3.js" defer></script>
{_stock_script_tag(sku)}{_trustpilot_script_tag()}    <script src="../components/cookie-banner.js" defer></script>
    <script src="../components/header.js" defer></script>
    <script src="../components/footer.js" defer></script>
</body>
</html>
"""


def build_compact_product_page(lang, prod):
    e = entry(prod["sku"])
    slug = prod["slug"]
    sku = prod["sku"]
    sale = e["unitAmountMinor"]
    compare = e["compareAtMinor"]
    disc = pct(sale, compare)
    labels = _labels_for(lang, sku)
    meta = TEMPLATE_META[prod["template"]]
    short = prod["card_name"]
    brand = prod.get("brand") or meta["brand"] or "Microsoft"
    cat_slug = meta["listing"]
    cat_name = meta["cat_label"][lang]
    eyebrow = meta["eyebrow"][lang]
    act_step = meta["activation"][lang]
    desc = f"{short}. {labels['desc_suffix']}"
    price_dec = f"{sale / 100:.2f}"
    img_src = _product_image_src(slug, prod.get("image"))
    og_image_abs = "https://aml-store.com/" + img_src.lstrip("./").replace("../", "", 1)

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Product",
                "@id": f"https://aml-store.com/{lang}/{slug}#product",
                "name": short,
                "sku": sku,
                **({"mpn": e["mpn"]} if e.get("mpn") else {}),
                "inLanguage": lang,
                "url": f"https://aml-store.com/{lang}/{slug}",
                "image": og_image_abs,
                "description": desc,
                "brand": {"@type": "Brand", "name": brand},
                "offers": {
                    "@type": "Offer",
                    "url": f"https://aml-store.com/{lang}/{slug}",
                    "priceCurrency": "EUR",
                    "price": price_dec,
                    "availability": "https://schema.org/InStock",
                    "itemCondition": "https://schema.org/NewCondition",
                },
            }
        ],
    }

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{short} — Aml Store</title>
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://aml-store.com/{lang}/{slug}">
    <meta property="og:type" content="product">
    <meta property="og:site_name" content="Aml Store">
    <meta property="og:title" content="{short} — Aml Store">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="https://aml-store.com/{lang}/{slug}">
    <meta property="og:locale" content="{LOCALE[lang]}">
    <meta property="og:image" content="{og_image_abs}">
    <meta property="product:price:amount" content="{price_dec}">
    <meta property="product:price:currency" content="EUR">
{hreflang_block(slug)}
    <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
    </script>
    <script src="../js/consent-init.js"></script>
    <link rel="icon" href="../favicon/favicon.png" type="image/png">
    <link rel="stylesheet" href="../fonts/montserrat.css">
    <link rel="stylesheet" href="../css/page.css">
    <link rel="stylesheet" href="../css/header.css">
    <link rel="stylesheet" href="../css/footer.css">
    <link rel="stylesheet" href="../css/product.css">
    <link rel="stylesheet" href="../css/product-pdp.css">
    <script src="../js/theme-init.js"></script>
</head>
<body>
    <a class="skip-link" href="#main">{labels['skip']}</a>
    <ecommerce-header translate="no" class="notranslate"></ecommerce-header>
    <div id="product-sticky-cta" class="product-sticky-cta" role="region" aria-label="{labels['sticky']}" aria-hidden="true">
        <div class="product-sticky-cta__inner">
            <span class="product-sticky-cta__title">{short}</span>
            <div class="product-sticky-cta__prices" aria-hidden="true">
                <span class="product-sticky-cta__msrp">€ {eur_fmt(compare)}</span>
                <span class="product-sticky-cta__sale">€ {eur_fmt(sale)}</span>
            </div>
            <button type="button" class="btn-primary" data-cart-add data-cart-source="sticky-cta">{labels['add']}</button>
        </div>
    </div>
    <section class="v2-hero" aria-label="Prodotto">
        <div class="v2-breadcrumb">
            <nav aria-label="Breadcrumb">
                <a href="/{lang}/">Home</a><span class="sep">/</span>
                <a href="/{lang}/{cat_slug}">{cat_name}</a><span class="sep">/</span>
                <span aria-current="page">{short}</span>
            </nav>
        </div>
        <div class="v2-hero__inner">
            <div class="v2-hero__left">
                <p class="v2-hero__eyebrow">{eyebrow}</p>
                <h1 class="v2-hero__title">{short}</h1>
                {product_code_html(labels, sku)}
                <p class="v2-hero__desc">{desc}</p>
            </div>
            <div class="v2-hero__right">
                <img class="v2-hero__cover" src="{img_src}" width="400" height="400" alt="{short}" fetchpriority="high" decoding="async">
            </div>
        </div>
    </section>
    <div class="v2-pricing-wrap">
        <div id="product-pricing" class="v2-pricing-card"
            data-stripe-currency="eur"
            data-stripe-unit-amount="{sale}"
            data-stripe-compare-at-amount="{compare}"
            data-stripe-product-sku="{sku}"
            data-discount-percent="{disc}"{_physical_attr(sku)}>
            <div class="v2-price-label">{labels['price_label']}</div>
            <div class="v2-price-row">
                {f'<span class="v2-price-msrp">€ {eur_fmt(compare)}</span>' if disc > 0 else ''}
                <span class="v2-price-sale">€ {eur_fmt(sale)}</span>
                {f'<span class="v2-price-badge">−{disc}%</span>' if disc > 0 else ''}
            </div>
            <div class="v2-price-tax">{labels['tax']}</div>
{_stock_block_html(lang, sku)}            <button type="button" id="product-primary-cta" class="v2-btn-primary" data-cart-add data-cart-source="product-pricing">{labels['add']}</button>
{_trustpilot_buy_mini(lang)}        </div>
    </div>
    <main id="main" class="product-page" data-cart-added-msg="{labels['add']}">
        <section class="product-process-steps" aria-labelledby="steps-title">
            <h2 id="steps-title">{labels['steps_title']}</h2>
            <ol class="product-process-steps__list">
                <li><strong>{labels['step_order']}</strong> — {labels['step_checkout']}</li>
                <li><strong>{labels['step_email']}</strong> — {labels['step_email_desc']}</li>
                <li><strong>{labels['step_act']}</strong> — {act_step}</li>
            </ol>
        </section>
    </main>
    <aml-cookie-banner></aml-cookie-banner>
    <ecommerce-footer translate="no" class="notranslate"></ecommerce-footer>
    <script src="../js/locale-path.js"></script>
    <script src="../js/cart.js" defer></script>
    <script src="../js/product-page.js" defer></script>
{_stock_script_tag(sku)}{_trustpilot_script_tag()}    <script src="../components/cookie-banner.js" defer></script>
    <script src="../components/header.js" defer></script>
    <script src="../components/footer.js" defer></script>
</body>
</html>
"""


def resolve_rich_content(slug):
    """Return (content, ui_map) or (None, None)."""
    # Ex PRESERVE_PAGES: contenuto estratto dalle vecchie pagine a mano.
    try:
        from product_content_flagship import get_flagship_content

        flagship = get_flagship_content(slug)
        if flagship:
            if slug.startswith("windows"):
                from product_content_windows import UI as W_UI

                return flagship, W_UI
            from product_content_office import UI as O_UI

            return flagship, O_UI
    except ImportError:
        pass

    try:
        from product_content_office import UI as OFFICE_UI
        from product_content_office import get_office_content
    except ImportError:
        get_office_content = lambda _s: None  # noqa: E731
        OFFICE_UI = None

    loaders = []
    if get_office_content:
        loaders.append(get_office_content)
    try:
        from product_content_office_2021 import get_office_2021_content

        loaders.append(get_office_2021_content)
    except ImportError:
        pass
    try:
        from product_content_office_apps import get_office_apps_content

        loaders.append(get_office_apps_content)
    except ImportError:
        pass

    for loader in loaders:
        content = loader(slug)
        if content:
            return content, OFFICE_UI

    try:
        from product_content_windows import UI as WINDOWS_UI
        from product_content_windows import get_windows_content

        content = get_windows_content(slug)
        if content:
            return content, WINDOWS_UI
    except ImportError:
        pass

    try:
        from product_content_antivirus import UI as ANTIVIRUS_UI
        from product_content_antivirus import get_antivirus_content

        content = get_antivirus_content(slug)
        if content:
            return content, ANTIVIRUS_UI
    except ImportError:
        pass

    # Windows Server e SQL Server: riusano la UI Windows, ma forniscono passi e
    # requisiti propri (l'attivazione server non è quella di un client).
    try:
        from product_content_server import get_server_content
        from product_content_windows import UI as SERVER_UI

        content = get_server_content(slug)
        if content:
            return content, SERVER_UI
    except ImportError:
        pass

    # Ex template compatto: Adobe Acrobat, CorelDRAW, Acronis. Riusano la UI
    # Windows solo per il chrome condiviso — forniscono sempre `steps`/`specs`
    # propri, quindi i default Microsoft-specific di quel dizionario non
    # vengono mai letti (vedi _render_steps_v3/_render_specs_v3).
    try:
        from product_content_tools import get_tools_content
        from product_content_windows import UI as TOOLS_UI

        content = get_tools_content(slug)
        if content:
            return content, TOOLS_UI
    except ImportError:
        pass

    # Ex template compatto: bundle M365 Personal + antivirus.
    try:
        from product_content_bundles import get_bundle_content
        from product_content_windows import UI as BUNDLE_UI

        content = get_bundle_content(slug)
        if content:
            return content, BUNDLE_UI
    except ImportError:
        pass

    return None, None


def build_product_page(lang, prod):
    content, ui_map = resolve_rich_content(prod["slug"])
    if content:
        return build_rich_product_page(lang, prod, content, ui_map=ui_map)
    return build_compact_product_page(lang, prod)


def build_catalog_page(lang, catalog_slug, products):
    labels = BASE_LABELS[lang]
    title, lede = CATALOG_META[catalog_slug][lang]
    cards = "".join(product_card(lang, p, labels) for p in products)
    og_image = PRODUCT_COVER_FALLBACK_ABS
    if products:
        first = products[0]
        rel = _product_image_src(first["slug"], first.get("image"))
        og_image = "https://aml-store.com/" + rel.lstrip("./").replace("../", "", 1)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Aml Store</title>
    <meta name="description" content="{lede}">
    <meta name="robots" content="index, follow">
    <script src="../js/consent-init.js"></script>
    <link rel="icon" href="../favicon/favicon.png" type="image/png">
    <link rel="apple-touch-icon" href="../favicon/apple-touch-icon.png">
    <link rel="canonical" href="https://aml-store.com/{lang}/{catalog_slug}">
{hreflang_block(catalog_slug)}
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title} | Aml Store">
    <meta property="og:description" content="{lede}">
    <meta property="og:url" content="https://aml-store.com/{lang}/{catalog_slug}">
    <meta property="og:locale" content="{LOCALE[lang]}">
    <meta property="og:image" content="{og_image}">
    <link rel="stylesheet" href="../fonts/montserrat.css">
    <link rel="stylesheet" href="../css/page.css">
    <link rel="stylesheet" href="../css/home.css">
    <script src="../js/theme-init.js"></script>
    <script type="application/ld+json">
    {{"@context":"https://schema.org","@type":"CollectionPage","name":"{title}","description":"{lede}","url":"https://aml-store.com/{lang}/{catalog_slug}","inLanguage":"{lang}","isPartOf":{{"@type":"WebSite","name":"Aml Store","url":"https://aml-store.com/"}}}}
    </script>
</head>
<body>
    <div class="scroll-progress" aria-hidden="true"></div>
    <a class="skip-link" href="#main">{labels['skip']}</a>
    <ecommerce-header translate="no" class="notranslate"></ecommerce-header>
    <main id="main" class="home-page">
        <section class="home-catalog" aria-labelledby="catalog-title" style="padding-top: 120px;">
            <h1 id="catalog-title" class="home-section-title">{title}</h1>
            <div class="home-catalog-lede-block">
                <p class="home-catalog-lede">{lede}</p>
            </div>
            <div class="product-grid">
{cards}
            </div>
        </section>
    </main>
    <aml-cookie-banner></aml-cookie-banner>
    <ecommerce-footer translate="no" class="notranslate"></ecommerce-footer>
    <script src="../js/locale-path.js"></script>
    <script src="../js/cart.js" defer></script>
    <script src="../components/cookie-banner.js" defer></script>
    <script src="../components/header.js" defer></script>
    <script src="../components/footer.js" defer></script>
</body>
</html>
"""
