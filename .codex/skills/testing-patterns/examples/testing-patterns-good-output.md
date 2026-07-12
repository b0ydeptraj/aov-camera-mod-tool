# testing-patterns Battle-Calibrated Output

Request: design the test strategy for a checkout regression, choosing fixture/factory, mock versus integration, and flake controls by risk

Recommended skill: `testing-patterns` because the request matches `quality-support` work and has concrete repo anchors.

Read first:

- `tests/fixtures/user_factory.py`
- `tests/integration/test_checkout.py`
- `tests/e2e/test_checkout_flow.py`

Evidence gathered:

- Confirmed `user_factory` or nearby ownership before recommending changes.
- Checked `fixture` and `factory` against the relevant source path.
- Identified `integration boundary` as a required proof term before completion.

Answer:

The safe next move is to inspect the named file path, compare it with the expected test or docs surface, and only then choose implementation, review, or planning. If the anchor is missing, ask one question that names the missing file, PR, log, screen, or workflow.

Residual risk:

- `flake` remains unverified until the focused gate or benchmark hit is captured.
