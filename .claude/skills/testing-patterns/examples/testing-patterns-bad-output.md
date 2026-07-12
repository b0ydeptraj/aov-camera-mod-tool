# testing-patterns Weak Output Anti-Example

Request: design the test strategy for a checkout regression, choosing fixture/factory, mock versus integration, and flake controls by risk

Weak answer:

This looks like `testing-patterns`, so follow the usual checklist and it should be fine.

Why this fails:

- No file path from `public test-heavy repo with fixtures, factories, unit tests, integration tests, and a flaky e2e lane` was inspected.
- No symbol such as `user_factory` was confirmed.
- No proof surface was named for `fixture`.
- It blurs verified evidence and inference, which is exactly how overclaim slips back into Relay-kit.

Correction:

Name the concrete path, inspect or search it, state what is verified, and leave unverified claims labeled until a gate proves them.
