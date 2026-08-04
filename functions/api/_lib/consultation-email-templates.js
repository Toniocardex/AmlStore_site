/**
 * Template email dedicati alle richieste di consulenza.
 * Separati dai template ordine per evitare dipendenze da checkout e D1.
 */

const TOPIC_LABELS_IT = {
    licences: 'Licenze software',
    workstations: 'Più postazioni',
    'microsoft-365': 'Microsoft 365',
    'server-database': 'Server e database',
    other: 'Altro',
};

const CONFIRMATION_COPY = {
    it: {
        subject: 'Abbiamo ricevuto la tua richiesta di consulenza',
        heading: 'Richiesta ricevuta',
        intro: 'Grazie per aver contattato Aml Store. Abbiamo ricevuto la tua richiesta e il nostro team ti risponderà via email.',
        support: 'L’assistenza per l’Italia è fornita in italiano.',
        reference: 'Riferimento richiesta',
        footer: 'Per aggiungere informazioni puoi rispondere direttamente a questa email.',
    },
    en: {
        subject: 'We received your consultation request',
        heading: 'Request received',
        intro: 'Thank you for contacting Aml Store. We received your request and our team will reply by email.',
        support: 'Support outside Italy is provided in English.',
        reference: 'Request reference',
        footer: 'You can reply directly to this email if you need to add information.',
    },
    fr: {
        subject: 'Nous avons reçu votre demande de consultation',
        heading: 'Demande reçue',
        intro: 'Merci d’avoir contacté Aml Store. Nous avons reçu votre demande et notre équipe vous répondra par e-mail.',
        support: 'La réponse de notre équipe d’assistance sera fournie en anglais.',
        reference: 'Référence de la demande',
        footer: 'Vous pouvez répondre directement à cet e-mail pour ajouter des informations.',
    },
    de: {
        subject: 'Wir haben Ihre Beratungsanfrage erhalten',
        heading: 'Anfrage erhalten',
        intro: 'Vielen Dank für Ihre Nachricht an Aml Store. Wir haben Ihre Anfrage erhalten und unser Team antwortet Ihnen per E-Mail.',
        support: 'Die Antwort unseres Support-Teams erfolgt auf Englisch.',
        reference: 'Anfragereferenz',
        footer: 'Sie können direkt auf diese E-Mail antworten, um weitere Informationen hinzuzufügen.',
    },
    es: {
        subject: 'Hemos recibido tu solicitud de asesoramiento',
        heading: 'Solicitud recibida',
        intro: 'Gracias por contactar con Aml Store. Hemos recibido tu solicitud y nuestro equipo responderá por correo electrónico.',
        support: 'La respuesta de nuestro equipo de asistencia se proporcionará en inglés.',
        reference: 'Referencia de la solicitud',
        footer: 'Puedes responder directamente a este correo para añadir información.',
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

function textValue(value, fallback = 'N/D') {
    const normalized = String(value ?? '').trim();
    return normalized || fallback;
}

function infoRow(label, value) {
    return `<tr>
        <td style="padding:7px 12px 7px 0;color:#5f6b7a;vertical-align:top;width:180px">${esc(label)}</td>
        <td style="padding:7px 0;color:#152033;font-weight:600;vertical-align:top">${esc(textValue(value))}</td>
    </tr>`;
}

export function consultationInternalEmail(lead) {
    const reference = String(lead.id || '').slice(0, 8).toUpperCase();
    const subject = `[Aml Store] Nuova richiesta di consulenza ${reference}`;
    const fullName = `${lead.firstName || ''} ${lead.lastName || ''}`.trim();
    const topic = TOPIC_LABELS_IT[lead.topic] || lead.topic;
    const received = new Date(lead.receivedAt).toLocaleString('it-IT', { timeZone: 'Europe/Rome' });

    const html = `<!DOCTYPE html>
<html lang="it"><head><meta charset="UTF-8"><title>${esc(subject)}</title></head>
<body style="margin:0;background:#f4f6f8;font-family:Arial,sans-serif;color:#152033">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:24px;background:#f4f6f8">
    <tr><td align="center">
      <table width="680" cellpadding="0" cellspacing="0" style="width:100%;max-width:680px;background:#fff;border:1px solid #dce3ea;border-radius:10px;overflow:hidden">
        <tr><td style="padding:22px 26px;background:#14243a;color:#fff">
          <p style="margin:0 0 6px;font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#b9cbe1">Aml Store</p>
          <h1 style="margin:0;font-size:22px">Nuova richiesta di consulenza</h1>
        </td></tr>
        <tr><td style="padding:24px 26px">
          <table width="100%" cellpadding="0" cellspacing="0">
            ${infoRow('Riferimento', reference)}
            ${infoRow('Ricevuta il', received)}
            ${infoRow('Nome', fullName)}
            ${infoRow('Azienda', lead.company)}
            ${infoRow('Email', lead.email)}
            ${infoRow('Tipo di richiesta', topic)}
            ${infoRow('Numero postazioni', lead.seats)}
            ${infoRow('Lingua pagina', String(lead.locale || '').toUpperCase())}
            ${infoRow('Lingua assistenza', lead.supportLanguage === 'it' ? 'Italiano' : 'Inglese')}
            ${infoRow('Pagina di origine', lead.sourcePath)}
          </table>
          <h2 style="margin:22px 0 10px;font-size:16px">Messaggio</h2>
          <div style="padding:14px 16px;background:#f4f6f8;border:1px solid #dce3ea;border-radius:8px;white-space:pre-wrap;line-height:1.6">${esc(lead.message)}</div>
          <p style="margin:20px 0 0;color:#5f6b7a;font-size:13px">Rispondi a questa email: il Reply-To è impostato sull’indirizzo del richiedente.</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body></html>`;

    const text = [
        'Nuova richiesta di consulenza Aml Store',
        '',
        `Riferimento: ${reference}`,
        `Ricevuta il: ${received}`,
        `Nome: ${fullName}`,
        `Azienda: ${textValue(lead.company)}`,
        `Email: ${lead.email}`,
        `Tipo di richiesta: ${textValue(topic)}`,
        `Numero postazioni: ${textValue(lead.seats)}`,
        `Lingua pagina: ${String(lead.locale || '').toUpperCase()}`,
        `Lingua assistenza: ${lead.supportLanguage === 'it' ? 'Italiano' : 'Inglese'}`,
        `Pagina di origine: ${textValue(lead.sourcePath)}`,
        '',
        'Messaggio:',
        lead.message,
    ].join('\n');

    return { subject, html, text };
}

export function consultationConfirmationEmail(lead) {
    const locale = CONFIRMATION_COPY[lead.locale] ? lead.locale : 'en';
    const copy = CONFIRMATION_COPY[locale];
    const reference = String(lead.id || '').slice(0, 8).toUpperCase();

    const html = `<!DOCTYPE html>
<html lang="${esc(locale)}"><head><meta charset="UTF-8"><title>${esc(copy.subject)}</title></head>
<body style="margin:0;background:#f4f6f8;font-family:Arial,sans-serif;color:#152033">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:24px;background:#f4f6f8">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0" style="width:100%;max-width:620px;background:#fff;border:1px solid #dce3ea;border-radius:10px;overflow:hidden">
        <tr><td style="padding:22px 26px;background:#14243a;color:#fff"><strong style="font-size:18px">Aml Store</strong></td></tr>
        <tr><td style="padding:28px 26px">
          <h1 style="margin:0 0 14px;font-size:24px">${esc(copy.heading)}</h1>
          <p style="margin:0 0 16px;line-height:1.65">${esc(copy.intro)}</p>
          <p style="margin:0 0 20px;padding:12px 14px;background:#eaf0f6;border-radius:8px;line-height:1.55"><strong>${esc(copy.support)}</strong></p>
          <p style="margin:0 0 18px;color:#5f6b7a">${esc(copy.reference)}: <strong style="color:#152033">${esc(reference)}</strong></p>
          <p style="margin:0;color:#5f6b7a;font-size:13px;line-height:1.55">${esc(copy.footer)}</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body></html>`;

    const text = [
        copy.heading,
        '',
        copy.intro,
        copy.support,
        '',
        `${copy.reference}: ${reference}`,
        '',
        copy.footer,
    ].join('\n');

    return { subject: copy.subject, html, text };
}
