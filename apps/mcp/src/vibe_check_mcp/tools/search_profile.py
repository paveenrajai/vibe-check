from typing import Any

from mcp.types import ToolAnnotations
from vibe_check_core.config import get_config
from vibe_check_core.profile.query import search_profile as search
from vibe_check_core.profile.store import ProfileStore

from vibe_check_mcp.server import mcp


@mcp.tool(
    title="Search profile",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
def search_profile(query: str) -> dict[str, Any]:
    """Retrieve profile snippets relevant to a task or keyword."""
    store = ProfileStore(get_config().data_dir)
    return {"query": query, "matches": search(store.load_profile(), query)}
