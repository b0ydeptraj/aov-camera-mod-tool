---
name: test-hub
description: Use when implementation exists, after a risky refactor, or whenever confidence is lower than the change impact. Coordinate verification, evidence collection, and residual-risk review before work is called done.
---

# Mission
Turn raw test execution into a real readiness decision.

## Mandatory routing
1. Use `testing-patterns` to map risk to the right proof surface.
2. Use `evidence-before-completion` for claim-to-evidence checks before final verdicts.
3. Use `signal-calibration` when a claim says production-ready, field-tested, commercial-ready, or unusually strong.
4. Use `token-economy` when long logs or large context need compression without losing failure evidence.
5. Use `mmo-mobile-app-automation` for device/emulator matrix evidence when mobile MMO flows are under test.

## Evidence contract
- build the smallest useful matrix that covers acceptance criteria and regression surface
- preserve failing command details or raw log pointers
- write or refresh `qa-report.md` with pass, fail, blocked, and residual-risk sections
- route failures to `debug-hub` with exact reproduction evidence

## Failure modes
Hold when evidence is only a screenshot of success, when failed logs are summarized away, or when the test scope does not match risk.

## Role
- verification-hub

## Layer
- layer-2-workflow-hubs

## Inputs
- story or tech-spec
- implementation evidence
- testing-patterns reference
- workflow-state

## Outputs
- .relay-kit/contracts/qa-report.md
- updated workflow-state with pass, fail, or blocked verdict

## Reference skills and rules
- Use qa-governor for the actual readiness gate.
- Prefer evidence tied to acceptance criteria and regression surface.
- Route back to debug-hub when verification fails unexpectedly.
- When discipline utilities are installed, use `evidence-before-completion` before calling the lane ready.
- Open `references/test-hub-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/test-hub-good-output.md` and `examples/test-hub-bad-output.md` to calibrate output quality.
- Use `evals/test-hub-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/test-hub-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- testing-patterns
- evidence-before-completion
- signal-calibration
- token-economy
- mmo-mobile-app-automation
- qa-governor
- review-hub
- debug-hub
- workflow-router
