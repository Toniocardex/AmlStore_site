#!/usr/bin/env python3
"""Genera un valore casuale sicuro per FRAUD_HASH_SECRET (HMAC rate-limit checkout).

Uso:
    python scripts/generate-fraud-hash-secret.py

Il valore esce su stdout (una sola riga). NON viene salvato da questo script.

  Locale — in `.dev.vars` (non committare):
      FRAUD_HASH_SECRET=<valore>

  Produzione:
      npx wrangler pages secret put FRAUD_HASH_SECRET

Usa `secrets` (CSPRNG), non `random`.
"""
import secrets
import sys

if __name__ == "__main__":
    value = secrets.token_urlsafe(32)  # 32 byte di entropia, ~43 caratteri
    print(value)
    sys.stdout.flush()
    print(
        "\nIncolla in .dev.vars oppure:\n"
        "  npx wrangler pages secret put FRAUD_HASH_SECRET",
        file=sys.stderr,
    )
