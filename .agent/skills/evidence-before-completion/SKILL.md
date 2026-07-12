---
name: evidence-before-completion
description: Use when a hub or specialist has specific completion claims to verify. Map each claim to fresh proof output before saying work is done, fixed, or ready. Claim-to-evidence utility.
---

# Mission
Stop premature completion claims by forcing a claim-to-evidence check.

## Boundary
- Use for specific completion claims that need proof output.
- This is not a readiness verdict and does not decide shipability.
- This utility does not own `qa-report.md`; qa-governor owns formal QA reports and go or no-go recommendations.

## Default outputs
- fresh claim-to-evidence checks and proof output appended to workflow-state or the active artifact

## Evidence contract
- Input must include the exact claims being made and the newest available evidence.
- Output must map each claim to a command, artifact, or observed proof output.
- Reject any claim without fresh evidence and route back to testing or debugging.

## Typical tasks
- List the exact claims being made.
- Name the command, artifact, or proof output that proves each claim.
- Check whether expected artifact deltas actually exist for code-change claims.
- Reject claims that are not backed by fresh evidence.

## Working rules
- Confidence is not evidence.
- Partial verification is not completion.
- If evidence is stale or missing, route back to testing or debugging instead of approving the lane.
- If a code-change claim has zero file delta and zero verification output, mark it invalid unless the lane explicitly recorded a no-code outcome.

## Role
- utility-provider

## Layer
- layer-3-utility-providers

## Inputs
- active hub or orchestrator request
- current authoritative artifact
- only the evidence relevant to this pass

## Outputs
- fresh claim-to-evidence checks and proof output appended to workflow-state or the active artifact

## Reference skills and rules
- No completion claims without fresh verification output.
- Match every claim to the command or evidence that proves it.
- Hand formal readiness verdicts to qa-governor or ready-check.
- Open `references/evidence-before-completion-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/evidence-before-completion-good-output.md` and `examples/evidence-before-completion-bad-output.md` to calibrate output quality.
- Use `evals/evidence-before-completion-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/evidence-before-completion-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- test-hub
- qa-governor
- review-hub
