import json

from vibe_check_core.config import get_config
from vibe_check_core.profile.query import get_section
from vibe_check_core.profile.store import ProfileStore

from vibe_check_mcp.server import mcp


@mcp.tool()
def get_profile(section: str | None = None) -> str:
    """Fetch the user profile or a single section (e.g. communication, code, context)."""
    store = ProfileStore(get_config().data_dir)
    profile = store.load_profile()
    payload = get_section(profile, section)
    return json.dumps(payload, indent=2, ensure_ascii=False)
