import { describe, expect, it } from 'vitest';
import { ChatProtocolError } from './errors';
import { createId } from './ids';
import { assertTransition, validateRetentionPolicy } from './lifecycle';
import { parseMessageSendCommand } from './schemas';

describe('chat protocol', () => {
    it('parses and normalizes a message.send command', () => {
        const parsed = parseMessageSendCommand({
            v: 1,
            type: 'message.send',
            requestId: createId('request'),
            conversationId: createId('conversation'),
            payload: {
                clientMessageId: createId('message'),
                body: '  hello\r\nworld  ',
            },
        });
        expect(parsed.payload.body).toBe('hello\nworld');
    });

    it('rejects an oversized body', () => {
        expect(() => parseMessageSendCommand({
            v: 1,
            type: 'message.send',
            requestId: createId('request'),
            conversationId: createId('conversation'),
            payload: {
                clientMessageId: createId('message'),
                body: 'x'.repeat(4_001),
            },
        })).toThrowError(ChatProtocolError);
    });

    it('rejects reopening PURGE_PENDING', () => {
        expect(() => assertTransition('PURGE_PENDING', 'OPEN')).toThrowError(ChatProtocolError);
    });

    it('rejects invalid retention ordering', () => {
        expect(() => validateRetentionPolicy({
            archiveAfterDays: 180,
            retentionDays: 180,
            spamRetentionDays: 14,
            deleteGraceDays: 0,
            tombstoneRetentionDays: 30,
            batchSize: 100,
        })).toThrow(/less than/);
    });
});
