#!/usr/bin/env python3
"""Security First Phase 2: nav order, homepage hierarchy, AV filters, PDP variants."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from product_page_lib import (  # noqa: E402
    BASE_LABELS,
    KASPERSKY_SKUS,
    LANGS,
    VARIANT_OF,
    VARIANT_SETS,
    _render_cross_sell,
    _render_kaspersky_partner,
    _render_plan_switcher,
    entry,
    eur_fmt,
    pct,
    product_card,
)

spec = importlib.util.spec_from_file_location(
    "refresh_home_featured", ROOT / "scripts" / "refresh-home-featured.py"
)
rhf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rhf)

CONSULT = {
    "it": "consulenza",
    "en": "consultation",
    "fr": "consultation",
    "de": "beratung",
    "es": "consultoria",
}

SEO = {
    "it": {
        "title": "Antivirus originale e licenze digitali | Aml Store",
        "desc": "Antivirus e software originale con consegna digitale, attivazione sui portali ufficiali, fattura e assistenza in italiano.",
    },
    "en": {
        "title": "Original antivirus and digital licences | Aml Store",
        "desc": "Genuine antivirus and digital software with email delivery, official-portal activation, invoices and human support.",
    },
    "fr": {
        "title": "Antivirus original et licences numériques | Aml Store",
        "desc": "Antivirus et logiciels originaux, livraison numérique, activation sur les portails officiels, facture et assistance humaine.",
    },
    "de": {
        "title": "Original-Antivirus und digitale Lizenzen | Aml Store",
        "desc": "Originales Antivirus und digitale Software mit digitaler Lieferung, Aktivierung auf offiziellen Portalen, Rechnung und persönlichem Support.",
    },
    "es": {
        "title": "Antivirus original y licencias digitales | Aml Store",
        "desc": "Antivirus y software original con entrega digital, activación en portales oficiales, factura y asistencia humana.",
    },
}

HERO = {
    "it": {
        "h1_a": "Protezione originale",
        "h1_b": "consegna in 2–15 minuti.",
        "sub": "Antivirus e abbonamenti digitali originali. Attivazione sui portali ufficiali, assistenza in italiano, fattura disponibile.",
    },
    "en": {
        "h1_a": "Genuine protection",
        "h1_b": "delivered in 2–15 minutes.",
        "sub": "Original antivirus and digital subscriptions. Official-portal activation, human support, invoices available.",
    },
    "fr": {
        "h1_a": "Protection originale",
        "h1_b": "livrée en 2–15 minutes.",
        "sub": "Antivirus et abonnements numériques originaux. Activation sur les portails officiels, assistance humaine, facture disponible.",
    },
    "de": {
        "h1_a": "Originaler Schutz",
        "h1_b": "in 2–15 Minuten geliefert.",
        "sub": "Originales Antivirus und digitale Abos. Aktivierung auf offiziellen Portalen, persönlicher Support, Rechnung verfügbar.",
    },
    "es": {
        "h1_a": "Protección original",
        "h1_b": "entrega en 2–15 minutos.",
        "sub": "Antivirus y suscripciones digitales originales. Activación en portales oficiales, asistencia humana, factura disponible.",
    },
}

COPY = {
    "it": {
        "protect_title": "Trova la protezione adatta",
        "protect_lede": "Scegli per quanti dispositivi vuoi copertura. Confronta i piani e trova la protezione più adatta a te.",
        "chip": "{n} dispositiv{sfx}",
        "m365_title": "Microsoft 365",
        "m365_lede": "Abbonamenti annuali per casa e famiglia, complementari alla protezione.",
        "m365_hero_badge": "Microsoft 365",
        "m365_hero_title": "Tutte le tue app e la sicurezza in un unico piano",
        "m365_hero_sub": "Word, Excel, PowerPoint, Outlook, Teams, OneDrive e Copilot per casa e lavoro.",
        "m365_personal": "Microsoft 365 Personal",
        "m365_family": "Microsoft 365 Family",
        "m365_cta": "Soluzioni Microsoft 365 per aziende",
        "biz_title": "Per aziende",
        "biz_lede": "Licensing specialistico, multi-seat e preventivi.",
        "biz_m365": "Microsoft 365 Business",
        "biz_server": "Windows Server e SQL",
        "biz_tools": "Project e Visio",
        "biz_cta": "Richiedi un preventivo",
        "cat_title": "Altre soluzioni",
        "av_name": "Antivirus e sicurezza",
        "av_desc": "Norton, Kaspersky, Bitdefender, ESET, McAfee",
        "m365_desc": "Personal, Family e Business",
        "win_desc": "Windows 10 e 11, Home e Pro",
        "off_desc": "Da Office 2019 a Office 2024",
        "filter_aria": "Filtra per numero di dispositivi",
        "filter_all": "Tutti",
        "filter_n": "{n} dispositiv{sfx}",
        "kasp_opt": "Protezione completa",
        "kasp_title": "Kaspersky Plus · 1 dispositivo",
        "kasp_body": "Piano Plus con le funzioni extra del catalogo Kaspersky. Attivazione sul portale ufficiale.",
        "guide_res_title": "ESET NOD32 · 1 dispositivo",
        "guide_res_body": "Protezione antivirus leggera per un solo dispositivo. Attivazione sul portale ufficiale ESET.",
    },
    "en": {
        "protect_title": "Find the right protection",
        "protect_lede": "Choose how many devices to cover, then compare the plans.",
        "chip": "{n} device{sfx}",
        "m365_title": "Microsoft 365",
        "m365_lede": "Yearly subscriptions for home and family, alongside security.",
        "m365_hero_badge": "Microsoft 365",
        "m365_hero_title": "All your apps and security in one single plan",
        "m365_hero_sub": "Word, Excel, PowerPoint, Outlook, Teams, OneDrive and Copilot for home and work.",
        "m365_personal": "Microsoft 365 Personal",
        "m365_family": "Microsoft 365 Family",
        "m365_cta": "Microsoft 365 solutions for business",
        "biz_title": "For business",
        "biz_lede": "Specialist licensing, multi-seat and quotes.",
        "biz_m365": "Microsoft 365 Business",
        "biz_server": "Windows Server and SQL",
        "biz_tools": "Project and Visio",
        "biz_cta": "Request a quote",
        "cat_title": "Other solutions",
        "av_name": "Antivirus and security",
        "av_desc": "Norton, Kaspersky, Bitdefender, ESET, McAfee",
        "m365_desc": "Personal, Family and Business",
        "win_desc": "Windows 10 and 11, Home and Pro",
        "off_desc": "From Office 2019 to Office 2024",
        "filter_aria": "Filter by number of devices",
        "filter_all": "All",
        "filter_n": "{n} device{sfx}",
        "kasp_opt": "Full protection",
        "kasp_title": "Kaspersky Plus · 1 device",
        "kasp_body": "Plus plan with the extra features in the Kaspersky catalogue. Activate on the official portal.",
        "guide_res_title": "ESET NOD32 · 1 device",
        "guide_res_body": "Lightweight antivirus for a single device. Activate on the official ESET portal.",
    },
    "fr": {
        "protect_title": "Trouver la protection adaptée",
        "protect_lede": "Choisissez le nombre d'appareils, puis comparez les offres.",
        "chip": "{n} appareil{sfx}",
        "m365_title": "Microsoft 365",
        "m365_lede": "Abonnements annuels pour la maison et la famille, en complément de la sécurité.",
        "m365_hero_badge": "Microsoft 365",
        "m365_hero_title": "Toutes vos applications et votre sécurité en un seul abonnement",
        "m365_hero_sub": "Word, Excel, PowerPoint, Outlook, Teams, OneDrive et Copilot pour la maison et le travail.",
        "m365_personal": "Microsoft 365 Personnel",
        "m365_family": "Microsoft 365 Famille",
        "m365_cta": "Solutions Microsoft 365 pour les entreprises",
        "biz_title": "Pour les entreprises",
        "biz_lede": "Licensing spécialisé, multi-postes et devis.",
        "biz_m365": "Microsoft 365 Business",
        "biz_server": "Windows Server et SQL",
        "biz_tools": "Project et Visio",
        "biz_cta": "Demander un devis",
        "cat_title": "Autres solutions",
        "av_name": "Antivirus et sécurité",
        "av_desc": "Norton, Kaspersky, Bitdefender, ESET, McAfee",
        "m365_desc": "Personnel, Famille et Business",
        "win_desc": "Windows 10 et 11, Home et Pro",
        "off_desc": "D'Office 2019 à Office 2024",
        "filter_aria": "Filtrer par nombre d'appareils",
        "filter_all": "Tous",
        "filter_n": "{n} appareil{sfx}",
        "kasp_opt": "Protection complète",
        "kasp_title": "Kaspersky Plus · 1 appareil",
        "kasp_body": "Offre Plus avec les fonctions supplémentaires du catalogue Kaspersky. Activation sur le portail officiel.",
        "guide_res_title": "ESET NOD32 · 1 appareil",
        "guide_res_body": "Antivirus léger pour un seul appareil. Activation sur le portail officiel ESET.",
    },
    "de": {
        "protect_title": "Passenden Schutz finden",
        "protect_lede": "Wählen Sie die Geräteanzahl und vergleichen Sie die Tarife.",
        "chip": "{n} Gerät{sfx}",
        "m365_title": "Microsoft 365",
        "m365_lede": "Jahresabos für Zuhause und Familie, ergänzend zur Sicherheit.",
        "m365_hero_badge": "Microsoft 365",
        "m365_hero_title": "Alle Ihre Apps und Sicherheit in einem Paket",
        "m365_hero_sub": "Word, Excel, PowerPoint, Outlook, Teams, OneDrive und Copilot für Zuhause und Beruf.",
        "m365_personal": "Microsoft 365 Personal",
        "m365_family": "Microsoft 365 Family",
        "m365_cta": "Microsoft-365-Lösungen für Unternehmen",
        "biz_title": "Für Unternehmen",
        "biz_lede": "Spezial-Licensing, mehrere Arbeitsplätze und Angebote.",
        "biz_m365": "Microsoft 365 Business",
        "biz_server": "Windows Server und SQL",
        "biz_tools": "Project und Visio",
        "biz_cta": "Angebot anfragen",
        "cat_title": "Weitere Lösungen",
        "av_name": "Antivirus und Sicherheit",
        "av_desc": "Norton, Kaspersky, Bitdefender, ESET, McAfee",
        "m365_desc": "Personal, Family und Business",
        "win_desc": "Windows 10 und 11, Home und Pro",
        "off_desc": "Von Office 2019 bis Office 2024",
        "filter_aria": "Nach Geräteanzahl filtern",
        "filter_all": "Alle",
        "filter_n": "{n} Gerät{sfx}",
        "kasp_opt": "Umfassender Schutz",
        "kasp_title": "Kaspersky Plus · 1 Gerät",
        "kasp_body": "Plus-Tarif mit den Extra-Funktionen aus dem Kaspersky-Katalog. Aktivierung über das offizielle Portal.",
        "guide_res_title": "ESET NOD32 · 1 Gerät",
        "guide_res_body": "Leichtes Antivirus für ein Gerät. Aktivierung über das offizielle ESET-Portal.",
    },
    "es": {
        "protect_title": "Encuentra la protección adecuada",
        "protect_lede": "Elige cuántos dispositivos cubrir y compara los planes.",
        "chip": "{n} dispositivo{sfx}",
        "m365_title": "Microsoft 365",
        "m365_lede": "Suscripciones anuales para casa y familia, junto a la seguridad.",
        "m365_hero_badge": "Microsoft 365",
        "m365_hero_title": "Todas tus aplicaciones y seguridad en un solo plan",
        "m365_hero_sub": "Word, Excel, PowerPoint, Outlook, Teams, OneDrive y Copilot para el hogar y el trabajo.",
        "m365_personal": "Microsoft 365 Personal",
        "m365_family": "Microsoft 365 Familia",
        "m365_cta": "Soluciones Microsoft 365 para empresas",
        "biz_title": "Para empresas",
        "biz_lede": "Licenciamiento especializado, varios puestos y presupuestos.",
        "biz_m365": "Microsoft 365 Business",
        "biz_server": "Windows Server y SQL",
        "biz_tools": "Project y Visio",
        "biz_cta": "Solicitar presupuesto",
        "cat_title": "Otras soluciones",
        "av_name": "Antivirus y seguridad",
        "av_desc": "Norton, Kaspersky, Bitdefender, ESET, McAfee",
        "m365_desc": "Personal, Familia y Business",
        "win_desc": "Windows 10 y 11, Home y Pro",
        "off_desc": "De Office 2019 a Office 2024",
        "filter_aria": "Filtrar por número de dispositivos",
        "filter_all": "Todos",
        "filter_n": "{n} dispositivo{sfx}",
        "kasp_opt": "Protección completa",
        "kasp_title": "Kaspersky Plus · 1 dispositivo",
        "kasp_body": "Plan Plus con las funciones extra del catálogo Kaspersky. Activación en el portal oficial.",
        "guide_res_title": "ESET NOD32 · 1 dispositivo",
        "guide_res_body": "Antivirus ligero para un solo dispositivo. Activación en el portal oficial ESET.",
    },
}

PLAN_UI = {
    "it": {
        "recommended": "Consigliato",
        "year": "/ anno",
        "more": "Scopri di più",
        "note_1": "Disponibile per 1 dispositivo",
        "devices_field": "Dispositivi",
        "trust": "Tutti i piani includono consegna digitale e attivazione ufficiale.",
        "see_all": "Vedi tutti i piani antivirus",
        "ideal": "Ideale per:",
        "role_std": "Protezione essenziale",
        "role_plus": "Protezione consigliata",
        "role_prem": "Protezione completa",
        "name_std": "Kaspersky Standard",
        "name_plus": "Kaspersky Plus",
        "name_prem": "Kaspersky Premium",
        "sub_std": "Protezione essenziale per l'uso quotidiano.",
        "sub_plus": "Sicurezza completa per lavoro, acquisti e navigazione.",
        "sub_prem": "Protezione avanzata con privacy e strumenti extra.",
        "feat_std": ["Antivirus in tempo reale", "Protezione web", "Anti-phishing"],
        "feat_plus": ["Protezione avanzata", "VPN / password come da piano", "Ottimizzazione prestazioni"],
        "feat_prem": ["Tutto di Plus", "Protezione avanzata e privacy"],
        "ideal_std": "uso personale e navigazione quotidiana",
        "ideal_plus": "casa, lavoro e acquisti online",
        "ideal_prem_1": "utenti avanzati e famiglie",
        "ideal_prem_n": "utenti avanzati, famiglie e più dispositivi",
        "m365_personal_payoff": "Per 1 persona",
        "m365_family_payoff": "Fino a 6 persone",
        "m365_kasp_name": "Microsoft 365 + Kaspersky",
        "m365_kasp_payoff": "Personal + Kaspersky Premium 5 dispositivi",
        "m365_mcafee_name": "Microsoft 365 + McAfee",
        "m365_mcafee_payoff": "Personal + McAfee 5 dispositivi",
        "brand_aria": "Scegli il brand",
        "name_norton_std": "Norton 360 Standard",
        "name_norton_deluxe": "Norton 360 Deluxe",
        "role_norton_std": "Protezione essenziale",
        "role_norton_deluxe": "Protezione consigliata",
        "sub_norton_std": "Antivirus, VPN e backup cloud per un dispositivo.",
        "sub_norton_deluxe": "Sicurezza completa con VPN, password manager e controllo genitori.",
        "feat_norton_std": ["Antivirus in tempo reale", "VPN sicura inclusa", "Backup cloud 10 GB"],
        "feat_norton_deluxe": ["Tutto di Standard", "Password manager e controllo genitori", "Backup cloud 25 GB"],
        "ideal_norton_std": "uso personale e navigazione quotidiana",
        "ideal_norton_deluxe": "famiglie con più dispositivi da proteggere",
        "role_devices_1": "Protezione essenziale",
        "role_devices_5": "Protezione consigliata",
        "role_devices_10": "Copertura estesa",
        "ideal_devices_1": "un solo dispositivo, uso personale",
        "ideal_devices_5": "famiglie con più dispositivi",
        "ideal_devices_10": "chi deve proteggere molti dispositivi",
        "name_eset": "ESET NOD32 Antivirus",
        "sub_eset": "Motore antivirus leggero, con impatto minimo sulle prestazioni del PC.",
        "feat_eset": ["Scansione antivirus in tempo reale", "Protezione anti-phishing", "Impatto minimo sulle prestazioni"],
        "name_mcafee": "McAfee Total Protection",
        "sub_mcafee": "Antivirus, firewall e password manager in un'unica suite.",
        "feat_mcafee": ["Antivirus e firewall", "Password manager incluso", "Protezione web e anti-phishing"],
        "name_bitdefender": "Bitdefender Antivirus Plus",
        "sub_bitdefender": "Protezione antivirus multilivello con anti-phishing e anti-frode.",
        "feat_bitdefender": ["Antivirus multilivello", "Anti-phishing e anti-frode", "Password manager incluso"],
    },
    "en": {
        "recommended": "Recommended",
        "year": "/ year",
        "more": "Learn more",
        "note_1": "Available for 1 device",
        "devices_field": "Devices",
        "trust": "Every plan includes digital delivery and official activation.",
        "see_all": "See all antivirus plans",
        "ideal": "Best for:",
        "role_std": "Essential protection",
        "role_plus": "Recommended protection",
        "role_prem": "Complete protection",
        "name_std": "Kaspersky Standard",
        "name_plus": "Kaspersky Plus",
        "name_prem": "Kaspersky Premium",
        "sub_std": "Essential protection for everyday use.",
        "sub_plus": "Complete security for work, shopping and browsing.",
        "sub_prem": "Advanced protection with extra privacy tools.",
        "feat_std": ["Real-time antivirus", "Web protection", "Anti-phishing"],
        "feat_plus": ["Advanced protection", "VPN / passwords as per plan", "Performance tools"],
        "feat_prem": ["Everything in Plus", "Advanced protection and privacy"],
        "ideal_std": "personal use and everyday browsing",
        "ideal_plus": "home, work and online shopping",
        "ideal_prem_1": "advanced users and families",
        "ideal_prem_n": "advanced users, families and multiple devices",
        "m365_personal_payoff": "For 1 person",
        "m365_family_payoff": "Up to 6 people",
        "m365_kasp_name": "Microsoft 365 + Kaspersky",
        "m365_kasp_payoff": "Personal + Kaspersky Premium 5 devices",
        "m365_mcafee_name": "Microsoft 365 + McAfee",
        "m365_mcafee_payoff": "Personal + McAfee 5 devices",
        "brand_aria": "Choose the brand",
        "name_norton_std": "Norton 360 Standard",
        "name_norton_deluxe": "Norton 360 Deluxe",
        "role_norton_std": "Essential protection",
        "role_norton_deluxe": "Recommended protection",
        "sub_norton_std": "Antivirus, VPN and cloud backup for one device.",
        "sub_norton_deluxe": "Complete security with VPN, password manager and parental control.",
        "feat_norton_std": ["Real-time antivirus", "Secure VPN included", "10 GB cloud backup"],
        "feat_norton_deluxe": ["Everything in Standard", "Password manager and parental control", "25 GB cloud backup"],
        "ideal_norton_std": "personal use and everyday browsing",
        "ideal_norton_deluxe": "families with several devices to protect",
        "role_devices_1": "Essential protection",
        "role_devices_5": "Recommended protection",
        "role_devices_10": "Extended coverage",
        "ideal_devices_1": "a single device, personal use",
        "ideal_devices_5": "families with multiple devices",
        "ideal_devices_10": "protecting many devices at once",
        "name_eset": "ESET NOD32 Antivirus",
        "sub_eset": "Lightweight antivirus engine with minimal impact on PC performance.",
        "feat_eset": ["Real-time antivirus scanning", "Anti-phishing protection", "Minimal performance impact"],
        "name_mcafee": "McAfee Total Protection",
        "sub_mcafee": "Antivirus, firewall and password manager in one suite.",
        "feat_mcafee": ["Antivirus and firewall", "Password manager included", "Web protection and anti-phishing"],
        "name_bitdefender": "Bitdefender Antivirus Plus",
        "sub_bitdefender": "Multi-layer antivirus protection with anti-phishing and anti-fraud.",
        "feat_bitdefender": ["Multi-layer antivirus", "Anti-phishing and anti-fraud", "Password manager included"],
    },
    "fr": {
        "recommended": "Conseillé",
        "year": "/ an",
        "more": "En savoir plus",
        "note_1": "Disponible pour 1 appareil",
        "devices_field": "Appareils",
        "trust": "Tous les plans incluent la livraison numérique et l'activation officielle.",
        "see_all": "Voir tous les plans antivirus",
        "ideal": "Idéal pour :",
        "role_std": "Protection essentielle",
        "role_plus": "Protection conseillée",
        "role_prem": "Protection complète",
        "name_std": "Kaspersky Standard",
        "name_plus": "Kaspersky Plus",
        "name_prem": "Kaspersky Premium",
        "sub_std": "Protection essentielle pour un usage quotidien.",
        "sub_plus": "Sécurité complète pour le travail, les achats et la navigation.",
        "sub_prem": "Protection avancée avec des outils de confidentialité.",
        "feat_std": ["Antivirus en temps réel", "Protection web", "Anti-hameçonnage"],
        "feat_plus": ["Protection avancée", "VPN / mots de passe selon l'offre", "Outils de performance"],
        "feat_prem": ["Tout Plus", "Protection avancée et confidentialité"],
        "ideal_std": "un usage personnel et la navigation quotidienne",
        "ideal_plus": "la maison, le travail et les achats en ligne",
        "ideal_prem_1": "les utilisateurs avancés et les familles",
        "ideal_prem_n": "les utilisateurs avancés, les familles et plusieurs appareils",
        "m365_personal_payoff": "Pour 1 personne",
        "m365_family_payoff": "Jusqu'à 6 personnes",
        "m365_kasp_name": "Microsoft 365 + Kaspersky",
        "m365_kasp_payoff": "Personnel + Kaspersky Premium 5 appareils",
        "m365_mcafee_name": "Microsoft 365 + McAfee",
        "m365_mcafee_payoff": "Personnel + McAfee 5 appareils",
        "brand_aria": "Choisissez la marque",
        "name_norton_std": "Norton 360 Standard",
        "name_norton_deluxe": "Norton 360 Deluxe",
        "role_norton_std": "Protection essentielle",
        "role_norton_deluxe": "Protection conseillée",
        "sub_norton_std": "Antivirus, VPN et sauvegarde cloud pour un appareil.",
        "sub_norton_deluxe": "Sécurité complète avec VPN, gestionnaire de mots de passe et contrôle parental.",
        "feat_norton_std": ["Antivirus en temps réel", "VPN sécurisé inclus", "Sauvegarde cloud 10 Go"],
        "feat_norton_deluxe": ["Tout ce qui est dans Standard", "Gestionnaire de mots de passe et contrôle parental", "Sauvegarde cloud 25 Go"],
        "ideal_norton_std": "un usage personnel et la navigation quotidienne",
        "ideal_norton_deluxe": "les familles avec plusieurs appareils à protéger",
        "role_devices_1": "Protection essentielle",
        "role_devices_5": "Protection conseillée",
        "role_devices_10": "Couverture étendue",
        "ideal_devices_1": "un seul appareil, usage personnel",
        "ideal_devices_5": "les familles avec plusieurs appareils",
        "ideal_devices_10": "protéger de nombreux appareils",
        "name_eset": "ESET NOD32 Antivirus",
        "sub_eset": "Moteur antivirus léger, avec un impact minime sur les performances du PC.",
        "feat_eset": ["Analyse antivirus en temps réel", "Protection anti-hameçonnage", "Impact minime sur les performances"],
        "name_mcafee": "McAfee Total Protection",
        "sub_mcafee": "Antivirus, pare-feu et gestionnaire de mots de passe dans une seule suite.",
        "feat_mcafee": ["Antivirus et pare-feu", "Gestionnaire de mots de passe inclus", "Protection web et anti-hameçonnage"],
        "name_bitdefender": "Bitdefender Antivirus Plus",
        "sub_bitdefender": "Protection antivirus multicouche avec anti-hameçonnage et anti-fraude.",
        "feat_bitdefender": ["Antivirus multicouche", "Anti-hameçonnage et anti-fraude", "Gestionnaire de mots de passe inclus"],
    },
    "de": {
        "recommended": "Empfohlen",
        "year": "/ Jahr",
        "more": "Mehr erfahren",
        "note_1": "Verfügbar für 1 Gerät",
        "devices_field": "Geräte",
        "trust": "Jeder Tarif umfasst digitale Lieferung und offizielle Aktivierung.",
        "see_all": "Alle Antivirus-Tarife ansehen",
        "ideal": "Ideal für:",
        "role_std": "Wesentlicher Schutz",
        "role_plus": "Empfohlener Schutz",
        "role_prem": "Umfassender Schutz",
        "name_std": "Kaspersky Standard",
        "name_plus": "Kaspersky Plus",
        "name_prem": "Kaspersky Premium",
        "sub_std": "Wesentlicher Schutz für den Alltag.",
        "sub_plus": "Umfassende Sicherheit für Arbeit, Einkauf und Surfen.",
        "sub_prem": "Erweiterter Schutz mit Extra-Datenschutz.",
        "feat_std": ["Echtzeit-Antivirus", "Webschutz", "Anti-Phishing"],
        "feat_plus": ["Erweiterter Schutz", "VPN / Passwörter laut Tarif", "Performance-Tools"],
        "feat_prem": ["Alles aus Plus", "Erweiterter Schutz und Datenschutz"],
        "ideal_std": "private Nutzung und alltägliches Surfen",
        "ideal_plus": "Zuhause, Arbeit und Online-Einkäufe",
        "ideal_prem_1": "Fortgeschrittene Nutzer und Familien",
        "ideal_prem_n": "Fortgeschrittene Nutzer, Familien und mehrere Geräte",
        "m365_personal_payoff": "Für 1 Person",
        "m365_family_payoff": "Bis zu 6 Personen",
        "m365_kasp_name": "Microsoft 365 + Kaspersky",
        "m365_kasp_payoff": "Personal + Kaspersky Premium 5 Geräte",
        "m365_mcafee_name": "Microsoft 365 + McAfee",
        "m365_mcafee_payoff": "Personal + McAfee 5 Geräte",
        "brand_aria": "Marke wählen",
        "name_norton_std": "Norton 360 Standard",
        "name_norton_deluxe": "Norton 360 Deluxe",
        "role_norton_std": "Wesentlicher Schutz",
        "role_norton_deluxe": "Empfohlener Schutz",
        "sub_norton_std": "Antivirus, VPN und Cloud-Backup für ein Gerät.",
        "sub_norton_deluxe": "Umfassende Sicherheit mit VPN, Passwort-Manager und Kindersicherung.",
        "feat_norton_std": ["Echtzeit-Antivirus", "Sicheres VPN inklusive", "10 GB Cloud-Backup"],
        "feat_norton_deluxe": ["Alles aus Standard", "Passwort-Manager und Kindersicherung", "25 GB Cloud-Backup"],
        "ideal_norton_std": "private Nutzung und alltägliches Surfen",
        "ideal_norton_deluxe": "Familien mit mehreren zu schützenden Geräten",
        "role_devices_1": "Wesentlicher Schutz",
        "role_devices_5": "Empfohlener Schutz",
        "role_devices_10": "Erweiterte Abdeckung",
        "ideal_devices_1": "ein Gerät, private Nutzung",
        "ideal_devices_5": "Familien mit mehreren Geräten",
        "ideal_devices_10": "Schutz für viele Geräte gleichzeitig",
        "name_eset": "ESET NOD32 Antivirus",
        "sub_eset": "Schlanke Antivirus-Engine mit minimaler Auswirkung auf die PC-Leistung.",
        "feat_eset": ["Echtzeit-Virenscan", "Anti-Phishing-Schutz", "Minimale Leistungsbeeinträchtigung"],
        "name_mcafee": "McAfee Total Protection",
        "sub_mcafee": "Antivirus, Firewall und Passwort-Manager in einer Suite.",
        "feat_mcafee": ["Antivirus und Firewall", "Passwort-Manager inklusive", "Webschutz und Anti-Phishing"],
        "name_bitdefender": "Bitdefender Antivirus Plus",
        "sub_bitdefender": "Mehrschichtiger Virenschutz mit Anti-Phishing und Betrugsschutz.",
        "feat_bitdefender": ["Mehrschichtiges Antivirus", "Anti-Phishing und Betrugsschutz", "Passwort-Manager inklusive"],
    },
    "es": {
        "recommended": "Recomendado",
        "year": "/ año",
        "more": "Saber más",
        "note_1": "Disponible para 1 dispositivo",
        "devices_field": "Dispositivos",
        "trust": "Todos los planes incluyen entrega digital y activación oficial.",
        "see_all": "Ver todos los planes antivirus",
        "ideal": "Ideal para:",
        "role_std": "Protección esencial",
        "role_plus": "Protección recomendada",
        "role_prem": "Protección completa",
        "name_std": "Kaspersky Standard",
        "name_plus": "Kaspersky Plus",
        "name_prem": "Kaspersky Premium",
        "sub_std": "Protección esencial para el uso diario.",
        "sub_plus": "Seguridad completa para trabajo, compras y navegación.",
        "sub_prem": "Protección avanzada con privacidad extra.",
        "feat_std": ["Antivirus en tiempo real", "Protección web", "Anti-phishing"],
        "feat_plus": ["Protección avanzada", "VPN / contraseñas según el plan", "Herramientas de rendimiento"],
        "feat_prem": ["Todo de Plus", "Protección avanzada y privacidad"],
        "ideal_std": "uso personal y navegación diaria",
        "ideal_plus": "casa, trabajo y compras online",
        "ideal_prem_1": "usuarios avanzados y familias",
        "ideal_prem_n": "usuarios avanzados, familias y varios dispositivos",
        "m365_personal_payoff": "Para 1 persona",
        "m365_family_payoff": "Hasta 6 personas",
        "m365_kasp_name": "Microsoft 365 + Kaspersky",
        "m365_kasp_payoff": "Personal + Kaspersky Premium 5 dispositivos",
        "m365_mcafee_name": "Microsoft 365 + McAfee",
        "m365_mcafee_payoff": "Personal + McAfee 5 dispositivos",
        "brand_aria": "Elige la marca",
        "name_norton_std": "Norton 360 Standard",
        "name_norton_deluxe": "Norton 360 Deluxe",
        "role_norton_std": "Protección esencial",
        "role_norton_deluxe": "Protección recomendada",
        "sub_norton_std": "Antivirus, VPN y copia de seguridad en la nube para un dispositivo.",
        "sub_norton_deluxe": "Seguridad completa con VPN, gestor de contraseñas y control parental.",
        "feat_norton_std": ["Antivirus en tiempo real", "VPN segura incluida", "Copia de seguridad en la nube de 10 GB"],
        "feat_norton_deluxe": ["Todo lo de Standard", "Gestor de contraseñas y control parental", "Copia de seguridad en la nube de 25 GB"],
        "ideal_norton_std": "uso personal y navegación diaria",
        "ideal_norton_deluxe": "familias con varios dispositivos que proteger",
        "role_devices_1": "Protección esencial",
        "role_devices_5": "Protección recomendada",
        "role_devices_10": "Cobertura amplia",
        "ideal_devices_1": "un solo dispositivo, uso personal",
        "ideal_devices_5": "familias con varios dispositivos",
        "ideal_devices_10": "proteger muchos dispositivos a la vez",
        "name_eset": "ESET NOD32 Antivirus",
        "sub_eset": "Motor antivirus ligero, con impacto mínimo en el rendimiento del PC.",
        "feat_eset": ["Análisis antivirus en tiempo real", "Protección anti-phishing", "Impacto mínimo en el rendimiento"],
        "name_mcafee": "McAfee Total Protection",
        "sub_mcafee": "Antivirus, firewall y gestor de contraseñas en una sola suite.",
        "feat_mcafee": ["Antivirus y firewall", "Gestor de contraseñas incluido", "Protección web y anti-phishing"],
        "name_bitdefender": "Bitdefender Antivirus Plus",
        "sub_bitdefender": "Protección antivirus multicapa con anti-phishing y antifraude.",
        "feat_bitdefender": ["Antivirus multicapa", "Anti-phishing y antifraude", "Gestor de contraseñas incluido"],
    },
}

PREMIUM_BY_N = {
    "1": ("KL1047TDAFS", "kaspersky-premium-1-device"),
    "3": ("KL1047GDCFS1", "kaspersky-premium-3-devices"),
    "5": ("KL1047GDEFS", "kaspersky-premium-5-devices"),
    "10": ("KL1047GDKFS", "kaspersky-premium-10-devices"),
}

M365_SKUS = (
    ("QQ2-00012", "microsoft-365-personal", "m365_personal", "m365_personal_payoff"),
    ("6GQ-00092", "microsoft-365-family", "m365_family", "m365_family_payoff"),
    ("SC_M365_KPremium_5Device", "bundle-m365-personal-kaspersky", "m365_kasp_name", "m365_kasp_payoff"),
    ("SC_M365P_MTOTPROT_5Device", "bundle-m365-personal-mcafee", "m365_mcafee_name", "m365_mcafee_payoff"),
)

# --- Protection Selector multi-brand ------------------------------------
# Un solo brand ("kaspersky") ha davvero 3 tier (Standard/Plus/Premium).
# Norton ha solo 2 tier reali a catalogo (nessun "Premium"). ESET, McAfee e
# Bitdefender sono ciascuno UN SOLO prodotto differenziato per numero di
# dispositivi: qui NON si inventano tier, si mostrano 3 tagli rappresentativi
# (1/5/10, gli unici comuni a tutti e tre) come "pseudo-tier" a dispositivi
# fissi, coerenti con lo stesso layout a card.
BRAND_ORDER = ("kaspersky", "norton", "eset", "mcafee", "bitdefender")

BRAND_META = {
    "kaspersky": {
        "mode": "tier-select",
        "label": "Kaspersky",
        "logo_src": "../asset/icon/img-aml-store_Kaspersky-Icon.png",
        "logo_kind": "icon",
        "logo_w": 28,
        "logo_h": 28,
    },
    "norton": {
        "mode": "tier-fixed",
        "label": "Norton",
        "logo_src": "../asset/vendor_logo/img-aml-store_Norton_logo.svg",
        "logo_kind": "wordmark",
        "logo_w": 34,
        "logo_h": 36,
    },
    "eset": {
        "mode": "devices",
        "label": "ESET",
        "logo_src": "../asset/vendor_logo/img-aml-store_ESET_logo.svg",
        "logo_kind": "wordmark",
        "logo_w": 70,
        "logo_h": 28,
    },
    "mcafee": {
        "mode": "devices",
        "label": "McAfee",
        "logo_src": "../asset/vendor_logo/img-aml-store_McAfee_logo.svg",
        "logo_kind": "wordmark",
        "logo_w": 98,
        "logo_h": 22,
    },
    "bitdefender": {
        "mode": "devices",
        "label": "Bitdefender",
        "logo_src": "../asset/icon/img-aml-store_Bitdefender-Icon.png",
        "logo_kind": "icon",
        "logo_w": 28,
        "logo_h": 28,
    },
}

NORTON_TIERS = {
    "standard": ("21395096E7", "norton-360-standard", 1),
    "deluxe": ("NORT_360DEL_3D_1A", "norton-360-deluxe", 3),
}

DEVICES_MODE_BY_N = {
    "eset": {
        "1": ("EAVH-N1-A1", "eset-nod32-1-device"),
        "5": ("EAVH-N1-A5", "eset-nod32-5-devices"),
        "10": ("EAVH-N1-A10", "eset-nod32-10-devices"),
    },
    "mcafee": {
        "1": ("1108921", "mcafee-total-protection-1-device"),
        "5": ("1108923", "mcafee-total-protection-5-devices"),
        "10": ("MTP00MNRXRAAD", "mcafee-total-protection-10-devices"),
    },
    "bitdefender": {
        "1": ("7470A", "bitdefender-plus-1-device"),
        "5": ("TL11012001-EN-5D", "bitdefender-plus-5-devices"),
        "10": ("TL11011010-DE", "bitdefender-plus-10-devices"),
    },
}
DEVICES_MODE_BRANDS = ("eset", "mcafee", "bitdefender")
DEVICES_MODE_FEATURED_N = "5"


def catalog_offer(sku: str, slug: str) -> dict:
    e = entry(sku)
    sale = e["unitAmountMinor"]
    compare = e["compareAtMinor"]
    return {
        "sku": sku,
        "amount": sale,
        "compare": compare,
        "disc": pct(sale, compare),
        "slug": slug,
    }


def devices_label(lang: str, n: int) -> str:
    return COPY[lang]["chip"].format(n=n, sfx=plural_sfx(lang, n))


def stripe_attrs(offer: dict) -> str:
    # data-cart-image riusa la stessa convenzione slug -> products/<slug>.webp
    # gia' usata dalle card prodotto: unica fonte per SKU/slug/immagine, nessuna
    # mappa duplicata da mantenere in js/cart.js.
    return (
        f'data-stripe-currency="eur" '
        f'data-stripe-unit-amount="{offer["amount"]}" '
        f'data-stripe-compare-at-amount="{offer["compare"]}" '
        f'data-stripe-product-sku="{offer["sku"]}" '
        f'data-discount-percent="{offer["disc"]}" '
        f'data-cart-image="../asset/media/products/{offer["slug"]}.webp"'
    )


def features_html(items: list[str], extra: str = "", extra_attr: str = "") -> str:
    rows = [f"                        <li>{item}</li>" for item in items]
    if extra:
        attr = f" {extra_attr}" if extra_attr else ""
        rows.append(f"                        <li{attr}>{extra}</li>")
    return "\n".join(rows)

ICON_AV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
ICON_M365 = '<svg viewBox="0 0 50 50" fill="currentColor"><path d="M20.13,32.5c-2.79-1.69-4.53-4.77-4.53-8.04V8.9c0-1.63,0.39-3.19,1.11-4.57L7.54,9.88C4.74,11.57,3,14.65,3,17.92v14.15c0,1.59,0.42,3.14,1.16,4.5c0.69,1.12,1.67,2.06,2.88,2.74c2.53,1.42,5.51,1.36,7.98-0.15l8.02-4.9L20.13,32.5z M42.84,27.14l-8.44-5.05v2.29c0,3.25-1.72,6.33-4.49,8.02l-13.84,8.47c-1.52,0.93-3.19,1.42-4.87,1.46l8.93,5.41c1.5,0.91,3.19,1.36,4.87,1.36s3.37-0.45,4.87-1.36l9.08-5.5l3.52-2.13c0.27-0.16,0.53-0.34,0.78-0.54c0.08-0.05,0.16-0.11,0.23-0.16c0.65-0.53,1.23-1.13,1.71-1.79c0.02-0.03,0.04-0.06,0.06-0.09c0.77-1.19,1.2-2.59,1.19-4.06C46.43,30.85,45.09,28.48,42.84,27.14z M42.46,9.88l-9.57-5.79l-3.02-1.83C29.45,2,29.01,1.79,28.56,1.61c-0.49-0.21-1-0.37-1.51-0.47c-1.84-0.38-3.76-0.08-5.46,0.89c-2.5,1.43-3.99,3.99-3.99,6.87v9.6l2.8-1.65c2.84-1.67,6.36-1.66,9.19,0.03l14.28,8.54c1.29,0.78,2.35,1.81,3.12,3.02L47,17.92C47,14.65,45.26,11.57,42.46,9.88z"></path></svg>'
ICON_WIN = '<svg viewBox="0 0 14 14" fill="currentColor"><path d="m 5.91827,7.331731 v 4.694712 L 1,11.348557 V 7.331731 h 4.91827 z m 0,-5.358174 V 6.725962 H 1 V 2.651443 z M 13,7.331731 V 13 L 6.45913,12.098557 V 7.331731 H 13 z M 13,1 V 6.725962 H 6.45913 V 1.901443 z"></path></svg>'
ICON_OFF = '<svg viewBox="0 0 50 50" fill="currentColor"><path d="M43 11.11v27.6c0 2.54-1.73 4.77-4.21 5.43l-8.63 2.41c.5-.94.78-2.02.78-3.16V5.65c0-.86-.19-1.68-.53-2.42l8.45 2.47C41.29 6.37 43 8.6 43 11.11zM28.94 37v6.39c0 1.99-1.19 3.72-2.96 4.33-.43.1-.87.15-1.31.15-1 0-2-.26-2.92-.76L13.45 42c-1.04-.64-1.52-1.86-1.19-3.04.33-1.17 1.38-1.96 2.6-1.96H28.94zM28.94 5.65v5.72l-10.28 3.64c-.99.36-1.66 1.3-1.66 2.36v13.36c0 1.09-.59 2.1-1.54 2.62l-4.07 2.27C10.94 35.88 10.44 36 9.95 36c-.51 0-1.03-.14-1.49-.41C7.54 35.05 7 34.1 7 33.05V14.83c0-1.93 1.04-3.72 2.72-4.68L22.8 2.71c1.08-.61 2.28-.83 3.45-.65.07.06.16.11.26.14C27.72 2.6 28.94 3.82 28.94 5.65z"></path></svg>'


def plural_sfx(lang: str, n: int) -> str:
    if lang == "de":
        return "" if n == 1 else "e"
    if lang == "en":
        return "" if n == 1 else "s"
    if lang == "fr":
        return "" if n == 1 else "s"
    if n == 1:
        return "o" if lang in ("it", "es") else ""
    return "i" if lang == "it" else "s"


def extract_div(html: str, cls: str) -> tuple[str, int, int] | None:
    needle = f'class="{cls}"'
    idx = html.find(needle)
    if idx < 0:
        return None
    start = html.rfind("<div", 0, idx)
    i = start
    depth = 0
    while i < len(html):
        if html.startswith("<div", i):
            depth += 1
            i = html.find(">", i) + 1
        elif html.startswith("</div>", i):
            depth -= 1
            i += 6
            if depth == 0:
                return html[start:i], start, i
        else:
            i += 1
    raise ValueError(cls)


def reorder_blocks(html: str, classes: list[str], new_order: list[str]) -> str:
    found = {}
    spans = []
    for cls in classes:
        hit = extract_div(html, cls)
        if not hit:
            return html
        block, start, end = hit
        found[cls] = block
        spans.append((start, end, cls))
    spans.sort()
    first, last = spans[0][0], spans[-1][1]
    between = []
    for i, (start, end, cls) in enumerate(spans[:-1]):
        nxt = spans[i + 1][0]
        between.append(html[end:nxt])
    sep = between[0] if between else "\n"
    rebuilt = sep.join(found[cls] for cls in new_order)
    return html[:first] + rebuilt + html[last:]


def reorder_chrome_source() -> None:
    header = ROOT / "scripts" / "chrome-renderer" / "header.js"
    text = header.read_text(encoding="utf-8")
    text = reorder_blocks(
        text,
        ["nav-win-wrap", "nav-office-wrap", "nav-m365-wrap", "nav-av-wrap"],
        ["nav-av-wrap", "nav-m365-wrap", "nav-win-wrap", "nav-office-wrap"],
    )
    text = reorder_blocks(
        text,
        ["drawer-win-block", "drawer-office-block", "drawer-m365-block", "drawer-bundle-block", "drawer-av-block"],
        ["drawer-av-block", "drawer-m365-block", "drawer-bundle-block", "drawer-win-block", "drawer-office-block"],
    )
    header.write_text(text, encoding="utf-8", newline="\n")

    footer = ROOT / "scripts" / "chrome-renderer" / "footer.js"
    ft = footer.read_text(encoding="utf-8")
    ft = re.sub(
        r"(<ul class=\"link-list\">\s*)"
        r"<li><a href=\"\$\{esc\(pageHref\('sistemi-operativi'\)\)\}\">\$\{esc\(t\.prodOs\)\}</a></li>\s*"
        r"<li><a href=\"\$\{esc\(pageHref\('suite-office'\)\)\}\">\$\{esc\(t\.prodOffice\)\}</a></li>\s*"
        r"<li><a href=\"\$\{esc\(pageHref\('microsoft-365-solutions'\)\)\}\">\$\{esc\(t\.prodM365\)\}</a></li>\s*"
        r"<li><a href=\"\$\{esc\(pageHref\('antivirus'\)\)\}\">\$\{esc\(t\.prodAntivirus\)\}</a></li>",
        r"\1<li><a href=\"${esc(pageHref('antivirus'))}\">${esc(t.prodAntivirus)}</a></li>\n"
        r"                                    <li><a href=\"${esc(pageHref('microsoft-365-solutions'))}\">${esc(t.prodM365)}</a></li>\n"
        r"                                    <li><a href=\"${esc(pageHref('sistemi-operativi'))}\">${esc(t.prodOs)}</a></li>\n"
        r"                                    <li><a href=\"${esc(pageHref('suite-office'))}\">${esc(t.prodOffice)}</a></li>",
        ft,
        count=1,
    )
    footer.write_text(ft, encoding="utf-8", newline="\n")


def reorder_footer_catalog(html: str, lang: str) -> str:
    def repl(m: re.Match[str]) -> str:
        block = m.group(0)
        items = re.findall(r"<li>.*?</li>", block, flags=re.DOTALL)
        by_href = {}
        for item in items:
            hm = re.search(rf'href="/{lang}/([^"]+)"', item)
            if hm:
                by_href[hm.group(1)] = item
        order = ["antivirus", "microsoft-365-solutions", "sistemi-operativi", "suite-office"]
        if not all(k in by_href for k in order):
            return block
        rebuilt = "\n                                    ".join(by_href[k] for k in order)
        return re.sub(r"(<ul class=\"link-list\">\s*).*(</ul>)", rf"\1{rebuilt}\n                                \2", block, count=1, flags=re.DOTALL)

    return re.sub(
        rf'<section class="nav-col" aria-labelledby="footer-catalog-{lang}">.*?</section>',
        repl,
        html,
        count=1,
        flags=re.DOTALL,
    )


def reorder_all_chrome_html() -> int:
    n = 0
    for lang in LANGS:
        for path in sorted((ROOT / lang).glob("*.html")):
            html = path.read_text(encoding="utf-8")
            orig = html
            html = reorder_blocks(
                html,
                ["nav-win-wrap", "nav-office-wrap", "nav-m365-wrap", "nav-av-wrap"],
                ["nav-av-wrap", "nav-m365-wrap", "nav-win-wrap", "nav-office-wrap"],
            )
            html = reorder_blocks(
                html,
                ["drawer-win-block", "drawer-office-block", "drawer-m365-block", "drawer-bundle-block", "drawer-av-block"],
                ["drawer-av-block", "drawer-m365-block", "drawer-bundle-block", "drawer-win-block", "drawer-office-block"],
            )
            html = reorder_footer_catalog(html, lang)
            if html != orig:
                path.write_text(html, encoding="utf-8", newline="\n")
                n += 1
    return n


def patch_seo(html: str, lang: str) -> str:
    s = SEO[lang]
    html = re.sub(r"<title>[^<]*</title>", f"<title>{s['title']}</title>", html, count=1)
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{s["desc"]}">',
        html,
        count=1,
    )
    html = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{s["title"]}">', html, count=1)
    html = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{s["desc"]}">', html, count=1)
    html = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{s["title"]}">', html, count=1)
    html = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{s["desc"]}">', html, count=1)
    html = html.replace(
        '"name": "Software originale per privati e aziende | Aml Store"',
        f'"name": "{s["title"]}"',
    )
    html = html.replace(
        '"name": "Original software for individuals and businesses | Aml Store"',
        f'"name": "{s["title"]}"',
    )
    html = re.sub(
        r'("url":\s*"https://aml-store.com/' + lang + r'/",\s*"name":\s*")[^"]+(")',
        rf'\1{s["title"]}\2',
        html,
        count=1,
    )
    html = re.sub(
        r'("#webpage","url":"https://aml-store.com/' + lang + r'/","name":")[^"]+(")',
        rf'\1{s["title"]}\2',
        html,
        count=1,
    )
    html = re.sub(
        r'("#webpage", "url": "https://aml-store.com/' + lang + r'/", "name": ")[^"]+(")',
        rf'\1{s["title"]}\2',
        html,
        count=1,
    )
    html = re.sub(
        rf'("#webpage".{{0,120}}"description":\s*")[^"]+(")',
        rf'\1{s["desc"]}\2',
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def patch_hero(html: str, lang: str) -> str:
    h = HERO[lang]
    html = re.sub(
        r'(<h1 id="home-hero-title" class="home-hero-title">)[\s\S]*?(</h1>)',
        rf'\1{h["h1_a"]}<br><span class="home-hero__accent">{h["h1_b"]}</span>\2',
        html,
        count=1,
    )
    html = re.sub(
        r'(<p class="home-hero-subtitle">)[\s\S]*?(</p>)',
        rf'\1{h["sub"]}\2',
        html,
        count=1,
    )
    return html


def reorder_vendors(html: str) -> str:
    m = re.search(r'(<ul class="home-vendors__list">)(.*?)(</ul>)', html, flags=re.DOTALL)
    if not m:
        return html
    items = re.findall(r"<li>.*?</li>", m.group(2), flags=re.DOTALL)
    def key(item: str) -> int:
        order = ["Kaspersky", "Norton", "ESET", "McAfee", "Bitdefender", "Microsoft"]
        for i, name in enumerate(order):
            if f'alt="{name}"' in item:
                return i
        return 99
    items.sort(key=key)
    inner = "\n                ".join(items)
    return html[: m.start()] + m.group(1) + "\n                " + inner + "\n            " + m.group(3) + html[m.end() :]


def tile(href: str, icon: str, name: str, desc: str) -> str:
    return f"""                <li>
                    <a href="{href}" class="home-category-tile">
                        <span class="home-category-icon" aria-hidden="true">{icon}</span>
                        <span class="home-category-copy">
                            <span class="home-category-name">{name}</span>
                            <span class="home-category-desc">{desc}</span>
                        </span>
                        <span class="home-category-arrow" aria-hidden="true">&rarr;</span>
                    </a>
                </li>"""


def extra_sections(lang: str) -> str:
    return protect_section(lang) + "\n" + m365_section(lang)


def protect_matrix(lang: str) -> dict:
    ui = PLAN_UI[lang]
    std = catalog_offer("KASP_STD_1D_1A", "kaspersky-standard")
    plus = catalog_offer("KASP_PLUS_1D_1A", "kaspersky-plus")
    devices = {}
    for n in ("1", "3", "5", "10"):
        sku, slug = PREMIUM_BY_N[n]
        prem = catalog_offer(sku, slug)
        count = int(n)
        prem["devices"] = count
        prem["devicesLabel"] = devices_label(lang, count)
        prem["ideal"] = ui["ideal_prem_1"] if n == "1" else ui["ideal_prem_n"]
        devices[n] = {
            "featured": "plus" if n == "1" else "premium",
            "premium": prem,
        }
    return {"fixed": {"standard": std, "plus": plus}, "devices": devices}


DEVICE_OPTIONS = (1, 3, 5, 10)


def devices_field_html(lang: str, plan: str, offer: dict) -> str:
    ui = PLAN_UI[lang]
    if plan != "premium":
        return (
            f'<p class="plan-card__devices">'
            f'<span class="plan-card__devices-label">{ui["devices_field"]}</span>'
            f'<span class="plan-card__devices-pill">{devices_label(lang, 1)}</span>'
            f'</p>'
        )
    current = offer.get("devices", 1)
    opts = []
    for n in DEVICE_OPTIONS:
        sel = " selected" if n == current else ""
        opts.append(f'<option value="{n}"{sel}>{devices_label(lang, n)}</option>')
    return (
        f'<p class="plan-card__devices">'
        f'<label class="plan-card__devices-label" for="home-protect-devices-premium">{ui["devices_field"]}</label>'
        f'<select class="plan-card__devices-select" id="home-protect-devices-premium" data-plan-devices-select>'
        f'{"".join(opts)}</select>'
        f'</p>'
    )


def brand_logo_html(brand: str) -> str:
    meta = BRAND_META[brand]
    cls = "plan-card__brand-icon"
    if meta["logo_kind"] == "wordmark":
        cls += " plan-card__brand-icon--wordmark"
    return (
        f'<img class="{cls}" src="{meta["logo_src"]}" alt="" '
        f'width="{meta["logo_w"]}" height="{meta["logo_h"]}" loading="lazy">'
    )


def plan_card_html(lang: str, plan: str, offer: dict, featured: bool) -> str:
    ui = PLAN_UI[lang]
    labels = BASE_LABELS[lang]
    role = {"standard": ui["role_std"], "plus": ui["role_plus"], "premium": ui["role_prem"]}[plan]
    name = {"standard": ui["name_std"], "plus": ui["name_plus"], "premium": ui["name_prem"]}[plan]
    sub = {"standard": ui["sub_std"], "plus": ui["sub_plus"], "premium": ui["sub_prem"]}[plan]
    feats = {"standard": ui["feat_std"], "plus": ui["feat_plus"], "premium": ui["feat_prem"]}[plan]
    ideal = {"standard": ui["ideal_std"], "plus": ui["ideal_plus"], "premium": ui["ideal_prem_1"]}[plan]
    feat_html = features_html(feats)
    featured_cls = " is-featured" if featured else ""
    ideal_attr = " data-plan-ideal-value" if plan == "premium" else ""
    devices_html = devices_field_html(lang, plan, offer)
    return f"""                <article class="plan-card plan-card--{plan}{featured_cls}" data-plan="{plan}" {stripe_attrs(offer)}>
                    <p class="plan-card__badge"><span class="plan-card__badge-icon" aria-hidden="true">★</span>{ui['recommended']}</p>
                    <div class="plan-card__brand">
                        {brand_logo_html("kaspersky")}
                        <div class="plan-card__brand-text">
                            <p class="plan-card__role">{role}</p>
                            <h3 class="plan-card__name">{name}</h3>
                        </div>
                    </div>
                    <p class="plan-card__sub">{sub}</p>
                    <div class="plan-card__price">
                        <span class="plan-card__price-sale">€ <span data-plan-price>{eur_fmt(offer['amount'])}</span></span>
                        <span class="plan-card__price-msrp" data-plan-msrp>€ {eur_fmt(offer['compare'])}</span>
                    </div>
                    <p class="plan-card__price-period">{ui['year']}</p>
                    {devices_html}
                    <ul class="plan-card__features">
{feat_html}
                    </ul>
                    <p class="plan-card__ideal"><strong>{ui['ideal']}</strong> <span{ideal_attr}>{ideal}</span></p>
                    <button type="button" class="btn-cta-primary" data-cart-add>{labels['add']}</button>
                    <a class="plan-card__more" data-plan-more href="{offer['slug']}">{ui['more']}</a>
                </article>
