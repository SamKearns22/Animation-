# Model body for every character? (Sam, 25 Nov, R7 chat 7, session_01U3pKQyzgm44MCDdyHMoACP)
Sam: "Should we be building *all* our characters in the way Jason was built? Is that the answer to a large amount of
our problems?" ... "Our solution needs to take into account dynamic movement: a future film may require any action from
an actor. Standing, moving around." Scheduled by Sam for 22:20 (UK) 25 Nov: "Schedule this full investigation".
Facts already checked (chat 7): Islamocommunism: El-Sayed sat behind the desk and STOOD (shot 4); AOC walked in.
GTA shot 4 (Jason, the model body): about 39% of a week (notes/bench/learn-step.md L1); Sam's notes on the model body
itself: poses and movement good, faults were cut-off and passing through the door. R7 approved plan part (b) (whole
seated person solid, house head and hands) is unbuilt. Chat 7 wrongly guessed twice (a 4-view set; "computer look"):
every claim about a past film comes from opening it, saying where.
## The investigation (proposal route: facts first, two helpers, blind judge, top two for Sam)
Requirement 1 (first test of every option): any action, one body, no visible change of drawing at any moment.
1. Count (cheap model for reading; cap 2.5%): every Sam note on every film (notes, archive, sam-notes, ledger notes):
   which a model body would have prevented, which not (likeness, timing, script...), which it might cause. A number.
   STOP after 1 and tell Sam if under about a third of body/pose/contact notes would be prevented.
2. One moving test (cap 6%): a real shot from a past film with people moving (sit, stand, walk), redone with model
   bodies and house heads and hands, at its real angle; beside the original. Clip, not a full render.
3. Blind judges score both; the proposal route's top two to Sam with Lost/Added and the cost impact (one-off switch,
   per film after), from the ledger, no padding.
Dressing (Sam asked what must be learned, chat 7): Jason's clothes were PAINTED on the skin (bench_pose.part_at) and
the trousers a pushed-out skin; loose clothes (open jackets, lapels, skirts, coats, robes, hi-vis) need real garments.
Step 2 checks first, before building: MakeHuman's own garment library (on disk? licence?). Blender: Sam said Y to it
(22 Nov, GTA chat 31; apt install blender, not in setup.sh, so install it first); it drew Jason (L2) but its cloth
simulation was never tried, then dresses the test in a suit jacket that hangs open; checks: cloth never through body or
chair, each garment one piece. Name what could not be learned.
Sam (chat 7): "Do we need to go as far as building 3d clothing models?" Default for step 2: NO garment models or
cloth simulation first. Our style is flat, so only each garment's outline and seam lines must be right. Clothes as
SHELLS from the body (already working: Jason's painted vest cut, chat 6/7 trouser shell hanging straight below the knee,
chat 6 skirt from the body's own skirt surface): a jacket = the trunk pushed out, cut open at the front, its hem hanging
straight and resting on the lap; lapels and ties painted on. Garment library / Blender cloth only if the shell fails a
named test (say which). Robes and coats swinging while walking: a lag rule, tested in the clip.
## Statement One questions the judge must answer (Sam, chat 7: "What aren't we considering? Aligning with statement one")
a. Paying for it: the switch is one-off kit cost outside films; when does it pay back (films to break even at a per-film
   saving from step 1's count)? Every film after must still be top quality within 15%.
b. Sets: people as model bodies against flat-drawn furniture and rooms is today's seam one level up (contact, depth).
   How do chairs, desks, doors, cars meet the body (Jason's car and R7's chair were in the same depth pass)?
c. Heads and hands: hand-drawn heads turning with a freely moving body (angles between our head views; the back of the
   head: Jason's "brown blob"); circle hands vs real hands holding things.
d. Moves: who poses a body for any action? Reuse the acting lists and pose kit; free motion-capture libraries as reference.
e. Checks: the rulebook's checks are built for flat bodies; which carry over, which must be rebuilt and re-proven
   (no rule without a working check) - a hidden cost.
f. The look: posted films vs new ones on the channel; a stranger test on the clip at phone size.
g. Open Wounds (live) stays on the flat kit; the switch only between films.
h. Success measure: the next films' cost and number of Sam's notes vs the last three; a stop rule if worse.
Push notification at the end of each step, pass or stop. Total cap 8.5% of a week; at the cap, stop and tell Sam.

## Step 1 result (investigation chat 1, 25 Nov, session_01U3pKQyLPecZFf57adRJxjG; Opus high; 1.8% of a week)
Where I looked: every film notes file in notes/ and notes/archive/ (28 films; handover, plan, acting, estimate and
work-log sections left out), 1682 lines (count/items.json, each with its file:line). Six Sonnet helpers sorted them
(count/instructions.md, out1-6.txt); a seventh sorted a random 200 again blind (out_sample.txt: agreed on 164 of 200);
then every "prevented" call on a body note checked by hand (count/hand-check.md). Tally: count/tally.py.
- Sam notes: 1058. Places/props 204, moves and timing 202, text/sound 131, camera 104, faces 96, BODY 90, script 86,
  CONTACT 68, other 41, clothes 26, HANDS 10. Body/pose/contact/hands together: 168 (16% of all notes).
- Of the 168: a model body prevents 50 outright (30%); 97 more only partly (87% together), nearly all of them a body
  meeting a flat chair, car, door, desk, table or prop: those need the furniture solid too (question b). 21 not at all.
  All 10 hand notes: not helped. 34 notes (body 15, face 8, clothes 7, hands 4) could be made worse by it.
- Body notes repeat about twice as often as the rest (20% read as repeats vs 11%): they are the costly ones.
- Stop rule: 30% sits right on "about a third", so step 1 stopped and asked Sam (Q1) rather than deciding alone.
Statement One, what step 1 already says (the rest is for step 3's judge):
 a. At most 16% of Sam's notes are about bodies; outright, 5% of all notes. Payback must come from the costly repeats
    (GTA shot 4 alone was about 39% of a week, notes/bench/learn-step.md L1), not from the note count.
 b. 63 of the 68 contact notes are only partly fixed by a solid body alone: sets would have to join the same depth
    pass (Jason's car did: learn-step.md L1 row 1). This is the bigger cost and is unmeasured.
 c. Hands: no hand note is fixed by it. Heads: 8 face notes could get worse (head views on a freely turning body).
 d-h. Not answerable from the count; step 2's clip and step 3's judge.
Open rule requests: none found in this investigation's notes.

## Where things stand (investigation chat 1)
Rules that bite next: 85 (cost watch: step caps), 30 (fix the method), CLAUDE.md "no rule without a working check".
Done: step 1 (the count), above; pushed to the main line.
Next: on Sam's 1, step 2 (Opus high, cap 6%): Blender installed, the moving test on a real past shot (sit, stand,
walk) beside the original, clip only; on Sam's 2, the investigation ends and is marked declined.
Needs Sam: nothing. Sam, 25 Nov (this chat): "1" = go on to step 2.
Read: this file only; count/hand-check.md for the numbers.
For Claude: tally.py in count/; first sort out1-6, blind re-sort out_sample; hand-check overrides by ID.
Locked by Sam: no film shot is touched by this investigation; Open Wounds stays on the flat kit (question g).
