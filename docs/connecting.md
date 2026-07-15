# Connecting vibe-check (stdio)

**Recommended for Cursor and Claude Desktop on macOS and Windows.** The host spawns `vibe-check` as a local process — no Docker, no URL, nothing to run manually in a terminal.

## 1. Install (once)

**macOS / Linux / Windows (PowerShell):**

```bash
cd /path/to/vibe-check   # macOS/Linux
cd C:\path\to\vibe-check # Windows
uv sync
```

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12+.

## 2. Config shape (all platforms)

Replace paths with your clone location. Use **absolute paths** only.

```json
{
  "mcpServers": {
    "vibe-check": {
      "command": "uv",
      "args": ["--directory", "<REPO>", "run", "vibe-check"],
      "env": {
        "VIBE_CHECK_DATA_DIR": "<REPO>/data",
        "VIBE_CHECK_TRANSPORT": "stdio"
      }
    }
  }
}
```

Profile data is written to `<REPO>/data/profile.json`. Both Cursor and Claude can point at the **same repo** and share one profile.

---

## Cursor

**Config file:** `.cursor/mcp.json` in your project, or **Cursor Settings → MCP** for a global config.

Examples: [`examples/mcp-cursor.mac.json`](../examples/mcp-cursor.mac.json), [`examples/mcp-cursor.windows.json`](../examples/mcp-cursor.windows.json)

1. Paste the config (correct paths for your OS)
2. Restart Cursor or reload MCP from settings
3. **Settings → MCP** → `vibe-check` should show connected

---

## Claude Desktop

### macOS

| | |
|---|---|
| **Config file** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Open from Terminal** | `open ~/Library/Application\ Support/Claude/claude_desktop_config.json` |
| **UI** | Menu bar **Claude → Settings… → Developer → Edit Config** |
| **Example** | [`examples/mcp-claude-desktop.mac.json`](../examples/mcp-claude-desktop.mac.json) |
| **Logs** | `~/Library/Logs/Claude/mcp*.log` |

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

1. Add under `mcpServers` (or create `{ "mcpServers": {} }` if the file is empty)
2. **Quit Claude completely** (Cmd+Q), then reopen
3. **Settings → Connectors → Manage** → confirm `vibe-check` and its tools

### Windows

| | |
|---|---|
| **Config file** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Typical path** | `C:\Users\you\AppData\Roaming\Claude\claude_desktop_config.json` |
| **Open from PowerShell** | `notepad $env:APPDATA\Claude\claude_desktop_config.json` |
| **UI** | **Claude → Settings → Developer → Edit Config** |
| **Example** | [`examples/mcp-claude-desktop.windows.json`](../examples/mcp-claude-desktop.windows.json) |
| **Logs** | `%APPDATA%\Claude\logs\mcp*.log` |

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

Use doubled backslashes (`\\`) in JSON paths on Windows.

1. Add under `mcpServers`
2. **Quit Claude completely** (File → Exit), then reopen
3. **Settings → Connectors → Manage** → confirm `vibe-check`

---

## Without `uv` in PATH

**macOS / Linux:**

```json
{
  "mcpServers": {
    "vibe-check": {
      "command": "/absolute/path/to/vibe-check/.venv/bin/python",
      "args": ["-m", "vibe_check_mcp"],
      "env": {
        "VIBE_CHECK_DATA_DIR": "/absolute/path/to/vibe-check/data",
        "VIBE_CHECK_TRANSPORT": "stdio"
      }
    }
  }
}
```

**Windows:**

```json
{
  "mcpServers": {
    "vibe-check": {
      "command": "C:\\Users\\you\\Projects\\vibe-check\\.venv\\Scripts\\python.exe",
      "args": ["-m", "vibe_check_mcp"],
      "env": {
        "VIBE_CHECK_DATA_DIR": "C:\\Users\\you\\Projects\\vibe-check\\data",
        "VIBE_CHECK_TRANSPORT": "stdio"
      }
    }
  }
}
```

---

## MCP CLI install (macOS / Windows)

From the repo root after `uv sync`:

```bash
uv run mcp install apps/mcp/src/vibe_check_mcp/__main__.py --name vibe-check \
  -v VIBE_CHECK_DATA_DIR=/absolute/path/to/vibe-check/data
```

On Windows PowerShell, use your path format for `VIBE_CHECK_DATA_DIR`. Restart Claude Desktop after install.

---

## Verify

- Ask the model to call `get_profile`
- Or run: `uv run pytest apps/mcp/tests/test_mcp_stdio.py -v`
- Inspect profile: open `data/profile.json`

---

## Optional: Docker + HTTP

Not needed for Cursor or Claude Desktop. Only for clients that connect via URL (e.g. Cursor URL mode). See [`self-hosting.md`](self-hosting.md).
