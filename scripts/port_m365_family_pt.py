#!/usr/bin/env python3
"""Port it/microsoft-365-family.html (pdp pilot) to pt only.

Standalone sibling of port_m365_family_locales.py: reuses the same
localize()/apply_pairs() logic but writes only pt/microsoft-365-family.html,
so it never touches the already-live it/en/fr/de/es pages.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "it" / "microsoft-365-family.html"

PT = [
    (
        "Microsoft 365 Family per 12 mesi, fino a 6 persone del gruppo famiglia: app Microsoft 365 e 1 TB OneDrive a persona. Copilot è riservato al titolare. Codice digitale via email in 5–15 minuti dal pagamento.",
        "Microsoft 365 Family durante 12 meses, para até 6 pessoas do grupo família Microsoft: apps Microsoft 365 e 1 TB de OneDrive por pessoa. O Copilot é reservado ao titular. Código digital por email em 5–15 minutos após o pagamento.",
    ),
    ("Microsoft 365 Family — 12 mesi", "Microsoft 365 Family — 12 meses"),
    (
        "L'email di consegna parte dopo la conferma del pagamento, di norma entro 5–15 minuti; in rari casi servono alcuni minuti in più per le verifiche del pagamento. Se dopo 30 minuti non hai ricevuto nulla, controlla anche spam e posta indesiderata e scrivi a Info@amlstore.it indicando prodotto acquistato ed email usata per l'ordine.",
        "O email de entrega é enviado após a confirmação do pagamento, normalmente dentro de 5–15 minutos; em casos raros são necessários mais alguns minutos para as verificações do pagamento. Se depois de 30 minutos não receberes nada, verifica também o spam/lixo eletrónico e escreve para Info@amlstore.it indicando o produto comprado e o email usado na encomenda.",
    ),
    (
        "Ricevi la product key di Microsoft 365 Family e le istruzioni per riscattarla sui portali ufficiali Microsoft. La consegna è solo digitale: non viene spedito alcun supporto fisico e non ci sono costi di spedizione.",
        "Recebes a product key do Microsoft 365 Family e as instruções para a resgatares nos portais oficiais Microsoft. A entrega é apenas digital: não é enviado nenhum suporte físico e não há custos de envio.",
    ),
    (
        "Al checkout sono disponibili carta, PayPal e wallet digitali come Apple Pay e Google Pay dove abilitati. L'elaborazione del pagamento è gestita in modo sicuro tramite Stripe.",
        "No checkout estão disponíveis cartão, PayPal e carteiras digitais como Apple Pay e Google Pay quando ativadas. O processamento do pagamento é feito de forma segura através da Stripe.",
    ),
    (
        "Sì. Al checkout scegli il profilo Azienda e inserisci partita IVA e Codice SDI oppure PEC: la fattura elettronica viene emessa su quei dati. Se ti serve dopo l'ordine, scrivi a Info@amlstore.it indicando l'email usata per l'ordine e il numero d'ordine.",
        "Sim. No checkout escolhe o perfil Empresa e introduz o NIF e os dados de faturação: a fatura eletrónica é emitida com esses dados. Se precisares depois da encomenda, escreve para Info@amlstore.it indicando o email usado na encomenda e o número de encomenda.",
    ),
    (
        "Vai su setup.office.com/Home, accedi con il tuo account Microsoft, inserisci il codice ricevuto via email e segui la procedura guidata. Al termine installa le app da office.com.",
        "Acede a setup.office.com/Home, inicia sessão com a tua conta Microsoft, introduz o código recebido por email e segue o processo guiado. No final instala as apps a partir de office.com.",
    ),
    (
        "Sì: il riscatto avviene su setup.office.com con il tuo account Microsoft. Se su quell'account è già attivo un abbonamento Microsoft 365, il comportamento (estensione o conversione del piano) segue le regole Microsoft mostrate durante il riscatto. Scegli l'account con attenzione: la licenza resta associata a quello usato al momento del riscatto.",
        "Sim: o resgate é feito em setup.office.com com a tua conta Microsoft. Se essa conta já tiver uma subscrição Microsoft 365 ativa, o comportamento (extensão ou conversão do plano) segue as regras Microsoft mostradas durante o resgate. Escolhe a conta com atenção: a licença fica associada à conta usada no momento do resgate.",
    ),
    (
        "Dopo l'attivazione sul tuo account Microsoft, usa le funzioni di condivisione del piano Family nell'area account Microsoft / abbonamenti, come indicato da Microsoft per il periodo di validità della licenza.",
        "Depois da ativação na tua conta Microsoft, usa as funções de partilha do plano Family na área conta Microsoft / subscrições, conforme indicado pela Microsoft para o período de validade da licença.",
    ),
    (
        "No. Le funzionalità Copilot comprese nel piano sono utilizzabili dal titolare dell'abbonamento. Gli altri cinque membri ricevono le app Microsoft 365, 1 TB di OneDrive ciascuno e Microsoft Defender, ma non le funzionalità AI.",
        "Não. As funcionalidades Copilot incluídas no plano podem ser usadas pelo titular da subscrição. Os outros cinco membros recebem as apps Microsoft 365, 1 TB de OneDrive cada e Microsoft Defender, mas não as funcionalidades de IA.",
    ),
    (
        "No. Ogni persona usa il proprio account Microsoft, con documenti, email, impostazioni e spazio OneDrive separati. La condivisione di singoli file o cartelle resta una scelta volontaria di chi li possiede.",
        "Não. Cada pessoa usa a sua própria conta Microsoft, com documentos, email, configurações e espaço OneDrive separados. A partilha de ficheiros ou pastas individuais continua a ser uma escolha voluntária de quem os possui.",
    ),
    (
        "Sì: con le app desktop installate puoi lavorare offline; servono comunque connessione e accesso periodici per la verifica della licenza, aggiornamenti e servizi cloud come OneDrive, come descritto da Microsoft.",
        "Sim: com as apps de secretária instaladas podes trabalhar offline; continuam a ser necessários ligação e acesso periódicos para a verificação da licença, atualizações e serviços cloud como o OneDrive, conforme descrito pela Microsoft.",
    ),
    (
        "Family è pensato per condividere il piano con il tuo gruppo famiglia Microsoft (fino a 6 persone), ciascuna con account e spazio OneDrive distinti. Personal copre un solo utente con 1 TB, secondo le condizioni Microsoft aggiornate.",
        "O Family foi pensado para partilhar o plano com o teu grupo família Microsoft (até 6 pessoas), cada uma com conta e espaço OneDrive distintos. O Personal cobre um único utilizador com 1 TB, segundo as condições Microsoft atualizadas.",
    ),
    (
        "No. Il codice attiva Microsoft 365 Family per 12 mesi con un pagamento una tantum: AML Store non addebita nulla automaticamente alla scadenza. Eventuali opzioni di rinnovo si gestiscono separatamente, direttamente nell'account Microsoft.",
        "Não. O código ativa o Microsoft 365 Family por 12 meses com um pagamento único: a AML Store não cobra nada automaticamente na expiração. Eventuais opções de renovação são geridas separadamente, diretamente na conta Microsoft.",
    ),
    (
        "Sì, puoi riscattarlo sullo stesso account che ha già Microsoft 365 Family attivo. Il modo in cui viene applicato (estensione della durata attuale o avvio di un nuovo periodo) segue le regole Microsoft mostrate al momento del riscatto su setup.office.com, non è qualcosa che decidiamo noi come rivenditore.",
        "Sim, podes resgatá-lo na mesma conta que já tem o Microsoft 365 Family ativo. A forma como é aplicado (extensão da duração atual ou início de um novo período) segue as regras Microsoft mostradas no momento do resgate em setup.office.com; não é algo que decidamos nós como revendedor.",
    ),
    (
        "Scrivici indicando numero d'ordine ed eventuale messaggio di errore. Verifichiamo il caso e, se viene confermato un difetto imputabile a noi o al fornitore della chiave, proponiamo sostituzione o rimborso nei tempi usuali di elaborazione. Assistenza: Info@amlstore.it — +39 392 558 0413.",
        "Escreve-nos indicando o número de encomenda e a eventual mensagem de erro. Analisamos o caso e, se se confirmar um defeito imputável a nós ou ao fornecedor da chave, propomos substituição ou reembolso nos prazos habituais de processamento. Assistência: Info@amlstore.it — +39 392 558 0413.",
    ),
    # UI chrome
    ("Vai al contenuto principale", "Ir para o conteúdo principal"),
    ("Acquisto rapido", "Compra rápida"),
    ("Microsoft 365 Family · 12 mesi", "Microsoft 365 Family · 12 meses"),
    ("Acquista ora", "Comprar agora"),
    ("Prodotto e acquisto", "Produto e compra"),
    ("Percorso navigazione", "Trilho de navegação"),
    ("Abbonamento digitale · 12 mesi", "Subscrição digital · 12 meses"),
    ("Codice articolo:", "Código do artigo:"),
    ("Microsoft 365 Family — grafica del prodotto", "Microsoft 365 Family — imagem do produto"),
    (
        "Microsoft 365 per te e altre cinque persone, con app complete e 1 TB di OneDrive personale per ciascun membro. Copilot è incluso per il titolare dell'abbonamento.",
        "Microsoft 365 para ti e mais cinco pessoas, com apps completas e 1 TB de OneDrive pessoal para cada membro. O Copilot está incluído para o titular da subscrição.",
    ),
    (
        "Microsoft 365 per te e altre cinque persone, con app complete e 1 TB di OneDrive personale per ciascun membro. Copilot è incluso per il titolare dell&#x27;abbonamento.",
        "Microsoft 365 para ti e mais cinco pessoas, com apps completas e 1 TB de OneDrive pessoal para cada membro. O Copilot está incluído para o titular da subscrição.",
    ),
    ("Fino a 6 persone, ognuna con il proprio account Microsoft", "Até 6 pessoas, cada uma com a sua própria conta Microsoft"),
    ("1 TB di OneDrive a persona, file e impostazioni separati", "1 TB de OneDrive por pessoa, ficheiros e configurações separados"),
    ("App desktop sempre aggiornate su PC, Mac, tablet e telefono", "Apps de secretária sempre atualizadas em PC, Mac, tablet e telemóvel"),
    ("Copilot per il titolare <em>— non condiviso con gli altri membri</em>", "Copilot para o titular <em>— não partilhado com os restantes membros</em>"),
    ("Prezzo AML Store", "Preço na AML Store"),
    ("Prezzi", "Preços"),
    ("Prezzo scontato 104,95 euro", "Preço com desconto 104,95 euros"),
    ("Prezzo originale 129 euro", "Preço original 129 euros"),
    ("Sconto 19 percento", "Desconto de 19 por cento"),
    (
        "IVA inclusa, nessun costo di spedizione. Risparmi <strong>€ 24,05</strong> rispetto al Microsoft Store (€ 129,00).",
        "IVA incluído, sem custos de envio. Poupas <strong>€ 24,05</strong> em relação à Microsoft Store (€ 129,00).",
    ),
    ("Aggiungi al carrello", "Adicionar ao carrinho"),
    ("Codice via email in 5–15 minuti dalla conferma del pagamento", "Código por email em 5–15 minutos após a confirmação do pagamento"),
    (
        "<strong>Incluso con l'acquisto:</strong> guida PDF all'utilizzo di Copilot, via email dopo l'ordine",
        "<strong>Incluído com a compra:</strong> guia PDF de utilização do Copilot, por email após a encomenda",
    ),
    ("Attivazione sui portali ufficiali Microsoft", "Ativação nos portais oficiais Microsoft"),
    ("Assistenza in italiano dopo l'acquisto", "Apoio após a compra"),
    ("Fattura elettronica disponibile", "Fatura eletrónica disponível"),
    ("Metodi di pagamento accettati", "Métodos de pagamento aceites"),
    (
        "Pagamenti protetti tramite <strong>Stripe</strong> e <strong>PayPal</strong>",
        "Pagamentos protegidos através de <strong>Stripe</strong> e <strong>PayPal</strong>",
    ),
    ("Azienda italiana", "Distribuidor europeu"),
    ("Sede e P.IVA in Italia", "Sede em Itália"),
    ("Fattura elettronica", "Fatura eletrónica"),
    ("Disponibile per privati e aziende", "Disponível para particulares e empresas"),
    ("Assistenza in italiano", "Apoio por escrito"),
    ("Supporto post-vendita via email", "Apoio por email e WhatsApp"),
    ("Pagamenti protetti", "Pagamentos protegidos"),
    ("Elaborati tramite Stripe e PayPal", "Processados via Stripe e PayPal"),
    ('data-cart-added-msg="Prodotto aggiunto al carrello."', 'data-cart-added-msg="Produto adicionado ao carrinho."'),
    ("Cosa ricevi", "O que recebes"),
    ("Sei persone, account e spazi separati", "Seis pessoas, contas e espaços separados"),
    (
        "Microsoft 365 Family è pensato per essere condiviso: ogni persona lavora sul proprio account, con il proprio spazio cloud.",
        "O Microsoft 365 Family foi pensado para ser partilhado: cada pessoa trabalha na sua própria conta, com o seu próprio espaço cloud.",
    ),
    ("Persone incluse", "Pessoas incluídas"),
    ("Titolare più 5 membri invitati, ognuno con account Microsoft separato.", "Titular mais 5 membros convidados, cada um com conta Microsoft separada."),
    ("OneDrive a persona", "OneDrive por pessoa"),
    ("Fino a 6 TB complessivi sul piano, non condivisi automaticamente.", "Até 6 TB no total no plano, não partilhados automaticamente."),
    ("Durata", "Duração"),
    ("Pagamento una tantum su AML Store, senza addebiti ricorrenti da parte nostra.", "Pagamento único na AML Store, sem cobranças recorrentes da nossa parte."),
    ("Dispositivi per persona", "Dispositivos por pessoa"),
    ("Accesso contemporaneo su PC, Mac, tablet e telefono, secondo le regole Microsoft.", "Acesso simultâneo em PC, Mac, tablet e telemóvel, segundo as regras Microsoft."),
    ("Specifiche del prodotto", "Especificações do produto"),
    ("Scheda tecnica", "Ficha técnica"),
    ("Specifiche tecniche e commerciali di Microsoft 365 Family", "Especificações técnicas e comerciais do Microsoft 365 Family"),
    ("Prodotto", "Produto"),
    ("Utenti", "Utilizadores"),
    ("Fino a 6 persone", "Até 6 pessoas"),
    ("Fino a 6", "Até 6"),
    ("Archiviazione", "Armazenamento"),
    ("1 TB OneDrive per persona", "1 TB OneDrive por pessoa"),
    ("Dispositivi", "Dispositivos"),
    ("Fino a 5 contemporanei per persona", "Até 5 simultâneos por pessoa"),
    ("Incluso per il titolare dell'abbonamento", "Incluído para o titular da subscrição"),
    ("Consegna", "Entrega"),
    ("Codice digitale via email", "Código digital por email"),
    ("Attivazione", "Ativação"),
    ("Account Microsoft, su setup.office.com", "Conta Microsoft, em setup.office.com"),
    ("Rinnovo", "Renovação"),
    ("Nuova attivazione o estensione secondo le regole Microsoft", "Nova ativação ou extensão segundo as regras Microsoft"),
    ("Codice prodotto", "Código do produto"),
    ("Fatturazione", "Faturação"),
    ("IVA inclusa, fattura elettronica disponibile", "IVA incluído, fatura eletrónica disponível"),
    ("Chi riceve cosa", "Quem recebe o quê"),
    ("Un abbonamento condiviso, sei esperienze separate", "Uma subscrição partilhada, seis experiências separadas"),
    (
        "Ogni persona utilizza il proprio account Microsoft. Documenti, email, fotografie e spazio cloud non vengono condivisi automaticamente con gli altri membri. L'unica differenza reale riguarda le funzionalità Copilot.",
        "Cada pessoa utiliza a sua própria conta Microsoft. Documentos, email, fotografias e espaço cloud não são partilhados automaticamente com os outros membros. A única diferença real está nas funcionalidades Copilot.",
    ),
    ("Confronto tra titolare dell'abbonamento e altri membri del gruppo famiglia", "Comparação entre o titular da subscrição e os outros membros do grupo família"),
    ("Funzionalità", "Funcionalidade"),
    ("Titolare", "Titular"),
    ("Altri 5 membri", "Outros 5 membros"),
    ("Incluso", "Incluído"),
    ("Non incluso", "Não incluído"),
    ("Word, Excel, PowerPoint e Outlook", "Word, Excel, PowerPoint e Outlook"),
    ("1 TB di OneDrive personale", "1 TB de OneDrive pessoal"),
    ("Account, file e impostazioni separati", "Contas, ficheiros e configurações separados"),
    ("Installazione su più dispositivi", "Instalação em vários dispositivos"),
    ("Funzionalità Copilot", "Funcionalidades Copilot"),
    ("Le funzioni AI comprese nel piano restano al proprietario dell'abbonamento.", "As funções de IA incluídas no plano ficam com o titular da subscrição."),
    ("App incluse", "Apps incluídas"),
    ("Tutte le app che usi, su tutti i tuoi dispositivi", "Todas as apps que usas, em todos os teus dispositivos"),
    (
        "Installa le applicazioni desktop supportate e continua a lavorare anche offline. I documenti possono essere sincronizzati tramite OneDrive.",
        "Instala as aplicações de secretária suportadas e continua a trabalhar mesmo offline. Os documentos podem ser sincronizados através do OneDrive.",
    ),
    ("Solo titolare", "Apenas o titular"),
    ("Vedi tutte le app incluse", "Ver todas as apps incluídas"),
    ("Famiglia che usa laptop e dispositivi insieme in un ambiente domestico luminoso e moderno.", "Família a usar portáteis e dispositivos juntos numa casa luminosa e moderna."),
    ("Condivisione", "Partilha"),
    ("Un piano, account separati", "Um plano, contas separadas"),
    (
        "Inviti fino a cinque persone dal tuo account Microsoft. Ognuna riceve il proprio spazio cloud, le proprie app e le proprie impostazioni: nessuno vede i documenti degli altri.",
        "Convida até cinco pessoas a partir da tua conta Microsoft. Cada uma recebe o seu próprio espaço cloud, apps e configurações: ninguém vê os documentos dos outros.",
    ),
    ("Le sei postazioni del piano", "Os seis lugares do plano"),
    ("Membro 2", "Membro 2"),
    ("Membro 3", "Membro 3"),
    ("Membro 4", "Membro 4"),
    ("Membro 5", "Membro 5"),
    ("Membro 6", "Membro 6"),
    ("Tutti ricevono le stesse app. Cambia solo Copilot, che resta al titolare.", "Todos recebem as mesmas apps. Só o Copilot muda — fica com o titular."),
    ("Quale scegliere", "Qual escolher"),
    ("Confronta i piani Microsoft 365", "Compara os planos Microsoft 365"),
    (
        "La differenza non è la potenza delle app: è quante persone useranno davvero il piano.",
        "A diferença não é a potência das apps: é quantas pessoas vão realmente usar o plano.",
    ),
    ("Confronto tra Microsoft 365 Personal e Microsoft 365 Family", "Comparação entre Microsoft 365 Personal e Microsoft 365 Family"),
    ("Persone", "Pessoas"),
    ("Spazio OneDrive", "Espaço OneDrive"),
    ("1 TB a persona", "1 TB por pessoa"),
    ("Account separati per ogni utente", "Conta separada por utilizador"),
    ("Non previsto", "Não aplicável"),
    ("Prezzo su AML Store", "Preço na AML Store"),
    ("Ideale per", "Ideal para"),
    ("Chi usa Office da solo", "Quem usa o Office a solo"),
    ("Due o più persone", "Duas ou mais pessoas"),
    (
        'Scegli Family se almeno due persone useranno realmente le app o lo spazio OneDrive. Altrimenti valuta <a href="/en/microsoft-365-personal">Microsoft 365 Personal</a>.',
        'Escolhe Family se pelo menos duas pessoas forem realmente usar as apps ou o espaço OneDrive. Caso contrário, considera <a href="/pt/microsoft-365-personal">Microsoft 365 Personal</a>.',
    ),
    ("Come funziona", "Como funciona"),
    ("Tre passi per iniziare", "Três passos para começar"),
    ("Completa l'ordine", "Conclui a encomenda"),
    ("Paga con uno dei metodi disponibili al checkout: carta, PayPal o wallet digitali.", "Paga com um dos métodos disponíveis no checkout: cartão, PayPal ou carteiras digitais."),
    ("Ricevi il codice", "Recebe o código"),
    ("Product key e istruzioni arrivano via email in 5–15 minuti dalla conferma del pagamento.", "A product key e as instruções chegam por email em 5–15 minutos após a confirmação do pagamento."),
    ("Attiva su Microsoft", "Ativa na Microsoft"),
    (
        'Accedi con il tuo account e riscatta il codice su <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com</a>, poi installa le app da <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.',
        'Inicia sessão com a tua conta e resgata o código em <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com</a>, depois instala as apps a partir de <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.',
    ),
    (
        "<strong>Controlla di usare l'account Microsoft corretto:</strong> la licenza viene associata all'account scelto durante il riscatto e non può essere spostata successivamente.",
        "<strong>Confirma que usas a conta Microsoft correta:</strong> a licença é associada à conta escolhida no momento do resgate e não pode ser transferida depois.",
    ),
    ("Cosa dicono i clienti", "O que dizem os clientes"),
    (
        "Le recensioni sono pubblicate e verificate da Trustpilot: le leggi direttamente sulla piattaforma, senza filtri da parte nostra.",
        "As avaliações são publicadas e verificadas pelo Trustpilot: lê-las diretamente na plataforma, sem filtros da nossa parte.",
    ),
    (
        'Esperienze reali dei clienti su Trustpilot. <a href="https://www.trustpilot.com/review/aml-store.com" target="_blank" rel="noopener noreferrer">Trustpilot</a>',
        'Experiências reais de clientes no Trustpilot. <a href="https://pt.trustpilot.com/review/aml-store.com" target="_blank" rel="noopener noreferrer">Trustpilot</a>',
    ),
    ("Leggi tutte le recensioni", "Lê todas as avaliações"),
    ("Acquista con maggiore tranquillità", "Compra com mais tranquilidade"),
    ("Rivenditore europeo", "Distribuidor europeu"),
    ("AML Store ha sede legale in Italia", "A AML Store tem sede legal em Itália"),
    ("Fattura disponibile", "Fatura disponível"),
    ("Documentazione per privati e aziende", "Documentação para particulares e empresas"),
    ("Supporto scritto", "Apoio por escrito"),
    ("Assistenza via email e WhatsApp", "Apoio por email e WhatsApp"),
    ("Transazioni tramite Stripe e PayPal", "Transações via Stripe e PayPal"),
    ("Domande frequenti", "Perguntas frequentes"),
    ("Le risposte prima dell'acquisto", "As respostas antes de comprar"),
    ("Acquisto e consegna", "Compra e entrega"),
    ("Quando ricevo il codice dopo il pagamento?", "Quando recebo o código depois do pagamento?"),
    (
        "L'email di consegna parte dopo la conferma del pagamento, di norma entro 5–15 minuti; in rari casi servono alcuni minuti in più per le verifiche del pagamento.",
        "O email de entrega é enviado após a confirmação do pagamento, normalmente dentro de 5–15 minutos; em casos raros são necessários mais alguns minutos para as verificações do pagamento.",
    ),
    (
        'Se dopo <strong>30 minuti</strong> non hai ricevuto nulla, controlla anche spam e posta indesiderata e scrivi a <a href="mailto:Info@amlstore.it">Info@amlstore.it</a> indicando prodotto acquistato ed email usata per l\'ordine.',
        'Se depois de <strong>30 minutos</strong> não receberes nada, verifica também o spam/lixo eletrónico e escreve para <a href="mailto:Info@amlstore.it">Info@amlstore.it</a> indicando o produto comprado e o email usado na encomenda.',
    ),
    # JSON-LD FAQPage text fields escape the href quotes with backslashes and
    # this particular answer keeps a "2-15" typo instead of "5-15": needs its
    # own pair, distinct from the visible-body FAQ answer above.
    (
        'L\'email di consegna parte dopo la conferma del pagamento, di norma entro 2\u201315 minuti; in rari casi servono alcuni minuti in più per le verifiche del pagamento. Se dopo <strong>30 minuti</strong> non hai ricevuto nulla, controlla anche spam e posta indesiderata e scrivi a <a href=\\"mailto:Info@amlstore.it\\">Info@amlstore.it</a> indicando prodotto acquistato ed email usata per l\'ordine.',
        'O email de entrega é enviado após a confirmação do pagamento, normalmente dentro de 2\u201315 minutos; em casos raros são necessários mais alguns minutos para as verificações do pagamento. Se depois de <strong>30 minutos</strong> não receberes nada, verifica também o spam/lixo eletrónico e escreve para <a href=\\"mailto:Info@amlstore.it\\">Info@amlstore.it</a> indicando o produto comprado e o email usado na encomenda.',
    ),
    (
        'Se ti serve dopo l\'ordine, scrivi a <a href=\\"mailto:Info@amlstore.it\\">Info@amlstore.it</a> indicando l\'email usata per l\'ordine e il numero d\'ordine.',
        'Se precisares depois da encomenda, escreve para <a href=\\"mailto:Info@amlstore.it\\">Info@amlstore.it</a> indicando o email usado na encomenda e o número de encomenda.',
    ),
    (
        'Assistenza: <a href=\\"mailto:Info@amlstore.it\\">Info@amlstore.it</a> — +39 392 558 0413.',
        'Assistência: <a href=\\"mailto:Info@amlstore.it\\">Info@amlstore.it</a> — +39 392 558 0413.',
    ),
    ("Posso riscattare il codice su un account che ha già Microsoft 365 attivo?", "Posso resgatar o código numa conta que já tem o Microsoft 365 ativo?"),
    (
        "Sì: il riscatto avviene su setup.office.com con il tuo account Microsoft, anche se ha già un abbonamento Microsoft 365 Family attivo. Il modo in cui viene applicato — estensione della durata attuale, avvio di un nuovo periodo o conversione del piano — segue le regole Microsoft mostrate al momento del riscatto, non è qualcosa che decidiamo noi come rivenditore. <strong>Scegli l'account con attenzione:</strong> la licenza resta associata a quello usato al momento del riscatto.",
        "Sim: o resgate é feito em setup.office.com com a tua conta Microsoft, mesmo que já tenha uma subscrição Microsoft 365 Family ativa. A forma como é aplicado — extensão da duração atual, início de um novo período ou conversão do plano — segue as regras Microsoft mostradas no momento do resgate; não é algo que decidamos nós como revendedor. <strong>Escolhe a conta com atenção:</strong> a licença fica associada à conta usada no momento do resgate.",
    ),
    ("Cosa ricevo esattamente nell'email?", "O que recebo exatamente no email?"),
    (
        "Ricevi la <strong>product key</strong> di Microsoft 365 Family e le istruzioni per riscattarla sui portali ufficiali Microsoft.",
        "Recebes a <strong>product key</strong> do Microsoft 365 Family e as instruções para a resgatares nos portais oficiais Microsoft.",
    ),
    (
        "La consegna è solo digitale: non viene spedito alcun supporto fisico e non ci sono costi di spedizione.",
        "A entrega é apenas digital: não é enviado nenhum suporte físico e não há custos de envio.",
    ),
    ("Quali metodi di pagamento posso usare?", "Que métodos de pagamento posso usar?"),
    (
        'Al checkout sono disponibili carta, PayPal e wallet digitali come Apple Pay e Google Pay dove abilitati. L\'elaborazione del pagamento è gestita in modo sicuro tramite <strong>Stripe</strong>.',
        'No checkout estão disponíveis cartão, PayPal e carteiras digitais como Apple Pay e Google Pay quando ativadas. O processamento do pagamento é feito de forma segura através da <strong>Stripe</strong>.',
    ),
    ("Posso avere la fattura elettronica?", "Posso ter fatura eletrónica?"),
    (
        "Sì. Al checkout scegli il profilo <strong>Azienda</strong> e inserisci partita IVA e Codice SDI oppure PEC: la fattura elettronica viene emessa su quei dati.",
        "Sim. No checkout escolhe o perfil <strong>Empresa</strong> e introduz o NIF e os dados de faturação: a fatura eletrónica é emitida com esses dados.",
    ),
    (
        'Se ti serve dopo l\'ordine, scrivi a <a href="mailto:Info@amlstore.it">Info@amlstore.it</a> indicando l\'email usata per l\'ordine e il numero d\'ordine.',
        'Se precisares depois da encomenda, escreve para <a href="mailto:Info@amlstore.it">Info@amlstore.it</a> indicando o email usado na encomenda e o número de encomenda.',
    ),
    ("Attivazione e account", "Ativação e conta"),
    ("Come si attiva Microsoft 365 Family dopo l'acquisto?", "Como se ativa o Microsoft 365 Family depois da compra?"),
    (
        'Vai su <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com/Home</a>, accedi con il tuo account Microsoft, inserisci il codice ricevuto via email e segui la procedura guidata. Al termine installa le app da <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.',
        'Acede a <a href="https://setup.office.com/Home" target="_blank" rel="noopener noreferrer">setup.office.com/Home</a>, inicia sessão com a tua conta Microsoft, introduz o código recebido por email e segue o processo guiado. No final instala as apps a partir de <a href="https://www.office.com" target="_blank" rel="noopener noreferrer">office.com</a>.',
    ),
    ("Posso riscattare il codice su un account Microsoft che uso già?", "Posso resgatar o código numa conta Microsoft que já uso?"),
    (
        "Sì: il riscatto avviene su setup.office.com con il tuo account Microsoft. Se su quell'account è già attivo un abbonamento Microsoft 365, il comportamento (estensione o conversione del piano) segue le regole Microsoft mostrate durante il riscatto.",
        "Sim: o resgate é feito em setup.office.com com a tua conta Microsoft. Se essa conta já tiver uma subscrição Microsoft 365 ativa, o comportamento (extensão ou conversão do plano) segue as regras Microsoft mostradas durante o resgate.",
    ),
    (
        "<strong>Scegli l'account con attenzione:</strong> la licenza resta associata a quello usato al momento del riscatto.",
        "<strong>Escolhe a conta com atenção:</strong> a licença fica associada à conta usada no momento do resgate.",
    ),
    ("Membri e funzionalità", "Membros e funcionalidades"),
    ("Come si invitano altri membri dopo l'acquisto?", "Como se convidam outros membros depois da compra?"),
    ("Copilot è disponibile per tutti i membri?", "O Copilot está disponível para todos os membros?"),
    (
        "No. Le funzionalità Copilot comprese nel piano sono utilizzabili dal <strong>titolare dell'abbonamento</strong>.",
        "Não. As funcionalidades Copilot incluídas no plano podem ser usadas pelo <strong>titular da subscrição</strong>.",
    ),
    (
        "Gli altri cinque membri ricevono le app Microsoft 365, 1 TB di OneDrive ciascuno e Microsoft Defender, ma non le funzionalità AI.",
        "Os outros cinco membros recebem as apps Microsoft 365, 1 TB de OneDrive cada e Microsoft Defender, mas não as funcionalidades de IA.",
    ),
    ("I file sono condivisi automaticamente tra i membri?", "Os ficheiros são partilhados automaticamente entre os membros?"),
    (
        "Sì: con le app desktop installate puoi lavorare offline; servono comunque connessione e accesso periodici per la verifica della licenza, aggiornamenti e servizi cloud come OneDrive.",
        "Sim: com as apps de secretária instaladas podes trabalhar offline; continuam a ser necessários ligação e acesso periódicos para a verificação da licença, atualizações e serviços cloud como o OneDrive.",
    ),
    ("Scelta del piano e assistenza", "Escolha do plano e apoio"),
    ("Qual è la differenza tra Microsoft 365 Family e Personal?", "Qual é a diferença entre o Microsoft 365 Family e o Personal?"),
    ("Il codice si rinnova automaticamente dopo 12 mesi?", "O código renova-se automaticamente depois de 12 meses?"),
    ("Posso usare il codice per rinnovare un abbonamento Family già attivo?", "Posso usar o código para renovar uma subscrição Family já ativa?"),
    ("Cosa succede se il codice non funziona?", "O que acontece se o código não funcionar?"),
    (
        "Scrivici indicando numero d'ordine ed eventuale messaggio di errore. Verifichiamo il caso e, se viene confermato un difetto imputabile a noi o al fornitore della chiave, proponiamo sostituzione o rimborso nei tempi usuali di elaborazione.",
        "Escreve-nos indicando o número de encomenda e a eventual mensagem de erro. Analisamos o caso e, se se confirmar um defeito imputável a nós ou ao fornecedor da chave, propomos substituição ou reembolso nos prazos habituais de processamento.",
    ),
    (
        'Assistenza: <a href="mailto:Info@amlstore.it">Info@amlstore.it</a> — +39 392 558 0413.',
        'Assistência: <a href="mailto:Info@amlstore.it">Info@amlstore.it</a> — +39 392 558 0413.',
    ),
    ("Requisiti di sistema", "Requisitos do sistema"),
    ("Compatibilità e requisiti tecnici", "Compatibilidade e requisitos técnicos"),
    (
        "Valori indicativi da documentazione Microsoft. Verifica sempre i requisiti aggiornati sulla scheda ufficiale Microsoft prima dell'installazione.",
        "Valores indicativos da documentação Microsoft. Verifica sempre os requisitos atualizados na ficha oficial Microsoft antes da instalação.",
    ),
    ("Sistemi operativi supportati", "Sistemas operativos suportados"),
    (
        "Windows 10 o versioni successive; le tre versioni più recenti di macOS; iOS e Android nelle versioni supportate da Microsoft.",
        "Windows 10 ou versões posteriores; as três versões mais recentes do macOS; iOS e Android nas versões suportadas pela Microsoft.",
    ),
    ("Processore e memoria", "Processador e memória"),
    (
        "Windows: processore a 1,6 GHz o superiore, due core. Mac: processore Intel o Apple Silicon compatibile con la versione di macOS supportata.",
        "Windows: processador a 1,6 GHz ou superior, dois núcleos. Mac: processador Intel ou Apple Silicon compatível com a versão de macOS suportada.",
    ),
    (
        "Memoria: 4 GB di RAM per le versioni a 64 bit, 2 GB per quelle a 32 bit.",
        "Memória: 4 GB de RAM para as versões de 64 bits, 2 GB para as de 32 bits.",
    ),
    ("Spazio su disco", "Espaço em disco"),
    (
        "Circa 4 GB di spazio disponibile su Windows e circa 10 GB su macOS, a seconda delle app installate.",
        "Cerca de 4 GB de espaço disponível no Windows e cerca de 10 GB no macOS, dependendo das apps instaladas.",
    ),
    ("Connessione e account Microsoft", "Ligação e conta Microsoft"),
    (
        "Servono un account Microsoft e una connessione internet per riscatto, attivazione, aggiornamenti e servizi cloud. Le app desktop installate funzionano anche offline, con verifiche periodiche della licenza.",
        "São necessárias uma conta Microsoft e uma ligação à Internet para o resgate, ativação, atualizações e serviços cloud. As apps de secretária instaladas funcionam também offline, com verificações periódicas da licença.",
    ),
    ("Microsoft 365 per tutta la famiglia", "Microsoft 365 para toda a família"),
    (
        "12 mesi · Fino a 6 persone · 1 TB ciascuno · Codice via email in 5–15 minuti.",
        "12 meses · Até 6 pessoas · 1 TB cada · Código por email em 5–15 minutos.",
    ),
    ("IVA inclusa, anziché € 129,00", "IVA incluído, em vez de € 129,00"),
    ("12 mesi", "12 meses"),
]


def apply_pairs(text: str, pairs: list[tuple[str, str]]) -> str:
    for src, dst in sorted(pairs, key=lambda p: len(p[0]), reverse=True):
        if src not in text:
            continue
        text = text.replace(src, dst)
    return text


def localize(html: str, lang: str, og: str, tp_host: str, tp_locale: str, pairs: list[tuple[str, str]]) -> str:
    out = html
    out = out.replace('lang="it"', f'lang="{lang}"', 1)
    out = out.replace("og:locale\" content=\"it_IT\"", f"og:locale\" content=\"{og}\"")
    out = out.replace('"inLanguage": "it"', f'"inLanguage": "{lang}"')

    # Protect the alternate hreflang block (it/en/fr/de/es self-links must stay
    # pointing at their own real page) before the generic /it/ -> /{lang}/ swap,
    # then patch only the canonical/og:url/product @id occurrences plus add pt.
    hreflang_block = (
        '    <link rel="alternate" hreflang="it" href="https://aml-store.com/it/microsoft-365-family">\n'
        '    <link rel="alternate" hreflang="en" href="https://aml-store.com/en/microsoft-365-family">\n'
        '    <link rel="alternate" hreflang="fr" href="https://aml-store.com/fr/microsoft-365-family">\n'
        '    <link rel="alternate" hreflang="de" href="https://aml-store.com/de/microsoft-365-family">\n'
        '    <link rel="alternate" hreflang="es" href="https://aml-store.com/es/microsoft-365-family">\n'
        '    <link rel="alternate" hreflang="x-default" href="https://aml-store.com/it/microsoft-365-family">'
    )
    hreflang_placeholder = "\x00HREFLANG_BLOCK\x00"
    assert hreflang_block in out, "hreflang block not found as expected"
    out = out.replace(hreflang_block, hreflang_placeholder, 1)

    lang_switcher_hrefs = [
        'href="/it/microsoft-365-family" class="lang-option active" role="menuitem" hreflang="it" aria-current="true"',
    ]
    switcher_placeholder = "\x00LANG_SWITCHER_SELF\x00"
    for original in lang_switcher_hrefs:
        if original in out:
            out = out.replace(original, switcher_placeholder, 1)

    out = out.replace("https://aml-store.com/it/", f"https://aml-store.com/{lang}/")
    out = out.replace('href="/it/', f'href="/{lang}/')

    new_hreflang_block = hreflang_block[:-len(
        '    <link rel="alternate" hreflang="x-default" href="https://aml-store.com/it/microsoft-365-family">'
    )] + (
        f'    <link rel="alternate" hreflang="{lang}" href="https://aml-store.com/{lang}/microsoft-365-family">\n'
        '    <link rel="alternate" hreflang="x-default" href="https://aml-store.com/it/microsoft-365-family">'
    )
    out = out.replace(hreflang_placeholder, new_hreflang_block, 1)
    out = out.replace(
        switcher_placeholder,
        f'href="/{lang}/microsoft-365-family" class="lang-option active" role="menuitem" hreflang="{lang}" aria-current="true"',
        1,
    )

    out = out.replace("https://it.trustpilot.com/review/aml-store.com", f"https://{tp_host}/review/aml-store.com")
    out = out.replace('data-locale="it-IT"', f'data-locale="{tp_locale}"')
    out = apply_pairs(out, pairs)
    return out


def leftover_italian(html: str) -> list[str]:
    markers = [
        "Vai al", "Acquista", "Aggiungi", "Abbonamento digitale", "Codice articolo",
        "Prezzo AML", "Cosa ricevi", "Scheda tecnica", "Titolare", "Membro ",
        "Domande frequenti", "fattura elettronica", "Assistenza in italiano",
        "Azienda italiana", "mesi", "Persone incluse", "Come funziona",
    ]
    hits = []
    for m in markers:
        if m in html:
            hits.append(m)
    return hits


COPILOT_NOTE_RE = re.compile(
    r'\n*\s*<p class="pdp-note">\s*<svg[^>]*>.*?</svg>\s*<span><strong>[^<]*Copilot[^<]*</strong>.*?</span>\s*</p>',
    re.S,
)


def strip_copilot_bonus(html: str) -> str:
    """Toglie la nota "guida Copilot in omaggio", che e' solo italiana.

    Il PDF viene allegato all'email solo per gli ordini it (GUIDE_LOCALES in
    functions/api/_lib/guide.js), e _render_copilot_bonus in product_page_lib
    la emette solo per lang == "it". Questa pagina non e' generata ma portata
    dall'italiano, quindi la nota va tolta qui: altrimenti il portoghese
    promette un allegato che non arrivera' mai.
    """
    return COPILOT_NOTE_RE.sub("", html)


def main() -> None:
    src = SRC.read_text(encoding="utf-8")
    out = localize(src, "pt", "pt_PT", "pt.trustpilot.com", "pt-PT", PT)
    out = strip_copilot_bonus(out)
    path = ROOT / "pt" / "microsoft-365-family.html"
    path.write_text(out, encoding="utf-8", newline="\n")
    left = leftover_italian(out)
    print(f"pt: wrote {path.relative_to(ROOT)} ({len(out)} bytes) leftovers={left[:8]}")


if __name__ == "__main__":
    main()
