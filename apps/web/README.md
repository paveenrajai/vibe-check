# Web (planned)

Browser UI for managing your vibe-check profile and memories.

## Role

- Inspect and edit every profile section
- Review pending observations (accept / reject / edit)
- Browse audit history
- Export / import profile JSON

## Planned stack

- Vite + React (or Next.js if you need SSR later)
- Talks to `apps/api` only — never reads `data/` directly
- Types generated from `schemas/profile.v1.json`

## Pages (draft)

| Page | Purpose |
|------|---------|
| `/` | Profile overview |
| `/communication` | Answer style, tone, formatting |
| `/code` | Naming, CSS, scope preferences |
| `/context` | Current projects, goals |
| `/observations` | Review inferred memories |
| `/audit` | Full change log |

## When to add

Scaffold with `npm create vite@latest` (or your preferred stack) inside this directory. Add `apps/api` first so the UI has something to call.
