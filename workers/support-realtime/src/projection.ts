import type { SupportRealtimeEnv } from './env';
import { emitMetric } from './observability';

export interface StoredOutboxEvent {
    eventId: string;
    eventType: string;
    seq: number | null;
    projectionVersion: number;
    payloadJson: string;
}

interface ConversationCreatedProjection {
    conversationId: string;
    visitorId: string;
    contactName: string | null;
    contactEmail: string | null;
    contactEmailLookupHash: string | null;
    contactVerifiedAt: number | null;
    locale: string | null;
    countryCode: string | null;
    productId: string | null;
    orderId: string | null;
    pagePath: string | null;
    messageId: string;
    body: string;
    createdAt: number;
}

interface MessageCreatedProjection {
    conversationId: string;
    senderType: 'visitor' | 'operator';
    body: string;
    createdAt: number;
}

interface ConversationStateProjection {
    conversationId: string;
    status: 'OPEN' | 'PENDING' | 'CLOSED' | 'ARCHIVED' | 'SPAM' | 'PURGE_PENDING';
    closedAt?: number | null;
    archivedAt?: number | null;
    archiveAt?: number | null;
    purgeAt?: number | null;
    purgeRequestedAt?: number | null;
    deletionReason?: string | null;
    updatedAt: number;
}

interface AssignmentProjection {
    conversationId: string;
    assignedOperatorId: string | null;
    updatedAt: number;
}

interface MessageReadProjection {
    conversationId: string;
    participantType: 'visitor' | 'operator';
    lastReadSeq: number;
    updatedAt: number;
}

async function hasTombstone(db: D1Database, conversationId: string): Promise<boolean> {
    const row = await db.prepare(
        'SELECT conversation_id FROM chat_conversation_tombstones WHERE conversation_id = ?',
    ).bind(conversationId).first();
    return Boolean(row);
}

