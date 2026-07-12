---
name: mmo-identity-infrastructure
description: Use when MMO multi-account operations need fingerprint isolation, proxy-to-profile binding, anti-detect browser setup, and consistent digital identity management per account.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Build airtight per-account digital identities that survive platform behavioral analysis and hardware fingerprinting.

## Mandatory scope checks
- define fingerprint profile strategy per account: UA, WebGL, Canvas, fonts, timezone, language, screen resolution
- enforce 1:1 rule: one proxy → one browser profile → one account; document each binding explicitly
- define proxy type selection per risk tier: residential for high-trust, mobile for highest stealth, ISP static for stable long sessions
- define consistency validation: timezone ↔ proxy geolocation ↔ language ↔ platform locale
- define fingerprint stability policy: when to keep stable (established accounts) vs when to rotate (new profiles only)
- define profile version control: fingerprint specs stored, tracked, and reproducible

## Evidence contract
- include profile × proxy binding registry with consistency audit output
- include fingerprint consistency check: timezone, locale, UA, hardware coherence all validated
- include one controlled test: new profile passes target platform basic trust gate

## Role
- mmo-identity-infrastructure

## Layer
- layer-4-specialists-and-standalones

## Inputs
- account inventory and risk tier classification
- proxy pool inventory (type, geo, ASN, provider)
- target platform fingerprint detection signals

## Outputs
- identity infrastructure plan: per-account profile specs, proxy assignments, consistency rules, rotation policy, and binding registry

## Reference skills and rules
- Never reuse a proxy or fingerprint profile across multiple accounts — IP clustering causes linked-account bans.
- Align timezone, language, and locale with proxy geolocation; mismatches are the #1 platform detection trigger.
- Use sticky sessions for established accounts; reserve proxy rotation for new profiles only.
- Treat fingerprint profiles as versioned infrastructure: changes must be logged with reason and timestamp.
- Anti-detect browsers (AdsPower, Multilogin, GoLogin, Hidemyacc) are the required execution environment.
- Open `references/mmo-identity-infrastructure-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-identity-infrastructure-good-output.md` and `examples/mmo-identity-infrastructure-bad-output.md` to calibrate output quality.
- Use `evals/mmo-identity-infrastructure-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-identity-infrastructure-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- mmo-browser-fleet-automation
- mmo-account-operations
- mmo-nick-warmup-engine
- mmo-proxy-network-ops
- policy-guard
