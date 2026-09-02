#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buy card v4: applica il redesign UX/CRO della scheda d'acquisto alle PDP.

Patch mirata sull'HTML esistente, non una rigenerazione — stessa scelta di
`apply-payment-logos.py` e per lo stesso motivo: i `regen-*.py` sono
disallineati dal pre-render di header/footer e riscriverebbero le pagine a una
versione priva di chrome inline e di hash `?v=`.

Cosa fa, in ordine di comparsa nella card:

1. pill disponibilita' troncato al "·"  ("Disponibile · consegna immediata" e
   la riga "Email in 2-15 min" accanto erano due promesse che si smentivano);
2. chip riquadrati -> `.pdp-trust-checks`, lista con spunte e senza cornici,
   piu' una terza voce di garanzia (framing positivo, al posto del vecchio
   "Se il codice non si attiva..." che stava in fondo alla card);
3. blocco prezzo unificato: sparisce l'etichetta "Prezzo Riservato", il badge
   sconto entra nella riga prezzo ridotto alla sola percentuale, sparisce la
   riga "Risparmi €X..." ma NON la qualifica del barrato come listino;
4. chip regione -> `.pdp-region`, riga con icona;
5. gerarchia CTA 1+1: via "Acquista ora" (buy card e sticky bar), la CTA
   primaria e' "Aggiungi al carrello", PayPal Express resta come percorso
   express dopo un separatore etichettato;
6. ponte `.pdp-added` verso il carrello, scoperto da `product-v3.js`;
7. link di confronto spostato sotto i percorsi d'acquisto;
8. Trustpilot in card: punteggio con etichetta, non conteggio;
9. promessa di consegna allineata (sticky bar e prosa) all'intervallo reale
   dichiarato nella card.

Idempotente: una pagina gia' convertita viene saltata. Da eseguire una
tantum, poi `scripts/bump-asset-version.py`.

Uso:
    python scripts/apply-buycard-v4.py            # tutte le PDP con buy card
    python scripts/apply-buycard-v4.py it/x.html  # solo i file indicati
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "fr", "de", "es", "pt", "nl")

GLOBE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
         'aria-hidden="true"><circle cx="12" cy="12" r="9"/>'
         '<path stroke-linecap="round" d="M3.2 9h17.6M3.2 15h17.6"/>'
         '<path stroke-linecap="round" d="M12 3c2.3 2.6 3.5 5.6 3.5 9s-1.2 6.4-3.5 9'
         'c-2.3-2.6-3.5-5.6-3.5-9S9.7 5.6 12 3z"/></svg>')

