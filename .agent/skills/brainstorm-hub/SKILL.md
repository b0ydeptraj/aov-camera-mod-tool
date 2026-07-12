---
name: brainstorm-hub
description: Use when the request is still an idea, an opportunity, or a loosely described improvement. Guide early ideation and rough problem framing before formal planning exists.
---

# Mission
Turn fuzzy idea energy into a bounded discovery lane that planning can actually use.

## Mandatory routing
1. Identify the decision the user is really trying to make.
2. Use `research` only for the freshest evidence that changes that decision.
3. Use `market-research` when ICP, pricing, competitor, or domain signal affects the direction.
4. Use `growth-marketing` when the next artifact is positioning, funnel, campaign, or launch messaging.
5. Use `vietnamese-product-localization` when the idea is for Vietnamese users or bilingual communication.
6. Route to `pm` only after the opportunity has enough shape for requirements.

## Evidence contract
- name the user segment, problem, success signal, and biggest unknown
- separate source-backed facts from assumptions and guesses
- include the smallest next artifact: product brief, market note, campaign note, or stop decision

## Failure modes
Hold instead of proceeding when the output becomes a giant feature wish list, generic marketing copy, or unsourced opportunity claims.

## Exit conditions
End with one of three outcomes: a brief ready for planning, a stop decision, or one exact question that blocks planning.

## Role
- ideation-hub

## Layer
- layer-2-workflow-hubs

## Inputs
- user idea or opportunity
- .relay-kit/state/workflow-state.md
- any existing brief or context

## Outputs
- .relay-kit/contracts/product-brief.md or a decision not to proceed

## Reference skills and rules
- Use analyst for structured discovery and pm only once the shape is coherent enough to plan.
- Prefer narrowing the problem over generating a giant feature wish list.
- Open `references/brainstorm-hub-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/brainstorm-hub-good-output.md` and `examples/brainstorm-hub-bad-output.md` to calibrate output quality.
- Use `evals/brainstorm-hub-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/brainstorm-hub-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- analyst
- research
- market-research
- growth-marketing
- vietnamese-product-localization
- pm
- plan-hub
- workflow-router
