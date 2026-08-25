#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contenuto guida aggiunto in coda alle pagine categoria (antivirus,
sistemi-operativi, suite-office) da build_catalog_page in product_page_lib.py.

Il product-grid resta generato dinamicamente dal catalogo: questo modulo
aggiunge solo la sezione statica "quale scegliere" + link ai confronti
dedicati + FAQ, per trasformare l'hub da lista prodotti a nodo semantico
(vedi roadmap SEO/GEO). Solo IT per ora: le altre lingue restano sul
template compatto finché i confronti non vengono tradotti.

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
                                <div class="home-faq-body"><p>Codice e istruzioni di attivazione via email, tipicamente entro pochi minuti dal pagamento.</p></div>
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
    },
}


def get_hub_content(catalog_slug, lang):
    """Ritorna l'HTML della sezione guida per (catalog_slug, lang), o None."""
    return HUB_CONTENT.get(catalog_slug, {}).get(lang)
