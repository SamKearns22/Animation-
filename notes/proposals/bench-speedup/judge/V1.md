# Helper B: bench speed-up

## Leak
The problem file lists remedies (Sam's Y list: distance grid, compiled fill, head once, 4 at a time, saved fits, checks first, splice, keep frames). Weighed below as candidates, not taken as given.

## Results
- Grey frame ~15 s, of which the fold press is 10.1 s. One inside test costs ~2 s, so the press is mostly inside tests. Start-up ~73 s every run (learn-step.md, chats 38-39).
- Dressed still 105 s, of which 65 s is the three fits re-run. The fits give fixed numbers and are never saved (learn-step.md chat 39; bench_move.py `fit_*`).
- Full grey run: 51 min (chat 35). Middle clip: 2,908 s for 131 frames, about 22 s a frame (chat 38).
- **Slowness let a fault through.** The get-up was never checked with the real checks, because chat 37 skipped span.py. Chat 39 then found it broken (legs through each other 12 cm, pistol 4.4 cm). Chat 39 also skipped the full run (~80 min) (learn-step.md chat 39).
- Waiting on renders is 2-11% of a bench chat's cost. Start-up floor plus Claude's words are 40-80% (ledger, "cost by kind" and "origins" for chats 1ca55da5 to 48615624). So speed mostly buys **chances to check** and **turns within one chat**, not tokens.
- The bench chats (33-39) cost about 13.4% of a week. The film stands at 82.55% against an estimate of 53.2% (ledger). The row-to-chat matching is unchecked.
- The record cannot yet say: how many inside tests one frame makes, how busy the 4 processors are during a frame, how large a frame bundle would be.

## The real decision
How the move gets checked in full after every fix, and seen dressed, without a chat ever skipping a gate because it is slow. The unit is the whole bench loop across chats, not one frame. Bigger levers than per-frame speed: (1) making only the frames a change touches, (2) the exact cost of the inside test. "No notes" itself also needs the get-up re-plan and the look faults. Speed does not fix those; it makes them affordable to check.

## Root cause
1. The inside test checks each point against all 20,304 triangles, and it is called up to 19 times a frame (press 8 rounds, settle 10, self_cross 1).
2. Nothing is remembered. Fits are re-run each run. Frames are lost each chat. Nothing records which frames a change touched, so every fix re-makes all 197.
3. **The distance-grid idea would gain almost nothing.** Every inside query sits 1.5 or 3 mm off the skin (`_inside2`: Q + N·0.003). "Exact test near the skin" would therefore run the exact test on nearly every point.

## Approaches weighed
A. Per-frame tuning: Sam's list as given. The grid fails (root cause 3). "4 at a time" helps little on grey frames, because the inside test already uses all 4 processors (inference, unchecked).
B. Reframe: a **frame store**. Each frame is filed under a fingerprint of what made it (its goals, the solver and drawing code, the fit numbers). A run checks every frame first, then makes only the frames whose fingerprint changed. The store is kept on GitHub as one bundle.
C. Learn-first, then an **exact faster inside test**. A hierarchical winding number (Jacobson 2013; libigl's WindingNumberAABB) groups distant triangles and counts each group by its edge outline instead. The answer is mathematically the same, with no approximation.
D. A bigger machine. None is offered (chat 38). Rejected.
E. Better skinning so folds never cross, removing the need for the press. This changes drawn pixels, which is outside the brief. Rejected here.
**Chosen: learning step first, then B and C's pieces, one change at a time.**

## Proposal
**L0, learning only (changes nothing, ~0.4%).**
- Profile 30 golden frames (keys, 13-23, the middle, 176-190, and the proof frames): inside tests per frame, seconds per test, processor use, drawing parts, PNG sizes.
- Save their skin points, check numbers and picture fingerprints as the **sameness bar**.
- Count the open edges of the body mesh (it should be open only at the wrists).
- Try installing libigl.

**Then one change at a time.** Each one is kept only if the sameness bar passes: identical check numbers and identical pixels on all 30 frames, and proof.txt reproduced.
1. **Saved fits** (~0.2%). The fits are filed under a fingerprint of the body, keys and car, and redone automatically when any of these changes. Bar: start-up 73 s down to 5 s or less, with the same fit numbers.
2. **Exact inside test** (~1.0%; +0.5% if libigl will not install and our own version is needed). Bar: under 0.2 s a test, 0 verdicts different from the old test over all 197 frames' check log, grey frame 15 s down to 6 s or less.
3. **Frame store, checks first, splice** (~0.6%).
   - Built into `run`/`clip`, so a chat cannot skip it.
   - Before any send, 10 reused frames picked at random are re-made and must match exactly; otherwise the store is wiped.
   - The bundle stays under 50 MB.
   - Bar: a one-span fix re-makes only that span.
4. **Compiled fill and head drawn once** (~0.4%). Bar: identical pixels; dressed drawing 16 s down to 6 s or less.
5. **4 at a time**: only if L0 shows the processors idle more than 30% of a frame; otherwise dropped, with a "Lost:" line.

**Cost:** ~2.6-3.1% of a week, an estimate, unchecked. The film is already far past 15%, and this will not bring it back. Its return is every fix fully checked within one chat.

**What Sam would notice:** clips sooner after each note. No grey or dressed frame ever looks different because of this work.

## Sam test
Q1 Expert: an expert measures first, caches by fingerprint, and uses the standard exact method. That is this plan.
Q2 Best result: the scope is the whole bench loop. The evidence is chats 35-39 and the ledger.
Q3 Comprehensive: the root cause is named. The guards live inside the run, not in a note a chat must read and choose to follow.
Q4 Most intelligent: five different approaches were weighed; the grid was dropped with a reason.
Q5 Risk: each change is undone on its own. Store errors are caught by the random re-make.
Q6 Checked: sources are named; gaps are marked.
Q7 Not cheap: exactness is required, not "close enough".
Q8 Nothing temporary: each change is permanent once it passes, and is reviewed when the film ends.

## Lost / Added
Lost: the distance grid, and possibly "4 at a time".
Added: a sameness bar, saved fits, a frame store with a guard, a faster exact inside test, compiled drawing.

## Unchecked
- Ledger rows matched to chat numbers.
- Inside tests per frame and processor use.
- That the mesh is open only at the wrists.
- That libigl installs here.
- Bundle size and how fast it grows the repository's history.
- All speed and cost estimates.
