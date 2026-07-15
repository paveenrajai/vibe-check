"""Profile validation against JSON Schema."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from typing import Any

import jsonschema

PROFILE_VALIDATION_ID = "vibe-check/profile/v1"


class ProfileValidationError(ValueError):
    """Raised when a profile document fails schema validation."""


@lru_cache(maxsize=1)
def load_profile_schema() -> dict[str, Any]:
    text = resources.files("vibe_check_core.schemas").joinpath("profile.v1.json").read_text(
        encoding="utf-8"
    )
    return json.loads(text)


def validate_profile(profile: dict[str, Any]) -> None:
    schema = load_profile_schema()
    try:
        jsonschema.validate(instance=profile, schema=schema)
    except jsonschema.ValidationError as exc:
        path = ".".join(str(part) for part in exc.absolute_path) or "(root)"
        msg = f"Profile validation failed at {path}: {exc.message}"
        raise ProfileValidationError(msg) from exc
