# orchestrator-rules

Layer-1 orchestrators own coordination, not implementation.

## bootstrap
Initialize state, detect missing contracts, and prepare the repo for a new line of work.

## team
Coordinate multiple lanes, avoid overlap, and keep shared artifacts authoritative.

## cook
Run the day-to-day loop for one request by selecting the right hub and checking completion gates.

## workflow-router
Act as the routing kernel that chooses the track, utility provider set, specialist, and escalation path.

## Parallel lane rules

- Never let two lanes edit the same artifact section without an explicit merge order.
- Shared artifacts win over chat memory; update the artifact before handing off.
- If a lane discovers architecture or scope drift, it must update workflow-state and notify team immediately.
- Use scout-hub before parallelizing into unfamiliar parts of the codebase.
- Every lane claim should appear in lane-registry before work starts.
- Every non-trivial handoff should appear in handoff-log before the receiver claims completion.
