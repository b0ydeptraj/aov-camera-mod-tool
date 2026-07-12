# /relay-support

- command-id: `relay-support`
- adapter: `agent`
- route-target: `qa-governor`

- locale-profile: `en`
- enforce-output-language: `True`

## Intent

Prepare support-ready triage and completion confidence signals.

## Expected Evidence

qa/support posture with blocker severity and next actions.

## Routing Contract

- Entry command: `/relay-support`
- Delegate to: `qa-governor`
- Keep skills and hubs as authoritative workflow units.
