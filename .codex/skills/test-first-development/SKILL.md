---
name: test-first-development
description: Use when implementation should follow a red-green-refactor loop instead of ad-hoc coding. Test-first execution utility.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Drive implementation through the smallest useful red-green-refactor loop.

## Default outputs
- test-first execution notes and evidence appended to story, tech-spec, or qa-report

## Typical tasks
- Name the behavior that should fail first.
- Capture the failing test or reproduction evidence.
- Implement only enough to turn the signal green before cleanup.

## Working rules
- If the behavior cannot be tested first, say why instead of pretending the loop happened.
- Keep one behavior per cycle.
- Keep tests, fixtures, and sample payloads plain ASCII unless the behavior explicitly depends on non-ASCII content.
- Do not widen scope during the green phase.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- test-first execution notes and evidence appended to story, tech-spec, or qa-report

## Reference skills and rules
- Write the failing test first when the behavior is testable.
- Keep the change minimal until the new test is green.
- Open `references/test-first-development-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/test-first-development-good-output.md` and `examples/test-first-development-bad-output.md` to calibrate output quality.
- Use `evals/test-first-development-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/test-first-development-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- developer
- test-hub
- qa-governor
