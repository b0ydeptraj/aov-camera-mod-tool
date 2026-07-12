---
name: mmo-nick-warmup-engine
description: Use when MMO accounts need a structured warmup sequence to build platform trust before high-risk actions, including behavioral scripting, interaction scheduling, and trust-score monitoring.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Turn newly created or recovered accounts into trusted platform citizens through a controlled, human-mimicking warmup program.

## Mandatory scope checks
- define warmup duration and phase gates per account tier: 7 days (basic trust) to 14 days (high-trust seeding-ready)
- define daily action budget per phase: scroll, like, comment, friend-add, group-join limits with escalation curve
- define behavioral variance rules: randomized delays, action order shuffling, natural rest windows
- define trust signal targets at each phase gate: profile completeness, 2FA, friend count, post history
- define checkpoint recovery protocol: steps when account hits verification or restriction wall
- define readiness verdict: binary pass/fail gate before account enters any monetization or seeding workflow

## Evidence contract
- include warmup schedule per phase with action budgets, variance parameters, and trust targets
- include trust-signal log at end of each phase
- include one full green run: account passes all phases and target platform trust gate

## Role
- mmo-nick-warmup

## Layer
- layer-4-specialists-and-standalones

## Inputs
- account batch inventory: age, source platform, current trust state, profile completeness
- target platform action budget and rate limits per account tier
- execution environment: boxphone / anti-detect browser / mobile emulator

## Outputs
- warmup program: phase plan, daily action scripts, behavioral variance config, trust checkpoints, and per-account readiness verdict

## Reference skills and rules
- Warmup is mandatory — skipping it causes mass bans on fresh accounts within 24-48 hours of high-risk actions.
- Human-like variance in timing is non-negotiable: never use fixed intervals or identical action sequences across accounts.
- Use AI-generated content variants for comments and posts during warmup to avoid pattern detection.
- Treat warmup completion as a binary gate: no account enters seeding or monetization without passing all phase checks.
- Boxphone (real physical devices) produces higher trust scores than emulator warmup for Facebook and TikTok.
- Open `references/mmo-nick-warmup-engine-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-nick-warmup-engine-good-output.md` and `examples/mmo-nick-warmup-engine-bad-output.md` to calibrate output quality.
- Use `evals/mmo-nick-warmup-engine-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-nick-warmup-engine-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- mmo-account-operations
- mmo-browser-fleet-automation
- mmo-social-marketing-automation
- mmo-identity-infrastructure
- policy-guard
