#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-shot: crea il prodotto ESET HOME Security Premium (licenza 1 anno) nelle
varianti 1 e 3 dispositivi, in tutte e 7 le lingue.

La pipeline di rigenerazione PDP e' ritirata (vedi scripts/page_pipeline_guard.py):
le pagine si costruiscono clonando una scheda pubblicata e ritoccandola. Qui la
sorgente e' mcafee-total-protection-3-devices.html (7 lingue) — la PDP "ricca"
piu' recente (buy-card v4, sticky CTA, FAQ concrete). Il chrome e le sezioni
generiche (trustbar, recensioni, passi 1-2) restano quelli del clone, gia'
localizzati; vengono riscritte solo le regioni specifiche del prodotto.

Prezzi (centesimi):
  1 disp.  vendita 2899  listino 7998  (barrato = listino ESET reale 79,98 EUR)
  3 disp.  vendita 3495  listino 8999  (barrato = listino ESET reale 89,99 EUR)

EAN (solo catalog.json -> feed Google Shopping; MAI nel JSON-LD, vedi il guard
"unverified gtin must not be published" in scripts/validate-product-pages.py):
  1 disp.  4022863006551   (SKU ESET EHSP-N1A1-VAKT-E)
  3 disp.  4022863006568   (SKU ESET EHSP-N1A3-VAKT-E)

Il gestore password NON compare nella copy: ESET lo ha ritirato (fine vendita
2025-10-21). L'immagine box lo cita ancora — scelta dell'utente di lasciarla.

Cosa fa (--apply per scrivere):
  1. catalog.json + functions/api/_lib/catalog.js: 2 nuove voci.
  2. 14 PDP  <lang>/eset-home-security-premium-{1-device,3-devices}.html
  3. Selettore .pdp-plans a 2 chip su entrambe le schede.
  4. Card prodotto (x2) nella pagina categoria antivirus.html (7 lingue),
     inserite dopo l'ultima card ESET NOD32.

Dopo, a mano (vedi GO-LIVE.md): build-google-shopping-feed.py,
build-cross-sell-index.py, build-search-index.py, rebuild-sitemap.py,
bump-asset-version.py, validate-product-pages.py.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es", "pt", "nl")
SRC_SLUG = "mcafee-total-protection-3-devices"
OLD_SKU = "MTP-3D-1Y"

VARIANTS = {
    1: dict(slug="eset-home-security-premium-1-device", sku="EHSP-N1A1-VAKT-E",
            ean="4022863006551", sale=2899, comp=7998),
    3: dict(slug="eset-home-security-premium-3-devices", sku="EHSP-N1A3-VAKT-E",
            ean="4022863006568", sale=3495, comp=8999),
}
SLUGS = {n: v["slug"] for n, v in VARIANTS.items()}

DEV = {
    "it": ("dispositivo", "dispositivi"), "en": ("device", "devices"),
    "es": ("dispositivo", "dispositivos"), "fr": ("appareil", "appareils"),
    "de": ("Gerät", "Geräte"), "nl": ("apparaat", "apparaten"),
    "pt": ("dispositivo", "dispositivos"),
}
YEAR1 = {"it": "1 anno", "en": "1 year", "es": "1 año", "fr": "1 an",
         "de": "1 Jahr", "nl": "1 jaar", "pt": "1 ano"}
CODE_LABEL = {"it": "Codice articolo:", "en": "Product code:", "es": "Código de producto:",
              "fr": "Référence produit:", "de": "Artikelnummer:", "nl": "Artikelcode:",
              "pt": "Código do produto:"}
# separatore versione nel titolo pagina (McAfee usa "·" per tutte)
BRAND_LINE = {  # <span class="pdp-badge"> — "ESET · <1 anno> · <n disp>"
    lang: f"ESET · {YEAR1[lang]} · {{nd}}" for lang in LANGS
}


def euro(minor):
    return f"{minor // 100},{minor % 100:02d}"


def dot(minor):
    return f"{minor // 100}.{minor % 100:02d}"


def disc(sale, comp):
    return round((1 - sale / comp) * 100)


def nd(lang, n):
    return f"{n} {DEV[lang][0 if n == 1 else 1]}"


def nd_title(n):
    return f"{n} " + ("Dispositivo" if n == 1 else "Dispositivi")


