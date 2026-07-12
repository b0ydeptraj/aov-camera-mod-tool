---
name: project-architecture
description: Use when designing a change, reviewing architectural drift, or implementing code in an unfamiliar area. Analyze the current codebase shape and maintain a living architecture reference.
---

# Mission
Build and maintain an accurate map of the current architecture so downstream roles stop guessing.

## Produce `.relay-kit/references/project-architecture.md`
Cover:
- entry points and execution flow
- entrypoint-to-call graph notes for the changed path
- layer or package structure
- module responsibilities
- ownership and boundary table for the modules under review
- dependency direction and boundaries
- architecture drift and hotspots
- files to mirror when adding new work

## Working rules
- Prefer observed runtime or code flow over folder names alone.
- Name boundaries explicitly: controllers, services, repositories, adapters, domain logic, jobs, or scripts.
- Flag any mismatch between the intended architecture and what the code actually does.
- Add file paths whenever the reference names a pattern or module.
- Mark hotspot files where unrelated features repeatedly collide.

## Role
- architecture-support

## Layer
- layer-4-specialists-and-standalones

## Inputs
- repository tree
- .relay-kit/contracts/project-context.md
- .relay-kit/contracts/architecture.md when available

## Outputs
- .relay-kit/references/project-architecture.md

## Reference skills and rules
- Document what the codebase actually does today, not what the team intended six months ago.
- Include concrete file paths, entrypoint mapping, call graph notes, ownership, dependency direction, and a boundary table.
- Open `references/project-architecture-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/project-architecture-good-output.md` and `examples/project-architecture-bad-output.md` to calibrate output quality.
- Use `evals/project-architecture-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/project-architecture-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- architect
- developer
- review-hub