# Le uniche stringhe nuove del redesign. Tutto il resto viene ripreso dalla
# pagina stessa (etichette gia' tradotte) e quindi non compare qui.
#
#  sconto      connettore della nota prezzo, minuscolo (maiuscolo in tedesco,
#              e' un sostantivo)
#  listino     accorciamento del frammento gia' tradotto `ui["save_vs"]`, solo
#              dove serve a far stare la nota su una riga; None = lascia intero
#  garanzia    etichetta della spunta di garanzia
#  rimedio     testo del link: NON inventato, e' la formula della policy in
#              /{lang}/returns-and-refunds ("proporremo sostituzione o
#              rimborso" e i suoi equivalenti). Niente "100%" ne' "immediato":
#              la policy condiziona il rimedio alla verifica del difetto
#  eccellente  etichetta con cui Trustpilot stesso qualifica un punteggio in
#              fascia alta; legata alla soglia, se il voto scende va rivista
#  ponte       invito persistente al carrello dopo l'aggiunta
#  spedizione  frase da togliere dalla nota prezzo: per un bene digitale
#              consegnato via email e' un residuo dell'e-commerce fisico.
#              Match esatto di proposito — sulle pagine di prodotti FISICI la
#              nota parla davvero di spedizione e non deve essere toccata
#  vago        quarta formulazione della consegna, in prosa: "in pochi minuti"
#              e simili diventano l'intervallo reale
I18N = {
    "it": {"sconto": "sconto", "listino": ("prezzo di listino", "listino"),
           "garanzia": "Garanzia:", "rimedio": "sostituzione o rimborso",
           "eccellente": "Eccellente",
           "ponte": "Vai al carrello e completa l'ordine",
           "spedizione": " Nessun costo di spedizione.",
           "vago": ("pochi minuti", "%s minuti")},
    "en": {"sconto": "discount", "listino": None,
           "garanzia": "Guarantee:", "rimedio": "replacement or refund",
           "eccellente": "Excellent",
           "ponte": "Go to cart and complete your order",
           "spedizione": " No shipping fees.",
           "vago": ("within minutes", "within %s minutes")},
    "fr": {"sconto": "remise", "listino": None,
           #   = insecable: in francese i due punti lo vogliono prima,
           # non e' uno spazio normale da "correggere".
           "garanzia": "Garantie :", "rimedio": "remplacement ou remboursement",
           "eccellente": "Excellent",
           "ponte": "Voir le panier et finaliser la commande",
           "spedizione": " Pas de frais de port.",
           "vago": ("en quelques minutes", "en %s minutes")},
    "de": {"sconto": "Rabatt", "listino": None,
           "garanzia": "Garantie:", "rimedio": "Ersatz oder Erstattung",
           "eccellente": "Hervorragend",
           "ponte": "Zum Warenkorb und Bestellung abschließen",
           "spedizione": " Keine Versandkosten.",
           "vago": ("innerhalb weniger Minuten", "innerhalb von %s Minuten")},
    "es": {"sconto": "descuento", "listino": None,
           "garanzia": "Garantía:", "rimedio": "sustitución o reembolso",
           "eccellente": "Excelente",
           "ponte": "Ir al carrito y completar el pedido",
           "spedizione": " Sin gastos de envío.",
           "vago": ("en pocos minutos", "en %s minutos")},
    "pt": {"sconto": "desconto", "listino": None,
           "garanzia": "Garantia:", "rimedio": "substituição ou reembolso",
           "eccellente": "Excelente",
           "ponte": "Ir para o carrinho e concluir o pedido",
           "spedizione": " Sem custos de envio.",
           "vago": ("em poucos minutos", "em %s minutos")},
    "nl": {"sconto": "korting", "listino": None,
           "garanzia": "Garantie:", "rimedio": "vervanging of terugbetaling",
           "eccellente": "Uitstekend",
           "ponte": "Naar winkelwagen en bestelling afronden",
           "spedizione": " Geen verzendkosten.",
           "vago": ("binnen enkele minuten", "binnen %s minuten")},
}

# NON-SOSTITUIRE: le stringhe "vago" qui sopra sono i termini da CERCARE,
# non da correggere. Una sweep testuale sul repo le riscriverebbe e la
# mappa diventerebbe una sostituzione a vuoto.

errori = []


def salta(path, msg):
    """Registra il problema e lascia la pagina intatta.

    Su 434 file un fail-fast lascerebbe il catalogo mezzo convertito: meglio
    saltare la pagina anomala e stampare il riepilogo alla fine.
    """
    errori.append((path, msg))
    return None


def testo_bottone(html):
    """Etichetta di un bottone, senza l'icona SVG."""
    senza_svg = re.sub(r"<svg.*?</svg>", "", html, flags=re.S)
    testo = re.sub(r"<[^>]+>", "", senza_svg)
    return testo.strip()


