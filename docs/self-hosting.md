# Self-hosting

## stdio (recommended)

For **Cursor** and **Claude Desktop** on macOS and Windows. See **[`connecting.md`](connecting.md)**.

---

## Docker + HTTP (optional)

For clients that support a remote MCP URL (e.g. Cursor URL mode). **Not supported natively by Claude Desktop.**

```bash
docker compose up -d --build
```

Server listens on `http://localhost:3100/mcp` (Streamable HTTP transport, stateless mode).

The HTTP server is **stateless**: it issues no `mcp-session-id`, keeps nothing in memory between requests, and answers with plain JSON (no SSE stream). Restarts don't disconnect clients. All state lives in the data directory. Running several replicas is possible only if they share the same `/data` volume, and profile writes are not yet locked across processes.

Set `VIBE_CHECK_AUTH_TOKEN` before exposing the port beyond your machine. Clients must then send `Authorization: Bearer <token>`; requests without it get `401`. Without a token the server starts but logs a warning.

Environment:

| Variable | Default | Description |
|----------|---------|-------------|
| `VIBE_CHECK_DATA_DIR` | `/data` | Profile storage (mount a volume) |
| `VIBE_CHECK_TRANSPORT` | `http` | `stdio` or `http` |
| `VIBE_CHECK_HOST` | `0.0.0.0` | HTTP bind address |
| `VIBE_CHECK_PORT` | `3100` | HTTP listen port |
| `VIBE_CHECK_AUTH_TOKEN` | — | Bearer token for HTTP. Strongly recommended for anything beyond localhost |

### Volume

```yaml
volumes:
  - ./data:/data
```

### Cursor (URL mode)

```json
{
  "mcpServers": {
    "vibe-check": {
      "url": "http://localhost:3100/mcp",
      "headers": {
        "Authorization": "Bearer ${VIBE_CHECK_AUTH_TOKEN}"
      }
    }
  }
}
```

Use `/mcp`. The legacy `/sse` endpoint was removed in favor of Streamable HTTP. Omit `headers` if you did not set a token.

### Claude Desktop + Docker

Claude Desktop config only accepts stdio. To use Docker HTTP, bridge with `mcp-remote`:

```json
{
  "mcpServers": {
    "vibe-check": {
      "command": "npx",
      "args": [
        "-y", "mcp-remote", "http://localhost:3100/mcp",
        "--header", "Authorization: Bearer <your-token>"
      ]
    }
  }
}
```

Prefer stdio instead — simpler and more reliable.
