#!/usr/bin/env python3
"""
Rich product-page content for antivirus SKUs.
Structure mirrors flagship samples (M365 Personal): hero ambient + pills,
floating pricing card, bento features, steps, specs, FAQ — no invented reviews.
"""

from copy import deepcopy

from product_content_office import UI as OFFICE_UI

LANGS = ("it", "en", "fr", "de", "es")


def L(**kwargs):
    return {k: kwargs[k] for k in LANGS}


# Antivirus UI: same chrome as Office sample, vendor activation instead of setup.office.com
UI = deepcopy(OFFICE_UI)
_AV_OVERRIDES = {
    "it": {
        "apps_eyebrow": "In evidenza",
        "step2_body": "Ti inviamo la <strong>licenza / codice</strong> e le istruzioni via email, di solito entro pochi minuti dall'approvazione del pagamento.",
        "step3_body": "Attiva sul <strong>portale ufficiale del produttore</strong> (Norton, Kaspersky, Bitdefender, ESET o McAfee) con il codice ricevuto e segui le istruzioni nell'email.",
        "spec_cpu_body": "PC o dispositivi supportati dal produttore; verifica i requisiti aggiornati sulla scheda ufficiale del software.",
        "spec_os_body": "Windows, macOS, Android o iOS secondo le piattaforme supportate dal prodotto acquistato.",
        "spec_ram_body": "Requisiti tipici da pochi GB di RAM; consulta la documentazione del produttore per il titolo specifico.",
        "spec_disk_body": "Spazio libero sufficiente per l'installazione del client di sicurezza, come da requisiti del produttore.",
        "specs_note": "Valori orientativi; verifica sempre i requisiti aggiornati sul sito ufficiale del produttore prima dell'installazione.",
    },
    "en": {
        "apps_eyebrow": "Highlights",
        "step2_body": "We email the <strong>licence / key</strong> and instructions, usually within minutes after payment approval.",
        "step3_body": "Activate on the <strong>official vendor portal</strong> (Norton, Kaspersky, Bitdefender, ESET or McAfee) with the code received and follow the email instructions.",
        "spec_cpu_body": "PCs or devices supported by the vendor; check the latest requirements on the official product page.",
        "spec_os_body": "Windows, macOS, Android or iOS depending on platforms supported by the purchased product.",
        "spec_ram_body": "Typical requirements are a few GB of RAM; see vendor documentation for the specific title.",
        "spec_disk_body": "Enough free space to install the security client, per the vendor’s requirements.",
        "specs_note": "Indicative values; always check the vendor’s latest requirements before installing.",
    },
    "fr": {
        "apps_eyebrow": "Points clés",
        "step2_body": "Nous envoyons la <strong>licence / clé</strong> et les instructions par e-mail, en général quelques minutes après validation du paiement.",
        "step3_body": "Activez sur le <strong>portail officiel de l'éditeur</strong> (Norton, Kaspersky, Bitdefender, ESET ou McAfee) avec le code reçu et suivez l'e-mail.",
        "spec_cpu_body": "PC ou appareils pris en charge par l'éditeur ; vérifiez la fiche officielle.",
        "spec_os_body": "Windows, macOS, Android ou iOS selon les plateformes supportées.",
        "spec_ram_body": "Quelques Go de RAM typiquement ; voir la doc de l'éditeur.",
        "spec_disk_body": "Espace libre suffisant pour le client de sécurité.",
        "specs_note": "Valeurs indicatives ; vérifiez toujours les exigences à jour de l'éditeur.",
    },
    "de": {
        "apps_eyebrow": "Highlights",
        "step2_body": "Wir senden <strong>Lizenz / Key</strong> und Anleitung per E-Mail, in der Regel wenige Minuten nach Zahlungsfreigabe.",
        "step3_body": "Aktivieren Sie im <strong>offiziellen Herstellerportal</strong> (Norton, Kaspersky, Bitdefender, ESET oder McAfee) mit dem erhaltenen Code und folgen Sie der E-Mail.",
        "spec_cpu_body": "Vom Hersteller unterstützte PCs/Geräte; aktuelle Anforderungen auf der Produktseite prüfen.",
        "spec_os_body": "Windows, macOS, Android oder iOS je nach unterstützten Plattformen.",
        "spec_ram_body": "Typisch einige GB RAM; Herstellerdokumentation prüfen.",
        "spec_disk_body": "Ausreichend freier Speicher für den Sicherheits-Client.",
        "specs_note": "Richtwerte; stets aktuelle Herstelleranforderungen prüfen.",
    },
    "es": {
        "apps_eyebrow": "Destacados",
        "step2_body": "Enviamos la <strong>licencia / clave</strong> e instrucciones por email, normalmente en minutos tras aprobar el pago.",
        "step3_body": "Activa en el <strong>portal oficial del fabricante</strong> (Norton, Kaspersky, Bitdefender, ESET o McAfee) con el código recibido y sigue el email.",
        "spec_cpu_body": "PCs o dispositivos admitidos por el fabricante; consulta los requisitos oficiales.",
        "spec_os_body": "Windows, macOS, Android o iOS según las plataformas del producto.",
        "spec_ram_body": "Normalmente unos pocos GB de RAM; consulta la documentación del fabricante.",
        "spec_disk_body": "Espacio libre suficiente para el cliente de seguridad.",
        "specs_note": "Valores orientativos; comprueba siempre los requisitos actualizados del fabricante.",
    },
}
for lg, ov in _AV_OVERRIDES.items():
    UI[lg].update(ov)


