#!/usr/bin/env python3
"""
Rich product-page content for antivirus SKUs.
Structure mirrors flagship samples (M365 Personal): hero ambient + pills,
floating pricing card, bento features, steps, specs, FAQ — no invented reviews.
"""

from copy import deepcopy

from product_content_office import UI as OFFICE_UI
from lang_backfill import backfill_lang
from nl_translations import nl_text

LANGS = ("it", "en", "fr", "de", "es", "pt", "nl")


def L(**kwargs):
    # "pt" e' opzionale nelle call site esistenti: se assente, eredita il
    # valore "es" (lingua piu' vicina) invece di far esplodere il generatore.
    if "pt" not in kwargs:
        kwargs["pt"] = kwargs.get("es") or kwargs.get("en")
    if "nl" not in kwargs:
        kwargs["nl"] = kwargs.get("en")
    return {k: kwargs[k] for k in LANGS}


# Antivirus UI: same chrome as Office sample, vendor activation instead of setup.office.com
UI = deepcopy(OFFICE_UI)
_AV_OVERRIDES = {
    "it": {
        "apps_eyebrow": "In evidenza",
        "step2_body": "Ti inviamo la <strong>licenza / codice</strong> e le istruzioni via email, di solito entro pochi minuti dall'approvazione del pagamento.",
        "step3_body": "Attiva sul <strong>portale ufficiale del produttore</strong> con il codice ricevuto e segui le istruzioni nell'email.",
        "spec_cpu_body": "PC o dispositivi supportati dal produttore; verifica i requisiti aggiornati sulla scheda ufficiale del software.",
        "spec_os_body": "Windows, macOS, Android o iOS secondo le piattaforme supportate dal prodotto acquistato.",
        "spec_ram_body": "Requisiti tipici da pochi GB di RAM; consulta la documentazione del produttore per il titolo specifico.",
        "spec_disk_body": "Spazio libero sufficiente per l'installazione del client di sicurezza, come da requisiti del produttore.",
        "specs_note": "Valori orientativi; verifica sempre i requisiti aggiornati sul sito ufficiale del produttore prima dell'installazione.",
    },
    "en": {
        "apps_eyebrow": "Highlights",
        "step2_body": "We email the <strong>licence / key</strong> and instructions, usually within minutes after payment approval.",
        "step3_body": "Activate on the <strong>official vendor portal</strong> with the code received and follow the email instructions.",
        "spec_cpu_body": "PCs or devices supported by the vendor; check the latest requirements on the official product page.",
        "spec_os_body": "Windows, macOS, Android or iOS depending on platforms supported by the purchased product.",
        "spec_ram_body": "Typical requirements are a few GB of RAM; see vendor documentation for the specific title.",
        "spec_disk_body": "Enough free space to install the security client, per the vendor’s requirements.",
        "specs_note": "Indicative values; always check the vendor’s latest requirements before installing.",
    },
    "fr": {
        "apps_eyebrow": "Points clés",
        "step2_body": "Nous envoyons la <strong>licence / clé</strong> et les instructions par e-mail, en général quelques minutes après validation du paiement.",
        "step3_body": "Activez sur le <strong>portail officiel de l'éditeur</strong> avec le code reçu et suivez l'e-mail.",
        "spec_cpu_body": "PC ou appareils pris en charge par l'éditeur ; vérifiez la fiche officielle.",
        "spec_os_body": "Windows, macOS, Android ou iOS selon les plateformes supportées.",
        "spec_ram_body": "Quelques Go de RAM typiquement ; voir la doc de l'éditeur.",
        "spec_disk_body": "Espace libre suffisant pour le client de sécurité.",
        "specs_note": "Valeurs indicatives ; vérifiez toujours les exigences à jour de l'éditeur.",
    },
    "de": {
        "apps_eyebrow": "Highlights",
        "step2_body": "Wir senden <strong>Lizenz / Key</strong> und Anleitung per E-Mail, in der Regel wenige Minuten nach Zahlungsfreigabe.",
        "step3_body": "Aktivieren Sie im <strong>offiziellen Herstellerportal</strong> mit dem erhaltenen Code und folgen Sie der E-Mail.",
        "spec_cpu_body": "Vom Hersteller unterstützte PCs/Geräte; aktuelle Anforderungen auf der Produktseite prüfen.",
        "spec_os_body": "Windows, macOS, Android oder iOS je nach unterstützten Plattformen.",
        "spec_ram_body": "Typisch einige GB RAM; Herstellerdokumentation prüfen.",
        "spec_disk_body": "Ausreichend freier Speicher für den Sicherheits-Client.",
        "specs_note": "Richtwerte; stets aktuelle Herstelleranforderungen prüfen.",
    },
    "es": {
        "apps_eyebrow": "Destacados",
        "step2_body": "Enviamos la <strong>licencia / clave</strong> e instrucciones por email, normalmente en minutos tras aprobar el pago.",
        "step3_body": "Activa en el <strong>portal oficial del fabricante</strong> con el código recibido y sigue el email.",
        "spec_cpu_body": "PCs o dispositivos admitidos por el fabricante; consulta los requisitos oficiales.",
        "spec_os_body": "Windows, macOS, Android o iOS según las plataformas del producto.",
        "spec_ram_body": "Normalmente unos pocos GB de RAM; consulta la documentación del fabricante.",
        "spec_disk_body": "Espacio libre suficiente para el cliente de seguridad.",
        "specs_note": "Valores orientativos; comprueba siempre los requisitos actualizados del fabricante.",
    },
    "pt": {
        "apps_eyebrow": "Destaques",
        "step2_body": "Enviamos-te a <strong>licença / código</strong> e as instruções por email, normalmente em poucos minutos após a aprovação do pagamento.",
        "step3_body": "Ativa no <strong>portal oficial do fabricante</strong> com o código recebido e segue as instruções no email.",
        "spec_cpu_body": "PC ou dispositivos suportados pelo fabricante; verifica os requisitos atualizados na ficha oficial do software.",
        "spec_os_body": "Windows, macOS, Android ou iOS segundo as plataformas suportadas pelo produto adquirido.",
        "spec_ram_body": "Requisitos típicos a partir de poucos GB de RAM; consulta a documentação do fabricante para o produto específico.",
        "spec_disk_body": "Espaço livre suficiente para a instalação do cliente de segurança, segundo os requisitos do fabricante.",
        "specs_note": "Valores indicativos; verifica sempre os requisitos atualizados no site oficial do fabricante antes de instalar.",
    },
    "nl": {
        "apps_eyebrow": "Hoogtepunten",
        "step2_body": "Wij sturen u de <strong>licentie / code</strong> en de instructies per e-mail, meestal binnen enkele minuten na goedkeuring van de betaling.",
        "step3_body": "Activeer op het <strong>officiële portaal van de uitgever</strong> met de ontvangen code en volg de instructies in de e-mail.",
        "spec_cpu_body": "Pc of apparaten die de uitgever ondersteunt; controleer de actuele vereisten op de officiële productfiche.",
        "spec_os_body": "Windows, macOS, Android of iOS volgens de platforms van het gekochte product.",
        "spec_ram_body": "Typische vereisten vanaf enkele GB RAM; raadpleeg de documentatie van de uitgever voor het specifieke product.",
        "spec_disk_body": "Voldoende vrije ruimte voor de beveiligingsclient, volgens de vereisten van de uitgever.",
        "specs_note": "Richtwaarden; controleer altijd de actuele vereisten op de officiële site van de uitgever vóór de installatie.",
    },
}
for lg, ov in _AV_OVERRIDES.items():
    UI[lg].update(ov)


ICON_SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
ICON_LAPTOP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><path d="M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0 1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16"/></svg>'
ICON_EMAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>'
ICON_CHECK_CIRCLE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><path d="m9 12 2 2 4-4"/><circle cx="12" cy="12" r="10"/></svg>'
ICON_LOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'
ICON_GLOBE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>'
ICON_CLOUD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>'


def _eset_feats():
    return {
        "it": [
            (ICON_SHIELD, "blue", "Sicurezza", "Protezione antivirus proattiva", "Difesa multilivello avanzata contro virus, ransomware, phishing e minacce zero-day senza interruzioni."),
            (ICON_LAPTOP, "teal", "Prestazioni", "Impatto minimo sul sistema", "Massima reattività ed efficienza hardware: scansioni rapide e fluide, ideale anche per gaming e lavoro."),
            (ICON_EMAIL, "purple", "Consegna", "Invio istantaneo via email", "Codice licenza originale e guida passo-passo inviati subito via email dopo la conferma del pagamento."),
            (ICON_CHECK_CIRCLE, "dark", "Attivazione", "Portale ufficiale ESET", "Attivazione autentica e sicura tramite account ufficiale ESET HOME con aggiornamenti costanti inclusi."),
        ],
        "en": [
            (ICON_SHIELD, "blue", "Security", "Proactive antivirus protection", "Advanced multi-layered defence against viruses, ransomware, phishing, and zero-day threats."),
            (ICON_LAPTOP, "teal", "Performance", "Minimal system impact", "High efficiency and low footprint: fast, smooth scanning, perfect for gaming and multitasking."),
            (ICON_EMAIL, "purple", "Delivery", "Instant email delivery", "Genuine licence key and step-by-step instructions sent directly to your inbox after purchase."),
            (ICON_CHECK_CIRCLE, "dark", "Activation", "Official ESET portal", "Authentic, secure activation via official ESET HOME account with regular protection updates."),
        ],
        "fr": [
            (ICON_SHIELD, "blue", "Sécurité", "Protection antivirus proactive", "Défense multicouche avancée contre les virus, ransomwares, phishing et menaces en ligne."),
            (ICON_LAPTOP, "teal", "Performance", "Impact minimal sur le système", "Faible empreinte et fluidité maximale : analyses rapides, idéal pour le travail et le jeu."),
            (ICON_EMAIL, "purple", "Livraison", "Envoi instantané par e-mail", "Clé de licence authentique et guide d'installation envoyés par e-mail dès validation."),
            (ICON_CHECK_CIRCLE, "dark", "Activation", "Portail officiel ESET", "Activation officielle et sécurisée sur ESET HOME avec mises à jour de sécurité incluses."),
        ],
        "de": [
            (ICON_SHIELD, "blue", "Sicherheit", "Proaktiver Virenschutz", "Mehrschichtige Abwehr vor Viren, Ransomware, Phishing und neuesten Bedrohungen."),
            (ICON_LAPTOP, "teal", "Leistung", "Geringe Systembelastung", "Minimaler Ressourcenverbrauch: schnelle, unauffällige Scans, ideal für Arbeit und Gaming."),
            (ICON_EMAIL, "purple", "Lieferung", "Sofortige E-Mail-Zustellung", "Originaler Lizenzschlüssel und Schritt-für-Schritt-Anleitung direkt nach dem Kauf per E-Mail."),
            (ICON_CHECK_CIRCLE, "dark", "Aktivierung", "Offizielles ESET-Portal", "Sichere Aktivierung über das offizielle ESET HOME Portal mit fortlaufenden Updates."),
        ],
        "es": [
            (ICON_SHIELD, "blue", "Seguridad", "Protección antivirus proactiva", "Defensa multicapa avanzada contra virus, ransomware, phishing y amenazas web."),
            (ICON_LAPTOP, "teal", "Rendimiento", "Impacto mínimo en el sistema", "Máxima eficiencia y bajo consumo de recursos: análisis rápidos, ideal para trabajo y juegos."),
            (ICON_EMAIL, "purple", "Entrega", "Envío inmediato por email", "Clave de licencia original e instrucciones claras enviadas por email tras el pago."),
            (ICON_CHECK_CIRCLE, "dark", "Activación", "Portal oficial de ESET", "Activación oficial y segura en ESET HOME con actualizaciones automáticas incluidas."),
        ],
        "pt": [
            (ICON_SHIELD, "blue", "Segurança", "Proteção antivírus proativa", "Defesa avançada em várias camadas contra vírus, ransomware, phishing e ameaças de dia zero sem interrupções."),
            (ICON_LAPTOP, "teal", "Desempenho", "Impacto mínimo no sistema", "Máxima eficiência e baixo consumo de recursos: análises rápidas e fluidas, ideal também para jogos e trabalho."),
            (ICON_EMAIL, "purple", "Entrega", "Envio instantâneo por email", "Código de licença original e guia passo a passo enviados de imediato por email após a confirmação do pagamento."),
            (ICON_CHECK_CIRCLE, "dark", "Ativação", "Portal oficial ESET", "Ativação autêntica e segura através da conta oficial ESET HOME com atualizações constantes incluídas."),
        ],
    }


