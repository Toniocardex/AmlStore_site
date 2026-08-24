import webpush from 'web-push';
import type { SupportRealtimeEnv } from './env';
import { emitMetric } from './observability';

interface PushSubscriptionRow {
    id: string;
    operator_id: string;
    endpoint: string;
    p256dh: string;
    auth: string;
    push_preview_enabled: number;
    notify_new_conversation: number;
    notify_new_visitor_message: number;
    notify_assigned_conversation: number;
}

interface PushConversation {
    id: string;
    contact_name: string | null;
    last_message_preview: string | null;
}

export interface VisitorPushEvent {
    conversationId: string;
    body?: string;
    kind?: 'new_conversation' | 'visitor_message' | 'assigned_conversation' | 'test';
}

function configured(env: SupportRealtimeEnv): env is SupportRealtimeEnv & {
    VAPID_PUBLIC_KEY: string;
    VAPID_PRIVATE_KEY: string;
    VAPID_SUBJECT: string;
} {
    return Boolean(env.VAPID_PUBLIC_KEY && env.VAPID_PRIVATE_KEY && env.VAPID_SUBJECT);
}

function permanentStatus(error: unknown): number | null {
    if (!error || typeof error !== 'object' || !('statusCode' in error)) return null;
    const value = Number((error as { statusCode?: unknown }).statusCode);
    return Number.isInteger(value) ? value : null;
}

export async function dispatchVisitorPush(
    env: SupportRealtimeEnv,
    event: VisitorPushEvent,
    suppressedOperatorIds: ReadonlySet<string> = new Set(),
    targetOperatorId?: string,
): Promise<{ sent: number; failed: number; disabled: number }> {
    const startedAt = Date.now();
    if (!configured(env)) return { sent: 0, failed: 0, disabled: 0 };
    const conversation = await env.CHAT_DB.prepare(`
        SELECT id, contact_name, last_message_preview
        FROM chat_conversations WHERE id = ?
    `).bind(event.conversationId).first<PushConversation>();
    if (!conversation) return { sent: 0, failed: 0, disabled: 0 };
    const unread = await env.CHAT_DB.prepare(`
        SELECT COUNT(*) AS total FROM chat_conversations
        WHERE operator_unread_count > 0 AND status IN ('OPEN','PENDING','CLOSED')
    `).first<{ total: number }>();
    const rows = await env.CHAT_DB.prepare(`
        SELECT s.id, s.operator_id, s.endpoint, s.p256dh, s.auth,
               COALESCE(p.push_preview_enabled, 0) AS push_preview_enabled,
               COALESCE(p.notify_new_conversation, 1) AS notify_new_conversation,
               COALESCE(p.notify_new_visitor_message, 1) AS notify_new_visitor_message,
               COALESCE(p.notify_assigned_conversation, 1) AS notify_assigned_conversation
        FROM chat_push_subscriptions s
        LEFT JOIN chat_operator_preferences p ON p.operator_id = s.operator_id
        WHERE s.enabled = 1
    `).all<PushSubscriptionRow>();
    let sent = 0;
    let failed = 0;
    let disabled = 0;
    await Promise.all((rows.results || []).map(async (row) => {
        if (targetOperatorId && row.operator_id !== targetOperatorId) return;
        if (suppressedOperatorIds.has(row.operator_id)) return;
        const kind = event.kind || 'visitor_message';
        if (kind === 'new_conversation' && !row.notify_new_conversation) return;
        if (kind === 'visitor_message' && !row.notify_new_visitor_message) return;
        if (kind === 'assigned_conversation' && !row.notify_assigned_conversation) return;
        const preview = row.push_preview_enabled
            ? (event.body || conversation.last_message_preview || 'Nuovo messaggio')
            : 'Apri Supporto per leggere il messaggio.';
        const title = kind === 'new_conversation'
            ? 'Nuova conversazione di assistenza'
            : kind === 'assigned_conversation'
                ? 'Conversazione assegnata'
                : kind === 'test'
                    ? 'Notifica di prova'
                    : 'Nuovo messaggio di assistenza';
        const payload = JSON.stringify({
            v: 1,
            type: 'support.notification',
            title,
            body: conversation.contact_name ? `${conversation.contact_name}: ${preview}` : preview,
            conversationId: event.conversationId,
            unreadCount: Number(unread?.total || 0),
        });
        try {
            await webpush.sendNotification({
                endpoint: row.endpoint,
                keys: { p256dh: row.p256dh, auth: row.auth },
            }, payload, {
                TTL: 120,
                urgency: 'high',
                vapidDetails: {
                    subject: env.VAPID_SUBJECT,
                    publicKey: env.VAPID_PUBLIC_KEY,
                    privateKey: env.VAPID_PRIVATE_KEY,
                },
            });
            sent += 1;
            await env.CHAT_DB.prepare(`
                UPDATE chat_push_subscriptions SET last_used_at = ?, failed_at = NULL WHERE id = ?
            `).bind(Date.now(), row.id).run();
        } catch (error) {
            failed += 1;
            const status = permanentStatus(error);
            if (status === 404 || status === 410) {
                disabled += 1;
                await env.CHAT_DB.prepare('DELETE FROM chat_push_subscriptions WHERE id = ?')
                    .bind(row.id).run();
            } else {
                await env.CHAT_DB.prepare(`
                    UPDATE chat_push_subscriptions SET failed_at = ? WHERE id = ?
                `).bind(Date.now(), row.id).run();
            }
            console.error('[chat-push] delivery failed', { subscriptionId: row.id, status });
            emitMetric('chat_error_total', 1, { component: 'push', status: status || 0 });
        }
    }));
    emitMetric('chat_push_sent_total', sent);
    emitMetric('chat_push_failed_total', failed);
    emitMetric('chat_push_dispatch_latency_ms', Date.now() - startedAt);
    return { sent, failed, disabled };
}
