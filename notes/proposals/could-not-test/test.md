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
