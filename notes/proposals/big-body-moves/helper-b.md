# Helper B: big body moves and a human-body check

## Leak
Lesson 10 (key poses per angle, layered by hand) and a two-part build; weighed, not assumed.

## Results
- Shot 4: four versions; version 4 drew 16 notes, 8 from one cause, a flat figure bent toward 3D points (notes 2, 3, 4, 6, 7, 8, 11, 15) (case study s.7 A).
- Version 4 passed the point checks; the critique (rule 89) was not run, as with version 3 (case study s.7 E). `source/finish.py` has no critique step, so it is optional in practice.
- 11 past notes on body placement (critique checklist P7, lines 29, 81).
- Film: estimated 53.2% of a week, spent 27.71%, forecast 78.2% (ledger). Gap: the ledger is per chat, so shot 4's own cost cannot be read.
- Existing means: `lying.py` (3D skeleton), `lying_flat.py` (draws it with the house's own flat torso views, sleeves, legs, head; nearer pieces over farther), `lying.solids` (limbs into the every-frame collision test, rule 5); cars are 3D (catalogue row 77). Listed for lying only (row 70); never used upright.

## The real decision
For every film: what a person is built from once they leave the tested standing and seated poses, and how judging by eye becomes unskippable. The body's build is the bigger lever: a real skeleton gives joins, lengths, sides and depth by construction.

## Root cause
No 3D body existed: a flat drawing was bent by a flat arm solver toward 3D points, depth faked by masks at three points, and a turn swapped the drawing while arm targets and draw order stayed front-facing. The check tested points because points were all the shot had. The 160-degree fix was judged on one frame (lesson 12). Both bad versions shipped because the critique is a written rule no tool enforces.

## Approaches weighed
1. Key poses per angle, layered by hand: new drawing per move per film; repeats the mask fault; still needs a check.
2. Reframe: one 3D skeleton for every big move, drawn with the flat house pieces; depth per piece against 3D cars; "human" measured on the skeleton.
3. Check-only: cold critique every 0.25 s, enforced at sending; catches, builds nothing right.
4. Learn first: measure what the existing means would have caught on version 4.

Chosen: 4, then 2, then the gate from 3, each its own yes.

## Proposal
**Learn (changes nothing; about 1% of a week, unchecked).** (a) A fresh helper critiques version 4 cold: how many of the 8 notes it names. (b) Pose the skeleton through shot 4's existing 3D keys, draw with `lying_flat` at 6 moments, one sheet beside version 4 at full and phone size; run the collision test against the car; count faults. (c) List what is missing upright.

**Change 1, body route (only if (b) reads human).** Big moves (climbs, turns past side-on, leaning out, car doors, falls) use the skeleton; pre-flight refuses one built on the flat standing figure. Beat: 0 cause-A notes on shot 4's next animatic, 0 collision faults every frame, 0 repeated body notes on the next film's big move. About 3% once (unchecked).

**Change 2, human-body check.** On the skeleton: limb lengths within 3%, elbows and knees in human range, each arm on its own side, no limb through another; on the drawing: each piece touches its parent, gun within 10 degrees of target. Runs in pre-flight and finishing; a fault blocks unless named. Beat: flags notes 3, 6, 7, 8 on version 4's poses, 0 false flags on the pose gallery. About 1.5%.

**Change 3, critique gate (only if (a) caught 6 of 8 or more).** Finishing refuses a clip without a critique record for that render. Beat: 0 clips sent uncritiqued. About 0.3%.

Total about 6% once (unchecked), against 15% a film. Sam sees one sheet, then shot 4's build proposal (rule 8), then each change as its own Y.

## Sam test
- Q1: Fixes the body's build and enforces review, not more masks.
- Q2: Evidence: shot 4 plus 11 past notes; tested on real frames first.
- Q3: Root cause named; enforced by tools, not reading; numbers to beat.
- Q4: Four different approaches; this removes the cause, the others catch it.
- Q5: Learning changes nothing; each change undoes alone.
- Q6: Sources named; estimates and the look marked unchecked.
- Q7: Sized to the result, added only as evidence earns it.
- Q8: Each change permanent when made, reviewed at film end.

## Lost / Added
- Lost: hand masks for big moves; sending without a critique.
- Added: learn sheet; skeleton route; human-body check; critique gate.

## Unchecked
Whether Sam accepted `lying_flat`'s look (Job I); whether cars give per-pixel depth; all costs; shot 4's own cost.
