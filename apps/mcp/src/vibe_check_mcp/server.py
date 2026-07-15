from mcp.server.fastmcp import FastMCP

mcp = FastMCP("vibe-check")

_handlers_registered = False


def register_handlers() -> None:
    """Import tool and resource modules for side-effect registration."""
    global _handlers_registered
    if _handlers_registered:
        return
    from vibe_check_mcp import resources, tools  # noqa: F401

    _handlers_registered = True


register_handlers()
