/**
 * Genera pagine prodotto statiche HTML (una per lingua) sotto `/{lang}/products/{slug}.html`
 * leggendo i prodotti attivi da D1 locale (wrangler). Da eseguire prima del deploy.
 *
 * Uso:
 *   npm run build:product-pages
 *   SITE_ORIGIN=https://Aml-Store.com npm run build:product-pages
 *
 * D1 remoto (CI): wrangler d1 execute aml-store-d1 --remote --file=scripts/sql/select-active-products-for-pages.sql
 *   e adattare questo script a leggere JSON da stdin se preferisci.
 */
import { execSync } from 'node:child_process';
import { existsSync, mkdirSync, readdirSync, rmSync, unlinkSync, writeFileSync } from 'node:fs';
import { isReservedStoreProductSlug, RESERVED_STORE_PRODUCT_SLUGS } from '../functions/lib/slug.js';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const LANGS = /** @type {const} */ (['it', 'en', 'de', 'fr', 'es']);

const SITE_ORIGIN = (process.env.SITE_ORIGIN || 'https://Aml-Store.com').replace(/\/$/, '');

/** Sottocartella solo per le schede generate (come l’ex `p/`). */
const PRODUCT_PAGES_DIR = 'products';

/** @param {string} s */
function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/** @param {string} slug */
function assertSafeSlug(slug) {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/i.test(slug)) {
    throw new Error(`Slug non sicuro per filesystem: ${slug}`);
  }
}

/**
 * @param {Record<string, unknown>} row
 * @param {'it'|'en'|'de'|'fr'|'es'} lang
 */
function titleFor(row, lang) {
  const v = row[`title_${lang}`];
  return String(v ?? row.title_it ?? '').trim();
}

/**
 * @param {Record<string, unknown>} row
 * @param {'it'|'en'|'de'|'fr'|'es'} lang
 */
function descFor(row, lang) {
  const v = row[`description_${lang}`];
  return String(v ?? row.description_it ?? '').trim();
}

/** @param {'it'|'en'|'de'|'fr'|'es'} lang */
function localeFor(lang) {
  const map = { it: 'it-IT', en: 'en-GB', de: 'de-DE', fr: 'fr-FR', es: 'es-ES' };
  return map[lang];
}

/** @param {number} cents @param {string} currency @param {'it'|'en'|'de'|'fr'|'es'} lang */
function formatMoney(cents, currency, lang) {
  const cur = currency || 'EUR';
  try {
    return new Intl.NumberFormat(localeFor(lang), { style: 'currency', currency: cur }).format(cents / 100);
  } catch {
    return `${(cents / 100).toFixed(2)} ${cur}`;
  }
}

/** @param {{ title: string; body: string }[]} cards */
function valueCardsHtml(cards) {
  return cards
    .map(
      (c) => `          <li class="product-value-card">
            <h3 class="product-value-card__title">${escapeHtml(c.title)}</h3>
            <p class="product-value-card__body">${escapeHtml(c.body)}</p>
          </li>`
    )
    .join('\n');
}

/** @param {{ q: string; a: string }[]} items */
function faqHtml(items) {
  return items
    .map(
      (item) => `          <details class="product-faq__item">
            <summary class="product-faq__summary">${escapeHtml(item.q)}</summary>
            <div class="product-faq__panel">${escapeHtml(item.a)}</div>
          </details>`
    )
    .join('\n');
}

/** @param {{ label: string; sub: string }[]} kpis */
function productKpisHtml(kpis) {
  return kpis
    .map(
      (k) => `          <li class="product-kpi-tile">
            <strong class="product-kpi-tile__label">${escapeHtml(k.label)}</strong>
            <span class="product-kpi-tile__sub">${escapeHtml(k.sub)}</span>
          </li>`
    )
    .join('\n');
}

/** @param {{ title: string; body: string }[]} steps */
function productStepsHtml(steps) {
  return steps
    .map(
      (s, i) => `          <li class="product-step">
            <span class="product-step__num" aria-hidden="true">${String(i + 1)}</span>
            <div class="product-step__body">
              <strong class="product-step__title">${escapeHtml(s.title)}</strong>
              <p class="product-step__text">${escapeHtml(s.body)}</p>
            </div>
          </li>`
    )
    .join('\n');
}

/** @param {[string, string][]} rows */
function productSpecTableHtml(rows) {
  return rows
    .map(
      ([k, v]) => `          <div class="product-spec-row">
            <dt class="product-spec-dt">${escapeHtml(k)}</dt>
            <dd class="product-spec-dd">${escapeHtml(v)}</dd>
          </div>`
    )
    .join('\n');
}

/** @param {string[]} labels */
function productAppsBadgesHtml(labels) {
  return labels
    .map((t) => `          <li class="product-app-badge">${escapeHtml(t)}</li>`)
    .join('\n');
}

/** @param {{ title: string; body: string }[]} items */
function productWhyStoreHtml(items) {
  return items
    .map(
      (it) => `          <li class="product-why-card">
            <h3 class="product-why-card__title">${escapeHtml(it.title)}</h3>
            <p class="product-why-card__body">${escapeHtml(it.body)}</p>
          </li>`
    )
    .join('\n');
}

