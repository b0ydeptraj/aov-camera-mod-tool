# /relay-ship

- command-id: `relay-ship`
- adapter: `claude`
- route-target: `release-readiness`

- locale-profile: `en`
- enforce-output-language: `True`

## Intent

Prepare release-readiness and deployment safety checks.

## Expected Evidence

release readiness checklist with smoke and rollback status.

## Routing Contract

- Entry command: `/relay-ship`
- Delegate to: `release-readiness`
- Keep skills and hubs as authoritative workflow units.
