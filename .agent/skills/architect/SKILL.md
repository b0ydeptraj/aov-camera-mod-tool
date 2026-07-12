---
name: architect
description: Use when a prd exists or when a change could alter module boundaries, data flow, security, or operations. Convert requirements into an implementation-ready architecture that fits the existing codebase.
---

# Mission
Make downstream implementation safer by turning requirements into explicit technical constraints and decisions.

## Produce `architecture.md`
Include:
- current-system constraints
- proposed design
- module boundaries
- data flow and integrations
- operational concerns
- trade-offs and ADR notes
- implementation readiness verdict

## Mandatory behavior
- Reuse existing patterns unless there is a documented reason not to.
- Name interfaces, boundaries, and ownership explicitly.
- State how observability, rollback, and failure handling will work for risky changes.
- Flag any requirement that cannot be satisfied within the current architecture without upstream scope negotiation.

## Role
- solutioning

## Layer
- layer-4-specialists-and-standalones

## Inputs
- .relay-kit/contracts/PRD.md
- .relay-kit/contracts/project-context.md
- existing support skills and references

## Outputs
- .relay-kit/contracts/architecture.md

## Reference skills and rules
- Mirror the existing codebase before inventing new patterns.
- Pull in project-architecture, dependency-management, api-integration, data-persistence, security-patterns, performance-optimization, and logging-observability when relevant.
- When stack-specific delivery is required, coordinate with go-service-engineering or next-product-frontend for implementation-level constraints.
- Architecture must include a readiness verdict, not just diagrams or aspirations.
- Open `references/architect-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/architect-good-output.md` and `examples/architect-bad-output.md` to calibrate output quality.
- Use `evals/architect-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/architect-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- project-architecture
- dependency-management
- api-integration
- data-persistence
- go-service-engineering
- next-product-frontend
- mmo-ecommerce-multichannel
- mermaid-diagrams
- scrum-master
- review-hub
- plan-hub
- workflow-router
