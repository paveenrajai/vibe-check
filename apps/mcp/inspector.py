"""MCP Inspector entry point.

Use with:
    VIBE_CHECK_DATA_DIR=./data uv run mcp dev apps/mcp/inspector.py:mcp

Do not use server.py:mcp directly — file loading creates a second FastMCP
instance without registered tools.
"""

from vibe_check_mcp.server import mcp

__all__ = ["mcp"]
