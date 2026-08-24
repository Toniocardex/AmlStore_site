import { describe, expect, it } from 'vitest';
import { isWithinBusinessHours, validateBusinessHoursPolicy } from './business-hours';

const policy = {
    startHour: 8,
    endHour: 19,
    activeWeekdays: new Set([1, 2, 3, 4, 5, 6]),
    timeZone: 'UTC',
};

describe('business-hours', () => {
    it('è dentro orario in un giorno feriale attivo', () => {
        // 2026-08-24 è un lunedì
        expect(isWithinBusinessHours(policy, new Date('2026-08-24T10:00:00Z'))).toBe(true);
    });

    it('è fuori orario prima dell\'apertura', () => {
        expect(isWithinBusinessHours(policy, new Date('2026-08-24T07:59:00Z'))).toBe(false);
    });

    it('è fuori orario alla chiusura e dopo', () => {
        expect(isWithinBusinessHours(policy, new Date('2026-08-24T19:00:00Z'))).toBe(false);
        expect(isWithinBusinessHours(policy, new Date('2026-08-24T23:00:00Z'))).toBe(false);
    });

    it('è sempre fuori orario in un giorno non attivo, anche dentro la fascia oraria', () => {
        // 2026-08-23 è una domenica, esclusa dalla policy di default
        expect(isWithinBusinessHours(policy, new Date('2026-08-23T10:00:00Z'))).toBe(false);
    });

    it('rifiuta una policy con chiusura non successiva all\'apertura', () => {
        expect(() => validateBusinessHoursPolicy({ ...policy, startHour: 20, endHour: 8 })).toThrow();
    });

    it('rifiuta una policy senza nessun giorno attivo', () => {
        expect(() => validateBusinessHoursPolicy({ ...policy, activeWeekdays: new Set() })).toThrow();
    });

    it('rifiuta un giorno fuori dall\'intervallo 0-6', () => {
        expect(() => validateBusinessHoursPolicy({ ...policy, activeWeekdays: new Set([7]) })).toThrow();
    });
});
