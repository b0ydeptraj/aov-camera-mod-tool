---
name: debug-hub
description: Use when work starts from a regression, flaky behavior, or an unexplained mismatch between expected and actual behavior. Triage failures, collect evidence, and decide whether the issue is a bug, a test problem, or a planning problem.
---

# Mission
Turn a symptom into evidence and a decision, not into random edits.

## Mandatory routing
1. Use `root-cause-debugging` before proposing fixes for regressions or flaky behavior.
2. Use `memory-search` when prior decisions or earlier failures may explain the mismatch.
3. Use `runtime-doctor` when generated surfaces, adapters, state, or live runtime drift might be involved.
4. Use `problem-solving` for competing hypotheses and `sequential-thinking` for ordered probes.
5. Route to `fix-hub` only when the cause and affected surface are bounded.

## Evidence contract
- reproduce the issue or mark reproduction as blocked with the missing condition
- write `investigation-notes.md` with evidence, likely cause, non-causes ruled out, and next probe
- include failing command, log, trace, screenshot, or state pointer where available
- state whether this is a code bug, test problem, runtime drift, or planning ambiguity

## Failure modes
Hold when the lane is guessing from symptoms, stacking fixes before one failing signal is understood, or hiding weak reproduction.

## Role
- debug-hub

## Layer
- layer-2-workflow-hubs

## Inputs
- failing behavior
- logs, traces, or test output
- workflow-state
- relevant references

## Outputs
- .relay-kit/contracts/investigation-notes.md
- .relay-kit/contracts/tech-spec.md when a fix path is clear

## Reference skills and rules
- When discipline utilities are installed, use `root-cause-debugging` before touching code.
- Use testing-patterns and problem-solving to turn evidence into a fix path.
- Root cause beats guess-and-patch.
- Escalate to plan-hub if the 'bug' is actually an unclear requirement or architectural mismatch.
- Open `references/debug-hub-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/debug-hub-good-output.md` and `examples/debug-hub-bad-output.md` to calibrate output quality.
- Use `evals/debug-hub-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/debug-hub-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- root-cause-debugging
- problem-solving
- sequential-thinking
- memory-search
- runtime-doctor
- fix-hub
- test-hub
- plan-hub
- workflow-router
