# Startup reading job: Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (change 4 as adopted, nothing wider), 85 (cost watch), 19 (filtered printouts).
- **Done (chat 5, Opus medium, 16 Nov):** change 3: `handover.py start --film` prints Where things stand + unticked notes
  (protest-tiers ~1.1k tokens vs ~6.3k); Notes round pack reads it. Kittest `notes_printout_reads_only_open_notes`.
  Billing fix (Sam asked): a chat whose task is under notes/proposals/ is billed to proposal-route, never a film; one chat,
  one ledger (this chat's duplicate 0.4% under the paused film removed). Kittest `process_work_is_never_billed_to_a_film`.
- **Done (chat 6, Sonnet medium, 16 Nov):** change 4's read-only map written: `claude-md-map.md` (every sentence -> rule,
  source fault, date, and which move: R tags to rulebook table, P to packs, K stays). No CLAUDE.md edits.
- **Next (chat 7, Opus, medium):** move the text word for word per the verdict (R: 12 dated tags; P: photo search order,
  the finish.py command, My accounts), each leaving a one-line pointer; add the sentence check (every old sentence found
  word for word in CLAUDE.md, rulebook or a pack, else refuse). Rewording of the 5 duplicates is a later proposal.
- **Needs Sam:** the 3 stranded branches (asked chat 4; answer goes to chat 4): claude/beautiful-brown-vutd0l merge;
  claude/blessed-c2-mics-wip keep off; claude/audit-honest-checker keep off (all three left alone by chat 6).
- **Read:** `notes/proposals/startup-fixes.md` ("Final version", change 4); `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **Sam's two cost-estimate asks (11:20, d675uk2u):** "Is any of this relevant to cost ledgers?" and "your estimates in terms of
  week costs (e.g. 3% of a week) are rarely correct". Chat 6's reading: yes, partly. The ledger lost 7 of 9 checked chats' cost
  rows (change 1), so past estimates were compared with incomplete totals; chat 5's billing fix also stops process chats being
  billed to a film. Whether estimates themselves are off is open: a later proposal (after change 1) compares the last films'
  estimates with complete ledger totals. Tell Sam at the next message.
- **For Claude:** shallow copy: fetch, `git checkout -B` the main line. Review list (not asked): job-packs line 32; the
  overnight rule now after the process check; UNROUTED 10:08 was a budget Y/N (Sam told). Failing before chat 5, untouched:
  kittests people_from_a_description, facehouse_whole_head (protest_tiers_cast uses the kit before Sam's OK).
