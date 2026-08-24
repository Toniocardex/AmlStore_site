import { readChatConfig } from '../../../support/shared/config';
import type { SupportRealtimeEnv } from './env';
import { emitMetric } from './observability';

export interface RetentionResult {
    archived: number;
    purgeRequested: number;
    purged: number;
}

export interface DeletionJob {
    id: string;
    conversation_id: string;
    reason: string;
    status: 'PENDING' | 'GATED' | 'DO_DELETED' | 'COMPLETE' | 'FAILED';
    previous_status?: string | null;
    previous_closed_at?: number | null;
    previous_archived_at?: number | null;
    previous_archive_at?: number | null;
    previous_purge_at?: number | null;
    attempts: number;
}

const retryDelay = (attempts: number) => Math.min(3_600_000, 5_000 * (2 ** Math.min(attempts, 9)));

function stubFor(env: SupportRealtimeEnv, conversationId: string): DurableObjectStub {
    return env.CHAT_CONVERSATIONS.get(
        env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
    );
}

async function internalPost(
    env: SupportRealtimeEnv,
    conversationId: string,
    path: string,
    body: Record<string, unknown>,
): Promise<void> {
    const response = await stubFor(env, conversationId).fetch(new Request(`https://internal${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ conversationId, ...body }),
    }));
    if (!response.ok) throw new Error(`${path} failed with ${response.status}`);
}

async function notifyPurgeComplete(
    env: SupportRealtimeEnv,
    job: DeletionJob,
    now: number,
): Promise<void> {
    const hub = env.SUPPORT_HUB.get(env.SUPPORT_HUB.idFromName('support-hub:default'));
    const eventId = job.id.startsWith('del_') ? `evt_${job.id.slice(4)}` : `evt_${crypto.randomUUID()}`;
    const response = await hub.fetch(new Request('https://internal/internal/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            v: 1,
            type: 'conversation.purged',
            eventId,
            serverTs: now,
            payload: { conversationId: job.conversation_id, reason: job.reason },
        }),
    }));
    if (!response.ok) throw new Error(`SupportHub purge notification failed with ${response.status}`);
}

export async function enqueueDeletionJob(
    env: SupportRealtimeEnv,
    conversationId: string,
    requestedBy: string,
    reason: string,
    now = Date.now(),
): Promise<string> {
    const conversation = await env.CHAT_DB.prepare(`
        SELECT status, closed_at, archived_at, archive_at, purge_at
        FROM chat_conversations WHERE id = ?
    `).bind(conversationId).first<{
        status: string;
        closed_at: number | null;
        archived_at: number | null;
        archive_at: number | null;
        purge_at: number | null;
    }>();
    if (!conversation) {
        const existing = await env.CHAT_DB.prepare(
            'SELECT id FROM chat_deletion_jobs WHERE conversation_id = ?',
        ).bind(conversationId).first<{ id: string }>();
        if (existing) return existing.id;
        throw new Error('Conversation not found for deletion');
    }
    const id = `del_${crypto.randomUUID()}`;
    await env.CHAT_DB.prepare(`
        INSERT INTO chat_deletion_jobs (
            id, conversation_id, requested_by, reason, status,
            previous_status, previous_closed_at, previous_archived_at,
            previous_archive_at, previous_purge_at,
            attempts, created_at, updated_at
        ) VALUES (?, ?, ?, ?, 'PENDING', ?, ?, ?, ?, ?, 0, ?, ?)
        ON CONFLICT(conversation_id) DO UPDATE SET
            requested_by = excluded.requested_by,
            reason = excluded.reason,
            updated_at = excluded.updated_at
    `).bind(
        id, conversationId, requestedBy, reason,
        conversation.status, conversation.closed_at, conversation.archived_at,
        conversation.archive_at, conversation.purge_at,
        now, now,
    ).run();
    const row = await env.CHAT_DB.prepare(
        'SELECT id FROM chat_deletion_jobs WHERE conversation_id = ?',
    ).bind(conversationId).first<{ id: string }>();
    return row?.id || id;
}

async function gateDeletionJob(
    env: SupportRealtimeEnv,
    job: DeletionJob,
    now: number,
    executeAt: number | null,
): Promise<void> {
    await env.CHAT_DB.prepare(`
        UPDATE chat_conversations
        SET status = 'PURGE_PENDING', purge_requested_at = ?, purge_at = ?,
            deletion_reason = ?, updated_at = ?
        WHERE id = ? AND status != 'PURGE_PENDING'
    `).bind(now, executeAt ?? now, job.reason, now, job.conversation_id).run();
    await internalPost(env, job.conversation_id, '/internal/system/conversations/purge/request', {
        reason: job.reason,
        requestedAt: now,
        purgeAt: executeAt ?? now,
    });
    await env.CHAT_DB.prepare(`
        UPDATE chat_deletion_jobs
        SET status = 'GATED', next_attempt_at = ?, updated_at = ?, last_error = NULL
        WHERE id = ?
    `).bind(executeAt, now, job.id).run();
}

export async function prepareDeletionJob(
    env: SupportRealtimeEnv,
    job: DeletionJob,
    executeAt: number | null,
    now = Date.now(),
): Promise<boolean> {
    try {
        await gateDeletionJob(env, job, now, executeAt);
        return true;
    } catch (error) {
        const attempts = job.attempts + 1;
        await env.CHAT_DB.prepare(`
            UPDATE chat_deletion_jobs
            SET attempts = ?, next_attempt_at = ?, last_error = ?, updated_at = ?
            WHERE id = ?
        `).bind(
            attempts,
            now + retryDelay(attempts),
            (error instanceof Error ? error.message : String(error)).slice(0, 500),
            now,
            job.id,
        ).run();
        return false;
    }
}

export async function processDeletionJob(
    env: SupportRealtimeEnv,
    job: DeletionJob,
    now = Date.now(),
): Promise<boolean> {
    const startedAt = Date.now();
    let status = job.status;
    try {
        if (status === 'PENDING' || status === 'FAILED') {
            await gateDeletionJob(env, job, now, null);
            status = 'GATED';
        }

        if (status === 'GATED') {
            await internalPost(env, job.conversation_id, '/internal/system/conversations/purge/finalize', {});
            await env.CHAT_DB.prepare(`
                UPDATE chat_deletion_jobs
                SET status = 'DO_DELETED', next_attempt_at = NULL, updated_at = ?, last_error = NULL
                WHERE id = ?
            `).bind(now, job.id).run();
            status = 'DO_DELETED';
        }

        if (status === 'DO_DELETED') {
            await env.CHAT_DB.batch([
                env.CHAT_DB.prepare(`
                    INSERT INTO chat_conversation_tombstones (conversation_id, purged_at, deletion_reason)
                    VALUES (?, ?, ?)
                    ON CONFLICT(conversation_id) DO UPDATE SET
                        purged_at = excluded.purged_at,
                        deletion_reason = excluded.deletion_reason
                `).bind(job.conversation_id, now, job.reason),
                env.CHAT_DB.prepare('DELETE FROM chat_conversations WHERE id = ?').bind(job.conversation_id),
            ]);
            await notifyPurgeComplete(env, job, now);
            await env.CHAT_DB.prepare(`
                UPDATE chat_deletion_jobs
                SET status = 'COMPLETE', completed_at = ?, updated_at = ?, last_error = NULL
                WHERE id = ?
            `).bind(now, now, job.id).run();
            emitMetric('chat_purge_completed_total');
            emitMetric('chat_purge_duration_ms', Date.now() - startedAt);
        }
        return true;
    } catch (error) {
        const attempts = job.attempts + 1;
        await env.CHAT_DB.prepare(`
            UPDATE chat_deletion_jobs
            SET attempts = ?, next_attempt_at = ?, last_error = ?, updated_at = ?
            WHERE id = ?
        `).bind(
            attempts,
            now + retryDelay(attempts),
            (error instanceof Error ? error.message : String(error)).slice(0, 500),
            now,
            job.id,
        ).run();
        console.error('[chat-retention] deletion job failed', { jobId: job.id, attempts });
        emitMetric('chat_purge_failed_total', 1, { attempts });
        return false;
    }
}

export async function runRetention(env: SupportRealtimeEnv): Promise<RetentionResult> {
    const startedAt = Date.now();
    const config = readChatConfig(env as unknown as Record<string, string | undefined>);
    const now = Date.now();
    let archived = 0;
    let purgeRequested = 0;
    let purged = 0;

    const archiveRows = await env.CHAT_DB.prepare(`
        SELECT id FROM chat_conversations
        WHERE status = 'CLOSED' AND archive_at IS NOT NULL AND archive_at <= ?
        ORDER BY archive_at ASC LIMIT ?
    `).bind(now, config.batchSize).all<{ id: string }>();
    for (const row of archiveRows.results || []) {
        try {
            await internalPost(env, row.id, '/internal/system/conversations/state', {
                status: 'ARCHIVED', updatedAt: now,
            });
            archived += 1;
            emitMetric('chat_conversation_archived_total');
        } catch {
            console.error('[chat-retention] archive failed', { conversationId: row.id });
        }
    }

    const purgeRows = await env.CHAT_DB.prepare(`
        SELECT id, status FROM chat_conversations
        WHERE status IN ('ARCHIVED','SPAM') AND purge_at IS NOT NULL AND purge_at <= ?
        ORDER BY purge_at ASC LIMIT ?
    `).bind(now, config.batchSize).all<{ id: string; status: string }>();
    for (const row of purgeRows.results || []) {
        await enqueueDeletionJob(env, row.id, 'system:retention',
            row.status === 'SPAM' ? 'spam_retention' : 'retention', now);
        purgeRequested += 1;
        emitMetric('chat_purge_requested_total');
    }

    const jobs = await env.CHAT_DB.prepare(`
        SELECT id, conversation_id, reason, status, attempts
        FROM chat_deletion_jobs
        WHERE status IN ('PENDING','GATED','DO_DELETED','FAILED')
          AND (next_attempt_at IS NULL OR next_attempt_at <= ?)
        ORDER BY created_at ASC LIMIT ?
    `).bind(now, config.batchSize).all<DeletionJob>();
    for (const job of jobs.results || []) {
        if (await processDeletionJob(env, job, now)) purged += 1;
    }

    const tombstoneCutoff = now - config.tombstoneRetentionDays * 86_400_000;
    await env.CHAT_DB.prepare(`
        DELETE FROM chat_conversation_tombstones
        WHERE purged_at < ? AND conversation_id NOT IN (
            SELECT conversation_id FROM chat_deletion_jobs WHERE status != 'COMPLETE'
        )
    `).bind(tombstoneCutoff).run();
    await env.CHAT_DB.prepare('DELETE FROM chat_rate_buckets WHERE expires_at < ?').bind(now).run();

    emitMetric('chat_retention_batch_total');
    emitMetric('chat_retention_batch_duration_ms', Date.now() - startedAt);
    return { archived, purgeRequested, purged };
}
