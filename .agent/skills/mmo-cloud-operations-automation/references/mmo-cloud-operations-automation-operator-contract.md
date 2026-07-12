# mmo-cloud-operations-automation Battle Contract

Primary role: mmo-cloud-automation
Layer: layer-4-specialists-and-standalones
Battle family: mmo-cloud-worker-queue

Use this skill only after the request is anchored to a real artifact, repo area, or explicit missing-context question. The goal is not to sound like an expert; the goal is to reduce ambiguity by tying the answer to files, symbols, commands, docs, logs, or state.

## Concrete Battle Profile

- Repo profile: operator-owned cloud worker repo with queue dashboard, worker pool, dead-letter queue, cost ceiling, and pause control
- First files to inspect: ops/queues.yaml, workers/cloud_worker.ts, logs/dead-letter.json, docs/cloud-worker-runbook.md
- Symbols or named surfaces to confirm: CloudWorker, DeadLetterQueue, pauseQueue
- Evidence terms that should appear in a strong answer: worker queue, queue depth, dead-letter, pause

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
