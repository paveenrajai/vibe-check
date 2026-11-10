from typing import Any

from mcp.types import ToolAnnotations
from vibe_check_core.config import get_config
from vibe_check_core.profile.store import ProfileStore

from vibe_check_mcp.server import mcp


@mcp.tool(
    title="Update profile section",
    annotations=ToolAnnotations(
        read_only_hint=False,
        destructive_hint=True,
        idempotent_hint=True,
        open_world_hint=False,
    ),
)
def update_profile(section: str, value: dict[str, Any]) -> dict[str, Any]:
    """Set or replace a top-level profile section (user-initiated)."""
    store = ProfileStore(get_config().data_dir)
    profile = store.load_profile()
    profile[section] = value
    store.save_profile(profile, source="update_profile")
    return {"ok": True, "section": section}
