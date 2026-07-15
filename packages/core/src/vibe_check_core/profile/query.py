import json
from typing import Any


def get_section(profile: dict[str, Any], section: str | None) -> dict[str, Any]:
    if section is None:
        return profile
    if section not in profile:
        msg = f"Unknown profile section: {section!r}"
        raise KeyError(msg)
    return {section: profile[section]}


def search_profile(profile: dict[str, Any], query: str) -> list[dict[str, str]]:
    """Naive substring search across profile values. Replace with better ranking later."""
    needle = query.lower()
    matches: list[dict[str, str]] = []

    def walk(prefix: str, value: Any) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                walk(f"{prefix}.{key}" if prefix else key, nested)
            return
        if isinstance(value, list):
            for index, item in enumerate(value):
                walk(f"{prefix}[{index}]", item)
            return
        text = json.dumps(value) if not isinstance(value, str) else value
        if needle in text.lower():
            matches.append({"path": prefix, "value": text})

    walk("", profile)
    return matches
