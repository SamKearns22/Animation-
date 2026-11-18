# Helper A: turned people drawn worse than front-on people

## Leak
Mild: "only for the parts it was given" steers toward adding parts. I also opened chat.md by mistake while listing the folder; this answer is reasoned on its own.

## Results
- On screen: scene 3 (11.0-15.3 s) + scene 6 (34.0-41.6 s) = 11.9 of 68.4 s (notes/milburn.md; milburn.py DUR).
- The listed differences are confirmed by eye on both pictures (fringe, streaks, piercings, moustache, eye bags, ears, haircuts; slab torsos).
- 17 Nov: the front gained streaks, piercings, shag, moustache in 5 commits; the turned drawer got one line, 'shag' -> 'long' "front only so far" (git log, people_parts.py vs people_turned.py).
- Repeat class (rule 30): Sam's turned-view notes in 4+ jobs: Ad-Vanced 42e, Blessed note 4 "blob people", face tool chat 12 "gaunt and weird", Milburn; Milburn notes 3 and 6 also touch turned views (notes/archive, notes/milburn.md).
- Cost: Milburn 19.56% spent, forecast 85.6% (ledger). Cost per turned-view round: unchecked; the ledger does not tag rounds by fault (a gap).
- Why it reaches Sam: rule 38's cast sheet shows front, side, back only; kittest outfit_every_view guards clothes, nothing guards face or hair parts.

## The real decision
Whether every person in every film has ONE drawing all views come from, with an automatic refusal when a turn loses something. That outranks fixing four people.

## Root cause
Two drawers. people_parts.front_head draws through the face frame `f(u,v)`, the same interface turnhead's 3D TurnFace gives, but people_turned never runs that code on the 3D head: it redraws a short list copied from Blessed's press pack ("blob people"). Each new front part is silently lost. 42e was fixed the right way (front design carried round the head) but for Vance only (Sam's Q13), so the kit never got the method. The torso repeats the split: one fixed three-quarter polygon (views.torso_outline).

## Approaches weighed
1. Patch: add missing parts to people_turned. Falls behind with the next new part (17 Nov proves it).
2. Reframe: run front_head's own code on TurnFace; the 3D head draws only outline, ear, nose bridge, back of hair. New parts turn by themselves.
3. Learn-first: a parity measure: each face-card item drawn with and without at 0/45/90; changes the front but not the turn = dropped.
4. Process: cast sheets show the three-quarter of anyone a shot turns.
Chosen: 3, then 2, then torso, then 4, one at a time.

## Proposal
- **Learn (changes nothing):** the parity measure, items read from the face card so new ones are covered automatically; run on every kit person on record. Today's dropped-part count is the number to beat. ~0.5%.
- **Change 1, heads:** turned kit heads drawn by the front's own code on the 3D head. Enforced: parity measure as kittest and pre-flight refusal before any animatic. Beat: 0 dropped parts; Sam passes a front/three-quarter/side sheet of the Milburn four. ~2.5% (one Opus high chat).
- **Change 2, torso:** turned outline from the front outline turned, shoulder line, near sleeve over the body; parity measure extended to torso items. Beat: sheet passed, no "slab" note. ~1.5%.
- **Change 3, cast sheet:** three-quarter tile for everyone a shot turns; posecheck refuses a sheet without it. Beat: 0 turned-view notes at the next film's animatic 1. ~0.3%.
- Total ~4.8% once, for every film; it pushes Milburn further past 15%, so it is logged as a kit job and reviewed against the next film's notes.
- Sam notices: a turnaround sheet per person, then clips of scenes 3 and 6.

## Sam test
Q1: Yes: one source drawing per character is standard; the patch is the trap.
Q2: Evidence spans four jobs and the git history.
Q3: Root cause found; the check finds parts itself and pre-flight refuses, so no paper compliance.
Q4: Four different approaches; this removes the cause.
Q5: Each change undoes alone; Sam sees a sheet before film use; Blessed risk named.
Q6: Sources named; unknowns listed below.
Q7: Sized to stop the repeat, not the cheap patch.
Q8: Permanent; reviewed at film end.

## Lost / Added
Lost: the press-pack hair look on turned kit people (posted films keep theirs through replicate).
Added: one parity check, a three-quarter cast-sheet tile, ~4.8% of a week once.

## Unchecked
Cost per past round; Blessed replica frames unchanged (replicate switches turned heads off via people_turned ON); cost estimates; fringe behaviour past the head's far edge; facehouse_whole_head (failing since 15 Nov), the same fault for famous people.
