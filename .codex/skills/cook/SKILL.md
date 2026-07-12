---
name: cook
description: Use when one active request already has routing and state, and needs the next solid handoff. Drive that request forward with the right hub or specialist.
---

# Mission
Run the day-to-day loop for one request without letting it skip gates or get stuck in vague next steps.

## Mandatory loop
1. Read workflow-state and identify the lane's current objective.
2. Choose exactly one hub that should move the work forward now.
3. Name the artifact that hub must create, update, or validate.
4. After the hub finishes, update workflow-state with what changed and which hub or specialist comes next.
5. Stop as soon as the next handoff is explicit.

## Safety rules
- Never jump straight from vague intent to implementation.
- When evidence is weak, prefer scout-hub, debug-hub, or test-hub over optimistic implementation.
- When scope shifts, send the lane back through workflow-router.

## Role
- lane-conductor

## Layer
- layer-1-orchestrators

## Inputs
- .relay-kit/state/workflow-state.md
- current request or lane objective
- available artifacts

## Outputs
- updated workflow-state
- a named next hub or specialist
- refreshed artifacts produced by the chosen lane

## Reference skills and rules
- Cook does not replace hubs; it chooses and sequences them.
- Keep each pass small: one hub, one artifact decision, one clear next handoff.
- If completion is claimed, force test-hub or review-hub before accepting it.
- If the lane is pausing or switching owners, trigger context-continuity checkpoint before handoff.
- Open `references/cook-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/cook-good-output.md` and `examples/cook-bad-output.md` to calibrate output quality.
- Use `evals/cook-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/cook-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- brainstorm-hub
- scout-hub
- plan-hub
- debug-hub
- fix-hub
- test-hub
- review-hub
- context-continuity
