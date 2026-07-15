from mcp.server.fastmcp import FastMCP

mcp = FastMCP("vibe-check")


def register_handlers() -> None:
    """Import tool and resource modules for side-effect registration."""
    from vibe_check_mcp import resources, tools  # noqa: F401
