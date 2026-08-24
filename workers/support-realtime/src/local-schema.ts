export const CONVERSATION_SCHEMA = `
CREATE TABLE IF NOT EXISTS messages (
    seq INTEGER PRIMARY KEY AUTOINCREMENT,
    id TEXT NOT NULL UNIQUE,
    client_message_id TEXT,
    sender_type TEXT NOT NULL,
    sender_id TEXT NOT NULL,
    message_type TEXT NOT NULL DEFAULT 'text',
    body_text TEXT NOT NULL,
    created_at INTEGER NOT NULL,
    UNIQUE(sender_id, client_message_id)
);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);

CREATE TABLE IF NOT EXISTS participant_state (
    participant_key TEXT PRIMARY KEY,
    last_read_seq INTEGER NOT NULL DEFAULT 0,
    updated_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS outbox (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    seq INTEGER,
    projection_version INTEGER NOT NULL,
    payload_json TEXT NOT NULL,
    projected_at INTEGER,
    hub_notified_at INTEGER,
    attempts INTEGER NOT NULL DEFAULT 0,
    next_attempt_at INTEGER,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_outbox_pending
ON outbox(projected_at, hub_notified_at, next_attempt_at, created_at);

CREATE TABLE IF NOT EXISTS conversation_local_state (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS message_rate_limits (
    participant_key TEXT PRIMARY KEY,
    window_start INTEGER NOT NULL,
    message_count INTEGER NOT NULL
);
`;