def patch(path):
    lang = path.parent.name
    if lang not in I18N:
        return salta(path, "lingua non riconosciuta")
    t = I18N[lang]

    src = path.read_text(encoding="utf-8")
    orig = src
    if 'class="pdp-trust-checks"' in src:
        return False
    if 'class="pdp-buy"' not in src:
        return salta(path, "nessuna buy card")

    # Le due etichette CTA si leggono dalla pagina: sono gia' tradotte, non
    # serve una tabella. `add` diventa anche il testo della sticky bar.
    ghost_m = re.search(r'<button type="button" class="pdp-btn-ghost" data-cart-add '
                        r'data-cart-source="product-pricing">.*?</button>', src, re.S)
    sticky_m = re.search(r'<button type="button" class="btn-primary" data-cart-add '
                         r'data-cart-source="product-pricing" data-pdp-buy-now>.*?</button>',
                         src, re.S)
    if not ghost_m or not sticky_m:
        return salta(path, "coppia di CTA attesa non trovata")
    lbl_add = testo_bottone(ghost_m.group(0))
    lbl_buy = testo_bottone(sticky_m.group(0))
    if not lbl_add or not lbl_buy:
        return salta(path, "etichette CTA vuote")

    # -- 1. chip riquadrati -> spunte inline -------------------------------
    partner = re.search(r'[ \t]*<p class="pdp-meta-row pdp-meta-row--partner".*?</p>\n',
                        src, re.S)
    checks = []
    if partner:
        inner = re.search(r'<strong>(.*?)</strong>\s*(.*?)\s*</span>', partner.group(0), re.S)
        if not inner:
            return salta(path, "chip partner con struttura inattesa")
        checks = ["<strong>%s</strong>" % inner.group(1), inner.group(2).rstrip('.')]
        src = src.replace(partner.group(0), "")

    assur = re.search(r'[ \t]*<ul class="pdp-assur">.*?</ul>\n', src, re.S)
    if not assur:
        return salta(path, "blocco .pdp-assur non trovato")
    if not checks:
        # Sulle pagine senza chip partner le rassicurazioni si prendono dalla
        # lista di chiusura, meno quelle sulla consegna: quella la dice gia'
        # il pill di disponibilita'.
        voci = re.findall(r'<li>(.*?)</li>', assur.group(0), re.S)
        parole_consegna = ('spedizion', 'consegna', 'shipping', 'delivery', 'livraison',
                           'versand', 'lieferung', 'envío', 'entrega', 'verzend', 'levering')
        checks = [v.strip() for v in voci
                  if not any(p in v.lower() for p in parole_consegna)]
    if not checks:
        return salta(path, "nessuna rassicurazione da promuovere in testa")

    checks.append('<strong>%s</strong> <a href="/%s/returns-and-refunds">%s</a>'
                  % (t["garanzia"], lang, t["rimedio"]))

    cross = re.search(r'[ \t]*<p class="pdp-cross">.*?</p>\n', src, re.S)
    cross_html = cross.group(0) if cross else ""
    if cross:
        src = src.replace(cross_html, "")
    # La lista di chiusura lascia il posto al link di confronto: la card ora
    # finisce con confronto + Trustpilot.
    src = src.replace(assur.group(0), cross_html)

    checks_html = ('                <ul class="pdp-trust-checks">\n'
                   + "".join("                    <li>%s</li>\n" % c for c in checks)
                   + '                </ul>\n')

    # Le spunte si agganciano sotto il blocco di disponibilita'. Sulle PDP
    # digitali e' il pill `.pdp-avail`; sui 7 SKU fisici e' `.v2-stock`, la
    # riga di giacenza che product-stock.js riempie a runtime.
    avail = re.search(r'[ \t]*<p class="pdp-avail">.*?</p>\n', src, re.S)
    if avail:
        # Il pill diceva "Disponibile · consegna immediata" e la riga accanto
        # "Email in 2-15 min": due promesse che si smentivano a 30px di
        # distanza. Il pill torna a fare solo il suo mestiere (c'e'/non c'e'),
        # la promessa la fa il numero. Il taglio al "·" separa le due meta' in
        # tutte e 7 le lingue, quindi non serve nessuna stringa nuova.
        pill = re.search(r'(<span class="pdp-avail__pill">.*?</span>)([^<]+)</span>',
                         avail.group(0), re.S)
        if not pill:
            return salta(path, "pill di disponibilita' con struttura inattesa")
        stato = re.split(r'\s*·\s*', pill.group(2).strip())[0]
        blocco_avail = avail.group(0).replace(pill.group(0), pill.group(1) + stato + '</span>')
    else:
        avail = re.search(r'[ \t]*<p class="v2-stock".*?</p>\n', src, re.S)
        if not avail:
            return salta(path, "nessun blocco di disponibilita' (.pdp-avail / .v2-stock)")
        blocco_avail = avail.group(0)
    src = src.replace(avail.group(0), blocco_avail + checks_html, 1)

    # -- 2. blocco prezzo: un solo gruppo ottico ---------------------------
    label = re.search(r'[ \t]*<p class="pdp-buy__label">.*?</p>\n', src, re.S)
    if not label:
        return salta(path, "etichetta .pdp-buy__label non trovata")
    badge = re.search(r'<span class="pdp-price-badge" aria-label="(.*?)">.*?</span>',
                      label.group(0), re.S)
    src = src.replace(label.group(0), "")
    if badge:
        # Si matcha l'intero blocco e si ricuce per posizione: "</div>" da solo
        # e' troppo comune perche' una replace lo colpisca nel punto giusto.
        row = re.search(r'<div class="pdp-price-row".*?\n([ \t]*)</div>\n', src, re.S)
        if not row:
            return salta(path, "blocco .pdp-price-row non trovato")
        # Solo la percentuale: col suffisso ("SCONTO", "OFF", "RABATT"...) la
        # riga sfora i 375px e il badge va a capo, rompendo il gruppo ottico.
        compatto = '<span class="pdp-price-badge">%s</span>' % badge.group(1)
        chiusura = '\n' + row.group(1) + '</div>\n'
        blocco = row.group(0).replace(
            chiusura, '\n' + row.group(1) + '    ' + compatto + chiusura)
        src = src[:row.start()] + blocco + src[row.end():]

    # "Risparmi €X rispetto al prezzo di listino (€Y)": la cifra del risparmio
    # e' la terza ripetizione dello stesso dato e sparisce. NON sparisce la
    # qualifica: senza, il barrato si legge come prezzo praticato prima da noi
    # invece che come listino del produttore, cioe' un annuncio di riduzione
    # di prezzo non qualificato. Il frammento (`ui["save_vs"]`) si riprende
    # dalla riga che stiamo togliendo: e' gia' tradotto.
    save = re.search(r'[ \t]*<p class="pdp-price-save">.*?</strong>\s*(.*?)</p>\n', src, re.S)
    qualifica = save.group(1).strip() if save else ""
    src = re.sub(r'[ \t]*<p class="pdp-price-save">.*?</p>\n', "", src, flags=re.S)
    src = src.replace(t["spedizione"], "")

    if qualifica and badge:
        qualifica = re.sub(r'\s*\([^)]*\)\s*\.?$', '', qualifica).strip().rstrip('.')
        if t["listino"]:
            qualifica = qualifica.replace(*t["listino"])
        note = re.search(r'(<p class="pdp-price-note">)(.*?)(</p>)', src, re.S)
        if not note:
            return salta(path, "riga .pdp-price-note non trovata")
        # La qualifica va dopo la PRIMA frase, non in coda: sulle PDP digitali
        # la nota e' solo "Tasse incluse" e le due cose coincidono, ma sugli
        # SKU fisici seguono altre due frasi su corriere e supporto fisico e
        # in coda la qualifica del barrato finirebbe sepolta.
        testo = note.group(2).strip()
        prima, punto, resto = testo.partition('. ')
        coda = ' ' + resto if resto else ''
        if not resto:
            prima = prima.rstrip('.')
        src = src.replace(
            note.group(0),
            note.group(1) + prima + ' · ' + t["sconto"] + ' ' + qualifica
            + ('.' if resto else '') + coda + note.group(3), 1)

    # -- 3. regione di attivazione: riga con icona -------------------------
    # Opzionale: su pt e nl il badge regione esiste solo su 7 pagine su 62
    # (add-activation-region-badge.py non e' mai stato completato la'). Dove
    # manca non c'e' niente da convertire — e' un buco di contenuto
    # preesistente, non un errore di questa patch.
    region = re.search(
        r'[ \t]*<p class="pdp-meta-row" role="group" aria-label="[^"]*">\s*'
        r'<span class="pdp-meta-chip"><strong>(.*?)</strong>\s*(.*?)</span>\s*</p>\n',
        src, re.S)
    if region:
        src = src.replace(
            region.group(0),
            '                <p class="pdp-region">\n'
            '                    ' + GLOBE + '\n'
            '                    <span><strong>' + region.group(1) + ':</strong> '
            + region.group(2).strip() + '</span>\n'
            '                </p>\n')

    # -- 4. gerarchia CTA 1+1 ---------------------------------------------
    # "Acquista ora" e PayPal Express saltavano entrambi il carrello: due
    # scorciatoie per lo stesso percorso, con in mezzo la CTA standard.
    buy_now = re.search(
        r'[ \t]*<button type="button" id="product-primary-cta" class="pdp-btn-primary"'
        r'[^>]*data-cart-checkout-redirect="[^"]*">.*?</button>\n', src, re.S)
    if not buy_now:
        return salta(path, "CTA di acquisto diretto non trovata nella buy card")
    src = src.replace(buy_now.group(0), "")
    src = src.replace(
        '<button type="button" class="pdp-btn-ghost" data-cart-add '
        'data-cart-source="product-pricing">',
        '<button type="button" id="product-primary-cta" class="pdp-btn-primary" '
        'data-cart-add data-cart-source="product-pricing">', 1)

    cta = re.search(r'<button type="button" id="product-primary-cta".*?</button>\n', src, re.S)
    if not cta:
        return salta(path, "CTA primaria non trovata per il ponte al carrello")
    ponte = ('                <p class="pdp-added" hidden>\n'
             '                    <a href="/%s/cart">%s →</a>\n'
             '                </p>\n' % (lang, t["ponte"]))
    src = src[:cta.end()] + ponte + src[cta.end():]

    # Il filetto nudo diventa separatore etichettato, e l'etichetta e' la
    # microcopy che stava SOTTO i bottoni PayPal: stessa parola, detta una
    # volta sola e prima del percorso che introduce. Gli SKU fisici il blocco
    # PayPal non ce l'hanno: qui non c'e' niente da fare.
    micro = re.search(r'[ \t]*<p class="pdp-paypal-express__microcopy">(.*?)</p>\n', src, re.S)
    if micro:
        src = src.replace(micro.group(0), "")
        src = src.replace('<hr class="pdp-paypal-sep" aria-hidden="true">',
                          '<p class="pdp-cta-sep">%s</p>' % micro.group(1).strip())
    # Il messaggio d'errore PayPal rimandava alla CTA che non esiste piu'.
    src = src.replace("Riprova o usa %s." % lbl_buy, "Riprova o usa %s." % lbl_add)
    src = src.replace(lbl_buy + ".\"\n", lbl_add + ".\"\n")

    # -- 5. sticky bar: stessa azione della CTA primaria -------------------
    sticky = re.search(
        r'(<button type="button" class="btn-primary" data-cart-add '
        r'data-cart-source="product-pricing") data-pdp-buy-now(>.*?)'
        + re.escape(lbl_buy) + r'(\s*</button>)', src, re.S)
    if not sticky:
        return salta(path, "bottone della sticky bar non trovato")
    src = src.replace(sticky.group(0),
                      sticky.group(1) + sticky.group(2) + lbl_add + sticky.group(3))

    # -- 6. una sola promessa di consegna ---------------------------------
    # La sticky prometteva "2 minuti" mentre la card dice "2-15 min": si
    # allinea alla card prendendo l'intervallo da li' e sostituendo solo la
    # cifra dentro la frase gia' tradotta.
    # Solo per i beni digitali: gli SKU fisici viaggiano col corriere, la loro
    # nota parla di 24 ore lavorative e non va toccata con l'intervallo email.
    eta = re.search(r'<span class="pdp-avail__eta">([^<]+)</span>', src)
    if eta:
        intervallo = re.search(r'\d+\s*[–-]\s*\d+\s*\S+', eta.group(1))
        if not intervallo:
            return salta(path, "intervallo di consegna non riconosciuto: %r" % eta.group(1))
        seta = re.search(r'(<span class="product-sticky-cta__eta">)([^<]+)(</span>)', src)
        if seta:
            allineata = re.sub(r'\d+\s+\S+', intervallo.group(0), seta.group(2), count=1)
            src = src.replace(seta.group(0), seta.group(1) + allineata + seta.group(3), 1)

        # Quarta formulazione, in prosa: piu' vaga, non in contraddizione. Con
        # l'intervallo dice la stessa cosa in modo verificabile. In prosa
        # l'unita' e' per esteso, non l'abbreviazione del pill.
        cifre = re.search(r'\d+\s*[–-]\s*\d+', intervallo.group(0))
        vago_da, vago_a = t["vago"]
        if cifre and vago_da in src:
            src = src.replace(vago_da, vago_a % cifre.group(0))

    # -- 7. Trustpilot in card: il punteggio, non il conteggio -------------
    # La top bar col voto e' display:none sotto il breakpoint mobile, quindi
    # la card e' l'unico posto in cui il punteggio puo' comparire. Il
    # conteggio non sparisce dalla pagina: resta in .pdp-reviews__count.
    tp = re.search(r'(<div class="product-trustpilot pdp-buy-trustpilot">.*?)'
                   r'<span class="tp-score__value">([^<]*)</span>\s*'
                   r'<span class="tp-score__count">([^<]*)</span>', src, re.S)
    if tp:
        voto = re.match(r'\s*([\d.,]+\s*/\s*\d+)\s*(.*)$', tp.group(2))
        if not voto:
            return salta(path, "voto Trustpilot con formato inatteso: %r" % tp.group(2))
        src = src.replace(
            tp.group(0),
            tp.group(1)
            + '<span class="tp-score__value">%s %s</span>\n' % (t["eccellente"],
                                                                voto.group(1).strip())
            + '                        '
            + '<span class="tp-score__count">%s</span>' % voto.group(2).strip(), 1)

    if src == orig:
        return salta(path, "nessuna modifica applicata")
    # Guardia strutturale, non testuale: cercare l'etichetta ("Acquista ora",
    # "Acheter"...) darebbe falsi positivi ogni volta che la stessa parola
    # compare nella prosa della pagina — in francese succede tre volte.
    if "data-pdp-buy-now" in src or "data-cart-checkout-redirect" in src:
        return salta(path, "resta un percorso di acquisto diretto non convertito")
    # newline="" preserva i fine riga del file: il repo ha HTML in LF e
    # asset in CRLF, e gli hash ?v= sono calcolati sui byte del working tree.
    path.write_text(src, encoding="utf-8", newline="")
    return True


def pagine():
    trovate = []
    for lang in LANGS:
        for f in sorted((ROOT / lang).glob("*.html")):
            if 'class="pdp-buy"' in f.read_text(encoding="utf-8"):
                trovate.append(f)
    return trovate


def main(argv):
    target = [Path(a).resolve() for a in argv] if argv else pagine()
    fatte = saltate = 0
    for p in target:
        esito = patch(p)
        if esito is True:
            fatte += 1
        elif esito is False:
            saltate += 1
    print("convertite: %d" % fatte)
    print("gia' a posto: %d" % saltate)
    if errori:
        print("NON toccate: %d" % len(errori))
        for p, msg in errori:
            print("  %s/%s: %s" % (p.parent.name, p.name, msg))
    return 1 if errori else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
