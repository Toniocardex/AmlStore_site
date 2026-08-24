export interface SupportRealtimeEnv {
    CHAT_CONVERSATIONS: DurableObjectNamespace;
    SUPPORT_HUB: DurableObjectNamespace;
    CHAT_DB: D1Database;
    CHAT_ENABLED?: string;
    CHAT_GUEST_SESSION_DAYS?: string;
    CHAT_GUEST_COOKIE_NAME?: string;
    CHAT_ARCHIVE_AFTER_DAYS?: string;
    CHAT_RETENTION_DAYS?: string;
    CHAT_SPAM_RETENTION_DAYS?: string;
    CHAT_DELETE_GRACE_DAYS?: string;
    CHAT_TOMBSTONE_RETENTION_DAYS?: string;
    CHAT_RETENTION_BATCH_SIZE?: string;
    CHAT_MAX_MESSAGE_LENGTH?: string;
    CHAT_GUEST_SESSION_SECRET?: string;
    CHAT_CONTACT_LOOKUP_SECRET?: string;
    VAPID_PUBLIC_KEY?: string;
    VAPID_PRIVATE_KEY?: string;
    VAPID_SUBJECT?: string;
    SITE_ORIGIN?: string;
}
