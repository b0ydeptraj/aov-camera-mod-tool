---
name: delegation-control
description: Use when creating subagents or parallel agent lanes is being considered. Decide whether delegation is worth its quota cost, assign reasoning tiers, require bounded context packs, and close completed agents after evidence handoff.
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Mission
Control subagent cost and lifecycle without pretending every adapter exposes the same spawn, reasoning, usage, or close controls.

## Default outputs
- delegation plan and quota decision under .relay-kit/delegation
- append-only delegation lifecycle events under .relay-kit/state/delegation-ledger.jsonl
- adapter capability and enforcement status

## Typical tasks
- Record the reasoning tier decision and use medium default unless evidence justifies low or high.
- Reject unnecessary spawn requests and approve only bounded delegation with an artifact, quota and lock scope, return condition, and verification.
- Create and retain the context pack path for each approved subagent.
- Keep concurrent and high-reasoning subagents within policy limits.
- Record advisory versus enforced adapter capabilities and actual token usage only when reported.
- Close completed agents only with handoff evidence and close reason, then perform evidence-preserving close of temporary context packs.

## Working rules
- Enforce no unnecessary spawn: do not create subagents merely because a task is large.
- Do not lower reasoning solely because quota is nearly exhausted.
- Do not call an adapter control enforced unless runtime capability evidence exists.
- Do not delete lifecycle ledger or handoff evidence during cleanup.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- delegation plan and quota decision under .relay-kit/delegation
- append-only delegation lifecycle events under .relay-kit/state/delegation-ledger.jsonl
- adapter capability and enforcement status

## Reference skills and rules
- Medium reasoning is the normal default; low is allowed only for proven mechanical, low-risk work.
- Prefer no subagent when the main agent can complete the bounded task safely.
- Use token-economy to create a separate context pack for every approved subagent.
- Close completed agents only after handoff evidence is recorded; preserve ledger and raw evidence.
- Open `references/delegation-control-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/delegation-control-good-output.md` and `examples/delegation-control-bad-output.md` to calibrate output quality.
- Use `evals/delegation-control-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/delegation-control-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- team
- token-economy
- context-continuity
- review-hub
- qa-governor
