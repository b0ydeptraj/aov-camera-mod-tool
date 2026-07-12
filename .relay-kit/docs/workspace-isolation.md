# workspace-isolation

Use workspace isolation when implementation needs a clean branch, risky experimentation, or parallel execution across lanes.

## Default expectations
- Prefer isolated worktrees or equivalent isolated branches for multi-lane work.
- Verify the isolation directory is ignored before writing into it.
- Run project setup and baseline verification before implementation begins.

## Safety checks
- Do not start feature work on the main branch by accident.
- Do not treat a dirty or failing baseline as a green light for new implementation.
- If baseline verification fails, record the failure before proceeding.

## Used by
- team
- developer
- review-hub
