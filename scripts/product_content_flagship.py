"""Contenuto ricco per le schede prodotto flagship (M365 Personal/Family, Windows 11 Home).
Rigenerato via pprint — vedi scripts/build-m365-family-content.py per il pattern.
"""

PRODUCTS = {'microsoft-365-personal': {'copilot_bonus': True,
                            'name': {'it': 'Microsoft 365 Personal',
                                     'en': 'Microsoft 365 Personal',
                                     'fr': 'Microsoft 365 Personnel',
                                     'de': 'Microsoft 365 Personal',
                                     'es': 'Microsoft 365 Personal'},
                            'seo_title': {'it': 'Microsoft 365 Personal — Aml Store',
                                          'en': 'Microsoft 365 Personal — Aml Store',
                                          'fr': 'Microsoft 365 Personnel — Aml Store',
                                          'de': 'Microsoft 365 Personal — Aml Store',
                                          'es': 'Microsoft 365 Personal — Aml Store'},
                            'desc': {'it': "L'abbonamento completo per uso personale: app Office "
                                           'premium sempre aggiornate, 1 TB OneDrive dedicato, '
                                           'Copilot AI integrato in tutte le app e consegna del '
                                           'codice via email in 2–15 minuti.',
                                     'en': 'The complete subscription for personal use: premium '
                                           'Office apps always up to date, 1 TB of dedicated '
                                           'OneDrive storage, Copilot AI built into every app, and '
                                           'the code delivered by email in 2-15 minutes.',
                                     'fr': "L'abonnement complet pour un usage personnel : "
                                           'applications Office premium toujours à jour, 1 To de '
                                           'stockage OneDrive dédié, Copilot IA intégré dans '
                                           'toutes les applications, et envoi du code par e-mail '
                                           'en 2 à 15 minutes.',
                                     'de': 'Das komplette Abo für die persönliche Nutzung: stets '
                                           'aktuelle Premium-Office-Apps, 1 TB dedizierter '
                                           'OneDrive-Speicher, in alle Apps integriertes '
                                           'Copilot-KI und Codelieferung per E-Mail innerhalb von '
                                           '2-15 Minuten.',
                                     'es': 'La suscripción completa para uso personal: '
                                           'aplicaciones Office premium siempre actualizadas, 1 TB '
                                           'de almacenamiento OneDrive dedicado, Copilot IA '
                                           'integrado en todas las aplicaciones y entrega del '
                                           'código por email en 2-15 minutos.'},
                            'eyebrow': {'it': 'Abbonamento premium · 12 mesi',
                                        'en': 'Premium subscription · 12 months',
                                        'fr': 'Abonnement premium · 12 mois',
                                        'de': 'Premium-Abo · 12 Monate',
                                        'es': 'Suscripción premium · 12 meses'},
                            'title_html': {'it': 'Microsoft 365 <span>Personal</span>',
                                           'en': 'Microsoft 365 <span>Personal</span>',
                                           'fr': 'Microsoft 365 <span>Personnel</span>',
                                           'de': 'Microsoft 365 <span>Personal</span>',
                                           'es': 'Microsoft 365 <span>Personal</span>'},
                            'features_title': {'it': 'Il tuo spazio di lavoro, sempre con te',
                                               'en': 'Your workspace, everywhere',
                                               'fr': 'Tout ce dont vous avez besoin',
                                               'de': 'Ihr Arbeitsplatz, überall',
                                               'es': 'Todo lo que necesitas'},
                            'apps_title': {'it': 'Piano Microsoft 365 Personal',
                                           'en': 'Microsoft 365 Personal plan',
                                           'fr': 'Plan Microsoft 365 Personnel',
                                           'de': 'Microsoft 365 Personal-Plan',
                                           'es': 'Plan Microsoft 365 Personal'},
                            'pills': {'it': [('teams', '1 utente'),
                                             ('onedrive', '1 TB OneDrive'),
                                             ('copilot', 'Include Copilot'),
                                             ('defender', 'Defender incluso')],
                                      'en': [('teams', '1 user'),
                                             ('onedrive', '1 TB OneDrive'),
                                             ('copilot', 'Includes Copilot'),
                                             ('defender', 'Defender included')],
                                      'fr': [('teams', '1 utilisateur'),
                                             ('onedrive', '1 To OneDrive'),
                                             ('copilot', 'Inclut Copilot'),
                                             ('defender', 'Defender inclus')],
                                      'de': [('teams', '1 Nutzer'),
                                             ('onedrive', '1 TB OneDrive'),
                                             ('copilot', 'Copilot inklusive'),
                                             ('defender', 'Defender inklusive')],
                                      'es': [('teams', '1 usuario'),
                                             ('onedrive', '1 TB OneDrive'),
                                             ('copilot', 'Incluye Copilot'),
                                             ('defender', 'Defender incluido')]},
                            'features': {'it': [('c8',
                                                 'blue',
                                                 'Il tuo account',
                                                 'Un utente, un piano completo',
                                                 'Il piano Personal è per un solo utente: con lo '
                                                 'stesso account Microsoft puoi usare le app '
                                                 'Office fino a 5 dispositivi contemporaneamente '
                                                 '(PC, Mac, tablet e smartphone), oltre al 1 TB '
                                                 'OneDrive incluso, secondo i limiti Microsoft del '
                                                 'piano.'),
                                                ('c4',
                                                 'teal',
                                                 '',
                                                 'Archiviazione cloud',
                                                 'Spazio OneDrive incluso nel piano per documenti, '
                                                 'foto e backup, condivisibile solo nei modi '
                                                 'previsti da Microsoft per Personal.'),
                                                ('c4',
                                                 'purple',
                                                 'Sicurezza',
                                                 'Microsoft Defender incluso',
                                                 'Protezione avanzata sui dispositivi supportati '
                                                 'collegati al tuo account, come da offerta '
                                                 'Microsoft per il piano Personal.'),
                                                ('c4',
                                                 '',
                                                 'Aggiornamenti',
                                                 'App sempre aggiornate',
                                                 'Word, Excel, PowerPoint, Outlook e tutte le '
                                                 'altre ricevono aggiornamenti continui senza '
                                                 'costi extra.'),
                                                ('c4',
                                                 '',
                                                 'AI',
                                                 'Microsoft Copilot',
                                                 'Assistente AI integrato nelle app dove Copilot è '
                                                 'incluso nel piano, per velocizzare documenti, '
                                                 'posta e presentazioni.'),
                                                ('c4',
                                                 'dark',
                                                 'Multi-device',
                                                 'PC, Mac, tablet e smartphone',
                                                 'Le app funzionano su Windows, macOS, iOS e '
                                                 'Android secondo i requisiti Microsoft.')],
                                         'en': [('c8',
                                                 'blue',
                                                 'Your account',
                                                 'One user, full plan',
                                                 'Personal is for one user: sign in with the same '
                                                 'Microsoft account to use the Office apps on up '
                                                 'to five devices at the same time (PC, Mac, '
                                                 'tablet and phone), plus 1 TB OneDrive included, '
                                                 'within Microsoft’s plan limits.'),
                                                ('c4',
                                                 'teal',
                                                 '',
                                                 'Cloud storage',
                                                 'OneDrive space included for documents, photos '
                                                 'and backups, with sharing only as allowed by '
                                                 'Microsoft for Personal.'),
                                                ('c4',
                                                 'purple',
                                                 'Security',
                                                 'Microsoft Defender included',
                                                 'Advanced protection on supported devices signed '
                                                 "in with your account, per Microsoft's Personal "
                                                 'offering.'),
                                                ('c4',
                                                 '',
                                                 'Updates',
                                                 'Apps always up to date',
                                                 'Word, Excel, PowerPoint, Outlook and all the '
                                                 'other apps receive continuous updates at no '
                                                 'extra cost.'),
                                                ('c4',
                                                 '',
                                                 'AI',
                                                 'Microsoft Copilot',
                                                 'AI assistant built into the apps where Copilot '
                                                 'is included in your plan, for faster documents, '
                                                 'email and presentations.'),
                                                ('c4',
                                                 'dark',
                                                 'Multi-device',
                                                 'PC, Mac, tablet and smartphone',
                                                 'The apps work on Windows, macOS, iOS and Android '
                                                 "subject to Microsoft's requirements.")],
                                         'fr': [('c8',
                                                 'blue',
                                                 'Un compte',
                                                 'Pour un seul utilisateur',
                                                 'Personnel concerne un seul utilisateur : avec le '
                                                 'même compte Microsoft, vous utilisez les '
                                                 'applications Office sur jusqu’à cinq appareils '
                                                 'en même temps (PC, Mac, tablette et téléphone), '
                                                 'avec 1 To OneDrive inclus, selon les limites '
                                                 'Microsoft du plan.'),
                                                ('c4',
                                                 'teal',
                                                 '',
                                                 'Stockage OneDrive',
                                                 '1 To de stockage cloud pour sauvegarder '
                                                 'documents, photos et fichiers, selon les '
                                                 'conditions Microsoft.'),
                                                ('c4',
                                                 'purple',
                                                 'Sécurité',
                                                 'Microsoft Defender inclus',
                                                 'Protection sur les appareils pris en charge '
                                                 'connectés à votre compte Microsoft.'),
                                                ('c4',
                                                 '',
                                                 'Mises à jour',
                                                 'Applications toujours à jour',
                                                 'Word, Excel, PowerPoint, Outlook et toutes les '
                                                 'autres applications reçoivent des mises à jour '
                                                 'continues sans frais supplémentaires.'),
                                                ('c4',
                                                 '',
                                                 'IA',
                                                 'Microsoft Copilot',
                                                 'Assistant IA intégré dans les applications pour '
                                                 'améliorer votre productivité.'),
                                                ('c4',
                                                 'dark',
                                                 'Multi-appareils',
                                                 'PC, Mac, tablette et smartphone',
                                                 'Les applications fonctionnent sur Windows, '
                                                 'macOS, iOS et Android selon les exigences de '
                                                 'Microsoft.')],
                                         'de': [('c8',
                                                 'blue',
                                                 'Ihr Konto',
                                                 'Ein Nutzer, voller Plan',
                                                 'Personal ist für einen Nutzer: Mit demselben '
                                                 'Microsoft-Konto nutzen Sie die Office-Apps auf '
                                                 'bis zu fünf Geräten gleichzeitig (PC, Mac, '
                                                 'Tablet und Smartphone), zuzüglich 1 TB OneDrive '
                                                 'laut Plan — innerhalb der von Microsoft '
                                                 'festgelegten Grenzen.'),
                                                ('c4',
                                                 'teal',
                                                 '',
                                                 'Cloud-Speicher',
                                                 'OneDrive-Speicher für Dokumente, Fotos und '
                                                 'Backups, geteilt nur in der für Personal '
                                                 'vorgesehenen Form.'),
                                                ('c4',
                                                 'purple',
                                                 'Sicherheit',
                                                 'Microsoft Defender inklusive',
                                                 'Erweiterter Schutz auf unterstützten Geräten mit '
                                                 'Ihrem Konto, gemäß dem Microsoft-Angebot für '
                                                 'Personal.'),
                                                ('c4',
                                                 '',
                                                 'Updates',
                                                 'Apps immer aktuell',
                                                 'Word, Excel, PowerPoint, Outlook und alle '
                                                 'weiteren Apps erhalten laufende Updates ohne '
                                                 'zusätzliche Kosten.'),
                                                ('c4',
                                                 '',
                                                 'KI',
                                                 'Microsoft Copilot',
                                                 'KI-Assistent in den Apps, wo Copilot im Plan '
                                                 'enthalten ist, für schnellere Dokumente, E-Mails '
                                                 'und Präsentationen.'),
                                                ('c4',
                                                 'dark',
                                                 'Multi-Device',
                                                 'PC, Mac, Tablet und Smartphone',
                                                 'Die Apps laufen auf Windows, macOS, iOS und '
                                                 'Android gemäß den Microsoft-Anforderungen.')],
                                         'es': [('c8',
                                                 'blue',
                                                 'Una cuenta',
                                                 'Un solo usuario',
                                                 'Personal es para un solo usuario: con la misma '
                                                 'cuenta Microsoft puedes usar las apps de Office '
                                                 'en hasta cinco dispositivos a la vez (PC, Mac, '
                                                 'tablet y smartphone), además de 1 TB de OneDrive '
                                                 'incluido, según los límites del plan de '
                                                 'Microsoft.'),
                                                ('c4',
                                                 'teal',
                                                 '',
                                                 'Almacenamiento OneDrive',
                                                 '1 TB de almacenamiento en la nube para '
                                                 'documentos, fotos y archivos, según las '
                                                 'condiciones de Microsoft.'),
                                                ('c4',
                                                 'purple',
                                                 'Seguridad',
                                                 'Microsoft Defender incluido',
                                                 'Protección en los dispositivos compatibles '
                                                 'vinculados a tu cuenta Microsoft.'),
                                                ('c4',
                                                 '',
                                                 'Actualizaciones',
                                                 'Apps siempre actualizadas',
                                                 'Word, Excel, PowerPoint, Outlook y todas las '
                                                 'demás apps reciben actualizaciones continuas sin '
                                                 'coste adicional.'),
                                                ('c4',
                                                 '',
                                                 'IA',
                                                 'Microsoft Copilot',
                                                 'Asistente de IA integrado en las apps para '
                                                 'aumentar tu productividad.'),
                                                ('c4',
                                                 'dark',
                                                 'Multi-dispositivo',
                                                 'PC, Mac, tablet y smartphone',
                                                 'Las apps funcionan en Windows, macOS, iOS y '
                                                 'Android según los requisitos de Microsoft.')]},
                            'steps': {'it': [('Ordine e pagamento',
                                              'Aggiungi il prodotto al carrello e completa il '
                                              'pagamento sicuro con i metodi disponibili. Ricevi '
                                              "la conferma d'ordine come da condizioni mostrate in "
                                              'checkout.'),
                                             ('Consegna digitale',
                                              'Ti inviamo la <strong>product key</strong> e le '
                                              'istruzioni via email, di solito entro pochi minuti '
                                              "dall'approvazione del pagamento."),
                                             ('Attivazione',
                                              'Riscatta il codice su <a '
                                              'href="https://setup.office.com/Home" '
                                              'target="_blank" rel="noopener '
                                              'noreferrer">setup.office.com</a>, associa la '
                                              'licenza al tuo account Microsoft e installa le app '
                                              'da <a href="https://www.office.com" target="_blank" '
                                              'rel="noopener noreferrer">office.com</a>.')],
                                      'en': [('Order and payment',
                                              'Add the product to your cart and complete the '
                                              'secure payment using one of the available methods. '
                                              'You will receive an order confirmation as per the '
                                              'terms shown at checkout.'),
                                             ('Digital delivery',
                                              'We will send you the <strong>product key</strong> '
                                              'and instructions by email, usually within a few '
                                              'minutes of payment approval.'),
                                             ('Activation',
                                              'Redeem the code at <a '
                                              'href="https://setup.office.com/Home" '
                                              'target="_blank" rel="noopener '
                                              'noreferrer">setup.office.com</a>, link the licence '
                                              'to your Microsoft account and install the apps from '
                                              '<a href="https://www.office.com" target="_blank" '
                                              'rel="noopener noreferrer">office.com</a>.')],
                                      'fr': [('Commande et paiement',
                                              'Ajoutez le produit au panier et finalisez le '
                                              "paiement sécurisé avec l'un des modes disponibles. "
                                              'Vous recevrez une confirmation de commande '
                                              'conformément aux conditions affichées lors du '
                                              'paiement.'),
                                             ('Livraison numérique',
                                              'Nous vous envoyons la <strong>clé de '
                                              'produit</strong> et les instructions par e-mail, '
                                              'généralement en quelques minutes après validation '
                                              'du paiement.'),
                                             ('Activation',
                                              'Échangez le code sur <a '
                                              'href="https://setup.office.com/Home" '
                                              'target="_blank" rel="noopener '
                                              'noreferrer">setup.office.com</a>, associez la '
                                              'licence à votre compte Microsoft et installez les '
                                              'applications depuis <a '
                                              'href="https://www.office.com" target="_blank" '
                                              'rel="noopener noreferrer">office.com</a>.')],
                                      'de': [('Bestellung und Zahlung',
                                              'Legen Sie das Produkt in den Warenkorb und '
                                              'schließen Sie die sichere Zahlung mit einer der '
                                              'verfügbaren Methoden ab. Sie erhalten eine '
                                              'Bestellbestätigung gemäß den beim Checkout '
                                              'angezeigten Bedingungen.'),
                                             ('Digitale Lieferung',
                                              'Wir senden Ihnen den <strong>Product Key</strong> '
                                              'und die Anweisungen per E-Mail, in der Regel wenige '
                                              'Minuten nach Zahlungsbestätigung.'),
                                             ('Aktivierung',
                                              'Lösen Sie den Code auf <a '
                                              'href="https://setup.office.com/Home" '
                                              'target="_blank" rel="noopener '
                                              'noreferrer">setup.office.com</a> ein, verknüpfen '
                                              'Sie die Lizenz mit Ihrem Microsoft-Konto und '
                                              'installieren Sie die Apps von <a '
                                              'href="https://www.office.com" target="_blank" '
                                              'rel="noopener noreferrer">office.com</a>.')],
                                      'es': [('Pedido y pago',
                                              'Añade el producto al carrito y completa el pago '
                                              'seguro con uno de los métodos disponibles. '
                                              'Recibirás la confirmación del pedido según las '
                                              'condiciones mostradas en el proceso de compra.'),
                                             ('Entrega digital',
                                              'Te enviamos la <strong>clave de producto</strong> y '
                                              'las instrucciones por email, normalmente en pocos '
                                              'minutos tras la aprobación del pago.'),
                                             ('Activación',
                                              'Canjea el código en <a '
                                              'href="https://setup.office.com/Home" '
                                              'target="_blank" rel="noopener '
                                              'noreferrer">setup.office.com</a>, vincula la '
                                              'licencia a tu cuenta Microsoft e instala las apps '
                                              'desde <a href="https://www.office.com" '
                                              'target="_blank" rel="noopener '
                                              'noreferrer">office.com</a>.')]},
                            'specs': {'it': [('Processore',
                                              'Windows: almeno 1,6 GHz dual‑core. Mac: Intel o '
                                              'Apple Silicon compatibili con macOS supportato.'),
                                             ('Sistema operativo',
                                              'Windows 10/11; ultime tre versioni di macOS; iOS e '
                                              'Android secondo le versioni supportate da '
                                              'Microsoft.'),
                                             ('Memoria (RAM)',
                                              'Almeno 4 GB consigliati per le app desktop; '
                                              'esigenze maggiori per funzioni avanzate o file '
                                              'grandi.'),
                                             ('Spazio su disco',
                                              'Almeno 4 GB liberi (PC) o superiori su Mac, a '
                                              'seconda della suite installata. Controlla la scheda '
                                              'ufficiale Microsoft.')],
                                      'en': [('Processor',
                                              'Windows: at least 1.6 GHz dual-core. Mac: Intel or '
                                              'Apple Silicon compatible with a supported macOS '
                                              'version.'),
                                             ('Operating system',
                                              'Windows 10/11; the latest three versions of macOS; '
                                              "iOS and Android per Microsoft's supported "
                                              'versions.'),
                                             ('Memory (RAM)',
                                              'At least 4 GB recommended for desktop apps; more '
                                              'may be required for advanced features or large '
                                              'files.'),
                                             ('Disk space',
                                              'At least 4 GB free (PC) or more on Mac, depending '
                                              'on the installed suite. Check the official '
                                              'Microsoft page.')],
                                      'fr': [('Processeur',
                                              'Windows : au moins 1,6 GHz double cœur. Mac : Intel '
                                              'ou Apple Silicon compatible avec une version macOS '
                                              'prise en charge.'),
                                             ("Système d'exploitation",
                                              'Windows 10/11 ; les trois dernières versions de '
                                              'macOS ; iOS et Android selon les versions prises en '
                                              'charge par Microsoft.'),
                                             ('Mémoire (RAM)',
                                              'Au moins 4 Go recommandés pour les applications de '
                                              'bureau ; davantage peut être nécessaire pour les '
                                              'fonctions avancées ou les fichiers volumineux.'),
                                             ('Espace disque',
                                              'Au moins 4 Go libres (PC) ou plus sur Mac, selon la '
                                              'suite installée. Consultez la page officielle '
                                              'Microsoft.')],
                                      'de': [('Prozessor',
                                              'Windows: mindestens 1,6 GHz Dual-Core. Mac: Intel '
                                              'oder Apple Silicon, kompatibel mit einer '
                                              'unterstützten macOS-Version.'),
                                             ('Betriebssystem',
                                              'Windows 10/11; die letzten drei macOS-Versionen; '
                                              'iOS und Android gemäß den von Microsoft '
                                              'unterstützten Versionen.'),
                                             ('Arbeitsspeicher (RAM)',
                                              'Mindestens 4 GB empfohlen für Desktop-Apps; für '
                                              'erweiterte Funktionen oder große Dateien kann mehr '
                                              'benötigt werden.'),
                                             ('Speicherplatz',
                                              'Mindestens 4 GB frei (PC) oder mehr auf Mac, je '
                                              'nach installierter Suite. Offizielle '
                                              'Microsoft-Seite beachten.')],
                                      'es': [('Procesador',
                                              'Windows: al menos 1,6 GHz de doble núcleo. Mac: '
                                              'Intel o Apple Silicon compatible con una versión de '
                                              'macOS admitida.'),
                                             ('Sistema operativo',
                                              'Windows 10/11; las tres últimas versiones de macOS; '
                                              'iOS y Android según las versiones compatibles con '
                                              'Microsoft.'),
                                             ('Memoria (RAM)',
                                              'Al menos 4 GB recomendados para las apps de '
                                              'escritorio; puede ser necesario más para funciones '
                                              'avanzadas o archivos de gran tamaño.'),
                                             ('Espacio en disco',
                                              'Al menos 4 GB libres (PC) o más en Mac, según la '
                                              'suite instalada. Consulta la página oficial de '
                                              'Microsoft.')]},
                            'specs_note': {'it': 'Valori orientativi da documentazione Microsoft; '
                                                 'verifica sempre i requisiti aggiornati prima '
                                                 "dell'installazione.",
                                           'en': 'Indicative values from Microsoft documentation; '
                                                 'always check the updated requirements before '
                                                 'installation.',
                                           'fr': 'Valeurs indicatives issues de la documentation '
                                                 'Microsoft ; vérifiez toujours les prérequis à '
                                                 "jour avant l'installation.",
                                           'de': 'Richtwerte aus der Microsoft-Dokumentation; '
                                                 'prüfen Sie stets die aktuellen Anforderungen vor '
                                                 'der Installation.',
                                           'es': 'Valores orientativos de la documentación de '
                                                 'Microsoft; comprueba siempre los requisitos '
                                                 'actualizados antes de la instalación.'},
                            'faq': {'it': [('Per chi è pensato Microsoft 365 Personal?',
                                            'Personal copre un solo utente con account Microsoft, '
                                            'app Office premium e 1 TB di OneDrive, secondo le '
                                            'condizioni Microsoft. Per condividere con più persone '
                                            'con account separati, valuta Microsoft 365 Family.'),
                                           ('Posso usare Personal su più dispositivi?',
                                            'Sì, entro i limiti del piano Microsoft: installa le '
                                            'app su PC, Mac, tablet e smartphone supportati '
                                            'collegati al tuo account, come descritto nella '
                                            'documentazione ufficiale.'),
                                           ('È un abbonamento o un acquisto una tantum?',
                                            'È un abbonamento con rinnovo annuale (12 mesi '
                                            'acquistati su questa scheda). Durata, rinnovo e '
                                            'prezzo al rinnovo dipendono da Microsoft e dalle '
                                            "condizioni mostrate in fase d'ordine."),
                                           ('Si possono usare le app Office anche offline?',
                                            'Sì: con le app desktop installate puoi lavorare '
                                            'offline; servono comunque connessione e accesso '
                                            'periodici per la verifica della licenza, '
                                            'aggiornamenti e servizi cloud come OneDrive.'),
                                           ('Come si attiva Microsoft 365 Personal dopo '
                                            "l'acquisto?",
                                            'Vai su <a href="https://setup.office.com/Home" '
                                            'target="_blank" rel="noopener '
                                            'noreferrer">setup.office.com/Home</a>, accedi con il '
                                            'tuo account Microsoft, inserisci il codice ricevuto '
                                            'via email e segui la procedura guidata. Al termine '
                                            'installa le app da <a href="https://www.office.com" '
                                            'target="_blank" rel="noopener '
                                            'noreferrer">office.com</a>.')],
                                    'en': [('Who is Microsoft 365 Personal for?',
                                            'Personal covers one Microsoft account with premium '
                                            "Office apps and 1 TB OneDrive, subject to Microsoft's "
                                            'terms. To share with several people on separate '
                                            'accounts, consider Microsoft 365 Family.'),
                                           ('Can I use Personal on more than one device?',
                                            'Yes, within the limits of the Microsoft plan: install '
                                            'the apps on supported PCs, Macs, tablets and '
                                            'smartphones signed in with your account, as described '
                                            "in Microsoft's documentation."),
                                           ('Is this a subscription or a one-time purchase?',
                                            'It is a subscription with annual renewal (12 months '
                                            'purchased on this page). Duration, renewal, and '
                                            'renewal price depend on Microsoft and the terms shown '
                                            'at checkout.'),
                                           ('Can I use Office apps offline?',
                                            'Yes: with the desktop apps installed you can work '
                                            'offline; however, periodic internet connection and '
                                            'sign-in are required for licence verification, '
                                            'updates, and cloud services such as OneDrive.'),
                                           ('How do I activate Microsoft 365 Personal after '
                                            'purchase?',
                                            'Go to <a href="https://setup.office.com/Home" '
                                            'target="_blank" rel="noopener '
                                            'noreferrer">setup.office.com/Home</a>, sign in with '
                                            'your Microsoft account, enter the code received by '
                                            'email and follow the guided setup. Once done, install '
                                            'the apps from <a href="https://www.office.com" '
                                            'target="_blank" rel="noopener '
                                            'noreferrer">office.com</a>.')],
                                    'fr': [("À qui s'adresse Microsoft 365 Personnel ?",
                                            'Personnel couvre un compte Microsoft avec les '
                                            'applications Office premium et 1 To OneDrive, selon '
                                            'les conditions Microsoft. Pour partager avec '
                                            'plusieurs personnes sur des comptes distincts, '
                                            'choisissez Microsoft 365 Famille.'),
                                           ('Puis-je utiliser Personnel sur plusieurs appareils ?',
                                            'Oui, dans les limites du plan Microsoft : installez '
                                            'les applications sur les PC, Mac, tablettes et '
                                            'smartphones pris en charge connectés à votre compte, '
                                            'comme décrit dans la documentation Microsoft.'),
                                           ("S'agit-il d'un abonnement ou d'un achat unique ?",
                                            "Il s'agit d'un abonnement avec renouvellement annuel "
                                            '(12 mois achetés sur cette page). La durée, le '
                                            'renouvellement et le prix de renouvellement dépendent '
                                            'de Microsoft et des conditions affichées lors de la '
                                            'commande.'),
                                           ('Peut-on utiliser les applications Office hors '
                                            'connexion ?',
                                            'Oui : avec les applications de bureau installées, '
                                            'vous pouvez travailler hors ligne ; une connexion '
                                            'internet et une authentification périodiques sont '
                                            'toutefois nécessaires pour la vérification de la '
                                            'licence, les mises à jour et les services cloud comme '
                                            'OneDrive.'),
                                           ("Comment activer Microsoft 365 Personnel après l'achat "
                                            '?',
                                            'Rendez-vous sur <a '
                                            'href="https://setup.office.com/Home" target="_blank" '
                                            'rel="noopener noreferrer">setup.office.com/Home</a>, '
                                            'connectez-vous avec votre compte Microsoft, saisissez '
                                            "le code reçu par e-mail et suivez l'assistant "
                                            "d'installation. Une fois terminé, installez les "
                                            'applications depuis <a href="https://www.office.com" '
                                            'target="_blank" rel="noopener '
                                            'noreferrer">office.com</a>.')],
                                    'de': [('Für wen ist Microsoft 365 Personal gedacht?',
                                            'Personal gilt für ein Microsoft-Konto mit '
                                            'Premium-Office-Apps und 1 TB OneDrive, gemäß den '
                                            'Microsoft-Bedingungen. Zum Teilen mit mehreren '
                                            'Personen auf separaten Konten eignet sich Microsoft '
                                            '365 Family.'),
                                           ('Kann ich Personal auf mehreren Geräten nutzen?',
                                            'Ja, innerhalb der Grenzen des Microsoft-Plans: '
                                            'Installieren Sie die Apps auf unterstützten PCs, '
                                            'Macs, Tablets und Smartphones mit Ihrem Konto, wie in '
                                            'der Microsoft-Dokumentation beschrieben.'),
                                           ('Ist das ein Abonnement oder ein einmaliger Kauf?',
                                            'Es handelt sich um ein Abonnement mit jährlicher '
                                            'Verlängerung (12 Monate, die auf dieser Seite gekauft '
                                            'werden). Laufzeit, Verlängerung und '
                                            'Verlängerungspreis richten sich nach Microsoft und '
                                            'den beim Bestellvorgang angezeigten Bedingungen.'),
                                           ('Kann ich Office-Apps auch offline nutzen?',
                                            'Ja: Mit den installierten Desktop-Apps können Sie '
                                            'offline arbeiten; für die Lizenzprüfung, Updates und '
                                            'Cloud-Dienste wie OneDrive ist jedoch eine '
                                            'gelegentliche Internetverbindung und Anmeldung '
                                            'erforderlich.'),
                                           ('Wie aktiviere ich Microsoft 365 Personal nach dem '
                                            'Kauf?',
                                            'Rufen Sie <a href="https://setup.office.com/Home" '
                                            'target="_blank" rel="noopener '
                                            'noreferrer">setup.office.com/Home</a> auf, melden Sie '
                                            'sich mit Ihrem Microsoft-Konto an, geben Sie den per '
                                            'E-Mail erhaltenen Code ein und folgen Sie dem '
                                            'Einrichtungsassistenten. Installieren Sie '
                                            'anschließend die Apps von <a '
                                            'href="https://www.office.com" target="_blank" '
                                            'rel="noopener noreferrer">office.com</a>.')],
                                    'es': [('¿Para quién es Microsoft 365 Personal?',
                                            'Personal cubre una cuenta Microsoft con apps Office '
                                            'premium y 1 TB en OneDrive, según las condiciones de '
                                            'Microsoft. Para compartir con varias personas en '
                                            'cuentas distintas, elige Microsoft 365 Familia.'),
                                           ('¿Puedo usar Personal en varios dispositivos?',
                                            'Sí, dentro de los límites del plan Microsoft: instala '
                                            'las apps en los PC, Mac, tabletas y smartphones '
                                            'compatibles vinculados a tu cuenta, como se describe '
                                            'en la documentación oficial.'),
                                           ('¿Es una suscripción o una compra única?',
                                            'Es una suscripción con renovación anual (12 meses '
                                            'comprados en esta página). La duración, la renovación '
                                            'y el precio de renovación dependen de Microsoft y de '
                                            'las condiciones mostradas en el proceso de compra.'),
                                           ('¿Se pueden usar las apps de Office sin conexión?',
                                            'Sí: con las aplicaciones de escritorio instaladas '
                                            'puedes trabajar sin conexión; sin embargo, se '
                                            'requiere conexión a internet e inicio de sesión '
                                            'periódicos para la verificación de la licencia, las '
                                            'actualizaciones y los servicios en la nube como '
                                            'OneDrive.'),
                                           ('¿Cómo activo Microsoft 365 Personal después de la '
                                            'compra?',
                                            'Ve a <a href="https://setup.office.com/Home" '
                                            'target="_blank" rel="noopener '
                                            'noreferrer">setup.office.com/Home</a>, inicia sesión '
                                            'con tu cuenta Microsoft, introduce el código recibido '
                                            'por email y sigue el asistente de configuración. Una '
                                            'vez finalizado, instala las apps desde <a '
                                            'href="https://www.office.com" target="_blank" '
                                            'rel="noopener noreferrer">office.com</a>.')]},
                            'apps': ['word',
                                     'excel',
                                     'powerpoint',
                                     'outlook',
                                     'onedrive',
                                     'teams',
                                     'defender',
                                     'copilot',
                                     'onenote',
                                     'designer',
                                     'clipchamp'],
                            'keypoints': {'it': ['<strong>Usa su 5 Dispositivi:</strong> PC, Mac, '
                                                 'iPad, iPhone e Android in contemporanea.',
                                                 '<strong>1.000 GB Cloud:</strong> Salva foto e '
                                                 'file senza occupare spazio sul dispositivo.',
                                                 '<strong>Sempre Aggiornato:</strong> Ricevi '
                                                 'sempre le ultimissime funzionalità senza costi '
                                                 'aggiuntivi.',
                                                 '<strong>Nessun Rinnovo Automatico:</strong> '
                                                 "Decidi tu in totale libertà se rinnovare l'anno "
                                                 'prossimo.']},
                            'lifestyle': {'image': 'microsoft-365-personal-lifestyle.webp',
                                          'image_640': 'microsoft-365-personal-lifestyle-640.webp',
                                          'width': 1024,
                                          'height': 640,
                                          'alt': {'it': 'Donna sorridente al lavoro con il laptop '
                                                        'in un angolo studio a casa.',
                                                  'en': 'Smiling woman working on her laptop at a '
                                                        'home desk.',
                                                  'fr': 'Femme souriante travaillant sur son '
                                                        'ordinateur portable à un bureau à '
                                                        'domicile.',
                                                  'de': 'Lächelnde Frau arbeitet am Laptop an '
                                                        'einem Schreibtisch zu Hause.',
                                                  'es': 'Mujer sonriente trabajando con su '
                                                        'portátil en un escritorio en casa.'},
                                          'kicker': {'it': 'Smart Working & Studio',
                                                     'en': 'Smart Working & Study',
                                                     'fr': 'Télétravail & Études',
                                                     'de': 'Homeoffice & Studium',
                                                     'es': 'Teletrabajo y Estudio'},
                                          'title': {'it': 'Lavora e studia ovunque, tutto '
                                                          'sincronizzato',
                                                    'en': 'Work and study anywhere, everything in '
                                                          'sync',
                                                    'fr': 'Travaillez et étudiez partout, tout '
                                                          'synchronisé',
                                                    'de': 'Arbeiten und lernen überall, alles '
                                                          'synchron',
                                                    'es': 'Trabaja y estudia donde quieras, todo '
                                                          'sincronizado'},
                                          'body': {'it': 'La libertà di lavorare, studiare e '
                                                         'creare da qualsiasi stanza di casa, con '
                                                         'i tuoi file sempre sincronizzati su '
                                                         'OneDrive.',
                                                   'en': 'The freedom to work, study and create '
                                                         'from anywhere at home, with your files '
                                                         'always in sync on OneDrive.',
                                                   'fr': 'La liberté de travailler, étudier et '
                                                         "créer depuis n'importe quelle pièce, "
                                                         'avec vos fichiers toujours synchronisés '
                                                         'sur OneDrive.',
                                                   'de': 'Die Freiheit, von jedem Zimmer aus zu '
                                                         'arbeiten, zu lernen und zu gestalten – '
                                                         'deine Dateien immer synchron auf '
                                                         'OneDrive.',
                                                   'es': 'La libertad de trabajar, estudiar y '
                                                         'crear desde cualquier rincón de casa, '
                                                         'con tus archivos siempre sincronizados '
                                                         'en OneDrive.'}},
                            'app_tabs_featured': ['word',
                                                  'excel',
                                                  'powerpoint',
                                                  'outlook',
                                                  'copilot',
                                                  'onedrive'],
                            'app_demo_rich': {'word': {'type': 'richtext',
                                                       'filename': {'it': 'Lettera_e_Curriculum_2026.docx',
                                                                    'en': 'Cover_Letter_and_Resume_2026.docx',
                                                                    'fr': 'Lettre_de_motivation_et_CV_2026.docx',
                                                                    'de': 'Anschreiben_und_Lebenslauf_2026.docx',
                                                                    'es': 'Carta_de_presentacion_y_CV_2026.docx'},
                                                       'tag': {'it': '✨ Copilot AI Attivo',
                                                               'en': '✨ Copilot AI Active',
                                                               'fr': '✨ Copilot IA actif',
                                                               'de': '✨ Copilot KI aktiv',
                                                               'es': '✨ Copilot IA activo'},
                                                       'quote': {'it': 'Crea documenti di testo '
                                                                       'impeccabili, tesine, '
                                                                       'relazioni e lettere di '
                                                                       'presentazione con la '
                                                                       'correzione automatica e il '
                                                                       'supporto della scrittura '
                                                                       'guidata.',
                                                                 'en': 'Create flawless documents, '
                                                                       'essays, reports and cover '
                                                                       'letters with automatic '
                                                                       'proofreading and guided '
                                                                       'writing support.',
                                                                 'fr': 'Créez des documents '
                                                                       'impeccables, '
                                                                       'dissertations, rapports et '
                                                                       'lettres de motivation avec '
                                                                       'correction automatique et '
                                                                       'aide à la rédaction '
                                                                       'guidée.',
                                                                 'de': 'Erstelle einwandfreie '
                                                                       'Dokumente, Hausarbeiten, '
                                                                       'Berichte und Anschreiben '
                                                                       'mit automatischer '
                                                                       'Rechtschreibprüfung und '
                                                                       'geführter '
                                                                       'Schreibunterstützung.',
                                                                 'es': 'Crea documentos '
                                                                       'impecables, trabajos, '
                                                                       'informes y cartas de '
                                                                       'presentación con '
                                                                       'corrección automática y '
                                                                       'ayuda de escritura '
                                                                       'guiada.'},
                                                       'callout_label': {'it': 'Suggerimento '
                                                                               'Copilot:',
                                                                         'en': 'Copilot '
                                                                               'suggestion:',
                                                                         'fr': 'Suggestion Copilot '
                                                                               ':',
                                                                         'de': 'Copilot-Vorschlag:',
                                                                         'es': 'Sugerencia de '
                                                                               'Copilot:'},
                                                       'callout_text': {'it': 'Ho rivisto il testo '
                                                                              'rendendolo più '
                                                                              'fluido, chiaro e '
                                                                              'privo di errori di '
                                                                              'battitura.',
                                                                        'en': "I've revised the "
                                                                              'text to make it '
                                                                              'smoother, clearer '
                                                                              'and free of typos.',
                                                                        'fr': "J'ai révisé le "
                                                                              'texte pour le '
                                                                              'rendre plus fluide, '
                                                                              'plus clair et sans '
                                                                              'fautes de frappe.',
                                                                        'de': 'Ich habe den Text '
                                                                              'überarbeitet, damit '
                                                                              'er flüssiger, '
                                                                              'klarer und frei von '
                                                                              'Tippfehlern ist.',
                                                                        'es': 'He revisado el '
                                                                              'texto para hacerlo '
                                                                              'más fluido, claro y '
                                                                              'sin errores '
                                                                              'tipográficos.'}},
                                              'excel': {'type': 'stats',
                                                        'filename': {'it': 'Bilancio_Familiare_Spese.xlsx',
                                                                     'en': 'Household_Budget.xlsx',
                                                                     'fr': 'Budget_Familial.xlsx',
                                                                     'de': 'Haushaltsbudget.xlsx',
                                                                     'es': 'Presupuesto_Familiar.xlsx'},
                                                        'tag': {'it': 'Controllo Automatico',
                                                                'en': 'Automatic Tracking',
                                                                'fr': 'Suivi automatique',
                                                                'de': 'Automatische Kontrolle',
                                                                'es': 'Control automático'},
                                                        'stats': {'it': [('Casa & Utenze',
                                                                          '€ 420,00',
                                                                          False),
                                                                         ('Spesa & Cibo',
                                                                          '€ 310,00',
                                                                          False),
                                                                         ('Risparmio Mese',
                                                                          '€ 280,00',
                                                                          True)],
                                                                  'en': [('Home & Utilities',
                                                                          '€ 420.00',
                                                                          False),
                                                                         ('Groceries & Food',
                                                                          '€ 310.00',
                                                                          False),
                                                                         ('Monthly Savings',
                                                                          '€ 280.00',
                                                                          True)],
                                                                  'fr': [('Maison & Charges',
                                                                          '420,00 €',
                                                                          False),
                                                                         ('Courses & Alimentation',
                                                                          '310,00 €',
                                                                          False),
                                                                         ('Économies du mois',
                                                                          '280,00 €',
                                                                          True)],
                                                                  'de': [('Wohnen & Nebenkosten',
                                                                          '420,00 €',
                                                                          False),
                                                                         ('Einkauf & Lebensmittel',
                                                                          '310,00 €',
                                                                          False),
                                                                         ('Monatliche Ersparnis',
                                                                          '280,00 €',
                                                                          True)],
                                                                  'es': [('Casa y suministros',
                                                                          '420,00 €',
                                                                          False),
                                                                         ('Compra y comida',
                                                                          '310,00 €',
                                                                          False),
                                                                         ('Ahorro del mes',
                                                                          '280,00 €',
                                                                          True)]}},
                                              'powerpoint': {'type': 'slide',
                                                             'filename': {'it': 'Presentazione_Progetto_Esame.pptx',
                                                                          'en': 'Exam_Project_Presentation.pptx',
                                                                          'fr': 'Presentation_Projet_Examen.pptx',
                                                                          'de': 'Praesentation_Pruefungsprojekt.pptx',
                                                                          'es': 'Presentacion_Proyecto_Examen.pptx'},
                                                             'tag': {'it': 'Designer Automatico',
                                                                     'en': 'Automatic Designer',
                                                                     'fr': 'Concepteur automatique',
                                                                     'de': 'Automatisches Design',
                                                                     'es': 'Diseñador automático'},
                                                             'slide_num': {'it': 'Slide 01',
                                                                           'en': 'Slide 01',
                                                                           'fr': 'Diapositive 01',
                                                                           'de': 'Folie 01',
                                                                           'es': 'Diapositiva 01'},
                                                             'slide_title': {'it': 'Vacanze e '
                                                                                   'Itinerario '
                                                                                   '2026',
                                                                             'en': '2026 Holiday '
                                                                                   'Itinerary',
                                                                             'fr': 'Itinéraire '
                                                                                   'vacances 2026',
                                                                             'de': 'Urlaub und '
                                                                                   'Reiseplan 2026',
                                                                             'es': 'Itinerario de '
                                                                                   'vacaciones '
                                                                                   '2026'},
                                                             'slide_desc': {'it': 'Layout, colori '
                                                                                  'e immagini '
                                                                                  'impaginati '
                                                                                  'automaticamente '
                                                                                  'con un solo '
                                                                                  'click.',
                                                                            'en': 'Layout, colors '
                                                                                  'and images '
                                                                                  'arranged '
                                                                                  'automatically '
                                                                                  'with a single '
                                                                                  'click.',
                                                                            'fr': 'Mise en page, '
                                                                                  'couleurs et '
                                                                                  'images '
                                                                                  'organisées '
                                                                                  'automatiquement '
                                                                                  'en un clic.',
                                                                            'de': 'Layout, Farben '
                                                                                  'und Bilder '
                                                                                  'automatisch mit '
                                                                                  'einem Klick '
                                                                                  'angeordnet.',
                                                                            'es': 'Diseño, colores '
                                                                                  'e imágenes '
                                                                                  'organizados '
                                                                                  'automáticamente '
                                                                                  'con un solo '
                                                                                  'clic.'}},
                                              'onedrive': {'type': 'cloud',
                                                           'filename': {'it': 'Cassaforte Foto e '
                                                                              'Documenti',
                                                                        'en': 'Photo & Document '
                                                                              'Vault',
                                                                        'fr': 'Coffre-fort Photos '
                                                                              'et Documents',
                                                                        'de': 'Foto- und '
                                                                              'Dokumententresor',
                                                                        'es': 'Caja fuerte de '
                                                                              'fotos y documentos'},
                                                           'tag': {'it': '1 TB Cloud Protetto',
                                                                   'en': '1 TB Protected Cloud',
                                                                   'fr': '1 To Cloud protégé',
                                                                   'de': '1 TB geschützte Cloud',
                                                                   'es': '1 TB en la nube '
                                                                         'protegido'},
                                                           'used_label': {'it': 'Foto e Video di '
                                                                                'Famiglia: 342 GB '
                                                                                'usati',
                                                                          'en': 'Family Photos & '
                                                                                'Videos: 342 GB '
                                                                                'used',
                                                                          'fr': 'Photos et vidéos '
                                                                                'de famille : 342 '
                                                                                'Go utilisés',
                                                                          'de': 'Familienfotos und '
                                                                                '-videos: 342 GB '
                                                                                'genutzt',
                                                                          'es': 'Fotos y vídeos '
                                                                                'familiares: 342 '
                                                                                'GB usados'},
                                                           'free_label': {'it': '658 GB liberi',
                                                                          'en': '658 GB free',
                                                                          'fr': '658 Go libres',
                                                                          'de': '658 GB frei',
                                                                          'es': '658 GB libres'},
                                                           'percent': 34},
                                              'outlook': {'type': 'simple',
                                                          'text': {'it': 'Posta, calendario e '
                                                                         "contatti in un'unica "
                                                                         'applicazione, '
                                                                         'sincronizzati con il tuo '
                                                                         'account Microsoft.',
                                                                   'en': 'Mail, calendar and '
                                                                         'contacts in one app, '
                                                                         'synced with your '
                                                                         'Microsoft account.',
                                                                   'fr': 'Messagerie, calendrier '
                                                                         'et contacts dans une '
                                                                         'seule application, '
                                                                         'synchronisés avec votre '
                                                                         'compte Microsoft.',
                                                                   'de': 'E-Mail, Kalender und '
                                                                         'Kontakte in einer App, '
                                                                         'synchronisiert mit '
                                                                         'deinem Microsoft-Konto.',
                                                                   'es': 'Correo, calendario y '
                                                                         'contactos en una sola '
                                                                         'aplicación, '
                                                                         'sincronizados con tu '
                                                                         'cuenta de Microsoft.'}},
                                              'copilot': {'type': 'simple',
                                                          'text': {'it': 'Assistente IA integrato '
                                                                         'in Word, Excel e '
                                                                         'PowerPoint per scrivere, '
                                                                         'calcolare e progettare '
                                                                         'più velocemente.',
                                                                   'en': 'AI assistant built into '
                                                                         'Word, Excel and '
                                                                         'PowerPoint to write, '
                                                                         'calculate and design '
                                                                         'faster.',
                                                                   'fr': 'Assistant IA intégré à '
                                                                         'Word, Excel et '
                                                                         'PowerPoint pour écrire, '
                                                                         'calculer et concevoir '
                                                                         'plus vite.',
                                                                   'de': 'KI-Assistent in Word, '
                                                                         'Excel und PowerPoint '
                                                                         'integriert, um schneller '
                                                                         'zu schreiben, zu rechnen '
                                                                         'und zu gestalten.',
                                                                   'es': 'Asistente de IA '
                                                                         'integrado en Word, Excel '
                                                                         'y PowerPoint para '
                                                                         'escribir, calcular y '
                                                                         'diseñar más rápido.'}}}},
 'windows-11-home': {'name': {'it': 'Windows 11 Home',
                              'en': 'Windows 11 Home',
                              'fr': 'Windows 11 Home',
                              'de': 'Windows 11 Home',
                              'es': 'Windows 11 Home'},
                     'seo_title': {'it': 'Windows 11 Home — Aml Store',
                                   'en': 'Windows 11 Home — Aml Store',
                                   'fr': 'Windows 11 Home — Aml Store',
                                   'de': 'Windows 11 Home — Aml Store',
                                   'es': 'Windows 11 Home — Aml Store'},
                     'desc': {'it': 'Porta la tua esperienza digitale al livello successivo con '
                                    "Windows 11 Home. L'equilibrio perfetto tra produttività "
                                    "basata sull'IA e prestazioni gaming senza compromessi.",
                              'en': 'Take your digital experience to the next level with Windows '
                                    '11 Home. The perfect balance between AI-driven productivity '
                                    'and uncompromising gaming performance.',
                              'fr': 'Faites passer votre expérience numérique au niveau supérieur '
                                    "avec Windows 11 Famille. L'équilibre parfait entre "
                                    "productivité basée sur l'IA et performances de jeu sans "
                                    'compromis.',
                              'de': 'Bringen Sie Ihr digitales Erlebnis mit Windows 11 Home auf '
                                    'die nächste Stufe. Die perfekte Balance zwischen '
                                    'KI-gestützter Produktivität und kompromissloser '
                                    'Gaming-Leistung.',
                              'es': 'Lleva tu experiencia digital al siguiente nivel con Windows '
                                    '11 Home. El equilibrio perfecto entre productividad basada en '
                                    'IA y un rendimiento de juego sin concesiones.'},
                     'eyebrow': {'it': 'Sistema Operativo',
                                 'en': 'Operating system',
                                 'fr': "Système d'exploitation",
                                 'de': 'Betriebssystem',
                                 'es': 'Sistema operativo'},
                     'title_html': {'it': 'Windows 11 <span>Home</span>',
                                    'en': 'Windows 11 <span>Home</span>',
                                    'fr': 'Windows 11 <span>Home</span>',
                                    'de': 'Windows 11 <span>Home</span>',
                                    'es': 'Windows 11 <span>Home</span>'},
                     'features_title': {'it': None, 'en': None, 'fr': None, 'de': None, 'es': None},
                     'apps_title': {'it': None, 'en': None, 'fr': None, 'de': None, 'es': None},
                     'pills': {'it': [(None, 'Layout Snap'),
                                      (None, 'Sicurezza integrata'),
                                      (None, 'Windows Defender')],
                               'en': [(None, 'Snap layouts'),
                                      (None, 'Built-in security'),
                                      (None, 'Windows Defender')],
                               'fr': [(None, 'Mise en page Snap'),
                                      (None, 'Sécurité intégrée'),
                                      (None, 'Windows Defender')],
                               'de': [(None, 'Snap-Layouts'),
                                      (None, 'Integrierte Sicherheit'),
                                      (None, 'Windows Defender')],
                               'es': [(None, 'Diseños Snap'),
                                      (None, 'Seguridad integrada'),
                                      (None, 'Windows Defender')]},
                     'features': {'it': [('c6',
                                          '',
                                          '',
                                          'Copilot Integrato',
                                          "L'intelligenza artificiale al tuo servizio per "
                                          'semplificare ogni task quotidiano.'),
                                         ('c6',
                                          '',
                                          '',
                                          'Gaming HDR',
                                          'Colori più vividi e caricamenti istantanei per '
                                          "un'esperienza di gioco immersiva."),
                                         ('c6',
                                          '',
                                          '',
                                          'Sicurezza Massima',
                                          'Protezione firewall e internet contro le minacce '
                                          'informatiche più recenti.'),
                                         ('c6',
                                          '',
                                          '',
                                          'Multitasking Snap',
                                          'Organizza il desktop con layout intelligenti per '
                                          'lavorare meglio e più velocemente.')],
                                  'en': [('c6',
                                          '',
                                          '',
                                          'Built-in Copilot',
                                          'AI at your service to simplify everyday tasks.'),
                                         ('c6',
                                          '',
                                          '',
                                          'HDR gaming',
                                          'Richer colours and fast loading for an immersive gaming '
                                          'experience.'),
                                         ('c6',
                                          '',
                                          '',
                                          'Maximum security',
                                          'Firewall and internet protection against the latest '
                                          'threats.'),
                                         ('c6',
                                          '',
                                          '',
                                          'Snap multitasking',
                                          'Organise your desktop with smart layouts to work faster '
                                          'and better.')],
                                  'fr': [('c6',
                                          '',
                                          '',
                                          'Copilot intégré',
                                          "L'intelligence artificielle à votre service pour "
                                          'simplifier chaque tâche quotidienne.'),
                                         ('c6',
                                          '',
                                          '',
                                          'Jeu HDR',
                                          'Des couleurs plus vives et des chargements rapides pour '
                                          'une expérience de jeu immersive.'),
                                         ('c6',
                                          '',
                                          '',
                                          'Sécurité maximale',
                                          'Pare-feu et protection Internet contre les menaces les '
                                          'plus récentes.'),
                                         ('c6',
                                          '',
                                          '',
                                          'Multitâche Snap',
                                          'Organisez le bureau avec des mises en page '
                                          'intelligentes pour travailler mieux et plus vite.')],
                                  'de': [('c6',
                                          '',
                                          '',
                                          'Integriertes Copilot',
                                          'KI an Ihrer Seite, um alltägliche Aufgaben zu '
                                          'vereinfachen.'),
                                         ('c6',
                                          '',
                                          '',
                                          'HDR-Gaming',
                                          'Lebendigere Farben und schnelles Laden für ein '
                                          'immersives Spielerlebnis.'),
                                         ('c6',
                                          '',
                                          '',
                                          'Maximale Sicherheit',
                                          'Firewall- und Internetschutz gegen die neuesten '
                                          'Bedrohungen.'),
                                         ('c6',
                                          '',
                                          '',
                                          'Snap-Multitasking',
                                          'Organisieren Sie den Desktop mit intelligenten Layouts '
                                          'für effizienteres Arbeiten.')],
                                  'es': [('c6',
                                          '',
                                          '',
                                          'Copilot integrado',
                                          'Inteligencia artificial a tu servicio para simplificar '
                                          'cada tarea diaria.'),
                                         ('c6',
                                          '',
                                          '',
                                          'Juego HDR',
                                          'Colores más vivos y cargas rápidas para una experiencia '
                                          'de juego inmersiva.'),
                                         ('c6',
                                          '',
                                          '',
                                          'Máxima seguridad',
                                          'Protección de firewall e internet frente a las amenazas '
                                          'más recientes.'),
                                         ('c6',
                                          '',
                                          '',
                                          'Multitarea Snap',
                                          'Organiza el escritorio con diseños inteligentes para '
                                          'trabajar mejor y más rápido.')]},
                     'steps': {'it': [('Ordine e pagamento',
                                       'Aggiungi il prodotto al carrello e completa il pagamento '
                                       'sicuro con i metodi disponibili. Ricevi la conferma '
                                       "d'ordine come da condizioni mostrate in checkout."),
                                      ('Consegna digitale',
                                       'Ti inviamo la <strong>product key</strong> e le istruzioni '
                                       "via email, di solito entro pochi minuti dall'approvazione "
                                       'del pagamento.'),
                                      ('Download e attivazione',
                                       'Scarica Windows 11 direttamente da Microsoft o usa il '
                                       'codice per attivare un PC esistente.')],
                               'en': [('Order and payment',
                                       'Add the product to your cart and complete secure payment '
                                       'with the available methods. You will receive an order '
                                       'confirmation as shown at checkout.'),
                                      ('Digital delivery',
                                       'We send your <strong>product key</strong> and instructions '
                                       'by email, usually within minutes of payment approval.'),
                                      ('Download and activation',
                                       'Download Windows 11 directly from Microsoft or use the '
                                       'code to activate an existing PC.')],
                               'fr': [('Commande et paiement',
                                       'Ajoutez le produit au panier et finalisez le paiement '
                                       'sécurisé avec les moyens disponibles. Vous recevrez une '
                                       'confirmation de commande comme indiqué au checkout.'),
                                      ('Livraison numérique',
                                       'Nous vous envoyons la <strong>clé de produit</strong> et '
                                       'les instructions par e-mail, généralement en quelques '
                                       'minutes après validation du paiement.'),
                                      ('Téléchargement et activation',
                                       'Téléchargez Windows 11 directement depuis Microsoft ou '
                                       'utilisez le code pour activer un PC existant.')],
                               'de': [('Bestellung und Zahlung',
                                       'Legen Sie das Produkt in den Warenkorb und schließen Sie '
                                       'die sichere Zahlung mit den verfügbaren Methoden ab. Sie '
                                       'erhalten eine Bestellbestätigung wie im Checkout '
                                       'angegeben.'),
                                      ('Digitale Lieferung',
                                       'Wir senden Ihnen den <strong>Produktschlüssel</strong> und '
                                       'Anweisungen per E-Mail, in der Regel wenige Minuten nach '
                                       'Zahlungsfreigabe.'),
                                      ('Download und Aktivierung',
                                       'Laden Sie Windows 11 direkt von Microsoft herunter oder '
                                       'verwenden Sie den Code zur Aktivierung eines vorhandenen '
                                       'PCs.')],
                               'es': [('Pedido y pago',
                                       'Añade el producto al carrito y completa el pago seguro con '
                                       'los métodos disponibles. Recibirás la confirmación del '
                                       'pedido según se muestra en el checkout.'),
                                      ('Entrega digital',
                                       'Te enviamos la <strong>clave de producto</strong> y las '
                                       'instrucciones por email, normalmente en pocos minutos tras '
                                       'la aprobación del pago.'),
                                      ('Descarga y activación',
                                       'Descarga Windows 11 directamente desde Microsoft o usa el '
                                       'código para activar un PC existente.')]},
                     'specs': {'it': [('Processore',
                                       '1 GHz o superiore con 2 o più core (64-bit).'),
                                      ('RAM', '4 GB o superiore.'),
                                      ('Archiviazione', '64 GB o superiore.'),
                                      ('Sicurezza',
                                       'UEFI, compatibile con Secure Boot e <strong>TPM '
                                       '2.0</strong>.')],
                               'en': [('Processor',
                                       '1 GHz or faster with 2 or more cores (64-bit).'),
                                      ('RAM', '4 GB or more.'),
                                      ('Storage', '64 GB or more.'),
                                      ('Security',
                                       'UEFI, Secure Boot capable and <strong>TPM 2.0</strong>.')],
                               'fr': [('Processeur',
                                       '1 GHz ou plus rapide avec 2 cœurs ou plus (64 bits).'),
                                      ('Mémoire vive', '4 Go ou plus.'),
                                      ('Stockage', '64 Go ou plus.'),
                                      ('Sécurité',
                                       'UEFI, compatible démarrage sécurisé et <strong>TPM '
                                       '2.0</strong>.')],
                               'de': [('Prozessor',
                                       '1 GHz oder schneller mit 2 oder mehr Kernen (64-Bit).'),
                                      ('Arbeitsspeicher', '4 GB oder mehr.'),
                                      ('Speicher', '64 GB oder mehr.'),
                                      ('Sicherheit',
                                       'UEFI, Secure Boot-fähig und <strong>TPM 2.0</strong>.')],
                               'es': [('Procesador',
                                       '1 GHz o superior con 2 o más núcleos (64 bits).'),
                                      ('RAM', '4 GB o superior.'),
                                      ('Almacenamiento', '64 GB o superior.'),
                                      ('Seguridad',
                                       'UEFI, compatible con arranque seguro y <strong>TPM '
                                       '2.0</strong>.')]},
                     'specs_note': {'it': None, 'en': None, 'fr': None, 'de': None, 'es': None},
                     'faq': {'it': [('La licenza è valida per sempre o a scadenza?',
                                     'La licenza è a vita (perpetua) per il dispositivo su cui '
                                     'viene attivata. Non ha scadenza né richiede rinnovi.'),
                                    ('Come si attiva la licenza di Windows 11?',
                                     'Inserisci il product key ricevuto via email durante '
                                     "l'installazione del sistema operativo oppure nelle "
                                     'impostazioni "Attivazione" se Windows 11 è già installato.'),
                                    ('Questa licenza può aggiornare da Windows 10?',
                                     'Sì, se il tuo PC rispetta i requisiti minimi hardware '
                                     'stabiliti da Microsoft, puoi utilizzare il product key per '
                                     'aggiornare la tua versione compatibile di Windows 10 a '
                                     'Windows 11.')],
                             'en': [('Is the licence perpetual or time-limited?',
                                     'The licence is perpetual (lifetime) for the device on which '
                                     'it is activated. It does not expire and requires no '
                                     'renewals.'),
                                    ('How do I activate my Windows 11 licence?',
                                     'Enter the product key you received by email during operating '
                                     'system installation, or in Settings under Activation if '
                                     'Windows 11 is already installed.'),
                                    ('Can this licence upgrade from Windows 10?',
                                     'Yes. If your PC meets Microsoft&rsquo;s minimum hardware '
                                     'requirements, you can use the product key to upgrade a '
                                     'compatible Windows 10 installation to Windows 11.')],
                             'fr': [('La licence est-elle à vie ou limitée dans le temps ?',
                                     "La licence est perpétuelle (à vie) pour l'appareil sur "
                                     "lequel elle est activée. Elle n'expire pas et ne nécessite "
                                     'aucun renouvellement.'),
                                    ('Comment activer ma licence Windows 11 ?',
                                     'Saisissez la clé de produit reçue par e-mail lors de '
                                     "l'installation du système d'exploitation, ou dans Paramètres "
                                     'sous Activation si Windows 11 est déjà installé.'),
                                    ('Cette licence permet-elle de passer de Windows 10 à Windows '
                                     '11 ?',
                                     'Oui. Si votre PC respecte les exigences matérielles '
                                     'minimales de Microsoft, vous pouvez utiliser la clé de '
                                     'produit pour mettre à jour une installation Windows 10 '
                                     'compatible vers Windows 11.')],
                             'de': [('Ist die Lizenz dauerhaft oder zeitlich begrenzt?',
                                     'Die Lizenz ist dauerhaft (lebenslang) für das Gerät, auf dem '
                                     'sie aktiviert wird. Sie läuft nicht ab und erfordert keine '
                                     'Verlängerungen.'),
                                    ('Wie aktiviere ich meine Windows 11 Lizenz?',
                                     'Geben Sie den per E-Mail erhaltenen Produktschlüssel während '
                                     'der Betriebssysteminstallation ein oder unter Einstellungen '
                                     '&gt; Aktivierung, wenn Windows 11 bereits installiert ist.'),
                                    ('Kann diese Lizenz ein Upgrade von Windows 10 ermöglichen?',
                                     'Ja. Wenn Ihr PC die Mindesthardwareanforderungen von '
                                     'Microsoft erfüllt, können Sie den Produktschlüssel '
                                     'verwenden, um eine kompatible Windows 10 Installation auf '
                                     'Windows 11 zu aktualisieren.')],
                             'es': [('¿La licencia es perpetua o tiene caducidad?',
                                     'La licencia es perpetua (de por vida) para el dispositivo en '
                                     'el que se activa. No caduca ni requiere renovaciones.'),
                                    ('¿Cómo activo la licencia de Windows 11?',
                                     'Introduce la clave de producto recibida por email durante la '
                                     'instalación del sistema operativo o en Configuración &gt; '
                                     'Activación si Windows 11 ya está instalado.'),
                                    ('¿Puede esta licencia actualizar desde Windows 10?',
                                     'Sí. Si tu PC cumple los requisitos mínimos de hardware de '
                                     'Microsoft, puedes usar la clave de producto para actualizar '
                                     'una instalación compatible de Windows 10 a Windows 11.')]},
                     'apps': [],
                     'lifestyle': {'image': 'windows-11-start-1024x640.jpg',
                                   'image_root': '',
                                   'width': '1024',
                                   'height': '640',
                                   'alt': {'it': 'Interfaccia di Windows 11 con il nuovo menu '
                                                 'Start centrale.',
                                           'en': 'Windows 11 interface with the new centred Start '
                                                 'menu.',
                                           'fr': 'Interface Windows 11 avec le nouveau menu '
                                                 'Démarrer centré.',
                                           'de': 'Windows 11 Oberfläche mit dem neuen zentrierten '
                                                 'Startmenü.',
                                           'es': 'Interfaz de Windows 11 con el nuevo menú Inicio '
                                                 'centrado.'},
                                   'kicker': {'it': 'Interfaccia',
                                              'en': 'Interface',
                                              'fr': 'Interface',
                                              'de': 'Oberfläche',
                                              'es': 'Interfaz'},
                                   'title': {'it': None,
                                             'en': None,
                                             'fr': None,
                                             'de': None,
                                             'es': None},
                                   'body': {'it': "L'interfaccia ridisegnata di Windows 11 ti "
                                                  'permette di accedere rapidamente alle tue app '
                                                  'preferite e ai file recenti in un ambiente '
                                                  'pulito, fluido e moderno.',
                                            'en': 'The redesigned Windows 11 interface gives you '
                                                  'quick access to your favourite apps and recent '
                                                  'files in a clean, fluid, modern environment.',
                                            'fr': "L'interface repensée de Windows 11 vous permet "
                                                  "d'accéder rapidement à vos applications "
                                                  'préférées et à vos fichiers récents dans un '
                                                  'environnement épuré, fluide et moderne.',
                                            'de': 'Die neu gestaltete Windows 11 Oberfläche '
                                                  'ermöglicht schnellen Zugriff auf Ihre '
                                                  'Lieblings-Apps und zuletzt verwendete Dateien '
                                                  'in einer klaren, flüssigen, modernen Umgebung.',
                                            'es': 'La interfaz rediseñada de Windows 11 te permite '
                                                  'acceder rápidamente a tus aplicaciones '
                                                  'favoritas y archivos recientes en un entorno '
                                                  'limpio, fluido y moderno.'}}},
 'microsoft-365-family': {'name': {'it': 'Microsoft 365 Family',
                                   'en': 'Microsoft 365 Family',
                                   'fr': 'Microsoft 365 Family',
                                   'de': 'Microsoft 365 Family',
                                   'es': 'Microsoft 365 Family'},
                          'seo_title': {'it': 'Microsoft 365 Family — Aml Store',
                                        'en': 'Microsoft 365 Family — Aml Store',
                                        'fr': 'Microsoft 365 Family — Aml Store',
                                        'de': 'Microsoft 365 Family — Aml Store',
                                        'es': 'Microsoft 365 Family — Aml Store'},
                          'desc': {'it': 'Microsoft 365 per te e altre cinque persone, con app '
                                         'complete e 1 TB di OneDrive personale per ciascun '
                                         'membro. Copilot è incluso per il titolare '
                                         "dell'abbonamento.",
                                   'en': 'Microsoft 365 for you and five other people, with full '
                                         'apps and 1 TB of personal OneDrive for each member. '
                                         'Copilot is included for the subscription owner.',
                                   'fr': 'Microsoft 365 pour vous et cinq autres personnes, avec '
                                         "des apps complètes et 1 To d'OneDrive personnel pour "
                                         'chaque membre. Copilot est inclus pour le titulaire de '
                                         "l'abonnement.",
                                   'de': 'Microsoft 365 für Sie und fünf weitere Personen, mit '
                                         'vollständigen Apps und jeweils 1 TB persönlichem '
                                         'OneDrive. Copilot ist für den Abonnementinhaber '
                                         'enthalten.',
                                   'es': 'Microsoft 365 para ti y otras cinco personas, con apps '
                                         'completas y 1 TB de OneDrive personal para cada miembro. '
                                         'Copilot está incluido para el titular de la '
                                         'suscripción.'},
                          'eyebrow': {'it': 'Abbonamento digitale · 12 mesi',
                                      'en': 'Digital subscription · 12 months',
                                      'fr': 'Abonnement numérique · 12 mois',
                                      'de': 'Digitales Abo · 12 Monate',
                                      'es': 'Suscripción digital · 12 meses'},
                          'title_html': {'it': 'Microsoft 365 <span>Family</span>',
                                         'en': 'Microsoft 365 <span>Family</span>',
                                         'fr': 'Microsoft 365 <span>Family</span>',
                                         'de': 'Microsoft 365 <span>Family</span>',
                                         'es': 'Microsoft 365 <span>Family</span>'},
                          'apps_title': {'it': 'Tutte le app che usi, su tutti i tuoi dispositivi',
                                         'en': 'All the apps you use, on all your devices',
                                         'fr': 'Toutes les apps que vous utilisez, sur tous vos '
                                               'appareils',
                                         'de': 'Alle Apps, die Sie nutzen — auf allen Geräten',
                                         'es': 'Todas las apps que usas, en todos tus '
                                               'dispositivos'},
                          'apps_sub': {'it': 'Installa le applicazioni desktop supportate e '
                                             'continua a lavorare anche offline. I documenti '
                                             'possono essere sincronizzati tramite OneDrive.',
                                       'en': 'Install the supported desktop apps and keep working '
                                             'offline. Documents can sync via OneDrive.',
                                       'fr': 'Installez les applications de bureau prises en '
                                             'charge et continuez à travailler hors ligne. Les '
                                             'documents peuvent être synchronisés via OneDrive.',
                                       'de': 'Installieren Sie die unterstützten Desktop-Apps und '
                                             'arbeiten Sie auch offline weiter. Dokumente können '
                                             'über OneDrive synchronisiert werden.',
                                       'es': 'Instala las apps de escritorio compatibles y sigue '
                                             'trabajando sin conexión. Los documentos pueden '
                                             'sincronizarse con OneDrive.'},
                          'apps': ['word',
                                   'excel',
                                   'powerpoint',
                                   'outlook',
                                   'onedrive',
                                   'copilot',
                                   'teams',
                                   'defender',
                                   'onenote',
                                   'designer',
                                   'clipchamp'],
                          'keypoints': {'it': ['Fino a 6 persone, ognuna con il proprio account '
                                               'Microsoft',
                                               '1 TB di OneDrive a persona, file e impostazioni '
                                               'separati',
                                               'App desktop sempre aggiornate su PC, Mac, tablet e '
                                               'telefono',
                                               'Copilot per il titolare <em>— non condiviso con '
                                               'gli altri membri</em>'],
                                        'en': ['Up to 6 people, each with their own Microsoft '
                                               'account',
                                               '1 TB of OneDrive per person, separate files and '
                                               'settings',
                                               'Desktop apps always up to date on PC, Mac, tablet '
                                               'and phone',
                                               'Copilot for the owner <em>— not shared with other '
                                               'members</em>'],
                                        'fr': ["Jusqu'à 6 personnes, chacune avec son compte "
                                               'Microsoft',
                                               "1 To d'OneDrive par personne, fichiers et "
                                               'paramètres séparés',
                                               'Apps de bureau toujours à jour sur PC, Mac, '
                                               'tablette et téléphone',
                                               'Copilot pour le titulaire <em>— non partagé avec '
                                               'les autres membres</em>'],
                                        'de': ['Bis zu 6 Personen, jeweils mit eigenem '
                                               'Microsoft-Konto',
                                               '1 TB OneDrive pro Person, getrennte Dateien und '
                                               'Einstellungen',
                                               'Desktop-Apps stets aktuell auf PC, Mac, Tablet und '
                                               'Smartphone',
                                               'Copilot für den Inhaber <em>— nicht mit anderen '
                                               'Mitgliedern geteilt</em>'],
                                        'es': ['Hasta 6 personas, cada una con su propia cuenta '
                                               'Microsoft',
                                               '1 TB de OneDrive por persona, archivos y ajustes '
                                               'separados',
                                               'Apps de escritorio siempre actualizadas en PC, '
                                               'Mac, tablet y móvil',
                                               'Copilot para el titular <em>— no se comparte con '
                                               'los demás miembros</em>']},
                          'steps': {'it': [("Completa l'ordine",
                                            'Paga con uno dei metodi disponibili al checkout: '
                                            'carta, PayPal o wallet digitali.'),
                                           ('Ricevi il codice',
                                            'Product key e istruzioni arrivano via email in 2–15 '
                                            'minuti dalla conferma del pagamento.'),
                                           ('Attiva su Microsoft',
                                            'Accedi con il tuo account e riscatta il codice su <a '
                                            'href="https://setup.office.com/Home" target="_blank" '
                                            'rel="noopener noreferrer">setup.office.com</a>, poi '
                                            'installa le app da <a href="https://www.office.com" '
                                            'target="_blank" rel="noopener '
                                            'noreferrer">office.com</a>.')],
                                    'en': [('Complete your order',
                                            'Pay with one of the methods available at checkout: '
                                            'card, PayPal or digital wallets.'),
                                           ('Receive your code',
                                            'Product key and instructions arrive by email within '
                                            '2–15 minutes of payment confirmation.'),
                                           ('Activate on Microsoft',
                                            'Sign in with your account and redeem the code on <a '
                                            'href="https://setup.office.com/Home" target="_blank" '
                                            'rel="noopener noreferrer">setup.office.com</a>, then '
                                            'install the apps from <a '
                                            'href="https://www.office.com" target="_blank" '
                                            'rel="noopener noreferrer">office.com</a>.')],
                                    'fr': [('Finalisez la commande',
                                            "Payez avec l'un des moyens disponibles au paiement : "
                                            'carte, PayPal ou portefeuilles numériques.'),
                                           ('Recevez le code',
                                            'La clé produit et les instructions arrivent par '
                                            'e-mail sous 2 à 15 minutes après confirmation du '
                                            'paiement.'),
                                           ('Activez chez Microsoft',
                                            'Connectez-vous avec votre compte et utilisez le code '
                                            'sur <a href="https://setup.office.com/Home" '
                                            'target="_blank" rel="noopener '
                                            'noreferrer">setup.office.com</a>, puis installez les '
                                            'apps depuis <a href="https://www.office.com" '
                                            'target="_blank" rel="noopener '
                                            'noreferrer">office.com</a>.')],
                                    'de': [('Bestellung abschließen',
                                            'Zahlen Sie mit einer der beim Checkout verfügbaren '
                                            'Methoden: Karte, PayPal oder digitale Wallets.'),
                                           ('Code erhalten',
                                            'Product Key und Anweisungen kommen per E-Mail '
                                            'innerhalb von 2–15 Minuten nach Zahlungsbestätigung.'),
                                           ('Bei Microsoft aktivieren',
                                            'Melden Sie sich mit Ihrem Konto an und lösen Sie den '
                                            'Code auf <a href="https://setup.office.com/Home" '
                                            'target="_blank" rel="noopener '
                                            'noreferrer">setup.office.com</a> ein; installieren '
                                            'Sie danach die Apps von <a '
                                            'href="https://www.office.com" target="_blank" '
                                            'rel="noopener noreferrer">office.com</a>.')],
                                    'es': [('Completa tu pedido',
                                            'Paga con uno de los métodos disponibles en el '
                                            'checkout: tarjeta, PayPal o monederos digitales.'),
                                           ('Recibe tu código',
                                            'La clave de producto y las instrucciones llegan por '
                                            'email en 2–15 minutos tras la confirmación del pago.'),
                                           ('Activa en Microsoft',
                                            'Inicia sesión con tu cuenta y canjea el código en <a '
                                            'href="https://setup.office.com/Home" target="_blank" '
                                            'rel="noopener noreferrer">setup.office.com</a>; '
                                            'después instala las apps desde <a '
                                            'href="https://www.office.com" target="_blank" '
                                            'rel="noopener noreferrer">office.com</a>.')]},
                          'steps_note': {'it': "<strong>Controlla di usare l'account Microsoft "
                                               'corretto:</strong> la licenza viene associata '
                                               "all'account scelto durante il riscatto e non può "
                                               'essere spostata successivamente.',
                                         'en': '<strong>Make sure you use the correct Microsoft '
                                               'account:</strong> the licence is tied to the '
                                               'account chosen at redemption and cannot be moved '
                                               'later.',
                                         'fr': "<strong>Vérifiez d'utiliser le bon compte "
                                               'Microsoft :</strong> la licence est associée au '
                                               "compte choisi lors de l'activation et ne peut pas "
                                               'être déplacée ensuite.',
                                         'de': '<strong>Nutzen Sie das richtige '
                                               'Microsoft-Konto:</strong> Die Lizenz ist an das '
                                               'bei der Einlösung gewählte Konto gebunden und kann '
                                               'später nicht verschoben werden.',
                                         'es': '<strong>Asegúrate de usar la cuenta Microsoft '
                                               'correcta:</strong> la licencia queda vinculada a '
                                               'la cuenta elegida en el canje y no se puede mover '
                                               'después.'},
                          'specs_note': {'it': 'Valori indicativi da documentazione Microsoft. '
                                               'Verifica sempre i requisiti aggiornati sulla '
                                               'scheda ufficiale Microsoft prima '
                                               "dell'installazione.",
                                         'en': 'Indicative values from Microsoft documentation. '
                                               'Always check the latest requirements on the '
                                               'official Microsoft product page before installing.',
                                         'fr': "Valeurs indicatives d'après la documentation "
                                               'Microsoft. Vérifiez toujours les exigences à jour '
                                               'sur la fiche Microsoft officielle avant '
                                               "l'installation.",
                                         'de': 'Richtwerte aus der Microsoft-Dokumentation. Prüfen '
                                               'Sie vor der Installation stets die aktuellen '
                                               'Anforderungen auf der offiziellen '
                                               'Microsoft-Produktseite.',
                                         'es': 'Valores orientativos de la documentación de '
                                               'Microsoft. Comprueba siempre los requisitos '
                                               'actualizados en la página oficial del producto '
                                               'Microsoft antes de instalar.'},
                          'specs': {'it': [('Sistemi operativi supportati',
                                            'Windows 10 o versioni successive; le tre versioni più '
                                            'recenti di macOS; iOS e Android nelle versioni '
                                            'supportate da Microsoft.'),
                                           ('Processore e memoria',
                                            ['Windows: processore a 1,6 GHz o superiore, due core. '
                                             'Mac: processore Intel o Apple Silicon compatibile '
                                             'con la versione di macOS supportata.',
                                             'Memoria: 4 GB di RAM per le versioni a 64 bit, 2 GB '
                                             'per quelle a 32 bit.']),
                                           ('Spazio su disco',
                                            'Circa 4 GB di spazio disponibile su Windows e circa '
                                            '10 GB su macOS, a seconda delle app installate.'),
                                           ('Connessione e account Microsoft',
                                            'Servono un account Microsoft e una connessione '
                                            'internet per riscatto, attivazione, aggiornamenti e '
                                            'servizi cloud. Le app desktop installate funzionano '
                                            'anche offline, con verifiche periodiche della '
                                            'licenza.')],
                                    'en': [('Supported operating systems',
                                            'Windows 10 or later; the three most recent versions '
                                            'of macOS; iOS and Android in versions supported by '
                                            'Microsoft.'),
                                           ('Processor and memory',
                                            ['Windows: 1.6 GHz or faster processor, two cores. '
                                             'Mac: Intel or Apple Silicon processor compatible '
                                             'with the supported macOS version.',
                                             'Memory: 4 GB RAM for 64-bit versions, 2 GB for '
                                             '32-bit versions.']),
                                           ('Disk space',
                                            'About 4 GB free space on Windows and about 10 GB on '
                                            'macOS, depending on the apps installed.'),
                                           ('Connection and Microsoft account',
                                            'A Microsoft account and an internet connection are '
                                            'required for redemption, activation, updates and '
                                            'cloud services. Installed desktop apps also work '
                                            'offline, with periodic licence checks.')],
                                    'fr': [("Systèmes d'exploitation pris en charge",
                                            'Windows 10 ou versions ultérieures ; les trois '
                                            'versions les plus récentes de macOS ; iOS et Android '
                                            'dans les versions prises en charge par Microsoft.'),
                                           ('Processeur et mémoire',
                                            ['Windows : processeur 1,6 GHz ou plus, deux cœurs. '
                                             'Mac : processeur Intel ou Apple Silicon compatible '
                                             'avec la version de macOS prise en charge.',
                                             'Mémoire : 4 Go de RAM pour les versions 64 bits, 2 '
                                             'Go pour les versions 32 bits.']),
                                           ('Espace disque',
                                            "Environ 4 Go d'espace libre sous Windows et environ "
                                            '10 Go sous macOS, selon les apps installées.'),
                                           ('Connexion et compte Microsoft',
                                            'Un compte Microsoft et une connexion Internet sont '
                                            "nécessaires pour l'activation, les mises à jour et "
                                            'les services cloud. Les apps de bureau installées '
                                            'fonctionnent aussi hors ligne, avec des vérifications '
                                            'périodiques de licence.')],
                                    'de': [('Unterstützte Betriebssysteme',
                                            'Windows 10 oder neuer; die drei neuesten '
                                            'macOS-Versionen; iOS und Android in von Microsoft '
                                            'unterstützten Versionen.'),
                                           ('Prozessor und Arbeitsspeicher',
                                            ['Windows: Prozessor mit 1,6 GHz oder schneller, zwei '
                                             'Kerne. Mac: Intel- oder Apple-Silicon-Prozessor, '
                                             'kompatibel mit der unterstützten macOS-Version.',
                                             'Arbeitsspeicher: 4 GB RAM für 64-Bit-Versionen, 2 GB '
                                             'für 32-Bit-Versionen.']),
                                           ('Speicherplatz',
                                            'Etwa 4 GB freier Speicher unter Windows und etwa 10 '
                                            'GB unter macOS, abhängig von den installierten Apps.'),
                                           ('Verbindung und Microsoft-Konto',
                                            'Für Einlösung, Aktivierung, Updates und Cloud-Dienste '
                                            'sind ein Microsoft-Konto und eine Internetverbindung '
                                            'erforderlich. Installierte Desktop-Apps funktionieren '
                                            'auch offline, mit regelmäßigen Lizenzprüfungen.')],
                                    'es': [('Sistemas operativos compatibles',
                                            'Windows 10 o posterior; las tres versiones más '
                                            'recientes de macOS; iOS y Android en las versiones '
                                            'compatibles con Microsoft.'),
                                           ('Procesador y memoria',
                                            ['Windows: procesador de 1,6 GHz o superior, dos '
                                             'núcleos. Mac: procesador Intel o Apple Silicon '
                                             'compatible con la versión de macOS admitida.',
                                             'Memoria: 4 GB de RAM para versiones de 64 bits, 2 GB '
                                             'para versiones de 32 bits.']),
                                           ('Espacio en disco',
                                            'Unos 4 GB libres en Windows y unos 10 GB en macOS, '
                                            'según de las apps instaladas.'),
                                           ('Conexión y cuenta Microsoft',
                                            'Se necesitan una cuenta Microsoft y una conexión a '
                                            'internet para el canje, la activación, las '
                                            'actualizaciones y los servicios en la nube. Las apps '
                                            'de escritorio instaladas también funcionan sin '
                                            'conexión, con comprobaciones periódicas de la '
                                            'licencia.')]},
                          'faq': {'it': [('Quando ricevo il codice dopo il pagamento?',
                                          ["L'email di consegna parte dopo la conferma del "
                                           'pagamento, di norma entro 2–15 minuti; in rari casi '
                                           'servono alcuni minuti in più per le verifiche del '
                                           'pagamento.',
                                           'Se dopo <strong>30 minuti</strong> non hai ricevuto '
                                           'nulla, controlla anche spam e posta indesiderata e '
                                           'scrivi a <a '
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                           'indicando prodotto acquistato ed email usata per '
                                           "l'ordine."]),
                                         ("Cosa ricevo esattamente nell'email?",
                                          ['Ricevi la <strong>product key</strong> di Microsoft '
                                           '365 Family e le istruzioni per riscattarla sui portali '
                                           'ufficiali Microsoft.',
                                           'La consegna è solo digitale: non viene spedito alcun '
                                           'supporto fisico e non ci sono costi di spedizione.']),
                                         ('Quali metodi di pagamento posso usare?',
                                          'Al checkout sono disponibili carta, PayPal e wallet '
                                          'digitali come Apple Pay e Google Pay dove abilitati. '
                                          "L'elaborazione del pagamento è gestita in modo sicuro "
                                          'tramite <strong>Stripe</strong>.'),
                                         ('Posso avere la fattura elettronica?',
                                          ['Sì. Al checkout scegli il profilo '
                                           '<strong>Azienda</strong> e inserisci partita IVA e '
                                           'Codice SDI oppure PEC: la fattura elettronica viene '
                                           'emessa su quei dati.',
                                           "Se ti serve dopo l'ordine, scrivi a <a "
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                           "indicando l'email usata per l'ordine e il numero "
                                           "d'ordine."]),
                                         ("Come si attiva Microsoft 365 Family dopo l'acquisto?",
                                          'Vai su <a href="https://setup.office.com/Home" '
                                          'target="_blank" rel="noopener '
                                          'noreferrer">setup.office.com/Home</a>, accedi con il '
                                          'tuo account Microsoft, inserisci il codice ricevuto via '
                                          'email e segui la procedura guidata. Al termine installa '
                                          'le app da <a href="https://www.office.com" '
                                          'target="_blank" rel="noopener '
                                          'noreferrer">office.com</a>.'),
                                         ('Posso riscattare il codice su un account Microsoft che '
                                          'uso già?',
                                          ['Sì: il riscatto avviene su setup.office.com con il tuo '
                                           "account Microsoft. Se su quell'account è già attivo un "
                                           'abbonamento Microsoft 365, il comportamento '
                                           '(estensione o conversione del piano) segue le regole '
                                           'Microsoft mostrate durante il riscatto.',
                                           "<strong>Scegli l'account con attenzione:</strong> la "
                                           'licenza resta associata a quello usato al momento del '
                                           'riscatto.']),
                                         ("Come si invitano altri membri dopo l'acquisto?",
                                          "Dopo l'attivazione sul tuo account Microsoft, usa le "
                                          "funzioni di condivisione del piano Family nell'area "
                                          'account Microsoft / abbonamenti, come indicato da '
                                          'Microsoft per il periodo di validità della licenza.'),
                                         ('Copilot è disponibile per tutti i membri?',
                                          ['No. Le funzionalità Copilot comprese nel piano sono '
                                           'utilizzabili dal <strong>titolare '
                                           "dell'abbonamento</strong>.",
                                           'Gli altri cinque membri ricevono le app Microsoft 365, '
                                           '1 TB di OneDrive ciascuno e Microsoft Defender, ma non '
                                           'le funzionalità AI.']),
                                         ('I file sono condivisi automaticamente tra i membri?',
                                          'No. Ogni persona usa il proprio account Microsoft, con '
                                          'documenti, email, impostazioni e spazio OneDrive '
                                          'separati. La condivisione di singoli file o cartelle '
                                          'resta una scelta volontaria di chi li possiede.'),
                                         ('Si possono usare le app Office anche offline?',
                                          'Sì: con le app desktop installate puoi lavorare '
                                          'offline; servono comunque connessione e accesso '
                                          'periodici per la verifica della licenza, aggiornamenti '
                                          'e servizi cloud come OneDrive.'),
                                         ('Qual è la differenza tra Microsoft 365 Family e '
                                          'Personal?',
                                          'Family è pensato per condividere il piano con il tuo '
                                          'gruppo famiglia Microsoft (fino a 6 persone), ciascuna '
                                          'con account e spazio OneDrive distinti. Personal copre '
                                          'un solo utente con 1 TB, secondo le condizioni '
                                          'Microsoft aggiornate.'),
                                         ('Il codice si rinnova automaticamente dopo 12 mesi?',
                                          'No. Il codice attiva Microsoft 365 Family per 12 mesi '
                                          'con un pagamento una tantum: AML Store non addebita '
                                          'nulla automaticamente alla scadenza. Eventuali opzioni '
                                          'di rinnovo si gestiscono separatamente, direttamente '
                                          "nell'account Microsoft."),
                                         ('Posso usare il codice per rinnovare un abbonamento '
                                          'Family già attivo?',
                                          'Sì, puoi riscattarlo sullo stesso account che ha già '
                                          'Microsoft 365 Family attivo. Il modo in cui viene '
                                          'applicato (estensione della durata attuale o avvio di '
                                          'un nuovo periodo) segue le regole Microsoft mostrate al '
                                          'momento del riscatto su setup.office.com, non è '
                                          'qualcosa che decidiamo noi come rivenditore.'),
                                         ('Cosa succede se il codice non funziona?',
                                          ["Scrivici indicando numero d'ordine ed eventuale "
                                           'messaggio di errore. Verifichiamo il caso e, se viene '
                                           'confermato un difetto imputabile a noi o al fornitore '
                                           'della chiave, proponiamo sostituzione o rimborso nei '
                                           'tempi usuali di elaborazione.',
                                           'Assistenza: <a '
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> — '
                                           '+39 392 558 0413.'])],
                                  'en': [('When do I receive the code after payment?',
                                          ['The delivery email is sent after payment confirmation, '
                                           'usually within 2–15 minutes; in rare cases a few extra '
                                           'minutes are needed for payment checks.',
                                           'If after <strong>30 minutes</strong> you have received '
                                           'nothing, also check spam/junk and email <a '
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                           'with the product purchased and the email used for the '
                                           'order.']),
                                         ('What exactly do I receive in the email?',
                                          ['You receive the Microsoft 365 Family <strong>product '
                                           'key</strong> and instructions to redeem it on official '
                                           'Microsoft portals.',
                                           'Delivery is digital only: nothing physical is shipped '
                                           'and there are no shipping fees.']),
                                         ('Which payment methods can I use?',
                                          'At checkout you can pay by card, PayPal and digital '
                                          'wallets such as Apple Pay and Google Pay where enabled. '
                                          'Payment processing is handled securely via '
                                          '<strong>Stripe</strong>.'),
                                         ('Can I get a VAT invoice?',
                                          ['Yes. At checkout choose the <strong>Business</strong> '
                                           'profile and enter your VAT details: we issue a VAT '
                                           'invoice on those details.',
                                           'If you need it after the order, email <a '
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                           'with the order email and order number.']),
                                         ('How do I activate Microsoft 365 Family after purchase?',
                                          'Go to <a href="https://setup.office.com/Home" '
                                          'target="_blank" rel="noopener '
                                          'noreferrer">setup.office.com/Home</a>, sign in with '
                                          'your Microsoft account, enter the code received by '
                                          'email and follow the guided setup. Then install the '
                                          'apps from <a href="https://www.office.com" '
                                          'target="_blank" rel="noopener '
                                          'noreferrer">office.com</a>.'),
                                         ('Can I redeem the code on a Microsoft account I already '
                                          'use?',
                                          ['Yes: redemption happens on setup.office.com with your '
                                           'Microsoft account. If that account already has an '
                                           'active Microsoft 365 subscription, the outcome '
                                           "(extension or plan conversion) follows Microsoft's "
                                           'rules shown during redemption.',
                                           '<strong>Choose the account carefully:</strong> the '
                                           'licence stays tied to the one used at redemption.']),
                                         ('How do I invite other members after purchase?',
                                          'After activation on your Microsoft account, use the '
                                          'Family plan sharing features in the Microsoft account / '
                                          'subscriptions area, as directed by Microsoft for the '
                                          'licence term.'),
                                         ('Is Copilot available to all members?',
                                          ['No. Copilot features included in the plan are '
                                           'available to the <strong>subscription owner</strong>.',
                                           'The other five members get Microsoft 365 apps, 1 TB of '
                                           'OneDrive each and Microsoft Defender, but not the AI '
                                           'features.']),
                                         ('Are files shared automatically between members?',
                                          'No. Each person uses their own Microsoft account, with '
                                          'separate documents, email, settings and OneDrive space. '
                                          'Sharing individual files or folders remains a voluntary '
                                          'choice by the owner.'),
                                         ('Can I use Office apps offline too?',
                                          'Yes: with the desktop apps installed you can work '
                                          'offline; periodic connection and sign-in are still '
                                          'required for licence checks, updates and cloud services '
                                          'such as OneDrive.'),
                                         ('What is the difference between Microsoft 365 Family and '
                                          'Personal?',
                                          'Family is designed to share the plan with your '
                                          'Microsoft family group (up to 6 people), each with a '
                                          'separate account and OneDrive space. Personal covers a '
                                          "single user with 1 TB, subject to Microsoft's current "
                                          'terms.'),
                                         ('Does the code renew automatically after 12 months?',
                                          'No. The code activates Microsoft 365 Family for 12 '
                                          'months with a one-time payment: AML Store does not '
                                          'charge anything automatically at expiry. Any renewal '
                                          'options are managed separately in your Microsoft '
                                          'account.'),
                                         ('Can I use the code to renew an active Family '
                                          'subscription?',
                                          'Yes, you can redeem it on the same account that already '
                                          'has Microsoft 365 Family active. How it is applied '
                                          '(extending the current term or starting a new period) '
                                          "follows Microsoft's rules shown at redemption on "
                                          'setup.office.com — it is not something we decide as a '
                                          'reseller.'),
                                         ('What if the code does not work?',
                                          ['Contact us with your order number and any error '
                                           'message. We review the case and, if a defect '
                                           'attributable to us or the key supplier is confirmed, '
                                           'we offer a replacement or refund within usual '
                                           'processing times.',
                                           'Support: <a '
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> — '
                                           '+39 392 558 0413.'])],
                                  'fr': [('Quand vais-je recevoir le code après le paiement ?',
                                          ["L'e-mail de livraison part après confirmation du "
                                           'paiement, en général sous 2 à 15 minutes ; dans de '
                                           'rares cas, quelques minutes supplémentaires sont '
                                           'nécessaires pour les vérifications.',
                                           "Si après <strong>30 minutes</strong> vous n'avez rien "
                                           'reçu, vérifiez aussi les indésirables et écrivez à <a '
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> en '
                                           "indiquant le produit acheté et l'e-mail utilisé pour "
                                           'la commande.']),
                                         ("Que vais-je exactement recevoir dans l'e-mail ?",
                                          ['Vous recevez la <strong>clé produit</strong> Microsoft '
                                           "365 Family et les instructions pour l'activer sur les "
                                           'portails officiels Microsoft.',
                                           'La livraison est uniquement numérique : aucun support '
                                           "physique n'est expédié et il n'y a pas de frais de "
                                           'port.']),
                                         ('Quels moyens de paiement puis-je utiliser ?',
                                          'Au paiement sont disponibles carte, PayPal et '
                                          'portefeuilles numériques comme Apple Pay et Google Pay '
                                          "lorsqu'ils sont activés. Le paiement est traité de "
                                          'façon sécurisée via <strong>Stripe</strong>.'),
                                         ('Puis-je obtenir une facture ?',
                                          ['Oui. Au paiement, choisissez le profil '
                                           '<strong>Entreprise</strong> et saisissez vos données '
                                           'de TVA : la facture est émise sur ces informations.',
                                           'Si vous en avez besoin après la commande, écrivez à <a '
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> en '
                                           "indiquant l'e-mail de commande et le numéro de "
                                           'commande.']),
                                         ("Comment activer Microsoft 365 Family après l'achat ?",
                                          'Allez sur <a href="https://setup.office.com/Home" '
                                          'target="_blank" rel="noopener '
                                          'noreferrer">setup.office.com/Home</a>, connectez-vous '
                                          'avec votre compte Microsoft, saisissez le code reçu par '
                                          "e-mail et suivez l'assistant. Ensuite, installez les "
                                          'apps depuis <a href="https://www.office.com" '
                                          'target="_blank" rel="noopener '
                                          'noreferrer">office.com</a>.'),
                                         ('Puis-je utiliser le code sur un compte Microsoft que '
                                          "j'utilise déjà ?",
                                          ["Oui : l'activation se fait sur setup.office.com avec "
                                           'votre compte Microsoft. Si un abonnement Microsoft 365 '
                                           'est déjà actif sur ce compte, le comportement '
                                           '(prolongation ou conversion) suit les règles Microsoft '
                                           "affichées pendant l'activation.",
                                           '<strong>Choisissez le compte avec attention :</strong> '
                                           'la licence reste associée à celui utilisé lors de '
                                           "l'activation."]),
                                         ("Comment inviter d'autres membres après l'achat ?",
                                          'Après activation sur votre compte Microsoft, utilisez '
                                          'les fonctions de partage du plan Family dans la zone '
                                          'compte Microsoft / abonnements, comme indiqué par '
                                          'Microsoft pour la durée de la licence.'),
                                         ('Copilot est-il disponible pour tous les membres ?',
                                          ['Non. Les fonctions Copilot incluses dans le plan sont '
                                           'utilisables par le <strong>titulaire de '
                                           "l'abonnement</strong>.",
                                           'Les cinq autres membres reçoivent les apps Microsoft '
                                           "365, 1 To d'OneDrive chacun et Microsoft Defender, "
                                           "mais pas les fonctions d'IA."]),
                                         ('Les fichiers sont-ils partagés automatiquement entre '
                                          'les membres ?',
                                          'Non. Chaque personne utilise son propre compte '
                                          'Microsoft, avec documents, e-mails, paramètres et '
                                          'espace OneDrive séparés. Le partage de fichiers ou '
                                          'dossiers individuels reste un choix volontaire du '
                                          'propriétaire.'),
                                         ('Peut-on utiliser les apps Office hors ligne ?',
                                          'Oui : avec les apps de bureau installées, vous pouvez '
                                          'travailler hors ligne ; une connexion et une connexion '
                                          'périodiques restent nécessaires pour la vérification de '
                                          'licence, les mises à jour et les services cloud comme '
                                          'OneDrive.'),
                                         ('Quelle est la différence entre Microsoft 365 Family et '
                                          'Personal ?',
                                          'Family est conçu pour partager le plan avec votre '
                                          "groupe famille Microsoft (jusqu'à 6 personnes), chacune "
                                          'avec un compte et un espace OneDrive distincts. '
                                          'Personal couvre un seul utilisateur avec 1 To, selon '
                                          'les conditions Microsoft à jour.'),
                                         ('Le code se renouvelle-t-il automatiquement après 12 '
                                          'mois ?',
                                          'Non. Le code active Microsoft 365 Family pour 12 mois '
                                          'avec un paiement unique : AML Store ne prélève rien '
                                          "automatiquement à l'échéance. Les options de "
                                          'renouvellement éventuelles se gèrent séparément dans le '
                                          'compte Microsoft.'),
                                         ('Puis-je utiliser le code pour renouveler un abonnement '
                                          'Family déjà actif ?',
                                          "Oui, vous pouvez l'activer sur le même compte qui a "
                                          "déjà Microsoft 365 Family. La façon dont il s'applique "
                                          '(prolongation de la durée actuelle ou nouveau période) '
                                          'suit les règles Microsoft affichées lors de '
                                          "l'activation sur setup.office.com — ce n'est pas nous "
                                          'qui le décidons en tant que revendeur.'),
                                         ('Que se passe-t-il si le code ne fonctionne pas ?',
                                          ['Écrivez-nous en indiquant le numéro de commande et le '
                                           "message d'erreur éventuel. Nous examinons le cas et, "
                                           'si un défaut imputable à nous ou au fournisseur de la '
                                           'clé est confirmé, nous proposons un remplacement ou un '
                                           'remboursement dans les délais habituels.',
                                           'Assistance : <a '
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> — '
                                           '+39 392 558 0413.'])],
                                  'de': [('Wann erhalte ich den Code nach der Zahlung?',
                                          ['Die Liefer-E-Mail wird nach Zahlungsbestätigung '
                                           'versendet, in der Regel innerhalb von 2–15 Minuten; in '
                                           'seltenen Fällen dauern Zahlungsprüfungen etwas länger.',
                                           'Wenn Sie nach <strong>30 Minuten</strong> nichts '
                                           'erhalten haben, prüfen Sie auch Spam/Junk und '
                                           'schreiben Sie an <a '
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                           'mit dem gekauften Produkt und der für die Bestellung '
                                           'verwendeten E-Mail-Adresse.']),
                                         ('Was genau erhalte ich in der E-Mail?',
                                          ['Sie erhalten den <strong>Product Key</strong> für '
                                           'Microsoft 365 Family sowie Anweisungen zur Einlösung '
                                           'auf den offiziellen Microsoft-Portalen.',
                                           'Die Lieferung erfolgt ausschließlich digital: Es wird '
                                           'nichts physisch versendet und es fallen keine '
                                           'Versandkosten an.']),
                                         ('Welche Zahlungsmethoden kann ich nutzen?',
                                          'Beim Checkout können Sie mit Karte, PayPal und '
                                          'digitalen Wallets wie Apple Pay und Google Pay zahlen, '
                                          'sofern freigeschaltet. Die Zahlungsabwicklung erfolgt '
                                          'sicher über <strong>Stripe</strong>.'),
                                         ('Kann ich eine MwSt.-Rechnung erhalten?',
                                          ['Ja. Wählen Sie beim Checkout das Profil '
                                           '<strong>Unternehmen</strong> und geben Sie Ihre '
                                           'MwSt.-Daten ein: Wir stellen die MwSt.-Rechnung auf '
                                           'diese Daten aus.',
                                           'Wenn Sie sie nach der Bestellung benötigen, schreiben '
                                           'Sie an <a '
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                           'mit der Bestell-E-Mail und der Bestellnummer.']),
                                         ('Wie aktiviere ich Microsoft 365 Family nach dem Kauf?',
                                          'Rufen Sie <a href="https://setup.office.com/Home" '
                                          'target="_blank" rel="noopener '
                                          'noreferrer">setup.office.com/Home</a> auf, melden Sie '
                                          'sich mit Ihrem Microsoft-Konto an, geben Sie den per '
                                          'E-Mail erhaltenen Code ein und folgen Sie dem '
                                          'Einrichtungsassistenten. Installieren Sie anschließend '
                                          'die Apps von <a href="https://www.office.com" '
                                          'target="_blank" rel="noopener '
                                          'noreferrer">office.com</a>.'),
                                         ('Kann ich den Code auf einem Microsoft-Konto einlösen, '
                                          'das ich bereits nutze?',
                                          ['Ja: Die Einlösung erfolgt auf setup.office.com mit '
                                           'Ihrem Microsoft-Konto. Wenn dieses Konto bereits ein '
                                           'aktives Microsoft 365-Abonnement hat, richtet sich das '
                                           'Ergebnis (Verlängerung oder Planwechsel) nach den '
                                           'Microsoft-Regeln, die bei der Einlösung angezeigt '
                                           'werden.',
                                           '<strong>Wählen Sie das Konto sorgfältig:</strong> Die '
                                           'Lizenz bleibt an das bei der Einlösung verwendete '
                                           'Konto gebunden.']),
                                         ('Wie lade ich nach dem Kauf weitere Mitglieder ein?',
                                          'Nach der Aktivierung auf Ihrem Microsoft-Konto nutzen '
                                          'Sie die Freigabefunktionen des Family-Plans im Bereich '
                                          'Microsoft-Konto / Abonnements, wie von Microsoft für '
                                          'die Lizenzlaufzeit vorgesehen.'),
                                         ('Ist Copilot für alle Mitglieder verfügbar?',
                                          ['Nein. Die im Plan enthaltenen Copilot-Funktionen '
                                           'stehen dem <strong>Abonnementinhaber</strong> zur '
                                           'Verfügung.',
                                           'Die anderen fünf Mitglieder erhalten Microsoft 365 '
                                           'Apps, jeweils 1 TB OneDrive und Microsoft Defender, '
                                           'jedoch nicht die KI-Funktionen.']),
                                         ('Werden Dateien automatisch zwischen Mitgliedern '
                                          'geteilt?',
                                          'Nein. Jede Person nutzt ihr eigenes Microsoft-Konto mit '
                                          'getrennten Dokumenten, E-Mails, Einstellungen und '
                                          'OneDrive-Speicher. Das Teilen einzelner Dateien oder '
                                          'Ordner bleibt eine freiwillige Entscheidung des '
                                          'Besitzers.'),
                                         ('Kann ich Office-Apps auch offline nutzen?',
                                          'Ja: Mit den installierten Desktop-Apps können Sie '
                                          'offline arbeiten; für Lizenzprüfungen, Updates und '
                                          'Cloud-Dienste wie OneDrive sind weiterhin eine '
                                          'gelegentliche Verbindung und Anmeldung erforderlich.'),
                                         ('Was ist der Unterschied zwischen Microsoft 365 Family '
                                          'und Personal?',
                                          'Family ist zum Teilen des Plans mit Ihrer '
                                          'Microsoft-Familiengruppe gedacht (bis zu 6 Personen), '
                                          'jeweils mit eigenem Konto und OneDrive-Speicher. '
                                          'Personal gilt für einen einzelnen Nutzer mit 1 TB, '
                                          'gemäß den aktuellen Microsoft-Bedingungen.'),
                                         ('Verlängert sich der Code nach 12 Monaten automatisch?',
                                          'Nein. Der Code aktiviert Microsoft 365 Family für 12 '
                                          'Monate mit einer einmaligen Zahlung: AML Store belastet '
                                          'bei Ablauf nichts automatisch. Etwaige '
                                          'Verlängerungsoptionen verwalten Sie separat in Ihrem '
                                          'Microsoft-Konto.'),
                                         ('Kann ich den Code zur Verlängerung eines aktiven '
                                          'Family-Abonnements nutzen?',
                                          'Ja, Sie können ihn auf demselben Konto einlösen, auf '
                                          'dem Microsoft 365 Family bereits aktiv ist. Wie er '
                                          'angewendet wird (Verlängerung der aktuellen Laufzeit '
                                          'oder Beginn einer neuen Periode) richtet sich nach den '
                                          'Microsoft-Regeln, die bei der Einlösung auf '
                                          'setup.office.com angezeigt werden — das entscheiden '
                                          'nicht wir als Händler.'),
                                         ('Was tun, wenn der Code nicht funktioniert?',
                                          ['Kontaktieren Sie uns mit Ihrer Bestellnummer und einer '
                                           'etwaigen Fehlermeldung. Wir prüfen den Fall und bieten '
                                           'bei einem nachweislich uns oder dem Key-Lieferanten '
                                           'zurechenbaren Defekt Ersatz oder Erstattung innerhalb '
                                           'der üblichen Bearbeitungszeiten.',
                                           'Support: <a '
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> — '
                                           '+39 392 558 0413.'])],
                                  'es': [('¿Cuándo recibo el código después del pago?',
                                          ['El email de entrega se envía tras la confirmación del '
                                           'pago, normalmente en 2–15 minutos; en casos '
                                           'excepcionales pueden hacer falta unos minutos más para '
                                           'las comprobaciones del pago.',
                                           'Si tras <strong>30 minutos</strong> no has recibido '
                                           'nada, revisa también spam/correo no deseado y escribe '
                                           'a <a '
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                           'indicando el producto comprado y el email usado en el '
                                           'pedido.']),
                                         ('¿Qué recibo exactamente en el email?',
                                          ['Recibes la <strong>clave de producto</strong> de '
                                           'Microsoft 365 Family y las instrucciones para '
                                           'canjearla en los portales oficiales de Microsoft.',
                                           'La entrega es solo digital: no se envía nada físico y '
                                           'no hay gastos de envío.']),
                                         ('¿Qué métodos de pago puedo usar?',
                                          'En el checkout puedes pagar con tarjeta, PayPal y '
                                          'monederos digitales como Apple Pay y Google Pay donde '
                                          'estén habilitados. El procesamiento del pago se '
                                          'gestiona de forma segura a través de '
                                          '<strong>Stripe</strong>.'),
                                         ('¿Puedo obtener factura con IVA?',
                                          ['Sí. En el checkout elige el perfil '
                                           '<strong>Empresa</strong> e introduce tus datos de IVA: '
                                           'emitimos la factura con IVA con esos datos.',
                                           'Si la necesitas después del pedido, escribe a <a '
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                           'con el email del pedido y el número de pedido.']),
                                         ('¿Cómo activo Microsoft 365 Family después de la compra?',
                                          'Ve a <a href="https://setup.office.com/Home" '
                                          'target="_blank" rel="noopener '
                                          'noreferrer">setup.office.com/Home</a>, inicia sesión '
                                          'con tu cuenta Microsoft, introduce el código recibido '
                                          'por email y sigue el asistente de configuración. '
                                          'Después instala las apps desde <a '
                                          'href="https://www.office.com" target="_blank" '
                                          'rel="noopener noreferrer">office.com</a>.'),
                                         ('¿Puedo canjear el código en una cuenta Microsoft que ya '
                                          'uso?',
                                          ['Sí: el canje se realiza en setup.office.com con tu '
                                           'cuenta Microsoft. Si esa cuenta ya tiene una '
                                           'suscripción Microsoft 365 activa, el resultado '
                                           '(prórroga o conversión de plan) sigue las reglas de '
                                           'Microsoft mostradas durante el canje.',
                                           '<strong>Elige la cuenta con cuidado:</strong> la '
                                           'licencia queda vinculada a la usada en el canje.']),
                                         ('¿Cómo invito a otros miembros después de la compra?',
                                          'Tras la activación en tu cuenta Microsoft, usa las '
                                          'funciones para compartir el plan Family en el área de '
                                          'cuenta Microsoft / suscripciones, según las '
                                          'indicaciones de Microsoft durante la vigencia de la '
                                          'licencia.'),
                                         ('¿Copilot está disponible para todos los miembros?',
                                          ['No. Las funciones de Copilot incluidas en el plan '
                                           'están disponibles para el <strong>titular de la '
                                           'suscripción</strong>.',
                                           'Los otros cinco miembros obtienen las apps Microsoft '
                                           '365, 1 TB de OneDrive cada uno y Microsoft Defender, '
                                           'pero no las funciones de IA.']),
                                         ('¿Los archivos se comparten automáticamente entre los '
                                          'miembros?',
                                          'No. Cada persona usa su propia cuenta Microsoft, con '
                                          'documentos, email, ajustes y espacio OneDrive '
                                          'separados. Compartir archivos o carpetas concretos '
                                          'sigue siendo una elección voluntaria del propietario.'),
                                         ('¿Puedo usar también las apps de Office sin conexión?',
                                          'Sí: con las aplicaciones de escritorio instaladas '
                                          'puedes trabajar sin conexión; aun así se requieren '
                                          'conexión e inicio de sesión periódicos para la '
                                          'verificación de la licencia, las actualizaciones y los '
                                          'servicios en la nube como OneDrive.'),
                                         ('¿Cuál es la diferencia entre Microsoft 365 Family y '
                                          'Personal?',
                                          'Family está pensado para compartir el plan con tu grupo '
                                          'familiar de Microsoft (hasta 6 personas), cada una con '
                                          'una cuenta y espacio OneDrive propios. Personal cubre a '
                                          'un solo usuario con 1 TB, según las condiciones '
                                          'vigentes de Microsoft.'),
                                         ('¿El código se renueva automáticamente después de 12 '
                                          'meses?',
                                          'No. El código activa Microsoft 365 Family durante 12 '
                                          'meses con un pago único: AML Store no cobra nada '
                                          'automáticamente al vencimiento. Cualquier opción de '
                                          'renovación se gestiona por separado en tu cuenta '
                                          'Microsoft.'),
                                         ('¿Puedo usar el código para renovar una suscripción '
                                          'Family activa?',
                                          'Sí, puedes canjearlo en la misma cuenta que ya tiene '
                                          'Microsoft 365 Family activo. Cómo se aplica (prorrogar '
                                          'el periodo actual o iniciar uno nuevo) sigue las reglas '
                                          'de Microsoft mostradas en el canje en setup.office.com: '
                                          'no es algo que decidamos nosotros como revendedor.'),
                                         ('¿Qué pasa si el código no funciona?',
                                          ['Contáctanos con tu número de pedido y cualquier '
                                           'mensaje de error. Revisamos el caso y, si se confirma '
                                           'un defecto imputable a nosotros o al proveedor de la '
                                           'clave, ofrecemos sustitución o reembolso en los plazos '
                                           'habituales de gestión.',
                                           'Soporte: <a '
                                           'href="mailto:Info@amlstore.it">Info@amlstore.it</a> — '
                                           '+39 392 558 0413.'])]},
                          'faq_groups': {'it': [('Acquisto e consegna',
                                                 [('Quando ricevo il codice dopo il pagamento?',
                                                   ["L'email di consegna parte dopo la conferma "
                                                    'del pagamento, di norma entro 2–15 minuti; in '
                                                    'rari casi servono alcuni minuti in più per le '
                                                    'verifiche del pagamento.',
                                                    'Se dopo <strong>30 minuti</strong> non hai '
                                                    'ricevuto nulla, controlla anche spam e posta '
                                                    'indesiderata e scrivi a <a '
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    'indicando prodotto acquistato ed email usata '
                                                    "per l'ordine."]),
                                                  ("Cosa ricevo esattamente nell'email?",
                                                   ['Ricevi la <strong>product key</strong> di '
                                                    'Microsoft 365 Family e le istruzioni per '
                                                    'riscattarla sui portali ufficiali Microsoft.',
                                                    'La consegna è solo digitale: non viene '
                                                    'spedito alcun supporto fisico e non ci sono '
                                                    'costi di spedizione.']),
                                                  ('Quali metodi di pagamento posso usare?',
                                                   'Al checkout sono disponibili carta, PayPal e '
                                                   'wallet digitali come Apple Pay e Google Pay '
                                                   "dove abilitati. L'elaborazione del pagamento è "
                                                   'gestita in modo sicuro tramite '
                                                   '<strong>Stripe</strong>.'),
                                                  ('Posso avere la fattura elettronica?',
                                                   ['Sì. Al checkout scegli il profilo '
                                                    '<strong>Azienda</strong> e inserisci partita '
                                                    'IVA e Codice SDI oppure PEC: la fattura '
                                                    'elettronica viene emessa su quei dati.',
                                                    "Se ti serve dopo l'ordine, scrivi a <a "
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    "indicando l'email usata per l'ordine e il "
                                                    "numero d'ordine."])]),
                                                ('Attivazione e account',
                                                 [('Come si attiva Microsoft 365 Family dopo '
                                                   "l'acquisto?",
                                                   'Vai su <a href="https://setup.office.com/Home" '
                                                   'target="_blank" rel="noopener '
                                                   'noreferrer">setup.office.com/Home</a>, accedi '
                                                   'con il tuo account Microsoft, inserisci il '
                                                   'codice ricevuto via email e segui la procedura '
                                                   'guidata. Al termine installa le app da <a '
                                                   'href="https://www.office.com" target="_blank" '
                                                   'rel="noopener noreferrer">office.com</a>.'),
                                                  ('Posso riscattare il codice su un account '
                                                   'Microsoft che uso già?',
                                                   ['Sì: il riscatto avviene su setup.office.com '
                                                    'con il tuo account Microsoft. Se su '
                                                    "quell'account è già attivo un abbonamento "
                                                    'Microsoft 365, il comportamento (estensione o '
                                                    'conversione del piano) segue le regole '
                                                    'Microsoft mostrate durante il riscatto.',
                                                    "<strong>Scegli l'account con "
                                                    'attenzione:</strong> la licenza resta '
                                                    'associata a quello usato al momento del '
                                                    'riscatto.'])]),
                                                ('Membri e funzionalità',
                                                 [("Come si invitano altri membri dopo l'acquisto?",
                                                   "Dopo l'attivazione sul tuo account Microsoft, "
                                                   'usa le funzioni di condivisione del piano '
                                                   "Family nell'area account Microsoft / "
                                                   'abbonamenti, come indicato da Microsoft per il '
                                                   'periodo di validità della licenza.'),
                                                  ('Copilot è disponibile per tutti i membri?',
                                                   ['No. Le funzionalità Copilot comprese nel '
                                                    'piano sono utilizzabili dal <strong>titolare '
                                                    "dell'abbonamento</strong>.",
                                                    'Gli altri cinque membri ricevono le app '
                                                    'Microsoft 365, 1 TB di OneDrive ciascuno e '
                                                    'Microsoft Defender, ma non le funzionalità '
                                                    'AI.']),
                                                  ('I file sono condivisi automaticamente tra i '
                                                   'membri?',
                                                   'No. Ogni persona usa il proprio account '
                                                   'Microsoft, con documenti, email, impostazioni '
                                                   'e spazio OneDrive separati. La condivisione di '
                                                   'singoli file o cartelle resta una scelta '
                                                   'volontaria di chi li possiede.'),
                                                  ('Si possono usare le app Office anche offline?',
                                                   'Sì: con le app desktop installate puoi '
                                                   'lavorare offline; servono comunque connessione '
                                                   'e accesso periodici per la verifica della '
                                                   'licenza, aggiornamenti e servizi cloud come '
                                                   'OneDrive.')]),
                                                ('Scelta del piano e assistenza',
                                                 [('Qual è la differenza tra Microsoft 365 Family '
                                                   'e Personal?',
                                                   'Family è pensato per condividere il piano con '
                                                   'il tuo gruppo famiglia Microsoft (fino a 6 '
                                                   'persone), ciascuna con account e spazio '
                                                   'OneDrive distinti. Personal copre un solo '
                                                   'utente con 1 TB, secondo le condizioni '
                                                   'Microsoft aggiornate.'),
                                                  ('Il codice si rinnova automaticamente dopo 12 '
                                                   'mesi?',
                                                   'No. Il codice attiva Microsoft 365 Family per '
                                                   '12 mesi con un pagamento una tantum: AML Store '
                                                   'non addebita nulla automaticamente alla '
                                                   'scadenza. Eventuali opzioni di rinnovo si '
                                                   'gestiscono separatamente, direttamente '
                                                   "nell'account Microsoft."),
                                                  ('Posso usare il codice per rinnovare un '
                                                   'abbonamento Family già attivo?',
                                                   'Sì, puoi riscattarlo sullo stesso account che '
                                                   'ha già Microsoft 365 Family attivo. Il modo in '
                                                   'cui viene applicato (estensione della durata '
                                                   'attuale o avvio di un nuovo periodo) segue le '
                                                   'regole Microsoft mostrate al momento del '
                                                   'riscatto su setup.office.com, non è qualcosa '
                                                   'che decidiamo noi come rivenditore.'),
                                                  ('Cosa succede se il codice non funziona?',
                                                   ["Scrivici indicando numero d'ordine ed "
                                                    'eventuale messaggio di errore. Verifichiamo '
                                                    'il caso e, se viene confermato un difetto '
                                                    'imputabile a noi o al fornitore della chiave, '
                                                    'proponiamo sostituzione o rimborso nei tempi '
                                                    'usuali di elaborazione.',
                                                    'Assistenza: <a '
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    '— +39 392 558 0413.'])])],
                                         'en': [('Purchase and delivery',
                                                 [('When do I receive the code after payment?',
                                                   ['The delivery email is sent after payment '
                                                    'confirmation, usually within 2–15 minutes; in '
                                                    'rare cases a few extra minutes are needed for '
                                                    'payment checks.',
                                                    'If after <strong>30 minutes</strong> you have '
                                                    'received nothing, also check spam/junk and '
                                                    'email <a '
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    'with the product purchased and the email used '
                                                    'for the order.']),
                                                  ('What exactly do I receive in the email?',
                                                   ['You receive the Microsoft 365 Family '
                                                    '<strong>product key</strong> and instructions '
                                                    'to redeem it on official Microsoft portals.',
                                                    'Delivery is digital only: nothing physical is '
                                                    'shipped and there are no shipping fees.']),
                                                  ('Which payment methods can I use?',
                                                   'At checkout you can pay by card, PayPal and '
                                                   'digital wallets such as Apple Pay and Google '
                                                   'Pay where enabled. Payment processing is '
                                                   'handled securely via <strong>Stripe</strong>.'),
                                                  ('Can I get a VAT invoice?',
                                                   ['Yes. At checkout choose the '
                                                    '<strong>Business</strong> profile and enter '
                                                    'your VAT details: we issue a VAT invoice on '
                                                    'those details.',
                                                    'If you need it after the order, email <a '
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    'with the order email and order number.'])]),
                                                ('Activation and account',
                                                 [('How do I activate Microsoft 365 Family after '
                                                   'purchase?',
                                                   'Go to <a href="https://setup.office.com/Home" '
                                                   'target="_blank" rel="noopener '
                                                   'noreferrer">setup.office.com/Home</a>, sign in '
                                                   'with your Microsoft account, enter the code '
                                                   'received by email and follow the guided setup. '
                                                   'Then install the apps from <a '
                                                   'href="https://www.office.com" target="_blank" '
                                                   'rel="noopener noreferrer">office.com</a>.'),
                                                  ('Can I redeem the code on a Microsoft account I '
                                                   'already use?',
                                                   ['Yes: redemption happens on setup.office.com '
                                                    'with your Microsoft account. If that account '
                                                    'already has an active Microsoft 365 '
                                                    'subscription, the outcome (extension or plan '
                                                    "conversion) follows Microsoft's rules shown "
                                                    'during redemption.',
                                                    '<strong>Choose the account '
                                                    'carefully:</strong> the licence stays tied to '
                                                    'the one used at redemption.'])]),
                                                ('Members and features',
                                                 [('How do I invite other members after purchase?',
                                                   'After activation on your Microsoft account, '
                                                   'use the Family plan sharing features in the '
                                                   'Microsoft account / subscriptions area, as '
                                                   'directed by Microsoft for the licence term.'),
                                                  ('Is Copilot available to all members?',
                                                   ['No. Copilot features included in the plan are '
                                                    'available to the <strong>subscription '
                                                    'owner</strong>.',
                                                    'The other five members get Microsoft 365 '
                                                    'apps, 1 TB of OneDrive each and Microsoft '
                                                    'Defender, but not the AI features.']),
                                                  ('Are files shared automatically between '
                                                   'members?',
                                                   'No. Each person uses their own Microsoft '
                                                   'account, with separate documents, email, '
                                                   'settings and OneDrive space. Sharing '
                                                   'individual files or folders remains a '
                                                   'voluntary choice by the owner.'),
                                                  ('Can I use Office apps offline too?',
                                                   'Yes: with the desktop apps installed you can '
                                                   'work offline; periodic connection and sign-in '
                                                   'are still required for licence checks, updates '
                                                   'and cloud services such as OneDrive.')]),
                                                ('Plan choice and support',
                                                 [('What is the difference between Microsoft 365 '
                                                   'Family and Personal?',
                                                   'Family is designed to share the plan with your '
                                                   'Microsoft family group (up to 6 people), each '
                                                   'with a separate account and OneDrive space. '
                                                   'Personal covers a single user with 1 TB, '
                                                   "subject to Microsoft's current terms."),
                                                  ('Does the code renew automatically after 12 '
                                                   'months?',
                                                   'No. The code activates Microsoft 365 Family '
                                                   'for 12 months with a one-time payment: AML '
                                                   'Store does not charge anything automatically '
                                                   'at expiry. Any renewal options are managed '
                                                   'separately in your Microsoft account.'),
                                                  ('Can I use the code to renew an active Family '
                                                   'subscription?',
                                                   'Yes, you can redeem it on the same account '
                                                   'that already has Microsoft 365 Family active. '
                                                   'How it is applied (extending the current term '
                                                   "or starting a new period) follows Microsoft's "
                                                   'rules shown at redemption on setup.office.com '
                                                   '— it is not something we decide as a '
                                                   'reseller.'),
                                                  ('What if the code does not work?',
                                                   ['Contact us with your order number and any '
                                                    'error message. We review the case and, if a '
                                                    'defect attributable to us or the key supplier '
                                                    'is confirmed, we offer a replacement or '
                                                    'refund within usual processing times.',
                                                    'Support: <a '
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    '— +39 392 558 0413.'])])],
                                         'fr': [('Achat et livraison',
                                                 [('Quand vais-je recevoir le code après le '
                                                   'paiement ?',
                                                   ["L'e-mail de livraison part après confirmation "
                                                    'du paiement, en général sous 2 à 15 minutes ; '
                                                    'dans de rares cas, quelques minutes '
                                                    'supplémentaires sont nécessaires pour les '
                                                    'vérifications.',
                                                    'Si après <strong>30 minutes</strong> vous '
                                                    "n'avez rien reçu, vérifiez aussi les "
                                                    'indésirables et écrivez à <a '
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    "en indiquant le produit acheté et l'e-mail "
                                                    'utilisé pour la commande.']),
                                                  ("Que vais-je exactement recevoir dans l'e-mail "
                                                   '?',
                                                   ['Vous recevez la <strong>clé produit</strong> '
                                                    'Microsoft 365 Family et les instructions pour '
                                                    "l'activer sur les portails officiels "
                                                    'Microsoft.',
                                                    'La livraison est uniquement numérique : aucun '
                                                    "support physique n'est expédié et il n'y a "
                                                    'pas de frais de port.']),
                                                  ('Quels moyens de paiement puis-je utiliser ?',
                                                   'Au paiement sont disponibles carte, PayPal et '
                                                   'portefeuilles numériques comme Apple Pay et '
                                                   "Google Pay lorsqu'ils sont activés. Le "
                                                   'paiement est traité de façon sécurisée via '
                                                   '<strong>Stripe</strong>.'),
                                                  ('Puis-je obtenir une facture ?',
                                                   ['Oui. Au paiement, choisissez le profil '
                                                    '<strong>Entreprise</strong> et saisissez vos '
                                                    'données de TVA : la facture est émise sur ces '
                                                    'informations.',
                                                    'Si vous en avez besoin après la commande, '
                                                    'écrivez à <a '
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    "en indiquant l'e-mail de commande et le "
                                                    'numéro de commande.'])]),
                                                ('Activation et compte',
                                                 [('Comment activer Microsoft 365 Family après '
                                                   "l'achat ?",
                                                   'Allez sur <a '
                                                   'href="https://setup.office.com/Home" '
                                                   'target="_blank" rel="noopener '
                                                   'noreferrer">setup.office.com/Home</a>, '
                                                   'connectez-vous avec votre compte Microsoft, '
                                                   'saisissez le code reçu par e-mail et suivez '
                                                   "l'assistant. Ensuite, installez les apps "
                                                   'depuis <a href="https://www.office.com" '
                                                   'target="_blank" rel="noopener '
                                                   'noreferrer">office.com</a>.'),
                                                  ('Puis-je utiliser le code sur un compte '
                                                   "Microsoft que j'utilise déjà ?",
                                                   ["Oui : l'activation se fait sur "
                                                    'setup.office.com avec votre compte Microsoft. '
                                                    'Si un abonnement Microsoft 365 est déjà actif '
                                                    'sur ce compte, le comportement (prolongation '
                                                    'ou conversion) suit les règles Microsoft '
                                                    "affichées pendant l'activation.",
                                                    '<strong>Choisissez le compte avec attention '
                                                    ':</strong> la licence reste associée à celui '
                                                    "utilisé lors de l'activation."])]),
                                                ('Membres et fonctionnalités',
                                                 [("Comment inviter d'autres membres après l'achat "
                                                   '?',
                                                   'Après activation sur votre compte Microsoft, '
                                                   'utilisez les fonctions de partage du plan '
                                                   'Family dans la zone compte Microsoft / '
                                                   'abonnements, comme indiqué par Microsoft pour '
                                                   'la durée de la licence.'),
                                                  ('Copilot est-il disponible pour tous les '
                                                   'membres ?',
                                                   ['Non. Les fonctions Copilot incluses dans le '
                                                    'plan sont utilisables par le '
                                                    "<strong>titulaire de l'abonnement</strong>.",
                                                    'Les cinq autres membres reçoivent les apps '
                                                    "Microsoft 365, 1 To d'OneDrive chacun et "
                                                    'Microsoft Defender, mais pas les fonctions '
                                                    "d'IA."]),
                                                  ('Les fichiers sont-ils partagés automatiquement '
                                                   'entre les membres ?',
                                                   'Non. Chaque personne utilise son propre compte '
                                                   'Microsoft, avec documents, e-mails, paramètres '
                                                   'et espace OneDrive séparés. Le partage de '
                                                   'fichiers ou dossiers individuels reste un '
                                                   'choix volontaire du propriétaire.'),
                                                  ('Peut-on utiliser les apps Office hors ligne ?',
                                                   'Oui : avec les apps de bureau installées, vous '
                                                   'pouvez travailler hors ligne ; une connexion '
                                                   'et une connexion périodiques restent '
                                                   'nécessaires pour la vérification de licence, '
                                                   'les mises à jour et les services cloud comme '
                                                   'OneDrive.')]),
                                                ('Choix du plan et assistance',
                                                 [('Quelle est la différence entre Microsoft 365 '
                                                   'Family et Personal ?',
                                                   'Family est conçu pour partager le plan avec '
                                                   "votre groupe famille Microsoft (jusqu'à 6 "
                                                   'personnes), chacune avec un compte et un '
                                                   'espace OneDrive distincts. Personal couvre un '
                                                   'seul utilisateur avec 1 To, selon les '
                                                   'conditions Microsoft à jour.'),
                                                  ('Le code se renouvelle-t-il automatiquement '
                                                   'après 12 mois ?',
                                                   'Non. Le code active Microsoft 365 Family pour '
                                                   '12 mois avec un paiement unique : AML Store ne '
                                                   "prélève rien automatiquement à l'échéance. Les "
                                                   'options de renouvellement éventuelles se '
                                                   'gèrent séparément dans le compte Microsoft.'),
                                                  ('Puis-je utiliser le code pour renouveler un '
                                                   'abonnement Family déjà actif ?',
                                                   "Oui, vous pouvez l'activer sur le même compte "
                                                   'qui a déjà Microsoft 365 Family. La façon dont '
                                                   "il s'applique (prolongation de la durée "
                                                   'actuelle ou nouveau période) suit les règles '
                                                   "Microsoft affichées lors de l'activation sur "
                                                   "setup.office.com — ce n'est pas nous qui le "
                                                   'décidons en tant que revendeur.'),
                                                  ('Que se passe-t-il si le code ne fonctionne pas '
                                                   '?',
                                                   ['Écrivez-nous en indiquant le numéro de '
                                                    "commande et le message d'erreur éventuel. "
                                                    'Nous examinons le cas et, si un défaut '
                                                    'imputable à nous ou au fournisseur de la clé '
                                                    'est confirmé, nous proposons un remplacement '
                                                    'ou un remboursement dans les délais '
                                                    'habituels.',
                                                    'Assistance : <a '
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    '— +39 392 558 0413.'])])],
                                         'de': [('Kauf und Lieferung',
                                                 [('Wann erhalte ich den Code nach der Zahlung?',
                                                   ['Die Liefer-E-Mail wird nach '
                                                    'Zahlungsbestätigung versendet, in der Regel '
                                                    'innerhalb von 2–15 Minuten; in seltenen '
                                                    'Fällen dauern Zahlungsprüfungen etwas länger.',
                                                    'Wenn Sie nach <strong>30 Minuten</strong> '
                                                    'nichts erhalten haben, prüfen Sie auch '
                                                    'Spam/Junk und schreiben Sie an <a '
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    'mit dem gekauften Produkt und der für die '
                                                    'Bestellung verwendeten E-Mail-Adresse.']),
                                                  ('Was genau erhalte ich in der E-Mail?',
                                                   ['Sie erhalten den <strong>Product Key</strong> '
                                                    'für Microsoft 365 Family sowie Anweisungen '
                                                    'zur Einlösung auf den offiziellen '
                                                    'Microsoft-Portalen.',
                                                    'Die Lieferung erfolgt ausschließlich digital: '
                                                    'Es wird nichts physisch versendet und es '
                                                    'fallen keine Versandkosten an.']),
                                                  ('Welche Zahlungsmethoden kann ich nutzen?',
                                                   'Beim Checkout können Sie mit Karte, PayPal und '
                                                   'digitalen Wallets wie Apple Pay und Google Pay '
                                                   'zahlen, sofern freigeschaltet. Die '
                                                   'Zahlungsabwicklung erfolgt sicher über '
                                                   '<strong>Stripe</strong>.'),
                                                  ('Kann ich eine MwSt.-Rechnung erhalten?',
                                                   ['Ja. Wählen Sie beim Checkout das Profil '
                                                    '<strong>Unternehmen</strong> und geben Sie '
                                                    'Ihre MwSt.-Daten ein: Wir stellen die '
                                                    'MwSt.-Rechnung auf diese Daten aus.',
                                                    'Wenn Sie sie nach der Bestellung benötigen, '
                                                    'schreiben Sie an <a '
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    'mit der Bestell-E-Mail und der '
                                                    'Bestellnummer.'])]),
                                                ('Aktivierung und Konto',
                                                 [('Wie aktiviere ich Microsoft 365 Family nach '
                                                   'dem Kauf?',
                                                   'Rufen Sie <a '
                                                   'href="https://setup.office.com/Home" '
                                                   'target="_blank" rel="noopener '
                                                   'noreferrer">setup.office.com/Home</a> auf, '
                                                   'melden Sie sich mit Ihrem Microsoft-Konto an, '
                                                   'geben Sie den per E-Mail erhaltenen Code ein '
                                                   'und folgen Sie dem Einrichtungsassistenten. '
                                                   'Installieren Sie anschließend die Apps von <a '
                                                   'href="https://www.office.com" target="_blank" '
                                                   'rel="noopener noreferrer">office.com</a>.'),
                                                  ('Kann ich den Code auf einem Microsoft-Konto '
                                                   'einlösen, das ich bereits nutze?',
                                                   ['Ja: Die Einlösung erfolgt auf '
                                                    'setup.office.com mit Ihrem Microsoft-Konto. '
                                                    'Wenn dieses Konto bereits ein aktives '
                                                    'Microsoft 365-Abonnement hat, richtet sich '
                                                    'das Ergebnis (Verlängerung oder Planwechsel) '
                                                    'nach den Microsoft-Regeln, die bei der '
                                                    'Einlösung angezeigt werden.',
                                                    '<strong>Wählen Sie das Konto '
                                                    'sorgfältig:</strong> Die Lizenz bleibt an das '
                                                    'bei der Einlösung verwendete Konto '
                                                    'gebunden.'])]),
                                                ('Mitglieder und Funktionen',
                                                 [('Wie lade ich nach dem Kauf weitere Mitglieder '
                                                   'ein?',
                                                   'Nach der Aktivierung auf Ihrem Microsoft-Konto '
                                                   'nutzen Sie die Freigabefunktionen des '
                                                   'Family-Plans im Bereich Microsoft-Konto / '
                                                   'Abonnements, wie von Microsoft für die '
                                                   'Lizenzlaufzeit vorgesehen.'),
                                                  ('Ist Copilot für alle Mitglieder verfügbar?',
                                                   ['Nein. Die im Plan enthaltenen '
                                                    'Copilot-Funktionen stehen dem '
                                                    '<strong>Abonnementinhaber</strong> zur '
                                                    'Verfügung.',
                                                    'Die anderen fünf Mitglieder erhalten '
                                                    'Microsoft 365 Apps, jeweils 1 TB OneDrive und '
                                                    'Microsoft Defender, jedoch nicht die '
                                                    'KI-Funktionen.']),
                                                  ('Werden Dateien automatisch zwischen '
                                                   'Mitgliedern geteilt?',
                                                   'Nein. Jede Person nutzt ihr eigenes '
                                                   'Microsoft-Konto mit getrennten Dokumenten, '
                                                   'E-Mails, Einstellungen und OneDrive-Speicher. '
                                                   'Das Teilen einzelner Dateien oder Ordner '
                                                   'bleibt eine freiwillige Entscheidung des '
                                                   'Besitzers.'),
                                                  ('Kann ich Office-Apps auch offline nutzen?',
                                                   'Ja: Mit den installierten Desktop-Apps können '
                                                   'Sie offline arbeiten; für Lizenzprüfungen, '
                                                   'Updates und Cloud-Dienste wie OneDrive sind '
                                                   'weiterhin eine gelegentliche Verbindung und '
                                                   'Anmeldung erforderlich.')]),
                                                ('Planwahl und Support',
                                                 [('Was ist der Unterschied zwischen Microsoft 365 '
                                                   'Family und Personal?',
                                                   'Family ist zum Teilen des Plans mit Ihrer '
                                                   'Microsoft-Familiengruppe gedacht (bis zu 6 '
                                                   'Personen), jeweils mit eigenem Konto und '
                                                   'OneDrive-Speicher. Personal gilt für einen '
                                                   'einzelnen Nutzer mit 1 TB, gemäß den aktuellen '
                                                   'Microsoft-Bedingungen.'),
                                                  ('Verlängert sich der Code nach 12 Monaten '
                                                   'automatisch?',
                                                   'Nein. Der Code aktiviert Microsoft 365 Family '
                                                   'für 12 Monate mit einer einmaligen Zahlung: '
                                                   'AML Store belastet bei Ablauf nichts '
                                                   'automatisch. Etwaige Verlängerungsoptionen '
                                                   'verwalten Sie separat in Ihrem '
                                                   'Microsoft-Konto.'),
                                                  ('Kann ich den Code zur Verlängerung eines '
                                                   'aktiven Family-Abonnements nutzen?',
                                                   'Ja, Sie können ihn auf demselben Konto '
                                                   'einlösen, auf dem Microsoft 365 Family bereits '
                                                   'aktiv ist. Wie er angewendet wird '
                                                   '(Verlängerung der aktuellen Laufzeit oder '
                                                   'Beginn einer neuen Periode) richtet sich nach '
                                                   'den Microsoft-Regeln, die bei der Einlösung '
                                                   'auf setup.office.com angezeigt werden — das '
                                                   'entscheiden nicht wir als Händler.'),
                                                  ('Was tun, wenn der Code nicht funktioniert?',
                                                   ['Kontaktieren Sie uns mit Ihrer Bestellnummer '
                                                    'und einer etwaigen Fehlermeldung. Wir prüfen '
                                                    'den Fall und bieten bei einem nachweislich '
                                                    'uns oder dem Key-Lieferanten zurechenbaren '
                                                    'Defekt Ersatz oder Erstattung innerhalb der '
                                                    'üblichen Bearbeitungszeiten.',
                                                    'Support: <a '
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    '— +39 392 558 0413.'])])],
                                         'es': [('Compra y entrega',
                                                 [('¿Cuándo recibo el código después del pago?',
                                                   ['El email de entrega se envía tras la '
                                                    'confirmación del pago, normalmente en 2–15 '
                                                    'minutos; en casos excepcionales pueden hacer '
                                                    'falta unos minutos más para las '
                                                    'comprobaciones del pago.',
                                                    'Si tras <strong>30 minutos</strong> no has '
                                                    'recibido nada, revisa también spam/correo no '
                                                    'deseado y escribe a <a '
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    'indicando el producto comprado y el email '
                                                    'usado en el pedido.']),
                                                  ('¿Qué recibo exactamente en el email?',
                                                   ['Recibes la <strong>clave de producto</strong> '
                                                    'de Microsoft 365 Family y las instrucciones '
                                                    'para canjearla en los portales oficiales de '
                                                    'Microsoft.',
                                                    'La entrega es solo digital: no se envía nada '
                                                    'físico y no hay gastos de envío.']),
                                                  ('¿Qué métodos de pago puedo usar?',
                                                   'En el checkout puedes pagar con tarjeta, '
                                                   'PayPal y monederos digitales como Apple Pay y '
                                                   'Google Pay donde estén habilitados. El '
                                                   'procesamiento del pago se gestiona de forma '
                                                   'segura a través de <strong>Stripe</strong>.'),
                                                  ('¿Puedo obtener factura con IVA?',
                                                   ['Sí. En el checkout elige el perfil '
                                                    '<strong>Empresa</strong> e introduce tus '
                                                    'datos de IVA: emitimos la factura con IVA con '
                                                    'esos datos.',
                                                    'Si la necesitas después del pedido, escribe a '
                                                    '<a '
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    'con el email del pedido y el número de '
                                                    'pedido.'])]),
                                                ('Activación y cuenta',
                                                 [('¿Cómo activo Microsoft 365 Family después de '
                                                   'la compra?',
                                                   'Ve a <a href="https://setup.office.com/Home" '
                                                   'target="_blank" rel="noopener '
                                                   'noreferrer">setup.office.com/Home</a>, inicia '
                                                   'sesión con tu cuenta Microsoft, introduce el '
                                                   'código recibido por email y sigue el asistente '
                                                   'de configuración. Después instala las apps '
                                                   'desde <a href="https://www.office.com" '
                                                   'target="_blank" rel="noopener '
                                                   'noreferrer">office.com</a>.'),
                                                  ('¿Puedo canjear el código en una cuenta '
                                                   'Microsoft que ya uso?',
                                                   ['Sí: el canje se realiza en setup.office.com '
                                                    'con tu cuenta Microsoft. Si esa cuenta ya '
                                                    'tiene una suscripción Microsoft 365 activa, '
                                                    'el resultado (prórroga o conversión de plan) '
                                                    'sigue las reglas de Microsoft mostradas '
                                                    'durante el canje.',
                                                    '<strong>Elige la cuenta con cuidado:</strong> '
                                                    'la licencia queda vinculada a la usada en el '
                                                    'canje.'])]),
                                                ('Miembros y funciones',
                                                 [('¿Cómo invito a otros miembros después de la '
                                                   'compra?',
                                                   'Tras la activación en tu cuenta Microsoft, usa '
                                                   'las funciones para compartir el plan Family en '
                                                   'el área de cuenta Microsoft / suscripciones, '
                                                   'según las indicaciones de Microsoft durante la '
                                                   'vigencia de la licencia.'),
                                                  ('¿Copilot está disponible para todos los '
                                                   'miembros?',
                                                   ['No. Las funciones de Copilot incluidas en el '
                                                    'plan están disponibles para el '
                                                    '<strong>titular de la suscripción</strong>.',
                                                    'Los otros cinco miembros obtienen las apps '
                                                    'Microsoft 365, 1 TB de OneDrive cada uno y '
                                                    'Microsoft Defender, pero no las funciones de '
                                                    'IA.']),
                                                  ('¿Los archivos se comparten automáticamente '
                                                   'entre los miembros?',
                                                   'No. Cada persona usa su propia cuenta '
                                                   'Microsoft, con documentos, email, ajustes y '
                                                   'espacio OneDrive separados. Compartir archivos '
                                                   'o carpetas concretos sigue siendo una elección '
                                                   'voluntaria del propietario.'),
                                                  ('¿Puedo usar también las apps de Office sin '
                                                   'conexión?',
                                                   'Sí: con las aplicaciones de escritorio '
                                                   'instaladas puedes trabajar sin conexión; aun '
                                                   'así se requieren conexión e inicio de sesión '
                                                   'periódicos para la verificación de la '
                                                   'licencia, las actualizaciones y los servicios '
                                                   'en la nube como OneDrive.')]),
                                                ('Elección del plan y soporte',
                                                 [('¿Cuál es la diferencia entre Microsoft 365 '
                                                   'Family y Personal?',
                                                   'Family está pensado para compartir el plan con '
                                                   'tu grupo familiar de Microsoft (hasta 6 '
                                                   'personas), cada una con una cuenta y espacio '
                                                   'OneDrive propios. Personal cubre a un solo '
                                                   'usuario con 1 TB, según las condiciones '
                                                   'vigentes de Microsoft.'),
                                                  ('¿El código se renueva automáticamente después '
                                                   'de 12 meses?',
                                                   'No. El código activa Microsoft 365 Family '
                                                   'durante 12 meses con un pago único: AML Store '
                                                   'no cobra nada automáticamente al vencimiento. '
                                                   'Cualquier opción de renovación se gestiona por '
                                                   'separado en tu cuenta Microsoft.'),
                                                  ('¿Puedo usar el código para renovar una '
                                                   'suscripción Family activa?',
                                                   'Sí, puedes canjearlo en la misma cuenta que ya '
                                                   'tiene Microsoft 365 Family activo. Cómo se '
                                                   'aplica (prorrogar el periodo actual o iniciar '
                                                   'uno nuevo) sigue las reglas de Microsoft '
                                                   'mostradas en el canje en setup.office.com: no '
                                                   'es algo que decidamos nosotros como '
                                                   'revendedor.'),
                                                  ('¿Qué pasa si el código no funciona?',
                                                   ['Contáctanos con tu número de pedido y '
                                                    'cualquier mensaje de error. Revisamos el caso '
                                                    'y, si se confirma un defecto imputable a '
                                                    'nosotros o al proveedor de la clave, '
                                                    'ofrecemos sustitución o reembolso en los '
                                                    'plazos habituales de gestión.',
                                                    'Soporte: <a '
                                                    'href="mailto:Info@amlstore.it">Info@amlstore.it</a> '
                                                    '— +39 392 558 0413.'])])]},
                          'bonus': {'it': "<strong>Incluso con l'acquisto:</strong> guida PDF "
                                          "all'utilizzo di Copilot, via email dopo l'ordine",
                                    'en': '<strong>Included with your purchase:</strong> Copilot '
                                          'PDF guide, sent by email after the order',
                                    'fr': "<strong>Inclus avec l'achat :</strong> guide PDF "
                                          'Copilot, envoyé par e-mail après la commande',
                                    'de': '<strong>Im Kauf enthalten:</strong> '
                                          'Copilot-PDF-Leitfaden, nach der Bestellung per E-Mail',
                                    'es': '<strong>Incluido con tu compra:</strong> guía PDF de '
                                          'Copilot, enviada por email tras el pedido'},
                          'stats': {'it': {'eyebrow': 'Cosa ricevi',
                                           'title': 'Sei persone, account e spazi separati',
                                           'sub': 'Microsoft 365 Family è pensato per essere '
                                                  'condiviso: ogni persona lavora sul proprio '
                                                  'account, con il proprio spazio cloud.',
                                           'rows': [('6',
                                                     'Persone incluse',
                                                     'Titolare più 5 membri invitati, ognuno con '
                                                     'account Microsoft separato.'),
                                                    ('1 TB',
                                                     'OneDrive a persona',
                                                     'Fino a 6 TB complessivi sul piano, non '
                                                     'condivisi automaticamente.'),
                                                    ('12 mesi',
                                                     'Durata',
                                                     'Pagamento una tantum su AML Store, senza '
                                                     'addebiti ricorrenti da parte nostra.'),
                                                    ('5',
                                                     'Dispositivi per persona',
                                                     'Accesso contemporaneo su PC, Mac, tablet e '
                                                     'telefono, secondo le regole Microsoft.')]},
                                    'en': {'eyebrow': 'What you get',
                                           'title': 'Six people, separate accounts and storage',
                                           'sub': 'Microsoft 365 Family is built to be shared: '
                                                  'each person works on their own account, with '
                                                  'their own cloud storage.',
                                           'rows': [('6',
                                                     'People included',
                                                     'Owner plus 5 invited members, each with a '
                                                     'separate Microsoft account.'),
                                                    ('1 TB',
                                                     'OneDrive per person',
                                                     'Up to 6 TB total on the plan, not shared '
                                                     'automatically.'),
                                                    ('12 months',
                                                     'Term',
                                                     'One-time payment on AML Store, with no '
                                                     'recurring charges from us.'),
                                                    ('5',
                                                     'Devices per person',
                                                     'Simultaneous access on PC, Mac, tablet and '
                                                     'phone, subject to Microsoft rules.')]},
                                    'fr': {'eyebrow': 'Ce que vous recevez',
                                           'title': 'Six personnes, comptes et espaces séparés',
                                           'sub': 'Microsoft 365 Family est conçu pour être '
                                                  'partagé : chaque personne travaille sur son '
                                                  'propre compte, avec son propre espace cloud.',
                                           'rows': [('6',
                                                     'Personnes incluses',
                                                     'Titulaire plus 5 membres invités, chacun '
                                                     'avec un compte Microsoft séparé.'),
                                                    ('1 TB',
                                                     'OneDrive par personne',
                                                     "Jusqu'à 6 To au total sur le plan, non "
                                                     'partagés automatiquement.'),
                                                    ('12 mois',
                                                     'Durée',
                                                     'Paiement unique sur AML Store, sans '
                                                     'prélèvement récurrent de notre part.'),
                                                    ('5',
                                                     'Appareils par personne',
                                                     'Accès simultané sur PC, Mac, tablette et '
                                                     'téléphone, selon les règles Microsoft.')]},
                                    'de': {'eyebrow': 'Was Sie erhalten',
                                           'title': 'Sechs Personen, getrennte Konten und Speicher',
                                           'sub': 'Microsoft 365 Family ist zum Teilen gedacht: '
                                                  'Jede Person arbeitet auf ihrem eigenen Konto '
                                                  'mit eigenem Cloud-Speicher.',
                                           'rows': [('6',
                                                     'Personen inklusive',
                                                     'Inhaber plus 5 eingeladene Mitglieder, '
                                                     'jeweils mit eigenem Microsoft-Konto.'),
                                                    ('1 TB',
                                                     'OneDrive pro Person',
                                                     'Bis zu 6 TB insgesamt im Plan, nicht '
                                                     'automatisch geteilt.'),
                                                    ('12 Monate',
                                                     'Laufzeit',
                                                     'Einmalzahlung bei AML Store, ohne '
                                                     'wiederkehrende Belastung durch uns.'),
                                                    ('5',
                                                     'Geräte pro Person',
                                                     'Gleichzeitiger Zugriff auf PC, Mac, Tablet '
                                                     'und Smartphone, gemäß Microsoft-Regeln.')]},
                                    'es': {'eyebrow': 'Qué recibes',
                                           'title': 'Seis personas, cuentas y almacenamiento '
                                                    'separados',
                                           'sub': 'Microsoft 365 Family está pensado para '
                                                  'compartir: cada persona trabaja en su propia '
                                                  'cuenta, con su propio almacenamiento en la '
                                                  'nube.',
                                           'rows': [('6',
                                                     'Personas incluidas',
                                                     'Titular más 5 miembros invitados, cada uno '
                                                     'con una cuenta Microsoft distinta.'),
                                                    ('1 TB',
                                                     'OneDrive por persona',
                                                     'Hasta 6 TB en total en el plan, no '
                                                     'compartidos automáticamente.'),
                                                    ('12 meses',
                                                     'Duración',
                                                     'Pago único en AML Store, sin cargos '
                                                     'recurrentes por nuestra parte.'),
                                                    ('5',
                                                     'Dispositivos por persona',
                                                     'Acceso simultáneo en PC, Mac, tablet y '
                                                     'móvil, según las reglas de Microsoft.')]}},
                          'specs_table': {'it': {'eyebrow': 'Specifiche del prodotto',
                                                 'title': 'Scheda tecnica',
                                                 'caption': 'Specifiche tecniche e commerciali di '
                                                            'Microsoft 365 Family',
                                                 'rows': [('Prodotto', 'Microsoft 365 Family'),
                                                          ('Durata', '12 mesi'),
                                                          ('Utenti', 'Fino a 6 persone'),
                                                          ('Archiviazione',
                                                           '1 TB OneDrive per persona'),
                                                          ('Dispositivi',
                                                           'Fino a 5 contemporanei per persona'),
                                                          ('Copilot',
                                                           'Incluso per il titolare '
                                                           "dell'abbonamento"),
                                                          ('Consegna', 'Codice digitale via email'),
                                                          ('Attivazione',
                                                           'Account Microsoft, su '
                                                           'setup.office.com'),
                                                          ('Rinnovo',
                                                           'Nuova attivazione o estensione secondo '
                                                           'le regole Microsoft'),
                                                          ('Codice prodotto', '@sku'),
                                                          ('Regione di attivazione',
                                                           'Unione Europea / SEE'),
                                                          ('Fatturazione',
                                                           'IVA inclusa, fattura elettronica '
                                                           'disponibile')]},
                                          'en': {'eyebrow': 'Product specifications',
                                                 'title': 'Tech sheet',
                                                 'caption': 'Technical and commercial '
                                                            'specifications for Microsoft 365 '
                                                            'Family',
                                                 'rows': [('Product', 'Microsoft 365 Family'),
                                                          ('Term', '12 months'),
                                                          ('Users', 'Up to 6 people'),
                                                          ('Storage', '1 TB OneDrive per person'),
                                                          ('Devices',
                                                           'Up to 5 simultaneous per person'),
                                                          ('Copilot',
                                                           'Included for the subscription owner'),
                                                          ('Delivery', 'Digital code by email'),
                                                          ('Activation',
                                                           'Microsoft account, on '
                                                           'setup.office.com'),
                                                          ('Renewal',
                                                           'New activation or extension per '
                                                           'Microsoft rules'),
                                                          ('Product code', '@sku'),
                                                          ('Activation region',
                                                           'European Union / EEA'),
                                                          ('Billing',
                                                           'Tax included, VAT invoice available')]},
                                          'fr': {'eyebrow': 'Spécifications du produit',
                                                 'title': 'Fiche technique',
                                                 'caption': 'Spécifications techniques et '
                                                            'commerciales de Microsoft 365 Family',
                                                 'rows': [('Produit', 'Microsoft 365 Family'),
                                                          ('Durée', '12 mois'),
                                                          ('Utilisateurs', "Jusqu'à 6 personnes"),
                                                          ('Stockage',
                                                           '1 To OneDrive par personne'),
                                                          ('Appareils',
                                                           "Jusqu'à 5 simultanés par personne"),
                                                          ('Copilot',
                                                           'Inclus pour le titulaire de '
                                                           "l'abonnement"),
                                                          ('Livraison',
                                                           'Code numérique par e-mail'),
                                                          ('Activation',
                                                           'Compte Microsoft, sur '
                                                           'setup.office.com'),
                                                          ('Renouvellement',
                                                           'Nouvelle activation ou prolongation '
                                                           'selon les règles Microsoft'),
                                                          ('Code produit', '@sku'),
                                                          ("Zone d'activation",
                                                           'Union européenne / EEE'),
                                                          ('Facturation',
                                                           'TVA incluse, facture disponible')]},
                                          'de': {'eyebrow': 'Produktspezifikationen',
                                                 'title': 'Technisches Datenblatt',
                                                 'caption': 'Technische und kommerzielle '
                                                            'Spezifikationen für Microsoft 365 '
                                                            'Family',
                                                 'rows': [('Produkt', 'Microsoft 365 Family'),
                                                          ('Laufzeit', '12 Monate'),
                                                          ('Nutzer', 'Bis zu 6 Personen'),
                                                          ('Speicher', '1 TB OneDrive pro Person'),
                                                          ('Geräte',
                                                           'Bis zu 5 gleichzeitig pro Person'),
                                                          ('Copilot',
                                                           'Enthalten für den Abonnementinhaber'),
                                                          ('Lieferung',
                                                           'Digitaler Code per E-Mail'),
                                                          ('Aktivierung',
                                                           'Microsoft-Konto, auf setup.office.com'),
                                                          ('Verlängerung',
                                                           'Neue Aktivierung oder Verlängerung '
                                                           'gemäß Microsoft-Regeln'),
                                                          ('Artikelnummer', '@sku'),
                                                          ('Aktivierungsregion',
                                                           'Europäische Union / EWR'),
                                                          ('Abrechnung',
                                                           'Steuern inklusive, MwSt.-Rechnung '
                                                           'verfügbar')]},
                                          'es': {'eyebrow': 'Especificaciones del producto',
                                                 'title': 'Ficha técnica',
                                                 'caption': 'Especificaciones técnicas y '
                                                            'comerciales de Microsoft 365 Family',
                                                 'rows': [('Producto', 'Microsoft 365 Family'),
                                                          ('Duración', '12 meses'),
                                                          ('Usuarios', 'Hasta 6 personas'),
                                                          ('Almacenamiento',
                                                           '1 TB OneDrive por persona'),
                                                          ('Dispositivos',
                                                           'Hasta 5 simultáneos por persona'),
                                                          ('Copilot',
                                                           'Incluido para el titular de la '
                                                           'suscripción'),
                                                          ('Entrega', 'Código digital por email'),
                                                          ('Activación',
                                                           'Cuenta Microsoft, en setup.office.com'),
                                                          ('Renovación',
                                                           'Nueva activación o prórroga según las '
                                                           'reglas de Microsoft'),
                                                          ('Código de producto', '@sku'),
                                                          ('Región de activación',
                                                           'Unión Europea / EEE'),
                                                          ('Facturación',
                                                           'Impuestos incluidos, factura con IVA '
                                                           'disponible')]}},
                          'roles': {'it': {'eyebrow': 'Chi riceve cosa',
                                           'title': 'Un abbonamento condiviso, sei esperienze '
                                                    'separate',
                                           'sub': 'Ogni persona utilizza il proprio account '
                                                  'Microsoft. Documenti, email, fotografie e '
                                                  'spazio cloud non vengono condivisi '
                                                  "automaticamente con gli altri membri. L'unica "
                                                  'differenza reale riguarda le funzionalità '
                                                  'Copilot.',
                                           'caption': "Confronto tra titolare dell'abbonamento e "
                                                      'altri membri del gruppo famiglia',
                                           'cols': ['Funzionalità', 'Titolare', 'Altri 5 membri'],
                                           'rows': [('Word, Excel, PowerPoint e Outlook',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('1 TB di OneDrive personale',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Account, file e impostazioni separati',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Installazione su più dispositivi',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Microsoft Defender',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Funzionalità Copilot',
                                                     'Le funzioni AI comprese nel piano restano al '
                                                     "proprietario dell'abbonamento.",
                                                     True,
                                                     'yes',
                                                     'no')],
                                           'yes_label': 'Incluso',
                                           'no_label': 'Non incluso'},
                                    'en': {'eyebrow': 'Who gets what',
                                           'title': 'One shared subscription, six separate '
                                                    'experiences',
                                           'sub': 'Each person uses their own Microsoft account. '
                                                  'Documents, email, photos and cloud storage are '
                                                  'not shared automatically with other members. '
                                                  'The only real difference is Copilot features.',
                                           'caption': 'Comparison between subscription owner and '
                                                      'other family group members',
                                           'cols': ['Feature', 'Owner', 'Other 5 members'],
                                           'rows': [('Word, Excel, PowerPoint and Outlook',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('1 TB of personal OneDrive',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Separate accounts, files and settings',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Install on multiple devices',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Microsoft Defender',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Copilot features',
                                                     'AI features included in the plan stay with '
                                                     'the subscription owner.',
                                                     True,
                                                     'yes',
                                                     'no')],
                                           'yes_label': 'Included',
                                           'no_label': 'Not included'},
                                    'fr': {'eyebrow': 'Qui reçoit quoi',
                                           'title': 'Un abonnement partagé, six expériences '
                                                    'séparées',
                                           'sub': 'Chaque personne utilise son propre compte '
                                                  'Microsoft. Documents, e-mails, photos et espace '
                                                  'cloud ne sont pas partagés automatiquement avec '
                                                  'les autres membres. La seule vraie différence '
                                                  'concerne les fonctions Copilot.',
                                           'caption': 'Comparaison entre le titulaire de '
                                                      "l'abonnement et les autres membres du "
                                                      'groupe famille',
                                           'cols': ['Fonctionnalité',
                                                    'Titulaire',
                                                    '5 autres membres'],
                                           'rows': [('Word, Excel, PowerPoint et Outlook',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ("1 To d'OneDrive personnel",
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Comptes, fichiers et paramètres séparés',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Installation sur plusieurs appareils',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Microsoft Defender',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Fonctions Copilot',
                                                     "Les fonctions d'IA incluses dans le plan "
                                                     "restent au propriétaire de l'abonnement.",
                                                     True,
                                                     'yes',
                                                     'no')],
                                           'yes_label': 'Inclus',
                                           'no_label': 'Non inclus'},
                                    'de': {'eyebrow': 'Wer erhält was',
                                           'title': 'Ein gemeinsames Abo, sechs getrennte '
                                                    'Erlebnisse',
                                           'sub': 'Jede Person nutzt ihr eigenes Microsoft-Konto. '
                                                  'Dokumente, E-Mails, Fotos und Cloud-Speicher '
                                                  'werden nicht automatisch mit anderen '
                                                  'Mitgliedern geteilt. Der einzige echte '
                                                  'Unterschied sind die Copilot-Funktionen.',
                                           'caption': 'Vergleich zwischen Abonnementinhaber und '
                                                      'anderen Mitgliedern der Familiengruppe',
                                           'cols': ['Funktion', 'Inhaber', 'Andere 5 Mitglieder'],
                                           'rows': [('Word, Excel, PowerPoint und Outlook',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('1 TB persönliches OneDrive',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Getrennte Konten, Dateien und Einstellungen',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Installation auf mehreren Geräten',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Microsoft Defender',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Copilot-Funktionen',
                                                     'Die im Plan enthaltenen KI-Funktionen '
                                                     'bleiben beim Abonnementinhaber.',
                                                     True,
                                                     'yes',
                                                     'no')],
                                           'yes_label': 'Enthalten',
                                           'no_label': 'Nicht enthalten'},
                                    'es': {'eyebrow': 'Quién recibe qué',
                                           'title': 'Una suscripción compartida, seis experiencias '
                                                    'separadas',
                                           'sub': 'Cada persona usa su propia cuenta Microsoft. '
                                                  'Documentos, email, fotos y almacenamiento en la '
                                                  'nube no se comparten automáticamente con los '
                                                  'demás miembros. La única diferencia real son '
                                                  'las funciones de Copilot.',
                                           'caption': 'Comparación entre el titular de la '
                                                      'suscripción y los demás miembros del grupo '
                                                      'familiar',
                                           'cols': ['Función', 'Titular', 'Otros 5 miembros'],
                                           'rows': [('Word, Excel, PowerPoint y Outlook',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('1 TB de OneDrive personal',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Cuentas, archivos y ajustes separados',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Instalación en varios dispositivos',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Microsoft Defender',
                                                     None,
                                                     False,
                                                     'yes',
                                                     'yes'),
                                                    ('Funciones de Copilot',
                                                     'Las funciones de IA incluidas en el plan '
                                                     'permanecen con el titular de la suscripción.',
                                                     True,
                                                     'yes',
                                                     'no')],
                                           'yes_label': 'Incluido',
                                           'no_label': 'No incluido'}},
                          'seats': {'it': {'eyebrow': 'Condivisione',
                                           'title': 'Un piano, account separati',
                                           'sub': 'Inviti fino a cinque persone dal tuo account '
                                                  'Microsoft. Ognuna riceve il proprio spazio '
                                                  'cloud, le proprie app e le proprie '
                                                  'impostazioni: nessuno vede i documenti degli '
                                                  'altri.',
                                           'list_aria': 'Le sei postazioni del piano',
                                           'foot': 'Tutti ricevono le stesse app. Cambia solo '
                                                   'Copilot, che resta al titolare.',
                                           'rows': [('Titolare', '1 TB <b>+ Copilot</b>', True),
                                                    ('Membro 2', '1 TB', False),
                                                    ('Membro 3', '1 TB', False),
                                                    ('Membro 4', '1 TB', False),
                                                    ('Membro 5', '1 TB', False),
                                                    ('Membro 6', '1 TB', False)],
                                           'media_src': '../asset/media/m365-family-lifestyle-bridge.webp',
                                           'media_alt': 'Famiglia che usa laptop e dispositivi '
                                                        'insieme in un ambiente domestico luminoso '
                                                        'e moderno.'},
                                    'en': {'eyebrow': 'Sharing',
                                           'title': 'One plan, separate accounts',
                                           'sub': 'Invite up to five people from your Microsoft '
                                                  'account. Each gets their own cloud storage, '
                                                  "apps and settings: nobody sees anyone else's "
                                                  'documents.',
                                           'list_aria': 'The six seats on the plan',
                                           'foot': 'Everyone gets the same apps. Only Copilot '
                                                   'differs — it stays with the owner.',
                                           'rows': [('Owner', '1 TB <b>+ Copilot</b>', True),
                                                    ('Member 2', '1 TB', False),
                                                    ('Member 3', '1 TB', False),
                                                    ('Member 4', '1 TB', False),
                                                    ('Member 5', '1 TB', False),
                                                    ('Member 6', '1 TB', False)],
                                           'media_src': '../asset/media/m365-family-lifestyle-bridge.webp',
                                           'media_alt': 'Family using laptops and devices together '
                                                        'in a bright, modern home.'},
                                    'fr': {'eyebrow': 'Partage',
                                           'title': 'Un plan, des comptes séparés',
                                           'sub': "Invitez jusqu'à cinq personnes depuis votre "
                                                  'compte Microsoft. Chacune reçoit son propre '
                                                  'espace cloud, ses apps et ses paramètres : '
                                                  'personne ne voit les documents des autres.',
                                           'list_aria': 'Les six places du plan',
                                           'foot': 'Tout le monde reçoit les mêmes apps. Seul '
                                                   'Copilot diffère — il reste au titulaire.',
                                           'rows': [('Titulaire', '1 TB <b>+ Copilot</b>', True),
                                                    ('Membre 2', '1 TB', False),
                                                    ('Membre 3', '1 TB', False),
                                                    ('Membre 4', '1 TB', False),
                                                    ('Membre 5', '1 TB', False),
                                                    ('Membre 6', '1 TB', False)],
                                           'media_src': '../asset/media/m365-family-lifestyle-bridge.webp',
                                           'media_alt': 'Famille utilisant ordinateurs et '
                                                        'appareils ensemble dans un intérieur '
                                                        'lumineux et moderne.'},
                                    'de': {'eyebrow': 'Teilen',
                                           'title': 'Ein Plan, getrennte Konten',
                                           'sub': 'Laden Sie bis zu fünf Personen von Ihrem '
                                                  'Microsoft-Konto aus ein. Jede erhält eigenen '
                                                  'Cloud-Speicher, Apps und Einstellungen: Niemand '
                                                  'sieht die Dokumente der anderen.',
                                           'list_aria': 'Die sechs Plätze im Plan',
                                           'foot': 'Alle erhalten dieselben Apps. Nur Copilot '
                                                   'unterscheidet sich — er bleibt beim Inhaber.',
                                           'rows': [('Inhaber', '1 TB <b>+ Copilot</b>', True),
                                                    ('Mitglied 2', '1 TB', False),
                                                    ('Mitglied 3', '1 TB', False),
                                                    ('Mitglied 4', '1 TB', False),
                                                    ('Mitglied 5', '1 TB', False),
                                                    ('Mitglied 6', '1 TB', False)],
                                           'media_src': '../asset/media/m365-family-lifestyle-bridge.webp',
                                           'media_alt': 'Familie nutzt gemeinsam Laptops und '
                                                        'Geräte in einem hellen, modernen '
                                                        'Zuhause.'},
                                    'es': {'eyebrow': 'Compartir',
                                           'title': 'Un plan, cuentas separadas',
                                           'sub': 'Invita hasta cinco personas desde tu cuenta '
                                                  'Microsoft. Cada una obtiene su propio '
                                                  'almacenamiento en la nube, apps y ajustes: '
                                                  'nadie ve los documentos de los demás.',
                                           'list_aria': 'Las seis plazas del plan',
                                           'foot': 'Todos reciben las mismas apps. Solo Copilot '
                                                   'cambia: permanece con el titular.',
                                           'rows': [('Titular', '1 TB <b>+ Copilot</b>', True),
                                                    ('Miembro 2', '1 TB', False),
                                                    ('Miembro 3', '1 TB', False),
                                                    ('Miembro 4', '1 TB', False),
                                                    ('Miembro 5', '1 TB', False),
                                                    ('Miembro 6', '1 TB', False)],
                                           'media_src': '../asset/media/m365-family-lifestyle-bridge.webp',
                                           'media_alt': 'Familia usando portátiles y dispositivos '
                                                        'juntos en un hogar luminoso y moderno.'}},
                          'compare': {'it': {'eyebrow': 'Quale scegliere',
                                             'title': 'Confronta i piani Microsoft 365',
                                             'sub': 'La differenza non è la potenza delle app: è '
                                                    'quante persone useranno davvero il piano.',
                                             'caption': 'Confronto tra Microsoft 365 Personal e '
                                                        'Microsoft 365 Family',
                                             'cols': ['Microsoft 365 Personal',
                                                      'Microsoft 365 Family'],
                                             'rows': [('Persone', '1', 'Fino a 6'),
                                                      ('Spazio OneDrive', '1 TB', '1 TB a persona'),
                                                      ('Account separati per ogni utente',
                                                       'no',
                                                       'yes'),
                                                      ('Funzionalità Copilot',
                                                       'Titolare',
                                                       'Solo titolare'),
                                                      ('Ideale per',
                                                       'Chi usa Office da solo',
                                                       'Due o più persone')],
                                             'yes_label': 'Incluso',
                                             'no_label': 'Non previsto',
                                             'price_row': 'Prezzo su AML Store',
                                             'skus': ['QQ2-00012', '6GQ-00092'],
                                             'foot': 'Scegli Family se almeno due persone useranno '
                                                     'realmente le app o lo spazio OneDrive. '
                                                     'Altrimenti valuta <a '
                                                     'href="/it/microsoft-365-personal">Microsoft '
                                                     '365 Personal</a>.'},
                                      'en': {'eyebrow': 'Which to choose',
                                             'title': 'Compare Microsoft 365 plans',
                                             'sub': 'The difference is not app power: it is how '
                                                    'many people will actually use the plan.',
                                             'caption': 'Comparison between Microsoft 365 Personal '
                                                        'and Microsoft 365 Family',
                                             'cols': ['Microsoft 365 Personal',
                                                      'Microsoft 365 Family'],
                                             'rows': [('People', '1', 'Up to 6'),
                                                      ('OneDrive storage',
                                                       '1 TB',
                                                       '1 TB per person'),
                                                      ('Separate account per user', 'no', 'yes'),
                                                      ('Copilot features', 'Owner', 'Owner only'),
                                                      ('Best for',
                                                       'Someone using Office alone',
                                                       'Two or more people')],
                                             'yes_label': 'Included',
                                             'no_label': 'Not applicable',
                                             'price_row': 'AML Store price',
                                             'skus': ['QQ2-00012', '6GQ-00092'],
                                             'foot': 'Choose Family if at least two people will '
                                                     'really use the apps or OneDrive storage. '
                                                     'Otherwise consider <a '
                                                     'href="/en/microsoft-365-personal">Microsoft '
                                                     '365 Personal</a>.'},
                                      'fr': {'eyebrow': 'Lequel choisir',
                                             'title': 'Comparer les plans Microsoft 365',
                                             'sub': "La différence n'est pas la puissance des apps "
                                                    ": c'est le nombre de personnes qui "
                                                    'utiliseront vraiment le plan.',
                                             'caption': 'Comparaison entre Microsoft 365 Personal '
                                                        'et Microsoft 365 Family',
                                             'cols': ['Microsoft 365 Personal',
                                                      'Microsoft 365 Family'],
                                             'rows': [('Personnes', '1', "Jusqu'à 6"),
                                                      ('Espace OneDrive',
                                                       '1 TB',
                                                       '1 To par personne'),
                                                      ('Compte séparé par utilisateur',
                                                       'no',
                                                       'yes'),
                                                      ('Fonctions Copilot',
                                                       'Titulaire',
                                                       'Titulaire uniquement'),
                                                      ('Idéal pour',
                                                       'Qui utilise Office seul',
                                                       'Deux personnes ou plus')],
                                             'yes_label': 'Inclus',
                                             'no_label': 'Non applicable',
                                             'price_row': 'Prix sur AML Store',
                                             'skus': ['QQ2-00012', '6GQ-00092'],
                                             'foot': 'Choisissez Family si au moins deux personnes '
                                                     "utiliseront réellement les apps ou l'espace "
                                                     'OneDrive. Sinon, voyez <a '
                                                     'href="/fr/microsoft-365-personal">Microsoft '
                                                     '365 Personal</a>.'},
                                      'de': {'eyebrow': 'Welchen Plan wählen',
                                             'title': 'Microsoft 365 Pläne im Vergleich',
                                             'sub': 'Der Unterschied liegt nicht in der '
                                                    'App-Leistung, sondern darin, wie viele '
                                                    'Personen den Plan wirklich nutzen.',
                                             'caption': 'Vergleich zwischen Microsoft 365 Personal '
                                                        'und Microsoft 365 Family',
                                             'cols': ['Microsoft 365 Personal',
                                                      'Microsoft 365 Family'],
                                             'rows': [('Personen', '1', 'Bis zu 6'),
                                                      ('OneDrive-Speicher',
                                                       '1 TB',
                                                       '1 TB pro Person'),
                                                      ('Eigenes Konto pro Nutzer', 'no', 'yes'),
                                                      ('Copilot-Funktionen',
                                                       'Inhaber',
                                                       'Nur Inhaber'),
                                                      ('Ideal für',
                                                       'Wer Office allein nutzt',
                                                       'Zwei oder mehr Personen')],
                                             'yes_label': 'Enthalten',
                                             'no_label': 'Nicht zutreffend',
                                             'price_row': 'AML Store-Preis',
                                             'skus': ['QQ2-00012', '6GQ-00092'],
                                             'foot': 'Wählen Sie Family, wenn mindestens zwei '
                                                     'Personen die Apps oder den OneDrive-Speicher '
                                                     'wirklich nutzen. Sonst kommt <a '
                                                     'href="/de/microsoft-365-personal">Microsoft '
                                                     '365 Personal</a> infrage.'},
                                      'es': {'eyebrow': 'Cuál elegir',
                                             'title': 'Compara los planes Microsoft 365',
                                             'sub': 'La diferencia no es la potencia de las apps: '
                                                    'es cuántas personas van a usar realmente el '
                                                    'plan.',
                                             'caption': 'Comparación entre Microsoft 365 Personal '
                                                        'y Microsoft 365 Family',
                                             'cols': ['Microsoft 365 Personal',
                                                      'Microsoft 365 Family'],
                                             'rows': [('Personas', '1', 'Hasta 6'),
                                                      ('Almacenamiento OneDrive',
                                                       '1 TB',
                                                       '1 TB por persona'),
                                                      ('Cuenta separada por usuario', 'no', 'yes'),
                                                      ('Funciones de Copilot',
                                                       'Titular',
                                                       'Solo titular'),
                                                      ('Ideal para',
                                                       'Quien usa Office en solitario',
                                                       'Dos o más personas')],
                                             'yes_label': 'Incluido',
                                             'no_label': 'No aplicable',
                                             'price_row': 'Precio AML Store',
                                             'skus': ['QQ2-00012', '6GQ-00092'],
                                             'foot': 'Elige Family si al menos dos personas van a '
                                                     'usar de verdad las apps o el almacenamiento '
                                                     'OneDrive. Si no, considera <a '
                                                     'href="/es/microsoft-365-personal">Microsoft '
                                                     '365 Personal</a>.'}}}}


def get_flagship_content(slug):
    return PRODUCTS.get(slug)
