#!/usr/bin/env python3
"""Static checks for internal order notification delivery."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATCHALL = (ROOT / "functions/api/[[catchall]].js").read_text(encoding="utf-8")
EMAIL = (ROOT / "functions/api/_lib/email.js").read_text(encoding="utf-8")
ORDER = (ROOT / "functions/api/_lib/order.js").read_text(encoding="utf-8")
ADMIN = (ROOT / "functions/api/_lib/admin.js").read_text(encoding="utf-8")
SCHEMA = (ROOT / "schema.sql").read_text(encoding="utf-8")
MIGRATION = (ROOT / "schema-internal-notification-migration.sql").read_text(encoding="utf-8")

errors = []


def require(label, condition):
    if not condition:
        errors.append(label)


require("internal recipient Info@amlstore.it missing", "Info@amlstore.it" in EMAIL)
require("internal recipient Outlook missing", "Antonino.cardelli@outlook.it" in EMAIL)
require("sendInternalOrderNotificationOnce missing", "sendInternalOrderNotificationOnce" in EMAIL)
require("internal notification idempotency check missing", "internal_notification_sent_at" in EMAIL)
require("manual license instruction missing", "DA INVIARE MANUALMENTE" in EMAIL)
require("SKU column missing", "ID articolo / SKU" in EMAIL)
require("customer email payment_method mapping missing", "payment_method: order.payment_method" in EMAIL)

require("order mark helper missing", "markInternalNotificationSent" in ORDER)
require("schema internal sent column missing", "internal_notification_sent_at" in SCHEMA)
require("schema internal event column missing", "internal_notification_event_src" in SCHEMA)
require("migration internal sent column missing", "internal_notification_sent_at" in MIGRATION)
require("migration internal event column missing", "internal_notification_event_src" in MIGRATION)

for event in ("webhook_stripe", "worker_capture", "bank_transfer_created"):
    require(f"internal notification not wired for {event}", event in CATCHALL)

require(
    "admin bank transfer fallback missing",
    "bank_transfer_marked_paid" in ADMIN and "sendInternalOrderNotificationOnce" in ADMIN,
)

if errors:
    print("ORDER NOTIFICATION VALIDATION FAILED:", len(errors), "issue(s)")
    for error in errors:
        print(" -", error)
    raise SystemExit(1)

print("OK: internal order notifications are wired")
