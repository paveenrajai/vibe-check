import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx
import pytest


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _sse_status_code(url: str) -> int:
    timeout = httpx.Timeout(5.0, connect=2.0, read=0.5)
    with httpx.Client(timeout=timeout) as client:
        with client.stream("GET", url) as response:
            return response.status_code


@pytest.fixture
def http_server(tmp_path: Path):
    port = _free_port()
    env = {
        **os.environ,
        "VIBE_CHECK_DATA_DIR": str(tmp_path),
        "VIBE_CHECK_TRANSPORT": "http",
        "VIBE_CHECK_HOST": "127.0.0.1",
        "VIBE_CHECK_PORT": str(port),
    }
    proc = subprocess.Popen(
        [sys.executable, "-m", "vibe_check_mcp"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    url = f"http://127.0.0.1:{port}/sse"
    deadline = time.time() + 10
    last_error: Exception | None = None
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError("MCP HTTP server exited early")
        try:
            if _sse_status_code(url) < 500:
                break
        except Exception as exc:  # noqa: BLE001 — polling until server is up
            last_error = exc
            time.sleep(0.2)
    else:
        proc.terminate()
        msg = f"MCP HTTP server did not become ready at {url}"
        if last_error:
            msg = f"{msg}: {last_error}"
        raise TimeoutError(msg)

    yield url

    proc.terminate()
    proc.wait(timeout=5)


def test_mcp_http_sse_endpoint_responds(http_server: str) -> None:
    assert _sse_status_code(http_server) == 200
