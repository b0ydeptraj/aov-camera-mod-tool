# /relay-brief

- command-id: `relay-brief`
- adapter: `codex`
- route-target: `brainstorm-hub`

- locale-profile: `en`
- enforce-output-language: `True`

## Intent

Turn a rough ask into a brief before planning depth increases.

## Expected Evidence

problem framing, initial constraints, and candidate direction.

## Routing Contract

- Entry command: `/relay-brief`
- Delegate to: `brainstorm-hub`
- Keep skills and hubs as authoritative workflow units.
