import json
from datetime import UTC, datetime
from uuid import uuid4

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
    store.ensure_data_dir()

    observation = {
        "id": f"obs_{uuid4().hex[:12]}",
        "section": section,
        "value": value,
        "source": source,
        "confidence": confidence,
        "status": "pending",
        "created_at": datetime.now(UTC).isoformat(),
    }

    with store.observations_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(observation, ensure_ascii=False) + "\n")

    return json.dumps(observation, ensure_ascii=False)
