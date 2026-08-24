import { validateBusinessHoursPolicy, type BusinessHoursPolicy } from './business-hours';
import { validateRetentionPolicy, type RetentionPolicy } from './lifecycle';

export interface ChatConfig extends RetentionPolicy {
    enabled: boolean;
    guestSessionDays: number;
    guestCookieName: string;
    maxMessageLength: number;
    siteOrigin: string;
    businessHours: BusinessHoursPolicy;
}

export type ChatConfigEnv = Record<string, string | undefined>;

function intValue(env: ChatConfigEnv, key: string, fallback: number): number {
    const raw = env[key];
    if (raw == null || raw === '') return fallback;
    const value = Number(raw);
    if (!Number.isInteger(value)) throw new Error(`${key} must be an integer`);
    return value;
}

function weekdaySetValue(env: ChatConfigEnv, key: string, fallback: number[]): Set<number> {
    const raw = env[key];
    if (raw == null || raw === '') return new Set(fallback);
    return new Set(raw.split(',').map((part) => Number(part.trim())));
}

export function readChatConfig(env: ChatConfigEnv): ChatConfig {
    const retention = validateRetentionPolicy({
        archiveAfterDays: intValue(env, 'CHAT_ARCHIVE_AFTER_DAYS', 30),
        retentionDays: intValue(env, 'CHAT_RETENTION_DAYS', 180),
        spamRetentionDays: intValue(env, 'CHAT_SPAM_RETENTION_DAYS', 14),
        deleteGraceDays: intValue(env, 'CHAT_DELETE_GRACE_DAYS', 0),
        tombstoneRetentionDays: intValue(env, 'CHAT_TOMBSTONE_RETENTION_DAYS', 30),
        batchSize: intValue(env, 'CHAT_RETENTION_BATCH_SIZE', 100),
    });
    const guestSessionDays = intValue(env, 'CHAT_GUEST_SESSION_DAYS', 180);
    const maxMessageLength = intValue(env, 'CHAT_MAX_MESSAGE_LENGTH', 4_000);
    if (guestSessionDays <= 0) throw new Error('CHAT_GUEST_SESSION_DAYS must be positive');
    if (maxMessageLength !== 4_000) throw new Error('CHAT_MAX_MESSAGE_LENGTH must be 4000 for MVP');
    const siteOrigin = String(env.SITE_ORIGIN || '').replace(/\/$/, '');
    if (!/^https:\/\//.test(siteOrigin) && !/^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(siteOrigin)) {
        throw new Error('SITE_ORIGIN must be an allowed HTTPS or localhost origin');
    }
    const businessHours = validateBusinessHoursPolicy({
        startHour: intValue(env, 'CHAT_BUSINESS_HOURS_START', 8),
        endHour: intValue(env, 'CHAT_BUSINESS_HOURS_END', 19),
        activeWeekdays: weekdaySetValue(env, 'CHAT_BUSINESS_HOURS_DAYS', [1, 2, 3, 4, 5, 6]),
        timeZone: String(env.CHAT_BUSINESS_HOURS_TIMEZONE || 'Europe/Rome'),
    });
    return {
        enabled: String(env.CHAT_ENABLED || '0') === '1',
        guestSessionDays,
        guestCookieName: String(env.CHAT_GUEST_COOKIE_NAME || '__Host-aml_chat_guest'),
        maxMessageLength,
        siteOrigin,
        businessHours,
        ...retention,
    };
}
