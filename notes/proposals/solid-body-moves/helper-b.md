## Leak
Yes: title and facts point at a remedy (3D skeleton, Blender, Line Art). Sam's asks kept as brief; tool chosen fresh.

## Results
- 14 attempts over 25 chats, all FAILED (case study section 17).
- Film cost 62.62% of a week, against 53.2% estimated and the 15% aim (ledger). Shot 4's share is unchecked (no shot tag); 25 chats at about 2% each is roughly 40-50%.
- Sam's notes: 16 on v4, 10 on v7, then "the exact same arm problem" a third time (case study 7, 15, 17). The ledger shows only "3 notes". **Gap:** it cannot measure the "fewer notes" aim.
- Strip check stayed at 311 fault lines after chat 30's fixes, none gone (film notes).
- Recent faults all sit where things meet: seal through arm, smears, post at mouth, elbow outside door (chats 30-31).
- Hands: chat 28 built fingered hands, crediting chat 26's own labels to Sam (problem file; archive line 443).

## The real decision
How the project gains and proves a whole-body move skill in the house look before any film relies on it. Bigger levers than "which tool": one source for what hides what, one for the look.

## Root cause
1. **Hiding is guessed, not measured.** Bones are flat pieces. A hand-made map (`_cover`) gives each pixel the car-hiding of the nearest bone on screen. That guess breaks wherever pieces meet each other or the car. Each fix added a special case; faults moved, not went.
2. **Four drawing methods joined by fades** (flat pieces, 3D hand, arm, head). Fades cause smears; separate inks drift the look.
3. **Moves invented without reference or a plan for the joints.** The shoulder slid over the planted hand, leaving only impossible elbow bends (chat 30).
4. **Learned inside the film,** a note at a time (Sam's diagnosis; the record agrees).

## Approaches weighed
- **A. Blender** (toon shading, Line Art): standard, but untested headless (unchecked); its lines and colours are not the house's.
- **B. One in-house pass:** pose MakeHuman's mesh by its own skin weights (`mhuman.py`); draw it with the car's 3D shape and the gun in one pass that keeps each pixel's depth and part; house colours and ink on outline and part borders; circle hands as 3D parts.
- **C. Reframe, motion first** (learn-first): get the move right as a grey 3D figure from reference footage with planted contacts, judged before any look.
- **D. Reframe the process:** a permanent test bench outside films; a new skill passes a viewer bar on a clip first.
- **E. Hand-drawn keys per view:** tried (big-body-moves), failed.

**Chosen:** D, then C, then B (causes 4, 3, 1-2). A only if B is too slow.

## Proposal
**Learn first, changes nothing (about 2.5%):**
- **L1.** Sort every fault and note since v4 by cause (hiding/joins, look, motion); the hiding share confirms B. Cost shot 4 chat by chat.
- **L2.** One single-pass frame at film size: seconds per frame, hiding checked by eye; whether Blender runs.
- **L3.** 3-5 reference clips of someone leaning out of a car window and back; key poses, planted contacts.

**Then one change at a time, each needing Sam's Y on a clip:**
1. **Test space (C):** Jason seated and the window only, shot 4's locked camera, a grey figure doing the L3 move. Bar: 0 body-car crossings tested every 1/24 s; no joint jump over 3 cm a frame; contacts held. A script prints them into the handover. About 5%.
2. **House render (B)** of that move. Bar: 0 strip faults (from 311); a side-by-side with Jason's approved seated frames (same colours, line width, circle hands); the stranger test at phone and full size. About 7%; then replaces `_cover` and the separate drawings.
3. Only after Sam's Y: into shot 4, camera and beats untouched; added to the kit catalogue.
4. **Its own proposal:** a lock on the house look; a hand-style change is refused unless it quotes Sam from the ledger.

Total about 14.5%, one-off, against roughly 40-50% spent on patches. Sam sees two clips, grey then drawn.

Question: 1. Test space uses circle hands, as before chat 28 (Y/N).

## Sam test
- Q1: Fixes how hiding is decided; learns outside the film.
- Q2: Every showstopper; whole record since v4.
- Q3: Causes 1-4; scripts measure bars; Sam's Y between.
- Q4: Five approaches; B, C remove causes.
- Q5: Stages undo alone; shot 4 untouched till clips pass.
- Q6: Sources named; cost, speed measured in L1-L2.
- Q7: Bars are 0 faults and Sam's eye.
- Q8: Bench and render are permanent kit.

## Lost / Added
- Lost: fingered hands; `_cover` and the separate drawings for this move (after stage 2).
- Added: a test bench, an in-house single-pass drawing method, a reference step for moves.

## Unchecked
Shot 4's cost share; Blender headless; in-house speed; whether the car has a closed 3D shape; suitable reference or CMU data.
