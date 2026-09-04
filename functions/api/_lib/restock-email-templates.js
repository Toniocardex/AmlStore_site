/**
 * Template dell'email "e' tornato disponibile".
 *
 * Separati dai template ordine, come per le consulenze: qui non c'e' nessuna
 * dipendenza da checkout o D1, quindi il modulo resta testabile in Node puro.
 *
 * La copia e' volutamente asciutta: e' una notifica di servizio richiesta dal
 * destinatario, non un'email promozionale. Niente sconti, niente cross-sell,
 * e il link di annullamento sempre visibile in fondo.
 */

const COPY = {
    it: {
        subject: (name) => `Di nuovo disponibile: ${name}`,
        heading: 'È tornato disponibile',
        intro: 'Ci avevi chiesto di avvisarti quando questo articolo sarebbe rientrato in magazzino. Eccolo:',
        note: 'Le quantità sono limitate e non sono riservate: la disponibilità vale fino a esaurimento.',
        cta: 'Vai al prodotto',
        why: 'Ricevi questa email perché hai lasciato il tuo indirizzo sulla pagina di questo prodotto mentre era esaurito. È un avviso singolo: non ti abbiamo iscritto a nessuna newsletter e non riceverai altri messaggi.',
        cancelLead: 'Non ti serve più questo avviso?',
        cancel: 'Annulla la richiesta',
    },
    en: {
        subject: (name) => `Back in stock: ${name}`,
        heading: 'Back in stock',
        intro: 'You asked us to let you know when this item returned to our warehouse. Here it is:',
        note: 'Quantities are limited and not reserved: availability lasts while stocks do.',
        cta: 'Go to the product',
        why: 'You are receiving this email because you left your address on this product page while it was out of stock. This is a one-off alert: we did not subscribe you to any newsletter and you will not receive further messages.',
        cancelLead: 'No longer need this alert?',
        cancel: 'Cancel the request',
    },
    de: {
        subject: (name) => `Wieder verfügbar: ${name}`,
        heading: 'Wieder verfügbar',
        intro: 'Sie hatten uns gebeten, Sie zu benachrichtigen, sobald dieser Artikel wieder auf Lager ist. Hier ist er:',
        note: 'Die Stückzahl ist begrenzt und wird nicht reserviert: Verfügbarkeit nur solange der Vorrat reicht.',
        cta: 'Zum Produkt',
        why: 'Sie erhalten diese E-Mail, weil Sie Ihre Adresse auf dieser Produktseite hinterlassen haben, während der Artikel ausverkauft war. Es handelt sich um eine einmalige Benachrichtigung: Wir haben Sie zu keinem Newsletter angemeldet und Sie erhalten keine weiteren Nachrichten.',
        cancelLead: 'Sie brauchen diese Benachrichtigung nicht mehr?',
        cancel: 'Anfrage stornieren',
    },
    fr: {
        subject: (name) => `De nouveau disponible : ${name}`,
        heading: 'De nouveau disponible',
        intro: 'Vous nous aviez demandé de vous prévenir dès le retour de cet article en stock. Le voici :',
        note: 'Les quantités sont limitées et ne sont pas réservées : disponibilité dans la limite des stocks.',
        cta: 'Voir le produit',
        why: 'Vous recevez cet e-mail parce que vous avez laissé votre adresse sur cette page produit alors qu’il était épuisé. C’est une alerte unique : nous ne vous avons inscrit à aucune newsletter et vous ne recevrez pas d’autres messages.',
        cancelLead: 'Vous n’avez plus besoin de cette alerte ?',
        cancel: 'Annuler la demande',
    },
    es: {
        subject: (name) => `De nuevo disponible: ${name}`,
        heading: 'De nuevo disponible',
        intro: 'Nos pediste que te avisáramos cuando este artículo volviera a estar en stock. Aquí lo tienes:',
        note: 'Las unidades son limitadas y no quedan reservadas: la disponibilidad dura hasta fin de existencias.',
        cta: 'Ir al producto',
        why: 'Recibes este correo porque dejaste tu dirección en la página de este producto mientras estaba agotado. Es un aviso único: no te hemos suscrito a ninguna newsletter y no recibirás más mensajes.',
        cancelLead: '¿Ya no necesitas este aviso?',
        cancel: 'Cancelar la solicitud',
    },
    nl: {
        subject: (name) => `Weer op voorraad: ${name}`,
        heading: 'Weer op voorraad',
        intro: 'Je had ons gevraagd je te laten weten wanneer dit artikel weer op voorraad zou zijn. Hier is het:',
        note: 'De aantallen zijn beperkt en worden niet gereserveerd: beschikbaar zolang de voorraad strekt.',
        cta: 'Naar het product',
        why: 'Je ontvangt deze e-mail omdat je je adres hebt achtergelaten op deze productpagina toen het artikel uitverkocht was. Dit is een eenmalige melding: we hebben je niet ingeschreven voor een nieuwsbrief en je ontvangt geen verdere berichten.',
        cancelLead: 'Heb je deze melding niet meer nodig?',
        cancel: 'Verzoek annuleren',
    },
    pt: {
        subject: (name) => `Novamente disponível: ${name}`,
        heading: 'Novamente disponível',
        intro: 'Pediu-nos para o avisar quando este artigo voltasse a estar em stock. Aqui está:',
        note: 'As quantidades são limitadas e não ficam reservadas: disponibilidade até esgotar.',
        cta: 'Ver o produto',
        why: 'Recebe este e-mail porque deixou o seu endereço na página deste produto enquanto estava esgotado. É um aviso único: não o inscrevemos em nenhuma newsletter e não receberá mais mensagens.',
        cancelLead: 'Já não precisa deste aviso?',
        cancel: 'Cancelar o pedido',
    },
};