const UI = {
  it: {
    siteTitle: 'Aml-Store',
    skip: 'Vai al contenuto',
    backCatalog: 'Torna al catalogo',
    ship: 'Prodotto fisico: al checkout servirà un indirizzo di spedizione.',
    addCart: 'Aggiungi al carrello',
    paymentsLabel: 'Metodi di pagamento',
    mediaPlaceholder: 'Immagine prodotto non disponibile',
    productPromoBadge: '',
    productCodeLabel: 'Codice prodotto',
    productTagline: 'Aml-Store.com · Software e licenze con consegna digitale',
    kpiSectionAria: 'Punti chiave',
    kpis: [
      { label: 'Checkout sicuro', sub: 'Prezzi verificati su database aggiornato' },
      { label: 'Email di conferma', sub: 'Riepilogo ordine e riferimenti' },
      { label: 'Licenza digitale', sub: 'ESD dove previsto dal vendor' },
      { label: 'Supporto', sub: 'Contatti su documento d’acquisto' },
    ],
    appsTitle: 'Cosa include questo acquisto',
    appsBadges: [
      'Catalogo multilingua',
      'Carrello condiviso',
      'Account e ordini',
      'Checkout guidato',
      'Metodi di pagamento sicuri',
      'Fatturazione se richiesta',
    ],
    specTitle: 'Specifiche tecniche e licenza',
    specLabelType: 'Tipo prodotto',
    specLabelSku: 'SKU / slug',
    specLabelLang: 'Lingue storefront',
    specDigital: 'Digitale (ESD) · nessuna spedizione fisica',
    specPhysical: 'Fisico · indirizzo di spedizione al checkout',
    specLangBcf: 'IT, EN, DE, FR, ES',
    stepsTitle: 'Consegna e attivazione',
    stepsSectionAria: 'Passi dopo l’acquisto',
    steps: [
      {
        title: 'Ordine confermato',
        body: 'Ricevi l’email di conferma con i dettagli dell’acquisto e il riferimento ordine.',
      },
      {
        title: 'Pagamento e verifica',
        body: 'Al checkout inserisci i dati richiesti; l’ordine viene registrato in modo sicuro.',
      },
      {
        title: 'Consegna digitale',
        body: 'Codici o link di attivazione seguono le policy del vendor (email o area riservata).',
      },
      {
        title: 'Attivazione',
        body: 'Completa l’attivazione sul portale ufficiale del produttore quando indicato.',
      },
    ],
    trustSectionTitle: 'Acquisto e fiducia',
    trustInvoiceLine: 'Fattura elettronica e dati SDI/PEC dove richiesti dal checkout.',
    trustPilotLine: 'Leggi le recensioni su Trustpilot',
    trustPilotHref: 'https://www.trustpilot.com/',
    whyStoreTitle: 'Perché scegliere AML Store',
    whyStoreLead: 'Licenze selezionate, processo chiaro e supporto operativo post-vendita.',
    whyStoreItems: [
      {
        title: 'Licenze e canali ufficiali',
        body: 'Percorsi di attivazione allineati alle policy dei vendor.',
      },
      {
        title: 'Fatturazione',
        body: 'Flusso pensato per professionisti e aziende con dati fiscali al checkout.',
      },
      {
        title: 'Tempi di consegna',
        body: 'Per i digitali: indicazioni in scheda e email; per i fisici: spedizione tracciata.',
      },
      {
        title: 'Assistenza',
        body: 'Canali indicati in fattura o email d’ordine per dubbi post-acquisto.',
      },
    ],
    stickyContinueShopping: 'Torna al catalogo',
    detailSectionTitle: 'Descrizione',
    advantagesTitle: 'Vantaggi',
    faqSectionTitle: 'Domande frequenti',
    valueCards: [
      {
        title: 'Catalogo su database edge',
        body: 'Prezzi e disponibilità aggiornati con bassa latenza, per un checkout affidabile.',
      },
      {
        title: 'Prezzi trasparenti',
        body: 'Vedi il totale nel carrello prima di procedere: niente sorprese in fase di pagamento.',
      },
      {
        title: 'Ordine tracciabile',
        body: 'Dopo l’acquisto l’ordine resta nel sistema: ideale per fatturazione e assistenza.',
      },
      {
        title: 'Digitale e fisico',
        body: 'Indica correttamente il tipo di prodotto: i digitali non richiedono spedizione.',
      },
    ],
    faq: [
      {
        q: 'Come compro un prodotto?',
        a: 'Aggiungi al carrello da questa scheda, apri il carrello e completa il checkout con i dati richiesti.',
      },
      {
        q: 'Cosa cambia tra digitale e fisico?',
        a: 'I prodotti fisici richiedono un indirizzo di spedizione al checkout; quelli digitali no.',
      },
      {
        q: 'Posso cambiare lingua del sito?',
        a: 'Sì: usa il menu lingua nell’header per passare a IT, EN, DE, FR o ES.',
      },
    ],
  },
  en: {
    siteTitle: 'Aml-Store',
    skip: 'Skip to content',
    backCatalog: 'Back to catalog',
    ship: 'Physical item: a shipping address is required at checkout.',
    addCart: 'Add to cart',
    paymentsLabel: 'Payment methods',
    mediaPlaceholder: 'Product image not available',
    productPromoBadge: '',
    productCodeLabel: 'Product code',
    productTagline: 'Aml-Store.com · Software and digital delivery',
    kpiSectionAria: 'Highlights',
    kpis: [
      { label: 'Secure checkout', sub: 'Prices verified against the database' },
      { label: 'Order email', sub: 'Confirmation and references' },
      { label: 'Digital licence', sub: 'ESD where applicable' },
      { label: 'Support', sub: 'Contact details on your purchase document' },
    ],
    appsTitle: 'What this purchase includes',
    appsBadges: [
      'Multilingual catalog',
      'Shared cart',
      'Account & orders',
      'Guided checkout',
      'Secure payments',
      'Invoicing when required',
    ],
    specTitle: 'Technical specs & licence',
    specLabelType: 'Product type',
    specLabelSku: 'SKU / slug',
    specLabelLang: 'Storefront languages',
    specDigital: 'Digital (ESD) · no physical shipment',
    specPhysical: 'Physical · shipping address required at checkout',
    specLangBcf: 'IT, EN, DE, FR, ES',
    stepsTitle: 'Delivery & activation',
    stepsSectionAria: 'Steps after purchase',
    steps: [
      {
        title: 'Order confirmed',
        body: 'You receive a confirmation email with purchase details and the order reference.',
      },
      {
        title: 'Payment & verification',
        body: 'Complete checkout fields; the order is stored securely.',
      },
      {
        title: 'Digital delivery',
        body: 'Codes or activation links follow the vendor policy (email or self-service).',
      },
      {
        title: 'Activation',
        body: 'Finish activation on the vendor portal when applicable.',
      },
    ],
    trustSectionTitle: 'Trust & purchase',
    trustInvoiceLine: 'E-invoicing and tax fields when required at checkout.',
    trustPilotLine: 'Read reviews on Trustpilot',
    trustPilotHref: 'https://www.trustpilot.com/',
    whyStoreTitle: 'Why choose AML Store',
    whyStoreLead: 'Curated licences, a clear flow, and practical post-sale support.',
    whyStoreItems: [
      {
        title: 'Official-style delivery',
        body: 'Activation paths aligned with vendor policies.',
      },
      {
        title: 'Invoicing',
        body: 'Checkout designed for pros and businesses.',
      },
      {
        title: 'Delivery times',
        body: 'Digital: stated on the page and email; physical: tracked shipping.',
      },
      {
        title: 'Help',
        body: 'Channels noted on invoice or order email.',
      },
    ],
    stickyContinueShopping: 'Back to catalog',
    detailSectionTitle: 'Description',
    advantagesTitle: 'Benefits',
    faqSectionTitle: 'FAQ',
    valueCards: [
      {
        title: 'Edge-backed catalog',
        body: 'Pricing and availability are served with low latency for a dependable checkout.',
      },
      {
        title: 'Clear pricing',
        body: 'Review your cart totals before you pay—no last‑minute surprises.',
      },
      {
        title: 'Order tracking',
        body: 'Your purchase stays in the system for invoicing and support follow‑up.',
      },
      {
        title: 'Digital and physical',
        body: 'Product type is explicit: digital items do not need a shipping address.',
      },
    ],
    faq: [
      {
        q: 'How do I buy?',
        a: 'Use Add to cart on this page, open your cart, then complete checkout with the required details.',
      },
      {
        q: 'Digital vs physical?',
        a: 'Physical products need a shipping address at checkout; digital products do not.',
      },
      {
        q: 'Can I change language?',
        a: 'Yes—use the language menu in the header (IT, EN, DE, FR, ES).',
      },
    ],
  },
  de: {
    siteTitle: 'Aml-Store',
    skip: 'Zum Inhalt springen',
    backCatalog: 'Zurück zum Katalog',
    ship: 'Physisches Produkt: Lieferadresse an der Kasse erforderlich.',
    addCart: 'In den Warenkorb',
    paymentsLabel: 'Zahlungsarten',
    mediaPlaceholder: 'Kein Produktbild',
    productPromoBadge: '',
    productCodeLabel: 'Produktcode',
    productTagline: 'Aml-Store.com · Software und digitale Lieferung',
    kpiSectionAria: 'Highlights',
    kpis: [
      { label: 'Sicherer Checkout', sub: 'Preise aus der Datenbank' },
      { label: 'Bestätigung per E-Mail', sub: 'Übersicht und Referenzen' },
      { label: 'Digital-Lizenz', sub: 'ESD je nach Vendor' },
      { label: 'Support', sub: 'Kontakt auf dem Beleg' },
    ],
    appsTitle: 'Inhalt dieses Kaufs',
    appsBadges: ['Mehrsprachiger Katalog', 'Warenkorb', 'Konto & Bestellungen', 'Checkout', 'Zahlungen', 'Rechnung'],
    specTitle: 'Spezifikationen & Lizenz',
    specLabelType: 'Produkttyp',
    specLabelSku: 'SKU / Slug',
    specLabelLang: 'Storefront-Sprachen',
    specDigital: 'Digital (ESD) · kein Versand',
    specPhysical: 'Physisch · Lieferadresse an der Kasse',
    specLangBcf: 'IT, EN, DE, FR, ES',
    stepsTitle: 'Lieferung & Aktivierung',
    stepsSectionAria: 'Schritte nach dem Kauf',
    steps: [
      { title: 'Bestellung bestätigt', body: 'E-Mail mit Details und Referenz.' },
      { title: 'Zahlung', body: 'Checkout ausfüllen; Bestellung wird sicher gespeichert.' },
      { title: 'Digitale Lieferung', body: 'Codes/Links gemäß Vendor-Richtlinie.' },
      { title: 'Aktivierung', body: 'Im Herstellerportal abschließen, falls nötig.' },
    ],
    trustSectionTitle: 'Vertrauen',
    trustInvoiceLine: 'E-Rechnung / Steuerdaten je nach Checkout.',
    trustPilotLine: 'Trustpilot-Bewertungen',
    trustPilotHref: 'https://www.trustpilot.com/',
    whyStoreTitle: 'Warum AML Store',
    whyStoreLead: 'Ausgewählte Lizenzen, klarer Ablauf, Support nach dem Kauf.',
    whyStoreItems: [
      { title: 'Lieferkanäle', body: 'Aktivierung gemäß Vendor.' },
      { title: 'Rechnung', body: 'Checkout für Profis und Firmen.' },
      { title: 'Lieferzeiten', body: 'Digital per Mail; physisch mit Tracking.' },
      { title: 'Hilfe', body: 'Kontakte auf Rechnung oder E-Mail.' },
    ],
    stickyContinueShopping: 'Zurück zum Katalog',
    detailSectionTitle: 'Beschreibung',
    advantagesTitle: 'Vorteile',
    faqSectionTitle: 'Häufige Fragen',
    valueCards: [
      {
        title: 'Katalog am Edge',
        body: 'Preise und Verfügbarkeit mit geringer Latenz – zuverlässiger Checkout.',
      },
      {
        title: 'Klare Preise',
        body: 'Summen im Warenkorb prüfen, bevor Sie zahlen.',
      },
      {
        title: 'Nachvollziehbare Bestellung',
        body: 'Der Kauf bleibt im System – hilfreich für Support und Abrechnung.',
      },
      {
        title: 'Digital und physisch',
        body: 'Der Produkttyp ist klar: digitale Artikel brauchen keine Lieferadresse.',
      },
    ],
    faq: [
      {
        q: 'Wie kaufe ich?',
        a: 'In den Warenkorb, Warenkorb öffnen, dann Checkout mit den erforderlichen Daten abschließen.',
      },
      {
        q: 'Digital oder physisch?',
        a: 'Physisch: Lieferadresse an der Kasse. Digital: keine Lieferadresse nötig.',
      },
      {
        q: 'Sprache wechseln?',
        a: 'Ja – Sprachmenü im Header (IT, EN, DE, FR, ES).',
      },
    ],
  },
  fr: {
    siteTitle: 'Aml-Store',
    skip: 'Aller au contenu',
    backCatalog: 'Retour au catalogue',
    ship: 'Produit physique : une adresse de livraison sera demandée au paiement.',
    addCart: 'Ajouter au panier',
    paymentsLabel: 'Moyens de paiement',
    mediaPlaceholder: 'Image produit indisponible',
    productPromoBadge: '',
    productCodeLabel: 'Code produit',
    productTagline: 'Aml-Store.com · Logiciels et livraison numérique',
    kpiSectionAria: 'Points clés',
    kpis: [
      { label: 'Paiement sécurisé', sub: 'Prix vérifiés en base' },
      { label: 'Email de confirmation', sub: 'Récapitulatif et références' },
      { label: 'Licence numérique', sub: 'ESD si applicable' },
      { label: 'Support', sub: 'Contacts sur le document d’achat' },
    ],
    appsTitle: 'Contenu de cet achat',
    appsBadges: ['Catalogue multilingue', 'Panier', 'Compte & commandes', 'Checkout', 'Paiements', 'Facturation'],
    specTitle: 'Spécifications & licence',
    specLabelType: 'Type de produit',
    specLabelSku: 'SKU / slug',
    specLabelLang: 'Langues du site',
    specDigital: 'Numérique (ESD) · pas d’envoi physique',
    specPhysical: 'Physique · adresse de livraison au checkout',
    specLangBcf: 'IT, EN, DE, FR, ES',
    stepsTitle: 'Livraison & activation',
    stepsSectionAria: 'Étapes après achat',
    steps: [
      { title: 'Commande confirmée', body: 'Email avec détails et référence.' },
      { title: 'Paiement', body: 'Checkout sécurisé; commande enregistrée.' },
      { title: 'Livraison numérique', body: 'Codes/liens selon politique du vendeur.' },
      { title: 'Activation', body: 'Portail fabricant si nécessaire.' },
    ],
    trustSectionTitle: 'Confiance',
    trustInvoiceLine: 'Facturation électronique si requise au checkout.',
    trustPilotLine: 'Avis Trustpilot',
    trustPilotHref: 'https://www.trustpilot.com/',
    whyStoreTitle: 'Pourquoi AML Store',
    whyStoreLead: 'Licences sélectionnées, parcours clair, support après-vente.',
    whyStoreItems: [
      { title: 'Canaux officiels', body: 'Activation alignée sur le vendor.' },
      { title: 'Facturation', body: 'Checkout pour pros et entreprises.' },
      { title: 'Délais', body: 'Numérique par email; physique suivi.' },
      { title: 'Aide', body: 'Contacts sur facture ou email.' },
    ],
    stickyContinueShopping: 'Retour au catalogue',
    detailSectionTitle: 'Description',
    advantagesTitle: 'Avantages',
    faqSectionTitle: 'Questions fréquentes',
    valueCards: [
      {
        title: 'Catalogue edge',
        body: 'Prix et disponibilité servis avec peu de latence pour un paiement fiable.',
      },
      {
        title: 'Prix clairs',
        body: 'Consultez le total du panier avant de payer.',
      },
      {
        title: 'Commande suivie',
        body: 'L’achat reste dans le système pour facturation et support.',
      },
      {
        title: 'Numérique et physique',
        body: 'Le type de produit est explicite : le numérique ne nécessite pas d’adresse de livraison.',
      },
    ],
    faq: [
      {
        q: 'Comment acheter ?',
        a: 'Ajoutez au panier depuis cette page, ouvrez le panier, puis finalisez le paiement.',
      },
      {
        q: 'Numérique ou physique ?',
        a: 'Physique : adresse de livraison au checkout. Numérique : pas d’adresse d’expédition.',
      },
      {
        q: 'Changer de langue ?',
        a: 'Oui — menu langue dans l’en-tête (IT, EN, DE, FR, ES).',
      },
    ],
  },
  es: {
    siteTitle: 'Aml-Store',
    skip: 'Ir al contenido',
    backCatalog: 'Volver al catálogo',
    ship: 'Producto físico: en el checkout se pedirá dirección de envío.',
    addCart: 'Añadir al carrito',
    paymentsLabel: 'Medios de pago',
    mediaPlaceholder: 'Imagen del producto no disponible',
    productPromoBadge: '',
    productCodeLabel: 'Código de producto',
    productTagline: 'Aml-Store.com · Software y entrega digital',
    kpiSectionAria: 'Puntos clave',
    kpis: [
      { label: 'Checkout seguro', sub: 'Precios verificados en base de datos' },
      { label: 'Email de confirmación', sub: 'Resumen y referencias' },
      { label: 'Licencia digital', sub: 'ESD si aplica' },
      { label: 'Soporte', sub: 'Contactos en el documento de compra' },
    ],
    appsTitle: 'Qué incluye esta compra',
    appsBadges: ['Catálogo multilingüe', 'Carrito', 'Cuenta y pedidos', 'Checkout', 'Pagos', 'Facturación'],
    specTitle: 'Especificaciones y licencia',
    specLabelType: 'Tipo de producto',
    specLabelSku: 'SKU / slug',
    specLabelLang: 'Idiomas del sitio',
    specDigital: 'Digital (ESD) · sin envío físico',
    specPhysical: 'Físico · dirección de envío en el checkout',
    specLangBcf: 'IT, EN, DE, FR, ES',
    stepsTitle: 'Entrega y activación',
    stepsSectionAria: 'Pasos tras la compra',
    steps: [
      { title: 'Pedido confirmado', body: 'Email con detalles y referencia.' },
      { title: 'Pago', body: 'Checkout seguro; pedido registrado.' },
      { title: 'Entrega digital', body: 'Códigos/enlaces según el vendor.' },
      { title: 'Activación', body: 'Portal del fabricante si aplica.' },
    ],
    trustSectionTitle: 'Confianza',
    trustInvoiceLine: 'Factura electrónica si el checkout lo requiere.',
    trustPilotLine: 'Reseñas en Trustpilot',
    trustPilotHref: 'https://www.trustpilot.com/',
    whyStoreTitle: 'Por qué AML Store',
    whyStoreLead: 'Licencias seleccionadas, flujo claro y soporte postventa.',
    whyStoreItems: [
      { title: 'Canales oficiales', body: 'Activación alineada con el vendor.' },
      { title: 'Facturación', body: 'Checkout para profesionales y empresas.' },
      { title: 'Plazos', body: 'Digital por email; físico con seguimiento.' },
      { title: 'Ayuda', body: 'Contactos en factura o email.' },
    ],
    stickyContinueShopping: 'Volver al catálogo',
    detailSectionTitle: 'Descripción',
    advantagesTitle: 'Ventajas',
    faqSectionTitle: 'Preguntas frecuentes',
    valueCards: [
      {
        title: 'Catálogo en el edge',
        body: 'Precios y disponibilidad con baja latencia para un checkout fiable.',
      },
      {
        title: 'Precios transparentes',
        body: 'Revisa el total del carrito antes de pagar.',
      },
      {
        title: 'Pedido trazable',
        body: 'La compra queda en el sistema para facturación y soporte.',
      },
      {
        title: 'Digital y físico',
        body: 'El tipo de producto es explícito: lo digital no requiere envío.',
      },
    ],
    faq: [
      {
        q: '¿Cómo compro?',
        a: 'Añade al carrito desde esta página, abre el carrito y completa el checkout.',
      },
      {
        q: '¿Digital o físico?',
        a: 'Físico: dirección de envío en el checkout. Digital: no hace falta envío.',
      },
      {
        q: '¿Cambiar idioma?',
        a: 'Sí — menú de idioma en la cabecera (IT, EN, DE, FR, ES).',
      },
    ],
  },
};

