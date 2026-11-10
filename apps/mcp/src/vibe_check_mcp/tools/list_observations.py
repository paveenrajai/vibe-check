from typing import Any

from mcp.types import ToolAnnotations
from vibe_check_core.config import get_config
from vibe_check_core.profile.store import ProfileStore

from vibe_check_mcp.server import mcp


@mcp.tool(
    title="List observations",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
def list_observations(status: str | None = "pending") -> dict[str, Any]:
    """List inferred preferences awaiting review, or filter by status."""
    store = ProfileStore(get_config().data_dir)
    return {"status": status, "observations": store.list_observations(status=status)}
