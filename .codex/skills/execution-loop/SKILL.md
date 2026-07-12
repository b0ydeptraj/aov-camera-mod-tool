---
name: execution-loop
description: Use when building or fixing code iteratively and require evidence before claiming completion. Self-correcting development loop for implementation work.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Execute implementation work in a tight loop without resorting to random fixes.

## The loop
1. Understand the story or tech-spec completely.
2. Make the smallest viable code change toward the goal.
3. Run the relevant checks or tests.
4. Analyze the result.
5. If it failed, debug root cause before changing anything else.
6. If it passed, collect evidence and hand off to QA.

## Non-negotiable rules
- No quick fixes without root-cause reasoning.
- No stacking multiple unrelated changes in one test cycle.
- Write or update a failing test whenever the change fixes a bug.
- Default to plain ASCII in code, comments, tests, fixtures, and sample data unless the repo or product explicitly requires non-ASCII content.
- Do not say done without fresh evidence from commands actually run.
- A code-change claim is invalid when there is zero file delta and zero verification output unless the task is explicitly a no-code decision update.

## Failure protocol
After three failed fix attempts, stop and question the story, architecture, or assumptions instead of thrashing.

## Role
- developer-support

## Layer
- layer-4-specialists-and-standalones

## Inputs
- story or tech-spec
- project-context
- relevant support skills

## Outputs
- working code plus test evidence

## Reference skills and rules
- testing-patterns
- If discipline utilities are installed, use `root-cause-debugging` before repeated fix attempts.
- If discipline utilities are installed, use `evidence-before-completion` before claiming success.
- State the slice objective and expected files before each cycle so context does not rot across long loops.
- Open `references/execution-loop-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/execution-loop-good-output.md` and `examples/execution-loop-bad-output.md` to calibrate output quality.
- Use `evals/execution-loop-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/execution-loop-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- test-hub
- qa-governor
