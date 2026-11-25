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
