---
name: runtime-doctor
description: Use when runtime integrity may have drifted and you need deterministic diagnostics over adapters, artifacts, and lane state surfaces.
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Mission
Catch adapter parity and runtime artifact drift early so regressions are blocked before release or cutover batches.

## Default outputs
- runtime drift findings with exact surface references appended to qa-report or workflow-state
- pass or hold recommendation for runtime health based on parity and artifact checks

## Typical tasks
- Verify required runtime docs and state artifacts exist under `.relay-kit`.
- Check adapter skill parity against canonical registry skills across `.claude`, `.agent`, and `.codex` surfaces.
- Flag missing, extra, or drifted skills with exact adapter paths.
- In live mode, detect stale placeholder state markers that invalidate readiness claims.

## Working rules
- Keep findings deterministic and path-specific so reruns are comparable.
- Distinguish template diagnostics from live runtime diagnostics in the final report.
- Do not auto-fix runtime drift; hand actionable findings back to fix-hub.
- Return hold when strict checks fail on parity or required artifacts.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- runtime drift findings with exact surface references appended to qa-report or workflow-state
- pass or hold recommendation for runtime health based on parity and artifact checks

## Reference skills and rules
- Use `relay-kit runtime doctor <project> --strict` for deterministic runtime diagnostics.
- Use `--state-mode live` when validating active project state artifacts before release claims.
- Open `references/runtime-doctor-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/runtime-doctor-good-output.md` and `examples/runtime-doctor-bad-output.md` to calibrate output quality.
- Use `evals/runtime-doctor-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/runtime-doctor-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- debug-hub
- test-hub
- review-hub
- fix-hub
