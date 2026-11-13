from typing import Any

from mcp.types import ToolAnnotations
from vibe_check_core.config import get_config
from vibe_check_core.profile.store import ProfileStore

from vibe_check_mcp.server import mcp


@mcp.tool(
    title="Record observation",
    annotations=ToolAnnotations(
        read_only_hint=False,
        destructive_hint=False,
        idempotent_hint=False,
        open_world_hint=False,
    ),
)
def record_observation(
    section: str,
    value: str,
    source: str,
    confidence: float = 0.8,
) -> dict[str, Any]:
    """Log an inferred preference for later review (does not merge into profile yet)."""
    store = ProfileStore(get_config().data_dir)
    return store.record_observation(
        section=section,
        value=value,
        source=source,
        confidence=confidence,
    )
