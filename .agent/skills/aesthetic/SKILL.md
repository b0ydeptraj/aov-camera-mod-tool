---
name: aesthetic
description: Use when UI quality matters and the first-pass output risks looking obviously AI-generated. Create aesthetically strong interfaces through reference-driven design, screenshot analysis, component sourcing, and iterative review.
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Mission
Prevent obviously AI-generated UI by forcing reference analysis, visual hierarchy critique, and a revision loop.

## Mandatory scope checks
- identify the first focal point and whether proof sits close enough to the main claim
- set design variance, motion intensity, and visual density before recommending changes
- compare the screen against real references or project-native patterns
- flag over-rounded panels, decorative gradient filler, safe hero blocks, equal-weight cards, and default icon or chart choices
- require loading, empty, and error states for real product surfaces

## Evidence contract
- include screenshot, reference, or rendered-state evidence for every visual verdict
- separate visible facts from taste judgments
- name one structural revision before minor polish when the UI still feels generic

## Handoff rules
Send implementation details to `frontend-design` or `ui-styling`; send static screenshot interpretation to `multimodal-evidence`.

## Role
- aesthetic-review

## Layer
- layer-4-specialists-and-standalones

## Inputs
- rendered UI, screenshot, or design direction
- reference examples
- product tone constraints

## Outputs
- aesthetic critique, revision direction, and evidence-backed visual quality verdict

## Reference skills and rules
- Reference-driven structure beats invented average structure.
- Beauty without hierarchy is decoration; critique structure first and polish second.
- Use multimodal-evidence for screenshot interpretation and browser-inspector for live browser facts.
- Open `references/aesthetic-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/aesthetic-good-output.md` and `examples/aesthetic-bad-output.md` to calibrate output quality.
- Use `evals/aesthetic-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/aesthetic-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- frontend-design
- ui-styling
- multimodal-evidence
- review-hub
