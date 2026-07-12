---
name: pm
description: Use when the work is past discovery and needs a buildable scope. Translate a product brief or scoped request into a prd, release slices, and acceptance criteria.
---

# Mission
Create a buildable plan, not a wish list.

## Produce `PRD.md`
Include:
- objective and scope
- functional requirements
- non-functional requirements
- out of scope
- acceptance criteria
- risks and mitigations
- release slices

## Produce `epics.md`
Organize the PRD into thin vertical slices with an order that reduces risk early.

## Readiness gate
The PRD is not ready if any of the following is missing:
- unambiguous acceptance criteria
- named risks for hard or irreversible changes
- explicit out-of-scope section
- at least one suggested slice order

## Role
- planning

## Layer
- layer-4-specialists-and-standalones

## Inputs
- .relay-kit/contracts/product-brief.md or direct scoped request
- .relay-kit/contracts/project-context.md

## Outputs
- .relay-kit/contracts/PRD.md
- .relay-kit/contracts/epics.md

## Reference skills and rules
- Do not hand wave acceptance criteria.
- Separate must-have requirements from stretch goals and out-of-scope ideas.
- Use UX and research support skills when the user experience is part of the risk.
- Open `references/pm-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/pm-good-output.md` and `examples/pm-bad-output.md` to calibrate output quality.
- Use `evals/pm-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/pm-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- architect
- scrum-master
- plan-hub
- review-hub
