#!/usr/bin/env python3
"""Pre-render pipeline for emoji assets."""
from __future__ import annotations

import subprocess
import sys


def main() -> None:
    result = subprocess.run([sys.executable, "scripts/build_tilesheet.py"], check=False)
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
