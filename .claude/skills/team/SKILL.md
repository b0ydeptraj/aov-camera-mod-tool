---
name: team
description: Use when work must proceed in parallel, when planning and implementation overlap, or when one lane is blocked and another can move. Coordinate multi-lane or multi-session work without letting agents step on each other.
---

# Mission
Coordinate parallel work while preserving one authoritative source of truth for each artifact.

## Mandatory behavior
1. Maintain `.relay-kit/state/team-board.md` with lanes, owners, active artifacts, blockers, and merge order.
2. Split work only when lanes are independent enough to avoid editing the same artifact section at the same time.
3. Use `cook` to drive each active lane, but keep final merge and priority decisions here.
4. If one lane uncovers architecture or scope drift, update workflow-state and notify all affected lanes.
5. Park lanes that are blocked instead of letting them thrash.
6. Record lock scope and handoff status whenever a lane changes ownership or pauses.
7. For each lane, record `depends_on`, `wave_id`, and `resume_condition`, then only advance to the next wave after current-wave verification gates pass.
8. Run `relay-kit lane audit <project> --strict --json` before claiming multi-lane state is safe.
9. Route through `delegation-control` before creating subagents; medium reasoning is the default and low reasoning requires a proven mechanical task.

## Do not do this
- Do not let two lanes silently diverge on the same acceptance criteria.
- Do not keep lane state only in memory.
- Do not parallelize before a quick scout when the codebase area is unfamiliar.
- Do not close a lane as done when no artifact delta or verification evidence exists.

## Role
- meta-orchestrator

## Layer
- layer-1-orchestrators

## Inputs
- .relay-kit/state/workflow-state.md
- .relay-kit/state/team-board.md
- active artifacts and blockers

## Outputs
- .relay-kit/state/team-board.md
- .relay-kit/state/workflow-state.md

## Reference skills and rules
- Shared artifacts beat chat summaries; update the artifact before handing off.
- Assign one owner skill per lane and name merge order explicitly.
- Use cook inside a lane, not as a replacement for team.
- Use `.relay-kit/docs/parallel-execution.md` to decide when work is independent enough to split safely.
- Require context-continuity handoff packs when ownership shifts across sessions or AIs.
- Prefer wave-based execution: parallel inside a wave, strict dependency gate between waves.
- Run `relay-kit lane audit <project> --strict --json` before trusting a multi-lane handoff.
- Open `references/team-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/team-good-output.md` and `examples/team-bad-output.md` to calibrate output quality.
- Use `evals/team-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/team-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- delegation-control
- cook
- plan-hub
- scout-hub
- debug-hub
- review-hub
- context-continuity
