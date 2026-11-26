# Proposal: A build format for new pose kits, from what worked in R7

Status: adopted (2026-11-26)

## Problem
Sam, 26 Nov (after R7 chat 11): "Please codify what succeeded in this build into a build format that can
successfully create kits for other poses. This was an arduous and expensive process and we should learn what worked
so that we don't repeat the mistakes of this process."
R7 (a natural seated lower body for May) took 11 chats and about 9.8% of a week against a 6% estimate (25 Nov Sam:
"Building body kits is costing huge unacceptable expenditure ... This cannot continue"). Most of Sam's notes were
faults he saw at a glance that no check had looked for. The next pose kits (other seated poses, other characters,
standing or moving poses) have no written order of work to follow, so they could repeat the same rounds.

## Facts
- Sam, 26 Nov (on chat 11's first draft of this job): "I'm not sure you have understood the crux of our improvement
  which was implementing the full body model and then layering clothes separately. Please check all R7 chats for
  what worked and then update the job." Chat 11's first facts and idea centred on checks and placement: wrong crux.
- Chats 1-5 (notes/archive/r7-handovers.md): the legs drawn as hand-made flat outlines and guessed 3D tubes
  (views.seated_lower, _r7_outline: arch, calf, cloth widths, shade tricks); each patch moved another view; blind
  judges stayed at 2-3 of 5 for four rounds (results-r7.md .. r7c4.md); Sam: "the legs look awful" (sheet v4).
  Chat 5's judged proposal (notes/proposals/seated-legs-3d.md, Final version, root cause): "the tubes are guessed ...
  and hiding is faked by cut-off numbers and shading, so each patch moves another view."
- Chat 6: source/solid_seat.py: the measured MakeHuman body (the GTA bench's way: posed by its own skin weights as ONE
  closed body, one depth pass, house flat colours and ink) built from any kit person's spec, posed on the kit's own
  joints (sitting.realize), drawn through the kit's own camera; trousers as a shell on the body. Judges rose at once
  (side 4/4/4, the rest 3-4; results-r7c6.md).
- Chat 7: patching the seams between solid legs and flat torso again; Sam: "Is there a more intelligent way?";
  Sam picked option 2, the whole person solid (r7.md "Sam's pick").
- Chat 8: mode seat_solid='body': the WHOLE solid body under May's UNCHANGED flat posted outfit (torso, arms, blouse,
  lapels drawn as before on top), the solid shown only below the jacket's seated hem. Sam: "This pose is 100%
  correct", "she is FINALLY correct. She has correct anatomy and outfit." First try had redrawn her clothes on the
  body: "you changed her clothes?", "This is the correct outfit. You have drawn a poor version of it".
- Chats 9-11: every later note was at a layer's edge, not the body: curves of the turned flat torso over the body
  (turned_curves), jacket colour under the hem (trousers seat layer), shoes vs trouser hem (shoe layer), the jacket
  hanging into the gap between parted legs (lap_open). Each fixed in the layer, with a picture check proved on Sam's
  saved frame (kittests turned_curves, jacket_under_hem, shoe_shapes, legs_apart_spread, jacket_triangle).
