# Self-hosting

## Docker (recommended for HTTP)

```bash
docker compose up -d --build
```

Default: stdio is not used in Docker; the container exposes HTTP on port `3100`.

Environment:

| Variable | Default | Description |
|----------|---------|-------------|
| `VIBE_CHECK_DATA_DIR` | `/data` | Profile storage (mount a volume) |
| `VIBE_CHECK_TRANSPORT` | `http` | `stdio` or `http` |
| `VIBE_CHECK_HOST` | `0.0.0.0` | HTTP bind address |
| `VIBE_CHECK_PORT` | `3100` | HTTP listen port |
| `VIBE_CHECK_AUTH_TOKEN` | — | Required for non-localhost HTTP (planned) |

## Volume

Mount host directory for persistence:

```yaml
volumes:
  - ./data:/data
```

## MCP over HTTP

The server mounts FastMCP's SSE app via uvicorn. Point clients that support remote MCP at:

```
http://localhost:3100/sse
```

Auth header support is planned: `Authorization: Bearer <VIBE_CHECK_AUTH_TOKEN>`.

## Local stdio (no Docker)

For Cursor / Claude Desktop:

```json
{
  "mcpServers": {
    "vibe-check": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/vibe-check", "run", "vibe-check"],
      "env": {
        "VIBE_CHECK_DATA_DIR": "/absolute/path/to/vibe-check/data",
        "VIBE_CHECK_TRANSPORT": "stdio"
      }
    }
  }
}
```

Alternative without uv in PATH:

```json
{
  "mcpServers": {
    "vibe-check": {
      "command": "/absolute/path/to/vibe-check/.venv/bin/python",
      "args": ["-m", "vibe_check"],
      "env": {
        "VIBE_CHECK_DATA_DIR": "/absolute/path/to/vibe-check/data"
      }
    }
  }
}
```

## Claude Desktop

After `uv sync`, install via MCP CLI:

```bash
uv run mcp install src/vibe_check/__main__.py --name vibe-check \
  -v VIBE_CHECK_DATA_DIR=/absolute/path/to/vibe-check/data
```
