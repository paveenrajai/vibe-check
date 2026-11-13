import json
import os
import sys
from pathlib import Path

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    return tmp_path / "data"


@pytest.mark.asyncio
async def test_mcp_stdio_lists_tools_and_gets_profile(data_dir: Path) -> None:
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "vibe_check_mcp"],
        env={
            **os.environ,
            "VIBE_CHECK_DATA_DIR": str(data_dir),
            "VIBE_CHECK_TRANSPORT": "stdio",
        },
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            tool_names = sorted(t.name for t in tools.tools)
            assert tool_names == [
                "accept_observation",
                "get_profile",
                "list_observations",
                "record_observation",
                "reject_observation",
                "search_profile",
                "update_profile",
            ]

            result = await session.call_tool(
                "get_profile",
                arguments={"section": "communication"},
            )
            assert result.structured_content["communication"]["verbosity"] == "concise"
            # Text content stays JSON for clients that ignore structured output.
            payload = json.loads(result.content[0].text)
            assert payload == result.structured_content

            tool_by_name = {t.name: t for t in tools.tools}
            assert tool_by_name["get_profile"].annotations.read_only_hint is True
            assert tool_by_name["update_profile"].annotations.destructive_hint is True
            assert tool_by_name["get_profile"].output_schema is not None
            assert (data_dir / "profile.json").exists()
