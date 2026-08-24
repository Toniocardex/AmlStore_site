import { ChatProtocolError } from './errors';

export const CONVERSATION_STATUSES = [
    'OPEN',
    'PENDING',
    'CLOSED',
    'ARCHIVED',
    'SPAM',
    'PURGE_PENDING',
] as const;

export type ConversationStatus = (typeof CONVERSATION_STATUSES)[number];

const ALLOWED_TRANSITIONS: Record<ConversationStatus, ReadonlySet<ConversationStatus>> = {
    OPEN: new Set(['PENDING', 'CLOSED', 'SPAM', 'PURGE_PENDING']),
    PENDING: new Set(['OPEN', 'CLOSED', 'SPAM', 'PURGE_PENDING']),
    CLOSED: new Set(['OPEN', 'ARCHIVED', 'SPAM', 'PURGE_PENDING']),
    ARCHIVED: new Set(['OPEN', 'SPAM', 'PURGE_PENDING']),
    SPAM: new Set(['PURGE_PENDING']),
    PURGE_PENDING: new Set(),
};

export function isConversationStatus(value: unknown): value is ConversationStatus {
    return typeof value === 'string'
        && (CONVERSATION_STATUSES as readonly string[]).includes(value);
}

export function assertTransition(from: ConversationStatus, to: ConversationStatus): void {
    if (from === to) return;
    if (!ALLOWED_TRANSITIONS[from].has(to)) {
        throw new ChatProtocolError(
            from === 'PURGE_PENDING' ? 'CONVERSATION_PURGE_PENDING' : 'INVALID_PAYLOAD',
            `Invalid conversation transition: ${from} -> ${to}`,
            409,
        );
    }
}

export interface RetentionPolicy {
    archiveAfterDays: number;
    retentionDays: number;
    spamRetentionDays: number;
    deleteGraceDays: number;
    tombstoneRetentionDays: number;
    batchSize: number;
}

export function validateRetentionPolicy(policy: RetentionPolicy): RetentionPolicy {
    const positive = [
        policy.archiveAfterDays,
        policy.retentionDays,
        policy.spamRetentionDays,
        policy.tombstoneRetentionDays,
        policy.batchSize,
    ];
    if (positive.some((value) => !Number.isInteger(value) || value <= 0)) {
        throw new Error('Retention values must be positive integers');
    }
    if (!Number.isInteger(policy.deleteGraceDays) || policy.deleteGraceDays < 0) {
        throw new Error('CHAT_DELETE_GRACE_DAYS must be a non-negative integer');
    }
    if (policy.archiveAfterDays >= policy.retentionDays) {
        throw new Error('CHAT_ARCHIVE_AFTER_DAYS must be less than CHAT_RETENTION_DAYS');
    }
    if (policy.batchSize > 500) {
        throw new Error('CHAT_RETENTION_BATCH_SIZE must not exceed 500');
    }
    return policy;
}
