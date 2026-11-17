# Helper A: Craft-next Step 2

## Leak
Leak: the facts carry the adopted plan's branch ("plan faults dominate: a per-shot card sheet and its gate only"). Treated as one option, not the answer.

## Results
- 36 shot-design notes over three films: plan wrong or silent 20, Sam's late choice 11, build drift 5; seen on a still 20, only when moving 16 (craft-next.md, Step 1 table; counts checked against the rows).
- Cross-count (checked against the rows): still+plan 12, still+Sam 6, still+drift 2, moving+plan 8, moving+Sam 5, moving+drift 3.
- By film: EPR 13 (10 moving-only), Blessed 13 (4), Remakes 10 (2) (craft-next.md:91).
- Repeats: 5 framing/camera notes came back (F13, Blessed 32, 42, Remakes 63, 71) (craft-census/notes.tsv, repeat=Y).
- Cost: Remakes spent 35.96% of a week against 14.5% planned (notes/ledger/remakes.md:5); Blessed 62.2% (ledger/blessed.md:7); protest tiers 101.3% (ledger/protest-tiers.md:7; that this is EPR is unchecked). Share of that spent on shot-design rounds: not in the record (a gap).
- Today's gate passes on any dated "Composition sheet sent:" line (source/preflight.py:230); Remakes and Blessed met it with sheets of a built film or of sets, not shots with people (problem file; unchecked).
- The moving+plan 8 are mostly plan silences about time: "no slot per piece" (F3), "jet at 2.5-4.0 of 4 s, bunches" (F23), "gap in bands, no metres" (F7), "grenade man in frame the whole time" (47).

## The real decision
Not "which sheet", but: at what point in the film does each shot's design get fixed, and how much of it can be shown to Sam before building without a moving rough he declined. The bigger lever is the time axis: a still card cannot reach 16 of the 36.

## Root cause
Shots are designed in code during the build, not on paper: the plan names 3-4 key shots, says nothing per shot about camera reason, the lead's size, focus or beat timing, and the gate checks only that a line exists. So plan silences (20) and Sam's choices (11) surface on the animatic. The EPR still roughs failed (F1, A1) because one still per shot shows a frame, not how the shot plays over its seconds.

## Approaches weighed
1. Per-shot card sheet, one still per shot with people placed, gate on every shot. Reach at best still+plan 12 and still+Sam 6 = 18 of 36.
2. Reframe: per-shot card as a still filmstrip: each shot drawn by rough.py at start, key beat and end on its draft clock, with a beat bar in seconds and each shot's open choices as numbered questions. Still pictures, not a moving rough. Reach at best 18 + moving+plan 8 = 26.
3. Learn-first: before building either, test on the record whether a strip would have shown the 8 moving+plan notes, from their plan lines.
4. Drift measurement against agreed frames: drift is 5 of 36, so it is not the lever (craft-next.md:93).

Chosen: 3 then 2. Choosing between 1 and 2 needs 3's answer.

## Proposal
**Learn first (no yes needed, changes nothing):** one chat takes the 8 moving+plan notes and, from each plan line, judges whether a 3-frame strip with a beat bar would have shown the fault. About 0.5% of a week (unchecked). Result: N of 8. If N is 4 or more, the change is the strip; if fewer, the single-still card.

**Then one change, for Sam's yes:** rule 11 rewritten, not added to. Every shot (not 3-4) gets a card drawn by rough.py from the film's shot list: camera height and distance with a reason, lead's height on screen, focus point and the next shot's focus, pieces that must match across cuts, (if chosen) start/beat/end frames on the draft clock, and the shot's open choices as numbered questions for Sam.
- Enforced in code: pre-flight refuses unless the sheet record lists every shot in the film's shot list, each with people on it, and was sent before the first build commit. A chat cannot pass it with an old sheet or a line of text.
- Number to beat: shot-design notes after building starts at most 3 per film on the next two films (from 8-13), none returned twice, counted from the census tags at each end-of-film review. Notes on the sheet are counted apart (cheap, before building).
- Cost: building the strip into rough.py about 2-3% of a week once; per film about 0.5-1% (unchecked; the ledger gets its own "cards" stage so it is measured). Set against 15% per film and rounds now costing 36-101% per film.
- Honest reach: at best 26 of 36 (about 3 per film left on average). It cannot reach Sam's moving mind-changes (5) or drift (5); an EPR-like motion-heavy film will likely stay above 3. Sam is told so.
- What Sam would notice: one bigger sheet before building, with a few numbered choices per shot; fewer framing notes on the animatic.

## Sam test
Q1: an expert moves design decisions earlier and tests reach on the record before building; this does both.
Q2: evidence is all 36 notes of three films, plus the 8 notes the learn step re-reads.
Q3: gate is code (every shot, people on it, sent before build); result counted at review.
Q4: four different approaches weighed; the chosen one reaches most within what Sam allowed.
Q5: one rule rewritten, undone alone; nothing unshown is trusted: the learn step decides the form.
Q6: sources named; cost figures and EPR=protest tiers marked unchecked.
Q7: sized by reach (strip over single still if the evidence says so), cost stated.
Q8: a permanent rule rewrite, reviewed at each film's end; no trial.

## Lost / Added
Lost: building waits for Sam's answers on a fuller sheet; about 0.5-1% of a week per film.
Added: one sheet of every shot with people, timing and numbered choices; a code gate that refuses a missing or late sheet.

## Unchecked
Per-film card cost; strip build cost; that protest tiers is EPR; which sheets Remakes and Blessed actually logged; share of film cost spent on shot-design rounds.
