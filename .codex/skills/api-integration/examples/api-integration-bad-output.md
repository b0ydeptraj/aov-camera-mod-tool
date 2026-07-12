# api-integration Weak Output Anti-Example

Request: trace a backend behavior bug from source file to test anchor without guessing from filenames only

Weak answer:

This looks like `api-integration`, so follow the usual checklist and it should be fine.

Why this fails:

- No file path from `public Python service repo with serializer, retry, cache, and session tests` was inspected.
- No symbol such as `SessionManager` was confirmed.
- No proof surface was named for `session`.
- It blurs verified evidence and inference, which is exactly how overclaim slips back into Relay-kit.

Correction:

Name the concrete path, inspect or search it, state what is verified, and leave unverified claims labeled until a gate proves them.
