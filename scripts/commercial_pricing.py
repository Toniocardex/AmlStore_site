#!/usr/bin/env python3
"""Policy centrale per trasformare un prezzo EUR sostenibile in prezzo pubblico."""

import json
from pathlib import Path

CLEAN_INTEGER_PRICE_THRESHOLD_EUR = 50
CLEAN_INTEGER_PRICE_THRESHOLD_MINOR_EUR = CLEAN_INTEGER_PRICE_THRESHOLD_EUR * 100
VALID_MODES = frozenset({"automatic", "manual", "preserve-cents"})
POLICY_PATH = Path(__file__).with_name("commercial-pricing-policy.json")


def load_policy(path=POLICY_PATH):
    if not path.exists():
        return {"currency": "EUR", "products": {}}
    policy = json.loads(path.read_text(encoding="utf-8"))
    if policy.get("currency", "EUR") != "EUR":
        raise ValueError("La policy commerciale supporta per ora solo EUR")
    if not isinstance(policy.get("products", {}), dict):
        raise ValueError("commercial-pricing-policy.json: products deve essere un oggetto")
    return policy


def normalize_commercial_price_minor(
    raw_minor,
    currency="EUR",
    mode="automatic",
    manual_public_price_minor=None,
):
    """Restituisce il prezzo pubblico in centesimi senza usare floating point."""
    if not isinstance(raw_minor, int) or isinstance(raw_minor, bool) or raw_minor < 0:
        raise ValueError("raw_minor deve essere un intero non negativo")
    if mode not in VALID_MODES:
        raise ValueError(f"Modalita di pricing non valida: {mode}")

    if mode == "manual":
        if (
            not isinstance(manual_public_price_minor, int)
            or isinstance(manual_public_price_minor, bool)
            or manual_public_price_minor < 0
        ):
            raise ValueError("L'override manuale deve essere un intero non negativo")
        return manual_public_price_minor

    if mode == "preserve-cents" or currency.upper() != "EUR":
        return raw_minor
    if raw_minor < CLEAN_INTEGER_PRICE_THRESHOLD_MINOR_EUR:
        return raw_minor
    return ((raw_minor + 99) // 100) * 100


def resolve_public_price_minor(entry, policy=None):
    policy = policy or load_policy()
    product_policy = policy.get("products", {}).get(entry.get("sku"), {})
    mode = product_policy.get("mode", "automatic")
    return normalize_commercial_price_minor(
        entry["unitAmountMinor"],
        entry.get("currency", "EUR"),
        mode,
        product_policy.get("publicPriceMinor"),
    )


def format_eur_minor(minor):
    """Formato pubblico it-IT a due decimali: 32,95 €, 144,00 €, 1.349,00 €."""
    if not isinstance(minor, int) or minor < 0:
        raise ValueError("minor deve essere un intero non negativo")
    euros, cents = divmod(minor, 100)
    integer = f"{euros:,}".replace(",", ".")
    return f"{integer},{cents:02d}"
