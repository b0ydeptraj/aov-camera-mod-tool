# /relay-start

- command-id: `relay-start`
- adapter: `agent`
- route-target: `workflow-router`

- locale-profile: `en`
- enforce-output-language: `True`

## Intent

Start a request with explicit routing and lane mode.

## Expected Evidence

workflow-state updated with selected track, hub, and next skill.

## Routing Contract

- Entry command: `/relay-start`
- Delegate to: `workflow-router`
- Keep skills and hubs as authoritative workflow units.
