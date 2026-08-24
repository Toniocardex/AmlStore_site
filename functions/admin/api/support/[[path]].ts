import { resolveAdminAuth } from '../../../api/_lib/admin.js';
import { assertAllowedOrigin } from '../../../_lib/chat/origin';
import { chatError, chatJson, readJsonBody } from '../../../_lib/chat/responses';
import { ChatProtocolError } from '../../../../support/shared/errors';
import { createId, isPrefixedId } from '../../../../support/shared/ids';
import { normalizePlainText } from '../../../../support/shared/schemas';
import { normalizeContact } from '../../../_lib/chat/contact';
import {
    enqueueDeletionJob,
    prepareDeletionJob,
    processDeletionJob,
    type DeletionJob,
} from '../../../../workers/support-realtime/src/retention';
import type { SupportRealtimeEnv } from '../../../../workers/support-realtime/src/env';

interface SupportAdminEnv {
    DB: D1Database;
    CHAT_CONVERSATIONS: DurableObjectNamespace;
    SUPPORT_HUB: DurableObjectNamespace;
    CHAT_ENABLED?: string;
    CHAT_MAX_MESSAGE_LENGTH?: string;
    SITE_ORIGIN?: string;
    CF_ACCESS_AUD?: string;
    CF_ACCESS_TEAM_DOMAIN?: string;
    ADMIN_ALLOWED_EMAILS?: string;
    ADMIN_DEV_BYPASS?: string;
    CHAT_CONTACT_LOOKUP_SECRET?: string;
    CHAT_DELETE_GRACE_DAYS?: string;
    CHAT_RETENTION_BATCH_SIZE?: string;
    VAPID_PUBLIC_KEY?: string;
}

interface Operator {
    id: string;
    email: string;
    displayName: string | null;
    permissions: string[];
}

function routeParts(context: EventContext<SupportAdminEnv, string, Record<string, unknown>>): string[] {
    const value = context.params.path;
    return Array.isArray(value) ? value.map(String) : (value ? [String(value)] : []);
}

async function requireOperator(request: Request, env: SupportAdminEnv): Promise<Operator> {
    const auth = await resolveAdminAuth(request, env as unknown as Record<string, unknown>);
    if (!auth.valid || !auth.email) {
        throw new ChatProtocolError('UNAUTHORIZED', 'Unauthorized', 401);
    }
    const email = auth.email.toLowerCase();
    let row = await env.DB.prepare(`
        SELECT id, email, display_name, permissions_json
        FROM chat_operators WHERE email = ?
    `).bind(email).first<{
        id: string;
        email: string;
        display_name: string | null;
        permissions_json: string;
    }>();
    if (!row) {
        const now = Date.now();
        const id = createId('operator');
        await env.DB.prepare(`
            INSERT INTO chat_operators (
                id, email, display_name, role, permissions_json, created_at, updated_at
            ) VALUES (?, ?, NULL, 'support', '["support.*"]', ?, ?)
            ON CONFLICT(email) DO NOTHING
        `).bind(id, email, now, now).run();
        row = await env.DB.prepare(`
            SELECT id, email, display_name, permissions_json
            FROM chat_operators WHERE email = ?
        `).bind(email).first<{
            id: string;
            email: string;
            display_name: string | null;
            permissions_json: string;
        }>();
    }
    if (!row) throw new ChatProtocolError('INTERNAL_ERROR', 'Operator initialization failed', 500);
    await env.DB.prepare(`
        INSERT INTO chat_operator_preferences (operator_id, updated_at)
        VALUES (?, ?)
        ON CONFLICT(operator_id) DO NOTHING
    `).bind(row.id, Date.now()).run();
    let permissions: string[] = [];
    try { permissions = JSON.parse(row.permissions_json) as string[]; } catch { /* deny below */ }
    if (!permissions.includes('support.*') && !permissions.includes('support.read')) {
        throw new ChatProtocolError('FORBIDDEN', 'Missing support permission', 403);
    }
    return { id: row.id, email: row.email, displayName: row.display_name, permissions };
}

