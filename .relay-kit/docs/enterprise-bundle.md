# enterprise-bundle

The `enterprise` bundle is the paid/team governance profile.

It starts from the baseline runtime and adds the full discipline utility set, including `test-first-development`.

## Included Control Surface

- all layer-1 orchestrators
- all layer-2 workflow hubs
- all role specialists
- all utility providers
- all native support skills
- all discipline utilities
- all artifact contracts used by baseline
- all support reference templates
- discipline docs for planning, workspace isolation, review, branch completion, and parallel execution

## Intended Use

Use `enterprise` when a project needs stricter repeatability, cross-session handoff, release gates, policy checks, and test-first implementation discipline by default.

Use `baseline` when onboarding speed matters more than installing every discipline utility.

## Operating Rule

Enterprise installs should be followed by:

```bash
relay-kit doctor /path/to/project
relay-kit manifest write /path/to/project
relay-kit upgrade mark-current /path/to/project --bundle enterprise --adapter codex
```

For multi-adapter teams, repeat `--adapter` or use `--adapter all` in the marker command.