"""


def fixed_devices_pill_html(lang: str, n: int) -> str:
    ui = PLAN_UI[lang]
    return (
        f'<p class="plan-card__devices">'
        f'<span class="plan-card__devices-label">{ui["devices_field"]}</span>'
        f'<span class="plan-card__devices-pill">{devices_label(lang, n)}</span>'
        f'</p>'
    )


def generic_plan_card_html(
    lang: str,
    brand: str,
    card_key: str,
    name: str,
    role: str,
    sub: str,
    feats: list[str],
    ideal: str,
    offer: dict,
    devices_n: int,
    featured: bool,
    default_featured: bool = False,
) -> str:
    ui = PLAN_UI[lang]
    labels = BASE_LABELS[lang]
    feat_html = features_html(feats)
    featured_cls = " is-featured" if featured else ""
    default_attr = " data-default-featured" if default_featured else ""
    devices_html = fixed_devices_pill_html(lang, devices_n)
    return f"""                <article class="plan-card plan-card--brand-{brand}{featured_cls}" data-plan="{card_key}" data-devices="{devices_n}"{default_attr} {stripe_attrs(offer)}>
                    <p class="plan-card__badge"><span class="plan-card__badge-icon" aria-hidden="true">★</span>{ui['recommended']}</p>
                    <div class="plan-card__brand">
                        {brand_logo_html(brand)}
                        <div class="plan-card__brand-text">
                            <p class="plan-card__role">{role}</p>
                            <h3 class="plan-card__name">{name}</h3>
                        </div>
                    </div>
                    <p class="plan-card__sub">{sub}</p>
                    <div class="plan-card__price">
                        <span class="plan-card__price-sale">€ <span data-plan-price>{eur_fmt(offer['amount'])}</span></span>
                        <span class="plan-card__price-msrp" data-plan-msrp>€ {eur_fmt(offer['compare'])}</span>
                    </div>
                    <p class="plan-card__price-period">{ui['year']}</p>
                    {devices_html}
                    <ul class="plan-card__features">
{feat_html}
                    </ul>
                    <p class="plan-card__ideal"><strong>{ui['ideal']}</strong> <span>{ideal}</span></p>
                    <button type="button" class="btn-cta-primary" data-cart-add>{labels['add']}</button>
                    <a class="plan-card__more" data-plan-more href="{offer['slug']}">{ui['more']}</a>
                </article>
