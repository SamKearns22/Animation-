# Proposal: Every step re-reads the whole chat, and a third of a film chat's steps are spent finding code by hand

Status: adopted (2026-11-16)

## Problem
Sam's aim (15 Nov): cut the cost of every stage of production as far as possible without harming quality. Most of
a film chat's money is not the work itself: every step (even an `ls`) re-reads the whole chat so far, so a chat's
cost grows with how long it runs and how much it pulls into its history, and film chats routinely end at 200-300k
tokens of history. A large share of those steps, and of what they pull in, is finding code by hand (greps, sed
ranges, whole-file reads) in film files and tools. The code finder Sam said yes to on 15 Nov, and the line telling
round chats to use it, have not changed that: in the chats that could be checked it was run 0 times. Quality must not
fall, every film is new (no content reuse), and Sam cannot code, so anything that only works if a chat remembers to
do it has already been shown to fail. The question is which change, to which rule, tool, check or way of running
chats, would cut this cost the most at the lowest risk.

## Facts
- Where an Opus chat's money goes (notes/cost-diagnosis.md "Job A results", 13 Nov; 36 Opus chats, $176, prices fitted
  to the app's figures): re-reading history 49%, writing new history 27%, output 22%. 26 of 36 ended at 200k+
  history and cost $158 of the $176; the 10 under 200k cost $18.
- Per action (notes/cost-diagnosis.md "Job B results"): each action re-reads the whole history; at 215k about 4.7
  cents before it does anything, at 400k about 9 cents. A median Opus film chat is ~78 actions ending ~220k, ~$5.6:
  the app's own ~80k re-read on every action ~25%; start-up reading ~15%; work history (code reads, printouts,
  pictures; 0.5-1.6k per action) ~25%; output ~20%; writes the rest. Most actions add under 2k but pay the full re-read.
- A model change or a long pause inside a chat re-pays the whole history at the write price (cost-diagnosis Job B:
  a switch to Sonnet at 364k cost $1.43; one fallback action at 414k $4.37; costwatch.py: after an hour idle).
