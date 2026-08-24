import type { SupportRealtimeEnv } from '../src/env';

declare global {
    namespace Cloudflare {
        interface Env extends SupportRealtimeEnv {
            CHAT_CORE_MIGRATION_QUERIES: string;
        }
    }
}

export {};
