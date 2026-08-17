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
        "assur_1": "Attivazione sui portali ufficiali",
        "assur_2": "Consegna digitale, nessuna spedizione",
        "assur_3": "Assistenza in italiano dopo l'acquisto",
        "assur_4": "Pagamenti gestiti da Stripe e PayPal",
        "assur_5": "Fattura elettronica disponibile",
        "receive_eyebrow": "Cosa ricevi",
        "apps_more": "Vedi tutte le app incluse",
        "apps_scroll_prev": "Scorri indietro",
        "apps_scroll_next": "Scorri avanti",
        "reviews_title": "Cosa dicono i clienti",
        "reviews_lead": "Le recensioni sono pubblicate e verificate da Trustpilot: le leggi direttamente sulla piattaforma, senza filtri da parte nostra.",
        "reviews_cta": "Leggi tutte le recensioni",
        "specs_title": "Compatibilità e requisiti tecnici",
        "faq_title": "Hai dubbi prima dell'acquisto?",
        "sticky_buy": "Acquista ora",
        "payments_aria": "Metodi di pagamento accettati",
        "trust_1_t": "Azienda italiana", "trust_1_d": "Sede e P.IVA in Italia",
        "trust_2_t": "Fattura elettronica", "trust_2_d": "Disponibile per privati e aziende",
        "trust_3_t": "Assistenza in italiano", "trust_3_d": "Supporto post-vendita via email e WhatsApp",
        "trust_4_t": "Pagamenti protetti", "trust_4_d": "Elaborati tramite Stripe e PayPal",
    },
    "en": {
        "assur_1": "Activation on official portals",
        "assur_2": "Digital delivery, nothing to ship",
        "assur_3": "Support after you buy",
        "assur_4": "Payments handled by Stripe and PayPal",
        "assur_5": "Invoice available",
        "receive_eyebrow": "What you get",
        "apps_more": "See all included apps",
        "apps_scroll_prev": "Scroll back",
        "apps_scroll_next": "Scroll forward",
        "reviews_title": "What customers say",
        "reviews_lead": "Reviews are published and verified by Trustpilot: read them straight on the platform, with nothing filtered by us.",
        "reviews_cta": "Read all reviews",
        "specs_title": "Compatibility and technical requirements",
        "faq_title": "Answers before you buy",
        "sticky_buy": "Buy now",
        "payments_aria": "Accepted payment methods",
        "trust_1_t": "European retailer", "trust_1_d": "Registered in Italy",
        "trust_2_t": "Invoice available", "trust_2_d": "VAT invoice for businesses",
        "trust_3_t": "Written support", "trust_3_d": "Email and WhatsApp",
        "trust_4_t": "Secure payments", "trust_4_d": "Processed via Stripe and PayPal",
    },
    "fr": {
        "assur_1": "Activation sur les portails officiels",
        "assur_2": "Livraison numérique, rien à expédier",
        "assur_3": "Assistance après l'achat",
        "assur_4": "Paiements gérés par Stripe et PayPal",
        "assur_5": "Facture disponible",
        "receive_eyebrow": "Ce que vous recevez",
        "apps_more": "Voir toutes les applications incluses",
        "apps_scroll_prev": "Défiler vers l'arrière",
        "apps_scroll_next": "Défiler vers l'avant",
        "reviews_title": "Ce que disent les clients",
        "reviews_lead": "Les avis sont publiés et vérifiés par Trustpilot : lisez-les directement sur la plateforme, sans filtre de notre part.",
        "reviews_cta": "Lire tous les avis",
        "specs_title": "Compatibilité et configuration requise",
        "faq_title": "Les réponses avant d'acheter",
        "sticky_buy": "Acheter",
        "payments_aria": "Moyens de paiement acceptés",
        "trust_1_t": "Revendeur européen", "trust_1_d": "Basé en Italie",
        "trust_2_t": "Facture disponible", "trust_2_d": "TVA pour les entreprises",
        "trust_3_t": "Support par écrit", "trust_3_d": "E-mail et WhatsApp",
        "trust_4_t": "Paiements sécurisés", "trust_4_d": "Via Stripe et PayPal",
    },
    "de": {
        "assur_1": "Aktivierung über offizielle Portale",
        "assur_2": "Digitale Lieferung, kein Versand",
        "assur_3": "Support nach dem Kauf",
        "assur_4": "Zahlungen über Stripe und PayPal",
        "assur_5": "Rechnung verfügbar",
        "receive_eyebrow": "Das bekommst du",
        "apps_more": "Alle enthaltenen Apps ansehen",
        "apps_scroll_prev": "Zurückscrollen",
        "apps_scroll_next": "Weiterscrollen",
        "reviews_title": "Was Kunden sagen",
        "reviews_lead": "Die Bewertungen werden von Trustpilot veröffentlicht und geprüft: Du liest sie direkt auf der Plattform, ungefiltert von uns.",
        "reviews_cta": "Alle Bewertungen lesen",
        "specs_title": "Kompatibilität und Systemvoraussetzungen",
        "faq_title": "Antworten vor dem Kauf",
        "sticky_buy": "Jetzt kaufen",
        "payments_aria": "Akzeptierte Zahlungsmethoden",
        "trust_1_t": "Europäischer Händler", "trust_1_d": "Sitz in Italien",
        "trust_2_t": "Rechnung verfügbar", "trust_2_d": "MwSt.-Rechnung für Firmen",
        "trust_3_t": "Schriftlicher Support", "trust_3_d": "E-Mail und WhatsApp",
        "trust_4_t": "Sichere Zahlungen", "trust_4_d": "Über Stripe und PayPal",
    },
    "es": {
        "assur_1": "Activación en portales oficiales",
        "assur_2": "Entrega digital, sin envío",
        "assur_3": "Asistencia tras la compra",
        "assur_4": "Pagos gestionados por Stripe y PayPal",
        "assur_5": "Factura disponible",
        "receive_eyebrow": "Qué recibes",
        "apps_more": "Ver todas las apps incluidas",
        "apps_scroll_prev": "Desplazar hacia atrás",
        "apps_scroll_next": "Desplazar hacia adelante",
        "reviews_title": "Lo que dicen los clientes",
        "reviews_lead": "Las reseñas las publica y verifica Trustpilot: las lees directamente en la plataforma, sin filtros por nuestra parte.",
        "reviews_cta": "Leer todas las reseñas",
        "specs_title": "Compatibilidad y requisitos técnicos",
        "faq_title": "Las respuestas antes de comprar",
        "sticky_buy": "Comprar ahora",
        "payments_aria": "Métodos de pago aceptados",
        "trust_1_t": "Distribuidor europeo", "trust_1_d": "Con sede en Italia",
        "trust_2_t": "Factura disponible", "trust_2_d": "IVA para empresas",
        "trust_3_t": "Soporte por escrito", "trust_3_d": "Email y WhatsApp",
        "trust_4_t": "Pagos seguros", "trust_4_d": "A través de Stripe y PayPal",
    },
}

