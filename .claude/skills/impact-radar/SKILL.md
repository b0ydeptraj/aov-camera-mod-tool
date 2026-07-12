---
name: impact-radar
description: Use when planning or review needs explicit blast-radius analysis before touching runtime, adapters, templates, or release-sensitive surfaces.
---

# Mission
Make change blast radius explicit before merge so gate selection is evidence-based instead of guess-based.

## Default outputs
- impact-area and changed-file breakdown appended to workflow-state or review notes
- risk level plus recommended verification gates for the current diff

## Typical tasks
- Classify changed files into runtime, adapter, scripts, templates, docs, and packaging impact areas.
- Return a compact risk level with the concrete reason it was assigned.
- Recommend the smallest gate set that still protects migration and runtime safety.
- Highlight high-impact areas that need additional manual review before merge.

## Working rules
- Use file-based evidence from git diff or working tree status; avoid speculative risk claims.
- Keep recommendations command-ready so the owning hub can execute immediately.
- Do not approve merges; provide impact evidence and required gates.
- Escalate to review-hub or qa-governor when impact spans runtime-core and adapter surfaces.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- impact-area and changed-file breakdown appended to workflow-state or review notes
- risk level plus recommended verification gates for the current diff

## Reference skills and rules
- Use `relay-kit impact radar <project>` for deterministic working-tree analysis.
- Use `--base` and `--head` when the lane needs commit-range impact evidence for review.
- Open `references/impact-radar-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/impact-radar-good-output.md` and `examples/impact-radar-bad-output.md` to calibrate output quality.
- Use `evals/impact-radar-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/impact-radar-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- plan-hub
- review-hub
- qa-governor
- workflow-router
