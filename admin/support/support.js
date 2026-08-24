(function () {
    'use strict';

    const state = { conversations: [], selected: null, detail: null, cursor: null, operator: null, preferences: null, profile: null, socket: null, reconnect: 0, unreadCount: 0 };
    const $ = (id) => document.getElementById(id);
    const shell = document.querySelector('.sup-shell');
    let installPrompt = null;

    function toast(message) {
        const node = $('sup-toast');
        node.textContent = message;
        node.classList.add('show');
        clearTimeout(toast.timer);
        toast.timer = setTimeout(() => node.classList.remove('show'), 3000);
    }

    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => navigator.serviceWorker.register('/admin/sw.js', { scope: '/admin/' })
            .catch(() => toast('Service Worker non disponibile.')));
    }
    window.addEventListener('beforeinstallprompt', (event) => {
        event.preventDefault(); installPrompt = event; $('install-app').hidden = false;
    });
    $('install-app').addEventListener('click', async () => {
        if (!installPrompt) return;
        installPrompt.prompt();
        await installPrompt.userChoice;
        installPrompt = null; $('install-app').hidden = true;
    });
    window.addEventListener('appinstalled', () => { installPrompt = null; $('install-app').hidden = true; });

    const asBool = (value) => Boolean(Number(value));
    function updateBadge(count) {
        state.unreadCount = Number(count || 0);
        if (state.unreadCount > 0) navigator.setAppBadge?.(state.unreadCount).catch?.(() => {});
        else navigator.clearAppBadge?.().catch?.(() => {});
    }

    function deviceId() {
        const key = 'aml-support-device-id';
        try {
            let value = localStorage.getItem(key);
            if (!value) { value = 'dev_' + crypto.randomUUID(); localStorage.setItem(key, value); }
            return value;
        } catch { return 'dev_' + crypto.randomUUID(); }
    }

    function vapidKey(value) {
        const padding = '='.repeat((4 - value.length % 4) % 4);
        const raw = atob((value + padding).replace(/-/g, '+').replace(/_/g, '/'));
        return Uint8Array.from(raw, (character) => character.charCodeAt(0));
    }

    async function currentPush() {
        if (!('serviceWorker' in navigator) || !('PushManager' in window)) return null;
        const registration = await navigator.serviceWorker.ready;
        return registration.pushManager.getSubscription();
    }

    async function storePush(subscription) {
        const json = subscription.toJSON();
        const result = await api('/admin/api/support/push/subscriptions', { method: 'POST', body: {
            deviceId: deviceId(), endpoint: json.endpoint, keys: json.keys,
        } });
        try { localStorage.setItem('aml-support-push-id', result.id); } catch { /* optional */ }
        return result.id;
    }

    async function refreshPushButton() {
        const subscription = await currentPush().catch(() => null);
        $('toggle-push').textContent = subscription ? 'Disattiva notifiche' : 'Attiva notifiche';
        $('test-push').disabled = !subscription;
        return subscription;
    }

    async function togglePush() {
        const existing = await currentPush();
        if (existing) {
            let subscriptionId = null;
            try { subscriptionId = localStorage.getItem('aml-support-push-id'); } catch { /* optional */ }
            if (!subscriptionId) subscriptionId = await storePush(existing);
            await api('/admin/api/support/push/subscriptions/' + encodeURIComponent(subscriptionId), { method: 'DELETE' });
            await existing.unsubscribe();
            try { localStorage.removeItem('aml-support-push-id'); } catch { /* optional */ }
            toast('Notifiche disattivate.');
        } else {
            if (!state.profile?.vapidPublicKey) throw new Error('VAPID non configurato sul server.');
            const permission = await Notification.requestPermission();
            if (permission !== 'granted') throw new Error('Permesso notifiche non concesso.');
            const registration = await navigator.serviceWorker.ready;
            const subscription = await registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: vapidKey(state.profile.vapidPublicKey),
            });
            await storePush(subscription);
            toast('Notifiche attivate.');
        }
        await refreshPushButton();
    }

    async function api(path, options) {
        const init = Object.assign({ credentials: 'same-origin', headers: {} }, options || {});
        if (Object.prototype.hasOwnProperty.call(init, 'body')) {
            init.headers['Content-Type'] = 'application/json';
            init.body = JSON.stringify(init.body || {});
        }
        const response = await fetch(path, init);
        const data = await response.json().catch(() => ({}));
        if (!response.ok) throw Object.assign(new Error(data.error?.message || data.error || 'HTTP ' + response.status), { status: response.status });
        return data;
    }

    const stamp = (value) => value ? new Date(Number(value)).toLocaleString('it-IT', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }) : '—';

    function renderInbox(append) {
        const list = $('conversation-list');
        if (!append) list.textContent = '';
        state.conversations.forEach((conversation) => {
            if (append && list.querySelector('[data-id="' + CSS.escape(conversation.id) + '"]')) return;
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'sup-card' + (conversation.id === state.selected ? ' active' : '');
            button.dataset.id = conversation.id;
            button.setAttribute('role', 'listitem');
            const top = document.createElement('span'); top.className = 'sup-card-top';
            const title = document.createElement('strong'); title.textContent = conversation.order_id || conversation.product_id || 'Guest';
            const time = document.createElement('time'); time.textContent = stamp(conversation.last_message_at || conversation.created_at);
            top.append(title, time);
            const preview = document.createElement('p'); preview.textContent = conversation.last_message_preview || 'Nuova conversazione';
            const meta = document.createElement('small'); meta.textContent = conversation.status + (conversation.assigned_operator_id ? ' · assegnata' : ' · non assegnata');
            button.append(top, preview, meta);
            if (Number(conversation.operator_unread_count || 0) > 0) {
                const unread = document.createElement('span'); unread.className = 'sup-unread'; unread.textContent = String(conversation.operator_unread_count); top.appendChild(unread);
            }
            button.addEventListener('click', () => openConversation(conversation.id, true));
            list.appendChild(button);
        });
        if (!list.children.length) {
            const empty = document.createElement('p'); empty.className = 'sup-placeholder'; empty.textContent = 'Nessuna conversazione.'; list.appendChild(empty);
        }
    }

    async function loadInbox(append) {
        const params = new URLSearchParams();
        const status = $('status-filter').value;
        if (status) params.set('status', status);
        if (append && state.cursor) {
            params.set('cursorAt', state.cursor.cursorAt);
            params.set('cursorId', state.cursor.cursorId);
        }
        try {
            const data = await api('/admin/api/support/conversations?' + params);
            state.conversations = append ? state.conversations.concat(data.conversations || []) : (data.conversations || []);
            state.cursor = data.nextCursor;
            updateBadge(data.unreadConversationCount);
            $('load-more').hidden = !state.cursor;
            renderInbox(append);
        } catch (error) {
            toast('Inbox: ' + error.message);
            if (!append) {
                const list = $('conversation-list');
                list.textContent = '';
                const notice = document.createElement('p');
                notice.className = 'sup-placeholder';
                notice.textContent = 'Impossibile caricare le conversazioni.';
                list.appendChild(notice);
            }
        }
    }

    function renderMessages(messages) {
        const list = $('message-list');
        list.textContent = '';
        messages.forEach((message) => {
            const item = document.createElement('div');
            item.className = 'sup-message ' + (message.senderType === 'operator' ? 'operator' : 'visitor');
            const body = document.createElement('span'); body.textContent = String(message.body || '');
            const time = document.createElement('small'); time.textContent = stamp(message.createdAt);
            item.append(body, time); list.appendChild(item);
        });
        if (!messages.length) {
            const empty = document.createElement('p'); empty.className = 'sup-placeholder'; empty.textContent = 'Nessun messaggio.'; list.appendChild(empty);
        }
        list.scrollTop = list.scrollHeight;
    }

    function renderDetails(detail) {
        const values = [
            ['Nome', detail.contactName], ['Email', detail.contactEmail], ['Lingua', detail.locale],
            ['Paese', detail.countryCode], ['Prodotto', detail.productId], ['Ordine verificato', detail.orderId],
            ['Pagina iniziale', detail.pagePath], ['Creata', stamp(detail.createdAt)],
        ];
        [$('guest-details'), $('guest-details-mobile')].forEach((dl) => {
            dl.textContent = '';
            values.forEach(([label, value]) => {
                const dt = document.createElement('dt'); dt.textContent = label;
                const dd = document.createElement('dd'); dd.textContent = value || '—'; dl.append(dt, dd);
            });
        });
    }

    async function openConversation(id, push) {
        state.selected = id;
        shell.classList.add('conversation-open');
        document.querySelector('.sup-conversation').dataset.empty = 'false';
        renderInbox(false);
        try {
            const [detail, historyData] = await Promise.all([
                api('/admin/api/support/conversations/' + encodeURIComponent(id)),
                api('/admin/api/support/conversations/' + encodeURIComponent(id) + '/messages?limit=100'),
            ]);
            state.detail = detail;
            $('conversation-title').textContent = detail.contactName || detail.orderId || 'Guest';
            $('conversation-status').textContent = detail.status + ' · seq ' + detail.lastSeq;
            $('toggle-status').textContent = ['CLOSED', 'ARCHIVED'].includes(detail.status) ? 'Riapri' : 'Chiudi';
            renderMessages(historyData.messages || []);
            renderDetails(detail);
            if (push) window.history.pushState({}, '', '/admin/support/conversations/' + encodeURIComponent(id));
            await api('/admin/api/support/conversations/' + encodeURIComponent(id) + '/read', { method: 'POST', body: { lastReadSeq: detail.lastSeq } });
        } catch (error) { toast('Conversazione: ' + error.message); }
    }

    async function mutate(suffix, method, body) {
        if (!state.selected) return;
        try {
            await api('/admin/api/support/conversations/' + encodeURIComponent(state.selected) + suffix, { method, body: body || {} });
            await Promise.all([loadInbox(false), openConversation(state.selected, false)]);
        } catch (error) { toast(error.message); }
    }

    function connectHub() {
        const scheme = location.protocol === 'https:' ? 'wss:' : 'ws:';
        const socket = new WebSocket(scheme + '//' + location.host + '/admin/api/support/ws');
        state.socket = socket;
        socket.addEventListener('open', () => {
            const reconnected = state.reconnect > 0;
            state.reconnect = 0; document.querySelector('.sup-presence').classList.add('online'); $('connection-state').textContent = 'Realtime';
            if (reconnected) socket.send(JSON.stringify({ v: 1, type: 'operator.reconnect', payload: {} }));
            socket.send(JSON.stringify({ v: 1, type: 'operator.visibility', payload: { visibility: document.hidden ? 'hidden' : 'visible' } }));
            socket.send(JSON.stringify({ v: 1, type: 'operator.presence', payload: { state: state.preferences?.availability_state || 'OFFLINE' } }));
            loadInbox(false); if (state.selected) openConversation(state.selected, false);
        });
        socket.addEventListener('message', (event) => {
            let data; try { data = JSON.parse(event.data); } catch (_) { return; }
            const conversationId = data.payload?.conversationId || data.conversationId;
            if (data.type === 'message.created' && data.payload?.senderType === 'visitor'
                && asBool(state.preferences?.sound_enabled) && !document.hidden) {
                try {
                    const context = new AudioContext(); const oscillator = context.createOscillator();
                    oscillator.frequency.value = 740; oscillator.connect(context.destination); oscillator.start();
                    oscillator.stop(context.currentTime + 0.08);
                } catch { /* enhancement only */ }
            }
            loadInbox(false);
            if (conversationId && conversationId === state.selected) openConversation(state.selected, false);
        });
        socket.addEventListener('close', () => {
            document.querySelector('.sup-presence').classList.remove('online'); $('connection-state').textContent = 'Riconnessione…';
            const delay = Math.min(30000, 800 * Math.pow(2, state.reconnect++)) * (0.8 + Math.random() * 0.4);
            setTimeout(connectHub, delay);
        });
        socket.addEventListener('error', () => socket.close());
    }

    $('status-filter').addEventListener('change', () => loadInbox(false));
    $('open-details').addEventListener('click', () => $('guest-dialog').showModal());
    $('close-details').addEventListener('click', () => $('guest-dialog').close());
    $('load-more').addEventListener('click', () => loadInbox(true));
    $('back-inbox').addEventListener('click', () => { shell.classList.remove('conversation-open'); history.pushState({}, '', '/admin/support/'); });
    $('reply-form').addEventListener('submit', async (event) => {
        event.preventDefault(); const input = $('reply-body'); const body = input.value.trim(); if (!body || !state.selected) return;
        const button = event.currentTarget.querySelector('button'); button.disabled = true;
        try {
            await api('/admin/api/support/conversations/' + encodeURIComponent(state.selected) + '/messages', { method: 'POST', body: { clientMessageId: 'msg_' + crypto.randomUUID(), body } });
            input.value = ''; await openConversation(state.selected, false);
        } catch (error) { toast(error.message); } finally { button.disabled = false; input.focus(); }
    });
    $('assign-me').addEventListener('click', () => mutate('/assignment', 'PATCH', { assignedOperatorId: 'me' }));
    $('toggle-status').addEventListener('click', () => {
        if (!state.detail) return;
        if (['CLOSED', 'ARCHIVED'].includes(state.detail.status)) mutate('/reopen', 'POST', {});
        else mutate('/status', 'PATCH', { status: 'CLOSED' });
    });
    $('archive').addEventListener('click', () => mutate('/archive', 'POST', {}));
    $('spam').addEventListener('click', () => { if (confirm('Contrassegnare la conversazione come spam?')) mutate('/spam', 'POST', {}); });
    $('export').addEventListener('click', () => {
        if (state.selected) location.href = '/admin/api/support/conversations/' + encodeURIComponent(state.selected) + '/export';
    });
    $('delete-chat').addEventListener('click', async () => {
        if (!state.selected || !confirm('Eliminare definitivamente questa chat? Gli ordini non verranno modificati.')) return;
        try {
            await api('/admin/api/support/conversations/' + encodeURIComponent(state.selected), { method: 'DELETE' });
            state.selected = null; state.detail = null; shell.classList.remove('conversation-open');
            document.querySelector('.sup-conversation').dataset.empty = 'true';
            $('conversation-title').textContent = 'Seleziona una conversazione';
            $('message-list').textContent = '';
            window.history.pushState({}, '', '/admin/support/');
            await loadInbox(false); toast('Cancellazione completata o accodata.');
        } catch (error) { toast(error.message); }
    });
    document.querySelectorAll('[data-quick]').forEach((button) => button.addEventListener('click', () => { $('reply-body').value = button.dataset.quick; $('reply-body').focus(); }));
    document.addEventListener('visibilitychange', () => {
        if (state.socket?.readyState === WebSocket.OPEN) {
            state.socket.send(JSON.stringify({ v: 1, type: 'operator.visibility', payload: { visibility: document.hidden ? 'hidden' : 'visible' } }));
        }
    });
    $('open-settings').addEventListener('click', async () => {
        const preferences = state.preferences || {};
        $('operator-availability').value = preferences.availability_state || 'OFFLINE';
        $('public-availability').value = state.profile?.publicAvailabilityOverride || 'AUTO';
        $('pref-new').checked = asBool(preferences.notify_new_conversation);
        $('pref-message').checked = asBool(preferences.notify_new_visitor_message);
        $('pref-assigned').checked = asBool(preferences.notify_assigned_conversation);
        $('pref-sound').checked = asBool(preferences.sound_enabled);
        $('pref-preview').checked = asBool(preferences.push_preview_enabled);
        await refreshPushButton();
        $('support-settings').showModal();
    });
    $('toggle-push').addEventListener('click', () => togglePush().catch((error) => toast(error.message)));
    $('test-push').addEventListener('click', () => api('/admin/api/support/push/test', { method: 'POST', body: {} })
        .then(() => toast('Push di prova inviata.')).catch((error) => toast(error.message)));
    $('save-settings').addEventListener('click', async () => {
        const availability = $('operator-availability').value;
        try {
            await Promise.all([
                api('/admin/api/support/preferences', { method: 'PATCH', body: {
                    notifyNewConversation: $('pref-new').checked,
                    notifyNewVisitorMessage: $('pref-message').checked,
                    notifyAssignedConversation: $('pref-assigned').checked,
                    soundEnabled: $('pref-sound').checked,
                    pushPreviewEnabled: $('pref-preview').checked,
                } }),
                api('/admin/api/support/availability', { method: 'PATCH', body: {
                    state: availability, publicOverride: $('public-availability').value,
                } }),
            ]);
            state.preferences = {
                notify_new_conversation: Number($('pref-new').checked),
                notify_new_visitor_message: Number($('pref-message').checked),
                notify_assigned_conversation: Number($('pref-assigned').checked),
                sound_enabled: Number($('pref-sound').checked),
                push_preview_enabled: Number($('pref-preview').checked),
                availability_state: availability,
            };
            state.profile.publicAvailabilityOverride = $('public-availability').value;
            state.socket?.send(JSON.stringify({ v: 1, type: 'operator.presence', payload: { state: availability } }));
            $('support-settings').close(); toast('Preferenze salvate.');
        } catch (error) { toast(error.message); }
    });
    window.addEventListener('popstate', () => {
        const match = location.pathname.match(/\/admin\/support\/conversations\/([^/]+)/);
        if (match) openConversation(decodeURIComponent(match[1]), false); else shell.classList.remove('conversation-open');
    });

    Promise.all([api('/admin/api/support/profile'), loadInbox(false)]).then(([profile]) => {
        state.profile = profile; state.operator = profile.operator; state.preferences = profile.preferences; connectHub();
        const match = location.pathname.match(/\/admin\/support\/conversations\/([^/]+)/);
        if (match) openConversation(decodeURIComponent(match[1]), false);
    }).catch((error) => toast(error.message));
})();