# SKU fisici (DVD/COA): niente "codice via email", si spedisce un supporto.
V3_PHYSICAL_UI = {
    "it": {"assur_2": "Supporto fisico spedito, non solo digitale"},
    "en": {"assur_2": "Physical media shipped, not digital-only"},
    "fr": {"assur_2": "Support physique expédié, pas seulement numérique"},
    "de": {"assur_2": "Physisches Medium wird versendet, nicht nur digital"},
    "es": {"assur_2": "Soporte físico enviado, no solo digital"},
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
        "price_label": "Prezzo Riservato",
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
    euros, cents = divmod(minor, 100)
    integer = f"{euros:,}".replace(",", ".")
    return f"{integer},{cents:02d}"


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
    # Come per features_title: un titolo assente arrivava in pagina come la
    # stringa "None". Se manca si tiene il kicker e si etichetta la sezione
    # con l'alt dell'immagine, che c'e' sempre.
    title = (lifestyle.get("title") or {}).get(lang)
    body = lifestyle["body"][lang]
    title_html = f'\n                <h3 class="bento-title">{title}</h3>' if title else ""
    # Di norma le foto lifestyle stanno sotto products/. `image_root: ""` serve alle
    # immagini che vivono direttamente in asset/media/ (es. windows-11-home).
    root = lifestyle.get("image_root", "products/")
    src = f"../asset/media/{root}{img}"
    srcset_attrs = ""
    if img_640 and img_640 != img:
        src_640 = f"../asset/media/{root}{img_640}"
        srcset_attrs = f'\n                    srcset="{src_640} 640w, {src} {w}w"\n                    sizes="100vw"'
    return f"""        <hr class="v2-divider">
        <section class="v2-section v2-section--gallery" aria-label="{title or alt}">
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
            </figure>
            <div class="bento-caption">
                <span class="bento-kicker">{kicker}</span>{title_html}
                <p class="bento-text">{body}</p>
            </div>
        </section>
"""


def _render_faq(faq_items):
    """
    `a` e' di norma una stringa (un paragrafo, wrappato qui in un <p>). M365
    Family ha portato le prime risposte a piu' paragrafi (es. "arriva in
    2-15 minuti" + "se non arriva, scrivici"): per quei casi `a` puo' essere
    una lista di paragrafi, uno per <p>. Senza questo ramo, una risposta a
    piu' paragrafi finiva innestata dentro un <p> solo (<p><p>...</p><p>...
    </p></p>), HTML non valido — scoperto confrontando la pagina Family
    rigenerata con l'originale scritto a mano.
    """
    parts = []
    for q, a in faq_items:
        if isinstance(a, (list, tuple)):
            body = "\n".join(f"                        <p>{p}</p>" for p in a)
        else:
            body = f"                        <p>{a}</p>"
        parts.append(
            f"""                <details class="home-faq-item">
                    <summary>{q}</summary>
                    <div class="home-faq-body">
{body}
                    </div>
                </details>"""
        )
    return "\n".join(parts)


def _render_faq_groups(faq_groups):
    """
    FAQ organizzate per argomento (.pdp-faq-group / .pdp-faq-group__title):
    variante di _render_faq_columns per i casi — M365 Family in testa — dove
    le domande sono troppe e troppo eterogenee per stare in una sola lista
    piatta. Ogni gruppo e' internamente identico a una sezione FAQ normale
    (stesse due colonne, stesso _render_faq), solo con un titolo sopra e un
    margine tra un gruppo e il successivo (--pdp-faq-group + .pdp-faq-group
    in product-pdp.css).
    """
    parts = []
    for title, items in faq_groups:
        parts.append(
            f'            <div class="pdp-faq-group">\n'
            f'                <h3 class="pdp-faq-group__title">{title}</h3>\n'
            f'                <div class="home-faq-list">\n'
            f'{_render_faq_columns(items)}\n'
            f'                </div>\n'
            f'            </div>'
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


def _render_payment_logos(v3):
    logos = "\n".join(
        f'                    <span class="pdp-pay__logo" data-brand="{alt}" title="{alt}">'
        f'<img src="../asset/payments_logo/{fname}" alt="{alt}" loading="lazy" decoding="async"></span>'
        for fname, alt in PAYMENT_LOGOS
    )
    return f"""                <div class="pdp-pay" role="group" aria-label="{v3['payments_aria']}">
                    <p class="pdp-pay__label">{v3['payments_aria']}</p>
                    <div class="pdp-pay__row">
{logos}
                    </div>
                </div>"""


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


# Recensioni reali, copiate da https://it.trustpilot.com/review/aml-store.com
# il 2026-08-16 (TrustScore 4,8 "Eccellente", 94 recensioni, 91% a 5 stelle).
# Nomi come mostrati pubblicamente da Trustpilot sulla propria pagina. Solo
# italiano: tradurre la testimonianza di un cliente reale in un'altra lingua
# significherebbe fargli dire parole sue in una forma che non ha scelto —
# niente traduzione finta spacciata per citazione.
REVIEWS_IT = [
    ("Roberto Galoppini", "Ho appena acquistato una copia di Microsoft 365, il codice è arrivato 2 minuti dopo il pagamento, ho potuto rinnovare il mio account per 1 anno, azienda superlativa!!"),
    ("Laura Ceccacci", "Il prodotto è arrivato in tempo reale, il supporto da parte del fornitore è eccezionale, davvero un serio distributore da tenere in considerazione per il futuro."),
    ("Mario", "Miglior prezzo del web per il prodotto originale, assistenza tempestiva e competente, fornitura via email immediata e nessun problema di attivazione."),
]
TRUSTPILOT_URL = "https://it.trustpilot.com/review/aml-store.com"
TRUSTPILOT_SCORE = "4,8"
TRUSTPILOT_COUNT_IT = "94 recensioni"


def _render_reviews(v3, lang):
    """
    Recensioni Trustpilot reali (vedi REVIEWS_IT sopra). Struttura del mockup
    di riferimento — intestazione con voto+conteggio, 3 card piatte — ma dati
    veri: il mockup aveva 3 citazioni scritte a mano con badge "Acquisto
    Verificato" fittizio, non riproducibili (vedi memoria guest-checkout /
    fedelta-mockup). Solo IT finche' non ci sono recensioni vere in altre
    lingue da mostrare.
    """
    if lang != "it" or not REVIEWS_IT:
        return ""
    stars = "★★★★★"
    items = "\n".join(
        f"""                <li>
                    <span class="pdp-reviews__name">{name}</span>
                    <span class="pdp-reviews__stars" aria-hidden="true">{stars}</span>
                    <p>«{quote}»</p>
                </li>"""
        for name, quote in REVIEWS_IT
    )
    return f"""        <hr class="pdp-divider">

        <section class="pdp-sec" aria-labelledby="pdp-reviews-title">
            <div class="pdp-reviews__head">
                <div>
                    <p class="pdp-reviews__rating">
                        <span class="pdp-reviews__tp">★ Trustpilot</span>
                        <span class="pdp-reviews__stars" aria-hidden="true">{stars}</span>
                        <span class="pdp-reviews__count">({TRUSTPILOT_SCORE}/5 su {TRUSTPILOT_COUNT_IT})</span>
                    </p>
                    <h2 id="pdp-reviews-title" class="pdp-sec__title">{v3['reviews_title']}</h2>
                </div>
                <a class="pdp-reviews__cta" href="{TRUSTPILOT_URL}" target="_blank" rel="noopener noreferrer">{v3['reviews_cta']}</a>
            </div>
            <ul class="pdp-reviews__grid">
{items}
            </ul>
        </section>
"""


def _render_stats(stats, lang):
    """
    Blocco statistiche (es. "6 Persone incluse"). Terzo blocco bespoke della
    pagina M365 Family portato nel generatore, stesso schema di seats/compare:
    opzionale, attivo solo con la chiave `stats`.
    """
    if not stats:
        return ""
    s = stats.get(lang) or stats.get("it")
    if not s:
        return ""
    items = "\n".join(
        f'                <li class="pdp-stat">\n'
        f'                    <span class="pdp-stat__value">{value}</span>\n'
        f'                    <span class="pdp-stat__label">{label}</span>\n'
        f'                    <span class="pdp-stat__note">{note}</span>\n'
        f'                </li>'
        for value, label, note in s["rows"]
    )
    # Divider IN TESTA, non in coda: come apps_block/seats_block/compare_block
    # (gia' esistenti), cosi' la sezione che segue non deve sapere se aggiungere
    # il proprio o no. Un trailing hr qui + un leading hr nel blocco dopo
    # produceva due <hr> consecutivi tra ruoli e app quando questi renderer
    # sono stati aggiunti — vedi verifica nella sessione che li ha introdotti.
    return f"""        <hr class="pdp-divider">

        <section class="pdp-sec" aria-labelledby="pdp-what-title">
            <p class="pdp-sec__eyebrow">{s['eyebrow']}</p>
            <h2 id="pdp-what-title" class="pdp-sec__title">{s['title']}</h2>
            <p class="pdp-sec__sub">{s['sub']}</p>
            <ul class="pdp-stats">
{items}
            </ul>
        </section>
"""


def _render_specs_table(specs_table, lang, sku):
    """
    Scheda tecnica completa (chiave/valore, N righe libere) — diversa dal
    blocco `specs` a 4 celle gia' supportato da _render_specs_v3. Il valore
    '@sku' nella riga viene sostituito con lo SKU reale del prodotto: cosi'
    la scheda tecnica non puo' restare disallineata dal codice articolo vero
    se la stessa struttura di contenuto viene riusata su un altro prodotto.
    """
    if not specs_table:
        return ""
    t = specs_table.get(lang) or specs_table.get("it")
    if not t:
        return ""
    rows = "\n".join(
        f'                        <tr><th scope="row">{k}</th>'
        f'<td>{sku if v == "@sku" else v}</td></tr>'
        for k, v in t["rows"]
    )
    return f"""        <hr class="pdp-divider">

        <section class="pdp-sec pdp-sec--tight" aria-labelledby="pdp-specs2-title">
            <p class="pdp-sec__eyebrow">{t['eyebrow']}</p>
            <h2 id="pdp-specs2-title" class="pdp-sec__title">{t['title']}</h2>
            <div class="pdp-tablewrap">
                <table class="pdp-table pdp-table--specs">
                    <caption class="visually-hidden">{t['caption']}</caption>
                    <tbody>
{rows}
                    </tbody>
                </table>
            </div>
        </section>
"""


def _render_roles(roles, lang):
    """
    Tabella titolare/membri: struttura simile a _render_compare (stesse
    label yes/no) ma con un elemento in piu' — una riga puo' avere un hint
    (.pdp-table__hint) e il modificatore .pdp-row--flag per segnalarla senza
    spezzare l'allineamento della prima riga. Tenuta separata da
    _render_compare invece di sovraccaricarne la firma con parametri opzionali.
    """
    if not roles:
        return ""
    r = roles.get(lang) or roles.get("it")
    if not r:
        return ""

    def cell(value):
        if value == "yes":
            return f'<span class="pdp-yes" aria-label="{html_module.escape(r["yes_label"], quote=True)}">✓</span>'
        if value == "no":
            return f'<span class="pdp-no" aria-label="{html_module.escape(r["no_label"], quote=True)}">—</span>'
        return value

    rows = []
    for label, hint, flagged, *values in r["rows"]:
        tr_cls = ' class="pdp-row--flag"' if flagged else ""
        hint_html = f'<span class="pdp-table__hint">{hint}</span>' if hint else ""
        cells = "".join(f"<td>{cell(v)}</td>" for v in values)
        rows.append(
            f'                        <tr{tr_cls}>\n'
            f'                            <th scope="row">{label}{hint_html}</th>\n'
            f'                            {cells}\n'
            f'                        </tr>'
        )
    body = "\n".join(rows)
    head = "".join(f'<th scope="col">{h}</th>' for h in r["cols"])

    return f"""        <hr class="pdp-divider">

        <section class="pdp-sec" aria-labelledby="pdp-roles-title">
            <p class="pdp-sec__eyebrow">{r['eyebrow']}</p>
            <h2 id="pdp-roles-title" class="pdp-sec__title">{r['title']}</h2>
            <p class="pdp-sec__sub">{r['sub']}</p>

            <div class="pdp-tablewrap">
                <table class="pdp-table">
                    <caption class="visually-hidden">{r['caption']}</caption>
                    <thead>
                        <tr>{head}</tr>
                    </thead>
                    <tbody>
{body}
                    </tbody>
                </table>
            </div>
        </section>
"""


# ── Renderer del layout v3 ──────────────────────────────────────────────────

NOTE_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">'
    '<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.3 3.9L2.6 17.3A2 2 0 004.3 20.3h15.4a2 '
    '2 0 001.7-3L13.7 3.9a2 2 0 00-3.4 0z"/></svg>'
)


ASSUR_KEYS = ("assur_1", "assur_2", "assur_3", "assur_4", "assur_5")


def _render_assur(v3, keys=ASSUR_KEYS):
    """
    `keys` permette di spezzare l'elenco: nel mockup il pannello d'acquisto
    tiene solo le due garanzie principali e tutto il resto sta fuori. Senza
    argomento il comportamento e' quello di prima (tutte e cinque).
    """
    return "\n".join(f"                            <li>{v3[k]}</li>" for k in keys)


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
    """features: (span, tone, label, title, body) — span, tone e label (testo)
    del vecchio bento non servono piu': l'etichetta per-card e' stata sostituita
    da un'icona decorativa a cerchio colorato (mockup di riferimento), le due
    tonalita' alternate restano dentro la palette a tre ruoli gia' approvata
    (arancione brand / verde fiducia), senza introdurre un terzo colore."""
    ICON_TONES = ("a", "b")
    parts = []
    for i, item in enumerate(features):
        title, body = item[3], item[4]
        tone = ICON_TONES[i % len(ICON_TONES)]
        parts.append(
            f"""                <li class="pdp-card">
                    <span class="pdp-card__icon pdp-card__icon--{tone}" aria-hidden="true">&#10003;</span>
                    <h3 class="pdp-card__title">{title}</h3>
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


def _render_overview(content, lang):
    """Optional long-form product description shown before feature cards."""
    localized = (content.get("overview") or {}).get(lang)
    if not localized:
        return ""
    eyebrow = html_module.escape(localized["eyebrow"])
    title = html_module.escape(localized["title"])
    paragraphs = "\n".join(
        f"                <p>{html_module.escape(paragraph)}</p>"
        for paragraph in localized.get("paragraphs", [])
    )
    return f"""        <section class="pdp-sec pdp-overview" aria-labelledby="pdp-overview-title">
            <p class="pdp-sec__eyebrow">{eyebrow}</p>
            <h2 id="pdp-overview-title" class="pdp-sec__title">{title}</h2>
            <div class="pdp-overview__copy">
{paragraphs}
            </div>
        </section>

        <hr class="pdp-divider">

"""


def _render_seats(seats, lang):
    """
    Blocco postazioni: era scritto a mano nella sola pagina M365 Family, che per
    questo restava fuori dal generatore. Qui diventa una sezione opzionale —
    compare solo se il contenuto dichiara `seats` — cosi' Family puo' rientrare
    nel flusso normale senza perdere il pezzo che spiega il prodotto, e il
    blocco resta riusabile per altri piani multi-utente.

    Il CSS (.pdp-seats, .pdp-seat, .pdp-seat--owner) e' gia' in product-pdp.css.
    """
    if not seats:
        return ""
    s = seats.get(lang) or seats.get("it")
    if not s:
        return ""

    rows = []
    for role, quota, is_owner in s["rows"]:
        cls = "pdp-seat pdp-seat--owner" if is_owner else "pdp-seat"
        rows.append(
            f'                        <li class="{cls}">\n'
            f'                            <span class="pdp-seat__avatar" aria-hidden="true">'
            f'<svg viewBox="0 0 24 24"><use href="#pdp-person"/></svg></span>\n'
            f'                            <span class="pdp-seat__role">{role}</span>\n'
            f'                            <span class="pdp-seat__quota">{quota}</span>\n'
            f'                        </li>'
        )

    media = ""
    if s.get("media_src"):
        media = f"""                <figure class="pdp-split__media">
                    <img src="{s['media_src']}" width="1200" height="675" alt="{html_module.escape(s.get('media_alt', ''), quote=True)}" loading="lazy" decoding="async">
                </figure>
"""

    return f"""        <hr class="pdp-divider">

        <section class="pdp-sec" aria-labelledby="pdp-share-title">
            <div class="pdp-split">
{media}                <div class="pdp-split__body">
                    <p class="pdp-sec__eyebrow">{s['eyebrow']}</p>
                    <h2 id="pdp-share-title" class="pdp-sec__title">{s['title']}</h2>
                    <p class="pdp-sec__sub" style="margin-bottom:0;">{s['sub']}</p>
                    <svg width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute">
                        <symbol id="pdp-person" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M12 12a4.2 4.2 0 100-8.4 4.2 4.2 0 000 8.4zm0 1.9c-3.6 0-7 1.9-7 4.2v1.4c0 .4.3.7.7.7h12.6c.4 0 .7-.3.7-.7v-1.4c0-2.3-3.4-4.2-7-4.2z"/>
                        </symbol>
                    </svg>

                    <ul class="pdp-seats" aria-label="{html_module.escape(s['list_aria'], quote=True)}">
{chr(10).join(rows)}
                    </ul>
                    <p class="pdp-seats__foot">{s['foot']}</p>
                </div>
            </div>
        </section>
"""


# Etichette del pannello acquisto in stile concept.
#
# Il claim di disponibilita' immediata esce SOLO sugli SKU digitali: i fisici
# vengono spediti e hanno gia' la loro riga di stock reale, alimentata da
# product-stock.js. Dire "consegna immediata" su quelli sarebbe falso.
#
# Nessun conteggio di pezzi: il concept scriveva "14 chiavi pronta consegna",
# ma quel numero non viene da nessuna fonte. Qui si dichiara la disponibilita',
# non una scorta inventata.
BUY_LABELS = {
    "it": {"avail": "Disponibile · consegna immediata", "eta": "Email in 2–15 min",
           "plan": "Seleziona la versione", "checkout": "Acquista ora",
           "sticky_delivery": "Consegna in 2 minuti via Email"},
    "en": {"avail": "In stock · instant delivery", "eta": "Email in 2–15 min",
           "plan": "Choose your edition", "checkout": "Buy now",
           "sticky_delivery": "Delivered in 2 minutes by email"},
    "fr": {"avail": "Disponible · livraison immédiate", "eta": "E-mail en 2–15 min",
           "plan": "Choisissez la version", "checkout": "Acheter maintenant",
           "sticky_delivery": "Livraison en 2 minutes par e-mail"},
    "de": {"avail": "Verfügbar · sofortige Lieferung", "eta": "E-Mail in 2–15 Min.",
           "plan": "Version auswählen", "checkout": "Jetzt kaufen",
           "sticky_delivery": "Lieferung in 2 Minuten per E-Mail"},
    "es": {"avail": "Disponible · entrega inmediata", "eta": "Email en 2–15 min",
           "plan": "Selecciona la versión", "checkout": "Comprar ahora",
           "sticky_delivery": "Entrega en 2 minutos por email"},
}

# Riga descrittiva del pannello dentro le tab app. Sono descrizioni di cosa fa
# l'app Microsoft, non claim su Aml Store: nessun numero, nessuna promessa.
# Le app non elencate qui ricadono sul solo nome, quindi la tabella puo'
# restare corta senza rompere niente.
APP_DEMOS = {
    "word": {
        "it": "Documenti, lettere e tesi con correzione e formattazione automatica.",
        "en": "Documents, letters and theses with automatic proofing and formatting.",
        "fr": "Documents, lettres et mémoires avec correction et mise en forme automatiques.",
        "de": "Dokumente, Briefe und Arbeiten mit automatischer Korrektur und Formatierung.",
        "es": "Documentos, cartas y trabajos con corrección y formato automáticos.",
    },
    "excel": {
        "it": "Fogli di calcolo, budget e grafici con formule e tabelle pivot.",
        "en": "Spreadsheets, budgets and charts with formulas and pivot tables.",
        "fr": "Feuilles de calcul, budgets et graphiques avec formules et tableaux croisés.",
        "de": "Tabellen, Budgets und Diagramme mit Formeln und Pivot-Tabellen.",
        "es": "Hojas de cálculo, presupuestos y gráficos con fórmulas y tablas dinámicas.",
    },
    "powerpoint": {
        "it": "Presentazioni con layout, transizioni e note per il relatore.",
        "en": "Presentations with layouts, transitions and speaker notes.",
        "fr": "Présentations avec mises en page, transitions et notes du présentateur.",
        "de": "Präsentationen mit Layouts, Übergängen und Sprechernotizen.",
        "es": "Presentaciones con diseños, transiciones y notas del orador.",
    },
    "outlook": {
        "it": "Posta, calendario e contatti in un'unica applicazione.",
        "en": "Mail, calendar and contacts in a single application.",
        "fr": "Messagerie, calendrier et contacts dans une seule application.",
        "de": "E-Mail, Kalender und Kontakte in einer Anwendung.",
        "es": "Correo, calendario y contactos en una sola aplicación.",
    },
    "onedrive": {
        "it": "Spazio cloud per file e foto, sincronizzati su tutti i dispositivi.",
        "en": "Cloud storage for files and photos, synced across your devices.",
        "fr": "Stockage cloud pour fichiers et photos, synchronisé sur vos appareils.",
        "de": "Cloud-Speicher für Dateien und Fotos, auf allen Geräten synchronisiert.",
        "es": "Almacenamiento en la nube para archivos y fotos, sincronizado en tus dispositivos.",
    },
    "teams": {
        "it": "Chat, chiamate e riunioni video con condivisione dello schermo.",
        "en": "Chat, calls and video meetings with screen sharing.",
        "fr": "Chat, appels et réunions vidéo avec partage d'écran.",
        "de": "Chat, Anrufe und Videobesprechungen mit Bildschirmfreigabe.",
        "es": "Chat, llamadas y reuniones de vídeo con pantalla compartida.",
    },
}


def _buy_labels(lang):
    return BUY_LABELS.get(lang, BUY_LABELS["en"])


def _render_avail_banner(lang, sku):
    if is_physical_sku(sku):
        return ""
    b = _buy_labels(lang)
    return f"""                <p class="pdp-avail">
                    <span class="pdp-avail__pill"><span class="pdp-avail__dot" aria-hidden="true"></span>{b['avail']}</span>
                    <span class="pdp-avail__eta">{b['eta']}</span>
                </p>
"""


def _render_secondary_cta(add_label):
    """Ghost "Aggiungi al carrello": secondaria sotto la CTA piena "Acquista
    ora" (che aggiunge e salta al checkout, vedi data-cart-checkout-redirect
    sul bottone primario). Resta per chi vuole aggiungere piu' prodotti prima
    di pagare, senza essere spinto subito al checkout."""
    return f"""                <button type="button" class="pdp-btn-ghost" data-cart-add data-cart-source="product-pricing">
                    {CART_ICON}
                    {add_label}
                </button>
"""


# Etichette della modale attivazione. Le uniche stringhe nuove: il titolo e i
# passi arrivano da ui['how_title'] e content['steps'], gia' localizzati.
GUIDE_LABELS = {
    "it": {"open": "Come funziona l'attivazione dopo l'acquisto?", "close": "Ho capito, chiudi"},
    "en": {"open": "How does activation work?", "close": "Got it, close"},
    "fr": {"open": "Comment fonctionne l'activation ?", "close": "J'ai compris, fermer"},
    "de": {"open": "Wie funktioniert die Aktivierung?", "close": "Verstanden, schließen"},
    "es": {"open": "¿Cómo funciona la activación?", "close": "Entendido, cerrar"},
}

# Suffisso del badge sconto ("−17% SCONTO" nel mockup di riferimento): micro-
# etichetta di interfaccia, non testo di un cliente — tradurla per lingua e'
# la stessa cosa che si fa per qualunque altra label dell'interfaccia.
DISCOUNT_SUFFIX = {"it": "SCONTO", "en": "OFF", "fr": "REMISE", "de": "RABATT", "es": "DTO"}


def _render_activation_modal(ui, content, lang):
    """
    Modale "come si attiva", come nel concept. Il bottone ha un href verso la
    sezione passi gia' in pagina: se il browser non supporta <dialog> — o se il
    JS non parte — resta un'ancora funzionante invece di un bottone morto.
    """
    steps = (content.get("steps") or {}).get(lang)
    if not steps:
        return "", ""
    g = GUIDE_LABELS.get(lang, GUIDE_LABELS["en"])

    items = "\n".join(
        f"                    <li><strong>{title}</strong> {body}</li>"
        for title, body in steps
    )

    trigger = f"""                        <p class="pdp-guide-link">
                            <a href="#pdp-steps-title" data-pdp-guide>{g['open']}</a>
                        </p>
"""

    dialog = f"""    <dialog id="pdp-activation" class="pdp-dialog" aria-labelledby="pdp-activation-title">
        <h2 id="pdp-activation-title" class="pdp-dialog__title">{ui['how_title']}</h2>
        <ol class="pdp-dialog__steps">
{items}
        </ol>
        <div class="pdp-dialog__foot">
            <button type="button" class="pdp-dialog__close" data-pdp-guide-close>{g['close']}</button>
        </div>
    </dialog>
"""
    return trigger, dialog


def _render_compare(compare, lang):
    """
    Tabella di confronto tra piani. Come le postazioni, era scritta a mano nella
    sola pagina Family: qui diventa opzionale, attiva solo con la chiave
    `compare`.

    Una differenza rispetto all'originale: la riga prezzo NON e' testo. Nella
    pagina scritta a mano erano due literal (€ 79,00 / € 109,00) rimasti indietro
    rispetto al listino; qui arrivano da entry(), quindi seguono il catalogo come
    tutti gli altri prezzi della scheda e non possono piu' divergere in silenzio.

    Nelle celle, i token "yes" e "no" diventano i marcatori ✓ / —; qualsiasi
    altro valore e' testo.
    """
    if not compare:
        return ""
    c = compare.get(lang) or compare.get("it")
    if not c:
        return ""

    def cell(value):
        if value == "yes":
            return f'<span class="pdp-yes" aria-label="{html_module.escape(c["yes_label"], quote=True)}">✓</span>'
        if value == "no":
            return f'<span class="pdp-no" aria-label="{html_module.escape(c["no_label"], quote=True)}">—</span>'
        return value

    rows = list(c["rows"])
    if c.get("price_row") and c.get("skus"):
        prices = tuple(f"€ {eur_fmt(entry(s)['unitAmountMinor'])}" for s in c["skus"])
        rows.append((c["price_row"],) + prices)

    body = "\n".join(
        "                        <tr>\n"
        f"                            <th scope=\"row\">{r[0]}</th>\n"
        + "".join(f"                            <td>{cell(v)}</td>\n" for v in r[1:])
        + "                        </tr>"
        for r in rows
    )
    head = "".join(
        f'                            <th scope="col">{h}</th>\n' for h in c["cols"]
    )

    return f"""        <hr class="pdp-divider">

        <section class="pdp-sec" aria-labelledby="pdp-compare-title">
            <p class="pdp-sec__eyebrow">{c['eyebrow']}</p>
            <h2 id="pdp-compare-title" class="pdp-sec__title">{c['title']}</h2>
            <p class="pdp-sec__sub">{c['sub']}</p>

            <div class="pdp-tablewrap">
                <table class="pdp-table">
                    <caption class="visually-hidden">{c['caption']}</caption>
                    <thead>
                        <tr>
                            <th scope="col">&nbsp;</th>
{head}                        </tr>
                    </thead>
                    <tbody>
{body}
                    </tbody>
                </table>
            </div>
            <p class="pdp-table-foot">{c['foot']}</p>
        </section>
"""


# ── Concept retail: selettore di versione ─────────────────────────────────────
# Nel concept lo switcher Personal/Family cambia SKU dentro la stessa pagina.
# Qui le due versioni sono pagine distinte, ognuna col proprio prezzo, canonical
# e dati strutturati: il controllo ha lo stesso aspetto ma naviga, così non si
# tocca né il carrello né la SEO. Se lo SKU non appartiene a un gruppo, lo
# switcher non viene emesso e l'hero resta invariato.
VARIANT_SETS = {
    "m365-consumer": [
        {"sku": "QQ2-00012", "slug": "microsoft-365-personal", "label": "Personal",
         "sub": {"it": "1 utente", "en": "1 user", "de": "1 Nutzer",
                 "fr": "1 utilisateur", "es": "1 usuario"}},
        {"sku": "6GQ-00092", "slug": "microsoft-365-family", "label": "Family",
         "sub": {"it": "fino a 6 utenti", "en": "up to 6 users", "de": "bis zu 6 Nutzer",
                 "fr": "jusqu'à 6 utilisateurs", "es": "hasta 6 usuarios"}},
    ],
}

VARIANT_OF = {
    v["sku"]: name for name, variants in VARIANT_SETS.items() for v in variants
}


def _render_plan_switcher(sku, lang, ui):
    group = VARIANT_OF.get(sku)
    if not group:
        return ""
    items = []
    for v in VARIANT_SETS[group]:
        sub = v["sub"].get(lang) or v["sub"]["en"]
        # Il prezzo nel selettore viene dal catalogo, come nel resto della
        # scheda: nel concept era scritto a mano e gia' divergeva dal listino.
        sub = f'{sub} · € {eur_fmt(entry(v["sku"])["unitAmountMinor"])}'
        if v["sku"] == sku:
            items.append(
                f'                    <span class="pdp-plan is-current" aria-current="true">'
                f'<b>{v["label"]}</b><span>{sub}</span></span>'
            )
        else:
            items.append(
                f'                    <a class="pdp-plan" href="/{lang}/{v["slug"]}">'
                f'<b>{v["label"]}</b><span>{sub}</span></a>'
            )
    rows = "\n".join(items)
    label = _buy_labels(lang)["plan"]
    return f"""                <p class="pdp-plans__label" id="pdp-plans-label">{label}</p>
                <div class="pdp-plans" role="group" aria-labelledby="pdp-plans-label">
{rows}
                </div>
"""


def _render_app_tabs(app_keys, v3, lang="it"):
    """
    Barra di tab del concept al posto della griglia di icone: stessa lista di
    app, ma una alla volta e con il nome in chiaro. Senza JS le tab sono radio
    + label, così restano navigabili da tastiera e funzionano anche se lo
    script non parte.
    """
    keys = app_keys[:6]
    if not keys:
        return ""
    tabs, panels = [], []
    for i, k in enumerate(keys):
        name = APP_NAMES.get(k, k.title())
        checked = " checked" if i == 0 else ""
        tabs.append(
            f'                    <input type="radio" name="pdp-apptab" id="pdp-apptab-{k}"'
            f' class="pdp-apptab__radio"{checked}>\n'
            f'                    <label class="pdp-apptab" for="pdp-apptab-{k}">'
            f'<img src="{_icon_src(k)}" width="20" height="20" alt="" loading="lazy" decoding="async">'
            f'{name}</label>'
        )
        demo = (APP_DEMOS.get(k) or {}).get(lang) or (APP_DEMOS.get(k) or {}).get("en")
        desc = f'<span class="pdp-apppanel__desc">{demo}</span>' if demo else ""
        panels.append(
            f'                    <div class="pdp-apppanel" data-app="{k}">'
            f'<img src="{_icon_src(k)}" width="40" height="40" alt="" loading="lazy" decoding="async">'
            f'<span class="pdp-apppanel__text"><b>{name}</b>{desc}</span></div>'
        )

    # App oltre la sesta: non una sezione a parte piu' in basso (duplicava le
    # tab qui sopra, stesso elenco due volte — vedi confronto col mockup che
    # non ripete mai le app), solo un elenco a comparsa nello stesso blocco.
    extra = app_keys[6:]
    more_html = ""
    if extra:
        items = "\n".join(_app_item(k, 24) for k in extra)
        more_html = f"""
                <details class="pdp-apps-more">
                    <summary>{v3['apps_more']}</summary>
                    <div class="pdp-apps-more__body">
                        <ul class="pdp-apps">
{items}
                        </ul>
                    </div>
                </details>"""

    return f"""                <div class="pdp-apptabs">
                    <div class="pdp-apptabs__wrap">
                        <button type="button" class="pdp-apptabs__nav pdp-apptabs__nav--prev" data-apptabs-nav="-1" aria-label="{v3['apps_scroll_prev']}">
                            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                        </button>
                        <div class="pdp-apptabs__row">
{chr(10).join(tabs)}
                        </div>
                        <button type="button" class="pdp-apptabs__nav pdp-apptabs__nav--next" data-apptabs-nav="1" aria-label="{v3['apps_scroll_next']}">
                            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                        </button>
                    </div>
                    <div class="pdp-apppanels">
{chr(10).join(panels)}
                    </div>
                </div>{more_html}"""


def _render_app_tabs_rich(app_keys, featured, demos, v3, lang="it"):
    """
    Variante "ricca" delle tab app (bottoni onclick + pannelli con anteprima
    per-app — filename, badge, contenuto specifico) invece delle radio/label
    CSS-only di _render_app_tabs. Solo opt-in: usata quando il prodotto
    fornisce `app_demo_rich` in product_content_flagship.py (oggi solo
    microsoft-365-personal), tutti gli altri restano su _render_app_tabs
    esattamente come prima — nessuna modifica per chi non ha questo contenuto.

    Richiede window.switchAppTab (js/product-page.js), gia' caricato su ogni
    pagina prodotto ricca. La CSP del sito permette script-src 'unsafe-inline',
    quindi gli onclick funzionano regolarmente in produzione.
    """
    keys = (featured or app_keys)[:6]
    if not keys:
        return ""
    tabs, panels = [], []
    for i, k in enumerate(keys):
        name = APP_NAMES.get(k, k.title())
        active = " active" if i == 0 else ""
        tabs.append(
            f'                    <button type="button" onclick="switchAppTab(\'{k}\')" id="btn-tab-{k}" class="pdp-tab-btn{active}">'
            f'<img src="{_icon_src(k)}" width="16" height="16" alt="" loading="lazy" decoding="async">'
            f'<span>{name}</span></button>'
        )
        demo = demos.get(k) or {}
        dtype = demo.get("type")
        if dtype == "richtext":
            body = f"""
                        <div class="pdp-preview-head">
                            <span class="pdp-preview-filename">{demo['filename'][lang]}</span>
                            <span class="pdp-preview-copilot-tag">{demo['tag'][lang]}</span>
                        </div>
                        <div class="pdp-preview-docbox">{demo['quote'][lang]}</div>
                        <div class="pdp-preview-callout">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
                            <span><strong>{demo['callout_label'][lang]}</strong> "{demo['callout_text'][lang]}"</span>
                        </div>"""
        elif dtype == "stats":
            cards = "\n".join(
                f'                            <div class="pdp-stat-card{" pdp-stat-card--highlight" if hi else ""}">'
                f'<div class="pdp-stat-label">{label}</div><div class="pdp-stat-val">{val}</div></div>'
                for label, val, hi in demo['stats'][lang]
            )
            body = f"""
                        <div class="pdp-preview-head">
                            <span class="pdp-preview-filename">{demo['filename'][lang]}</span>
                            <span class="pdp-preview-copilot-tag">{demo['tag'][lang]}</span>
                        </div>
                        <div class="pdp-preview-stats">
{cards}
                        </div>"""
        elif dtype == "slide":
            body = f"""
                        <div class="pdp-preview-head">
                            <span class="pdp-preview-filename">{demo['filename'][lang]}</span>
                            <span class="pdp-preview-copilot-tag">{demo['tag'][lang]}</span>
                        </div>
                        <div class="pdp-slide-preview">
                            <div class="pdp-slide-num">{demo['slide_num'][lang]}</div>
                            <div class="pdp-slide-title">{demo['slide_title'][lang]}</div>
                            <div class="pdp-slide-desc">{demo['slide_desc'][lang]}</div>
                        </div>"""
        elif dtype == "cloud":
            body = f"""
                        <div class="pdp-preview-head">
                            <span class="pdp-preview-filename">{demo['filename'][lang]}</span>
                            <span class="pdp-preview-copilot-tag">{demo['tag'][lang]}</span>
                        </div>
                        <div class="pdp-cloud-progress-wrap">
                            <div class="pdp-cloud-progress-info">
                                <span>{demo['used_label'][lang]}</span>
                                <strong>{demo['free_label'][lang]}</strong>
                            </div>
                            <div class="pdp-cloud-track"><div class="pdp-cloud-bar" style="width:{demo['percent']}%"></div></div>
                        </div>"""
        else:
            text = (demo.get("text") or {}).get(lang) or (APP_DEMOS.get(k) or {}).get(lang) or (APP_DEMOS.get(k) or {}).get("en") or ""
            body = f'\n                        <div class="pdp-preview-text">{text}</div>' if text else ""
        panels.append(
            f'                    <div id="preview-content-{k}" class="pdp-preview-panel{active}">{body}\n'
            f'                    </div>'
        )

    extra = [a for a in app_keys if a not in keys]
    more_html = ""
    if extra:
        items = "\n".join(_app_item(k, 24) for k in extra)
        more_html = f"""
                <details class="pdp-apps-more">
                    <summary>{v3['apps_more']}</summary>
                    <div class="pdp-apps-more__body">
                        <ul class="pdp-apps">
{items}
                        </ul>
                    </div>
                </details>"""

    return f"""                <div class="pdp-tabs-clean">
{chr(10).join(tabs)}
                </div>
                <div class="pdp-preview-workspace" id="app-preview-container">
{chr(10).join(panels)}
                </div>{more_html}"""


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
        f'<span class="pdp-price-badge" aria-label="−{disc}%">−{disc}% '
        f'{DISCOUNT_SUFFIX.get(lang, DISCOUNT_SUFFIX["en"])}</span>'
        if disc > 0
        else ""
    )
    msrp_html = (
        f'<span class="pdp-price-msrp" aria-label="{eur_fmt(compare)}">€ {eur_fmt(compare)}</span>'
        if disc > 0
        else ""
    )
    # Riga propria sopra la nota tasse/consegna (risparmio in evidenza, poi il
    # resto in tono neutro sotto) — come nel mockup di riferimento, non più
    # concatenata nella stessa frase.
    save_html = ""
    if save > 0:
        save_html = (
            f'                <p class="pdp-price-save">{ui["save_prefix"]} '
            f'<strong>€ {eur_fmt(save)}</strong> {ui["save_vs"]} '
            f'(€ {eur_fmt(compare)}).</p>\n'
        )
    faq_entities = [
        {
            "@type": "Question",
            "name": q,
            # "text" nello schema.org Answer vuole una stringa: una risposta a
            # piu' paragrafi (vedi _render_faq) va congiunta qui, altrimenti
            # json.dumps la serializza come array e il rich result FAQPage
            # smette di validare.
            "acceptedAnswer": {
                "@type": "Answer",
                "text": " ".join(a) if isinstance(a, (list, tuple)) else a,
            },
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
    plan_switcher_html = _render_plan_switcher(sku, lang, ui)
    rich_demos = content.get("app_demo_rich")
    if rich_demos:
        app_tabs_html = _render_app_tabs_rich(
            content.get("apps") or [], content.get("app_tabs_featured"), rich_demos, v3, lang
        )
    else:
        app_tabs_html = _render_app_tabs(content.get("apps") or [], v3, lang)
    # Secondo badge dell'hero: prima pill del prodotto, gia' localizzata e
    # specifica (es. "Include Copilot"). Niente claim inventati.
    pills = (content.get("pills") or {}).get(lang) or []
    badge2_html = (
        f'\n                    <span class="pdp-badge pdp-badge--alt">{pills[0][1]}</span>'
        if pills
        else ""
    )
    steps_title = (content.get('steps_title') or {}).get(lang) or ui['how_title']
    specs_note = (content.get('specs_note') or {}).get(lang) or ui['specs_note']
    # Nota facoltativa dopo i 3 passi (es. avviso account Microsoft su M365
    # Family). Stessa veste .pdp-note usata altrove nel file, gia' styled.
    steps_note = (content.get('steps_note') or {}).get(lang)
    steps_note_html = (
        f'            <p class="pdp-note">\n'
        f'                {NOTE_ICON}\n'
        f'                <span>{steps_note}</span>\n'
        f'            </p>\n'
        if steps_note
        else ""
    )
    overview_block = _render_overview(content, lang)

    # Sezioni condizionali: compaiono solo se il prodotto fornisce i dati.
    # Le app sono gia' tutte nelle tab dell'hero (con l'elenco a comparsa per
    # quelle oltre la sesta): questa sezione non ripete piu' la griglia, e
    # quindi ha senso SOLO quando c'e' un sottotitolo con contenuto vero da
    # dire (M365 Family: "installa le app desktop, lavora offline..."). Senza
    # sottotitolo sarebbe un titolo isolato che duplica l'hero — via, come nel
    # mockup, che le app le mostra una volta sola.
    apps_block = ""
    apps_sub = (content.get("apps_sub") or {}).get(lang)
    if content.get("apps") and apps_sub:
        apps_block = f"""        <hr class="pdp-divider">

        <section class="pdp-sec" aria-labelledby="pdp-apps-title">
            <p class="pdp-sec__eyebrow">{ui['apps_eyebrow']}</p>
            <h2 id="pdp-apps-title" class="pdp-sec__title">{content['apps_title'][lang]}</h2>
            <p class="pdp-sec__sub">{apps_sub}</p>
        </section>
"""

    # Sezione feature: opzionale come le altre. Alcune schede — M365 Family in
    # testa — costruiscono la pagina su blocchi propri (postazioni, confronto)
    # e non hanno card feature: pretenderle significherebbe inventarle.
    features_block = ""
    features = (content.get("features") or {}).get(lang)
    # Il titolo puo' mancare (None) quando il contenuto e' stato estratto da una
    # vecchia pagina che non aveva l'<h2>: interpolarlo cosi' com'e' stampava la
    # stringa "None" in pagina. Meglio l'occhiello da solo che un titolo falso.
    features_title = (content.get("features_title") or {}).get(lang)
    features_title_html = (
        f'\n            <h2 id="pdp-features-title" class="pdp-sec__title">{features_title}</h2>'
        if features_title else ""
    )
    labelled_by = ' aria-labelledby="pdp-features-title"' if features_title else ""
    if features:
        features_block = f"""        <section class="pdp-sec"{labelled_by}>
            <p class="pdp-sec__eyebrow">{ui['features_eyebrow']}</p>{features_title_html}
            <ul class="pdp-cards">
{_render_cards(features)}
            </ul>
        </section>

"""

    lifestyle_block = _render_lifestyle_band(content.get("lifestyle"), lang)
    seats_block = _render_seats(content.get("seats"), lang)
    compare_block = _render_compare(content.get("compare"), lang)
    stats_block = _render_stats(content.get("stats"), lang)
    specs_table_block = _render_specs_table(content.get("specs_table"), lang, sku)
    roles_block = _render_roles(content.get("roles"), lang)

    # FAQ per argomento se il prodotto le fornisce (M365 Family), altrimenti
    # la lista piatta a due colonne di sempre — nessun cambiamento per tutti
    # gli altri prodotti.
    faq_groups = (content.get("faq_groups") or {}).get(lang)
    if faq_groups:
        faq_body_html = _render_faq_groups(faq_groups)
    else:
        faq_body_html = (
            '            <div class="home-faq-list">\n'
            f"{_render_faq_columns(content['faq'][lang])}\n"
            "            </div>"
        )
    guide_trigger, guide_dialog = _render_activation_modal(ui, content, lang)

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
    <!-- Font del mockup di riferimento (Plus Jakarta Sans + Inter), scopato alla
         sola PDP tramite --font-sans su .pdp-page — non tocca header/footer,
         che leggono --aml-font-sans direttamente (restano su Montserrat).
         Da Google Fonts, non auto-ospitato come Montserrat: senza le metriche
         di fallback calibrate apposta (vedi fonts/montserrat.css), il primo
         render usa il font di sistema e poi scatta al cambio font — piccolo
         CLS accettato per allinearsi al mockup, non ancora ottimizzato. -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
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
            <img class="product-sticky-cta__thumb" src="{img_src}" width="40" height="40" alt="" loading="lazy" decoding="async">
            <div class="product-sticky-cta__name">
                <span class="product-sticky-cta__title">{short}</span>
                {f'<span class="product-sticky-cta__eta">{_buy_labels(lang)["sticky_delivery"]}</span>' if not is_physical_sku(sku) else ''}
            </div>
            <div class="product-sticky-cta__prices" aria-hidden="true">
                {f'<span class="product-sticky-cta__msrp">€ {eur_fmt(compare)}</span>' if disc > 0 else ''}
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
                <div class="pdp-badges">
                    <span class="pdp-badge">{eyebrow}</span>{badge2_html}
                    {product_code_html(labels, sku)}
                </div>
                <h1 class="pdp-h1 v2-hero__title">{title_html}</h1>
                <p class="v2-hero__desc">{desc}</p>

                <figure class="pdp-media">
                    <img class="pdp-media__img product-cover-img" src="{img_src}" width="400" height="400" alt="{short}" fetchpriority="high" decoding="async">
                </figure>

                <div class="pdp-apptabs-block">
{app_tabs_html}
                </div>

{keypoints_html}

{guide_trigger}            </div>

            <div id="product-pricing" class="pdp-buy"
                data-stripe-currency="eur"
                data-stripe-unit-amount="{sale}"
                data-stripe-compare-at-amount="{compare}"
                data-stripe-product-sku="{sku}"
                data-discount-percent="{disc}"{_physical_attr(sku)}>
{_render_avail_banner(lang, sku)}{plan_switcher_html}                <p class="pdp-buy__label">{labels['price_label']}{badge_html}</p>

                <div class="pdp-price-row" role="group" aria-label="{ui['prices_aria']}">
                    <span class="pdp-price-sale">€ {eur_fmt(sale)}</span>
                    {msrp_html}
                </div>
{save_html}                <p class="pdp-price-note">{labels['tax']}</p>
{_stock_block_html(lang, sku)}
                <button type="button" id="product-primary-cta" class="pdp-btn-primary" data-cart-add data-cart-source="product-pricing" data-cart-checkout-redirect="/{lang}/checkout">
                    {CART_ICON}
                    {_buy_labels(lang)['checkout']}
                </button>
{_render_secondary_cta(labels['add'])}
                <ul class="pdp-assur">
{_render_assur(v3, ASSUR_KEYS[:2])}
                </ul>
            </div>
        </div>
    </section>
{_render_trustbar(v3)}
    <main id="main" class="product-page" data-cart-added-msg="{ui['cart_added']}">
        <div id="product-cart-live" class="visually-hidden" aria-live="polite" aria-atomic="true"></div>

{overview_block}{features_block}
{stats_block}{specs_table_block}{roles_block}{apps_block}{seats_block}{compare_block}{lifestyle_block}        <hr class="pdp-divider">

        <section class="pdp-sec" aria-labelledby="pdp-steps-title">
            <p class="pdp-sec__eyebrow">{ui['how_eyebrow']}</p>
            <h2 id="pdp-steps-title" class="pdp-sec__title">{steps_title}</h2>
            <ol class="pdp-steps">
{_render_steps_v3(ui, content, lang)}
            </ol>
{steps_note_html}        </section>
{_render_reviews(v3, lang)}
        <hr class="pdp-divider">

        <section id="faq" class="pdp-sec home-faq" aria-labelledby="pdp-faq-title">
            <p class="pdp-sec__eyebrow">{ui['faq_eyebrow']}</p>
            <h2 id="pdp-faq-title" class="pdp-sec__title pdp-faq__title">{v3['faq_title']}</h2>
{faq_body_html}
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
    </main>
{guide_dialog}    <aml-cookie-banner></aml-cookie-banner>
    <ecommerce-footer translate="no" class="notranslate"></ecommerce-footer>
    <script src="../js/locale-path.js"></script>
    <script src="../js/cart.js" defer></script>
    <script src="../js/faq.js" defer></script>
    <script src="../js/product-page.js" defer></script>
    <script src="../js/product-v3.js" defer></script>
    <script src="../js/pdp-activation-modal.js" defer></script>
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
            <img class="product-sticky-cta__thumb" src="{img_src}" width="40" height="40" alt="" loading="lazy" decoding="async">
            <div class="product-sticky-cta__name">
                <span class="product-sticky-cta__title">{short}</span>
                {f'<span class="product-sticky-cta__eta">{_buy_labels(lang)["sticky_delivery"]}</span>' if not is_physical_sku(sku) else ''}
            </div>
            <div class="product-sticky-cta__prices" aria-hidden="true">
                {f'<span class="product-sticky-cta__msrp">€ {eur_fmt(compare)}</span>' if disc > 0 else ''}
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
