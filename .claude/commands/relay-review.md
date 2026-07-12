# /relay-review

- command-id: `relay-review`
- adapter: `claude`
- route-target: `review-hub`

- locale-profile: `en`
- enforce-output-language: `True`

## Intent

Run coherence and readiness review before completion claims.

## Expected Evidence

review findings or explicit pass with residual risks.

## Routing Contract

- Entry command: `/relay-review`
- Delegate to: `review-hub`
- Keep skills and hubs as authoritative workflow units.
