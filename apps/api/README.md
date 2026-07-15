# API (planned)

REST API for the vibe-check web UI and third-party integrations.

## Role

- Serves `apps/web` with profile CRUD, observation review, and audit history
- Reuses `packages/core` — same `ProfileStore` as the MCP server
- Auth, rate limiting, and multi-user support live here (not in MCP)

## Planned stack

- FastAPI
- Shares `data/` with MCP in single-user local mode
- OpenAPI spec generated from the same types as `schemas/profile.v1.json`

## Endpoints (draft)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/profile` | Full profile |
| PATCH | `/api/profile/{section}` | Update section |
| GET | `/api/observations` | Pending inferred preferences |
| POST | `/api/observations/{id}/accept` | Merge into profile |
| POST | `/api/observations/{id}/reject` | Discard |
| GET | `/api/audit` | Change history |

## When to add

Add this app when you start `apps/web`. The MCP server stays thin — it does not need to know about HTTP routes for humans.
