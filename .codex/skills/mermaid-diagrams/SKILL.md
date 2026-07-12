---
name: mermaid-diagrams
description: Use when architecture, flow, or sequencing should be expressed as a quick mermaid diagram inside an artifact. Diagramming utility.
---

# Mission
Make complex flow or structure easier to reason about with a compact diagram.

## Default outputs
- mermaid snippets inserted into architecture, project-context, or docs

## Typical tasks
- Draw module boundaries or request flows.
- Show sequence or state transitions.
- Keep the diagram synchronized with the surrounding text.

## Working rules
- Use only the detail level needed for the current decision.
- Avoid giant diagrams.
- Explain trade-offs in text when the diagram alone is insufficient.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- mermaid snippets inserted into architecture, project-context, or docs

## Reference skills and rules
- Prefer diagrams that clarify ownership, flow, or sequencing.
- Diagrams should serve the artifact, not replace it.
- Open `references/mermaid-diagrams-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mermaid-diagrams-good-output.md` and `examples/mermaid-diagrams-bad-output.md` to calibrate output quality.
- Use `evals/mermaid-diagrams-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mermaid-diagrams-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- plan-hub
- architect
- review-hub
