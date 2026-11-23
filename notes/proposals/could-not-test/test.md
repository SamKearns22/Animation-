# could-not-test: the Milburn replay (the learning step; changed nothing)

Chat: session_01U3pKR1xydztyQLbhMiM5M9 (Opus high, 22 Nov). Versions replayed (saved code, each checked out on its own):
chat 12 = 4f5ece1f (animatic 1, Sam's chat 13 note on it), chat 13 = e03bf0b6 (cards moved), animatic 3 = f4c1d0d5
(Sam's chat 18 note on it), chat 18 fix = d0f06955 (Milburn's card at depth 1.32), final code = 6dc5df69 (card 1.44).
Every table shot (4a 4c 7a 7c 7e and 1 4b 7b 7d), one frame each 0.5 s: 96-99 frames per version.
Sam's words: chat 13 "Move name placards so Andy and Pat's arms don't clip through -- how did it pass clipping
check?" (notes/ledger/sam/agnagzd2.md); chat 18 "his sleeve clipped its edge at 3 s" (story/milburn-places.txt).

## How
- (a) The clipping check's drawing-order rule (clipcheck.py order_faults: a layer drawn later must not be further away
  than one it covers, 0.05 m slack), fed automatically: every room piece the places painter draws became its own layer
  at its own depth (the painter already knows it); every person their own layer, depth = seat to seat minus 0.45 m
  (hands reaching forward). Who is on top was read from the real frame. Script: the scratch replay.py (not kept).
- (b) Readability: each name card's share covered by the caption, the caption drawn as finish.py draws it, on the
  code's own frames; then the posted video itself looked at (1.5, 19.7, 26.9, 41.5, 48.5 s).

## (a) Clipping check, fed the painter's pieces
| version | Andy's card | Pat's card | Milburn's card | false alarms |
|---|---|---|---|---|
| chat 12 | flagged 20 of 50 reverse frames | flagged 50 of 50 | flagged 46 of 46 | 1 pair (Milburn's hands on his papers), every frame |
| chat 13 | clean | clean | flagged 46 of 46 (the repeat note) | same 1 pair |
| animatic 3 | clean | clean | flagged 50 of 50 (Sam: sleeve at 3 s) | same 1 pair |
| final code | clean | clean | clean | same 1 pair |
- Caught: all 3 hand/sleeve card faults, at the first animatic. Milburn's would have been caught two rounds before Sam
  noted it. Each fix reads clean afterwards. The verdict's F4 ("unproven whether it flags a hand over a card"): answered,
  yes, with pieces fed one by one.
- False alarm: 1 (hands resting on flat papers lying on the table: touching, not passing through).
- Weak spot: the person's depth was my guess (0.45 m reach). At 0.6 m, Andy's and Pat's cards (1.6 m against seats at
  2.2 m) would NOT flag. The cover must take each arm's real depth from the pose (the check's solids), not a guess.
- Not run: the painter's four whole layers (back, mid, front, over) as four blocks. The front block holds the cards
  and the table top together, so reasoning says it flags every arm on the table or none. Per piece is needed.

## (b) Captions over the cards
- The posted final (animations/milburn-vertical.mp4): Milburn's card is cut by the caption in shot 1 (1.5 s, "report
  is quite simple.": the lower half, "Milburn" crossed) and shot 4b (26.9 s, "Milburn" crossed). The notes said "the
  caption's top edge touches, name readable".
- Why the notes missed it: those shots in the posted video were drawn with the card at depth 1.32 (pixel match:
  box 95-289 x 1376-1468), though the code was moved to 1.44 at 10:11 and the final committed at 10:23. Re-drawn from
  the code, the card is clear. A check that re-draws from code says clear; the posted film is not.
- On the 1.32 version's frames: 20-28% of Milburn's card under captions in shot 1 from 0.5 s; 34 of 148 sampled card
  frames 5% or more covered (shots 1, 4b, 7b, 7d), worst 42% (7d).
- Earlier versions' frames: Milburn's card up to 70% under the caption in 7d (chats 12, 13, animatic 3). Those
  animatics are not kept, so not confirmed on video.
- False alarms: Andy's and Pat's cards 16-20% covered on re-drawn frames from chat 13 on, but three posted frames
  (19.7, 41.5, 48.5 s) show the captions clear below them. Re-drawn caption placement is not trustworthy: 2 false alarms.
- The clipping check, even fed, cannot see any of this (captions go on after the picture).

## (c) COULD NOT TEST on recent films
- 3 of the last 4 films give the check nothing (no solids, no layers), so it printed COULD NOT TEST: Milburn,
  Blessed (draw_order only), Grand Theft Autism at film level (its car checks run inside two shots only). Protest Tiers
  feeds solids. Ledger rounds keep pre-flight output for Milburn only (round-0, twice).
- Faults behind it on Milburn: 3 (Andy and Pat's cards, Milburn's card) plus the caption cut that reached the post.
  Blessed's (rule 19's start, 13 Nov): not looked up.

## What it means for step 2
1. The stop: needed (3 of 4 films ran blind).
2. Cover by default: proven. Feed each painted piece at its own depth, people with their arms' real depth from the
   pose; flat things under resting hands allowed. Number to beat: chat 12 flags all three cards, final is clean, 0 false
   alarms (today 1).
