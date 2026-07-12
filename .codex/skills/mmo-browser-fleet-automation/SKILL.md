---
name: mmo-browser-fleet-automation
description: Use when MMO browser-based operations need profile inventory, session orchestration, deterministic waits, live debug evidence, and anti-flake reliability controls.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Run browser MMO operations with high reliability, clear limits, and policy-safe automation behavior.

## Mandatory scope checks
- define profile isolation, profile-to-proxy affinity, and session lease strategy
- define operator inventory fields: profile id, folder, tags, proxy status, lease owner, browser state, last run, next allowed run
- define selector contract and wait strategy per critical action
- define retry and backoff rules for transient UI/network failures
- define live debug evidence: screenshots, console logs, network errors, DOM snapshot, and human takeover marker
- define runbook for stuck session, timeout, and rate-limit events

## Evidence contract
- include run traces for one success path and one controlled failure path
- include selector drift and timeout diagnostics
- include policy and rate-limit guard decisions per run with raw trace pointers

## Role
- mmo-browser-automation

## Layer
- layer-4-specialists-and-standalones

## Inputs
- browser workflow map
- profile/session constraints
- target platform policy and limits

## Outputs
- browser fleet operator design with profile/session lease table, stable selectors, run queue, and debug evidence

## Reference skills and rules
- Prefer official API paths when available; use browser automation for allowed UI workflows only.
- Use explicit waits, resilient locators, and deterministic retry policy instead of blind sleeps.
- Keep profile-to-proxy affinity explicit; validate proxy health before launch and preserve profile folders/tags for operator filtering.
- Design dense operator screens: live session list, lease owner, selector drift, screenshot trace, console/network tabs, retry button, and stop button.
- Forbid automation patterns that rely on stealth evasion or non-API scraping prohibited by policy.
- Open `references/mmo-browser-fleet-automation-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-browser-fleet-automation-good-output.md` and `examples/mmo-browser-fleet-automation-bad-output.md` to calibrate output quality.
- Use `evals/mmo-browser-fleet-automation-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-browser-fleet-automation-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- automation-ops
- browser-inspector
- policy-guard
- qa-governor
