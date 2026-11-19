# Helper B: what every check catches

## Leak
The title and the Problem give the answer ("record what every check catches ... whether Sam would have seen the fault"). Weighed below as one option, not taken as given.

## Results
- Code checks have saved nothing anywhere: `checks` is {} in all 27 `notes/ledger/*.json` (counted). All 15 round files under `notes/ledger/*/round-*.txt` hold only critique entries; none comes from a code check (every "== " header is "critique").
- Why it saves nothing: `ledger.record()` returns quietly when `current()` finds no `notes/ledger/.current`. That file is written only by `ledger.py round` and never reaches GitHub (absent here). The kittests make their own `.current` in a temporary folder (`source/kittests.py` 969-970, 2679, 2872), so they pass while real chats save nothing.
- `quick_checks` keeps only a total per run: Milburn 14 runs, Protest Tiers 13 (ledgers, checked).
- The critic already has a usable catch record: per rule line, faults and false alarms (Milburn 25 lines, Protest Tiers 32, Blessed 26; ledger `critique.lines`).
- Sam's notes are not recorded either. `notes` is 0 in every chat row of every ledger, yet Milburn's notes table has numbered notes 1-11 plus one on the final (`notes/archive/milburn.md`). Notes are counted only if a chat types `ledger.py log --notes N` (`source/ledger.py` 820), and none did. So the result the rule cares about, notes reaching Sam, has no number, and misses (notes a check should have caught) cannot be counted.
- What a check costs a chat is not measured. The ledger's step kinds have no "checks" kind; "other" is 21.6 of Milburn's 32.4% (ledger). That is a gap.
- Past films can be measured now. `notes/proposals/learn/late-faults-replay.md` re-ran today's pre-flight on the code each Protest Tiers chat left, read-only. There are 64 archived Protest Tiers, Milburn and Blessed branches (`git branch -a`).

## The real decision
Can the retire rule be followed now, for the checks that exist, across the last three films and every film after? A counter only answers it three films from now. Two bigger levers: the missing outcome measure (Sam's notes, and which check should have caught each), and replaying past films so that no one has to wait.

## Root cause
The catch record was hung on a manual step (`ledger.py round`) whose marker file lives only inside one container. Each chat is a fresh container, so every real run fails, and fails silently. The tests fake the marker, so nothing noticed. Sam's notes count is a second manual typed step that no stage enforces.

## Approaches weighed
1. **Fix the counter** (the frame given). Each check run saves to the film's ledger with no round needed. This gives evidence only after three more films, and none on misses.
2. **Reframe: measure from Sam's end.** Each note from Sam (and each critic fault) is tagged with the check that should have caught it, or "none". A check's worth is what it stops reaching Sam; a check that never matches anything is a retirement candidate.
3. **Learn first: replay.** Run every current check on the archived code of Protest Tiers, Milburn and Blessed. For each fault, mark whether it was gone before the animatic Sam saw. Tag the three films' notes as in 2. This gives three films of evidence now and changes nothing.
4. Switch one check off per film and watch the notes. Rejected: it lets faults reach Sam on purpose.

Chosen: 3 first, then 1 and the recording half of 2, as separate changes.

## Proposal
**Learn (read-only, first, alone):** one Sonnet chat per film, with today's checks on each building chat's branch. Output is one table: check · runs · faults it listed · faults gone before Sam's animatic ("removed before Sam") · Sam's notes it should have caught ("missed") · could not test. Whether Sam would have noticed a removed fault cannot be measured without removing the check; this step marks it "would have been on screen at phone size: yes / no" from the animatic frame and calls it a proxy. Job 1 uses this table.

**Change 1, the counter that always saves.** Each check run writes to the film's ledger, naming the film from the run itself. A line is printed if it cannot save. `handover.py end` refuses when pre-flight ran (quick_checks grew) but `checks` stayed empty. A kittest runs it on a fresh copy with no marker file. Number to beat: on the next film, every check pre-flight runs has a row, with runs equal to the quick_checks count (today: 0 rows against 14 runs).

**Change 2, Sam's notes counted and tagged.** `handover.py end` counts the numbered notes from Sam in the film's notes table, writes them to the ledger, and asks for a "should have caught: CHECK / none" tag on each one. It refuses an untagged note. Number to beat: the ledger count equals the table (Milburn: 0 against about 12).

Cost: learn about 1-2% of a week per film, so about 3-5% once (unchecked; filed as tool work, not film work). Changes 1 and 2: about 1.5% and 1% once, then near 0 per film. Against 15% per film: no added film cost.

What Sam would notice: one table before job 1 asks him to retire anything, and "Lost:" lines that name a check's catches and misses in three films.

## Sam test
Q1 Expert: yes. Measure the outcome (misses) as well as the activity (catches), and replay before waiting.
Q2 Best result: yes. Three films replayed beats waiting for three more; one film alone is too narrow.
Q3 Comprehensive: yes. Root cause fixed (no marker file), enforced by handover refusals, and a fresh-copy test.
Q4 Most intelligent: yes. Four different routes weighed; the counter alone was the weakest.
Q5 Risk: low. The learn step changes nothing; each change is undone alone; nothing is retired here.
Q6 Checked: yes. Sources named; costs and the proxy are marked.
Q7 Not the cheap version: yes. The cheap version (counter only) gives no misses and no evidence for three films.
Q8 Nothing temporary: yes. The replay is a one-off reading; both changes are permanent and reviewed at the film's end.

## Lost / Added
Lost: nothing. Added: a one-off replay table; a ledger row per check; one tag per note from Sam at handover; two handover refusals.

## Unchecked
Replay cost per film; whether today's checks run on older code (the late-faults replay hit "could not test"); exact note counts for Protest Tiers and Blessed; what a check costs per chat.
