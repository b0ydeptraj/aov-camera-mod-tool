# automation-ops Battle-Calibrated Output

Request: plan an operational automation change with rollback and dry-run evidence before enabling it

Recommended skill: `automation-ops` because the request matches `automation` work and has concrete repo anchors.

Read first:

- `.github/workflows/validate-runtime.yml`
- `scripts/runtime_doctor.py`
- `docs/site/readiness.md`

Evidence gathered:

- Confirmed `main` or nearby ownership before recommending changes.
- Checked `dry run` and `rollback` against the relevant source path.
- Identified `workflow log` as a required proof term before completion.

Answer:

The safe next move is to inspect the named file path, compare it with the expected test or docs surface, and only then choose implementation, review, or planning. If the anchor is missing, ask one question that names the missing file, PR, log, screen, or workflow.

Residual risk:

- `idempotency` remains unverified until the focused gate or benchmark hit is captured.
