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
