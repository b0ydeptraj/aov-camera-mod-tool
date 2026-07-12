# mmo-mobile-app-automation Battle-Calibrated Output

Request: review mobile automation with device inventory, hub, provider, lease owner, logcat, and app-state recovery evidence

Recommended skill: `mmo-mobile-app-automation` because the request matches `mmo-mobile-automation` work and has concrete repo anchors.

Read first:

- `ops/devices.json`
- `workers/mobile_runner.ts`
- `docs/mobile-recovery-runbook.md`

Evidence gathered:

- Confirmed `DeviceLease` or nearby ownership before recommending changes.
- Checked `device lease` and `logcat` against the relevant source path.
- Identified `app-state` as a required proof term before completion.

Answer:

The safe next move is to inspect the named file path, compare it with the expected test or docs surface, and only then choose implementation, review, or planning. If the anchor is missing, ask one question that names the missing file, PR, log, screen, or workflow.

Residual risk:

- `operator ledger` remains unverified until the focused gate or benchmark hit is captured.