def _devices(n):
    return L(
        it=f"{n} dispositivo" if n == 1 else f"{n} dispositivi",
        en=f"{n} device" if n == 1 else f"{n} devices",
        fr=f"{n} appareil" if n == 1 else f"{n} appareils",
        de=f"{n} Gerät" if n == 1 else f"{n} Geräte",
        es=f"{n} dispositivo" if n == 1 else f"{n} dispositivos",
    )


def _year(years=1):
    return L(
        it="1 anno" if years == 1 else f"{years} anni",
        en="1 year" if years == 1 else f"{years} years",
        fr="1 an" if years == 1 else f"{years} ans",
        de="1 Jahr" if years == 1 else f"{years} Jahre",
        es="1 año" if years == 1 else f"{years} años",
    )


def _av_page(
    *,
    brand,
    line,
    title_span,
    devices,
    years,
    name,
    desc,
    pills,
    features_title,
    features,
    faq,
    no_sub=False,
):
    """Build one rich antivirus content dict (sample-page shape)."""
    y = _year(years)
    d = _devices(devices)
    eyebrow = {}
    for lg in LANGS:
        parts = [brand, y[lg], d[lg]]
        if no_sub:
            parts.append(
                {
                    "it": "senza rinnovo automatico",
                    "en": "no auto-renewal",
                    "fr": "sans renouvellement auto",
                    "de": "ohne Auto-Verlängerung",
                    "es": "sin renovación automática",
                }[lg]
            )
        eyebrow[lg] = " · ".join(parts)

    return {
        "apps": [],
        "name": name,
        "title_html": L(
            it=f"{brand} <span>{title_span['it']}</span>",
            en=f"{brand} <span>{title_span['en']}</span>",
            fr=f"{brand} <span>{title_span['fr']}</span>",
            de=f"{brand} <span>{title_span['de']}</span>",
            es=f"{brand} <span>{title_span['es']}</span>",
        ),
        "eyebrow": eyebrow,
        "desc": desc,
        "pills": pills,
        "features_title": features_title,
        "features": features,
        "apps_title": L(it="", en="", fr="", de="", es=""),
        "faq": faq,
    }


