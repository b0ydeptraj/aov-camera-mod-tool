# ui-styling Battle-Calibrated Output

Request: review a login UI change, name files first, and identify the test evidence before editing

Recommended skill: `ui-styling` because the request matches `ui-styling` work and has concrete repo anchors.

Read first:

- `src/app/login/page.tsx`
- `src/components/LoginForm.tsx`
- `tests/login.spec.ts`

Evidence gathered:

- Confirmed `LoginForm` or nearby ownership before recommending changes.
- Checked `login flow` and `component boundary` against the relevant source path.
- Identified `accessibility state` as a required proof term before completion.

Answer:

The safe next move is to inspect the named file path, compare it with the expected test or docs surface, and only then choose implementation, review, or planning. If the anchor is missing, ask one question that names the missing file, PR, log, screen, or workflow.

Residual risk:

- `visual regression` remains unverified until the focused gate or benchmark hit is captured.
