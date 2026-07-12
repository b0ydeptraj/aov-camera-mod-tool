---
name: api-integration
description: Use when building or changing API clients, webhooks, endpoints, or network-facing code. Document external service integration patterns, clients, auth, retries, and error handling.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Make network-facing behavior predictable so changes to API code do not become reliability surprises.

## Produce `.relay-kit/references/api-integration.md`
Cover:
- clients, transports, and endpoints
- authentication and secret handling
- request id or correlation id propagation
- retry, timeout budget, 429, and idempotency rules
- request and response patterns
- error mapping and recovery
- testing and mocking approach

## Working rules
- Name client wrappers, service classes, or endpoint modules directly.
- Include where auth is injected and how secrets are sourced.
- Require redacted sample payloads when evidence includes tokens, cookies, emails, phone numbers, or account identifiers.
- Explain how the code handles network failures, partial failures, and upstream rate limits.
- Note what should be mocked versus tested against a real service.

## Role
- integration-support

## Layer
- layer-4-specialists-and-standalones

## Inputs
- HTTP or RPC client code
- settings or secret config
- test or mock code

## Outputs
- .relay-kit/references/api-integration.md

## Reference skills and rules
- Prefer concrete service names, client classes, and endpoint groups over generic summaries.
- Make request id propagation, timeout budget, retries, 429 handling, idempotency, redacted logs, and error translation explicit.
- Open `references/api-integration-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/api-integration-good-output.md` and `examples/api-integration-bad-output.md` to calibrate output quality.
- Use `evals/api-integration-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/api-integration-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- architect
- developer
- qa-governor
- review-hub