3. Stays readable: proven needed; the only thing that sees the caption cut. It must measure the frames actually
   rendered (the render keeps each listed thing's box per frame, finish.py checks captions against them), not re-draw
   from the code. Number to beat: catches shots 1 and 4b of the posted final; Andy and Pat clean.

Cost of this test: see the ledger line for this chat.

## Sam's pick on the step-2 ask (22 Nov)
"1": all three together: (1) the stop no chat can skip (pre-flight, the render tool and finish.py; the only way past
is the check's own Exceptions line with Sam's Y); (2) cover by default: the places painter hands each piece to
clipcheck at its own depth, people with their arms' real depth from the pose, flat things under resting hands
allowed; number to beat: Milburn at chat 12 flags all three cards, final code clean, 0 false alarms; (3) stays
readable: listed things (cards, signs, faces) measured against captions and Hook Text on the frames actually
rendered (the render keeps their boxes per frame), not re-drawn from code; number to beat: Milburn's posted shots
1 and 4b caught, Andy's and Pat's cards clear. Stop lands with the cover, never before it. About 5-6% of a week once.

## The build (chat session_01U3pKQzaw3rkdJXunde285d, Opus high, 23 Nov): all three parts, tested
Branch claude/could-not-test-build, merged to the main line. Replays run on each saved version (worktrees, the new
cover copied in, the taps patched into that version's painters), every table shot one frame each 0.5 s.

### (2) Cover by default (cover.py): numbers before and after
| version | Andy's card | Pat's card | Milburn's card | false alarms |
|---|---|---|---|---|
| chat 12 (4f5ece1f) | flagged 17 frames (shot 4c) | flagged 49 (4a) | flagged 46 (shot 1) | 0 (replay: 1) |
| chat 13 (e03bf0b6) | clean | clean | flagged 46 | 0 |
| animatic 3 (f4c1d0d5) | clean | clean | flagged 49 | 0 |
| chat 18 fix (d0f06955) | clean | clean | clean | 0 |
| final code (6dc5df69) | clean | clean | clean | 0 |
- Arms at their REAL depth from the pose: views.person draws each arm also on a clear layer (cover._arm), its depth
  from shoulder, elbow and wrist (Andy's and Pat's forearms 1.82-1.87 m against their cards at 1.6 m: flagged without
  any reach guess). Pieces: every places piece is its own layer at its own depth (near to far for things lying flat).
- Who is in front is read from the real frame; a pixel another layer also explains, and 1-2 px outlines, prove
  nothing (removed: the fireplace-over-chair and white-shirt alarms seen while building).
- Flat things (papers, folders, coasters, table tops) under anything resting on or above them are allowed: the
  replay's one false alarm (Milburn's hands on his papers) is gone.
- About 26 s for 95-97 frames on 4 processors.

### (3) Stays readable (render record + finish.py): numbers
- The render (film_engine) keeps, beside the video, every drawing's box for each text piece the painter drew (name
  cards, signs, notices, cans) and each KEEP_CLEAR box (VIDEO.readable.json); finish.py measures the captions and the
  Hook Text against them. A thing with words is measured on its words band (the middle of its box), 5% the bar.
- The posted film is a splice: shots 1 and 4b drawn with the card at 1.32 m, 7d at 1.44 m (checked on the posted
  pixels: the card's box white 0.60 / 0.59 at 1.32 against 0.33 at 1.44 for 1.5 s and 25.0 s; 0.77 at 1.44 for 56.5 s).
  On that mix the check flags shot 1 (17-20% of the name under "report is quite simple.") and shot 4b (11-30%), and
  nothing else. Andy's and Pat's cards clear (0 false alarms; the replay had 2). The final code alone: clear.
- First version measured the whole card box: Andy's and Pat's flagged 13-19% where the caption only touches their
  card's lower edge (posted frames 18.0 and 44.0 s show the names readable): fixed by the words band.

### (1) The stop no chat can skip
- Pre-flight puts every clipcheck COULD NOT TEST in its pass stamp ("untested"); the render tool (lock_fault) and
  finish.py refuse while any is there, before --faults-named is looked at. The only way past: a row in the notes'
  "## Exceptions" | clipcheck | could not test, or the shot | why, with Sam's Y | looked at |.
- COULD NOT TEST now means: nothing the film draws was recorded, or a shot's people were drawn with no depth (no places
  view lists them, no cover.person). It lands only with the cover: Grand Theft Autism (started before, no places views)
  keeps the old nameable fault (preflight.COVER_BEFORE) until its chat wraps its people in cover.person.
- satire_template draws its wall, floor and table inside cover.thing and its people inside cover.person (clean).

### Every change (for the end-of-film review; each part undoes on its own)
1. NEW source/cover.py (the recorder, the analysis, the readable measure).
2. source/places.py painter: each piece inside cover.piece (no cost when not recording).
3. source/views.py: TAP hooks (start, mid, head) for cover; nothing when not recording.
4. source/clipcheck.py: MAP says the cover feeds it by default.
5. source/preflight.py: cover_faults on every 3rd frame of a film with people; untested in the stamp; untested_waived
   (the Exceptions row with Sam's Y); COVER_BEFORE (GTA). Undo (1): drop the untested list from write_pass.
6. source/film_engine.py: write_pass keeps untested; untested_fault refuses before --faults-named; the render records
   each drawing's boxes (.read.json in the cache, VIDEO.readable.json beside the video). Undo (3): remove that record.
7. source/finish.py: the readable check (refuses unless --faults-named; a clean video with no record: COULD NOT TEST,
   nameable), the untested stop, the record copied with the kept animatic.
8. source/satire_template.py: set and people inside cover.thing / cover.person.
9. source/kittests.py: could_not_test_cover, could_not_test_readable.
- Cost note: the first render of each film after this re-draws its cached frames once (each needs its record).
