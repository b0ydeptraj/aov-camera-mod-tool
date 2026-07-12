# /relay-token-audit

- command-id: `relay-token-audit`
- adapter: `agent`
- route-target: `token-economy`

- locale-profile: `en`
- enforce-output-language: `True`

## Intent

Audit token budget, compression safety, and signal retention before execution.

## Expected Evidence

token audit report with budget violations, raw pointers, and retention metrics.

## Routing Contract

- Entry command: `/relay-token-audit`
- Delegate to: `token-economy`
- Keep skills and hubs as authoritative workflow units.