def _eset_keypoints():
    return {
        "it": [
            "Protezione proattiva contro virus, malware e ransomware",
            "Scansioni ultra-rapide a basso impatto sulle risorse",
            "Codice licenza originale e guida inviati via email",
            "Attivazione ufficiale e download da portale ESET",
        ],
        "en": [
            "Proactive protection against viruses, malware, and ransomware",
            "Ultra-fast scans with minimal system impact",
            "Genuine license key and guide delivered by email",
            "Official activation and downloads via ESET portal",
        ],
        "fr": [
            "Protection proactive contre virus, malwares et ransomwares",
            "Analyses ultra-rapides à faible impact système",
            "Clé de licence originale et guide envoyés par e-mail",
            "Activation officielle et téléchargement sur le portail ESET",
        ],
        "de": [
            "Proaktiver Schutz vor Viren, Malware und Ransomware",
            "Ultraschnelle Scans mit minimaler Systembelastung",
            "Originaler Lizenzschlüssel und Anleitung per E-Mail",
            "Offizielle Aktivierung und Download über das ESET-Portal",
        ],
        "es": [
            "Protección proactiva contra virus, malware y ransomware",
            "Análisis ultrarrápidos con mínimo impacto en el sistema",
            "Clave de licencia original y guía enviadas por email",
            "Activación oficial y descarga desde el portal ESET",
        ],
        "pt": [
            "Proteção proativa contra vírus, malware e ransomware",
            "Análises ultrarrápidas com mínimo impacto no sistema",
            "Código de licença original e guia enviados por email",
            "Ativação oficial e download a partir do portal ESET",
        ],
    }


SPECS_TABLE_ESET = {
    "it": {
        "eyebrow": "Requisiti di sistema",
        "title": "Requisiti di sistema e compatibilità",
        "sub": "Valori orientativi; verifica sempre i requisiti aggiornati sul sito ufficiale del produttore prima dell'installazione.",
        "caption": "Requisiti di sistema per ESET NOD32 Antivirus",
        "col_req": "Requisito",
        "col_det": "Dettaglio Tecnico",
        "rows": [
            ("Sistema operativo", "Windows 10 / 11, macOS 11+, Android 8.0+"),
            ("Processore", "1 GHz a 32-bit (x86) / 64-bit (x64)"),
            ("Memoria RAM", "1 GB minimo"),
            ("Spazio su disco", "320 MB liberi"),
        ],
    },
    "en": {
        "eyebrow": "System requirements",
        "title": "System requirements and compatibility",
        "sub": "Indicative values; always check the vendor’s latest requirements before installing.",
        "caption": "System requirements for ESET NOD32 Antivirus",
        "col_req": "Requirement",
        "col_det": "Technical Details",
        "rows": [
            ("Operating system", "Windows 10 / 11, macOS 11+, Android 8.0+"),
            ("Processor", "1 GHz 32-bit (x86) / 64-bit (x64)"),
            ("RAM memory", "1 GB minimum"),
            ("Disk space", "320 MB free space"),
        ],
    },
    "fr": {
        "eyebrow": "Configuration requise",
        "title": "Configuration requise et compatibilité",
        "sub": "Valeurs indicatives ; vérifiez toujours les exigences à jour de l'éditeur.",
        "caption": "Configuration requise pour ESET NOD32 Antivirus",
        "col_req": "Exigence",
        "col_det": "Détail technique",
        "rows": [
            ("Système d'exploitation", "Windows 10 / 11, macOS 11+, Android 8.0+"),
            ("Processeur", "1 GHz 32 bits (x86) / 64 bits (x64)"),
            ("Mémoire RAM", "1 Go minimum"),
            ("Espace disque", "320 Mo libres"),
        ],
    },
    "de": {
        "eyebrow": "Systemanforderungen",
        "title": "Systemanforderungen und Kompatibilität",
        "sub": "Richtwerte; stets aktuelle Herstelleranforderungen prüfen.",
        "caption": "Systemanforderungen für ESET NOD32 Antivirus",
        "col_req": "Anforderung",
        "col_det": "Technische Details",
        "rows": [
            ("Betriebssystem", "Windows 10 / 11, macOS 11+, Android 8.0+"),
            ("Prozessor", "1 GHz 32-Bit (x86) / 64-Bit (x64)"),
            ("Arbeitsspeicher", "1 GB mindestens"),
            ("Festplattenspeicher", "320 MB freier Speicher"),
        ],
    },
    "es": {
        "eyebrow": "Requisitos del sistema",
        "title": "Requisitos del sistema y compatibilidad",
        "sub": "Valores orientativos; comprueba siempre los requisitos actualizados del fabricante.",
        "caption": "Requisitos del sistema para ESET NOD32 Antivirus",
        "col_req": "Requisito",
        "col_det": "Detalle técnico",
        "rows": [
            ("Sistema operativo", "Windows 10 / 11, macOS 11+, Android 8.0+"),
            ("Procesador", "1 GHz de 32 bits (x86) / 64 bits (x64)"),
            ("Memoria RAM", "1 GB mínimo"),
            ("Espacio en disco", "320 MB libres"),
        ],
    },
    "pt": {
        "eyebrow": "Requisitos do sistema",
        "title": "Requisitos do sistema e compatibilidade",
        "sub": "Valores indicativos; verifica sempre os requisitos atualizados do fabricante.",
        "caption": "Requisitos do sistema para ESET NOD32 Antivirus",
        "col_req": "Requisito",
        "col_det": "Detalhe técnico",
        "rows": [
            ("Sistema operativo", "Windows 10 / 11, macOS 11+, Android 8.0+"),
            ("Processador", "1 GHz a 32 bits (x86) / 64 bits (x64)"),
            ("Memória RAM", "1 GB mínimo"),
            ("Espaço em disco", "320 MB livres"),
        ],
    },
    "nl": {
        "eyebrow": "Systeemvereisten",
        "title": "Systeemvereisten en compatibiliteit",
        "sub": "Richtwaarden; controleer altijd de actuele vereisten van de uitgever.",
        "caption": "Systeemvereisten voor ESET NOD32 Antivirus",
        "col_req": "Vereiste",
        "col_det": "Technisch detail",
        "rows": [
            ("Besturingssysteem", "Windows 10 / 11, macOS 11+, Android 8.0+"),
            ("Processor", "1 GHz 32-bit (x86) / 64-bit (x64)"),
            ("RAM-geheugen", "Minimaal 1 GB"),
            ("Schijfruimte", "320 MB vrij"),
        ],
    },
}


def _steps_for_brand(portal):
    return {
        "it": [
            ("Completa l'ordine", "Scegli il piano e procedi con il pagamento sicuro tramite carta o PayPal."),
            ("Ricevi la licenza via email", "Ti inviamo il codice licenza originale e la guida di installazione via email in pochi minuti."),
            ("Attiva sul portale ufficiale", f"Attiva sul <strong>{portal['it']}</strong> con il codice ricevuto e installa il software ufficiale in tutta sicurezza."),
        ],
        "en": [
            ("Complete your order", "Select your plan and complete the secure payment by card or PayPal."),
            ("Receive licence by email", "We email your genuine licence key and setup instructions within minutes."),
            ("Activate on official portal", f"Activate on the <strong>{portal['en']}</strong> with your received key and download the official client safely."),
        ],
        "fr": [
            ("Finalisez la commande", "Choisissez votre offre et réglez en toute sécurité par carte bancaire ou PayPal."),
            ("Recevez la clé par e-mail", "Nous vous envoyons votre clé de licence officielle et le guide d'installation par e-mail en quelques minutes."),
            ("Activez sur le portail officiel", f"Activez sur le <strong>{portal['fr']}</strong> avec votre clé et installez l'antivirus officiel."),
        ],
        "de": [
            ("Bestellung abschließen", "Wählen Sie Ihren Plan und zahlen Sie sicher per Karte oder PayPal."),
            ("Lizenz per E-Mail erhalten", "Wir senden Ihren originalen Lizenzschlüssel und die Anleitung innerhalb weniger Minuten per E-Mail."),
            ("Im offiziellen Portal aktivieren", f"Aktivieren Sie im <strong>{portal['de']}</strong> mit Ihrem Key und installieren Sie die offizielle Software."),
        ],
        "es": [
            ("Completa el pedido", "Elige tu plan y realiza el pago seguro con tarjeta o PayPal."),
            ("Recibe la clave por email", "Te enviamos la clave de licencia original e instrucciones claras por email en pocos minutos."),
            ("Activa en el portal oficial", f"Activa en el <strong>{portal['es']}</strong> con tu código e instala el software oficial de forma segura."),
        ],
        "pt": [
            ("Completa a encomenda", "Escolhe o plano e conclui o pagamento seguro com cartão ou PayPal."),
            ("Recebe a licença por email", "Enviamos-te o código de licença original e o guia de instalação por email em poucos minutos."),
            ("Ativa no portal oficial", f"Ativa no <strong>{portal['pt']}</strong> com o código recebido e instala o software oficial com toda a segurança."),
        ],
        "nl": [
            ("Rond de bestelling af", "Kies het plan en rond de veilige betaling af met kaart of PayPal."),
            ("Ontvang de licentie per e-mail", "Wij sturen u de originele licentiecode en de installatiegids binnen enkele minuten per e-mail."),
            ("Activeer op het officiële portaal", f"Activeer op het <strong>{portal['nl']}</strong> met de ontvangen code en installeer de officiële software veilig."),
        ],
    }


