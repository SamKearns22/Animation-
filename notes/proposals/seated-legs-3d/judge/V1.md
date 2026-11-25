# Helper A: seated legs

## Leak
The name ("-3d") and bench-heavy Facts point to one answer; "hand-written 2D outlines" is wrong (Root cause).

## Results
- R7 chats 1-4 cost 27% of a week by Sam's figure (ledger/sam/ycewuzsu.md). Unchecked: the r7 ledger has 0 chats.
- Blind judges, out of 5. Chat 2: front 3-4, 3/4 4, side 4, crossed 3 (results-r7.md). Chat 4: front 2-3, 3/4 3,
  side 3, crossed 2-3 (results-r7c4.md). **The scores fell while the cost rose.** Chat 4 judges read Kemi at 3/4 as a
  man, 3 of 3.
- Sam's seated-legs note: Blessed, 24 Nov, 25 Nov (next-jobs.md R7). Rule 30.
- R7 does not cover skirts or shorts: it switches off when `leg_cover` is set (views.py 367).
- The bench's dressed 3D Jason: Sam said "It looks very good" (23 Nov). His later notes were about fitting Jason into
  the film, not about the body (archive notes). Bench chats cost about 2-2.6% each (estimates).
- **Gap:** the measured body has never been drawn seated in the kit's camera, in trousers, as a woman, or seen front-on.

## The real decision
How the kit makes body shapes that hold in every view without hand-tuning each view: every person, pose and film. A bigger lever too: R7 ran for two chats after its scores stopped
rising, and nothing stopped it.

## Root cause
R7 already builds the legs as 3D tubes and projects them. The tubes are guessed shapes: rings with set radii, plus
hand-set bumps (R7_ARCH, R7_CALF, R7_SPREAD). Flat-picture rules then decide what is hidden:
- a hull or a profile outline, chosen by a cut-off number (R7_END_ON);
- the far leg darkened (R7_FAR);
- the knee drawn again over the jacket hem.

Each patch changed one shared number, so fixing one view moved another. "Stiff tubes" and "lumpy knee" come from guessed shapes;
"which leg is which" and "one dark mass" from faked hiding. A skeleton-first rebuild
would not help: the skeleton is already right (sitting.realize).

## Approaches weighed
1. Patch R7 again. Rejected: the scores fell, and rule 30 says the method is wrong.
2. Measured legs under the flat torso: the MakeHuman mesh on realize()'s joints, drawn the bench way (nearest surface
   on top, house colours, ink), joined to the torso at the jacket hem, a real clothing edge, as R7 joins there now.
3. Reframe, the whole seated person in 3D like Jason. Rejected for now: someone who stands up would change drawing at
   the cut (GTA fault F10).
4. Learn first: one measured sheet, judged blind, before anything is replaced.
5. Traced photo outlines for each view. Rejected: they cannot cover in-between angles, moves or other builds.

Chosen: 4, then 2.

## Proposal
**Learn (changes nothing).** One Opus-high chat (about 2.5% of a week):
- takes the Jason- and car-specific code out of the bench's drawing;
- poses the man and woman builds for May, Kemi and Blair, trousers labelled;
- draws sheet_r7's four views under the flat torsos;
- runs fresh judges (judge_r7.py).

To beat: at least 4/5 in every view, and the right woman or man by 3 of 3 judges (today 2-3/5). If it misses, stop
and tell Sam plainly what is missing.

**Change 1 (only after a pass, its own yes).** The measured legs replace `seated_lower` behind the existing switch
(people.BEFORE_SEATED). Kittests: seated_r7_switch keeps posted films pixel-identical; seated_look still catches Sam's
v4 frames. About 3-4%, once for the kit.

**Change 2 (separate yes).** The mesh becomes the check. A drawn leg outline must match the mesh's outline at the same
joints, and the check must catch Sam's v4 examples. About 1%.

**Change 3 (separate proposal).** A kit job stops after two judged rounds with no whole-point gain. Evidence: chats 2-4.

Skirts wait for their own learning step. Sam sees one judged sheet, then legs that hold.

## Sam test
- Q1: measure first; build on the tool that worked.
- Q2: scoped to the kit's body method; three builds, four views.
- Q3: root cause named; switch and kittests enforce it.
- Q4: five approaches, one a reframe.
- Q5: learning changes nothing; each change can be undone alone.
- Q6: sources are named; the 27% and the bench costs are marked unchecked.
- Q7: aims at 4/5 in every view; the cost is stated.
- Q8: the sheet is finding out, not a trial; changes are permanent, reviewed at film end.

## Lost / Added
- Lost: R7's guessed tubes, for new films.
- Added: a general measured-body drawer, a mesh-outline check and a stop rule for kit jobs, each its own yes.

## Unchecked
The 27%; the bench costs; whether the arm "sausage" came from its join; whether the mesh reads front-on in the kit's
camera (the learning step answers this).