"""


def kaspersky_panel_html(lang: str) -> str:
    matrix = protect_matrix(lang)
    std = matrix["fixed"]["standard"]
    plus = matrix["fixed"]["plus"]
    prem = matrix["devices"]["1"]["premium"]
    payload = json.dumps(matrix, ensure_ascii=False, separators=(",", ":"))
    cards = (
        plan_card_html(lang, "standard", std, False)
        + plan_card_html(lang, "plus", plus, True)
        + plan_card_html(lang, "premium", prem, False)
    )
    return f"""                <div class="plan-grid" data-protect-brand-panel="kaspersky" data-plan-mode="tier-select">
{cards}                    <script type="application/json" data-protect-matrix>{payload}</script>
                </div>"""


def norton_panel_html(lang: str) -> str:
    ui = PLAN_UI[lang]
    std_sku, std_slug, std_n = NORTON_TIERS["standard"]
    del_sku, del_slug, del_n = NORTON_TIERS["deluxe"]
    std_offer = catalog_offer(std_sku, std_slug)
    del_offer = catalog_offer(del_sku, del_slug)
    cards = (
        generic_plan_card_html(
            lang, "norton", "standard", ui["name_norton_std"], ui["role_norton_std"], ui["sub_norton_std"],
            ui["feat_norton_std"], ui["ideal_norton_std"], std_offer, std_n, False,
        )
        + generic_plan_card_html(
            lang, "norton", "deluxe", ui["name_norton_deluxe"], ui["role_norton_deluxe"], ui["sub_norton_deluxe"],
            ui["feat_norton_deluxe"], ui["ideal_norton_deluxe"], del_offer, del_n, True,
        )
    )
    return f"""                <div class="plan-grid plan-grid--count-2" data-protect-brand-panel="norton" data-plan-mode="tier-fixed" hidden>
{cards}                </div>"""


def devices_panel_html(lang: str, brand: str) -> str:
    ui = PLAN_UI[lang]
    name = ui[f"name_{brand}"]
    sub = ui[f"sub_{brand}"]
    feats = ui[f"feat_{brand}"]
    cards = []
    for n in ("1", "5", "10"):
        sku, slug = DEVICES_MODE_BY_N[brand][n]
        offer = catalog_offer(sku, slug)
        role = ui[f"role_devices_{n}"]
        ideal = ui[f"ideal_devices_{n}"]
        default_featured = n == DEVICES_MODE_FEATURED_N
        cards.append(
            generic_plan_card_html(
                lang, brand, f"d{n}", name, role, sub, feats, ideal, offer, int(n),
                default_featured, default_featured,
            )
        )
    return (
        f'                <div class="plan-grid" data-protect-brand-panel="{brand}" data-plan-mode="devices" hidden>\n'
        + "".join(cards)
        + "                </div>"
    )


def protect_brand_tabs_html(lang: str) -> str:
    ui = PLAN_UI[lang]
    buttons = []
    for i, brand in enumerate(BRAND_ORDER):
        selected = i == 0
        cls = ' class="is-selected"' if selected else ""
        pressed = "true" if selected else "false"
        buttons.append(
            f'                    <button type="button"{cls} data-protect-brand="{brand}" aria-pressed="{pressed}">{BRAND_META[brand]["label"]}</button>'
        )
    return (
        f'                <div class="protect-brand-tabs" data-protect-brand-tabs role="group" aria-label="{ui["brand_aria"]}">\n'
        + "\n".join(buttons)
        + "\n                </div>"
    )


def protect_section(lang: str) -> str:
    c = COPY[lang]
    ui = PLAN_UI[lang]
    panels = "\n".join([
        kaspersky_panel_html(lang),
        norton_panel_html(lang),
        devices_panel_html(lang, "eset"),
        devices_panel_html(lang, "mcafee"),
        devices_panel_html(lang, "bitdefender"),
    ])
    return f"""        <section class="home-protect" aria-labelledby="home-protect-title" data-home-protect>
            <div class="home-protect__bg" aria-hidden="true"></div>
            <div class="home-protect__inner">
                <h2 id="home-protect-title" class="home-section-title">{c['protect_title']}</h2>
                <p class="home-catalog-lede">{c['protect_lede']}</p>
{protect_brand_tabs_html(lang)}
{panels}
                <p class="home-protect__trust">{ui['trust']}</p>
                <a class="home-protect__all" href="antivirus">{ui['see_all']}</a>
            </div>
        </section>
