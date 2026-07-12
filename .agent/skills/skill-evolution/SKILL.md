---
name: skill-evolution
description: Use when creating, upgrading, reviewing, or pruning a Relay-kit SKILL.md. Audit trigger descriptions, paths frontmatter, allowed tools, handoff contract, and scenario fixtures before changing skill behavior.
paths: ["**/SKILL.md", "relay_kit_v3/registry/skills.py", "docs/relay-kit-skill-*.md"]
context: fork
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
effort: high
---

# Mission
Evolve Relay-kit skills as versioned runtime capabilities with explicit trigger, frontmatter, handoff, and regression evidence.

## Boundary
- Use for changes to generated skills, skill registry entries, skill docs, or skill routing fixtures.
- Do not own broad product planning; return to plan-hub when the skill change implies a new product surface.
- Do not ship a skill change without a route or gauntlet proof unless the change is docs-only and clearly marked.

## Default outputs
- skill delta notes appended to tech-spec, qa-report, or the active artifact
- frontmatter and trigger audit for every changed skill
- scenario fixture or gauntlet evidence proving routing behavior

## Evidence contract
- Input must include the skill names or skill folders under review and the reason behavior should change.
- Output must classify each skill delta as add, update, merge, prune, or leave unchanged.
- Every changed trigger must name the scenario, prompt shape, expected skill, and evidence command.
- Every high-risk skill must name its allowed tool profile or explain why tool scoping is not supported by the adapter.

## Typical tasks
- Read the current SKILL.md, registry spec, and generated adapter copy before proposing edits.
- Check trigger specificity, duplicate trigger noise, likely next-step validity, inputs, outputs, and handoff ownership.
- Add or update path-scoped frontmatter when a skill only makes sense for certain files.
- Use forked context guidance for exploratory, review-heavy, or report-heavy skill work that should not pollute the main lane.
- Update semantic fixtures or focused tests so routing drift is caught before release.

## Working rules
- Keep skill names Relay-kit-owned and distinct from external projects even when a pattern was inspired elsewhere.
- Short frontmatter beats long body text for activation quality.
- A thin skill should be merged, aliased, or given a concrete evidence contract instead of staying vague.
- A skill that can invoke shell, file edits, or external tools needs an explicit permission or allowed-tools stance.
- Record source patterns as evidence, but write new Relay-kit instructions in Relay-kit terminology.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- skill delta notes appended to tech-spec, qa-report, or the active artifact
- frontmatter and trigger audit for every changed skill
- scenario fixture or gauntlet evidence proving routing behavior

## Reference skills and rules
- Treat SKILL.md as a progressively disclosed command surface, not generic documentation.
- Prefer path-scoped activation, forked context, and tight tool profiles for specialized or high-risk skills.
- Do not copy external skill names or prompts; translate proven patterns into Relay-kit-owned names and contracts.
- Open `references/skill-evolution-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/skill-evolution-good-output.md` and `examples/skill-evolution-bad-output.md` to calibrate output quality.
- Use `evals/skill-evolution-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/skill-evolution-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- skill-gauntlet
- workflow-router
- review-hub
