from datetime import UTC, datetime
from typing import Any

PROFILE_SCHEMA_VERSION = 1
PROFILE_SCHEMA_ID = "vibe-check/profile/v1"


def default_profile() -> dict[str, Any]:
    return {
        "$schema": PROFILE_SCHEMA_ID,
        "version": PROFILE_SCHEMA_VERSION,
        "updated_at": datetime.now(UTC).isoformat(),
        "communication": {
            "verbosity": "concise",
            "tone": ["warm", "direct"],
            "formatting": {"prefer_markdown": True},
            "notes": "",
        },
        "code": {
            "naming": "match surrounding conventions",
            "css_units": "rem/em only, never px",
            "scope": "minimal diffs",
            "comments": "only non-obvious logic",
        },
        "design": {"aesthetic": "clean, accessible", "colors": {}, "typography": {}},
        "personality": {"traits": [], "addressing": ""},
        "interests": [],
        "context": {"current_projects": [], "goals": [], "blockers": []},
        "tooling": {},
        "custom": {},
    }
