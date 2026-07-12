# browser-inspector Battle-Calibrated Output

Request: inspect a browser login runtime issue with console, network, DOM state, screenshot, and reproduction trace evidence

Recommended skill: `browser-inspector` because the request matches `utility-provider` work and has concrete repo anchors.

Read first:

- `src/app/login/page.tsx`
- `tests/e2e/login.spec.ts`
- `artifacts/login-screenshot.md`

Evidence gathered:

- Confirmed `LoginPage` or nearby ownership before recommending changes.
- Checked `console` and `network` against the relevant source path.
- Identified `dom` as a required proof term before completion.

Answer:

The safe next move is to inspect the named file path, compare it with the expected test or docs surface, and only then choose implementation, review, or planning. If the anchor is missing, ask one question that names the missing file, PR, log, screen, or workflow.

Residual risk:

- `screenshot` remains unverified until the focused gate or benchmark hit is captured.
