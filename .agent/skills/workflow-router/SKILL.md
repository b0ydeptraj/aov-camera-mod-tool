---
name: workflow-router
description: Use when a request arrives, the user asks what to do next, or scope or complexity is unclear. Route a request through the right delivery track, choose the active orchestrator or hub, keep workflow-state current, and turn short or ambiguous prompts into file-aware working guidance.
---

# Mission
Act as the routing kernel for the whole system: choose the track, choose the active lane, and make the next move explicit.

## Prompt enhancement posture
When the user gives a short, vague, or compressed request, do not pretend the skill makes the model an expert. Treat the skill as a context-aware prompt enhancer:
- infer the likely work type from the request shape
- name the recommended skill and why
- name the files, state, logs, or artifacts to read first
- name the evidence required before coding, answering, or claiming done
- choose whether to act, scout first, or ask exactly one high-value clarification
If `.relay-kit/context/index.json` exists, treat graph hits as candidate files to inspect first. If it is missing, continue with normal repo reading; do not block the user just because the index has not been built.

## Mandatory routing procedure
1. Read `.relay-kit/contracts/project-context.md` and `.relay-kit/state/workflow-state.md` if they exist.
2. Score the request on five axes: ambiguity, breadth of change, architecture risk, operational risk, and coordination cost.
3. Classify complexity:
   - `L0`: single bug or tiny refactor
   - `L1`: small feature or bug cluster
   - `L2`: multi-component feature slice
   - `L3`: product or platform change with design trade-offs
   - `L4`: enterprise, compliance, or scale-sensitive work
4. Choose track:
   - `L0-L1` -> quick-flow
   - `L2-L3` -> product-flow
   - `L4` -> enterprise-flow
5. Choose the layer-1 entrypoint:
   - use `bootstrap` if state, context, or artifacts are missing
   - use `cook` for one active request in one lane
   - use `team` if more than one lane, owner, or branch of work must be coordinated
6. Choose the first layer-2 hub:
   - `scout-hub` when the codebase area is unclear
   - `plan-hub` when planning artifacts are missing or stale
   - `debug-hub` when the request starts from a failure or regression
7. Mark the lane mode explicitly as one of: discovery, planning, implementation, or verification.
8. When parallel or parked lanes exist, record `depends_on`, `wave_id`, and `resume_condition` in team-board and lane-registry.
9. Update `.relay-kit/state/workflow-state.md` with the chosen track, orchestrator, hub, exact next skill, and any blockers.

## Escalation rules
Escalate immediately when:
- a small fix changes contracts, schemas, APIs, or infrastructure
- acceptance criteria are unclear or disputed
- multiple bounded contexts are touched
- rollout, migration, security, or compliance risk appears

## Output contract
Never end with vague advice. Always name the next skill, the artifact it should create or update, and what evidence is still missing.

## Role
- routing-kernel

## Layer
- layer-1-orchestrators

## Inputs
- user request
- short or ambiguous user prompt
- .relay-kit/contracts/project-context.md (if present)
- .relay-kit/state/workflow-state.md (if present)
- .relay-kit/state/team-board.md (if present)

## Outputs
- .relay-kit/state/workflow-state.md
- prompt enhancement summary when the user request is short or unclear
- .relay-kit/contracts/tech-spec.md or product-brief.md kickoff
- .relay-kit/state/team-board.md when parallel lanes are needed

## Reference skills and rules
- Prefer existing project-context over assumptions.
- For short prompts, expand intent into recommended skill, read-first context, required evidence, and an ask-or-act decision.
- When `.relay-kit/context/index.json` exists, use local context graph hits before broad repo scans.
- Prompt enhancement is not a semantic context engine, expert guarantee, or production-readiness claim.
- Escalate from quick-flow to product-flow whenever hidden complexity appears.
- Hand off to bootstrap when base artifacts are missing, to cook for a single request, and to team when multiple lanes must move in parallel.
- If session continuity is weak, run context-continuity checkpoint or rehydrate before routing deeper work.
- For existing codebases, prefer scout-hub plus repo-map before planning when dependency boundaries are still unclear.
- Open `references/workflow-router-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/workflow-router-good-output.md` and `examples/workflow-router-bad-output.md` to calibrate output quality.
- Use `evals/workflow-router-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/workflow-router-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- bootstrap
- cook
- team
- context-continuity
- scout-hub
- plan-hub
- debug-hub
- token-economy
