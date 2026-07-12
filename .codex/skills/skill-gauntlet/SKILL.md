---
name: skill-gauntlet
description: Use when runtime skill behavior may have drifted and you need a regression gate before trusting routing or completion claims.
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Mission
Protect routing quality by detecting skill drift early instead of waiting for behavior regressions in live lanes.

## Default outputs
- skill behavior regression findings appended to qa-report or workflow-state
- explicit pass or hold verdict for SKILL.md trigger and structure discipline

## Typical tasks
- Validate SKILL.md frontmatter, trigger descriptions, and required section structure across runtime surfaces.
- Report malformed or stale skill files with concrete paths and checks.
- Gate release or migration work when skill quality checks fail.
- Hand failures to fix-hub with exact remediation targets.

## Working rules
- Treat skill behavior regressions as release risk, not optional cleanup.
- Prefer deterministic checks over subjective style review.
- Fail fast when trigger wording or core sections drift from required structure.
- Keep the gauntlet report small and path-specific so fixes are easy to apply.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- skill behavior regression findings appended to qa-report or workflow-state
- explicit pass or hold verdict for SKILL.md trigger and structure discipline

## Reference skills and rules
- Use `relay-kit skill gauntlet <project> --strict` for machine-checkable gating.
- Run this before promoting large skill edits, bundle changes, or release branches.
- Open `references/skill-gauntlet-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/skill-gauntlet-good-output.md` and `examples/skill-gauntlet-bad-output.md` to calibrate output quality.
- Use `evals/skill-gauntlet-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/skill-gauntlet-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- review-hub
- qa-governor
- workflow-router
- fix-hub