"""


def m365_section(lang: str) -> str:
    c = COPY[lang]
    ui = PLAN_UI[lang]
    labels = BASE_LABELS[lang]
    cards = []
    for sku, slug, name_key, payoff_key in M365_SKUS:
        offer = catalog_offer(sku, slug)
        name = c[name_key] if name_key in c else ui[name_key]
        payoff = ui[payoff_key]
        cards.append(
            f"""                    <li>
                        <article class="m365-card" {stripe_attrs(offer)}>
                            <img class="m365-card__icon" src="../asset/icon/img-aml-store_Microsoft-Icon.svg" alt="" width="28" height="28" loading="lazy">
                            <h3 class="m365-card__name">{name}</h3>
                            <p class="m365-card__payoff">{payoff}</p>
                            <div class="m365-card__price">
                                <span class="m365-card__price-sale">€ {eur_fmt(offer['amount'])}</span>
                                <span class="m365-card__price-msrp">€ {eur_fmt(offer['compare'])}</span>
                            </div>
                            <p class="m365-card__price-period">{ui['year']}</p>
                            <button type="button" class="btn-cta-primary" data-cart-add>{labels['add']}</button>
                            <a class="m365-card__more" href="{slug}">{ui['more']}</a>
                        </article>
                    </li>"""
        )
    return f"""        <section class="home-m365-band" aria-labelledby="home-m365-title">
            <div class="home-m365-band__inner">
                <div class="home-m365-hero">
                    <div class="home-m365-hero__content">
                        <span class="home-m365-hero__badge">{c['m365_hero_badge']}</span>
                        <p class="home-m365-hero__title">{c['m365_hero_title']}</p>
                        <p class="home-m365-hero__sub">{c['m365_hero_sub']}</p>
                    </div>
                    <div class="home-m365-hero__media" aria-hidden="true"></div>
                </div>
                <div class="home-m365-band__label">
                    <h2 id="home-m365-title" class="home-section-title">{c['m365_title']}</h2>
                    <p class="home-catalog-lede">{c['m365_lede']}</p>
                </div>
                <div class="home-m365-band__content">
                    <ul class="m365-grid">
{chr(10).join(cards)}
                    </ul>
                    <a class="home-m365-band__cta" href="microsoft-365-solutions">{c['m365_cta']}</a>
                </div>
            </div>
        </section>
