#!/usr/bin/env python3
import argparse
import importlib.util
import json
import sqlite3
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Optional

Handler = Callable[[Dict[str, Any]], Dict[str, Any]]


@dataclass
class Event:
    event_id: str
    kind: str
    origin: str
    text: str
    metadata: Dict[str, Any]
    created_at: str


class HandlerRegistry:
    def __init__(self) -> None:
        self._handlers: Dict[str, Handler] = {}

    def register(self, kind: str, handler: Handler) -> None:
        self._handlers[kind] = handler

    def get(self, kind: str) -> Optional[Handler]:
        return self._handlers.get(kind)

    def kinds(self) -> Iterable[str]:
        return sorted(self._handlers.keys())


def normalize(kind: str, origin: str, text: str) -> Event:
    return Event(
        event_id=str(uuid.uuid4()),
        kind=kind.strip(),
        origin=origin.strip(),
        text=text.strip(),
        metadata={},
        created_at=datetime.now(timezone.utc).isoformat(),
    )


def guardian_gate(event: Event) -> Event:
    if not event.text:
        raise ValueError("Guardian gate rejected empty text payload")
    return event


def route(event: Event, registry: HandlerRegistry) -> Event:
    handler = registry.get(event.kind)
    if handler:
        update = handler(
            {
                "event_id": event.event_id,
                "kind": event.kind,
                "origin": event.origin,
                "text": event.text,
                "metadata": dict(event.metadata),
                "created_at": event.created_at,
            }
        )
        event.metadata.update(update.get("metadata", {}))
    else:
        event.metadata.setdefault("routing", {}).update(
            {
                "status": "unhandled",
                "message": f"No handler registered for {event.kind}",
            }
        )
    return event


def ensure_db(db_path: Path) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tofar_events (
                event_id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                origin TEXT NOT NULL,
                text TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def log_tofar(event: Event, db_path: Path) -> None:
    ensure_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO tofar_events (
                event_id,
                kind,
                origin,
                text,
                metadata_json,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                event.event_id,
                event.kind,
                event.origin,
                event.text,
                json.dumps(event.metadata, ensure_ascii=False),
                event.created_at,
            ),
        )
        conn.commit()


def emit(event: Event) -> None:
    payload = {
        "event_id": event.event_id,
        "kind": event.kind,
        "origin": event.origin,
        "text": event.text,
        "metadata": event.metadata,
        "created_at": event.created_at,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def load_plugins(registry: HandlerRegistry, plugins_dir: Path) -> None:
    if not plugins_dir.exists():
        return
    for plugin_path in sorted(plugins_dir.glob("*.py")):
        spec = importlib.util.spec_from_file_location(plugin_path.stem, plugin_path)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        register_fn = getattr(module, "register", None)
        if callable(register_fn):
            register_fn(registry)


def build_default_registry() -> HandlerRegistry:
    registry = HandlerRegistry()

    def default_handler(event: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "metadata": {
                "routing": {
                    "status": "accepted",
                    "handler": "default",
                }
            }
        }

    registry.register("whisper.text", default_handler)
    return registry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="POE Orchestrator")
    parser.add_argument("--db", required=True, help="SQLite database path")
    parser.add_argument("--plugins", help="Directory of plugin handlers")

    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="Run a single event")
    run_parser.add_argument("--kind", required=True)
    run_parser.add_argument("--origin", required=True)
    run_parser.add_argument("--text", required=True)

    list_parser = subparsers.add_parser("list", help="List registered handlers")
    list_parser.add_argument("--kind", help="Filter by kind")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    db_path = Path(args.db)

    registry = build_default_registry()
    if args.plugins:
        load_plugins(registry, Path(args.plugins))

    if args.command == "list":
        kinds = registry.kinds()
        if args.kind:
            kinds = [kind for kind in kinds if kind == args.kind]
        for kind in kinds:
            print(kind)
        return 0

    event = normalize(args.kind, args.origin, args.text)
    event = guardian_gate(event)
    event = route(event, registry)
    log_tofar(event, db_path)
    emit(event)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