- New poses on the body are made by joint targets (sitting._leg_by_knee, chat 11) behind a pose flag, so locked
  poses stay pixel-identical (seated_r7_switch; chat 11's 'upright' diff: none).
- Cost: notes/ledger/r7.json, estimate 6.0; chats about 2.2-2.3 each on Opus; 9.87% of 15% at chat 10. Chats 1-5
  and 7 (outline patching) produced nothing kept in the final look.
- Still untested: mode 'body' for standing and moving poses; other people (Kemi, Blair) in mode 'body'; clothes other
  than a suit jacket over trousers (vest, skirt, dress). notes/proposals/model-body-all.md is the related chain.

## Record
notes/r7.md
notes/archive/r7-handovers.md
notes/ledger/r7.json
notes/learn/seated/
guides/kit-catalogue.md
guides/figure-rig.md
guides/pose-gallery.md
guides/job-packs.md
notes/proposals/seated-legs-3d.md
notes/proposals/model-body-all.md
notes/learn/seated/judge/
source/views.py
source/solid_seat.py
source/sitting.py
source/kittests.py

## Verdict (the judge, word for word)
<!-- verdict-hash: e65537762a2d8f10 -->
Who wrote which (hidden from the judge): V1 = helper B, V2 = chat, V3 = helper A. Picked: V3 (helper A). Critiqued: 9 found, 5 fixed, 4 named.

## Leak
yes: the title and the Problem's wording name a remedy ("a build format", "no written order of work to follow"), which steers toward a written guide. The facts also carry Sam's crux (whole body first, clothes layered separately), but that is Sam's own words, not a leak. Weighed the written order as one option among others.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 3 | 4 | 4 | 19 |
| V2 | 3 | 2 | 3 | 3 | 5 | 16 |
| V3 | 4 | 4 | 4 | 3 | 4 | 19 |
## Sam test
Q1: Yes. An expert puts the proven method into the tool every kit job runs (a sheet command with refusals) and a gate at hand-over, not a page a chat may skip; and fixes the cost record so overspend shows.
Q2: Evidence is wide: all 11 R7 chats (handovers checked; a filtered pass over the transcripts as Sam asked), three cost records, GTA shot 4 and the model-body chain. The real unknown (does it carry to other people and outfits) is measured first, on Kemi and Blair.
Q3: Root causes named with evidence (no entry point for the proven route, no stop on a dead method, seam checks only after Sam and only on May, cost filed elsewhere). It happens in every kit chat because the hand-over check refuses a kit chat that skips it; each change has a number to beat.
Q4: Five approaches weighed (guide, code format, learn first, whole-default reframe, stall stop); the pick sits inside the reframe (body as every person's default) rather than forking it.
Q5: Learn changes nothing; locked poses are diffed to "none"; each change undoes alone; the stall stop goes live only once the judges agree with Sam's own verdict.
Q6: Costs checked against the three cost records (13.3 in two other records, 11.2 in R7's own, one chat booked twice); rule 24 pause and rule 87's per-fix wording checked; costs are estimates and marked so.
Q7: Sized by R7's ~15.6% that bought nothing; about 6% once. Not a cheap page.
Q8: Permanent changes, no trial; reviewed against the next pose job's results when Sam calls it done.
## Pick
V3
## Why
V3 makes the format code (one pose command that builds the standard sheet and refuses a missing reference or a locked-pose change) and extends the seam checks to every person; that is the most comprehensive and cheapest real answer. Its gaps: nothing made a kit chat start on it, its stall stop trusts judges never checked against Sam, and it extends checks before knowing they carry. Taken from V1: the Learn probe (Kemi in her vest and Blair, seated on the whole body, every R7 check run, a viewer pass on each seam), the kit-job pack and catalogue row with a hand-over gate, and the stall stop going live only once the judges agree with Sam. Taken from V2: the format's content stated plainly as two layers in order (body by joint targets, then the posted outfit untouched with each lower garment its own layer), and "fault in the body: fix joints; at an edge: fix that layer". V2 alone relies on a chat reading a page and leaves cost and stopping untouched. V1 alone has no sheet tool, so the gate checks paperwork rather than the picture.
## Faults in the pick
- F1 [fixed] Stall stop rested on blind judges never scored against Sam's mode-body verdict; now live only once they agree with him.
- F2 [fixed] No entry point: a kit-job pack, a catalogue row and a hand-over gate now make every kit chat start on the command.
- F3 [fixed] Checks extended before knowing they carry; the Learn probe decides which carry, and each that does not becomes a listed thing to learn.
- F4 [fixed] The crux was implied, not stated; the two-layer order is now the command's default and the pack's first lines.
- F5 [fixed] Showing running costs would break rule 24's pause; booking is fixed quietly and the true cost appears in the end-of-job review.
- F6 [named] Untested standing, moving, skirt or dress: until a job proves one, it opens with a "what must be learned" step, not the format.
- F7 [named] All costs are transcript estimates, not app figures.
- F8 [named] One yes covers Learn and the booking fix; later pieces follow Learn, each sent first as one Lost/Added line Sam can refuse.
- F9 [named] V3's "three sheets for the apart pose" is unchecked (two sent so far); the bar is two sheets.
## Final version
**Learn (changes nothing; Opus medium, about 2%).** One filtered pass over all 11 R7 transcripts: each Sam note and dead end, the layer it sat on, what would have caught it, its cost. Then Kemi (vest) and Blair seated on the whole body, under their posted outfits, each beside their posted look; every R7 seam check run, each seam looked at full size. Output: which checks carry, miss or cannot run.

**C1 booking (0.3%, now).** The start check books each chat to the job it names; R7's five misfiled chats and the double-booked one moved to R7. Beat: R7 shows about 24.5%, matching its chats.

**C2 the format as a command (about 2%).** A pose is joint targets plus a saved reference photo, behind a pose flag. The command builds the body from the person's spec, posed on the kit's skeleton and camera; lays the posted outfit on top unchanged, the body showing only below its hem, each lower garment (trousers, seat, shoes, lap opening) its own layer; draws four views beside the posted look and the reference; runs every seam check that Learn shows carries; diffs locked poses. It refuses no reference, a redrawn outfit, or a locked diff not "none". Fault in the body: change joints, never an outline. Beat: Sam's "correct" within two sheets per pose.

**C3 entry and gate (0.5%).** A kit-job pack and catalogue row name the command; the hand-over check refuses a kit chat whose sheet did not come from it. Outline patching is refused.

**C4 checks on every person (1%).** Carrying seam checks run on the whole cast, tested on Kemi and Blair. Beat: no Sam note an existing check covers.

**C5 stall stop (0.3%).** Two judged rounds without a whole-point rise: the next step is a "what must be learned" question to Sam. Live once the judges agree with Sam on the passed May sheet.

About 6% once, against R7's 15.6% lost. Reviewed at the next pose job's end.
## For Sam
### Option 1: The format built into the drawing tool
Problem: Your new seated pose took 11 chats and about a quarter of a week, not the 10% you were told, because five chats were booked to other jobs. Six chats were spent patching hand-drawn legs before we used the real body, and every later note was where two layers meet, which no check looked at until you did.
1. First, a look that changes nothing: go through all 11 chats, then try Kemi and Blair sitting with the real body under their own posted clothes, run every check, and list what carries over.
2. Book every chat to the job it belongs to, so the true cost is on record.
3. Make the method one tool: the real body posed by its joints, your posted outfit laid on top untouched, each lower garment its own layer, four views beside the posted look and a reference photo, every check run, your locked poses proved unchanged.
4. Make every new pose job start with that tool; a chat that skips it cannot hand over.
5. Run the edge checks on every person, not just May.
6. If two rounds of fresh scorers (helpers who rate pictures without knowing who made them) show no real gain, stop and ask you what must be learned; this turns on once they agree with your own verdict on May.
Why: It makes what worked automatic instead of a page a chat might skip, and catches edge faults before you see them.
You'd notice: New poses reach "correct" in about two sheets; no edge note given twice; the true cost in the end-of-job review.
Other option: Option 2 below, a hand-over gate without the new tool.
Lost: Patching hand-drawn legs; booking a chat to another job; more than two flat rounds on one method.
Added: One tool, a hand-over gate, checks on every person, about 6% of a week once.
### Option 2: A rule at hand-over, no new tool
Problem: The same as option 1: the working method is written nowhere a new pose job starts, so it gets relearned at great cost.
1. First, the same Kemi and Blair test, changing nothing.
2. Book every chat to its own job.
3. Write the method into what pose jobs read, with a list: pose kept separate from locked ones, a reference photo saved, the sheet beside the posted look, a check on every edge.
4. The hand-over check refuses a pose job missing any item on the list.
5. The same stop after two flat rounds, once the scorers agree with you.
Why: Smaller and quicker, still enforced.
You'd notice: The same true cost and first sheets beside the posted look.
Other option: Option 1, which builds the method into the tool itself.
Lost: Patching hand-drawn legs.
Added: A list checked at hand-over; about 5% of a week once.
