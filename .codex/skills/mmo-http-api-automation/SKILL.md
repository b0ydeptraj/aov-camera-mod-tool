---
name: mmo-http-api-automation
description: Use when MMO workloads are primarily HTTP/API-driven and need endpoint catalog, contract-safe request orchestration, quota handling, redacted logs, and replay-safe execution.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Execute MMO API automation with contract handling that a backend reviewer can replay and debug.

## Mandatory scope checks
- define endpoint groups by risk and side-effect level
- define authentication scope and token lifecycle
- define request ledger fields: request id, endpoint, method, status code, duration, retry count, origin, cost, idempotency key
- propagate request id or correlation id through logs
- define rate-limit parsing and retry-backoff behavior
- define idempotency key, dedupe, redacted logging, and replay-safety policy

## Evidence contract
- include redacted request/response samples for success and 429 throttled paths
- include idempotency key replay proof for write endpoints
- include contract drift checks against API schema or docs plus status-code filter evidence

## Role
- mmo-api-automation

## Layer
- layer-4-specialists-and-standalones

## Inputs
- endpoint catalog
- auth and scope model
- rate-limit and retry constraints

## Outputs
- HTTP/API operator design with endpoint catalog, request ledger, contract validation, idempotent retry logic, and audit-ready logs

## Reference skills and rules
- Define request contracts from official API documentation before implementation.
- Handle 429 and transient 5xx paths with bounded retries and reset-aware backoff.
- Use idempotency key, request id, redacted raw request/response evidence, and replay checks for write operations.
- Mirror real API dashboards: endpoint groups, status-code filters, origin filters, retry count, duration, cost, and replay-safe request detail.
- Open `references/mmo-http-api-automation-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-http-api-automation-good-output.md` and `examples/mmo-http-api-automation-bad-output.md` to calibrate output quality.
- Use `evals/mmo-http-api-automation-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-http-api-automation-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- api-integration
- automation-ops
- policy-guard
- qa-governor
