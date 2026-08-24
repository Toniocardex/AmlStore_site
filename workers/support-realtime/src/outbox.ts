import type { SupportRealtimeEnv } from './env';
import { projectOutboxEvent, type StoredOutboxEvent } from './projection';
import { emitMetric } from './observability';

interface OutboxRow {
    [key: string]: SqlStorageValue;
    event_id: string;
    event_type: string;
    seq: number | null;
    projection_version: number;
    payload_json: string;
    projected_at: number | null;
    hub_notified_at: number | null;
    attempts: number;
}

export interface OutboxHost {
    readonly ctx: DurableObjectState;
    readonly env: SupportRealtimeEnv;
}

function retryDelay(attempts: number): number {
    return Math.min(60_000, 1_000 * (2 ** Math.min(attempts, 6)));
}

async function notifyHub(env: SupportRealtimeEnv, event: StoredOutboxEvent): Promise<void> {
    const hub = env.SUPPORT_HUB.get(env.SUPPORT_HUB.idFromName('support-hub:default'));
    const response = await hub.fetch(new Request('https://internal/internal/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            v: 1,
            type: event.eventType,
            eventId: event.eventId,
            seq: event.seq,
            projectionVersion: event.projectionVersion,
            payload: JSON.parse(event.payloadJson),
        }),
    }));
    if (!response.ok) throw new Error(`SupportHub notification failed: ${response.status}`);
}

export async function scheduleOutbox(host: OutboxHost, when = Date.now() + 1_000): Promise<void> {
    const current = await host.ctx.storage.getAlarm();
    if (current == null || current > when) await host.ctx.storage.setAlarm(when);
}

export async function drainOutbox(host: OutboxHost): Promise<void> {
    const now = Date.now();
    const rows = host.ctx.storage.sql.exec<OutboxRow>(`
        SELECT event_id, event_type, seq, projection_version, payload_json,
               projected_at, hub_notified_at, attempts
        FROM outbox
        WHERE (projected_at IS NULL OR hub_notified_at IS NULL)
          AND (next_attempt_at IS NULL OR next_attempt_at <= ?)
        ORDER BY created_at ASC, rowid ASC
        LIMIT 20
    `, now).toArray();

    let nextAlarm: number | null = null;
    for (const row of rows) {
        const event: StoredOutboxEvent = {
            eventId: row.event_id,
            eventType: row.event_type,
            seq: row.seq,
            projectionVersion: row.projection_version,
            payloadJson: row.payload_json,
        };
        try {
            if (row.projected_at == null) {
                const projectionStartedAt = Date.now();
                await projectOutboxEvent(host.env, event);
                emitMetric('chat_projection_latency_ms', Date.now() - projectionStartedAt, { eventType: event.eventType });
                host.ctx.storage.sql.exec(
                    'UPDATE outbox SET projected_at = ? WHERE event_id = ? AND projected_at IS NULL',
                    Date.now(), row.event_id,
                );
            }
            if (row.hub_notified_at == null) {
                await notifyHub(host.env, event);
                host.ctx.storage.sql.exec(
                    'UPDATE outbox SET hub_notified_at = ? WHERE event_id = ? AND hub_notified_at IS NULL',
                    Date.now(), row.event_id,
                );
            }
        } catch (error) {
            const attempts = row.attempts + 1;
            const retryAt = Date.now() + retryDelay(attempts);
            host.ctx.storage.sql.exec(
                'UPDATE outbox SET attempts = ?, next_attempt_at = ? WHERE event_id = ?',
                attempts, retryAt, row.event_id,
            );
            nextAlarm = nextAlarm == null ? retryAt : Math.min(nextAlarm, retryAt);
            console.error('[chat-outbox] delivery failed', {
                eventId: row.event_id,
                eventType: row.event_type,
                attempts,
                error: error instanceof Error ? error.message : String(error),
            });
            emitMetric('chat_projection_retry_total', 1, { eventType: row.event_type, attempts });
            emitMetric('chat_error_total', 1, { component: 'outbox', eventType: row.event_type });
            // L'outbox è per conversazione e le projection D1 sono protette da guardie
            // monotone (`last_seq`, `projection_version`): consegnare un evento successivo
            // mentre uno precedente è in retry lo renderebbe definitivamente scartabile.
            // Si interrompe il drain e si riparte dall'evento fallito al prossimo alarm.
            break;
        }
    }

    const pending = host.ctx.storage.sql.exec<{ next_attempt_at: number | null }>(`
        SELECT MIN(COALESCE(next_attempt_at, ?)) AS next_attempt_at
        FROM outbox
        WHERE projected_at IS NULL OR hub_notified_at IS NULL
    `, Date.now() + 1_000).toArray()[0]?.next_attempt_at;
    if (pending != null) nextAlarm = nextAlarm == null ? pending : Math.min(nextAlarm, pending);
    if (nextAlarm != null) await scheduleOutbox(host, nextAlarm);
}
