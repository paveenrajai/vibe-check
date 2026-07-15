# Testing

All commands run from the repo root.

## Automated

```bash
uv sync
uv run pytest -v
```

| Test | What it verifies |
|------|------------------|
| `packages/core/tests/` | Profile JSON bootstrap and storage |
| `apps/mcp/tests/test_mcp_stdio.py` | Full MCP stdio session: list tools, call `get_profile` |
| `apps/mcp/tests/test_mcp_http.py` | HTTP server starts; `/sse` responds |

## MCP Inspector (manual)

Handlers register when the installed package loads. Use `inspector.py`, not `server.py:mcp`:

```bash
VIBE_CHECK_DATA_DIR=./data \
  uv run mcp dev apps/mcp/inspector.py:mcp
```

Open the Inspector URL printed in the terminal. Try `get_profile` and read `vibe-check://profile`.

> **Why not `server.py:mcp`?** `mcp dev` loads that file in isolation, which creates a second empty FastMCP instance. Tools register on the package instance instead, so `tools/list` returns `[]`.

## Cursor & Claude Desktop (manual, stdio)

macOS and Windows: see [`docs/connecting.md`](connecting.md). Restart the client → MCP / Connectors → confirm `vibe-check` is connected.

## Docker (optional)

```bash
docker compose up --build -d
curl -s -o /dev/null -w "%{http_code}\n" --max-time 2 http://localhost:3100/sse
docker compose down
```

Expect `200`. Use `--max-time` because `/sse` is a long-lived stream.
