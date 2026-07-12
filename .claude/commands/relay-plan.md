# /relay-plan

- command-id: `relay-plan`
- adapter: `claude`
- route-target: `plan-hub`

- locale-profile: `en`
- enforce-output-language: `True`

## Intent

Build implementation-ready plan artifacts and slice sequence.

## Expected Evidence

updated plan artifacts with acceptance and delivery order.

## Routing Contract

- Entry command: `/relay-plan`
- Delegate to: `plan-hub`
- Keep skills and hubs as authoritative workflow units.
