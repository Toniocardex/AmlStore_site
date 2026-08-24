import { readFile } from 'node:fs/promises';
import { describe, expect, it } from 'vitest';

describe('admin support PWA', () => {
    it('uses the required /admin scope and standalone support start URL', async () => {
        const manifest = JSON.parse(await readFile('admin/support/manifest.webmanifest', 'utf8'));
        expect(manifest.scope).toBe('/admin/');
        expect(manifest.start_url).toBe('/admin/support/');
        expect(manifest.display).toBe('standalone');
        expect(manifest.icons.some((icon: { purpose?: string }) => icon.purpose?.includes('maskable'))).toBe(true);
    });

    it('never places support or chat APIs in the app-shell cache', async () => {
        const worker = await readFile('admin/sw.js', 'utf8');
        expect(worker).toContain("url.pathname.startsWith('/admin/api/')");
        expect(worker).toContain("url.pathname.startsWith('/api/chat/')");
        const shellMatch = worker.match(/const APP_SHELL = \[([\s\S]*?)\];/);
        expect(shellMatch?.[1]).not.toContain('/admin/api/');
        expect(shellMatch?.[1]).not.toContain('/api/chat/');
    });
});
