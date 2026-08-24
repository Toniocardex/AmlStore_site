export const ID_PREFIXES = {
    visitor: 'vis',
    conversation: 'conv',
    message: 'msg',
    event: 'evt',
    request: 'req',
    operator: 'op',
    device: 'dev',
} as const;

export type IdKind = keyof typeof ID_PREFIXES;

export function createId(kind: IdKind): string {
    return `${ID_PREFIXES[kind]}_${crypto.randomUUID()}`;
}

export function isPrefixedId(value: unknown, kind: IdKind): value is string {
    if (typeof value !== 'string') return false;
    const prefix = ID_PREFIXES[kind];
    return value.startsWith(`${prefix}_`) && value.length <= 64;
}
