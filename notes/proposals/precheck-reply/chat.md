# The chat's own idea (written before the helpers)

1. Add `propose.py check` that reads a draft reply (from a file or stdin) and prints the same faults the Stop hook would.
2. A line in CLAUDE.md, Messages to me: any reply that asks Sam a numbered question is run through the check first.
3. Narrow the checker so a question about what Sam meant, or whether to start the route, is not a change approval
   (e.g. "start the process" / "did you mean" pass), each tested against the logged lines in unrouted.md.
Lost: nothing Sam sees. Added: one step per question-carrying reply.
