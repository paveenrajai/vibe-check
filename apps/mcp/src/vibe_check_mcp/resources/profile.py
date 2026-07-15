import json

from vibe_check_core.config import get_config
from vibe_check_core.profile.query import get_section
from vibe_check_core.profile.store import ProfileStore

from vibe_check_mcp.server import mcp


@mcp.resource("vibe-check://profile")
def profile_resource() -> str:
    """Full user preference profile."""
    store = ProfileStore(get_config().data_dir)
    return json.dumps(store.load_profile(), indent=2, ensure_ascii=False)


@mcp.resource("vibe-check://profile/{section}")
def profile_section_resource(section: str) -> str:
    """Single profile section (communication, code, design, context, etc.)."""
    store = ProfileStore(get_config().data_dir)
    profile = store.load_profile()
    payload = get_section(profile, section)
    return json.dumps(payload, indent=2, ensure_ascii=False)