def _line_feats(brand, line_it, line_en, focus_it, focus_en, focus_fr, focus_de, focus_es, tip_it, tip_en):
    return {
        "it": [
            ("c8", "blue", "Protezione", line_it, f"Licenza digitale {brand}: protezione per i dispositivi indicati in scheda, con attivazione sul portale ufficiale del produttore."),
            ("c4", "teal", None, focus_it, "Funzioni di sicurezza del piano acquistato, come descritte dal produttore."),
            ("c4", "purple", "Consegna", "Via email", "Ricevi codice/licenza e istruzioni dopo il pagamento, senza spedizione fisica del software."),
            ("c4", None, "Attivazione", "Portale ufficiale", f"Attivi su {brand} con il codice ricevuto e installi il client ufficiale."),
            ("c4", None, "Dispositivi", "Come da scheda", "Il numero di dispositivi e la durata sono quelli indicati nel titolo prodotto."),
            ("c4", "dark", "Nota", tip_it, tip_en if False else tip_it),
        ],
        "en": [
            ("c8", "blue", "Protection", line_en, f"Digital {brand} licence: protection for the devices listed on this page, activated on the official vendor portal."),
            ("c4", "teal", None, focus_en, "Security features of the purchased plan, as described by the vendor."),
            ("c4", "purple", "Delivery", "By email", "Receive the licence/key and instructions after payment—no physical software shipment."),
            ("c4", None, "Activation", "Official portal", f"Activate with {brand} using the received code and install the official client."),
            ("c4", None, "Devices", "As listed", "Device count and term are those shown in the product title."),
            ("c4", "dark", "Note", tip_en, tip_en),
        ],
        "fr": [
            ("c8", "blue", "Protection", line_en, f"Licence numérique {brand} : protection pour les appareils indiqués, activation sur le portail officiel."),
            ("c4", "teal", None, focus_fr, "Fonctions de sécurité du plan acheté, selon l'éditeur."),
            ("c4", "purple", "Livraison", "Par e-mail", "Licence/clé et instructions après paiement."),
            ("c4", None, "Activation", "Portail officiel", f"Activation chez {brand} avec le code reçu."),
            ("c4", None, "Appareils", "Selon la fiche", "Nombre d'appareils et durée comme dans le titre."),
            ("c4", "dark", "Note", tip_en, tip_en),
        ],
        "de": [
            ("c8", "blue", "Schutz", line_en, f"Digitale {brand}-Lizenz: Schutz für die angegebenen Geräte, Aktivierung im offiziellen Portal."),
            ("c4", "teal", None, focus_de, "Sicherheitsfunktionen des gekauften Plans laut Hersteller."),
            ("c4", "purple", "Lieferung", "Per E-Mail", "Lizenz/Key und Anleitung nach der Zahlung."),
            ("c4", None, "Aktivierung", "Offizielles Portal", f"Aktivierung bei {brand} mit dem erhaltenen Code."),
            ("c4", None, "Geräte", "Laut Seite", "Gerätezahl und Laufzeit wie im Produkttitel."),
            ("c4", "dark", "Hinweis", tip_en, tip_en),
        ],
        "es": [
            ("c8", "blue", "Protección", line_en, f"Licencia digital {brand}: protección para los dispositivos de la ficha, activación en el portal oficial."),
            ("c4", "teal", None, focus_es, "Funciones de seguridad del plan comprado, según el fabricante."),
            ("c4", "purple", "Entrega", "Por email", "Licencia/clave e instrucciones tras el pago."),
            ("c4", None, "Activación", "Portal oficial", f"Activa en {brand} con el código recibido."),
            ("c4", None, "Dispositivos", "Según ficha", "Número de dispositivos y duración como en el título."),
            ("c4", "dark", "Nota", tip_en, tip_en),
        ],
    }


# Fix Italian tip cell - the dark cell used tip_it wrongly for EN in it block. Rebuild feats more carefully per product family.

