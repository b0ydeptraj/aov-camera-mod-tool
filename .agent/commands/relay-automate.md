# /relay-automate

- command-id: `relay-automate`
- adapter: `agent`
- route-target: `automation-ops`

- locale-profile: `en`
- enforce-output-language: `True`

## Intent

Design safe workflow automation and operations runbooks.

## Expected Evidence

dry-run, rollback, and owner-aware automation plan.

## Routing Contract

- Entry command: `/relay-automate`
- Delegate to: `automation-ops`
- Keep skills and hubs as authoritative workflow units.
