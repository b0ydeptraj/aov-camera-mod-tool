# parallelism-rules

Runtime phase hardens team parallelism so `team` behaves like a real meta-orchestrator instead of a loose wrapper.

## Lane discipline
- Never let two lanes edit the same artifact section without an explicit merge order.
- Shared artifacts win over chat memory; update the artifact before handing off.
- If a lane discovers architecture or scope drift, it must update workflow-state and notify team immediately.
- Use scout-hub before parallelizing into unfamiliar parts of the codebase.
- Every lane claim should appear in lane-registry before work starts.
- Every non-trivial handoff should appear in handoff-log before the receiver claims completion.

## Required state files
- `.relay-kit/state/workflow-state.md`
- `.relay-kit/state/team-board.md`
- `.relay-kit/state/lane-registry.md`
- `.relay-kit/state/handoff-log.md`

## Handoff minimum
- source skill
- target skill
- lane
- authoritative artifact
- evidence linked
- expected return condition
