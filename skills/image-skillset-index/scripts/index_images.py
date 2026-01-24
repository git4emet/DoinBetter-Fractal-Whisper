#!/usr/bin/env python3
"""Create/update a skillsset image index from local image files."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import mimetypes
import os
from pathlib import Path
import shutil
from typing import Any

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff", ".tif"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_captions(path: Path | None) -> dict[str, str]:
    if not path:
        return {}
    if not path.exists():
        raise FileNotFoundError(f"Captions file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_image_size(path: Path) -> dict[str, int] | None:
    if importlib.util.find_spec("PIL") is None:
        return None
    from PIL import Image  # pylint: disable=import-error

    with Image.open(path) as img:
        width, height = img.size
    return {"width": width, "height": height}


def try_ocr_text(path: Path) -> str | None:
    if importlib.util.find_spec("pytesseract") is None:
        return None
    if shutil.which("tesseract") is None:
        return None
    import pytesseract  # pylint: disable=import-error
    from PIL import Image  # pylint: disable=import-error

    with Image.open(path) as img:
        return pytesseract.image_to_string(img).strip() or None


def build_entry(path: Path, captions: dict[str, str]) -> dict[str, Any]:
    rel_path = str(path)
    entry: dict[str, Any] = {
        "path": rel_path,
        "filename": path.name,
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
        "mime": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
        "indexed_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
    size = load_image_size(path)
    if size:
        entry["size"] = size
    if path.name in captions:
        entry["caption"] = captions[path.name]
    text = try_ocr_text(path)
    if text:
        entry["ocr_text"] = text
    return entry


def main() -> None:
    parser = argparse.ArgumentParser(description="Index image files into a skillsset JSON.")
    parser.add_argument("input", help="Directory containing images to index.")
    parser.add_argument(
        "--output",
        default="skillsset_index.json",
        help="Output JSON file path (default: skillsset_index.json).",
    )
    parser.add_argument(
        "--captions",
        help="Optional JSON file mapping filenames to captions.",
    )
    args = parser.parse_args()

    input_dir = Path(args.input)
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    captions = load_captions(Path(args.captions)) if args.captions else {}

    entries = []
    for path in sorted(input_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        entries.append(build_entry(path, captions))

    output = {
        "generated_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "input": str(input_dir),
        "count": len(entries),
        "entries": entries,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
