# mmo-cloud-operations-automation Battle-Calibrated Output

Request: review cloud automation with worker pool, queue depth, stalled jobs, dead-letter handling, pause control, and operator ledger evidence

Recommended skill: `mmo-cloud-operations-automation` because the request matches `mmo-cloud-automation` work and has concrete repo anchors.

Read first:

- `ops/queues.yaml`
- `workers/cloud_worker.ts`
- `docs/cloud-worker-runbook.md`

Evidence gathered:

- Confirmed `CloudWorker` or nearby ownership before recommending changes.
- Checked `worker queue` and `queue depth` against the relevant source path.
- Identified `dead-letter` as a required proof term before completion.

Answer:

The safe next move is to inspect the named file path, compare it with the expected test or docs surface, and only then choose implementation, review, or planning. If the anchor is missing, ask one question that names the missing file, PR, log, screen, or workflow.

Residual risk:

- `pause` remains unverified until the focused gate or benchmark hit is captured.
