#!/usr/bin/env python3
"""Rich content per i bundle Microsoft 365 Personal + antivirus (Kaspersky
Premium, McAfee Total Protection). Stesso approccio di product_content_tools.py:
`steps`/`specs` propri, il chrome UI condiviso arriva da product_content_windows.UI.
"""

from nl_translations import nl_text

LANGS = ("it", "en", "fr", "de", "es", "pt", "nl")


def L(**kwargs):
    if "pt" not in kwargs:
        kwargs["pt"] = kwargs.get("es") or kwargs.get("en")
    if "nl" not in kwargs:
        kwargs["nl"] = kwargs.get("en")
    return {k: kwargs[k] for k in LANGS}


def _bundle(av_name, av_short, av_feature_it, av_feature_en, av_feature_fr, av_feature_de, av_feature_es, av_feature_pt, av_feature_nl=None):
    return {
        # Bundle con M365 Personal: idoneo alla guida Copilot omaggio (solo IT,
        # vedi functions/api/_lib/guide.js M365_SKUS/GUIDE_LOCALES).
        "copilot_bonus": True,
        "title_html": L(
            it=f'Microsoft 365 Personal <span>+ {av_short}</span>',
            en=f'Microsoft 365 Personal <span>+ {av_short}</span>',
            fr=f'Microsoft 365 Personal <span>+ {av_short}</span>',
            de=f'Microsoft 365 Personal <span>+ {av_short}</span>',
            es=f'Microsoft 365 Personal <span>+ {av_short}</span>',
            pt=f'Microsoft 365 Personal <span>+ {av_short}</span>',
            nl=f'Microsoft 365 Personal <span>+ {av_short}</span>',
        ),
        "eyebrow": L(
            it="Pacchetto digitale · Office + sicurezza in un ordine",
            en="Digital bundle · Office + security in one order",
            fr="Pack numérique · Office + sécurité en une commande",
            de="Digitales Paket · Office + Sicherheit in einer Bestellung",
            es="Pack digital · Office + seguridad en un solo pedido",
            pt="Pacote digital · Office + segurança num só pedido",
            nl="Digitaal pakket · Office + beveiliging in één bestelling",
        ),
        "desc": L(
            it=f"Microsoft 365 Personal in abbonamento più {av_name} in un unico ordine: le app Office sempre aggiornate e {av_short} su fino a 5 dispositivi. Due codici via email dopo l'acquisto.",
            en=f"Microsoft 365 Personal subscription plus {av_name} in a single order: always up-to-date Office apps and {av_short} on up to 5 devices. Two codes by email after purchase.",
            fr=f"Abonnement Microsoft 365 Personal plus {av_name} en une seule commande : applications Office toujours à jour et {av_short} sur jusqu'à 5 appareils. Deux codes par e-mail après l'achat.",
            de=f"Microsoft-365-Personal-Abo plus {av_name} in einer Bestellung: stets aktuelle Office-Apps und {av_short} auf bis zu 5 Geräten. Zwei Codes per E-Mail nach dem Kauf.",
            es=f"Suscripción a Microsoft 365 Personal más {av_name} en un solo pedido: apps Office siempre actualizadas y {av_short} en hasta 5 dispositivos. Dos códigos por email tras la compra.",
            pt=f"Subscrição Microsoft 365 Personal mais {av_name} num único pedido: apps Office sempre atualizadas e {av_short} em até 5 dispositivos. Dois códigos por email após a compra.",
            nl=f"Microsoft 365 Personal-abonnement plus {av_name} in één bestelling: altijd actuele Office-apps en {av_short} op maximaal 5 apparaten. Twee codes per e-mail na aankoop.",
        ),
        "features_title": L(
            it="Produttività e sicurezza, insieme",
            en="Productivity and security, together",
            fr="Productivité et sécurité, ensemble",
            de="Produktivität und Sicherheit vereint",
            es="Productividad y seguridad, juntas",
            pt="Produtividade e segurança, juntas",
            nl="Productiviteit en beveiliging, samen",
        ),
        "keypoints": L(
            it=["Word, Excel, PowerPoint sempre aggiornati", "1 TB di spazio OneDrive", f"{av_short} su fino a 5 dispositivi", "Due licenze, un solo checkout"],
            en=["Word, Excel, PowerPoint always up to date", "1 TB of OneDrive storage", f"{av_short} on up to 5 devices", "Two licences, a single checkout"],
            fr=["Word, Excel, PowerPoint toujours à jour", "1 To d'espace OneDrive", f"{av_short} sur jusqu'à 5 appareils", "Deux licences, un seul paiement"],
            de=["Word, Excel, PowerPoint stets aktuell", "1 TB OneDrive-Speicher", f"{av_short} auf bis zu 5 Geräten", "Zwei Lizenzen, ein Checkout"],
            es=["Word, Excel, PowerPoint siempre actualizados", "1 TB de espacio OneDrive", f"{av_short} en hasta 5 dispositivos", "Dos licencias, un solo pago"],
            pt=["Word, Excel, PowerPoint sempre atualizados", "1 TB de espaço OneDrive", f"{av_short} em até 5 dispositivos", "Duas licenças, um só checkout"],
            nl=["Word, Excel, PowerPoint altijd actueel", "1 TB OneDrive-opslag", f"{av_short} op maximaal 5 apparaten", "Twee licenties, één checkout"],
        ),
        "features": {
            "it": [
                ("c8", "blue", "Office", "Microsoft 365 Personal incluso", "Word, Excel, PowerPoint e Outlook sempre aggiornati, con 1 TB di OneDrive e Copilot integrato, per 1 utente."),
                ("c4", "teal", "Sicurezza", av_short, av_feature_it),
                ("c4", "purple", "Risparmio", "Un solo ordine, un solo prezzo", "Acquisti entrambe le licenze in un unico checkout, a un prezzo più conveniente che separatamente."),
                ("c4", None, "Consegna", "Due codici via email", "Ricevi i codici di attivazione di Office e dell'antivirus nella stessa email di conferma."),
                ("c4", None, "Attivazione", "Due account ufficiali", "Attivi Microsoft 365 sul tuo account Microsoft e la protezione sul portale del produttore antivirus."),
                ("c4", "dark", "Copertura", "Fino a 5 dispositivi protetti", "La protezione antivirus copre più dispositivi della famiglia; Microsoft 365 Personal resta per 1 utente."),
            ],
            "en": [
                ("c8", "blue", "Office", "Microsoft 365 Personal included", "Word, Excel, PowerPoint and Outlook always up to date, with 1 TB of OneDrive and built-in Copilot, for 1 user."),
                ("c4", "teal", "Security", av_short, av_feature_en),
                ("c4", "purple", "Savings", "One order, one price", "Buy both licences in a single checkout, at a better price than buying them separately."),
                ("c4", None, "Delivery", "Two codes by email", "You receive the activation codes for Office and the antivirus in the same confirmation email."),
                ("c4", None, "Activation", "Two official accounts", "Activate Microsoft 365 on your Microsoft account and the protection on the antivirus vendor's portal."),
                ("c4", "dark", "Coverage", "Up to 5 devices protected", "Antivirus protection covers several household devices; Microsoft 365 Personal remains for 1 user."),
            ],
            "fr": [
                ("c8", "blue", "Office", "Microsoft 365 Personal inclus", "Word, Excel, PowerPoint et Outlook toujours à jour, avec 1 To de OneDrive et Copilot intégré, pour 1 utilisateur."),
                ("c4", "teal", "Sécurité", av_short, av_feature_fr),
                ("c4", "purple", "Économie", "Une seule commande, un seul prix", "Achetez les deux licences en un seul paiement, à un prix plus avantageux que séparément."),
                ("c4", None, "Livraison", "Deux codes par e-mail", "Vous recevez les codes d'activation d'Office et de l'antivirus dans le même e-mail de confirmation."),
                ("c4", None, "Activation", "Deux comptes officiels", "Activez Microsoft 365 sur votre compte Microsoft et la protection sur le portail de l'éditeur antivirus."),
                ("c4", "dark", "Couverture", "Jusqu'à 5 appareils protégés", "La protection antivirus couvre plusieurs appareils du foyer ; Microsoft 365 Personal reste pour 1 utilisateur."),
            ],
            "de": [
                ("c8", "blue", "Office", "Microsoft 365 Personal inklusive", "Word, Excel, PowerPoint und Outlook stets aktuell, mit 1 TB OneDrive und integriertem Copilot, für 1 Nutzer."),
                ("c4", "teal", "Sicherheit", av_short, av_feature_de),
                ("c4", "purple", "Ersparnis", "Eine Bestellung, ein Preis", "Beide Lizenzen in einem Checkout kaufen, zu einem günstigeren Preis als einzeln."),
                ("c4", None, "Lieferung", "Zwei Codes per E-Mail", "Sie erhalten die Aktivierungscodes für Office und den Virenschutz in derselben Bestätigungs-E-Mail."),
                ("c4", None, "Aktivierung", "Zwei offizielle Konten", "Microsoft 365 im Microsoft-Konto aktivieren, den Schutz im Portal des Antivirus-Herstellers."),
                ("c4", "dark", "Abdeckung", "Bis zu 5 geschützte Geräte", "Der Virenschutz deckt mehrere Geräte im Haushalt ab; Microsoft 365 Personal bleibt für 1 Nutzer."),
            ],
            "es": [
                ("c8", "blue", "Office", "Microsoft 365 Personal incluido", "Word, Excel, PowerPoint y Outlook siempre actualizados, con 1 TB de OneDrive y Copilot integrado, para 1 usuario."),
                ("c4", "teal", "Seguridad", av_short, av_feature_es),
                ("c4", "purple", "Ahorro", "Un solo pedido, un solo precio", "Compra ambas licencias en un único pago, a un precio mejor que por separado."),
                ("c4", None, "Entrega", "Dos códigos por email", "Recibes los códigos de activación de Office y del antivirus en el mismo email de confirmación."),
                ("c4", None, "Activación", "Dos cuentas oficiales", "Activa Microsoft 365 en tu cuenta Microsoft y la protección en el portal del fabricante del antivirus."),
                ("c4", "dark", "Cobertura", "Hasta 5 dispositivos protegidos", "La protección antivirus cubre varios dispositivos del hogar; Microsoft 365 Personal sigue siendo para 1 usuario."),
            ],
            "pt": [
                ("c8", "blue", "Office", "Microsoft 365 Personal incluído", "Word, Excel, PowerPoint e Outlook sempre atualizados, com 1 TB de OneDrive e Copilot integrado, para 1 utilizador."),
                ("c4", "teal", "Segurança", av_short, av_feature_pt),
                ("c4", "purple", "Poupança", "Um só pedido, um só preço", "Compra ambas as licenças num único checkout, a um preço mais vantajoso do que em separado."),
                ("c4", None, "Entrega", "Dois códigos por email", "Recebe os códigos de ativação do Office e do antivírus no mesmo email de confirmação."),
                ("c4", None, "Ativação", "Duas contas oficiais", "Ativa o Microsoft 365 na tua conta Microsoft e a proteção no portal do fabricante do antivírus."),
                ("c4", "dark", "Cobertura", "Até 5 dispositivos protegidos", "A proteção antivírus cobre vários dispositivos da família; o Microsoft 365 Personal continua para 1 utilizador."),
            ],
            "nl": [
                ("c8", "blue", "Office", "Microsoft 365 Personal inbegrepen", "Word, Excel, PowerPoint en Outlook altijd actueel, met 1 TB OneDrive en geïntegreerde Copilot, voor 1 gebruiker."),
                ("c4", "teal", "Beveiliging", av_short, av_feature_nl or av_feature_en),
                ("c4", "purple", "Voordeel", "Eén bestelling, één prijs", "Koop beide licenties in één checkout, voordeliger dan afzonderlijk."),
                ("c4", None, "Levering", "Twee codes per e-mail", "U ontvangt de activeringscodes van Office en de antivirus in dezelfde bevestigingsmail."),
                ("c4", None, "Activering", "Twee officiële accounts", "Activeer Microsoft 365 op uw Microsoft-account en de beveiliging op het portaal van de antivirusuitgever."),
                ("c4", "dark", "Dekking", "Maximaal 5 beveiligde apparaten", "De antivirusdekking geldt voor meerdere apparaten in huis; Microsoft 365 Personal blijft voor 1 gebruiker."),
            ],
        },
        "steps": {
            "it": [
                ("Ordine e pagamento", "Aggiungi il bundle al carrello e completa il pagamento con i metodi disponibili."),
                ("Consegna digitale", "Ricevi via email entrambi i codici — Microsoft 365 e antivirus — di norma entro pochi minuti dal pagamento."),
                ("Doppia attivazione", "Colleghi il codice Microsoft 365 al tuo account Microsoft e installi l'antivirus con il proprio codice sul portale del produttore."),
            ],
            "en": [
                ("Order and payment", "Add the bundle to your cart and complete checkout with the available methods."),
                ("Digital delivery", "You receive both codes — Microsoft 365 and antivirus — usually within minutes of payment."),
                ("Two activations", "Link the Microsoft 365 code to your Microsoft account and install the antivirus with its own code on the vendor's portal."),
            ],
            "fr": [
                ("Commande et paiement", "Ajoutez le pack au panier et finalisez le paiement avec les méthodes disponibles."),
                ("Livraison numérique", "Vous recevez les deux codes — Microsoft 365 et antivirus — généralement en quelques minutes."),
                ("Deux activations", "Liez le code Microsoft 365 à votre compte Microsoft et installez l'antivirus avec son propre code sur le portail de l'éditeur."),
            ],
            "de": [
                ("Bestellung und Zahlung", "Paket in den Warenkorb legen und die Zahlung mit den verfügbaren Methoden abschließen."),
                ("Digitale Lieferung", "Sie erhalten beide Codes — Microsoft 365 und Virenschutz — meist innerhalb weniger Minuten."),
                ("Zwei Aktivierungen", "Microsoft-365-Code im Microsoft-Konto verknüpfen und den Virenschutz mit eigenem Code im Herstellerportal installieren."),
            ],
            "es": [
                ("Pedido y pago", "Añade el pack al carrito y completa el pago con los métodos disponibles."),
                ("Entrega digital", "Recibes ambos códigos —Microsoft 365 y antivirus— normalmente en pocos minutos."),
                ("Doble activación", "Vincula el código de Microsoft 365 a tu cuenta Microsoft e instala el antivirus con su propio código en el portal del fabricante."),
            ],
            "pt": [
                ("Pedido e pagamento", "Adiciona o pacote ao carrinho e conclui o pagamento com os métodos disponíveis."),
                ("Entrega digital", "Recebes por email ambos os códigos — Microsoft 365 e antivírus — normalmente em poucos minutos após o pagamento."),
                ("Dupla ativação", "Associa o código Microsoft 365 à tua conta Microsoft e instala o antivírus com o seu próprio código no portal do fabricante."),
            ],
        },
        "specs": {
            "it": [
                ("Microsoft 365", "Windows 10/11, macOS, web e app mobile; 1 utente, 1 TB OneDrive."),
                ("Antivirus", f"{av_short}: fino a 5 dispositivi Windows, macOS, Android o iOS secondo il piano."),
                ("Connessione", "Internet richiesta per attivazione, aggiornamenti e funzioni cloud di entrambi i prodotti."),
                ("Validità", "La durata di ciascun abbonamento è indicata nella scheda prodotto e nell'email di consegna."),
            ],
            "en": [
                ("Microsoft 365", "Windows 10/11, macOS, web and mobile app; 1 user, 1 TB OneDrive."),
                ("Antivirus", f"{av_short}: up to 5 Windows, macOS, Android or iOS devices depending on the plan."),
                ("Connection", "Internet required for activation, updates and cloud features of both products."),
                ("Validity", "The term of each subscription is shown on the product page and in the delivery email."),
            ],
            "fr": [
                ("Microsoft 365", "Windows 10/11, macOS, web et app mobile ; 1 utilisateur, 1 To OneDrive."),
                ("Antivirus", f"{av_short} : jusqu'à 5 appareils Windows, macOS, Android ou iOS selon le forfait."),
                ("Connexion", "Internet requis pour l'activation, les mises à jour et les fonctions cloud des deux produits."),
                ("Validité", "La durée de chaque abonnement est indiquée sur la fiche produit et dans l'e-mail de livraison."),
            ],
            "de": [
                ("Microsoft 365", "Windows 10/11, macOS, Web und Mobil-App; 1 Nutzer, 1 TB OneDrive."),
                ("Virenschutz", f"{av_short}: bis zu 5 Windows-, macOS-, Android- oder iOS-Geräte je nach Plan."),
                ("Verbindung", "Internet erforderlich für Aktivierung, Updates und Cloud-Funktionen beider Produkte."),
                ("Laufzeit", "Die Laufzeit jedes Abos steht auf der Produktseite und in der Liefer-E-Mail."),
            ],
            "es": [
                ("Microsoft 365", "Windows 10/11, macOS, web y app móvil; 1 usuario, 1 TB de OneDrive."),
                ("Antivirus", f"{av_short}: hasta 5 dispositivos Windows, macOS, Android o iOS según el plan."),
                ("Conexión", "Internet necesario para la activación, las actualizaciones y las funciones en la nube de ambos productos."),
                ("Vigencia", "La duración de cada suscripción se indica en la ficha del producto y en el email de entrega."),
            ],
            "pt": [
                ("Microsoft 365", "Windows 10/11, macOS, web e app móvel; 1 utilizador, 1 TB OneDrive."),
                ("Antivírus", f"{av_short}: até 5 dispositivos Windows, macOS, Android ou iOS de acordo com o plano."),
                ("Ligação", "Internet necessária para ativação, atualizações e funções na nuvem de ambos os produtos."),
                ("Validade", "A duração de cada subscrição está indicada na ficha do produto e no email de entrega."),
            ],
        },
        "faq": {
            "it": [
                ("Ricevo due licenze separate?", "Sì: un codice per Microsoft 365 Personal e uno per l'antivirus, entrambi nella stessa email."),
                ("I due prodotti coprono lo stesso numero di dispositivi?", "No: Microsoft 365 Personal è per 1 utente, l'antivirus copre più dispositivi (fino a 5) secondo il piano."),
                ("Ho già Microsoft 365: posso comprare solo l'antivirus?", "Questa scheda è per il bundle; se ti serve solo l'antivirus, cercalo singolarmente nel catalogo."),
                ("Come si attivano le due licenze?", "Microsoft 365 si collega al tuo account Microsoft; l'antivirus si installa e attiva sul portale del produttore con il proprio codice."),
                ("Cosa succede al rinnovo?", "Ogni abbonamento si rinnova secondo i propri termini; puoi gestire i rinnovi separatamente dai due account."),
                ("È più conveniente del prezzo separato?", "Sì, il prezzo del bundle è pensato per costare meno della somma dei due prodotti acquistati separatamente."),
            ],
            "en": [
                ("Do I get two separate licences?", "Yes: one code for Microsoft 365 Personal and one for the antivirus, both in the same email."),
                ("Do the two products cover the same number of devices?", "No: Microsoft 365 Personal is for 1 user, the antivirus covers more devices (up to 5) depending on the plan."),
                ("I already have Microsoft 365 — can I buy just the antivirus?", "This page is for the bundle; if you only need the antivirus, look for it separately in the catalogue."),
                ("How do I activate the two licences?", "Microsoft 365 links to your Microsoft account; the antivirus is installed and activated on the vendor's portal with its own code."),
                ("What happens at renewal?", "Each subscription renews under its own terms; you can manage renewals separately from the two accounts."),
                ("Is it cheaper than buying separately?", "Yes, the bundle price is designed to cost less than the sum of the two products bought separately."),
            ],
            "fr": [
                ("Est-ce que je reçois deux licences séparées ?", "Oui : un code pour Microsoft 365 Personal et un pour l'antivirus, tous deux dans le même e-mail."),
                ("Les deux produits couvrent-ils le même nombre d'appareils ?", "Non : Microsoft 365 Personal est pour 1 utilisateur, l'antivirus couvre plus d'appareils (jusqu'à 5) selon le forfait."),
                ("J'ai déjà Microsoft 365, puis-je acheter seulement l'antivirus ?", "Cette fiche concerne le pack ; si vous n'avez besoin que de l'antivirus, cherchez-le séparément dans le catalogue."),
                ("Comment activer les deux licences ?", "Microsoft 365 se lie à votre compte Microsoft ; l'antivirus s'installe et s'active sur le portail de l'éditeur avec son propre code."),
                ("Que se passe-t-il au renouvellement ?", "Chaque abonnement se renouvelle selon ses propres conditions ; vous gérez les renouvellements séparément depuis les deux comptes."),
                ("Est-ce plus avantageux que séparément ?", "Oui, le prix du pack est conçu pour coûter moins cher que la somme des deux produits achetés séparément."),
            ],
            "de": [
                ("Erhalte ich zwei separate Lizenzen?", "Ja: ein Code für Microsoft 365 Personal und einer für den Virenschutz, beide in derselben E-Mail."),
                ("Decken die beiden Produkte dieselbe Geräteanzahl ab?", "Nein: Microsoft 365 Personal ist für 1 Nutzer, der Virenschutz deckt je nach Plan mehr Geräte ab (bis zu 5)."),
                ("Ich habe bereits Microsoft 365 — kann ich nur den Virenschutz kaufen?", "Diese Seite gilt für das Paket; wenn Sie nur den Virenschutz brauchen, suchen Sie ihn separat im Katalog."),
                ("Wie werden die beiden Lizenzen aktiviert?", "Microsoft 365 wird mit Ihrem Microsoft-Konto verknüpft; der Virenschutz wird mit eigenem Code im Herstellerportal installiert und aktiviert."),
                ("Was passiert bei der Verlängerung?", "Jedes Abo verlängert sich nach eigenen Bedingungen; Sie verwalten die Verlängerungen separat über die beiden Konten."),
                ("Ist es günstiger als getrennter Kauf?", "Ja, der Paketpreis ist so gestaltet, dass er günstiger ist als die Summe der beiden einzeln gekauften Produkte."),
            ],
            "es": [
                ("¿Recibo dos licencias separadas?", "Sí: un código para Microsoft 365 Personal y otro para el antivirus, ambos en el mismo email."),
                ("¿Los dos productos cubren el mismo número de dispositivos?", "No: Microsoft 365 Personal es para 1 usuario, el antivirus cubre más dispositivos (hasta 5) según el plan."),
                ("Ya tengo Microsoft 365, ¿puedo comprar solo el antivirus?", "Esta ficha es para el pack; si solo necesitas el antivirus, búscalo por separado en el catálogo."),
                ("¿Cómo se activan las dos licencias?", "Microsoft 365 se vincula a tu cuenta Microsoft; el antivirus se instala y activa en el portal del fabricante con su propio código."),
                ("¿Qué pasa al renovar?", "Cada suscripción se renueva según sus propias condiciones; puedes gestionar las renovaciones por separado desde las dos cuentas."),
                ("¿Es más barato que comprarlos por separado?", "Sí, el precio del pack está pensado para costar menos que la suma de los dos productos comprados por separado."),
            ],
            "pt": [
                ("Recebo duas licenças separadas?", "Sim: um código para Microsoft 365 Personal e outro para o antivírus, ambos no mesmo email."),
                ("Os dois produtos cobrem o mesmo número de dispositivos?", "Não: o Microsoft 365 Personal é para 1 utilizador, o antivírus cobre mais dispositivos (até 5) de acordo com o plano."),
                ("Já tenho Microsoft 365: posso comprar só o antivírus?", "Esta ficha é para o pacote; se precisares apenas do antivírus, procura-o em separado no catálogo."),
                ("Como se ativam as duas licenças?", "O Microsoft 365 associa-se à tua conta Microsoft; o antivírus instala-se e ativa-se no portal do fabricante com o seu próprio código."),
                ("O que acontece na renovação?", "Cada subscrição renova-se de acordo com os seus próprios termos; podes gerir as renovações separadamente a partir das duas contas."),
                ("É mais vantajoso do que comprar em separado?", "Sim, o preço do pacote foi pensado para custar menos do que a soma dos dois produtos comprados separadamente."),
            ],
        },
    }


