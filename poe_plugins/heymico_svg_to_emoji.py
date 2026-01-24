import json
import os
import re
import urllib.request
from typing import Any, Dict

SVG_PATTERN = re.compile(r"svg:(?P<path>\S+)")


def _maybe_call_emoji_server(svg_path: str) -> Dict[str, Any]:
    url = os.environ.get("EMOJI_SERVER_URL")
    if not url:
        return {
            "emoji_server": "skipped",
            "reason": "EMOJI_SERVER_URL not set",
        }

    payload = json.dumps({"svg_path": svg_path}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            body = response.read().decode("utf-8")
        return {
            "emoji_server": "ok",
            "response": body,
        }
    except Exception as exc:
        return {
            "emoji_server": "error",
            "error": str(exc),
        }


def handle(event: Dict[str, Any]) -> Dict[str, Any]:
    text = event.get("text", "")
    match = SVG_PATTERN.search(text)
    if not match:
        return {
            "metadata": {
                "routing": {
                    "status": "ignored",
                    "handler": "heymico_svg_to_emoji",
                    "message": "No svg: payload detected",
                }
            }
        }

    svg_path = match.group("path")
    emoji_result = _maybe_call_emoji_server(svg_path)
    return {
        "metadata": {
            "routing": {
                "status": "handled",
                "handler": "heymico_svg_to_emoji",
            },
            "heymico": {
                "svg_path": svg_path,
                "emoji_result": emoji_result,
            },
        }
    }


def register(registry) -> None:
    registry.register("whisper.text", handle)