def _devices(n):
    return L(
        it=f"{n} dispositivo" if n == 1 else f"{n} dispositivi",
        en=f"{n} device" if n == 1 else f"{n} devices",
        fr=f"{n} appareil" if n == 1 else f"{n} appareils",
        de=f"{n} Gerät" if n == 1 else f"{n} Geräte",
        es=f"{n} dispositivo" if n == 1 else f"{n} dispositivos",
        pt=f"{n} dispositivo" if n == 1 else f"{n} dispositivos",
        nl=f"{n} apparaat" if n == 1 else f"{n} apparaten",
    )


def _year(years=1):
    return L(
        it="1 anno" if years == 1 else f"{years} anni",
        en="1 year" if years == 1 else f"{years} years",
        fr="1 an" if years == 1 else f"{years} ans",
        de="1 Jahr" if years == 1 else f"{years} Jahre",
        es="1 año" if years == 1 else f"{years} años",
        pt="1 ano" if years == 1 else f"{years} anos",
        nl="1 jaar" if years == 1 else f"{years} jaar",
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
    specs_table=None,
    steps=None,
    keypoints=None,
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
                    "pt": "sem renovação automática",
                    "nl": "zonder automatische verlenging",
                }[lg]
            )
        eyebrow[lg] = " · ".join(parts)

    res = {
        "apps": [],
        "name": name,
        "title_html": L(
            it=f"{brand} <span>{title_span['it']}</span>",
            en=f"{brand} <span>{title_span['en']}</span>",
            fr=f"{brand} <span>{title_span['fr']}</span>",
            de=f"{brand} <span>{title_span['de']}</span>",
            es=f"{brand} <span>{title_span['es']}</span>",
            pt=f"{brand} <span>{title_span.get('pt', title_span['es'])}</span>",
            nl=f"{brand} <span>{title_span.get('nl', title_span['en'])}</span>",
        ),
        "eyebrow": eyebrow,
        "desc": desc,
        "pills": pills,
        "features_title": features_title,
        "features": features,
        "apps_title": L(it="", en="", fr="", de="", es=""),
        "faq": faq,
    }
    if specs_table is not None:
        res["specs_table"] = specs_table
    if steps is not None:
        res["steps"] = steps
    if keypoints is not None:
        res["keypoints"] = keypoints
    return res


# Helper for specs tables across antivirus products
def _specs_table_helper(product_title, rows_by_lang):
    return {
        "it": {
            "eyebrow": "Requisiti di sistema",
            "title": "Requisiti di sistema e compatibilità",
            "sub": "Valori orientativi; verifica sempre i requisiti aggiornati sul sito ufficiale del produttore prima dell'installazione.",
            "caption": f"Requisiti di sistema per {product_title}",
            "col_req": "Requisito",
            "col_det": "Dettaglio Tecnico",
            "rows": rows_by_lang["it"],
        },
        "en": {
            "eyebrow": "System requirements",
            "title": "System requirements and compatibility",
            "sub": "Indicative values; always check the vendor’s latest requirements before installing.",
            "caption": f"System requirements for {product_title}",
            "col_req": "Requirement",
            "col_det": "Technical Details",
            "rows": rows_by_lang["en"],
        },
        "fr": {
            "eyebrow": "Configuration requise",
            "title": "Configuration requise et compatibilité",
            "sub": "Valeurs indicatives ; vérifiez toujours les exigences à jour de l'éditeur.",
            "caption": f"Configuration requise pour {product_title}",
            "col_req": "Exigence",
            "col_det": "Détail technique",
            "rows": rows_by_lang["fr"],
        },
        "de": {
            "eyebrow": "Systemanforderungen",
            "title": "Systemanforderungen und Kompatibilität",
            "sub": "Richtwerte; stets aktuelle Herstelleranforderungen prüfen.",
            "caption": f"Systemanforderungen für {product_title}",
            "col_req": "Anforderung",
            "col_det": "Technische Details",
            "rows": rows_by_lang["de"],
        },
        "es": {
            "eyebrow": "Requisitos del sistema",
            "title": "Requisitos del sistema y compatibilidad",
            "sub": "Valores orientativos; comprueba siempre los requisitos actualizados del fabricante.",
            "caption": f"Requisitos del sistema para {product_title}",
            "col_req": "Requisito",
            "col_det": "Detalle técnico",
            "rows": rows_by_lang["es"],
        },
        "pt": {
            "eyebrow": "Requisitos do sistema",
            "title": "Requisitos do sistema e compatibilidade",
            "sub": "Valores indicativos; verifica sempre os requisitos atualizados do fabricante.",
            "caption": f"Requisitos do sistema para {product_title}",
            "col_req": "Requisito",
            "col_det": "Detalhe técnico",
            "rows": rows_by_lang.get("pt", rows_by_lang["es"]),
        },
        "nl": {
            "eyebrow": "Systeemvereisten",
            "title": "Systeemvereisten en compatibiliteit",
            "sub": "Indicatieve waarden; controleer altijd de actuele eisen van de fabrikant voor installatie.",
            "caption": f"Systeemvereisten voor {product_title}",
            "col_req": "Vereiste",
            "col_det": "Technische details",
            # Le righe non fornite in olandese passano da nl_text(), che
            # traduce ricorsivamente le tuple (etichetta, dettaglio).
            "rows": nl_text(rows_by_lang.get("nl", rows_by_lang["en"])),
        },
    }


SPECS_TABLE_NORTON = _specs_table_helper("Norton 360", {
    "it": [
        ("Sistema operativo", "Windows 11 / 10 / 8.1, macOS (versione attuale e 2 prec.), Android 8.0+, iOS"),
        ("Processore", "1 GHz minimo (x86 / x64)"),
        ("Memoria RAM", "512 MB (32-bit) / 1 GB (64-bit), 2 GB su macOS"),
        ("Spazio su disco", "300 MB di spazio libero"),
    ],
    "en": [
        ("Operating system", "Windows 11 / 10 / 8.1, macOS (current and 2 prior), Android 8.0+, iOS"),
        ("Processor", "1 GHz minimum (x86 / x64)"),
        ("RAM memory", "512 MB (32-bit) / 1 GB (64-bit), 2 GB for macOS"),
        ("Disk space", "300 MB free space"),
    ],
    "fr": [
        ("Système d'exploitation", "Windows 11 / 10 / 8.1, macOS (actuel + 2 préc.), Android 8.0+, iOS"),
        ("Processeur", "1 GHz minimum (x86 / x64)"),
        ("Mémoire RAM", "512 Mo (32 bits) / 1 Go (64 bits), 2 Go sur macOS"),
        ("Espace disque", "300 Mo libres"),
    ],
    "de": [
        ("Betriebssystem", "Windows 11 / 10 / 8.1, macOS (aktuelle + 2 Vorversionen), Android 8.0+, iOS"),
        ("Prozessor", "1 GHz mindestens (x86 / x64)"),
        ("Arbeitsspeicher", "512 MB (32-Bit) / 1 GB (64-Bit), 2 GB für macOS"),
        ("Festplattenspeicher", "300 MB freier Speicher"),
    ],
    "es": [
        ("Sistema operativo", "Windows 11 / 10 / 8.1, macOS (actual y 2 anteriores), Android 8.0+, iOS"),
        ("Procesador", "1 GHz mínimo (x86 / x64)"),
        ("Memoria RAM", "512 MB (32 bits) / 1 GB (64 bits), 2 GB en macOS"),
        ("Espacio en disco", "300 MB libres"),
    ],
    "pt": [
        ("Sistema operativo", "Windows 11 / 10 / 8.1, macOS (atual e 2 anteriores), Android 8.0+, iOS"),
        ("Processador", "1 GHz mínimo (x86 / x64)"),
        ("Memória RAM", "512 MB (32 bits) / 1 GB (64 bits), 2 GB em macOS"),
        ("Espaço em disco", "300 MB livres"),
    ],
})

SPECS_TABLE_BITDEFENDER = _specs_table_helper("Bitdefender Antivirus Plus", {
    "it": [
        ("Sistema operativo", "Windows 11 / 10 / 8.1 / 7 con Service Pack 1"),
        ("Processore", "Intel Core 2 Duo (2 GHz) o processore equivalente"),
        ("Memoria RAM", "2 GB minimo"),
        ("Spazio su disco", "2.5 GB di spazio libero"),
    ],
    "en": [
        ("Operating system", "Windows 11 / 10 / 8.1 / 7 with Service Pack 1"),
        ("Processor", "Intel Core 2 Duo (2 GHz) or equivalent"),
        ("RAM memory", "2 GB minimum"),
        ("Disk space", "2.5 GB free space"),
    ],
    "fr": [
        ("Système d'exploitation", "Windows 11 / 10 / 8.1 / 7 avec Service Pack 1"),
        ("Processeur", "Intel Core 2 Duo (2 GHz) ou équivalent"),
        ("Mémoire RAM", "2 Go minimum"),
        ("Espace disque", "2,5 Go libres"),
    ],
    "de": [
        ("Betriebssystem", "Windows 11 / 10 / 8.1 / 7 mit Service Pack 1"),
        ("Prozessor", "Intel Core 2 Duo (2 GHz) oder gleichwertig"),
        ("Arbeitsspeicher", "2 GB mindestens"),
        ("Festplattenspeicher", "2,5 GB freier Speicher"),
    ],
    "es": [
        ("Sistema operativo", "Windows 11 / 10 / 8.1 / 7 con Service Pack 1"),
        ("Procesador", "Intel Core 2 Duo (2 GHz) o equivalente"),
        ("Memoria RAM", "2 GB mínimo"),
        ("Espacio en disco", "2.5 GB libres"),
    ],
    "pt": [
        ("Sistema operativo", "Windows 11 / 10 / 8.1 / 7 com Service Pack 1"),
        ("Processador", "Intel Core 2 Duo (2 GHz) ou equivalente"),
        ("Memória RAM", "2 GB mínimo"),
        ("Espaço em disco", "2,5 GB livres"),
    ],
})

