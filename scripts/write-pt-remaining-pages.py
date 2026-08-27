#!/usr/bin/env python3
"""Port remaining hand-written pages to pt/ from es/ (home, 404, M365 solutions).

Strips inlined chrome (header/footer) to empty tags so build-inline-chrome
can fill them. Applies a European-Portuguese replacement list on the
visible copy. Does not touch the plan file.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Longest-first. Spanish source → European Portuguese.
ES_PT = [
    (
        "Antivirus y software original con entrega digital, activación en portales oficiales, factura y asistencia humana.",
        "Antivírus e software original com entrega digital, ativação em portais oficiais, fatura e assistência humana.",
    ),
    (
        "Antivirus original y licencias digitales | Eurolicenze",
        "Antivírus original e licenças digitais | Eurolicenze",
    ),
    (
        "Antivirus y suscripciones digitales originales. Activación en portales oficiales, asistencia humana, factura disponible.",
        "Antivírus e subscrições digitais originais. Ativação em portais oficiais, assistência humana, fatura disponível.",
    ),
    (
        "La página que buscas no existe o se ha movido. Busca un producto, explora las categorías o vuelve a la página de inicio de Eurolicenze.",
        "A página que procura não existe ou foi movida. Pesquise um produto, explore as categorias ou volte à página inicial da Eurolicenze.",
    ),
    (
        "Microsoft 365: Office, OneDrive, seguridad y Copilot en una suite que evoluciona. Licencias digitales para casa, equipos y volumen — encuentra tu plan en Eurolicenze.",
        "Microsoft 365: Office, OneDrive, segurança e Copilot numa suite em evolução. Licenças digitais para casa, equipas e volume — encontre o seu plano na Eurolicenze.",
    ),
    (
        "Crea, colabora y protege tu trabajo con Microsoft 365. Licencias digitales originales en Eurolicenze.",
        "Crie, colabore e proteja o seu trabalho com Microsoft 365. Licenças digitais originais na Eurolicenze.",
    ),
    ("Página no encontrada — Eurolicenze", "Página não encontrada — Eurolicenze"),
    ("Ir al contenido principal", "Ir para o conteúdo principal"),
    ("Protección original", "Proteção original"),
    ("entrega en 2–15 minutos.", "entrega em 2–15 minutos."),
    ("Valorado Excelente en Trustpilot", "Avaliado Excelente no Trustpilot"),
    ("Valorado <strong>Excelente</strong> en Trustpilot", "Avaliado <strong>Excelente</strong> no Trustpilot"),
    ("Marcas que ofrecemos", "Marcas que oferecemos"),
    ("Los más vendidos", "Os mais vendidos"),
    ("Licencias más solicitadas, precios claros y entrega digital inmediata.", "Licenças mais pedidas, preços claros e entrega digital imediata."),
    ("Añadir al carrito", "Adicionar ao carrinho"),
    ("Suscripción 12 meses", "Subscrição 12 meses"),
    ("hasta 6 usuarios", "até 6 utilizadores"),
    ("licencia digital", "licença digital"),
    ("Licencia perpetua", "Licença perpétua"),
    ("Pack · Windows de por vida", "Pacote · Windows vitalício"),
    ("Encuentra la protección adecuada", "Encontre a proteção adequada"),
    ("Elige cuántos dispositivos cubrir y compara los planes.", "Escolha quantos dispositivos proteger e compare os planos."),
    ("Recomendado", "Recomendado"),
    ("Protección esencial", "Proteção essencial"),
    ("Protección recomendada", "Proteção recomendada"),
    ("Protección completa", "Proteção completa"),
    ("Protección avanzada con privacidad extra.", "Proteção avançada com privacidade extra."),
    ("Protección esencial para el uso diario.", "Proteção essencial para o uso diário."),
    ("Seguridad completa para trabajo, compras y navegación.", "Segurança completa para trabalho, compras e navegação."),
    ("Antivirus, VPN y copia de seguridad en la nube para un dispositivo.", "Antivírus, VPN e cópia de segurança na nuvem para um dispositivo."),
    ("Antivirus, firewall y gestor de contraseñas en una sola suite.", "Antivírus, firewall e gestor de palavras-passe numa só suite."),
    ("Protección antivirus multicapa con anti-phishing y antifraude.", "Proteção antivírus multicamada com anti-phishing e antifraude."),
    ("Análisis antivirus en tiempo real", "Análise antivírus em tempo real"),
    ("Protección anti-phishing", "Proteção anti-phishing"),
    ("Impacto mínimo en el rendimiento", "Impacto mínimo no desempenho"),
    ("Antivirus y firewall", "Antivírus e firewall"),
    ("Gestor de contraseñas incluido", "Gestor de palavras-passe incluído"),
    ("Protección web y anti-phishing", "Proteção web e anti-phishing"),
    ("Antivirus multicapa", "Antivírus multicamada"),
    ("Anti-phishing y antifraude", "Anti-phishing e antifraude"),
    ("Cobertura amplia", "Cobertura ampla"),
    ("Dispositivos", "Dispositivos"),
    ("1 dispositivoo", "1 dispositivo"),
    ("1 dispositivo", "1 dispositivo"),
    ("/ año", "/ ano"),
    ("Ideal para:", "Ideal para:"),
    ("uso personal y navegación diaria", "uso pessoal e navegação diária"),
    ("casa, trabajo y compras online", "casa, trabalho e compras online"),
    ("usuarios avanzados y familias", "utilizadores avançados e famílias"),
    ("proteger muchos dispositivos a la vez", "proteger muitos dispositivos ao mesmo tempo"),
    ("un solo dispositivo, uso personal", "um só dispositivo, uso pessoal"),
    ("familias con varios dispositivos", "famílias com vários dispositivos"),
    ("Saber más", "Saber mais"),
    ("Cómo funciona", "Como funciona"),
    ("Compra, paga y recibe la licencia por email.", "Compre, pague e receba a licença por email."),
    ("Elige el producto", "Escolha o produto"),
    ("Paga de forma segura", "Pague de forma segura"),
    ("Activa en el portal oficial", "Ative no portal oficial"),
    ("Guía incluida", "Guia incluído"),
    ("Preguntas frecuentes", "Perguntas frequentes"),
    ("¿Qué recibo exactamente después de la compra?", "O que recebo exatamente após a compra?"),
    ("¿Cuánto tarda el email con la licencia?", "Quanto tempo demora o email com a licença?"),
    ("¿Nunca he comprado una licencia digital: cómo funciona de principio a fin?", "Nunca comprei uma licença digital: como funciona do início ao fim?"),
    ("¿El precio es más bajo que en otros sitios: la licencia es regular?", "O preço é mais baixo do que noutros sítios: a licença é regular?"),
    ("¿Dónde introduzco el código y cómo instalo el software?", "Onde introduzo o código e como instalo o software?"),
    ("¿Cómo os contacto por problemas con el pedido, el pago o la activación?", "Como vos contacto por problemas com a encomenda, o pagamento ou a ativação?"),
    ("Página no encontrada", "Página não encontrada"),
    ("La dirección que has abierto no existe o se ha movido. Reconstruimos el sitio recientemente: un enlace guardado en favoritos, o publicado en otro sitio, puede apuntar a una página que cambió de dirección.", "O endereço que abriu não existe ou foi movido. Reconstruímos o sítio recentemente: uma ligação guardada nos favoritos, ou publicada noutro sítio, pode apontar para uma página que mudou de endereço."),
    ("Buscar un producto", "Pesquisar um produto"),
    ("Volver a la página de inicio", "Voltar à página inicial"),
    ("Explora las categorías", "Explore as categorias"),
    ("Sistemas operativos", "Sistemas operativos"),
    ("Suite Office", "Suite Office"),
    ("Soluciones Microsoft 365", "Soluções Microsoft 365"),
    ("Windows Server y SQL", "Windows Server e SQL"),
    ("Herramientas y más", "Ferramentas e mais"),
    ("Entre los más pedidos", "Entre os mais pedidos"),
    ("¿No encuentras lo que buscas? Escribe a", "Não encontra o que procura? Escreva para"),
    ("y te indicaremos la página correcta.", "e indicamos-lhe a página correta."),
    ("Soluciones Microsoft 365 | Eurolicenze", "Soluções Microsoft 365 | Eurolicenze"),
    ("Tu trabajo,<br>", "O seu trabalho,<br>"),
    ("más rápido con IA.", "mais rápido com IA."),
    ("Una suscripción para crear, compartir y proteger: las apps Office que ya conoces, OneDrive en la nube y Copilot donde tu plan Microsoft lo incluye — menos herramientas que gestionar, más resultados.", "Uma subscrição para criar, partilhar e proteger: as apps Office que já conhece, OneDrive na nuvem e Copilot onde o seu plano Microsoft o inclui — menos ferramentas para gerir, mais resultados."),
    ("Hogar y familia", "Casa e família"),
    ("Office para varias personas, cuentas familiares y almacenamiento OneDrive — la suite que mantiene deberes, trabajo y recuerdos sincronizados. Detalles y límites siguen el producto Microsoft que compras.", "Office para várias pessoas, contas familiares e armazenamento OneDrive — a suite que mantém trabalhos, deveres e memórias sincronizados. Detalhes e limites seguem o produto Microsoft que compra."),
    ("Ver producto", "Ver produto"),
    ("Equipos y empresas", "Equipas e empresas"),
    ("Colaboración profesional para equipos en crecimiento — te ayudamos con puestos, facturación y opciones alineadas con el catálogo Microsoft.", "Colaboração profissional para equipas em crescimento — ajudamos com postos, faturação e opções alinhadas com o catálogo Microsoft."),
    ("Hablar con ventas", "Falar com vendas"),
    ("Volumen y enterprise", "Volume e enterprise"),
    ("Compras centralizadas sencillas: comparte el número de puestos y tipos de licencia para un presupuesto a medida alineado con las ofertas Microsoft.", "Compras centralizadas simples: partilhe o número de postos e tipos de licença para um orçamento à medida alinhado com as ofertas Microsoft."),
    ("Pedir presupuesto", "Pedir orçamento"),
    ("Las apps Office que ya te gustan,<br>siempre actualizadas y conectadas a la nube.", "As apps Office de que já gosta,<br>sempre atualizadas e ligadas à nuvem."),
    ("Crea, presenta y colabora con Word, Excel, PowerPoint y Teams — herramientas premium incluidas en tu plan Microsoft 365, con funciones y actualizaciones definidas por Microsoft.", "Crie, apresente e colabore com Word, Excel, PowerPoint e Teams — ferramentas premium incluídas no seu plano Microsoft 365, com funções e atualizações definidas pela Microsoft."),
    ("Documentos pulidos, creados juntos.", "Documentos cuidados, criados em conjunto."),
    ("Datos claros, decisiones seguras.", "Dados claros, decisões seguras."),
    ("Presentaciones que convencen.", "Apresentações que convencem."),
    ("Reuniones y chat, un solo hub.", "Reuniões e chat, um só centro."),
    ("Copilot: menos trabajo rutinario, más resultados", "Copilot: menos trabalho rotineiro, mais resultados"),
    ("Lleva la IA a Word, Excel y más — borradores, resúmenes y sugerencias cuando tu plan y región lo permiten. Las capacidades siguen el producto Microsoft que compras.", "Leve a IA ao Word, Excel e mais — rascunhos, resumos e sugestões quando o seu plano e região o permitirem. As capacidades seguem o produto Microsoft que compra."),
    ("OneDrive: tus archivos, donde trabajes", "OneDrive: os seus ficheiros, onde trabalhar"),
    ("Copia de seguridad y sincronización en PC, móvil y web — abre documentos y fotos en segundos, dentro del almacenamiento incluido en tu plan Microsoft 365. Consulta capacidad y condiciones en el producto que elijas.", "Cópia de segurança e sincronização em PC, telemóvel e web — abra documentos e fotos em segundos, dentro do armazenamento incluído no seu plano Microsoft 365. Consulte capacidade e condições no produto que escolher."),
    ("Defender: seguridad que sigue el ritmo", "Defender: segurança que acompanha o ritmo"),
    ("Protección de Windows y actualizaciones cuando están incluidas en tu suscripción — de planes personales a ofertas multi-puesto de nuestro catálogo. Cobertura y requisitos dependen del producto Microsoft.", "Proteção do Windows e atualizações quando estão incluídas na sua subscrição — de planos pessoais a ofertas multi-posto do nosso catálogo. Cobertura e requisitos dependem do produto Microsoft."),
    ("Quienes somos", "Sobre nós"),
    ("quienes-somos", "sobre-nos"),
    ("Consultoría", "Consultoria"),
    ("Distribuidor de software europeo", "Distribuidor de software europeu"),
    ("Factura con IVA disponible", "Fatura com IVA disponível"),
    ("Soporte por email y WhatsApp", "Suporte por email e WhatsApp"),
    ("Microsoft 365 Familia", "Microsoft 365 Family"),
    ("Hasta 6 personas", "Até 6 pessoas"),
    ("Soluciones Microsoft 365 para empresas", "Soluções Microsoft 365 para empresas"),
    ("Guía de compra", "Guia de compra"),
    ("¿No sabes qué licencia elegir?", "Não sabe que licença escolher?"),
    ("Responde a dos preguntas y te decimos qué software es adecuado para ti.", "Responda a duas perguntas e indicamos o software adequado para si."),
    ("1. ¿Qué necesitas?", "1. Do que precisa?"),
    ("Office y productividad", "Office e produtividade"),
    ("Servidores y empresas", "Servidores e empresas"),
    ("2. ¿Para quién es?", "2. Para quem é?"),
    ("Solo para mí (1 usuario)", "Só para mim (1 utilizador)"),
    ("Toda la familia (hasta 6)", "Toda a família (até 6)"),
    ("Prefiero pagar una sola vez", "Prefiro pagar uma só vez"),
    ("Mi empresa", "A minha empresa"),
    ("2. ¿En qué PC?", "2. Em que PC?"),
    ("Uso personal, en casa", "Uso pessoal, em casa"),
    ("Trabajo o estudio profesional", "Trabalho ou estudo profissional"),
    ("Un PC más antiguo", "Um PC mais antigo"),
    ("2. ¿Cuántos dispositivos proteges?", "2. Quantos dispositivos protege?"),
    ("Solo uno", "Só um"),
    ("Hasta 5 (familia)", "Até 5 (família)"),
    ("10 o más", "10 ou mais"),
    ("2. ¿Qué necesitas gestionar?", "2. O que precisa de gerir?"),
    ("Los puestos de mis colaboradores", "Os postos dos meus colaboradores"),
    ("Word, Excel, PowerPoint y Outlook, 1 TB de OneDrive y Copilot, en 5 dispositivos a la vez.", "Word, Excel, PowerPoint e Outlook, 1 TB de OneDrive e Copilot, em 5 dispositivos ao mesmo tempo."),
    ("Hasta 6 personas, cada una con su cuenta y 1 TB de OneDrive. Copilot se queda con el titular.", "Até 6 pessoas, cada uma com a sua conta e 1 TB de OneDrive. O Copilot fica com o titular."),
    ("Word, Excel, PowerPoint, Outlook y OneNote en 1 PC o Mac. Licencia perpetua: se paga una vez, sin renovación anual.", "Word, Excel, PowerPoint, Outlook e OneNote em 1 PC ou Mac. Licença perpétua: paga-se uma vez, sem renovação anual."),
    ("Aplicaciones Office premium para empresas, con los servicios en la nube previstos por el plan de Microsoft.", "Aplicações Office premium para empresas, com os serviços na nuvem previstos pelo plano da Microsoft."),
    ("Licencia digital original para un PC de casa. Código e instrucciones por email tras el pago.", "Licença digital original para um PC de casa. Código e instruções por email após o pagamento."),
    ("Funciones profesionales como BitLocker y Escritorio remoto, según Microsoft. Licencia perpetua.", "Funções profissionais como BitLocker e Ambiente de Trabalho Remoto, segundo a Microsoft. Licença perpétua."),
    ("Licencia digital original de 32/64 bits con funciones profesionales, para hardware no compatible con Windows 11.", "Licença digital original de 32/64 bits com funções profissionais, para hardware incompatível com o Windows 11."),
    ("Protección antivirus ligera para un solo dispositivo. Activación en el portal oficial de ESET.", "Proteção antivírus leve para um só dispositivo. Ativação no portal oficial da ESET."),
    ("Cubre hasta 5 dispositivos: la opción habitual para una familia. Activación en el portal oficial de Bitdefender.", "Cobre até 5 dispositivos: a opção habitual para uma família. Ativação no portal oficial da Bitdefender."),
    ("Licencia para 10 dispositivos, activación en el portal oficial de McAfee.", "Licença para 10 dispositivos, ativação no portal oficial da McAfee."),
    ("Plan Plus con las funciones extra del catálogo Kaspersky. Activación en el portal oficial.", "Plano Plus com as funções extra do catálogo Kaspersky. Ativação no portal oficial."),
    ("¿Qué recibo exactamente después de la compra?", "O que recebo exatamente após a compra?"),
    ("¿Cuánto tarda entre el pago y el correo con la licencia?", "Quanto tempo passa entre o pagamento e o email com a licença?"),
    ("Nunca he comprado una licencia digital: ¿cómo funciona de principio a fin?", "Nunca comprei uma licença digital: como funciona do início ao fim?"),
    ("El precio es más bajo que en otros sitios: ¿la licencia es correcta? ¿Por qué cuesta menos?", "O preço é mais baixo do que noutros sítios: a licença é regular? Porque custa menos?"),
    ("¿Dónde introduzco el código y cómo instalo el software?", "Onde introduzo o código e como instalo o software?"),
    ("¿Cómo os contacto por problemas con pedido, pago o activación?", "Como vos contacto por problemas com a encomenda, o pagamento ou a ativação?"),
    (
        "Recibes un correo electrónico de entrega digital con lo necesario para usar la licencia (normalmente un código y/o instrucciones prácticas, además de referencias útiles para acreditar la compra, según el contenido real del mensaje enviado). La entrega es solo digital: conserva el correo y revisa también spam/correo no deseado si no ves nada en la bandeja de entrada.",
        "Recebe um email de entrega digital com o necessário para usar a licença (normalmente um código e/ou instruções práticas, além de referências úteis para comprovar a compra, conforme o conteúdo real da mensagem enviada). A entrega é apenas digital: conserve o email e verifique também o spam/correio indesejado se não vir nada na caixa de entrada.",
    ),
    (
        "Por lo general, el correo llega justo después de confirmar el pago; en casos puntuales pueden necesitarse unos minutos más por verificaciones del pago. Si en 30 minutos aún no has recibido nada, revisa spam/correo no deseado y escribe a Desk@eurolicenze.com con el producto comprado y el correo usado en el pedido, para que podamos comprobar el envío.",
        "Em regra, o email chega logo após a confirmação do pagamento; em casos pontuais podem ser precisos alguns minutos extra para verificações. Se em 30 minutos ainda não tiver recebido nada, verifique o spam/correio indesejado e escreva para Desk@eurolicenze.com com o produto comprado e o email usado na encomenda, para verificarmos o envio.",
    ),
    (
        "Elige el producto, completa el pedido y el pago en el checkout con los métodos disponibles — tarjeta, PayPal y monederos digitales (Apple Pay, Google Pay, cuando estén activados). El procesamiento se realiza de forma segura con Stripe. Tras confirmar el pago recibes la entrega por correo; para usar la licencia sigue el correo y la ficha de producto en nuestro sitio, donde encontrarás referencias coherentes con ese título.",
        "Escolha o produto, conclua a encomenda e o pagamento no checkout com os métodos disponíveis — cartão, PayPal e carteiras digitais (Apple Pay, Google Pay, quando ativados). O processamento é feito de forma segura com o Stripe. Após confirmar o pagamento recebe a entrega por email; para usar a licença siga o email e a ficha de produto no nosso sítio, onde encontrará referências coerentes com esse título.",
    ),
    (
        "Vendemos licencias digitales descritas en las fichas de producto, con precios claros y condiciones consultables en los Términos y condiciones y la Política de privacidad antes de comprar. Si quieres una referencia externa, puedes leer reseñas públicas en Trustpilot (https://it.trustpilot.com/review/aml-store.com). Para dudas operativas, escribe a Desk@eurolicenze.com.",
        "Vendemos licenças digitais descritas nas fichas de produto, com preços claros e condições consultáveis nos Termos e condições e na Política de privacidade antes de comprar. Se quiser uma referência externa, pode ler avaliações públicas no Trustpilot (https://it.trustpilot.com/review/aml-store.com). Para dúvidas operacionais, escreva para Desk@eurolicenze.com.",
    ),
    (
        "La activación y la instalación se realizan en los sitios y portales oficiales del fabricante, según las reglas de ese producto. Después de la compra usa las instrucciones del correo y, para el detalle paso a paso, la ficha de producto en nuestro sitio. Si algo no funciona, escribe a Desk@eurolicenze.com con el producto y el correo del pedido.",
        "A ativação e a instalação realizam-se nos sítios e portais oficiais do fabricante, segundo as regras desse produto. Após a compra use as instruções do email e, para o detalhe passo a passo, a ficha de produto no nosso sítio. Se algo não funcionar, escreva para Desk@eurolicenze.com com o produto e o email da encomenda.",
    ),
    (
        "Escribe a Desk@eurolicenze.com: es el canal principal indicado también en el pie de página del sitio. Incluye producto, correo usado en el pedido y una breve descripción del problema; para privacidad, condiciones y devoluciones usa los enlaces del pie (Política de privacidad, Términos y condiciones, Devoluciones y reembolsos).",
        "Escreva para Desk@eurolicenze.com: é o canal principal indicado também no rodapé do sítio. Inclua produto, email usado na encomenda e uma breve descrição do problema; para privacidade, condições e devoluções use as ligações do rodapé (Política de privacidade, Termos e condições, Devoluções e reembolsos).",
    ),
]


HEADER_RE = re.compile(
    r"(<ecommerce-header\b[^>]*>)[\s\S]*?(</ecommerce-header>)",
    re.IGNORECASE,
)
FOOTER_RE = re.compile(
    r"(<ecommerce-footer\b[^>]*>)[\s\S]*?(</ecommerce-footer>)",
    re.IGNORECASE,
)


def strip_chrome(html: str) -> str:
    html = HEADER_RE.sub(r"\1</ecommerce-header>", html)
    html = FOOTER_RE.sub(r"\1</ecommerce-footer>", html)
    return html


def apply_translations(html: str) -> str:
    pairs = sorted(ES_PT, key=lambda p: len(p[0]), reverse=True)
    for src, dst in pairs:
        html = html.replace(src, dst)
    return html


def remap_locale(html: str, *, home: bool = False) -> str:
    html = html.replace('lang="es"', 'lang="pt"', 1)
    html = html.replace('content="es_ES"', 'content="pt_PT"', 1)
    html = html.replace('content="es_GB"', 'content="pt_PT"', 1)
    if 'hreflang="pt"' not in html:
        html = html.replace(
            '<link rel="alternate" hreflang="x-default"',
            '<link rel="alternate" hreflang="pt" href="https://eurolicenze.com/pt/PLACEHOLDER">\n    <link rel="alternate" hreflang="x-default"',
        )
    html = html.replace("/es/", "/pt/")
    html = html.replace('"inLanguage":"es"', '"inLanguage":"pt"')
    html = html.replace('"inLanguage": "es"', '"inLanguage": "pt"')
    html = html.replace('["it","en","fr","de","es"]', '["it","en","fr","de","es","pt"]')
    html = html.replace('["it", "en", "fr", "de", "es"]', '["it", "en", "fr", "de", "es", "pt"]')
    return html


def fix_pt_hreflang(html: str, slug: str) -> str:
    href = f"https://eurolicenze.com/pt/{slug}" if slug else "https://eurolicenze.com/pt/"
    return html.replace(
        'hreflang="pt" href="https://eurolicenze.com/pt/PLACEHOLDER"',
        f'hreflang="pt" href="{href}"',
    )


def add_og_locale_alternate(html: str) -> str:
    if 'og:locale:alternate" content="pt_PT"' in html:
        return html
    needle = '<meta property="og:locale:alternate" content="es_ES">'
    # already remapped es_ES→pt_PT on the primary locale; insert after last alternate
    if '<meta property="og:locale:alternate" content="de_DE">' in html:
        html = html.replace(
            '<meta property="og:locale:alternate" content="de_DE">',
            '<meta property="og:locale:alternate" content="de_DE">\n    <meta property="og:locale:alternate" content="es_ES">\n    <meta property="og:locale:alternate" content="pt_PT">',
            1,
        )
    return html


def port(src_rel: str, dest_rel: str, slug: str, home: bool = False) -> None:
    src = ROOT / src_rel
    dest = ROOT / dest_rel
    html = src.read_text(encoding="utf-8")
    html = strip_chrome(html)
    html = remap_locale(html, home=home)
    html = apply_translations(html)
    html = fix_pt_hreflang(html, slug)
    if home:
        html = add_og_locale_alternate(html)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8", newline="\n")
    print("wrote", dest_rel, "bytes", dest.stat().st_size)


def main() -> None:
    port("es/index.html", "pt/index.html", "", home=True)
    port("es/404.html", "pt/404.html", "404")
    port("es/microsoft-365-solutions.html", "pt/microsoft-365-solutions.html", "microsoft-365-solutions")


if __name__ == "__main__":
    main()
