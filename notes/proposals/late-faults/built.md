## Built (chat 8, 16 Nov, Sam's 1; change 1 only)
- One film name: preflight (import and notes file), finish.py (load_film), critique (`_last` compares names with - and _
  alike: the fault that kept pre-flight from reading the critique), rough (story files) accept `protest-tiers` or
  `protest_tiers`. page.py and ledger already did.
- `handover.py end` now runs the quick check (`preflight.py FILM OUT --text`, ~80 s on Protest Tiers) on every film whose code
  this chat changed (uncommitted, or on this branch and not yet on the main line: so `end` runs before the main-line push).
  Each fault is listed FIRST as "QUICK CHECK film: ..." and must be fixed or waived in the notes' "## Exceptions" (pre-flight
  drops waived ones); COULD NOT TEST counts as a fault; the count goes to the film's ledger (`quick_checks`). At red the
  handover still goes, these listed first. `end` stamps notes/logs/handover-end.log; `start PARENT` says when the parent has
  no stamp.
- Test: Protest Tiers' code as chat 26 left it (branch claude/protest-tiers-c26), today's tools: `end`'s check found the film
  changed and listed **107 faults (62 teleports, 11 pass-throughs, 34 other)**, the same 107 chat 28 found at the gate.
- Number to beat (next film): under 10 faults first found by a chat that did not build them (was 107 and 44); no gate-only
  fix chats (was 4, 8.0% of a week). Changes 2 and 3 not built (each its own yes, after the replay's split).