def _feats(brand, line, focus, tip):
    """features dict with proper i18n for all 6 bento cells."""
    out = {}
    for lg in LANGS:
        out[lg] = [
            (
                "c8",
                "blue",
                {"it": "Protezione", "en": "Protection", "fr": "Protection", "de": "Schutz", "es": "Protección"}[lg],
                line[lg],
                {
                    "it": f"Licenza digitale {brand}: protezione per i dispositivi indicati in scheda, con attivazione sul portale ufficiale del produttore.",
                    "en": f"Digital {brand} licence: protection for the devices listed on this page, activated on the official vendor portal.",
                    "fr": f"Licence numérique {brand} : protection pour les appareils indiqués, activation sur le portail officiel.",
                    "de": f"Digitale {brand}-Lizenz: Schutz für die angegebenen Geräte, Aktivierung im offiziellen Portal.",
                    "es": f"Licencia digital {brand}: protección para los dispositivos de la ficha, activación en el portal oficial.",
                }[lg],
            ),
            (
                "c4",
                "teal",
                None,
                focus[lg],
                {
                    "it": "Funzioni di sicurezza del piano acquistato, come descritte dal produttore.",
                    "en": "Security features of the purchased plan, as described by the vendor.",
                    "fr": "Fonctions de sécurité du plan acheté, selon l'éditeur.",
                    "de": "Sicherheitsfunktionen des gekauften Plans laut Hersteller.",
                    "es": "Funciones de seguridad del plan comprado, según el fabricante.",
                }[lg],
            ),
            (
                "c4",
                "purple",
                {"it": "Consegna", "en": "Delivery", "fr": "Livraison", "de": "Lieferung", "es": "Entrega"}[lg],
                {"it": "Via email", "en": "By email", "fr": "Par e-mail", "de": "Per E-Mail", "es": "Por email"}[lg],
                {
                    "it": "Ricevi codice/licenza e istruzioni dopo il pagamento, senza spedizione fisica del software.",
                    "en": "Receive the licence/key and instructions after payment—no physical software shipment.",
                    "fr": "Licence/clé et instructions après paiement, sans envoi physique du logiciel.",
                    "de": "Lizenz/Key und Anleitung nach der Zahlung — ohne physischen Software-Versand.",
                    "es": "Licencia/clave e instrucciones tras el pago, sin envío físico del software.",
                }[lg],
            ),
            (
                "c4",
                None,
                {"it": "Attivazione", "en": "Activation", "fr": "Activation", "de": "Aktivierung", "es": "Activación"}[lg],
                {"it": "Portale ufficiale", "en": "Official portal", "fr": "Portail officiel", "de": "Offizielles Portal", "es": "Portal oficial"}[lg],
                {
                    "it": f"Attivi su {brand} con il codice ricevuto e installi il client ufficiale.",
                    "en": f"Activate with {brand} using the received code and install the official client.",
                    "fr": f"Activation chez {brand} avec le code reçu et installation du client officiel.",
                    "de": f"Aktivierung bei {brand} mit dem erhaltenen Code und Installation des offiziellen Clients.",
                    "es": f"Activa en {brand} con el código recibido e instala el cliente oficial.",
                }[lg],
            ),
            (
                "c4",
                None,
                {"it": "Dispositivi", "en": "Devices", "fr": "Appareils", "de": "Geräte", "es": "Dispositivos"}[lg],
                {"it": "Come da scheda", "en": "As listed", "fr": "Selon la fiche", "de": "Laut Seite", "es": "Según ficha"}[lg],
                {
                    "it": "Il numero di dispositivi e la durata sono quelli indicati nel titolo prodotto.",
                    "en": "Device count and term are those shown in the product title.",
                    "fr": "Nombre d'appareils et durée comme dans le titre produit.",
                    "de": "Gerätezahl und Laufzeit wie im Produkttitel.",
                    "es": "Número de dispositivos y duración como en el título del producto.",
                }[lg],
            ),
            (
                "c4",
                "dark",
                {"it": "Nota", "en": "Note", "fr": "Note", "de": "Hinweis", "es": "Nota"}[lg],
                tip[lg],
                {
                    "it": "Niente stelle o recensioni inventate: per esperienze reali vedi Trustpilot e il sito del produttore.",
                    "en": "No invented star ratings: for real experiences see Trustpilot and the vendor’s site.",
                    "fr": "Pas d'avis inventés : pour des retours réels, voyez Trustpilot et le site de l'éditeur.",
                    "de": "Keine erfundenen Sterne: echte Erfahrungen auf Trustpilot und der Herstellerseite.",
                    "es": "Sin valoraciones inventadas: experiencias reales en Trustpilot y el sitio del fabricante.",
                }[lg],
            ),
        ]
    return out


def _faq_av(brand, devices_note=True):
    return {
        "it": [
            ("Cosa ricevo dopo l'acquisto?", "Una email con licenza/codice e istruzioni per attivare sul portale ufficiale del produttore."),
            ("È un abbonamento?", "Dipende dal titolo: molte edizioni sono abbonamenti annuali; le varianti «no abbonamento» / senza rinnovo automatico sono indicate in scheda."),
            ("Su quanti dispositivi?", "Il numero è quello nel titolo (es. 1, 3, 5 o 10 dispositivi), secondo le condizioni del produttore."),
            ("Come si attiva?", f"Usa il codice ricevuto sul portale ufficiale {brand} e segui le istruzioni email."),
            ("Funziona su Mac/Android?", "Se il produttore lo prevede per quel prodotto. Controlla piattaforme supportate sulla documentazione ufficiale."),
        ],
        "en": [
            ("What do I receive after purchase?", "An email with the licence/key and instructions to activate on the official vendor portal."),
            ("Is it a subscription?", "Depends on the title: many editions are yearly subscriptions; “no subscription” / no auto-renewal variants are labelled on the page."),
            ("How many devices?", "The count in the title (e.g. 1, 3, 5 or 10 devices), under the vendor’s terms."),
            ("How do I activate?", f"Use the received code on the official {brand} portal and follow the email instructions."),
            ("Works on Mac/Android?", "If the vendor supports those platforms for that product. Check official documentation."),
        ],
        "fr": [
            ("Que vais-je recevoir ?", "Un e-mail avec licence/clé et instructions d'activation sur le portail officiel."),
            ("Abonnement ?", "Selon le titre : souvent annuel ; les variantes sans renouvellement auto sont indiquées."),
            ("Combien d'appareils ?", "Le nombre indiqué dans le titre, selon l'éditeur."),
            ("Activation ?", f"Code reçu sur le portail officiel {brand}."),
            ("Mac/Android ?", "Si l'éditeur le prévoit pour ce produit."),
        ],
        "de": [
            ("Was erhalte ich?", "E-Mail mit Lizenz/Key und Aktivierungsanleitung im Herstellerportal."),
            ("Abo?", "Je nach Titel oft jährlich; Varianten ohne Auto-Verlängerung sind gekennzeichnet."),
            ("Wie viele Geräte?", "Anzahl im Titel, gemäß Herstellerbedingungen."),
            ("Aktivierung?", f"Erhaltenen Code im offiziellen {brand}-Portal verwenden."),
            ("Mac/Android?", "Falls der Hersteller es für das Produkt unterstützt."),
        ],
        "es": [
            ("¿Qué recibo?", "Un email con licencia/clave e instrucciones para activar en el portal oficial."),
            ("¿Es suscripción?", "Depende del título: muchas son anuales; las variantes sin renovación automática están indicadas."),
            ("¿Cuántos dispositivos?", "El número del título, según el fabricante."),
            ("¿Cómo se activa?", f"Usa el código en el portal oficial de {brand}."),
            ("¿Mac/Android?", "Si el fabricante lo admite para ese producto."),
        ],
    }


