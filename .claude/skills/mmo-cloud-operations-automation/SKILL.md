---
name: mmo-cloud-operations-automation
description: Use when MMO automation runs in cloud infrastructure and needs worker pools, scheduler, queue, retry, idempotency, and cost-guarded operations.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Run MMO cloud automation at scale with resilient retries, safe concurrency, and controlled operational cost.

## Mandatory scope checks
- define scheduler, producer, worker pool, and queue boundaries
- define queue dashboard fields: waiting, active, delayed, failed, completed, stalled, throughput, failure rate, average duration
- define queue depth thresholds, dead-letter policy, and poison-message handling
- define retry policy, jitter, and max-attempt semantics
- define idempotency keys and dedupe strategy for side effects
- define cost ceiling and emergency scale-down controls

## Evidence contract
- include retry/backoff test evidence on throttling scenarios
- include idempotency key and duplicate-prevention evidence
- include worker health, queue health, alerts, and SLO signal mapping for operations

## Role
- mmo-cloud-automation

## Layer
- layer-4-specialists-and-standalones

## Inputs
- cloud runtime topology
- job and queue model
- SLA, cost, and security constraints

## Outputs
- cloud MMO operations architecture with worker pool, queue dashboard, idempotent jobs, backoff policies, and observability

## Reference skills and rules
- Use idempotent job contracts, idempotency keys, and dead-letter handling for failure isolation.
- Use exponential backoff with jitter for transient failures and throttling events.
- Include queue depth, cost ceiling, and quota safeguards before scaling concurrency.
- Expose operator controls for pause, resume, retry, drain, replay, dead-letter inspection, and safe scale-down.
- Open `references/mmo-cloud-operations-automation-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-cloud-operations-automation-good-output.md` and `examples/mmo-cloud-operations-automation-bad-output.md` to calibrate output quality.
- Use `evals/mmo-cloud-operations-automation-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-cloud-operations-automation-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- automation-ops
- release-readiness
- policy-guard
- qa-governor
