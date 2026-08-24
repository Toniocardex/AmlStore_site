#!/usr/bin/env python3
"""Apply schema.sql (+ stock migration) to all local Miniflare D1 sqlite files used by pages dev."""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = (ROOT / "schema.sql").read_text(encoding="utf-8")
STOCK = (ROOT / "schema-stock-migration.sql").read_text(encoding="utf-8")
CHAT_CORE = (ROOT / "migrations" / "0002_chat_core.sql").read_text(encoding="utf-8")
D1_DIRS = [
    ROOT / ".wrangler" / "state-chat" / "v3" / "d1" / "miniflare-D1DatabaseObject",
    ROOT / ".wrangler" / "state-pages" / "v3" / "d1" / "miniflare-D1DatabaseObject",
    # Legacy location kept so existing local databases are upgraded once.
    ROOT / ".wrangler" / "state" / "v3" / "d1" / "miniflare-D1DatabaseObject",
]
existing_dirs = [path for path in D1_DIRS if path.exists()]

DELETION_JOBS_V2 = """
CREATE TABLE chat_deletion_jobs_v2 (
    id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL UNIQUE,
    requested_by TEXT NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'PENDING',
    previous_status TEXT,
    previous_closed_at INTEGER,
    previous_archived_at INTEGER,
    previous_archive_at INTEGER,
    previous_purge_at INTEGER,
    attempts INTEGER NOT NULL DEFAULT 0,
    next_attempt_at INTEGER,
    last_error TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    completed_at INTEGER,
    CHECK (status IN ('PENDING','GATED','DO_DELETED','COMPLETE','FAILED'))
);
"""


def upgrade_deletion_jobs(con: sqlite3.Connection) -> None:
    row = con.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='chat_deletion_jobs'"
    ).fetchone()
    if not row or ('DO_DELETED' in row[0] and 'previous_status' in row[0]):
        return
    columns = {item[1] for item in con.execute("PRAGMA table_info(chat_deletion_jobs)")}
    con.executescript(DELETION_JOBS_V2)
    previous = lambda name: name if name in columns else "NULL"
    con.execute(f"""
        INSERT INTO chat_deletion_jobs_v2 (
            id, conversation_id, requested_by, reason, status,
            previous_status, previous_closed_at, previous_archived_at,
            previous_archive_at, previous_purge_at,
            attempts, next_attempt_at, last_error, created_at, updated_at, completed_at
        )
        SELECT id, conversation_id, requested_by, reason,
               CASE status WHEN 'D1_DELETED' THEN 'DO_DELETED' ELSE status END,
               {previous('previous_status')}, {previous('previous_closed_at')},
               {previous('previous_archived_at')}, {previous('previous_archive_at')},
               {previous('previous_purge_at')},
               attempts, next_attempt_at, last_error, created_at, updated_at, completed_at
        FROM chat_deletion_jobs
    """)
    con.executescript("""
        DROP TABLE chat_deletion_jobs;
        ALTER TABLE chat_deletion_jobs_v2 RENAME TO chat_deletion_jobs;
        CREATE INDEX IF NOT EXISTS idx_chat_deletion_jobs_pending
        ON chat_deletion_jobs(status, next_attempt_at, created_at);
    """)

if not existing_dirs:
    print("No local D1 dir yet — run wrangler pages dev once, then re-run this script.")
    raise SystemExit(1)

applied = 0
for d1_dir in existing_dirs:
    for db_path in sorted(d1_dir.glob("*.sqlite")):
        if db_path.name == "metadata.sqlite":
            continue
        con = sqlite3.connect(db_path)
        con.executescript(SCHEMA)
        con.executescript(STOCK)
        con.executescript(CHAT_CORE)
        upgrade_deletion_jobs(con)
        con.commit()
        tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        con.close()
        print(f"OK {db_path.name[:12]}… tables={tables}")
        applied += 1

if not applied:
    print("No D1 database files found.")
    raise SystemExit(1)

print(f"Schema applied to {applied} local database(s).")
