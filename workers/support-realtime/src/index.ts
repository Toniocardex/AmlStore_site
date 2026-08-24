import { readChatConfig } from '../../../support/shared/config';
import { ConversationDurableObject } from './conversation-do';
import type { SupportRealtimeEnv } from './env';
import { runRetention } from './retention';
import { SupportHubDurableObject } from './support-hub-do';

export { ConversationDurableObject, SupportHubDurableObject };

export default {
    async fetch(_request: Request, env: SupportRealtimeEnv): Promise<Response> {
        readChatConfig(env as unknown as Record<string, string | undefined>);
        return Response.json({ error: 'Not found' }, { status: 404 });
    },

    async scheduled(
        _controller: ScheduledController,
        env: SupportRealtimeEnv,
        ctx: ExecutionContext,
    ): Promise<void> {
        ctx.waitUntil(runRetention(env));
    },
};
