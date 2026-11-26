# Proposal: Test five ways for Claude to see our drawings and movement

Status: adopted (2026-11-26)

## Problem
Claude can read only still frames and cannot watch motion, so faults between frames (a hand's path, contact, who is in front, overlap the scene means versus a real mistake) reach Sam or get flagged wrongly. Sam (26 Nov, chat 36) asked what tools or programs would improve how Claude looks at the project's images and its own drawings and animations, was given five candidates in chat, and asked for a proposal. The first route (notes/proposals/better-seeing-tools.md) dropped most of them; Sam: "Your proposal doesn't mention any of the 5 answers you gave me". The proposal must deal with each of the five by name, say plainly which can and cannot be done here and what must be learned or obtained first (CLAUDE.md Statement Two), and checks must never block requested work (rule 93).

## Facts
The five candidates Sam was given, word for word in substance, each with Claude's stated limit:
1. A "who is where" colour copy of each frame: our own engine draws a second copy where every person, hand and prop is one flat colour, so overlap and contact come from the picture, not guessed depths. Claude's pick, cheapest, no downloads. Untested.
2. Motion tracing between frames (a standard video tool, e.g. optical flow in OpenCV): how far each part moves frame to frame, so jumps and vanishing hands show as numbers. Claude's second pick. Whether OpenCV is installed here: unchecked.
3. A picture model that outlines each person/hand in a finished frame (e.g. Segment Anything): checks old animatics; slower, may be wrong on flat cartoons; needs a model download. Untested.
4. Body-pose finders (e.g. MediaPipe): trained on photos of real people; Claude expects them to do badly on our flat drawings. Untested.
5. A model that watches video directly: some other companies' models do; none available in this setup; how well it would work: unknown.
Other facts:
- A download of the people-building files was blocked here on 26 Nov (preflight git clone of makehuman failed): new downloads may need the environment's network widened.
- Existing seeing aids: stills, clips, contact sheets, critique.py (rule 89), handcheck.py, humancheck.py, preflight picture_faults (geometry from plan depths).
- Chat 36: 9 picture-check flags; 3 looked at by eye were mostly intended crowd overlap (notes/proposals/check-knows-intent.md).
- The first route's winner: a test set from Sam's past movement and clipping notes, tried cold by a fresh helper, and a "path picture" per movement (faint in-betweens, hand and head paths): notes/proposals/better-seeing-tools.md.
Chat's own pick: 1 first, then 2; 3 only after a test; 4 not recommended; 5 not available.

## Record
notes/proposals/better-seeing-tools.md
notes/proposals/check-knows-intent.md
source/film_engine.py
source/preflight.py
source/critique.py
source/handcheck.py
source/humancheck.py
guides/film-quality-rules.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 91765efde6dce005 -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = chat, V3 = helper B. Picked: V2 (chat). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes: the Facts end with the chat's own pick ("1 first, then 2; 3 only after a test; 4 not recommended; 5 not available") and call candidate 1 "Claude's pick, cheapest". V3 is that pick restated.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 5 | 21 |
| V2 | 5 | 4 | 4 | 4 | 5 | 22 |
| V3 | 2 | 2 | 3 | 2 | 4 | 13 |
## Sam test
Q1: Yes: an expert uses the exact positions the engine already has, and tests each outside tool on Sam's own saved notes instead of ranking them by opinion; the final also tries the person cut-out model already in the project before installing a heavy new one.
Q2: Evidence is two films' saved notes (Brexit Is Done motion notes 13, 14, 15, 19, 22, 23.1, 23.3, 23.4; GTA v5 contact notes 2-6, 8, 9, from the first route's verdict), the existing bench as baseline, and moves Sam passed for false alarms. Wide enough; not one chat.
Q3: Root cause named (every look is one instant; checks read plan depths, not what was drawn; nothing tuned on motion notes). Success is a counted catch rate per candidate; the winner is added by code to every movement clip, not left to a chat's choice.
Q4: Build-now, engine-data reframe, learn-first and wait-for-video were weighed; learn-first compares all five plus today's stills on equal terms.
Q5: The learn step changes nothing in the films; each later change has its own yes, its own target and comes out alone. Nothing untested is asked to be trusted.
Q6: Installs (OpenCV 5.1, MediaPipe 1.2.3, onnxruntime 1.29, no torch), the models folder, the hand check's coverage, the bench rows and the ledger were checked here. Costs, the bench's denominators and whether downloads finish are marked unchecked.
Q7: Sized by catch rate, not price; the cheap trap (build candidate 1 untested, drop 4 unseen) is rejected. Honest cost stated.
Q8: Results become permanent shared tools with kit tests or are written down as tested and not used, with their score; reviewed when Sam declares the next film complete.
## Pick
V2
## Why
V1 and V2 both see the real decision: which way of looking, over a whole film's movement shots, catches the motion and contact notes Sam has had to give, with fewest false alarms, and an honest tried-or-cannot line for each of the five by name (what the first route failed to do). V2 wins on evidence and completeness: it adds GTA's contact notes, keeps today's stills and the first route's path picture as baselines, notes MediaPipe is already used here, splits contact and motion into separate yeses, names optical flow's likely weakness on flat colour as something to measure, and says plainly what candidate 5 would need (another company's service, a key, Sam's yes to send frames out). Taken from V1: run candidate 3 through the already installed onnxruntime rather than installing torch; set motion tracing's numbers beside the engine's own numbers to show which is truer; aim candidates 3 and 4 at what the engine cannot see (the 3D bodies, old animatics, Sam's reference photos). Neither version noticed that a person cut-out model already sits in the project (the selfie segmenter used for likeness work); it is now candidate 3's first try. V3 is the leaked pick, untested and unsized.
## Faults in the pick
- F1 [fixed] Candidate 3 planned to install torch, a heavy install that may not fit the session; now tries the cut-out model already in the project first, then a small exported model through onnxruntime, and only says "cannot here" if both fail.
- F2 [fixed] Candidate 3 and 4 were run only on our own frames; now also on the 3D bodies and old animatics (which the hand check cannot see) and 4 on reference photos.
- F3 [fixed] Motion tracing had no truth to compare with; now set beside the engine's exact positions.
- F4 [named] The bench catch counts (2-4 of 7, 2 of 12) rest on V2's own reading of a table with no totals column: unchecked.
- F5 [named] Candidate 5 cannot be done here; Claude still sees only pictures made from motion, never the motion itself.
- F6 [named] All costs unchecked; whether model downloads complete is unchecked.
## Final version
**Learn (changes nothing in any film; Sonnet; about 2.5% of a week, unchecked).** Test set: the bench's existing cases plus Brexit Is Done motion notes 13, 14, 15, 19, 22, 23.1, 23.3, 23.4 and GTA v5 contact notes 2-6, 8, 9, rebuilt from the commit Sam saw, plus five moves Sam passed (for false alarms). Baselines: today's stills and critique pack, and the first route's path picture (faint in-betweens, hand and head paths from engine data). Each of Sam's five, by name:
1. Who-is-where colour copy: extend the hand check's key-colour redraw to every person and prop, stacked in drawing order, every frame of the move.
2. Motion tracing (OpenCV, installed): frame-to-frame movement on the rendered clip, printed as jumps and vanishings, beside the same numbers from the engine. Weakness on flat fills measured, not assumed.
3. Cut-out model: first the person segmenter already in the project, then one small exported model through onnxruntime if it downloads; run on old animatic frames and the 3D bodies. If neither works: "cannot here; needs X", named.
4. Pose finder (MediaPipe, installed; pose model fetched if reachable): on our frames, the 3D bodies, and Sam's reference photos.
5. Video-watching model: cannot be done here; needs another company's service, a key added in the environment settings, and Sam's yes to send frames out. Not attempted.
A fresh helper who has not seen the notes scores each cold: caught, missed, false alarms. Sam gets one table, one line per candidate.

