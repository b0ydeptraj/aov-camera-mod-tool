# parallel-execution

Use this overlay when `team` or `developer` is considering multiple lanes or subagent-style execution.

## Split only when all of these are true
- The work items are independent enough that one fix is unlikely to invalidate the others.
- Each lane can claim a narrow lock scope.
- Merge order is known before the split.
- Shared artifacts are updated before handoff, not after memory drifts.

## Lane rules
- One owner skill per lane.
- Record lock scope in `team-board.md` and `lane-registry.md`.
- Record handoffs in `handoff-log.md` whenever ownership changes.
- Park blocked lanes instead of letting them guess in parallel.

## Subagent mode
- Route through `delegation-control` before creating a subagent.
- Medium reasoning is the default; low requires a proven mechanical, low-risk task with known verification.
- Every approved subagent receives its own token-economy context pack and quota.
- Only use subagent-style execution when tasks are already sliced and independent.
- Use one subagent per bounded task, not one subagent for the whole feature.
- Return every result through the lane owner before calling the work complete.
- Close completed subagents after handoff evidence is recorded; preserve the ledger and raw evidence.
