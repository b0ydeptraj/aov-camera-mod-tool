---
name: root-cause-debugging
description: Use when a hub needs a disciplined investigation before proposing fixes. Structured root-cause debugging utility.
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Mission
Force a root-cause-first debugging pass so the lane stops guessing and starts proving.

## Default outputs
- root-cause notes and disproven hypotheses appended to investigation-notes or the active artifact

## Typical tasks
- Read the failure carefully and restate the symptom.
- Trace the issue through the narrowest useful chain of evidence.
- Record likely cause, non-causes, and the smallest validating next move.

## Working rules
- Do not recommend fixes before the evidence is good enough to reject obvious alternatives.
- Prefer one hypothesis at a time.
- Escalate back to planning when the issue is really a requirements or architecture mismatch.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- root-cause notes and disproven hypotheses appended to investigation-notes or the active artifact

## Reference skills and rules
- No fixes before investigation.
- Prefer evidence at component boundaries over guessed explanations.
- Open `references/root-cause-debugging-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/root-cause-debugging-good-output.md` and `examples/root-cause-debugging-bad-output.md` to calibrate output quality.
- Use `evals/root-cause-debugging-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/root-cause-debugging-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- debug-hub
- fix-hub
- test-hub