/**
 * @param {Record<string, unknown>} row
 * @param {'it'|'en'|'de'|'fr'|'es'} lang
 */
function buildPage(row, lang) {
  const slug = String(row.slug ?? '').trim();
  assertSafeSlug(slug);
  if (isReservedStoreProductSlug(slug)) {
    throw new Error(
      `Slug "${slug}" riservato (stessa URL di una pagina del sito). Rinomina il prodotto in admin o D1.`
    );
  }
  const title = titleFor(row, lang);
  const description = descFor(row, lang);
  const price_cents = Math.round(Number(row.price_cents) || 0);
  const currency = String(row.currency || 'EUR');
  const fulfillment = String(row.fulfillment || 'digital').toLowerCase() === 'physical' ? 'physical' : 'digital';
  const cover = typeof row.cover_image === 'string' ? row.cover_image.trim() : '';
  const coverOk = cover.startsWith('/img/products/') && !cover.includes('..');
  const coverAbs = coverOk ? `${SITE_ORIGIN}${cover}` : `${SITE_ORIGIN}/img/logo/logo-header-400.webp`;
  const canonical = `${SITE_ORIGIN}/${lang}/${PRODUCT_PAGES_DIR}/${encodeURIComponent(slug)}.html`;
  const u = UI[lang];
  const priceStr = formatMoney(price_cents, currency, lang);
  const priceSchema = (price_cents / 100).toFixed(2);

  const hrefRows = LANGS.map(
    (l) =>
      `  <link rel="alternate" hreflang="${l}" href="${SITE_ORIGIN}/${l}/${PRODUCT_PAGES_DIR}/${encodeURIComponent(slug)}.html" />`
  ).join('\n');

  const langNavFixed = LANGS.map((l) => {
    const labels = { it: 'Italiano', en: 'English', de: 'Deutsch', fr: 'Français', es: 'Español' };
    const base = `href="/${l}/${PRODUCT_PAGES_DIR}/${encodeURIComponent(slug)}.html" hreflang="${l}" class="lang-dropdown__link`;
    const cls = l === lang ? `${base} is-current" aria-current="page"` : `${base}"`;
    return `            <a ${cls}>${labels[l]}</a>`;
  }).join('\n');

  const ld = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: title,
    description,
    sku: slug,
    url: canonical,
    image: [coverAbs],
    offers: {
      '@type': 'Offer',
      url: canonical,
      priceCurrency: currency,
      price: priceSchema,
      availability: 'https://schema.org/InStock',
    },
  };
  const ldJson = JSON.stringify(ld).replace(/</g, '\\u003c');

  const payload = {
    slug,
    title,
    price_cents,
    currency,
    fulfillment,
  };
  const payloadJson = JSON.stringify(payload).replace(/</g, '\\u003c');

  const mediaBlock = coverOk
    ? `<figure class="product-cover">
          <img src="${escapeHtml(cover)}" width="880" height="495" alt="" decoding="async" fetchpriority="high" class="product-cover__img" />
        </figure>`
    : `<figure class="product-cover product-cover--placeholder" aria-label="${escapeHtml(u.mediaPlaceholder)}">
          <div class="product-cover__placeholder" role="img"></div>
        </figure>`;

  const valueCardsBlock = valueCardsHtml(u.valueCards);
  const faqBlock = faqHtml(u.faq);

  const shipBlock =
    fulfillment === 'physical'
      ? `<p class="product-ship-note">${escapeHtml(u.ship)}</p>`
      : '';

  const dealBannerBlock = u.productPromoBadge
    ? `          <div class="product-deal-banner">${escapeHtml(u.productPromoBadge)}</div>\n`
    : '';
  const breadcrumbTail = title.length > 56 ? `${title.slice(0, 56)}…` : title;
  const breadcrumbHtml = `      <nav class="product-breadcrumb product-breadcrumb--rich" aria-label="Breadcrumb">
        <div class="product-breadcrumb__path">
          <a href="/${lang}/#catalog">${escapeHtml(u.backCatalog)}</a>
          <span class="product-breadcrumb__sep" aria-hidden="true">›</span>
          <span class="product-breadcrumb__current">${escapeHtml(breadcrumbTail)}</span>
        </div>
      </nav>`;
  const licType = fulfillment === 'physical' ? u.specPhysical : u.specDigital;
  const specRowsHtml = productSpecTableHtml([
    [u.specLabelType, licType],
    [u.specLabelSku, slug],
    [u.specLabelLang, u.specLangBcf],
  ]);
  const kpiBlock = productKpisHtml(u.kpis);
  const appsBlock = productAppsBadgesHtml(u.appsBadges);
  const stepsBlock = productStepsHtml(u.steps);
  const whyBlock = productWhyStoreHtml(u.whyStoreItems);

  return `<!DOCTYPE html>
<html lang="${lang}">
<head>
  <meta charset="utf-8" />
  <script src="/js/theme-init.js"></script>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#1e3a6e" />
  <link rel="icon" href="/favicon.ico" sizes="any" />
  <link rel="icon" type="image/webp" href="/img/favicon/icon-32.webp" sizes="32x32" />
  <link rel="apple-touch-icon" href="/img/favicon/apple-touch-icon.png" />
  <title>${escapeHtml(title)} · ${escapeHtml(u.siteTitle)}</title>
  <meta name="description" content="${escapeHtml(description.slice(0, 300))}" />
  <link rel="canonical" href="${escapeHtml(canonical)}" />
${hrefRows}
  <link rel="alternate" hreflang="x-default" href="${SITE_ORIGIN}/it/${PRODUCT_PAGES_DIR}/${encodeURIComponent(slug)}.html" />
  <meta property="og:type" content="product" />
  <meta property="og:title" content="${escapeHtml(title)}" />
  <meta property="og:description" content="${escapeHtml(description.slice(0, 200))}" />
  <meta property="og:url" content="${escapeHtml(canonical)}" />
  <meta property="og:image" content="${escapeHtml(coverAbs)}" />
  <meta property="og:locale" content="${localeFor(lang).replace('-', '_')}" />
  <script type="application/ld+json">${ldJson}</script>
  <link rel="preload" href="/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="/fonts/inter-latin-ext-400-normal.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="/css/style.css" />
  <script type="module" src="/js/nav.js"></script>
  <script type="module" src="/js/product-page.js"></script>
</head>
<body>
  <a class="skip-link" href="#contenuto">${escapeHtml(u.skip)}</a>
  <header class="site-header" translate="no">
    <div class="inner header-inner">
      <div class="brand-block">
        <a href="/${lang}/" class="logo-link" aria-label="${escapeHtml(u.siteTitle)}">
          <img class="logo-img logo-img--for-light-bg" src="/img/logo/logo-header-200.webp" srcset="/img/logo/logo-header-200.webp 200w, /img/logo/logo-header-400.webp 400w" sizes="(max-width: 480px) 88vw, 300px" width="300" height="146" alt="Aml-Store.com" decoding="async" fetchpriority="high" />
          <img class="logo-img logo-img--for-dark-bg" src="/img/logo/logo-header-200-light.webp" srcset="/img/logo/logo-header-200-light.webp 200w, /img/logo/logo-header-400-light.webp 400w" sizes="(max-width: 480px) 88vw, 300px" width="300" height="146" alt="" decoding="async" fetchpriority="low" aria-hidden="true" />
        </a>
      </div>
      <div class="header-end">
        <nav class="user-nav" aria-label="Account">
          <a class="user-nav-link user-nav-link--icon" href="/${lang}/cart.html" aria-label="Cart">
            <span class="nav-icon-wrap">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
              <span id="cart-badge" class="cart-badge" hidden></span>
            </span>
          </a>
          <a class="user-nav-link" href="/${lang}/account.html">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <span>Account</span>
          </a>
        </nav>
        <details class="lang-dropdown" translate="no">
          <summary class="lang-dropdown__summary" aria-label="Language">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
            <span class="lang-dropdown__code">${lang.toUpperCase()}</span>
          </summary>
          <div class="lang-dropdown__panel" role="navigation" aria-label="Language">
${langNavFixed}
          </div>
        </details>
        <button id="theme-toggle" type="button" class="theme-toggle" aria-label="Theme">
          <svg class="theme-icon theme-icon--sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
          <svg class="theme-icon theme-icon--moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
      </div>
    </div>
  </header>
  <main id="contenuto" class="main">
    <article class="product-page product-page--storefront" data-product-slug="${escapeHtml(slug)}">
${breadcrumbHtml}

      <section class="product-hero" aria-labelledby="product-title">
        <div class="product-hero__media">
          ${mediaBlock}
        </div>
        <div class="product-hero__buybox">
${dealBannerBlock}          <h1 id="product-title" class="product-title">${escapeHtml(title)}</h1>
          <p class="product-code"><span class="product-code__label">${escapeHtml(u.productCodeLabel)}</span> <code>${escapeHtml(slug)}</code></p>
          <div class="product-price-stack" aria-label="Price">
            <p class="product-price-stack__current">${escapeHtml(priceStr)}</p>
          </div>
          <p class="product-tagline">${escapeHtml(u.productTagline)}</p>
          ${shipBlock}
          <div class="product-actions">
            <button type="button" id="product-add-cart" class="btn btn-primary btn--product-cta">${escapeHtml(u.addCart)}</button>
          </div>
          <div class="product-payments" role="group" aria-labelledby="product-payments-heading">
            <p id="product-payments-heading" class="product-payments__label">${escapeHtml(u.paymentsLabel)}</p>
            <ul class="payments-strip payments-strip--product">
              <li><img src="/img/payments/pay-1.svg" alt="" width="64" height="40" decoding="async" /></li>
              <li><img src="/img/payments/pay-2.svg" alt="" width="64" height="40" decoding="async" /></li>
              <li><img src="/img/payments/pay-3.svg" alt="" width="64" height="40" decoding="async" /></li>
              <li><img src="/img/payments/pay-4.svg" alt="" width="64" height="40" decoding="async" /></li>
            </ul>
          </div>
        </div>
      </section>

      <section class="product-section product-section--kpi" aria-labelledby="product-kpi-heading">
        <h2 id="product-kpi-heading" class="visually-hidden">${escapeHtml(u.kpiSectionAria)}</h2>
        <ul class="product-kpi-list">
${kpiBlock}
        </ul>
      </section>

      <section class="product-section product-section--detail" aria-labelledby="product-detail-heading">
        <h2 id="product-detail-heading" class="product-section__title">${escapeHtml(u.detailSectionTitle)}</h2>
        <div class="product-body lead">${escapeHtml(description)}</div>
      </section>

      <section class="product-section product-section--apps" aria-labelledby="product-apps-heading">
        <h2 id="product-apps-heading" class="product-section__title">${escapeHtml(u.appsTitle)}</h2>
        <ul class="product-apps" role="list">
${appsBlock}
        </ul>
      </section>

      <section class="product-section product-section--specs" aria-labelledby="product-spec-heading">
        <h2 id="product-spec-heading" class="product-section__title">${escapeHtml(u.specTitle)}</h2>
        <dl class="product-spec-dl">
${specRowsHtml}
        </dl>
      </section>

      <section class="product-section product-section--value" aria-labelledby="product-value-heading">
        <h2 id="product-value-heading" class="product-section__title">${escapeHtml(u.advantagesTitle)}</h2>
        <ul class="product-value-grid">
${valueCardsBlock}
        </ul>
      </section>

      <section class="product-section product-section--steps" aria-labelledby="product-steps-heading">
        <h2 id="product-steps-heading" class="product-section__title">${escapeHtml(u.stepsTitle)}</h2>
        <ol class="product-steps" aria-label="${escapeHtml(u.stepsSectionAria)}">
${stepsBlock}
        </ol>
      </section>

      <section class="product-section product-section--trust" aria-labelledby="product-trust-heading">
        <h2 id="product-trust-heading" class="product-section__title">${escapeHtml(u.trustSectionTitle)}</h2>
        <div class="product-trust">
          <a class="product-trust__pill" href="${escapeHtml(u.trustPilotHref)}" target="_blank" rel="noopener noreferrer">${escapeHtml(u.trustPilotLine)}</a>
          <p class="product-trust__note">${escapeHtml(u.trustInvoiceLine)}</p>
        </div>
      </section>

      <section class="product-section product-section--faq" aria-labelledby="product-faq-heading">
        <h2 id="product-faq-heading" class="product-section__title">${escapeHtml(u.faqSectionTitle)}</h2>
        <div class="product-faq">
${faqBlock}
        </div>
      </section>

      <section class="product-section product-section--why-store" aria-labelledby="product-why-heading">
        <h2 id="product-why-heading" class="product-section__title">${escapeHtml(u.whyStoreTitle)}</h2>
        <p class="product-why-lead">${escapeHtml(u.whyStoreLead)}</p>
        <ul class="product-why-grid">
${whyBlock}
        </ul>
      </section>

      <div class="product-sticky-cta" id="product-sticky-cta" inert>
        <div class="product-sticky-cta__inner">
          <p class="product-sticky-cta__price">${escapeHtml(priceStr)}</p>
          <div class="product-sticky-cta__right">
            <button type="button" id="product-add-cart-sticky" class="btn btn-primary product-sticky-cta__btn">${escapeHtml(u.addCart)}</button>
            <a href="/${lang}/#catalog" class="product-sticky-cta__catalog">${escapeHtml(u.stickyContinueShopping)}</a>
          </div>
        </div>
      </div>

      <script type="application/json" id="product-payload">${payloadJson}</script>
    </article>
  </main>
  <footer class="site-footer">
    <div class="inner">
      <p class="footer-legal">Aml Store © è un marchio di Licensoft di Cardelli Antonino. P.Iva 11461870963.</p>
    </div>
  </footer>
</body>
</html>
`;
}

