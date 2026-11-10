from mcp.server.mcpserver import MCPServer

from vibe_check_mcp import __version__

mcp = MCPServer(
    name="vibe-check",
    title="vibe-check",
    version=__version__,
    instructions=(
        "Transparent user preference profile. Call get_profile or search_profile before "
        "tailoring output to the user. Use record_observation for inferred preferences; "
        "only the user should accept or reject observations."
    ),
)

_handlers_registered = False


def register_handlers() -> None:
    """Import tool and resource modules for side-effect registration."""
    global _handlers_registered
    if _handlers_registered:
        return
    from vibe_check_mcp import resources, tools  # noqa: F401

    _handlers_registered = True


register_handlers()