# ---------------------------------------------------------------------------
# COPY per lingua. Le stringhe con {nd} vengono formattate per variante.
# ---------------------------------------------------------------------------
C = {
"it": {
 "title": "ESET HOME Security Premium · {nd} · Licenza 1 anno — Eurolicenze",
 "desc": "ESET HOME Security Premium per {nd}: licenza originale di 1 anno con antivirus multilivello, VPN illimitata e crittografia dei dati. Consegna via email in pochi minuti.",
 "name": "ESET HOME Security Premium — {nd} · 1 anno",
 "h1": 'ESET <span>HOME Security Premium · {nd}</span>',
 "hero": "Con ESET HOME Security Premium proteggi {nd} per 12 mesi: antivirus multilivello contro ransomware e phishing, firewall e controllo della rete, Safe Banking, più VPN illimitata e crittografia dei file sensibili. Licenza digitale originale, consegna via email in pochi minuti e attivazione sul portale ufficiale ESET HOME.",
 "keylist": [
   "Antivirus multilivello in tempo reale per {nd}, con aggiornamenti automatici",
   "Difesa da ransomware, spyware, trojan e tentativi di phishing",
   "VPN con traffico illimitato{vpncap} e crittografia di file e foto sensibili",
   "Firewall, controllo della rete Wi-Fi e Safe Banking per pagamenti protetti",
   "Windows, macOS, Android e iOS · gestione dal portale ufficiale ESET HOME",
 ],
 "vpncap3": " (fino a 3 dispositivi)",
 "feat_title": "Perché scegliere ESET HOME Security Premium",
 "feat_sub": "ESET HOME Security Premium è la suite completa di ESET: unisce antivirus multilivello, VPN illimitata, crittografia dei dati e protezione della navigazione in un'unica licenza. Questa edizione copre {nd} per 12 mesi e si gestisce dal portale ufficiale ESET HOME, dove controlli account, rinnovo e dispositivi protetti.",
 "cards": [
   ("Protezione multilivello", "Difesa proattiva da virus, ransomware, spyware e phishing, con firewall, controllo della rete Wi-Fi e rilevamento avanzato basato su cloud e machine learning."),
   ("VPN illimitata e privacy", "Naviga con indirizzo IP mascherato e traffico VPN senza limiti su server in decine di Paesi, con protezione della webcam e del browser."),
   ("Crittografia dei dati sensibili", "Proteggi file e foto riservati con crittografia avanzata, anche su unità rimovibili: restano illeggibili in caso di furto o smarrimento del dispositivo."),
   ("Portale ufficiale ESET HOME", "Attivazione autentica e gestione centralizzata dei dispositivi dall'account ufficiale ESET HOME, con aggiornamenti continui inclusi."),
 ],
 "specs_caption": "Requisiti di sistema per ESET HOME Security Premium",
 "specs_head": ("Requisito", "Dettaglio Tecnico"),
 "specs_rows": [
   ("Sistema operativo", "Windows 11 / 10 (64-bit), macOS 12 / 13 / 14, Android 8.0+, iOS 15+"),
   ("Processore", "1 GHz (x64 o ARM64)"),
   ("Memoria RAM", "1 GB minimo"),
   ("Spazio su disco", "1 GB di spazio libero"),
 ],
 "steps": [
   ("Completa l'ordine", "Scegli la versione e procedi con il pagamento sicuro tramite carta o PayPal."),
   ("Ricevi la licenza via email", "Ti inviamo il codice licenza originale e la guida di installazione via email in 2–15 minuti."),
   ("Attiva sul portale ufficiale", "Attiva sul <strong>portale ufficiale ESET (ESET HOME)</strong> con il codice ricevuto e installa il software ufficiale in tutta sicurezza."),
 ],
 "faq": [
   ("Cosa include ESET HOME Security Premium?", "Antivirus multilivello in tempo reale, difesa da ransomware e phishing, firewall e controllo della rete Wi-Fi, Safe Banking, VPN con traffico illimitato e crittografia dei file e delle foto sensibili (Secure Data). Le funzioni attive restano visibili nel portale ESET HOME dopo l'attivazione."),
   ("Per quanti dispositivi è valida la licenza?", "@DEVICES@"),
   ("È un abbonamento con rinnovo automatico?", "È una licenza di 12 mesi. Il rinnovo automatico si gestisce dall'account ESET HOME e puoi disattivarlo quando vuoi: la protezione resta attiva fino alla fine del periodo già pagato."),
   ("Come si attiva il codice dopo l'acquisto?", "Dopo il pagamento ricevi via email la licenza originale e una guida rapida. Accedi a ESET HOME (home.eset.com) con il tuo account ESET, inserisci il codice e scarica l'installer ufficiale."),
   ("È compatibile con Windows 11 e macOS?", "Sì. ESET HOME Security Premium funziona su Windows 11 e 10 a 64 bit, macOS 12 o versioni successive, Android 8+ e iOS 15+. Su iOS le funzioni sono limitate a VPN e app ESET HOME."),
   ("La licenza è originale e ricevo fattura?", "Sì. Le licenze ESET sono originali e si attivano sui canali ufficiali del produttore. Emettiamo fattura per privati e aziende e offriamo assistenza via email e WhatsApp."),
 ],
 "faq_devices": {
   1: "Questa versione protegge 1 dispositivo per 12 mesi, su Windows, macOS o Android; su iOS sono disponibili VPN e app ESET HOME. Gestisci tutto dal portale ESET HOME.",
   3: "Questa versione protegge 3 dispositivi per 12 mesi. Distribuisci la protezione tra PC Windows, Mac e dispositivi Android o iOS gestendoli dallo stesso account ESET HOME.",
 },
 "card_blurb": "Abbonamento · licenza digitale",
},

"en": {
 "title": "ESET HOME Security Premium · {nd} · 1-year licence — Eurolicenze",
 "desc": "ESET HOME Security Premium for {nd}: genuine 1-year licence with multilayered antivirus, unlimited VPN and data encryption. Email delivery within minutes.",
 "name": "ESET HOME Security Premium — {nd} · 1 year",
 "h1": 'ESET <span>HOME Security Premium · {nd}</span>',
 "hero": "With ESET HOME Security Premium you protect {nd} for 12 months: multilayered antivirus against ransomware and phishing, firewall and network inspection, safe banking, plus unlimited VPN and encryption of sensitive files. Genuine digital licence, email delivery within minutes and activation on the official ESET HOME portal.",
 "keylist": [
   "Real-time multilayered antivirus for {nd}, with automatic updates",
   "Defence against ransomware, spyware, trojans and phishing attempts",
   "Unlimited-traffic VPN{vpncap} and encryption of sensitive files and photos",
   "Firewall, Wi-Fi network inspection and safe banking for protected payments",
   "Windows, macOS, Android and iOS · managed from the official ESET HOME portal",
 ],
 "vpncap3": " (up to 3 devices)",
 "feat_title": "Why choose ESET HOME Security Premium",
 "feat_sub": "ESET HOME Security Premium is ESET's complete suite: it combines multilayered antivirus, unlimited VPN, data encryption and browsing protection in a single licence. This edition covers {nd} for 12 months and is managed from the official ESET HOME portal, where you handle your account, renewal and protected devices.",
 "cards": [
   ("Multilayered protection", "Proactive defence against viruses, ransomware, spyware and phishing, with a firewall, Wi-Fi network inspection and advanced cloud- and machine-learning-based detection."),
   ("Unlimited VPN and privacy", "Browse with a masked IP address and unlimited VPN traffic across servers in dozens of countries, with webcam and browser protection."),
   ("Encryption of sensitive data", "Protect confidential files and photos with strong encryption, including on removable drives: they stay unreadable if the device is lost or stolen."),
   ("Official ESET HOME portal", "Genuine activation and centralised device management from your official ESET HOME account, with continuous updates included."),
 ],
 "specs_caption": "System requirements for ESET HOME Security Premium",
 "specs_head": ("Requirement", "Technical detail"),
 "specs_rows": [
   ("Operating system", "Windows 11 / 10 (64-bit), macOS 12 / 13 / 14, Android 8.0+, iOS 15+"),
   ("Processor", "1 GHz (x64 or ARM64)"),
   ("RAM", "1 GB minimum"),
   ("Disk space", "1 GB of free space"),
 ],
 "steps": [
   ("Complete your order", "Choose the edition and pay securely by card or PayPal."),
   ("Receive the licence by email", "We send your genuine licence key and the installation guide by email within 2–15 minutes."),
   ("Activate on the official portal", "Activate on the <strong>official ESET portal (ESET HOME)</strong> with the key you receive and install the official software safely."),
 ],
 "faq": [
   ("What does ESET HOME Security Premium include?", "Real-time multilayered antivirus, defence against ransomware and phishing, a firewall and Wi-Fi network inspection, safe banking, an unlimited-traffic VPN and encryption of sensitive files and photos (Secure Data). The active features remain visible in the ESET HOME portal after activation."),
   ("How many devices does the licence cover?", "@DEVICES@"),
   ("Is it a subscription with automatic renewal?", "It is a 12-month licence. Automatic renewal is managed from your ESET HOME account and can be turned off at any time: protection stays active until the end of the period already paid for."),
   ("How do I activate the code after purchase?", "After payment you receive the genuine licence and a quick guide by email. Sign in to ESET HOME (home.eset.com) with your ESET account, enter the code and download the official installer."),
   ("Is it compatible with Windows 11 and macOS?", "Yes. ESET HOME Security Premium runs on Windows 11 and 10 (64-bit), macOS 12 or later, Android 8+ and iOS 15+. On iOS the features are limited to VPN and the ESET HOME app."),
   ("Is the licence genuine and do I get an invoice?", "Yes. ESET licences are genuine and activate through the manufacturer's official channels. We issue invoices for individuals and businesses and offer support by email and WhatsApp."),
 ],
 "faq_devices": {
   1: "This version protects 1 device for 12 months, on Windows, macOS or Android; on iOS the VPN and ESET HOME app are available. Manage everything from the ESET HOME portal.",
   3: "This version protects 3 devices for 12 months. Split the protection across Windows PCs, Macs and Android or iOS devices, all managed from the same ESET HOME account.",
 },
 "card_blurb": "Subscription · digital licence",
},

"fr": {
 "title": "ESET HOME Security Premium · {nd} · Licence 1 an — Eurolicenze",
 "desc": "ESET HOME Security Premium pour {nd} : licence authentique 1 an avec antivirus multicouche, VPN illimité et chiffrement des données. Livraison par e-mail en quelques minutes.",
 "name": "ESET HOME Security Premium — {nd} · 1 an",
 "h1": 'ESET <span>HOME Security Premium · {nd}</span>',
 "hero": "Avec ESET HOME Security Premium, vous protégez {nd} pendant 12 mois : antivirus multicouche contre les rançongiciels et le phishing, pare-feu et inspection réseau, navigation bancaire sécurisée, plus un VPN illimité et le chiffrement des fichiers sensibles. Licence numérique authentique, livraison par e-mail en quelques minutes et activation sur le portail officiel ESET HOME.",
 "keylist": [
   "Antivirus multicouche en temps réel pour {nd}, avec mises à jour automatiques",
   "Défense contre les rançongiciels, logiciels espions, chevaux de Troie et tentatives de phishing",
   "VPN à trafic illimité{vpncap} et chiffrement des fichiers et photos sensibles",
   "Pare-feu, inspection du réseau Wi-Fi et navigation bancaire sécurisée pour des paiements protégés",
   "Windows, macOS, Android et iOS · gestion depuis le portail officiel ESET HOME",
 ],
 "vpncap3": " (jusqu'à 3 appareils)",
 "feat_title": "Pourquoi choisir ESET HOME Security Premium",
 "feat_sub": "ESET HOME Security Premium est la suite complète d'ESET : elle réunit antivirus multicouche, VPN illimité, chiffrement des données et protection de la navigation dans une seule licence. Cette édition couvre {nd} pendant 12 mois et se gère depuis le portail officiel ESET HOME, où vous gérez compte, renouvellement et appareils protégés.",
 "cards": [
   ("Protection multicouche", "Défense proactive contre les virus, rançongiciels, logiciels espions et le phishing, avec pare-feu, inspection du réseau Wi-Fi et détection avancée basée sur le cloud et le machine learning."),
   ("VPN illimité et confidentialité", "Naviguez avec une adresse IP masquée et un trafic VPN sans limite sur des serveurs dans des dizaines de pays, avec protection de la webcam et du navigateur."),
   ("Chiffrement des données sensibles", "Protégez fichiers et photos confidentiels par un chiffrement fort, y compris sur supports amovibles : ils restent illisibles en cas de perte ou de vol de l'appareil."),
   ("Portail officiel ESET HOME", "Activation authentique et gestion centralisée des appareils depuis votre compte officiel ESET HOME, avec mises à jour continues incluses."),
 ],
 "specs_caption": "Configuration requise pour ESET HOME Security Premium",
 "specs_head": ("Élément", "Détail technique"),
 "specs_rows": [
   ("Système d'exploitation", "Windows 11 / 10 (64 bits), macOS 12 / 13 / 14, Android 8.0+, iOS 15+"),
   ("Processeur", "1 GHz (x64 ou ARM64)"),
   ("Mémoire RAM", "1 Go minimum"),
   ("Espace disque", "1 Go d'espace libre"),
 ],
 "steps": [
   ("Finalisez la commande", "Choisissez la version et payez en toute sécurité par carte ou PayPal."),
   ("Recevez la licence par e-mail", "Nous envoyons votre clé de licence authentique et le guide d'installation par e-mail en 2 à 15 minutes."),
   ("Activez sur le portail officiel", "Activez sur le <strong>portail officiel ESET (ESET HOME)</strong> avec la clé reçue et installez le logiciel officiel en toute sécurité."),
 ],
 "faq": [
   ("Que contient ESET HOME Security Premium ?", "Antivirus multicouche en temps réel, défense contre les rançongiciels et le phishing, pare-feu et inspection du réseau Wi-Fi, navigation bancaire sécurisée, VPN à trafic illimité et chiffrement des fichiers et photos sensibles (Secure Data). Les fonctions actives restent visibles dans le portail ESET HOME après l'activation."),
   ("Pour combien d'appareils la licence est-elle valable ?", "@DEVICES@"),
   ("Est-ce un abonnement avec renouvellement automatique ?", "C'est une licence de 12 mois. Le renouvellement automatique se gère depuis votre compte ESET HOME et peut être désactivé à tout moment : la protection reste active jusqu'à la fin de la période déjà payée."),
   ("Comment activer le code après l'achat ?", "Après le paiement, vous recevez la licence authentique et un guide rapide par e-mail. Connectez-vous à ESET HOME (home.eset.com) avec votre compte ESET, saisissez le code et téléchargez l'installateur officiel."),
   ("Est-ce compatible avec Windows 11 et macOS ?", "Oui. ESET HOME Security Premium fonctionne sous Windows 11 et 10 (64 bits), macOS 12 ou version ultérieure, Android 8+ et iOS 15+. Sous iOS, les fonctions se limitent au VPN et à l'application ESET HOME."),
   ("La licence est-elle authentique et ai-je une facture ?", "Oui. Les licences ESET sont authentiques et s'activent via les canaux officiels du fabricant. Nous émettons des factures pour les particuliers et les entreprises et proposons une assistance par e-mail et WhatsApp."),
 ],
 "faq_devices": {
   1: "Cette version protège 1 appareil pendant 12 mois, sous Windows, macOS ou Android ; sous iOS, le VPN et l'application ESET HOME sont disponibles. Gérez le tout depuis le portail ESET HOME.",
   3: "Cette version protège 3 appareils pendant 12 mois. Répartissez la protection entre PC Windows, Mac et appareils Android ou iOS, tous gérés depuis le même compte ESET HOME.",
 },
 "card_blurb": "Abonnement · licence numérique",
},

"de": {
 "title": "ESET HOME Security Premium · {nd} · Lizenz 1 Jahr — Eurolicenze",
 "desc": "ESET HOME Security Premium für {nd}: Original-Lizenz für 1 Jahr mit mehrschichtigem Antivirus, unbegrenztem VPN und Datenverschlüsselung. E-Mail-Zustellung in wenigen Minuten.",
 "name": "ESET HOME Security Premium — {nd} · 1 Jahr",
 "h1": 'ESET <span>HOME Security Premium · {nd}</span>',
 "hero": "Mit ESET HOME Security Premium schützen Sie {nd} für 12 Monate: mehrschichtiger Antivirus gegen Ransomware und Phishing, Firewall und Netzwerkprüfung, sicheres Online-Banking, dazu unbegrenztes VPN und Verschlüsselung sensibler Dateien. Digitale Original-Lizenz, E-Mail-Zustellung in wenigen Minuten und Aktivierung im offiziellen ESET-HOME-Portal.",
 "keylist": [
   "Mehrschichtiger Echtzeit-Antivirus für {nd}, mit automatischen Updates",
   "Schutz vor Ransomware, Spyware, Trojanern und Phishing-Versuchen",
   "VPN mit unbegrenztem Datenvolumen{vpncap} und Verschlüsselung sensibler Dateien und Fotos",
   "Firewall, WLAN-Netzwerkprüfung und sicheres Banking für geschützte Zahlungen",
   "Windows, macOS, Android und iOS · Verwaltung über das offizielle ESET-HOME-Portal",
 ],
 "vpncap3": " (bis zu 3 Geräte)",
 "feat_title": "Warum ESET HOME Security Premium wählen",
 "feat_sub": "ESET HOME Security Premium ist die komplette Suite von ESET: Sie vereint mehrschichtigen Antivirus, unbegrenztes VPN, Datenverschlüsselung und Surfschutz in einer einzigen Lizenz. Diese Edition deckt {nd} für 12 Monate ab und wird über das offizielle ESET-HOME-Portal verwaltet, wo Sie Konto, Verlängerung und geschützte Geräte steuern.",
 "cards": [
   ("Mehrschichtiger Schutz", "Proaktive Abwehr von Viren, Ransomware, Spyware und Phishing, mit Firewall, WLAN-Netzwerkprüfung und fortschrittlicher Erkennung auf Basis von Cloud und maschinellem Lernen."),
   ("Unbegrenztes VPN und Privatsphäre", "Surfen Sie mit maskierter IP-Adresse und unbegrenztem VPN-Datenvolumen über Server in Dutzenden Ländern, mit Webcam- und Browser-Schutz."),
   ("Verschlüsselung sensibler Daten", "Schützen Sie vertrauliche Dateien und Fotos mit starker Verschlüsselung, auch auf Wechseldatenträgern: Bei Verlust oder Diebstahl des Geräts bleiben sie unlesbar."),
   ("Offizielles ESET-HOME-Portal", "Echte Aktivierung und zentrale Geräteverwaltung über Ihr offizielles ESET-HOME-Konto, mit kontinuierlichen Updates."),
 ],
 "specs_caption": "Systemanforderungen für ESET HOME Security Premium",
 "specs_head": ("Anforderung", "Technische Details"),
 "specs_rows": [
   ("Betriebssystem", "Windows 11 / 10 (64-Bit), macOS 12 / 13 / 14, Android 8.0+, iOS 15+"),
   ("Prozessor", "1 GHz (x64 oder ARM64)"),
   ("Arbeitsspeicher", "1 GB mindestens"),
   ("Festplattenspeicher", "1 GB freier Speicher"),
 ],
 "steps": [
   ("Bestellung abschließen", "Wählen Sie die Version und zahlen Sie sicher per Karte oder PayPal."),
   ("Lizenz per E-Mail erhalten", "Wir senden Ihren originalen Lizenzschlüssel und die Installationsanleitung innerhalb von 2–15 Minuten per E-Mail."),
   ("Im offiziellen Portal aktivieren", "Aktivieren Sie im <strong>offiziellen ESET-Portal (ESET HOME)</strong> mit dem erhaltenen Schlüssel und installieren Sie die offizielle Software sicher."),
 ],
 "faq": [
   ("Was ist in ESET HOME Security Premium enthalten?", "Mehrschichtiger Echtzeit-Antivirus, Schutz vor Ransomware und Phishing, Firewall und WLAN-Netzwerkprüfung, sicheres Banking, ein VPN mit unbegrenztem Datenvolumen und Verschlüsselung sensibler Dateien und Fotos (Secure Data). Die aktiven Funktionen bleiben nach der Aktivierung im ESET-HOME-Portal sichtbar."),
   ("Für wie viele Geräte gilt die Lizenz?", "@DEVICES@"),
   ("Ist es ein Abo mit automatischer Verlängerung?", "Es ist eine Lizenz für 12 Monate. Die automatische Verlängerung wird über Ihr ESET-HOME-Konto verwaltet und kann jederzeit deaktiviert werden: Der Schutz bleibt bis zum Ende des bereits bezahlten Zeitraums aktiv."),
   ("Wie aktiviere ich den Code nach dem Kauf?", "Nach der Zahlung erhalten Sie die Original-Lizenz und eine Kurzanleitung per E-Mail. Melden Sie sich bei ESET HOME (home.eset.com) mit Ihrem ESET-Konto an, geben Sie den Code ein und laden Sie das offizielle Installationsprogramm herunter."),
   ("Ist es mit Windows 11 und macOS kompatibel?", "Ja. ESET HOME Security Premium läuft unter Windows 11 und 10 (64 Bit), macOS 12 oder neuer, Android 8+ und iOS 15+. Unter iOS beschränken sich die Funktionen auf VPN und die ESET-HOME-App."),
   ("Ist die Lizenz original und erhalte ich eine Rechnung?", "Ja. Die ESET-Lizenzen sind original und werden über die offiziellen Kanäle des Herstellers aktiviert. Wir stellen Rechnungen für Privatpersonen und Unternehmen aus und bieten Support per E-Mail und WhatsApp."),
 ],
 "faq_devices": {
   1: "Diese Version schützt 1 Gerät für 12 Monate, unter Windows, macOS oder Android; unter iOS stehen VPN und die ESET-HOME-App bereit. Alles wird über das ESET-HOME-Portal verwaltet.",
   3: "Diese Version schützt 3 Geräte für 12 Monate. Verteilen Sie den Schutz auf Windows-PCs, Macs sowie Android- oder iOS-Geräte, alle über dasselbe ESET-HOME-Konto verwaltet.",
 },
 "card_blurb": "Abo · digitale Lizenz",
},

"es": {
 "title": "ESET HOME Security Premium · {nd} · Licencia 1 año — Eurolicenze",
 "desc": "ESET HOME Security Premium para {nd}: licencia original de 1 año con antivirus multicapa, VPN ilimitada y cifrado de datos. Entrega por email en pocos minutos.",
 "name": "ESET HOME Security Premium — {nd} · 1 año",
 "h1": 'ESET <span>HOME Security Premium · {nd}</span>',
 "hero": "Con ESET HOME Security Premium proteges {nd} durante 12 meses: antivirus multicapa contra ransomware y phishing, firewall e inspección de red, banca en línea segura, además de VPN ilimitada y cifrado de archivos sensibles. Licencia digital original, entrega por email en pocos minutos y activación en el portal oficial ESET HOME.",
 "keylist": [
   "Antivirus multicapa en tiempo real para {nd}, con actualizaciones automáticas",
   "Defensa frente a ransomware, spyware, troyanos e intentos de phishing",
   "VPN de tráfico ilimitado{vpncap} y cifrado de archivos y fotos sensibles",
   "Firewall, inspección de red Wi-Fi y banca segura para pagos protegidos",
   "Windows, macOS, Android e iOS · gestión desde el portal oficial ESET HOME",
 ],
 "vpncap3": " (hasta 3 dispositivos)",
 "feat_title": "Por qué elegir ESET HOME Security Premium",
 "feat_sub": "ESET HOME Security Premium es la suite completa de ESET: combina antivirus multicapa, VPN ilimitada, cifrado de datos y protección de la navegación en una sola licencia. Esta edición cubre {nd} durante 12 meses y se gestiona desde el portal oficial ESET HOME, donde controlas cuenta, renovación y dispositivos protegidos.",
 "cards": [
   ("Protección multicapa", "Defensa proactiva frente a virus, ransomware, spyware y phishing, con firewall, inspección de red Wi-Fi y detección avanzada basada en la nube y el aprendizaje automático."),
   ("VPN ilimitada y privacidad", "Navega con dirección IP enmascarada y tráfico VPN sin límite en servidores de decenas de países, con protección de la webcam y del navegador."),
   ("Cifrado de datos sensibles", "Protege archivos y fotos confidenciales con cifrado fuerte, también en unidades extraíbles: permanecen ilegibles si el dispositivo se pierde o lo roban."),
   ("Portal oficial ESET HOME", "Activación auténtica y gestión centralizada de los dispositivos desde tu cuenta oficial ESET HOME, con actualizaciones continuas incluidas."),
 ],
 "specs_caption": "Requisitos del sistema para ESET HOME Security Premium",
 "specs_head": ("Requisito", "Detalle técnico"),
 "specs_rows": [
   ("Sistema operativo", "Windows 11 / 10 (64 bits), macOS 12 / 13 / 14, Android 8.0+, iOS 15+"),
   ("Procesador", "1 GHz (x64 o ARM64)"),
   ("Memoria RAM", "1 GB mínimo"),
   ("Espacio en disco", "1 GB de espacio libre"),
 ],
 "steps": [
   ("Completa el pedido", "Elige la versión y paga de forma segura con tarjeta o PayPal."),
   ("Recibe la licencia por email", "Te enviamos la clave de licencia original y la guía de instalación por email en 2–15 minutos."),
   ("Activa en el portal oficial", "Activa en el <strong>portal oficial de ESET (ESET HOME)</strong> con la clave recibida e instala el software oficial con total seguridad."),
 ],
 "faq": [
   ("¿Qué incluye ESET HOME Security Premium?", "Antivirus multicapa en tiempo real, defensa frente a ransomware y phishing, firewall e inspección de red Wi-Fi, banca segura, una VPN de tráfico ilimitado y cifrado de archivos y fotos sensibles (Secure Data). Las funciones activas siguen visibles en el portal ESET HOME tras la activación."),
   ("¿Para cuántos dispositivos es válida la licencia?", "@DEVICES@"),
   ("¿Es una suscripción con renovación automática?", "Es una licencia de 12 meses. La renovación automática se gestiona desde tu cuenta ESET HOME y puedes desactivarla cuando quieras: la protección sigue activa hasta el final del periodo ya pagado."),
   ("¿Cómo se activa el código tras la compra?", "Tras el pago recibes la licencia original y una guía rápida por email. Inicia sesión en ESET HOME (home.eset.com) con tu cuenta ESET, introduce el código y descarga el instalador oficial."),
   ("¿Es compatible con Windows 11 y macOS?", "Sí. ESET HOME Security Premium funciona en Windows 11 y 10 (64 bits), macOS 12 o posterior, Android 8+ e iOS 15+. En iOS las funciones se limitan a la VPN y la app ESET HOME."),
   ("¿La licencia es original y recibo factura?", "Sí. Las licencias ESET son originales y se activan por los canales oficiales del fabricante. Emitimos factura para particulares y empresas y ofrecemos asistencia por email y WhatsApp."),
 ],
 "faq_devices": {
   1: "Esta versión protege 1 dispositivo durante 12 meses, en Windows, macOS o Android; en iOS están disponibles la VPN y la app ESET HOME. Gestiona todo desde el portal ESET HOME.",
   3: "Esta versión protege 3 dispositivos durante 12 meses. Reparte la protección entre PC con Windows, Mac y dispositivos Android o iOS, todos gestionados desde la misma cuenta ESET HOME.",
 },
 "card_blurb": "Suscripción · licencia digital",
},

"pt": {
 "title": "ESET HOME Security Premium · {nd} · Licença 1 ano — Eurolicenze",
 "desc": "ESET HOME Security Premium para {nd}: licença original de 1 ano com antivírus multicamada, VPN ilimitada e encriptação de dados. Entrega por email em poucos minutos.",
 "name": "ESET HOME Security Premium — {nd} · 1 ano",
 "h1": 'ESET <span>HOME Security Premium · {nd}</span>',
 "hero": "Com o ESET HOME Security Premium protege {nd} durante 12 meses: antivírus multicamada contra ransomware e phishing, firewall e inspeção de rede, banca online segura, além de VPN ilimitada e encriptação de ficheiros sensíveis. Licença digital original, entrega por email em poucos minutos e ativação no portal oficial ESET HOME.",
 "keylist": [
   "Antivírus multicamada em tempo real para {nd}, com atualizações automáticas",
   "Defesa contra ransomware, spyware, trojans e tentativas de phishing",
   "VPN de tráfego ilimitado{vpncap} e encriptação de ficheiros e fotos sensíveis",
   "Firewall, inspeção da rede Wi-Fi e banca segura para pagamentos protegidos",
   "Windows, macOS, Android e iOS · gestão a partir do portal oficial ESET HOME",
 ],
 "vpncap3": " (até 3 dispositivos)",
 "feat_title": "Porque escolher o ESET HOME Security Premium",
 "feat_sub": "O ESET HOME Security Premium é a suite completa da ESET: reúne antivírus multicamada, VPN ilimitada, encriptação de dados e proteção da navegação numa única licença. Esta edição cobre {nd} durante 12 meses e é gerida a partir do portal oficial ESET HOME, onde controla conta, renovação e dispositivos protegidos.",
 "cards": [
   ("Proteção multicamada", "Defesa proativa contra vírus, ransomware, spyware e phishing, com firewall, inspeção da rede Wi-Fi e deteção avançada baseada na cloud e em machine learning."),
   ("VPN ilimitada e privacidade", "Navegue com endereço IP mascarado e tráfego VPN sem limite em servidores de dezenas de países, com proteção da webcam e do navegador."),
   ("Encriptação de dados sensíveis", "Proteja ficheiros e fotos confidenciais com encriptação forte, também em unidades removíveis: ficam ilegíveis em caso de perda ou roubo do dispositivo."),
   ("Portal oficial ESET HOME", "Ativação autêntica e gestão centralizada dos dispositivos a partir da sua conta oficial ESET HOME, com atualizações contínuas incluídas."),
 ],
 "specs_caption": "Requisitos do sistema para ESET HOME Security Premium",
 "specs_head": ("Requisito", "Detalhe técnico"),
 "specs_rows": [
   ("Sistema operativo", "Windows 11 / 10 (64 bits), macOS 12 / 13 / 14, Android 8.0+, iOS 15+"),
   ("Processador", "1 GHz (x64 ou ARM64)"),
   ("Memória RAM", "1 GB mínimo"),
   ("Espaço em disco", "1 GB de espaço livre"),
 ],
 "steps": [
   ("Conclua a encomenda", "Escolha a versão e pague em segurança com cartão ou PayPal."),
   ("Receba a licença por email", "Enviamos a chave de licença original e o guia de instalação por email em 2–15 minutos."),
   ("Ative no portal oficial", "Ative no <strong>portal oficial da ESET (ESET HOME)</strong> com a chave recebida e instale o software oficial com total segurança."),
 ],
 "faq": [
   ("O que inclui o ESET HOME Security Premium?", "Antivírus multicamada em tempo real, defesa contra ransomware e phishing, firewall e inspeção da rede Wi-Fi, banca segura, uma VPN de tráfego ilimitado e encriptação de ficheiros e fotos sensíveis (Secure Data). As funções ativas continuam visíveis no portal ESET HOME após a ativação."),
   ("Para quantos dispositivos é válida a licença?", "@DEVICES@"),
   ("É uma subscrição com renovação automática?", "É uma licença de 12 meses. A renovação automática é gerida a partir da conta ESET HOME e pode ser desativada quando quiser: a proteção continua ativa até ao fim do período já pago."),
   ("Como se ativa o código depois da compra?", "Após o pagamento recebe a licença original e um guia rápido por email. Inicie sessão no ESET HOME (home.eset.com) com a sua conta ESET, introduza o código e transfira o instalador oficial."),
   ("É compatível com o Windows 11 e o macOS?", "Sim. O ESET HOME Security Premium funciona no Windows 11 e 10 (64 bits), macOS 12 ou posterior, Android 8+ e iOS 15+. No iOS as funções limitam-se à VPN e à app ESET HOME."),
   ("A licença é original e recebo fatura?", "Sim. As licenças ESET são originais e ativam-se pelos canais oficiais do fabricante. Emitimos fatura para particulares e empresas e oferecemos apoio por email e WhatsApp."),
 ],
 "faq_devices": {
   1: "Esta versão protege 1 dispositivo durante 12 meses, em Windows, macOS ou Android; no iOS estão disponíveis a VPN e a app ESET HOME. Faça a gestão a partir do portal ESET HOME.",
   3: "Esta versão protege 3 dispositivos durante 12 meses. Distribua a proteção por PCs Windows, Macs e dispositivos Android ou iOS, todos geridos a partir da mesma conta ESET HOME.",
 },
 "card_blurb": "Subscrição · licença digital",
},

"nl": {
 "title": "ESET HOME Security Premium · {nd} · Licentie 1 jaar — Eurolicenze",
 "desc": "ESET HOME Security Premium voor {nd}: originele licentie van 1 jaar met meerlaagse antivirus, onbeperkte VPN en gegevensversleuteling. Levering per e-mail binnen enkele minuten.",
 "name": "ESET HOME Security Premium — {nd} · 1 jaar",
 "h1": 'ESET <span>HOME Security Premium · {nd}</span>',
 "hero": "Met ESET HOME Security Premium beschermt u {nd} 12 maanden lang: meerlaagse antivirus tegen ransomware en phishing, firewall en netwerkinspectie, veilig bankieren, plus onbeperkte VPN en versleuteling van gevoelige bestanden. Originele digitale licentie, levering per e-mail binnen enkele minuten en activering op het officiële ESET HOME-portaal.",
 "keylist": [
   "Meerlaagse antivirus in realtime voor {nd}, met automatische updates",
   "Bescherming tegen ransomware, spyware, trojans en phishingpogingen",
   "VPN met onbeperkt verkeer{vpncap} en versleuteling van gevoelige bestanden en foto's",
   "Firewall, wifi-netwerkinspectie en veilig bankieren voor beschermde betalingen",
   "Windows, macOS, Android en iOS · beheer via het officiële ESET HOME-portaal",
 ],
 "vpncap3": " (tot 3 apparaten)",
 "feat_title": "Waarom ESET HOME Security Premium kiezen",
 "feat_sub": "ESET HOME Security Premium is de complete suite van ESET: het combineert meerlaagse antivirus, onbeperkte VPN, gegevensversleuteling en surfbescherming in één licentie. Deze editie dekt {nd} 12 maanden lang en wordt beheerd via het officiële ESET HOME-portaal, waar u account, verlenging en beschermde apparaten regelt.",
 "cards": [
   ("Meerlaagse bescherming", "Proactieve verdediging tegen virussen, ransomware, spyware en phishing, met firewall, wifi-netwerkinspectie en geavanceerde detectie op basis van cloud en machine learning."),
   ("Onbeperkte VPN en privacy", "Surf met een gemaskeerd IP-adres en onbeperkt VPN-verkeer via servers in tientallen landen, met webcam- en browserbescherming."),
   ("Versleuteling van gevoelige gegevens", "Bescherm vertrouwelijke bestanden en foto's met sterke versleuteling, ook op verwisselbare schijven: ze blijven onleesbaar als het apparaat verloren of gestolen wordt."),
   ("Officieel ESET HOME-portaal", "Echte activering en centraal apparaatbeheer via uw officiële ESET HOME-account, met doorlopende updates inbegrepen."),
 ],
 "specs_caption": "Systeemvereisten voor ESET HOME Security Premium",
 "specs_head": ("Vereiste", "Technische details"),
 "specs_rows": [
   ("Besturingssysteem", "Windows 11 / 10 (64-bit), macOS 12 / 13 / 14, Android 8.0+, iOS 15+"),
   ("Processor", "1 GHz (x64 of ARM64)"),
   ("RAM-geheugen", "1 GB minimaal"),
   ("Schijfruimte", "1 GB vrije ruimte"),
 ],
 "steps": [
   ("Rond de bestelling af", "Kies de versie en betaal veilig met kaart of PayPal."),
   ("Ontvang de licentie per e-mail", "We sturen uw originele licentiesleutel en de installatiehandleiding per e-mail binnen 2–15 minuten."),
   ("Activeer op het officiële portaal", "Activeer op het <strong>officiële ESET-portaal (ESET HOME)</strong> met de ontvangen sleutel en installeer de officiële software veilig."),
 ],
 "faq": [
   ("Wat zit er in ESET HOME Security Premium?", "Meerlaagse antivirus in realtime, bescherming tegen ransomware en phishing, firewall en wifi-netwerkinspectie, veilig bankieren, een VPN met onbeperkt verkeer en versleuteling van gevoelige bestanden en foto's (Secure Data). De actieve functies blijven na activering zichtbaar in het ESET HOME-portaal."),
   ("Voor hoeveel apparaten geldt de licentie?", "@DEVICES@"),
   ("Is het een abonnement met automatische verlenging?", "Het is een licentie van 12 maanden. De automatische verlenging wordt beheerd via uw ESET HOME-account en kan op elk moment worden uitgeschakeld: de bescherming blijft actief tot het einde van de reeds betaalde periode."),
   ("Hoe activeer ik de code na aankoop?", "Na betaling ontvangt u de originele licentie en een korte handleiding per e-mail. Meld u aan bij ESET HOME (home.eset.com) met uw ESET-account, voer de code in en download het officiële installatieprogramma."),
   ("Is het compatibel met Windows 11 en macOS?", "Ja. ESET HOME Security Premium draait op Windows 11 en 10 (64-bit), macOS 12 of nieuwer, Android 8+ en iOS 15+. Op iOS zijn de functies beperkt tot VPN en de ESET HOME-app."),
   ("Is de licentie origineel en krijg ik een factuur?", "Ja. ESET-licenties zijn origineel en worden geactiveerd via de officiële kanalen van de fabrikant. We stellen facturen op voor particulieren en bedrijven en bieden ondersteuning per e-mail en WhatsApp."),
 ],
 "faq_devices": {
   1: "Deze versie beschermt 1 apparaat gedurende 12 maanden, op Windows, macOS of Android; op iOS zijn de VPN en de ESET HOME-app beschikbaar. U beheert alles via het ESET HOME-portaal.",
   3: "Deze versie beschermt 3 apparaten gedurende 12 maanden. Verdeel de bescherming over Windows-pc's, Macs en Android- of iOS-apparaten, allemaal beheerd via hetzelfde ESET HOME-account.",
 },
 "card_blurb": "Abonnement · digitale licentie",
},
}

