#!/usr/bin/env python3
"""
Rewrite Content-Security-Policy in _headers (compact).

Cloudflare Pages silently drops oversized CSP header values; keep under ~3KB
while covering GA4 + Google Ads per:
https://developers.google.com/tag-platform/security/guides/csp
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# CSP forbids wildcards on the TLD side (www.google.*). Keep only markets we sell in.
GOOGLE_TLDS = (
    "com", "it", "de", "fr", "es", "ie", "co.uk", "nl", "be", "at", "ch", "pt", "pl",
)


def google_hosts() -> str:
    hosts: list[str] = []
    for tld in GOOGLE_TLDS:
        hosts.append(f"https://www.google.{tld}")
        hosts.append(f"https://google.{tld}")
    return " ".join(hosts)


def build_csp() -> str:
    g = google_hosts()
    return (
        "default-src 'self'; "
        "base-uri 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "form-action 'self'; "
        "script-src 'self' 'unsafe-inline' "
        "https://widget.trustpilot.com https://*.paypal.com https://*.paypalobjects.com "
        "https://www.googletagmanager.com https://www.google-analytics.com "
        "https://www.googleadservices.com https://www.google.com https://google.com "
        "https://pagead2.googlesyndication.com https://googleads.g.doubleclick.net; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: "
        "https://*.trustpilot.com https://*.paypalobjects.com "
        "https://*.google-analytics.com https://www.googletagmanager.com "
        "https://*.g.doubleclick.net https://googleads.g.doubleclick.net "
        "https://pagead2.googlesyndication.com https://www.googleadservices.com "
        "https://www.gstatic.com https://ssl.gstatic.com "
        f"{g}; "
        "font-src 'self' data:; "
        "connect-src 'self' "
        "https://*.trustpilot.com https://*.paypal.com https://*.paypalobjects.com "
        "https://*.google-analytics.com https://*.analytics.google.com "
        "https://www.googletagmanager.com "
        "https://*.g.doubleclick.net https://googleads.g.doubleclick.net https://ad.doubleclick.net "
        "https://pagead2.googlesyndication.com https://www.googleadservices.com "
        "https://*.merchant-center-analytics.goog "
        f"{g}; "
        "frame-src https://widget.trustpilot.com https://*.paypal.com "
        "https://www.googletagmanager.com https://*.doubleclick.net https://www.googleadservices.com; "
        "worker-src 'self'; "
        "manifest-src 'self'; "
        "media-src 'self'; "
        "upgrade-insecure-requests"
    )


def main() -> None:
    path = ROOT / "_headers"
    text = path.read_text(encoding="utf-8")
    csp = build_csp()
    if len(csp) > 3500:
        raise SystemExit(f"CSP still too long: {len(csp)} bytes")
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
    print("has_pagead2", "pagead2.googlesyndication.com" in csp)
    print("has_google_ie", "https://www.google.ie" in csp)


if __name__ == "__main__":
    main()
