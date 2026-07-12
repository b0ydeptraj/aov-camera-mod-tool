---
name: mmo-social-marketing-automation
description: Use when MMO social media or marketing automation needs official API routing, campaign workspace, content calendar, moderation safeguards, and quota-aware execution.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Execute social MMO automation that can scale marketing outcomes without crossing platform enforcement lines.

## Mandatory scope checks
- map each action to official API endpoint and permission scope
- define campaign workspace fields: campaign, channel, account, asset, audience, schedule window, approval status
- define per-platform quota budget and reset handling
- define content duplication and frequency guardrails
- define moderation queue, reject reason taxonomy, and incident escalation path

## Evidence contract
- include API quota budget report and throttling behavior
- include campaign QA checks, approval trail, and reject reasons
- include compliance checklist for each target platform

## Handoff rules
Route campaign message quality to `growth-marketing`, market assumptions to `market-research`, operational scheduling to `automation-ops`, and policy risk to `policy-guard`.

## Failure modes
Hold when the plan depends on unofficial endpoints, duplicated posting bursts, missing approval lanes, weak moderation evidence, or generic social dashboard screens with no operator workflow.

## Role
- mmo-social-automation

## Layer
- layer-4-specialists-and-standalones

## Inputs
- campaign objective
- platform API capabilities
- content and moderation policy

## Outputs
- social automation operator workflow with campaign queue, content QA, quota controls, and policy-safe execution

## Reference skills and rules
- Use official platform APIs and published quota/automation rules as the default path.
- Prevent duplicate or spam-like content bursts across accounts and channels.
- Model campaign operations as a work queue: content calendar, asset library, approval lane, reject reasons, quota meter, and per-channel status.
- Keep consent, data-use transparency, and account-safety requirements explicit.
- Open `references/mmo-social-marketing-automation-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-social-marketing-automation-good-output.md` and `examples/mmo-social-marketing-automation-bad-output.md` to calibrate output quality.
- Use `evals/mmo-social-marketing-automation-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-social-marketing-automation-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- growth-marketing
- automation-ops
- market-research
- review-hub
