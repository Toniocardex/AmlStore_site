export function encodeBase64Url(bytes: Uint8Array): string {
    let binary = '';
    for (const byte of bytes) binary += String.fromCharCode(byte);
    return btoa(binary)
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/g, '');
}

export function decodeBase64Url(value: string): Uint8Array<ArrayBuffer> {
    const normalized = value.replace(/-/g, '+').replace(/_/g, '/');
    const padded = normalized + '='.repeat((4 - (normalized.length % 4)) % 4);
    const binary = atob(padded);
    const bytes = new Uint8Array(new ArrayBuffer(binary.length));
    for (let index = 0; index < binary.length; index += 1) {
        bytes[index] = binary.charCodeAt(index);
    }
    return bytes;
}

export function encodeUtf8Base64Url(value: string): string {
    return encodeBase64Url(new TextEncoder().encode(value));
}

export function decodeUtf8Base64Url(value: string): string {
    return new TextDecoder().decode(decodeBase64Url(value));
}
