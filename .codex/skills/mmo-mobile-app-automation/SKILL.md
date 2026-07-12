---
name: mmo-mobile-app-automation
description: Use when MMO mobile workflows need device inventory, emulator or device automation, stable selectors, app-state control, and repeatable run evidence.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Deliver stable mobile MMO automation for repetitive app workflows with measurable reliability.

## Mandatory scope checks
- define emulator or device matrix, provider, hub, and startup method
- define device inventory fields: device id, OS, app version, provider, health, lease owner, battery, network, last run
- define app-state preconditions for each critical user journey
- define selector strategy and wait/retry policy
- define failure triage for crash, ANR, and timeout signals

## Evidence contract
- include one full green run on target matrix
- include one failure-path reproduction with root-cause notes
- include run artifacts: logcat, screenshots, video or trace pointers, crash/ANR markers

## Handoff rules
Route scheduler and queue concerns to `automation-ops`, proof design to `testing-patterns`, readiness verdicts to `qa-governor`, and visual/video evidence to `multimodal-evidence`.

## Failure modes
Hold when the design has no device lease model, no app-state reset, no selector drift handling, no raw logcat/crash evidence, or a fake dashboard that hides operator retry controls.

## Role
- mmo-mobile-automation

## Layer
- layer-4-specialists-and-standalones

## Inputs
- mobile workflow journeys
- device or emulator matrix
- toolchain constraints and policy rules

## Outputs
- mobile automation operations plan with device farm inventory, session lease, environment matrix, reliability controls, and evidence artifacts

## Reference skills and rules
- Prefer supported frameworks and official automation drivers for device control.
- Define deterministic app-state setup and teardown to reduce flake.
- Model the device farm like a real ops tool: hub/provider split, device status, lease owner, app version, logcat/crash/ANR evidence, and remote-control link.
- Do not design rooted, tampered, or policy-evasion mobile automation paths.
- Open `references/mmo-mobile-app-automation-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-mobile-app-automation-good-output.md` and `examples/mmo-mobile-app-automation-bad-output.md` to calibrate output quality.
- Use `evals/mmo-mobile-app-automation-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-mobile-app-automation-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- automation-ops
- testing-patterns
- qa-governor
- review-hub