def _pills(brand_short, devices, years=1, extra=None):
    d = _devices(devices)
    y = _year(years)
    out = {}
    for lg in LANGS:
        items = [(None, brand_short), (None, y[lg]), (None, d[lg])]
        if extra:
            items.append((None, extra[lg]))
        out[lg] = items
    return out


def _name(brand, line, devices, years=1, no_sub=False):
    d = _devices(devices)
    y = _year(years)
    out = {}
    for lg in LANGS:
        base = f"{brand} {line} — {d[lg]}"
        if years != 1:
            base = f"{brand} {line} — {d[lg]} · {y[lg]}"
        if no_sub:
            suffix = {
                "it": " (no abbonamento)",
                "en": " (no subscription)",
                "fr": " (sans abonnement)",
                "de": " (kein Abo)",
                "es": " (sin suscripción)",
            }[lg]
            base += suffix
        out[lg] = base
    return out


PRODUCTS = {}


def _add_eset(slug, devices, years=1):
    span = {
        "it": f"NOD32 · {devices} disp." + (f" · {years} anni" if years > 1 else ""),
        "en": f"NOD32 · {devices} dev." + (f" · {years} yr" if years > 1 else ""),
        "fr": f"NOD32 · {devices} app." + (f" · {years} ans" if years > 1 else ""),
        "de": f"NOD32 · {devices} Ger." + (f" · {years} J." if years > 1 else ""),
        "es": f"NOD32 · {devices} disp." + (f" · {years} años" if years > 1 else ""),
    }
    PRODUCTS[slug] = _av_page(
        brand="ESET",
        line="NOD32",
        title_span=span,
        devices=devices,
        years=years,
        name=_name("ESET NOD32", "", devices, years) if False else L(
            **{lg: f"ESET NOD32 — {_devices(devices)[lg]}" + (f" · {_year(years)[lg]}" if years > 1 else "") for lg in LANGS}
        ),
        desc=L(
            it=f"ESET NOD32 per {_devices(devices)['it']}: protezione antivirus leggera con licenza digitale e consegna via email. Attivazione sul portale ufficiale ESET.",
            en=f"ESET NOD32 for {_devices(devices)['en']}: lightweight antivirus protection with a digital licence and email delivery. Activate on the official ESET portal.",
            fr=f"ESET NOD32 pour {_devices(devices)['fr']} : antivirus léger, licence numérique et livraison par e-mail. Activation sur le portail ESET.",
            de=f"ESET NOD32 für {_devices(devices)['de']}: schlanker Antivirus-Schutz mit digitaler Lizenz und E-Mail-Zustellung. Aktivierung im ESET-Portal.",
            es=f"ESET NOD32 para {_devices(devices)['es']}: protección antivirus ligera con licencia digital y entrega por email. Activación en el portal ESET.",
        ),
        pills=_pills("ESET", devices, years),
        features_title=L(
            it="Protezione ESET NOD32",
            en="ESET NOD32 protection",
            fr="Protection ESET NOD32",
            de="ESET NOD32 Schutz",
            es="Protección ESET NOD32",
        ),
        features=_feats(
            "ESET",
            L(it="NOD32 Antivirus", en="NOD32 Antivirus", fr="NOD32 Antivirus", de="NOD32 Antivirus", es="NOD32 Antivirus"),
            L(it="Leggero e rapido", en="Light and fast", fr="Léger et rapide", de="Leicht und schnell", es="Ligero y rápido"),
            L(it="Licenza digitale", en="Digital licence", fr="Licence numérique", de="Digitale Lizenz", es="Licencia digital"),
        ),
        faq=_faq_av("ESET"),
    )


