import { createExecutionContext, env, waitOnExecutionContext } from 'cloudflare:test';
import { beforeEach, describe, expect, it } from 'vitest';
import worker from '../src/index';

beforeEach(async () => {
    const queries = JSON.parse(env.CHAT_CORE_MIGRATION_QUERIES) as string[];
    await env.CHAT_DB.batch(queries.map((query) => env.CHAT_DB.prepare(query)));
});

describe('scheduled retention gate', () => {
    it('does not touch D1 when CHAT_ENABLED is 0', async () => {
        expect(env.CHAT_ENABLED).toBe('0');
        const ctx = createExecutionContext();
        await worker.scheduled(
            { cron: '*/15 * * * *' } as ScheduledController,
            env,
            ctx,
        );
        await waitOnExecutionContext(ctx);
        // Nessuna query di retention deve essere partita: la tabella non ha
        // ricevuto scritture (nessuna riga da archiviare/purgare, nessun batch job).
        const jobs = await env.CHAT_DB.prepare('SELECT COUNT(*) AS total FROM chat_deletion_jobs')
            .first<{ total: number }>();
        expect(jobs?.total).toBe(0);
    });

    it('runs the retention batch when CHAT_ENABLED is 1', async () => {
        const enabledEnv = { ...env, CHAT_ENABLED: '1' };
        const now = Date.now();
        await env.CHAT_DB.prepare(`
            INSERT INTO chat_conversations (
                id, visitor_id, status, last_seq, projection_version,
                purge_at, created_at, updated_at
            ) VALUES ('conv_ret_test', 'vis_ret_test', 'ARCHIVED', 1, 1, ?, ?, ?)
        `).bind(now - 1_000, now, now).run();

        const ctx = createExecutionContext();
        await worker.scheduled({ cron: '*/15 * * * *' } as ScheduledController, enabledEnv, ctx);
        await waitOnExecutionContext(ctx);

        const jobs = await env.CHAT_DB.prepare('SELECT COUNT(*) AS total FROM chat_deletion_jobs')
            .first<{ total: number }>();
        expect(jobs?.total).toBe(1);
    });
});