**Then one change per yes, each with its kit test, each undone alone, all advice only (rule 93):**
- Change A (contact): the best contact view is added by code to every critique pack and movement clip. Beat: more GTA contact cases than stills, at most 1 false alarm on passed moves, no lost bench catches.
- Change B (motion): the best motion view, same terms; beat at least 6 of 8 Brexit motion cases.
- An outside tool is kept only if it catches cases the engine views missed; else written down as tested and not used, with its score.
Each change about 1.5-2.5%; later films about 0.2% each (unchecked). Reviewed when Sam declares the next film complete: its movement and contact notes against Brexit Is Done's.
Lost: nothing. Added: a test set from Sam's notes, a scored line for each of the five, then up to two shared views.
## For Sam
### Option 1: Test all five on your old notes, then keep the winners
Problem: I only see still pictures, so faults between frames (a hand's path, touching, who is in front) reach you or get flagged wrongly. You asked what each of the five tools I named could do, and the last answer dropped them.
1. Gather your past notes about movement and touching from Brexit Is Done and GTA, plus five moves you passed, and redraw them as you saw them.
2. Try each of the five on them: the colour copy of who is where, the frame-to-frame movement measure, the picture cut-out tool, the body-pose finder, and a video-watching model (this last one cannot be done here: it needs another company's service, a key and your yes to send pictures out, so I will say so, not fake it).
3. A fresh helper who has not seen your notes scores each: what it caught, missed and wrongly flagged.
4. You get one table, one line per tool. Then you say yes or no to each winner, one at a time, for touching and for movement.
Why: it answers your question about all five with results, not my opinion, and only keeps what actually catches your notes.
You'd notice: a short table naming all five; later, a coloured copy or path picture with movement clips, and fewer repeated notes on hands and who is in front.
Other option: build the colour copy straight away and drop the rest untested.
Lost: nothing; stills, sheets and current checks stay.
Added: a test of the five on your old notes, about 2.5% of a week once; then up to two new ways of looking, about 2% each, and a little per film.
### Option 2: Build the colour copy and movement measure now
Problem: I only see still pictures, so faults between frames (a hand's path, touching, who is in front) reach you or get flagged wrongly.
1. Make a second copy of each frame where every person, hand and prop is one flat colour.
2. Add the frame-to-frame movement measure to every movement clip.
3. Leave the picture cut-out tool and the pose finder untried, and say the video-watching model cannot be done here.
Why: quicker and cheaper; it is what I first suggested.
You'd notice: the new pictures sooner, but no proof they catch your notes, and two of the five never tried.
Other option: test all five on your old notes first.
Lost: a fair test of the cut-out tool and pose finder.
Added: two new ways of looking, about 4% of a week once, untested.

## Sam's pick (26 Nov, chat 36)
"1. Y but lose option 5": option 1 adopted, testing four tools (colour who-is-where copy, frame-to-frame movement measure, picture cut-out tool, body-pose finder); the video-watching model is dropped.
