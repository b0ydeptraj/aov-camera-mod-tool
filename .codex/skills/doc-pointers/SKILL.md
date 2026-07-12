---
name: doc-pointers
description: Use when a hub needs exact docs fragments, file paths, or source references before deciding. Stateless docs retrieval utility.
---

# Mission
Find the smallest set of authoritative documentation fragments needed to unblock the lane.

## Default outputs
- doc pointers, file paths, or citations appended to the active artifact
- a short conflict note when documentation and implementation disagree

## Typical tasks
- Check repo-local docs, comments, and nearby code first when the question is codebase-specific.
- Locate the smallest authoritative fragment that answers the current question.
- Return exact file paths, anchors, or section names whenever possible.
- Flag contradictions between docs and implementation instead of smoothing them over.

## Working rules
- Citations and file paths are more valuable than long summaries.
- Quote or summarize only the load-bearing fragment.
- Format the result so the owning hub can paste it straight into the active artifact.
- Stop once the next skill has enough exact evidence to act safely.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- doc pointers, file paths, or citations appended to the active artifact
- a short conflict note when documentation and implementation disagree

## Reference skills and rules
- Return exact doc pointers, not vague summaries.
- Prefer repo-local docs and code comments before broader sources when the task is codebase-specific.
- Open `references/doc-pointers-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/doc-pointers-good-output.md` and `examples/doc-pointers-bad-output.md` to calibrate output quality.
- Use `evals/doc-pointers-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/doc-pointers-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- scout-hub
- review-hub
- workflow-router
