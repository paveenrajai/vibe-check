import json

from vibe_check_core.config import get_config
from vibe_check_core.profile.store import ProfileStore

from vibe_check_mcp.server import mcp


@mcp.tool()
def reject_observation(observation_id: str) -> str:
    """Reject a pending observation without changing the profile."""
    store = ProfileStore(get_config().data_dir)
    observation = store.reject_observation(observation_id)
    return json.dumps(observation, indent=2, ensure_ascii=False)
