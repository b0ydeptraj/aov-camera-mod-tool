# api-integration Battle-Calibrated Output

Request: trace a backend behavior bug from source file to test anchor without guessing from filenames only

Recommended skill: `api-integration` because the request matches `integration-support` work and has concrete repo anchors.

Read first:

- `src/service/session.py`
- `src/service/retry.py`
- `tests/test_session.py`

Evidence gathered:

- Confirmed `SessionManager` or nearby ownership before recommending changes.
- Checked `session` and `retry` against the relevant source path.
- Identified `cache` as a required proof term before completion.

Answer:

The safe next move is to inspect the named file path, compare it with the expected test or docs surface, and only then choose implementation, review, or planning. If the anchor is missing, ask one question that names the missing file, PR, log, screen, or workflow.

Residual risk:

- `transaction boundary` remains unverified until the focused gate or benchmark hit is captured.
