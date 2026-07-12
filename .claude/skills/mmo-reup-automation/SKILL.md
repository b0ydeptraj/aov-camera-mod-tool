---
name: mmo-reup-automation
description: Use when controlled MMO reup workflows need operator-run queues, scheduling windows, deduplication, attribution tracking, and policy-safe publishing controls.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Build safe, measurable content reup automation for MMO operations without violating platform rules.

## Mandatory scope checks
- define content ownership and permitted reuse policy
- define source inventory fields: source id, rights status, attribution, fingerprint, last published, channel
- define dedupe key strategy and repost frequency caps
- define channel-specific posting windows and rate limits
- define run queue states: draft, queued, publishing, rejected, published, rolled back
- define emergency stop, rollback, and operator ownership

## Evidence contract
- include dry-run output with dedupe and throttle decisions
- include sample publish and reject logs with reason codes in an evidence drawer
- include rollback and disable-runbook instructions

## Role
- mmo-reup

## Layer
- layer-4-specialists-and-standalones

## Inputs
- content source inventory
- rights and attribution constraints
- target channel policy limits

## Outputs
- reup operator console design with dedupe ledger, run queue, rate controls, and rollback plan

## Reference skills and rules
- Require explicit rights and attribution constraints before any automated repost flow.
- Use deterministic dedup keys and publish windows to avoid accidental spam bursts.
- Model the UI as an operator workbench: source inventory table, bulk action bar, publish queue, reject drawer, and evidence timeline.
- Block flows that depend on policy evasion, account abuse, or non-consensual content reuse.
- Open `references/mmo-reup-automation-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-reup-automation-good-output.md` and `examples/mmo-reup-automation-bad-output.md` to calibrate output quality.
- Use `evals/mmo-reup-automation-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-reup-automation-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- automation-ops
- policy-guard
- qa-governor
- review-hub
