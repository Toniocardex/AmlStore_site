export type ChatMetricName =
    | 'chat_conversation_created_total'
    | 'chat_message_created_total'
    | 'chat_ws_connected'
    | 'chat_ws_reconnect_total'
    | 'chat_projection_retry_total'
    | 'chat_push_sent_total'
    | 'chat_push_failed_total'
    | 'chat_rate_limited_total'
    | 'chat_conversation_archived_total'
    | 'chat_purge_requested_total'
    | 'chat_purge_completed_total'
    | 'chat_purge_failed_total'
    | 'chat_retention_batch_total'
    | 'chat_tombstone_discarded_event_total'
    | 'chat_error_total'
    | 'chat_message_persistence_latency_ms'
    | 'chat_projection_latency_ms'
    | 'chat_push_dispatch_latency_ms'
    | 'chat_retention_batch_duration_ms'
    | 'chat_purge_duration_ms';

export function emitMetric(
    name: ChatMetricName,
    value = 1,
    attributes: Record<string, string | number | boolean | null> = {},
): void {
    console.log('[chat-metric]', JSON.stringify({
        name,
        value,
        timestamp: Date.now(),
        attributes,
    }));
}
