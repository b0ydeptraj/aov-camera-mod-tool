---
name: testing-patterns
description: Use when adding tests, updating fixtures, validating regressions, or deciding what proof is enough. Capture how the project tests code, mocks dependencies, and gathers evidence.
---

# Mission
Turn the project test suite into a usable playbook for implementation and quality review.

## Produce `.relay-kit/references/testing-patterns.md`
Cover:
- frameworks and folder rules
- fixture and factory patterns
- mocking and dependency isolation
- fake versus mock choice and integration boundary rules
- async or integration testing rules
- commands for local evidence
- flake history, coverage gaps, and brittle areas

## Working rules
- Name the real commands contributors should run for fast confidence versus deeper verification.
- Show where fixtures, factories, and mocks live and when each should be preferred.
- Mark the integration boundary where a fake stops being enough and a real service or contract test is required.
- Call out unstable tests, heavy integration paths, and areas with weak coverage.
- Tie recommendations back to risk, not just test quantity.

## Role
- quality-support

## Layer
- layer-4-specialists-and-standalones

## Inputs
- test folders
- test config
- fixtures or factories
- CI or local test commands

## Outputs
- .relay-kit/references/testing-patterns.md

## Reference skills and rules
- Explain how to produce evidence locally, not only what frameworks exist.
- Map tests to risk areas and brittle zones where regressions cluster.
- Open `references/testing-patterns-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/testing-patterns-good-output.md` and `examples/testing-patterns-bad-output.md` to calibrate output quality.
- Use `evals/testing-patterns-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/testing-patterns-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- developer
- qa-governor
- debug-hub
- test-hub
- review-hub
