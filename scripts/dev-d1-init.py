#!/usr/bin/env python3
"""Apply schema.sql to all local Miniflare D1 sqlite files used by pages dev."""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = (ROOT / "schema.sql").read_text(encoding="utf-8")
D1_DIR = ROOT / ".wrangler" / "state" / "v3" / "d1" / "miniflare-D1DatabaseObject"

if not D1_DIR.exists():
    print("No local D1 dir yet — run wrangler pages dev once, then re-run this script.")
    raise SystemExit(1)

applied = 0
for db_path in sorted(D1_DIR.glob("*.sqlite")):
    if db_path.name == "metadata.sqlite":
        continue
    con = sqlite3.connect(db_path)
    con.executescript(SCHEMA)
    con.commit()
    tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    con.close()
    print(f"OK {db_path.name[:12]}… tables={tables}")
    applied += 1

if not applied:
    print("No D1 database files found.")
    raise SystemExit(1)

print(f"Schema applied to {applied} local database(s).")
