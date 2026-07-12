---
name: sequential-thinking
description: Use when a hub needs structured thought without changing ownership. Stepwise reasoning utility for debugging, planning, or decomposition.
---

# Mission
Turn a messy question into a short sequence of evidence-backed steps.

## Boundary
- Use for ordering a known problem into steps, checkpoints, or observations.
- Do not use for ranking competing solution options; hand that to problem-solving.
- Do not become the decision owner; return the sequence to the active hub.

## Default outputs
- ordered reasoning steps added to investigation-notes or the active artifact

## Evidence contract
- Input must include the active question, current artifact, and at least one known constraint or evidence source.
- Output must be a numbered sequence with a reason for each step and the evidence or artifact it depends on.
- End with the next most informative observation or test, not a completion claim.

## Typical tasks
- Decompose the problem into checkpoints.
- Identify what must be known before acting.
- Recommend the next most informative test or observation.

## Working rules
- Keep the sequence short and testable.
- Tie each step to an artifact or evidence source.
- Do not claim completion for the lane.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- ordered reasoning steps added to investigation-notes or the active artifact

## Reference skills and rules
- Break work into explicit steps and checkpoints.
- Reasoning should support a decision, not become the decision owner.
- Open `references/sequential-thinking-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/sequential-thinking-good-output.md` and `examples/sequential-thinking-bad-output.md` to calibrate output quality.
- Use `evals/sequential-thinking-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/sequential-thinking-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- debug-hub
- plan-hub
- fix-hub
