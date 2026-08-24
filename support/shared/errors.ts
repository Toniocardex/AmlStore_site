export const CHAT_ERROR_CODES = [
    'UNAUTHORIZED',
    'FORBIDDEN',
    'NOT_FOUND',
    'INVALID_PAYLOAD',
    'MESSAGE_TOO_LONG',
    'RATE_LIMITED',
    'CONVERSATION_CLOSED',
    'CONVERSATION_ARCHIVED',
    'CONVERSATION_PURGE_PENDING',
    'CONVERSATION_PURGED',
    'INTERNAL_ERROR',
    'TEMPORARILY_UNAVAILABLE',
] as const;

export type ChatErrorCode = (typeof CHAT_ERROR_CODES)[number];

export class ChatProtocolError extends Error {
    readonly code: ChatErrorCode;
    readonly status: number;

    constructor(code: ChatErrorCode, message: string, status = 400) {
        super(message);
        this.name = 'ChatProtocolError';
        this.code = code;
        this.status = status;
    }
}
