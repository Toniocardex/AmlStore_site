(function () {
    'use strict';

    const COPY = {
        it: { launcher: 'Chat', title: 'Assistenza Aml Store', intro: 'Come possiamo aiutarti?', name: 'Nome', email: 'Email', placeholder: 'Scrivi un messaggio…', sendHint: 'Premi Invio per inviare, Maiuscolo+Invio per andare a capo.', send: 'Invia', loading: 'Connessione…', offline: 'Chat non disponibile. Scrivici a info@amlstore.it', retry: 'Riconnessione…', error: 'Messaggio non inviato. Riprova.', close: 'Chiudi chat', open: 'Apri la chat di assistenza', stOnline: 'Online', stOffline: 'Offline', stConnecting: 'Connessione…', stReconnecting: 'Riconnessione…', stError: 'Non disponibile', noticeOnline: 'Assistenza online. Di solito rispondiamo in pochi minuti.', noticeOffline: 'Siamo offline. Lascia nome, email e un messaggio: ti ricontattiamo appena possibile.' },
        en: { launcher: 'Chat', title: 'Aml Store support', intro: 'How can we help?', name: 'Name', email: 'Email', placeholder: 'Write a message…', sendHint: 'Press Enter to send, Shift+Enter for a new line.', send: 'Send', loading: 'Connecting…', offline: 'Chat unavailable. Email info@amlstore.it', retry: 'Reconnecting…', error: 'Message not sent. Please retry.', close: 'Close chat', open: 'Open the support chat', stOnline: 'Online', stOffline: 'Offline', stConnecting: 'Connecting…', stReconnecting: 'Reconnecting…', stError: 'Unavailable', noticeOnline: 'Support is online. We usually reply within minutes.', noticeOffline: 'We are offline. Leave your name, email and a message: we will get back to you.' },
        fr: { launcher: 'Chat', title: 'Assistance Aml Store', intro: 'Comment pouvons-nous vous aider ?', name: 'Nom', email: 'E-mail', placeholder: 'Écrivez un message…', sendHint: 'Appuyez sur Entrée pour envoyer, Maj+Entrée pour un retour à la ligne.', send: 'Envoyer', loading: 'Connexion…', offline: 'Chat indisponible. Écrivez à info@amlstore.it', retry: 'Reconnexion…', error: 'Message non envoyé. Réessayez.', close: 'Fermer le chat', open: 'Ouvrir le chat d’assistance', stOnline: 'En ligne', stOffline: 'Hors ligne', stConnecting: 'Connexion…', stReconnecting: 'Reconnexion…', stError: 'Indisponible', noticeOnline: 'Assistance en ligne. Nous répondons en quelques minutes.', noticeOffline: 'Nous sommes hors ligne. Laissez nom, e-mail et un message : nous vous recontacterons.' },
        de: { launcher: 'Chat', title: 'Aml Store Support', intro: 'Wie können wir helfen?', name: 'Name', email: 'E-Mail', placeholder: 'Nachricht schreiben…', sendHint: 'Eingabetaste zum Senden, Umschalt+Eingabetaste für einen Zeilenumbruch.', send: 'Senden', loading: 'Verbindung…', offline: 'Chat nicht verfügbar. E-Mail: info@amlstore.it', retry: 'Verbindung wird wiederhergestellt…', error: 'Nachricht nicht gesendet. Erneut versuchen.', close: 'Chat schließen', open: 'Support-Chat öffnen', stOnline: 'Online', stOffline: 'Offline', stConnecting: 'Verbindung…', stReconnecting: 'Neuverbindung…', stError: 'Nicht verfügbar', noticeOnline: 'Support ist online. Wir antworten meist in wenigen Minuten.', noticeOffline: 'Wir sind offline. Hinterlassen Sie Name, E-Mail und eine Nachricht, wir melden uns.' },
        es: { launcher: 'Chat', title: 'Soporte Aml Store', intro: '¿Cómo podemos ayudarte?', name: 'Nombre', email: 'Email', placeholder: 'Escribe un mensaje…', sendHint: 'Pulsa Intro para enviar, Mayús+Intro para un salto de línea.', send: 'Enviar', loading: 'Conectando…', offline: 'Chat no disponible. Escribe a info@amlstore.it', retry: 'Reconectando…', error: 'Mensaje no enviado. Inténtalo de nuevo.', close: 'Cerrar chat', open: 'Abrir el chat de soporte', stOnline: 'En línea', stOffline: 'Sin conexión', stConnecting: 'Conectando…', stReconnecting: 'Reconectando…', stError: 'No disponible', noticeOnline: 'Soporte en línea. Solemos responder en pocos minutos.', noticeOffline: 'Estamos sin conexión. Deja tu nombre, email y un mensaje: te responderemos.' },
    };

    const id = (prefix) => prefix + '_' + crypto.randomUUID();
    const locale = () => {
        const lang = String(document.documentElement.lang || 'it').toLowerCase().split('-')[0];
        return COPY[lang] ? lang : 'it';
    };

    class SupportChat extends HTMLElement {
        constructor() {
            super();
            this.attachShadow({ mode: 'open' });
            this.localeCode = locale();
            this.t = COPY[this.localeCode];
            this.conversationId = null;
            this.lastSeq = 0;
            this.socket = null;
            this.events = new Set();
            this.pending = new Map();
            this.reconnectAttempt = 0;
            this.initialized = false;
            this.availability = 'OFFLINE';
            this.render();
        }

        connectedCallback() {
            this.shadowRoot.querySelector('.launcher').addEventListener('click', () => this.open());
            this.shadowRoot.querySelector('.close').addEventListener('click', () => this.close());
            this.shadowRoot.querySelector('form').addEventListener('submit', (event) => this.submit(event));
            const input = this.shadowRoot.querySelector('textarea');
            const draftKey = 'aml-support-draft:' + this.localeCode;
            try { input.value = localStorage.getItem(draftKey) || ''; } catch (_) { /* storage optional */ }
            input.addEventListener('input', () => {
                try { localStorage.setItem(draftKey, input.value); } catch (_) { /* storage optional */ }
            });
            // Invio invia il messaggio, Maiuscolo+Invio va a capo (come nei client di
            // chat piu' comuni). isComposing esclude la conferma di un candidato IME
            // (cinese/giapponese/coreano), che non deve inviare il messaggio.
            input.addEventListener('keydown', (event) => {
                if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
                    event.preventDefault();
                    this.shadowRoot.querySelector('form').requestSubmit();
                }
            });
            document.addEventListener('visibilitychange', () => {
                if (!document.hidden && this.conversationId && (!this.socket || this.socket.readyState > 1)) {
                    this.connectSocket();
                }
            });
            window.addEventListener('aml-support-open', () => this.open());
            this.shadowRoot.addEventListener('keydown', (event) => {
                const panel = this.shadowRoot.querySelector('.panel');
                if (panel.hidden) return;
                if (event.key === 'Escape') { this.close(); return; }
                if (event.key === 'Tab') this.trapFocus(event, panel);
            });
            this.watchConsentBanner();
        }

        // Il pannello e' un dialog ARIA, non un <dialog> nativo: il browser non
        // intrappola da solo il focus dentro, quindi Tab dall'ultimo elemento
        // (Invia) uscirebbe sul resto della pagina dietro al widget.
        trapFocus(event, panel) {
            const focusable = Array.from(panel.querySelectorAll('button, input, textarea'))
                .filter((el) => !el.disabled && el.offsetParent !== null);
            if (!focusable.length) return;
            const first = focusable[0];
            const last = focusable[focusable.length - 1];
            const active = this.shadowRoot.activeElement;
            if (event.shiftKey && active === first) {
                event.preventDefault();
                last.focus();
            } else if (!event.shiftKey && active === last) {
                event.preventDefault();
                first.focus();
            }
        }

        /* Il banner cookie e' fixed in basso e copre l'angolo del launcher: finche'
           il consenso e' aperto il launcher si ritira, altrimenti su mobile finirebbe
           sopra i pulsanti "Accetta"/"Rifiuta". */
        watchConsentBanner() {
            const banner = document.querySelector('aml-cookie-banner');
            if (!banner) return;
            const sync = () => {
                this.toggleAttribute('data-consent-open', !banner.hasAttribute('hidden'));
            };
            sync();
            new MutationObserver(sync).observe(banner, { attributes: true, attributeFilter: ['hidden'] });
            if (banner.shadowRoot) new MutationObserver(sync).observe(banner.shadowRoot, { childList: true });
            window.addEventListener('load', sync, { once: true });
        }

        render() {
            const bubbleIcon = '<svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" '
                + 'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
                + '<path d="M20.5 11.6a8.2 8.2 0 0 1-8.8 8.2 8.7 8.7 0 0 1-3.6-.9L3.5 20.5l1.6-4.6a8.2 8.2 0 0 1-.9-3.7 8.2 8.2 0 0 1 8.2-8.2h.5a8.2 8.2 0 0 1 7.6 7.6z"/></svg>';
            this.shadowRoot.innerHTML = `<style>
                /* Il widget e' chrome di assistenza, non una CTA d'acquisto: per la regola
                   dei tre ruoli del design system usa la superficie slate/navy e lascia
                   l'arancione alla sola azione primaria interna (Invia). Ogni token ha un
                   fallback perche' lo shadow DOM puo' finire su pagine senza css/page.css. */
                :host{
                    --sc-ink: var(--aml-slate-900, #0F172A);
                    --sc-ink-soft: var(--aml-slate-800, #1E293B);
                    --sc-muted: var(--aml-slate-600, #475569);
                    --sc-line: var(--aml-line, #E2E8F0);
                    --sc-surface: var(--aml-surface, #FFFFFF);
                    --sc-paper: var(--aml-paper-2, #F8FAFC);
                    --sc-cta: var(--aml-cta-bg, #EA580C);
                    --sc-cta-hover: var(--aml-cta-bg-hover, #F97316);
                    font-family: var(--aml-font-sans, 'Montserrat', system-ui, sans-serif);
                    font-size: 16px;
                    color: var(--sc-ink);
                    position: fixed;
                    right: clamp(12px, 2.5vw, 20px);
                    bottom: calc(clamp(12px, 2.5vw, 20px) + env(safe-area-inset-bottom, 0px));
                    /* Sotto aml-cookie-banner (10050): il consenso deve restare cliccabile. */
                    z-index: 10040;
                }
                *{box-sizing:border-box}
                button,input,textarea{font:inherit;color:inherit}
                :focus-visible{outline:3px solid var(--sc-cta);outline-offset:2px}

                /* ── Launcher ───────────────────────────────────────────────── */
                .launcher{
                    display:inline-flex;align-items:center;gap:9px;
                    height:52px;padding:0 20px 0 17px;
                    border:0;border-radius:999px;
                    background:var(--sc-ink);color:#fff;
                    font-size:15px;font-weight:700;letter-spacing:-0.01em;
                    cursor:pointer;
                    /* Il footer del sito e' esattamente --aml-slate-900, cioe' lo stesso
                       colore del launcher: li' il contorno e' l'unica cosa che separa il
                       pulsante dallo sfondo. A .42 su quel fondo il bordo misura 4,06:1,
                       sopra il 3:1 richiesto da WCAG 1.4.11 per i componenti UI. Su
                       pagina chiara il ring bianco sparisce e a separare resta il fill
                       navy (17,85:1), quindi un solo valore copre entrambi i casi. */
                    box-shadow:0 10px 28px rgba(15,23,42,.28),0 0 0 2px rgba(255,255,255,.42);
                    transition:transform .18s ease,box-shadow .18s ease,background .18s ease,opacity .18s ease;
                }
                .launcher:hover{background:var(--sc-ink-soft);transform:translateY(-2px);box-shadow:0 16px 36px rgba(15,23,42,.34),0 0 0 2px rgba(255,255,255,.55)}
                .launcher:active{transform:translateY(0)}
                .launcher[hidden]{display:none}
                /* Solo opacity/visibility: una transizione su transform lasciata a meta'
                   (tab in background, compositor fermo) inchioderebbe il launcher
                   fuori posizione. Il transform resta al solo hover, dove e' innocuo. */
                :host([data-consent-open]) .launcher{opacity:0;visibility:hidden;pointer-events:none}

                /* ── Pannello ───────────────────────────────────────────────── */
                .panel{
                    position:absolute;right:0;bottom:64px;
                    width:min(384px,calc(100vw - 24px));
                    height:min(600px,calc(100dvh - 120px));
                    background:var(--sc-surface);
                    border:1px solid var(--sc-line);border-radius:16px;
                    box-shadow:0 24px 64px rgba(15,23,42,.22);
                    display:grid;grid-template-rows:auto auto 1fr auto;
                    overflow:hidden;
                }
                .panel[hidden]{display:none}
                header{display:flex;align-items:center;gap:11px;padding:13px 12px 13px 16px;background:var(--sc-ink);color:#fff}
                .avatar{flex:none;width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.13);display:grid;place-items:center}
                .head-text{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
                .head-text strong{font-size:14px;font-weight:700;letter-spacing:-0.01em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
                .state{display:flex;align-items:center;gap:6px;font-size:11.5px;color:rgba(255,255,255,.74)}
                .state i{flex:none;width:7px;height:7px;border-radius:50%;background:#94A3B8}
                .panel[data-state=ONLINE] .state i{background:#34D399;box-shadow:0 0 0 3px rgba(52,211,153,.2)}
                .panel[data-state=CONNECTING] .state i,
                .panel[data-state=RECONNECTING] .state i{background:var(--aml-amber-400,#FBBF24)}
                .panel[data-state=ERROR] .state i{background:#F87171}
                .close{flex:none;width:40px;height:40px;display:grid;place-items:center;border:0;border-radius:10px;background:transparent;color:#fff;cursor:pointer;transition:background .15s ease}
                .close:hover{background:rgba(255,255,255,.14)}
                .notice{margin:0;padding:10px 16px;background:var(--sc-paper);border-bottom:1px solid var(--sc-line);color:var(--sc-muted);font-size:12.5px;line-height:1.45}

                /* ── Messaggi ───────────────────────────────────────────────── */
                .messages{overflow:auto;padding:16px 14px;display:flex;flex-direction:column;gap:10px;background:var(--sc-paper);overscroll-behavior:contain}
                .empty{margin:auto;max-width:26ch;text-align:center;color:var(--sc-muted);font-size:13.5px;line-height:1.5}
                .message{
                    max-width:85%;padding:10px 13px;border-radius:14px;
                    background:var(--sc-surface);border:1px solid var(--sc-line);
                    font-size:14px;line-height:1.45;
                    white-space:pre-wrap;overflow-wrap:anywhere;
                    box-shadow:0 1px 2px rgba(15,23,42,.04);
                }
                .message.operator{align-self:flex-start;border-bottom-left-radius:5px}
                .message.visitor{align-self:flex-end;background:var(--sc-ink);border-color:var(--sc-ink);color:#fff;border-bottom-right-radius:5px}
                /* Orari a colore pieno invece che in opacity: a 11px l'alpha faceva
                   scendere il contrasto sotto la soglia AA. */
                .message small{display:block;margin-top:5px;font-size:11px;color:var(--sc-muted)}
                .message.visitor small{color:rgba(255,255,255,.78)}

                /* ── Form ───────────────────────────────────────────────────── */
                form{border-top:1px solid var(--sc-line);padding:12px;background:var(--sc-surface)}
                .contact{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px}
                .contact[hidden]{display:none}
                input,textarea{width:100%;border:1px solid var(--sc-line);border-radius:10px;padding:10px 12px;font-size:14px;background:var(--sc-surface);transition:border-color .15s ease}
                input::placeholder,textarea::placeholder{color:var(--sc-muted);opacity:1}
                input:hover,textarea:hover{border-color:var(--aml-slate-300,#CBD5E1)}
                input:focus,textarea:focus{border-color:var(--sc-ink)}
                textarea{resize:none;min-height:66px;max-height:132px;line-height:1.45}
                .sendrow{display:flex;align-items:flex-end;gap:8px}
                .sendrow button{
                    flex:none;display:inline-flex;align-items:center;gap:7px;
                    height:44px;padding:0 16px;border:0;border-radius:10px;
                    background:var(--sc-cta);color:#fff;
                    font-size:14px;font-weight:800;cursor:pointer;
                    transition:background .15s ease;
                }
                .sendrow button:hover:not(:disabled){background:var(--sc-cta-hover)}
                .sendrow button:disabled{opacity:.55;cursor:wait}

                /* ── Schermi stretti: il pannello diventa una sheet a tutto schermo ── */
                @media(max-width:560px){
                    .panel{position:fixed;inset:0;width:100%;height:100dvh;max-height:none;border:0;border-radius:0}
                    header{padding-top:calc(13px + env(safe-area-inset-top,0px))}
                    form{padding-bottom:calc(12px + env(safe-area-inset-bottom,0px))}
                    .contact{grid-template-columns:1fr}
                    .message{max-width:90%}
                }
                /* Sotto i 360px l'etichetta occuperebbe una fetta reale di viewport:
                   resta l'icona, il nome accessibile arriva da aria-label. */
                @media(max-width:359px){
                    .launcher{width:52px;padding:0;justify-content:center;gap:0}
                    .launcher-label{display:none}
                }
                /* Telefono in orizzontale: niente pannello piu' alto della finestra. */
                @media(max-height:460px) and (min-width:561px){
                    .panel{height:calc(100dvh - 88px);bottom:60px}
                    textarea{min-height:48px}
                }
                @media(prefers-reduced-motion:no-preference){
                    .panel{animation:sc-in .18s ease-out}
                    @keyframes sc-in{from{opacity:0;transform:translateY(10px) scale(.99)}}
                }
                @media(prefers-reduced-motion:reduce){
                    .launcher,.close,.sendrow button,input,textarea{transition:none}
                }
                .sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
            </style><button class="launcher" type="button" aria-haspopup="dialog" aria-expanded="false" aria-label="${this.t.open}">${bubbleIcon}<span class="launcher-label">${this.t.launcher}</span></button><section class="panel" role="dialog" aria-modal="true" aria-label="${this.t.title}" hidden><header><span class="avatar" aria-hidden="true">${bubbleIcon}</span><span class="head-text"><strong>${this.t.title}</strong><span class="state" role="status" aria-atomic="true"><i aria-hidden="true"></i><span class="state-label">${this.t.stOffline}</span></span></span><button class="close" type="button" aria-label="${this.t.close}"><svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18"/></svg></button></header><p class="notice" role="status" aria-atomic="true">${this.t.intro}</p><div class="messages" role="log" aria-live="polite"><p class="empty">${this.t.intro}</p></div><form><div class="contact"><label class="sr-only" for="sc-name">${this.t.name}</label><input id="sc-name" name="name" maxlength="100" autocomplete="name" placeholder="${this.t.name}"><label class="sr-only" for="sc-email">${this.t.email}</label><input id="sc-email" name="email" maxlength="254" type="email" autocomplete="email" placeholder="${this.t.email}"></div><div class="sendrow"><label class="sr-only" for="sc-body">${this.t.placeholder}</label><textarea id="sc-body" maxlength="4000" required placeholder="${this.t.placeholder}" aria-describedby="sc-send-hint"></textarea><span id="sc-send-hint" class="sr-only">${this.t.sendHint}</span><button type="submit"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M21.5 2.5L11 13M21.5 2.5l-6.8 19-3.7-8.5L2.5 9.3z"/></svg>${this.t.send}</button></div></form></section>`;
        }

        async open() {
            const panel = this.shadowRoot.querySelector('.panel');
            const launcher = this.shadowRoot.querySelector('.launcher');
            panel.hidden = false;
            launcher.hidden = true;
            launcher.setAttribute('aria-expanded', 'true');
            this.shadowRoot.querySelector('textarea').focus();
            if (this.initialized) {
                // Il listener 'close' della socket smette di ritentare mentre il
                // pannello e' hidden (per non tenere una connessione aperta a vuoto),
                // quindi riaprire non riprendeva mai la riconnessione da solo: restava
                // "OFFLINE"/stantio finche' non arrivava un visibilitychange casuale
                // della TAB, che e' un evento diverso dal riaprire il pannello.
                if (this.conversationId && (!this.socket || this.socket.readyState > 1)) {
                    this.reconnectAttempt = 0;
                    this.connectSocket();
                }
                return;
            }
            this.initialized = true;
            this.setState('CONNECTING', this.t.loading);
            try {
                await this.api('/api/chat/session', { method: 'POST', body: {} });
                /* Disponibilita' pubblica del supporto: e' un dato diverso dallo stato
                   della socket (ADR §45), ed e' quello che il badge deve mostrare. */
                const status = await this.api('/api/chat/availability').catch(() => null);
                this.availability = status && status.availability === 'ONLINE' ? 'ONLINE' : 'OFFLINE';
                this.updateContactRequirement();
                const data = await this.api('/api/chat/conversations');
                const latest = (data.conversations || [])[0];
                if (latest) {
                    this.conversationId = latest.id;
                    this.lastSeq = Number(latest.lastSeq || 0);
                    // Nome/email hanno senso solo per il primo messaggio: una
                    // conversazione gia' esistente ha gia' un'identita' associata.
                    this.shadowRoot.querySelector('.contact').hidden = true;
                    await this.loadHistory();
                    this.connectSocket();
                } else {
                    this.setState(this.availability, this.availabilityNotice());
                }
            } catch (_) {
                this.setState('ERROR', this.t.offline);
            }
        }

        close() {
            const launcher = this.shadowRoot.querySelector('.launcher');
            this.shadowRoot.querySelector('.panel').hidden = true;
            launcher.hidden = false;
            launcher.setAttribute('aria-expanded', 'false');
            launcher.focus();
        }

        async api(path, options) {
            const init = Object.assign({ credentials: 'same-origin', headers: {} }, options || {});
            if (Object.prototype.hasOwnProperty.call(init, 'body')) {
                init.headers['Content-Type'] = 'application/json';
                init.body = JSON.stringify(init.body);
            }
            const response = await fetch(path, init);
            const data = await response.json().catch(() => ({}));
            if (!response.ok) throw Object.assign(new Error(data.error?.message || 'HTTP ' + response.status), { data, status: response.status });
            return data;
        }

        async loadHistory() {
            const data = await this.api('/api/chat/conversations/' + encodeURIComponent(this.conversationId) + '/messages?limit=100');
            this.shadowRoot.querySelector('.messages').textContent = '';
            (data.messages || []).forEach((message) => this.addMessage(message));
        }

        addMessage(message) {
            const key = message.messageId || message.clientMessageId;
            if (key && this.events.has(key)) return;
            if (key) this.events.add(key);
            this.lastSeq = Math.max(this.lastSeq, Number(message.seq || 0));
            const list = this.shadowRoot.querySelector('.messages');
            list.querySelector('.empty')?.remove();
            const item = document.createElement('div');
            item.className = 'message ' + (message.senderType === 'operator' ? 'operator' : 'visitor');
            const body = document.createElement('span');
            body.textContent = String(message.body || '');
            const time = document.createElement('small');
            time.textContent = new Date(Number(message.createdAt || Date.now())).toLocaleTimeString(this.localeCode, { hour: '2-digit', minute: '2-digit' });
            item.append(body, time);
            list.appendChild(item);
            list.scrollTop = list.scrollHeight;
        }

        availabilityNotice() {
            return this.availability === 'ONLINE' ? this.t.noticeOnline : this.t.noticeOffline;
        }

        // Offline nessuno legge il messaggio in tempo reale: senza un modo per
        // ricontattarlo il primo messaggio del visitatore rischia di restare senza
        // risposta. Online la richiesta resta facoltativa, la conversazione prosegue
        // gia' in chat. L'asterisco (non una frase tra parentesi) segnala
        // l'obbligatorieta': i campi sono a meta' larghezza del pannello e un testo
        // esplicativo tradotto in 5 lingue ci finiva tagliato (es. "Email (per
        // ricontattarti)"). Il "perche'" resta comunque nel .notice sopra al form.
        updateContactRequirement() {
            const offline = this.availability === 'OFFLINE';
            const nameInput = this.shadowRoot.querySelector('#sc-name');
            const emailInput = this.shadowRoot.querySelector('#sc-email');
            const nameLabel = this.shadowRoot.querySelector('label[for="sc-name"]');
            const emailLabel = this.shadowRoot.querySelector('label[for="sc-email"]');
            const nameText = offline ? this.t.name + ' *' : this.t.name;
            const emailText = offline ? this.t.email + ' *' : this.t.email;
            nameInput.required = offline;
            emailInput.required = offline;
            nameInput.placeholder = nameText;
            emailInput.placeholder = emailText;
            nameLabel.textContent = nameText;
            emailLabel.textContent = emailText;
        }

        setState(state, notice) {
            const labels = {
                ONLINE: this.t.stOnline,
                OFFLINE: this.t.stOffline,
                CONNECTING: this.t.stConnecting,
                RECONNECTING: this.t.stReconnecting,
                ERROR: this.t.stError,
            };
            this.shadowRoot.querySelector('.panel').dataset.state = state;
            this.shadowRoot.querySelector('.state-label').textContent = labels[state] || labels.OFFLINE;
            if (notice) this.shadowRoot.querySelector('.notice').textContent = notice;
        }

        async submit(event) {
            event.preventDefault();
            const textarea = this.shadowRoot.querySelector('textarea');
            const button = this.shadowRoot.querySelector('.sendrow button');
            const body = textarea.value.trim();
            if (!body || button.disabled) return;
            const clientMessageId = id('msg');
            button.disabled = true;
            try {
                let result;
                if (!this.conversationId) {
                    const name = this.shadowRoot.querySelector('[name=name]').value.trim();
                    const email = this.shadowRoot.querySelector('[name=email]').value.trim();
                    result = await this.api('/api/chat/conversations', { method: 'POST', body: {
                        clientMessageId, body, locale: this.localeCode,
                        pagePath: location.pathname,
                        productId: document.body.dataset.productId || null,
                        contact: { name: name || null, email: email || null },
                    } });
                    this.conversationId = result.conversationId;
                    this.shadowRoot.querySelector('.contact').hidden = true;
                    this.connectSocket();
                } else {
                    result = await this.sendExisting(clientMessageId, body);
                }
                this.addMessage({
                    seq: result.seq,
                    messageId: result.payload?.messageId,
                    clientMessageId,
                    senderType: 'visitor', body, createdAt: result.serverTs,
                });
                textarea.value = '';
                try { localStorage.removeItem('aml-support-draft:' + this.localeCode); } catch (_) { /* optional */ }
                this.setState(this.availability, this.availabilityNotice());
            } catch (_) {
                this.setState('ERROR', this.t.error);
            } finally {
                button.disabled = false;
                textarea.focus();
            }
        }

        sendExisting(clientMessageId, body) {
            if (!this.socket || this.socket.readyState !== 1) {
                return this.api('/api/chat/conversations/' + encodeURIComponent(this.conversationId) + '/messages', {
                    method: 'POST', body: { clientMessageId, body },
                });
            }
            const requestId = id('req');
            return new Promise((resolve, reject) => {
                const timer = setTimeout(() => {
                    this.pending.delete(clientMessageId);
                    this.api('/api/chat/conversations/' + encodeURIComponent(this.conversationId) + '/messages', {
                        method: 'POST', body: { clientMessageId, body },
                    }).then(resolve, reject);
                }, 5000);
                this.pending.set(clientMessageId, { resolve, reject, timer });
                this.socket.send(JSON.stringify({ v: 1, type: 'message.send', requestId, conversationId: this.conversationId, payload: { clientMessageId, body } }));
            });
        }

        connectSocket() {
            if (!this.conversationId || this.socket?.readyState === 1) return;
            const scheme = location.protocol === 'https:' ? 'wss:' : 'ws:';
            this.setState('CONNECTING', this.reconnectAttempt ? this.t.retry : this.t.loading);
            const socket = new WebSocket(scheme + '//' + location.host + '/api/chat/conversations/' + encodeURIComponent(this.conversationId) + '/ws?lastKnownSeq=' + this.lastSeq);
            this.socket = socket;
            socket.addEventListener('open', () => {
                this.reconnectAttempt = 0;
                this.setState(this.availability, this.availabilityNotice());
            });
            socket.addEventListener('message', (event) => {
                let data;
                try { data = JSON.parse(event.data); } catch (_) { return; }
                if (data.type === 'message.created') {
                    const clientId = data.payload?.clientMessageId;
                    const wait = clientId && this.pending.get(clientId);
                    if (wait) { clearTimeout(wait.timer); this.pending.delete(clientId); wait.resolve(data); }
                    this.addMessage({ seq: data.seq, messageId: data.payload?.messageId, clientMessageId: clientId, senderType: data.payload?.senderType, body: data.payload?.body, createdAt: data.serverTs });
                }
                if (data.type === 'conversation.reopened') this.setState(this.availability, this.availabilityNotice());
            });
            socket.addEventListener('close', () => {
                if (this.shadowRoot.querySelector('.panel').hidden) return;
                this.setState('RECONNECTING', this.t.retry);
                const delay = Math.min(30000, 750 * Math.pow(2, this.reconnectAttempt++)) * (0.8 + Math.random() * 0.4);
                setTimeout(() => this.connectSocket(), delay);
            });
            socket.addEventListener('error', () => socket.close());
        }
    }

    if (!customElements.get('support-chat')) customElements.define('support-chat', SupportChat);
})();