SPECS_TABLE_KASPERSKY = _specs_table_helper("Kaspersky Security", {
    "it": [
        ("Sistema operativo", "Windows 11 / 10 / 8.1 / 7 SP1, macOS 11+, Android 8.0+, iOS"),
        ("Processore", "1 GHz a 32-bit (x86) o 64-bit (x64)"),
        ("Memoria RAM", "1 GB (32-bit) o 2 GB (64-bit)"),
        ("Spazio su disco", "1.5 GB di spazio libero"),
    ],
    "en": [
        ("Operating system", "Windows 11 / 10 / 8.1 / 7 SP1, macOS 11+, Android 8.0+, iOS"),
        ("Processor", "1 GHz 32-bit (x86) or 64-bit (x64)"),
        ("RAM memory", "1 GB (32-bit) or 2 GB (64-bit)"),
        ("Disk space", "1.5 GB free space"),
    ],
    "fr": [
        ("Système d'exploitation", "Windows 11 / 10 / 8.1 / 7 SP1, macOS 11+, Android 8.0+, iOS"),
        ("Processeur", "1 GHz 32 bits (x86) ou 64 bits (x64)"),
        ("Mémoire RAM", "1 Go (32 bits) ou 2 Go (64 bits)"),
        ("Espace disque", "1,5 Go libres"),
    ],
    "de": [
        ("Betriebssystem", "Windows 11 / 10 / 8.1 / 7 SP1, macOS 11+, Android 8.0+, iOS"),
        ("Prozessor", "1 GHz 32-Bit (x86) oder 64-Bit (x64)"),
        ("Arbeitsspeicher", "1 GB (32-Bit) oder 2 GB (64-Bit)"),
        ("Festplattenspeicher", "1,5 GB freier Speicher"),
    ],
    "es": [
        ("Sistema operativo", "Windows 11 / 10 / 8.1 / 7 SP1, macOS 11+, Android 8.0+, iOS"),
        ("Procesador", "1 GHz de 32 bits (x86) o 64 bits (x64)"),
        ("Memoria RAM", "1 GB (32 bits) o 2 GB (64 bits)"),
        ("Espacio en disco", "1.5 GB libres"),
    ],
    "pt": [
        ("Sistema operativo", "Windows 11 / 10 / 8.1 / 7 SP1, macOS 11+, Android 8.0+, iOS"),
        ("Processador", "1 GHz a 32 bits (x86) ou 64 bits (x64)"),
        ("Memória RAM", "1 GB (32 bits) ou 2 GB (64 bits)"),
        ("Espaço em disco", "1,5 GB livres"),
    ],
})

SPECS_TABLE_MCAFEE = _specs_table_helper("McAfee Total Protection", {
    "it": [
        ("Sistema operativo", "Windows 11 / 10 (64-bit), macOS 11+, Android 9.0+, iOS 15+"),
        ("Processore", "1 GHz a 64-bit (x64) o superiore"),
        ("Memoria RAM", "2 GB minimo"),
        ("Spazio su disco", "1.3 GB di spazio libero"),
    ],
    "en": [
        ("Operating system", "Windows 11 / 10 (64-bit), macOS 11+, Android 9.0+, iOS 15+"),
        ("Processor", "1 GHz 64-bit (x64) or higher"),
        ("RAM memory", "2 GB minimum"),
        ("Disk space", "1.3 GB free space"),
    ],
    "fr": [
        ("Système d'exploitation", "Windows 11 / 10 (64 bits), macOS 11+, Android 9.0+, iOS 15+"),
        ("Processeur", "1 GHz 64 bits (x64) ou supérieur"),
        ("Mémoire RAM", "2 Go minimum"),
        ("Espace disque", "1,3 Go libres"),
    ],
    "de": [
        ("Betriebssystem", "Windows 11 / 10 (64-Bit), macOS 11+, Android 9.0+, iOS 15+"),
        ("Prozessor", "1 GHz 64-Bit (x64) oder höher"),
        ("Arbeitsspeicher", "2 GB mindestens"),
        ("Festplattenspeicher", "1,3 GB freier Speicher"),
    ],
    "es": [
        ("Sistema operativo", "Windows 11 / 10 (64 bits), macOS 11+, Android 9.0+, iOS 15+"),
        ("Procesador", "1 GHz de 64 bits (x64) o superior"),
        ("Memoria RAM", "2 GB mínimo"),
        ("Espacio en disco", "1.3 GB libres"),
    ],
    "pt": [
        ("Sistema operativo", "Windows 11 / 10 (64 bits), macOS 11+, Android 9.0+, iOS 15+"),
        ("Processador", "1 GHz a 64 bits (x64) ou superior"),
        ("Memória RAM", "2 GB mínimo"),
        ("Espaço em disco", "1,3 GB livres"),
    ],
})


def _norton_feats(edition, cloud):
    return {
        "it": [
            (ICON_SHIELD, "blue", "Sicurezza", "Protezione in tempo reale multilivello", "Difesa proattiva continua contro virus, malware, ransomware e minacce di hacking su tutti i tuoi dispositivi."),
            (ICON_LOCK, "teal", "Privacy", "Secure VPN e crittografia avanzata", "Naviga in totale anonimato su reti Wi-Fi pubbliche e proteggi password e informazioni bancarie da occhi indiscreti."),
            (ICON_CLOUD, "purple", "Backup", f"Backup cloud sicuro per PC ({cloud})", f"Spazio cloud protetto da {cloud} per salvare automaticamente file importanti e documenti contro guasti hardware o ransomware."),
            (ICON_CHECK_CIRCLE, "dark", "Attivazione", "Portale ufficiale My Norton", "Attivazione sicura con licenza autentica gestita tramite account ufficiale Norton con aggiornamenti continui inclusi."),
        ],
        "en": [
            (ICON_SHIELD, "blue", "Security", "Real-time multi-layered protection", "Continuous proactive defence against viruses, malware, ransomware, and hacking threats across all your devices."),
            (ICON_LOCK, "teal", "Privacy", "Secure VPN and advanced encryption", "Browse anonymously on public Wi-Fi networks and protect your passwords and banking data from prying eyes."),
            (ICON_CLOUD, "purple", "Backup", f"Secure PC cloud backup ({cloud})", f"{cloud} dedicated secure cloud storage to automatically back up critical files against hardware failure or ransomware."),
            (ICON_CHECK_CIRCLE, "dark", "Activation", "Official My Norton portal", "Authentic activation managed via official Norton account with continuous security updates included."),
        ],
        "fr": [
            (ICON_SHIELD, "blue", "Sécurité", "Protection multicouche en temps réel", "Défense proactive continue contre les virus, malwares, ransomwares et tentatives de piratage sur tous vos appareils."),
            (ICON_LOCK, "teal", "Confidentialité", "Secure VPN et chiffrement avancé", "Naviguez en toute confidentialité sur les réseaux Wi-Fi publics et protégez vos mots de passe et données bancaires."),
            (ICON_CLOUD, "purple", "Sauvegarde", f"Sauvegarde cloud pour PC ({cloud})", f"Espace cloud sécurisé de {cloud} pour sauvegarder vos documents essentiels contre les pannes ou ransomwares."),
            (ICON_CHECK_CIRCLE, "dark", "Activation", "Portail officiel My Norton", "Activation sécurisée et gestion de licence via votre compte officiel Norton avec mises à jour incluses."),
        ],
        "de": [
            (ICON_SHIELD, "blue", "Sicherheit", "Mehrschichtiger Echtzeitschutz", "Fortlaufende proaktive Abwehr vor Viren, Malware, Ransomware und Hacking-Angriffen auf all Ihren Geräten."),
            (ICON_LOCK, "teal", "Privatsphäre", "Secure VPN und starke Verschlüsselung", "Surfen Sie anonym in öffentlichen WLAN-Netzen und schützen Sie Passwörter sowie Bankdaten vor fremdem Zugriff."),
            (ICON_CLOUD, "purple", "Backup", f"Sicheres PC-Cloud-Backup ({cloud})", f"{cloud} geschützter Cloud-Speicher zur automatischen Sicherung wichtiger Daten vor Hardware-Defekten oder Ransomware."),
            (ICON_CHECK_CIRCLE, "dark", "Aktivierung", "Offizielles My Norton Portal", "Sichere Aktivierung über das offizielle Norton-Konto mit zentraler Verwaltung und regelmäßigen Updates."),
        ],
        "es": [
            (ICON_SHIELD, "blue", "Seguridad", "Protección multicapa en tiempo real", "Defensa proactiva continua contra virus, malware, ransomware e intentos de hackeo en todos tus dispositivos."),
            (ICON_LOCK, "teal", "Privacidad", "Secure VPN y cifrado avanzado", "Navega con total privacidad en redes Wi-Fi públicas y protege tus contraseñas y datos bancarios de accesos no autorizados."),
            (ICON_CLOUD, "purple", "Copia de seguridad", f"Copia de seguridad en la nube ({cloud})", f"Espacio en la nube de {cloud} para respaldar automáticamente archivos clave ante fallos de disco o ransomware."),
            (ICON_CHECK_CIRCLE, "dark", "Activación", "Portal oficial My Norton", "Activación segura gestionada en tu cuenta oficial de Norton con actualizaciones automáticas incluidas."),
        ],
        "pt": [
            (ICON_SHIELD, "blue", "Segurança", "Proteção multicamada em tempo real", "Defesa proativa contínua contra vírus, malware, ransomware e tentativas de hacking em todos os teus dispositivos."),
            (ICON_LOCK, "teal", "Privacidade", "Secure VPN e encriptação avançada", "Navega com total anonimato em redes Wi-Fi públicas e protege as tuas palavras-passe e dados bancários de acessos não autorizados."),
            (ICON_CLOUD, "purple", "Cópia de segurança", f"Cópia de segurança na cloud ({cloud})", f"Espaço na cloud de {cloud} para guardar automaticamente ficheiros importantes contra falhas de disco ou ransomware."),
            (ICON_CHECK_CIRCLE, "dark", "Ativação", "Portal oficial My Norton", "Ativação segura gerida na tua conta oficial da Norton com atualizações automáticas incluídas."),
        ],
    }


