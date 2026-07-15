# vibe-check

A local, self-hostable [MCP](https://modelcontextprotocol.io) server that builds a **transparent profile** of how you work with AI — so every LLM client (Cursor, Claude, ChatGPT, Perplexity, etc.) can know your preferences without you repeating yourself.

Built with the [official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and [FastMCP](https://modelcontextprotocol.io/docs/develop/build-server).

## The problem

Every new chat starts from zero. You re-explain that you prefer concise answers, hate `px` in CSS, want warm but direct tone, care about naming conventions, or that you're currently building a Django API. Preferences scatter across Cursor rules, system prompts, and memory features you can't inspect or port.

**vibe-check** is one profile, owned by you, readable by any MCP-compatible client — with a planned web UI to manage it all.

## What goes in a profile

| Area | Examples |
|------|----------|
| **Communication** | Concise vs thorough, tone, markdown preferences |
| **Code & design** | Naming style, CSS units, framework choices |
| **Personality** | How you like to be addressed, humor |
| **Interests** | Topics you care about |
| **Context** | Current projects, stack, goals |
| **Tooling** | Editors, commit style, test philosophy |

Nothing is hidden. You can read, edit, export, or delete any field.

## Architecture

```
apps/web  ──►  apps/api  ──┐
                           ├──►  packages/core  ──►  data/
apps/mcp (MCP clients)  ───┘
```

- **`packages/core`** — shared profile logic (schema, store, query)
- **`apps/mcp`** — MCP server for LLM clients (today)
- **`apps/api`** — REST API for the web UI (planned)
- **`apps/web`** — browser UI to manage profile & memories (planned)
- **`schemas/`** — JSON Schema contract shared across Python and frontend

See [`docs/architecture.md`](docs/architecture.md).

## Quick start

```bash
git clone https://github.com/paveenrajai/vibe-check.git
cd vibe-check
uv sync
uv run vibe-check          # MCP server (stdio)
```

### Docker

```bash
docker compose up --build
```

### Cursor MCP config

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

See [`examples/mcp-cursor.json`](examples/mcp-cursor.json) and [`docs/self-hosting.md`](docs/self-hosting.md).

## Project layout

```
vibe-check/
├── packages/core/          # vibe-check-core — shared domain logic
├── apps/
│   ├── mcp/                # MCP server (shipping)
│   ├── api/                # REST API (planned)
│   └── web/                # Frontend (planned)
├── schemas/                # JSON Schema contracts
├── data/                   # Local profile storage (gitignored)
├── docs/
├── docker/
├── Dockerfile
└── docker-compose.yml
```

## Development

```bash
uv sync
uv run pytest
uv run ruff check packages apps
```

## Roadmap

- [x] Monorepo with shared `packages/core`
- [x] MCP server (FastMCP + stdio)
- [x] JSON file store
- [x] Docker for MCP HTTP
- [ ] `apps/api` — REST endpoints for profile management
- [ ] `apps/web` — UI for profile, observations, audit log
- [ ] Auth for HTTP / API

## License

MIT — see [LICENSE](LICENSE).
