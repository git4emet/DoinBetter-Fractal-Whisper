#!/usr/bin/env python3
"""Build tilesheet.json from SVG metadata."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SVG_DIR = Path("assets/heyMicojava_labels_svg_morning")
OUT_PATH = Path("build/tilesheet.json")

METADATA_RE = re.compile(r"<metadata>(.*?)</metadata>", re.DOTALL | re.IGNORECASE)


@dataclass
class SvgTile:
    name: str
    path: str
    metadata: dict[str, Any]


def parse_metadata(svg_text: str) -> dict[str, Any]:
    match = METADATA_RE.search(svg_text)
    if not match:
        return {}
    raw = match.group(1).strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def build_tiles(svg_dir: Path) -> list[SvgTile]:
    tiles: list[SvgTile] = []
    for svg_path in sorted(svg_dir.glob("*.svg")):
        svg_text = svg_path.read_text(encoding="utf-8")
        tiles.append(
            SvgTile(
                name=svg_path.stem,
                path=str(svg_path.as_posix()),
                metadata=parse_metadata(svg_text),
            )
        )
    return tiles


def main() -> None:
    tiles = build_tiles(SVG_DIR)
    payload = {
        "source": str(SVG_DIR.as_posix()),
        "count": len(tiles),
        "tiles": [tile.__dict__ for tile in tiles],
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
