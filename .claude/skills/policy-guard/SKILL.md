---
name: policy-guard
description: Use when high-risk agent operations need deterministic policy checks before trusting shell, path, secret, prompt, or allowlist changes, with a strict fail-closed posture.
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Mission
Fail closed on deterministic high-risk agent operation patterns before they reach release or handoff.

## Default outputs
- policy risk findings appended to qa-report or workflow-state
- explicit pass or hold verdict for high-risk runtime operations

## Typical tasks
- Scan runtime and source surfaces for path traversal, destructive shell commands, hard-coded secrets, and prompt-injection phrases.
- Report exact file, line, and check names so the owning hub can fix or explicitly escalate.
- Rerun the strict policy gate after any remediation before claiming the lane is safe.
- Apply fail-closed handling whenever risk classification is uncertain.

## Working rules
- Do not treat policy findings as cosmetic lint.
- Prefer fixing the risky surface over allowlisting it.
- Escalate to review-hub when a finding is intentional but operationally sensitive.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- policy risk findings appended to qa-report or workflow-state
- explicit pass or hold verdict for high-risk runtime operations

## Reference skills and rules
- Use `relay-kit policy check <project> --strict` as the canonical policy gate.
- Treat policy findings as release blockers until reviewed by qa-governor or review-hub.
- Open `references/policy-guard-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/policy-guard-good-output.md` and `examples/policy-guard-bad-output.md` to calibrate output quality.
- Use `evals/policy-guard-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/policy-guard-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- qa-governor
- review-hub
- fix-hub
