## Leak
yes: the problem's "What is missing" line asks for "a bar that says whether a move this fast reads as believable to a viewer from THIS camera, and a way to draw it so it does", which points at a camera-based bar plus a drawing fix; and its facts quote chat 34's "count sudden jumps instead?". Both helpers named and set it aside; the chat's own version (V1) follows it closely.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 3 | 2 | 3 | 2 | 3 | 13 |
| V2 | 4 | 3 | 3 | 4 | 4 | 18 |
| V3 | 4 | 4 | 4 | 4 | 4 | 20 |
## Sam test
Q1: Yes. An animator's answer (the times are fixed, so fix the spacing: ease and overlap inside the window) with a bar computed from physics, not guessed; the expert addition taken from V2 is judging at the delivered 1.1x speed and on screen through the film camera.
Q2: Scope is right: every fast locked move, not one shot. Evidence: chat 42's per-joint numbers, the camera keys (gta_rehearse CAM4), Sam's notes (impossible bodies, never speed: pass list 18-20), the gun hand's 0.8 m reach (learn-step L96) and its K1 hold to 0.83 s then 22-28 cm a drawing (L303). Per-joint travel for the other joints is measured in the learning step, not assumed.
Q3: Root cause shown: the climb is crammed into about 0.33 s of a 0.5 s window (keys C1 0.56 to C3 0.89), so joints wait then whip; the gun hand's 33.8 cm speed change is about 13 times what its window needs. Enforced in jumps(), which the clip build calls (bench_move.py L1676, L1946). The paper-compliance gap (shrink the move's travel to lower the floor) is closed by a key-pose lock [F2]. Proof: old faults still caught; pops at or under the floor; no speed note from Sam.
Q4: Raise the number, a screen-only test, a real-people speed table, Sam's eye, and fix-the-drawing were all weighed across V1-V3; the floor-referenced bar plus re-spacing beats them because speed is Sam's locked choice, not a fault.
Q5: The learning changes nothing; then two separate yeses (the bar, then the drawing), each undone alone by restoring the old function or the old keys. Nothing new in the house look (V1's smear is left out).
Q6: Checked against the record: jumps() code (L1455-1468), _lerp_goal's halfway snap (L430-431), CAM4 keys, rule 70 (1.1x), L73 (no footage of knees on the seat), proof.txt (142 / 411), ledger estimate 53.2. Unchecked and marked: the 283 / 341 counts, the 89% spent figure, chat 41's "9-17 cm", which joints are on screen.
Q7: Sized by the result (283 pops to 0 except those physics forces, each printed with its floor), not by price; it costs a little more than V1's ask-Sam route and far less than V2's human-speed table, which could not change the locked timing anyway.
Q8: Permanent: written into the rulebook's motion check for every film, reviewed at film end against Sam's notes on this shot.
## Pick
V3
## Why
V1 changes the bar before anything is measured, adds a smear (new to the house look), rests on an unsourced human-speed figure and makes Sam the check. V2 finds the right split (break versus speed) and the right viewing conditions (film camera, 1.1x), but its speed test against real people cannot be acted on: the timing is Sam's and locked, so a failing speed result leads only to a style question; and its "jump" test (solved joint off the goal's smooth path) misses a goal path that is itself crammed, which is the actual cause. V3 is the only one that does the arithmetic: the 3 cm speed bar can never pass, but the 3 cm speed-change bar mostly can if the move uses its whole window, so the fault is in the drawing's spacing, exactly what "fix the drawing, never the shot" asks. Taken from V2: measuring at the delivered 1.1x speed; the goal-snap and per-frame-solve flip as named causes to sort in the learning; the guard that no break can be named and passed. Added by me: the key-pose lock and a moving watch at phone size.
## Faults in the pick
- F1 [fixed] V3 computed floors at 24 fps film speed; the film is delivered at 1.1x (rule 70), so steps grow 1.1 times and speed changes about 1.2 times. Floors and on-screen steps are now computed at delivered speed.
- F2 [fixed] A chat could pass the new bar by shrinking the move (smaller travel, lower floor). Key poses K1-K3 are locked; travel is measured from them, never from the re-spaced drawing.
- F3 [fixed] V3's floor ignored the two causes V2 found in the code: a goal missing from one key snaps across at the halfway point (_lerp_goal), and each frame is solved from scratch (the 81 cm knee flip). The learning sorts every flag into these, crammed spacing, or forced speed.
- F4 [fixed] Numbers alone do not show it reads; a 1.1x clip from the film camera, watched at phone size and slowed, goes with the bar's numbers (Seeing like Sam 1).
- F5 [named] The floor assumes rest-to-rest travel per joint; curved paths and joints tied to planted contacts may need a little more than the ideal ease. Any joint above its floor is printed, not silently passed.
- F6 [named] Whether every send check reads jumps() is unchecked; the clip build does.
- F7 [named] The film has spent about 89% of a week against a 53% estimate (ledger total unchecked); this adds about 4%, honest overspend, reused by every later fast move.
## Final version
**Learn first (changes nothing; about 0.5% of a week; Opus high, the next stage-1 chat).** For the get-up (K1 0.5 to K2 1.0 s) and sit-down (K2 7.4 to K1 7.8 s), per joint, print: travel between the locked key poses; the least speed and the least speed change that window allows (speed at least D/N, change at least 4.9 D/N² for a smooth ease), at the delivered 1.1x speed; the measured values; whether it is on screen in each drawing through the film camera; its on-screen step against the limb's own on-screen width. Sort every flag into: goal snap (a goal missing from one key), solver flip (a frame solved into a different pose), crammed spacing (above the floor), or forced speed (at the floor).