function conversationStub(env: SupportAdminEnv, conversationId: string): DurableObjectStub {
    if (!isPrefixedId(conversationId, 'conversation')) {
        throw new ChatProtocolError('NOT_FOUND', 'Conversation not found', 404);
    }
    return env.CHAT_CONVERSATIONS.get(
        env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
    );
}

function assertPermission(operator: Operator, permission: 'support.read' | 'support.write'): void {
    if (!operator.permissions.includes('support.*') && !operator.permissions.includes(permission)) {
        throw new ChatProtocolError('FORBIDDEN', 'Missing support permission', 403);
    }
}

function workerEnv(env: SupportAdminEnv): SupportRealtimeEnv {
    return { ...env, CHAT_DB: env.DB } as unknown as SupportRealtimeEnv;
}

async function enqueueManualDeletion(
    env: SupportAdminEnv,
    operator: Operator,
    conversationId: string,
    reason: string,
): Promise<string> {
    const adapted = workerEnv(env);
    const jobId = await enqueueDeletionJob(adapted, conversationId, `operator:${operator.id}`, reason);
    const graceDays = Number(env.CHAT_DELETE_GRACE_DAYS || 0);
    const job = await env.DB.prepare(`
        SELECT id, conversation_id, reason, status,
               previous_status, previous_closed_at, previous_archived_at,
               previous_archive_at, previous_purge_at, attempts
        FROM chat_deletion_jobs WHERE id = ?
    `).bind(jobId).first<DeletionJob>();
    if (job && job.status === 'PENDING') {
        const executeAt = graceDays > 0 ? Date.now() + graceDays * 86_400_000 : null;
        const prepared = await prepareDeletionJob(adapted, job, executeAt);
        if (prepared && executeAt == null) {
            await processDeletionJob(adapted, { ...job, status: 'GATED' });
        }
    }
    return jobId;
}

const ERASURE_BATCH_CEILING = 100;

function erasureBatchSize(env: SupportAdminEnv): number {
    const value = Number(env.CHAT_RETENTION_BATCH_SIZE || 50);
    if (!Number.isInteger(value) || value <= 0) return 50;
    return Math.min(value, ERASURE_BATCH_CEILING);
}

/**
 * ADR §69.11: la cancellazione dello storico guest deve essere batch-based,
 * resumable e idempotente. Ogni chiamata blocca (gate) un numero limitato di
 * conversazioni e lascia la finalizzazione al retention worker: purgare
 * sincronamente N conversazioni dentro una singola richiesta HTTP supererebbe i
 * limiti di subrequest/CPU senza alcuna possibilità di ripresa.
 */
async function enqueueErasureBatch(
    env: SupportAdminEnv,
    operator: Operator,
    conversationIds: string[],
    reason: string,
): Promise<{ jobs: string[]; gateFailures: string[] }> {
    const adapted = workerEnv(env);
    const graceDays = Number(env.CHAT_DELETE_GRACE_DAYS || 0);
    const executeAt = graceDays > 0 ? Date.now() + graceDays * 86_400_000 : null;
    const jobs: string[] = [];
    const gateFailures: string[] = [];
    for (const conversationId of conversationIds) {
        const jobId = await enqueueDeletionJob(adapted, conversationId, `operator:${operator.id}`, reason);
        const job = await env.DB.prepare(`
            SELECT id, conversation_id, reason, status,
                   previous_status, previous_closed_at, previous_archived_at,
                   previous_archive_at, previous_purge_at, attempts
            FROM chat_deletion_jobs WHERE id = ?
        `).bind(jobId).first<DeletionJob>();
        if (job && job.status === 'PENDING' && !await prepareDeletionJob(adapted, job, executeAt)) {
            // Il job resta persistito con next_attempt_at: il cron riprova il gate.
            gateFailures.push(conversationId);
        }
        jobs.push(jobId);
    }
    return { jobs, gateFailures };
}

