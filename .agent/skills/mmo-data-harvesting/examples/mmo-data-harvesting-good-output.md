# mmo-data-harvesting Battle-Calibrated Output

Request: review an operator-owned MMO automation lane for safety, repeatability, and evidence logging

Recommended skill: `mmo-data-harvesting` because the request matches `mmo-data-ops` work and has concrete repo anchors.

Read first:

- `ops/accounts.csv`
- `workers/session_runner.ts`
- `logs/run-2026-05-17.json`

Evidence gathered:

- Confirmed `SessionRunner` or nearby ownership before recommending changes.
- Checked `operator queue` and `quota` against the relevant source path.
- Identified `dedupe` as a required proof term before completion.

Answer:

The safe next move is to inspect the named file path, compare it with the expected test or docs surface, and only then choose implementation, review, or planning. If the anchor is missing, ask one question that names the missing file, PR, log, screen, or workflow.

Residual risk:

- `recovery runbook` remains unverified until the focused gate or benchmark hit is captured.