for slug, n in [
    ("eset-nod32-1-device", 1),
    ("eset-nod32-2-devices", 2),
    ("eset-nod32-3-devices", 3),
    ("eset-nod32-5-devices", 5),
    ("eset-nod32-10-devices", 10),
]:
    _add_eset(slug, n)
_add_eset("eset-nod32-1-device-2y", 1, years=2)


def _add_norton(slug, edition, devices, no_sub=False):
    span = {
        "it": edition + (" · no sub" if no_sub else ""),
        "en": edition + (" · no sub" if no_sub else ""),
        "fr": edition + (" · sans abo" if no_sub else ""),
        "de": edition + (" · kein Abo" if no_sub else ""),
        "es": edition + (" · sin sub" if no_sub else ""),
    }
    cloud = "10 GB" if "Standard" in edition else "25 GB"
    PRODUCTS[slug] = _av_page(
        brand="Norton",
        line=edition,
        title_span=span,
        devices=devices,
        years=1,
        name=_name(f"Norton 360 {edition}", "", devices, 1, no_sub),
        desc=L(
            it=f"Norton 360 {edition} per {_devices(devices)['it']}: protezione online con licenza digitale e consegna via email. Attivazione sul portale ufficiale Norton."
            + (" Variante senza rinnovo automatico, come indicato in scheda." if no_sub else ""),
            en=f"Norton 360 {edition} for {_devices(devices)['en']}: online protection with a digital licence and email delivery. Activate on the official Norton portal."
            + (" No auto-renewal variant, as labelled on this page." if no_sub else ""),
            fr=f"Norton 360 {edition} pour {_devices(devices)['fr']} : protection en ligne, licence numérique, e-mail. Activation sur le portail Norton."
            + (" Variante sans renouvellement automatique." if no_sub else ""),
            de=f"Norton 360 {edition} für {_devices(devices)['de']}: Online-Schutz mit digitaler Lizenz und E-Mail. Aktivierung im Norton-Portal."
            + (" Variante ohne Auto-Verlängerung." if no_sub else ""),
            es=f"Norton 360 {edition} para {_devices(devices)['es']}: protección online con licencia digital y email. Activación en el portal Norton."
            + (" Variante sin renovación automática." if no_sub else ""),
        ),
        pills=_pills(
            "Norton",
            devices,
            1,
            extra=L(it=f"Cloud {cloud}", en=f"{cloud} cloud", fr=f"Cloud {cloud}", de=f"{cloud} Cloud", es=f"Cloud {cloud}")
            if "Deluxe" in edition or "Standard" in edition
            else None,
        ),
        features_title=L(
            it=f"Norton 360 {edition}",
            en=f"Norton 360 {edition}",
            fr=f"Norton 360 {edition}",
            de=f"Norton 360 {edition}",
            es=f"Norton 360 {edition}",
        ),
        features=_feats(
            "Norton",
            L(it=f"360 {edition}", en=f"360 {edition}", fr=f"360 {edition}", de=f"360 {edition}", es=f"360 {edition}"),
            L(
                it="VPN / cloud come da piano",
                en="VPN / cloud as per plan",
                fr="VPN / cloud selon l'offre",
                de="VPN / Cloud laut Plan",
                es="VPN / cloud según el plan",
            ),
            L(
                it="No auto-rinnovo" if no_sub else "Licenza digitale",
                en="No auto-renewal" if no_sub else "Digital licence",
                fr="Sans renouvellement auto" if no_sub else "Licence numérique",
                de="Ohne Auto-Verlängerung" if no_sub else "Digitale Lizenz",
                es="Sin renovación auto" if no_sub else "Licencia digital",
            ),
        ),
        faq=_faq_av("Norton"),
        no_sub=no_sub,
    )


