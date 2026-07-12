# dependency-management Weak Output Anti-Example

Request: review a dependency drift report, compare manifest to lockfile, and name rollback or pin evidence before recommending an upgrade

Weak answer:

This looks like `dependency-management`, so follow the usual checklist and it should be fine.

Why this fails:

- No file path from `public package repo with package manifest, lockfile, dependency policy, and upgrade notes` was inspected.
- No symbol such as `resolveDependencyPlan` was confirmed.
- No proof surface was named for `dependency drift`.
- It blurs verified evidence and inference, which is exactly how overclaim slips back into Relay-kit.

Correction:

Name the concrete path, inspect or search it, state what is verified, and leave unverified claims labeled until a gate proves them.
