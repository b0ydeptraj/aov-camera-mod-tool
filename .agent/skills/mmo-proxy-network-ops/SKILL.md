---
name: mmo-proxy-network-ops
description: Use when MMO operations need proxy pool management, health monitoring, sticky session assignment, rotation policy, and network-level isolation per account or workflow.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Operate a reliable, cost-efficient proxy network that supports multi-account isolation without IP clustering or session leakage.

## Mandatory scope checks
- define proxy pool composition ratio: residential, mobile, ISP static — by platform risk tier
- define sticky session policy: duration per account tier, renewal trigger, failure fallback
- define health check schedule: latency, anonymity level, geo drift, blacklist status
- define proxy assignment registry: each proxy bound to exactly one profile/account
- define cost ceiling and automatic scale-down trigger
- define decommission protocol: blacklisted proxies removed immediately

## Evidence contract
- include proxy health check report: latency, geo, ASN, blacklist status per proxy
- include session stability log covering at least one 24-hour window
- include assignment registry proving zero proxy-sharing across accounts

## Role
- mmo-proxy-ops

## Layer
- layer-4-specialists-and-standalones

## Inputs
- proxy pool inventory (provider, type, geo, ASN, expiry, cost)
- account and browser profile binding requirements
- target platform sensitivity level and known detection signals

## Outputs
- proxy operations plan: pool segmentation, assignment registry, health check schedule, rotation triggers, and monitoring runbook

## Reference skills and rules
- Residential and mobile proxies are required for high-trust platforms; datacenter proxies fail modern detection.
- Never rotate IP mid-session for established accounts — treat IP change as a trust-reset event requiring re-warmup.
- Log every proxy assignment change with timestamp, reason, and operator; treat the registry as a security artifact.
- Decommission proxies that appear on blacklists immediately, even if an active session is running.
- Open `references/mmo-proxy-network-ops-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-proxy-network-ops-good-output.md` and `examples/mmo-proxy-network-ops-bad-output.md` to calibrate output quality.
- Use `evals/mmo-proxy-network-ops-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-proxy-network-ops-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- mmo-identity-infrastructure
- mmo-browser-fleet-automation
- mmo-account-operations
- mmo-nick-warmup-engine
- policy-guard
