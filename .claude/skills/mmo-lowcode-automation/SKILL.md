---
name: mmo-lowcode-automation
description: Use when MMO operations rely on no-code or low-code orchestration stacks and need execution history, modular flows, error handlers, and safe deployment controls.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Build MMO low-code automation that stays debuggable, recoverable, and cost-aware under load.

## Mandatory scope checks
- define trigger, schedule, manual execution, production execution, and dependency graph ownership
- define execution list columns: workflow, node, status, duration, retries, operator, environment
- define error handler and retry/backoff strategy per critical module
- define rate-limit controls and queue behavior
- define publish, rollback, and incident-response procedure
- define redaction rules for credentials, tokens, cookies, payload samples, and account identifiers

## Evidence contract
- include module-level success and failure traces
- include throttling, queue-pressure, and redacted execution evidence
- include publish-versus-draft workflow control proof

## Role
- mmo-lowcode-ops

## Layer
- layer-4-specialists-and-standalones

## Inputs
- workflow platform capabilities
- trigger and dependency graph
- operational SLA and rollback constraints

## Outputs
- low-code operations design with node graph, execution list, module contracts, retries, redaction, and observability hooks

## Reference skills and rules
- Treat visual workflow nodes as production logic: define contracts and failure semantics explicitly.
- Enforce per-scenario run limits and queue controls to prevent request storms.
- Mirror real automation tools: manual vs production execution, active/inactive state, node-level output, error workflow, redacted execution data, and execution search.
- Separate draft/test workflows from published production workflows.
- Open `references/mmo-lowcode-automation-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-lowcode-automation-good-output.md` and `examples/mmo-lowcode-automation-bad-output.md` to calibrate output quality.
- Use `evals/mmo-lowcode-automation-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-lowcode-automation-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- automation-ops
- release-readiness
- qa-governor
- review-hub
