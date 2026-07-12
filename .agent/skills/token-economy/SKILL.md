---
name: token-economy
description: Use when context is large and the lane needs deterministic token budgeting, context packing, and signal retention checks before execution.
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Mission
Reduce context cost without reducing execution signal quality.

## Default outputs
- token budget, task-scoped context pack, or token audit report artifacts under .relay-kit/context or .relay-kit/token
- explicit raw-required blocks and raw pointers for failing evidence
- budget violation findings with keep/drop decisions and retention metrics

## Typical tasks
- Estimate raw and packed token size with deterministic `ceil(len(text)/4)` accounting.
- Classify context blocks as raw-required, compressible, or summary-only.
- Build a task-scoped context pack with authority and freshness ranking plus max-tokens enforcement.
- Preserve raw pointers for failure-heavy evidence such as error, traceback, assertion, or exit-code blocks.
- Report budget violations and retention metrics before handing context to implementation lanes.

## Working rules
- Do not drop critical failure evidence.
- Signal retention must remain 1.0 in strict mode.
- If uncertain, keep the block raw-required and mark why.
- Record both selected and dropped context sources so downstream lanes can rehydrate if needed.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- token budget, task-scoped context pack, or token audit report artifacts under .relay-kit/context or .relay-kit/token
- explicit raw-required blocks and raw pointers for failing evidence
- budget violation findings with keep/drop decisions and retention metrics

## Reference skills and rules
- Use `relay-kit context budget`, `relay-kit context pack`, and `relay-kit token audit` as canonical entrypoints.
- Never hide failing command details without a raw path pointer.
- Fail open to raw-required when signal retention is uncertain.
- Open `references/token-economy-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/token-economy-good-output.md` and `examples/token-economy-bad-output.md` to calibrate output quality.
- Use `evals/token-economy-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/token-economy-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- workflow-router
- context-continuity
- handoff-context
- review-hub
- qa-governor
