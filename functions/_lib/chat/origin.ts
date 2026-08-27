import { ChatProtocolError } from '../../../support/shared/errors';

export interface OriginEnv { SITE_ORIGIN?: string }

export function allowedChatOrigins(env: OriginEnv): ReadonlySet<string> {
    const values = new Set([
        'https://eurolicenze.com',
        'https://www.eurolicenze.com',
        'http://localhost:8788',
        'http://127.0.0.1:8788',
    ]);
    if (env.SITE_ORIGIN) values.add(env.SITE_ORIGIN.replace(/\/$/, ''));
    return values;
}

export function assertAllowedOrigin(request: Request, env: OriginEnv): void {
    const origin = request.headers.get('Origin') || '';
    if (!origin || !allowedChatOrigins(env).has(origin)) {
        throw new ChatProtocolError('FORBIDDEN', 'Origin not allowed', 403);
    }
}
