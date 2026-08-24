export interface BusinessHoursPolicy {
    startHour: number;
    endHour: number;
    activeWeekdays: ReadonlySet<number>;
    timeZone: string;
}

export function validateBusinessHoursPolicy(policy: BusinessHoursPolicy): BusinessHoursPolicy {
    if (!Number.isInteger(policy.startHour) || policy.startHour < 0 || policy.startHour > 23) {
        throw new Error('CHAT_BUSINESS_HOURS_START must be an integer between 0 and 23');
    }
    if (!Number.isInteger(policy.endHour) || policy.endHour < 1 || policy.endHour > 24) {
        throw new Error('CHAT_BUSINESS_HOURS_END must be an integer between 1 and 24');
    }
    if (policy.endHour <= policy.startHour) {
        throw new Error('CHAT_BUSINESS_HOURS_END must be greater than CHAT_BUSINESS_HOURS_START');
    }
    if (!policy.activeWeekdays.size) {
        throw new Error('CHAT_BUSINESS_HOURS_DAYS must include at least one weekday');
    }
    for (const day of policy.activeWeekdays) {
        if (!Number.isInteger(day) || day < 0 || day > 6) {
            throw new Error('CHAT_BUSINESS_HOURS_DAYS must contain integers between 0 (Sunday) and 6 (Saturday)');
        }
    }
    return policy;
}

const WEEKDAY_INDEX: Record<string, number> = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };

/**
 * ADR §45: la disponibilita' pubblica "AUTO" segue l'orario del negozio, non
 * la connessione WS dell'operatore — l'attivita' e' gestita da una sola
 * persona che non tiene il pannello admin aperto tutto il giorno. Usa
 * Intl.DateTimeFormat (non l'ora del Worker, quasi sempre UTC) per restare
 * corretto attraverso il cambio ora legale/solare di Europe/Rome.
 */
export function isWithinBusinessHours(policy: BusinessHoursPolicy, now: Date = new Date()): boolean {
    const parts = new Intl.DateTimeFormat('en-US', {
        timeZone: policy.timeZone,
        weekday: 'short',
        hour: '2-digit',
        hour12: false,
    }).formatToParts(now);
    const weekdayPart = parts.find((part) => part.type === 'weekday')?.value || 'Sun';
    const hourPart = parts.find((part) => part.type === 'hour')?.value || '0';
    const weekday = WEEKDAY_INDEX[weekdayPart] ?? 0;
    // Alcuni engine restituiscono "24" per la mezzanotte con hour12:false.
    const hour = Number(hourPart) % 24;
    if (!policy.activeWeekdays.has(weekday)) return false;
    return hour >= policy.startHour && hour < policy.endHour;
}