_add_norton("norton-360-standard", "Standard", 1, no_sub=False)
_add_norton("norton-360-standard-no-sub", "Standard", 1, no_sub=True)
_add_norton("norton-360-deluxe", "Deluxe", 3, no_sub=False)
_add_norton("norton-360-deluxe-no-sub", "Deluxe", 3, no_sub=True)


def _add_bitdefender(slug, devices):
    PRODUCTS[slug] = _av_page(
        brand="Bitdefender",
        line="Antivirus Plus",
        title_span=L(
            it=f"Plus · {_devices(devices)['it']}",
            en=f"Plus · {_devices(devices)['en']}",
            fr=f"Plus · {_devices(devices)['fr']}",
            de=f"Plus · {_devices(devices)['de']}",
            es=f"Plus · {_devices(devices)['es']}",
        ),
        devices=devices,
        years=1,
        name=_name("Bitdefender Plus", "", devices),
        desc=L(
            it=f"Bitdefender Antivirus Plus per {_devices(devices)['it']}: protezione digitale con consegna del codice via email e attivazione sul portale ufficiale Bitdefender.",
            en=f"Bitdefender Antivirus Plus for {_devices(devices)['en']}: digital protection with email key delivery and activation on the official Bitdefender portal.",
            fr=f"Bitdefender Antivirus Plus pour {_devices(devices)['fr']} : protection numérique, code par e-mail, activation sur le portail Bitdefender.",
            de=f"Bitdefender Antivirus Plus für {_devices(devices)['de']}: digitaler Schutz mit Key per E-Mail und Aktivierung im Bitdefender-Portal.",
            es=f"Bitdefender Antivirus Plus para {_devices(devices)['es']}: protección digital con clave por email y activación en el portal Bitdefender.",
        ),
        pills=_pills("Bitdefender", devices),
        features_title=L(
            it="Bitdefender Antivirus Plus",
            en="Bitdefender Antivirus Plus",
            fr="Bitdefender Antivirus Plus",
            de="Bitdefender Antivirus Plus",
            es="Bitdefender Antivirus Plus",
        ),
        features=_feats(
            "Bitdefender",
            L(it="Antivirus Plus", en="Antivirus Plus", fr="Antivirus Plus", de="Antivirus Plus", es="Antivirus Plus"),
            L(it="Protezione web", en="Web protection", fr="Protection web", de="Web-Schutz", es="Protección web"),
            L(it="Licenza digitale", en="Digital licence", fr="Licence numérique", de="Digitale Lizenz", es="Licencia digital"),
        ),
        faq=_faq_av("Bitdefender"),
    )


for slug, n in [
    ("bitdefender-plus-1-device", 1),
    ("bitdefender-plus-3-devices", 3),
    ("bitdefender-plus-5-devices", 5),
    ("bitdefender-plus-10-devices", 10),
]:
    _add_bitdefender(slug, n)


def _add_kaspersky(slug, tier, devices):
    PRODUCTS[slug] = _av_page(
        brand="Kaspersky",
        line=tier,
        title_span=L(
            it=f"{tier} · {_devices(devices)['it']}",
            en=f"{tier} · {_devices(devices)['en']}",
            fr=f"{tier} · {_devices(devices)['fr']}",
            de=f"{tier} · {_devices(devices)['de']}",
            es=f"{tier} · {_devices(devices)['es']}",
        ),
        devices=devices,
        years=1,
        name=_name(f"Kaspersky {tier}", "", devices),
        desc=L(
            it=f"Kaspersky {tier} per {_devices(devices)['it']}: licenza digitale con consegna via email. Attivazione sul portale ufficiale Kaspersky.",
            en=f"Kaspersky {tier} for {_devices(devices)['en']}: digital licence with email delivery. Activate on the official Kaspersky portal.",
            fr=f"Kaspersky {tier} pour {_devices(devices)['fr']} : licence numérique, livraison par e-mail. Activation sur le portail Kaspersky.",
            de=f"Kaspersky {tier} für {_devices(devices)['de']}: digitale Lizenz mit E-Mail-Zustellung. Aktivierung im Kaspersky-Portal.",
            es=f"Kaspersky {tier} para {_devices(devices)['es']}: licencia digital con entrega por email. Activación en el portal Kaspersky.",
        ),
        pills=_pills("Kaspersky", devices, extra=L(it=tier, en=tier, fr=tier, de=tier, es=tier)),
        features_title=L(
            it=f"Kaspersky {tier}",
            en=f"Kaspersky {tier}",
            fr=f"Kaspersky {tier}",
            de=f"Kaspersky {tier}",
            es=f"Kaspersky {tier}",
        ),
        features=_feats(
            "Kaspersky",
            L(it=tier, en=tier, fr=tier, de=tier, es=tier),
            L(
                it="VPN / password come da piano" if tier != "Standard" else "Protezione essenziale",
                en="VPN / passwords as per plan" if tier != "Standard" else "Essential protection",
                fr="VPN / mots de passe selon l'offre" if tier != "Standard" else "Protection essentielle",
                de="VPN / Passwörter laut Plan" if tier != "Standard" else "Wesentlicher Schutz",
                es="VPN / contraseñas según el plan" if tier != "Standard" else "Protección esencial",
            ),
            L(it="Licenza digitale", en="Digital licence", fr="Licence numérique", de="Digitale Lizenz", es="Licencia digital"),
        ),
        faq=_faq_av("Kaspersky"),
    )


