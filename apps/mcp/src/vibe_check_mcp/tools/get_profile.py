from typing import Any

from mcp.types import ToolAnnotations
from vibe_check_core.config import get_config
from vibe_check_core.profile.query import get_section
from vibe_check_core.profile.store import ProfileStore

from vibe_check_mcp.server import mcp


@mcp.tool(
    title="Get profile",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
def get_profile(section: str | None = None) -> dict[str, Any]:
    """Fetch the user profile or a single section (e.g. communication, code, context)."""
    store = ProfileStore(get_config().data_dir)
    return get_section(store.load_profile(), section)
