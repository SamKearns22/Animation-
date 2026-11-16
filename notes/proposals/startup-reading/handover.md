# Startup reading job: Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (changes 3-4 as adopted, nothing wider), 85 (cost watch), 19 (filtered printouts).
- **Done (chat 4, Opus medium, 16 Nov):** change 1: cost rows and Sam's saved messages go straight onto the main line
  (own commit, only those files); 18 stranded rows gathered, `ledger.py audit` 0 missing; kittest
  `cost_rows_reach_the_main_line`. Change 2: start hook lists only branches with work the main line lacks (3 lines,
  ~0.1k tokens, was ~2.0k); `handover.py end` refuses an unnamed one; CLAUDE.md line updated; Sam logs 5t3vj4eb and
  phxjozvs merged; kittest `branch_printout_lists_only_real_work`. Handed over at amber.
- **Next (chat 5, Opus, medium):** change 3 (notes printout: `handover.py start --film` prints "Where things stand" and
  the unticked notes; carried() still reads the whole file), with a kittest, pushed and checked; then open chat 6
  (Sonnet, medium): change 4's read-only mapping of CLAUDE.md.
- **Needs Sam:** the 3 stranded branches (asked 16 Nov, chat 4): (1) claude/beautiful-brown-vutd0l, the slurp profile
  picture: pick merge; (2) claude/blessed-c2-mics-wip, Blessed WIP source/blessed.py: pick keep off; (3)
  claude/audit-honest-checker, 12 Nov audit, 16 files incl. CLAUDE.md: pick keep off. His answer comes back to chat 4.
- **Read:** `notes/proposals/startup-fixes.md` ("Final version", change 3); `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **For Claude:** main was rewritten once and this copy is shallow: merged-ness is judged by blob content
  (source/branches.py); fetch uses --shallow-since. Not asked, list at review: Sam's message log also goes via
  mainline.to_main (it stranded the same way); gather keeps non-row keys as main has them (first run revived Blessed's
  alarms_off; put back at once). The ledger .md merge keeps ours until the next row rewrites it.
