import { ChatProtocolError } from './errors';
import { isPrefixedId } from './ids';
import { CHAT_PROTOCOL_VERSION, type ClientCommand, type MessageSendPayload } from './protocol';

export const DEFAULT_MAX_MESSAGE_LENGTH = 4_000;

function isRecord(value: unknown): value is Record<string, unknown> {
    return typeof value === 'object' && value !== null && !Array.isArray(value);
}

export function normalizePlainText(value: unknown, maxLength = DEFAULT_MAX_MESSAGE_LENGTH): string {
    if (typeof value !== 'string') {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Message body must be a string');
    }
    const body = value.replace(/\r\n?/g, '\n').trim();
    if (!body) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Message body is required');
    }
    if (body.length > maxLength) {
        throw new ChatProtocolError('MESSAGE_TOO_LONG', 'Message body exceeds the configured limit', 413);
    }
    return body;
}

export function parseMessageSendCommand(
    input: unknown,
    maxLength = DEFAULT_MAX_MESSAGE_LENGTH,
): ClientCommand<MessageSendPayload> {
    if (!isRecord(input) || input.v !== CHAT_PROTOCOL_VERSION || input.type !== 'message.send') {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid message.send envelope');
    }
    if (!isPrefixedId(input.requestId, 'request')) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid requestId');
    }
    if (!isPrefixedId(input.conversationId, 'conversation')) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid conversationId');
    }
    if (!isRecord(input.payload) || !isPrefixedId(input.payload.clientMessageId, 'message')) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid clientMessageId');
    }
    return {
        v: CHAT_PROTOCOL_VERSION,
        type: 'message.send',
        requestId: input.requestId,
        conversationId: input.conversationId,
        payload: {
            clientMessageId: input.payload.clientMessageId,
            body: normalizePlainText(input.payload.body, maxLength),
        },
    };
}
