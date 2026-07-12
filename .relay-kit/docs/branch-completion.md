# branch-completion

Branch completion is an operational discipline, not a separate orchestration layer.

## Required order
1. Run the verification command that proves the branch is ready.
2. Decide whether the outcome is local merge, PR, keep branch, or discard.
3. If the branch will be integrated, re-check tests on the integration target when needed.
4. Clean up the isolated workspace only after the chosen integration path is explicit.

## Red flags
- No completion path without fresh verification evidence.
- No discard path without explicit confirmation.
- No hidden cleanup that destroys a recoverable worktree or branch.
