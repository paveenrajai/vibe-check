import json
from typing import Any

from vibe_check_core.config import get_config
from vibe_check_core.profile.store import ProfileStore

from vibe_check_mcp.server import mcp


@mcp.tool()
def update_profile(section: str, value: dict[str, Any]) -> str:
    """Set or replace a top-level profile section (user-initiated)."""
    store = ProfileStore(get_config().data_dir)
    profile = store.load_profile()
    profile[section] = value
    store.save_profile(profile, source="update_profile")
    return json.dumps({"ok": True, "section": section}, ensure_ascii=False)
