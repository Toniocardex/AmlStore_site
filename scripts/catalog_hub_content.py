#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contenuto guida aggiunto in coda alle pagine categoria (antivirus,
sistemi-operativi, suite-office) da build_catalog_page in product_page_lib.py.

Il product-grid resta generato dinamicamente dal catalogo: questo modulo
aggiunge solo la sezione statica "quale scegliere" + link ai confronti
dedicati + FAQ, per trasformare l'hub da lista prodotti a nodo semantico
(vedi roadmap SEO/GEO). Tutte e 7 le lingue, stessa struttura ovunque
(stesse righe di tabella, stesso numero di FAQ) cosi' le pagine restano
confrontabili tra loro.

Rigenerare con: python scripts/regen-catalogs-only.py
"""

HUB_CONTENT = {
    "antivirus": {
        "it": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Quale scegliere</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">5 marche, un solo antivirus da comprare</h2>
                <p class="pdp-sec__sub">Le differenze reali tra ESET, Kaspersky, Norton, Bitdefender e McAfee sono nel motore di scansione e in cosa includono oltre all'antivirus — non nel numero di funzioni elencate.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Punto di partenza per profilo, prezzo per 1 dispositivo/1 anno</caption>
                        <thead>
                            <tr><th scope="col">Marca</th><th scope="col">Da</th><th scope="col">Cosa include oltre l'antivirus</th><th scope="col">Indicato per</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">ESET NOD32</th><td>€ 22,65</td><td>Solo protezione — nessun bundle</td><td>Chi vuole il minimo impatto su CPU/RAM, anche per gaming</td></tr>
                            <tr><th scope="row">Kaspersky Standard</th><td>€ 19,56</td><td>Protezione bancaria, ottimizzazione PC</td><td>Uso quotidiano con acquisti online frequenti</td></tr>
                            <tr><th scope="row">Norton 360 Standard</th><td>€ 15,44</td><td>VPN illimitata, backup cloud 10 GB</td><td>Chi vuole tutto incluso in un solo abbonamento</td></tr>
                            <tr><th scope="row">Bitdefender Plus</th><td>€ 20,59</td><td>Filtro web anti-phishing, motore leggero (Photon)</td><td>PC meno recenti, priorità alla reattività</td></tr>
                            <tr><th scope="row">McAfee Total Protection</th><td>€ 10,25</td><td>Protezione multi-dispositivo</td><td>Famiglie con più PC, budget contenuto</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="kaspersky-vs-eset-nod32">
                        <strong>Kaspersky vs ESET NOD32 →</strong>
                        <span>Protezione completa o motore leggero: il confronto diretto.</span>
                    </a>
                    <a class="hub-guide__link-card" href="norton-vs-bitdefender">
                        <strong>Norton vs Bitdefender →</strong>
                        <span>Suite con VPN inclusa o motore Photon a basso impatto.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-antivirus-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Domande frequenti</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Qual è il miglior antivirus per un PC lento o datato?</summary>
                                <div class="home-faq-body"><p>ESET NOD32 e Bitdefender Plus sono pensati per un impatto minimo sulle risorse, secondo i rispettivi produttori — indicati se il PC non è recente.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Un antivirus con VPN inclusa conviene?</summary>
                                <div class="home-faq-body"><p>Norton 360 è l'unico dei cinque a includere una VPN illimitata nel prezzo base secondo la scheda Norton — con gli altri la VPN, se disponibile, va valutata a parte.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Posso proteggere più dispositivi con la stessa licenza?</summary>
                                <div class="home-faq-body"><p>Sì: ogni marca in catalogo ha varianti da 1 a 10 dispositivi sulla stessa licenza annuale — il prezzo per dispositivo scende all'aumentare del numero.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Serve disinstallare l'antivirus precedente prima di attivarne uno nuovo?</summary>
                                <div class="home-faq-body"><p>Sì, è la prassi raccomandata dai produttori per evitare conflitti tra motori di scansione concorrenti.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "en": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Which to choose</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">5 brands, one antivirus to buy</h2>
                <p class="pdp-sec__sub">The real differences between ESET, Kaspersky, Norton, Bitdefender and McAfee are in the scanning engine and what's bundled beyond the antivirus itself — not in how many features are listed.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Starting point by profile, price for 1 device / 1 year</caption>
                        <thead>
                            <tr><th scope="col">Brand</th><th scope="col">From</th><th scope="col">Included beyond the antivirus</th><th scope="col">Best for</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">ESET NOD32</th><td>€ 22,65</td><td>Protection only — no bundle</td><td>Minimal CPU/RAM impact, gaming included</td></tr>
                            <tr><th scope="row">Kaspersky Standard</th><td>€ 19,56</td><td>Banking protection, PC optimisation</td><td>Daily use with frequent online purchases</td></tr>
                            <tr><th scope="row">Norton 360 Standard</th><td>€ 15,44</td><td>Unlimited VPN, 10 GB cloud backup</td><td>Wants everything in one subscription</td></tr>
                            <tr><th scope="row">Bitdefender Plus</th><td>€ 20,59</td><td>Anti-phishing web filter, lightweight engine (Photon)</td><td>Older PCs, priority on responsiveness</td></tr>
                            <tr><th scope="row">McAfee Total Protection</th><td>€ 10,25</td><td>Multi-device protection</td><td>Families with several PCs, tight budget</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="kaspersky-vs-eset-nod32">
                        <strong>Kaspersky vs ESET NOD32 →</strong>
                        <span>Full protection or a lightweight engine: the direct comparison.</span>
                    </a>
                    <a class="hub-guide__link-card" href="norton-vs-bitdefender">
                        <strong>Norton vs Bitdefender →</strong>
                        <span>A suite with VPN included, or the low-impact Photon engine.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-antivirus-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Frequently asked questions</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>What's the best antivirus for a slow or older PC?</summary>
                                <div class="home-faq-body"><p>ESET NOD32 and Bitdefender Plus are built for minimal resource impact, according to their makers — worth considering if your PC isn't recent.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Does an antivirus with VPN included pay off?</summary>
                                <div class="home-faq-body"><p>Norton 360 is the only one of the five that bundles an unlimited VPN in the base price according to Norton's own listing — with the others, VPN, if available, needs to be evaluated separately.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Can I protect more than one device with the same licence?</summary>
                                <div class="home-faq-body"><p>Yes: every brand in the catalogue has variants from 1 to 10 devices on the same annual licence — the price per device drops as the count goes up.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Do I need to uninstall my previous antivirus before activating a new one?</summary>
                                <div class="home-faq-body"><p>Yes, that's the practice recommended by manufacturers to avoid conflicts between competing scan engines.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "fr": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Lequel choisir</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">5 marques, un seul antivirus à acheter</h2>
                <p class="pdp-sec__sub">Les vraies différences entre ESET, Kaspersky, Norton, Bitdefender et McAfee se jouent sur le moteur d'analyse et ce qui est inclus en plus de l'antivirus — pas sur le nombre de fonctions listées.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Point de départ par profil, prix pour 1 appareil / 1 an</caption>
                        <thead>
                            <tr><th scope="col">Marque</th><th scope="col">À partir de</th><th scope="col">Inclus en plus de l'antivirus</th><th scope="col">Indiqué pour</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">ESET NOD32</th><td>€ 22,65</td><td>Protection seule — aucun bundle</td><td>Impact minimal sur CPU/RAM, même pour le gaming</td></tr>
                            <tr><th scope="row">Kaspersky Standard</th><td>€ 19,56</td><td>Protection bancaire, optimisation PC</td><td>Usage quotidien avec achats en ligne fréquents</td></tr>
                            <tr><th scope="row">Norton 360 Standard</th><td>€ 15,44</td><td>VPN illimité, sauvegarde cloud 10 Go</td><td>Tout inclus dans un seul abonnement</td></tr>
                            <tr><th scope="row">Bitdefender Plus</th><td>€ 20,59</td><td>Filtre web anti-phishing, moteur léger (Photon)</td><td>PC moins récents, priorité à la réactivité</td></tr>
                            <tr><th scope="row">McAfee Total Protection</th><td>€ 10,25</td><td>Protection multi-appareils</td><td>Familles avec plusieurs PC, budget serré</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="kaspersky-vs-eset-nod32">
                        <strong>Kaspersky vs ESET NOD32 →</strong>
                        <span>Protection complète ou moteur léger : la comparaison directe.</span>
                    </a>
                    <a class="hub-guide__link-card" href="norton-vs-bitdefender">
                        <strong>Norton vs Bitdefender →</strong>
                        <span>Suite avec VPN inclus ou moteur Photon à faible impact.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-antivirus-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Questions fréquentes</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Quel est le meilleur antivirus pour un PC lent ou ancien ?</summary>
                                <div class="home-faq-body"><p>ESET NOD32 et Bitdefender Plus sont conçus pour un impact minimal sur les ressources, selon leurs éditeurs respectifs — à privilégier si le PC n'est pas récent.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Un antivirus avec VPN inclus, ça vaut le coup ?</summary>
                                <div class="home-faq-body"><p>Norton 360 est le seul des cinq à inclure un VPN illimité dans son prix de base selon la fiche Norton — pour les autres, le VPN, s'il est disponible, doit être évalué séparément.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Puis-je protéger plusieurs appareils avec la même licence ?</summary>
                                <div class="home-faq-body"><p>Oui : chaque marque du catalogue propose des variantes de 1 à 10 appareils sur la même licence annuelle — le prix par appareil baisse quand le nombre augmente.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Faut-il désinstaller l'ancien antivirus avant d'en activer un nouveau ?</summary>
                                <div class="home-faq-body"><p>Oui, c'est la pratique recommandée par les éditeurs pour éviter les conflits entre moteurs d'analyse concurrents.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "de": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Welche Wahl</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">5 Marken, ein Antivirus zum Kaufen</h2>
                <p class="pdp-sec__sub">Die echten Unterschiede zwischen ESET, Kaspersky, Norton, Bitdefender und McAfee liegen in der Scan-Engine und dem, was zusätzlich zum Antivirus enthalten ist — nicht in der Anzahl der aufgelisteten Funktionen.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Ausgangspunkt nach Profil, Preis für 1 Gerät / 1 Jahr</caption>
                        <thead>
                            <tr><th scope="col">Marke</th><th scope="col">Ab</th><th scope="col">Zusätzlich zum Antivirus enthalten</th><th scope="col">Geeignet für</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">ESET NOD32</th><td>€ 22,65</td><td>Nur Schutz — kein Bundle</td><td>Minimale CPU-/RAM-Belastung, auch fürs Gaming</td></tr>
                            <tr><th scope="row">Kaspersky Standard</th><td>€ 19,56</td><td>Banking-Schutz, PC-Optimierung</td><td>Alltagsnutzung mit häufigen Online-Käufen</td></tr>
                            <tr><th scope="row">Norton 360 Standard</th><td>€ 15,44</td><td>Unbegrenztes VPN, 10 GB Cloud-Backup</td><td>Alles in einem Abo</td></tr>
                            <tr><th scope="row">Bitdefender Plus</th><td>€ 20,59</td><td>Anti-Phishing-Webfilter, leichte Engine (Photon)</td><td>Ältere PCs, Fokus auf Reaktionsfähigkeit</td></tr>
                            <tr><th scope="row">McAfee Total Protection</th><td>€ 10,25</td><td>Schutz für mehrere Geräte</td><td>Familien mit mehreren PCs, kleines Budget</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="kaspersky-vs-eset-nod32">
                        <strong>Kaspersky vs ESET NOD32 →</strong>
                        <span>Umfassender Schutz oder schlanke Engine: der direkte Vergleich.</span>
                    </a>
                    <a class="hub-guide__link-card" href="norton-vs-bitdefender">
                        <strong>Norton vs Bitdefender →</strong>
                        <span>Suite mit VPN inklusive oder die ressourcenschonende Photon-Engine.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-antivirus-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Häufig gestellte Fragen</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Was ist das beste Antivirenprogramm für einen langsamen oder älteren PC?</summary>
                                <div class="home-faq-body"><p>ESET NOD32 und Bitdefender Plus sind laut Hersteller auf minimale Ressourcenbelastung ausgelegt — empfehlenswert, wenn der PC nicht mehr neu ist.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Lohnt sich ein Antivirus mit inkludiertem VPN?</summary>
                                <div class="home-faq-body"><p>Norton 360 ist laut eigener Produktseite als einziges der fünf mit einem unbegrenzten VPN im Grundpreis ausgestattet — bei den anderen muss ein VPN, falls verfügbar, separat betrachtet werden.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Kann ich mit derselben Lizenz mehrere Geräte schützen?</summary>
                                <div class="home-faq-body"><p>Ja: Jede Marke im Katalog bietet Varianten für 1 bis 10 Geräte auf derselben Jahreslizenz — der Preis pro Gerät sinkt mit steigender Anzahl.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Muss das alte Antivirenprogramm vor der Aktivierung eines neuen deinstalliert werden?</summary>
                                <div class="home-faq-body"><p>Ja, das ist die von den Herstellern empfohlene Vorgehensweise, um Konflikte zwischen konkurrierenden Scan-Engines zu vermeiden.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "es": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Cuál elegir</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">5 marcas, un solo antivirus que comprar</h2>
                <p class="pdp-sec__sub">Las diferencias reales entre ESET, Kaspersky, Norton, Bitdefender y McAfee están en el motor de análisis y en lo que incluyen además del antivirus, no en el número de funciones que se enumeran.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Punto de partida por perfil, precio para 1 dispositivo / 1 año</caption>
                        <thead>
                            <tr><th scope="col">Marca</th><th scope="col">Desde</th><th scope="col">Qué incluye además del antivirus</th><th scope="col">Recomendado para</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">ESET NOD32</th><td>€ 22,65</td><td>Solo protección — sin extras</td><td>Impacto mínimo en CPU/RAM, también para gaming</td></tr>
                            <tr><th scope="row">Kaspersky Standard</th><td>€ 19,56</td><td>Protección bancaria, optimización de PC</td><td>Uso diario con compras online frecuentes</td></tr>
                            <tr><th scope="row">Norton 360 Standard</th><td>€ 15,44</td><td>VPN ilimitada, copia de seguridad en la nube de 10 GB</td><td>Todo incluido en una sola suscripción</td></tr>
                            <tr><th scope="row">Bitdefender Plus</th><td>€ 20,59</td><td>Filtro web antiphishing, motor ligero (Photon)</td><td>PC menos recientes, prioridad a la fluidez</td></tr>
                            <tr><th scope="row">McAfee Total Protection</th><td>€ 10,25</td><td>Protección multidispositivo</td><td>Familias con varios PC, presupuesto ajustado</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="kaspersky-vs-eset-nod32">
                        <strong>Kaspersky vs ESET NOD32 →</strong>
                        <span>Protección completa o motor ligero: la comparación directa.</span>
                    </a>
                    <a class="hub-guide__link-card" href="norton-vs-bitdefender">
                        <strong>Norton vs Bitdefender →</strong>
                        <span>Suite con VPN incluida o motor Photon de bajo impacto.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-antivirus-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Preguntas frecuentes</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>¿Cuál es el mejor antivirus para un PC lento o antiguo?</summary>
                                <div class="home-faq-body"><p>ESET NOD32 y Bitdefender Plus están pensados para un impacto mínimo en los recursos, según sus fabricantes — recomendables si el PC no es reciente.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>¿Merece la pena un antivirus con VPN incluida?</summary>
                                <div class="home-faq-body"><p>Norton 360 es el único de los cinco que incluye una VPN ilimitada en el precio base, según su propia ficha — en los demás, la VPN, si está disponible, hay que valorarla aparte.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>¿Puedo proteger varios dispositivos con la misma licencia?</summary>
                                <div class="home-faq-body"><p>Sí: cada marca del catálogo tiene variantes de 1 a 10 dispositivos con la misma licencia anual — el precio por dispositivo baja cuanto mayor es el número.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>¿Hay que desinstalar el antivirus anterior antes de activar uno nuevo?</summary>
                                <div class="home-faq-body"><p>Sí, es la práctica recomendada por los fabricantes para evitar conflictos entre motores de análisis distintos.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "pt": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Qual escolher</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">5 marcas, um único antivírus para comprar</h2>
                <p class="pdp-sec__sub">As diferenças reais entre ESET, Kaspersky, Norton, Bitdefender e McAfee estão no motor de análise e no que incluem além do antivírus — não no número de funcionalidades listadas.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Ponto de partida por perfil, preço para 1 dispositivo / 1 ano</caption>
                        <thead>
                            <tr><th scope="col">Marca</th><th scope="col">Desde</th><th scope="col">O que inclui além do antivírus</th><th scope="col">Indicado para</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">ESET NOD32</th><td>€ 22,65</td><td>Só proteção — sem extras</td><td>Impacto mínimo em CPU/RAM, também para gaming</td></tr>
                            <tr><th scope="row">Kaspersky Standard</th><td>€ 19,56</td><td>Proteção bancária, otimização do PC</td><td>Uso diário com compras online frequentes</td></tr>
                            <tr><th scope="row">Norton 360 Standard</th><td>€ 15,44</td><td>VPN ilimitada, cópia de segurança na nuvem de 10 GB</td><td>Tudo incluído numa só subscrição</td></tr>
                            <tr><th scope="row">Bitdefender Plus</th><td>€ 20,59</td><td>Filtro web antiphishing, motor leve (Photon)</td><td>PCs menos recentes, prioridade à fluidez</td></tr>
                            <tr><th scope="row">McAfee Total Protection</th><td>€ 10,25</td><td>Proteção multidispositivo</td><td>Famílias com vários PC, orçamento reduzido</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="kaspersky-vs-eset-nod32">
                        <strong>Kaspersky vs ESET NOD32 →</strong>
                        <span>Proteção completa ou motor leve: a comparação direta.</span>
                    </a>
                    <a class="hub-guide__link-card" href="norton-vs-bitdefender">
                        <strong>Norton vs Bitdefender →</strong>
                        <span>Suite com VPN incluída ou motor Photon de baixo impacto.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-antivirus-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Perguntas frequentes</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Qual é o melhor antivírus para um PC lento ou antigo?</summary>
                                <div class="home-faq-body"><p>O ESET NOD32 e o Bitdefender Plus são pensados para um impacto mínimo nos recursos, segundo os respetivos fabricantes — indicados se o PC não for recente.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Compensa um antivírus com VPN incluída?</summary>
                                <div class="home-faq-body"><p>O Norton 360 é o único dos cinco a incluir uma VPN ilimitada no preço base, segundo a ficha da Norton — nos outros, a VPN, quando disponível, deve ser avaliada à parte.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Posso proteger vários dispositivos com a mesma licença?</summary>
                                <div class="home-faq-body"><p>Sim: cada marca no catálogo tem variantes de 1 a 10 dispositivos na mesma licença anual — o preço por dispositivo desce à medida que o número aumenta.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>É preciso desinstalar o antivírus anterior antes de ativar um novo?</summary>
                                <div class="home-faq-body"><p>Sim, é a prática recomendada pelos fabricantes para evitar conflitos entre motores de análise concorrentes.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "nl": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Welke kiezen</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">5 merken, één antivirus om te kopen</h2>
                <p class="pdp-sec__sub">De echte verschillen tussen ESET, Kaspersky, Norton, Bitdefender en McAfee zitten in de scanengine en wat er naast de antivirus wordt meegeleverd — niet in het aantal genoemde functies.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Startpunt per profiel, prijs voor 1 apparaat / 1 jaar</caption>
                        <thead>
                            <tr><th scope="col">Merk</th><th scope="col">Vanaf</th><th scope="col">Wat zit erbij naast de antivirus</th><th scope="col">Geschikt voor</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">ESET NOD32</th><td>€ 22,65</td><td>Alleen bescherming — geen extra's</td><td>Minimale impact op cpu/ram, ook voor gaming</td></tr>
                            <tr><th scope="row">Kaspersky Standard</th><td>€ 19,56</td><td>Bankbescherming, pc-optimalisatie</td><td>Dagelijks gebruik met regelmatige online aankopen</td></tr>
                            <tr><th scope="row">Norton 360 Standard</th><td>€ 15,44</td><td>Onbeperkte VPN, 10 GB cloudback-up</td><td>Alles in één abonnement</td></tr>
                            <tr><th scope="row">Bitdefender Plus</th><td>€ 20,59</td><td>Anti-phishing webfilter, lichte engine (Photon)</td><td>Oudere pc's, prioriteit bij snelheid</td></tr>
                            <tr><th scope="row">McAfee Total Protection</th><td>€ 10,25</td><td>Bescherming voor meerdere apparaten</td><td>Gezinnen met meerdere pc's, krap budget</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="kaspersky-vs-eset-nod32">
                        <strong>Kaspersky vs ESET NOD32 →</strong>
                        <span>Volledige bescherming of een lichte engine: de directe vergelijking.</span>
                    </a>
                    <a class="hub-guide__link-card" href="norton-vs-bitdefender">
                        <strong>Norton vs Bitdefender →</strong>
                        <span>Suite met VPN inbegrepen of de Photon-engine met lage impact.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-antivirus-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Veelgestelde vragen</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Wat is de beste antivirus voor een trage of oudere pc?</summary>
                                <div class="home-faq-body"><p>ESET NOD32 en Bitdefender Plus zijn volgens de fabrikanten gemaakt voor minimale impact op de systeembronnen — aan te raden als de pc niet recent is.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Loont een antivirus met VPN erbij?</summary>
                                <div class="home-faq-body"><p>Norton 360 is als enige van de vijf uitgerust met een onbeperkte VPN in de basisprijs, volgens de eigen productpagina — bij de andere merken moet een VPN, indien beschikbaar, apart worden bekeken.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Kan ik meerdere apparaten beschermen met dezelfde licentie?</summary>
                                <div class="home-faq-body"><p>Ja: elk merk in de catalogus heeft varianten van 1 tot 10 apparaten op dezelfde jaarlicentie — de prijs per apparaat daalt naarmate het aantal toeneemt.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Moet de oude antivirus worden verwijderd voordat je een nieuwe activeert?</summary>
                                <div class="home-faq-body"><p>Ja, dat is de door fabrikanten aanbevolen werkwijze om conflicten tussen concurrerende scanengines te voorkomen.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
    },
    "sistemi-operativi": {
        "it": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Quale scegliere</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">Home, Pro o Server: la licenza giusta in base all'uso</h2>
                <p class="pdp-sec__sub">Windows 11 Home copre l'uso privato. Pro aggiunge le funzioni orientate al lavoro. Server è un sistema operativo diverso, pensato per macchine che erogano servizi di rete.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Confronto rapido, prezzo licenza singola</caption>
                        <thead>
                            <tr><th scope="col">Edizione</th><th scope="col">Da</th><th scope="col">In più rispetto a Home</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">Windows 11 Home</th><td>€ 61,00</td><td>—</td></tr>
                            <tr><th scope="row">Windows 11 Pro</th><td>€ 99,00</td><td>BitLocker, Desktop remoto come host, secondo Microsoft</td></tr>
                            <tr><th scope="row">Windows 10 Home / Pro</th><td>€ 39,13 / € 60,00</td><td>Stessa differenza Home→Pro, generazione precedente</td></tr>
                            <tr><th scope="row">Windows Server</th><td>vedi <a href="windows-server">Windows Server e SQL</a></td><td>Sistema operativo per server, non per postazione singola</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="windows-11-home-vs-pro">
                        <strong>Windows 11 Home vs Pro →</strong>
                        <span>Cosa cambia davvero e chi ha bisogno di Pro.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-win-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Domande frequenti</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Che differenza c'è tra licenza OEM, ESD e COA?</summary>
                                <div class="home-faq-body"><p>ESD è la licenza digitale via email; OEM DVD include il supporto fisico; COA è l'adesivo con il codice originale. Il sistema operativo attivato è lo stesso — cambia solo il formato di consegna.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Conviene passare da Windows 10 a Windows 11?</summary>
                                <div class="home-faq-body"><p>Dipende dai requisiti hardware Microsoft (CPU compatibile, TPM 2.0, Secure Boot): vanno verificati prima di installare, come indicato in ogni scheda Windows 11.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Windows 11 Pro serve anche per un uso privato avanzato?</summary>
                                <div class="home-faq-body"><p>Sì, se usi BitLocker per criptare il disco o il Desktop remoto come host verso il tuo PC — funzioni non presenti in Home secondo Microsoft.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Come ricevo la licenza dopo l'acquisto?</summary>
                                <div class="home-faq-body"><p>Codice e istruzioni di attivazione via email, tipicamente entro 2–15 minuti dal pagamento.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "en": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Which to choose</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">Home, Pro or Server: the right licence for how you use it</h2>
                <p class="pdp-sec__sub">Windows 11 Home covers personal use. Pro adds work-oriented features. Server is a different operating system, built for machines that provide network services.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Quick comparison, single licence price</caption>
                        <thead>
                            <tr><th scope="col">Edition</th><th scope="col">From</th><th scope="col">On top of Home</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">Windows 11 Home</th><td>€ 61,00</td><td>—</td></tr>
                            <tr><th scope="row">Windows 11 Pro</th><td>€ 99,00</td><td>BitLocker, Remote Desktop as host, according to Microsoft</td></tr>
                            <tr><th scope="row">Windows 10 Home / Pro</th><td>€ 39,13 / € 60,00</td><td>Same Home→Pro difference, previous generation</td></tr>
                            <tr><th scope="row">Windows Server</th><td>see <a href="windows-server">Windows Server &amp; SQL</a></td><td>Server operating system, not for a single workstation</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="windows-11-home-vs-pro">
                        <strong>Windows 11 Home vs Pro →</strong>
                        <span>What really changes, and who actually needs Pro.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-win-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Frequently asked questions</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>What's the difference between OEM, ESD and COA licences?</summary>
                                <div class="home-faq-body"><p>ESD is the digital licence delivered by email; OEM DVD includes physical media; COA is the sticker with the original code. The activated operating system is the same — only the delivery format changes.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Is it worth upgrading from Windows 10 to Windows 11?</summary>
                                <div class="home-faq-body"><p>It depends on Microsoft's hardware requirements (compatible CPU, TPM 2.0, Secure Boot): check these before installing, as noted on every Windows 11 listing.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Is Windows 11 Pro useful for advanced personal use too?</summary>
                                <div class="home-faq-body"><p>Yes, if you use BitLocker to encrypt your drive or Remote Desktop as a host to your PC — features not present in Home according to Microsoft.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>How do I receive the licence after purchase?</summary>
                                <div class="home-faq-body"><p>Activation code and instructions by email, typically within 2–15 minutes of payment.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "fr": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Lequel choisir</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">Home, Pro ou Server : la bonne licence selon l'usage</h2>
                <p class="pdp-sec__sub">Windows 11 Home couvre l'usage privé. Pro ajoute des fonctions orientées travail. Server est un système d'exploitation différent, conçu pour les machines qui fournissent des services réseau.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Comparaison rapide, prix licence unique</caption>
                        <thead>
                            <tr><th scope="col">Édition</th><th scope="col">À partir de</th><th scope="col">En plus de Home</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">Windows 11 Home</th><td>€ 61,00</td><td>—</td></tr>
                            <tr><th scope="row">Windows 11 Pro</th><td>€ 99,00</td><td>BitLocker, Bureau à distance en tant qu'hôte, selon Microsoft</td></tr>
                            <tr><th scope="row">Windows 10 Home / Pro</th><td>€ 39,13 / € 60,00</td><td>Même différence Home→Pro, génération précédente</td></tr>
                            <tr><th scope="row">Windows Server</th><td>voir <a href="windows-server">Windows Server et SQL</a></td><td>Système d'exploitation serveur, pas pour un poste unique</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="windows-11-home-vs-pro">
                        <strong>Windows 11 Home vs Pro →</strong>
                        <span>Ce qui change vraiment, et qui a réellement besoin de Pro.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-win-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Questions fréquentes</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Quelle est la différence entre licence OEM, ESD et COA ?</summary>
                                <div class="home-faq-body"><p>ESD est la licence numérique envoyée par email ; OEM DVD inclut un support physique ; COA est l'autocollant avec le code d'origine. Le système d'exploitation activé est le même — seul le format de livraison change.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Vaut-il la peine de passer de Windows 10 à Windows 11 ?</summary>
                                <div class="home-faq-body"><p>Cela dépend des prérequis matériels Microsoft (CPU compatible, TPM 2.0, Secure Boot) : à vérifier avant d'installer, comme indiqué sur chaque fiche Windows 11.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Windows 11 Pro est-il utile aussi pour un usage privé avancé ?</summary>
                                <div class="home-faq-body"><p>Oui, si vous utilisez BitLocker pour chiffrer le disque ou le Bureau à distance en tant qu'hôte vers votre PC — des fonctions absentes de Home selon Microsoft.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Comment est-ce que je reçois la licence après l'achat ?</summary>
                                <div class="home-faq-body"><p>Code et instructions d'activation par email, généralement quelques minutes après le paiement.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "de": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Welche Wahl</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">Home, Pro oder Server: die richtige Lizenz je nach Nutzung</h2>
                <p class="pdp-sec__sub">Windows 11 Home deckt die private Nutzung ab. Pro ergänzt arbeitsorientierte Funktionen. Server ist ein eigenes Betriebssystem für Maschinen, die Netzwerkdienste bereitstellen.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Schnellvergleich, Preis für eine Einzellizenz</caption>
                        <thead>
                            <tr><th scope="col">Edition</th><th scope="col">Ab</th><th scope="col">Zusätzlich zu Home</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">Windows 11 Home</th><td>€ 61,00</td><td>—</td></tr>
                            <tr><th scope="row">Windows 11 Pro</th><td>€ 99,00</td><td>BitLocker, Remotedesktop als Host, laut Microsoft</td></tr>
                            <tr><th scope="row">Windows 10 Home / Pro</th><td>€ 39,13 / € 60,00</td><td>Gleicher Home→Pro-Unterschied, vorherige Generation</td></tr>
                            <tr><th scope="row">Windows Server</th><td>siehe <a href="windows-server">Windows Server &amp; SQL</a></td><td>Server-Betriebssystem, nicht für einen Einzelarbeitsplatz</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="windows-11-home-vs-pro">
                        <strong>Windows 11 Home vs Pro →</strong>
                        <span>Was sich wirklich ändert und wer Pro tatsächlich braucht.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-win-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Häufig gestellte Fragen</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Was ist der Unterschied zwischen OEM-, ESD- und COA-Lizenz?</summary>
                                <div class="home-faq-body"><p>ESD ist die per E-Mail gelieferte digitale Lizenz; OEM-DVD enthält einen physischen Datenträger; COA ist der Aufkleber mit dem Originalcode. Das aktivierte Betriebssystem ist dasselbe — nur das Lieferformat unterscheidet sich.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Lohnt sich der Umstieg von Windows 10 auf Windows 11?</summary>
                                <div class="home-faq-body"><p>Das hängt von Microsofts Hardwarevoraussetzungen ab (kompatible CPU, TPM 2.0, Secure Boot): Diese sollten vor der Installation geprüft werden, wie auf jeder Windows-11-Produktseite angegeben.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Ist Windows 11 Pro auch für anspruchsvolle private Nutzung sinnvoll?</summary>
                                <div class="home-faq-body"><p>Ja, wenn Sie BitLocker zur Festplattenverschlüsselung oder Remotedesktop als Host zu Ihrem PC nutzen — Funktionen, die laut Microsoft in Home nicht enthalten sind.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Wie erhalte ich die Lizenz nach dem Kauf?</summary>
                                <div class="home-faq-body"><p>Aktivierungscode und Anleitung per E-Mail, in der Regel innerhalb von 2–15 Minuten nach der Zahlung.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "es": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Cuál elegir</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">Home, Pro o Server: la licencia adecuada según el uso</h2>
                <p class="pdp-sec__sub">Windows 11 Home cubre el uso privado. Pro añade funciones orientadas al trabajo. Server es un sistema operativo distinto, pensado para máquinas que ofrecen servicios de red.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Comparación rápida, precio de licencia individual</caption>
                        <thead>
                            <tr><th scope="col">Edición</th><th scope="col">Desde</th><th scope="col">Además de Home</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">Windows 11 Home</th><td>€ 61,00</td><td>—</td></tr>
                            <tr><th scope="row">Windows 11 Pro</th><td>€ 99,00</td><td>BitLocker, Escritorio remoto como host, según Microsoft</td></tr>
                            <tr><th scope="row">Windows 10 Home / Pro</th><td>€ 39,13 / € 60,00</td><td>Misma diferencia Home→Pro, generación anterior</td></tr>
                            <tr><th scope="row">Windows Server</th><td>ver <a href="windows-server">Windows Server y SQL</a></td><td>Sistema operativo para servidores, no para un puesto individual</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="windows-11-home-vs-pro">
                        <strong>Windows 11 Home vs Pro →</strong>
                        <span>Qué cambia realmente y quién necesita Pro de verdad.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-win-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Preguntas frecuentes</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>¿Cuál es la diferencia entre licencia OEM, ESD y COA?</summary>
                                <div class="home-faq-body"><p>ESD es la licencia digital enviada por email; OEM DVD incluye el soporte físico; COA es la pegatina con el código original. El sistema operativo activado es el mismo — solo cambia el formato de entrega.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>¿Merece la pena pasar de Windows 10 a Windows 11?</summary>
                                <div class="home-faq-body"><p>Depende de los requisitos de hardware de Microsoft (CPU compatible, TPM 2.0, Secure Boot): hay que comprobarlos antes de instalar, como se indica en cada ficha de Windows 11.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>¿Windows 11 Pro también es útil para un uso privado avanzado?</summary>
                                <div class="home-faq-body"><p>Sí, si usas BitLocker para cifrar el disco o el Escritorio remoto como host hacia tu PC — funciones no presentes en Home según Microsoft.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>¿Cómo recibo la licencia después de la compra?</summary>
                                <div class="home-faq-body"><p>Código e instrucciones de activación por email, normalmente a los pocos minutos del pago.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "pt": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Qual escolher</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">Home, Pro ou Server: a licença certa consoante o uso</h2>
                <p class="pdp-sec__sub">O Windows 11 Home cobre o uso privado. O Pro acrescenta funcionalidades orientadas para o trabalho. O Server é um sistema operativo diferente, pensado para máquinas que fornecem serviços de rede.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Comparação rápida, preço de licença individual</caption>
                        <thead>
                            <tr><th scope="col">Edição</th><th scope="col">Desde</th><th scope="col">Além do Home</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">Windows 11 Home</th><td>€ 61,00</td><td>—</td></tr>
                            <tr><th scope="row">Windows 11 Pro</th><td>€ 99,00</td><td>BitLocker, Ambiente de Trabalho Remoto como anfitrião, segundo a Microsoft</td></tr>
                            <tr><th scope="row">Windows 10 Home / Pro</th><td>€ 39,13 / € 60,00</td><td>Mesma diferença Home→Pro, geração anterior</td></tr>
                            <tr><th scope="row">Windows Server</th><td>ver <a href="windows-server">Windows Server e SQL</a></td><td>Sistema operativo para servidores, não para um posto único</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="windows-11-home-vs-pro">
                        <strong>Windows 11 Home vs Pro →</strong>
                        <span>O que muda realmente e quem precisa mesmo do Pro.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-win-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Perguntas frequentes</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Qual é a diferença entre licença OEM, ESD e COA?</summary>
                                <div class="home-faq-body"><p>ESD é a licença digital enviada por email; OEM DVD inclui o suporte físico; COA é o autocolante com o código original. O sistema operativo ativado é o mesmo — só muda o formato de entrega.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Compensa passar do Windows 10 para o Windows 11?</summary>
                                <div class="home-faq-body"><p>Depende dos requisitos de hardware da Microsoft (CPU compatível, TPM 2.0, Secure Boot): devem ser verificados antes de instalar, como indicado em cada ficha do Windows 11.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>O Windows 11 Pro também é útil para um uso privado mais avançado?</summary>
                                <div class="home-faq-body"><p>Sim, se usar o BitLocker para encriptar o disco ou o Ambiente de Trabalho Remoto como anfitrião do seu PC — funcionalidades não presentes no Home segundo a Microsoft.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Como recebo a licença depois da compra?</summary>
                                <div class="home-faq-body"><p>Código e instruções de ativação por email, normalmente poucos minutos depois do pagamento.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "nl": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Welke kiezen</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">Home, Pro of Server: de juiste licentie per gebruik</h2>
                <p class="pdp-sec__sub">Windows 11 Home dekt privégebruik. Pro voegt werkgerichte functies toe. Server is een ander besturingssysteem, bedoeld voor machines die netwerkdiensten leveren.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Snelle vergelijking, prijs losse licentie</caption>
                        <thead>
                            <tr><th scope="col">Editie</th><th scope="col">Vanaf</th><th scope="col">Extra ten opzichte van Home</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">Windows 11 Home</th><td>€ 61,00</td><td>—</td></tr>
                            <tr><th scope="row">Windows 11 Pro</th><td>€ 99,00</td><td>BitLocker, Extern bureaublad als host, volgens Microsoft</td></tr>
                            <tr><th scope="row">Windows 10 Home / Pro</th><td>€ 39,13 / € 60,00</td><td>Zelfde verschil Home→Pro, vorige generatie</td></tr>
                            <tr><th scope="row">Windows Server</th><td>zie <a href="windows-server">Windows Server en SQL</a></td><td>Besturingssysteem voor servers, niet voor één werkplek</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="windows-11-home-vs-pro">
                        <strong>Windows 11 Home vs Pro →</strong>
                        <span>Wat er echt verandert en wie Pro daadwerkelijk nodig heeft.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-win-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Veelgestelde vragen</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Wat is het verschil tussen een OEM-, ESD- en COA-licentie?</summary>
                                <div class="home-faq-body"><p>ESD is de digitale licentie die via e-mail wordt geleverd; OEM-dvd bevat de fysieke drager; COA is de sticker met de originele code. Het geactiveerde besturingssysteem is hetzelfde — alleen het leveringsformaat verschilt.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Is overstappen van Windows 10 naar Windows 11 de moeite waard?</summary>
                                <div class="home-faq-body"><p>Dat hangt af van de hardware-eisen van Microsoft (compatibele cpu, TPM 2.0, Secure Boot): controleer deze voor de installatie, zoals aangegeven op elke Windows 11-productpagina.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Is Windows 11 Pro ook nuttig voor geavanceerd privégebruik?</summary>
                                <div class="home-faq-body"><p>Ja, als je BitLocker gebruikt om de schijf te versleutelen of Extern bureaublad als host naar je pc — functies die volgens Microsoft niet in Home zitten.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Hoe ontvang ik de licentie na aankoop?</summary>
                                <div class="home-faq-body"><p>Activeringscode en instructies per e-mail, meestal binnen 2–15 minuten na betaling.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
    },
    "suite-office": {
        "it": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Quale scegliere</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">Licenza unica o abbonamento? E quale piano Microsoft 365</h2>
                <p class="pdp-sec__sub">Office 2024/2021/2019 si pagano una volta sola e restano quelli. Microsoft 365 è un abbonamento che include Copilot AI, spazio cloud e aggiornamenti continui delle app.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Le opzioni principali in catalogo</caption>
                        <thead>
                            <tr><th scope="col">Prodotto</th><th scope="col">Prezzo</th><th scope="col">Formula</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">Microsoft 365 Personal</th><td>€ 84,79 / anno</td><td>Abbonamento — 1 persona, 1TB cloud, Copilot AI</td></tr>
                            <tr><th scope="row">Microsoft 365 Family</th><td>€ 104,95 / anno</td><td>Abbonamento — fino a 6 persone, 6TB cloud totali</td></tr>
                            <tr><th scope="row">Office 2024 Home</th><td>€ 134,00</td><td>Licenza perpetua — PC/Mac, un solo pagamento</td></tr>
                            <tr><th scope="row">Office 2024 Home &amp; Business</th><td>€ 209,00</td><td>Licenza perpetua — include Outlook</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="office-2024-vs-microsoft-365">
                        <strong>Office 2024 vs Microsoft 365 →</strong>
                        <span>Licenza perpetua o abbonamento: cosa conviene davvero.</span>
                    </a>
                    <a class="hub-guide__link-card" href="microsoft-365-family-vs-personal">
                        <strong>Microsoft 365 Family vs Personal →</strong>
                        <span>Quante persone possono usarlo e cosa cambia nel prezzo.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-office-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Domande frequenti</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Office 2024 riceve gli stessi aggiornamenti di Microsoft 365?</summary>
                                <div class="home-faq-body"><p>No: Office 2024 riceve aggiornamenti di sicurezza ma non le nuove funzioni introdotte via abbonamento, incluso Copilot — quelle restano esclusive di Microsoft 365, secondo Microsoft.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Posso installare Office su più computer con la stessa licenza perpetua?</summary>
                                <div class="home-faq-body"><p>Dipende dal prodotto: verifica il numero di dispositivi indicato nella scheda del titolo che acquisti.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Cosa succede se non rinnovo Microsoft 365?</summary>
                                <div class="home-faq-body"><p>Le app passano in modalità di sola visualizzazione e lo spazio cloud oltre i limiti gratuiti resta di sola lettura, secondo le condizioni Microsoft — i file restano tuoi.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Serve Windows per usare Office, o funziona anche su Mac?</summary>
                                <div class="home-faq-body"><p>Le versioni Office 2024 e i piani Microsoft 365 in catalogo indicano la compatibilità Mac direttamente nel titolo o nella scheda prodotto.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "en": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Which to choose</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">One-time licence or subscription? And which Microsoft 365 plan</h2>
                <p class="pdp-sec__sub">Office 2024/2021/2019 are paid once and stay as they are. Microsoft 365 is a subscription that includes Copilot AI, cloud storage and continuous app updates.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>The main options in the catalogue</caption>
                        <thead>
                            <tr><th scope="col">Product</th><th scope="col">Price</th><th scope="col">Formula</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">Microsoft 365 Personal</th><td>€ 84,79 / year</td><td>Subscription — 1 person, 1TB cloud, Copilot AI</td></tr>
                            <tr><th scope="row">Microsoft 365 Family</th><td>€ 104,95 / year</td><td>Subscription — up to 6 people, 6TB cloud total</td></tr>
                            <tr><th scope="row">Office 2024 Home</th><td>€ 134,00</td><td>One-time licence — PC/Mac, single payment</td></tr>
                            <tr><th scope="row">Office 2024 Home &amp; Business</th><td>€ 209,00</td><td>One-time licence — includes Outlook</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="office-2024-vs-microsoft-365">
                        <strong>Office 2024 vs Microsoft 365 →</strong>
                        <span>One-time licence or subscription: what actually pays off.</span>
                    </a>
                    <a class="hub-guide__link-card" href="microsoft-365-family-vs-personal">
                        <strong>Microsoft 365 Family vs Personal →</strong>
                        <span>How many people can use it and what changes in price.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-office-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Frequently asked questions</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Does Office 2024 get the same updates as Microsoft 365?</summary>
                                <div class="home-faq-body"><p>No: Office 2024 receives security updates but not the new features rolled out via subscription, Copilot included — those remain exclusive to Microsoft 365, according to Microsoft.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Can I install a one-time Office licence on more than one computer?</summary>
                                <div class="home-faq-body"><p>It depends on the product: check the number of devices stated on the listing for the title you buy.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>What happens if I don't renew Microsoft 365?</summary>
                                <div class="home-faq-body"><p>The apps switch to view-only mode and cloud storage beyond the free limits becomes read-only too, according to Microsoft's terms — your files stay yours.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Do I need Windows to use Office, or does it work on Mac too?</summary>
                                <div class="home-faq-body"><p>The Office 2024 versions and Microsoft 365 plans in the catalogue state Mac compatibility directly in the title or the product listing.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "fr": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Lequel choisir</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">Licence unique ou abonnement ? Et quel plan Microsoft 365</h2>
                <p class="pdp-sec__sub">Office 2024/2021/2019 se paient une seule fois et restent tels quels. Microsoft 365 est un abonnement qui inclut Copilot AI, de l'espace cloud et des mises à jour continues des applications.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Les principales options du catalogue</caption>
                        <thead>
                            <tr><th scope="col">Produit</th><th scope="col">Prix</th><th scope="col">Formule</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">Microsoft 365 Personal</th><td>€ 84,79 / an</td><td>Abonnement — 1 personne, 1 To cloud, Copilot AI</td></tr>
                            <tr><th scope="row">Microsoft 365 Family</th><td>€ 104,95 / an</td><td>Abonnement — jusqu'à 6 personnes, 6 To cloud au total</td></tr>
                            <tr><th scope="row">Office 2024 Home</th><td>€ 134,00</td><td>Licence perpétuelle — PC/Mac, paiement unique</td></tr>
                            <tr><th scope="row">Office 2024 Home &amp; Business</th><td>€ 209,00</td><td>Licence perpétuelle — Outlook inclus</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="office-2024-vs-microsoft-365">
                        <strong>Office 2024 vs Microsoft 365 →</strong>
                        <span>Licence unique ou abonnement : ce qui est vraiment rentable.</span>
                    </a>
                    <a class="hub-guide__link-card" href="microsoft-365-family-vs-personal">
                        <strong>Microsoft 365 Family vs Personal →</strong>
                        <span>Combien de personnes peuvent l'utiliser et ce qui change au niveau du prix.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-office-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Questions fréquentes</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Office 2024 reçoit-il les mêmes mises à jour que Microsoft 365 ?</summary>
                                <div class="home-faq-body"><p>Non : Office 2024 reçoit des mises à jour de sécurité mais pas les nouvelles fonctions introduites via abonnement, Copilot inclus — celles-ci restent exclusives à Microsoft 365, selon Microsoft.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Puis-je installer Office sur plusieurs ordinateurs avec la même licence perpétuelle ?</summary>
                                <div class="home-faq-body"><p>Cela dépend du produit : vérifiez le nombre d'appareils indiqué sur la fiche du titre que vous achetez.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Que se passe-t-il si je ne renouvelle pas Microsoft 365 ?</summary>
                                <div class="home-faq-body"><p>Les applications passent en mode lecture seule et l'espace cloud au-delà des limites gratuites devient également en lecture seule, selon les conditions Microsoft — vos fichiers restent les vôtres.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Faut-il Windows pour utiliser Office, ou fonctionne-t-il aussi sur Mac ?</summary>
                                <div class="home-faq-body"><p>Les versions Office 2024 et les plans Microsoft 365 du catalogue indiquent la compatibilité Mac directement dans le titre ou sur la fiche produit.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "de": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Welche Wahl</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">Einmallizenz oder Abo? Und welcher Microsoft-365-Plan</h2>
                <p class="pdp-sec__sub">Office 2024/2021/2019 werden einmal bezahlt und bleiben so, wie sie sind. Microsoft 365 ist ein Abo mit Copilot AI, Cloud-Speicher und laufenden App-Updates.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Die wichtigsten Optionen im Katalog</caption>
                        <thead>
                            <tr><th scope="col">Produkt</th><th scope="col">Preis</th><th scope="col">Modell</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">Microsoft 365 Personal</th><td>€ 84,79 / Jahr</td><td>Abo — 1 Person, 1 TB Cloud, Copilot AI</td></tr>
                            <tr><th scope="row">Microsoft 365 Family</th><td>€ 104,95 / Jahr</td><td>Abo — bis zu 6 Personen, 6 TB Cloud insgesamt</td></tr>
                            <tr><th scope="row">Office 2024 Home</th><td>€ 134,00</td><td>Einmallizenz — PC/Mac, einmalige Zahlung</td></tr>
                            <tr><th scope="row">Office 2024 Home &amp; Business</th><td>€ 209,00</td><td>Einmallizenz — inklusive Outlook</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="office-2024-vs-microsoft-365">
                        <strong>Office 2024 vs Microsoft 365 →</strong>
                        <span>Einmallizenz oder Abo: was sich wirklich lohnt.</span>
                    </a>
                    <a class="hub-guide__link-card" href="microsoft-365-family-vs-personal">
                        <strong>Microsoft 365 Family vs Personal →</strong>
                        <span>Wie viele Personen es nutzen können und was sich beim Preis ändert.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-office-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Häufig gestellte Fragen</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Erhält Office 2024 dieselben Updates wie Microsoft 365?</summary>
                                <div class="home-faq-body"><p>Nein: Office 2024 erhält Sicherheitsupdates, aber nicht die neuen Funktionen, die über das Abo eingeführt werden, Copilot eingeschlossen — diese bleiben laut Microsoft Microsoft 365 vorbehalten.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Kann ich eine Einmallizenz von Office auf mehreren Computern installieren?</summary>
                                <div class="home-faq-body"><p>Das hängt vom Produkt ab: Prüfen Sie die auf der Produktseite des gekauften Titels angegebene Geräteanzahl.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Was passiert, wenn ich Microsoft 365 nicht verlängere?</summary>
                                <div class="home-faq-body"><p>Die Apps wechseln in den reinen Anzeigemodus, und Cloud-Speicher über die kostenlosen Grenzen hinaus wird laut Microsoft-Bedingungen ebenfalls nur noch lesbar — Ihre Dateien bleiben Ihnen erhalten.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Brauche ich Windows, um Office zu nutzen, oder funktioniert es auch auf dem Mac?</summary>
                                <div class="home-faq-body"><p>Die Office-2024-Versionen und die Microsoft-365-Pläne im Katalog geben die Mac-Kompatibilität direkt im Titel oder auf der Produktseite an.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "es": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Cuál elegir</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">¿Licencia única o suscripción? Y qué plan de Microsoft 365</h2>
                <p class="pdp-sec__sub">Office 2024/2021/2019 se pagan una sola vez y se quedan tal cual. Microsoft 365 es una suscripción que incluye Copilot AI, espacio en la nube y actualizaciones continuas de las apps.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>Las principales opciones del catálogo</caption>
                        <thead>
                            <tr><th scope="col">Producto</th><th scope="col">Precio</th><th scope="col">Fórmula</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">Microsoft 365 Personal</th><td>€ 84,79 / año</td><td>Suscripción — 1 persona, 1 TB en la nube, Copilot AI</td></tr>
                            <tr><th scope="row">Microsoft 365 Family</th><td>€ 104,95 / año</td><td>Suscripción — hasta 6 personas, 6 TB en la nube en total</td></tr>
                            <tr><th scope="row">Office 2024 Home</th><td>€ 134,00</td><td>Licencia única — PC/Mac, un solo pago</td></tr>
                            <tr><th scope="row">Office 2024 Home &amp; Business</th><td>€ 209,00</td><td>Licencia única — incluye Outlook</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="office-2024-vs-microsoft-365">
                        <strong>Office 2024 vs Microsoft 365 →</strong>
                        <span>Licencia única o suscripción: qué compensa de verdad.</span>
                    </a>
                    <a class="hub-guide__link-card" href="microsoft-365-family-vs-personal">
                        <strong>Microsoft 365 Family vs Personal →</strong>
                        <span>Cuántas personas pueden usarlo y qué cambia en el precio.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-office-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Preguntas frecuentes</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>¿Office 2024 recibe las mismas actualizaciones que Microsoft 365?</summary>
                                <div class="home-faq-body"><p>No: Office 2024 recibe actualizaciones de seguridad pero no las nuevas funciones que se lanzan vía suscripción, Copilot incluido — esas quedan exclusivas de Microsoft 365, según Microsoft.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>¿Puedo instalar una licencia única de Office en varios ordenadores?</summary>
                                <div class="home-faq-body"><p>Depende del producto: comprueba el número de dispositivos indicado en la ficha del título que compras.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>¿Qué pasa si no renuevo Microsoft 365?</summary>
                                <div class="home-faq-body"><p>Las apps pasan a modo de solo lectura y el espacio en la nube por encima de los límites gratuitos también queda en solo lectura, según las condiciones de Microsoft — tus archivos siguen siendo tuyos.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>¿Necesito Windows para usar Office, o también funciona en Mac?</summary>
                                <div class="home-faq-body"><p>Las versiones de Office 2024 y los planes de Microsoft 365 del catálogo indican la compatibilidad con Mac directamente en el título o en la ficha del producto.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "pt": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Qual escolher</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">Licença única ou subscrição? E que plano Microsoft 365</h2>
                <p class="pdp-sec__sub">O Office 2024/2021/2019 paga-se uma única vez e fica como está. O Microsoft 365 é uma subscrição que inclui Copilot AI, espaço na nuvem e atualizações contínuas das apps.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>As principais opções do catálogo</caption>
                        <thead>
                            <tr><th scope="col">Produto</th><th scope="col">Preço</th><th scope="col">Fórmula</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">Microsoft 365 Personal</th><td>€ 84,79 / ano</td><td>Subscrição — 1 pessoa, 1 TB na nuvem, Copilot AI</td></tr>
                            <tr><th scope="row">Microsoft 365 Family</th><td>€ 104,95 / ano</td><td>Subscrição — até 6 pessoas, 6 TB na nuvem no total</td></tr>
                            <tr><th scope="row">Office 2024 Home</th><td>€ 134,00</td><td>Licença única — PC/Mac, pagamento único</td></tr>
                            <tr><th scope="row">Office 2024 Home &amp; Business</th><td>€ 209,00</td><td>Licença única — inclui Outlook</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="office-2024-vs-microsoft-365">
                        <strong>Office 2024 vs Microsoft 365 →</strong>
                        <span>Licença única ou subscrição: o que compensa realmente.</span>
                    </a>
                    <a class="hub-guide__link-card" href="microsoft-365-family-vs-personal">
                        <strong>Microsoft 365 Family vs Personal →</strong>
                        <span>Quantas pessoas podem usá-lo e o que muda no preço.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-office-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Perguntas frequentes</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>O Office 2024 recebe as mesmas atualizações que o Microsoft 365?</summary>
                                <div class="home-faq-body"><p>Não: o Office 2024 recebe atualizações de segurança mas não as novas funcionalidades lançadas via subscrição, incluindo o Copilot — essas ficam exclusivas do Microsoft 365, segundo a Microsoft.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Posso instalar uma licença única do Office em vários computadores?</summary>
                                <div class="home-faq-body"><p>Depende do produto: verifique o número de dispositivos indicado na ficha do título que compra.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>O que acontece se não renovar o Microsoft 365?</summary>
                                <div class="home-faq-body"><p>As apps passam a modo só de leitura e o espaço na nuvem acima dos limites gratuitos também fica só de leitura, segundo as condições da Microsoft — os ficheiros continuam seus.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Preciso do Windows para usar o Office, ou também funciona em Mac?</summary>
                                <div class="home-faq-body"><p>As versões do Office 2024 e os planos Microsoft 365 do catálogo indicam a compatibilidade com Mac diretamente no título ou na ficha do produto.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
        "nl": """
        <section class="hub-guide pdp-page" aria-labelledby="hub-guide-title">
            <div class="hub-guide__inner">
                <p class="pdp-sec__eyebrow">Welke kiezen</p>
                <h2 id="hub-guide-title" class="pdp-sec__title">Eenmalige licentie of abonnement? En welk Microsoft 365-plan</h2>
                <p class="pdp-sec__sub">Office 2024/2021/2019 betaal je één keer en blijft zoals het is. Microsoft 365 is een abonnement met Copilot AI, cloudopslag en doorlopende app-updates.</p>

                <div class="cmp-table-wrap">
                    <table class="cmp-table">
                        <caption>De belangrijkste opties in de catalogus</caption>
                        <thead>
                            <tr><th scope="col">Product</th><th scope="col">Prijs</th><th scope="col">Formule</th></tr>
                        </thead>
                        <tbody>
                            <tr><th scope="row">Microsoft 365 Personal</th><td>€ 84,79 / jaar</td><td>Abonnement — 1 persoon, 1 TB cloud, Copilot AI</td></tr>
                            <tr><th scope="row">Microsoft 365 Family</th><td>€ 104,95 / jaar</td><td>Abonnement — tot 6 personen, 6 TB cloud in totaal</td></tr>
                            <tr><th scope="row">Office 2024 Home</th><td>€ 134,00</td><td>Eenmalige licentie — pc/Mac, één betaling</td></tr>
                            <tr><th scope="row">Office 2024 Home &amp; Business</th><td>€ 209,00</td><td>Eenmalige licentie — inclusief Outlook</td></tr>
                        </tbody>
                    </table>
                </div>

                <div class="hub-guide__links">
                    <a class="hub-guide__link-card" href="office-2024-vs-microsoft-365">
                        <strong>Office 2024 vs Microsoft 365 →</strong>
                        <span>Eenmalige licentie of abonnement: wat echt loont.</span>
                    </a>
                    <a class="hub-guide__link-card" href="microsoft-365-family-vs-personal">
                        <strong>Microsoft 365 Family vs Personal →</strong>
                        <span>Hoeveel personen het kunnen gebruiken en wat er verandert in de prijs.</span>
                    </a>
                </div>

                <div class="pdp-sec pdp-sec--tight pdp-faq" style="padding-inline:0;">
                    <h3 id="hub-office-faq-title" class="pdp-sec__title pdp-faq__title" style="font-size:var(--aml-text-lg);">Veelgestelde vragen</h3>
                    <div class="home-faq-list">
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Krijgt Office 2024 dezelfde updates als Microsoft 365?</summary>
                                <div class="home-faq-body"><p>Nee: Office 2024 krijgt beveiligingsupdates maar niet de nieuwe functies die via het abonnement worden uitgebracht, Copilot inbegrepen — die blijven exclusief voor Microsoft 365, volgens Microsoft.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Kan ik een eenmalige Office-licentie op meerdere computers installeren?</summary>
                                <div class="home-faq-body"><p>Dat hangt af van het product: controleer het aantal apparaten dat vermeld staat op de productpagina van de gekochte titel.</p></div>
                            </details>
                        </div>
                        <div class="pf-faq-col">
                            <details class="home-faq-item">
                                <summary>Wat gebeurt er als ik Microsoft 365 niet verleng?</summary>
                                <div class="home-faq-body"><p>De apps schakelen over naar alleen-lezen en cloudopslag boven de gratis limieten wordt eveneens alleen-lezen, volgens de voorwaarden van Microsoft — je bestanden blijven van jou.</p></div>
                            </details>
                            <details class="home-faq-item">
                                <summary>Heb ik Windows nodig om Office te gebruiken, of werkt het ook op Mac?</summary>
                                <div class="home-faq-body"><p>De Office 2024-versies en de Microsoft 365-plannen in de catalogus vermelden de Mac-compatibiliteit rechtstreeks in de titel of op de productpagina.</p></div>
                            </details>
                        </div>
                    </div>
                </div>
            </div>
        </section>
""",
    },
}


def get_hub_content(catalog_slug, lang):
    """Ritorna l'HTML della sezione guida per (catalog_slug, lang), o None."""
    return HUB_CONTENT.get(catalog_slug, {}).get(lang)
