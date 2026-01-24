#!/usr/bin/env python3
import argparse
import sqlite3
from pathlib import Path
from typing import Optional


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS systems (
    system_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tofar_events (
    event_id TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    origin TEXT NOT NULL,
    text TEXT NOT NULL,
    metadata_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS schema_notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    content TEXT NOT NULL
);
"""


def read_schema_text(schema_txt: Optional[str]) -> Optional[str]:
    if not schema_txt:
        return None
    path = Path(schema_txt)
    if path.exists():
        return path.read_text(encoding="utf-8")
    return schema_txt


def init_db(db_path: Path, schema_txt: Optional[str]) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
        if schema_txt:
            conn.execute(
                "INSERT INTO schema_notes (source, content) VALUES (?, ?)",
                ("schema_txt", schema_txt),
            )
        conn.commit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize Mobiius relational DB")
    parser.add_argument("--schema_txt", help="Schema text or path to schema text file")
    parser.add_argument("--out", required=True, help="SQLite output path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    schema_txt = read_schema_text(args.schema_txt)
    init_db(Path(args.out), schema_txt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
