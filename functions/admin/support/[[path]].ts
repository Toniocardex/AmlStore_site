interface AdminSupportAssetsEnv { ASSETS: Fetcher }

export const onRequest: PagesFunction<AdminSupportAssetsEnv> = async ({ request, env }) => {
    const url = new URL(request.url);
    if (request.method !== 'GET' || !/^\/admin\/support(?:\/|$)/.test(url.pathname)) {
        return new Response('Not found', { status: 404 });
    }
    if (/\.(?:css|js|json|webmanifest|png|webp|svg|ico)$/.test(url.pathname)) {
        return env.ASSETS.fetch(request);
    }
    const assetUrl = new URL('/admin/support/app-shell.txt', url);
    const response = await env.ASSETS.fetch(new Request(assetUrl, request));
    const headers = new Headers(response.headers);
    headers.set('Cache-Control', 'no-store');
    headers.set('Content-Type', 'text/html; charset=utf-8');
    return new Response(response.body, { status: response.status, headers });
};
