#!/usr/bin/env python3
"""Genera un valore casuale sicuro per TOKEN_SECRET (o altri secret interni).

Uso:
    python scripts/generate-secret.py

Il valore NON viene salvato da nessuna parte da questo script: copialo e
incollalo tu stesso quando richiesto da:

    wrangler pages secret put TOKEN_SECRET

Usa `secrets` (CSPRNG), non `random`: adatto a un segreto di produzione.
"""
import secrets

if __name__ == "__main__":
    value = secrets.token_urlsafe(32)  # 32 byte di entropia, ~43 caratteri
    print(value)
