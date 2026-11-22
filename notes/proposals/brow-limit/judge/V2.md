## Leak
Sam's 19 Nov words "the brow limit enforced by the kit" name a remedy; weighed below as one approach, not assumed.

## Results
- One Sam note (Milburn note 1, 18 Nov): scene 7's angry brows tipped into "steep slashes through the glasses". Cause: `frown` (the brow pull) at 0.16 (rage) and 0.22 plus lowered brows (gape); fixed by setting both to 0.14 (notes/archive/milburn.md, chat 13 Done; source/milburn.py lines 169-175).
- Cost: chat 13 spent 2.25% of a week, but it also fixed four other notes; the brow share is unchecked (notes/ledger/milburn.md line 38).
- The limit lives only as a comment in source/milburn.py and a line in the archived notes. The "Rule 56" chat 13 cites no longer exists: old 56 was merged into rule 89 on 10 Nov (guides/film-quality-rules.md lines 90, 126). Nothing enforces 0.14 anywhere (grep for a frown limit in source/: only ad_vanced_notice_cast.py).
- The opposite fault has happened: Ad-Vanced Notice note 36c, Sam marked "Seen before": anger didn't show because that film capped the frown at 0.13, so stronger anger drew the same brows (notes/archive/ad-vanced-notice.md line 174; source/ad_vanced_notice_cast.py line 493). A plain cap already cost a repeat note.
- `frown` is not one unit: faces.py and turnhead.py add it to the inner brow end on top of each head's own measured brow slope (faces.py brow_uv; turnhead.py line 634); measured slopes run from about -12 to +1.8 degrees (source/patriots4_cast.py lines 47-65). traitors.py uses frown 1.0 and 1.4 in a different drawing. So 0.14 is right for Milburn's heads only; the same number draws a different angle on another head.
- The 3/4-parts rule exists as a kit test, `turned_parts_kept` (source/kittests.py line 48), run only on Milburn's cast. It is not in the rulebook. Kit tests run in the background at session start (.claude/hooks/setup.sh line 33) and block nothing: `facehouse_whole_head` has failed since 15 Nov (milburn.md Checks line).
- Gap: no record of how steep a brow looks wrong on a non-glasses head, a turned head, or a kit person.

## The real decision
Not "write 0.14 down somewhere" but: how does every future film's face stop drawing a brow shape Sam has rejected, without losing the anger he asked for, and how does a lesson tested on one film's cast cover every film's cast. The bigger lever is that kit tests are tied to the film that taught them and do not stop anything.

## Root cause
1. The limit was set as a number in the film's own mood table, in a unit that changes meaning per head, so it could not be carried over even if written down.
2. Lessons become tests on that film's cast, and tests warn rather than refuse.
3. Nothing checks that anger still reads once the brow stops (the 36c fault).

## Approaches weighed
A. Write 0.14 into the rulebook and the kit catalogue. Relies on a chat reading it; wrong number for other heads. Rejected.
B. Clamp `frown` at 0.14 in the kit. Enforced, but the wrong unit, and repeats 36c's silent cap.
C. Reframe: limit the drawn result, not the input. The kit measures the angle of the brow's inner half on the head being drawn (front and turned) and never draws it steeper than a learned limit; any mood that hits the limit is named in pre-flight so its anger is carried by squint, lids, mouth and head.
D. Learn first: one sheet of the angry moods on every head kind, to find where each starts to look wrong. Feeds C.
Chosen: D, then C, then a separate change for every-film tests.

## Proposal
**Learn first (changes nothing, about 0.5%, Sonnet):** one labelled sheet: frown 0.06 to 0.22 on Andy and Milburn (house heads, glasses), a kit person without glasses, and each turned at 45 degrees; each brow's inner angle printed under it; looked at at phone size against Sam's note picture. Result: the angle where the brow becomes a slash, and whether glasses change it.
**Change 1, brow shape in the kit (own yes, about 1.5%, Opus medium):** faces.py and turnhead.py stop the inner brow at the learned angle on every head; pre-flight prints each mood that reached it ("rage: brow at its limit; anger from squint/lids/mouth"). Kit test: refuses Milburn's old rage 0.16 and gape 0.22 shapes, passes 0.14, and on Kemi's and a kit head gives the same angle. Number to beat: zero Sam notes on brow slashes and zero "anger doesn't show" notes over the next two films.
**Change 2, kit tests follow the film (own yes, about 0.5%, after Change 1):** `turned_parts_kept` and the brow test run on the current film's cast in pre-flight, and a failure refuses the animatic like other pre-flight faults. Number to beat: no turned person missing a front part in the next film's animatic.
Total about 2.5% once, against 15% per film; nothing per film after.
Sam would notice: angry faces stay angry without slashes; possibly an extra Checks line naming a brow at its limit.

## Sam test
Q1: an expert fixes the measure and the check, not one number. Pass.
Q2: evidence from two films (Milburn, Ad-Vanced Notice) and every head kind on the sheet. Pass.
Q3: enforced in the drawing and pre-flight, not by reading; the anger guard closes the comply-on-paper gap. Pass.
Q4: four different approaches weighed. Pass.
Q5: each change undone alone; nothing changes before the sheet shows the angle. Pass.
Q6: sources named; brow share of chat 13 unchecked. Pass.
Q7: not the cheap clamp (B), which already failed once. Pass.
Q8: permanent kit changes, reviewed at film end. Pass.

## Lost / Added
Lost: films can no longer draw a brow steeper than the limit, even on purpose (a cartoon V needs Sam's yes).
Added: one Checks line when a mood is at the limit; a test that refuses the animatic if a turned person loses a front part.

## Unchecked
Brow share of chat 13's 2.25%; whether people_parts.py front heads route through faces.brows; Andy's glasses in scene 7; the face-size scale of `frown` per head.
