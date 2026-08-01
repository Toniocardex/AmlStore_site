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

TRUSTPILOT_BUSINESS_UNIT = "61c44c912f493a1a7cd810fa"
TRUSTPILOT_TEMPLATE_ID = "5419b6a8b0d04a076446a9ad"
TRUSTPILOT_TOKEN = "27270fde-f5a0-4937-9101-76b7ebae8a1a"


def _trustpilot_block(lang):
    """Micro TrustBox + fallback link (loader: js/trustpilot-widget.js)."""
    tp_locale, tp_url = TRUSTPILOT_LOCALE[lang]
    t = TRUSTPILOT_I18N[lang]
    return f"""        <section class="product-trustpilot v2-section v2-section--tight" aria-labelledby="product-trustpilot-title">
            <h2 id="product-trustpilot-title" class="visually-hidden">{t['title']}</h2>
            <p class="product-trustpilot__fallback trustpilot-fallback">{t['fallback']} <a href="{tp_url}" target="_blank" rel="noopener noreferrer">Trustpilot</a></p>
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
        </section>
"""


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
        "price_label": "Il nostro prezzo",
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
        "price_label": "Our price",
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
        "price_label": "Notre prix",
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
        "price_label": "Unser Preis",
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
        "price_label": "Nuestro precio",
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
            f'    <link rel="alternate" hreflang="{lg}" href="https://aml-store.com/{lg}/{slug}.html">'
        )
    lines.append(
        f'    <link rel="alternate" hreflang="x-default" href="https://aml-store.com/it/{slug}.html">'
    )
    return "\n".join(lines)


def product_card_price_block(sale, compare, disc):
    if disc > 0:
        return f"""                    <div class="product-card-price-block">
                        <div class="product-card-price-block__row">
                            <span class="product-card-price-block__msrp">€ {eur_fmt(compare)}</span>
                            <span class="product-card-price-block__sale">€ {eur_fmt(sale)}</span>
                            <span class="product-card-price-block__save">−{disc}%</span>
                        </div>
                    </div>"""
    return f"""                    <p class="product-card-price">€ {eur_fmt(sale)}</p>"""


