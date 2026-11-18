# Helper A: search-first

## Leak
The title names two remedies ("use the finder", "the app's figure"); set aside. Problem (2) also misreads the record: "tool search" in the ledger is not loading tool definitions. In `source/stepcost.py` (kind_of) it is any Grep/Glob/sed/partial Read that does not name the film's own files: shared tools, guides, notes.

## Results
- Milburn: 15 chats, 1,259 steps, 32.14% recorded, all rows "estimate" (notes/ledger/milburn.json). Sam's meter: 22% (problem file). Ratio 1.46.
- The estimate is not a guess at tokens: stepcost reads each step's real usage. The dollars are turned into "% of a week" with one constant, `WEEK_USD = 245`, marked PROVISIONAL in `.claude/hooks/costwatch.py`. If 71% to 93% was all Milburn, the constant should be about 358. That is unchecked, because other work may have run in that window.
- No Milburn session has an app row. Protest Tiers has app and estimate rows, but none for the same session, so the estimate has never been checked against the app chat by chat (protest-tiers.json). That is a gap.
- Hand searches: 248 of the film's own code plus 531 of shared tools, guides and notes. That is 779 search calls in 1,259 steps. The finder was used 12 times (milburn.json, summed).
- Share of cost: "other" (start-up reading, history, Claude's words) is about 67%, tool search 5.27 points, film-file search 2.77 points (problem file; per-chat shares checked in milburn.json).
- The 17 Nov reminder (`.claude/hooks/finderwarn.py`) warns and never blocks. It covers film code only, so the 531 shared-tool searches never trigger it.
- The record cannot split build chats from note rounds: every row is stage "auto", with notes 0 and round null. That is a gap.

## The real decision
How a whole film gets from about 22% (real) to 15% or less, steered while it is made by a figure that matches Sam's meter. Searching is about a quarter of the estimate. "Other" (history, start-up) is two thirds of it and is the bigger lever. So is the number of chats and steps per film.

## Root cause
1. The cost figure is off because a provisional conversion constant was never re-set against the app, and the app import (`ledger.py app`) is not run at handover. The transcript reading is not the cause.
2. Most searching (531 of 779 calls) is chats rediscovering how the shared kit works. For example, facehouse.py was searched 30 times and people.py 27 times across 15 chats. The finder does not cover that question, and nothing gives a chat a map of the kit. Each chat starts cold and pays again. The reminder failed for two reasons: it answers a different question (where a note lives in film code), and it only advises.

## Approaches weighed
- A (reframe: film budget). Real cost is imported at every handover and the constant is re-set. Each chat sees a running film total and a forecast against 15%, broken down by stage.
- B (one look-up for all code). Widen the finder to the shared kit: one command answers "where and how" across the film, the tools and the guides.
- C (hand-carry). Each handover passes the next chat the exact files and lines for every open note, so the chat has no need to search.
- D (learn first). Classify all 779 searches by stage, purpose and repeats (the same function looked up in more than one chat). Pair each Milburn chat's app figure with its estimate.

Chosen: D first, then A, then B or C, whichever D shows matters more.

## Proposal
Learn (changes nothing):
1. Pull the app's figure for all 15 Milburn sessions with get_session and import them with `ledger.py app`. Set each one against its estimate.
2. Re-run stepcost on the 15 transcripts. Label every search with its stage, its target (film code, shared tool, guide, notes) and whether an earlier chat already looked up the same thing.
3. Report how many points repeats cost.

Cost: about 1% of a week, Sonnet.

Change 1 (cost figure, alone):
- Set `WEEK_USD` from the paired data.
- `handover.py end` runs the app import for the chat's own session and refuses to hand over without it. It prints the film's running real total and a forecast.
- Enforced by the handover check, which already runs every chat.
- Number to beat: the ledger is within 5% of Sam's meter on the next film.
- Cost: about 1%.

Change 2 (after the learn result, alone): B if repeated shared-kit lookups are most of the search cost; C if note-round film searches are.
- Enforced by a hook that blocks, rather than warns.
- Number to beat: search points per film halved from 8.04 on Milburn's scale. That is about 2.7 real points.
- Cost: about 2–3% Opus, once.

Honest sum: these cut about 3 to 4 real points. Getting from 22% to 15% needs 7, so the "other" share and chats per film stay the next lever, judged on Change 1's real figures.

What Sam would notice: one cost line in each handover that matches his app, and fewer, shorter chats per film after change 2.

## Sam test
- Q1: An expert measures real cost first, then removes repeated rediscovery, rather than adding more reminders.
- Q2: It covers all 15 chats and all 779 searches, and is checked against Protest Tiers and Blessed.
- Q3: It is enforced by the handover check and a blocking hook, not by a chat choosing to read something. Each change has its own number.
- Q4: Four different approaches were weighed, one of them a reframe and one learn-first.
- Q5: Learning changes nothing. Each change can be undone alone (one constant; one hook).
- Q6: Sources are named; gaps are marked.
- Q7: It is sized to the measured share. It also states plainly that this alone does not reach 15%.
- Q8: Both changes are permanent, made properly, and reviewed when the film is declared complete.

## Lost / Added
- Lost: handover cannot finish without the app import (one step per chat).
- Added: a real running film total; one look-up or hand-carried note map (B or C); a blocking search hook.

## Unchecked
- That 71% to 93% was all Milburn.
- Whether get_session usage is available for every Milburn session.
- The split of build and round searches.
- Which of B or C wins (the learning step answers this).
