from typing import Any

from mcp.types import ToolAnnotations
from vibe_check_core.config import get_config
from vibe_check_core.profile.store import ProfileStore

from vibe_check_mcp.server import mcp


@mcp.tool(
    title="Reject observation",
    annotations=ToolAnnotations(
        read_only_hint=False,
        destructive_hint=False,
        idempotent_hint=False,
        open_world_hint=False,
    ),
)
def reject_observation(observation_id: str) -> dict[str, Any]:
    """Reject a pending observation without changing the profile."""
    store = ProfileStore(get_config().data_dir)
    return store.reject_observation(observation_id)
