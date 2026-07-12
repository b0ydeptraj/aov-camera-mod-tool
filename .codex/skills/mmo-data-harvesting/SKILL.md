---
name: mmo-data-harvesting
description: Use when MMO operations need structured data collection, lead enrichment, UID targeting list building, or AI-assisted seeding content generation within authorized access boundaries.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Collect, enrich, and structure targeting data for MMO campaigns using authorized access, then generate AI content variants for seeding.

## Mandatory scope checks
- define data source authorization per collection method: official API, robots.txt-compliant scraping, or consent-collected leads
- define data schema: UID, platform handle, segment tag, interaction history, collection timestamp, source
- define enrichment pipeline: raw collection → dedup → validation → segment tagging → encrypted storage
- define seeding target list criteria: segment qualifications and frequency caps per campaign type
- define AI seeding content generator config: base template → N variants with minimum diversity score
- define retention and deletion policy: data age limits, PII encryption at rest

## Evidence contract
- include data source authorization proof for each collection method
- include enriched dataset sample with dedup count, validation pass rate, segment distribution
- include AI variant sample: 1 base message → N variants with diversity scores

## Role
- mmo-data-ops

## Layer
- layer-4-specialists-and-standalones

## Inputs
- data source inventory (API endpoints, public pages within robots.txt scope, consent form outputs)
- target segment criteria for each campaign type
- seeding campaign brief and base message templates

## Outputs
- data pipeline: collection config, enrichment rules, segmentation schema, seeding target lists, and AI content variant batches

## Reference skills and rules
- Only collect data through explicitly authorized channels — unauthorized PII collection is a legal risk and platform ban trigger.
- Deduplicate aggressively before seeding: duplicate UIDs cause redundant interactions that trigger spam detection.
- AI comment variants must have minimum edit distance — identical strings across seeding accounts cause immediate detection.
- Never store phone numbers, emails, or UIDs in plaintext — hash or encrypt all PII before storage.
- Route all seeding content through a human-review gate before deployment to high-value accounts.
- Open `references/mmo-data-harvesting-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-data-harvesting-good-output.md` and `examples/mmo-data-harvesting-bad-output.md` to calibrate output quality.
- Use `evals/mmo-data-harvesting-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-data-harvesting-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- mmo-social-marketing-automation
- mmo-content-factory
- mmo-nick-warmup-engine
- mmo-reup-automation
- policy-guard
