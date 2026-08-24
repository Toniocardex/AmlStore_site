import { CHAT_PROTOCOL_VERSION, type ErrorEnvelope } from '../../../support/shared/protocol';
import { ChatProtocolError } from '../../../support/shared/errors';

const NO_STORE_HEADERS = {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
};

export function chatJson(data: unknown, status = 200, extraHeaders?: HeadersInit): Response {
    const headers = new Headers(NO_STORE_HEADERS);
    if (extraHeaders) {
        new Headers(extraHeaders).forEach((value, name) => headers.set(name, value));
    }
    return new Response(JSON.stringify(data), {
        status,
        headers,
    });
}

export function chatError(error: unknown, requestId?: string): Response {
    const known = error instanceof ChatProtocolError
        ? error
        : new ChatProtocolError('INTERNAL_ERROR', 'Internal server error', 500);
    const body: ErrorEnvelope = {
        v: CHAT_PROTOCOL_VERSION,
        type: 'error',
        ...(requestId ? { requestId } : {}),
        error: { code: known.code, message: known.message },
    };
    return chatJson(body, known.status);
}

export async function readJsonBody(request: Request, maxBytes = 16 * 1024): Promise<unknown> {
    const contentType = (request.headers.get('Content-Type') || '').split(';', 1)[0].trim().toLowerCase();
    if (contentType !== 'application/json') {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Content-Type must be application/json', 415);
    }
    const declared = Number(request.headers.get('Content-Length') || 0);
    if (declared > maxBytes) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Payload too large', 413);
    }
    const text = await request.text();
    if (new TextEncoder().encode(text).byteLength > maxBytes) {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Payload too large', 413);
    }
    try { return JSON.parse(text); } catch {
        throw new ChatProtocolError('INVALID_PAYLOAD', 'Invalid JSON');
    }
}
