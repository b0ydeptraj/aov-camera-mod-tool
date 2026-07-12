# orchestration-changelog

Orchestration phase tightened coordination around the 4-layer model:

- added layer-1 orchestrators: `bootstrap`, `team`, `cook`
- added layer-2 workflow hubs: `brainstorm-hub`, `scout-hub`, `plan-hub`, `debug-hub`, `fix-hub`, `test-hub`, `review-hub`
- added an explicit `developer` specialist so execution has a first-class handoff target
- upgraded workflow-state to record orchestrator, hub, lane, and active specialist
- added `team-board.md` and `investigation-notes.md` so multi-lane and debugging work have stable artifacts
- established the orchestration bundle family for stable rollout
