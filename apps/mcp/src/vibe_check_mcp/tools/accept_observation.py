import json

from vibe_check_core.config import get_config
from vibe_check_core.profile.store import ProfileStore

from vibe_check_mcp.server import mcp


@mcp.tool()
def accept_observation(observation_id: str) -> str:
    """Accept a pending observation and merge it into the profile."""
    store = ProfileStore(get_config().data_dir)
    observation = store.accept_observation(observation_id)
    return json.dumps(observation, indent=2, ensure_ascii=False)
