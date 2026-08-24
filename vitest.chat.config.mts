import { readFile } from 'node:fs/promises';
import { cloudflareTest } from '@cloudflare/vitest-plugin';
import { defineConfig } from 'vitest/config';

export default defineConfig({
    plugins: [
        cloudflareTest(async () => {
            const migration = (await readFile('./migrations/0002_chat_core.sql', 'utf8'))
                .replace(/^--.*$/gm, '');
            const migrationQueries = migration
                .split(';')
                .map((query) => query.trim())
                .filter(Boolean);
            return {
                main: './workers/support-realtime/src/index.ts',
                additionalExports: {
                    ConversationDurableObject: 'DurableObject',
                    SupportHubDurableObject: 'DurableObject',
                },
                wrangler: {
                    configPath: './workers/support-realtime/wrangler.toml',
                },
                miniflare: {
                    bindings: {
                        CHAT_CORE_MIGRATION_QUERIES: JSON.stringify(migrationQueries),
                    },
                },
            };
        }),
    ],
    test: {
        include: [
            'support/**/*.test.ts',
            'functions/_lib/chat/**/*.test.ts',
            'workers/support-realtime/test/**/*.test.ts',
        ],
        testTimeout: 10_000,
    },
});
