import os
import socket
import subprocess
import sys
import time
from collections.abc import Iterator
from pathlib import Path

import httpx
import httpx2
import pytest
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

TOKEN = "test-token"


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _start_server(tmp_path: Path, token: str | None) -> tuple[subprocess.Popen, str]:
    port = _free_port()
    env = {
        **os.environ,
        "VIBE_CHECK_DATA_DIR": str(tmp_path),
        "VIBE_CHECK_TRANSPORT": "http",
        "VIBE_CHECK_HOST": "127.0.0.1",
        "VIBE_CHECK_PORT": str(port),
    }
    env.pop("VIBE_CHECK_AUTH_TOKEN", None)
    if token:
        env["VIBE_CHECK_AUTH_TOKEN"] = token
    proc = subprocess.Popen(
        [sys.executable, "-m", "vibe_check_mcp"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    url = f"http://127.0.0.1:{port}/mcp"
    deadline = time.time() + 10
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError("MCP HTTP server exited early")
        try:
            httpx.get(url, timeout=0.5)
            return proc, url
        except httpx.HTTPError:
            time.sleep(0.2)
    proc.terminate()
    raise TimeoutError(f"MCP HTTP server did not become ready at {url}")


@pytest.fixture
def http_server(tmp_path: Path) -> Iterator[str]:
    proc, url = _start_server(tmp_path, TOKEN)
    yield url
    proc.terminate()
    proc.wait(timeout=5)


def test_mcp_http_rejects_missing_token(http_server: str) -> None:
    response = httpx.post(http_server, json={}, timeout=2)
    assert response.status_code == 401


def test_mcp_http_rejects_wrong_token(http_server: str) -> None:
    response = httpx.post(http_server, json={}, headers={"Authorization": "Bearer nope"}, timeout=2)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_mcp_streamable_http_round_trip(http_server: str) -> None:
    headers = {"Authorization": f"Bearer {TOKEN}"}
    async with httpx2.AsyncClient(headers=headers) as client:
        async with streamable_http_client(http_server, http_client=client) as streams:
            read, write = streams[0], streams[1]
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                assert "get_profile" in {t.name for t in tools.tools}

                result = await session.call_tool(
                    "get_profile", arguments={"section": "communication"}
                )
                assert result.structured_content is not None
                assert result.structured_content["communication"]["verbosity"] == "concise"


def test_mcp_http_is_stateless(http_server: str) -> None:
    init = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "0"},
        },
    }
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json, text/event-stream",
    }
    response = httpx.post(http_server, json=init, headers=headers, timeout=5)
    assert response.status_code == 200
    assert "mcp-session-id" not in response.headers
    assert response.headers["content-type"].startswith("application/json")

    # A tools call with no session header must work without a prior handshake on this connection.
    call = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "get_profile", "arguments": {"section": "communication"}},
    }
    response = httpx.post(http_server, json=call, headers=headers, timeout=5)
    assert response.status_code == 200
    body = response.json()
    assert body["result"]["structuredContent"]["communication"]["verbosity"] == "concise"
