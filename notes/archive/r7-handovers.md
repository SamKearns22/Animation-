# R7 handovers (archived)

  - **R7, where things stand (chat 1, 25 Nov, session_01U3pKR21qH3HD4urog8SVBy; next: chat 2, Opus high):**
    Rules that bite next: 86 (every tool a kittest), 13, 85. Locked by Sam: Open Wounds' seated frames (switch off).
    Done: views.seated_lower: bottom, thighs, knees, shins as ONE shape (3D solids projected, outlined once); the knee
    is the thigh's rounded end over the shin; people sit ON the chair's seat (sitting.Seat.surface). Switch:
    people.BEFORE_SEATED (Open Wounds + posted films off; every new film on); kittest seated_r7_switch (9 Open Wounds
    frames unchanged; 546/546 fingerprints of 3 films unchanged). Check: castsheet.seated_look reads the PICTURE
    (ball knee; jacket hem with no bottom under it); catches Sam's frame (R7_EXAMPLES) and the old drawing; kittest
    seated_r7_look. Sheet sent to Sam: notes/learn/seated/r7-before-after-v1.jpg.
    Open (chat 2): (1) no_bottom still misreads R7's own front views and Kemi's vest (hands/stripes taken as the hem):
    retune until R7 passes and Sam's frame still fails, then assert it in seated_r7_look; (2) front-view knees read a
    little blobby: try a narrower knee end and a crease between the thighs; (3) Kemi three-quarter/side: a short stray
    line under the vest (look whether it is the torso's); (4) blind judge + woman/man judge on seated views (R7 brief);
    (5) reference photos: Wikimedia refused (too many requests), Openverse needs a login, Unsplash blocked: proportions
    came from figure-drawing measures, so ask Sam for 3 phone photos (front, three-quarter, side) of someone seated.
    Read: this R7 entry; views.py "R7: the seated lower body"; castsheet.py "R7: ... seen as a viewer"; kittests seated_r7_*.
    For Claude: render with R7 on: sp['seat_r7']=True, sitting.pose(sp,'upright'|'cross, knee over knee').


  - **R7, where things stand (chat 2, 25 Nov, session_01U3pKQzwtcxXpPFrs5pH7DZ; next: chat 3, Opus high):**
    Rules that bite next: 86, 13, 85. Locked by Sam: Open Wounds' seated frames (switch off). Lock test: Blair 45/90
    re-fingerprinted (Open Wounds' own sleeve change moved them; proven R7 not the cause).
    Done (chat 2): (1) castsheet.no_bottom reads the hem whole (shaded folds, across hands and stripes, sides skipped,
    a hand under the edge not judged; a drawing's exact colours): every R7 view and pose passes (lowest 87%), Sam's frame
    60%, the old drawing fails at 3/4; kittest seated_r7_look asserts all three (and pins views.KIT_LEG: remakes_cast
    swaps views.leg on import). (2) Front knees: knee 33 across (was 38), no line where the knee's end lies on its own
    shin, a kneecap curve when seen end-on (R7_END_ON, R7_CAP). (3) Kemi's stray lines: the hi-vis zip ran to a
    standing length (people_parts.workwear_torso) and the short top's seat piece drew a box (body.trouser_seat r7):
    both new-films only. (4) 3 blind judges: notes/learn/seated/judge/results-r7.md. Sheet: r7-before-after-v2.jpg. Next (chat 3, Opus high): the judges' faults, fix the drawing: crossed top leg's shoe a floating lump and the knee
    join; front-view trouser legs too thin (cloth, not calves; show the lap); women seated read as men from the front
    and side (Kemi). Then fresh judges again (judge_r7.py). Also (Sam "1 Y", 25 Nov): kit-test results kept per run,
    each test written as it ends, a restart re-runs only the unfinished; proposal route first, then build. Needs Sam: 3 phone photos (asked, chat 2; Commons answers the web-fetch helper now, so chat 3 tries it too).
    Read: this entry; results-r7.md; views.py "R7: the seated lower body". No rule requests. Branches named in notes/brexit-is-done.md and open-wounds-chat14 (Open Wounds' chain): not R7's.

## Chat 3 handover (archived by chat 4, 25 Nov)
  - **R7, where things stand (chat 3, 25 Nov, session_01U3pKR3Cspb5BP616FtwQHs; next: chat 4, Opus high):**
    Rules that bite next: 86, 13, 85. Locked by Sam: Open Wounds' seated frames (switch off; seated_r7_switch passes).
    Done (chat 3): 16 Commons photos with licences (notes/learn/seated/refs, LICENCES.md). Crossed leg (new films,
    sitting.R7_CROSS): the top knee rests on the R7 thigh, the shin hangs nearly parallel, foot off the floor, toes down.
    Shaped shoe turned whole (views._r7_shoe; the old box sheared). Trouser legs as cloth (views.R7_CLOTH; knee 14 cm
    across, straight to the hem); women's knees together touching (sitting.R7_WOMAN); a thigh pressed on the seat
    spreads 1.3 (R7_SPREAD). The ball-knee check needs a round patch (castsheet.BALL_ROUND: Blair's two legs fooled it).
    Judges (results-r7c3.md): Kemi side now woman 3/3; crossed still 2, upright legs "one dark mass", front "no knees".
    Next (chat 4, Opus high): results-r7c3.md "For chat 4" 1-5 (near leg's edge over the far leg; front knees and lap;
    side thigh curve; women), then fresh judges (judge_r7.py r7c4). Then Sam's "1 Y": proposal kittest-resume is
    written (problem, facts, chat.md): `propose.py pack kittest-resume`, two helpers, judge, record, then build + kittest.
    Needs Sam: nothing (his 3 phone photos not needed). Read: this entry; results-r7c3.md; views.py "R7: the seated
    lower body". Open rule requests: none. For Claude: sitting.py's R7 changes gated by sp['seat_r7']; not R7's (named,
    25 Nov): branches kit-tests-when-build, brexit-chat15, gta-*, dreamy-fermi; CLAUDE.md sentence moves; the file's
    project "Where things stand" (R7 is a sub-entry).


## R7 chat 4 (moved by chat 5, 25 Nov)
  - **R7, where things stand (chat 4, 25 Nov, session_01U3pKR2q2S17Htq5WHcspgq; next: chat 5, Opus high, after Sam's Q1):**
    Rules that bite next: 86, 13, 85. Locked by Sam: Open Wounds' seated frames (switch off; seated_r7_switch passes).
    Done (chat 4): legs drawn by their profile, not a convex hull (views._r7_outline): the thigh's arched top and dip
    before the knee (R7_ARCH), a calf (R7_CALF), the cloth narrower under the knee; the far/under leg in shade and the
    near leg's edge the whole thigh (_r7_col, R7_FAR); from the front the shins in shade under the knees (a lit lap read
    as the seat: R7_LAP 0); feet staggered (sitting.R7_STAGGER). Check: castsheet.one_tone (chat 3's "one dark mass"
    saved: notes/learn/seated/examples), no_bottom reads all the cloth's tones; seated_r7_look extended. Judges r7c4
    (results-r7c4.md): May a woman in every view; far leg and shoes fixed; scores still 2-3.
    Next (chat 5, Opus high): results-r7c4.md "For chat 5" 1-6 (crossed shin and shoe; trouser hem breaks; front
    re-judge; far-leg shade read as crossing; Kemi 3/4; shoes from the side), then judges judge_r7.py r7c5.
    Needs Sam: Q1 kittest-resume (judge picked Option 1, built into the kit-tests-when record, still unmerged on
    claude/kit-tests-when-build; Sam's Y was Option 2's shape). Read: this entry; results-r7c4.md; views.py "R7".
    Open rule requests: none. For Claude: not R7's (named, left for their chains): claude/kit-tests-when-build,
    claude/brexit-chat15, claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31;
    the CLAUDE.md sentence moves; the project "Where things stand" (R7 is a sub-entry). one_tone skipped at yaw 90.

## Where things stand (chat 5, 25 Nov, session_01U3pKQyiJ2poN3syCEWUzsu)
Rules that bite next: 30 (fix the method, not the picture), 87 (a fix failing twice stops), 85 (cost watch).
Done: Sam's 25 Nov notes saved (notes/learn/seated/handover-sam-25nov.md); proposal seated-legs-3d judged; Sam
picked "1" (adopted). The judge's V2/V3 labels look swapped (seated-legs-3d/judge-labels.md). No code changed.
Next: chat 6, Opus high (building new): Learn steps 1-5 of the proposal's Final version, cap 4% of a week, cost in
the r7 ledger at each handover; below the pass bar, stop and tell Sam what is missing; no outline patching.
Needs Sam: with the learn sheet, in one message: Change 1 Y/N and Change 2 Y/N (each needs its own yes).
Locked by Sam: Open Wounds' seated frames (switch off; kittest seated_r7_switch); the bum/seat he accepted.
Read: the proposal's Final version; guides/job-packs.md "Build"; MAPs of source/bench_pose.py, bench_draw.py,
bench_move.py (dressed_draw), sitting.py realize, views.py _limb3. Open rule requests: none.
For Claude: end-check SENTENCE x4 are CLAUDE.md edits by other chats (34f49840, 0945cc85; named by earlier chats),
not R7's. Branches not R7's, left for their chains: claude/kit-tests-when-build, claude/gta-v5-sound-draft,
claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31.

Cost line (recorded every handover; shown to Sam only on a problem): film so far 0% of 15%; forecast not yet planned (2026-11-25)

## Where things stand (chat 6, 25 Nov, session_01U3pKQzBQSVMGz9aFiBTmTa)
Rules that bite next: 30 (fix the method, not the picture), 87 (a fix failing twice stops), 85 (cost watch).
Done: Learn 1-3 of seated-legs-3d. source/solid_seat.py draws the measured body's legs for ANY kit person on the kit's
joints and camera (switch seat_solid; off for every film), trousers, shoes, a knee-length skirt from the body's own skirt
surface (works: May, 4 views). Crossings 0 (Kemi crossed: 6 points under 7 mm, named). Judges (results-r7c6.md): side
4/4/4 (passes), crossed 3-4, 3/4 3, front 2-3; nothing below chat 4. no_bottom fails every tile: bottom hidden.
Next: chat 7, Opus high (building new): fixes 1-4 in results-r7c6.md "For the next chat", re-judge (r7c7); add kittest solid_seat (crossings 0 on May; the check finds them with
PRESS_ROUNDS=0: 29/107 in chat 6). Cap left:
2.2% (ledger: 1.78% spent). Pass -> step 5 (Sam: winner beside v4, Change 1 Y/N, Change 2 Y/N); cap hit -> tell Sam.
Order (Sam, 25 Nov 18:15, session at 73%): the Open Wounds animatic first (Sonnet chat 17), then R7 chat 7. Kit tests 147/147.
Needs Sam: nothing yet. Locked by Sam: Open Wounds' seated frames (seat_r7 switch off); the bum/seat he accepted.
Read: results-r7c6.md; source/solid_seat.py MAP; proposal Final version; sheet: notes/learn/seated/solid/sheet_solid.py.
Open rule requests: none. For Claude: whole-person solid (2b) not built yet: chat 7 decides after the legs pass.
Branches not R7's, left for their chains: claude/kit-tests-when-build, claude/kit-tests-per-film, claude/gta-v5-sound-draft,
claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31. End-check SENTENCE x4 are CLAUDE.md edits by other
chats (34f49840, 0945cc85; named by earlier chats), not R7's.

## Where things stand (chat 8, 25 Nov, session_01U3pKQz5xGww8EfKdFsFKXb; cost amber: handed over)
Rules that bite next: 87 (a fix failing twice stops), 30 (fix the method), 85 (cost watch).
Done: mode seat_solid='body' (solid_seat.py; off for every film): the whole solid body under May's flat posted outfit,
solid shown only below the jacket's seated hem. Sam: "FINALLY correct ... correct anatomy and outfit", front "100%".
Next: chat 9, Opus medium (a round of Sam's notes): 1. the crossed three-quarter's curves (Brief checklist: find
which drawing makes the bust, waist and hip curves; straighten to her posted boxy jacket; nothing else moves; a sheet
of 4 views to Sam). 2. then the proposal route (source/propose.py): mode 'body' as the default for every new film's
people (seated first; standing/moving next), with Lost/Added, cost, and Kemi/Blair as the next test.
Needs Sam: nothing until chat 9's sheet.
Read: Brief checklist (top lines); source/solid_seat.py MAP + draw(); views._person (solid_whole / seat_solid).
Open rule requests: none. Kit check: started unasked (rule 90), stopped; the film's final runs it.
Locked by Sam: May mode 'body' front, side, three-quarter (examples/sam-25nov-may-front-correct.png); her posted
outfit (sam-25nov-may-correct-outfit.jpg); Open Wounds' seated frames (switch off); the bum/seat.
For Claude: sheet = notes/learn/seated/solid/may_sheet.py OUT body (sheet_solid tiles, MODE body; crops 240,620,840,1740); HEM_OVERLAP, BODY_TOP;
mode 'whole' kept unused; model-body-all chain merged (live). Other chains' branches named in chat 6's archive entry.


## Where things stand (chat 10, 26 Nov, session_01U3pKQyXrivk6K5JRC22Lv5; cost amber at 117 steps: handed over)
Rules that bite next: 87 (a fix failing twice stops), 30 (fix the method), the proposal route (any change to how films are built).
Done: Sam "1 2 yy": both three-quarters hang straight like her boxy jacket with a small bust (turned_curves 0,
turned_bust 0.6: "a very small amount of bust bump ... The side view is a good representation"); her seat below the
jacket is trousers (solid_seat SEAT_TROUSERS). Checks: views.turned_curves_fault (kittest turned_curves), seated
'jacket under the hem' (kittest jacket_under_hem); each catches Sam's frame and passes the fix; Open Wounds untouched.
Sheet c10b; Sam's two shoe notes on it fixed (low shoes, clean hem; check shoe_faults, kittest
shoe_shapes); the sheet no longer cuts her feet off. Sheet sent: notes/learn/seated/solid/may-body-r7c10c.jpg.
Next: chat 11, Opus medium: Sam's two notes on 'upright, apart' (Brief checklist, last lines), a 2-pose front sheet; then the proposal route (source/propose.py solid-body-default; chat 9's draft was lost): mode 'body' (with
turned_curves 0 / turned_bust 0.6 and the trousers seat) as every new film's default people, Kemi/Blair next test.
Needs Sam: OK on sheet c10c (shoes); budget Y/N asked (9.8% of a 6% estimate; he sent notes, read as go on). Read: Brief checklist; solid_seat.py draw(); views._built_outline (turned).
Open rule requests: none. Kit check: not this chat (rule 90; Sam's N by default, the final runs it).
Locked by Sam: May mode 'body' front and side; both three-quarters and the shoes as on c10c once he OKs it; her posted outfit;
Open Wounds' seated frames (switch off); the bum/seat.
For Claude: sheet = may_sheet.py OUT body (sheet_solid sets turned_curves/turned_bust in mode body). handover end's
"SENTENCE lost from CLAUDE.md" lines are other chats' CLAUDE.md edits (34f49840, 0945cc85), not R7's.