"""


def business_section(lang: str) -> str:
    """Sezione "Per aziende" — temporaneamente disattivata in home.

    Non viene piu' chiamata da patch_home(): resta qui per il ripristino.
    """
    c = COPY[lang]
    consult = CONSULT[lang]
    return f"""
        <section class="home-business" aria-labelledby="home-business-title">
            <div class="home-business__inner">
                <div class="home-business__copy">
                    <h2 id="home-business-title" class="home-section-title">{c['biz_title']}</h2>
                    <p class="home-catalog-lede">{c['biz_lede']}</p>
                </div>
                <ul class="home-business__grid">
                    <li><a class="home-business__card" href="microsoft-365-business-standard">{c['biz_m365']}</a></li>
                    <li><a class="home-business__card" href="windows-server">{c['biz_server']}</a></li>
                    <li><a class="home-business__card" href="strumenti">{c['biz_tools']}</a></li>
                </ul>
                <a class="home-business__cta" href="{consult}">{c['biz_cta']}</a>
            </div>
        </section>
"""


def categories_section(lang: str) -> str:
    """Sezione "Altre soluzioni" — temporaneamente disattivata in home.

    Non viene piu' chiamata da patch_home(): resta qui per il ripristino.
    Nota: conteneva l'ancora #soluzioni, ora sostituita da #piu-venduti nei CTA.
    """
    c = COPY[lang]
    names = {
        "it": ("Windows", "Office"),
        "en": ("Windows", "Office"),
        "fr": ("Windows", "Office"),
        "de": ("Windows", "Office"),
        "es": ("Windows", "Office"),
    }
    win, off = names[lang]
    tiles = "\n".join([
        tile("antivirus", ICON_AV, c["av_name"], c["av_desc"]),
        tile("microsoft-365-solutions", ICON_M365, "Microsoft 365", c["m365_desc"]),
        tile("sistemi-operativi", ICON_WIN, win, c["win_desc"]),
        tile("suite-office", ICON_OFF, off, c["off_desc"]),
    ])
    return f"""        <section id="soluzioni" class="home-categories" aria-labelledby="home-categories-title">
            <h2 id="home-categories-title" class="home-section-title">{c['cat_title']}</h2>
            <ul class="home-categories-grid">
{tiles}
            </ul>
        </section>"""


def patch_guide(html: str, lang: str) -> str:
    c = COPY[lang]
    html = re.sub(
        r'(<button type="button" class="home-guide__option) is-selected(" data-guide-category="office" aria-pressed=")true(")',
        r'\1\2false\3',
        html,
        count=1,
    )
    html = re.sub(
        r'(<button type="button" class="home-guide__option)(" data-guide-category="antivirus" aria-pressed=")false(")',
        r'\1 is-selected\2true\3',
        html,
        count=1,
    )
    html = re.sub(
        r'<div class="home-guide__options home-guide__options--inline">.*?</div>',
        lambda m: reorder_guide_cats(m.group(0)),
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = html.replace(
        'data-guide-group="office">',
        'data-guide-group="office" hidden>',
        1,
    )
    html = html.replace(
        'data-guide-group="antivirus" hidden>',
        'data-guide-group="antivirus">',
        1,
    )
    kasp = (
        f'\n                                <button type="button" class="home-guide__option" data-guide-option\n'
        f'                                    aria-pressed="false"\n'
        f'                                    data-guide-href="kaspersky-plus"\n'
        f'                                    data-guide-title-value="{c["kasp_title"]}"\n'
        f'                                    data-guide-body-value="{c["kasp_body"]}">{c["kasp_opt"]}</button>'
    )
    if 'data-guide-href="kaspersky-plus"' not in html:
        html = re.sub(
            r'(data-guide-href="mcafee-total-protection-10-devices"[\s\S]*?</button>)',
            rf'\1{kasp}',
            html,
            count=1,
        )
    html = re.sub(
        r'(<img class="home-guide__result-img"[^>]*src=")[^"]+',
        r'\1../asset/media/products/eset-nod32-1-device.webp',
        html,
        count=1,
    )
    html = re.sub(
        r'(<p class="home-guide__result-title" data-guide-title>)[^<]+',
        rf'\1{c["guide_res_title"]}',
        html,
        count=1,
    )
    html = re.sub(
        r'(<p class="home-guide__result-body" data-guide-body>)[^<]+',
        rf'\1{c["guide_res_body"]}',
        html,
        count=1,
    )
    html = re.sub(
        r'(<a class="home-btn home-btn-primary" href=")[^"]+(" data-guide-link>)',
        r'\1eset-nod32-1-device\2',
        html,
        count=1,
    )
    return html


def reorder_guide_cats(block: str) -> str:
    buttons = re.findall(r"<button[\s\S]*?</button>", block)
    order = ["antivirus", "office", "windows", "business"]
    keyed = {}
    for b in buttons:
        m = re.search(r'data-guide-category="([^"]+)"', b)
        if m:
            keyed[m.group(1)] = b
    if not all(k in keyed for k in order):
        return block
    inner = "\n                            ".join(keyed[k] for k in order)
    return re.sub(r"(<div class=\"home-guide__options home-guide__options--inline\">\s*).*(</div>)", rf"\1{inner}\n                        \2", block, count=1, flags=re.DOTALL)


def collapse_blank_lines_in_main(html: str) -> str:
    """Riduce a una sola le righe vuote consecutive dentro <main>.

    Le sostituzioni di sezione lasciano righe vuote residue che si sommano a
    ogni run: qui vengono normalizzate, senza toccare head/header/footer.
    """
    m = re.search(r"<main\b[\s\S]*?</main>", html)
    if not m:
        return html
    body = re.sub(r"\n(?:[ \t]*\n){2,}", "\n\n", m.group(0))
    return html[: m.start()] + body + html[m.end() :]


def patch_home(lang: str) -> None:
    path = ROOT / lang / "index.html"
    html = path.read_text(encoding="utf-8")
    labels = BASE_LABELS[lang]
    html = patch_seo(html, lang)
    html = patch_hero(html, lang)
    html = reorder_vendors(html)

    cards = "".join(product_card(lang, rhf.featured_prod(lang, p), labels, clean_price=False) for p in rhf.FEATURED)
    catalog = rhf.HOME_COPY[lang]
    catalog_section = f"""<section id="piu-venduti" class="home-catalog" aria-labelledby="catalog-title">
            <h2 id="catalog-title" class="home-section-title">{catalog['catalog_title']}</h2>
            <div class="home-catalog-intro">
                <p class="home-catalog-lede">{catalog['catalog_lede']}</p>
            </div>
            <div class="product-grid">
{cards}            </div>
        </section>"""
    html = rhf.CATALOG_SECTION_RE.sub(catalog_section, html, count=1)

    extras_protect = protect_section(lang)
    extras_m365 = m365_section(lang)
    # I pattern consumano indentazione e newline attorno alla sezione: le
    # stringhe di rimpiazzo li reintroducono gia' loro, altrimenti a ogni run
    # si accumulano 8 spazi di rientro e una riga vuota in piu'.
    if re.search(r'<section class="home-protect"', html):
        html = re.sub(
            r'[ \t]*<section class="home-protect"[\s\S]*?</section>\n?',
            lambda _m: extras_protect,
            html,
            count=1,
        )
        html = re.sub(
            r'[ \t]*<section class="home-m365-band"[\s\S]*?</section>\n?',
            lambda _m: extras_m365,
            html,
            count=1,
        )
    else:
        html = re.sub(
            r'[ \t]*<section id="soluzioni" class="home-categories"[\s\S]*?</section>\n?',
            lambda _m: extras_protect + extras_m365,
            html,
            count=1,
        )

    # Temporaneamente rimossi: 'Altre soluzioni' (.home-categories) e 'Per aziende' (.home-business)
    html = re.sub(r'\n?[ \t]*<section id="soluzioni" class="home-categories"[\s\S]*?</section>', '', html)
    html = re.sub(r'\n?[ \t]*<section class="home-categories"[\s\S]*?</section>', '', html)
    html = re.sub(r'\n?[ \t]*<section class="home-business"[\s\S]*?</section>', '', html)

    if "home-protect.js" not in html:
        html = re.sub(
            r'(<script src="../js/home-guide\.js[^"]*" defer></script>)',
            r'    <script src="../js/home-protect.js" defer></script>\n    \1',
            html,
            count=1,
        )
    html = patch_guide(html, lang)

    # Temporaneamente rimossi: 'Prodotti consigliati' (.home-recommended / #prodotti-consigliati)
    html = re.sub(r'\n?[ \t]*<section id="prodotti-consigliati"[\s\S]*?</section>', '', html)
    html = re.sub(r'\n?[ \t]*<section class="home-recommended"[\s\S]*?</section>', '', html)

    html = collapse_blank_lines_in_main(html)

    path.write_text(html, encoding="utf-8", newline="\n")
    print("home", lang)


def devices_for_slug(slug: str) -> str:
    if "10-device" in slug:
        return "10"
    if "5-device" in slug:
        return "5"
    if "3-device" in slug or "deluxe" in slug:
        return "3"
    if "2-device" in slug:
        return "2"
    return "1"


def brand_for_slug(slug: str) -> str:
    for name in ("kaspersky", "norton", "eset", "mcafee", "bitdefender"):
        if name in slug:
            return name
    return ""


def patch_antivirus(lang: str) -> None:
    path = ROOT / lang / "antivirus.html"
    html = path.read_text(encoding="utf-8")
    c = COPY[lang]
    ui = PLAN_UI[lang]

    def add_data(m: re.Match[str]) -> str:
        open_tag, rest, href = m.group(1), m.group(2), m.group(3)
        # open_tag si ferma a class="product-card": gli attributi già inseriti in una
        # esecuzione precedente stanno in rest, prima del '>' del tag di apertura.
        # Senza controllarli qui, una seconda esecuzione li duplicherebbe.
        tag_attrs = rest.split(">", 1)[0]
        if "data-devices=" in open_tag or "data-devices=" in tag_attrs:
            return m.group(0)
        slug = href.replace(".html", "")
        devices = devices_for_slug(slug)
        brand = brand_for_slug(slug)
        extra = f' data-devices="{devices}"'
        if brand:
            extra += f' data-brand="{brand}"'
        return f'{open_tag}{extra}{rest}{href}'

    html = re.sub(
        r'(<div\s+class="product-card")([^>]*>[\s\S]*?<a href=")([^"]+)',
        add_data,
        html,
    )

    chips = [f'                <button type="button" data-av-filter="all" class="is-selected" aria-pressed="true">{c["filter_all"]}</button>']
    for n in (1, 3, 5, 10):
        chips.append(
            f'                <button type="button" data-av-filter="{n}" aria-pressed="false">{c["filter_n"].format(n=n, sfx=plural_sfx(lang, n))}</button>'
        )
    bar = (
        f'            <div class="av-filters" data-av-filters role="group" aria-label="{c["filter_aria"]}">\n'
        + "\n".join(chips)
        + "\n            </div>\n"
    )
    brand_chips = [f'                <button type="button" data-av-brand="all" class="is-selected" aria-pressed="true">{c["filter_all"]}</button>']
    for brand in BRAND_ORDER:
        brand_chips.append(
            f'                <button type="button" data-av-brand="{brand}" aria-pressed="false">{BRAND_META[brand]["label"]}</button>'
        )
    brand_bar = (
        f'            <div class="av-filters" data-av-brand-filters role="group" aria-label="{ui["brand_aria"]}">\n'
        + "\n".join(brand_chips)
        + "\n            </div>\n"
    )
    if "data-av-brand-filters" not in html:
        html = html.replace('<div class="product-grid">', brand_bar + '            <div class="product-grid">', 1)
    if "data-av-filters" not in html:
        html = html.replace('<div class="product-grid">', bar + '            <div class="product-grid">', 1)
    if "antivirus-filter.js" not in html:
        html = html.replace(
            "</body>",
            '    <script src="../js/antivirus-filter.js" defer></script>\n</body>',
            1,
        )
    path.write_text(html, encoding="utf-8", newline="\n")
    print("antivirus", lang)


def sku_from_html(html: str) -> str | None:
    m = re.search(r'data-stripe-product-sku="([^"]+)"', html)
    return m.group(1) if m else None


def patch_pdp(path: Path, lang: str) -> bool:
    html = path.read_text(encoding="utf-8")
    sku = sku_from_html(html)
    if not sku:
        return False
    orig = html
    if sku in VARIANT_OF and "pdp-plans" not in html:
        switcher = _render_plan_switcher(sku, lang, {})
        html = html.replace(
            '<p class="pdp-buy__label"',
            switcher + '                <p class="pdp-buy__label"',
            1,
        )
    if sku in KASPERSKY_SKUS and "pdp-meta-row--partner" not in html:
        chip = _render_kaspersky_partner(sku, lang)
        if 'class="pdp-meta-row"' in html:
            html = re.sub(
                r'(<p class="pdp-meta-row"[^>]*>[\s\S]*?</p>)',
                rf"\1\n{chip}",
                html,
                count=1,
            )
        else:
            html = html.replace(
                '<button type="button" id="product-primary-cta"',
                chip + '                <button type="button" id="product-primary-cta"',
                1,
            )
    cross = _render_cross_sell(sku, lang)
    if cross and "pdp-cross" not in html:
        html = html.replace(
            '<button type="button" id="product-primary-cta"',
            cross + '                <button type="button" id="product-primary-cta"',
            1,
        )
    if html == orig:
        return False
    path.write_text(html, encoding="utf-8", newline="\n")
    return True


def patch_all_pdps() -> int:
    n = 0
    for lang in LANGS:
        for path in sorted((ROOT / lang).glob("*.html")):
            if patch_pdp(path, lang):
                n += 1
    return n


def main() -> None:
    rhf.validate_merchandising()
    reorder_chrome_source()
    n = reorder_all_chrome_html()
    print("chrome html", n)
    for lang in LANGS:
        patch_home(lang)
        patch_antivirus(lang)
    print("pdp patched", patch_all_pdps())


if __name__ == "__main__":
    if "--home-plans" in sys.argv:
        rhf.validate_merchandising()
        for lang in LANGS:
            patch_home(lang)
    else:
        main()