PRODUCTS = {
    "bundle-m365-personal-kaspersky": _bundle(
        av_name={"it": "Kaspersky Premium", "en": "Kaspersky Premium", "fr": "Kaspersky Premium", "de": "Kaspersky Premium", "es": "Kaspersky Premium", "pt": "Kaspersky Premium"}["it"],
        av_short="Kaspersky Premium",
        av_feature_it="Protezione in tempo reale, VPN e strumenti anti-phishing su fino a 5 dispositivi.",
        av_feature_en="Real-time protection, VPN and anti-phishing tools on up to 5 devices.",
        av_feature_fr="Protection en temps réel, VPN et outils anti-hameçonnage sur jusqu'à 5 appareils.",
        av_feature_de="Echtzeitschutz, VPN und Anti-Phishing-Tools auf bis zu 5 Geräten.",
        av_feature_es="Protección en tiempo real, VPN y herramientas antiphishing en hasta 5 dispositivos.",
        av_feature_pt="Proteção em tempo real, VPN e ferramentas antiphishing em até 5 dispositivos.",
        av_feature_nl="Realtimebescherming, VPN en anti-phishingtools op maximaal 5 apparaten.",
    ),
    "bundle-m365-personal-mcafee": _bundle(
        av_name={"it": "McAfee Total Protection", "en": "McAfee Total Protection", "fr": "McAfee Total Protection", "de": "McAfee Total Protection", "es": "McAfee Total Protection", "pt": "McAfee Total Protection"}["it"],
        av_short="McAfee Total Protection",
        av_feature_it="Antivirus, firewall, VPN e monitoraggio dell'identità su fino a 5 dispositivi.",
        av_feature_en="Antivirus, firewall, VPN and identity monitoring on up to 5 devices.",
        av_feature_fr="Antivirus, pare-feu, VPN et surveillance d'identité sur jusqu'à 5 appareils.",
        av_feature_de="Virenschutz, Firewall, VPN und Identitätsüberwachung auf bis zu 5 Geräten.",
        av_feature_es="Antivirus, cortafuegos, VPN y supervisión de identidad en hasta 5 dispositivos.",
        av_feature_pt="Antivírus, firewall, VPN e monitorização de identidade em até 5 dispositivos.",
        av_feature_nl="Antivirus, firewall, VPN en identiteitsbewaking op maximaal 5 apparaten.",
    ),
    "bundle-windows-11-home-m365-personal": {
        # Idoneo alla guida Copilot omaggio (solo IT, vedi guide.js M365_SKUS).
        "copilot_bonus": True,
        "title_html": L(
            it='Windows 11 Home <span>+ M365 Personal</span>',
            en='Windows 11 Home <span>+ M365 Personal</span>',
            fr='Windows 11 Home <span>+ M365 Personal</span>',
            de='Windows 11 Home <span>+ M365 Personal</span>',
            es='Windows 11 Home <span>+ M365 Personal</span>',
            pt='Windows 11 Home <span>+ M365 Personal</span>',
            nl='Windows 11 Home <span>+ M365 Personal</span>',
        ),
        "eyebrow": L(
            it="Pacchetto digitale · Licenza a vita + abbonamento 12 mesi",
            en="Digital bundle · Lifetime licence + 12-month subscription",
            fr="Pack numérique · Licence à vie + abonnement 12 mois",
            de="Digitales Paket · Dauerlizenz + 12-Monats-Abo",
            es="Pack digital · Licencia de por vida + suscripción de 12 meses",
            pt="Pacote digital · Licença vitalícia + subscrição de 12 meses",
            nl="Digitaal pakket · permanente licentie + 12 maanden abonnement",
        ),
        "desc": L(
            it="Windows 11 Home in licenza digitale a vita più l'abbonamento Microsoft 365 Personal di 12 mesi: app Office sempre aggiornate, 1 TB OneDrive, Copilot AI e consegna via email in pochi minuti.",
            en="Windows 11 Home as a lifetime digital licence plus a 12-month Microsoft 365 Personal subscription: always up-to-date Office apps, 1 TB of OneDrive, Copilot AI and delivery by email in minutes.",
            fr="Windows 11 Home en licence numérique à vie plus l'abonnement Microsoft 365 Personal de 12 mois : applications Office toujours à jour, 1 To de OneDrive, Copilot IA et livraison par e-mail en quelques minutes.",
            de="Windows 11 Home als digitale Dauerlizenz plus ein 12-monatiges Microsoft-365-Personal-Abo: stets aktuelle Office-Apps, 1 TB OneDrive, Copilot KI und Lieferung per E-Mail in wenigen Minuten.",
            es="Windows 11 Home en licencia digital de por vida más la suscripción de 12 meses a Microsoft 365 Personal: apps Office siempre actualizadas, 1 TB de OneDrive, Copilot IA y entrega por email en minutos.",
            pt="Windows 11 Home em licença digital vitalícia mais a subscrição de 12 meses do Microsoft 365 Personal: apps Office sempre atualizadas, 1 TB OneDrive, Copilot IA e entrega por email em poucos minutos.",
            nl="Windows 11 Home als permanente digitale licentie plus 12 maanden Microsoft 365 Personal: altijd actuele Office-apps, 1 TB OneDrive, Copilot AI en levering per e-mail binnen enkele minuten.",
        ),
        "features_title": L(
            it="Due prodotti Microsoft, un solo acquisto",
            en="Two Microsoft products, one purchase",
            fr="Deux produits Microsoft, un seul achat",
            de="Zwei Microsoft-Produkte, ein Kauf",
            es="Dos productos Microsoft, una sola compra",
            pt="Dois produtos Microsoft, uma só compra",
            nl="Twee Microsoft-producten, één aankoop",
        ),
        "keypoints": L(
            it=["Windows 11 Home, licenza a vita", "M365 Personal, 12 mesi inclusi", "App Office + Copilot integrato", "Due licenze, attivazione guidata"],
            en=["Windows 11 Home, lifetime licence", "M365 Personal, 12 months included", "Office apps + built-in Copilot", "Two licences, guided activation"],
            fr=["Windows 11 Home, licence à vie", "M365 Personal, 12 mois inclus", "Apps Office + Copilot intégré", "Deux licences, activation guidée"],
            de=["Windows 11 Home, Dauerlizenz", "M365 Personal, 12 Monate inklusive", "Office-Apps + integriertes Copilot", "Zwei Lizenzen, geführte Aktivierung"],
            es=["Windows 11 Home, licencia de por vida", "M365 Personal, 12 meses incluidos", "Apps Office + Copilot integrado", "Dos licencias, activación guiada"],
            pt=["Windows 11 Home, licença vitalícia", "M365 Personal, 12 meses incluídos", "Apps Office + Copilot integrado", "Duas licenças, ativação guiada"],
            nl=["Windows 11 Home, permanente licentie", "M365 Personal, 12 maanden inbegrepen", "Office-apps + geïntegreerde Copilot", "Twee licenties, begeleide activering"],
        ),
        "features": {
            "it": [
                ("c6", None, "Sistema operativo", "Windows 11 Home incluso", "Licenza digitale a vita per attivare o aggiornare un PC compatibile: nessuna scadenza, nessun canone per il sistema operativo."),
                ("c6", None, "Produttività", "Microsoft 365 Personal incluso", "Abbonamento di 12 mesi con app Office premium, 1 TB di OneDrive e Copilot AI integrato, secondo i limiti del piano Personal Microsoft."),
                ("c6", None, "Attivazione", "Due licenze indipendenti", "Windows 11 e Microsoft 365 Personal si attivano con due codici distinti, ciascuno sul portale ufficiale previsto da Microsoft."),
                ("c6", None, "Comodità", "Un solo checkout", "Ordini, paghi e ricevi entrambi i codici in un'unica procedura d'acquisto, senza gestire due ordini separati."),
            ],
            "en": [
                ("c6", None, "Operating system", "Windows 11 Home included", "Lifetime digital licence to activate or upgrade a compatible PC: no expiry, no fee for the operating system."),
                ("c6", None, "Productivity", "Microsoft 365 Personal included", "12-month subscription with premium Office apps, 1 TB of OneDrive and built-in Copilot AI, within the limits of the Microsoft Personal plan."),
                ("c6", None, "Activation", "Two independent licences", "Windows 11 and Microsoft 365 Personal are activated with two separate codes, each on Microsoft's official portal."),
                ("c6", None, "Convenience", "A single checkout", "Order, pay and receive both codes in a single purchase flow, without managing two separate orders."),
            ],
            "fr": [
                ("c6", None, "Système d'exploitation", "Windows 11 Home inclus", "Licence numérique à vie pour activer ou mettre à niveau un PC compatible : pas d'expiration, pas d'abonnement pour le système."),
                ("c6", None, "Productivité", "Microsoft 365 Personal inclus", "Abonnement de 12 mois avec applications Office premium, 1 To de OneDrive et Copilot IA intégré, selon les limites du plan Personal Microsoft."),
                ("c6", None, "Activation", "Deux licences indépendantes", "Windows 11 et Microsoft 365 Personal s'activent avec deux codes distincts, chacun sur le portail officiel Microsoft."),
                ("c6", None, "Simplicité", "Un seul paiement", "Commandez, payez et recevez les deux codes en une seule procédure d'achat, sans gérer deux commandes séparées."),
            ],
            "de": [
                ("c6", None, "Betriebssystem", "Windows 11 Home inklusive", "Digitale Dauerlizenz zur Aktivierung oder zum Upgrade eines kompatiblen PCs: kein Ablauf, keine Gebühr für das Betriebssystem."),
                ("c6", None, "Produktivität", "Microsoft 365 Personal inklusive", "12-Monats-Abo mit Premium-Office-Apps, 1 TB OneDrive und integriertem Copilot KI, im Rahmen des Microsoft Personal-Plans."),
                ("c6", None, "Aktivierung", "Zwei unabhängige Lizenzen", "Windows 11 und Microsoft 365 Personal werden mit zwei separaten Codes aktiviert, jeweils im offiziellen Microsoft-Portal."),
                ("c6", None, "Komfort", "Ein einziger Checkout", "Bestellen, bezahlen und beide Codes in einem einzigen Kaufvorgang erhalten, ohne zwei getrennte Bestellungen zu verwalten."),
            ],
            "es": [
                ("c6", None, "Sistema operativo", "Windows 11 Home incluido", "Licencia digital de por vida para activar o actualizar un PC compatible: sin caducidad, sin cuota por el sistema operativo."),
                ("c6", None, "Productividad", "Microsoft 365 Personal incluido", "Suscripción de 12 meses con apps Office premium, 1 TB de OneDrive y Copilot IA integrado, según los límites del plan Personal de Microsoft."),
                ("c6", None, "Activación", "Dos licencias independientes", "Windows 11 y Microsoft 365 Personal se activan con dos códigos distintos, cada uno en el portal oficial de Microsoft."),
                ("c6", None, "Comodidad", "Un solo pago", "Pide, paga y recibe ambos códigos en un único proceso de compra, sin gestionar dos pedidos separados."),
            ],
            "pt": [
                ("c6", None, "Sistema operativo", "Windows 11 Home incluído", "Licença digital vitalícia para ativar ou atualizar um PC compatível: sem prazo de validade, sem mensalidade pelo sistema operativo."),
                ("c6", None, "Produtividade", "Microsoft 365 Personal incluído", "Subscrição de 12 meses com apps Office premium, 1 TB de OneDrive e Copilot IA integrado, de acordo com os limites do plano Personal da Microsoft."),
                ("c6", None, "Ativação", "Duas licenças independentes", "Windows 11 e Microsoft 365 Personal ativam-se com dois códigos distintos, cada um no portal oficial da Microsoft."),
                ("c6", None, "Comodidade", "Um só checkout", "Pedes, pagas e recebes ambos os códigos num único processo de compra, sem gerir dois pedidos separados."),
            ],
        },
        "apps": ["word", "excel", "powerpoint", "outlook", "onedrive", "teams", "defender", "copilot", "onenote", "designer", "clipchamp"],
        "apps_title": L(
            it="La suite Office del pacchetto",
            en="The bundle's Office suite",
            fr="La suite Office du pack",
            de="Die Office-Suite des Pakets",
            es="La suite Office del pack",
            pt="A suite Office do pacote",
            nl="De Office-suite van het pakket",
        ),
        "steps": {
            "it": [
                ("Ordine e pagamento", "Aggiungi il pacchetto al carrello e completa il pagamento sicuro con i metodi disponibili. Ricevi la conferma d'ordine come da condizioni mostrate in checkout."),
                ("Due codici via email", "Ti inviamo il <strong>product key</strong> di Windows 11 Home e il codice Microsoft 365 Personal, con le rispettive istruzioni, di solito entro pochi minuti dall'approvazione del pagamento."),
                ("Attivazione separata", 'Attiva Windows 11 Home durante l\'installazione o dalle impostazioni di sistema, poi riscatta il codice Microsoft 365 su <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com</a> e installa le app da <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.'),
            ],
            "en": [
                ("Order and payment", "Add the bundle to your cart and complete secure checkout with the available methods. You receive an order confirmation as shown at checkout."),
                ("Two codes by email", "We email the <strong>product key</strong> for Windows 11 Home and the Microsoft 365 Personal code, with their instructions, usually within minutes of payment approval."),
                ("Two separate activations", 'Activate Windows 11 Home during setup or from system settings, then redeem the Microsoft 365 code at <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com</a> and install the apps from <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.'),
            ],
            "fr": [
                ("Commande et paiement", "Ajoutez le pack au panier et finalisez le paiement sécurisé avec les méthodes disponibles. Vous recevez une confirmation de commande selon les conditions affichées au paiement."),
                ("Deux codes par e-mail", "Nous vous envoyons le <strong>product key</strong> de Windows 11 Home et le code Microsoft 365 Personal, avec leurs instructions, généralement en quelques minutes après l'approbation du paiement."),
                ("Deux activations séparées", 'Activez Windows 11 Home lors de l\'installation ou depuis les paramètres système, puis utilisez le code Microsoft 365 sur <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com</a> et installez les apps depuis <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.'),
            ],
            "de": [
                ("Bestellung und Zahlung", "Paket in den Warenkorb legen und die sichere Zahlung mit den verfügbaren Methoden abschließen. Sie erhalten eine Bestellbestätigung gemäß den beim Checkout angezeigten Bedingungen."),
                ("Zwei Codes per E-Mail", "Wir senden Ihnen den <strong>Product Key</strong> für Windows 11 Home und den Microsoft-365-Personal-Code mit der jeweiligen Anleitung, meist innerhalb weniger Minuten nach Zahlungsfreigabe."),
                ("Zwei separate Aktivierungen", 'Windows 11 Home während der Installation oder in den Systemeinstellungen aktivieren, dann den Microsoft-365-Code unter <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com</a> einlösen und die Apps über <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a> installieren.'),
            ],
            "es": [
                ("Pedido y pago", "Añade el pack al carrito y completa el pago seguro con los métodos disponibles. Recibes la confirmación del pedido según las condiciones mostradas en el checkout."),
                ("Dos códigos por email", "Te enviamos la <strong>clave de producto</strong> de Windows 11 Home y el código de Microsoft 365 Personal, con sus instrucciones, normalmente en pocos minutos tras la aprobación del pago."),
                ("Doble activación", 'Activa Windows 11 Home durante la instalación o desde la configuración del sistema, luego canjea el código de Microsoft 365 en <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com</a> e instala las apps desde <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.'),
            ],
            "pt": [
                ("Pedido e pagamento", "Adiciona o pacote ao carrinho e conclui o pagamento seguro com os métodos disponíveis. Recebes a confirmação do pedido de acordo com as condições apresentadas no checkout."),
                ("Dois códigos por email", "Enviamos-te a <strong>chave de produto</strong> do Windows 11 Home e o código do Microsoft 365 Personal, com as respetivas instruções, normalmente em poucos minutos após a aprovação do pagamento."),
                ("Ativação separada", 'Ativa o Windows 11 Home durante a instalação ou nas definições do sistema, depois resgata o código do Microsoft 365 em <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com</a> e instala as apps a partir de <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.'),
            ],
        },
        "specs_note": L(
            it="Requisiti hardware minimi per Windows 11 Home da documentazione Microsoft; verifica sempre i valori aggiornati prima dell'installazione.",
            en="Minimum hardware requirements for Windows 11 Home from Microsoft documentation; always check the latest values before installing.",
            fr="Configuration matérielle minimale pour Windows 11 Home d'après la documentation Microsoft ; vérifiez toujours les valeurs à jour avant l'installation.",
            de="Mindest-Hardwareanforderungen für Windows 11 Home laut Microsoft-Dokumentation; prüfen Sie vor der Installation immer die aktuellen Werte.",
            es="Requisitos mínimos de hardware para Windows 11 Home según la documentación de Microsoft; comprueba siempre los valores actualizados antes de instalar.",
            pt="Requisitos mínimos de hardware para o Windows 11 Home segundo a documentação da Microsoft; verifica sempre os valores atualizados antes de instalar.",
            nl="Minimale hardwarevereisten voor Windows 11 Home volgens de Microsoft-documentatie; controleer altijd de actuele waarden vóór de installatie.",
        ),
        "specs": {
            "it": [
                ("Processore", "1 GHz o superiore con 2 o più core (64-bit)."),
                ("RAM", "4 GB o superiore."),
                ("Archiviazione", "64 GB o superiore."),
                ("Sicurezza", "UEFI, compatibile con Secure Boot e <strong>TPM 2.0</strong>."),
            ],
            "en": [
                ("Processor", "1 GHz or faster with 2 or more cores (64-bit)."),
                ("RAM", "4 GB or more."),
                ("Storage", "64 GB or more."),
                ("Security", "UEFI, Secure Boot capable, with <strong>TPM 2.0</strong>."),
            ],
            "fr": [
                ("Processeur", "1 GHz ou plus avec 2 cœurs ou plus (64 bits)."),
                ("RAM", "4 Go ou plus."),
                ("Stockage", "64 Go ou plus."),
                ("Sécurité", "UEFI, compatible Secure Boot, avec <strong>TPM 2.0</strong>."),
            ],
            "de": [
                ("Prozessor", "1 GHz oder schneller mit 2 oder mehr Kernen (64-Bit)."),
                ("RAM", "4 GB oder mehr."),
                ("Speicher", "64 GB oder mehr."),
                ("Sicherheit", "UEFI, Secure-Boot-fähig, mit <strong>TPM 2.0</strong>."),
            ],
            "es": [
                ("Procesador", "1 GHz o superior con 2 o más núcleos (64 bits)."),
                ("RAM", "4 GB o superior."),
                ("Almacenamiento", "64 GB o superior."),
                ("Seguridad", "UEFI, compatible con Secure Boot, con <strong>TPM 2.0</strong>."),
            ],
            "pt": [
                ("Processador", "1 GHz ou superior com 2 ou mais núcleos (64 bits)."),
                ("RAM", "4 GB ou superior."),
                ("Armazenamento", "64 GB ou superior."),
                ("Segurança", "UEFI, compatível com Secure Boot, com <strong>TPM 2.0</strong>."),
            ],
        },
        "faq": {
            "it": [
                ("Cosa comprende esattamente questo pacchetto?", "Il pacchetto include una licenza digitale di Windows 11 Home per l'attivazione del sistema operativo e un abbonamento Microsoft 365 Personal di 12 mesi, con app Office, 1 TB di OneDrive e Copilot integrato secondo l'offerta Microsoft. Ricevi due codici via email, ciascuno con le proprie istruzioni di attivazione."),
                ("Le due licenze si attivano insieme o separatamente?", "Si attivano separatamente: il product key di Windows 11 Home va inserito durante l'installazione del sistema operativo o nelle impostazioni di attivazione; il codice Microsoft 365 Personal si riscatta su setup.office.com con il tuo account Microsoft."),
                ("Il codice Windows 11 Home vale per un'installazione pulita o solo per l'aggiornamento?", "Il product key consente sia un'installazione pulita di Windows 11 sia, se il tuo PC rispetta i requisiti minimi hardware Microsoft, l'aggiornamento da una versione compatibile di Windows 10."),
                ("Microsoft 365 Personal incluso in questo bundle è uguale alla versione singola?", "Sì: stesse condizioni del piano Personal Microsoft, un utente con account Microsoft, app Office premium, 1 TB di OneDrive e Copilot integrato nelle app dove previsto dal piano."),
                ("La licenza Windows 11 e l'abbonamento Microsoft 365 si rinnovano insieme?", "No: la licenza Windows 11 Home è a vita (perpetua) per il dispositivo attivato e non richiede rinnovi. L'abbonamento Microsoft 365 Personal ha invece rinnovo annuale, secondo le condizioni Microsoft mostrate in fase d'ordine."),
            ],
            "en": [
                ("What does this bundle include exactly?", "The bundle includes a Windows 11 Home digital licence to activate the operating system and a 12-month Microsoft 365 Personal subscription, with Office apps, 1 TB of OneDrive and built-in Copilot as per the Microsoft offer. You receive two codes by email, each with its own activation instructions."),
                ("Do the two licences activate together or separately?", "They activate separately: the Windows 11 Home product key is entered during OS installation or in activation settings; the Microsoft 365 Personal code is redeemed at setup.office.com with your Microsoft account."),
                ("Does the Windows 11 Home code work for a clean install or only an upgrade?", "The product key allows both a clean install of Windows 11 and, if your PC meets Microsoft's minimum hardware requirements, an upgrade from a compatible Windows 10 version."),
                ("Is the Microsoft 365 Personal in this bundle the same as the standalone version?", "Yes: the same terms as the Microsoft Personal plan — one user with a Microsoft account, premium Office apps, 1 TB of OneDrive and Copilot built into the apps where the plan provides it."),
                ("Do the Windows 11 licence and the Microsoft 365 subscription renew together?", "No: the Windows 11 Home licence is lifetime (perpetual) for the activated device and needs no renewal. The Microsoft 365 Personal subscription renews annually instead, under the Microsoft terms shown at checkout."),
            ],
            "fr": [
                ("Que comprend exactement ce pack ?", "Le pack comprend une licence numérique Windows 11 Home pour activer le système d'exploitation et un abonnement Microsoft 365 Personal de 12 mois, avec applications Office, 1 To de OneDrive et Copilot intégré selon l'offre Microsoft. Vous recevez deux codes par e-mail, chacun avec ses propres instructions d'activation."),
                ("Les deux licences s'activent-elles ensemble ou séparément ?", "Elles s'activent séparément : le product key Windows 11 Home se saisit lors de l'installation du système ou dans les paramètres d'activation ; le code Microsoft 365 Personal s'utilise sur setup.office.com avec votre compte Microsoft."),
                ("Le code Windows 11 Home vaut-il pour une installation propre ou seulement une mise à niveau ?", "Le product key permet à la fois une installation propre de Windows 11 et, si votre PC respecte la configuration matérielle minimale Microsoft, une mise à niveau depuis une version compatible de Windows 10."),
                ("Le Microsoft 365 Personal inclus dans ce pack est-il identique à la version seule ?", "Oui : mêmes conditions que le plan Personal Microsoft, un utilisateur avec compte Microsoft, applications Office premium, 1 To de OneDrive et Copilot intégré dans les apps prévues par le plan."),
                ("La licence Windows 11 et l'abonnement Microsoft 365 se renouvellent-ils ensemble ?", "Non : la licence Windows 11 Home est à vie (perpétuelle) pour l'appareil activé et ne nécessite aucun renouvellement. L'abonnement Microsoft 365 Personal se renouvelle en revanche chaque année, selon les conditions Microsoft affichées à la commande."),
            ],
            "de": [
                ("Was genau ist in diesem Paket enthalten?", "Das Paket enthält eine digitale Windows-11-Home-Lizenz zur Aktivierung des Betriebssystems sowie ein 12-monatiges Microsoft-365-Personal-Abo mit Office-Apps, 1 TB OneDrive und integriertem Copilot gemäß Microsoft-Angebot. Sie erhalten zwei Codes per E-Mail, jeweils mit eigener Aktivierungsanleitung."),
                ("Werden die beiden Lizenzen zusammen oder getrennt aktiviert?", "Sie werden getrennt aktiviert: Der Windows-11-Home-Product-Key wird bei der Systeminstallation oder in den Aktivierungseinstellungen eingegeben; der Microsoft-365-Personal-Code wird unter setup.office.com mit Ihrem Microsoft-Konto eingelöst."),
                ("Gilt der Windows-11-Home-Code für eine Neuinstallation oder nur für ein Upgrade?", "Der Product Key ermöglicht sowohl eine Neuinstallation von Windows 11 als auch — sofern Ihr PC die Microsoft-Mindestanforderungen erfüllt — ein Upgrade von einer kompatiblen Windows-10-Version."),
                ("Ist das in diesem Paket enthaltene Microsoft 365 Personal identisch mit der Einzelversion?", "Ja: gleiche Bedingungen wie beim Microsoft-Personal-Plan — ein Nutzer mit Microsoft-Konto, Premium-Office-Apps, 1 TB OneDrive und in den Apps integriertes Copilot, soweit im Plan vorgesehen."),
                ("Verlängern sich die Windows-11-Lizenz und das Microsoft-365-Abo gemeinsam?", "Nein: Die Windows-11-Home-Lizenz gilt lebenslang (dauerhaft) für das aktivierte Gerät und erfordert keine Verlängerung. Das Microsoft-365-Personal-Abo verlängert sich hingegen jährlich, gemäß den beim Kauf angezeigten Microsoft-Bedingungen."),
            ],
            "es": [
                ("¿Qué incluye exactamente este pack?", "El pack incluye una licencia digital de Windows 11 Home para activar el sistema operativo y una suscripción de 12 meses a Microsoft 365 Personal, con apps Office, 1 TB de OneDrive y Copilot integrado según la oferta de Microsoft. Recibes dos códigos por email, cada uno con sus propias instrucciones de activación."),
                ("¿Las dos licencias se activan juntas o por separado?", "Se activan por separado: la clave de producto de Windows 11 Home se introduce durante la instalación del sistema o en la configuración de activación; el código de Microsoft 365 Personal se canjea en setup.office.com con tu cuenta Microsoft."),
                ("¿El código de Windows 11 Home sirve para una instalación limpia o solo para actualizar?", "La clave de producto permite tanto una instalación limpia de Windows 11 como, si tu PC cumple los requisitos mínimos de hardware de Microsoft, una actualización desde una versión compatible de Windows 10."),
                ("¿El Microsoft 365 Personal incluido en este pack es igual a la versión individual?", "Sí: mismas condiciones que el plan Personal de Microsoft, un usuario con cuenta Microsoft, apps Office premium, 1 TB de OneDrive y Copilot integrado en las apps donde lo prevea el plan."),
                ("¿La licencia de Windows 11 y la suscripción de Microsoft 365 se renuevan juntas?", "No: la licencia de Windows 11 Home es de por vida (perpetua) para el dispositivo activado y no requiere renovación. La suscripción de Microsoft 365 Personal, en cambio, se renueva anualmente, según las condiciones de Microsoft mostradas al pedir."),
            ],
            "pt": [
                ("O que inclui exatamente este pacote?", "O pacote inclui uma licença digital de Windows 11 Home para ativar o sistema operativo e uma subscrição de 12 meses do Microsoft 365 Personal, com apps Office, 1 TB de OneDrive e Copilot integrado de acordo com a oferta Microsoft. Recebes dois códigos por email, cada um com as suas próprias instruções de ativação."),
                ("As duas licenças ativam-se juntas ou separadamente?", "Ativam-se separadamente: a chave de produto do Windows 11 Home introduz-se durante a instalação do sistema ou nas definições de ativação; o código do Microsoft 365 Personal resgata-se em setup.office.com com a tua conta Microsoft."),
                ("O código do Windows 11 Home serve para uma instalação limpa ou só para atualizar?", "A chave de produto permite tanto uma instalação limpa do Windows 11 como, se o teu PC cumprir os requisitos mínimos de hardware da Microsoft, uma atualização a partir de uma versão compatível do Windows 10."),
                ("O Microsoft 365 Personal incluído neste pacote é igual à versão individual?", "Sim: mesmas condições do plano Personal da Microsoft, um utilizador com conta Microsoft, apps Office premium, 1 TB de OneDrive e Copilot integrado nas apps onde o plano o preveja."),
                ("A licença do Windows 11 e a subscrição do Microsoft 365 renovam-se juntas?", "Não: a licença do Windows 11 Home é vitalícia (perpétua) para o dispositivo ativado e não requer renovação. A subscrição do Microsoft 365 Personal, por sua vez, renova-se anualmente, de acordo com as condições Microsoft mostradas no momento do pedido."),
            ],
        },
    },
}

from lang_backfill import backfill_lang
backfill_lang(PRODUCTS)
backfill_lang(PRODUCTS, target="nl", source="en", translate=nl_text)


def get_bundle_content(slug):
    return PRODUCTS.get(slug)
