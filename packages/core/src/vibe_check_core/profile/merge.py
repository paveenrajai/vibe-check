"""Apply dot-path updates to profile documents."""

from __future__ import annotations

import json
from typing import Any

PROTECTED_KEYS = {"$schema", "version", "updated_at"}


def parse_observation_value(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def apply_dot_path(profile: dict[str, Any], path: str, value: Any) -> None:
    keys = [part for part in path.split(".") if part]
    if not keys:
        msg = "Observation section path cannot be empty"
        raise ValueError(msg)
    if keys[0] in PROTECTED_KEYS:
        msg = f"Cannot write protected profile key: {keys[0]}"
        raise ValueError(msg)

    target: Any = profile
    for key in keys[:-1]:
        if key not in target:
            target[key] = {}
        if not isinstance(target[key], dict):
            msg = f"Cannot set nested path on non-object at {key!r}"
            raise ValueError(msg)
        target = target[key]

    leaf = keys[-1]
    if isinstance(target, dict):
        target[leaf] = value
        return

    msg = f"Cannot set path on non-object parent for {path!r}"
    raise ValueError(msg)