export async function projectOutboxEvent(
    env: SupportRealtimeEnv,
    event: StoredOutboxEvent,
): Promise<'applied' | 'discarded'> {
    const payload = JSON.parse(event.payloadJson) as
        ConversationCreatedProjection | MessageCreatedProjection |
        ConversationStateProjection | MessageReadProjection | AssignmentProjection;
    const conversationId = payload.conversationId;
    if (await hasTombstone(env.CHAT_DB, conversationId)) {
        emitMetric('chat_tombstone_discarded_event_total', 1, { eventType: event.eventType });
        return 'discarded';
    }

    if (event.eventType === 'conversation.created') {
        const value = payload as ConversationCreatedProjection;
        const preview = value.body.slice(0, 240);
        await env.CHAT_DB.prepare(`
            INSERT INTO chat_conversations (
                id, visitor_id, customer_id,
                contact_name, contact_email, contact_email_lookup_hash, contact_verified_at,
                status, assigned_operator_id,
                locale, country_code, product_id, order_id, page_path,
                last_seq, projection_version, last_message_at,
                last_message_sender, last_message_preview,
                visitor_unread_count, operator_unread_count,
                created_at, updated_at
            ) VALUES (?, ?, NULL, ?, ?, ?, ?, 'OPEN', NULL, ?, ?, ?, ?, ?, ?, ?, ?, 'visitor', ?, 0, 1, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                contact_name = excluded.contact_name,
                contact_email = excluded.contact_email,
                contact_email_lookup_hash = excluded.contact_email_lookup_hash,
                contact_verified_at = excluded.contact_verified_at,
                locale = excluded.locale,
                country_code = excluded.country_code,
                product_id = excluded.product_id,
                order_id = excluded.order_id,
                page_path = excluded.page_path,
                last_seq = CASE WHEN excluded.last_seq > chat_conversations.last_seq
                                THEN excluded.last_seq ELSE chat_conversations.last_seq END,
                projection_version = excluded.projection_version,
                last_message_at = excluded.last_message_at,
                last_message_sender = excluded.last_message_sender,
                last_message_preview = excluded.last_message_preview,
                operator_unread_count = MAX(chat_conversations.operator_unread_count, 1),
                updated_at = excluded.updated_at
            WHERE excluded.projection_version > chat_conversations.projection_version
        `).bind(
            value.conversationId,
            value.visitorId,
            value.contactName,
            value.contactEmail,
            value.contactEmailLookupHash,
            value.contactVerifiedAt,
            value.locale,
            value.countryCode,
            value.productId,
            value.orderId,
            value.pagePath,
            event.seq || 1,
            event.projectionVersion,
            value.createdAt,
            preview,
            value.createdAt,
            value.createdAt,
        ).run();
        return 'applied';
    }

    if (event.eventType === 'message.created' && event.seq != null) {
        const value = payload as MessageCreatedProjection;
        await env.CHAT_DB.prepare(`
            UPDATE chat_conversations
            SET last_seq = ?,
                projection_version = MAX(projection_version, ?),
                last_message_at = ?,
                last_message_sender = ?,
                last_message_preview = ?,
                visitor_unread_count = visitor_unread_count + CASE WHEN ? = 'operator' THEN 1 ELSE 0 END,
                operator_unread_count = operator_unread_count + CASE WHEN ? = 'visitor' THEN 1 ELSE 0 END,
                updated_at = ?
            WHERE id = ? AND last_seq < ?
        `).bind(
            event.seq,
            event.projectionVersion,
            value.createdAt,
            value.senderType,
            value.body.slice(0, 240),
            value.senderType,
            value.senderType,
            value.createdAt,
            value.conversationId,
            event.seq,
        ).run();
    }


    if (['conversation.reopened', 'conversation.updated', 'conversation.closed',
        'conversation.archived', 'conversation.spam_marked',
        'conversation.purge_requested'].includes(event.eventType)) {
        const value = payload as ConversationStateProjection;
        await env.CHAT_DB.prepare(`
            UPDATE chat_conversations
            SET status = ?,
                projection_version = ?,
                closed_at = ?,
                archived_at = ?,
                archive_at = ?,
                purge_at = ?,
                purge_requested_at = ?,
                deletion_reason = ?,
                updated_at = ?
            WHERE id = ? AND projection_version < ?
        `).bind(
            value.status,
            event.projectionVersion,
            value.status === 'OPEN' ? null : value.closedAt ?? null,
            value.status === 'OPEN' ? null : value.archivedAt ?? null,
            value.status === 'OPEN' ? null : value.archiveAt ?? null,
            value.status === 'OPEN' ? null : value.purgeAt ?? null,
            value.status === 'PURGE_PENDING' ? value.purgeRequestedAt ?? value.updatedAt : null,
            value.status === 'PURGE_PENDING' ? value.deletionReason ?? null : null,
            value.updatedAt,
            value.conversationId,
            event.projectionVersion,
        ).run();
    }

    if (event.eventType === 'operator.assignment') {
        const value = payload as AssignmentProjection;
        await env.CHAT_DB.prepare(`
            UPDATE chat_conversations
            SET assigned_operator_id = ?, projection_version = ?, updated_at = ?
            WHERE id = ? AND projection_version < ?
        `).bind(
            value.assignedOperatorId,
            event.projectionVersion,
            value.updatedAt,
            value.conversationId,
            event.projectionVersion,
        ).run();
    }


    if (event.eventType === 'message.read') {
        const value = payload as MessageReadProjection;
        const unreadColumn = value.participantType === 'visitor'
            ? 'visitor_unread_count'
            : 'operator_unread_count';
        await env.CHAT_DB.prepare(`
            UPDATE chat_conversations
            SET ${unreadColumn} = CASE WHEN last_seq <= ? THEN 0 ELSE ${unreadColumn} END,
                projection_version = MAX(projection_version, ?),
                updated_at = MAX(updated_at, ?)
            WHERE id = ?
        `).bind(
            value.lastReadSeq,
            event.projectionVersion,
            value.updatedAt,
            value.conversationId,
        ).run();
    }
    return 'applied';
}
