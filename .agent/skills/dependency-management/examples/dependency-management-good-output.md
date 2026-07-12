# dependency-management Battle-Calibrated Output

Request: review a dependency drift report, compare manifest to lockfile, and name rollback or pin evidence before recommending an upgrade

Recommended skill: `dependency-management` because the request matches `build-support` work and has concrete repo anchors.

Read first:

- `package.json`
- `pnpm-lock.yaml`
- `tests/dependency-lock.test.ts`

Evidence gathered:

- Confirmed `resolveDependencyPlan` or nearby ownership before recommending changes.
- Checked `dependency drift` and `lockfile` against the relevant source path.
- Identified `transitive dependency` as a required proof term before completion.

Answer:

The safe next move is to inspect the named file path, compare it with the expected test or docs surface, and only then choose implementation, review, or planning. If the anchor is missing, ask one question that names the missing file, PR, log, screen, or workflow.

Residual risk:

- `rollback pin` remains unverified until the focused gate or benchmark hit is captured.
