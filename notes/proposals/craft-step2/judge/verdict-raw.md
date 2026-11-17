## Leak
yes: the facts carry the adopted plan's branch ("if plan faults dominate, a per-shot card sheet and its gate only") and say drift is 5 of 36 so the measuring branch is not triggered. That points the helpers at a card sheet; both helpers named it and weighed it as one option. It also carries the counter-fact (more than a third moving-only, so a still-only change cannot reach the number), which is fair to give.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 3 | 3 | 4 | 4 | 5 | 19 |
| V2 | 4 | 4 | 3 | 3 | 4 | 18 |
| V3 | 4 | 4 | 4 | 4 | 4 | 20 |
| V0 | 5 | 4 | 4 | 4 | 4 | 21 |
## Sam test
Q1: Yes: an expert closes the gate that a typed line passes, makes the pre-build picture the real shot drawn by the kits (camera, people at their marks, three moments, the next shot beside it), and tests it on the record before asking.
Q2: Rests on all 36 shot-design notes of three films; the learn step draws the board from each film's plan as it stood before its first notes (git history, e.g. the Remakes film file at its first commit), not from the fixed code, so it is not judged with hindsight.
Q3: Root cause shown (no picture of a planned shot with its people existed before building on any of the three films; the gate passes any dated line, preflight.py:230; Remakes logged its built check sheet, Blessed its sets sheet). The gate reads rough.py's record, every shot in the shot list, sent before the first build commit; success is counted from census tags at each end-of-film review.
Q4: Four approaches weighed (written cards, kit-drawn board, moving rough already declined, drift measuring not triggered); the board reaches the most of the record that Sam has allowed.
Q5: One rule and its gate, undone alone. Sam is not asked to trust it unshown: the learn step's count and timing come to him with the ask. Risk named: building waits on the board.
Q6: Counts checked against the Step 1 table; rough.py's fixed draft mark (rough.py:224) and spread-out outlines (rough.py:186) checked; ledger costs checked (Remakes 35.96%, Blessed 62.21%, protest tiers/EPR 101.29%). Build and per-film costs, and how much of film cost is notes rounds, unchecked.
Q7: Sized to every shot with real people over time, not 3-4 pencil shots; still honest that it reaches about half.
Q8: Permanent rule rewrite, reviewed at each film's end; the learn step is a measurement, not a trial.
## Pick
V0
## Why
V3 is closest: its facts are right (rough.py draws people alone at a fixed draft mark and outlines spread across the frame, so nothing yet draws the real shot), its reach claim is honest (about 17, excluding F1 and A1, which passed stills), and it names the gap in how sheet notes count. But three things needed mending, so V0 is V3 improved rather than V3 as written. (1) Its learn step runs the board on Remakes' and Blessed's story files, which already hold every fix Sam asked for, so the count would be made with hindsight; V0 draws from each film's first-commit plan. (2) It quietly swapped Sam's agreed aim (at most 3 shot-design notes per film) for "plan-caused at most 1"; V0 keeps Sam's number and says plainly this change alone will likely leave about 6. (3) It proposed counting board notes apart without asking; that redefines Sam's number, so V0 puts it to Sam as a numbered question. From V2: the per-shot fields written on each board row (camera height and distance with its reason, the lead's height on screen, the focus point and the next shot's focus, pieces that must match across cuts) and each shot's open choices as numbered questions, which turn Sam's late choices into early ones. V2 lost points for claiming all 8 moving+plan notes (including F1 and A1, which stills already failed to show) and for calling whole-film overspend "rounds now costing 36-101%", which the ledger does not split. V1 is a written card with a gate on a named line, reach 18 counted generously (Sam's changed mind is not reliably moved earlier by a card), and nothing for timing.
## Faults in the pick
- F1 [fixed] V3's learn step measured on fixed code (hindsight); now drawn from each film's plan before its first notes.
- F2 [fixed] V3 changed Sam's number to "plan-caused at most 1"; Sam's number kept, shortfall stated.
- F3 [fixed] Counting board notes apart was assumed; now a question to Sam.
- F4 [named] Reaches about 17 of 36 at best (about 6 per film left); "at most 3" needs a later change, chosen after two films' results.
- F5 [named] Build cost (about 2-3% of a week once) and per-film cost (about 0.5%) are unchecked; the ledger gets a "board" stage so the next film measures it.
- F6 [named] Untested on flat-people films (where people's heights and positions are drawn differently).
- F7 [named] Camera height felt only in motion (F1, A1), Sam's mind changes on moving shots (5) and drift (5) are out of reach.
## Final version
**Learn first (changes nothing, about 0.5% of a week, unchecked).** rough.py gains a board mode. Draw the board for Remakes (14 shots, from its film file at the first commit, before any notes) and for Blessed's plan at the same point. A judge chat that did not draw it counts how many of those films' shot-design notes the board visibly shows, row by row against the census, and times the run. Result goes to Sam with the ask.

**The one change (its own yes).** Rule 11 is rewritten, not added to: before building, every shot in the film's shot list is drawn by the kits on one board: its real camera, its cast at their marks and true heights, at three moments on the draft clock (start, key beat, end), with the next shot's first frame beside it. Under each shot a short row: camera height and distance and why, the lead's height on screen, the focus point and where the next shot's focus sits, pieces that must match across the cut, and the shot's open choices as numbered questions. Rule 10 names these fields.

**Gate in code.** Pre-flight reads rough.py's record, not a typed line: it refuses if any shot in the shot list is missing from a delivered board, any shot has no people on it, or the board was sent after the film's code was first committed.

**Number to beat.** Sam's: at most 3 shot-design notes per film after building, on the next two films, none returned twice, counted from census tags at each end-of-film review. Said plainly: this reaches about 17 of the 36 (still + plan 12, plus timing, order and cut rows that show across three frames: F3, F7, F23, A31, Remakes 47), so about 6 per film may remain; the next change is chosen from what the two films leave.

**Cost.** Build about 2-3% of a week once; per film about 0.5% (both unchecked; measured in the learn step and in the ledger's own stage).
## For Sam
### Option 1: A drawn board of every shot before building
Before anything is built, you get one picture sheet showing every shot as the camera will see it, with the people standing where they will stand at three moments (start, the key beat, the end), the next shot beside it, and a few numbered choices per shot. A check refuses to start building until that sheet has reached you. First, it is tried on the plans of Remakes and Blessed to count how many of your old notes it would have caught, and that count comes with the ask. Honestly: it can catch about half of your framing notes; ones you only feel when things move will still come on the animatic.
1. Should notes you give on the board count toward your "at most 3 per film"? (pick: N, they are counted apart, since they cost little.)
Lost: building waits for your answers on a bigger sheet, about half a percent of a week per film.
Added: a sheet of every real shot with people, timing and choices; a check that a typed line cannot get past.
### Option 2: Written shot cards, one picture each
Each shot gets a short written card (camera height and why, how big the lead is, where the eye goes, what must match the next shot) and one still picture drawn from it, sent before building, with a check that the card sheet was sent. Cheaper to build, but one still per shot cannot show order or timing, so it reaches fewer of your notes, about a third.
Lost: about a third of a percent of a week per film; timing problems still wait for the animatic.
Added: a written card and one still for every shot before building.
