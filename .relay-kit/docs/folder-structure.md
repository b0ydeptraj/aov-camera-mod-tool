# folder-structure

Recommended runtime layout:

- `.relay-kit/contracts/` -> stable artifact contracts shared across roles and hubs
- `.relay-kit/state/` -> workflow-state, team-board, lane-registry, handoff-log, runtime-locale policy, and other runtime breadcrumbs
- `.relay-kit/references/` -> living support references for architecture, APIs, persistence, testing, security, observability, and performance
- `.relay-kit/docs/` -> topology docs, migration notes, gating rules, and orchestration rules
- `.claude/skills/`, `.agent/skills/`, `.codex/skills/` -> adapter-specific runtime skill folders
- `.relay-kit-prompts/` -> preferred generic prompt output path
- `relay_kit.py` -> current Relay-kit v3 entrypoint that adds orchestration, routing, hubs, utility providers, contracts, and gating
