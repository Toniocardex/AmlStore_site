import { ChatProtocolError } from '../../../support/shared/errors';
import {
    handleAvailability,
    handleCreateConversation,
    handleGuestConversationDetail,
    handleGuestRead,
    handleGuestSession,
    handleGuestWebSocket,
    handleListGuestConversations,
    handleSendGuestMessage,
    type ChatPagesEnv,
} from '../../_lib/chat/gateway';
import { chatError } from '../../_lib/chat/responses';

function routeParts(context: EventContext<ChatPagesEnv, string, Record<string, unknown>>): string[] {
    const value = context.params.path;
    return Array.isArray(value) ? value.map(String) : (value ? [String(value)] : []);
}

export const onRequest: PagesFunction<ChatPagesEnv> = async (context) => {
    const { request, env } = context;
    const parts = routeParts(context);
    try {
        if (request.method === 'OPTIONS') return new Response(null, { status: 204 });
        if (request.method === 'POST' && parts.length === 1 && parts[0] === 'session') {
            return await handleGuestSession(request, env);
        }
        if (request.method === 'GET' && parts.length === 1 && parts[0] === 'availability') {
            return await handleAvailability(env);
        }
        if (parts.length === 1 && parts[0] === 'conversations') {
            if (request.method === 'POST') return await handleCreateConversation(request, env);
            if (request.method === 'GET') return await handleListGuestConversations(request, env);
        }
        if (parts[0] === 'conversations' && parts.length >= 2) {
            if (request.method === 'GET' && parts.length === 2) {
                return await handleGuestConversationDetail(request, env, parts[1]);
            }
            if (request.method === 'GET' && parts.length === 3 && parts[2] === 'messages') {
                return await handleGuestConversationDetail(request, env, parts[1], true);
            }
            if (request.method === 'POST' && parts.length === 3 && parts[2] === 'messages') {
                return await handleSendGuestMessage(request, env, parts[1]);
            }
            if (request.method === 'POST' && parts.length === 3 && parts[2] === 'read') {
                return await handleGuestRead(request, env, parts[1]);
            }
            if (request.method === 'GET' && parts.length === 3 && parts[2] === 'ws') {
                return await handleGuestWebSocket(request, env, parts[1]);
            }
        }
        throw new ChatProtocolError('NOT_FOUND', 'Not found', 404);
    } catch (error) {
        if (!(error instanceof ChatProtocolError)) console.error('[chat] request failed', error);
        return chatError(error);
    }
};
