# repo-map Battle-Calibrated Output

Request: map the repo area for a session bug, naming entrypoints, ownership boundary, dependency direction, and nearby tests/docs

Recommended skill: `repo-map` because the request matches `utility-provider` work and has concrete repo anchors.

Read first:

- `src/main.ts`
- `src/auth/session.ts`
- `docs/architecture.md`

Evidence gathered:

- Confirmed `main` or nearby ownership before recommending changes.
- Checked `entrypoint` and `ownership` against the relevant source path.
- Identified `dependency direction` as a required proof term before completion.

Answer:

The safe next move is to inspect the named file path, compare it with the expected test or docs surface, and only then choose implementation, review, or planning. If the anchor is missing, ask one question that names the missing file, PR, log, screen, or workflow.

Residual risk:

- `nearby test` remains unverified until the focused gate or benchmark hit is captured.
