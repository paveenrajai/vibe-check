# Roadmap

## Phase 1 — MCP + local profile (current)

- [x] Monorepo with shared `packages/core`
- [x] MCP server (FastMCP + stdio)
- [x] Tools: `get_profile`, `update_profile`, `record_observation`, `search_profile`
- [x] MCP resources: `vibe-check://profile`
- [x] JSON file store (`profile.json`, `audit.jsonl`, `observations.jsonl`)
- [x] stdio setup for Cursor and Claude Desktop (macOS + Windows)
- [x] Integration tests (stdio + HTTP)
- [x] Docker for legacy SSE HTTP (optional)

## Phase 2 — Hardening

- [ ] JSON Schema validation on read/write
- [ ] Observation review workflow (accept / reject / merge)
- [ ] Richer audit metadata (client, session, actor)
- [ ] Field-level `update_profile` (patch, not full section replace)
- [ ] CLI to inspect and edit profile from terminal
- [ ] Streamable HTTP transport (`/mcp`) for ChatGPT and remote clients
- [ ] Auth for HTTP transport (`VIBE_CHECK_AUTH_TOKEN`)

## Phase 3 — Web UI

- [ ] `apps/api` — REST API over `packages/core`
- [ ] `apps/web` — profile editor, observation inbox, audit history
- [ ] Export / import profile JSON
- [ ] Types generated from `schemas/profile.v1.json`

## Phase 4 — Later

- [ ] Optional encryption at rest for `data/`
- [ ] Multi-machine sync (git-backed or WebDAV)
- [ ] Local-only inference suggestions for `record_observation`
- [ ] Per-field provenance inside profile document
