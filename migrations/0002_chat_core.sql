-- ADR-CHAT-001 rev1.2 — support chat query model (core)
-- Additive and safe to apply before enabling the feature.

CREATE TABLE IF NOT EXISTS chat_conversations (
    id                          TEXT PRIMARY KEY,
    visitor_id                  TEXT NOT NULL,
    customer_id                 TEXT DEFAULT NULL,

    contact_name                TEXT,
    contact_email               TEXT,
    contact_email_lookup_hash   TEXT,
    contact_verified_at         INTEGER,

    status                      TEXT NOT NULL,
    assigned_operator_id        TEXT,

    locale                      TEXT,
    country_code                TEXT,
    product_id                  TEXT,
    order_id                    TEXT,
    page_path                   TEXT,

    last_seq                    INTEGER NOT NULL DEFAULT 0,
    projection_version          INTEGER NOT NULL DEFAULT 0,
    last_message_at             INTEGER,
    last_message_sender         TEXT,
    last_message_preview        TEXT,

    visitor_unread_count        INTEGER NOT NULL DEFAULT 0,
    operator_unread_count       INTEGER NOT NULL DEFAULT 0,

    closed_at                   INTEGER,
    archived_at                 INTEGER,
    archive_at                  INTEGER,
    purge_at                    INTEGER,
    purge_requested_at          INTEGER,
    deletion_reason             TEXT,

    created_at                  INTEGER NOT NULL,
    updated_at                  INTEGER NOT NULL,

    CHECK (customer_id IS NULL),
    CHECK (status IN ('OPEN', 'PENDING', 'CLOSED', 'ARCHIVED', 'SPAM', 'PURGE_PENDING'))
);

CREATE INDEX IF NOT EXISTS idx_chat_status_last_message
ON chat_conversations(status, last_message_at DESC, id DESC);

CREATE INDEX IF NOT EXISTS idx_chat_visitor
ON chat_conversations(visitor_id, last_message_at DESC, id DESC);

CREATE INDEX IF NOT EXISTS idx_chat_contact_lookup
ON chat_conversations(contact_email_lookup_hash, last_message_at DESC)
WHERE contact_email_lookup_hash IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_chat_order
ON chat_conversations(order_id);

CREATE INDEX IF NOT EXISTS idx_chat_assigned
ON chat_conversations(assigned_operator_id, status, last_message_at DESC, id DESC);

CREATE INDEX IF NOT EXISTS idx_chat_archive_due
ON chat_conversations(archive_at)
WHERE archive_at IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_chat_purge_due
ON chat_conversations(purge_at)
WHERE purge_at IS NOT NULL;

CREATE TABLE IF NOT EXISTS chat_conversation_tombstones (
    conversation_id TEXT PRIMARY KEY,
    purged_at INTEGER NOT NULL,
    deletion_reason TEXT
);

CREATE INDEX IF NOT EXISTS idx_chat_tombstones_purged_at
ON chat_conversation_tombstones(purged_at);

CREATE TABLE IF NOT EXISTS chat_rate_buckets (
    bucket_key TEXT NOT NULL,
    window_start INTEGER NOT NULL,
    request_count INTEGER NOT NULL,
    expires_at INTEGER NOT NULL,
    PRIMARY KEY (bucket_key, window_start)
);

CREATE INDEX IF NOT EXISTS idx_chat_rate_buckets_expires
ON chat_rate_buckets(expires_at);

CREATE TABLE IF NOT EXISTS chat_operators (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    role TEXT NOT NULL DEFAULT 'support',
    permissions_json TEXT NOT NULL DEFAULT '["support.*"]',
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS chat_deletion_jobs (
    id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL UNIQUE,
    requested_by TEXT NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'PENDING',
    previous_status TEXT,
    previous_closed_at INTEGER,
    previous_archived_at INTEGER,
    previous_archive_at INTEGER,
    previous_purge_at INTEGER,
    attempts INTEGER NOT NULL DEFAULT 0,
    next_attempt_at INTEGER,
    last_error TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    completed_at INTEGER,
    CHECK (status IN ('PENDING','GATED','DO_DELETED','COMPLETE','FAILED'))
);

CREATE INDEX IF NOT EXISTS idx_chat_deletion_jobs_pending
ON chat_deletion_jobs(status, next_attempt_at, created_at);

CREATE TABLE IF NOT EXISTS chat_push_subscriptions (
    id TEXT PRIMARY KEY,
    operator_id TEXT NOT NULL,
    device_id TEXT NOT NULL,
    endpoint TEXT NOT NULL UNIQUE,
    p256dh TEXT NOT NULL,
    auth TEXT NOT NULL,
    user_agent TEXT,
    enabled INTEGER NOT NULL DEFAULT 1,
    created_at INTEGER NOT NULL,
    last_used_at INTEGER,
    failed_at INTEGER
);

CREATE INDEX IF NOT EXISTS idx_push_operator
ON chat_push_subscriptions(operator_id, enabled);

CREATE TABLE IF NOT EXISTS chat_operator_preferences (
    operator_id TEXT PRIMARY KEY,
    notify_new_conversation INTEGER NOT NULL DEFAULT 1,
    notify_new_visitor_message INTEGER NOT NULL DEFAULT 1,
    notify_assigned_conversation INTEGER NOT NULL DEFAULT 1,
    sound_enabled INTEGER NOT NULL DEFAULT 1,
    push_preview_enabled INTEGER NOT NULL DEFAULT 0,
    availability_state TEXT NOT NULL DEFAULT 'OFFLINE',
    updated_at INTEGER NOT NULL,
    CHECK (availability_state IN ('ONLINE','BUSY','OFFLINE'))
);

CREATE TABLE IF NOT EXISTS chat_support_settings (
    settings_key TEXT PRIMARY KEY,
    public_availability_override TEXT NOT NULL DEFAULT 'AUTO',
    updated_by TEXT,
    updated_at INTEGER NOT NULL,
    CHECK (public_availability_override IN ('AUTO','ONLINE','OFFLINE'))
);

INSERT INTO chat_support_settings (settings_key, public_availability_override, updated_at)
VALUES ('default', 'AUTO', 0)
ON CONFLICT(settings_key) DO NOTHING;
