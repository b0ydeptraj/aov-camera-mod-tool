# /relay-test

- command-id: `relay-test`
- adapter: `codex`
- route-target: `test-hub`

- locale-profile: `en`
- enforce-output-language: `True`

## Intent

Run verification and route-quality checks for the active change.

## Expected Evidence

test and gate output mapped to acceptance criteria.

## Routing Contract

- Entry command: `/relay-test`
- Delegate to: `test-hub`
- Keep skills and hubs as authoritative workflow units.
