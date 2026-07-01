#!/usr/bin/env python3
"""Static guardrails for checkout/admin anti-tampering controls."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATCHALL = (ROOT / "functions/api/[[catchall]].js").read_text(encoding="utf-8")
ADMIN = (ROOT / "functions/api/_lib/admin.js").read_text(encoding="utf-8")
PAYPAL = (ROOT / "functions/api/_lib/paypal.js").read_text(encoding="utf-8")

errors = []


def require(name, condition):
    if not condition:
        errors.append(name)


def handler_block(name):
    marker = f"async function {name}"
    start = CATCHALL.find(marker)
    if start < 0:
        return ""
    next_marker = CATCHALL.find("\nasync function ", start + len(marker))
    return CATCHALL[start:] if next_marker < 0 else CATCHALL[start:next_marker]


for handler in (
    "handleStripeCreateSession",
    "handlePaypalCreateOrder",
    "handlePaypalCaptureOrder",
    "handleBankTransferOrder",
):
    block = handler_block(handler)
    require(f"{handler}: missing JSON/origin guard", "validateCheckoutRequest(request, env)" in block)

require("checkout origin allowlist missing", "isAllowedCheckoutOrigin" in CATCHALL)
require("checkout content-type guard missing", "isJsonContentType" in CATCHALL)
require("checkout body-size guard missing", "MAX_JSON_BODY_BYTES" in CATCHALL)
require("customer email validation missing", "validateEmail(customer.email)" in CATCHALL)
require("customer first name validation missing", "Nome cliente mancante" in CATCHALL)
require("customer last name validation missing", "Cognome cliente mancante" in CATCHALL)
require("business VAT validation missing", "validatePIVA(customer.piva)" in CATCHALL)
require("business SDI/PEC validation missing", "Inserire Codice SDI o PEC" in CATCHALL)
require("locale allowlist missing", "ALLOWED_LOCALES" in CATCHALL)
require("idempotency key validation missing", "normalizeIdempotencyKey" in CATCHALL)

require("admin aud mismatch must reject", "return { valid: false, reason: 'aud_mismatch' }" in ADMIN)
require("admin missing audience must reject", "CF_ACCESS_AUD non configurato" in ADMIN)
require("admin email allowlist missing", "ADMIN_ALLOWED_EMAILS" in ADMIN and "admin_email_not_allowed" in ADMIN)
require("admin mutation origin guard missing", "validateAdminMutationRequest(request, env)" in CATCHALL)
require("admin mutation body-size guard missing", "MAX_ADMIN_JSON_BODY_BYTES" in CATCHALL)
require("admin delete flag missing", "ADMIN_ALLOW_DELETE_ORDERS" in CATCHALL)
require("admin delete requires archived order", "not_archived" in ADMIN and "archived_at" in ADMIN)

require("PayPal capture amount not returned", "amountValue:" in PAYPAL)
require("PayPal capture currency not returned", "currencyCode:" in PAYPAL)
require("PayPal captured amount not compared", "capturedMinor !== Number(order.total_minor)" in CATCHALL)
require("PayPal captured currency not compared", "currencyCode" in CATCHALL and "order.currency" in CATCHALL)

if errors:
    print("SECURITY VALIDATION FAILED:", len(errors), "issue(s)")
    for error in errors:
        print(" -", error)
    raise SystemExit(1)

print("OK: checkout/admin anti-tampering controls are present")