async function forwardConversation(
    env: SupportAdminEnv,
    operator: Operator,
    conversationId: string,
    action: 'detail' | 'messages',
    url: URL,
): Promise<Response> {
    const response = await conversationStub(env, conversationId).fetch(new Request(
        `https://internal/internal/admin/conversations/${action}`,
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                conversationId,
                operatorId: operator.id,
                beforeSeq: url.searchParams.get('beforeSeq'),
                limit: url.searchParams.get('limit'),
            }),
        },
    ));
    return new Response(response.body, {
        status: response.status,
        headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
    });
}

async function forwardMutation(
    env: SupportAdminEnv,
    operator: Operator,
    conversationId: string,
    action: 'state' | 'assignment' | 'read',
    payload: Record<string, unknown>,
): Promise<Response> {
    const response = await conversationStub(env, conversationId).fetch(new Request(
        `https://internal/internal/admin/conversations/${action}`,
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                conversationId,
                operatorId: operator.id,
                ...payload,
                updatedAt: Date.now(),
            }),
        },
    ));
    return new Response(response.body, {
        status: response.status,
        headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
    });
}

async function listConversations(request: Request, env: SupportAdminEnv): Promise<Response> {
    const url = new URL(request.url);
    const status = url.searchParams.get('status');
    const cursorAt = Number(url.searchParams.get('cursorAt') || Number.MAX_SAFE_INTEGER);
    const cursorId = url.searchParams.get('cursorId') || '\uffff';
    const allowed = ['OPEN', 'PENDING', 'CLOSED', 'ARCHIVED', 'SPAM', 'PURGE_PENDING'];
    if (status && !allowed.includes(status)) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid status filter');
    }
    if (!Number.isFinite(cursorAt) || cursorAt < 0) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid cursor');
    }
    const whereStatus = status ? 'AND status = ?' : "AND status != 'PURGE_PENDING'";
    const bindings: unknown[] = [cursorAt, cursorAt, cursorId];
    if (status) bindings.push(status);
    const rows = await env.DB.prepare(`
        SELECT id, status, assigned_operator_id, locale, country_code,
               product_id, order_id, page_path, last_seq, projection_version,
               last_message_at, last_message_sender, last_message_preview,
               visitor_unread_count, operator_unread_count, created_at, updated_at
        FROM chat_conversations
        WHERE (COALESCE(last_message_at, created_at) < ?
               OR (COALESCE(last_message_at, created_at) = ? AND id < ?))
          ${whereStatus}
        ORDER BY COALESCE(last_message_at, created_at) DESC, id DESC
        LIMIT 51
    `).bind(...bindings).all<Record<string, unknown>>();
    const result = rows.results || [];
    const page = result.slice(0, 50);
    const last = page.at(-1);
    const unread = await env.DB.prepare(`
        SELECT COUNT(*) AS total FROM chat_conversations
        WHERE operator_unread_count > 0 AND status IN ('OPEN','PENDING','CLOSED')
    `).first<{ total: number }>();
    return chatJson({
        conversations: page,
        unreadConversationCount: Number(unread?.total || 0),
        nextCursor: result.length > 50 && last ? {
            cursorAt: last.last_message_at || last.created_at,
            cursorId: last.id,
        } : null,
    });
}

