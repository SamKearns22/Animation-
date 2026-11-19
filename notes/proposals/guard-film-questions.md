# Proposal: The guard stops plain film questions as if they were system changes

Status: parked (Sam 19 Nov: "just the communication problem for now"; packed, helpers not run)

## Problem
The guard (the Stop hook in source/propose.py: a script that reads each reply before Sam sees it and sends it back
once if it asks Sam to approve a system change that has not been through the proposal route) stopped questions about
the film itself on Milburn: whether to close the props stage, which recording was "Report", whether to lower effects
while someone speaks. Each cost a re-send and taught chats to word around it. It must keep stopping real system asks.
Milburn review section 1 item 10, lesson 6; Sam (19 Nov): "fix and test".

## Facts
- notes/proposals/unrouted.md (each line is a reply the guard stopped once and then let through) lists five Milburn
  blocks: 2026-11-17 20:07 estimates (missing Critiqued line: a true catch); 23:56 "Close the props stage and let the
  1am run carry on?"; 2026-11-18 06:11 "Shall I update the stale test so it knows you approved those two tools?" (a
  true system ask); 08:57 "was the file called "Report" the opening line"; 08:59 "should I lower the effects only while
  someone is speaking". The review counts four as film questions; by its own notes three are (unchecked which is right).
- 19 Nov blocks in the same file: 8 more, from chats 60c7e293, 86bc5e6a, 87a9ac49, 689989ae (some are system asks,
  some questions about what Sam meant: "did you mean 1 or 2?").
- How the guard decides: source/propose.py lines ~361-416 (ASK_RE, CHANGE_RE, ROUTINE_RE, questions, is_change,
  reply_faults). "stage", "file", "effects" are not change words; the context-lines rule (a change word in the six
  lines above plus an action verb like "run", "make", "change") is the likely trigger (unchecked per message).
- The last widening: notes/proposals/guard-holes.md (15 Nov) and its probe notes/proposals/guard-holes/probe.py (12
  change questions, 10 routine). Kittest proposal_route_hook in source/kittests.py.
- A separate proposal (plain-check, 19 Nov) may also change what the guard reads in a change ask.

## Record
source/propose.py
source/kittests.py
notes/proposals/unrouted.md
notes/proposals/guard-holes.md
notes/proposals/guard-holes/probe.py
notes/proposals/milburn-review.md
notes/ledger/sam/