_add_kaspersky("kaspersky-standard", "Standard", 1)
_add_kaspersky("kaspersky-plus", "Plus", 1)
_add_kaspersky("kaspersky-premium-1-device", "Premium", 1)
_add_kaspersky("kaspersky-premium-3-devices", "Premium", 3)
_add_kaspersky("kaspersky-premium-5-devices", "Premium", 5)
_add_kaspersky("kaspersky-premium-10-devices", "Premium", 10)


def _add_mcafee(slug, devices):
    PRODUCTS[slug] = _av_page(
        brand="McAfee",
        line="Total Protection",
        title_span=L(
            it=f"Total Protection · {_devices(devices)['it']}",
            en=f"Total Protection · {_devices(devices)['en']}",
            fr=f"Total Protection · {_devices(devices)['fr']}",
            de=f"Total Protection · {_devices(devices)['de']}",
            es=f"Total Protection · {_devices(devices)['es']}",
        ),
        devices=devices,
        years=1,
        name=_name("McAfee Total Protection", "", devices),
        desc=L(
            it=f"McAfee Total Protection per {_devices(devices)['it']}: licenza digitale con consegna via email e attivazione sul portale ufficiale McAfee.",
            en=f"McAfee Total Protection for {_devices(devices)['en']}: digital licence with email delivery and activation on the official McAfee portal.",
            fr=f"McAfee Total Protection pour {_devices(devices)['fr']} : licence numérique, e-mail, activation sur le portail McAfee.",
            de=f"McAfee Total Protection für {_devices(devices)['de']}: digitale Lizenz mit E-Mail und Aktivierung im McAfee-Portal.",
            es=f"McAfee Total Protection para {_devices(devices)['es']}: licencia digital con email y activación en el portal McAfee.",
        ),
        pills=_pills("McAfee", devices),
        features_title=L(
            it="McAfee Total Protection",
            en="McAfee Total Protection",
            fr="McAfee Total Protection",
            de="McAfee Total Protection",
            es="McAfee Total Protection",
        ),
        features=_feats(
            "McAfee",
            L(
                it="Total Protection",
                en="Total Protection",
                fr="Total Protection",
                de="Total Protection",
                es="Total Protection",
            ),
            L(
                it="Sicurezza multi-device",
                en="Multi-device security",
                fr="Sécurité multi-appareils",
                de="Multi-Geräte-Schutz",
                es="Seguridad multi-dispositivo",
            ),
            L(it="Licenza digitale", en="Digital licence", fr="Licence numérique", de="Digitale Lizenz", es="Licencia digital"),
        ),
        faq=_faq_av("McAfee"),
    )


for slug, n in [
    ("mcafee-total-protection-1-device", 1),
    ("mcafee-total-protection-5-devices", 5),
    ("mcafee-total-protection-10-devices", 10),
]:
    _add_mcafee(slug, n)


# Fix ESET names (cleaner)
for slug, n, years in [
    ("eset-nod32-1-device", 1, 1),
    ("eset-nod32-2-devices", 2, 1),
    ("eset-nod32-3-devices", 3, 1),
    ("eset-nod32-5-devices", 5, 1),
    ("eset-nod32-10-devices", 10, 1),
    ("eset-nod32-1-device-2y", 1, 2),
]:
    PRODUCTS[slug]["name"] = L(
        **{
            lg: f"ESET NOD32 — {_devices(n)[lg]}"
            + (f" · {_year(years)[lg]}" if years > 1 else "")
            for lg in LANGS
        }
    )


def get_antivirus_content(slug):
    return PRODUCTS.get(slug)
