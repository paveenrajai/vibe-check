import json

from vibe_check_core.config import get_config
from vibe_check_core.profile.store import ProfileStore

from vibe_check_mcp.server import mcp


@mcp.tool()
def list_observations(status: str | None = "pending") -> str:
    """List inferred preferences awaiting review, or filter by status."""
    store = ProfileStore(get_config().data_dir)
    observations = store.list_observations(status=status)
    return json.dumps(observations, indent=2, ensure_ascii=False)
