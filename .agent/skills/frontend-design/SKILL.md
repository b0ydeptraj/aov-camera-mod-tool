---
name: frontend-design
description: Use when the user asks to build web components, pages, or applications and visual quality matters. Create distinctive, production-grade frontend interfaces that avoid generic AI aesthetics.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Ship frontend work that feels designed for the product instead of assembled from generic AI patterns.

## Mandatory scope checks
- define purpose, audience, and primary task before choosing layout
- choose design variance, motion intensity, and visual density explicitly
- anchor layout in a real reference, existing screen, or trusted component source
- define loading, empty, error, and mobile states for real product surfaces
- reject oversized safe heroes, equal-card filler, default icons, and purple gradient padding when they do not serve hierarchy

## Evidence contract
- include reference or screenshot notes before claiming visual quality
- include before/after or rendered-state evidence when implementation changed
- include accessibility and performance risk notes for user-facing changes

## Handoff rules
Hand component-level styling to `ui-styling`, product UI architecture to `next-product-frontend`, and final visual critique to `aesthetic` or `review-hub`.

## Role
- frontend-design

## Layer
- layer-4-specialists-and-standalones

## Inputs
- frontend request
- product context
- existing design system or reference screenshots

## Outputs
- implemented or reviewed frontend surface with visual direction, state coverage, and screenshot evidence

## Reference skills and rules
- Anchor visual direction in real references, existing product patterns, or component sources before styling.
- Use aesthetic for critique, ui-styling for component system details, and accessibility-review for merge gates.
- Prefer deliberate hierarchy, density, and state coverage over generic card-heavy layouts.
- Open `references/frontend-design-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/frontend-design-good-output.md` and `examples/frontend-design-bad-output.md` to calibrate output quality.
- Use `evals/frontend-design-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/frontend-design-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- next-product-frontend
- ui-styling
- aesthetic
- accessibility-review
- review-hub
