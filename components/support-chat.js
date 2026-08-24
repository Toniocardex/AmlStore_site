(function () {
    'use strict';

    const COPY = {
        it: { launcher: 'Chat', title: 'Assistenza Aml Store', intro: 'Come possiamo aiutarti?', name: 'Nome (facoltativo)', email: 'Email (facoltativa)', placeholder: 'Scrivi un messaggio…', send: 'Invia', loading: 'Connessione…', offline: 'Chat non disponibile. Scrivici a info@amlstore.it', retry: 'Riconnessione…', error: 'Messaggio non inviato. Riprova.', close: 'Chiudi chat' },
        en: { launcher: 'Chat', title: 'Aml Store support', intro: 'How can we help?', name: 'Name (optional)', email: 'Email (optional)', placeholder: 'Write a message…', send: 'Send', loading: 'Connecting…', offline: 'Chat unavailable. Email info@amlstore.it', retry: 'Reconnecting…', error: 'Message not sent. Please retry.', close: 'Close chat' },
        fr: { launcher: 'Chat', title: 'Assistance Aml Store', intro: 'Comment pouvons-nous vous aider ?', name: 'Nom (facultatif)', email: 'E-mail (facultatif)', placeholder: 'Écrivez un message…', send: 'Envoyer', loading: 'Connexion…', offline: 'Chat indisponible. Écrivez à info@amlstore.it', retry: 'Reconnexion…', error: 'Message non envoyé. Réessayez.', close: 'Fermer le chat' },
        de: { launcher: 'Chat', title: 'Aml Store Support', intro: 'Wie können wir helfen?', name: 'Name (optional)', email: 'E-Mail (optional)', placeholder: 'Nachricht schreiben…', send: 'Senden', loading: 'Verbindung…', offline: 'Chat nicht verfügbar. E-Mail: info@amlstore.it', retry: 'Verbindung wird wiederhergestellt…', error: 'Nachricht nicht gesendet. Erneut versuchen.', close: 'Chat schließen' },
        es: { launcher: 'Chat', title: 'Soporte Aml Store', intro: '¿Cómo podemos ayudarte?', name: 'Nombre (opcional)', email: 'Email (opcional)', placeholder: 'Escribe un mensaje…', send: 'Enviar', loading: 'Conectando…', offline: 'Chat no disponible. Escribe a info@amlstore.it', retry: 'Reconectando…', error: 'Mensaje no enviado. Inténtalo de nuevo.', close: 'Cerrar chat' },
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
            document.addEventListener('visibilitychange', () => {
                if (!document.hidden && this.conversationId && (!this.socket || this.socket.readyState > 1)) {
                    this.connectSocket();
                }
            });
            window.addEventListener('aml-support-open', () => this.open());
        }

        render() {
            this.shadowRoot.innerHTML = `<style>
                :host{font-family:Montserrat,system-ui,sans-serif;color:#172033;position:fixed;right:20px;bottom:20px;z-index:2147482000}
                *{box-sizing:border-box}.launcher{border:0;border-radius:999px;background:#176b5b;color:#fff;font:700 14px inherit;padding:13px 19px;box-shadow:0 8px 28px #112a2440;cursor:pointer}.launcher:focus-visible,.close:focus-visible,button:focus-visible,textarea:focus-visible,input:focus-visible{outline:3px solid #edb84b;outline-offset:2px}
                .panel{position:absolute;right:0;bottom:58px;width:min(380px,calc(100vw - 24px));height:min(620px,calc(100vh - 100px));background:#fff;border:1px solid #dbe2e8;border-radius:18px;box-shadow:0 18px 60px #14211e38;display:grid;grid-template-rows:auto auto 1fr auto;overflow:hidden}.panel[hidden]{display:none}
                header{display:flex;align-items:center;gap:10px;padding:15px 16px;background:#123d37;color:#fff}header strong{flex:1;font-size:15px}.state{font-size:11px;opacity:.8}.close{border:0;background:transparent;color:#fff;font-size:22px;cursor:pointer}
                .notice{margin:0;padding:9px 14px;background:#f4f7f6;color:#44534f;font-size:12px}.messages{overflow:auto;padding:14px;display:flex;flex-direction:column;gap:9px;overscroll-behavior:contain}.empty{text-align:center;margin:auto;color:#5c6966;font-size:14px}.message{max-width:84%;padding:10px 12px;border-radius:14px;background:#edf2f1;white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px;line-height:1.4}.message.visitor{align-self:flex-end;background:#176b5b;color:#fff}.message.operator{align-self:flex-start}.message small{display:block;margin-top:4px;opacity:.65;font-size:10px}
                form{border-top:1px solid #e1e6e5;padding:10px;background:#fff}.contact{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:7px}.contact[hidden]{display:none}input,textarea{width:100%;border:1px solid #cbd5d2;border-radius:9px;padding:9px;font:13px inherit;color:inherit}textarea{resize:none;min-height:64px;max-height:120px}.sendrow{display:flex;align-items:end;gap:8px}.sendrow button{border:0;border-radius:9px;background:#176b5b;color:#fff;font:700 13px inherit;padding:11px 14px;cursor:pointer}.sendrow button:disabled{opacity:.55;cursor:wait}
                @media(max-width:520px){:host{right:12px;bottom:12px}.panel{position:fixed;inset:0;width:100vw;height:100dvh;border:0;border-radius:0}.contact{grid-template-columns:1fr}}
                @media(prefers-reduced-motion:no-preference){.panel{animation:open .16s ease-out}@keyframes open{from{opacity:0;transform:translateY(8px)}}}
            </style><button class="launcher" type="button" aria-haspopup="dialog">${this.t.launcher}</button><section class="panel" role="dialog" aria-label="${this.t.title}" hidden><header><strong>${this.t.title}</strong><span class="state">OFFLINE</span><button class="close" type="button" aria-label="${this.t.close}">×</button></header><p class="notice">${this.t.intro}</p><div class="messages" aria-live="polite"><p class="empty">${this.t.intro}</p></div><form><div class="contact"><input name="name" maxlength="100" autocomplete="name" placeholder="${this.t.name}"><input name="email" maxlength="254" type="email" autocomplete="email" placeholder="${this.t.email}"></div><div class="sendrow"><textarea maxlength="4000" required placeholder="${this.t.placeholder}"></textarea><button type="submit">${this.t.send}</button></div></form></section>`;
        }

        async open() {
            const panel = this.shadowRoot.querySelector('.panel');
            panel.hidden = false;
            this.shadowRoot.querySelector('.launcher').hidden = true;
            this.shadowRoot.querySelector('textarea').focus();
            if (this.initialized) return;
            this.initialized = true;
            this.setState('CONNECTING', this.t.loading);
            try {
                await this.api('/api/chat/session', { method: 'POST', body: {} });
                const data = await this.api('/api/chat/conversations');
                const latest = (data.conversations || [])[0];
                if (latest) {
                    this.conversationId = latest.id;
                    this.lastSeq = Number(latest.lastSeq || 0);
                    await this.loadHistory();
                    this.connectSocket();
                } else {
                    this.setState('OFFLINE', this.t.intro);
                }
            } catch (_) {
                this.setState('ERROR', this.t.offline);
            }
        }

        close() {
            this.shadowRoot.querySelector('.panel').hidden = true;
            this.shadowRoot.querySelector('.launcher').hidden = false;
            this.shadowRoot.querySelector('.launcher').focus();
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

        setState(state, notice) {
            this.shadowRoot.querySelector('.state').textContent = state;
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
                this.setState(this.socket?.readyState === 1 ? 'ONLINE' : 'OFFLINE', this.t.intro);
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
            socket.addEventListener('open', () => { this.reconnectAttempt = 0; this.setState('ONLINE', this.t.intro); });
            socket.addEventListener('message', (event) => {
                let data;
                try { data = JSON.parse(event.data); } catch (_) { return; }
                if (data.type === 'message.created') {
                    const clientId = data.payload?.clientMessageId;
                    const wait = clientId && this.pending.get(clientId);
                    if (wait) { clearTimeout(wait.timer); this.pending.delete(clientId); wait.resolve(data); }
                    this.addMessage({ seq: data.seq, messageId: data.payload?.messageId, clientMessageId: clientId, senderType: data.payload?.senderType, body: data.payload?.body, createdAt: data.serverTs });
                }
                if (data.type === 'conversation.reopened') this.setState('ONLINE', this.t.intro);
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
