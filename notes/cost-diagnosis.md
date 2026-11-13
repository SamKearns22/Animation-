# Cost diagnosis job (Sam, 13 Nov): why each step got expensive, and how to make it cheap AND good

## Where things stand (the ONE handover)
- **Rules that bite next:** 85 (cost watch: it measures a chat, never a film), 24 (estimates from real costs), 74.
- **Done (13 Nov, diagnosis chat, Sonnet then Opus):** found that the cost record is wrong and the process has grown
  (facts below). Sam: Y to rebuilding the record; NO to "a film cap": "recording and alarming is useful but doesn't
  solve the problem: how do we make each step cost-efficient and high quality."
- **Next: chat 1 of 8, Opus high (building new tools and a new plan).** Jobs A, B, C below, in order.
- **Needs Sam:** nothing until the proposals (job C).
- **Read:** this file only; then the parts named in each job.
- **Open rule requests:** none.
- **For Claude:** real per-chat cost = `get_session(...).external_metadata.usage.cost_usd` (list $), plus
  `modelUsage` in the last `result` event (`list_events kinds=["result"]`) for the split by model. WEEK_USD 290 in
  `.claude/hooks/costwatch.py` is the yardstick (an estimate).

## The facts found (13 Nov)
- **The record misses most of the cost.** `ledger.py auto` commits then runs `git push origin HEAD`; the start-up hook
  (`setup.sh` line 23) tells chats to `git checkout --detach`, and a detached `push origin HEAD` fails (tested). A
  chat that ends on Sam's usage limit never runs the Stop hook at all. Blessed chat 5 (13 Nov, session
  ..WX6ZgL6kQ5WZ2nxNH) cost $27.73 (about 9.6% of a week) and has no row.
- **Real costs, 14 Blessed chats visible from 12 Nov 17:10:** $94.80 (about 33% of a week). Earlier Blessed chats are
  not visible from this account (Sam switched accounts 12 Nov). Per chat: $4.4-8.2, one at $27.7; 12 of 14 on Opus.
- **The cost is re-reading.** Chat 5: 92M tokens re-read, 1.3M written, 177k output; chats end at 200-414k tokens
  of history, and every step re-reads all of it. Job E (notes/job-e-measurements.md): a fresh chat is 80k before
  work, a film round reads 40-55k more.
- **The process grew (main line, words):** rulebook 3,034 (28 Oct) -> 5,898 now; kit catalogue 1,845 -> 5,057; tools
  147 -> 229 files; Blessed's own code 48k words in 6 files. New per-round steps since early Nov: pre-flight
  (15-40 min; one run printed 99 faults, mostly noise), critique helpers (2 hunts per stage, 13-17 faults each),
  name test, check sheets, pictures read into the chat. Every step's output stays in the history that each later
  step re-reads.
- **And mistakes still pass, so we pay twice.** The same faults return each round (ball hands, no necks, no thighs:
  "named, not changed"); the Walliams face took about 5 chats; notes 8, 10, 11 were repeats. The checks look at
  stills and poses, not overlaps or movement (note 8: body through the pool table).
- **Models:** animatics 2 and 3 rendered inside Opus chats; chats bundled stages ("tune, clip, animatic 2"), so the
  model-by-stage rule never fired; Sam switched chats 4 and 5 to Sonnet himself.
- **Earlier films:** Ad-Vanced Notice about 10%, Halo 12-15%, Netan-yahoo 12-18% (archive notes).

## Job A: the real cost record (Sam: Y)
Rebuild the ledger from the app's own per-session figures (above), not the transcript estimate or a git push:
Blessed, Remakes, Protest Tiers. Fix the detached-push loss. Small.

## Job B: where each step's money goes (the real question)
For 2-3 Blessed chats (chat 5, round-2 chat 2, chat 2 of 8 on 13 Nov) and one cheap older film's chats if visible,
split the cost by step: start-up reading, film code reads, pre-flight, critique helpers, pictures, renders waited on,
rework of a repeated fault. Name the 3-5 steps that cost most and whether each ever caught a fault Sam would have
named (the ledger's critique lines, notes tables).

## Job C: proposals for Sam (one message, numbered, Y/N)
Make each step cheap and good: cut or shrink steps that cost much and catch little; keep chats small (one stage
each, on its model); reuse before re-reading; checks that test what Sam actually notes (overlaps, movement,
repeats). Each proposal: what it saves (in % of a week, measured), what it risks, the rule or tool it replaces
(CLAUDE.md: the rulebook never grows). Target: a film in 10-15% again.
