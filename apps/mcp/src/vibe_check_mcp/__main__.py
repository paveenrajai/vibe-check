import logging
import sys

import uvicorn
from vibe_check_core.config import get_config

from vibe_check_mcp.auth import BearerTokenMiddleware
from vibe_check_mcp.server import mcp, register_handlers

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    config = get_config()
    register_handlers()

    if config.transport == "stdio":
        mcp.run(transport="stdio")
        return

    # Stateless: no in-memory sessions, so restarts don't break clients and any
    # instance can serve any request. All state lives in the data directory.
    app = mcp.streamable_http_app(host=config.host, stateless_http=True, json_response=True)
    if config.auth_token:
        app = BearerTokenMiddleware(app, config.auth_token)
    else:
        logger.warning(
            "VIBE_CHECK_AUTH_TOKEN is not set; the HTTP endpoint is unauthenticated. "
            "Set it before exposing the server beyond localhost."
        )

    logger.info(
        "Starting vibe-check Streamable HTTP server on http://%s:%s/mcp",
        config.host,
        config.port,
    )
    uvicorn.run(app, host=config.host, port=config.port, log_level="info")


if __name__ == "__main__":
    main()
