# Architecture

## Overview

vibe-check is a **monorepo**. Shared profile logic lives in one package; each delivery surface (MCP, REST API, web UI) is a separate app that imports it.

```
                    ┌─────────────┐
                    │  apps/web   │  (planned) browser UI
                    └──────┬──────┘
                           │ HTTP
                    ┌──────▼──────┐
                    │  apps/api   │  (planned) REST API
                    └──────┬──────┘
                           │
┌─────────────┐     ┌──────▼──────────────────────────┐     ┌─────────────┐
│ MCP clients │────►│  apps/mcp                       │────►│  data/      │
│ Cursor etc. │ MCP │  FastMCP tools + resources      │     │  profile    │
└─────────────┘     └──────┬──────────────────────────┘     └─────────────┘
                           │
                    ┌──────▼──────┐
                    │ packages/   │
                    │    core     │  schema, store, query
                    └─────────────┘
                           ▲
                    ┌──────┴──────┐
                    │  schemas/   │  JSON Schema (shared contract)
                    └─────────────┘
```

## Packages

### `packages/core` (`vibe-check-core`)

Domain logic with **no transport dependencies**. Used by MCP, API, CLI, and tests.

```
packages/core/src/vibe_check_core/
├── config.py
└── profile/
    ├── schema.py     # Defaults + version constants
    ├── store.py      # Read/write profile, audit, observations
    └── query.py      # Section lookup, search
```

### `apps/mcp` (`vibe-check-mcp`)

Thin MCP adapter. Registers tools and resources; delegates to `vibe-check-core`.

```
apps/mcp/src/vibe_check_mcp/
├── __main__.py
├── server.py
├── tools/
└── resources/
```

### `apps/api` (planned)

REST API for the web UI. Will import `ProfileStore` from core — no duplicated business logic.

### `apps/web` (planned)

Frontend only. Calls `apps/api`; types derived from `schemas/profile.v1.json`.

## Data flow

1. Any app calls `ProfileStore(data_dir)`.
2. Store reads/writes `data/profile.json`; appends to `data/audit.jsonl`.
3. Observations go to `data/observations.jsonl` until accepted via API or future CLI.
4. MCP clients never touch the filesystem directly — they go through tools.

## Storage

| File | Purpose |
|------|---------|
| `data/profile.json` | Canonical profile document |
| `data/audit.jsonl` | Append-only change log |
| `data/observations.jsonl` | Pending inferred preferences |

## Transports

| App | Transport | Use case |
|-----|-----------|----------|
| `apps/mcp` | stdio | Cursor, Claude Desktop |
| `apps/mcp` | HTTP (SSE) | Docker self-host |
| `apps/api` | HTTP REST | Web UI, integrations |

## Why monorepo

- **One source of truth** for profile shape (`packages/core` + `schemas/`)
- **MCP stays small** — no UI routes mixed into the MCP process
- **Web UI is additive** — drop in `apps/web` + `apps/api` without rewriting the MCP server
- **Same data directory** in local single-user mode

## Security

- MCP stdio: no network exposure
- MCP HTTP / API: auth token (planned)
- `data/` never committed to git
