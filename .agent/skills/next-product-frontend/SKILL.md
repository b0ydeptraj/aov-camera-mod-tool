---
name: next-product-frontend
description: Use when work is primarily Next.js product UI or frontend architecture. Plan and implement App Router flows, server and client boundaries, server actions, data fetching, and quality gates for user-facing delivery.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Build or refactor Next.js product surfaces with explicit server/client architecture and measurable quality.

## Mandatory scope checks
- identify App Router route ownership and layout boundaries
- document server component versus client component decisions
- define server actions contracts for mutation-heavy flows
- define data fetching and cache behavior for changed screens
- define component ownership, styling system, and state coverage before coding
- enforce accessibility and performance checks for user-facing risk

## Evidence contract
- include route-level behavior proof
- include accessibility findings or gate output
- include performance or hydration-risk notes when relevant

## Handoff rules
Hand implementation to `developer`, styling detail to `ui-styling`, visual critique to `aesthetic`, and accessibility proof to `accessibility-review`.

## Failure modes
Hold when the plan treats every screen as generic client-side React, skips cache semantics, ignores error/loading states, or produces a page that looks like a template instead of a product surface.

## Role
- next-frontend

## Layer
- layer-4-specialists-and-standalones

## Inputs
- frontend request or story
- existing Next.js structure
- design and UX constraints

## Outputs
- Next.js implementation plan or code delta with accessibility and performance evidence

## Reference skills and rules
- Prefer App Router and server/client boundary clarity over generic React-only guidance.
- Keep shadcn or existing component-system usage consistent with local patterns.
- Collect accessibility and performance evidence before completion claims.
- Open `references/next-product-frontend-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/next-product-frontend-good-output.md` and `examples/next-product-frontend-bad-output.md` to calibrate output quality.
- Use `evals/next-product-frontend-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/next-product-frontend-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- developer
- ux-structure
- accessibility-review
- review-hub