function esc(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

export function restockLocale(lang) {
    return COPY[lang] ? lang : 'en';
}

/**
 * @param {object} params
 * @param {string} params.lang        lingua della PDP di iscrizione
 * @param {string} params.productName nome commerciale da CATALOG
 * @param {string} params.productUrl  URL assoluto della PDP
 * @param {string} params.cancelUrl   URL assoluto di annullamento (token)
 */
export function restockBackInStockEmail({ lang, productName, productUrl, cancelUrl }) {
    const locale = restockLocale(lang);
    const copy = COPY[locale];
    const subject = copy.subject(productName);

    const html = `<!DOCTYPE html>
<html lang="${esc(locale)}"><head><meta charset="UTF-8"><title>${esc(subject)}</title></head>
<body style="margin:0;background:#f4f6f8;font-family:Arial,sans-serif;color:#152033">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:24px;background:#f4f6f8">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0" style="width:100%;max-width:620px;background:#fff;border:1px solid #dce3ea;border-radius:10px;overflow:hidden">
        <tr><td style="padding:22px 26px;background:#0F172A;color:#fff"><strong style="font-size:18px">Eurolicenze</strong></td></tr>
        <tr><td style="padding:28px 26px">
          <h1 style="margin:0 0 14px;font-size:24px">${esc(copy.heading)}</h1>
          <p style="margin:0 0 16px;line-height:1.65">${esc(copy.intro)}</p>
          <p style="margin:0 0 20px;padding:14px 16px;background:#f4f6f8;border:1px solid #dce3ea;border-radius:8px;font-weight:700;line-height:1.5">${esc(productName)}</p>
          <p style="margin:0 0 20px">
            <a href="${esc(productUrl)}" style="display:inline-block;padding:13px 26px;background:#E8590C;color:#fff;font-weight:700;text-decoration:none;border-radius:6px">${esc(copy.cta)}</a>
          </p>
          <p style="margin:0 0 22px;color:#5f6b7a;font-size:13px;line-height:1.55">${esc(copy.note)}</p>
          <hr style="border:none;border-top:1px solid #dce3ea;margin:0 0 18px">
          <p style="margin:0 0 10px;color:#5f6b7a;font-size:12px;line-height:1.55">${esc(copy.why)}</p>
          <p style="margin:0;color:#5f6b7a;font-size:12px;line-height:1.55">${esc(copy.cancelLead)} <a href="${esc(cancelUrl)}" style="color:#5f6b7a">${esc(copy.cancel)}</a></p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body></html>`;

    const text = [
        copy.heading,
        '',
        copy.intro,
        productName,
        productUrl,
        '',
        copy.note,
        '',
        copy.why,
        '',
        `${copy.cancelLead} ${cancelUrl}`,
    ].join('\n');

    return { subject, html, text };
}

/** Pagina di conferma/esito dell'annullamento, servita da /api/restock-cancel. */
const CANCEL_PAGE_COPY = {
    it: {
        title: 'Annulla l’avviso di disponibilità',
        confirmHeading: 'Vuoi annullare l’avviso?',
        confirmBody: 'Non ti avviseremo più quando questo articolo tornerà disponibile e il tuo indirizzo verrà cancellato.',
        confirmCta: 'Sì, annulla l’avviso',
        doneHeading: 'Avviso annullato',
        doneBody: 'Il tuo indirizzo è stato cancellato. Non riceverai altri messaggi su questo articolo.',
        goneHeading: 'Nessun avviso attivo',
        goneBody: 'Questa richiesta non esiste più: potrebbe essere già stata annullata.',
        back: 'Torna al sito',
    },
    en: {
        title: 'Cancel the back-in-stock alert',
        confirmHeading: 'Cancel this alert?',
        confirmBody: 'We will not notify you when this item is back in stock, and your address will be deleted.',
        confirmCta: 'Yes, cancel the alert',
        doneHeading: 'Alert cancelled',
        doneBody: 'Your address has been deleted. You will not receive any further messages about this item.',
        goneHeading: 'No active alert',
        goneBody: 'This request no longer exists: it may already have been cancelled.',
        back: 'Back to the site',
    },
    de: {
        title: 'Verfügbarkeitsbenachrichtigung stornieren',
        confirmHeading: 'Benachrichtigung stornieren?',
        confirmBody: 'Wir benachrichtigen Sie nicht mehr, wenn dieser Artikel wieder verfügbar ist, und Ihre Adresse wird gelöscht.',
        confirmCta: 'Ja, Benachrichtigung stornieren',
        doneHeading: 'Benachrichtigung storniert',
        doneBody: 'Ihre Adresse wurde gelöscht. Sie erhalten keine weiteren Nachrichten zu diesem Artikel.',
        goneHeading: 'Keine aktive Benachrichtigung',
        goneBody: 'Diese Anfrage existiert nicht mehr: Sie wurde möglicherweise bereits storniert.',
        back: 'Zurück zur Website',
    },
    fr: {
        title: 'Annuler l’alerte de disponibilité',
        confirmHeading: 'Annuler cette alerte ?',
        confirmBody: 'Nous ne vous préviendrons plus du retour en stock de cet article et votre adresse sera supprimée.',
        confirmCta: 'Oui, annuler l’alerte',
        doneHeading: 'Alerte annulée',
        doneBody: 'Votre adresse a été supprimée. Vous ne recevrez plus de messages concernant cet article.',
        goneHeading: 'Aucune alerte active',
        goneBody: 'Cette demande n’existe plus : elle a peut-être déjà été annulée.',
        back: 'Retour au site',
    },
    es: {
        title: 'Cancelar el aviso de disponibilidad',
        confirmHeading: '¿Cancelar este aviso?',
        confirmBody: 'No te avisaremos cuando este artículo vuelva a estar disponible y tu dirección se eliminará.',
        confirmCta: 'Sí, cancelar el aviso',
        doneHeading: 'Aviso cancelado',
        doneBody: 'Tu dirección se ha eliminado. No recibirás más mensajes sobre este artículo.',
        goneHeading: 'Ningún aviso activo',
        goneBody: 'Esta solicitud ya no existe: es posible que ya se haya cancelado.',
        back: 'Volver al sitio',
    },
    nl: {
        title: 'Voorraadmelding annuleren',
        confirmHeading: 'Deze melding annuleren?',
        confirmBody: 'We laten je niet meer weten wanneer dit artikel weer op voorraad is, en je adres wordt verwijderd.',
        confirmCta: 'Ja, melding annuleren',
        doneHeading: 'Melding geannuleerd',
        doneBody: 'Je adres is verwijderd. Je ontvangt geen berichten meer over dit artikel.',
        goneHeading: 'Geen actieve melding',
        goneBody: 'Dit verzoek bestaat niet meer: mogelijk is het al geannuleerd.',
        back: 'Terug naar de site',
    },
    pt: {
        title: 'Cancelar o aviso de disponibilidade',
        confirmHeading: 'Cancelar este aviso?',
        confirmBody: 'Deixaremos de o avisar quando este artigo voltar a estar disponível e o seu endereço será eliminado.',
        confirmCta: 'Sim, cancelar o aviso',
        doneHeading: 'Aviso cancelado',
        doneBody: 'O seu endereço foi eliminado. Não receberá mais mensagens sobre este artigo.',
        goneHeading: 'Nenhum aviso ativo',
        goneBody: 'Este pedido já não existe: pode já ter sido cancelado.',
        back: 'Voltar ao site',
    },
};

export function restockCancelPage({ lang, state, siteOrigin, token }) {
    const copy = CANCEL_PAGE_COPY[lang] || CANCEL_PAGE_COPY.en;
    const locale = CANCEL_PAGE_COPY[lang] ? lang : 'en';

    const heading = state === 'confirm' ? copy.confirmHeading
        : state === 'done' ? copy.doneHeading
        : copy.goneHeading;
    const body = state === 'confirm' ? copy.confirmBody
        : state === 'done' ? copy.doneBody
        : copy.goneBody;

    /* Il tasto di conferma manda una POST: un GET che cancellasse da solo
       verrebbe sparato anche dai prefetch dei client di posta, disiscrivendo
       chi non ha mai cliccato. */
    const form = state === 'confirm'
        ? `<form method="POST" action="/api/restock-cancel?lang=${esc(locale)}">
             <input type="hidden" name="token" value="${esc(token)}">
             <button type="submit">${esc(copy.confirmCta)}</button>
           </form>`
        : '';

    return `<!DOCTYPE html>
<html lang="${esc(locale)}"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>${esc(copy.title)}</title>
<style>
  body{margin:0;background:#f4f6f8;color:#152033;font-family:system-ui,-apple-system,Segoe UI,Arial,sans-serif;
       display:flex;align-items:center;justify-content:center;min-height:100vh;padding:24px}
  .card{background:#fff;border:1px solid #dce3ea;border-radius:12px;padding:32px;max-width:520px;width:100%}
  h1{margin:0 0 12px;font-size:22px}
  p{margin:0 0 20px;line-height:1.6;color:#3d4a5c}
  button{padding:13px 26px;background:#E8590C;color:#fff;border:none;border-radius:6px;
         font-size:15px;font-weight:700;cursor:pointer;font-family:inherit}
  button:hover{background:#d24f06}
  a{color:#5f6b7a;font-size:14px}
</style></head>
<body><main class="card">
  <h1>${esc(heading)}</h1>
  <p>${esc(body)}</p>
  ${form}
  <p style="margin:20px 0 0"><a href="${esc(siteOrigin)}/${esc(locale)}/">${esc(copy.back)}</a></p>
</main></body></html>`;
}
