## Leak
Yes: the Facts line "a second flat-colour copy of each frame ... could be drawn by the same code" names one remedy, and the list of outside tools (motion measuring, cut-out models, pose finders) names three more. Weighed below, not assumed.

## Results
- Brexit Is Done: 15 notes, 7 repeated; 62.76% of a week spent against a 52% estimate and the 15% aim (notes/ledger/brexit-is-done.md).
- Of the seven notes Sam gave on 26 Nov (notes/brexit-is-done.md, Notes table), five are about motion or contact, not about a single still: 19 (hands hover over chair arms), 22 (pounce too quick to read), 23.1 (nods and lean grown comic: "THIS IS A MAJOR ERROR"), 23.3 (Kemi's arm path on "backwards"), 23.4 (wolves and guests swap who is in front while running). Four are marked "seen before". The other two (20, 21) are about likeness.
- What each "should have caught" line says: 23.3 "no check looks at the in-between frames of a gesture"; 22 nothing measured how long an action holds (readtime.py built after); 23.1 the size check had a floor set "from a sheet, never from the films Sam passed"; 23.4 the order check merged four guests under one name and was skipped under Override (same file).
- Chat 36 animatic: 9 picture-check flags, mostly meant overlap when looked at (notes/proposals/check-knows-intent.md). That route is already being decided there; this proposal does not repeat it.
- The engine already logs, every frame, who is drawn, in what order, and where (preflight.probe, install_probes; critique.where uses draw_order(t)) (checked: source/preflight.py 72-110, source/critique.py MAP).
- Gap: no record says which seeing method would have caught each motion note. Nobody has tested a strip, a track, a flat-colour copy or an outside model against Sam's saved notes. That is the finding the decision needs first.

## The real decision
Not "which outside program lets Claude watch video". The real question is how the whole film's movement and contact faults get seen before Sam, in every chat that draws or checks moves. The bigger lever is that the engine already knows where every limb, hand and prop is in every frame. Reading that knowledge over time is a bigger step than any pixel tool.

## Root cause
Every seeing aid works one instant at a time: stills, sheets, critique packs, the hand and body checks, picture_faults. Sam's faults happen between instants: speed, hold time, a hand's path, size over a move, front-to-back order across a run. Claude cannot watch video (Statement Two: say so). So a fault that exists only across frames has no picture and no number that shows it. The few time checks that exist (readtime, movesize) were built one note at a time, after Sam saw the fault, and tuned on sheets rather than on passed films. That is why notes come back.

## Approaches weighed
1. **Outside tools** (pose finders, motion measuring, video models). They are trained on photos, downloads are blocked here (makehuman clone failed), and they would guess at positions the engine already knows exactly. Weak, but tested once in the learn step if it installs.
2. **Reframe: motion pictures built from the engine's own truth.** A motion strip shows each moving part's path, with ghosted in-betweens and speed marked, in one still. Claude and a fresh helper can read it as a viewer does.
3. **Time checks from engine tracks.** Each person's joints and depth order logged per frame, with checks on speed, hold, path through the body and order flips. The window for each is set from moves Sam passed.
4. **Flat-colour copy** of each frame (the leaked idea). It helps with overlap and contact in one frame, but it is still one instant and the probes already give draw order.
5. **Learn first:** replay the saved notes against each view and count which one catches them.

Chosen: 5, then 2, then 3, each on its own yes.

## Proposal
**Learn (changes nothing; Sonnet; about 2% of a week, unchecked):** collect every motion or contact note from the last two films (Brexit Is Done 13, 19, 22, 23.1, 23.3, 23.4, plus the earlier film's from its notes and archive). For each note, rebuild the moment from the code as it was then (git), and make four views: (a) motion strip, (b) track plot (path, speed, size), (c) flat-colour copy, (d) one outside pose finder, only if it installs; if not, say it cannot be tried here. A fresh helper who has not seen the note judges each view cold: fault seen, yes or no. Add five moves Sam passed to count false alarms. The result is a table of caught and missed per view. This gives the numbers to beat.

**Change 1 (own yes):** the view that caught the most becomes a shared tool. Expected is the motion strip, added by code to every movement clip and critique pack (`final --small --span` and critique.pack), never by a chat choosing to. It is advice only and never blocks requested work (rule 93). To beat: it catches at least 5 of the 6 saved notes cold, with at most 1 false alarm on the passed moves. About 2% of a week once, then about 0.2% a film (unchecked).

**Change 2 (own yes, only for notes the strip missed):** the animatic render saves the engine's per-frame tracks with the probes. One time check is added for each missed kind (gesture path through the body for 23.3, order flips for 23.4), with its window set from moves Sam passed. Each check has a kit test on its saved note, run once. To beat: it catches its note, with 0 false alarms on passed moves. About 1% per check (unchecked).

Reviewed against the film's results when Sam declares it complete: movement and contact notes per film, against this film's 5.

Sam would notice: each movement clip comes with one picture showing the paths, and fewer notes about hands, speed and who runs in front.

## Sam test
Q1: Yes. An expert uses the ground truth the program already has before guessing from pixels.
Q2: Evidence comes from two films' motion notes and passed moves, not one chat.
Q3: Root cause shown (instant-only seeing, with the notes' own "should have caught" lines). The views are added by code. Success is counted cold against saved notes.
Q4: Five different approaches weighed, including outside tools and the leaked copy.
Q5: Each step has its own yes and comes out alone. Nothing is trusted before it beats saved notes.
Q6: Notes, counts and spend checked against named files. Costs marked unchecked.
Q7: Sized by catching Sam's notes, not by price. The cheap trap (one more still check) is rejected.
Q8: Permanent shared tools with kit tests, reviewed at film end.

## Lost / Added
Lost: nothing; the stills and sheets stay.
Added: a learn table, a motion strip in clips and packs, and time checks only where the strip missed. About 3-5% of a week once (estimate).

## Unchecked
Costs. Whether a video-watching model is available here: none found, so the plan assumes none. Whether outside pose finders read flat drawings. The earlier film's motion-note count.
