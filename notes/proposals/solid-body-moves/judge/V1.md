# Helper A: solid body moves

## Leak
The title and the "industry practice" fact point to Blender. Sam himself asked for 2.5D or 3D, so 3D stays; Blender is weighed, not assumed.

## Results
- 14 attempts, chats 6-31, all FAILED. Sam stopped the work on 22 Nov (case study section 17).
- Sam's notes: 16 on version 4, 10 on version 7, the arm fault a third time on version 8, animatic v3 "riddled" (sections 7, 15, 17).
- Cost: 62.62% of a week spent, against a 53.2% estimate and the 15% aim, over 32 chats (notes/ledger/grand-theft-autism.md). Shot 4's share is unchecked (no split by shot).
- The poses were not at fault. The skeleton measured as human at all six moments tested; "the horror came from the flat drawing method" (section 10).
- The car is drawn in painter's order: whole parts stacked back to front, with no depth test for each dot of the picture (gta_cars.py, the MAP's draw_car line). Jason is separate pieces, and a hand-made map decides what the car hides (leanout.py MAP).
- Hands: Sam said only "so many problems with hands" (notes/ledger/sam/xt7jubnm.md); leanout.py lines 267-268 credit chat 26's words to him.
- Blender 4.0.2 is offered by the package list but not installed, and bpy is missing (both checked). Whether it renders headless here is unchecked.

## The real decision
How to learn a drawing skill outside a live film, against a pass bar set first, for every future showstopper. Bigger levers: one depth test shared by body and car, a pass bar from every past note, a look lock.

## Root cause
Body and car are separate flat drawers, stacked in a hand-set order. Each joint is an ordering guess, so every fix moved the fault to the next join. Hands changed because nothing guards the approved look or checks that words credited to Sam are his.

## Approaches weighed
1. **One solid scene** (learn-first): the posed MakeHuman body, circle hands as solids at the wrists, and the 3D car in one picture, with a depth test for every dot. Flat house colours, outlines from edges and part borders, the house face on top. Overlaps become impossible.
2. **Reference-led 2D**: pose the flat pieces to motion capture or a phone clip. The poses were never at fault. Rejected.
3. **Reframe: a skill bench**: a standing test space with three moves (lean-out, getting into a car, a fall). The frame, not the method.
4. **A collision check on the current pieces**: it finds faults but cannot draw them right. Rejected.

Chosen: 1 inside the frame of 3.

## Proposal
**Learn (changes nothing; about 2.5% of a week; one Opus high chat):**
- (a) Turn every Sam note on shot 4, and the faults from chats 28-31, into one numbered pass list with pictures, and name what the body check misses.
- (b) Install Blender. Test a headless render with outlines on the processor alone. Time it against a numpy depth test of the MakeHuman mesh,, keep what renders correctly.
- (c) One still from shot 4's camera: seated Jason the solid way beside the approved Jason, phone size.

**Then, one change at a time, each on Sam's own Y:**
1. **Look lock** (about 1%): pre-flight refuses a change to approved look parts (circle hands, outline weight, flat fills, the face) unless the notes quote Sam word for word from notes/ledger/sam. To beat: it refuses chat 28's change.
2. **The solid way of drawing** in the test space (about 4%). To beat: Sam's Y on "same style?", and a cold judge cannot pick it out at phone size.
3. **The move in the test space** (about 4%). To beat: 0 faults on the pass list, the body check at 0 (it was 11), and the strip check at 0 (the film's baseline is 311). Then Sam's Y on the clip.
4. Shot 4 back in the film is Sam's separate decision.

Total about 11.5% of a week, once, for a skill every film keeps. Sam sees one still and one clip.

## Sam test
Q1: the method is fixed at its root. Q2: the bar comes from every note across 25 chats. Q3: enforced by checks and pre-flight, not by a chat choosing to read. Q4: four approaches weighed. Q5: nothing enters the film without Sam's Y; each change undoes alone. Q6: sources named, gaps marked. Q7: sized to remove overlaps, not patch them. Q8: permanent once passed, reviewed when the film is complete.

## Lost / Added
Lost: shot 4's per-part patch tools once the solid way passes. Added: Blender (if chosen), a test space, a look lock, a pass list.

## Unchecked
Headless Blender here; render time; the solid look matching the house; shot 4's cost share.
