---
name: media-tooling
description: Use when screenshots, assets, or content files need transformation or evidence extraction for the current lane. Media handling utility.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Handle media-specific steps that support the current lane without creating a parallel project.

## Default outputs
- media processing notes or asset instructions appended to the active artifact

## Typical tasks
- Prepare screenshots or assets for evidence.
- Describe required transforms or formats.
- Hand back what the next skill needs to continue.

## Working rules
- Keep transformations reversible when possible.
- Name exact asset sources and outputs.
- Route any broader UX or product decisions back to the owning hub.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- media processing notes or asset instructions appended to the active artifact

## Reference skills and rules
- Useful for evidence packaging and asset-heavy workflows.
- Should stay stateless and task-scoped.
- Open `references/media-tooling-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/media-tooling-good-output.md` and `examples/media-tooling-bad-output.md` to calibrate output quality.
- Use `evals/media-tooling-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/media-tooling-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- test-hub
- review-hub
- ux-structure
