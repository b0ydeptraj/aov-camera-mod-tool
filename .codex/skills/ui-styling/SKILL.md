---
name: ui-styling
description: Use when building user interfaces, implementing design systems, creating responsive layouts, adding accessible components, customizing themes, or establishing consistent styling patterns across applications.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Convert UI requirements into component and styling decisions that are responsive, accessible, and visually intentional.

## Mandatory scope checks
- identify the component system, token source, and responsive breakpoints
- define corner, contrast, spacing, and type systems before composing screens
- design loading, empty, error, focus, disabled, and validation states when the UI is interactive
- avoid default library surfaces, equal-radius panels everywhere, and chart or icon defaults without a reason
- keep motion transform/opacity-first and respect reduced-motion needs

## Evidence contract
- include component/state coverage and screenshot or browser evidence when available
- include accessibility notes for keyboard, labels, focus, and contrast
- include exact files, components, or tokens changed during implementation

## Handoff rules
Route broader screen direction to `frontend-design`, screenshot critique to `aesthetic`, and release confidence to `accessibility-review` or `test-hub`.

## Role
- ui-styling

## Layer
- layer-4-specialists-and-standalones

## Inputs
- component or page requirements
- design tokens or component library
- accessibility constraints

## Outputs
- styled UI implementation or system guidance with responsive, state, and accessibility evidence

## Reference skills and rules
- Treat component libraries as raw material; do not ship their default look without product-specific structure.
- Use repo-native UI components, icon systems, and theme tokens when present.
- Keep source code, comments, fixture text, and placeholder copy plain ASCII unless product content requires otherwise.
- Open `references/ui-styling-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/ui-styling-good-output.md` and `examples/ui-styling-bad-output.md` to calibrate output quality.
- Use `evals/ui-styling-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/ui-styling-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- frontend-design
- aesthetic
- accessibility-review
- test-hub
- review-hub