def product_card(lang, prod, labels):
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
    price_html = product_card_price_block(sale, compare, disc)
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
                            <img src="{image_src}" width="400" height="400" alt="{name}" decoding="async"{lazy_attr} class="product-card-img" onerror="this.onerror=null;this.src='{PRODUCT_COVER_FALLBACK_SRC}'">
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
    src = f"../asset/media/products/{img}"
    srcset_attrs = ""
    if img_640 and img_640 != img:
        src_640 = f"../asset/media/products/{img_640}"
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
            f"""                <details>
                    <summary>{q}</summary>
                    <p>{a}</p>
                </details>"""
        )
    return "\n".join(parts)


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
    page_url = f"https://aml-store.com/{lang}/{slug}.html"
    badge_html = (
        f'<span class="v2-price-badge" aria-label="−{disc}%">−{disc}%</span>'
        if disc > 0
        else ""
    )
    msrp_html = (
        f'<span class="v2-price-msrp" aria-label="{eur_fmt(compare)}">€ {eur_fmt(compare)}</span>'
        if disc > 0
        else ""
    )
    save_html = ""
    if save > 0:
        save_html = f"""                    <div class="v2-price-compare">
                        {ui['save_prefix']} <strong>€ {eur_fmt(save)}</strong> {ui['save_vs']} (€ {eur_fmt(compare)})
                    </div>"""

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
                    {"@type": "ListItem", "position": 2, "name": cat_name, "item": f"https://aml-store.com/{lang}/{cat_slug}.html"},
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

    lifestyle_block = _render_lifestyle_band(content.get("lifestyle"), lang)

    if content.get("apps"):
        apps_block = f"""{lifestyle_block}        <section class="v2-apps-section" aria-labelledby="v2-apps-title">
            <p class="v2-eyebrow">{ui['apps_eyebrow']}</p>
            <h2 id="v2-apps-title" class="v2-section-title" style="margin-bottom:32px;">{content['apps_title'][lang]}</h2>
            <div class="v2-apps-grid">
{_render_apps(content['apps'])}
            </div>
        </section>
        <hr class="v2-divider">
"""
    else:
        apps_block = f"{lifestyle_block}        <hr class=\"v2-divider\">\n"

    steps_block = _render_steps_block(ui, content, lang)
    specs_block = _render_specs_block(ui, content, lang)

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
    <link rel="stylesheet" href="../css/product.css">
    <link rel="stylesheet" href="../css/microsoft-365-product.css">
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
            <button type="button" class="btn-primary" data-cart-add data-cart-source="sticky-cta">
                {CART_ICON}
                {ui['sticky_add']}
            </button>
        </div>
    </div>
    <section class="v2-hero" aria-label="{ui['hero_aria']}">
        <div class="v2-hero__ambient" aria-hidden="true"></div>
        <div class="v2-hero__ambient-2" aria-hidden="true"></div>
        <div class="v2-hero__ambient-mid" aria-hidden="true"></div>
        <div class="v2-breadcrumb">
            <nav aria-label="{ui['breadcrumb_nav']}">
                <a href="/{lang}/">Home</a>
                <span class="sep" aria-hidden="true">/</span>
                <a href="/{lang}/{cat_slug}.html">{cat_name}</a>
                <span class="sep" aria-hidden="true">/</span>
                <span aria-current="page">{short}</span>
            </nav>
        </div>
        <div class="v2-hero__inner">
            <div class="v2-hero__left">
                <p class="v2-hero__eyebrow">{eyebrow}</p>
                <h1 class="v2-hero__title">{title_html}</h1>
                {product_code_html(labels, sku)}
                <p class="v2-hero__desc">{desc}</p>
                <div class="v2-pills" aria-label="{ui['features_eyebrow']}">
{_render_pills(content['pills'][lang])}
                </div>
            </div>
            <div class="v2-hero__right">
                <div class="v2-hero__cover-wrap">
                    <img class="v2-hero__cover" src="{img_src}" width="400" height="400" alt="{short}" fetchpriority="high" decoding="async">
                </div>
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
            <div>
                <div class="v2-price-label">{labels['price_label']}</div>
                <div class="v2-price-row" role="group" aria-label="{ui['prices_aria']}">
                    {msrp_html}
                    <span class="v2-price-sale">€ {eur_fmt(sale)}</span>
                    {badge_html}
                </div>
                <div class="v2-price-tax">{labels['tax']}</div>
{_stock_block_html(lang, sku)}{save_html}
            </div>
            <div class="v2-pricing-actions">
                <button type="button" id="product-primary-cta" class="v2-btn-primary" data-cart-add data-cart-source="product-pricing">
                    {CART_ICON}
                    {labels['add']}
                </button>
{_render_payment_row(ui)}
            </div>
        </div>
    </div>
    <main id="main" class="product-page" data-cart-added-msg="{ui['cart_added']}">
        <div id="product-cart-live" class="visually-hidden" aria-live="polite" aria-atomic="true"></div>
        <section class="v2-section" aria-labelledby="v2-features-title">
            <p class="v2-eyebrow">{ui['features_eyebrow']}</p>
            <h2 id="v2-features-title" class="v2-section-title">{content['features_title'][lang]}</h2>
            <div class="v2-bento" role="list">
{_render_features(content['features'][lang])}
            </div>
        </section>
{apps_block}{steps_block}
{_trustpilot_block(lang)}        <hr class="v2-divider">
{specs_block}
        <hr class="v2-divider">
        <section class="v2-section" aria-labelledby="v2-faq-title">
            <p class="v2-eyebrow">{ui['faq_eyebrow']}</p>
            <h2 id="v2-faq-title" class="v2-section-title">{ui['faq_title']}</h2>
            <div class="v2-faq">
{_render_faq(content['faq'][lang])}
            </div>
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
                "@id": f"https://aml-store.com/{lang}/{slug}.html#product",
                "name": short,
                "sku": sku,
                **({"mpn": e["mpn"]} if e.get("mpn") else {}),
                "inLanguage": lang,
                "url": f"https://aml-store.com/{lang}/{slug}.html",
                "image": og_image_abs,
                "description": desc,
                "brand": {"@type": "Brand", "name": brand},
                "offers": {
                    "@type": "Offer",
                    "url": f"https://aml-store.com/{lang}/{slug}.html",
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
    <link rel="canonical" href="https://aml-store.com/{lang}/{slug}.html">
    <meta property="og:type" content="product">
    <meta property="og:site_name" content="Aml Store">
    <meta property="og:title" content="{short} — Aml Store">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="https://aml-store.com/{lang}/{slug}.html">
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
    <link rel="stylesheet" href="../css/product.css">
    <link rel="stylesheet" href="../css/microsoft-365-product.css">
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
                <a href="/{lang}/{cat_slug}.html">{cat_name}</a><span class="sep">/</span>
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
        </div>
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
{_trustpilot_block(lang)}    </main>
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
    <link rel="canonical" href="https://aml-store.com/{lang}/{catalog_slug}.html">
{hreflang_block(catalog_slug)}
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title} | Aml Store">
    <meta property="og:description" content="{lede}">
    <meta property="og:url" content="https://aml-store.com/{lang}/{catalog_slug}.html">
    <meta property="og:locale" content="{LOCALE[lang]}">
    <meta property="og:image" content="{og_image}">
    <link rel="stylesheet" href="../fonts/montserrat.css">
    <link rel="stylesheet" href="../css/page.css">
    <link rel="stylesheet" href="../css/home.css">
    <script src="../js/theme-init.js"></script>
    <script type="application/ld+json">
    {{"@context":"https://schema.org","@type":"CollectionPage","name":"{title}","description":"{lede}","url":"https://aml-store.com/{lang}/{catalog_slug}.html","inLanguage":"{lang}","isPartOf":{{"@type":"WebSite","name":"Aml Store","url":"https://aml-store.com/"}}}}
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
