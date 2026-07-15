import logging
import sys

import uvicorn
from vibe_check_core.config import get_config

from vibe_check_mcp.server import mcp, register_handlers

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    config = get_config()
    register_handlers()

    if config.transport == "stdio":
        mcp.run(transport="stdio")
        return

    logger.info("Starting vibe-check HTTP server on %s:%s", config.host, config.port)
    uvicorn.run(
        mcp.sse_app(),
        host=config.host,
        port=config.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
