# planning-discipline

This overlay imports strong planning discipline without creating a second planning stack.

## Core rules
- Plan from authoritative artifacts first: brief -> PRD -> architecture -> stories or tech-spec.
- Split unrelated subsystems before implementation starts.
- Prefer thin, verifiable slices over broad implementation batches.
- Every story or tech-spec should name the first verification command or evidence expected.

## Task slicing bar
- Small enough to complete in one focused implementation pass.
- Large enough to produce visible progress or meaningful evidence.
- Explicit about dependencies on upstream artifacts.
- Explicit about what will fail if the slice is implemented incorrectly.

## Used by
- plan-hub
- scrum-master
- review-hub when planning artifacts disagree
