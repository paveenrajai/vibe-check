# Profile schema

Human-readable JSON document stored at `data/profile.json`. Versioned with `$schema` and `version` fields.

Machine-readable JSON Schema: [`schemas/profile.v1.json`](../schemas/profile.v1.json).

## Top-level shape (draft)

```json
{
  "$schema": "vibe-check/profile/v1",
  "version": 1,
  "updated_at": "2026-07-15T12:00:00Z",
  "communication": {
    "verbosity": "concise",
    "tone": ["warm", "direct"],
    "formatting": {
      "prefer_markdown": true,
      "avoid_bold_overuse": true
    },
    "notes": "Complete sentences; no engagement bait at end of replies."
  },
  "code": {
    "naming": "descriptive, match surrounding conventions",
    "css_units": "rem/em only, never px",
    "scope": "minimal diffs; avoid over-engineering",
    "comments": "only non-obvious logic"
  },
  "design": {
    "aesthetic": "clean, accessible",
    "colors": {},
    "typography": {}
  },
  "personality": {
    "traits": ["curious", "pragmatic"],
    "addressing": "first name ok"
  },
  "interests": [
    "developer tools",
    "AI observability"
  ],
  "context": {
    "current_projects": [
      {
        "name": "vibe-check",
        "stack": ["TypeScript", "MCP", "Docker"],
        "status": "greenfield"
      }
    ],
    "goals": [],
    "blockers": []
  },
  "tooling": {
    "editor": "Cursor",
    "commit_style": "conventional, why over what"
  },
  "custom": {}
}
```

## Sections

| Key | MCP resource path | Description |
|-----|-------------------|-------------|
| `communication` | `vibe-check://profile/communication` | How answers should be written |
| `code` | `vibe-check://profile/code` | Engineering preferences |
| `design` | `vibe-check://profile/design` | Visual and UX taste |
| `personality` | `vibe-check://profile/personality` | Tone and interpersonal style |
| `interests` | `vibe-check://profile/interests` | General topics |
| `context` | `vibe-check://profile/context` | Active work and goals |
| `tooling` | `vibe-check://profile/tooling` | Editors, workflows |
| `custom` | `vibe-check://profile/custom` | Free-form extensions |

## Observations (audit)

Inferred updates use `record_observation` before merging into the profile:

```json
{
  "id": "obs_…",
  "section": "code.css_units",
  "value": "never px",
  "source": "cursor session 2026-07-15",
  "confidence": 0.9,
  "status": "pending | accepted | rejected",
  "created_at": "…"
}
```

Users review pending observations with MCP tools:

| Tool | Purpose |
|------|---------|
| `list_observations` | List pending (or filter by status) |
| `accept_observation` | Merge into profile at dot-path `section` |
| `reject_observation` | Discard without profile changes |

Profile documents are validated against [`schemas/profile.v1.json`](../schemas/profile.v1.json) on every read and write.
