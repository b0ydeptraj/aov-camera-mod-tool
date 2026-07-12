# go-service-engineering Battle-Calibrated Output

Request: trace a Go request from handler to service and repo, then identify context cancellation and httptest evidence before changing behavior

Recommended skill: `go-service-engineering` because the request matches `go-engineering` work and has concrete repo anchors.

Read first:

- `cmd/api/main.go`
- `internal/http/user_handler.go`
- `internal/service/user_service_test.go`

Evidence gathered:

- Confirmed `UserHandler` or nearby ownership before recommending changes.
- Checked `handler boundary` and `context cancellation` against the relevant source path.
- Identified `transaction boundary` as a required proof term before completion.

Answer:

The safe next move is to inspect the named file path, compare it with the expected test or docs surface, and only then choose implementation, review, or planning. If the anchor is missing, ask one question that names the missing file, PR, log, screen, or workflow.

Residual risk:

- `httptest` remains unverified until the focused gate or benchmark hit is captured.
