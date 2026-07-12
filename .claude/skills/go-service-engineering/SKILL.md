---
name: go-service-engineering
description: Use when the request is primarily Go backend service work. Define handler boundary, transaction boundary, persistence, middleware, jobs, caching, and test evidence for Go service delivery.
---

# Mission
Deliver Go service work the way a backend owner would review it: boundaries first, failure modes named, evidence attached.

## Mandatory scope checks
- Confirm module boundaries, routing table ownership, and service ownership before coding.
- Define handler boundary, request validation, response shape, and error mapping for the target service.
- Make persistence strategy explicit: ORM, sqlc, query builder, or SQL-first path.
- Name transaction boundary, repository interface, cache invalidation, and background job behavior when state or throughput depends on them.
- Handle context cancellation and timeout propagation on IO-heavy paths.
- Require unit, httptest, integration, migration rollback, and observability evidence before claiming completion.

## Evidence contract
- name the exact test commands used
- include failing signal and green signal for changed behavior
- include one table-driven edge case or explicit reason it does not apply
- record any migration or data-risk notes for rollout

## Role
- go-engineering

## Layer
- layer-4-specialists-and-standalones

## Inputs
- go service requirements
- existing Go module structure
- architecture or tech-spec when available

## Outputs
- Go service implementation plan or code delta with test and runtime evidence

## Reference skills and rules
- Prefer established local service patterns over introducing a new framework by default.
- Cover routing table, handler boundary, repository interface, transaction boundary, cache ownership, background jobs, and observability in one coherent service contract.
- Include evidence commands for unit tests, httptest or handler tests, integration tests, context cancellation, and migration rollback safety where relevant.
- Open `references/go-service-engineering-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/go-service-engineering-good-output.md` and `examples/go-service-engineering-bad-output.md` to calibrate output quality.
- Use `evals/go-service-engineering-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/go-service-engineering-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- developer
- testing-patterns
- qa-governor
- review-hub
