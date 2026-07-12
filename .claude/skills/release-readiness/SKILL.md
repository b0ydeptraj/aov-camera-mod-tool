---
name: release-readiness
description: Use when a lane needs a pre-deploy or post-deploy readiness verdict with explicit smoke signals and rollback guardrails.
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Mission
Convert release confidence into concrete pre and post deploy evidence instead of relying on optimistic completion claims.

## Default outputs
- release-readiness checklist notes appended to qa-report or workflow-state
- explicit go, hold, or rollback recommendation tied to machine-checkable signals

## Typical tasks
- Run a pre-deploy gate for build, tests, migration risk, and rollback plan status.
- Run a post-deploy smoke gate for health, error budget, and critical path behavior.
- Record which checks are observed, inferred, or still missing.
- Escalate hold or rollback when a critical signal fails.

## Working rules
- No go recommendation without machine-checkable evidence for critical signals.
- Keep pre and post deploy verdicts separate to avoid false confidence.
- If evidence is incomplete, return hold by default and list the exact missing signals.
- Document rollback trigger thresholds before calling a deploy safe.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- release-readiness checklist notes appended to qa-report or workflow-state
- explicit go, hold, or rollback recommendation tied to machine-checkable signals

## Reference skills and rules
- Use `relay-kit release readiness <project> --phase pre|post` for deterministic checklists and signal evaluation.
- Treat `ready-check` as review readiness, not automatic production readiness.
- Open `references/release-readiness-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/release-readiness-good-output.md` and `examples/release-readiness-bad-output.md` to calibrate output quality.
- Use `evals/release-readiness-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/release-readiness-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- test-hub
- review-hub
- qa-governor
- workflow-router
