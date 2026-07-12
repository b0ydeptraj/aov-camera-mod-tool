---
name: memory-search
description: Use when a hub needs past decisions, handoff breadcrumbs, or prior debug evidence from .relay-kit artifacts. Read-only state retrieval utility.
---

# Mission
Recover prior context quickly so the lane can reuse proven decisions and avoid repeating old mistakes.

## Default outputs
- matching evidence excerpts from .relay-kit/state or .relay-kit/contracts appended to the active artifact
- a short continuity note that links current work to prior decisions

## Typical tasks
- Search `.relay-kit/state` and `.relay-kit/contracts` for the exact decision, failure pattern, or handoff being referenced.
- Use intent-aware retrieval when the lane needs decision, handoff, debug, review, or migration evidence.
- Return file paths and line-level excerpts that the active hub can verify immediately.
- Call out conflicts between older decisions and the current request instead of smoothing them over.
- Extract only the evidence needed for the next decision and stop.

## Working rules
- Stay read-only; do not rewrite artifacts during retrieval.
- Mark stale hits explicitly instead of mixing stale and fresh evidence silently.
- Cite concrete paths and lines, not vague summaries.
- Separate observed facts from interpretation when prior context is noisy.
- If no evidence is found, say so explicitly and route to fresh investigation instead of guessing.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- matching evidence excerpts from .relay-kit/state or .relay-kit/contracts appended to the active artifact
- a short continuity note that links current work to prior decisions

## Reference skills and rules
- Prefer read-only retrieval from authoritative artifacts over replaying chat memory.
- Use `relay-kit query search <project> --query ...` for deterministic lookups.
- Use intent/path/freshness filters to return high-signal context in one pass instead of broad dumps.
- Open `references/memory-search-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/memory-search-good-output.md` and `examples/memory-search-bad-output.md` to calibrate output quality.
- Use `evals/memory-search-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/memory-search-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- debug-hub
- review-hub
- plan-hub
- workflow-router
