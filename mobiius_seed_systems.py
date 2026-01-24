#!/usr/bin/env python3
import argparse
import sqlite3
from pathlib import Path


SEED_SYSTEMS = [
    ("Mobiius Core", "Baseline relational spine for TOFAR logging and routing"),
    ("Whisper", "Speech-to-text ingestion pipeline"),
    ("heyMicojava", "SVG-to-emoji rendering workflow"),
]


def seed(db_path: Path) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.executemany(
            "INSERT INTO systems (name, description) VALUES (?, ?)",
            SEED_SYSTEMS,
        )
        conn.commit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed Mobiius system rows")
    parser.add_argument("--db", required=True, help="SQLite database path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    seed(Path(args.db))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
