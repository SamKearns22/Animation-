# Helper B: what every check catches

## Leak
The title and the Problem give the answer: record what every check catches. Treated here as one option.

## Results
- Code checks have saved nothing. `checks` is {} in all 27 `notes/ledger/*.json`, and all 15 round files `notes/ledger/*/round-*.txt` hold only critique entries (counted).
- Cause: `ledger.record()` returns quietly without `notes/ledger/.current`, written only by `ledger.py round`, never on GitHub. Kittests make their own (`source/kittests.py` 969-970, 2679, 2872), so they pass.
- `quick_checks` keeps fault totals only: Milburn 14 runs, Protest Tiers 13 (ledgers).
- The critic already keeps a per-line record of faults and false alarms: Milburn 25 lines, Protest Tiers 32, Blessed 26 (`critique.lines`).
- Sam's notes are not counted: `notes` is 0 in every chat row of every ledger, though Milburn has notes 1-11 plus one on the final (`notes/archive/milburn.md`). Only a typed `ledger.py log --notes` counts them (`ledger.py` 820); no chat typed it. So misses cannot be counted.
- What a check costs a chat is not measured (no "checks" step kind; "other" is 21.6 of Milburn's 32.4%).
- Past films can be measured now: `notes/proposals/learn/late-faults-replay.md` re-ran pre-flight on each chat's branch, read-only; 64 such branches exist for the last three films.

## The real decision
Can the retire rule be followed now, for today's checks, across the last three films and every film after? Bigger levers than a counter: the missing outcome measure (Sam's notes tagged with the check that should have caught each) and replaying past films.

## Root cause
Catches were tied to a manual step whose marker file lives in one container. Every chat is a fresh container, so every run failed silently, and the tests faked the marker. The notes count is a second unenforced manual step.

## Approaches weighed
1. Fix the counter (the given frame): evidence only after three films, nothing on misses.
2. Reframe, from Sam's end: tag each note from Sam with the check that should have caught it. A check's worth is what it keeps from Sam.
3. Learn first, by replay: run today's checks on the archived code of the last three films and tag their notes. This gives three films of evidence now.
4. Switch checks off per film: rejected, it lets faults reach Sam on purpose.

Chosen: 3, then 1 and 2 as separate changes.

## Proposal
**Learn (read-only, alone, first):** one Sonnet chat per film. It makes one table, one row per check:
- runs
- faults listed
- faults gone before the animatic Sam saw
- Sam's notes it should have caught (misses)
- could not test

"Would Sam have seen it" is a proxy: visible at phone size in the animatic frame. Job 1 uses this table.

**Change 1: a counter that always saves.**
- How it works: each check run saves under the film it ran on, and prints a line if it cannot save.
- Enforced: `handover.py end` refuses if pre-flight ran but `checks` is empty, and a kittest runs on a fresh copy with no marker file.
- Number to beat: every check pre-flight runs has a row on the next film, with runs equal to quick_checks (today, 0 rows against 14 runs).

**Change 2: notes counted and tagged.**
- How it works: `handover.py end` counts Sam's numbered notes into the ledger and asks for "should have caught: CHECK / none" on each.
- Enforced: the handover refuses while a note is untagged.
- Number to beat: the ledger count equals the notes table (Milburn: 0 against about 12).

**Cost:**
- Learn: about 3-5% of a week once (unchecked), filed as tool work.
- Changes 1 and 2: about 1.5% and 1% once, then near 0 per film, well inside 15%.

Sam would notice: "Lost:" lines that name a check's catches and misses.

## Sam test
- Q1 Expert: yes. It measures misses, not only activity, and replays rather than waits.
- Q2 Best result: yes. Three films now, not later.
- Q3 Comprehensive: yes. Root cause fixed; handover refusals; fresh-copy test.
- Q4 Most intelligent: yes. Four routes were weighed.
- Q5 Risk: low. Learning changes nothing, each change undoes alone, and nothing is retired here.
- Q6 Checked: yes. Sources named; costs and proxy marked.
- Q7 Not cheap: yes. The counter alone gives no misses and no evidence for three films.
- Q8 Nothing temporary: yes. Replay is a reading; changes permanent, reviewed at film end.

## Lost / Added
Lost: nothing. Added: a replay table, a ledger row per check, a tag per note from Sam, and two handover refusals.

## Unchecked
Replay cost; whether today's checks run on older code ("could not test" in the late-faults replay); note counts for Protest Tiers and Blessed; what a check costs per chat.
