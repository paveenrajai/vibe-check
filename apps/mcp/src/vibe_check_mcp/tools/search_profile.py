import json

from vibe_check_core.config import get_config
from vibe_check_core.profile.query import search_profile as search
from vibe_check_core.profile.store import ProfileStore

from vibe_check_mcp.server import mcp


@mcp.tool()
def search_profile(query: str) -> str:
    """Retrieve profile snippets relevant to a task or keyword."""
    store = ProfileStore(get_config().data_dir)
    profile = store.load_profile()
    matches = search(profile, query)
    return json.dumps(matches, indent=2, ensure_ascii=False)