export const onRequest: PagesFunction<SupportAdminEnv> = async (context) => {
    const { request, env } = context;
    try {
        if (env.CHAT_ENABLED !== '1') {
            throw new ChatProtocolError('TEMPORARILY_UNAVAILABLE', 'Chat is disabled', 503);
        }
        const operator = await requireOperator(request, env);
        const parts = routeParts(context);
        const url = new URL(request.url);

        if (request.method === 'GET' && parts.length === 1 && parts[0] === 'profile') {
            const preferences = await env.DB.prepare(`
                SELECT notify_new_conversation, notify_new_visitor_message,
                       notify_assigned_conversation, sound_enabled,
                       push_preview_enabled, availability_state
                FROM chat_operator_preferences WHERE operator_id = ?
            `).bind(operator.id).first();
            const settings = await env.DB.prepare(`
                SELECT public_availability_override
                FROM chat_support_settings WHERE settings_key = 'default'
            `).first();
            return chatJson({
                operator,
                preferences,
                publicAvailabilityOverride: settings?.public_availability_override || 'AUTO',
                vapidPublicKey: env.VAPID_PUBLIC_KEY || null,
            });
        }
        if (request.method === 'PATCH' && parts.length === 1 && parts[0] === 'preferences') {
            assertPermission(operator, 'support.write');
            assertAllowedOrigin(request, env);
            const body = await readJsonBody(request) as Record<string, unknown>;
            const boolean = (name: string): number => {
                if (typeof body[name] !== 'boolean') throw new ChatProtocolError('INVALID_PAYLOAD', `Invalid ${name}`);
                return body[name] ? 1 : 0;
            };
            await env.DB.prepare(`
                UPDATE chat_operator_preferences
                SET notify_new_conversation = ?, notify_new_visitor_message = ?,
                    notify_assigned_conversation = ?, sound_enabled = ?,
                    push_preview_enabled = ?, updated_at = ?
                WHERE operator_id = ?
            `).bind(
                boolean('notifyNewConversation'), boolean('notifyNewVisitorMessage'),
                boolean('notifyAssignedConversation'), boolean('soundEnabled'),
                boolean('pushPreviewEnabled'), Date.now(), operator.id,
            ).run();
            return chatJson({ ok: true });
        }
        if (request.method === 'PATCH' && parts.length === 1 && parts[0] === 'availability') {
            assertPermission(operator, 'support.write');
            assertAllowedOrigin(request, env);
            const body = await readJsonBody(request) as Record<string, unknown>;
            if (!['ONLINE', 'BUSY', 'OFFLINE'].includes(String(body.state))) {
                throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid operator availability');
            }
            if (!['AUTO', 'ONLINE', 'OFFLINE'].includes(String(body.publicOverride))) {
                throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid public availability override');
            }
            await env.DB.batch([
                env.DB.prepare(`
                    UPDATE chat_operator_preferences SET availability_state = ?, updated_at = ?
                    WHERE operator_id = ?
                `).bind(body.state, Date.now(), operator.id),
                env.DB.prepare(`
                    UPDATE chat_support_settings
                    SET public_availability_override = ?, updated_by = ?, updated_at = ?
                    WHERE settings_key = 'default'
                `).bind(body.publicOverride, operator.id, Date.now()),
            ]);
            return chatJson({ ok: true });
        }
        if (request.method === 'POST' && parts.length === 2
            && parts[0] === 'push' && parts[1] === 'subscriptions') {
            assertPermission(operator, 'support.write');
            assertAllowedOrigin(request, env);
            const body = await readJsonBody(request) as Record<string, unknown>;
            const keys = body.keys as Record<string, unknown> | undefined;
            if (!isPrefixedId(body.deviceId, 'device') || typeof body.endpoint !== 'string'
                || !body.endpoint.startsWith('https://') || body.endpoint.length > 2_048
                || typeof keys?.p256dh !== 'string' || typeof keys?.auth !== 'string') {
                throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid push subscription');
            }
            const owner = await env.DB.prepare(`
                SELECT operator_id FROM chat_push_subscriptions WHERE endpoint = ?
            `).bind(body.endpoint).first<{ operator_id: string }>();
            if (owner && owner.operator_id !== operator.id) {
                throw new ChatProtocolError('FORBIDDEN', 'Push endpoint belongs to another operator', 403);
            }
            const id = createId('device');
            await env.DB.prepare(`
                INSERT INTO chat_push_subscriptions (
                    id, operator_id, device_id, endpoint, p256dh, auth,
                    user_agent, enabled, created_at, last_used_at, failed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, NULL, NULL)
                ON CONFLICT(endpoint) DO UPDATE SET
                    device_id = excluded.device_id, p256dh = excluded.p256dh,
                    auth = excluded.auth, user_agent = excluded.user_agent,
                    enabled = 1, failed_at = NULL
            `).bind(
                id, operator.id, body.deviceId, body.endpoint, keys.p256dh, keys.auth,
                request.headers.get('User-Agent'), Date.now(),
            ).run();
            const stored = await env.DB.prepare(`
                SELECT id FROM chat_push_subscriptions WHERE endpoint = ?
            `).bind(body.endpoint).first<{ id: string }>();
            return chatJson({ id: stored?.id || id }, 201);
        }
        if (request.method === 'GET' && parts.length === 2
            && parts[0] === 'push' && parts[1] === 'subscriptions') {
            assertPermission(operator, 'support.read');
            const subscriptions = await env.DB.prepare(`
                SELECT id, device_id, user_agent, enabled, created_at, last_used_at, failed_at
                FROM chat_push_subscriptions
                WHERE operator_id = ?
                ORDER BY created_at DESC
            `).bind(operator.id).all();
            return chatJson({ subscriptions: subscriptions.results || [] });
        }
        if (request.method === 'DELETE' && parts.length === 3
            && parts[0] === 'push' && parts[1] === 'subscriptions') {
            assertPermission(operator, 'support.write');
            assertAllowedOrigin(request, env);
            await env.DB.prepare(`
                DELETE FROM chat_push_subscriptions WHERE id = ? AND operator_id = ?
            `).bind(parts[2], operator.id).run();
            return chatJson({ ok: true });
        }
        if (request.method === 'POST' && parts.length === 2
            && parts[0] === 'push' && parts[1] === 'test') {
            assertPermission(operator, 'support.write');
            assertAllowedOrigin(request, env);
            await readJsonBody(request);
            const latest = await env.DB.prepare(`
                SELECT id FROM chat_conversations
                WHERE status NOT IN ('SPAM','PURGE_PENDING')
                ORDER BY COALESCE(last_message_at, created_at) DESC LIMIT 1
            `).first<{ id: string }>();
            if (!latest) throw new ChatProtocolError('NOT_FOUND', 'No conversation available for push test', 404);
            const hub = env.SUPPORT_HUB.get(env.SUPPORT_HUB.idFromName('support-hub:default'));
            const response = await hub.fetch(new Request('https://internal/internal/push/test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ operatorId: operator.id, conversationId: latest.id }),
            }));
            return new Response(response.body, { status: response.status, headers: response.headers });
        }
        if (request.method === 'GET' && parts.length === 1 && parts[0] === 'conversations') {
            assertPermission(operator, 'support.read');
            return listConversations(request, env);
        }
        if (request.method === 'GET' && parts.length === 1 && parts[0] === 'ws') {
            assertPermission(operator, 'support.read');
            assertAllowedOrigin(request, env);
            const hub = env.SUPPORT_HUB.get(env.SUPPORT_HUB.idFromName('support-hub:default'));
            return hub.fetch(new Request(
                `https://internal/internal/operators/ws?operatorId=${encodeURIComponent(operator.id)}`,
                { headers: { Upgrade: 'websocket' } },
            ));
        }
        if (request.method === 'GET' && parts.length === 2 && parts[0] === 'deletion-jobs') {
            assertPermission(operator, 'support.read');
            const job = await env.DB.prepare(`
                SELECT id, conversation_id, requested_by, reason, status, attempts,
                       next_attempt_at, last_error, created_at, updated_at, completed_at
                FROM chat_deletion_jobs WHERE id = ?
            `).bind(parts[1]).first();
            if (!job) throw new ChatProtocolError('NOT_FOUND', 'Deletion job not found', 404);
            return chatJson({ job });
        }
        if (request.method === 'DELETE' && parts.length === 2 && parts[0] === 'deletion-jobs') {
            assertPermission(operator, 'support.write');
            assertAllowedOrigin(request, env);
            const job = await env.DB.prepare(`
                SELECT id, conversation_id, status, next_attempt_at,
                       previous_status, previous_closed_at, previous_archived_at,
                       previous_archive_at, previous_purge_at
                FROM chat_deletion_jobs WHERE id = ?
            `).bind(parts[1]).first<DeletionJob & { next_attempt_at: number | null }>();
            if (!job) throw new ChatProtocolError('NOT_FOUND', 'Deletion job not found', 404);
            if (job.status !== 'GATED' || job.next_attempt_at == null || job.next_attempt_at <= Date.now()) {
                throw new ChatProtocolError('CONVERSATION_PURGE_PENDING', 'Deletion can no longer be cancelled', 409);
            }
            const response = await conversationStub(env, job.conversation_id).fetch(new Request(
                'https://internal/internal/system/conversations/purge/cancel', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        conversationId: job.conversation_id,
                        previousStatus: job.previous_status,
                        previousClosedAt: job.previous_closed_at,
                        previousArchivedAt: job.previous_archived_at,
                        previousArchiveAt: job.previous_archive_at,
                        previousPurgeAt: job.previous_purge_at,
                        updatedAt: Date.now(),
                    }),
                },
            ));
            if (!response.ok) return new Response(response.body, { status: response.status, headers: response.headers });
            await env.DB.batch([
                env.DB.prepare(`
                    UPDATE chat_conversations
                    SET status = ?, closed_at = ?, archived_at = ?, archive_at = ?, purge_at = ?,
                        purge_requested_at = NULL, deletion_reason = NULL, updated_at = ?
                    WHERE id = ? AND status = 'PURGE_PENDING'
                `).bind(
                    job.previous_status, job.previous_closed_at, job.previous_archived_at,
                    job.previous_archive_at, job.previous_purge_at, Date.now(), job.conversation_id,
                ),
                env.DB.prepare('DELETE FROM chat_deletion_jobs WHERE id = ?').bind(job.id),
            ]);
            return chatJson({ ok: true, conversationId: job.conversation_id });
        }
        if (request.method === 'POST' && parts.length === 3
            && parts[0] === 'guests' && parts[2] === 'deletion-jobs') {
            assertPermission(operator, 'support.write');
            assertAllowedOrigin(request, env);
            const visitorId = parts[1];
            if (!isPrefixedId(visitorId, 'visitor')) {
                throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid visitorId');
            }
            await readJsonBody(request);
            const batchSize = erasureBatchSize(env);
            const rows = await env.DB.prepare(`
                SELECT id FROM chat_conversations
                WHERE visitor_id = ? AND status != 'PURGE_PENDING'
                ORDER BY created_at ASC
                LIMIT ?
            `).bind(visitorId, batchSize + 1).all<{ id: string }>();
            const found = rows.results || [];
            const { jobs, gateFailures } = await enqueueErasureBatch(
                env, operator, found.slice(0, batchSize).map((row) => row.id), 'guest_erasure',
            );
            return chatJson({
                jobs,
                count: jobs.length,
                gateFailures,
                hasMore: found.length > batchSize,
            }, 202);
        }
        if (request.method === 'POST' && parts.length === 2
            && parts[0] === 'contacts' && parts[1] === 'deletion-jobs') {
            assertPermission(operator, 'support.write');
            assertAllowedOrigin(request, env);
            const body = await readJsonBody(request) as Record<string, unknown>;
            const contact = await normalizeContact({ email: body.email }, env);
            if (!contact.emailLookupHash) throw new ChatProtocolError('INVALID_PAYLOAD', 'Email is required');
            const batchSize = erasureBatchSize(env);
            const rows = await env.DB.prepare(`
                SELECT id FROM chat_conversations
                WHERE contact_email_lookup_hash = ? AND contact_verified_at IS NOT NULL
                  AND status != 'PURGE_PENDING'
                ORDER BY created_at ASC
                LIMIT ?
            `).bind(contact.emailLookupHash, batchSize + 1).all<{ id: string }>();
            const found = rows.results || [];
            const { jobs, gateFailures } = await enqueueErasureBatch(
                env, operator, found.slice(0, batchSize).map((row) => row.id), 'verified_contact_erasure',
            );
            return chatJson({
                jobs,
                count: jobs.length,
                gateFailures,
                hasMore: found.length > batchSize,
            }, 202);
        }
        if (parts[0] === 'conversations' && parts.length >= 2) {
            const conversationId = parts[1];
            if (request.method === 'GET' && parts.length === 2) {
                assertPermission(operator, 'support.read');
                return forwardConversation(env, operator, conversationId, 'detail', url);
            }
            if (request.method === 'GET' && parts.length === 3 && parts[2] === 'messages') {
                assertPermission(operator, 'support.read');
                return forwardConversation(env, operator, conversationId, 'messages', url);
            }
            if (request.method === 'GET' && parts.length === 3 && parts[2] === 'export') {
                assertPermission(operator, 'support.read');
                const response = await conversationStub(env, conversationId).fetch(new Request(
                    'https://internal/internal/admin/conversations/export', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ conversationId, operatorId: operator.id }),
                    },
                ));
                const headers = new Headers(response.headers);
                headers.set('Content-Disposition', `attachment; filename="chat-${conversationId}.json"`);
                headers.set('Cache-Control', 'no-store');
                return new Response(response.body, { status: response.status, headers });
            }
            if (request.method === 'DELETE' && parts.length === 2) {
                assertPermission(operator, 'support.write');
                assertAllowedOrigin(request, env);
                const exists = await env.DB.prepare(
                    'SELECT id FROM chat_conversations WHERE id = ?',
                ).bind(conversationId).first();
                if (!exists) throw new ChatProtocolError('NOT_FOUND', 'Conversation not found', 404);
                const jobId = await enqueueManualDeletion(env, operator, conversationId, 'manual_admin_delete');
                return chatJson({ jobId }, 202);
            }
            if (request.method === 'POST' && parts.length === 3 && parts[2] === 'messages') {
                assertPermission(operator, 'support.write');
                assertAllowedOrigin(request, env);
                const body = await readJsonBody(request) as Record<string, unknown>;
                if (!isPrefixedId(body.clientMessageId, 'message')) {
                    throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid clientMessageId');
                }
                const messageBody = normalizePlainText(
                    body.body,
                    Number(env.CHAT_MAX_MESSAGE_LENGTH || 4_000),
                );
                const response = await conversationStub(env, conversationId).fetch(new Request(
                    'https://internal/internal/admin/conversations/messages/send',
                    {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            conversationId,
                            operatorId: operator.id,
                            clientMessageId: body.clientMessageId,
                            body: messageBody,
                            createdAt: Date.now(),
                        }),
                    },
                ));
                return new Response(response.body, { status: response.status, headers: response.headers });
            }
            if (request.method === 'POST' && parts.length === 3 && parts[2] === 'read') {
                assertPermission(operator, 'support.write');
                assertAllowedOrigin(request, env);
                const body = await readJsonBody(request) as Record<string, unknown>;
                return forwardMutation(env, operator, conversationId, 'read', {
                    lastReadSeq: body.lastReadSeq,
                });
            }
            if (request.method === 'PATCH' && parts.length === 3 && parts[2] === 'status') {
                assertPermission(operator, 'support.write');
                assertAllowedOrigin(request, env);
                const body = await readJsonBody(request) as Record<string, unknown>;
                return forwardMutation(env, operator, conversationId, 'state', { status: body.status });
            }
            if (request.method === 'PATCH' && parts.length === 3 && parts[2] === 'assignment') {
                assertPermission(operator, 'support.write');
                assertAllowedOrigin(request, env);
                const body = await readJsonBody(request) as Record<string, unknown>;
                const assignedOperatorId = body.assignedOperatorId === 'me'
                    ? operator.id
                    : body.assignedOperatorId;
                return forwardMutation(env, operator, conversationId, 'assignment', { assignedOperatorId });
            }
            if (request.method === 'POST' && parts.length === 3
                && ['archive', 'reopen', 'spam'].includes(parts[2])) {
                assertPermission(operator, 'support.write');
                assertAllowedOrigin(request, env);
                await readJsonBody(request);
                const status = parts[2] === 'archive' ? 'ARCHIVED'
                    : parts[2] === 'reopen' ? 'OPEN' : 'SPAM';
                return forwardMutation(env, operator, conversationId, 'state', { status });
            }
        }
        throw new ChatProtocolError('NOT_FOUND', 'Not found', 404);
    } catch (error) {
        if (!(error instanceof ChatProtocolError)) console.error('[support-admin] request failed', error);
        return chatError(error);
    }
};
