---
name: mmo-content-factory
description: Use when MMO operations need AI-assisted bulk content generation, multi-platform scheduling, video repurposing, variant creation, and cross-channel content distribution at scale.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Run a content production pipeline that converts raw assets into platform-optimized variants and schedules them without detectable spam patterns.

## Mandatory scope checks
- define content brief → variant generation pipeline: text, image, short video cuts from long-form source
- define platform-specific output specs: TikTok (9:16, 15-60s), Facebook Reel (9:16), YouTube Shorts (<60s)
- define variant diversity threshold: minimum edit-distance or visual-diff score between variants
- define publishing schedule: posting windows, frequency caps per account, platform quota alignment
- define human-review gate: content types and risk tiers requiring operator approval
- define performance feedback loop: track per-variant reach and feed signal back into generation config

## Evidence contract
- include sample batch: 1 brief → N variants with diversity diff scores
- include publishing schedule proof: no platform quota breach across all active accounts
- include human-review decision log for flagged content

## Role
- mmo-content-ops

## Layer
- layer-4-specialists-and-standalones

## Inputs
- content briefs or raw assets (long-form video, images, article text, product info)
- platform account inventory and per-account quota budgets
- brand voice guidelines, prohibited content rules, platform-specific formatting requirements

## Outputs
- content production pipeline: generation config, variant specs, diversity rules, scheduling plan, review gates, and performance feedback schema

## Reference skills and rules
- Identical or near-identical content across accounts triggers spam detection — enforce minimum diversity scores between all variants.
- AI-generated content variants must pass a human-review gate before deployment to high-risk accounts.
- Platform-specific formatting is not optional: wrong aspect ratio or duration causes algorithmic reach penalty.
- Publishing windows must be staggered across accounts — never schedule identical content to multiple accounts simultaneously.
- Open `references/mmo-content-factory-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-content-factory-good-output.md` and `examples/mmo-content-factory-bad-output.md` to calibrate output quality.
- Use `evals/mmo-content-factory-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-content-factory-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- mmo-reup-automation
- mmo-social-marketing-automation
- mmo-data-harvesting
- growth-marketing
- qa-governor
