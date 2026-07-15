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
```

No server to run manually — Cursor and Claude Desktop spawn vibe-check over **stdio** when needed.

### Connect (stdio — recommended)

Full guide: **[`docs/connecting.md`](docs/connecting.md)**

| Client | Config file |
|--------|-------------|
| **Cursor** | `.cursor/mcp.json` (project or global MCP settings) |
| **Claude Desktop (macOS)** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Claude Desktop (Windows)** | `%APPDATA%\Claude\claude_desktop_config.json` |

**macOS example:**

```json
{
  "mcpServers": {
    "vibe-check": {
      "command": "uv",
      "args": ["--directory", "/Users/you/Projects/vibe-check", "run", "vibe-check"],
      "env": {
        "VIBE_CHECK_DATA_DIR": "/Users/you/Projects/vibe-check/data",
        "VIBE_CHECK_TRANSPORT": "stdio"
      }
    }
  }
}
```

**Windows example** (note escaped backslashes in JSON):

```json
{
  "mcpServers": {
    "vibe-check": {
      "command": "uv",
      "args": ["--directory", "C:\\Users\\you\\Projects\\vibe-check", "run", "vibe-check"],
      "env": {
        "VIBE_CHECK_DATA_DIR": "C:\\Users\\you\\Projects\\vibe-check\\data",
        "VIBE_CHECK_TRANSPORT": "stdio"
      }
    }
  }
}
```

Restart the client → confirm `vibe-check` is connected (Cursor: MCP settings; Claude: Connectors → Manage).

**Examples:** [`examples/`](examples/) — per-platform JSON templates.

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
├── Dockerfile              # optional HTTP mode
└── docker-compose.yml
```

## Development

```bash
uv sync
uv run pytest -v
uv run ruff check packages apps
```

See [`docs/testing.md`](docs/testing.md).

## Roadmap

MCP + local profile works today. Next: hardening, API, web UI. Full plan: [`docs/roadmap.md`](docs/roadmap.md).

## License

MIT — see [LICENSE](LICENSE).
