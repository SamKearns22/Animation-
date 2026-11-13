# Cost diagnosis job (Sam, 13 Nov): why each step got expensive, and how to make it cheap AND good

## Where things stand (the ONE handover)
- **Rules that bite next:** 85 (cost watch), 24 (estimates from real costs), 74.
- **Done (13 Nov, cost job chat 1 of 8, Opus high): Job A.** The record now holds the app's real figures (below).
  Fixed: the Stop hook's ledger push from a detached copy now goes to the chat's own branch `claude/chat-XXXXXXXX`
  (tested); rows carry the app session id so a real figure is never overwritten by an estimate.
- **Next: chat 2 of 8, Opus high: Jobs B then C.** Measure with `list_events` filtered (`kinds=["result"]` for
  modelUsage; `["assistant"]` pages for what each step did), never whole transcripts: chat 1 hit amber at ~150k
  history just from 45 `get_session` calls (1.7k tokens each). Hand over before 200k.
- **Needs Sam:** nothing until Job C's numbered Y/N message.
- **Read:** this file only; `notes/ledger/app-costs.tsv` for the numbers.
- **Open rule requests:** none.
- **For Claude:** `python3 source/ledger.py app` rebuilds film rows from `notes/ledger/app-costs.tsv` (one line per
  chat: film, session id without `session_`, created, title, cost_usd, cache read M, cache write M, output k, history
  k, model). To add a chat: `get_session` it, append a line, run `ledger.py app`. Blessed keeps 6 estimate rows (11 Nov,
  chats not in the app: earlier account) marked keep.

## Job A results (13 Nov, real app figures, list $; % of a week at WEEK_USD 290)
- **Blessed 44.7%** (16 chats from the app $93.6 = 32.3%, plus 12.4% estimated for 11 Nov chats the app cannot show);
  estimate 19%. Chat 5 alone $27.73 (9.6%). **Remakes 30.4%** in the app (19 chats from 10 Nov; the old ledger's
  "45% from Sam's meter" was the whole week's meter, not this film). **Protest Tiers 8.5%** so far (7 chats incl.
  framing research and sketches; plan and research only).
- **Where an Opus chat's money goes** (36 Opus chats, $176, prices fitted to the app's own figures: re-read $0.22/M,
  write $6/M, output $20/M): **re-reading history 49%, writing new history 27%, output 22%.** 26 of 36 Opus chats ended
  at 200k+ history and cost $158 of the $176; the 10 that stayed under 200k cost $18.
- **Sonnet is ~50x cheaper per routine stage:** 6 Sonnet chats (animatics, finals) cost $2.80 in all ($0.13-0.97 each);
  Opus chats that rendered animatics cost $5-28 (Blessed chats 3 and 5, Remakes "animatic completion" $6.50).
- Typical Opus film chat: $4-8 (1.5-3% of a week), ending at 200-300k history. A film at 10-15% is about 5-7 such chats;
  Blessed has used 22 and Remakes 19.

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
