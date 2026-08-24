import type { ChatErrorCode } from './errors';
import type { ConversationStatus } from './lifecycle';

export const CHAT_PROTOCOL_VERSION = 1 as const;

export type ParticipantType = 'visitor' | 'operator' | 'system';

export type ClientCommandType =
    | 'message.send'
    | 'message.read'
    | 'typing.started'
    | 'typing.stopped'
    | 'conversation.close'
    | 'conversation.reopen'
    | 'conversation.archive'
    | 'conversation.spam'
    | 'operator.assignment'
    | 'operator.presence';

export type ServerEventType =
    | 'conversation.created'
    | 'conversation.updated'
    | 'conversation.reopened'
    | 'conversation.closed'
    | 'conversation.archived'
    | 'conversation.spam_marked'
    | 'conversation.purge_requested'
    | 'conversation.purged'
    | 'message.created'
    | 'message.read'
    | 'typing.started'
    | 'typing.stopped'
    | 'operator.presence'
    | 'operator.assignment'
    | 'support.unread_changed';

export interface MessageSendPayload {
    clientMessageId: string;
    body: string;
}

export interface ClientCommand<T = unknown> {
    v: typeof CHAT_PROTOCOL_VERSION;
    type: ClientCommandType;
    requestId: string;
    conversationId: string;
    payload: T;
}

export interface ServerEvent<T = unknown> {
    v: typeof CHAT_PROTOCOL_VERSION;
    type: ServerEventType;
    eventId: string;
    conversationId: string;
    seq?: number;
    projectionVersion?: number;
    serverTs: number;
    payload: T;
}

export interface ErrorEnvelope {
    v: typeof CHAT_PROTOCOL_VERSION;
    type: 'error';
    requestId?: string;
    error: {
        code: ChatErrorCode;
        message: string;
    };
}

export interface ConversationSummary {
    id: string;
    visitorId: string;
    status: ConversationStatus;
    assignedOperatorId: string | null;
    locale: string | null;
    productId: string | null;
    orderId: string | null;
    pagePath: string | null;
    lastSeq: number;
    projectionVersion: number;
    lastMessageAt: number | null;
    lastMessageSender: ParticipantType | null;
    lastMessagePreview: string | null;
    visitorUnreadCount: number;
    operatorUnreadCount: number;
    createdAt: number;
    updatedAt: number;
}
