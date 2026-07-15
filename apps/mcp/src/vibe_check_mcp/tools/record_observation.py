import json

from vibe_check_core.config import get_config
from vibe_check_core.profile.store import ProfileStore

from vibe_check_mcp.server import mcp


@mcp.tool()
def record_observation(
    section: str,
    value: str,
    source: str,
    confidence: float = 0.8,
) -> str:
    """Log an inferred preference for later review (does not merge into profile yet)."""
    store = ProfileStore(get_config().data_dir)
    observation = store.record_observation(
        section=section,
        value=value,
        source=source,
        confidence=confidence,
    )
    return json.dumps(observation, ensure_ascii=False)
