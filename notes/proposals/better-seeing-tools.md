# Proposal: Better ways for Claude to look at our images and animations

Status: replaced:seeing-five-candidates (2026-11-26)

## Problem
Claude can read only still frames, one at a time or on a sheet, and cannot watch motion. Judging hands, limbs, contact and movement from stills is the weak point: checks flag the wrong things or miss faults, and Sam (26 Nov, chat 36) asked whether any tools or programs would improve how Claude looks at the project's images and at its own drawings and animations, beyond what it does now. Checks must never block requested work (rule 93).

## Facts
- Chat 36 animatic: 9 picture-check faults from geometry checks (source/preflight.py picture_faults, plans depth); looking at three stills showed mostly intended overlap; the checks cannot read intent (notes/proposals/check-knows-intent.md).
- The films are drawn by our own engine (source/film_engine.py, brexit_is_done.py), so a second flat-colour copy of each frame (one colour per person, hand, prop) could be drawn by the same code: untested.
- Frame-to-frame motion measuring, person/hand cut-out picture models and pose finders exist outside the project: none tested on our drawings; pose finders are trained on photos, our people are flat drawings: unchecked.
- A container download of the people-building files failed on 26 Nov (preflight: git clone of makehuman blocked): network access to new tools is limited here.
- Existing seeing aids: critique.py (rule 89: a fresh helper reads a pack of pictures), stills and clips, body check and hand check, humancheck.
- Whether any video-watching model is available to this setup: unchecked.

## Record
notes/proposals/check-knows-intent.md
source/film_engine.py
source/preflight.py
source/critique.py
source/handcheck.py
source/humancheck.py
guides/film-quality-rules.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 707a1c41e3354d35 -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = helper B, V3 = chat. Picked: V2 (helper B). Critiqued: 7 found, 4 fixed, 3 named.

