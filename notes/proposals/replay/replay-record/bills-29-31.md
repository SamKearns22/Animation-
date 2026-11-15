# Bills of Protest Tiers chats 29 and 31 (a read-only helper, 15 Nov 19:43; raw counts)

Method (the helper's words): I read all 4 pages of chat 29 and all 6 pages of chat 31 and counted tool calls from the
transcripts. Categories are keyword-classified, so counts are approximate. Cost shares are my estimate only: each
action re-reads the whole history, so cost per call grows with position in the chat. Call-count weighted guesses, not
metered per action.

Chat 29 (92 tool calls, $6.29, Opus; final history 252k tokens)
| Category | Calls | Share of calls | Est. cost share |
|---|---|---|---|
| ls/cat/grep/sed looks at code | 32 | 35% | ~33% |
| Checks (preflight, clipcheck, audit) | 21 | 23% | ~25% |
| Code edits via python heredoc | ~21 | 23% | ~22% |
| Bookkeeping (handover/notes/status) | 11 | 12% | ~12% |
| git commit/push | 3 | 3% | ~3% |
| Renders | ~0 | 0% | 0% |
| Read, ToolSearch, create_session, PushNotification | 4 | 4% | ~5% |
- Start-up: of the first 20 actions, about 12 were git/branch, handover and notes reading, plus code reads. Reads of
  notes, guides or CLAUDE.md: about 11.
- Repeats: 3 identical or near-identical edit/inspect scripts, each run 2 or 3 times. Retries after failure: ~5.
- Helper spawns: 0.

Chat 31 (117 tool calls, $5.78; final history 229k tokens)
| Category | Calls | Share of calls | Est. cost share |
|---|---|---|---|
| ls/cat/grep/sed looks | 32 | 27% | ~27% |
| Renders (including a monitored background render) | 14 | 12% | ~13% |
| git commit/push | 12 | 10% | ~10% |
| Bookkeeping (handover) | 11 | 9% | ~9% |
| Monitor, ReadNotifications, TaskStop (waiting on renders) | 16 | 14% | ~12% |
| Checks | 5 | 4% | ~5% |
| Other (python edits, scratch scripts, 1 Edit) | 17 | 15% | ~15% |
| Read | 4 | 3% | ~3% |
| SendUserFile, create_session, ToolSearch, PushNotification | 6 | 5% | ~5% |
- Start-up: of the first 20 actions, about 9 were git, handover.py start and notes reading. Reads of notes, guides
  or CLAUDE.md: about 19.
- Repeats: tailing the same render output file 5 or more times, plus the same scratch script run twice. Retries ~6.
- Helper spawns: 0.

The real app cost of every Protest Tiers chat so far is in notes/ledger/protest-tiers.md (29 chats).