- Code searching (notes/proposals/learn/code-search-count.md, counted from 7 chats' own records): 169 of 564 steps
  (30%) were hand code searches (Grep, Read of source/*.py, grep/sed/awk/head on .py), 16-36% per chat; page.py run 0
  times. Six were Blessed chats of 12-13 Nov (before page.py existed: the baseline). The one readable chat after
  page.py was built (Protest Tiers cast chat 5, 14 Nov evening, 2.59% of a week) searched by hand 18 times of 58
  steps, page.py 0. Protest Tiers chats 29 and 31 (15 Nov, other account, unchecked here): 0 runs, 25 and 26 hand
  searches (notes/proposal-route.md). Share of COST (not steps) spent on searching: unchecked.
- What exists now: source/page.py (`FILM show "note words"`: the note's words -> ~40 numbered lines of the functions
  it touches; `find`; a page of every def per film file, about a tenth of the code's words, Blessed 6.7k tokens vs
  ~60k). Rule 61 (guides/film-quality-rules.md) and guides/job-packs.md "Notes round" name it as the one look per
  note ("no greps or sed ranges on film files first"); `handover.py start` prints the same line. None of these
  enforces it; nothing records whether it was used. Whether `show` was used by any chat since Sam's Y on 15 Nov:
  unchecked (those chats are on the other account). Shared tools (source/*.py, not film files) have MAPs in their
  headers (rule 61 is about film files); whether page.py covers tools: it does not (it globs source/FILM*.py).
- Chat sizes: Protest Tiers chats 0-8 ended at 90-300k history (notes/proposals/learn/protest-tiers-costs.md);
  chats 9-32 unchecked. Opus film chats cost 1.3-3.2% of a week each; per-chat cost did not fall after the 13 Nov
  fixes; Protest Tiers took 33 chats, 53.6% against ~20% planned.
- Cost watch (.claude/hooks/costwatch.py, rule 85): amber at 200k history or 3% of a week, red at 300k or 5%; amber
  = finish the step and hand over, red = hand over at once. It acts only at those lines; below them nothing limits
  what a step pulls into history.
- Start-up reading (measured now, characters/4): CLAUDE.md ~3.2k tokens (loaded in every chat), guides/job-packs.md
  ~1.1k, the rulebook ~9.6k (looked up by section). The handover (15 lines) and a film's notes (under 4,000 words)
  are read at start. A new chat in this chain begins at ~80k before its first action (the app's own share).
- Hooks in force (.claude/settings.json): SessionStart setup.sh; UserPromptSubmit and PostToolUse costwatch.py;
  UserPromptSubmit handover.py log; Stop ledger.py auto and propose.py hook. No hook looks at what a tool call reads.
- Earlier attempts that did not land: naming page.py in the job pack (chats 29/31 still searched by hand); the 13 Nov
  "Never again" ideas in cost-diagnosis.md (real-money ledger, budget stop: in force; per-chat cost did not fall).
- LIMIT: chats 9-32 of Protest Tiers (session ids 01Gzna...) cannot be opened from this account.

## Record
notes/cost-diagnosis.md
notes/proposals/learn/code-search-count.md
notes/proposals/learn/protest-tiers-costs.md
notes/proposal-route.md
notes/ledger/protest-tiers.json
notes/ledger/blessed.json
source/page.py
source/handover.py
.claude/hooks/costwatch.py
.claude/settings.json
guides/job-packs.md
guides/film-quality-rules.md
CLAUDE.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 2d121af00d89b713 -->
Who wrote which (hidden from the judge): V1 = helper B, V2 = helper A, V3 = chat. Picked: V1 (helper B). Critiqued: 7 found, 3 fixed, 4 named.

## Leak
yes: the Facts say "anything that only works if a chat remembers to do it has already been shown to fail" and "No hook looks at what a tool call reads", which together point at a hook that blocks hand searches; all three versions land on that same gate.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 3 | 4 | 4 | 5 | 20 |
| V2 | 3 | 3 | 4 | 4 | 5 | 19 |
| V3 | 3 | 3 | 3 | 2 | 4 | 15 |
## Sam test
Q1: Yes, with the improvements below. An agent-workflow expert would first record cost by kind of step in every chat automatically, prove the finder works on past notes, then block at the tool call. That is what the pick does. They would also say plainly that chat count and rework are bigger levers than search (named, and measured by the same ledger fields).
Q2: Two sources, both wide. The ledger records every future chat on either account. A read-only backfill now covers every readable chat (Blessed, Protest Tiers 0-8), so the decision does not wait a whole film. Chats 9-32 stay unreadable (named).
Q3: The root cause has evidence: the finder was named three times in text and ran 0 times. The block acts on every chat with no reading needed. Running `show` and then grepping anyway, or overusing the escape line, appears in the ledger counts and is checked at the end-of-film review.
Q4: Four different approaches were weighed (block, earlier handover, a helper finder, measure first). The two reframes were costed and held back until the numbers exist, not dropped.
Q5: Measuring changes no film. The block needs its own Y, only after the replay shows `show` finds the right code at least 80% of the time. It lets the step through if it errors, has a logged escape line, and is removed by deleting one settings line.
Q6: Every number is sourced. The cost share of searching, the saving, the split between film files and shared tools, and whether the ledger can read per-step usage are all marked unchecked.
Q7: Sized by the result: a block at the tool call, because the cheap fix (a line in the pack) already failed. The cost is stated (~1.5-2% once to measure, ~1% to build). Nothing is built for shared tools until the split shows it is worth it.
Q8: Permanent. The ledger fields and the block (if Sam says Y) stay and are reviewed against the film's results when Sam calls the film complete. The backfill is a measurement, not a provisional change.
## Pick
V1
## Why
V1 is the only version whose measurement is permanent and automatic: every chat's ledger row gets steps, end history and cost by kind of step. That answers this problem, and it also shows whether rework or chat count is the bigger lever (Q2, Q3, Q8). V2's measurement is a one-off study, and it records only search counts. V3 builds the most before anything is measured: it bundles the block, a tool-wide finder and a whole-file ban into one Y, forces a finder never shown to work, and leans on a wrong fact (it says every tool's MAP already exists; only 72 of 247 source/*.py files have one in their first 30 lines).
Taken from V2: a read-only backfill from the readable chats now (cost share, search targets, what fills the ~80k start), so the gate decision does not wait a film. Also V2's gate details: the block is per film file, reads of up to 80 lines are allowed after `show`, `find` and a second `show` always pass, and refusals and allowed reads are logged.
Taken from V3: a logged escape line, so a `show` miss never stalls a chat. Also V3's refusal of whole-file reads of big .py files, kept in change 1 only if the backfill shows it matters. And V3's second number to beat: median round-chat history under 200k.
## Faults in the pick
- F1 [fixed] V1's block allowed only the lines `show` named, so a `show` miss could stall a chat. Now `find`, a second `show`, reads of up to 80 lines and a logged escape all pass.
- F2 [fixed] V1 measured only future chats, which delayed the decision by a film. A backfill from the readable chats is added.
- F3 [fixed] Whole-file reads of big code files add to every later step's cost and were not measured. They are now counted, and blocked in change 1 only if the counts show they matter.
- F4 [named] Whether the Stop hook's transcript holds per-step usage, so cost by kind can be read from it, is unchecked. If it does not, steps and history are recorded and cost is estimated from them.
- F5 [named] A chat can still comply on paper (run `show`, then search by hand within the rules, or overuse the escape). The counts show it; nothing prevents it.
- F6 [named] Searching's share of cost, and the ~4% of a week saving per film, are unchecked estimates. Searches in shared tools are left unblocked until the split is known.
- F7 [named] The bigger levers (33 chats, ~30% of Protest Tiers in rework and critique by title-level count, unchecked) are not fixed here. They are only measured.
## Final version
**Learn (one Y; permanent fields plus one backfill; ~1.5-2% of a week once).**
- `ledger.py auto` (already the Stop hook) adds to each chat's row: steps, history at the end, and cost by kind of step. The kinds are: film-file search, tool search, whole-file .py read, `page.py`, renders, pictures, and other. Each step is charged its own re-read plus what it added times the steps after it. This runs on every chat, on either account, with no chat choosing to.
- A backfill, read only, on Sonnet, from the readable chats (Blessed, Protest Tiers 0-8), written to `notes/proposals/learn/search-cost.md`:
  - (a) searching's share of cost;
  - (b) search targets (film files, shared tools, kits);
  - (c) whole-file reads and their size;
  - (d) what fills the ~80k start;
  - (e) `show` replayed on every note those chats fixed: did its lines hold the lines finally edited?

**Change 1 (its own Y, ~1%; only if film-file searching is at least ~10% of a round chat's cost and the replay hits at least 80%; if the replay misses, `show` is fixed first, as its own change).**
- A before-step hook covers Grep, Read and grep/sed/awk/head/cat on `source/FILM*.py`. Until `page.py FILM show` (or `find`) has run for that film in this chat, it refuses and prints the ready command.
- After that, reads of up to 80 lines, `find` and further `show`s pass.
- If (c) shows they matter, whole-file reads of any .py over 300 lines are refused at any time, with the offset/limit form printed.
- Edits, new files, notes and guides are never blocked.
- `# codelook: ok <reason>` passes and is logged.
- On its own error, the hook lets the step through.
- Refusals, `show` runs, escapes and allowed reads go into the chat's ledger row.

**Numbers to beat (next film's round chats):**
- hand searches under 10% of steps (now 30%);
- film-file search cost at a third of the backfill baseline;
- median round-chat history at end under 200k;
- Sam's notes and repeat notes per round no higher.

**Later, each its own Y, set by the numbers:**
- extend the finder and the block to shared tools, if (b) shows a third or more of searches are there;
- hand over earlier, if the history curve shows it pays.

**Undo:** delete one settings line. The ledger fields stay.

**Estimate (unchecked):** searching is ~15% of an Opus chat's cost. Cutting two-thirds of that saves ~3-6% of a week per film.
## For Sam
### Option 1: Measure, then block hand searching
Every chat would record on its own where its money goes, kind by kind, with nobody needing to remember. A quick look back at past chats would test whether the code finder really finds the right code. If it does, and searching costs enough to matter, a guard would stop a chat from hunting through film code by hand until it has used the finder. There is a logged way round, so work never stalls. You'd notice cheaper fix rounds, and each film's review would show where the money went.
Lost: chats searching film code freely before using the finder (only after a second yes).
Added: cost-by-kind lines in every chat's record, one look back at past chats, and later one guard.
### Option 2: Block it all now
The same guard would go on straight away, with no look back first. It would cover film code and shared tools, and it would ban reading whole big files. It's faster to start, but it forces a finder that has never been shown to work, and the tool-wide part rests on maps that most files don't have yet.
Lost: free searching everywhere at once, plus the proof that the finder works before chats depend on it.
Added: one guard over all code, a tool-wide finder, and search counts in every chat's record.
