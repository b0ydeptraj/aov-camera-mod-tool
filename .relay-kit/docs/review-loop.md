# review-loop

This overlay hardens review handling without adding a second review hub.

## Requesting review
- Ask for review after a meaningful slice, not only at the very end.
- Give the reviewer bounded context: artifact, diff, requirements, and expected behavior.

## Receiving review
- Verify feedback against codebase reality before applying it.
- Handle one review item at a time when it changes code or scope.
- Push back with technical reasoning when feedback is incorrect or out of scope.

## Completion gate
- Review feedback does not override verification evidence.
- If review exposes planning or debugging gaps, route back through the appropriate hub explicitly.
