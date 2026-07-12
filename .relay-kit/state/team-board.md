# team-board

## Shared objective
No active shared objective recorded.

## Active orchestrator
- team

## Lanes
| Lane | Owner skill | Current hub | Current artifact | Lock scope | Status | depends_on | wave_id | resume_condition | Handoff status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| primary | unassigned | none | none | none | queued | none | wave-1 | active | none | empty lane |
| lane-2 | unassigned | none | none | none | parked | primary | wave-2 | explicitly routed by team | none | empty lane |
| lane-3 | unassigned | none | none | none | parked | primary | wave-2 | explicitly routed by team | none | empty lane |

## Shared artifacts that must stay authoritative
- `.relay-kit/state/workflow-state.md`
- `.relay-kit/state/lane-registry.md`
- `.relay-kit/state/handoff-log.md`
- `.relay-kit/contracts/project-context.md`
- `.relay-kit/contracts/PRD.md`
- `.relay-kit/contracts/architecture.md`

## Merge order
wave-1 before wave-2 by default; parallel lanes must record depends_on before merge.

## Merge prerequisites
Passing gates, no active lock conflicts, handoff evidence linked, and lane audit pass.

## Conflict risks
none recorded

## Decision log
no decisions recorded
