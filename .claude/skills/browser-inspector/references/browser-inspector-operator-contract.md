# browser-inspector Battle Contract

Primary role: utility-provider
Layer: layer-3-utility-providers
Battle family: browser-runtime

Use this skill only after the request is anchored to a real artifact, repo area, or explicit missing-context question. The goal is not to sound like an expert; the goal is to reduce ambiguity by tying the answer to files, symbols, commands, docs, logs, or state.

## Concrete Battle Profile

- Repo profile: public frontend repo with login page, Playwright flow, console log artifact, network HAR, and screenshot evidence
- First files to inspect: src/app/login/page.tsx, tests/e2e/login.spec.ts, artifacts/login-console.json, artifacts/login-network.har, artifacts/login-screenshot.md
- Symbols or named surfaces to confirm: LoginPage, loginSpec, ConsoleError
- Evidence terms that should appear in a strong answer: console, network, dom, screenshot

## Working Loop

1. Restate the user task as a verifiable repo action.
2. Name the candidate files before giving advice.
3. Check at least one source file and one proof surface when the task touches code, docs, release, routing, or automation.
4. Separate verified facts, inferred risk, and unknowns.
5. End with the next executable check or handoff, not broad process advice.

## Failure Modes To Block

- Guessing from the skill name without opening files.
- Treating a checklist as proof.
- Saying a change is ready when tests, generated adapters, docs, or safety scans were not checked.
- Hiding that a public repo benchmark is read-only and not user adoption proof.

## Evidence Checklist

- File evidence: cite exact paths or say which anchor is missing.
- Behavior evidence: cite test, static scan, route score, benchmark hit, screenshot, or command output.
- Risk evidence: name residual risk and the smallest next verification.
- Handoff evidence: name the receiving skill or CLI gate when another lane should continue.
