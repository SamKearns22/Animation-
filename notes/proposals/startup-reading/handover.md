# Startup reading job: Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (change 4 as adopted, nothing wider), 85 (cost watch), 19 (filtered printouts).
- **Done (chat 5, Opus medium, 16 Nov):** change 3: `handover.py start --film` prints "Where things stand" and the
  unticked notes (`- [ ]` lines; table rows under a "done?"/"status" column not marked done); carried() still checks
  the whole file. On protest-tiers: ~1.1k tokens printed against ~6.3k for the file. Job pack "Notes round" now reads
  the printout, not the file. Kittest `notes_printout_reads_only_open_notes`. Changes 1-2 done in chat 4.
- **Next (chat 6, Sonnet, medium):** change 4's read-only map of CLAUDE.md: every sentence -> its rule, its source
  fault and its date, written to notes/proposals/startup-reading/claude-md-map.md; no edits to CLAUDE.md. Then open
  chat 7 (Opus, medium) to move text word for word per the verdict (with the sentence check).
- **Needs Sam:** the 3 stranded branches (asked 16 Nov, chat 4; his answer goes to chat 4): (1)
  claude/beautiful-brown-vutd0l merge; (2) claude/blessed-c2-mics-wip keep off; (3) claude/audit-honest-checker keep off.
- **Read:** `notes/proposals/startup-fixes.md` ("Final version", change 4); `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **For Claude:** main was rewritten once and this copy is shallow (fetch, then `git checkout -B` the main line). Not
  asked, list at review: chat 5 also changed job-packs.md line 32 (Notes round reads the printout).
