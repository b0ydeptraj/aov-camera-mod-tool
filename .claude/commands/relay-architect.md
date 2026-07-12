# /relay-architect

- command-id: `relay-architect`
- adapter: `claude`
- route-target: `architect`

- locale-profile: `en`
- enforce-output-language: `True`

## Intent

Resolve architecture-level decisions for the selected slice.

## Expected Evidence

architecture notes with boundaries, tradeoffs, and risk calls.

## Routing Contract

- Entry command: `/relay-architect`
- Delegate to: `architect`
- Keep skills and hubs as authoritative workflow units.