function loadRowsFromD1() {
  const cmd =
    'npx wrangler d1 execute aml-store-d1 --local --file=scripts/sql/select-active-products-for-pages.sql --json';
  const out = execSync(cmd, {
    cwd: ROOT,
    encoding: 'utf-8',
    shell: true,
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  const parsed = JSON.parse(out);
  const first = Array.isArray(parsed) ? parsed[0] : parsed;
  if (!first || !Array.isArray(first.results)) {
    throw new Error('Risposta D1 inattesa: eseguire migrazioni e `npm run db:local` se serve.');
  }
  return /** @type {Record<string, unknown>[]} */ (first.results);
}

/**
 * Rimuove schede obsolete in `/{lang}/products/*.html` (slug non più su D1).
 * @param {Set<string>} activeSlugs slug attivi in minuscolo
 */
function cleanStaleProductPages(activeSlugs) {
  for (const lang of LANGS) {
    const dir = join(ROOT, lang, PRODUCT_PAGES_DIR);
    if (!existsSync(dir)) continue;
    for (const name of readdirSync(dir)) {
      if (!name.endsWith('.html')) continue;
      const lower = name.slice(0, -5).toLowerCase();
      if (!activeSlugs.has(lower)) {
        unlinkSync(join(dir, name));
        console.warn(`Rimosso obsoleto: /${lang}/${PRODUCT_PAGES_DIR}/${name}`);
      }
    }
  }
}

/**
 * Rimuove dalla **root** `/{lang}/` gli HTML con pattern slug-prodotto (schema precedente `/{lang}/{slug}.html`).
 * Non tocca index, cart, checkout, ecc. Aggiungi a RESERVED se aggiungi altre pagine statiche `nome-slug.html`.
 */
function removeProductShapedHtmlFromLangRoot() {
  for (const lang of LANGS) {
    const dir = join(ROOT, lang);
    if (!existsSync(dir)) continue;
    for (const name of readdirSync(dir)) {
      if (!name.endsWith('.html')) continue;
      const base = name.slice(0, -5);
      const lower = base.toLowerCase();
      if (RESERVED_STORE_PRODUCT_SLUGS.has(lower)) continue;
      if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/i.test(base)) continue;
      unlinkSync(join(dir, name));
      console.warn(`Rimosso dalla root lingua (migrazione): /${lang}/${name}`);
    }
  }
}

function removeLegacyProductDirs() {
  for (const lang of LANGS) {
    const legacy = join(ROOT, lang, 'p');
    if (!existsSync(legacy)) continue;
    rmSync(legacy, { recursive: true, force: true });
    console.warn(`Rimossa cartella legacy: /${lang}/p/`);
  }
}

function main() {
  console.info(`SITE_ORIGIN=${SITE_ORIGIN}`);
  const rows = loadRowsFromD1();
  const activeSlugs = new Set(rows.map((r) => String(r.slug ?? '').trim().toLowerCase()));

  cleanStaleProductPages(activeSlugs);
  removeProductShapedHtmlFromLangRoot();

  let n = 0;
  for (const row of rows) {
    const slug = String(row.slug ?? '').trim();
    assertSafeSlug(slug);
    if (isReservedStoreProductSlug(slug)) {
      throw new Error(`Slug prodotto riservato in D1: "${slug}". Aggiorna il record prima di generare.`);
    }
    for (const lang of LANGS) {
      const html = buildPage(row, lang);
      const outDir = join(ROOT, lang, PRODUCT_PAGES_DIR);
      mkdirSync(outDir, { recursive: true });
      const path = join(outDir, `${slug}.html`);
      writeFileSync(path, html, 'utf-8');
      n += 1;
    }
  }
  removeLegacyProductDirs();
  console.info(`Generate product pages: ${rows.length} prodotti × ${LANGS.length} lingue = ${n} file HTML.`);
}

main();
