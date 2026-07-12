# go-service-engineering Weak Output Anti-Example

Request: trace a Go request from handler to service and repo, then identify context cancellation and httptest evidence before changing behavior

Weak answer:

This looks like `go-service-engineering`, so follow the usual checklist and it should be fine.

Why this fails:

- No file path from `public Go API service with handler, service, repository, middleware, and httptest coverage` was inspected.
- No symbol such as `UserHandler` was confirmed.
- No proof surface was named for `handler boundary`.
- It blurs verified evidence and inference, which is exactly how overclaim slips back into Relay-kit.

Correction:

Name the concrete path, inspect or search it, state what is verified, and leave unverified claims labeled until a gate proves them.
