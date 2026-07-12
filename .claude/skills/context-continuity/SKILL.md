---
name: context-continuity
description: Use when work needs reliable continuity across long chats, new threads, AI switches, or resume-after-gap sessions.
---

# Mission
Preserve lane continuity with explicit artifacts so the next session can continue safely without replaying full chat history.

## Default outputs
- checkpoint, rehydrate, handoff, or diff artifacts under .relay-kit/state and .relay-kit/handoffs
- a compact resume brief with explicit next step and open loops

## Typical tasks
- Run checkpoint before likely truncation, compaction, or session break.
- Run rehydrate at the start of a new thread to restore objective, lane, blockers, and next step.
- Run handoff when ownership moves across AI, thread, or operator.
- Run diff-since-last to detect drift from the most recent checkpoint snapshot.

## Working rules
- Separate observed evidence from inferred context in all continuity outputs.
- Do not call continuity complete if next step, blockers, and evidence pointers are missing.
- Treat continuity artifacts as append-first records; avoid destructive rewrites.
- If continuity conflicts with current repo reality, escalate through workflow-router before coding.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- checkpoint, rehydrate, handoff, or diff artifacts under .relay-kit/state and .relay-kit/handoffs
- a compact resume brief with explicit next step and open loops

## Reference skills and rules
- Use `relay-kit continuity` modes for deterministic continuity artifacts.
- Context continuity complements `handoff-context`; it does not replace authoritative contracts and state.
- Open `references/context-continuity-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/context-continuity-good-output.md` and `examples/context-continuity-bad-output.md` to calibrate output quality.
- Use `evals/context-continuity-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/context-continuity-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- workflow-router
- cook
- team
- handoff-context
- review-hub
