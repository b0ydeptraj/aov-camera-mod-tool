---
name: ux-structure
description: Use when a hub needs sharper information hierarchy, cleaner flows, stronger screen structure, less generic AI-looking UI, or concrete UX corrections tied to implementation reality. UX and layout utility for user-facing work.
---

# Mission
Sharpen hierarchy, flow, and design taste without stealing ownership from product or implementation lanes.

## Default outputs
- ux notes appended to product-brief, PRD, architecture, or qa-report
- recommended taste controls for design variance, motion intensity, and visual density
- state coverage notes for loading, empty, and error handling when the surface is real product UI

## Typical tasks
- Outline the user journey or interaction flow.
- Set design variance, motion intensity, and visual density for the current slice before recommending layout changes.
- Call out friction, edge cases, copy issues, and template-like structure.
- Require loading, empty, and error states when the surface is a real product flow.
- Replace generic three-card layouts, filler gradients, and flex-hack compositions with stronger structure.

## Working rules
- Tie UX comments to a specific screen or step.
- Balance UX gains with implementation cost.
- Keep notes focused on the current slice.
- Do not approve purple-blue gradient filler, three-equal-card SaaS layouts, or layout choices that feel obviously AI-generated.
- Prefer grid layout or deliberate asymmetry over flex hacks when hierarchy matters.
- Keep motion performance-safe: prefer transform and opacity, and respect reduced-motion needs.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- ux notes appended to product-brief, PRD, architecture, or qa-report
- recommended taste controls for design variance, motion intensity, and visual density
- state coverage notes for loading, empty, and error handling when the surface is real product UI

## Reference skills and rules
- Use this skill to block AI-slop layouts, not merely to polish them.
- Prefer reference-driven direction, explicit hierarchy, and deliberate grid structure over generic SaaS template patterns.
- Return notes to the owning hub rather than taking over the project.
- Open `references/ux-structure-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/ux-structure-good-output.md` and `examples/ux-structure-bad-output.md` to calibrate output quality.
- Use `evals/ux-structure-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/ux-structure-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- brainstorm-hub
- plan-hub
- review-hub