## Leak
yes: the Facts line "a second flat-colour copy of each frame (one colour per person, hand, prop) could be drawn by the same code" names a remedy, and the list of outside tools (motion measuring, cut-out models, pose finders) names three more. V3 is exactly that anchored answer. (The flat-colour copy also already exists in part: the hand check draws each person again in key colours, source/handcheck.py header, which the problem file does not say.)
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 5 | 21 |
| V2 | 4 | 5 | 4 | 3 | 5 | 21 |
| V3 | 2 | 2 | 3 | 2 | 4 | 13 |
## Sam test
Q1: Yes, as fixed: an expert measures today's seeing against the client's own saved notes, uses the exact positions the program already knows before guessing from pixels, and tests one outside tool only where it can be installed, saying plainly where it cannot.
Q2: Evidence is two films (Brexit Is Done movement and contact notes 13, 14, 15, 19, 22, 23.1, 23.3, 23.4; GTA v5 notes 2-6, 8, 9) plus the existing critic bench, and passed films for false alarms. Wide enough for the decision.
Q3: Root cause shown with the notes' own "should have caught" lines: every look is one instant, and the time checks that exist were tuned on sheets, not on passed films, or never run on the film. Success is a counted catch rate on saved notes; the new picture is added by code to every movement clip and critique pack, not by a chat choosing to.
Q4: Outside tools, a motion picture drawn from the engine, the flat-colour copy, calibration of existing checks, and learn-first were all weighed; the learn step itself compares them on the same notes.
Q5: Nothing is built before the measurement; each change has its own yes and each check is adopted alone, so a failed one comes out without touching the rest. Not asked to trust anything unshown.
Q6: Notes, ledger, bench scores, tools installed (ffmpeg, OpenCV 5.1) checked. Ledger now reads 63.2% spent (versions quoted 62.76%: fixed). Costs and video-model availability unchecked.
Q7: Sized by the catch rate it must reach (numbers to beat), not by price; the cheap trap (more stills, or V3's untested tool list) is rejected.
Q8: Permanent shared tools with kit tests; the learn step is a measurement, not a trial; reviewed when Sam declares the next film complete.
## Pick
V2
## Why
V1 and V2 both see the real decision (motion and contact faults across the whole film, judged against Sam's saved notes) and both learn first. V2 wins on reuse and evidence: it builds on the existing critic bench, measures today's pack as a baseline, adds the GTA notes, notices the key-colour copy already exists, and fixes the calibration root cause behind 23.1 and 23.4. Its faults were a bundled second yes, an untested rejection of outside tools (Sam asked about tools), and GTA single-frame clipping cases scored against a motion sheet. From V1 I took: comparing several views cold in the learn step, one outside tool tried if it installs, false alarms counted on moves Sam passed, and one yes per check. V3 is the problem file's hint restated, untested and unsized.
## Faults in the pick
- F1 [fixed] Change 2 bundled four checks' recalibration into one yes; now each check is adopted alone (from V1).
- F2 [fixed] Outside tools rejected without a test; now one pose finder and one motion measurer are tried in the learn step if they install, else said plainly.
- F3 [fixed] GTA clipping cases are mostly single-frame contact faults; they are now scored against the key-colour copy, not counted toward the motion sheet's target.
- F4 [fixed] Spend figure updated to the ledger's 63.2%.
- F5 [named] No video-watching model is known here; Claude still cannot watch motion, only pictures made from it.
- F6 [named] Engine positions cover only people drawn by the satire kit's flat people, not the steep-camera 3D bodies.
- F7 [named] All costs are estimates.
## Final version
**Learn (changes nothing; Sonnet; about 2% of a week, unchecked).** Add bench cases from Brexit Is Done notes 13, 14, 15, 19, 22, 23.1, 23.3, 23.4 (motion) and GTA v5 notes 2-6, 8, 9 (contact and clipping), rebuilt from the code as Sam saw it, plus five moves Sam passed. A fresh helper who has not seen the notes scores, cold, each view: (a) today's critique pack (baseline); (b) a motion sheet from engine data: faint overlaid in-between drawings, hand and head path lines, a who-is-in-front lane strip; (c) the existing key-colour copy from the hand check, stacked in drawing order; (d) one outside pose finder and one frame-to-frame motion measurer, only if they install here, otherwise recorded as "cannot be tried here". Also record whether each check's numbers already showed the fault. Result: caught, missed and false alarms per view.

**Change 1 (own yes; Opus high; about 2.5%).** The best view for motion (expected: the motion sheet) becomes shared, added by code to every movement clip and critique pack, with its kit test. To beat: at least 6 of the 8 motion cases cold, no lost Blessed or Remakes catches, at most 1 false alarm on the passed moves. If the key-colour view catches most GTA cases, it goes into the pack too, on the same terms.

**Change 2 (one yes per check; about 0.5% each).** Move size, read time, cover order and gesture path each get limits measured from films Sam passed and are run on the whole film every animatic; each is adopted only if it catches its saved notes with no false alarm on passed films. Advice only, never a lock (rule 93).

Later films: about 0.2% a film. Reviewed when Sam declares the next film complete: movement and contact notes against this film's 8.
## For Sam
### Option 1: Test on your old notes, then build what wins
Problem: I can't watch movement, only still pictures, so faults that happen between frames (a hand's path, a too-quick pounce, runners swapping who's in front) reach you. Nobody has measured which way of looking would have caught them.
1. Turn your past movement and clipping notes from the last two films into a test set, plus five moves you passed.
2. A fresh helper who hasn't seen your notes tries each way of looking cold: today's pictures; one picture per movement showing faint in-between drawings and the path of each hand and head; a coloured copy showing who is in front; and one outside program, if it can be installed here.
3. The way that catches most becomes part of every movement clip, on its own yes.
4. Each movement check gets its limits set from films you passed, one yes per check.
Why: it fixes the looking, not one frame, and only builds what proved it catches your notes.
You'd notice: movement clips come with one "path picture", and fewer notes about hands, speed and who runs in front.
Other option: build the path picture straight away without testing first.
Lost: nothing; stills and sheets stay.
Added: a test set of your old notes, one path picture per movement, better-set checks; about 5% of a week once, then a little per film.
### Option 2: Build the path picture straight away
Problem: the same: I can't watch movement, so faults between frames reach you.
1. Make one picture per movement showing faint in-between drawings and each hand's and head's path, added to every movement clip.
2. Test it once on your past movement notes.
Why: it is quicker to start and turns movement into a still I can read well.
You'd notice: path pictures with clips sooner.
Other option: test several ways of looking on your old notes first, then build the winner.
Lost: the comparison with other ways of looking, so it may not be the best one.
Added: one path picture per movement; about 2.5% of a week once.
