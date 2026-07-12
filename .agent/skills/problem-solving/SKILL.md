---
name: problem-solving
description: Use when a hub needs hypotheses, trade-offs, or resolution paths grounded in current evidence. Option-generation and root-cause utility.
---

# Mission
Turn evidence into plausible options and ranked next moves.

## Boundary
- Use for hypotheses, trade-offs, and option ranking after evidence exists.
- Do not use for step ordering or checkpoint decomposition; hand that to sequential-thinking.
- Do not own implementation, release, or completion verdicts.

## Default outputs
- options, hypotheses, and trade-offs appended to the active artifact

## Evidence contract
- Input must include current evidence, constraints, and the decision that needs options.
- Output must separate option, supporting evidence, risk, cheapest validation, and recommended next owner.
- When evidence disagrees, output at least two competing models and explain which counts, order, invariants, or workflow cues each one satisfies.
- Mark uncertainty explicitly when evidence is weak or conflicting.

## Typical tasks
- Generate root-cause hypotheses.
- Compare implementation or mitigation options.
- Reconcile conflicting artifacts, counts, sequences, or human workflow cues.
- Call out the cheapest validating experiment.

## Working rules
- Ground every option in evidence already collected.
- Build a workflow-level explanation when a strict diff or first-pass extraction conflicts with real-world constraints.
- State uncertainty instead of bluffing.
- Recommend escalation if the issue is really a planning problem.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- options, hypotheses, and trade-offs appended to the active artifact

## Reference skills and rules
- Root cause beats guess-and-patch.
- Surface trade-offs before implementation starts.
- Open `references/problem-solving-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/problem-solving-good-output.md` and `examples/problem-solving-bad-output.md` to calibrate output quality.
- Use `evals/problem-solving-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/problem-solving-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- debug-hub
- plan-hub
- review-hub
