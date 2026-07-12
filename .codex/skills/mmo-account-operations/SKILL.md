---
name: mmo-account-operations
description: Use when MMO account operations need profile inventory, lifecycle automation, health checks, risk segmentation, and recovery runbooks.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Operate MMO account fleets with deterministic controls, safety gates, and clear audit trails.

## Mandatory scope checks
- classify account states: onboarding, active, limited, suspended, retired
- define account inventory fields: owner, folder, tags, proxy binding, session status, health score, last action, cooldown until
- enforce credential storage and rotation controls
- define per-account and per-platform action budgets
- define bulk action review and dry-run approval before changes touch more than one account
- define incident response and suspension recovery path

## Evidence contract
- include account-state transition logs
- include budget and limit guard outputs
- include quarantine, cooldown, and escalation checklist for enforcement events

## Role
- mmo-account-ops

## Layer
- layer-4-specialists-and-standalones

## Inputs
- account inventory and ownership
- security and compliance policy
- platform limits and escalation paths

## Outputs
- account operations console contract with profile table, health scoring, risk controls, observability, and recovery plan

## Reference skills and rules
- Account automation must use authorized credentials, clear ownership, and auditable actions.
- Never design flows for CAPTCHA bypass, identity spoofing, or policy circumvention.
- Mirror real account tools: folder/tag filters, owner columns, proxy binding, account health, cooldown, quarantine, and bulk action review.
- Separate routine lifecycle automation from high-risk actions that require manual approval.
- Open `references/mmo-account-operations-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-account-operations-good-output.md` and `examples/mmo-account-operations-bad-output.md` to calibrate output quality.
- Use `evals/mmo-account-operations-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-account-operations-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- automation-ops
- policy-guard
- release-readiness
- qa-governor
