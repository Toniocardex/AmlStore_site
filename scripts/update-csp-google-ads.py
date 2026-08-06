#!/usr/bin/env python3
"""Rewrite Content-Security-Policy in _headers per Google official CSP guide."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# EU + site locales + common markets (CSP forbids www.google.* wildcards on TLD)
SUFFIXES = [
    ".google.com", ".google.it", ".google.de", ".google.fr", ".google.es", ".google.ie",
    ".google.co.uk", ".google.nl", ".google.be", ".google.at", ".google.ch", ".google.pt",
    ".google.pl", ".google.ro", ".google.se", ".google.dk", ".google.fi", ".google.no",
    ".google.cz", ".google.hu", ".google.gr", ".google.sk", ".google.si", ".google.hr",
    ".google.bg", ".google.lt", ".google.lv", ".google.ee", ".google.lu", ".google.com.mt",
    ".google.com.cy", ".google.is", ".google.co.il", ".google.com.au", ".google.ca",
    ".google.com.br", ".google.co.jp", ".google.com.mx", ".google.com.tr", ".google.ru",
    ".google.com.ua", ".google.cat",
]


def google_hosts() -> str:
    out: list[str] = []
    seen: set[str] = set()
    for suffix in SUFFIXES:
        host = suffix.lstrip(".")
        for h in (f"https://www.{host}", f"https://{host}"):
            if h not in seen:
                seen.add(h)
                out.append(h)
    return " ".join(out)


def build_csp() -> str:
    g = google_hosts()
    # https://developers.google.com/tag-platform/security/guides/csp
    # GA4 + Google Ads (+ Trustpilot / PayPal già usati dal sito)
    return (
        "default-src 'self'; "
        "base-uri 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "form-action 'self'; "
        "script-src 'self' 'unsafe-inline' "
        "https://widget.trustpilot.com https://*.paypal.com https://*.paypalobjects.com "
        "https://www.googletagmanager.com https://*.googletagmanager.com "
        "https://www.google-analytics.com https://*.google-analytics.com "
        "https://www.googleadservices.com https://www.google.com https://google.com "
        "https://pagead2.googlesyndication.com https://googleads.g.doubleclick.net "
        "https://*.doubleclick.net https://*.google.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: "
        "https://*.trustpilot.com https://*.paypalobjects.com "
        "https://*.google-analytics.com https://www.googletagmanager.com https://*.googletagmanager.com "
        "https://*.g.doubleclick.net https://googleads.g.doubleclick.net https://*.doubleclick.net "
        "https://pagead2.googlesyndication.com https://*.googlesyndication.com "
        "https://www.googleadservices.com https://www.gstatic.com https://ssl.gstatic.com "
        f"{g}; "
        "font-src 'self' data:; "
        "connect-src 'self' "
        "https://*.trustpilot.com https://*.paypal.com https://*.paypalobjects.com "
        "https://*.google-analytics.com https://*.analytics.google.com "
        "https://www.googletagmanager.com https://*.googletagmanager.com "
        "https://*.g.doubleclick.net https://googleads.g.doubleclick.net "
        "https://ad.doubleclick.net https://*.doubleclick.net "
        "https://pagead2.googlesyndication.com https://*.googlesyndication.com "
        "https://www.googleadservices.com "
        "https://www.merchant-center-analytics.goog https://*.merchant-center-analytics.goog "
        f"{g}; "
        "frame-src https://widget.trustpilot.com https://*.paypal.com "
        "https://www.googletagmanager.com https://*.googletagmanager.com "
        "https://*.doubleclick.net https://www.googleadservices.com https://*.google.com; "
        "worker-src 'self'; "
        "manifest-src 'self'; "
        "media-src 'self'; "
        "upgrade-insecure-requests"
    )


def main() -> None:
    path = ROOT / "_headers"
    text = path.read_text(encoding="utf-8")
    csp = build_csp()
    new_text, n = re.subn(
        r"  Content-Security-Policy: .*",
        "  Content-Security-Policy: " + csp,
        text,
        count=1,
    )
    if n != 1:
        raise SystemExit(f"expected 1 CSP line, got {n}")
    path.write_text(new_text, encoding="utf-8", newline="\n")
    print("csp_bytes", len(csp))
    print("has_pagead2", "https://pagead2.googlesyndication.com" in csp)
    print("has_google_ie", "https://www.google.ie" in csp)


if __name__ == "__main__":
    main()