def _norton_keypoints(edition, devices, cloud):
    d_label_it = "1 dispositivo" if devices == 1 else f"{devices} dispositivi"
    d_label_en = "1 device" if devices == 1 else f"{devices} devices"
    d_label_fr = "1 appareil" if devices == 1 else f"{devices} appareils"
    d_label_de = "1 Gerät" if devices == 1 else f"{devices} Geräte"
    d_label_es = "1 dispositivo" if devices == 1 else f"{devices} dispositivos"
    d_label_pt = "1 dispositivo" if devices == 1 else f"{devices} dispositivos"
    return {
        "it": [
            f"Protezione completa da virus, malware e ransomware ({d_label_it})",
            "Secure VPN illimitata per privacy e sicurezza delle connessioni",
            f"Backup cloud sicuro per PC ({cloud}) contro la perdita di file",
            "Attivazione ufficiale e gestione account su My Norton",
        ],
        "en": [
            f"Complete virus, malware, and ransomware protection ({d_label_en})",
            "Unlimited Secure VPN for privacy and connection safety",
            f"Secure PC cloud backup ({cloud}) against data loss",
            "Official activation and account management on My Norton",
        ],
        "fr": [
            f"Protection complète contre virus, malwares et ransomwares ({d_label_fr})",
            "Secure VPN illimité pour la confidentialité de vos connexions",
            f"Sauvegarde cloud sécurisée pour PC ({cloud}) contre la perte de données",
            "Activation officielle et gestion sur My Norton",
        ],
        "de": [
            f"Kompletter Schutz vor Viren, Malware und Ransomware ({d_label_de})",
            "Unbegrenztes Secure VPN für Privatsphäre und sichere Verbindungen",
            f"Sicheres PC-Cloud-Backup ({cloud}) gegen Datenverlust",
            "Offizielle Aktivierung und Kontoverwaltung auf My Norton",
        ],
        "es": [
            f"Protección completa contra virus, malware y ransomware ({d_label_es})",
            "Secure VPN ilimitada para privacidad y conexiones seguras",
            f"Copia de seguridad en la nube ({cloud}) contra pérdida de datos",
            "Activación oficial y gestión de cuenta en My Norton",
        ],
        "pt": [
            f"Proteção completa contra vírus, malware e ransomware ({d_label_pt})",
            "Secure VPN ilimitada para privacidade e segurança das ligações",
            f"Cópia de segurança na cloud ({cloud}) contra a perda de ficheiros",
            "Ativação oficial e gestão de conta em My Norton",
        ],
    }


def _bitdefender_feats():
    return {
        "it": [
            (ICON_SHIELD, "blue", "Sicurezza", "Protezione anti-malware pluripremiata", "Difesa proattiva continua contro qualsiasi minaccia informatica: virus, trojan, ransomware e attacchi zero-day."),
            (ICON_LAPTOP, "teal", "Prestazioni", "Tecnologia Bitdefender Photon", "Adatta l'uso delle risorse all'hardware del computer, garantendo la massima velocità senza alcun rallentamento."),
            (ICON_GLOBE, "purple", "Web", "Navigazione sicura e anti-phishing", "Filtro web avanzato che blocca siti fraudolenti, tentativi di truffa finanziaria e download pericolosi in tempo reale."),
            (ICON_CHECK_CIRCLE, "dark", "Attivazione", "Portale ufficiale Bitdefender Central", "Gestione centralizzata dei dispositivi e installazione rapida tramite account ufficiale Bitdefender con aggiornamenti inclusi."),
        ],
        "en": [
            (ICON_SHIELD, "blue", "Security", "Award-winning anti-malware protection", "Continuous proactive defence against all digital threats: viruses, trojans, ransomware, and zero-day exploits."),
            (ICON_LAPTOP, "teal", "Performance", "Bitdefender Photon technology", "Adapts to your hardware configuration to save system resources and deliver peak computing speed."),
            (ICON_GLOBE, "purple", "Web", "Safe browsing and anti-phishing", "Advanced web filter blocking fraudulent websites, financial scam attempts, and unsafe downloads in real time."),
            (ICON_CHECK_CIRCLE, "dark", "Activation", "Official Bitdefender Central portal", "Centralized device management and fast setup via official Bitdefender account with continuous updates."),
        ],
        "fr": [
            (ICON_SHIELD, "blue", "Sécurité", "Protection anti-malware primée", "Défense proactive contre toutes les menaces numériques : virus, chevaux de Troie, ransomwares et attaques zero-day."),
            (ICON_LAPTOP, "teal", "Performance", "Technologie Bitdefender Photon", "S'adapte à la configuration de votre matériel pour préserver les ressources et maintenir une fluidité maximale."),
            (ICON_GLOBE, "purple", "Web", "Navigation sécurisée et anti-phishing", "Filtrage web avancé bloquant les sites frauduleux, les tentatives d'escroquerie et les téléchargements suspects."),
            (ICON_CHECK_CIRCLE, "dark", "Activation", "Portail officiel Bitdefender Central", "Gestion centralisée de vos appareils et installation guidée via le compte officiel Bitdefender avec mises à jour."),
        ],
        "de": [
            (ICON_SHIELD, "blue", "Sicherheit", "Prämierter Anti-Malware-Schutz", "Proaktive Abwehr aller digitalen Bedrohungen: Viren, Trojaner, Ransomware und Zero-Day-Schwachstellen."),
            (ICON_LAPTOP, "teal", "Leistung", "Bitdefender Photon Technologie", "Passt sich der Hardware an, um Systemressourcen zu schonen und höchste Arbeits- und Gaming-Geschwindigkeit zu sichern."),
            (ICON_GLOBE, "purple", "Web", "Sicheres Surfen und Anti-Phishing", "Fortschrittlicher Webfilter zum Blockieren betrügerischer Seiten, Phishing-Versuche und gefährlicher Downloads."),
            (ICON_CHECK_CIRCLE, "dark", "Aktivierung", "Offizielles Bitdefender Central Portal", "Zentrale Geräteverwaltung und schnelle Installation über das offizielle Bitdefender-Konto mit laufenden Updates."),
        ],
        "es": [
            (ICON_SHIELD, "blue", "Seguridad", "Protección anti-malware premiada", "Defensa proactiva contra todas las amenazas digitales: virus, troyanos, ransomware y ataques de día cero."),
            (ICON_LAPTOP, "teal", "Rendimiento", "Tecnología Bitdefender Photon", "Se adapta al hardware de tu equipo para optimizar el rendimiento y garantizar la máxima rapidez sin bloqueos."),
            (ICON_GLOBE, "purple", "Web", "Navegación segura y anti-phishing", "Filtro web avanzado que bloquea sitios fraudulentos, estafas financieras y descargas peligrosas en tiempo real."),
            (ICON_CHECK_CIRCLE, "dark", "Activación", "Portal oficial Bitdefender Central", "Gestión centralizada de dispositivos e instalación sencilla mediante cuenta oficial de Bitdefender con actualizaciones."),
        ],
        "pt": [
            (ICON_SHIELD, "blue", "Segurança", "Proteção antimalware premiada", "Defesa proativa contínua contra todas as ameaças digitais: vírus, trojans, ransomware e ataques de dia zero."),
            (ICON_LAPTOP, "teal", "Desempenho", "Tecnologia Bitdefender Photon", "Adapta o uso de recursos ao hardware do computador, garantindo a máxima velocidade sem qualquer lentidão."),
            (ICON_GLOBE, "purple", "Web", "Navegação segura e anti-phishing", "Filtro web avançado que bloqueia sites fraudulentos, tentativas de fraude financeira e downloads perigosos em tempo real."),
            (ICON_CHECK_CIRCLE, "dark", "Ativação", "Portal oficial Bitdefender Central", "Gestão centralizada dos dispositivos e instalação rápida através da conta oficial Bitdefender com atualizações incluídas."),
        ],
    }


def _bitdefender_keypoints(devices):
    d_label_it = "1 dispositivo" if devices == 1 else f"{devices} dispositivi"
    d_label_en = "1 device" if devices == 1 else f"{devices} devices"
    d_label_fr = "1 appareil" if devices == 1 else f"{devices} appareils"
    d_label_de = "1 Gerät" if devices == 1 else f"{devices} Geräte"
    d_label_es = "1 dispositivo" if devices == 1 else f"{devices} dispositivos"
    d_label_pt = "1 dispositivo" if devices == 1 else f"{devices} dispositivos"
    return {
        "it": [
            f"Protezione anti-malware in tempo reale ({d_label_it})",
            "Tecnologia Photon per scansioni veloci a zero rallentamenti",
            "Filtro web proattivo contro phishing, truffe e siti malevoli",
            "Gestione e attivazione ufficiale su Bitdefender Central",
        ],
        "en": [
            f"Real-time anti-malware protection ({d_label_en})",
            "Photon technology for fast scans with zero slowdowns",
            "Proactive web shield against phishing and malicious websites",
            "Official device management and activation on Bitdefender Central",
        ],
        "fr": [
            f"Protection anti-malware en temps réel ({d_label_fr})",
            "Technologie Photon pour des analyses rapides sans ralentissement",
            "Filtre web proactif contre le phishing et les sites malveillants",
            "Gestion et activation officielle sur Bitdefender Central",
        ],
        "de": [
            f"Echtzeit-Schutz vor Malware ({d_label_de})",
            "Photon-Technologie für schnelle Scans ohne Systembremsen",
            "Proaktiver Webfilter gegen Phishing und betrügerische Seiten",
            "Offizielle Verwaltung und Aktivierung im Bitdefender Central Portal",
        ],
        "es": [
            f"Protección anti-malware en tiempo real ({d_label_es})",
            "Tecnología Photon para análisis rápidos sin ralentizaciones",
            "Filtro web proactivo contra phishing y páginas maliciosas",
            "Gestión y activación oficial en Bitdefender Central",
        ],
        "pt": [
            f"Proteção antimalware em tempo real ({d_label_pt})",
            "Tecnologia Photon para análises rápidas sem qualquer lentidão",
            "Filtro web proativo contra phishing e sites maliciosos",
            "Gestão e ativação oficial em Bitdefender Central",
        ],
    }


