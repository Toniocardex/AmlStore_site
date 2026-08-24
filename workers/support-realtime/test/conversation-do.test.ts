import { env } from 'cloudflare:test';
import { beforeEach, describe, expect, it } from 'vitest';
import { createId } from '../../../support/shared/ids';
import { enqueueDeletionJob, prepareDeletionJob, processDeletionJob, runRetention } from '../src/retention';
import { projectOutboxEvent } from '../src/projection';

beforeEach(async () => {
    const queries = JSON.parse(env.CHAT_CORE_MIGRATION_QUERIES) as string[];
    await env.CHAT_DB.batch(queries.map((query) => env.CHAT_DB.prepare(query)));
});

function createPayload(conversationId: string, visitorId: string, clientMessageId: string) {
    return {
        conversationId,
        visitorId,
        clientMessageId,
        body: 'First guest message',
        contactName: 'Mario',
        contactEmail: 'mario@example.com',
        contactEmailLookupHash: 'test-hash',
        contactVerifiedAt: null,
        pagePath: '/it/office-2024-home-business',
        productId: 'office-2024-hb',
        orderId: null,
        locale: 'it',
        countryCode: 'IT',
        createdAt: Date.now(),
    };
}

describe('ConversationDurableObject', () => {
    it('atomically creates the conversation and returns the same logical message on retry', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const clientMessageId = createId('message');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        const body = JSON.stringify(createPayload(conversationId, visitorId, clientMessageId));

        const first = await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body,
        });
        expect(first.status).toBe(201);
        const firstEvent = await first.json<Record<string, unknown>>();

        const retry = await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body,
        });
        expect(retry.status).toBe(201);
        const retryEvent = await retry.json<Record<string, unknown>>();
        expect(retryEvent.eventId).toBe(firstEvent.eventId);
        expect(retryEvent.seq).toBe(1);
        expect((retryEvent.payload as Record<string, unknown>).messageId)
            .toBe((firstEvent.payload as Record<string, unknown>).messageId);

        const projection = await env.CHAT_DB.prepare(`
            SELECT visitor_id, customer_id, last_seq, projection_version
            FROM chat_conversations WHERE id = ?
        `).bind(conversationId).first<{
            visitor_id: string;
            customer_id: string | null;
            last_seq: number;
            projection_version: number;
        }>();
        expect(projection).toMatchObject({
            visitor_id: visitorId,
            customer_id: null,
            last_seq: 1,
            projection_version: 1,
        });
    });

    it('does not reveal a conversation to another visitor', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(createPayload(conversationId, visitorId, createId('message'))),
        });
        const response = await stub.fetch('https://internal/internal/conversations/detail', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ conversationId, visitorId: createId('visitor') }),
        });
        expect(response.status).toBe(404);
    });

    it('sends subsequent messages idempotently and advances the D1 projection', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(createPayload(conversationId, visitorId, createId('message'))),
        });
        const clientMessageId = createId('message');
        const payload = JSON.stringify({
            conversationId,
            visitorId,
            clientMessageId,
            body: 'Second guest message',
            createdAt: Date.now() + 1,
        });
        const first = await stub.fetch('https://internal/internal/conversations/messages/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: payload,
        });
        const retry = await stub.fetch('https://internal/internal/conversations/messages/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: payload,
        });
        expect(first.status).toBe(201);
        expect(retry.status).toBe(201);
        const firstEvent = await first.json<Record<string, unknown>>();
        const retryEvent = await retry.json<Record<string, unknown>>();
        expect(retryEvent.eventId).toBe(firstEvent.eventId);
        expect(retryEvent.seq).toBe(2);

        await expect.poll(async () => env.CHAT_DB.prepare(`
                SELECT last_seq, projection_version, last_message_preview
                FROM chat_conversations WHERE id = ?
            `).bind(conversationId).first<{
                last_seq: number;
                projection_version: number;
                last_message_preview: string;
            }>(), { timeout: 2_000 }).toMatchObject({
                last_seq: 2,
                projection_version: 2,
                last_message_preview: 'Second guest message',
            });
    });

    it('upgrades only the owning guest to a hibernating WebSocket', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(createPayload(conversationId, visitorId, createId('message'))),
        });

        const denied = await stub.fetch(
            `https://internal/internal/conversations/ws?conversationId=${conversationId}`
                + `&visitorId=${createId('visitor')}&lastKnownSeq=0`,
            { headers: { Upgrade: 'websocket' } },
        );
        expect(denied.status).toBe(404);

        const upgraded = await stub.fetch(
            `https://internal/internal/conversations/ws?conversationId=${conversationId}`
                + `&visitorId=${visitorId}&lastKnownSeq=0`,
            { headers: { Upgrade: 'websocket' } },
        );
        expect(upgraded.status).toBe(101);
        expect(upgraded.webSocket).toBeTruthy();
        upgraded.webSocket?.accept();
        upgraded.webSocket?.close(1000, 'test complete');
    });

    it('commits an idempotent operator reply and exposes it to the owning guest', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const operatorId = createId('operator');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(createPayload(conversationId, visitorId, createId('message'))),
        });
        const clientMessageId = createId('message');
        const reply = JSON.stringify({
            conversationId,
            operatorId,
            clientMessageId,
            body: 'Operator reply',
            createdAt: Date.now() + 1,
        });
        const first = await stub.fetch('https://internal/internal/admin/conversations/messages/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: reply,
        });
        const retry = await stub.fetch('https://internal/internal/admin/conversations/messages/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: reply,
        });
        expect(first.status).toBe(201);
        expect(retry.status).toBe(201);
        expect((await retry.json<Record<string, unknown>>()).eventId)
            .toBe((await first.json<Record<string, unknown>>()).eventId);

        const history = await stub.fetch('https://internal/internal/conversations/messages', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ conversationId, visitorId, limit: 50 }),
        });
        const result = await history.json<{ messages: Array<Record<string, unknown>> }>();
        expect(result.messages).toHaveLength(2);
        expect(result.messages[1]).toMatchObject({
            senderType: 'operator',
            body: 'Operator reply',
        });
        await expect.poll(async () => env.CHAT_DB.prepare(`
            SELECT visitor_unread_count FROM chat_conversations WHERE id = ?
        `).bind(conversationId).first<{ visitor_unread_count: number }>()).toMatchObject({
            visitor_unread_count: 1,
        });
    });

    it('projects lifecycle and assignment, then reopens on a new guest message', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const operatorId = createId('operator');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        const createdAt = Date.now();
        await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...createPayload(conversationId, visitorId, createId('message')),
                createdAt,
            }),
        });
        const assignment = await stub.fetch('https://internal/internal/admin/conversations/assignment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                conversationId,
                operatorId,
                assignedOperatorId: operatorId,
                updatedAt: createdAt + 1,
            }),
        });
        expect(assignment.status).toBe(200);
        const closed = await stub.fetch('https://internal/internal/admin/conversations/state', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                conversationId,
                operatorId,
                status: 'CLOSED',
                updatedAt: createdAt + 2,
            }),
        });
        expect(closed.status).toBe(200);

        const reopened = await stub.fetch('https://internal/internal/conversations/messages/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                conversationId,
                visitorId,
                clientMessageId: createId('message'),
                body: 'I still need help',
                createdAt: createdAt + 3,
            }),
        });
        expect(reopened.status).toBe(201);

        // La riapertura azzera i timer di lifecycle (ADR §29) e non perde l'assegnazione.
        await expect.poll(async () => env.CHAT_DB.prepare(`
            SELECT status, assigned_operator_id, last_seq, closed_at, archive_at, purge_at
            FROM chat_conversations WHERE id = ?
        `).bind(conversationId).first<Record<string, unknown>>()).toMatchObject({
            status: 'OPEN',
            assigned_operator_id: operatorId,
            last_seq: 2,
            closed_at: null,
            archive_at: null,
            purge_at: null,
        });
    });

    it('moves to PENDING on an operator reply and back to OPEN on the visitor answer', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const operatorId = createId('operator');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        const createdAt = Date.now();
        await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...createPayload(conversationId, visitorId, createId('message')),
                createdAt,
            }),
        });

        const reply = await stub.fetch('https://internal/internal/admin/conversations/messages/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                conversationId,
                operatorId,
                clientMessageId: createId('message'),
                body: 'Ti rispondo subito',
                createdAt: createdAt + 1,
            }),
        });
        expect(reply.status).toBe(201);
        await expect.poll(async () => env.CHAT_DB.prepare(`
            SELECT status, last_seq, last_message_sender FROM chat_conversations WHERE id = ?
        `).bind(conversationId).first<Record<string, unknown>>()).toMatchObject({
            status: 'PENDING',
            last_seq: 2,
            last_message_sender: 'operator',
        });

        const answer = await stub.fetch('https://internal/internal/conversations/messages/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                conversationId,
                visitorId,
                clientMessageId: createId('message'),
                body: 'Grazie, aspetto',
                createdAt: createdAt + 2,
            }),
        });
        expect(answer.status).toBe(201);
        await expect.poll(async () => env.CHAT_DB.prepare(`
            SELECT status, last_seq, last_message_sender FROM chat_conversations WHERE id = ?
        `).bind(conversationId).first<Record<string, unknown>>()).toMatchObject({
            status: 'OPEN',
            last_seq: 3,
            last_message_sender: 'visitor',
        });
    });

    it('schedules the purge from closed_at and does not restart it when archiving', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const operatorId = createId('operator');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        const createdAt = Date.now();
        await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...createPayload(conversationId, visitorId, createId('message')),
                createdAt,
            }),
        });
        const closedAt = createdAt + 2;
        await stub.fetch('https://internal/internal/admin/conversations/state', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ conversationId, operatorId, status: 'CLOSED', updatedAt: closedAt }),
        });
        const day = 86_400_000;
        const archiveAfterDays = Number(env.CHAT_ARCHIVE_AFTER_DAYS || 30);
        const retentionDays = Number(env.CHAT_RETENTION_DAYS || 180);
        // ADR §69.2: entrambe le scadenze decorrono da closed_at.
        await expect.poll(async () => env.CHAT_DB.prepare(`
            SELECT status, closed_at, archive_at, purge_at FROM chat_conversations WHERE id = ?
        `).bind(conversationId).first<Record<string, unknown>>()).toMatchObject({
            status: 'CLOSED',
            closed_at: closedAt,
            archive_at: closedAt + archiveAfterDays * day,
            purge_at: closedAt + retentionDays * day,
        });

        await stub.fetch('https://internal/internal/system/conversations/state', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ conversationId, status: 'ARCHIVED', updatedAt: closedAt + day }),
        });
        // L'archiviazione non fa ripartire la retention dal momento dell'archiviazione.
        await expect.poll(async () => env.CHAT_DB.prepare(`
            SELECT status, closed_at, purge_at FROM chat_conversations WHERE id = ?
        `).bind(conversationId).first<Record<string, unknown>>()).toMatchObject({
            status: 'ARCHIVED',
            closed_at: closedAt,
            purge_at: closedAt + retentionDays * day,
        });
    });

    it('purges through the write gate and a tombstone rejects stale projections', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(createPayload(conversationId, visitorId, createId('message'))),
        });
        await expect.poll(async () => env.CHAT_DB.prepare(
            'SELECT id FROM chat_conversations WHERE id = ?',
        ).bind(conversationId).first()).toMatchObject({ id: conversationId });
        const jobId = await enqueueDeletionJob(env, conversationId, 'operator:test', 'test_purge');
        const job = await env.CHAT_DB.prepare(`
            SELECT id, conversation_id, reason, status, attempts
            FROM chat_deletion_jobs WHERE id = ?
        `).bind(jobId).first<{
            id: string;
            conversation_id: string;
            reason: string;
            status: 'PENDING';
            attempts: number;
        }>();
        expect(job).toBeTruthy();
        expect(await processDeletionJob(env, job!)).toBe(true);

        expect(await env.CHAT_DB.prepare(
            'SELECT id FROM chat_conversations WHERE id = ?',
        ).bind(conversationId).first()).toBeNull();
        expect(await env.CHAT_DB.prepare(
            'SELECT conversation_id FROM chat_conversation_tombstones WHERE conversation_id = ?',
        ).bind(conversationId).first()).toMatchObject({ conversation_id: conversationId });
        expect(await env.CHAT_DB.prepare(
            'SELECT status FROM chat_deletion_jobs WHERE id = ?',
        ).bind(jobId).first()).toMatchObject({ status: 'COMPLETE' });

        const rejectedWrite = await stub.fetch('https://internal/internal/conversations/messages/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                conversationId,
                visitorId,
                clientMessageId: createId('message'),
                body: 'Must not survive',
                createdAt: Date.now(),
            }),
        });
        expect(rejectedWrite.status).toBe(404);

        const stale = await projectOutboxEvent(env, {
            eventId: createId('event'),
            eventType: 'conversation.created',
            seq: 1,
            projectionVersion: 99,
            payloadJson: JSON.stringify({
                ...createPayload(conversationId, visitorId, createId('message')),
                messageId: createId('message'),
            }),
        });
        expect(stale).toBe('discarded');
        expect(await env.CHAT_DB.prepare(
            'SELECT id FROM chat_conversations WHERE id = ?',
        ).bind(conversationId).first()).toBeNull();
    });

    it('gates immediately and can cancel a deletion during its grace period', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(createPayload(conversationId, visitorId, createId('message'))),
        });
        await expect.poll(async () => env.CHAT_DB.prepare(
            'SELECT status FROM chat_conversations WHERE id = ?',
        ).bind(conversationId).first()).toMatchObject({ status: 'OPEN' });
        const jobId = await enqueueDeletionJob(env, conversationId, 'operator:test', 'manual_admin_delete');
        const job = await env.CHAT_DB.prepare(`
            SELECT id, conversation_id, reason, status,
                   previous_status, previous_closed_at, previous_archived_at,
                   previous_archive_at, previous_purge_at, attempts
            FROM chat_deletion_jobs WHERE id = ?
        `).bind(jobId).first<any>();
        const executeAt = Date.now() + 86_400_000;
        expect(await prepareDeletionJob(env, job, executeAt)).toBe(true);
        expect(await env.CHAT_DB.prepare(`
            SELECT status FROM chat_conversations WHERE id = ?
        `).bind(conversationId).first()).toMatchObject({ status: 'PURGE_PENDING' });

        const blocked = await stub.fetch('https://internal/internal/conversations/messages/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                conversationId, visitorId, clientMessageId: createId('message'),
                body: 'Must remain blocked', createdAt: Date.now(),
            }),
        });
        expect(blocked.status).toBe(409);

        const cancelled = await stub.fetch('https://internal/internal/system/conversations/purge/cancel', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                conversationId,
                previousStatus: job.previous_status,
                previousClosedAt: job.previous_closed_at,
                previousArchivedAt: job.previous_archived_at,
                previousArchiveAt: job.previous_archive_at,
                previousPurgeAt: job.previous_purge_at,
                updatedAt: Date.now(),
            }),
        });
        expect(cancelled.ok).toBe(true);
        await expect.poll(async () => env.CHAT_DB.prepare(
            'SELECT status FROM chat_conversations WHERE id = ?',
        ).bind(conversationId).first()).toMatchObject({ status: 'OPEN' });
    });

    it('archives and purges due conversations in bounded scheduled passes', async () => {
        const conversationId = createId('conversation');
        const visitorId = createId('visitor');
        const operatorId = createId('operator');
        const stub = env.CHAT_CONVERSATIONS.get(
            env.CHAT_CONVERSATIONS.idFromName(`conversation:${conversationId}`),
        );
        const now = Date.now();
        await stub.fetch('https://internal/internal/conversations/create', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(createPayload(conversationId, visitorId, createId('message'))),
        });
        await stub.fetch('https://internal/internal/admin/conversations/state', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ conversationId, operatorId, status: 'CLOSED', updatedAt: now }),
        });
        await expect.poll(async () => env.CHAT_DB.prepare(
            'SELECT status FROM chat_conversations WHERE id = ?',
        ).bind(conversationId).first()).toMatchObject({ status: 'CLOSED' });
        await env.CHAT_DB.prepare(
            'UPDATE chat_conversations SET archive_at = ? WHERE id = ?',
        ).bind(now - 1, conversationId).run();

        const archivePass = await runRetention(env);
        expect(archivePass.archived).toBeGreaterThanOrEqual(1);
        await expect.poll(async () => env.CHAT_DB.prepare(
            'SELECT status FROM chat_conversations WHERE id = ?',
        ).bind(conversationId).first()).toMatchObject({ status: 'ARCHIVED' });
        await env.CHAT_DB.prepare(
            'UPDATE chat_conversations SET purge_at = ? WHERE id = ?',
        ).bind(now - 1, conversationId).run();

        const purgePass = await runRetention(env);
        expect(purgePass.purgeRequested).toBeGreaterThanOrEqual(1);
        expect(await env.CHAT_DB.prepare(
            'SELECT conversation_id FROM chat_conversation_tombstones WHERE conversation_id = ?',
        ).bind(conversationId).first()).toMatchObject({ conversation_id: conversationId });
        const retryPass = await runRetention(env);
        expect(retryPass.purgeRequested).toBe(0);
    });
});
