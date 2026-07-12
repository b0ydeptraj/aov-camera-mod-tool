# /relay-research

- command-id: `relay-research`
- adapter: `codex`
- route-target: `research`

- locale-profile: `en`
- enforce-output-language: `True`

## Intent

Collect focused evidence for product or technical uncertainty.

## Expected Evidence

ranked source findings and decision-impact summary.

## Routing Contract

- Entry command: `/relay-research`
- Delegate to: `research`
- Keep skills and hubs as authoritative workflow units.
