---
name: multimodal-evidence
description: Use when screenshots, diagrams, rendered UIs, or media artifacts contain important clues. Multimodal evidence utility.
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Mission
Translate visual or media evidence into concrete observations the active lane can use.

## Boundary
- Use only when an image, video, diagram, rendered UI, or media artifact is itself the evidence.
- Use browser-inspector instead when the required evidence is live DOM, console, network, or performance state.
- Do not infer hidden behavior from visuals alone; label visible facts separately from interpretation.

## Default outputs
- visual or media observations appended to the active artifact

## Evidence contract
- Input must identify the artifact path, source, timestamp or version, and the question being answered.
- Output must list visible observations, confidence, affected acceptance criteria, and follow-up checks.
- Reference any helper used, such as `templates/skills/multimodal-evidence/scripts/document_converter.py` or `media_optimizer.py`.

## Typical tasks
- Inspect screenshots, diagrams, or logs embedded as images.
- Summarize what changed between before/after artifacts.
- Call out ambiguous areas that need manual confirmation.

## Working rules
- Do not over-interpret weak signals.
- Tie observations to UI states, logs, or acceptance criteria.
- Keep the output compact and actionable.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- visual or media observations appended to the active artifact

## Reference skills and rules
- Describe what is visible and why it matters.
- Feed observations back to the owning hub.
- Open `references/multimodal-evidence-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/multimodal-evidence-good-output.md` and `examples/multimodal-evidence-bad-output.md` to calibrate output quality.
- Use `evals/multimodal-evidence-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/multimodal-evidence-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- debug-hub
- test-hub
- review-hub
