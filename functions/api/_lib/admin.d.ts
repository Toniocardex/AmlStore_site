export interface AdminAuthResult {
    valid: boolean;
    email?: string;
    reason?: string;
}

export function resolveAdminAuth(
    request: Request,
    env: Record<string, unknown>,
): Promise<AdminAuthResult>;
