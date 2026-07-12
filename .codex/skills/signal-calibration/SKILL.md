---
name: signal-calibration
description: Use when a claim risks being overrated, guessed, or stronger than the available evidence. Calibrate readiness, skill quality, field-tested, production-ready, commercial-ready, backend realism, UI realism, MMO/API realism, or benchmark claims before accepting them.
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Mission
Turn confident-sounding claims into calibrated proof levels so Relay-kit does not overrate itself or the work it produces.

## Boundary
- Use for claim calibration and overclaim detection, not for running the whole QA lane.
- Do not replace evidence-before-completion for narrow completion proof or qa-governor for formal readiness verdicts.
- Do not treat local fixtures, public repo benchmarks, or read-only audits as field validation.

## Default outputs
- signal calibration report with claim, claim_type, proof_level, verdict, confidence, overclaim flags, residual risk, and next verification
- explicit pass or hold verdict for overclaim-prone wording before readiness, release, quality, or benchmark claims
- claim-to-evidence notes appended to qa-report, workflow-state, or release artifacts

## Evidence contract
- Input must include the exact claim or the report surface being calibrated.
- Output must include `claim`, `claim_type`, `proof_level`, `verdict`, `confidence`, `evidence_sources`, `overclaim_flags`, `residual_risk`, and `next_verification`.
- Claims without concrete file, command, log, source, or artifact evidence must be marked inferred or unsupported.
- Field-tested, production-ready, and commercial-ready wording must be blocked unless the required evidence class exists.

## Typical tasks
- Classify claims as proven, partially-proven, inferred, unsupported, or contradicted.
- Map skill quality claims to proof audit, real-world eval, skill-battle, competency-battle, or battle-audit evidence.
- Downgrade fixture-backed claims to validated instead of field-tested.
- Detect public copy or operator answers that imply stronger evidence than Relay-kit actually has.
- Name the smallest next verification needed to make the claim safe.

## Working rules
- Confidence is not proof.
- Benchmark evidence is not adoption evidence.
- Validated is not field-tested.
- If evidence class is unclear, block the claim instead of smoothing it over.
- Keep Relay-kit-owned terminology; do not call this a confusion matrix.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- signal calibration report with claim, claim_type, proof_level, verdict, confidence, overclaim flags, residual risk, and next verification
- explicit pass or hold verdict for overclaim-prone wording before readiness, release, quality, or benchmark claims
- claim-to-evidence notes appended to qa-report, workflow-state, or release artifacts

## Reference skills and rules
- Use `relay-kit calibrate readiness <project> --strict` for enterprise readiness claim calibration.
- Use `relay-kit calibrate skill <project> --skill all --strict` before claiming skill quality.
- Use `relay-kit calibrate claims <project> --claim "..." --strict` when exact wording needs proof.
- Do not call fixture validation field-tested; field-tested requires `.relay-kit/evidence/skill-field-evidence.json`.
- Open `references/signal-calibration-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/signal-calibration-good-output.md` and `examples/signal-calibration-bad-output.md` to calibrate output quality.
- Use `evals/signal-calibration-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/signal-calibration-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- evidence-before-completion
- qa-governor
- review-hub
- skill-gauntlet
- release-readiness
