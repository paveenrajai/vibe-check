# Self-hosting

## stdio (recommended)

For **Cursor** and **Claude Desktop** on macOS and Windows. See **[`connecting.md`](connecting.md)**.

---

## Docker + HTTP (optional)

For clients that support a remote MCP URL (e.g. Cursor URL mode). **Not supported natively by Claude Desktop.**

```bash
docker compose up -d --build
```

Server listens on `http://localhost:3100/sse` (legacy SSE transport).

Environment:

| Variable | Default | Description |
|----------|---------|-------------|
| `VIBE_CHECK_DATA_DIR` | `/data` | Profile storage (mount a volume) |
| `VIBE_CHECK_TRANSPORT` | `http` | `stdio` or `http` |
| `VIBE_CHECK_HOST` | `0.0.0.0` | HTTP bind address |
| `VIBE_CHECK_PORT` | `3100` | HTTP listen port |
| `VIBE_CHECK_AUTH_TOKEN` | — | Required for non-localhost HTTP (planned) |

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
      "url": "http://localhost:3100/sse"
    }
  }
}
```

Use `/sse`, not `/mcp` — vibe-check Docker currently exposes SSE, not Streamable HTTP.

### Claude Desktop + Docker

Claude Desktop config only accepts stdio. To use Docker HTTP, bridge with `mcp-remote`:

```json
{
  "mcpServers": {
    "vibe-check": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://localhost:3100/sse"]
    }
  }
}
```

Prefer stdio instead — simpler and more reliable.