TP_LANG = {"it": "it", "en": "www", "fr": "fr", "de": "de", "es": "es", "pt": "www", "nl": "www"}


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def jsonld(lang, n, v, name, desc, price):
    faq = []
    for q, a in build_faq(lang, n):
        faq.append({
            "@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
    graph = [
        {"@type": "Organization", "@id": "https://eurolicenze.com/#organization",
         "name": "Eurolicenze", "url": "https://eurolicenze.com/"},
        {"@type": "Product",
         "@id": f"https://eurolicenze.com/{lang}/{v['slug']}#product",
         "name": name, "sku": v["sku"], "inLanguage": lang,
         "url": f"https://eurolicenze.com/{lang}/{v['slug']}",
         "image": f"https://eurolicenze.com/asset/media/products/{v['slug']}.webp",
         "description": desc,
         "brand": {"@type": "Brand", "name": "ESET"},
         "offers": {"@type": "Offer",
                    "url": f"https://eurolicenze.com/{lang}/{v['slug']}",
                    "priceCurrency": "EUR", "price": price,
                    "availability": "https://schema.org/InStock",
                    "itemCondition": "https://schema.org/NewCondition",
                    "seller": {"@id": "https://eurolicenze.com/#organization"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": f"https://eurolicenze.com/{lang}/"},
            {"@type": "ListItem", "position": 2, "name": "Antivirus",
             "item": f"https://eurolicenze.com/{lang}/antivirus"},
            {"@type": "ListItem", "position": 3, "name": name},
        ]},
        {"@type": "FAQPage", "inLanguage": lang,
         "url": f"https://eurolicenze.com/{lang}/{v['slug']}",
         "mainEntity": faq},
    ]
    body = json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, indent=2)
    return '<script type="application/ld+json">\n' + body + '\n    </script>'


def build_faq(lang, n):
    out = []
    for q, a in C[lang]["faq"]:
        if a == "@DEVICES@":
            a = C[lang]["faq_devices"][n]
        out.append((q, a))
    return out


def specs_table(lang):
    c = C[lang]
    h1, h2 = c["specs_head"]
    rows = "".join(
        f'\n                        <tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td></tr>'
        for a, b in c["specs_rows"]
    )
    return (
        '<table class="pdp-table pdp-table--specs">\n'
        f'                    <caption class="visually-hidden">{esc(c["specs_caption"])}</caption>\n'
        '                    <thead>\n'
        f'                        <tr><th scope="col">{esc(h1)}</th><th scope="col">{esc(h2)}</th></tr>\n'
        '                    </thead>\n'
        '                    <tbody>' + rows + '\n'
        '                    </tbody>\n'
        '                </table>'
    )


def steps_ol(lang):
    parts = ['<ol class="pdp-steps">']
    for h, p in C[lang]["steps"]:
        parts.append(
            '                <li class="pdp-step">\n'
            '                    <div>\n'
            f'                        <h3>{h}</h3>\n'
            f'                        <p>{p}</p>\n'
            '                    </div>\n'
            '                </li>'
        )
    parts.append('            </ol>')
    return "\n".join(parts)


def dialog_ol(lang):
    parts = ['<ol class="pdp-dialog__steps">']
    for h, p in C[lang]["steps"]:
        parts.append(f'                    <li><strong>{h}</strong> {p}</li>')
    parts.append('        </ol>')
    return "\n".join(parts)


def keylist_ul(lang, n):
    vpncap = C[lang]["vpncap3"] if n == 3 else ""
    lis = "".join(
        f'\n                            <li>{item.format(nd=nd(lang, n), vpncap=vpncap)}</li>'
        for item in C[lang]["keylist"]
    )
    return '<ul class="pdp-keylist">' + lis + '\n                        </ul>'


def cards_ul(lang):
    icons = ["blue", "teal", "purple", "dark"]
    svgs = [
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
        '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
        '<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
        '<path d="m9 12 2 2 4-4"/><circle cx="12" cy="12" r="10"/>',
    ]
    out = ['<ul class="pdp-cards">']
    for (title, body), ic, sv in zip(C[lang]["cards"], icons, svgs):
        out.append(
            f'                <li class="pdp-card">\n'
            f'                    <span class="pdp-card__icon pdp-card__icon--custom pdp-card__icon--{ic}" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20">{sv}</svg></span>\n'
            f'                    <h3 class="pdp-card__title">{esc(title)}</h3>\n'
            f'                    <p class="pdp-card__body">{esc(body)}</p>\n'
            f'                </li>'
        )
    out.append('            </ul>')
    return "\n".join(out)


def plans_div(lang, current_n):
    sing, plur = DEV[lang]
    out = ['<div class="pdp-plans" role="group" aria-labelledby="pdp-plans-label">']
    for k in (1, 3):
        word = sing if k == 1 else plur
        label = f'{k} {word} · € {euro(VARIANTS[k]["sale"])}'
        if k == current_n:
            out.append(f'                    <span class="pdp-plan is-current" aria-current="true"><b>{k}</b><span>{label}</span></span>')
        else:
            out.append(f'                    <a class="pdp-plan" href="/{lang}/{SLUGS[k]}"><b>{k}</b><span>{label}</span></a>')
    out.append('                </div>')
    return "\n".join(out)


def sub_once(pattern, repl, text, label, flags=re.S):
    new, count = re.subn(pattern, lambda _m: repl, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"[{label}] atteso 1 match, trovati {count}")
    return new


def build_page(lang, n):
    v = VARIANTS[n]
    c = C[lang]
    src = (ROOT / lang / f"{SRC_SLUG}.html").read_text(encoding="utf-8")
    t = src
    ndv = nd(lang, n)
    name = c["name"].format(nd=ndv)
    desc = c["desc"].format(nd=ndv)
    title = c["title"].format(nd=ndv)
    price = dot(v["sale"])
    d = disc(v["sale"], v["comp"])

    # slug ovunque (canonical, og:url, hreflang, lang dropdown, preload, img, og:image)
    t = t.replace(SRC_SLUG, v["slug"])

    # <head> meta -------------------------------------------------------------
    t = sub_once(r"<title>.*?</title>", f"<title>{esc(title)}</title>", t, "title")
    t = sub_once(r'<meta name="description" content=".*?">',
                 f'<meta name="description" content="{esc(desc)}">', t, "meta-desc")
    t = sub_once(r'<meta property="og:title" content=".*?">',
                 f'<meta property="og:title" content="{esc(title)}">', t, "og:title")
    t = sub_once(r'<meta property="og:description" content=".*?">',
                 f'<meta property="og:description" content="{esc(desc)}">', t, "og:desc")
    t = sub_once(r'<meta property="product:price:amount" content=".*?">',
                 f'<meta property="product:price:amount" content="{price}">', t, "og:price")

    # JSON-LD (blocco intero) ----------------------------------------------
    t = sub_once(r'<script type="application/ld\+json">.*?</script>',
                 jsonld(lang, n, v, name, desc, price), t, "jsonld")

    # sticky CTA ----------------------------------------------------------
    t = sub_once(r'<span class="product-sticky-cta__title">.*?</span>',
                 f'<span class="product-sticky-cta__title">{esc(name)}</span>', t, "sticky-title")
    t = sub_once(r'<span class="product-sticky-cta__msrp">.*?</span>',
                 f'<span class="product-sticky-cta__msrp">€ {euro(v["comp"])}</span>', t, "sticky-msrp")
    t = sub_once(r'<span class="product-sticky-cta__sale">.*?</span>',
                 f'<span class="product-sticky-cta__sale">€ {euro(v["sale"])}</span>', t, "sticky-sale")

    # breadcrumb visibile ------------------------------------------------
    t = re.sub(r'(<div class="pdp-breadcrumb">.*?<span aria-current="page">).*?(</span>)',
               lambda m: m.group(1) + esc(name) + m.group(2), t, count=1, flags=re.S)

    # badge + codice --------------------------------------------------------
    t = sub_once(r'<span class="pdp-badge">.*?</span>',
                 f'<span class="pdp-badge">{esc(BRAND_LINE[lang].format(nd=ndv))}</span>', t, "badge")
    t = sub_once(r'<span class="pdp-badge pdp-badge--alt">.*?</span>',
                 '<span class="pdp-badge pdp-badge--alt">ESET</span>', t, "badge-alt")
    t = sub_once(r'<code class="v2-product-code__value">.*?</code>',
                 f'<code class="v2-product-code__value">{v["sku"]}</code>', t, "code")

    # H1 + hero desc ------------------------------------------------------
    t = sub_once(r'<h1 class="pdp-h1 v2-hero__title">.*?</h1>',
                 f'<h1 class="pdp-h1 v2-hero__title">{c["h1"].format(nd=esc(ndv))}</h1>', t, "h1")
    t = sub_once(r'<p class="v2-hero__desc">.*?</p>',
                 f'<p class="v2-hero__desc">{esc(c["hero"].format(nd=ndv))}</p>', t, "hero")

    # figura: alt immagine ------------------------------------------------
    t = re.sub(r'(class="pdp-media__img product-cover-img" src="[^"]*"[^>]*alt=")[^"]*(")',
               lambda m: m.group(1) + esc(name) + m.group(2), t, count=1)

    # keylist -----------------------------------------------------------
    t = sub_once(r'<ul class="pdp-keylist">.*?</ul>', keylist_ul(lang, n), t, "keylist")

    # buy card: attributi prezzo/sku ---------------------------------------
    t = sub_once(r'data-stripe-unit-amount="\d+"',
                 f'data-stripe-unit-amount="{v["sale"]}"', t, "unit")
    t = sub_once(r'data-stripe-compare-at-amount="\d+"',
                 f'data-stripe-compare-at-amount="{v["comp"]}"', t, "compare")
    t = sub_once(r'data-stripe-product-sku="[^"]+"',
                 f'data-stripe-product-sku="{v["sku"]}"', t, "sku-attr")
    t = sub_once(r'data-discount-percent="\d+"',
                 f'data-discount-percent="{d}"', t, "disc-attr")

    # selettore versioni (2 chip) ---------------------------------------
    t = sub_once(r'<div class="pdp-plans" role="group"[^>]*>.*?</div>',
                 plans_div(lang, n), t, "plans")

    # price row --------------------------------------------------------
    t = sub_once(r'<span class="pdp-price-sale">.*?</span>',
                 f'<span class="pdp-price-sale">€ {euro(v["sale"])}</span>', t, "price-sale")
    t = sub_once(r'<span class="pdp-price-msrp"[^>]*>.*?</span>',
                 f'<span class="pdp-price-msrp" aria-label="{euro(v["comp"])}">€ {euro(v["comp"])}</span>',
                 t, "price-msrp")
    t = sub_once(r'<span class="pdp-price-badge">.*?</span>',
                 f'<span class="pdp-price-badge">−{d}%</span>', t, "price-badge")

    # sezione "perché sceglierlo": titolo + sub + cards ------------------
    t = re.sub(
        r'(<h2 id="pdp-features-title"[^>]*>).*?(</h2>\s*<p class="pdp-sec__sub">).*?(</p>)',
        lambda m: m.group(1) + esc(c["feat_title"]) + m.group(2)
        + esc(c["feat_sub"].format(nd=ndv)) + m.group(3),
        t, count=1, flags=re.S)
    t = sub_once(r'<ul class="pdp-cards">.*?</ul>', cards_ul(lang), t, "cards")

    # requisiti di sistema: tabella intera -----------------------------
    t = sub_once(r'<table class="pdp-table pdp-table--specs">.*?</table>',
                 specs_table(lang), t, "specs")

    # passi + dialog --------------------------------------------------
    t = sub_once(r'<ol class="pdp-steps">.*?</ol>', steps_ol(lang), t, "steps")
    t = sub_once(r'<ol class="pdp-dialog__steps">.*?</ol>', dialog_ol(lang), t, "dialog")

    # FAQ visibile (2 colonne, 3+3) ----------------------------------
    faq = build_faq(lang, n)
    col1 = faq[:3]
    col2 = faq[3:]

    def faq_col(items):
        rows = []
        for q, a in items:
            rows.append(
                '                <details class="home-faq-item">\n'
                f'                    <summary>{esc(q)}</summary>\n'
                '                    <div class="home-faq-body">\n'
                f'                        <p>{esc(a)}</p>\n'
                '                    </div>\n'
                '                </details>'
            )
        return '                <div class="pf-faq-col">\n' + "\n".join(rows) + '\n                </div>'

    faq_block = ('<div class="home-faq-list">\n' + faq_col(col1) + '\n' + faq_col(col2)
                 + '\n            </div>\n        </section>')
    t = sub_once(r'<div class="home-faq-list">.*?</div>\s*</section>', faq_block, t, "faq")

    # nav/drawer: sposta lo stato "corrente" da McAfee a ESET NOD32 -------
    t = t.replace(
        f'<a href="/{lang}/mcafee-total-protection-1-device" role="menuitem" aria-current="page">',
        f'<a href="/{lang}/mcafee-total-protection-1-device" role="menuitem">')
    t = t.replace(
        f'<a href="/{lang}/eset-nod32-1-device" role="menuitem">ESET NOD32</a>',
        f'<a href="/{lang}/eset-nod32-1-device" role="menuitem" aria-current="page">ESET NOD32</a>')
    t = t.replace(
        f'<a href="/{lang}/mcafee-total-protection-1-device" class="active">McAfee Total Protection</a>',
        f'<a href="/{lang}/mcafee-total-protection-1-device">McAfee Total Protection</a>')
    t = t.replace(
        f'<a href="/{lang}/eset-nod32-1-device">ESET NOD32</a>',
        f'<a href="/{lang}/eset-nod32-1-device" class="active">ESET NOD32</a>')

    if "mcafee-total-protection-3-devices" in t:
        raise SystemExit(f"[{lang}/{v['slug']}] slug McAfee residuo")
    return t


# --- catalog -------------------------------------------------------------
def update_catalog_json(apply):
    path = ROOT / "catalog.json"
    entries = json.loads(path.read_text(encoding="utf-8"))
    have = {e["sku"] for e in entries}
    add = []
    for n, v in VARIANTS.items():
        if v["sku"] in have:
            print(f"catalog.json: {v['sku']} gia' presente, salto")
            continue
        add.append({
            "sku": v["sku"], "ean": v["ean"],
            "name": f"ESET HOME Security Premium | 1 Anno | {nd_title(n)}",
            "unitAmountMinor": v["sale"], "compareAtMinor": v["comp"],
            "currency": "EUR", "type": "subscription", "category": "antivirus",
        })
    if not add:
        return
    entries.extend(add)
    print(f"catalog.json: +{len(add)} voci")
    if apply:
        path.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")


def update_catalog_js(apply):
    path = ROOT / "functions" / "api" / "_lib" / "catalog.js"
    t = path.read_text(encoding="utf-8")
    lines = []
    for n, v in VARIANTS.items():
        if v["sku"] in t:
            print(f"catalog.js: {v['sku']} gia' presente, salto")
            continue
        lines.append(
            f'  "{v["sku"]}": {{ name: "ESET HOME Security Premium | 1 Anno | '
            f'{nd_title(n)}", unitAmountMinor: {v["sale"]}, '
            f'compareAtMinor: {v["comp"]}, currency: \'EUR\', type: "subscription", '
            f'category: "antivirus" }},'
        )
    if not lines:
        return
    anchor = '  "EAVH-N2-A1": {'
    i = t.index(anchor)
    j = t.index("\n", i) + 1
    t = t[:j] + "\n".join(lines) + "\n" + t[j:]
    print(f"catalog.js: +{len(lines)} voci dopo EAVH-N2-A1")
    if apply:
        path.write_text(t, encoding="utf-8")


# --- card pagina categoria --------------------------------------------
CARD_OPEN = '                <div\n                    class="product-card"\n'


def add_category_cards(lang, apply):
    p = ROOT / lang / "antivirus.html"
    t = p.read_text(encoding="utf-8")
    if f"{SLUGS[3]}.html" in t:
        print(f"{lang}/antivirus.html: card gia' presenti, salto")
        return
    anchor = 'data-stripe-product-sku="EAVH-N1-A10"'
    si = t.find(anchor)
    if si < 0:
        print(f"{lang}/antivirus.html: ancora NOD32-10 non trovata, card NON aggiunte")
        return
    start = t.rfind(CARD_OPEN, 0, si)
    end = t.find(CARD_OPEN, si)
    if start < 0 or end < 0:
        print(f"{lang}/antivirus.html: confini card NOD32-10 non trovati")
        return
    tmpl = t[start:end]  # blocco card NOD32-10 dispositivi (chiuso da </div>\n)
    if 'data-stripe-product-sku="EAVH-N1-A10"' not in tmpl or not tmpl.rstrip().endswith("</div>"):
        print(f"{lang}/antivirus.html: card NOD32-10 malformata")
        return
    sing, plur = DEV[lang]
    blocks = []
    for n in (1, 3):
        v = VARIANTS[n]
        word = sing if n == 1 else plur
        card = tmpl
        card = card.replace('data-stripe-unit-amount="7300"', f'data-stripe-unit-amount="{v["sale"]}"')
        card = card.replace('data-stripe-compare-at-amount="8499"', f'data-stripe-compare-at-amount="{v["comp"]}"')
        card = card.replace('data-stripe-product-sku="EAVH-N1-A10"', f'data-stripe-product-sku="{v["sku"]}"')
        card = card.replace('data-discount-percent="14"', f'data-discount-percent="{disc(v["sale"], v["comp"])}"')
        card = re.sub(r'href="eset-nod32-10-devices\.html"', f'href="{v["slug"]}.html"', card)
        card = re.sub(r'src="\.\./asset/media/products/eset-nod32-10-devices\.webp(\?v=[a-f0-9]+)?"',
                      f'src="../asset/media/products/{v["slug"]}.webp"', card)
        card = re.sub(r'alt="[^"]*"', f'alt="ESET HOME Security Premium — {n} {word}"', card, count=1)
        card = re.sub(r'<p class="product-card-name">[^<]*</p>',
                      f'<p class="product-card-name">ESET HOME Security Premium — {n} {word}</p>', card)
        card = re.sub(r'<p class="product-card-blurb">[^<]*</p>',
                      f'<p class="product-card-blurb">{esc(C[lang]["card_blurb"])}</p>', card)
        card = re.sub(r'<span class="product-card-price-block__msrp">[^<]*</span>',
                      f'<span class="product-card-price-block__msrp">€ {euro(v["comp"])}</span>', card)
        card = re.sub(r'<span class="product-card-price-block__sale">[^<]*</span>',
                      f'<span class="product-card-price-block__sale">€ {euro(v["sale"])}</span>', card)
        card = re.sub(r'<span class="product-card-price-block__save">[^<]*</span>',
                      f'<span class="product-card-price-block__save">−{disc(v["sale"], v["comp"])}%</span>', card)
        blocks.append(card)
    out = t[:end] + "".join(blocks) + t[end:]
    print(f"{lang}/antivirus.html: +2 card ESET HOME Security Premium dopo NOD32-10")
    if apply:
        p.write_text(out, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    apply = args.apply

    update_catalog_json(apply)
    update_catalog_js(apply)

    for lang in LANGS:
        for n in (1, 3):
            out = build_page(lang, n)
            dest = ROOT / lang / f"{VARIANTS[n]['slug']}.html"
            print(f"{lang}/{VARIANTS[n]['slug']}.html: {'scritta' if apply else 'anteprima'} ({len(out)} byte)")
            if apply:
                dest.write_text(out, encoding="utf-8")
        add_category_cards(lang, apply)

    if not apply:
        print("\nDry-run. Rilancia con --apply.")


if __name__ == "__main__":
    main()
