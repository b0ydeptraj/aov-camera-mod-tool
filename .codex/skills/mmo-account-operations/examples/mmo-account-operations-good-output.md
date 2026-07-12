# mmo-account-operations Battle-Calibrated Output

Request: review account health automation with profile table, proxy binding, cooldown, quarantine, and operator ledger evidence

Recommended skill: `mmo-account-operations` because the request matches `mmo-account-ops` work and has concrete repo anchors.

Read first:

- `ops/accounts.csv`
- `ops/account_health.ts`
- `docs/account-runbook.md`

Evidence gathered:

- Confirmed `AccountHealth` or nearby ownership before recommending changes.
- Checked `account health` and `quarantine` against the relevant source path.
- Identified `cooldown` as a required proof term before completion.

Answer:

The safe next move is to inspect the named file path, compare it with the expected test or docs surface, and only then choose implementation, review, or planning. If the anchor is missing, ask one question that names the missing file, PR, log, screen, or workflow.

Residual risk:

- `operator ledger` remains unverified until the focused gate or benchmark hit is captured.
