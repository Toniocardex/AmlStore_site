const CACHE_VERSION = 'aml-support-shell-v4';
const APP_SHELL = [
    '/admin/support/',
    '/admin/support/support.css',
    '/admin/support/support-settings.css',
    '/admin/support/support.js',
    '/admin/support/manifest.webmanifest',
    '/admin/support/icon.svg',
    '/fonts/montserrat.css',
    '/logo/logo-header-400-light.webp',
    '/favicon/apple-touch-icon.png',
];

self.addEventListener('install', (event) => {
    event.waitUntil(caches.open(CACHE_VERSION).then((cache) => cache.addAll(APP_SHELL)));
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(Promise.all([
        caches.keys().then((keys) => Promise.all(
            keys.filter((key) => key.startsWith('aml-support-shell-') && key !== CACHE_VERSION)
                .map((key) => caches.delete(key)),
        )),
        self.clients.claim(),
    ]));
});

function isSensitive(url) {
    return url.pathname.startsWith('/admin/api/') || url.pathname.startsWith('/api/chat/');
}

self.addEventListener('fetch', (event) => {
    const request = event.request;
    if (request.method !== 'GET') return;
    const url = new URL(request.url);
    if (url.origin !== self.location.origin || isSensitive(url)) return;

    if (request.mode === 'navigate' && url.pathname.startsWith('/admin/support')) {
        event.respondWith(fetch(request).catch(() => caches.match('/admin/support/')));
        return;
    }
    if (!APP_SHELL.includes(url.pathname)) return;
    event.respondWith(caches.match(request).then((cached) => cached || fetch(request).then((response) => {
        if (response.ok) {
            const copy = response.clone();
            event.waitUntil(caches.open(CACHE_VERSION).then((cache) => cache.put(request, copy)));
        }
        return response;
    })));
});

self.addEventListener('push', (event) => {
    let payload = {};
    try { payload = event.data?.json() || {}; } catch { payload = {}; }
    const unreadCount = Number(payload.unreadCount || 0);
    const conversationId = typeof payload.conversationId === 'string' ? payload.conversationId : null;
    event.waitUntil(Promise.all([
        self.registration.showNotification(payload.title || 'Eurolicenze Support', {
            body: payload.body || 'Nuovo messaggio di assistenza',
            icon: '/admin/support/icon.svg',
            badge: '/favicon/favicon.png',
            tag: conversationId ? `support-${conversationId}` : 'support-message',
            renotify: true,
            data: { conversationId },
        }),
        typeof self.navigator.setAppBadge === 'function'
            ? (unreadCount > 0 ? self.navigator.setAppBadge(unreadCount) : self.navigator.clearAppBadge())
            : Promise.resolve(),
    ]));
});

self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    const conversationId = event.notification.data?.conversationId;
    const target = conversationId
        ? `/admin/support/conversations/${encodeURIComponent(conversationId)}`
        : '/admin/support/';
    event.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(async (clients) => {
        const existing = clients.find((client) => new URL(client.url).pathname.startsWith('/admin/support'));
        if (existing) {
            await existing.navigate(target);
            return existing.focus();
        }
        return self.clients.openWindow(target);
    }));
});