def _kaspersky_feats(tier):
    return {
        "it": [
            (ICON_SHIELD, "blue", "Sicurezza", "Protezione in tempo reale multilivello", "Rilevamento istantaneo e blocco di virus, malware, ransomware e attacchi hacker prima che danneggino i dispositivi."),
            (ICON_LOCK, "teal", "Privacy", "Protezione pagamenti e privacy online", "Strumenti dedicati per schermare le transazioni bancarie, bloccare il tracciamento pubblicitario e prevenire furti d'identità."),
            (ICON_LAPTOP, "purple", "Prestazioni", "Ottimizzazione e pulizia del PC", "Pulizia automatica dello spazio su disco e gestione intelligente dei processi in background per un sistema sempre reattivo."),
            (ICON_CHECK_CIRCLE, "dark", "Attivazione", "Portale ufficiale My Kaspersky", "Attivazione ufficiale e sicura tramite account My Kaspersky con sincronizzazione immediata delle licenze e aggiornamenti inclusi."),
        ],
        "en": [
            (ICON_SHIELD, "blue", "Security", "Real-time multi-layered protection", "Instant detection and blocking of viruses, malware, ransomware, and hacking attacks before they harm your system."),
            (ICON_LOCK, "teal", "Privacy", "Payment protection and online privacy", "Dedicated tools to shield financial transactions, block advertising trackers, and prevent identity theft."),
            (ICON_LAPTOP, "purple", "Performance", "PC performance and cleanup tools", "Automatic disk space cleanup and smart background process management to keep your device running fast."),
            (ICON_CHECK_CIRCLE, "dark", "Activation", "Official My Kaspersky portal", "Authentic activation via official My Kaspersky account with instant licence synchronization and regular updates."),
        ],
        "fr": [
            (ICON_SHIELD, "blue", "Sécurité", "Protection multicouche en temps réel", "Détection instantanée et blocage des virus, malwares, ransomwares et tentatives d'intrusion."),
            (ICON_LOCK, "teal", "Confidentialité", "Protection des paiements et vie privée", "Outils dédiés pour sécuriser les transactions bancaires, bloquer les traceurs et prévenir l'usurpation d'identité."),
            (ICON_LAPTOP, "purple", "Performance", "Outils d'optimisation et nettoyage", "Nettoyage automatique du disque et gestion intelligente des ressources pour préserver la réactivité du PC."),
            (ICON_CHECK_CIRCLE, "dark", "Activation", "Portail officiel My Kaspersky", "Activation officielle et gestion sécurisée sur My Kaspersky avec synchronisation de licence et mises à jour."),
        ],
        "de": [
            (ICON_SHIELD, "blue", "Sicherheit", "Mehrschichtiger Echtzeitschutz", "Sofortige Erkennung und Abwehr von Viren, Malware, Ransomware und Hackerangriffen auf Ihren Geräten."),
            (ICON_LOCK, "teal", "Privatsphäre", "Zahlungsschutz und Privatsphäre", "Spezielle Sicherheitsfunktionen zum Schutz von Online-Banking, Blockieren von Trackern und Verhinderung von Identitätsdiebstahl."),
            (ICON_LAPTOP, "purple", "Leistung", "PC-Optimierung und Bereinigung", "Automatische Bereinigung von Speicherplatz und intelligente Ressourcensteuerung für ein schnelles System."),
            (ICON_CHECK_CIRCLE, "dark", "Aktivierung", "Offizielles My Kaspersky Portal", "Sichere Aktivierung über das My Kaspersky Konto mit synchronisiertem Lizenzstatus und regelmäßigen Updates."),
        ],
        "es": [
            (ICON_SHIELD, "blue", "Seguridad", "Protección multicapa en tiempo real", "Detección y bloqueo instantáneo de virus, malware, ransomware e intentos de hackeo en todos tus equipos."),
            (ICON_LOCK, "teal", "Privacidad", "Protección de pagos y privacidad online", "Herramientas especializadas para blindar operaciones bancarias, frenar rastreadores y prevenir el robo de identidad."),
            (ICON_LAPTOP, "purple", "Rendimiento", "Optimización y limpieza del equipo", "Limpieza automática de archivos innecesarios y gestión de procesos en segundo plano para máxima velocidad."),
            (ICON_CHECK_CIRCLE, "dark", "Activación", "Portal oficial My Kaspersky", "Activación oficial mediante cuenta My Kaspersky con sincronización automática de licencias y actualizaciones."),
        ],
        "pt": [
            (ICON_SHIELD, "blue", "Segurança", "Proteção multicamada em tempo real", "Deteção instantânea e bloqueio de vírus, malware, ransomware e ataques de hackers antes que danifiquem os dispositivos."),
            (ICON_LOCK, "teal", "Privacidade", "Proteção de pagamentos e privacidade online", "Ferramentas dedicadas para proteger transações bancárias, bloquear rastreadores publicitários e prevenir o roubo de identidade."),
            (ICON_LAPTOP, "purple", "Desempenho", "Otimização e limpeza do PC", "Limpeza automática do espaço em disco e gestão inteligente dos processos em segundo plano para um sistema sempre rápido."),
            (ICON_CHECK_CIRCLE, "dark", "Ativação", "Portal oficial My Kaspersky", "Ativação oficial e segura através da conta My Kaspersky com sincronização imediata das licenças e atualizações incluídas."),
        ],
    }


def _kaspersky_keypoints(tier, devices):
    d_label_it = "1 dispositivo" if devices == 1 else f"{devices} dispositivi"
    d_label_en = "1 device" if devices == 1 else f"{devices} devices"
    d_label_fr = "1 appareil" if devices == 1 else f"{devices} appareils"
    d_label_de = "1 Gerät" if devices == 1 else f"{devices} Geräte"
    d_label_es = "1 dispositivo" if devices == 1 else f"{devices} dispositivos"
    d_label_pt = "1 dispositivo" if devices == 1 else f"{devices} dispositivos"
    return {
        "it": [
            f"Protezione avanzata da virus, malware e ransomware ({d_label_it})",
            "Navigazione protetta e difesa dei dati bancari durante gli acquisti",
            "Strumenti di ottimizzazione per mantenere il PC veloce e pulito",
            "Attivazione ufficiale e download autentico da My Kaspersky",
        ],
        "en": [
            f"Advanced protection against viruses, malware, and ransomware ({d_label_en})",
            "Secure browsing and banking data protection during online shopping",
            "Optimization tools to keep your PC fast and clean",
            "Official activation and authentic downloads from My Kaspersky",
        ],
        "fr": [
            f"Protection avancée contre virus, malwares et ransomwares ({d_label_fr})",
            "Navigation sécurisée et protection des données bancaires",
            "Outils d'optimisation pour un PC rapide et nettoyé",
            "Activation officielle et téléchargement sécurisé sur My Kaspersky",
        ],
        "de": [
            f"Fortschrittlicher Schutz vor Viren, Malware und Ransomware ({d_label_de})",
            "Sicheres Surfen und Schutz von Bankdaten beim Online-Einkauf",
            "Optimierungstools für ein schnelles und sauberes System",
            "Offizielle Aktivierung und Download über My Kaspersky",
        ],
        "es": [
            f"Protección avanzada contra virus, malware y ransomware ({d_label_es})",
            "Navegación protegida y defensa de datos bancarios en compras",
            "Herramientas de optimización para mantener el equipo rápido y limpio",
            "Activación oficial y descarga auténtica desde My Kaspersky",
        ],
        "pt": [
            f"Proteção avançada contra vírus, malware e ransomware ({d_label_pt})",
            "Navegação protegida e defesa dos dados bancários durante as compras",
            "Ferramentas de otimização para manter o PC rápido e limpo",
            "Ativação oficial e download autêntico a partir de My Kaspersky",
        ],
    }


def _mcafee_feats():
    return {
        "it": [
            (ICON_SHIELD, "blue", "Sicurezza", "Difesa completa contro le minacce", "Protezione continua e intelligente da virus, malware, spyware e ransomware con aggiornamenti costanti in tempo reale."),
            (ICON_GLOBE, "teal", "Web", "Protezione web McAfee WebAdvisor", "Navigazione serena con avvisi preventivi su siti pericolosi, collegamenti ingannevoli e download a rischio."),
            (ICON_LAPTOP, "purple", "Prestazioni", "Ottimizzazione del sistema e velocità", "Strumenti dedicati per velocizzare l'avvio delle applicazioni, liberare memoria e mantenere alte le prestazioni del dispositivo."),
            (ICON_CHECK_CIRCLE, "dark", "Attivazione", "Portale ufficiale McAfee My Account", "Attivazione autentica della licenza con gestione centralizzata dei dispositivi sul portale ufficiale McAfee."),
        ],
        "en": [
            (ICON_SHIELD, "blue", "Security", "Comprehensive threat defence", "Continuous smart protection against viruses, malware, spyware, and ransomware with real-time updates."),
            (ICON_GLOBE, "teal", "Web", "McAfee WebAdvisor web protection", "Safe browsing with proactive warnings against dangerous websites, deceptive links, and risky downloads."),
            (ICON_LAPTOP, "purple", "Performance", "System optimization and speed", "Built-in tools to accelerate application startup, free up memory, and maintain peak device performance."),
            (ICON_CHECK_CIRCLE, "dark", "Activation", "Official McAfee My Account portal", "Authentic licence activation with centralized device management directly via official McAfee portal."),
        ],
        "fr": [
            (ICON_SHIELD, "blue", "Sécurité", "Défense complète contre les menaces", "Protection intelligente continue contre les virus, malwares, spywares et ransomwares avec mises à jour en temps réel."),
            (ICON_GLOBE, "teal", "Web", "Protection web McAfee WebAdvisor", "Navigation sécurisée avec alertes proactives sur les sites dangereux, liens trompeurs et téléchargements suspects."),
            (ICON_LAPTOP, "purple", "Performance", "Optimisation du système et rapidité", "Outils dédiés pour accélérer le lancement des applications, libérer de la mémoire et préserver la fluidité."),
            (ICON_CHECK_CIRCLE, "dark", "Activation", "Portail officiel McAfee My Account", "Activation officielle avec gestion centralisée de vos appareils sur le portail officiel McAfee."),
        ],
        "de": [
            (ICON_SHIELD, "blue", "Sicherheit", "Umfassender Schutz vor Bedrohungen", "Fortlaufender intelligenter Schutz vor Viren, Malware, Spyware und Ransomware mit Echtzeit-Aktualisierungen."),
            (ICON_GLOBE, "teal", "Web", "McAfee WebAdvisor Web-Schutz", "Sicheres Surfen mit proaktiven Warnungen vor gefährlichen Webseiten, betrügerischen Links und verdächtigen Downloads."),
            (ICON_LAPTOP, "purple", "Leistung", "Systemoptimierung und Schnelligkeit", "Integrierte Tools zur Beschleunigung von Apps, Freigabe von Arbeitsspeicher und Erhaltung der Höchstleistung."),
            (ICON_CHECK_CIRCLE, "dark", "Aktivierung", "Offizielles McAfee My Account Portal", "Offizielle Lizenzaktivierung mit zentraler Geräteverwaltung über das offizielle McAfee-Portal."),
        ],
        "es": [
            (ICON_SHIELD, "blue", "Seguridad", "Defensa completa contra amenazas", "Protección continua e inteligente contra virus, malware, spyware y ransomware con actualizaciones en tiempo real."),
            (ICON_GLOBE, "teal", "Web", "Protección web McAfee WebAdvisor", "Navegación protegida con advertencias proactivas ante sitios web peligrosos, enlaces engañosos y descargas dudosas."),
            (ICON_LAPTOP, "purple", "Rendimiento", "Optimización del equipo y fluidez", "Herramientas integradas para acelerar el inicio de aplicaciones, liberar memoria y asegurar un rendimiento óptimo."),
            (ICON_CHECK_CIRCLE, "dark", "Activación", "Portal oficial McAfee My Account", "Activación oficial y gestión centralizada de tus dispositivos en el portal oficial de McAfee."),
        ],
        "pt": [
            (ICON_SHIELD, "blue", "Segurança", "Defesa completa contra ameaças", "Proteção contínua e inteligente contra vírus, malware, spyware e ransomware com atualizações constantes em tempo real."),
            (ICON_GLOBE, "teal", "Web", "Proteção web McAfee WebAdvisor", "Navegação tranquila com avisos preventivos sobre sites perigosos, links enganosos e downloads de risco."),
            (ICON_LAPTOP, "purple", "Desempenho", "Otimização do sistema e velocidade", "Ferramentas dedicadas para acelerar o arranque das aplicações, libertar memória e manter o desempenho do dispositivo."),
            (ICON_CHECK_CIRCLE, "dark", "Ativação", "Portal oficial McAfee My Account", "Ativação autêntica da licença com gestão centralizada dos dispositivos no portal oficial McAfee."),
        ],
    }


