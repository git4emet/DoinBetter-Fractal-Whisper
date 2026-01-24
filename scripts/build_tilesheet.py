#!/usr/bin/env python3
"""Build tilesheet JSON from heyMicojava SVGs."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


KEY_VALUE_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+)\s*[:=]\s*(.+?)\s*$")


def _read_metadata(svg_path: Path) -> dict:
    metadata: dict[str, str | float | int | dict] = {}
    try:
        tree = ET.parse(svg_path)
    except ET.ParseError:
        return metadata

    root = tree.getroot()
    metadata_nodes = root.findall("{http://www.w3.org/2000/svg}metadata") + root.findall("metadata")
    if not metadata_nodes:
        return metadata

    raw_chunks = []
    for node in metadata_nodes:
        if node.text:
            raw_chunks.append(node.text.strip())
    raw_text = "\n".join(chunk for chunk in raw_chunks if chunk)
    if not raw_text:
        return metadata

    raw_text = raw_text.strip()
    if raw_text.startswith("{") and raw_text.endswith("}"):
        try:
            parsed = json.loads(raw_text)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    for line in raw_text.splitlines():
        match = KEY_VALUE_RE.match(line)
        if not match:
            continue
        key, value = match.groups()
        metadata[key] = value

    return metadata


def _parse_dimension(value: str | None) -> float | None:
    if not value:
        return None
    match = re.match(r"([0-9.]+)", value)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def build_tilesheet(source_dir: Path, output_path: Path) -> dict:
    entries = []
    for svg_path in sorted(source_dir.glob("*.svg")):
        contents = svg_path.read_bytes()
        metadata = _read_metadata(svg_path)
        root = None
        try:
            root = ET.fromstring(contents)
        except ET.ParseError:
            root = None
        width = _parse_dimension(root.get("width") if root is not None else None)
        height = _parse_dimension(root.get("height") if root is not None else None)
        emoji_hash = hashlib.sha256(contents).hexdigest()
        label = metadata.get("label") if isinstance(metadata, dict) else None
        entries.append(
            {
                "id": svg_path.stem,
                "label": label or svg_path.stem,
                "file": svg_path.as_posix(),
                "hash": emoji_hash,
                "dimensions": {
                    "width": width,
                    "height": height,
                },
                "metadata": metadata,
            }
        )

    tilesheet = {
        "source": source_dir.as_posix(),
        "count": len(entries),
        "tiles": entries,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(tilesheet, indent=2, sort_keys=True) + "\n")
    return tilesheet


def main() -> None:
    parser = argparse.ArgumentParser(description="Build tilesheet JSON from heyMicojava SVGs.")
    parser.add_argument(
        "--source",
        default="assets/heyMicojava_labels_svg_morning",
        help="Directory with SVG glyphs.",
    )
    parser.add_argument(
        "--output",
        default="assets/tilesheet.json",
        help="Output tilesheet JSON path.",
    )
    args = parser.parse_args()

    source_dir = Path(args.source)
    output_path = Path(args.output)
    build_tilesheet(source_dir, output_path)


if __name__ == "__main__":
    main()
