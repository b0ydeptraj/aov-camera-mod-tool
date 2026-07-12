---
name: research
description: Use when a hub needs fresh evidence but should retain ownership of the lane. Stateless research utility for product, market, technical, or domain questions.
---

# Mission
Gather the minimum useful research needed for the next decision, then hand control back immediately.

## Default outputs
- evidence bullets appended to the active artifact
- assumption checks or citations for the current decision
- a short list of unresolved questions only when they block the next decision

## Typical tasks
- Answer the current decision question, not the whole topic.
- Summarize only the market, technical, or domain evidence that changes the next move.
- Mark which assumptions are confirmed, unconfirmed, or contradicted.
- Recommend the smallest next question only when uncertainty still blocks the lane.

## Working rules
- Write into `product-brief.md`, `PRD.md`, or the active artifact instead of creating a side quest.
- Separate evidence from recommendation.
- Name the source, provenance, and freshness whenever possible.
- Stop as soon as the owning hub can decide without another broad research pass.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- evidence bullets appended to the active artifact
- assumption checks or citations for the current decision
- a short list of unresolved questions only when they block the next decision

## Reference skills and rules
- Do not own the plan; feed findings back to the current hub.
- Prefer current evidence over generic opinions.
- Open `references/research-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/research-good-output.md` and `examples/research-bad-output.md` to calibrate output quality.
- Use `evals/research-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/research-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- brainstorm-hub
- plan-hub
- workflow-router