**Then one change at a time, each on Sam's Y:**
1. The speed-change bar: a pop is a speed change over 3 cm a drawing or over its window's smooth-ease value, whichever is larger, at delivered speed. Key poses are locked; travel is taken from them. Proven first on old faults (the 81 cm knee flip, the 33 cm elbow snap, the 22.3 cm elbow pop): all still caught. A goal snap or solver flip is never passable by naming. Target: 283 pops to 0, except joints whose floor is above 3 cm, each printed with it. In jumps(). About 0.3%.
2. The drawing, judged by bar 1: re-space get-up and sit-down over the whole windows, eased in and out, overlapping (hips lead, gun hand starts with them at 0.5 s, head follows). Camera, beats, times, poses untouched. A 1.1x clip from the film camera, watched at phone size and slowed, with the numbers. About 2.5%.
3. Only if on-screen steps exceed limb width: the 3 cm step bar becomes that "reads as two drawings" test on visible parts; otherwise it is removed, on Sam's Y. About 0.5%.

Written into the rulebook's motion check for every film; reviewed when the film is done. Total about 3.8%.
## For Sam
### Option 1: Fix the spacing, measure jerks not speed
The approved rule "no joint moves over 3 cm a drawing" can never pass, because your timing makes Jason move faster than that; that speed is your choice, not a fault. What IS a fault is the drawing: he sits still, then whips up in a third of the time you gave him. First I measure, for each part of his body, the smoothest move your timing allows. Then (your Y) the check only flags sudden jerks beyond that, and (your Y again) I redraw the climb to use the whole half-second, easing in and out, hips first. You'd see a smoother get-up at your exact timing, sent as a short clip from your camera.
Lost: the flat 3 cm-a-drawing speed limit (only after the measuring, on your Y).
Added: a jerk check set by your timing, and a re-drawn, smoother climb.
### Option 2: Sort the faults, then compare with real people
Split the check in two: sudden breaks (never allowed) and speed, judged only on the parts your camera shows, at the speed you watch, against measured real people climbing fast. Then redraw the climb. If he is still faster than a real person, you'd get a question about how the house style shows fast moves.
Lost: the 3 cm speed limit you approved.
Added: a breaks check, an on-screen speed check, a table of real people's speeds (footage of this exact climb may not exist).
