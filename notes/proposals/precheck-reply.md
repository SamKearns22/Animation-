# Proposal: Sam sees a message twice when the proposal checker blocks after sending

Status: open

## Problem
When the proposal checker (the Stop hook in source/propose.py) decides a reply asks Sam to approve an unjudged change,
it blocks only after Sam has already seen the reply. The chat must then write again, so Sam gets the same message
twice (or a near copy). Sam, 22 Nov: "You keep sending me messages twice." Some blocks were also on questions that
were not change approvals (a question about what Sam meant; a question whether to start the route itself), so each
false block costs Sam a duplicate message and the chat extra steps.

## Facts
- The checker runs as a Stop hook: after the reply is written and shown (.claude/settings.json, "Stop"; propose.py hook()).
- On a block the chat must answer again; on a second fault it lets the reply through and logs it
  (notes/proposals/unrouted.md): 43 such lines, 15-22 Nov (counted). Blocks that were fixed on the first resend are
  not logged anywhere (unchecked how many).
- This chat (session 56d8e5c4, 22 Nov): blocked twice. Once on "did you mean every film or a normal-size film"
  (a question about Sam's own request), once on "should I start the suggest-and-judge process on way 1" (a question
  about running the route, not approving a change). Both resent; Sam noticed the doubles.
- Sam's rule added 22 Nov (CLAUDE.md, Messages to me): after a block, resend only the changed line.
- reply_faults(reply, touched) already exists as a plain function (propose.py ~line 391); only hook() calls it.
- Statement One (CLAUDE.md top): quality within 15% of a week; cost down by catching faults before Sam sees them.

## Record
source/propose.py
.claude/settings.json
notes/proposals/unrouted.md
CLAUDE.md
guides/proposal-route/
