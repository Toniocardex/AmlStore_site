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
        // Il Cron Trigger e' registrato a livello di Worker, non di feature flag:
        // senza questa guardia la retention interroga il D1 configurato in
        // wrangler.toml (oggi quello di produzione) ogni 15 minuti anche mentre
        // CHAT_ENABLED=0, comprese le finestre in cui la migration 0002 non e'
        // ancora stata applicata.
        const config = readChatConfig(env as unknown as Record<string, string | undefined>);
        if (!config.enabled) return;
        ctx.waitUntil(runRetention(env));
    },
};
