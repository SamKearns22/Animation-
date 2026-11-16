## Leak
yes: mild. The Facts point at one remedy ("Whether a span clip also runs clipcheck/audit: unchecked. Chat 29 found a span check by hand ... about 5 s a tier"), which anchored V3 and was weighed by V2. The problem file also carries a wrong fact the helpers leaned on: "a span clip ... runs the picture checks". It does not: source/film_engine.py 196-215 sets `lock = not span`, and `check` (the picture checks) is only switched on under `lock`, so a span clip runs no checks at all (V1 caught this; V2 repeated the wrong claim as "checked"; V3 built on it). It also names rule 24 for phone-size Glimpses; that is rule 89 (rule 24 is the estimate).
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 4 | 20 |
| V2 | 4 | 4 | 4 | 3 | 4 | 19 |
| V3 | 3 | 3 | 3 | 2 | 4 | 15 |
## Sam test
Q1: Yes. A top agent-workflow expert moves the machine check to the exit of the chat that wrote the code (the code is still fresh, no second start-up) and measures on real commits before changing the system; that is the pick. They would also make the check's inputs exist early and fix the tool fault (film name vs code name) that stopped the check running at all; both are in.
Q2: The replay runs today's quick check on the code as each Protest Tiers build chat left it (branches claude/protest-tiers-c13 to c31 exist, checked) and on Blessed's last two build chats where their code can be found (unchecked). That is the whole film's build chats plus a second film, not one chain.
Q3: Root cause found with evidence: no build chat ever ran a machine check (stills and span clips check nothing; handover.py end runs no film check, checked), the checks lacked their inputs (44 faults, mostly undeclared lists), and the tool could not even be called by the documented name until chat 28. Enforced by the mandatory handover check, not by a chat choosing to read a rule; `start` reports a skipped `end`. Paper compliance (naming every fault in Exceptions instead of fixing) is counted per chat and shown at the film's end. Eye-only faults (phone-size reading, chain 1) are not caught by this: named.
Q4: Six approaches weighed: exit gate, checks inside span clips (V3), critique after every step, tool tests first, declare lists at plan, fewer longer chats (rejected: history is ~49% of a chat's cost). The exit gate is the one point every build chat passes through.
Q5: The first yes changes nothing (a measurement). Each change after it is its own yes with its replay number, one flag each, undone alone. Risks: false faults breeding waivers (counted); a chat at amber spending more fixing before it hands over (red still hands over, faults listed first).
Q6: Checked: span clips run no checks; handover.py end runs no film checks; build branches exist; only critique.py maps protest-tiers to protest_tiers (preflight and finish do not); fix-only gate chats 17, 18, 29, 30 = 1.78+1.6+2.24+2.36 = 8.0%. Unchecked: the saving per film, kittests' run time, whether old branches run under today's tools, Blessed's causes.
Q7: Sized to the result (no gate-only fix chats; under 10 faults first found at the gate, against 107 and 44), not to the price; the declaration step and tool tests are included where the replay shows they matter, not dropped to save.
Q8: Nothing temporary: the replay is a measurement, each change is made properly once its number supports it, and reviewed against the next film's results at its end.
## Pick
V1
## Why
V1 has the right unit (every build chat's exit, across the whole film), the only correct reading of the span-clip code, a learn-first replay that decides each change by number, and covers shared-tool faults (chain 5) with tool tests. V2 is nearly as good but states a wrong fact as checked and leaves tool tests out. V3 bundles three changes into one yes, rests on the span clip already running checks (false), invents a 40 px floor nobody measured, and relies on a rule sentence a chat must choose to follow.
Taken from V2: the name mapper (one film name for every tool, so the check can run at all), Blessed in the replay, and the plan-stage declaration change as its own gated yes. Taken from V3: at plan end the quick check runs once on the near-empty film, so shared-tool crashes show on day one (part of the declaration change).
## Faults in the pick
- F1 [fixed] V1 left the hyphen/underscore name fault standing, which is what stopped the quick check running until chat 28: the mapper is now part of change 1.
- F2 [fixed] V1's evidence was one film: Blessed's last two build chats added to the replay.
- F3 [fixed] V1 left undeclared lists to the gate's first run: the plan-stage declaration step added as change 3, gated on the replay showing COULD NOT TEST hid faults.
- F4 [named] Eye-only faults (does it read at phone size, chain 1: 15 of 21 in hunt 1) are not caught by a machine check unless the readability check's inputs exist; change 3 helps, the rest waits on the replay's split.
- F5 [named] Stopped drawings (the black frames, chain 4) show only in a drawing pass, not the quick check; chat 31's own proposal ("a stopped drawing never ships") covers it and is separate.
- F6 [named] The saving per film (estimated 4-8% of a week) is unmeasured; old branches may not run under today's tools (then the replay runs each branch's own tools and says so).
## Final version
**Learn first (changes nothing; Sonnet; about 1% of a week, filed as tool work).** Run today's quick pre-flight (`preflight.py protest_tiers OUT --text`) and kittests on the code as each Protest Tiers build chat left it (c13, c15-17, c21-26), and on Blessed's last two build chats if their code can be found. Output, one table: each gate fault, the chat that made it, whether a machine check could see it at that chat's end, its kind, and the check's run time. Plus: how many faults hid behind COULD NOT TEST, and how many came from shared tools.

**Change 1, only if at least 60% of gate faults were visible at build end (Opus medium, about 1.5%).**
- One film name for every tool: pre-flight, finish.py, critique and the ledger all accept `protest-tiers` or `protest_tiers`.
- `handover.py end` runs the quick check whenever this chat changed the film's code. Each fault is fixed, or written in Exceptions with a reason, before the handover goes; an undeclared list counts as a fault. At red budget the handover still goes, faults listed first. `start` reports a chat that skipped `end`. Fixed and named counts go to the ledger.
- Number to beat: under 10 faults first found by a chat that did not build them (was 107 and 44); no gate-only fix chats (was 4, 8.0% of a week).

**Change 2, only if the replay shows shared-tool faults reached the film (about 0.75%).** `handover.py end` runs kittests when a shared tool changed in this chat. Number to beat: no film chat spent on a shared-tool fault (was chat 18, parts of 17, 28, 29).

**Change 3, only if the replay shows COULD NOT TEST hid faults (about 0.5%).** The film's file starts from a template holding every list pre-flight reads; the plan chat runs the quick check once on it, so tool crashes and missing lists show on day one. Number to beat: no "declare" faults at the first gate (was most of 44).

Each change is its own yes, one flag, undone alone; reviewed at the film's end against the next film's ledger.
## For Sam
### Option 1: Check before handing over, measured first
Most of the costly fix chats on Protest Tiers (about 8% of a week) were spent fixing mistakes the computer's own checks would have spotted, but the checks only ran several chats later. First, a cheap test run (about 1% of a week, changes nothing) replays the checks on the code each building chat left behind, to see how many mistakes were catchable then. If most were, every building chat must run the checks and fix what they find before it hands over, while the work is still fresh. You would notice animatics arriving sooner and fewer "frames missing" style notes.
Lost: a building chat can no longer hand over with mistakes the checks can see (it still can at the red cost warning, listing them first).
Added: about a minute of checks at each building handover, the test run first, and up to two follow-on fixes (tool self-tests, setting up each film's check lists on day one), each asked separately with its numbers.
### Option 2: Checks on every quick clip
Every short movement clip a building chat makes would also run the jumping-hands and walking-through-people checks for those seconds, and each film would start with its check lists ready. Faults would show the moment a move is made, but only on the moments that get a clip, it relies on each chat making the clips, and three changes would be asked in one yes before anything is measured.
Lost: nothing you see; each clip takes 10-30 seconds longer.
Added: a fault line on every clip, a starting template for each film, and a minimum size for things in quick glimpses.
