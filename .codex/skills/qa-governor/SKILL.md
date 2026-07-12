---
name: qa-governor
description: Use when work needs a readiness verdict or implementation confidence is low. Check readiness against acceptance criteria, risk, and regression scope, then write a QA report.
---

# Mission
Produce a readiness verdict and surface residual risk clearly.

## Boundary
- Use qa-governor for readiness verdict, shipability, acceptance coverage, risk, and regression scope.
- This is not a one-claim proof pass; use evidence-before-completion for claim-to-evidence checks.
- End with a go or no-go recommendation grounded in evidence.

## Produce `qa-report.md`
Include:
- scope checked
- acceptance coverage
- risk matrix
- regression surface
- evidence collected
- go or no-go recommendation

## Mandatory checks
- Compare actual evidence to acceptance criteria, not just implementation intent.
- Name the regression surface explicitly.
- Call out missing tests, weak evidence, or unverified assumptions.
- Bounce work back when story, tech-spec, or architecture is still underspecified.
- Treat completion claims as invalid until the claim-to-evidence pass has fresh verification evidence.

## Role
- quality

## Layer
- layer-4-specialists-and-standalones

## Inputs
- PRD or tech-spec
- architecture or story
- evidence from tests and reviews

## Outputs
- .relay-kit/contracts/qa-report.md

## Reference skills and rules
- Use testing-patterns as the evidence map for the project.
- Use `evidence-before-completion` only for the narrow claim-to-evidence pass before this readiness gate.
- Use `.relay-kit/docs/review-loop.md` when review feedback must be validated before action.
- Coverage must be explained against acceptance criteria and risk, not just number of tests.
- Use context-continuity when readiness evidence must survive a new thread or handoff before final sign-off.
- Open `references/qa-governor-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/qa-governor-good-output.md` and `examples/qa-governor-bad-output.md` to calibrate output quality.
- Use `evals/qa-governor-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/qa-governor-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- signal-calibration
- evidence-before-completion
- runtime-doctor
- review-hub
- debug-hub
- context-continuity
- workflow-router