def _mcafee_keypoints(devices):
    d_label_it = "1 dispositivo" if devices == 1 else f"{devices} dispositivi"
    d_label_en = "1 device" if devices == 1 else f"{devices} devices"
    d_label_fr = "1 appareil" if devices == 1 else f"{devices} appareils"
    d_label_de = "1 Gerät" if devices == 1 else f"{devices} Geräte"
    d_label_es = "1 dispositivo" if devices == 1 else f"{devices} dispositivos"
    d_label_pt = "1 dispositivo" if devices == 1 else f"{devices} dispositivos"
    return {
        "it": [
            f"Protezione completa e continua da virus e malware ({d_label_it})",
            "Tecnologia McAfee WebAdvisor per bloccare siti e link pericolosi",
            "Strumenti di ottimizzazione per velocizzare app e memoria",
            "Attivazione sicura e gestione ufficiale su McAfee My Account",
        ],
        "en": [
            f"Complete continuous virus and malware protection ({d_label_en})",
            "McAfee WebAdvisor technology to block malicious sites and links",
            "Optimization tools to accelerate applications and free up memory",
            "Secure activation and official management on McAfee My Account",
        ],
        "fr": [
            f"Protection complète et continue contre virus et malwares ({d_label_fr})",
            "Technologie McAfee WebAdvisor pour bloquer les sites et liens dangereux",
            "Outils d'optimisation pour accélérer les applications et la mémoire",
            "Activation sécurisée et gestion officielle sur McAfee My Account",
        ],
        "de": [
            f"Umfassender und fortlaufender Schutz vor Viren und Malware ({d_label_de})",
            "McAfee WebAdvisor-Technologie zum Blockieren gefährlicher Webseiten und Links",
            "Optimierungstools zur Beschleunigung von Apps und Arbeitsspeicher",
            "Sichere Aktivierung und offizielle Verwaltung im McAfee My Account Portal",
        ],
        "es": [
            f"Protección completa y continua contra virus y malware ({d_label_es})",
            "Tecnologia McAfee WebAdvisor para bloquear páginas y enlaces peligrosos",
            "Herramientas de optimización para acelerar aplicaciones y memoria",
            "Activación segura y gestión oficial en McAfee My Account",
        ],
        "pt": [
            f"Proteção completa e contínua contra vírus e malware ({d_label_pt})",
            "Tecnologia McAfee WebAdvisor para bloquear sites e links perigosos",
            "Ferramentas de otimização para acelerar apps e libertar memória",
            "Ativação segura e gestão oficial em McAfee My Account",
        ],
    }


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
        "pt": [
            ("O que recebo após a compra?", "Um email com a licença/código e instruções para ativar no portal oficial do fabricante."),
            ("É uma subscrição?", "Depende do produto: muitas edições são subscrições anuais; as variantes «sem subscrição» / sem renovação automática estão indicadas na ficha."),
            ("Em quantos dispositivos?", "O número é o que consta no título (ex. 1, 3, 5 ou 10 dispositivos), segundo as condições do fabricante."),
            ("Como se ativa?", f"Usa o código recebido no portal oficial {brand} e segue as instruções do email."),
            ("Funciona em Mac/Android?", "Se o fabricante o previr para esse produto. Verifica as plataformas suportadas na documentação oficial."),
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
        prefix = f"{brand} {line}".strip() if line else brand
        base = f"{prefix} — {d[lg]}"
        if years != 1:
            base = f"{prefix} — {d[lg]} · {y[lg]}"
        if no_sub:
            suffix = {
                "it": " (no abbonamento)",
                "en": " (no subscription)",
                "fr": " (sans abonnement)",
                "de": " (kein Abo)",
                "es": " (sin suscripción)",
                "pt": " (sem subscrição)",
                "nl": " (geen abonnement)",
            }[lg]
            base += suffix
        out[lg] = base
    return out


PRODUCTS = {}


def _add_eset(slug, devices, years=1):
    dev_str = {
        "it": f"{devices} Dispositivo" if devices == 1 else f"{devices} Dispositivi",
        "en": f"{devices} Device" if devices == 1 else f"{devices} Devices",
        "fr": f"{devices} Appareil" if devices == 1 else f"{devices} Appareils",
        "de": f"{devices} Gerät" if devices == 1 else f"{devices} Geräte",
        "es": f"{devices} Dispositivo" if devices == 1 else f"{devices} Dispositivos",
        "pt": f"{devices} Dispositivo" if devices == 1 else f"{devices} Dispositivos",
        "nl": f"{devices} apparaat" if devices == 1 else f"{devices} apparaten",
    }
    yr_str = {
        "it": f"{years} Anno" if years == 1 else f"{years} Anni",
        "en": f"{years} Year" if years == 1 else f"{years} Years",
        "fr": f"{years} An" if years == 1 else f"{years} Ans",
        "de": f"{years} Jahr" if years == 1 else f"{years} Jahre",
        "es": f"{years} Año" if years == 1 else f"{years} Años",
        "pt": f"{years} Ano" if years == 1 else f"{years} Anos",
        "nl": f"{years} jaar" if years == 1 else f"{years} jaar",
    }
    span = {
        "it": f"NOD32 Antivirus – {dev_str['it']} ({yr_str['it']})",
        "en": f"NOD32 Antivirus – {dev_str['en']} ({yr_str['en']})",
        "fr": f"NOD32 Antivirus – {dev_str['fr']} ({yr_str['fr']})",
        "de": f"NOD32 Antivirus – {dev_str['de']} ({yr_str['de']})",
        "es": f"NOD32 Antivirus – {dev_str['es']} ({yr_str['es']})",
        "pt": f"NOD32 Antivirus – {dev_str['pt']} ({yr_str['pt']})",
        "nl": f"NOD32 Antivirus – {dev_str['nl']} ({yr_str['nl']})",
    }
    PRODUCTS[slug] = _av_page(
        brand="ESET",
        line="NOD32 Antivirus",
        title_span=span,
        devices=devices,
        years=years,
        name=L(
            **{lg: f"ESET NOD32 Antivirus – {dev_str[lg]} ({yr_str[lg]})" for lg in LANGS}
        ),
        desc=L(
            it=f"ESET NOD32 Antivirus per {dev_str['it']}: protezione leggera e reattiva con licenza originale e consegna immediata via email. Attivazione sicura sul portale ufficiale ESET HOME.",
            en=f"ESET NOD32 Antivirus for {dev_str['en']}: lightweight, fast protection with a genuine digital licence and instant email delivery. Official activation via ESET HOME.",
            fr=f"ESET NOD32 Antivirus pour {dev_str['fr']} : protection légère et réactive, licence numérique authentique et envoi rapide par e-mail. Activation sur ESET HOME.",
            de=f"ESET NOD32 Antivirus für {dev_str['de']}: schlanker, schneller Schutz mit originaler digitaler Lizenz und sofortiger E-Mail-Zustellung. Offizielle Aktivierung im ESET HOME Portal.",
            es=f"ESET NOD32 Antivirus para {dev_str['es']}: protección ligera y eficiente con licencia digital oficial y entrega inmediata por email. Activación segura en ESET HOME.",
            pt=f"ESET NOD32 Antivirus para {dev_str['pt']}: proteção leve e eficiente com licença digital original e entrega imediata por email. Ativação segura no ESET HOME.",
            nl=f"ESET NOD32 Antivirus voor {dev_str['nl']}: lichte, efficiënte bescherming met een originele digitale licentie en directe levering per e-mail. Veilige activering via ESET HOME.",
        ),
        pills=_pills("ESET", devices, years),
        features_title=L(
            it="Perché scegliere ESET NOD32 Antivirus",
            en="Why choose ESET NOD32 Antivirus",
            fr="Pourquoi choisir ESET NOD32 Antivirus",
            de="Warum ESET NOD32 Antivirus wählen",
            es="Por qué elegir ESET NOD32 Antivirus",
            pt="Porque escolher o ESET NOD32 Antivirus",
            nl="Waarom ESET NOD32 Antivirus kiezen",
        ),
        features=_eset_feats(),
        keypoints=_eset_keypoints(),
        specs_table=SPECS_TABLE_ESET,
        steps=_steps_for_brand({
            "it": "portale ufficiale ESET (ESET HOME)",
            "en": "official ESET portal (ESET HOME)",
            "fr": "portail officiel ESET (ESET HOME)",
            "de": "offiziellen ESET-Portal (ESET HOME)",
            "es": "portal oficial de ESET (ESET HOME)",
            "pt": "portal oficial ESET (ESET HOME)",
            "nl": "officiële ESET-portaal (ESET HOME)",
        }),
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
        "pt": edition + (" · sem sub" if no_sub else ""),
        "nl": edition + (" · geen abo" if no_sub else ""),
    }
    cloud = "10 GB" if "Standard" in edition else "25 GB"
    PRODUCTS[slug] = _av_page(
        brand="Norton",
        line=f"360 {edition}",
        title_span=span,
        devices=devices,
        years=1,
        name=_name(f"Norton 360 {edition}", "", devices, 1, no_sub),
        desc=L(
            it=f"Norton 360 {edition} per {_devices(devices)['it']}: protezione online completa con licenza digitale e consegna istantanea via email. Attivazione sicura sul portale ufficiale My Norton."
            + (" Variante senza rinnovo automatico." if no_sub else ""),
            en=f"Norton 360 {edition} for {_devices(devices)['en']}: complete online protection with a digital licence and instant email delivery. Official activation via My Norton."
            + (" No auto-renewal variant." if no_sub else ""),
            fr=f"Norton 360 {edition} pour {_devices(devices)['fr']} : protection en ligne complète, licence numérique et livraison par e-mail. Activation sur le portail officiel My Norton."
            + (" Variante sans renouvellement automatique." if no_sub else ""),
            de=f"Norton 360 {edition} für {_devices(devices)['de']}: Rundum-Online-Schutz mit digitaler Lizenz und sofortiger E-Mail-Zustellung. Offizielle Aktivierung im My Norton Portal."
            + (" Variante ohne automatische Verlängerung." if no_sub else ""),
            es=f"Norton 360 {edition} para {_devices(devices)['es']}: protección online completa con licencia digital y entrega inmediata por email. Activación segura en My Norton."
            + (" Variante sin renovación automática." if no_sub else ""),
            pt=f"Norton 360 {edition} para {_devices(devices)['pt']}: proteção online completa com licença digital e entrega imediata por email. Ativação segura no My Norton."
            + (" Variante sem renovação automática." if no_sub else ""),
            nl=f"Norton 360 {edition} voor {_devices(devices)['nl']}: complete onlinebescherming met een digitale licentie en directe levering per e-mail. Veilige activering via My Norton."
            + (" Variant zonder automatische verlenging." if no_sub else ""),
        ),
        pills=_pills(
            "Norton",
            devices,
            1,
            extra=L(it=f"Cloud {cloud}", en=f"{cloud} cloud", fr=f"Cloud {cloud}", de=f"{cloud} Cloud", es=f"Cloud {cloud}", pt=f"Cloud {cloud}", nl=f"{cloud} cloud")
            if "Deluxe" in edition or "Standard" in edition
            else None,
        ),
        features_title=L(
            it=f"Perché scegliere Norton 360 {edition}",
            en=f"Why choose Norton 360 {edition}",
            fr=f"Pourquoi choisir Norton 360 {edition}",
            de=f"Warum Norton 360 {edition} wählen",
            es=f"Por qué elegir Norton 360 {edition}",
            pt=f"Porque escolher o Norton 360 {edition}",
            nl=f"Waarom Norton 360 {edition} kiezen",
        ),
        features=_norton_feats(edition, cloud),
        keypoints=_norton_keypoints(edition, devices, cloud),
        specs_table=SPECS_TABLE_NORTON,
        steps=_steps_for_brand({
            "it": "portale ufficiale Norton (My Norton)",
            "en": "official Norton portal (My Norton)",
            "fr": "portail officiel Norton (My Norton)",
            "de": "offiziellen Norton-Portal (My Norton)",
            "es": "portal oficial de Norton (My Norton)",
            "pt": "portal oficial Norton (My Norton)",
            "nl": "officiële Norton-portaal (My Norton)",
        }),
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
            pt=f"Plus · {_devices(devices)['pt']}",
            nl=f"Plus · {_devices(devices)['nl']}",
        ),
        devices=devices,
        years=1,
        name=_name("Bitdefender Antivirus Plus", "", devices),
        desc=L(
            it=f"Bitdefender Antivirus Plus per {_devices(devices)['it']}: protezione anti-malware proattiva e leggera con licenza originale e consegna immediata via email. Attivazione su Bitdefender Central.",
            en=f"Bitdefender Antivirus Plus for {_devices(devices)['en']}: proactive, lightweight anti-malware protection with genuine digital key and instant email delivery. Activate on Bitdefender Central.",
            fr=f"Bitdefender Antivirus Plus pour {_devices(devices)['fr']} : protection anti-malware proactive et légère, clé numérique authentique livrée par e-mail. Activation sur Bitdefender Central.",
            de=f"Bitdefender Antivirus Plus für {_devices(devices)['de']}: proaktiver, ressourcenschonender Schutz vor Malware mit digitalem Key per E-Mail. Aktivierung im Bitdefender Central Portal.",
            es=f"Bitdefender Antivirus Plus para {_devices(devices)['es']}: protección digital con clave por email y activación en el portal Bitdefender.",
            pt=f"Bitdefender Antivirus Plus para {_devices(devices)['pt']}: proteção antimalware proativa e leve com chave digital original e entrega imediata por email. Ativação no Bitdefender Central.",
            nl=f"Bitdefender Antivirus Plus voor {_devices(devices)['nl']}: proactieve, lichte antimalwarebescherming met een originele digitale sleutel en directe levering per e-mail. Activering via Bitdefender Central.",
        ),
        pills=_pills("Bitdefender", devices),
        features_title=L(
            it="Perché scegliere Bitdefender Antivirus Plus",
            en="Why choose Bitdefender Antivirus Plus",
            fr="Pourquoi choisir Bitdefender Antivirus Plus",
            de="Warum Bitdefender Antivirus Plus wählen",
            es="Por qué elegir Bitdefender Antivirus Plus",
            pt="Porque escolher o Bitdefender Antivirus Plus",
            nl="Waarom Bitdefender Antivirus Plus kiezen",
        ),
        features=_bitdefender_feats(),
        keypoints=_bitdefender_keypoints(devices),
        specs_table=SPECS_TABLE_BITDEFENDER,
        steps=_steps_for_brand({
            "it": "portale ufficiale Bitdefender (Bitdefender Central)",
            "en": "official Bitdefender portal (Bitdefender Central)",
            "fr": "portail officiel Bitdefender (Bitdefender Central)",
            "de": "offiziellen Bitdefender-Portal (Bitdefender Central)",
            "es": "portal oficial de Bitdefender (Bitdefender Central)",
            "pt": "portal oficial Bitdefender (Bitdefender Central)",
            "nl": "officiële Bitdefender-portaal (Bitdefender Central)",
        }),
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
            pt=f"{tier} · {_devices(devices)['pt']}",
            nl=f"{tier} · {_devices(devices)['nl']}",
        ),
        devices=devices,
        years=1,
        name=_name(f"Kaspersky {tier}", "", devices),
        desc=L(
            it=f"Kaspersky {tier} per {_devices(devices)['it']}: suite di sicurezza avanzata con protezione in tempo reale, licenza originale e invio immediato via email. Attivazione sicura su My Kaspersky.",
            en=f"Kaspersky {tier} for {_devices(devices)['en']}: advanced security suite with real-time defence, genuine digital licence, and instant email delivery. Official activation on My Kaspersky.",
            fr=f"Kaspersky {tier} pour {_devices(devices)['fr']} : suite de sécurité avancée avec protection en temps réel, licence numérique authentique et envoi rapide par e-mail. Activation sur My Kaspersky.",
            de=f"Kaspersky {tier} für {_devices(devices)['de']}: moderne Sicherheits-Suite mit Echtzeitschutz, digitaler Original-Lizenz und schneller E-Mail-Zustellung. Aktivierung im My Kaspersky Portal.",
            es=f"Kaspersky {tier} para {_devices(devices)['es']}: suite de seguridad avanzada con protección en tiempo real, licencia digital oficial y entrega inmediata por email. Activación en My Kaspersky.",
            pt=f"Kaspersky {tier} para {_devices(devices)['pt']}: suite de segurança avançada com proteção em tempo real, licença digital original e envio imediato por email. Ativação segura no My Kaspersky.",
            nl=f"Kaspersky {tier} voor {_devices(devices)['nl']}: geavanceerde beveiligingssuite met realtimebescherming, een originele digitale licentie en directe verzending per e-mail. Veilige activering via My Kaspersky.",
        ),
        pills=_pills("Kaspersky", devices, extra=L(it=tier, en=tier, fr=tier, de=tier, es=tier, pt=tier, nl=tier)),
        features_title=L(
            it=f"Perché scegliere Kaspersky {tier}",
            en=f"Why choose Kaspersky {tier}",
            fr=f"Pourquoi choisir Kaspersky {tier}",
            de=f"Warum Kaspersky {tier} wählen",
            es=f"Por qué elegir Kaspersky {tier}",
            pt=f"Porque escolher o Kaspersky {tier}",
            nl=f"Waarom Kaspersky {tier} kiezen",
        ),
        features=_kaspersky_feats(tier),
        keypoints=_kaspersky_keypoints(tier, devices),
        specs_table=SPECS_TABLE_KASPERSKY,
        steps=_steps_for_brand({
            "it": "portale ufficiale Kaspersky (My Kaspersky)",
            "en": "official Kaspersky portal (My Kaspersky)",
            "fr": "portail officiel Kaspersky (My Kaspersky)",
            "de": "offiziellen Kaspersky-Portal (My Kaspersky)",
            "es": "portal oficial de Kaspersky (My Kaspersky)",
            "pt": "portal oficial Kaspersky (My Kaspersky)",
            "nl": "officiële Kaspersky-portaal (My Kaspersky)",
        }),
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
            pt=f"Total Protection · {_devices(devices)['pt']}",
            nl=f"Total Protection · {_devices(devices)['nl']}",
        ),
        devices=devices,
        years=1,
        name=_name("McAfee Total Protection", "", devices),
        desc=L(
            it=f"McAfee Total Protection per {_devices(devices)['it']}: difesa multi-dispositivo completa con protezione web avanzata, licenza digitale originale e consegna immediata via email. Attivazione su McAfee My Account.",
            en=f"McAfee Total Protection for {_devices(devices)['en']}: complete multi-device protection with advanced web security, genuine licence, and instant email delivery. Official activation via McAfee My Account.",
            fr=f"McAfee Total Protection pour {_devices(devices)['fr']} : protection multi-appareils complète avec sécurité web avancée, licence authentique et livraison par e-mail. Activation sur McAfee My Account.",
            de=f"McAfee Total Protection für {_devices(devices)['de']}: umfassender Mehrgeräteschutz mit fortschrittlicher Websicherheit, digitaler Original-Lizenz und E-Mail-Zustellung. Aktivierung im McAfee-Portal.",
            es=f"McAfee Total Protection para {_devices(devices)['es']}: protección integral multidispositivo con seguridad web avanzada, licencia digital oficial y entrega inmediata por email. Activación en McAfee My Account.",
            pt=f"McAfee Total Protection para {_devices(devices)['pt']}: defesa multi-dispositivo completa com proteção web avançada, licença digital original e entrega imediata por email. Ativação na McAfee My Account.",
            nl=f"McAfee Total Protection voor {_devices(devices)['nl']}: complete bescherming voor meerdere apparaten met geavanceerde webbeveiliging, een originele digitale licentie en directe levering per e-mail. Activering via McAfee My Account.",
        ),
        pills=_pills("McAfee", devices),
        features_title=L(
            it="Perché scegliere McAfee Total Protection",
            en="Why choose McAfee Total Protection",
            fr="Pourquoi choisir McAfee Total Protection",
            de="Warum McAfee Total Protection wählen",
            es="Por qué elegir McAfee Total Protection",
            pt="Porque escolher o McAfee Total Protection",
            nl="Waarom McAfee Total Protection kiezen",
        ),
        features=_mcafee_feats(),
        keypoints=_mcafee_keypoints(devices),
        specs_table=SPECS_TABLE_MCAFEE,
        steps=_steps_for_brand({
            "it": "portale ufficiale McAfee (McAfee My Account)",
            "en": "official McAfee portal (McAfee My Account)",
            "fr": "portail officiel McAfee (McAfee My Account)",
            "de": "offiziellen McAfee-Portal (McAfee My Account)",
            "es": "portal oficial de McAfee (McAfee My Account)",
            "pt": "portal oficial McAfee (McAfee My Account)",
            "nl": "officiële McAfee-portaal (McAfee My Account)",
        }),
        faq=_faq_av("McAfee"),
    )


for slug, n in [
    ("mcafee-total-protection-1-device", 1),
    ("mcafee-total-protection-5-devices", 5),
    ("mcafee-total-protection-10-devices", 10),
]:
    _add_mcafee(slug, n)

backfill_lang(PRODUCTS)
backfill_lang(PRODUCTS, target="nl", source="en", translate=nl_text)


def get_antivirus_content(slug):
    return PRODUCTS.get(slug)
