# mmo-reup-automation Battle-Calibrated Output

Request: review reup workflow with source inventory, publish queue, dedupe, reject drawer, and evidence timeline before automation changes

Recommended skill: `mmo-reup-automation` because the request matches `mmo-reup` work and has concrete repo anchors.

Read first:

- `ops/source_inventory.csv`
- `workers/reup_queue.ts`
- `docs/reup-source-policy.md`

Evidence gathered:

- Confirmed `SourceInventory` or nearby ownership before recommending changes.
- Checked `source inventory` and `publish queue` against the relevant source path.
- Identified `dedupe` as a required proof term before completion.

Answer:

The safe next move is to inspect the named file path, compare it with the expected test or docs surface, and only then choose implementation, review, or planning. If the anchor is missing, ask one question that names the missing file, PR, log, screen, or workflow.

Residual risk:

- `evidence timeline` remains unverified until the focused gate or benchmark hit is captured.
