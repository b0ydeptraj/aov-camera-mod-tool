---
name: analyst
description: Use when discovery is needed before writing a prd or choosing architecture. Clarify product intent, assumptions, users, and open questions; produce a product brief for work that is not already fully scoped.
---

# Mission
Turn an idea, problem report, or vague request into a brief that downstream roles can reason from.

## Produce `product-brief.md`
Cover these sections:
- problem statement
- target users and jobs-to-be-done
- desired outcomes and success signals
- assumptions and unknowns
- constraints and non-goals
- open questions

## Guardrails
- Prefer validated facts over storytelling.
- Call out what is unknown instead of silently guessing.
- If the request is already well-scoped and quick-flow fits, do not force a brief.
- If a fresh brief already exists, update only the parts affected by the new request.

## Role
- analysis

## Layer
- layer-4-specialists-and-standalones

## Inputs
- user request
- .relay-kit/contracts/project-context.md
- .relay-kit/state/workflow-state.md

## Outputs
- .relay-kit/contracts/product-brief.md

## Reference skills and rules
- Lean on research-expert, problem-solving, and sequential-thinking when the scope is fuzzy.
- Keep the brief short enough that downstream roles can actually use it.
- Open `references/analyst-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/analyst-good-output.md` and `examples/analyst-bad-output.md` to calibrate output quality.
- Use `evals/analyst-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/analyst-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- pm
- plan-hub
- workflow-router
