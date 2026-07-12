---
name: vietnamese-product-localization
description: Use when product output must be localized for Vietnamese users. Produce Vietnamese or bilingual docs, support copy, release notes, and communication artifacts with quality constraints.
---

# Mission
Localize product-facing communication for Vietnamese users with consistent terminology and clear quality boundaries.

## Mandatory scope checks
- confirm whether output should be Vietnamese-only or bilingual
- apply terminology consistency across all related artifacts
- identify locale-sensitive phrasing that can affect support or release communication
- verify whether runtime locale policy is opt-in and whether canonical IDs stay unchanged

## Evidence contract
- include glossary or terminology notes for key product terms
- mark unresolved translation ambiguities
- keep localization policy explicitly opt-in by profile

## Handoff rules
Route product positioning to `growth-marketing`, requirements changes to `pm`, readiness wording to `qa-governor`, and unsupported locale claims to `signal-calibration`.

## Failure modes
Hold when localization silently changes route names, weakens technical meaning, mixes tones across support and release copy, or claims full i18n without metadata/runtime evidence.

## Role
- localization

## Layer
- layer-4-specialists-and-standalones

## Inputs
- source content or request
- target audience context
- localization policy profile

## Outputs
- Vietnamese or bilingual product artifacts with terminology and quality notes

## Reference skills and rules
- Treat Vietnamese support as profile-based policy, not a forced global default.
- Maintain terminology consistency across docs, support, and product messaging.
- Call out any untranslated or uncertain terms explicitly.
- Open `references/vietnamese-product-localization-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/vietnamese-product-localization-good-output.md` and `examples/vietnamese-product-localization-bad-output.md` to calibrate output quality.
- Use `evals/vietnamese-product-localization-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/vietnamese-product-localization-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- growth-marketing
- pm
- review-hub
- qa-governor
